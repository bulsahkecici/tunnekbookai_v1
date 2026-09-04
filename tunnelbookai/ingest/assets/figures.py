"""Figure / picture asset extraction (task §8, §12, §25).

Emits `processing/<id>/figures/FIGNNNN.png` plus a metadata record per figure. Docling
provenance (page + bbox) is preserved when present and left `null` when not — never invented.

`ocr_text` and `visual_description` are separate fields and are filled by the OCR / vision
providers downstream (§23, §24, §27). This module only ever writes them as None.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import asset_id, base_asset, pixel_digest, prov_of

FIGURES_DIRNAME = "figures"


def _classification(item: Any) -> str | None:
    """Docling picture classification annotation, when do_picture_classification ran."""
    for annotation in getattr(item, "annotations", None) or []:
        predicted = getattr(annotation, "predicted_classes", None)
        if predicted:
            best = predicted[0]
            label = getattr(best, "class_name", None)
            if label:
                return str(label)
        kind = getattr(annotation, "kind", None)
        if kind == "classification":
            return None
    return None


def extract_figures(
    docling_document: Any,
    bundle: Path,
    *,
    document_id: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    pictures = list(getattr(docling_document, "pictures", None) or [])
    if not pictures:
        return [], warnings

    out_dir = bundle / FIGURES_DIRNAME
    out_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []

    for index, picture in enumerate(pictures, start=1):
        aid = asset_id("FIG", index)
        page, bbox = prov_of(picture)
        target: Path | None = out_dir / f"{aid}.png"
        try:
            image = picture.get_image(docling_document)
        except Exception as exc:
            image = None
            warnings.append(f"FIGURE_IMAGE_FAILED:{aid}:{type(exc).__name__}")
        if image is None:
            warnings.append(f"FIGURE_IMAGE_UNAVAILABLE:{aid}")
            target = None
        else:
            try:
                image.convert("RGB").save(str(target))
            except Exception as exc:
                warnings.append(f"FIGURE_SAVE_FAILED:{aid}:{type(exc).__name__}")
                target = None

        try:
            caption = picture.caption_text(docling_document) or None
        except Exception:
            caption = None

        record = base_asset(document_id, aid, "FIGURE", target)
        record["pixel_digest"] = pixel_digest(target) if target else None
        record.update({
            "page": page,
            "caption": caption,
            "bbox": bbox,
            "element_ref": getattr(picture, "self_ref", None),
            "picture_class": _classification(picture),
            "width": image.size[0] if image is not None else None,
            "height": image.size[1] if image is not None else None,
            # filled downstream, kept strictly separate (§24)
            "ocr_status": "NOT_RUN",
            "ocr_text": None,
            "visual_description_status": "NOT_RUN",
            "visual_description": None,
        })
        records.append(record)
    return records, warnings


def register_embedded_image(
    document_id: str,
    index: int,
    path: Path,
    *,
    caption: str | None = None,
    page: int | None = None,
    heading_path: list[str] | None = None,
    source_order: int | None = None,
    slide_number: int | None = None,
) -> dict[str, Any]:
    """Record for an image pulled straight out of an OOXML package (§12, DOCX/PPTX media)."""
    aid = asset_id("FIG", index)
    record = base_asset(document_id, aid, "FIGURE", path)
    record["pixel_digest"] = pixel_digest(path)
    record.update({
        "page": page,
        "slide_number": slide_number,
        "caption": caption,
        "bbox": None,
        "element_ref": None,
        "picture_class": None,
        "heading_path": heading_path or [],
        "source_order": source_order,
        "ocr_status": "NOT_RUN",
        "ocr_text": None,
        "visual_description_status": "NOT_RUN",
        "visual_description": None,
    })
    try:
        from PIL import Image

        with Image.open(path) as image:
            record["width"], record["height"] = image.size
    except Exception:
        record["width"] = record["height"] = None
    return record
