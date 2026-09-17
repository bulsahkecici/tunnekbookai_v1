from __future__ import annotations

import unittest
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tunnelbookai.ingest.acceleration import (
    OCR_ACCELERATOR_ENV,
    rapidocr_torch_params,
    resolve_accelerator,
    resolve_ocr_accelerator,
)
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.docling_adapter import build_pdf_options, convert
from tunnelbookai.ingest.ocr.provider import OcrProvider, ocr_figures
from tunnelbookai.ingest.vision.provider import describe_figures


class AcceleratorSelectionTests(unittest.TestCase):
    def test_auto_prefers_mps_when_available(self):
        config = SimpleNamespace(ocr={"accelerator": "auto"})
        with mock.patch(
            "tunnelbookai.ingest.acceleration._torch_device_available",
            side_effect=lambda device: device == "mps",
        ):
            selected = resolve_accelerator(config)
        self.assertEqual(selected.resolved, "mps")
        self.assertEqual(selected.reason, "auto_selected_mps")

    def test_unavailable_explicit_mps_falls_back_to_cpu(self):
        config = SimpleNamespace(ocr={"accelerator": "mps"})
        with mock.patch(
            "tunnelbookai.ingest.acceleration._torch_device_available", return_value=False
        ):
            selected = resolve_accelerator(config)
        self.assertEqual(selected.resolved, "cpu")
        self.assertEqual(selected.reason, "mps_unavailable_cpu_fallback")

    def test_rapidocr_flags_are_mutually_exclusive(self):
        self.assertEqual(
            rapidocr_torch_params("mps"),
            {"EngineConfig.torch.use_cuda": False, "EngineConfig.torch.use_mps": True},
        )

    def test_rapidocr_defaults_to_cpu_for_long_run_stability(self):
        config = SimpleNamespace(ocr={"accelerator": "auto"})
        with mock.patch.dict("os.environ", {}, clear=True):
            selected = resolve_ocr_accelerator(config)
        self.assertEqual(selected.resolved, "cpu")
        self.assertEqual(selected.reason, "rapidocr_stability_default")

    def test_rapidocr_mps_can_be_explicitly_enabled(self):
        config = SimpleNamespace(ocr={})
        with (
            mock.patch.dict("os.environ", {OCR_ACCELERATOR_ENV: "mps"}, clear=True),
            mock.patch(
                "tunnelbookai.ingest.acceleration._torch_device_available",
                return_value=True,
            ),
        ):
            selected = resolve_ocr_accelerator(config)
        self.assertEqual(selected.resolved, "mps")
        self.assertEqual(selected.reason, "explicit_selection")


class OpenCvArmResizeRegressionTests(unittest.TestCase):
    def test_rapidocr_near_unity_rgb_resize_does_not_segfault(self):
        """OpenCV 4.14/5.0 + KleidiCV 26.03 crashes here on ARM64."""
        code = (
            "import cv2, numpy as np; "
            "out=cv2.resize(np.zeros((2598,1736,3),np.uint8),(1728,2592)); "
            "assert out.shape == (2592,1728,3)"
        )
        completed = subprocess.run(
            [sys.executable, "-c", code], capture_output=True, text=True, timeout=30
        )
        self.assertEqual(
            completed.returncode,
            0,
            f"OpenCV resize subprocess crashed: {completed.stderr}",
        )


class DoclingAccelerationTests(unittest.TestCase):
    def test_mps_is_applied_to_docling_but_rapidocr_stays_on_cpu(self):
        with mock.patch(
            "tunnelbookai.ingest.docling_adapter.resolve_accelerator"
        ) as resolve:
            resolve.return_value = SimpleNamespace(
                requested="auto", resolved="mps", reason="auto_selected_mps"
            )
            options, applied, unsupported = build_pdf_options(load_config(), do_ocr=True)

        self.assertEqual(str(options.accelerator_options.device), "mps")
        self.assertFalse(options.ocr_options.rapidocr_params["EngineConfig.torch.use_mps"])
        self.assertEqual(applied["accelerator_device"], "mps")
        self.assertEqual(applied["ocr_accelerator_device"], "cpu")
        self.assertEqual(applied["ocr_accelerator_reason"], "rapidocr_stability_default")
        self.assertNotIn("accelerator_options", unsupported)

    def test_docling_runtime_failure_retries_on_cpu(self):
        selected = SimpleNamespace(
            requested="auto", resolved="mps", reason="auto_selected_mps"
        )
        first_converter = mock.Mock()
        first_converter.convert.side_effect = RuntimeError("unsupported MPS operation")
        document = SimpleNamespace(
            texts=[], tables=[], pictures=[],
            export_to_markdown=lambda: "fallback text",
            export_to_text=lambda: "fallback text",
            export_to_dict=lambda: {"text": "fallback text"},
        )
        second_converter = mock.Mock()
        second_converter.convert.return_value = SimpleNamespace(
            status=SimpleNamespace(name="SUCCESS"), errors=[], document=document
        )

        with (
            mock.patch(
                "tunnelbookai.ingest.docling_adapter.resolve_accelerator",
                return_value=selected,
            ),
            mock.patch(
                "docling.document_converter.DocumentConverter",
                side_effect=[first_converter, second_converter],
            ),
        ):
            result = convert(
                Path("sample.pdf"),
                load_config(),
                input_format="PDF",
            )

        self.assertEqual(result.status, "SUCCESS")
        self.assertEqual(result.markdown, "fallback text")
        self.assertEqual(result.applied_options["accelerator_device"], "cpu")
        self.assertTrue(
            any(
                value.startswith("note:accelerator_cpu_fallback_after:")
                for value in result.unsupported_options
            )
        )

    def test_converter_is_reused_for_identical_options(self):
        document = SimpleNamespace(
            texts=[], tables=[], pictures=[],
            export_to_markdown=lambda: "cached text",
            export_to_text=lambda: "cached text",
            export_to_dict=lambda: {"text": "cached text"},
        )
        converter = mock.Mock()
        converter.convert.return_value = SimpleNamespace(
            status=SimpleNamespace(name="SUCCESS"), errors=[], document=document
        )
        constructor = mock.Mock(return_value=converter)

        with mock.patch("docling.document_converter.DocumentConverter", constructor):
            first = convert(Path("first.docx"), load_config(), input_format="DOCX", do_ocr=False)
            second = convert(Path("second.docx"), load_config(), input_format="DOCX", do_ocr=False)

        self.assertEqual(constructor.call_count, 1)
        self.assertEqual(first.applied_options["converter_cache"], "created")
        self.assertEqual(second.applied_options["converter_cache"], "reused")


