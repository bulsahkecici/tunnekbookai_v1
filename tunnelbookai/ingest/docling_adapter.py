"""Version-guarded Docling wrapper (task §6, probe report `reports/docling_api_probe.md`).

Every pipeline option is applied through `_set` which checks `hasattr` first, so a Docling
upgrade that renames or drops a flag degrades to NOT_SUPPORTED instead of crashing the run.
The resolved option set and the runtime versions are recorded into every
`processing/<id>/extraction_report.json` so an extraction can always be explained.

Security: `enable_remote_services` and `allow_external_plugins` are forced False (§26, §80).
"""

from __future__ import annotations

import importlib.metadata
import json
import threading
from collections import OrderedDict
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

from .acceleration import (
    rapidocr_torch_params,
    resolve_accelerator,
    resolve_ocr_accelerator,
)
from .config import IngestConfig


class DoclingUnavailable(RuntimeError):
    pass


# DocumentConverter lazily loads the expensive layout/OCR models.  The ingest worker is
# serial, so keeping a small per-process cache avoids paying that startup cost for every
# document without introducing concurrent access to a converter instance.
_CONVERTER_CACHE_MAX = 6
_CONVERTER_CACHE: OrderedDict[str, tuple[Any, Any]] = OrderedDict()
_CONVERTER_CACHE_LOCK = threading.Lock()


def _converter_cache_key(fmt_key: str, applied: dict[str, Any]) -> str:
    return json.dumps(
        {"format": fmt_key, "options": applied},
        ensure_ascii=True,
        sort_keys=True,
        default=str,
        separators=(",", ":"),
    )


def _cached_converter(constructor: Any, key: str, format_options: dict[Any, Any]) -> tuple[Any, bool]:
    with _CONVERTER_CACHE_LOCK:
        cached = _CONVERTER_CACHE.pop(key, None)
        if cached is not None and cached[0] is constructor:
            _CONVERTER_CACHE[key] = cached
            return cached[1], True
        converter = constructor(format_options=format_options or None)
        _CONVERTER_CACHE[key] = (constructor, converter)
        while len(_CONVERTER_CACHE) > _CONVERTER_CACHE_MAX:
            _CONVERTER_CACHE.popitem(last=False)
        return converter, False


def _discard_converter(key: str) -> None:
    with _CONVERTER_CACHE_LOCK:
        _CONVERTER_CACHE.pop(key, None)


@lru_cache(maxsize=1)
def version_info() -> dict[str, str]:
    out: dict[str, str] = {}
    for dist in ("docling", "docling-core", "docling-ibm-models", "docling-parse"):
        try:
            out[dist] = importlib.metadata.version(dist)
        except importlib.metadata.PackageNotFoundError:
            out[dist] = "not-installed"
    return out


def _set(options: Any, name: str, value: Any, applied: dict[str, Any], unsupported: list[str]) -> None:
    if hasattr(options, name):
        try:
            setattr(options, name, value)
            applied[name] = value
        except Exception:  # pydantic validation refused the value
            unsupported.append(name)
    else:
        unsupported.append(name)


@dataclass
class DoclingConversion:
    """Everything a format adapter needs from one Docling run."""
    status: str
    document: Any = None
    markdown: str = ""
    text: str = ""
    document_dict: dict[str, Any] = field(default_factory=dict)
    applied_options: dict[str, Any] = field(default_factory=dict)
    unsupported_options: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    versions: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.document is not None and self.status in {"SUCCESS", "PARTIAL_SUCCESS"}


def _ocr_options(config: IngestConfig, unsupported: list[str], *, device: str = "cpu"):
    """Build an OCR options object for the configured local engine. Never remote."""
    engine = str(config.ocr.get("engine", "rapidocr")).lower()
    langs = list(config.ocr.get("languages", ["tr", "en"]))
    try:
        from docling.datamodel import pipeline_options as po
    except ImportError as exc:  # pragma: no cover
        raise DoclingUnavailable(str(exc)) from exc

    if engine == "rapidocr" and hasattr(po, "RapidOcrOptions"):
        # RapidOCR language codes differ from ISO-639-1; map conservatively.
        mapped = [{"en": "english", "tr": "latin", "ch": "chinese"}.get(l, l) for l in langs]
        # The default RapidOCR backend is onnxruntime, which this environment does not ship;
        # config/ocr.yaml pins the locally validated torch engine.
        backend = {"torch": "torch", "onnxruntime": "onnxruntime",
                   "openvino": "openvino", "paddle": "paddle"}.get(
                       str(config.ocr.get("engine_type", "torch")).lower())
        primary_kwargs: dict[str, Any] = {"lang": mapped, "backend": backend}
        if backend == "torch":
            primary_kwargs["rapidocr_params"] = rapidocr_torch_params(device)
        for kwargs in ([primary_kwargs, {"lang": mapped, "backend": backend}] if backend else []) + \
                      [{"lang": mapped}, {}]:
            try:
                return po.RapidOcrOptions(**kwargs)
            except Exception:
                continue
        unsupported.append("ocr_options.rapidocr")
    if engine == "ocrmac" and hasattr(po, "OcrMacOptions"):
        try:
            return po.OcrMacOptions(lang=langs)
        except Exception:
            unsupported.append("ocr_options.ocrmac")
    if engine == "tesseract" and hasattr(po, "TesseractOcrOptions"):
        try:
            return po.TesseractOcrOptions(lang=langs)
        except Exception:
            unsupported.append("ocr_options.tesseract")
    if engine not in {"docling_default", "rapidocr", "ocrmac", "tesseract"}:
        unsupported.append(f"ocr_engine:{engine}")
    return None


