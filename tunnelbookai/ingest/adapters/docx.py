"""DOCX adapter (task §10, §11, §12).

The structural authority is the ORIGINAL DOCX read through Docling — never a rendered PDF
(§10). The rendered PDF exists only to produce visual page snapshots (§11) and is derived,
temporary data.

Embedded images are pulled straight out of the OOXML package (`word/media/*`) so figures
survive even when Docling emits no PictureItem for them (§12). Caption / nearby-heading
association is done only where the relationship is deterministic from document order; it is
never guessed.
"""

from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any

from .. import docling_adapter
from ..assets import figures as figures_assets
from ..assets import tables as tables_assets
from ..elements import from_docling, plain_text
from ..extraction import ExtractionResult, write_normalized
from ..ocr import provider as ocr_provider
from ..office_renderer import VISUAL_RENDERER_UNAVAILABLE
from . import AdapterContext

MEDIA_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".emf", ".wmf"}
RASTER_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"}


def extract_embedded_media(source: Path, bundle: Path, document_id: str, *,
                           media_prefix: str = "word/media/",
                           start_index: int = 1) -> tuple[list[dict[str, Any]], list[str]]:
    """Copy raster media out of the OOXML package into figures/ (§12)."""
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    try:
        archive = zipfile.ZipFile(source)
    except (OSError, zipfile.BadZipFile) as exc:
        return records, [f"EMBEDDED_MEDIA_UNREADABLE:{type(exc).__name__}"]
    out_dir = bundle / figures_assets.FIGURES_DIRNAME
    index = start_index
    with archive:
        names = sorted(n for n in archive.namelist() if n.startswith(media_prefix))
        for name in names:
            suffix = Path(name).suffix.lower()
            if suffix not in MEDIA_EXTENSIONS:
                continue
            if suffix not in RASTER_EXTENSIONS:
                warnings.append(f"EMBEDDED_MEDIA_VECTOR_SKIPPED:{Path(name).name}")
                continue
            out_dir.mkdir(parents=True, exist_ok=True)
            target = out_dir / f"FIG{index:04d}{suffix}"
            try:
                target.write_bytes(archive.read(name))
            except Exception as exc:
                warnings.append(f"EMBEDDED_MEDIA_FAILED:{Path(name).name}:{type(exc).__name__}")
                continue
            record = figures_assets.register_embedded_image(
                document_id, index, target, source_order=index)
            record["package_member"] = name
            record["origin"] = "ooxml_media"
            records.append(record)
            index += 1
    return records, warnings


def run(context: AdapterContext) -> ExtractionResult:
    fmt = context.detection.fmt.value
    result = ExtractionResult(document_id=context.document_id, format=fmt, adapter="docx")
    source = context.original_path

    conversion = docling_adapter.convert(source, context.config, input_format=fmt,
                                         do_ocr=False, want_vision=False)
    result.engine = {
        "docling_status": conversion.status,
        "docling_versions": conversion.versions,
        "docling_options": conversion.applied_options,
        "structural_authority": "original_docx_via_docling",
    }
    for error in conversion.errors:
        result.warn(f"DOCLING:{error[:120]}")
    document = conversion.document
    if not conversion.ok:
        result.fail(f"DOCLING_CONVERSION_FAILED:{conversion.status}")
        return result

    tcfg = context.tables_cfg
    table_records, table_warnings = tables_assets.extract_tables(
        document, context.bundle, document_id=context.document_id,
        emit_csv=bool(tcfg.get("emit_csv", True)), emit_png=False,
    )
    for warning in table_warnings:
        result.warn(warning)

    docling_figures, figure_warnings = figures_assets.extract_figures(
        document, context.bundle, document_id=context.document_id)
    for warning in figure_warnings:
        result.warn(warning)

    embedded, embedded_warnings = extract_embedded_media(
        source, context.bundle, context.document_id,
        start_index=len(docling_figures) + 1,
    )
    for warning in embedded_warnings:
        result.warn(warning)
    # The same picture reaches us twice — once as a Docling PictureItem, once as the raw
    # package member. Compare DECODED PIXELS, not file bytes, or a re-encode slips through.
    seen_pixels = {f.get("pixel_digest") for f in docling_figures if f.get("pixel_digest")}
    seen_bytes = {f.get("sha256") for f in docling_figures}
    kept_embedded = []
    for record in embedded:
        digest = record.get("pixel_digest")
        if (digest and digest in seen_pixels) or record.get("sha256") in seen_bytes:
            duplicate = record.get("path")
            if duplicate:
                (context.root / duplicate).unlink(missing_ok=True)
            continue
        kept_embedded.append(record)
    embedded = kept_embedded
    figure_records = docling_figures + embedded

    table_ids = {t.get("element_ref"): t["table_id"] for t in table_records if t.get("element_ref")}
    figure_ids = {f.get("element_ref"): f["asset_id"] for f in docling_figures if f.get("element_ref")}
    elements = from_docling(document, table_ids=table_ids, figure_ids=figure_ids)

    # Deterministic association only: an embedded image inherits the heading path that was
    # open at the end of the document body; anything richer would be a guess (§12).
    trailing_path = elements[-1]["heading_path"] if elements else []
    for record in embedded:
        record.setdefault("heading_path", list(trailing_path))

    # Visual snapshots via the OfficeRenderer (§11). Absence is a warning, never a rejection.
    snapshots: list[dict[str, Any]] = []
    renderer = context.office_renderer
    if context.snapshots_enabled and renderer is not None:
        snapshots, snapshot_warnings = renderer.render_pages(
            source, context.bundle, document_id=context.document_id, scale=context.snapshot_scale)
        for warning in snapshot_warnings:
            result.warn(warning)
    elif context.snapshots_enabled:
        result.warn(VISUAL_RENDERER_UNAVAILABLE)

    if context.ocr is not None and context.do_ocr and figure_records:
        for warning in ocr_provider.ocr_figures(context.ocr, figure_records, context.root):
            result.warn(warning)

    text = plain_text(elements) or (conversion.text or "")
    document_json = {
        "document_id": context.document_id,
        "format": fmt,
        "adapter": "docx",
        "source_filename": context.original_filename,
        "structural_authority": "original_docx",
        "docling": conversion.document_dict or None,
        "elements": elements,
        "pages": [{"page_number": s["page_number"], "snapshot_asset_id": s["asset_id"],
                   "snapshot_path": s["path"], "element_ids": []} for s in snapshots],
    }
    write_normalized(context.bundle, result, markdown=conversion.markdown,
                     document_json=document_json, text=text)

    result.pages = snapshots
    result.tables = table_records
    result.figures = figure_records
    result.text_elements = elements
    result.page_count = len(snapshots)
    result.capabilities = {
        "text": bool(text.strip()),
        "tables": bool(table_records),
        "figures": bool(figure_records),
        "page_snapshots": bool(snapshots),
        "ocr": any(f.get("ocr_status") == "SUCCESS" for f in figure_records),
        "vision": any(f.get("visual_description_status") == "SUCCESS" for f in figure_records),
        "formulas": any(e["type"] == "formula" for e in elements),
        "charts": False,
        "slides": False,
        "sheets": False,
    }
    return result
