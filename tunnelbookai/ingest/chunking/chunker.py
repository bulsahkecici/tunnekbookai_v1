"""Structure-aware multimodal chunker (task §48-§62).

Input is the extraction bundle — the element stream, tables, figures, slides, sheets and the
OCR items — NOT the Markdown. Each modality gets its own first-class chunk type (§50) and
every chunk keeps its heading path (§52), its page/slide/sheet provenance (§53) and the
source element ids it was built from (§54).

Authoritative chunk location: `processing/<document_id>/chunks/chunk_manifest.jsonl` (§49).
The staging bundle references it rather than holding a second copy.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import tokenizer
from .policy import (
    CHUNK_TYPES, FIGURE_CHUNK, OCR_CHUNK, SHEET_CHUNK, SLIDE_CHUNK, TABLE_CHUNK, TEXT_CHUNK,
    ChunkPolicy, chunk_id, normalize_for_id,
)

CHUNKS_DIRNAME = "chunks"
MANIFEST_NAME = "chunk_manifest.jsonl"

_SENTENCE_RE = re.compile(r"(?<=[.!?…])\s+|\n{2,}")
_WORD_RE = re.compile(r"\w+", re.UNICODE)


@dataclass
class ChunkingContext:
    """Everything a chunk needs to be self-describing."""
    document_id: str
    original_sha256: str | None
    source_kind: str | None
    final_primary_section: str | None
    final_secondary_sections: list[str] = field(default_factory=list)
    format: str | None = None
    evidence_level: str | None = None


def _provenance(context: ChunkingContext) -> dict[str, Any]:
    return {
        "original_sha256": context.original_sha256,
        "source_kind": context.source_kind,
        "format": context.format,
        "evidence_level": context.evidence_level,
    }


def _base_chunk(context: ChunkingContext, policy: ChunkPolicy, chunk_type: str,
                text: str, source_elements: list[str], *,
                identity_part: str | None = None) -> dict[str, Any]:
    chunk = {
        "chunk_id": chunk_id(
            context.document_id, chunk_type, source_elements, text, policy, identity_part
        ),
        "document_id": context.document_id,
        "chunk_type": chunk_type,
        "final_primary_section": context.final_primary_section,
        "final_secondary_sections": list(context.final_secondary_sections),
        "heading_path": [],
        "page_start": None,
        "page_end": None,
        "slide_number": None,
        "sheet_name": None,
        "cell_range": None,
        "source_elements": list(source_elements),
        "text": text,
        "token_count": tokenizer.count(text),
        "provenance": _provenance(context),
        "chunk_schema_version": policy.schema_version,
        "chunk_policy_version": policy.policy_version,
        "tokenizer": policy.tokenizer_name,
    }
    if identity_part is not None:
        chunk["chunk_identity_part"] = identity_part
    return chunk


# --------------------------------------------------------------------------- text chunks
def _split_oversized(text: str, policy: ChunkPolicy) -> list[str]:
    """Split a block at the normal maximum, using sentence boundaries where possible."""
    if tokenizer.count(text) <= policy.max_tokens:
        return [text]
    pieces = [p for p in _SENTENCE_RE.split(text) if p.strip()]
    out: list[str] = []
    current: list[str] = []
    size = 0
    for piece in pieces:
        piece_tokens = tokenizer.count(piece)
        if piece_tokens > policy.max_tokens:
            if current:
                out.append(" ".join(current))
                current, size = [], 0
            remaining = piece
            while remaining:
                head = tokenizer.truncate_to(remaining, policy.max_tokens)
                if head == remaining:
                    current, size = [remaining], tokenizer.count(remaining)
                    break
                if not head:
                    raise RuntimeError("tokenizer could not advance while splitting text")
                out.append(head)
                remaining = remaining[len(head):].lstrip()
            continue
        if size + piece_tokens > policy.max_tokens and current:
            out.append(" ".join(current))
            current, size = [], 0
        current.append(piece)
        size += piece_tokens
    if current:
        out.append(" ".join(current))
    return out or [text]


def _flush_text_group(group: list[dict[str, Any]], context: ChunkingContext,
                      policy: ChunkPolicy, previous_tail: str) -> tuple[list[dict[str, Any]], str]:
    """Turn a run of accumulated elements into one or more TEXT_CHUNKs."""
    if not group:
        return [], previous_tail
    body = "\n\n".join(e["text"] for e in group if e.get("text"))
    if not body.strip():
        return [], previous_tail

    element_ids = [e["element_id"] for e in group]
    # The chunk belongs to the section its CONTENT sits under, not to the first heading that
    # happens to open the group: a chunk of "H1, H1.1, body" is a chunk of H1 > H1.1.
    content = [e for e in group if e.get("type") != "heading"]
    heading_path = (content[0] if content else group[-1]).get("heading_path") or []
    pages = [e.get("page_start") for e in group if e.get("page_start")]
    page_end_values = [e.get("page_end") or e.get("page_start") for e in group
                       if (e.get("page_end") or e.get("page_start"))]
    slides = [e.get("slide_number") for e in group if e.get("slide_number")]

    chunks: list[dict[str, Any]] = []
    parts = _split_oversized(body, policy)
    for index, part in enumerate(parts):
        text = part
        if index == 0 and previous_tail and policy.overlap_tokens > 0:
            # Adding the normal overlap must not push the final chunk over the
            # preferred maximum.  The hard maximum remains a fail-closed guard.
            overlap_budget = max(0, policy.max_tokens - tokenizer.count(part))
            overlap = tokenizer.tail_tokens(
                previous_tail, min(policy.overlap_tokens, overlap_budget)
            )
            if overlap:
                text = f"{overlap}\n\n{part}"
        identity_part = f"{index + 1}/{len(parts)}" if len(parts) > 1 else None
        chunk = _base_chunk(
            context, policy, TEXT_CHUNK, text, element_ids, identity_part=identity_part
        )
        chunk["heading_path"] = list(heading_path)
        chunk["page_start"] = min(pages) if pages else None
        chunk["page_end"] = max(page_end_values) if page_end_values else chunk["page_start"]
        chunk["slide_number"] = slides[0] if slides else None
        chunks.append(chunk)
        previous_tail = ""
    tail = tokenizer.tail_tokens(body, policy.overlap_tokens) if policy.overlap_tokens else ""
    return chunks, tail


def build_text_chunks(elements: list[dict[str, Any]], context: ChunkingContext,
                      policy: ChunkPolicy) -> list[dict[str, Any]]:
    """Heading/paragraph-bounded chunking — never a blind fixed-size split (§51)."""
    chunks: list[dict[str, Any]] = []
    group: list[dict[str, Any]] = []
    size = 0
    tail = ""

    for element in elements:
        kind = element.get("type")
        if kind in {"table_ref", "figure_ref", "furniture"}:
            continue  # these become their own first-class chunks (§50)
        text = (element.get("text") or "").strip()
        if not text:
            continue
        element_tokens = tokenizer.count(text)

        # A heading starts a new chunk once the current one is substantial enough.
        if kind == "heading" and size >= policy.min_tokens:
            produced, tail = _flush_text_group(group, context, policy, tail)
            chunks += produced
            group, size = [], 0
        elif size + element_tokens > policy.max_tokens and group:
            produced, tail = _flush_text_group(group, context, policy, tail)
            chunks += produced
            group, size = [], 0

        group.append(element)
        size += element_tokens

        if size >= policy.target_tokens and kind != "heading":
            produced, tail = _flush_text_group(group, context, policy, tail)
            chunks += produced
            group, size = [], 0

    produced, _ = _flush_text_group(group, context, policy, tail)
    chunks += produced

    # Merge a trailing fragment back into its predecessor when it is below the floor and
    # they share a heading path — a stray two-line chunk retrieves badly.
    merged: list[dict[str, Any]] = []
    for chunk in chunks:
        if (merged and chunk["token_count"] < policy.min_tokens
                and merged[-1]["heading_path"] == chunk["heading_path"]
                and merged[-1]["token_count"] + chunk["token_count"] <= policy.max_tokens):
            previous = merged[-1]
            previous["text"] = f"{previous['text']}\n\n{chunk['text']}"
            previous["source_elements"] += chunk["source_elements"]
            previous["token_count"] = tokenizer.count(previous["text"])
            previous["page_end"] = chunk["page_end"] or previous["page_end"]
            previous["chunk_id"] = chunk_id(context.document_id, TEXT_CHUNK,
                                            previous["source_elements"], previous["text"], policy)
            continue
        merged.append(chunk)
    return merged


# -------------------------------------------------------------------------- table chunks
def table_text(table: dict[str, Any], root: Path) -> str:
    """Concise textual rendering for retrieval; the structured file stays the authority (§55)."""
    parts: list[str] = []
    caption = table.get("caption")
    if caption:
        parts.append(str(caption))
    markdown = table.get("markdown")
    grid = None
    structured = table.get("structured_path")
    if structured:
        path = root / structured if not Path(structured).is_absolute() else Path(structured)
        if path.is_file():
            try:
                grid = json.loads(path.read_text(encoding="utf-8")).get("grid")
            except (OSError, ValueError):
                grid = None
    if grid:
        header, *rows = grid
        parts.append(" | ".join(str(c) for c in header))
        for row in rows[:60]:
            parts.append(" | ".join("" if c is None else str(c) for c in row))
    elif markdown:
        parts.append(str(markdown))
    return "\n".join(p for p in parts if p).strip()


def build_table_chunks(tables: list[dict[str, Any]], elements: list[dict[str, Any]],
                       context: ChunkingContext, policy: ChunkPolicy,
                       root: Path) -> list[dict[str, Any]]:
    by_asset = {e.get("asset_id"): e for e in elements if e.get("asset_id")}
    chunks: list[dict[str, Any]] = []
    for table in tables:
        tid = table.get("table_id") or table.get("asset_id")
        text = table_text(table, root)
        if not text:
            continue
        element = by_asset.get(tid)
        source_elements = [element["element_id"]] if element else []
        # Table rows are newline-delimited. Expose them as split boundaries so a
        # large table can never bypass the document-wide hard token limit. The
        # structured table remains authoritative and every part points to it.
        parts = _split_oversized(text.replace("\n", "\n\n"), policy)
        for index, part in enumerate(parts, 1):
            chunk = _base_chunk(
                context, policy, TABLE_CHUNK, part, source_elements or [tid],
                identity_part=f"{index}/{len(parts)}" if len(parts) > 1 else None,
            )
            chunk.update({
                "table_id": tid,
                "table_part": index,
                "table_parts": len(parts),
                "caption": table.get("caption"),
                "structured_path": table.get("structured_path"),
                "csv_path": table.get("csv_path"),
                "image_path": table.get("image_path"),
                "page": table.get("page"),
                "page_start": table.get("page"),
                "page_end": table.get("page"),
                "slide_number": table.get("slide_number"),
                "rows": table.get("rows"),
                "columns": table.get("columns"),
                "heading_path": list((element or {}).get("heading_path") or []),
            })
            chunks.append(chunk)
    return chunks


def split_chunks_to_soft_max(
    chunks: list[dict[str, Any]], policy: ChunkPolicy
) -> list[dict[str, Any]]:
    """Apply the normal maximum to every modality without losing its metadata.

    Figure and OCR chunks used to bypass the format-specific splitters.  This final
    pass makes the token policy uniform while preserving source references and
    modality fields on every resulting part.
    """
    split: list[dict[str, Any]] = []
    for original in chunks:
        parts = _split_oversized(str(original.get("text") or ""), policy)
        if len(parts) == 1:
            split.append(original)
            continue
        for index, part in enumerate(parts, start=1):
            chunk = dict(original)
            chunk["text"] = part
            chunk["token_count"] = tokenizer.count(part)
            chunk["size_part"] = index
            chunk["size_parts"] = len(parts)
            chunk["chunk_identity_part"] = f"{index}/{len(parts)}"
            chunk["chunk_id"] = chunk_id(
                str(original.get("document_id") or ""),
                str(original.get("chunk_type") or ""),
                list(original.get("source_elements") or []),
                part,
                policy,
                chunk["chunk_identity_part"],
            )
            split.append(chunk)
    for ordinal, chunk in enumerate(split, start=1):
        chunk["ordinal"] = ordinal
    return split


def merge_short_text_chunks(
    chunks: list[dict[str, Any]], policy: ChunkPolicy
) -> list[dict[str, Any]]:
    """Merge only short adjacent text chunks that share the same heading path."""
    merged = [dict(chunk) for chunk in chunks]
    changed = True
    while changed:
        changed = False
        for index, chunk in enumerate(merged):
            if (
                chunk.get("chunk_type") != TEXT_CHUNK
                or int(chunk.get("token_count") or 0) >= policy.min_tokens
            ):
                continue
            neighbours = [
                neighbour for neighbour in (index - 1, index + 1)
                if 0 <= neighbour < len(merged)
                and merged[neighbour].get("chunk_type") == TEXT_CHUNK
                and merged[neighbour].get("heading_path") == chunk.get("heading_path")
                and int(merged[neighbour].get("token_count") or 0)
                    + int(chunk.get("token_count") or 0) <= policy.max_tokens
            ]
            if not neighbours:
                continue
            neighbour = min(
                neighbours, key=lambda position: int(merged[position].get("token_count") or 0)
            )
            first_index, second_index = sorted((index, neighbour))
            first, second = merged[first_index], merged[second_index]
            combined = dict(first)
            combined["text"] = f"{first.get('text') or ''}\n\n{second.get('text') or ''}".strip()
            combined["source_elements"] = list(dict.fromkeys(
                list(first.get("source_elements") or [])
                + list(second.get("source_elements") or [])
            ))
            combined["token_count"] = tokenizer.count(combined["text"])
            starts = [value for value in (first.get("page_start"), second.get("page_start")) if value]
            ends = [value for value in (first.get("page_end"), second.get("page_end")) if value]
            combined["page_start"] = min(starts) if starts else None
            combined["page_end"] = max(ends) if ends else combined["page_start"]
            for key in ("size_part", "size_parts", "chunk_identity_part"):
                combined.pop(key, None)
            combined["chunk_id"] = chunk_id(
                str(combined.get("document_id") or ""), TEXT_CHUNK,
                combined["source_elements"], combined["text"], policy,
            )
            merged[first_index:second_index + 1] = [combined]
            changed = True
            break
    for ordinal, chunk in enumerate(merged, start=1):
        chunk["ordinal"] = ordinal
    return merged


# ------------------------------------------------------------------------- figure chunks
def build_figure_chunks(figures: list[dict[str, Any]], elements: list[dict[str, Any]],
                        context: ChunkingContext, policy: ChunkPolicy) -> list[dict[str, Any]]:
    by_asset = {e.get("asset_id"): e for e in elements if e.get("asset_id")}
    chunks: list[dict[str, Any]] = []
    for figure in figures:
        fid = figure.get("asset_id")
        caption = figure.get("caption")
        ocr_text = figure.get("ocr_text")
        description = figure.get("visual_description")
        if policy.figure_requires_content and not any([caption, ocr_text, description]):
            continue
        text = "\n".join(str(p) for p in (caption, ocr_text, description) if p).strip()
        element = by_asset.get(fid)
        source_elements = [element["element_id"]] if element else [fid]
        chunk = _base_chunk(context, policy, FIGURE_CHUNK, text, source_elements)
        chunk.update({
            "figure_id": fid,
            "caption": caption,
            # OCR text and visual description stay strictly separate (§24, §56)
            "ocr_text": ocr_text,
            "ocr_status": figure.get("ocr_status"),
            "visual_description": description,
            "visual_description_status": figure.get("visual_description_status", "NOT_RUN"),
            "image_path": figure.get("path"),
            "page": figure.get("page"),
            "page_start": figure.get("page"),
            "page_end": figure.get("page"),
            "slide_number": figure.get("slide_number"),
            "heading_path": list((element or {}).get("heading_path")
                                 or figure.get("heading_path") or []),
        })
        chunks.append(chunk)
    return chunks


# ---------------------------------------------------------------------------- OCR chunks
def build_ocr_chunks(ocr_items: list[dict[str, Any]], figure_chunks: list[dict[str, Any]],
                     context: ChunkingContext, policy: ChunkPolicy) -> list[dict[str, Any]]:
    """Page-scope OCR only, and never text already carried by a figure chunk (§57)."""
    represented = {normalize_for_id(c.get("ocr_text") or "") for c in figure_chunks}
    represented.discard("")
    chunks: list[dict[str, Any]] = []
    for item in ocr_items:
        text = (item.get("ocr_text") or "").strip()
        if not text:
            continue
        if policy.skip_ocr_chunk_if_in_figure and normalize_for_id(text) in represented:
            continue
        if item.get("scope") == "FIGURE" and policy.skip_ocr_chunk_if_in_figure:
            continue
        chunk = _base_chunk(context, policy, OCR_CHUNK, text,
                            [item.get("ocr_item_id") or item.get("asset_id") or "OCR"])
        chunk.update({
            "ocr_item_id": item.get("ocr_item_id"),
            "ocr_scope": item.get("scope"),
            "ocr_status": item.get("ocr_status"),
            "ocr_engine": item.get("ocr_engine"),
            "ocr_confidence": item.get("ocr_confidence"),
            "page": item.get("page"),
            "page_start": item.get("page"),
            "page_end": item.get("page"),
            "asset_id": item.get("asset_id"),
        })
        chunks.append(chunk)
    return chunks


# -------------------------------------------------------------------------- slide chunks
def build_slide_chunks(slides: list[dict[str, Any]], context: ChunkingContext,
                       policy: ChunkPolicy) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    for slide in slides:
        number = slide.get("slide_number")
        parts = [p for p in (slide.get("title"), slide.get("text")) if p]
        if policy.include_speaker_notes and slide.get("notes"):
            parts.append(f"Konuşmacı notu: {slide['notes']}")
        body = "\n\n".join(parts).strip()
        if not body:
            continue
        # one slide may need several chunks when it is very large (§58)
        slide_parts = _split_oversized(body, policy)
        for part_index, part in enumerate(slide_parts, 1):
            chunk = _base_chunk(
                context, policy, SLIDE_CHUNK, part, [f"SLIDE{number:04d}"],
                identity_part=(
                    f"{part_index}/{len(slide_parts)}" if len(slide_parts) > 1 else None
                ),
            )
            chunk.update({
                "slide_number": number,
                "slide_title": slide.get("title"),
                "speaker_notes": slide.get("notes") if policy.include_speaker_notes else None,
                "table_refs": list(slide.get("tables") or []),
                "figure_refs": list(slide.get("figures") or []),
                "chart_refs": list(slide.get("charts") or []),
                "snapshot_path": slide.get("snapshot_path"),
                "heading_path": [slide["title"]] if slide.get("title") else [],
                "page_start": number,
                "page_end": number,
            })
            chunks.append(chunk)
    return chunks


# -------------------------------------------------------------------------- sheet chunks
def build_sheet_chunks(sheets: list[dict[str, Any]], context: ChunkingContext,
                       policy: ChunkPolicy, root: Path) -> list[dict[str, Any]]:
    """A workbook never becomes one giant text chunk; each sheet is banded by rows (§59)."""
    chunks: list[dict[str, Any]] = []
    for sheet in sheets:
        name = sheet.get("sheet_name")
        structured = sheet.get("structured_path")
        cells: list[dict[str, Any]] = []
        if structured:
            path = root / structured if not Path(structured).is_absolute() else Path(structured)
            if path.is_file():
                try:
                    cells = json.loads(path.read_text(encoding="utf-8")).get("cells") or []
                except (OSError, ValueError):
                    cells = []
        by_row: dict[int, list[dict[str, Any]]] = {}
        for cell in cells:
            by_row.setdefault(int(cell.get("row") or 0), []).append(cell)

        rows = sorted(by_row)
        if not rows:
            continue
        band = max(1, policy.max_rows_per_sheet_chunk)
        for start in range(0, len(rows), band):
            window = rows[start:start + band]
            lines: list[str] = []
            formulas = 0
            for row_number in window:
                cells_in_row = sorted(by_row[row_number], key=lambda c: int(c.get("column") or 0))
                rendered = []
                for cell in cells_in_row:
                    if cell.get("formula"):
                        formulas += 1
                        value = cell["value"]
                        rendered.append(f"{cell['cell']}={cell['formula']}"
                                        + (f" -> {value}" if value is not None else ""))
                    elif cell.get("value") is not None:
                        rendered.append(f"{cell['cell']}: {cell['value']}")
                if rendered:
                    lines.append(" | ".join(rendered))
            body = "\n".join(lines).strip()
            if not body:
                continue
            first, last = window[0], window[-1]
            columns = [int(c.get("column") or 1) for r in window for c in by_row[r]]
            cell_range = (f"R{first}C{min(columns)}:R{last}C{max(columns)}"
                          if columns else sheet.get("used_range"))
            header = f"Sayfa: {name}" + (" (gizli)" if sheet.get("hidden") else "")
            text = f"{header}\n{body}"
            source_elements = [sheet.get("asset_id") or f"SHEET:{name}"]
            # A fixed row band is not a sufficient size bound: formula-heavy or
            # very wide sheets can contain thousands of lexical tokens in only a
            # handful of rows. Apply the same deterministic last-resort splitter
            # used by text and tables while retaining the structured sheet as the
            # authoritative source for every part.
            parts = _split_oversized(text.replace("\n", "\n\n"), policy)
            for index, part in enumerate(parts, 1):
                chunk = _base_chunk(
                    context, policy, SHEET_CHUNK, part, source_elements,
                    identity_part=f"{index}/{len(parts)}" if len(parts) > 1 else None,
                )
                chunk.update({
                    "sheet_name": name,
                    "sheet_hidden": bool(sheet.get("hidden")),
                    "sheet_part": index,
                    "sheet_parts": len(parts),
                    "cell_range": cell_range,
                    "used_range": sheet.get("used_range"),
                    "formula_present": formulas > 0,
                    "formula_count": formulas,
                    "excel_tables": [t.get("name") for t in (sheet.get("excel_tables") or [])],
                    "structured_path": structured,
                    "csv_path": sheet.get("csv_path"),
                    "heading_path": [str(name)] if name else [],
                })
                chunks.append(chunk)
    return chunks


# ------------------------------------------------------------------------------- dedup
def _shingles(text: str, size: int) -> set[str]:
    words = _WORD_RE.findall(normalize_for_id(text))
    if len(words) < size:
        return {" ".join(words)} if words else set()
    return {" ".join(words[i:i + size]) for i in range(len(words) - size + 1)}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    intersection = len(a & b)
    return intersection / (len(a) + len(b) - intersection)


# Native text beats OCR when the two say the same thing (§60).
_PRIORITY = {TEXT_CHUNK: 0, SLIDE_CHUNK: 1, SHEET_CHUNK: 1, TABLE_CHUNK: 2,
             FIGURE_CHUNK: 3, OCR_CHUNK: 4}


def deduplicate(chunks: list[dict[str, Any]], policy: ChunkPolicy
                ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Drop near-identical chunks within one document. Returns (kept, dropped)."""
    if not policy.dedup_enabled:
        return chunks, []
    ordered = sorted(range(len(chunks)),
                     key=lambda i: (_PRIORITY.get(chunks[i]["chunk_type"], 9), i))
    kept_indices: list[int] = []
    kept_shingles: list[set[str]] = []
    dropped: list[dict[str, Any]] = []

    for index in ordered:
        chunk = chunks[index]
        shingles = _shingles(chunk["text"], policy.dedup_shingle)
        duplicate_of = None
        for position, existing in enumerate(kept_shingles):
            if _jaccard(shingles, existing) >= policy.dedup_threshold:
                duplicate_of = chunks[kept_indices[position]]["chunk_id"]
                break
        if duplicate_of:
            dropped.append({"chunk_id": chunk["chunk_id"], "chunk_type": chunk["chunk_type"],
                            "duplicate_of": duplicate_of})
            continue
        kept_indices.append(index)
        kept_shingles.append(shingles)

    kept = [chunks[i] for i in sorted(kept_indices)]
    return kept, dropped


