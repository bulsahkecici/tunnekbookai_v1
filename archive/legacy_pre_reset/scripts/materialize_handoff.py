#!/usr/bin/env python3
"""Expose the migrated crawler handoff through the unified project layout."""

from __future__ import annotations

import csv
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "data" / "downloads"
PACKAGE = ROOT / "handoff" / "accepted" / "TunnelBookAI_Source_Pack"
SOURCE_MANIFEST = PACKAGE / "00_registry" / "handoff_manifest.jsonl"
SOURCE_REVIEW = PACKAGE / "99_audit" / "review_queue.jsonl"
CLASSIFICATIONS = DOWNLOADS / "classification_index.jsonl"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def link_or_copy(source: Path, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if destination.stat().st_size == source.stat().st_size:
            return "existing"
        raise RuntimeError(f"staging conflict: {destination}")
    try:
        os.link(source, destination)
        return "hardlink"
    except OSError:
        shutil.copy2(source, destination)
        return "copy"


def main() -> int:
    if not SOURCE_MANIFEST.is_file():
        raise FileNotFoundError(SOURCE_MANIFEST)
    manifest_out = ROOT / "handoff" / "manifests" / "handoff_manifest.jsonl"
    review_out = ROOT / "handoff" / "review" / "review_queue.csv"
    staging = ROOT / "corpus" / "staging"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    review_out.parent.mkdir(parents=True, exist_ok=True)
    staging.mkdir(parents=True, exist_ok=True)

    rows = read_jsonl(SOURCE_MANIFEST)
    expected_ids = {str(row.get("canonical_id") or "") for row in rows}
    stale_root = ROOT / "corpus" / "rejects" / "stale_handoff"
    for child in staging.iterdir():
        if child.is_dir() and child.name not in expected_ids:
            stale_root.mkdir(parents=True, exist_ok=True)
            destination = stale_root / child.name
            if destination.exists():
                raise RuntimeError(f"stale handoff conflict: {destination}")
            shutil.move(str(child), str(destination))
    materialized = []
    for row in rows:
        source = PACKAGE / str(row.get("local_path") or "")
        if not source.is_file():
            raise FileNotFoundError(source)
        canonical_id = str(row.get("canonical_id") or "")
        destination = staging / canonical_id / source.name
        mode = link_or_copy(source, destination)
        normalized = dict(row)
        normalized["local_path"] = destination.relative_to(ROOT).as_posix()
        normalized["handoff_status"] = "STAGING"
        normalized.setdefault("provenance", {})["migration_source_package"] = str(PACKAGE)
        normalized["provenance"]["staging_copy_mode"] = mode
        sidecar = destination.parent / "provenance.json"
        sidecar.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
        materialized.append(normalized)
    with manifest_out.open("w", encoding="utf-8") as handle:
        for row in materialized:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    index = read_jsonl(CLASSIFICATIONS)
    lookup = {
        str(row.get("document_key") or row.get("doi") or row.get("source_sha256") or ""): row
        for row in index
    }
    review = read_jsonl(SOURCE_REVIEW) if SOURCE_REVIEW.is_file() else []
    columns = [
        "document_id", "canonical_id", "title", "source", "document_type",
        "source_tier", "primary_section", "secondary_sections", "confidence",
        "evidence_level", "reason_for_review", "url", "local_path",
    ]
    with review_out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for entry in review:
            source = lookup.get(str(entry.get("document_id") or ""), {})
            writer.writerow({
                "document_id": entry.get("document_id"),
                "canonical_id": source.get("canonical_id"),
                "title": entry.get("title"),
                "source": entry.get("discovery_source"),
                "document_type": source.get("normalized_document_type") or source.get("document_type"),
                "source_tier": source.get("source_tier"),
                "primary_section": entry.get("primary_section"),
                "secondary_sections": ";".join(
                    str(item.get("id")) for item in source.get("book_sections") or []
                    if item.get("id") != entry.get("primary_section")
                ),
                "confidence": source.get("classification_confidence"),
                "evidence_level": source.get("evidence_level"),
                "reason_for_review": entry.get("reason"),
                "url": source.get("source_url") or source.get("landing_url"),
                "local_path": source.get("source_path"),
            })

    state_source = DOWNLOADS / "audit" / "pipeline_state.json"
    if state_source.is_file():
        shutil.copy2(state_source, ROOT / "audit" / "pipeline_state.json")
    print(json.dumps({"handoff_records": len(materialized), "review_records": len(review), "staging_documents": len(materialized)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
