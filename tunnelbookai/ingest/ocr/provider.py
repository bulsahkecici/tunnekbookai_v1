"""Local OCR provider (task §23, §24, §25).

Local engines only — there is no network path in this module (§26, §80). RapidOCR (torch
backend) is the preferred engine, matching the existing `scripts/03_convert.py` setup so the
two pipelines produce comparable text.

Contract per OCR run:

    {"ocr_status", "ocr_engine", "ocr_languages", "ocr_text", "ocr_confidence"}

`ocr_confidence` is null unless the engine returns a calibrated score — RapidOCR does not,
so we never fabricate one (§23). `ocr_text` is NEVER written into `visual_description` (§24).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

SUCCESS = "SUCCESS"
EMPTY = "EMPTY"
SKIPPED_PHOTOGRAPHIC = "SKIPPED_PHOTOGRAPHIC"
DISABLED = "DISABLED"
NOT_RUN = "NOT_RUN"
FAILED = "FAILED"
ENGINE_UNAVAILABLE = "ENGINE_UNAVAILABLE"


def empty_result(status: str = NOT_RUN, engine: str | None = None,
                 languages: list[str] | None = None) -> dict[str, Any]:
    return {
        "ocr_status": status,
        "ocr_engine": engine,
        "ocr_languages": list(languages or []),
        "ocr_text": None,
        "ocr_confidence": None,
    }


def looks_photographic(path: Path, min_edge_density: float = 0.02) -> bool:
    """Cheap gate to skip OCR on obviously photographic assets (§25).

    Text-bearing images have a high proportion of hard edges and a small colour palette;
    photographs have smooth gradients. Conservative: on any doubt we return False and OCR runs.
    """
    try:
        from PIL import Image, ImageFilter
    except ImportError:
        return False
    try:
        with Image.open(path) as image:
            grey = image.convert("L")
            if min(grey.size) < 16:
                return False
            grey.thumbnail((512, 512))
            edges = grey.filter(ImageFilter.FIND_EDGES)
            histogram = edges.histogram()
            total = sum(histogram) or 1
            strong = sum(histogram[64:])
            density = strong / total
            colours = grey.getcolors(maxcolors=256)
    except Exception:
        return False
    # few distinct grey levels + low edge density => smooth photo, not a text raster
    if density >= min_edge_density:
        return False
    return colours is None or len(colours) > 32


class OcrProvider:
    """Wraps one local OCR engine. `available()` never raises; failures degrade to status."""

    def __init__(self, config: Any, *, enabled: bool = True) -> None:
        ocr_cfg = getattr(config, "ocr", {}) or {}
        self.config = ocr_cfg
        self.engine_name = str(ocr_cfg.get("engine", "rapidocr")).lower()
        self.engine_type = str(ocr_cfg.get("engine_type", "torch")).lower()
        self.languages = list(ocr_cfg.get("languages", ["tr", "en"]))
        self.enabled = bool(enabled) and bool(ocr_cfg.get("enabled", True))
        self._engine: Any = None
        self._load_error: str | None = None
        presence = ocr_cfg.get("text_presence_detection", {}) or {}
        self.presence_enabled = bool(presence.get("enabled", True))
        self.min_edge_density = float(presence.get("min_edge_density", 0.02))
        figure_cfg = ocr_cfg.get("figure_ocr", {}) or {}
        self.figure_ocr_enabled = bool(figure_cfg.get("enabled", True))
        self.skip_photographic = bool(figure_cfg.get("skip_photographic", True))

    # ------------------------------------------------------------------ engine
    def _load(self) -> Any:
        if self._engine is not None or self._load_error is not None:
            return self._engine
        if self.engine_name != "rapidocr":
            self._load_error = f"unsupported_engine:{self.engine_name}"
            return None
        try:
            from rapidocr import RapidOCR
            from rapidocr.utils.typings import EngineType

            engine_type = EngineType.TORCH if self.engine_type == "torch" else EngineType.ONNXRUNTIME
            self._engine = RapidOCR(params={
                "Det.engine_type": engine_type,
                "Cls.engine_type": engine_type,
                "Rec.engine_type": engine_type,
            })
        except Exception as exc:
            self._load_error = f"{type(exc).__name__}: {exc}"
            self._engine = None
        return self._engine

    def available(self) -> bool:
        if not self.enabled:
            return False
        return self._load() is not None

    def engine_id(self) -> str:
        return f"{self.engine_name}_{self.engine_type}"

    # ------------------------------------------------------------------- runs
    def run_image(self, path: Path, *, allow_photographic_skip: bool = True) -> dict[str, Any]:
        if not self.enabled:
            return empty_result(DISABLED, None, self.languages)
        path = Path(path)
        if not path.is_file():
            return empty_result(FAILED, self.engine_id(), self.languages)
        if (allow_photographic_skip and self.presence_enabled and self.skip_photographic
                and looks_photographic(path, self.min_edge_density)):
            return empty_result(SKIPPED_PHOTOGRAPHIC, self.engine_id(), self.languages)
        engine = self._load()
        if engine is None:
            result = empty_result(ENGINE_UNAVAILABLE, self.engine_id(), self.languages)
            result["ocr_error"] = self._load_error
            return result
        try:
            raw = engine(str(path))
        except Exception as exc:
            result = empty_result(FAILED, self.engine_id(), self.languages)
            result["ocr_error"] = f"{type(exc).__name__}: {exc}"
            return result
        return self._from_raw(raw)

    def run_pil(self, image: Any) -> dict[str, Any]:
        if not self.enabled:
            return empty_result(DISABLED, None, self.languages)
        engine = self._load()
        if engine is None:
            result = empty_result(ENGINE_UNAVAILABLE, self.engine_id(), self.languages)
            result["ocr_error"] = self._load_error
            return result
        try:
            import numpy as np

            raw = engine(np.asarray(image.convert("RGB")))
        except Exception as exc:
            result = empty_result(FAILED, self.engine_id(), self.languages)
            result["ocr_error"] = f"{type(exc).__name__}: {exc}"
            return result
        return self._from_raw(raw)

    def _from_raw(self, raw: Any) -> dict[str, Any]:
        texts = [t.strip() for t in (getattr(raw, "txts", None) or []) if t and str(t).strip()]
        result = empty_result(SUCCESS if texts else EMPTY, self.engine_id(), self.languages)
        result["ocr_text"] = "\n".join(texts) if texts else None
        # RapidOCR exposes per-box scores but no calibrated document confidence (§23).
        result["ocr_confidence"] = None
        return result


def ocr_figures(provider: OcrProvider, figures: list[dict[str, Any]],
                root: Path) -> list[str]:
    """Attach OCR to extracted figures in place (§25). Returns warnings."""
    warnings: list[str] = []
    if not provider.figure_ocr_enabled:
        return warnings
    for figure in figures:
        rel = figure.get("path")
        if not rel:
            continue
        path = root / rel if not Path(rel).is_absolute() else Path(rel)
        if not path.is_file():
            continue
        result = provider.run_image(path)
        figure["ocr_status"] = result["ocr_status"]
        figure["ocr_engine"] = result["ocr_engine"]
        figure["ocr_languages"] = result["ocr_languages"]
        figure["ocr_text"] = result["ocr_text"]
        figure["ocr_confidence"] = result["ocr_confidence"]
        if result["ocr_status"] in {ocr_status for ocr_status in (FAILED, ENGINE_UNAVAILABLE)}:
            warnings.append(f"FIGURE_OCR_{result['ocr_status']}:{figure.get('asset_id')}")
    return warnings
