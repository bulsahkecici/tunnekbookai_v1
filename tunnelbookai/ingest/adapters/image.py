"""Image adapter — PNG / JPG / JPEG (task §19).

A standalone image is a valid source document. Pipeline:

    original image -> image metadata -> OCR -> text presence -> optional local vision
                   -> final classification input

The image itself is registered as figure FIG0001 so downstream chunking has a FIGURE_CHUNK
to attach OCR text and any visual description to. A photographic image that yields no OCR
text is not an error — it becomes a VISUAL_ONLY document (§42, §45).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..assets import asset_id, base_asset
from ..elements import ElementBuilder, FIGURE_REF, HEADING, PARAGRAPH
from ..extraction import ExtractionResult, write_normalized
from ..paths import relpath
from . import AdapterContext


def image_metadata(path: Path) -> dict[str, Any]:
    try:
        from PIL import Image
    except ImportError:
        return {}
    try:
        with Image.open(path) as image:
            info = {
                "width": image.size[0],
                "height": image.size[1],
                "mode": image.mode,
                "image_format": image.format,
                "n_frames": getattr(image, "n_frames", 1),
            }
            exif = None
            try:
                raw = image.getexif()
                if raw:
                    exif = {str(k): str(v)[:200] for k, v in raw.items()}
            except Exception:
                exif = None
            info["exif"] = exif
            return info
    except Exception:
        return {}


def run(context: AdapterContext) -> ExtractionResult:
    fmt = context.detection.fmt.value
    result = ExtractionResult(document_id=context.document_id, format=fmt, adapter="image")
    source = context.original_path

    info = image_metadata(source)
    if not info:
        result.fail("IMAGE_UNREADABLE")
        return result

    # The original image is the figure; it is copied (never moved) into figures/.
    figures_dir = context.bundle / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    fig_path = figures_dir / f"FIG0001{source.suffix.lower()}"
    fig_path.write_bytes(source.read_bytes())

    figure = base_asset(context.document_id, asset_id("FIG", 1), "FIGURE", fig_path)
    figure.update({
        "page": 1, "caption": None, "bbox": None, "element_ref": None,
        "picture_class": None, "origin": "standalone_image",
        "width": info.get("width"), "height": info.get("height"),
        "ocr_status": "NOT_RUN", "ocr_text": None, "ocr_confidence": None,
        "visual_description_status": "NOT_RUN", "visual_description": None,
    })

    ocr_result: dict[str, Any] = {"ocr_status": "NOT_RUN", "ocr_text": None,
                                  "ocr_engine": None, "ocr_languages": [], "ocr_confidence": None}
    if context.do_ocr and context.ocr is not None:
        # A standalone image is the whole document: never skip it as "photographic" before
        # trying, or a scanned page would silently lose its text.
        ocr_result = context.ocr.run_image(fig_path, allow_photographic_skip=False)
        figure.update({k: ocr_result[k] for k in
                       ("ocr_status", "ocr_engine", "ocr_languages", "ocr_text", "ocr_confidence")})
        if ocr_result["ocr_status"] in {"FAILED", "ENGINE_UNAVAILABLE"}:
            result.warn(f"IMAGE_OCR_{ocr_result['ocr_status']}")
    elif not context.do_ocr:
        result.warn("OCR_DISABLED")

    ocr_text = ocr_result.get("ocr_text") or ""
    has_text = bool(ocr_text.strip())
    if not has_text:
        result.warn("OCR_EMPTY_TEXT_IMAGE")

    if context.do_vision and context.vision is not None:
        from ..vision.provider import describe_figures

        for warning in describe_figures(context.vision, [figure], context.root):
            result.warn(warning)

    builder = ElementBuilder()
    builder.add(HEADING, context.display_name, level=1, page_start=1,
                extra={"origin": "filename"})
    builder.add(FIGURE_REF, "", page_start=1, asset_id=figure["asset_id"])
    if has_text:
        builder.add(PARAGRAPH, ocr_text.strip(), page_start=1, asset_id=figure["asset_id"],
                    extra={"origin": "ocr"})

    ocr_items = [{
        "ocr_item_id": "OCRFIG0001", "scope": "FIGURE", "page": 1,
        "asset_id": figure["asset_id"], **ocr_result,
    }]

    markdown_lines = [
        f"# {context.display_name}", "",
        f"![{context.display_name}]({relpath(fig_path)})", "",
        "## Görsel üstverisi", "",
        f"- Boyut: {info.get('width')} × {info.get('height')} piksel",
        f"- Biçim: {info.get('image_format')}",
        "", "## OCR metni", "",
        ocr_text.strip() if has_text else "OCR ile metin tespit edilmedi.",
    ]
    if figure.get("visual_description"):
        markdown_lines += ["", "## Görsel açıklama (yerel VLM)", "", figure["visual_description"]]
    markdown = "\n".join(markdown_lines)

    document_json = {
        "document_id": context.document_id,
        "format": fmt,
        "adapter": "image",
        "source_filename": context.original_filename,
        "image": info,
        "figures": [figure],
        "elements": builder.elements,
        "ocr": ocr_result,
        "pages": [{"page_number": 1, "snapshot_asset_id": None,
                   "snapshot_path": relpath(fig_path), "element_ids":
                   [e["element_id"] for e in builder.elements]}],
    }
    write_normalized(context.bundle, result, markdown=markdown,
                     document_json=document_json, text=ocr_text.strip())

    result.figures = [figure]
    result.ocr_items = ocr_items
    result.text_elements = builder.elements
    result.page_count = 1
    result.engine = {"native_parser": "pillow", "ocr_engine": ocr_result.get("ocr_engine")}
    result.capabilities = {
        "text": has_text,
        "tables": False,
        "figures": True,
        "page_snapshots": False,
        "ocr": ocr_result.get("ocr_status") == "SUCCESS",
        "vision": figure.get("visual_description_status") == "SUCCESS",
        "formulas": False,
        "charts": False,
        "slides": False,
        "sheets": False,
    }
    return result