class OcrProviderAccelerationTests(unittest.TestCase):
    def test_provider_uses_stable_cpu_default(self):
        config = SimpleNamespace(ocr={"engine": "rapidocr", "engine_type": "torch"})
        selected = SimpleNamespace(
            requested="cpu", resolved="cpu", reason="rapidocr_stability_default"
        )
        with mock.patch(
            "tunnelbookai.ingest.ocr.provider.resolve_ocr_accelerator", return_value=selected
        ):
            provider = OcrProvider(config)
        fake_engine = mock.Mock()
        with mock.patch("rapidocr.RapidOCR", return_value=fake_engine) as constructor:
            self.assertIs(provider._load(), fake_engine)

        params = constructor.call_args.kwargs["params"]
        self.assertFalse(params["EngineConfig.torch.use_mps"])
        self.assertFalse(params["EngineConfig.torch.use_cuda"])
        self.assertEqual(provider.engine_id(), "rapidocr_torch_cpu")

    def test_runtime_mps_failure_retries_on_cpu(self):
        config = SimpleNamespace(ocr={"engine": "rapidocr", "engine_type": "torch"})
        selected = SimpleNamespace(
            requested="auto", resolved="mps", reason="auto_selected_mps"
        )
        with mock.patch(
            "tunnelbookai.ingest.ocr.provider.resolve_ocr_accelerator", return_value=selected
        ):
            provider = OcrProvider(config)

        mps_engine = mock.Mock(side_effect=RuntimeError("unsupported MPS operation"))
        cpu_result = SimpleNamespace(txts=["fallback text"])
        cpu_engine = mock.Mock(return_value=cpu_result)
        with mock.patch.object(
            provider, "_create_engine", side_effect=[mps_engine, cpu_engine]
        ):
            raw, error = provider._invoke("image.png")

        self.assertIsNone(error)
        self.assertIs(raw, cpu_result)
        self.assertEqual(provider.device, "cpu")
        self.assertEqual(provider.accelerator_reason, "mps_runtime_failed_cpu_fallback")


class RepeatedFigureCacheTests(unittest.TestCase):
    def test_identical_pixels_are_ocred_once(self):
        run_image = mock.Mock(return_value={
            "ocr_status": "SUCCESS", "ocr_engine": "test", "ocr_languages": ["tr"],
            "ocr_text": "Tünel", "ocr_confidence": None,
        })
        provider = SimpleNamespace(figure_ocr_enabled=True, run_image=run_image)
        figures = [
            {"asset_id": "FIG0001", "path": "tests/ingest/fixtures/_embedded.png", "pixel_digest": "same"},
            {"asset_id": "FIG0002", "path": "tests/ingest/fixtures/_embedded.png", "pixel_digest": "same"},
        ]
        ocr_figures(provider, figures, Path.cwd())
        self.assertEqual(run_image.call_count, 1)
        self.assertFalse(figures[0]["ocr_cache_hit"])
        self.assertTrue(figures[1]["ocr_cache_hit"])
        self.assertEqual(figures[1]["ocr_text"], "Tünel")

    def test_identical_pixels_are_described_once(self):
        describe = mock.Mock(return_value={
            "visual_description_status": "SUCCESS", "visual_description": "Kesit",
            "provider": "test", "model": "test-vlm",
        })
        provider = SimpleNamespace(available=lambda: True, describe=describe)
        figures = [
            {"asset_id": "FIG0001", "path": "tests/ingest/fixtures/_embedded.png", "pixel_digest": "same"},
            {"asset_id": "FIG0002", "path": "tests/ingest/fixtures/_embedded.png", "pixel_digest": "same"},
        ]
        describe_figures(provider, figures, Path.cwd())
        self.assertEqual(describe.call_count, 1)
        self.assertFalse(figures[0]["vision_cache_hit"])
        self.assertTrue(figures[1]["vision_cache_hit"])
        self.assertEqual(figures[1]["visual_description"], "Kesit")

    def test_tiny_icons_skip_both_expensive_models(self):
        run_image = mock.Mock()
        ocr = SimpleNamespace(
            figure_ocr_enabled=True,
            run_image=run_image,
            engine_id=lambda: "test",
            languages=["tr"],
        )
        describe = mock.Mock()
        vision = SimpleNamespace(
            name="test", model="test-vlm", available=lambda: True, describe=describe
        )
        figure = {
            "asset_id": "FIG0001", "path": "tests/ingest/fixtures/_embedded.png",
            "pixel_digest": "tiny", "width": 20, "height": 20,
        }

        ocr_figures(ocr, [figure], Path.cwd())
        describe_figures(vision, [figure], Path.cwd())

        run_image.assert_not_called()
        describe.assert_not_called()
        self.assertEqual(figure["ocr_status"], "SKIPPED_TOO_SMALL")
        self.assertEqual(figure["vision_skip_reason"], "TOO_SMALL")


if __name__ == "__main__":
    unittest.main()
