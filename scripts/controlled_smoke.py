#!/usr/bin/env python3
"""Two-query public-metadata smoke test with a two-document acquisition budget."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "crawler" / "src"))

import classify_catalog
import free_discovery
import tunnel_harvest

QUERIES = ("NATM tunnel support", "road tunnel maintenance cost")


def main() -> int:
    smoke_root = Path(tempfile.mkdtemp(prefix="tunnelbookai_smoke_"))
    tunnel_harvest.set_output_dir(smoke_root)
    (smoke_root / "catalog.json").write_text('{"papers": []}', encoding="utf-8")
    candidates = []
    errors = []
    for query in QUERIES:
        batch, batch_errors = free_discovery.discover_existing_academic(
            query,
            per_source=2,
            disabled_sources={"europe_pmc", "doaj", "arxiv"},
        )
        filtered, _ = free_discovery.filter_relevant_records(batch)
        candidates.extend(filtered)
        errors.extend(batch_errors)
    candidates = free_discovery.deduplicate(candidates)
    candidates.sort(key=lambda row: (float(row.tunnel_relevance_score or 0), bool(row.pdf_url), bool(row.doi)), reverse=True)
    acquired = []
    downloads = 0
    for record in candidates[:6]:
        if downloads < 2 and (record.pdf_url or record.source_url or record.landing_url):
            payload = free_discovery.acquire_record(record, smoke_root / "discovery_sources")
            downloads += int(payload.get("acquisition_status") in {"DOWNLOADED_PDF", "SNAPSHOTTED_WEB"})
        else:
            payload = record.as_dict() | {"acquisition_status": "METADATA_RANKED"}
        acquired.append(payload)
    with (smoke_root / "discovery_catalog.jsonl").open("w", encoding="utf-8") as handle:
        for row in acquired:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    classification = classify_catalog.classify_catalog(smoke_root, use_local_ai=False)
    report = {
        "decision": "PASS" if len(candidates) > 0 and classification.get("reconciliation", {}).get("invariant_ok") else "FAIL",
        "queries": list(QUERIES),
        "maximum_results_per_source": 2,
        "download_budget": 2,
        "metadata_candidates": len(candidates),
        "downloads_successful": downloads,
        "classified": classification.get("documents"),
        "coverage_parent_aggregation": classification.get("coverage", {}).get("parent_aggregation"),
        "provider_errors": errors,
        "temporary_output": str(smoke_root),
        "production_crawl": False,
    }
    destination = ROOT / "audit" / "controlled_smoke_test.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
