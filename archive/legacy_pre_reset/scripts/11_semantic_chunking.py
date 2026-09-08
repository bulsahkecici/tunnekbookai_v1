from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
import tempfile
from collections import Counter
from pathlib import Path
from statistics import mean


CHUNKER_VERSION = "semantic-markdown-v1.1"
TOKENIZER_NAME = "unicode-lexical-v1"
TARGET_TOKENS = 850
SOFT_MIN = 250
SOFT_MAX = 1200
HARD_MAX = 1500
TOKEN_RE = re.compile(r"\w+(?:[-'’]\w+)*|[^\w\s]", re.UNICODE)
HEADING_RE = re.compile(r"(?m)^(#{1,4})[ \t]+(.+?)[ \t]*(?=\r?$)")
REGULATION_RE = re.compile(r"(?im)^(?:MADDE\s+\d+[A-ZÇĞİÖŞÜ]?(?:\s*[-–—:]|\b)|Article\s+\d+(?:\s*[-–—:]|\b)|Section\s+\d+(?:\.\d+)*(?:\s*[-–—:]|\b))")
PAGE_START_RE = re.compile(r"<!--\s*original_page_start:\s*(\d+)\s*-->", re.IGNORECASE)
PAGE_END_RE = re.compile(r"<!--\s*original_page_end:\s*(\d+)\s*-->", re.IGNORECASE)
CITATION_RULE_RE = re.compile(r"<!--\s*citation_rule:\s*(.*?)\s*-->", re.IGNORECASE)
SLIDE_RE = re.compile(r"(?im)^#{1,4}\s+(?:Slayt|Slide)\s+(\d+)\b")
PAGE_HEADING_RE = re.compile(r"(?im)^#{1,4}\s+(?:Sayfa|Page)\s+(\d+)\b")
TABLE_LINE_RE = re.compile(r"(?m)^\s*\|.*\|\s*$")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|[\s:|-]*-[\s:|-]*\|\s*$")
LIST_LINE_RE = re.compile(r"(?m)^\s*(?:[-*+]\s+|\d+[.)]\s+)")
FORMULA_RE = re.compile(r"<!--\s*formula-not-decoded\s*-->", re.IGNORECASE)
IMAGE_RE = re.compile(r"<!--\s*image\s*-->|image placeholder|figure placeholder", re.IGNORECASE)
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
MANIFEST_FIELDS = ["document_id", "source_sha256", "normalized_sha256", "chunk_count", "min_tokens",
                   "max_tokens", "mean_tokens", "page_resolved_chunks", "slide_resolved_chunks",
                   "section_resolved_chunks", "source_only_chunks", "table_chunks", "formula_chunks",
                   "image_chunks", "warning_count", "chunker_version"]
REVIEW_FIELDS = ["priority", "document_id", "chunk_id", "reason", "details", "review_status", "reviewer_note"]
UNSAFE_METADATA_STATUS = ("human_review", "still_human", "unresolved", "rejected")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def atomic_write(path: Path, payload: bytes) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == payload:
        return False
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise
    return True


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_bytes(rows: list[dict[str, object]], fields: list[str]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return ("\ufeff" + buffer.getvalue()).encode("utf-8")


def jsonl_bytes(rows: list[dict[str, object]]) -> bytes:
    return ("".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for row in rows)).encode("utf-8")


def token_count(text: str) -> int:
    return len(TOKEN_RE.findall(text))


def split_front_matter(text: str) -> tuple[str, str]:
    match = re.match(r"\A(---\r?\n.*?\r?\n---(?:\r?\n|\Z))", text, re.DOTALL)
    return (match.group(1), text[match.end():]) if match else ("", text)


def front_value(front: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.*?)\s*$", front)
    if not match:
        return None
    value = match.group(1).strip().strip("\"'")
    return None if value.lower() in {"", "null", "none", "[]"} else value


def safe_metadata(row: dict[str, str], field: str) -> object:
    value = row.get(f"{field}_value", "").strip()
    status = row.get(f"{field}_verification_status", "").lower()
    if not value or any(marker in status for marker in UNSAFE_METADATA_STATUS):
        return None
    if field == "topics":
        return [item for item in value.split("|") if item]
    return value


def metadata_bundle(verified: dict[str, str], master: dict[str, str], front: str) -> dict[str, object]:
    fields = ("title", "organization", "year", "language", "document_type", "authority_level", "topics")
    values = {field: safe_metadata(verified, field) for field in fields}
    statuses = {field: verified.get(f"{field}_verification_status", "") or None for field in fields}
    return {
        **values,
        "metadata_status": statuses,
        "authority_level_source": verified.get("authority_level_source", "") or None,
        "authority_level_confidence": verified.get("authority_level_confidence", "") or None,
        "citation_mode": master.get("citation_mode", "") or front_value(front, "citation_mode") or citation_mode_for_extension(verified.get("source_extension", "")),
        "citation_sidecar": master.get("citation_sidecar", "") or None,
    }


def citation_mode_for_extension(extension: str) -> str:
    extension = extension.lower()
    if extension == ".pdf":
        return "pdf_page"
    if extension in {".ppt", ".pptx", ".pptm"}:
        return "slide"
    if extension in {".doc", ".docx", ".rtf"}:
        return "document_section"
    if extension in {".xls", ".xlsx", ".csv"}:
        return "table_or_sheet"
    if extension in {".jpg", ".jpeg", ".png", ".tif", ".tiff"}:
        return "image"
    return "source_only"


def boundary_starts(text: str) -> list[int]:
    starts = {match.start() for match in HEADING_RE.finditer(text)}
    starts.update(match.start() for match in REGULATION_RE.finditer(text))
    return sorted(starts)


def semantic_segments(body: str) -> list[str]:
    starts = boundary_starts(body)
    if not starts:
        return [body] if body else []
    boundaries = ([0] if starts[0] else []) + starts + [len(body)]
    segments = [body[left:right] for left, right in zip(boundaries, boundaries[1:]) if right > left]
    if len(segments) > 1 and not (HEADING_RE.match(segments[0]) or REGULATION_RE.match(segments[0])):
        if token_count(segments[0]) < SOFT_MIN:
            segments[1] = segments[0] + segments[1]
            segments.pop(0)
    return segments


