#!/usr/bin/env python3
"""Build additive provenance records for the preserved legacy canonical corpus."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "corpus" / "metadata"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    manifest = rows(METADATA / "final_corpus_manifest.csv")
    master = {row.get("document_id"): row for row in rows(METADATA / "final_metadata_master.csv")}
    generated = datetime.now(timezone.utc).isoformat()
    output = []
    for item in manifest:
        document_id = str(item.get("document_id") or "")
        meta = master.get(document_id, {})
        final_output = str(item.get("final_output") or "")
        prefix = "data/corpus_final/"
        relative = final_output[len(prefix):] if final_output.startswith(prefix) else final_output
        output.append({
            "document_id": document_id,
            "canonical_id": "TB_" + document_id,
            "source_url": None,
            "source_path": item.get("source_relative_path"),
            "discovery_source": "legacy_tunnelbookai_inventory",
            "acquisition_timestamp": None,
            "migration_timestamp": generated,
            "source_type": "legacy_local_document",
            "sha256": item.get("source_sha256"),
            "classification": {
                "document_type": item.get("document_type") or meta.get("document_type") or "unknown",
                "authority_level": item.get("authority_level") or meta.get("authority_level") or None,
            },
            "section": None,
            "evidence_level": "FULL_TEXT",
            "canonical_path": "corpus/canonical/" + relative,
            "legacy_provenance_limitations": ["source_url_not_recorded", "section_not_assigned"] if not item.get("source_url") else ["section_not_assigned"],
        })
    destination = METADATA / "canonical_provenance.jsonl"
    with destination.open("w", encoding="utf-8") as handle:
        for row in output:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"canonical_provenance_records": len(output), "destination": str(destination)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
