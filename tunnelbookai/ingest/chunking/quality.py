"""Chunk quality gate (task §63).

Validates, per document:

    chunk ids unique                source element refs resolve
    no empty chunks                 document_id matches
    token sizes within policy       section ids valid in the canonical taxonomy
    provenance present              no duplicate-text flood

Writes `processing/<document_id>/chunk_quality.json`.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from ..classify.taxonomy import is_valid_section
from . import tokenizer
from .chunker import _shingles, _jaccard
from .policy import CHUNK_TYPES, ChunkPolicy, normalize_for_id

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"

DUPLICATE_FLOOD_RATIO = 0.25


def evaluate(
    *,
    document_id: str,
    chunks: list[dict[str, Any]],
    elements: list[dict[str, Any]],
    tables: list[dict[str, Any]],
    figures: list[dict[str, Any]],
    sheets: list[dict[str, Any]],
    slides: list[dict[str, Any]],
    policy: ChunkPolicy,
    dropped: list[dict[str, Any]] | None = None,
    trusted_source_refs: set[str] | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    known_refs = {e["element_id"] for e in elements}
    known_refs |= {e.get("asset_id") for e in elements if e.get("asset_id")}
    known_refs |= {t.get("table_id") or t.get("asset_id") for t in tables}
    known_refs |= {f.get("asset_id") for f in figures}
    known_refs |= {s.get("asset_id") for s in sheets}
    known_refs |= {f"SHEET:{s.get('sheet_name')}" for s in sheets}
    known_refs |= {f"SLIDE{int(s['slide_number']):04d}" for s in slides
                   if s.get("slide_number") is not None}
    known_refs |= {f"OCRPAGE{int(c.get('page') or 0):04d}" for c in chunks}
    known_refs |= {c.get("ocr_item_id") for c in chunks if c.get("ocr_item_id")}
    known_refs |= set(trusted_source_refs or ())
    known_refs.discard(None)

    ids = [c["chunk_id"] for c in chunks]
    duplicates = [cid for cid, count in Counter(ids).items() if count > 1]
    if duplicates:
        errors.append(f"DUPLICATE_CHUNK_IDS:{len(duplicates)}")

    token_counts: list[int] = []
    for index, chunk in enumerate(chunks):
        cid = chunk.get("chunk_id", "?")
        if chunk.get("document_id") != document_id:
            errors.append(f"DOCUMENT_ID_MISMATCH:{cid}")
        if chunk.get("chunk_type") not in CHUNK_TYPES:
            errors.append(f"UNKNOWN_CHUNK_TYPE:{cid}:{chunk.get('chunk_type')}")
        text = (chunk.get("text") or "").strip()
        if not text:
            errors.append(f"EMPTY_CHUNK:{cid}")
            continue
        recomputed = tokenizer.count(chunk["text"])
        if recomputed != chunk.get("token_count"):
            errors.append(f"TOKEN_COUNT_MISMATCH:{cid}")
        token_counts.append(recomputed)
        if recomputed > policy.hard_max_tokens:
            errors.append(f"CHUNK_OVER_HARD_MAX:{cid}:{recomputed}")
        elif recomputed > policy.max_tokens:
            warnings.append(f"CHUNK_OVER_MAX:{cid}:{recomputed}")
        elif recomputed < policy.min_tokens and chunk["chunk_type"] == "TEXT_CHUNK":
            # A short fragment is actionable only when it can be merged without
            # crossing a heading boundary or the normal maximum.  Standalone
            # abstracts, captions and short terminal sections are valid evidence.
            mergeable = any(
                0 <= neighbour < len(chunks)
                and chunks[neighbour].get("chunk_type") == "TEXT_CHUNK"
                and chunks[neighbour].get("heading_path") == chunk.get("heading_path")
                and recomputed + int(chunks[neighbour].get("token_count") or 0)
                    <= policy.max_tokens
                for neighbour in (index - 1, index + 1)
            )
            code = "CHUNK_UNDER_MIN" if mergeable else "CHUNK_SHORT_STRUCTURAL"
            warnings.append(f"{code}:{cid}:{recomputed}")

        unresolved = [r for r in (chunk.get("source_elements") or []) if r not in known_refs]
        if unresolved:
            errors.append(f"UNRESOLVED_SOURCE_ELEMENTS:{cid}:{','.join(unresolved[:3])}")
        if not chunk.get("source_elements"):
            errors.append(f"NO_SOURCE_ELEMENTS:{cid}")

        provenance = chunk.get("provenance") or {}
        if not provenance.get("original_sha256") or not provenance.get("source_kind"):
            errors.append(f"CHUNK_PROVENANCE_MISSING:{cid}")

        primary = chunk.get("final_primary_section")
        if primary is not None and not is_valid_section(primary):
            errors.append(f"INVALID_SECTION:{cid}:{primary}")
        for secondary in chunk.get("final_secondary_sections") or []:
            if not is_valid_section(secondary):
                errors.append(f"INVALID_SECONDARY_SECTION:{cid}:{secondary}")

        if not chunk.get("chunk_schema_version") or not chunk.get("chunk_policy_version"):
            errors.append(f"CHUNK_POLICY_VERSION_MISSING:{cid}")

    # duplicate-text flood: a re-check that dedup actually held (§60, §63)
    flood = 0
    shingles = [_shingles(c.get("text", ""), policy.dedup_shingle) for c in chunks]
    for i in range(len(chunks)):
        for j in range(i + 1, len(chunks)):
            if _jaccard(shingles[i], shingles[j]) >= policy.dedup_threshold:
                flood += 1
    if chunks and flood > max(1, int(len(chunks) * DUPLICATE_FLOOD_RATIO)):
        errors.append(f"DUPLICATE_TEXT_FLOOD:{flood}")
    elif flood:
        warnings.append(f"NEAR_DUPLICATE_PAIRS:{flood}")

    exact = len(chunks) - len({normalize_for_id(c.get("text", "")) for c in chunks})
    if exact > 0:
        errors.append(f"EXACT_DUPLICATE_TEXT:{exact}")

    status = FAIL if errors else (WARN if warnings else PASS)
    by_type = Counter(c.get("chunk_type") for c in chunks)
    return {
        "document_id": document_id,
        "status": status,
        "chunk_count": len(chunks),
        "chunks_by_type": dict(by_type),
        "token_stats": {
            "min": min(token_counts) if token_counts else 0,
            "max": max(token_counts) if token_counts else 0,
            "mean": round(sum(token_counts) / len(token_counts), 1) if token_counts else 0,
            "total": sum(token_counts),
        },
        "policy": {
            "chunk_schema_version": policy.schema_version,
            "chunk_policy_version": policy.policy_version,
            "tokenizer": policy.tokenizer_name,
            "target_tokens": policy.target_tokens,
            "min_tokens": policy.min_tokens,
            "max_tokens": policy.max_tokens,
            "hard_max_tokens": policy.hard_max_tokens,
            "overlap_tokens": policy.overlap_tokens,
        },
        "deduplicated_chunks": list(dropped or []),
        "errors": errors,
        "warnings": warnings,
    }


def write_report(bundle: Path, report: dict[str, Any]) -> Path:
    bundle.mkdir(parents=True, exist_ok=True)
    path = bundle / "chunk_quality.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