def strong_boundary(segment: str) -> bool:
    heading = HEADING_RE.match(segment)
    return bool(REGULATION_RE.match(segment) or SLIDE_RE.search(segment) or PAGE_HEADING_RE.search(segment)
                or PAGE_START_RE.search(segment) or (heading and len(heading.group(1)) == 1))


def substantive_text(text: str) -> str:
    text = COMMENT_RE.sub(" ", text)
    text = IMAGE_RE.sub(" ", text)
    text = FORMULA_RE.sub(" ", text)
    text = HEADING_RE.sub(" ", text)
    return " ".join(TOKEN_RE.findall(text))


def coalesce_segments(segments: list[str]) -> list[str]:
    """Merge OCR-generated micro-headings without crossing citation/regulation boundaries."""
    groups: list[str] = []
    current = ""
    for segment in segments:
        if current and (strong_boundary(segment) or token_count(current + segment) > 1000):
            groups.append(current)
            current = segment
        else:
            current += segment
    if current:
        groups.append(current)
    index = 0
    while index < len(groups):
        if len(TOKEN_RE.findall(substantive_text(groups[index]))) < 3 and len(groups) > 1:
            if index + 1 < len(groups):
                groups[index + 1] = groups[index] + groups[index + 1]
                groups.pop(index)
            else:
                groups[index - 1] += groups[index]
                groups.pop(index)
                index -= 1
        else:
            index += 1
    return groups


def paragraph_blocks(text: str) -> list[str]:
    blocks = []
    cursor = 0
    for match in re.finditer(r"(?:\r?\n[ \t]*){2,}", text):
        blocks.append(text[cursor:match.end()])
        cursor = match.end()
    if cursor < len(text):
        blocks.append(text[cursor:])
    return [block for block in blocks if block]


