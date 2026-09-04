"""Page / slide / sheet visual snapshots (task §7, §14, §18).

Snapshots are *visual provenance*, never textual evidence (§7). Two renderers:

  1. pypdfium2 — the preferred PDF page renderer (deterministic, no ML, no network).
  2. Docling page images — used when a conversion already produced them and pdfium is absent.

Office formats reach this module through `office_renderer.OfficeRenderer` (DOCX/PPTX/XLSX ->
temporary PDF -> PNG). The temporary PDF is derived data and is discarded (§11).
A missing renderer yields the warning VISUAL_RENDERER_UNAVAILABLE and never a rejection.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import asset_id, base_asset

PAGE_DIRNAME = "pages"
SLIDE_DIRNAME = "slides"
SHEET_DIRNAME = "sheet_snapshots"


def _record(document_id: str, aid: str, kind: str, path: Path, page_number: int,
            width: int, height: int, renderer: str) -> dict[str, Any]:
    rec = base_asset(document_id, aid, kind, path)
    rec.update({
        "page_number": page_number,
        "width": int(width),
        "height": int(height),
        "renderer": renderer,
        "role": "VISUAL_PROVENANCE",
    })
    return rec


def pdfium_available() -> bool:
    try:
        import pypdfium2  # noqa: F401
    except ImportError:
        return False
    return True


def render_pdf_pages(
    pdf_path: Path,
    out_dir: Path,
    *,
    document_id: str,
    scale: float = 2.0,
    prefix: str = "page",
    kind: str = "PAGE",
    id_prefix: str = "PAGE",
    max_pages: int = 0,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Render every page of `pdf_path` to `out_dir/<prefix>_NNNN.png` with pypdfium2."""
    warnings: list[str] = []
    if not pdfium_available():
        return [], ["SNAPSHOT_RENDERER_UNAVAILABLE:pypdfium2"]

    import pypdfium2 as pdfium

    out_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    document = pdfium.PdfDocument(str(pdf_path))
    try:
        total = len(document)
        limit = min(total, max_pages) if max_pages else total
        for index in range(limit):
            page_number = index + 1
            target = out_dir / f"{prefix}_{page_number:04d}.png"
            try:
                page = document[index]
                image = page.render(scale=scale, rotation=0).to_pil()
                image.save(str(target))
                width, height = image.size
                page.close()
            except Exception as exc:
                warnings.append(f"SNAPSHOT_PAGE_FAILED:{page_number}:{type(exc).__name__}")
                continue
            records.append(_record(document_id, asset_id(id_prefix, page_number), kind,
                                   target, page_number, width, height, "pypdfium2"))
        if max_pages and total > limit:
            warnings.append(f"SNAPSHOT_TRUNCATED:{limit}/{total}")
    finally:
        document.close()
    return records, warnings


def render_docling_page_images(
    document: Any,
    out_dir: Path,
    *,
    document_id: str,
    prefix: str = "page",
    kind: str = "PAGE",
    id_prefix: str = "PAGE",
) -> tuple[list[dict[str, Any]], list[str]]:
    """Fallback: persist the page images Docling already produced (generate_page_images=True)."""
    warnings: list[str] = []
    pages = getattr(document, "pages", None) or {}
    if not pages:
        return [], ["SNAPSHOT_NO_DOCLING_PAGE_IMAGES"]
    out_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    for page_no in sorted(pages):
        page = pages[page_no]
        image_ref = getattr(page, "image", None)
        pil = getattr(image_ref, "pil_image", None) if image_ref is not None else None
        if pil is None:
            warnings.append(f"SNAPSHOT_PAGE_IMAGE_MISSING:{page_no}")
            continue
        target = out_dir / f"{prefix}_{int(page_no):04d}.png"
        try:
            pil.save(str(target))
        except Exception as exc:
            warnings.append(f"SNAPSHOT_PAGE_FAILED:{page_no}:{type(exc).__name__}")
            continue
        records.append(_record(document_id, asset_id(id_prefix, int(page_no)), kind, target,
                               int(page_no), pil.size[0], pil.size[1], "docling_page_image"))
    return records, warnings


def snapshot_pdf(
    pdf_path: Path,
    bundle: Path,
    *,
    document_id: str,
    scale: float,
    docling_document: Any = None,
    dirname: str = PAGE_DIRNAME,
    prefix: str = "page",
    kind: str = "PAGE",
    id_prefix: str = "PAGE",
) -> tuple[list[dict[str, Any]], list[str]]:
    """Preferred pdfium render, with the Docling page images as fallback."""
    out_dir = bundle / dirname
    records, warnings = render_pdf_pages(
        pdf_path, out_dir, document_id=document_id, scale=scale,
        prefix=prefix, kind=kind, id_prefix=id_prefix,
    )
    if records:
        return records, warnings
    if docling_document is not None:
        fallback, fallback_warnings = render_docling_page_images(
            docling_document, out_dir, document_id=document_id,
            prefix=prefix, kind=kind, id_prefix=id_prefix,
        )
        if fallback:
            return fallback, warnings + fallback_warnings
        warnings += fallback_warnings
    warnings.append("VISUAL_RENDERER_UNAVAILABLE")
    return [], warnings
