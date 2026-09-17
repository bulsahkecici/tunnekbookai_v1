#!/usr/bin/env python3
"""Run the fixed Book Retrieval V1 semantic acceptance benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tunnelbookai.book.retrieval import inspect_index, search_index  # noqa: E402


CASES = (
    {
        "id": "chapter_3_history",
        "section": "3",
        "query": "Karayolları Genel Müdürlüğü tünellerinin tarihsel gelişimi Ovit ve Zigana tünelleri",
        "expected_document_ids": ["ING_62c2a5de1e2d13c0013a", "ING_7d7c44992e83c7185c41"],
    },
    {
        "id": "chapter_4_transport_cost",
        "section": "4",
        "query": "Ulaşım yatırımlarında yaşam döngüsü maliyeti ve maliyet kavramı",
        "expected_document_ids": ["ING_339e05e3358e01b537d8", "ING_43bc7c7729c6e993a390"],
    },
    {
        "id": "chapter_5_maintenance",
        "section": "5",
        "query": "Karayolu tünellerinde periyodik bakım işletme ve enerji maliyetleri",
        "expected_document_ids": ["ING_746d18498e07a8a0f397", "ING_aa8140c07fce1b3482e4"],
    },
    {
        "id": "chapter_6_construction_cost",
        "section": "6",
        "query": "Tünel yapım maliyetleri birim fiyat kazı püskürtme beton ve destekleme",
        "expected_document_ids": ["ING_5c2983ff4ac61dc979ff", "ING_ecb7b50dece6c5a14085"],
    },
)


def _matches_section(result: dict, section: str) -> bool:
    values = [str(result.get("section_id") or ""), *[str(value) for value in result.get("secondary_section_ids") or []]]
    return any(value == section or value.startswith(section + ".") for value in values)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--top-k", type=int, default=10)
    args = parser.parse_args()
    root = args.project_root.resolve()
    index = inspect_index(root)
    if not index.ready or not index.manifest:
        print(json.dumps(index.to_dict(), ensure_ascii=False, indent=2))
        return 2

    cases = []
    for definition in CASES:
        result = search_index(
            definition["query"], root,
            section=definition["section"], top_k=args.top_k,
        )
        rows = result["results"]
        found = sorted(set(definition["expected_document_ids"]) & {row["document_id"] for row in rows})
        passed = bool(rows) and bool(found) and all(_matches_section(row, definition["section"]) for row in rows)
        cases.append({
            **definition,
            "passed": passed,
            "expected_document_found": found,
            "result_count": len(rows),
            "top_score": rows[0]["score"] if rows else None,
            "results": rows,
        })
        print(json.dumps({
            "event": "BENCHMARK_CASE", "id": definition["id"],
            "passed": passed, "expected_document_found": found,
            "top_document": rows[0]["document_id"] if rows else None,
            "top_score": rows[0]["score"] if rows else None,
        }, ensure_ascii=False), flush=True)

    payload = {
        "schema_version": "1.0",
        "benchmark_version": "book-retrieval-v1-fixed-queries",
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "index_id": index.manifest["index_id"],
        "canonical_corpus_digest": index.manifest["canonical_corpus_digest"],
        "model_id": index.manifest["model_id"],
        "case_count": len(cases),
        "passed_case_count": sum(case["passed"] for case in cases),
        "passed": all(case["passed"] for case in cases),
        "cases": cases,
    }
    output = args.output
    if output is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output = root / "audit" / "retrieval" / f"semantic_benchmark_{stamp}.json"
    elif not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": output.relative_to(root).as_posix(), "passed": payload["passed"],
        "passed_case_count": payload["passed_case_count"], "case_count": payload["case_count"],
    }, ensure_ascii=False, indent=2))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