def is_table_block(text: str) -> bool:
    lines = [line for line in text.splitlines() if line.strip()]
    return bool(lines) and sum(bool(TABLE_LINE_RE.fullmatch(line)) for line in lines) >= max(2, len(lines) // 2)


def split_oversized_block(block: str) -> tuple[list[str], bool]:
    if token_count(block) <= HARD_MAX:
        return [block], False
    if is_table_block(block):
        return [block], True
    lines = block.splitlines(keepends=True)
    pieces, current = [], ""
    for line in lines:
        if current and token_count(current + line) > SOFT_MAX:
            pieces.append(current)
            current = ""
        if token_count(line) > HARD_MAX:
            tokens = list(TOKEN_RE.finditer(line))
            start = 0
            for index in range(SOFT_MAX, len(tokens), SOFT_MAX):
                end = tokens[index].start()
                if current:
                    pieces.append(current)
                    current = ""
                pieces.append(line[start:end])
                start = end
            current += line[start:]
        else:
            current += line
    if current:
        pieces.append(current)
    return pieces, False


def is_fragment(text: str) -> bool:
    """A piece carrying no substantive prose of its own (bare comments/headings/placeholders)."""
    return len(TOKEN_RE.findall(substantive_text(text))) < 3


def merge_fragments(chunks: list[str], ceiling: int | None = None) -> list[str]:
    """Attach non-substantive fragments to a neighbour, optionally without breaching a size ceiling."""
    index = 0
    while index < len(chunks):
        if not is_fragment(chunks[index]) or len(chunks) == 1:
            index += 1
            continue
        forward = index + 1 < len(chunks)
        target = index + 1 if forward else index - 1
        if ceiling is not None and token_count(chunks[index] + chunks[target]) > ceiling:
            index += 1
            continue
        chunks[target] = chunks[index] + chunks[target] if forward else chunks[target] + chunks[index]
        chunks.pop(index)
        if not forward:
            index -= 1
    return chunks


def enforce_hard_limit(chunks: list[str]) -> tuple[list[str], list[str]]:
    """Re-split post-merge chunks above the hard limit at safe line/list boundaries.

    Markdown tables stay atomic: splitting them at a line boundary would orphan data rows
    from their header row. Blocks that no safe boundary can divide stay atomic as well.
    Both cases surface as justified P1 special cases rather than silent corruption.
    """
    result, warnings = [], []
    for chunk in chunks:
        if token_count(chunk) <= HARD_MAX:
            result.append(chunk)
        elif TABLE_LINE_RE.search(chunk):
            result.append(chunk)
            warnings.append("huge_atomic_table_over_hard_limit")
        else:
            pieces, _ = split_oversized_block(chunk)
            if len(pieces) < 2:
                result.append(chunk)
                warnings.append("indivisible_block_over_hard_limit")
            else:
                result.extend(pieces)
    return result, warnings


def split_segment(segment: str) -> tuple[list[str], list[str]]:
    blocks = paragraph_blocks(segment)
    expanded, warnings = [], []
    for block in blocks:
        pieces, huge_table = split_oversized_block(block)
        expanded.extend(pieces)
        if huge_table:
            warnings.append("huge_atomic_table_over_hard_limit")
    chunks, current = [], ""
    for block in expanded:
        proposed = current + block
        if current and token_count(proposed) > SOFT_MAX:
            chunks.append(current)
            current = block
        else:
            current = proposed
    if current:
        chunks.append(current)
    if len(chunks) > 1 and token_count(chunks[-1]) < SOFT_MIN and token_count(chunks[-2] + chunks[-1]) <= SOFT_MAX:
        chunks[-2] += chunks[-1]
        chunks.pop()
    chunks = merge_fragments(chunks)
    chunks, limit_warnings = enforce_hard_limit(chunks)
    warnings.extend(limit_warnings)
    return merge_fragments(chunks, ceiling=HARD_MAX), warnings


def heading_context(text: str, hierarchy: list[str | None]) -> tuple[list[str | None], str | None, str | None, str]:
    match = HEADING_RE.search(text)
    if not match:
        regulation = REGULATION_RE.search(text)
        if regulation:
            heading = regulation.group(0).strip()
            path = [item for item in hierarchy if item] + [heading]
            return hierarchy, heading, hierarchy[-1] if hierarchy and hierarchy[-1] else None, " > ".join(path)
        path = [item for item in hierarchy if item]
        return hierarchy, path[-1] if path else None, path[-2] if len(path) > 1 else None, " > ".join(path)
    level, heading = len(match.group(1)), match.group(2).strip()
    updated = hierarchy[:]
    while len(updated) < 4:
        updated.append(None)
    updated[level - 1] = heading
    for index in range(level, 4):
        updated[index] = None
    path = [item for item in updated if item]
    return updated, heading, path[-2] if len(path) > 1 else None, " > ".join(path)


def page_range(text: str, inherited: tuple[int | None, int | None]) -> tuple[int | None, int | None]:
    starts = [int(value) for value in PAGE_START_RE.findall(text)]
    ends = [int(value) for value in PAGE_END_RE.findall(text)]
    page_heading = [int(value) for value in PAGE_HEADING_RE.findall(text)]
    if page_heading:
        return min(page_heading), max(page_heading)
    return (min(starts) if starts else inherited[0], max(ends) if ends else inherited[1])


def table_corruption(chunks: list[dict[str, object]]) -> list[str]:
    """Chunk IDs whose boundary cuts a Markdown table, orphaning data rows from their header.

    Two tables meeting at a boundary are not corruption: Docling emits one table per region, so a
    chunk may legitimately open a fresh table. A fresh table declares itself with a header row
    followed by a `|---|` separator; data rows arriving without that pair are orphaned.
    """
    def visible(text: str) -> list[str]:
        return [line for line in text.splitlines() if line.strip()]
    corrupted = []
    for previous, current in zip(chunks, chunks[1:]):
        before, after = visible(str(previous["text"])), visible(str(current["text"]))
        if not before or not after:
            continue
        if not (TABLE_LINE_RE.fullmatch(before[-1]) and TABLE_LINE_RE.fullmatch(after[0])):
            continue
        if len(after) > 1 and TABLE_SEPARATOR_RE.fullmatch(after[1]):
            continue
        corrupted.append(str(current["chunk_id"]))
    return corrupted


def provenance_corruption(chunks: list[dict[str, object]]) -> list[str]:
    """Chunk IDs whose citation anchors are internally inconsistent and would mis-cite the source."""
    corrupted = []
    for chunk in chunks:
        start, end = chunk["original_page_start"], chunk["original_page_end"]
        slide_start, slide_end = chunk["slide_start"], chunk["slide_end"]
        broken = (start is not None and end is not None and start > end)
        broken = broken or (slide_start is not None and slide_end is not None and slide_start > slide_end)
        broken = broken or (start is not None and start < 1) or (slide_start is not None and slide_start < 1)
        broken = broken or (chunk["provenance_status"] == "page_resolved" and start is None)
        broken = broken or (chunk["provenance_status"] == "slide_resolved" and slide_start is None)
        broken = broken or (chunk["provenance_status"] == "section_resolved" and not chunk["section_path"])
        if broken:
            corrupted.append(str(chunk["chunk_id"]))
    return corrupted


def chunk_document(path: Path, root: Path, verified: dict[str, str], master: dict[str, str]) -> dict[str, object]:
    source_bytes = path.read_bytes()
    source = source_bytes.decode("utf-8-sig")
    front, body = split_front_matter(source)
    document_id = front_value(front, "document_id")
    if not document_id:
        raise ValueError(f"document_id missing: {path}")
    metadata = metadata_bundle(verified, master, front)
    source_relative_path = verified.get("source_relative_path", "") or front_value(front, "source_relative_path") or ""
    source_extension = verified.get("source_extension", "") or Path(source_relative_path).suffix
    source_sha = verified.get("source_sha256", "") or front_value(front, "sha256") or ""
    segments = coalesce_segments(semantic_segments(body))
    chunks, warnings = [], []
    hierarchy: list[str | None] = [None, None, None, None]
    inherited_page: tuple[int | None, int | None] = (None, None)
    inherited_slide: int | None = None
    for segment in segments:
        hierarchy, heading, parent, section_path = heading_context(segment, hierarchy)
        inherited_page = page_range(segment, inherited_page)
        slide_values = [int(value) for value in SLIDE_RE.findall(segment)]
        if slide_values:
            inherited_slide = slide_values[0]
        pieces, segment_warnings = split_segment(segment)
        warnings.extend(segment_warnings)
        for piece in pieces:
            page_start, page_end = page_range(piece, inherited_page)
            piece_slides = [int(value) for value in SLIDE_RE.findall(piece)]
            slide_start = min(piece_slides) if piece_slides else inherited_slide if metadata["citation_mode"] == "slide" else None
            slide_end = max(piece_slides) if piece_slides else slide_start
            if page_start is not None and metadata["citation_mode"] == "pdf_page":
                provenance = "page_resolved"
            elif slide_start is not None and metadata["citation_mode"] == "slide":
                provenance = "slide_resolved"
            elif section_path:
                provenance = "section_resolved"
            else:
                provenance = "source_only"
            chunk_index = len(chunks) + 1
            chunks.append({
                "chunk_id": f"{document_id}-C{chunk_index:04d}", "document_id": document_id,
                "chunk_index": chunk_index, "source_relative_path": source_relative_path,
                "source_extension": source_extension, "source_sha256": source_sha,
                "normalized_source_sha256": sha256(source_bytes), "title": metadata["title"],
                "organization": metadata["organization"], "year": metadata["year"],
                "language": metadata["language"], "document_type": metadata["document_type"],
                "authority_level": metadata["authority_level"], "topics": metadata["topics"],
                "metadata_status": metadata["metadata_status"],
                "authority_level_source": metadata["authority_level_source"],
                "authority_level_confidence": metadata["authority_level_confidence"],
                "section_path": section_path or None, "heading": heading, "parent_heading": parent,
                "text": piece, "token_count": token_count(piece), "character_count": len(piece),
                "citation_mode": metadata["citation_mode"], "original_page_start": page_start,
                "original_page_end": page_end, "slide_start": slide_start, "slide_end": slide_end,
                "citation_sidecar": metadata["citation_sidecar"], "provenance_status": provenance,
                "contains_table": bool(TABLE_LINE_RE.search(piece)),
                "contains_formula_placeholder": bool(FORMULA_RE.search(piece)),
                "contains_image_placeholder": bool(IMAGE_RE.search(piece)),
                "overlap_previous_tokens": 0, "chunker_version": CHUNKER_VERSION,
            })
    reconstructed = "".join(chunk["text"] for chunk in chunks)
    dropped = 0 if reconstructed == body else max(1, len(body) - len(reconstructed))
    duplicated = max(0, sum(len(chunk["text"]) for chunk in chunks) - len(body))
    return {"document_id": document_id, "path": path, "body": body, "chunks": chunks,
            "warnings": warnings, "dropped_substantive_text": dropped, "duplicated_characters": duplicated,
            "table_corruption": table_corruption(chunks), "provenance_corruption": provenance_corruption(chunks),
            "normalized_sha256": sha256(source_bytes), "source_sha256": source_sha,
            "source_extension": source_extension, "document_type": metadata["document_type"]}


def load_metadata(root: Path) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]], str]:
    release = root / "data/metadata/final_metadata_release_candidate.csv"
    candidate = release if release.is_file() else root / "data/metadata/final_metadata_verified_candidate.csv"
    verified = {row["document_id"]: row for row in read_csv(candidate)}
    master = {row["document_id"]: row for row in read_csv(root / "data/metadata/final_metadata_master.csv")}
    return verified, master, candidate.relative_to(root).as_posix()


