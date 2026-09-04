"""Chart extraction (task §22).

Charts are strictly best-effort. Three outcomes, and none of them may fail a document:

    SUCCESS             structured series recovered
    NOT_SUPPORTED       the running Docling build has no chart extraction at all
    FAILED_NONBLOCKING  the feature exists but this document's charts could not be parsed

PPTX chart *metadata* (title, type, series names, categories) comes from python-pptx and is
deterministic — it is recorded even when Docling chart parsing is unavailable.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import asset_id, base_asset, prov_of
from ..paths import relpath

CHARTS_DIRNAME = "charts"

NOT_SUPPORTED = "NOT_SUPPORTED"
FAILED_NONBLOCKING = "FAILED_NONBLOCKING"
SUCCESS = "SUCCESS"
DISABLED = "DISABLED"


def chart_extraction_supported() -> bool:
    try:
        from docling.datamodel.pipeline_options import PdfPipelineOptions
    except ImportError:
        return False
    return hasattr(PdfPipelineOptions(), "do_chart_extraction")


def _chart_annotation(picture: Any) -> dict[str, Any] | None:
    """Pull a chart/series annotation off a Docling PictureItem when the build emits one."""
    for annotation in getattr(picture, "annotations", None) or []:
        kind = str(getattr(annotation, "kind", "") or "")
        if "chart" in kind.lower() or hasattr(annotation, "chart_type"):
            try:
                return json.loads(annotation.model_dump_json())
            except Exception:
                try:
                    return dict(annotation)
                except Exception:
                    return {"kind": kind}
    return None


def extract_charts(
    docling_document: Any,
    bundle: Path,
    *,
    document_id: str,
    enabled: bool = True,
) -> tuple[list[dict[str, Any]], str, list[str]]:
    """Returns (records, status, warnings). Never raises."""
    if not enabled:
        return [], DISABLED, ["CHART_EXTRACTION_DISABLED_BY_CONFIG"]
    if not chart_extraction_supported():
        return [], NOT_SUPPORTED, ["CHART_EXTRACTION_NOT_SUPPORTED"]

    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    try:
        pictures = list(getattr(docling_document, "pictures", None) or [])
    except Exception as exc:
        return [], FAILED_NONBLOCKING, [f"CHART_EXTRACTION_FAILED:{type(exc).__name__}: {exc}"]

    out_dir = bundle / CHARTS_DIRNAME
    index = 0
    for picture in pictures:
        annotation = _chart_annotation(picture)
        if annotation is None:
            continue
        index += 1
        cid = asset_id("CHART", index)
        page, bbox = prov_of(picture)
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{cid}.json"
        payload = {
            "document_id": document_id, "chart_id": cid, "page": page, "bbox": bbox,
            "element_ref": getattr(picture, "self_ref", None), "annotation": annotation,
        }
        try:
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str),
                            encoding="utf-8")
        except Exception as exc:
            warnings.append(f"CHART_WRITE_FAILED:{cid}:{type(exc).__name__}")
            continue
        record = base_asset(document_id, cid, "CHART", path)
        record.update({"chart_id": cid, "page": page, "bbox": bbox,
                       "structured_path": relpath(path), "status": SUCCESS})
        records.append(record)

    status = SUCCESS if records else FAILED_NONBLOCKING
    if not records:
        warnings.append("CHART_EXTRACTION_NO_CHARTS_FOUND")
        status = SUCCESS  # "no charts in this document" is not a failure
    return records, status, warnings


def record_pptx_chart(
    document_id: str,
    index: int,
    bundle: Path,
    *,
    slide_number: int,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    """Deterministic PPTX chart metadata (§13) — no image parsing involved."""
    cid = asset_id("CHART", index)
    out_dir = bundle / CHARTS_DIRNAME
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{cid}.json"
    payload = {"document_id": document_id, "chart_id": cid, "slide_number": slide_number,
               "source": "pptx_native", **metadata}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    record = base_asset(document_id, cid, "CHART", path)
    record.update({"chart_id": cid, "slide_number": slide_number, "page": None, "bbox": None,
                   "structured_path": relpath(path), "status": SUCCESS, **metadata})
    return record
