"""OfficeRenderer: detection, DOCX/PPTX/XLSX snapshots, degradation, subprocess safety.

Task §16 and §17. Every test that needs a real conversion skips when LibreOffice is absent,
so the suite stays green on a machine without it; the degradation tests run everywhere
because they mock the binary away.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tunnelbookai.ingest.office_renderer import (
    VISUAL_RENDERER_UNAVAILABLE, OfficeRenderer, find_libreoffice,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HAVE_LIBREOFFICE = find_libreoffice() is not None
NEEDS_LIBREOFFICE = unittest.skipUnless(HAVE_LIBREOFFICE, "LibreOffice is not installed")


class DetectionTests(unittest.TestCase):
    """§3, §16 — one locator, reused; no duplicate implementation."""

    def test_locator_returns_an_existing_executable_or_none(self):
        found = find_libreoffice()
        if found is None:
            self.skipTest("LibreOffice is not installed")
        self.assertTrue(found.exists())
        self.assertTrue(found.is_file())

    def test_renderer_availability_tracks_the_locator(self):
        renderer = OfficeRenderer()
        self.assertEqual(renderer.available(), find_libreoffice() is not None)
        self.assertEqual(renderer.backend, "libreoffice" if renderer.available() else None)

    @NEEDS_LIBREOFFICE
    def test_detected_binary_reports_a_version(self):
        proc = subprocess.run([str(find_libreoffice()), "--version"], capture_output=True,
                              text=True, timeout=120, check=False)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("LibreOffice", proc.stdout)


class RendererUnavailableTests(unittest.TestCase):
    """§16 — graceful degradation: a warning, never an exception and never a rejection."""

    def setUp(self):
        with mock.patch("tunnelbookai.ingest.office_renderer.find_libreoffice", return_value=None):
            self.renderer = OfficeRenderer()

    def test_reports_itself_unavailable(self):
        self.assertFalse(self.renderer.available())
        self.assertIsNone(self.renderer.backend)

    def test_render_to_pdf_warns_and_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdf, warnings = self.renderer.render_to_pdf(FIXTURES / "sample.docx", Path(tmp))
            self.assertIsNone(pdf)
            self.assertEqual(warnings, [VISUAL_RENDERER_UNAVAILABLE])

    def test_render_pages_warns_and_returns_no_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            records, warnings = self.renderer.render_pages(
                FIXTURES / "sample.pptx", Path(tmp) / "bundle", document_id="DOC000001")
            self.assertEqual(records, [])
            self.assertEqual(warnings, [VISUAL_RENDERER_UNAVAILABLE])

    def test_no_subprocess_is_launched_when_unavailable(self):
        with mock.patch("tunnelbookai.ingest.office_renderer.subprocess.run") as run:
            with tempfile.TemporaryDirectory() as tmp:
                self.renderer.render_to_pdf(FIXTURES / "sample.docx", Path(tmp))
        run.assert_not_called()


class RendererFailureTests(unittest.TestCase):
    """§16 — a present-but-failing renderer degrades to a warning too."""

    def test_timeout_is_reported_as_a_warning(self):
        renderer = OfficeRenderer(timeout_seconds=1)
        renderer._binary = Path("/bin/echo")  # present, so `available()` is True
        with mock.patch("tunnelbookai.ingest.office_renderer.subprocess.run",
                        side_effect=subprocess.TimeoutExpired(cmd="soffice", timeout=1)):
            with tempfile.TemporaryDirectory() as tmp:
                pdf, warnings = renderer.render_to_pdf(FIXTURES / "sample.docx", Path(tmp))
        self.assertIsNone(pdf)
        self.assertEqual(warnings, ["OFFICE_RENDER_TIMEOUT"])

    def test_producing_no_pdf_is_reported_as_a_warning(self):
        renderer = OfficeRenderer()
        renderer._binary = Path("/bin/echo")
        with tempfile.TemporaryDirectory() as tmp:
            pdf, warnings = renderer.render_to_pdf(FIXTURES / "sample.docx", Path(tmp))
        self.assertIsNone(pdf)
        self.assertEqual(len(warnings), 1)
        self.assertTrue(warnings[0].startswith("OFFICE_RENDER_NO_OUTPUT"))

    def test_xls_conversion_timeout_is_reported(self):
        renderer = OfficeRenderer(timeout_seconds=1)
        renderer._binary = Path("/bin/echo")
        with mock.patch(
            "tunnelbookai.ingest.office_renderer.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="soffice", timeout=1),
        ):
            with tempfile.TemporaryDirectory() as tmp:
                converted, warnings = renderer.convert_to_xlsx(
                    Path(tmp) / "legacy.xls", Path(tmp) / "out"
                )
        self.assertIsNone(converted)
        self.assertEqual(warnings, ["XLS_CONVERSION_TIMEOUT"])

    def test_ppt_conversion_timeout_is_reported(self):
        renderer = OfficeRenderer(timeout_seconds=1)
        renderer._binary = Path("/bin/echo")
        with mock.patch(
            "tunnelbookai.ingest.office_renderer.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="soffice", timeout=1),
        ):
            with tempfile.TemporaryDirectory() as tmp:
                converted, warnings = renderer.convert_to_pptx(
                    Path(tmp) / "legacy.ppt", Path(tmp) / "out"
                )
        self.assertIsNone(converted)
        self.assertEqual(warnings, ["PPT_CONVERSION_TIMEOUT"])


class SubprocessSafetyTests(unittest.TestCase):
    """§17 — argument array, no shell, isolated profile, timeout, stderr captured."""

    def captured_call(self, source: Path, out_dir: Path):
        renderer = OfficeRenderer(timeout_seconds=42)
        renderer._binary = Path("/bin/echo")
        with mock.patch("tunnelbookai.ingest.office_renderer.subprocess.run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, "", "")
            renderer.render_to_pdf(source, out_dir)
        self.assertEqual(run.call_count, 1)
        return run.call_args

    def test_command_is_an_argument_array_and_never_uses_a_shell(self):
        with tempfile.TemporaryDirectory() as tmp:
            args, kwargs = self.captured_call(FIXTURES / "sample.docx", Path(tmp) / "out")
        command = args[0]
        self.assertIsInstance(command, list)
        self.assertTrue(all(isinstance(part, str) for part in command))
        self.assertNotIn("shell", kwargs)
        self.assertFalse(kwargs.get("shell", False))

    def test_timeout_and_stderr_capture_are_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, kwargs = self.captured_call(FIXTURES / "sample.docx", Path(tmp) / "out")
        self.assertEqual(kwargs["timeout"], 42)
        self.assertTrue(kwargs["capture_output"])
        self.assertFalse(kwargs["check"])

    def test_an_isolated_user_profile_is_requested_as_a_valid_uri(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "out (arşiv) ışık"
            args, _ = self.captured_call(FIXTURES / "sample.docx", out_dir)
        profile = next(part for part in args[0] if part.startswith("-env:UserInstallation="))
        value = profile.split("=", 1)[1]
        self.assertTrue(value.startswith("file:///"))
        # a raw path here would produce a malformed URL and abort LibreOffice
        self.assertNotIn(" ", value)
        self.assertNotIn("ı", value)
        self.assertTrue(value.endswith("_lo_profile"))

    def test_source_is_passed_as_an_absolute_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            args, _ = self.captured_call(FIXTURES / "sample.docx", Path(tmp) / "out")
        self.assertTrue(Path(args[0][-1]).is_absolute())
        self.assertFalse(args[0][-1].startswith("-"))

    def test_xls_conversion_uses_argument_array_and_isolated_profile(self):
        renderer = OfficeRenderer(timeout_seconds=42)
        renderer._binary = Path("/bin/echo")
        with mock.patch("tunnelbookai.ingest.office_renderer.subprocess.run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, "", "")
            with tempfile.TemporaryDirectory() as tmp:
                renderer.convert_to_xlsx(Path(tmp) / "legacy.xls", Path(tmp) / "out")
        command = run.call_args.args[0]
        kwargs = run.call_args.kwargs
        self.assertIsInstance(command, list)
        self.assertIn("xlsx", command)
        self.assertTrue(any(p.startswith("-env:UserInstallation=file:///") for p in command))
        self.assertFalse(kwargs.get("shell", False))

    def test_ppt_conversion_uses_argument_array_and_isolated_profile(self):
        renderer = OfficeRenderer(timeout_seconds=42)
        renderer._binary = Path("/bin/echo")
        with mock.patch("tunnelbookai.ingest.office_renderer.subprocess.run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, "", "")
            with tempfile.TemporaryDirectory() as tmp:
                renderer.convert_to_pptx(Path(tmp) / "legacy.ppt", Path(tmp) / "out")
        command = run.call_args.args[0]
        kwargs = run.call_args.kwargs
        self.assertIsInstance(command, list)
        self.assertIn("pptx", command)
        self.assertTrue(any(p.startswith("-env:UserInstallation=file:///") for p in command))
        self.assertFalse(kwargs.get("shell", False))


class SnapshotHarness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.renderer = OfficeRenderer()

    def snapshots(self, fixture: str, **kwargs):
        tmp = tempfile.TemporaryDirectory(prefix="tbai_office_test_")
        self.addCleanup(tmp.cleanup)
        bundle = Path(tmp.name) / "bundle"
        records, warnings = self.renderer.render_pages(
            FIXTURES / fixture, bundle, document_id="DOC000001", **kwargs)
        return records, warnings, bundle

    def assertValidSnapshots(self, records, warnings, bundle, *, minimum: int):
        self.assertEqual(warnings, [])
        self.assertGreaterEqual(len(records), minimum)
        for record in records:
            path = Path(record["path"])
            if not path.is_absolute():
                path = Path(__file__).resolve().parents[2] / path
            with self.subTest(asset=record.get("asset_id")):
                self.assertTrue(path.is_file(), f"snapshot missing: {path}")
                payload = path.read_bytes()
                self.assertTrue(payload.startswith(b"\x89PNG\r\n\x1a\n"), "not a valid PNG")
                self.assertGreater(len(payload), 1000)
                # §7 — provenance is recorded, and the digest matches the bytes on disk
                self.assertEqual(record["renderer"], "libreoffice+pypdfium2")
                self.assertEqual(record["derived_from"], "temporary_rendered_pdf")
                if record.get("sha256"):
                    self.assertEqual(record["sha256"], hashlib.sha256(payload).hexdigest())


@NEEDS_LIBREOFFICE
class DocxSnapshotTests(SnapshotHarness):
    def test_docx_renders_page_snapshots(self):
        records, warnings, bundle = self.snapshots("sample.docx", kind="PAGE", id_prefix="PAGE")
        self.assertValidSnapshots(records, warnings, bundle, minimum=1)
        self.assertEqual([r["asset_id"] for r in records][:1], ["PAGE0001"])

    def test_original_docx_is_not_modified(self):
        source = FIXTURES / "sample.docx"
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        self.snapshots("sample.docx")
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)


@NEEDS_LIBREOFFICE
class PptxSnapshotTests(SnapshotHarness):
    def test_pptx_renders_one_snapshot_per_slide(self):
        records, warnings, bundle = self.snapshots(
            "sample.pptx", dirname="slides", prefix="slide", kind="SLIDE", id_prefix="SLIDE")
        self.assertValidSnapshots(records, warnings, bundle, minimum=2)
        self.assertEqual([r["asset_id"] for r in records], ["SLIDE0001", "SLIDE0002"])


@NEEDS_LIBREOFFICE
class XlsxSnapshotTests(SnapshotHarness):
    def test_xlsx_renders_sheet_page_snapshots(self):
        records, warnings, bundle = self.snapshots(
            "sample.xlsx", dirname="sheets", prefix="sheet", kind="SHEET", id_prefix="SHEET")
        self.assertValidSnapshots(records, warnings, bundle, minimum=1)


@NEEDS_LIBREOFFICE
class TemporaryPdfTests(unittest.TestCase):
    """§7 — the rendered PDF is derived data: produced, used, then gone."""

    def test_render_to_pdf_produces_a_real_pdf(self):
        renderer = OfficeRenderer()
        with tempfile.TemporaryDirectory() as tmp:
            pdf, warnings = renderer.render_to_pdf(FIXTURES / "sample.docx", Path(tmp) / "out")
            self.assertEqual(warnings, [])
            self.assertIsNotNone(pdf)
            self.assertTrue(pdf.is_file())
            self.assertTrue(pdf.read_bytes().startswith(b"%PDF-"))

    def test_render_pages_leaves_no_pdf_behind_in_the_bundle(self):
        renderer = OfficeRenderer()
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "bundle"
            records, warnings = renderer.render_pages(
                FIXTURES / "sample.docx", bundle, document_id="DOC000001")
            self.assertEqual(warnings, [])
            self.assertTrue(records)
            self.assertEqual(list(bundle.rglob("*.pdf")), [])
            self.assertEqual(list(bundle.rglob("_lo_profile")), [])


@NEEDS_LIBREOFFICE
class HostilePathTests(unittest.TestCase):
    """§17 — spaces, Turkish characters and parentheses, in both file and directory names."""

    CASES = [
        "ovit tuneli raporu.docx",
        "ışık İSTANBUL şğüöç.docx",
        "rapor (final) v2.docx",
        "Tünel Bakımı (2024) ölçüm şeması.docx",
    ]

    def test_hostile_source_and_output_paths_render(self):
        renderer = OfficeRenderer()
        for name in self.CASES:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                source_dir = Path(tmp) / "kaynak (arşiv) ışık"
                source_dir.mkdir(parents=True)
                source = source_dir / name
                shutil.copy(FIXTURES / "sample.docx", source)
                records, warnings = renderer.render_pages(
                    source, Path(tmp) / "bundle (çıktı)", document_id="DOC000001")
                self.assertEqual(warnings, [], f"failed for {name}")
                self.assertGreaterEqual(len(records), 1)

    def test_hostile_output_directory_alone_renders(self):
        renderer = OfficeRenderer()
        for directory in ["out (ışık) dir", "İSTANBUL şğüöç (2)", "a b c"]:
            with self.subTest(directory=directory), tempfile.TemporaryDirectory() as tmp:
                pdf, warnings = renderer.render_to_pdf(
                    FIXTURES / "sample.docx", Path(tmp) / directory)
                self.assertEqual(warnings, [], f"failed for {directory}")
                self.assertIsNotNone(pdf)


if __name__ == "__main__":
    unittest.main()