def build_pdf_options(
    config: IngestConfig, *, do_ocr: bool, want_vision: bool = False,
    accelerator_override: str | None = None,
    ocr_accelerator_override: str | None = None,
):
    """PdfPipelineOptions with every flag guarded. Returns (options, applied, unsupported)."""
    try:
        from docling.datamodel.accelerator_options import AcceleratorOptions
        from docling.datamodel.pipeline_options import PdfPipelineOptions
    except ImportError as exc:  # pragma: no cover
        raise DoclingUnavailable(str(exc)) from exc

    dcfg = config.docling_options
    applied: dict[str, Any] = {}
    unsupported: list[str] = []
    opts = PdfPipelineOptions()

    selection = resolve_accelerator(config)
    accelerator_device = accelerator_override or selection.resolved
    if accelerator_device not in {"cpu", "cuda", "mps"}:
        raise ValueError(f"invalid accelerator override: {accelerator_device}")
    accelerator_options = AcceleratorOptions(
        device=accelerator_device,
        num_threads=int(dcfg.get("num_threads", 4)),
    )
    _set(opts, "accelerator_options", accelerator_options, applied, unsupported)
    applied["accelerator_options"] = {
        "device": accelerator_device,
        "num_threads": accelerator_options.num_threads,
    }
    applied["accelerator_requested"] = selection.requested
    applied["accelerator_device"] = accelerator_device
    applied["accelerator_reason"] = (
        "runtime_cpu_fallback" if accelerator_override == "cpu" else selection.reason
    )

    ocr_selection = resolve_ocr_accelerator(config)
    ocr_accelerator_device = ocr_accelerator_override or ocr_selection.resolved
    if ocr_accelerator_device not in {"cpu", "cuda", "mps"}:
        raise ValueError(f"invalid OCR accelerator override: {ocr_accelerator_device}")

    _set(opts, "images_scale", float(dcfg.get("images_scale", 2.0)), applied, unsupported)
    _set(opts, "generate_page_images", bool(dcfg.get("generate_page_images", True)), applied, unsupported)
    _set(opts, "generate_picture_images", bool(dcfg.get("generate_picture_images", True)), applied, unsupported)
    _set(opts, "do_table_structure", bool(dcfg.get("do_table_structure", True)), applied, unsupported)
    _set(opts, "do_ocr", bool(do_ocr), applied, unsupported)
    _set(opts, "do_picture_classification", bool(dcfg.get("do_picture_classification", True)), applied, unsupported)
    _set(opts, "do_formula_enrichment", bool(dcfg.get("do_formula_enrichment", False)), applied, unsupported)
    # Charts (§22): the flag exists in Docling 2.124.0 but is NOT stable — on a probe it
    # emitted a fully fabricated "Bar chart" series table for a plain gradient image
    # (reports/unified_ingest_engine_audit.md). Fabricated data is a stop condition (§90),
    # so 'auto' resolves to OFF and only an explicit `charts.enabled: true` turns it on.
    charts_cfg = config.ingest.get("charts", {}).get("enabled", "auto")
    want_charts = charts_cfg is True or str(charts_cfg).lower() == "true"
    if want_charts and hasattr(opts, "do_chart_extraction"):
        _set(opts, "do_chart_extraction", True, applied, unsupported)
    elif want_charts:
        unsupported.append("do_chart_extraction")
    else:
        _set(opts, "do_chart_extraction", False, applied, unsupported)
    # Hard security invariants (§26, §80) — never configurable to True.
    _set(opts, "enable_remote_services", False, applied, unsupported)
    _set(opts, "allow_external_plugins", False, applied, unsupported)
    timeout = dcfg.get("document_timeout_seconds")
    if timeout:
        _set(opts, "document_timeout", float(timeout), applied, unsupported)

    ocr_opts = _ocr_options(config, unsupported, device=ocr_accelerator_device) if do_ocr else None
    if ocr_opts is not None:
        _set(opts, "ocr_options", ocr_opts, applied, unsupported)
        applied["ocr_options"] = type(ocr_opts).__name__
        applied["ocr_accelerator_requested"] = ocr_selection.requested
        applied["ocr_accelerator_device"] = ocr_accelerator_device
        applied["ocr_accelerator_reason"] = (
            "runtime_cpu_fallback"
            if ocr_accelerator_override == "cpu"
            else ocr_selection.reason
        )

    if not want_vision:
        _set(opts, "do_picture_description", False, applied, unsupported)
    return opts, applied, unsupported


