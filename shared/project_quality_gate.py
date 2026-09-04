"""Unified fail-closed quality gate for migration, crawler handoff, and corpus."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def json_file(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def jsonl(path: Path) -> tuple[list[dict[str, Any]], bool]:
    if not path.is_file():
        return [], False
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        return rows, all(isinstance(row, dict) for row in rows)
    except (OSError, ValueError):
        return [], False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def evaluate() -> dict[str, Any]:
    blocking: list[str] = []
    warnings: list[str] = []
    migration = json_file(ROOT / "audit" / "migration_manifest.json")
    state = json_file(ROOT / "audit" / "pipeline_state.json")
    classification = json_file(ROOT / "data" / "downloads" / "audit" / "classification_audit.json")
    handoff, handoff_ok = jsonl(ROOT / "handoff" / "manifests" / "handoff_manifest.jsonl")
    index, index_ok = jsonl(ROOT / "data" / "downloads" / "classification_index.jsonl")
    if migration.get("decision") != "PASS":
        blocking.append("migration_integrity_failed")
    stages = state.get("stages") or {}
    if not stages or any(value != "COMPLETED" for value in stages.values()):
        blocking.append("pipeline_incomplete")
    if not index_ok:
        blocking.append("classification_index_unreadable")
    if not (classification.get("reconciliation") or {}).get("invariant_ok"):
        blocking.append("reconciliation_broken")
    if not (classification.get("coverage") or {}).get("parent_aggregation"):
        blocking.append("coverage_accounting_broken")
    if not handoff_ok:
        blocking.append("missing_handoff_manifest")

    canonical_ids = [str(row.get("canonical_id") or "") for row in handoff]
    if "" in canonical_ids or len(canonical_ids) != len(set(canonical_ids)):
        blocking.append("duplicate_canonical_id")
    shas = [str(row.get("sha256") or "") for row in handoff]
    if "" in shas or len(shas) != len(set(shas)):
        blocking.append("same_sha_on_multiple_canonical_docs")
    for row in handoff:
        local = ROOT / str(row.get("local_path") or "")
        if not local.is_file():
            blocking.append("missing_staging_file")
            break
        if sha256(local) != str(row.get("sha256") or ""):
            blocking.append("staging_sha_mismatch")
            break
        if not row.get("provenance"):
            blocking.append("missing_provenance")
            break

    corpus_manifest = ROOT / "corpus" / "metadata" / "final_corpus_manifest.csv"
    canonical_files = list((ROOT / "corpus" / "canonical").rglob("*.md"))
    manifest_rows = []
    if corpus_manifest.is_file():
        with corpus_manifest.open(encoding="utf-8-sig", newline="") as handle:
            manifest_rows = list(csv.DictReader(handle))
    if not canonical_files or len(canonical_files) != len(manifest_rows):
        blocking.append("missing_canonical_file")
    corpus_hashes = [sha256(path) for path in canonical_files]
    if len(corpus_hashes) != len(set(corpus_hashes)):
        blocking.append("same_sha_on_multiple_existing_canonical_docs")
    canonical_provenance, provenance_ok = jsonl(ROOT / "corpus" / "metadata" / "canonical_provenance.jsonl")
    if not provenance_ok or len(canonical_provenance) != len(canonical_files):
        blocking.append("missing_canonical_provenance")
    elif any(not row.get("source_path") or not row.get("sha256") or not row.get("evidence_level") for row in canonical_provenance):
        blocking.append("incomplete_canonical_provenance")
    elif any(row.get("legacy_provenance_limitations") for row in canonical_provenance):
        warnings.append("legacy_canonical_provenance_has_recorded_limitations")

    review_path = ROOT / "handoff" / "review" / "review_queue.csv"
    review_count = 0
    if review_path.is_file():
        with review_path.open(encoding="utf-8", newline="") as handle:
            review_count = sum(1 for _ in csv.DictReader(handle))
    if review_count:
        warnings.append("manual_review_queue_not_empty")
    evidence = Counter(str(row.get("evidence_level") or "UNKNOWN") for row in index)
    rejected = max(0, len(index) - len(handoff) - review_count)
    duplicates = int((classification.get("reconciliation") or {}).get("dedup_removed") or 0)
    result = {
        "decision": "NO_GO" if blocking else ("CONDITIONAL_GO" if warnings else "GO"),
        "total_records": len(index),
        "canonical_records": len(canonical_files),
        "new_staging_records": len(handoff),
        "handoff_eligible": len(handoff),
        "review_required": review_count,
        "rejected": rejected,
        "duplicates_removed": duplicates,
        "fulltext_records": evidence["FULL_TEXT"] + evidence["PDF_EXTRACT"] + evidence["WEBPAGE_TEXT"],
        "abstract_only_records": evidence["ABSTRACT"],
        "title_only_records": evidence["TITLE_METADATA_ONLY"],
        "coverage": classification.get("coverage") or {},
        "source_health": json_file(ROOT / "data" / "downloads" / "audit" / "source_health.json"),
        "blocking_issues": sorted(set(blocking)),
        "warnings": warnings,
    }
    destination = ROOT / "audit" / "corpus_quality_gate.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False, indent=2))