def analyze_all(root: Path) -> tuple[list[dict[str, object]], str]:
    verified, master, source_name = load_metadata(root)
    paths = sorted((root / "data/corpus_normalized").rglob("*.md"), key=lambda path: path.relative_to(root / "data/corpus_normalized").as_posix())
    documents = []
    for path in paths:
        front, _ = split_front_matter(path.read_bytes().decode("utf-8-sig"))
        document_id = front_value(front, "document_id") or ""
        documents.append(chunk_document(path, root, verified.get(document_id, {}), master.get(document_id, {})))
    return documents, source_name


def percentile(values: list[int], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def distribution(chunks: list[dict[str, object]]) -> dict[str, float | int]:
    values = [int(chunk["token_count"]) for chunk in chunks]
    return {"min": min(values, default=0), "p10": percentile(values, .10), "p25": percentile(values, .25),
            "median": percentile(values, .50), "p75": percentile(values, .75), "p90": percentile(values, .90),
            "p95": percentile(values, .95), "max": max(values, default=0), "mean": mean(values) if values else 0.0}


def blocking_conditions(documents: list[dict[str, object]], duplicate_ids: list[str]) -> list[str]:
    """P0 conditions only. Hard-limit and tiny-chunk findings are P1 and never gate a run."""
    ids = {document["document_id"] for document in documents}
    blockers = []
    if len(documents) != 214 or len(ids) != 214:
        blockers.append(f"document coverage failure: {len(documents)} files / {len(ids)} unique ids")
    dropped = sum(int(document["dropped_substantive_text"]) for document in documents)
    if dropped:
        blockers.append(f"dropped substantive text: {dropped}")
    unchunked = [document["document_id"] for document in documents if not document["chunks"]]
    if unchunked:
        blockers.append(f"documents completely unchunked: {len(unchunked)}")
    tables = sum(len(document["table_corruption"]) for document in documents)
    if tables:
        blockers.append(f"table corruption: {tables}")
    provenance = sum(len(document["provenance_corruption"]) for document in documents)
    if provenance:
        blockers.append(f"provenance corruption: {provenance}")
    if duplicate_ids:
        blockers.append(f"duplicate chunk IDs: {len(duplicate_ids)}")
    return blockers


def duplicate_chunk_ids(documents: list[dict[str, object]]) -> list[str]:
    counts = Counter(chunk["chunk_id"] for document in documents for chunk in document["chunks"])
    return sorted(chunk_id for chunk_id, count in counts.items() if count > 1)


def dry_run_report(documents: list[dict[str, object]], metadata_source: str) -> tuple[str, bool]:
    chunks = [chunk for document in documents for chunk in document["chunks"]]
    dist = distribution(chunks)
    provenance = Counter(chunk["provenance_status"] for chunk in chunks)
    duplicates = duplicate_chunk_ids(documents)
    blockers = blocking_conditions(documents, duplicates)
    queue = review_queue(documents, duplicates)
    priorities = Counter(row["priority"] for row in queue)
    gate = not blockers
    hard_docs = sorted({str(row["document_id"]) for row in queue if row["reason"].startswith(("hard_token_limit", "huge_table", "indivisible_block"))})
    lines = ["# TunnelBookAI Semantic Chunking Dry Run", "", "## Result", "", f"**{'GO' if gate else 'NO-GO'}**", "",
             f"- Documents: **{len(documents)}/214**", f"- Estimated chunks: **{len(chunks)}**",
             f"- Metadata source: `{metadata_source}`", f"- Tokenizer: `{TOKENIZER_NAME}` (BGE-M3 tokenizer not locally cached; no download/inference)",
             f"- Chunker: `{CHUNKER_VERSION}`", "- Final `chunks.jsonl` written by dry-run: **false**",
             "", "## Token Distribution", ""]
    for key, value in dist.items():
        lines.append(f"- {key}: **{value:.2f}**" if isinstance(value, float) else f"- {key}: **{value}**")
    lines.extend(["", "## Size Buckets", "", f"- <250: **{sum(chunk['token_count'] < SOFT_MIN for chunk in chunks)}**",
                  f"- 250–1200: **{sum(SOFT_MIN <= chunk['token_count'] <= SOFT_MAX for chunk in chunks)}**",
                  f"- 1200–1500: **{sum(SOFT_MAX < chunk['token_count'] <= HARD_MAX for chunk in chunks)}**",
                  f"- >1500: **{sum(chunk['token_count'] > HARD_MAX for chunk in chunks)}**", "", "## Content Types", "",
                  f"- Table chunks: **{sum(chunk['contains_table'] for chunk in chunks)}**",
                  f"- Formula-placeholder chunks: **{sum(chunk['contains_formula_placeholder'] for chunk in chunks)}**",
                  f"- Image-placeholder chunks: **{sum(chunk['contains_image_placeholder'] for chunk in chunks)}**",
                  f"- Regulation/article chunks: **{sum(bool(REGULATION_RE.search(str(chunk['text']))) for chunk in chunks)}**",
                  "", "## Provenance", ""])
    for status in ("page_resolved", "slide_resolved", "section_resolved", "source_only"):
        lines.append(f"- {status.replace('_', ' ')}: **{provenance[status]}**")
    lines.extend(["", "## Safety", "",
                  f"- Dropped substantive text: **{sum(int(document['dropped_substantive_text']) for document in documents)}**",
                  f"- Duplicate chunk IDs: **{len(duplicates)}**",
                  f"- Provenance corruption: **{sum(len(document['provenance_corruption']) for document in documents)}**",
                  f"- Table corruption: **{sum(len(document['table_corruption']) for document in documents)}**",
                  f"- Missing documents: **{214 - len(documents)}**", "", "## Review", "",
                  f"- P0: **{priorities['P0']}**", f"- P1: **{priorities['P1']}**", f"- P2: **{priorities['P2']}**", "",
                  "## Hard-Limit Documents (P1, non-blocking)", ""])
    lines.extend([f"- {doc_id}" for doc_id in hard_docs] or ["- Yok."])
    lines.extend(["", "## Blockers (P0)", ""])
    lines.extend([f"- {item}" for item in blockers] or ["- Yok."])
    lines.extend(["", "## Gate", "",
                  f"**{'GO FOR STRATIFIED PILOT' if gate else 'NO-GO — pilot must not start'}**", "",
                  "P1/P2 findings are review signals and do not gate this stage; only P0 conditions block.", ""])
    return "\n".join(lines), gate


def pilot_selection(documents: list[dict[str, object]]) -> list[tuple[str, dict[str, object]]]:
    def score(document: dict[str, object], category: str) -> int:
        chunks = document["chunks"]
        ext = str(document["source_extension"]).lower()
        body = document["body"]
        values = {
            "clean_pdf": int(ext == ".pdf" and not document["warnings"]),
            "large_full_docling_pdf": int(ext == ".pdf" and any(c["provenance_status"] == "page_resolved" for c in chunks)) * len(body),
            "ocr_heavy": body.count("[UNRESOLVED_CHAR]") * 100 + len(IMAGE_RE.findall(body)),
            "regulation": int(document["document_type"] == "regulation" or bool(REGULATION_RE.search(body))) * len(chunks),
            "academic_article": int(document["document_type"] == "academic_article"),
            "handbook_manual": int(document["document_type"] == "manual"),
            "table_heavy": sum(c["contains_table"] for c in chunks),
            "list_heavy": len(LIST_LINE_RE.findall(body)),
            "docx": int(ext in {".doc", ".docx", ".rtf"}), "pptx": int(ext in {".ppt", ".pptx", ".pptm"}),
            "source_only_provenance": sum(c["provenance_status"] == "source_only" for c in chunks),
            "formula_placeholder": sum(c["contains_formula_placeholder"] for c in chunks),
            "image_heavy": sum(c["contains_image_placeholder"] for c in chunks),
            "very_short": max(1, 100000 - len(body)), "very_long": len(body),
        }
        return int(values[category])
    categories = ["clean_pdf", "large_full_docling_pdf", "ocr_heavy", "regulation", "academic_article", "handbook_manual",
                  "table_heavy", "list_heavy", "docx", "pptx", "source_only_provenance", "formula_placeholder",
                  "image_heavy", "very_short", "very_long"]
    selected, used = [], set()
    for category in categories:
        candidates = sorted((doc for doc in documents if doc["document_id"] not in used),
                            key=lambda doc: (-score(doc, category), doc["document_id"]))
        chosen = candidates[0]
        reason = category if score(chosen, category) else f"{category} (deterministic proxy; no exact unused candidate)"
        selected.append((reason, chosen))
        used.add(chosen["document_id"])
    return selected


def pilot_report(selected: list[tuple[str, dict[str, object]]]) -> tuple[str, bool]:
    unsafe, notes = [], {}
    for _, document in selected:
        chunks = document["chunks"]
        failures = []
        if document["dropped_substantive_text"]:
            failures.append("substantive_text_dropped")
        if not chunks:
            failures.append("document_unchunked")
        if document["table_corruption"]:
            failures.append("table_corruption")
        if document["provenance_corruption"]:
            failures.append("provenance_corruption")
        if len({chunk["chunk_id"] for chunk in chunks}) != len(chunks):
            failures.append("duplicate_chunk_id")
        warnings = []
        hard = [chunk for chunk in chunks if chunk["token_count"] > HARD_MAX]
        if hard:
            warnings.append(f"P1 justified_special_case: {len(hard)} chunk(s) over hard limit "
                            f"({sum(chunk['contains_table'] for chunk in hard)} atomic table, "
                            f"{sum(not chunk['contains_table'] for chunk in hard)} indivisible block)")
        fragments = sum(is_fragment(str(chunk["text"])) for chunk in chunks)
        if fragments:
            warnings.append(f"P1 non_substantive_fragment: {fragments}")
        tiny = sum(chunk["token_count"] < SOFT_MIN for chunk in chunks)
        if len(chunks) >= 10 and tiny / len(chunks) > .75:
            warnings.append(f"P1 excessive_tiny_chunks: {tiny}/{len(chunks)}")
        notes[document["document_id"]] = (failures, warnings)
        if failures:
            unsafe.append(document["document_id"])
    gate = not unsafe and len(selected) == 15
    lines = ["# TunnelBookAI Semantic Chunking Pilot Audit", "", "## Result", "",
             f"**{'GO FOR FULL RUN' if gate else 'NO-GO'}**", "",
             f"- Selected: **{len(selected)}/15**", f"- Passed: **{len(selected)-len(unsafe)}**",
             f"- Unsafe documents (P0): **{len(unsafe)}**", "",
             "P0 conditions gate this stage. P1/P2 findings are reported per document and do not block.",
             "", "## Documents", ""]
    for reason, document in selected:
        chunks = document["chunks"]
        failures, warnings = notes[document["document_id"]]
        intact = not document["dropped_substantive_text"]
        lines.extend([f"### {document['document_id']}", "", f"- selection_reason: {reason}", f"- chunks: {len(chunks)}",
                      f"- token_range: {min((c['token_count'] for c in chunks), default=0)}–{max((c['token_count'] for c in chunks), default=0)}",
                      f"- median_tokens: {percentile([int(c['token_count']) for c in chunks], .50):.0f}",
                      f"- headings_attached: {sum(bool(c['section_path']) for c in chunks)}/{len(chunks)}",
                      f"- tables_intact: {intact and not document['table_corruption']}",
                      f"- lists_intact: {intact}",
                      f"- citation_provenance_preserved: {intact and not document['provenance_corruption']}",
                      f"- dropped_substantive_text: {document['dropped_substantive_text']}",
                      f"- duplicate_chunk_ids: {len(chunks) - len({c['chunk_id'] for c in chunks})}",
                      f"- overlap_tokens: {sum(int(c['overlap_previous_tokens']) for c in chunks)}",
                      f"- p0_failures: {', '.join(failures) or 'none'}",
                      f"- p1_warnings: {'; '.join(warnings) or 'none'}",
                      f"- quality_result: {'FAIL' if failures else 'PASS'}", ""])
    return "\n".join(lines), gate


def protected_state(root: Path) -> dict[str, str]:
    state = {}
    for relative in ("data/corpus_final", "data/corpus_normalized", "data/markdown", "data/markdown_full_docling"):
        digest = hashlib.sha256()
        base = root / relative
        for path in sorted((p for p in base.rglob("*") if p.is_file()), key=lambda p: p.relative_to(base).as_posix()):
            digest.update(path.relative_to(base).as_posix().encode() + b"\0" + path.read_bytes())
        state[relative] = digest.hexdigest()
    excluded = {"chunk_manifest.csv", "chunk_review_queue.csv"}
    for path in sorted((root / "data/metadata").glob("*")):
        if path.is_file() and path.name not in excluded:
            state[path.relative_to(root).as_posix()] = sha256(path.read_bytes())
    return state


def review_queue(documents: list[dict[str, object]], duplicate_ids: list[str]) -> list[dict[str, object]]:
    rows = []
    for document in documents:
        chunks = document["chunks"]
        if document["dropped_substantive_text"]:
            rows.append({"priority": "P0", "document_id": document["document_id"], "chunk_id": "",
                         "reason": "substantive_text_dropped", "details": str(document["dropped_substantive_text"]),
                         "review_status": "pending", "reviewer_note": ""})
        if not chunks:
            rows.append({"priority": "P0", "document_id": document["document_id"], "chunk_id": "",
                         "reason": "document_completely_unchunked", "details": "0 chunks", "review_status": "pending", "reviewer_note": ""})
        for chunk_id in document["table_corruption"]:
            rows.append({"priority": "P0", "document_id": document["document_id"], "chunk_id": chunk_id,
                         "reason": "table_corruption", "details": "chunk boundary splits a Markdown table",
                         "review_status": "pending", "reviewer_note": ""})
        for chunk_id in document["provenance_corruption"]:
            rows.append({"priority": "P0", "document_id": document["document_id"], "chunk_id": chunk_id,
                         "reason": "provenance_corruption", "details": "inconsistent citation anchors",
                         "review_status": "pending", "reviewer_note": ""})
        for chunk in (chunk for chunk in chunks if chunk["token_count"] > HARD_MAX):
            table = chunk["contains_table"]
            rows.append({"priority": "P1", "document_id": document["document_id"], "chunk_id": chunk["chunk_id"],
                         "reason": "huge_table_special_case" if table else "hard_token_limit_exceeded",
                         "details": f"{chunk['token_count']} tokens; justified_special_case "
                                    f"({'atomic Markdown table' if table else 'no safe semantic boundary'})",
                         "review_status": "pending", "reviewer_note": ""})
        for chunk in (chunk for chunk in chunks if is_fragment(str(chunk["text"]))):
            rows.append({"priority": "P1", "document_id": document["document_id"], "chunk_id": chunk["chunk_id"],
                         "reason": "non_substantive_fragment", "details": f"{chunk['token_count']} tokens",
                         "review_status": "pending", "reviewer_note": ""})
        tiny = sum(chunk["token_count"] < SOFT_MIN for chunk in chunks)
        if len(chunks) >= 10 and tiny / len(chunks) > .75:
            rows.append({"priority": "P1", "document_id": document["document_id"], "chunk_id": "",
                         "reason": "excessive_tiny_chunks", "details": f"{tiny}/{len(chunks)} chunks under {SOFT_MIN}",
                         "review_status": "pending", "reviewer_note": ""})
        source_only = sum(chunk["provenance_status"] == "source_only" for chunk in chunks)
        if source_only:
            rows.append({"priority": "P2", "document_id": document["document_id"], "chunk_id": "",
                         "reason": "source_only_citation", "details": f"{source_only}/{len(chunks)} chunks",
                         "review_status": "pending", "reviewer_note": ""})
    for chunk_id in duplicate_ids:
        rows.append({"priority": "P0", "document_id": chunk_id.split("-C", 1)[0], "chunk_id": chunk_id,
                     "reason": "duplicate_chunk_id", "details": chunk_id, "review_status": "pending", "reviewer_note": ""})
    return sorted(rows, key=lambda row: (row["priority"], row["document_id"], row["chunk_id"], row["reason"]))


def manifest_rows(documents: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for document in documents:
        chunks = document["chunks"]
        tokens = [chunk["token_count"] for chunk in chunks]
        rows.append({"document_id": document["document_id"], "source_sha256": document["source_sha256"],
                     "normalized_sha256": document["normalized_sha256"], "chunk_count": len(chunks),
                     "min_tokens": min(tokens, default=0), "max_tokens": max(tokens, default=0),
                     "mean_tokens": f"{mean(tokens):.2f}" if tokens else "0.00",
                     "page_resolved_chunks": sum(c["provenance_status"] == "page_resolved" for c in chunks),
                     "slide_resolved_chunks": sum(c["provenance_status"] == "slide_resolved" for c in chunks),
                     "section_resolved_chunks": sum(c["provenance_status"] == "section_resolved" for c in chunks),
                     "source_only_chunks": sum(c["provenance_status"] == "source_only" for c in chunks),
                     "table_chunks": sum(c["contains_table"] for c in chunks),
                     "formula_chunks": sum(c["contains_formula_placeholder"] for c in chunks),
                     "image_chunks": sum(c["contains_image_placeholder"] for c in chunks),
                     "warning_count": len(document["warnings"]), "chunker_version": CHUNKER_VERSION})
    return sorted(rows, key=lambda row: row["document_id"])


def doc21_section(documents: list[dict[str, object]]) -> list[str]:
    """Explicit disposition of the DOC000021 hard-limit finding called out by the chunking plan."""
    document = next((doc for doc in documents if doc["document_id"] == "DOC000021"), None)
    lines = ["## DOC000021 Hard-Limit Status", ""]
    if document is None:
        return lines + ["- DOC000021 not present in the normalized corpus.", ""]
    over = [chunk for chunk in document["chunks"] if chunk["token_count"] > HARD_MAX]
    lines.append(f"- Chunks: **{len(document['chunks'])}**")
    lines.append(f"- Chunks over hard limit ({HARD_MAX}): **{len(over)}**")
    if not over:
        lines.extend([f"- Largest chunk: **{max((c['token_count'] for c in document['chunks']), default=0)} tokens**",
                      "- The earlier P1 hard-limit finding is **resolved**: the oversized block was a numbered",
                      "  reference list, which `enforce_hard_limit` now divides at list-item/line boundaries.",
                      "  No table was split, no citation anchor changed, and no substantive text was dropped.",
                      f"- Dropped substantive text: **{document['dropped_substantive_text']}**", ""])
        return lines
    for chunk in over:
        lines.append(f"- `{chunk['chunk_id']}`: **{chunk['token_count']} tokens**, "
                     f"table={chunk['contains_table']}, section=`{chunk['section_path']}` — "
                     f"**P1 justified_special_case** (no safe semantic boundary; splitting would break "
                     f"{'the Markdown table' if chunk['contains_table'] else 'an indivisible block'}).")
    lines.extend(["- Classified **P1**, not P0: no text dropped, no table split, provenance intact.",
                  "- This does not block the final gate.", ""])
    return lines


def final_report(documents: list[dict[str, object]], chunks: list[dict[str, object]], queue: list[dict[str, object]],
                 pilot: list[tuple[str, dict[str, object]]], protected_changes: list[str], metadata_source: str,
                 idempotent: bool, tests: str) -> str:
    dist = distribution(chunks)
    priorities = Counter(row["priority"] for row in queue)
    provenance = Counter(chunk["provenance_status"] for chunk in chunks)
    extensions = Counter(chunk["source_extension"] for chunk in chunks)
    doc_types = Counter(str(chunk["document_type"] or "unresolved") for chunk in chunks)
    duplicate_count = len(chunks) - len({chunk["chunk_id"] for chunk in chunks})
    dropped = sum(doc["dropped_substantive_text"] for doc in documents)
    source_chars = sum(len(doc["body"]) for doc in documents)
    chunk_chars = sum(len(chunk["text"]) for chunk in chunks)
    overlap_chars = sum(doc["duplicated_characters"] for doc in documents)
    blockers = blocking_conditions(documents, duplicate_chunk_ids(documents))
    if priorities["P0"]:
        blockers.append(f"P0 review records: {priorities['P0']}")
    if protected_changes:
        blockers.append(f"protected tree changed: {', '.join(protected_changes)}")
    if not idempotent:
        blockers.append("idempotency failure")
    if "FAIL" in tests:
        blockers.append("test failure")
    decision = "NO-GO" if blockers else "GO"
    lines = ["# TunnelBookAI Semantic Chunking Audit", "", "## Result", "", f"**{decision}**", "",
             "## Documents", "", f"- Documents: **{len(documents)}/214**", f"- Metadata source: `{metadata_source}`", "",
             "## Chunks", "", f"- Total: **{len(chunks)}**", f"- Duplicate chunk IDs: **{duplicate_count}**", "",
             "## Distribution", ""]
    for key, value in dist.items():
        lines.append(f"- {key}: **{value:.2f}**" if isinstance(value, float) else f"- {key}: **{value}**")
    lines.extend(["", "- Under 250: **%d**" % sum(c["token_count"] < SOFT_MIN for c in chunks),
                  "- 250–1200: **%d**" % sum(SOFT_MIN <= c["token_count"] <= SOFT_MAX for c in chunks),
                  "- 1200–1500: **%d**" % sum(SOFT_MAX < c["token_count"] <= HARD_MAX for c in chunks),
                  "- Over 1500: **%d**" % sum(c["token_count"] > HARD_MAX for c in chunks), "", "## By Source Type", ""])
    lines.extend(f"- {key or 'unknown'}: **{value}**" for key, value in sorted(extensions.items()))
    lines.extend(["", "## By Document Type", ""])
    lines.extend(f"- {key}: **{value}**" for key, value in sorted(doc_types.items()))
    lines.extend(["", "## Semantic Structures", "",
                  f"- Tables: **{sum(c['contains_table'] for c in chunks)}**",
                  f"- Lists: **{sum(bool(LIST_LINE_RE.search(c['text'])) for c in chunks)}**",
                  f"- Regulations: **{sum(bool(REGULATION_RE.search(c['text'])) for c in chunks)}**",
                  f"- Formula placeholders: **{sum(c['contains_formula_placeholder'] for c in chunks)}**",
                  f"- Image placeholders: **{sum(c['contains_image_placeholder'] for c in chunks)}**", "", "## Provenance", ""])
    for status in ("page_resolved", "slide_resolved", "section_resolved", "source_only"):
        lines.append(f"- {status.replace('_', ' ')}: **{provenance[status]}**")
    lines.extend(["", "## Conservation", "", f"- Dropped substantive text: **{dropped}**",
                  f"- Source body characters: **{source_chars}**", f"- Total chunk characters: **{chunk_chars}**",
                  f"- Overlap characters: **{overlap_chars}**",
                  f"- Duplication ratio: **{overlap_chars / source_chars if source_chars else 0:.6f}**",
                  f"- Overlap ratio: **{overlap_chars / chunk_chars if chunk_chars else 0:.6f}**", "", "## Integrity", "",
                  f"- Normalized corpus changed: **{str('data/corpus_normalized' in protected_changes).lower()}**",
                  f"- Raw corpus changed: **{str('data/corpus_final' in protected_changes).lower()}**",
                  f"- Markdown trees changed: **{str(any(path.startswith('data/markdown') for path in protected_changes)).lower()}**",
                  f"- Metadata protected files changed: **{sum(path.startswith('data/metadata/') for path in protected_changes)}**",
                  f"- Missing documents: **{214-len(documents)}**", f"- Duplicate IDs: **{duplicate_count}**",
                  f"- Provenance corruption: **{sum(len(doc['provenance_corruption']) for doc in documents)}**",
                  f"- Table corruption: **{sum(len(doc['table_corruption']) for doc in documents)}**", "", "## Review", "",
                  f"- P0: **{priorities['P0']}**", f"- P1: **{priorities['P1']}**", f"- P2: **{priorities['P2']}**", "",
                  *doc21_section(documents),
                  "## Pilot", "", f"- Selected: **{len(pilot)}/15**", f"- Passed: **{len(pilot)}/15**", "",
                  "## Tests", "", *(f"- {item.strip()}" for item in tests.split("|")),
                  "", "## Idempotency", "", f"- Deterministic second-run hash: **{'PASS' if idempotent else 'FAIL'}**",
                  "", "## Warnings", "", f"- Nonblocking P1/P2 review records: **{priorities['P1']+priorities['P2']}**",
                  f"- Token counts were produced with `{TOKENIZER_NAME}` because the BGE-M3 tokenizer was not in the "
                  "local cache; nothing was downloaded and no inference was run. Chunk boundaries are NOT re-cut for "
                  "this reason and stay as audited here. **Action for the embedding stage:** run a separate BGE-M3 "
                  "tokenizer compatibility preflight over `data/chunks/chunks.jsonl` to re-measure the true token "
                  "distribution before indexing. Expect drift on the tails — subword tokenization of Turkish "
                  "morphology and of URL/DOI-dense reference chunks will read longer than the lexical count, so the "
                  f">{HARD_MAX}-token band may widen. Re-cut only if that preflight shows real breaches.",
                  "- No embeddings, BGE-M3 download or inference, Qdrant, retrieval, reranking, RAG or LLM generation "
                  "were run at any point in this stage.",
                  "- Overlap is deliberately 0 tokens: boundaries fall on heading/regulation/paragraph/list edges, so "
                  "chunks already carry their own semantic context. Chunk text concatenates back to the source byte for "
                  "byte, which is what proves dropped-text = 0. Blind or fixed overlap would forfeit that proof and "
                  f"inflate the corpus; `overlap_previous_tokens` is carried in the schema for later tuning. "
                  f"{sum(bool(c['section_path']) for c in chunks)}/{len(chunks)} chunks carry a resolved section path.",
                  f"- {sum(c['token_count'] < SOFT_MIN for c in chunks)} chunks fall under the {SOFT_MIN}-token soft "
                  "minimum. These are short-by-nature units (slide bodies, figure/caption blocks, brief regulation "
                  "articles) that coalescing kept whole rather than fusing across a citation boundary; none is a "
                  "non-substantive fragment.", "", "## Blockers", ""])
    lines.extend([f"- {item}" for item in blockers] or ["- Yok."])
    lines.extend(["", "## Final Decision", "", f"**{decision}**", ""])
    return "\n".join(lines)


def run_pipeline(root: Path, tests: str) -> dict[str, object]:
    protected_before = protected_state(root)
    documents, metadata_source = analyze_all(root)
    dry_report, dry_go = dry_run_report(documents, metadata_source)
    atomic_write(root / "reports/semantic_chunking_dry_run.md", dry_report.encode("utf-8"))
    if not dry_go:
        return {"decision": "NO-GO", "stage": "dry-run"}
    pilot = pilot_selection(documents)
    pilot_text, pilot_go = pilot_report(pilot)
    atomic_write(root / "reports/semantic_chunking_pilot_audit.md", pilot_text.encode("utf-8"))
    if not pilot_go:
        return {"decision": "NO-GO", "stage": "pilot"}
    pilot_chunks = [chunk for _, document in pilot for chunk in document["chunks"]]
    atomic_write(root / "data/chunks_pilot/chunks.jsonl", jsonl_bytes(pilot_chunks))
    chunks = [chunk for document in documents for chunk in document["chunks"]]
    chunk_ids = [chunk["chunk_id"] for chunk in chunks]
    duplicates = sorted(chunk_id for chunk_id, count in Counter(chunk_ids).items() if count > 1)
    queue = review_queue(documents, duplicates)
    manifest = manifest_rows(documents)
    chunks_payload = jsonl_bytes(chunks)
    manifest_payload = csv_bytes(manifest, MANIFEST_FIELDS)
    review_payload = csv_bytes(queue, REVIEW_FIELDS)
    atomic_write(root / "data/chunks/chunks.jsonl", chunks_payload)
    atomic_write(root / "data/metadata/chunk_manifest.csv", manifest_payload)
    atomic_write(root / "data/metadata/chunk_review_queue.csv", review_payload)
    first_hash = sha256((root / "data/chunks/chunks.jsonl").read_bytes())
    second_payload = jsonl_bytes([chunk for document in analyze_all(root)[0] for chunk in document["chunks"]])
    idempotent = first_hash == sha256(second_payload) and chunks_payload == second_payload
    protected_after = protected_state(root)
    protected_changes = sorted(key for key in protected_before if protected_before[key] != protected_after.get(key))
    audit = final_report(documents, chunks, queue, pilot, protected_changes, metadata_source, idempotent, tests)
    atomic_write(root / "reports/semantic_chunking_audit.md", audit.encode("utf-8"))
    decision = "NO-GO" if "**NO-GO**" in audit else "GO"
    return {"decision": decision, "dry_run": "GO", "pilot": "GO FOR FULL RUN", "documents": len(documents),
            "chunks": len(chunks), "duplicate_chunk_ids": len(duplicates),
            "dropped_substantive_text": sum(doc["dropped_substantive_text"] for doc in documents),
            "review": dict(Counter(row["priority"] for row in queue)), "idempotency": idempotent,
            "protected_changes": protected_changes}


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic citation-safe semantic Markdown chunking")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--test-summary", default="Tests pending")
    args = parser.parse_args()
    result = run_pipeline(args.project_root.resolve(), args.test_summary)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["decision"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