# ------------------------------------------------------------------------------- driver
def chunk_document(
    *,
    context: ChunkingContext,
    elements: list[dict[str, Any]],
    tables: list[dict[str, Any]],
    figures: list[dict[str, Any]],
    slides: list[dict[str, Any]],
    sheets: list[dict[str, Any]],
    ocr_items: list[dict[str, Any]],
    policy: ChunkPolicy,
    root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    chunks: list[dict[str, Any]] = []
    if policy.allows(TEXT_CHUNK) and not slides and not sheets:
        chunks += build_text_chunks(elements, context, policy)
    elif policy.allows(TEXT_CHUNK) and not slides and sheets:
        pass  # a workbook's text is fully represented by its SHEET_CHUNKs
    if policy.allows(SLIDE_CHUNK) and slides:
        chunks += build_slide_chunks(slides, context, policy)
    if policy.allows(SHEET_CHUNK) and sheets:
        chunks += build_sheet_chunks(sheets, context, policy, root)
    if policy.allows(TABLE_CHUNK) and tables:
        chunks += build_table_chunks(tables, elements, context, policy, root)
    figure_chunks: list[dict[str, Any]] = []
    if policy.allows(FIGURE_CHUNK) and figures:
        figure_chunks = build_figure_chunks(figures, elements, context, policy)
        chunks += figure_chunks
    if policy.allows(OCR_CHUNK) and ocr_items:
        chunks += build_ocr_chunks(ocr_items, figure_chunks, context, policy)

    kept, dropped = deduplicate(chunks, policy)
    kept = split_chunks_to_soft_max(kept, policy)
    kept = merge_short_text_chunks(kept, policy)
    for ordinal, chunk in enumerate(kept, start=1):
        chunk["ordinal"] = ordinal
    return kept, dropped


def write_chunks(bundle: Path, chunks: list[dict[str, Any]]) -> Path:
    out_dir = bundle / CHUNKS_DIRNAME
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / MANIFEST_NAME
    with path.open("w", encoding="utf-8") as handle:
        for chunk in chunks:
            handle.write(json.dumps(chunk, ensure_ascii=False, default=str) + "\n")
    return path


def read_chunks(bundle: Path) -> list[dict[str, Any]]:
    path = bundle / CHUNKS_DIRNAME / MANIFEST_NAME
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]
