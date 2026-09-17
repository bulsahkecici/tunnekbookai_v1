#!/usr/bin/env python3
"""Deterministic lexical smoke test over the verified canonical corpus.

This is an acceptance check for canonical content and section routing.  It is not the
future embedding/vector-based Book Retrieval Layer.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tunnelbookai.canonical.verifier import require_ready


CASES = (
    {
        "id": "chapter_3_history",
        "section_prefix": "3",
        "query": "Karayolları Genel Müdürlüğü KGM tünellerinin tarihçesi Ovit Zigana",
        "expected_document_ids": ["ING_62c2a5de1e2d13c0013a", "ING_7d7c44992e83c7185c41"],
    },
    {
        "id": "chapter_4_transport_cost",
        "section_prefix": "4",
        "query": "ulaşım maliyetleri yaşam döngüsü maliyet kavramı",
        "expected_document_ids": [],
    },
    {
        "id": "chapter_5_maintenance",
        "section_prefix": "5",
        "query": "tünel bakım işletme enerji maliyeti periyodik bakım",
        "expected_document_ids": [],
    },
    {
        "id": "chapter_6_construction_cost",
        "section_prefix": "6",
        "query": "tünel yapım maliyeti birim fiyat püskürtme beton destek",
        "expected_document_ids": [
            "ING_0f9fb625ee12d331f34a",
            "ING_29dc43677cbbd95c697d",
            "ING_5c2983ff4ac61dc979ff",
        ],
    },
)

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is", "of", "on", "or", "the", "to",
    "bir", "bu", "da", "de", "ile", "icin", "ve",
}


def _tokens(value: str) -> list[str]:
    folded = unicodedata.normalize("NFKD", value.casefold())
    ascii_text = "".join(char for char in folded if not unicodedata.combining(char))
    return [token for token in re.findall(r"[a-z0-9]+", ascii_text) if len(token) > 1 and token not in STOP_WORDS]


def _safe_canonical_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    canonical_root = (root / "corpus" / "canonical").resolve()
    if candidate != canonical_root and canonical_root not in candidate.parents:
        raise ValueError(f"canonical path escape: {relative}")
    if not candidate.is_file() or candidate.is_symlink():
        raise ValueError(f"missing canonical file: {relative}")
    return candidate


def _metadata_title(root: Path, record: dict[str, Any]) -> str | None:
    for item in record["canonical_files"]:
        if item.get("role") == "metadata.json":
            payload = json.loads(_safe_canonical_path(root, str(item["path"])).read_text(encoding="utf-8"))
            return payload.get("title") or payload.get("original_filename")
    return None


def _matches_section(section_id: object, prefix: str) -> bool:
    value = str(section_id or "")
    return value == prefix or value.startswith(prefix + ".")


def _search_case(root: Path, records: list[dict[str, Any]], case: dict[str, Any], top_k: int) -> dict[str, Any]:
    query_tokens = _tokens(case["query"])
    candidates: list[tuple[dict[str, Any], dict[str, Any], list[str]]] = []
    titles: dict[str, str | None] = {}

    for record in records:
        document_id = str(record["document_id"])
        titles[document_id] = _metadata_title(root, record)
        ready_path = _safe_canonical_path(root, str(record["chunks"]["retrieval_manifest_path"]))
        with ready_path.open(encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("eligible") is not True or not _matches_section(row.get("section_id"), case["section_prefix"]):
                    continue
                text_tokens = _tokens(str(row.get("embedding_text") or ""))
                candidates.append((record, row, text_tokens))

    document_frequency = {
        token: sum(token in set(text_tokens) for _, _, text_tokens in candidates)
        for token in query_tokens
    }
    best_by_document: dict[str, dict[str, Any]] = {}
    total = max(len(candidates), 1)

    for record, row, text_tokens in candidates:
        counts = Counter(text_tokens)
        matched = [token for token in query_tokens if counts[token]]
        if not matched:
            continue
        score = sum(
            (1.0 + math.log(counts[token])) * (math.log((total + 1) / (document_frequency[token] + 1)) + 1.0)
            for token in matched
        )
        coverage = len(set(matched)) / len(set(query_tokens))
        score += coverage * 3.0
        document_id = str(record["document_id"])
        result = {
            "document_id": document_id,
            "title": titles[document_id],
            "chunk_id": row.get("chunk_id"),
            "chunk_type": row.get("chunk_type"),
            "section_id": row.get("section_id"),
            "page_start": row.get("page_start"),
            "page_end": row.get("page_end"),
            "score": round(score, 6),
            "query_term_coverage": round(coverage, 4),
            "matched_terms": sorted(set(matched)),
            "snippet": " ".join(str(row.get("embedding_text") or "").split())[:320],
        }
        previous = best_by_document.get(document_id)
        if previous is None or result["score"] > previous["score"]:
            best_by_document[document_id] = result

    results = sorted(best_by_document.values(), key=lambda item: (-item["score"], item["document_id"]))[:top_k]
    expected = set(case["expected_document_ids"])
    found = {row["document_id"] for row in results}
    passed = bool(results) and results[0]["query_term_coverage"] >= 0.4 and (not expected or bool(expected & found))
    return {
        **case,
        "candidate_chunks": len(candidates),
        "candidate_documents": len({str(record["document_id"]) for record, _, _ in candidates}),
        "results": results,
        "expected_document_found": sorted(expected & found),
        "passed": passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    root = args.project_root.resolve()
    snapshot = require_ready(root)
    records = [record.to_dict() for record in snapshot.manifest.documents]
    cases = [_search_case(root, records, dict(case), args.top_k) for case in CASES]
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    payload = {
        "schema_version": "1.0",
        "test_kind": "CANONICAL_LEXICAL_SEARCH_SMOKE",
        "created_at": created_at,
        "method": "deterministic section-filtered TF-IDF-like lexical ranking",
        "limitation": "This verifies canonical text and section routing; it is not an embedding/vector retrieval evaluation.",
        "canonical": snapshot.inventory.to_dict(),
        "case_count": len(cases),
        "passed_case_count": sum(case["passed"] for case in cases),
        "passed": all(case["passed"] for case in cases),
        "cases": cases,
    }
    output = args.output
    if output is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output = root / "audit" / "retrieval" / f"corpus_search_smoke_{stamp}.json"
    elif not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(root)), **payload}, ensure_ascii=False, indent=2))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
