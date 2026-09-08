"""PDF adapter (task §6, §7, §8, §9).

    PDF -> validate -> Docling conversion -> OCR where required -> page model
        -> tables -> pictures -> page snapshots -> normalized outputs

Native text is preferred over OCR: OCR runs when Docling's text layer is thin or empty
(the validated `pdf_rapidocr` path, reused rather than duplicated —
here it renders through the same `assets.snapshots` pdfium path).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .. import docling_adapter
from ..assets import charts as charts_assets
from ..assets import figures as figures_assets
from ..assets import snapshots as snapshot_assets
from ..assets import tables as tables_assets
from ..elements import from_docling, plain_text
from ..extraction import ExtractionResult, write_normalized
from ..ocr import provider as ocr_provider
from . import AdapterContext

# Below this many characters of native text per page we treat the text layer as unusable
# and fall back to page OCR.
MIN_NATIVE_CHARS_PER_PAGE = 40


def validate_pdf(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with path.open("rb") as handle:
            header = handle.read(5)
    except OSError as exc:
        return [f"PDF_UNREADABLE:{exc}"]
    if header[:4] != b"%PDF":
        errors.append("PDF_BAD_HEADER")
    return errors


def native_text_probe(path: Path) -> tuple[int | None, int]:
    """(page_count, characters in the PDF's own text layer) via pdfium — no ML, no OCR.

    This is what tells FULL_TEXT apart from a scan that only became readable because OCR
    ran: Docling reports both as "text", so the distinction has to be measured here.
    """
    try:
        import pypdfium2 as pdfium
    except ImportError:
        return None, 0
    try:
        document = pdfium.PdfDocument(str(path))
    except Exception:
        return None, 0
    try:
        total = len(document)
        characters = 0
        for index in range(total):
            page = document[index]
            try:
                characters += len((page.get_textpage().get_text_range() or "").strip())
            except Exception:
                pass
            finally:
                page.close()
        return total, characters
    except Exception:
        return None, 0
    finally:
        document.close()


def page_count(path: Path) -> int | None:
    try:
        import pypdfium2 as pdfium
    except ImportError:
        return None
    try:
        document = pdfium.PdfDocument(str(path))
        try:
            return len(document)
        finally:
            document.close()
    except Exception:
        return None


def _page_model(document: Any, snapshots: list[dict[str, Any]],
                elements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One record per page: geometry, snapshot asset, and the elements found on it."""
    pages = getattr(document, "pages", None) or {}
    by_page: dict[int, list[str]] = {}
    for element in elements:
        if element.get("page_start"):
            by_page.setdefault(int(element["page_start"]), []).append(element["element_id"])
    snapshot_by_page = {int(s["page_number"]): s for s in snapshots}

    numbers = sorted(set(pages) | set(snapshot_by_page) | set(by_page))
    model: list[dict[str, Any]] = []
    for number in numbers:
        page = pages.get(number)
        size = getattr(page, "size", None)
        snapshot = snapshot_by_page.get(number)
        model.append({
            "page_number": int(number),
            "width_pt": float(getattr(size, "width", 0) or 0) or None,
            "height_pt": float(getattr(size, "height", 0) or 0) or None,
            "snapshot_asset_id": snapshot["asset_id"] if snapshot else None,
            "snapshot_path": snapshot["path"] if snapshot else None,
            "element_ids": by_page.get(int(number), []),
        })
    return model


def _page_ocr(context: AdapterContext, snapshots: list[dict[str, Any]],
              result: ExtractionResult) -> list[dict[str, Any]]:
    """OCR every rendered page image; used only when the native text layer is unusable."""
    items: list[dict[str, Any]] = []
    if context.ocr is None or not context.ocr.available():
        result.warn("PAGE_OCR_UNAVAILABLE")
        return items
    for snapshot in snapshots:
        path = context.root / snapshot["path"]
        outcome = context.ocr.run_image(path, allow_photographic_skip=False)
        items.append({
            "ocr_item_id": f"OCRPAGE{snapshot['page_number']:04d}",
            "scope": "PAGE",
            "page": snapshot["page_number"],
            "asset_id": snapshot["asset_id"],
            **outcome,
        })
    return items


def run(context: AdapterContext) -> ExtractionResult:
    result = ExtractionResult(document_id=context.document_id, format="PDF", adapter="pdf")
    source = context.original_path

    for error in validate_pdf(source):
        result.fail(error)
    if result.errors:
        return result

    pages_total, native_layer_chars = native_text_probe(source)
    if pages_total is None:
        pages_total = page_count(source)
    if pages_total is not None:
        result.page_count = pages_total
    native_layer_thin = native_layer_chars < MIN_NATIVE_CHARS_PER_PAGE * max(1, pages_total or 1)

    # 1) Docling conversion. If the OCR-enabled pass fails (e.g. the configured OCR backend
    #    is not installed) retry without Docling OCR: structure is still worth having, and
    #    this adapter has its own pdfium+RapidOCR page fallback below.
    conversion = docling_adapter.convert(source, context.config, input_format="PDF",
                                         do_ocr=context.do_ocr, want_vision=False)
    if not conversion.ok and context.do_ocr:
        retry = docling_adapter.convert(source, context.config, input_format="PDF",
                                        do_ocr=False, want_vision=False)
        if retry.ok:
            result.warn(f"DOCLING_OCR_PASS_FAILED_RETRIED_WITHOUT_OCR:{conversion.status}")
            for error in conversion.errors:
                result.warn(f"DOCLING_OCR:{error[:120]}")
            conversion = retry
    result.engine = {
        "docling_status": conversion.status,
        "docling_versions": conversion.versions,
        "docling_options": conversion.applied_options,
        "docling_unsupported_options": conversion.unsupported_options,
    }
    for error in conversion.errors:
        result.warn(f"DOCLING:{error[:120]}")

    document = conversion.document
    if not conversion.ok:
        result.fail(f"DOCLING_CONVERSION_FAILED:{conversion.status}")

    # 2) Assets — tables, figures, charts (each individually non-fatal).
    table_records: list[dict[str, Any]] = []
    figure_records: list[dict[str, Any]] = []
    chart_records: list[dict[str, Any]] = []
    chart_status = charts_assets.NOT_SUPPORTED
    if document is not None:
        tcfg = context.tables_cfg
        if tcfg.get("enabled", True):
            table_records, table_warnings = tables_assets.extract_tables(
                document, context.bundle, document_id=context.document_id,
                emit_csv=bool(tcfg.get("emit_csv", True)), emit_png=bool(tcfg.get("emit_png", True)),
            )
            for warning in table_warnings:
                result.warn(warning)
        figure_records, figure_warnings = figures_assets.extract_figures(
            document, context.bundle, document_id=context.document_id)
        for warning in figure_warnings:
            result.warn(warning)
        charts_cfg = (context.config.ingest.get("charts", {}) or {}).get("enabled", "auto")
        chart_records, chart_status, chart_warnings = charts_assets.extract_charts(
            document, context.bundle, document_id=context.document_id,
            enabled=charts_cfg is True or str(charts_cfg).lower() == "true")
        for warning in chart_warnings:
            result.warn(warning)

    # 3) Page snapshots — visual provenance (§7).
    snapshots: list[dict[str, Any]] = []
    if context.snapshots_enabled:
        snapshots, snapshot_warnings = snapshot_assets.snapshot_pdf(
            source, context.bundle, document_id=context.document_id,
            scale=context.snapshot_scale, docling_document=document,
        )
        for warning in snapshot_warnings:
            result.warn(warning)
        if pages_total and len(snapshots) < pages_total:
            result.warn(f"SNAPSHOT_INCOMPLETE:{len(snapshots)}/{pages_total}")

    # 4) Element stream.
    table_ids = {t.get("element_ref"): t["table_id"] for t in table_records if t.get("element_ref")}
    figure_ids = {f.get("element_ref"): f["asset_id"] for f in figure_records if f.get("element_ref")}
    elements = from_docling(document, table_ids=table_ids, figure_ids=figure_ids) if document else []

    native_text = plain_text(elements) or (conversion.text or "").strip()
    effective_pages = pages_total or len(snapshots) or 1
    thin_text_layer = len(native_text) < MIN_NATIVE_CHARS_PER_PAGE * effective_pages
    # Docling's own OCR may already have recovered a scan: the document has text, but that
    # text came from OCR, not from the file. Record it as such rather than as FULL_TEXT.
    docling_ocr_recovered = (
        native_layer_thin and not thin_text_layer
        and bool(conversion.applied_options.get("do_ocr")))
    if docling_ocr_recovered:
        result.warn("NATIVE_TEXT_LAYER_THIN_DOCLING_OCR_RECOVERED")

    # 5) OCR fallback when the native text layer cannot carry the document.
    ocr_items: list[dict[str, Any]] = []
    if thin_text_layer and context.do_ocr and snapshots:
        result.warn("NATIVE_TEXT_LAYER_THIN_OCR_FALLBACK")
        ocr_items = _page_ocr(context, snapshots, result)
        ocr_text = "\n\n".join(
            f"## Sayfa {i['page']}\n\n{i['ocr_text']}" for i in ocr_items if i.get("ocr_text")
        )
        if ocr_text and len(ocr_text) > len(native_text):
            native_text = ocr_text
    elif thin_text_layer and not context.do_ocr:
        result.warn("NATIVE_TEXT_LAYER_THIN_OCR_DISABLED")

    # 6) Figure OCR (§25).
    if context.ocr is not None and context.do_ocr and figure_records:
        for warning in ocr_provider.ocr_figures(context.ocr, figure_records, context.root):
            result.warn(warning)

    # 7) Normalized outputs.
    markdown = conversion.markdown or ""
    if not markdown.strip() and native_text:
        markdown = f"# {context.display_name}\n\n{native_text}"
    document_json = {
        "document_id": context.document_id,
        "format": "PDF",
        "adapter": "pdf",
        "source_filename": context.original_filename,
        "page_count": effective_pages,
        "docling": conversion.document_dict or None,
        "elements": elements,
        "pages": _page_model(document, snapshots, elements) if document is not None else [
            {"page_number": s["page_number"], "snapshot_asset_id": s["asset_id"],
             "snapshot_path": s["path"], "element_ids": []} for s in snapshots
        ],
    }
    write_normalized(context.bundle, result, markdown=markdown,
                     document_json=document_json, text=native_text)

    result.pages = snapshots
    result.tables = table_records
    result.figures = figure_records
    result.charts = chart_records
    result.ocr_items = ocr_items
    result.text_elements = elements
    result.page_count = effective_pages
    result.capabilities = {
        "text": bool(native_text),
        "tables": bool(table_records),
        "figures": bool(figure_records),
        "page_snapshots": bool(snapshots),
        "ocr": (docling_ocr_recovered
                or any(i.get("ocr_status") == "SUCCESS" for i in ocr_items)
                or any(f.get("ocr_status") == "SUCCESS" for f in figure_records)),
        "vision": any(f.get("visual_description_status") == "SUCCESS" for f in figure_records),
        "formulas": any(e["type"] == "formula" for e in elements),
        "charts": bool(chart_records),
        "slides": False,
        "sheets": False,
    }
    result.engine["chart_status"] = chart_status
    result.engine["native_text_layer_chars"] = native_layer_chars
    result.engine["native_text_layer"] = (
        "ABSENT_OCR_RECOVERED" if docling_ocr_recovered
        else ("THIN" if thin_text_layer else "OK"))
    return result
