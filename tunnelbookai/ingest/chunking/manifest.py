"""Embedding-ready manifest (task §64).

One row per chunk in `audit/embedding_ready_manifest.jsonl`. This engine decides ELIGIBILITY
and prepares `embedding_text`; it does NOT compute embeddings and does not touch Qdrant.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import tokenizer
from .policy import ChunkPolicy

READY = "READY"
TOO_SHORT = "TOO_SHORT"
TYPE_EXCLUDED = "TYPE_EXCLUDED"
NO_SECTION = "NO_SECTION"
CHUNK_QUALITY_FAILED = "CHUNK_QUALITY_FAILED"
DOCUMENT_NOT_STAGED = "DOCUMENT_NOT_STAGED"


def embedding_text(chunk: dict[str, Any]) -> str:
    """Retrieval text: heading path + modality context + body, in that order."""
    parts: list[str] = []
    heading_path = chunk.get("heading_path") or []
    if heading_path:
        parts.append(" > ".join(str(h) for h in heading_path))
    chunk_type = chunk.get("chunk_type")
    if chunk_type == "TABLE_CHUNK" and chunk.get("caption"):
        parts.append(f"Tablo: {chunk['caption']}")
    elif chunk_type == "FIGURE_CHUNK" and chunk.get("caption"):
        parts.append(f"Şekil: {chunk['caption']}")
    elif chunk_type == "SLIDE_CHUNK" and chunk.get("slide_title"):
        parts.append(f"Slayt {chunk.get('slide_number')}: {chunk['slide_title']}")
    elif chunk_type == "SHEET_CHUNK" and chunk.get("sheet_name"):
        parts.append(f"Çalışma sayfası: {chunk['sheet_name']}")
    parts.append(chunk.get("text") or "")
    return "\n".join(p for p in parts if p).strip()


def row_for(chunk: dict[str, Any], policy: ChunkPolicy, *,
            document_staged: bool = True, chunk_quality_ok: bool = True) -> dict[str, Any]:
    text = embedding_text(chunk)
    tokens = tokenizer.count(text)
    eligible = True
    reason = READY
    if not document_staged:
        eligible, reason = False, DOCUMENT_NOT_STAGED
    elif not chunk_quality_ok:
        eligible, reason = False, CHUNK_QUALITY_FAILED
    elif not policy.allows(chunk.get("chunk_type", "")):
        eligible, reason = False, TYPE_EXCLUDED
    elif tokens < policy.embedding_min_tokens:
        eligible, reason = False, TOO_SHORT
    elif not chunk.get("final_primary_section"):
        eligible, reason = False, NO_SECTION

    return {
        "chunk_id": chunk["chunk_id"],
        "document_id": chunk["document_id"],
        "chunk_type": chunk.get("chunk_type"),
        "section_id": chunk.get("final_primary_section"),
        "secondary_section_ids": list(chunk.get("final_secondary_sections") or []),
        "ordinal": chunk.get("ordinal"),
        "text_path": None,
        "embedding_text": text,
        "token_count": tokens,
        "page_start": chunk.get("page_start"),
        "page_end": chunk.get("page_end"),
        "slide_number": chunk.get("slide_number"),
        "sheet_name": chunk.get("sheet_name"),
        "provenance": chunk.get("provenance"),
        "chunk_schema_version": chunk.get("chunk_schema_version"),
        "chunk_policy_version": chunk.get("chunk_policy_version"),
        "eligible": eligible,
        "reason": reason,
    }


def build_rows(chunks: list[dict[str, Any]], policy: ChunkPolicy, *,
               document_staged: bool = True, chunk_quality_ok: bool = True
               ) -> list[dict[str, Any]]:
    return [row_for(c, policy, document_staged=document_staged,
                    chunk_quality_ok=chunk_quality_ok) for c in chunks]


def merge_into(path: Path, rows: list[dict[str, Any]], *, document_ids: set[str]) -> int:
    """Rewrite the manifest, replacing every row belonging to `document_ids`."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("document_id") not in document_ids:
                existing.append(row)
    existing += rows
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        for row in existing:
            handle.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
    tmp.replace(path)
    return len(existing)
