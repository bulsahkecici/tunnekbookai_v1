"""Asset system (task §21).

Every asset — page snapshot, figure, table, chart — carries the same identity spine:

    document_id, asset_id, source location, sha256, type

Asset ids are deterministic and zero-padded so a re-run of the same original reproduces the
same ids: PAGE0001, FIG0001, TABLE0001, CHART0001, SLIDE0001.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

ASSET_KINDS = ("PAGE", "FIGURE", "TABLE", "CHART", "SLIDE", "SHEET")


def asset_id(prefix: str, index: int, width: int = 4) -> str:
    return f"{prefix}{index:0{width}d}"


def sha256_path(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while block := handle.read(chunk_size):
            digest.update(block)
    return digest.hexdigest()


def pixel_digest(path: Path) -> str | None:
    """SHA256 of an image's DECODED RGB pixels.

    Two encodings of the same picture (Docling's re-saved PNG and the raw OOXML package
    member) have different file bytes but identical pixels; figure de-duplication has to
    compare the pixels or the same image is extracted twice.
    """
    try:
        from PIL import Image

        with Image.open(path) as image:
            rgb = image.convert("RGB")
            payload = rgb.tobytes()
            header = f"{rgb.size[0]}x{rgb.size[1]}".encode()
    except Exception:
        return None
    return hashlib.sha256(header + payload).hexdigest()


def bbox_to_list(bbox: Any) -> list[float] | None:
    """Docling BoundingBox -> [l, t, r, b], or None when unavailable. Never invented (§8)."""
    if bbox is None:
        return None
    try:
        return [float(bbox.l), float(bbox.t), float(bbox.r), float(bbox.b)]
    except Exception:
        pass
    if isinstance(bbox, (list, tuple)) and len(bbox) == 4:
        try:
            return [float(v) for v in bbox]
        except Exception:
            return None
    return None


def prov_of(item: Any) -> tuple[int | None, list[float] | None]:
    """(page_no, bbox) from a Docling item's first provenance entry; (None, None) if absent."""
    prov = getattr(item, "prov", None) or []
    if not prov:
        return None, None
    first = prov[0]
    page = getattr(first, "page_no", None)
    return (int(page) if page is not None else None), bbox_to_list(getattr(first, "bbox", None))


def base_asset(document_id: str, aid: str, kind: str, path: Path | None) -> dict[str, Any]:
    from ..paths import relpath

    record: dict[str, Any] = {
        "document_id": document_id,
        "asset_id": aid,
        "asset_type": kind,
        "path": relpath(path) if path is not None else None,
        "sha256": sha256_path(path) if path is not None and Path(path).is_file() else None,
    }
    return record