def convert(
    source: Path,
    config: IngestConfig,
    *,
    input_format: str,
    do_ocr: bool = True,
    want_vision: bool = False,
) -> DoclingConversion:
    """Run one Docling conversion. Never raises for content problems — returns status/errors."""
    versions = version_info()
    applied: dict[str, Any] = {}
    unsupported: list[str] = []
    try:
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling.datamodel.base_models import InputFormat
    except ImportError as exc:
        return DoclingConversion(status="DOCLING_UNAVAILABLE", errors=[f"import: {exc}"],
                                 versions=versions)

    fmt_key = input_format.upper()
    format_options: dict[Any, Any] = {}
    if fmt_key in {"PDF", "IMAGE", "PNG", "JPG"}:
        try:
            opts, applied, unsupported = build_pdf_options(config, do_ocr=do_ocr, want_vision=want_vision)
        except DoclingUnavailable as exc:
            return DoclingConversion(status="DOCLING_UNAVAILABLE", errors=[str(exc)], versions=versions)
        target = InputFormat.PDF if fmt_key == "PDF" else InputFormat.IMAGE
        option_cls = PdfFormatOption
        try:
            format_options[target] = option_cls(pipeline_options=opts)
        except Exception as exc:
            unsupported.append(f"format_option:{fmt_key}:{exc}")

    def _run_once(options: dict[Any, Any], cache_key: str):
        try:
            converter, reused = _cached_converter(DocumentConverter, cache_key, options)
            return converter.convert(str(source)), None, reused
        except Exception as exc:
            # A converter that raised may contain partially initialized native state.
            _discard_converter(cache_key)
            return None, f"{type(exc).__name__}: {exc}", None

    active_format_options = format_options
    active_cache_key = _converter_cache_key(fmt_key, applied)
    result, failure, reused = _run_once(active_format_options, active_cache_key)
    applied["converter_cache"] = "reused" if reused else "created"
    if result is None and applied.get("accelerator_device") != "cpu" and format_options:
        try:
            fallback_opts, fallback_applied, fallback_unsupported = build_pdf_options(
                config,
                do_ocr=do_ocr,
                want_vision=want_vision,
                accelerator_override="cpu",
                ocr_accelerator_override="cpu",
            )
            fallback_options = {target: option_cls(pipeline_options=fallback_opts)}
            fallback_cache_key = _converter_cache_key(fmt_key, fallback_applied)
            result, fallback_failure, fallback_reused = _run_once(
                fallback_options, fallback_cache_key
            )
            unsupported.extend(fallback_unsupported)
            if result is not None:
                unsupported.append(f"note:accelerator_cpu_fallback_after:{failure}")
                applied.update(fallback_applied)
                applied["converter_cache"] = "reused" if fallback_reused else "created"
                active_format_options = fallback_options
                active_cache_key = fallback_cache_key
            else:
                failure = f"{failure}; CPU fallback: {fallback_failure}"
        except Exception as exc:
            failure = f"{failure}; CPU fallback setup: {type(exc).__name__}: {exc}"
    if result is None:
        return DoclingConversion(status="CONVERSION_FAILED", errors=[failure or "unknown"],
                                 applied_options=applied, unsupported_options=unsupported,
                                 versions=versions)

    def _errors_of(res) -> list[str]:
        return [str(getattr(e, "error_message", e))[:500] for e in (getattr(res, "errors", []) or [])]

    def _status_of(res) -> str:
        return getattr(getattr(res, "status", None), "name", str(getattr(res, "status", "UNKNOWN")))

    def _richness(res) -> int:
        doc = getattr(res, "document", None)
        if doc is None:
            return -1
        return (len(getattr(doc, "texts", []) or []) + len(getattr(doc, "tables", []) or [])
                + len(getattr(doc, "pictures", []) or []))

    # docling-parse intermittently drops a single page on first touch; one retry recovers it
    # and we keep whichever pass produced more content.
    if _status_of(result) == "PARTIAL_SUCCESS" and any(
            "failed to parse" in e.lower() for e in _errors_of(result)):
        retried, _, _ = _run_once(active_format_options, active_cache_key)
        if retried is not None and _richness(retried) > _richness(result):
            unsupported.append("note:retried_after_partial_page_parse")
            result = retried

    status = _status_of(result)
    errors = _errors_of(result)

    document = getattr(result, "document", None)
    if document is None:
        return DoclingConversion(status=status or "NO_DOCUMENT", errors=errors or ["no document"],
                                 applied_options=applied, unsupported_options=unsupported,
                                 versions=versions)

    try:
        markdown = document.export_to_markdown()
    except Exception as exc:
        markdown = ""
        errors.append(f"export_to_markdown: {exc}")
    try:
        text = document.export_to_text()
    except Exception:
        text = markdown
    try:
        document_dict = document.export_to_dict()
    except Exception as exc:
        document_dict = {}
        errors.append(f"export_to_dict: {exc}")

    return DoclingConversion(
        status=status, document=document, markdown=markdown, text=text,
        document_dict=document_dict, applied_options=applied,
        unsupported_options=unsupported, errors=errors, versions=versions,
    )
