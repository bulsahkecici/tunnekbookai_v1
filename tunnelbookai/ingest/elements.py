"""Structural element stream — the shared spine between extraction and chunking.

Every adapter produces a flat, ordered list of elements. Each element keeps its own identity
(`element_id`), its structural role, its heading path (§52) and its page/slide/sheet
provenance (§53). The structure-aware chunker consumes exactly this list, so chunk
`source_elements` refs are verifiable against the extraction bundle (§63).

Element ids are deterministic per document and per kind:

    HEAD0001  heading            PARA0001  paragraph
    LIST0001  list item          CAPT0001  caption
    FORM0001  formula            CODE0001  code block
    TREF0001  table reference    FREF0001  figure reference
"""

from __future__ import annotations

from typing import Any

HEADING = "heading"
PARAGRAPH = "paragraph"
LIST_ITEM = "list_item"
CAPTION = "caption"
FORMULA = "formula"
CODE = "code"
TABLE_REF = "table_ref"
FIGURE_REF = "figure_ref"
FURNITURE = "furniture"

_PREFIX = {
    HEADING: "HEAD", PARAGRAPH: "PARA", LIST_ITEM: "LIST", CAPTION: "CAPT",
    FORMULA: "FORM", CODE: "CODE", TABLE_REF: "TREF", FIGURE_REF: "FREF",
    FURNITURE: "FURN",
}

_LABEL_MAP = {
    "title": HEADING, "section_header": HEADING,
    "text": PARAGRAPH, "paragraph": PARAGRAPH,
    "list_item": LIST_ITEM, "caption": CAPTION, "formula": FORMULA, "code": CODE,
    "table": TABLE_REF, "picture": FIGURE_REF, "chart": FIGURE_REF,
    "page_header": FURNITURE, "page_footer": FURNITURE, "footnote": FURNITURE,
}


class ElementBuilder:
    """Assigns deterministic element ids and maintains the running heading path."""

    def __init__(self) -> None:
        self._counters: dict[str, int] = {}
        self._heading_stack: list[tuple[int, str]] = []
        self.elements: list[dict[str, Any]] = []

    def _next_id(self, kind: str) -> str:
        prefix = _PREFIX.get(kind, "ELEM")
        self._counters[prefix] = self._counters.get(prefix, 0) + 1
        return f"{prefix}{self._counters[prefix]:04d}"

    @property
    def heading_path(self) -> list[str]:
        return [title for _, title in self._heading_stack]

    def push_heading(self, level: int, title: str) -> None:
        level = max(1, int(level or 1))
        while self._heading_stack and self._heading_stack[-1][0] >= level:
            self._heading_stack.pop()
        self._heading_stack.append((level, title))

    def add(
        self,
        kind: str,
        text: str,
        *,
        level: int | None = None,
        page_start: int | None = None,
        page_end: int | None = None,
        slide_number: int | None = None,
        sheet_name: str | None = None,
        cell_range: str | None = None,
        element_ref: str | None = None,
        asset_id: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if kind == HEADING and text:
            self.push_heading(level or 1, text)
            path = self.heading_path
        else:
            path = self.heading_path
        element = {
            "element_id": self._next_id(kind),
            "type": kind,
            "text": text or "",
            "level": level,
            "heading_path": list(path),
            "page_start": page_start,
            "page_end": page_end if page_end is not None else page_start,
            "slide_number": slide_number,
            "sheet_name": sheet_name,
            "cell_range": cell_range,
            "element_ref": element_ref,
            "asset_id": asset_id,
        }
        if extra:
            element.update(extra)
        self.elements.append(element)
        return element


def from_docling(document: Any, *, table_ids: dict[str, str] | None = None,
                 figure_ids: dict[str, str] | None = None) -> list[dict[str, Any]]:
    """Flatten a DoclingDocument into the shared element stream.

    `table_ids` / `figure_ids` map a Docling `self_ref` to the asset id already assigned by
    `assets.tables` / `assets.figures`, so an element can point at its extracted asset.
    """
    builder = ElementBuilder()
    table_ids = table_ids or {}
    figure_ids = figure_ids or {}

    try:
        stream = list(document.iterate_items())
    except Exception:
        stream = [(item, 0) for item in (getattr(document, "texts", None) or [])]

    for item, _depth in stream:
        label = str(getattr(getattr(item, "label", None), "value", getattr(item, "label", "")) or "")
        kind = _LABEL_MAP.get(label.lower())
        if kind is None:
            kind = PARAGRAPH if getattr(item, "text", None) else None
        if kind is None:
            continue

        page = None
        prov = getattr(item, "prov", None) or []
        if prov:
            page = getattr(prov[0], "page_no", None)
            page = int(page) if page is not None else None

        ref = getattr(item, "self_ref", None)
        text = str(getattr(item, "text", "") or "").strip()

        if kind == TABLE_REF:
            asset = table_ids.get(ref)
            try:
                caption = item.caption_text(document) or ""
            except Exception:
                caption = ""
            builder.add(TABLE_REF, caption, page_start=page, element_ref=ref, asset_id=asset)
            continue
        if kind == FIGURE_REF:
            asset = figure_ids.get(ref)
            try:
                caption = item.caption_text(document) or ""
            except Exception:
                caption = ""
            builder.add(FIGURE_REF, caption, page_start=page, element_ref=ref, asset_id=asset)
            continue
        if not text:
            continue
        level = getattr(item, "level", None)
        builder.add(kind, text, level=int(level) if level else None,
                    page_start=page, element_ref=ref)

    return builder.elements


def element_index(elements: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {e["element_id"]: e for e in elements}


def plain_text(elements: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for element in elements:
        if element["type"] == FURNITURE or not element["text"]:
            continue
        if element["type"] == HEADING:
            parts.append(f"\n{element['text']}\n")
        else:
            parts.append(element["text"])
    return "\n".join(parts).strip()
