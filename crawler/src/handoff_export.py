#!/usr/bin/env python3
"""Create a self-contained TunnelBookAI source handoff package.

The exporter never mutates canonical PaperCrawler sources. It validates the
classification gate, source existence and SHA256, then hardlinks (or copies)
accepted sources into deterministic source-type folders with metadata and
classification sidecars. Discovery provenance and optional raw web snapshots are
preserved for TunnelBookAI auditability.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

import tunnel_harvest as harvest
import corpus_policy
import relevance_engine as relevance
from project_paths import CRAWLER_CONFIG_ROOT, resolve_local_path

ROOT = Path(__file__).resolve().parent
CONFIG_DIR = CRAWLER_CONFIG_ROOT


def _policy() -> dict[str, Any]:
    with (CONFIG_DIR / "classification_policy.yaml").open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    return payload.get("handoff") or {}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stable_document_id(row: dict[str, Any], source_path: Path) -> str:
    sha = str(row.get("source_sha256") or "").strip().lower()
    if not sha:
        sha = _sha256(source_path)
    return "PC_" + sha[:16].upper()


def _safe_route(route_path: str) -> Path:
    route = Path(str(route_path or "90_STAGING/NEEDS_CLASSIFICATION"))
    if route.is_absolute() or ".." in route.parts:
        raise ValueError(f"Unsafe route path: {route_path}")
    return route


def _link_or_copy(src: Path, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    try:
        os.link(src, dest)
        return "hardlink"
    except OSError:
        shutil.copy2(src, dest)
        return "copy"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        item = json.loads(line)
        if isinstance(item, dict):
            rows.append(item)
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def _queue_entry(row: dict[str, Any], reason: str, action: str) -> dict[str, Any]:
    return {
        "document_id": row.get("document_key") or row.get("doi") or row.get("source_sha256"),
        "title": row.get("title"),
        "source_path": row.get("source_path"),
        "source_sha256": row.get("source_sha256"),
        "classification_status": row.get("classification_status"),
        "relevance_status": row.get("relevance_status"),
        "primary_section": row.get("primary_section"),
        "reason": reason,
        "recommended_action": action,
        "discovery_source": row.get("discovery_source"),
    }


def export_handoff(
    output_dir: str | Path | None = None,
    *,
    destination: str | Path | None = None,
) -> dict[str, Any]:
    if output_dir is not None:
        harvest.set_output_dir(output_dir)
    source_root = harvest.OUTPUT_DIR
    policy = _policy()
    allowed = set(policy.get("allowed_classification_statuses") or [])
    require_section = bool(policy.get("require_primary_section", True))
    require_source = bool(policy.get("require_existing_source", True))
    require_sha = bool(policy.get("require_sha256", True))
    package_name = str(policy.get("package_name") or "TunnelBookAI_Source_Pack")

    package_root = Path(destination).resolve() if destination else (source_root / "exports" / package_name)
    originals_root = package_root / "01_originals"
    registry_root = package_root / "00_registry"
    audit_root = package_root / "99_audit"
    registry_root.mkdir(parents=True, exist_ok=True)
    audit_root.mkdir(parents=True, exist_ok=True)

    rows = _read_jsonl(source_root / "classification_index.jsonl")
    manifest: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    review_queue: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    route_counts: Counter[str] = Counter()
    copy_modes: Counter[str] = Counter()
    seen_ids: set[str] = set()

    for row in rows:
        status = str(row.get("classification_status") or "")
        reason = None
        row = dict(row)
        row["evidence_level"] = str(row.get("evidence_level") or corpus_policy.evidence_level(row))
        row["source_tier"] = str(row.get("source_tier") or corpus_policy.source_tier(row))
        row["normalized_document_type"] = str(row.get("normalized_document_type") or corpus_policy.normalized_document_type(row))
        policy_decision, policy_reason = corpus_policy.handoff_decision(row)
        recheck = relevance.evaluate(row, text_override=str(row.get("abstract") or ""))
        row = {**row, **recheck}
        if status not in allowed:
            reason = "classification_status_not_allowed"
        elif require_section and not row.get("primary_section"):
            reason = "primary_section_missing"
        elif row.get("handoff_candidate") is False:
            reason = "not_handoff_candidate"

        source_value = row.get("source_path")
        source_path = resolve_local_path(source_value)
        if reason is None and require_source and (source_path is None or not source_path.exists()):
            reason = "source_missing"
        if reason:
            entry = _queue_entry(row, reason, "MANUAL_REVIEW" if status in {"NEEDS_REVIEW", "LOCAL_LLM_REVIEW"} or recheck["relevance_status"] == "PROBABLE" else "REJECT")
            rejected.append(entry)
            if entry["recommended_action"] == "MANUAL_REVIEW":
                review_queue.append(entry)
            continue
        assert source_path is not None

        actual_sha = _sha256(source_path)
        expected_sha = str(row.get("source_sha256") or "").strip().lower()
        if expected_sha and expected_sha != actual_sha:
            rejected.append(_queue_entry(row, "sha256_mismatch", "REJECT"))
            continue
        if require_sha and not expected_sha:
            row["source_sha256"] = actual_sha

        if recheck["relevance_status"] not in {"STRONG", "PROBABLE"}:
            entry = _queue_entry(row, "relevance_gate_failed", "MANUAL_REVIEW" if recheck["relevance_status"] == "PROBABLE" else "REJECT")
            rejected.append(entry)
            if entry["recommended_action"] == "MANUAL_REVIEW":
                review_queue.append(entry)
            continue

        if policy_decision != "AUTO_HANDOFF":
            entry = _queue_entry(row, policy_reason, "MANUAL_REVIEW" if policy_decision == "REVIEW" else "REJECT")
            rejected.append(entry)
            if entry["recommended_action"] == "MANUAL_REVIEW":
                review_queue.append(entry)
            continue

        document_id = _stable_document_id(row, source_path)
        if document_id in seen_ids:
            rejected.append(_queue_entry(row, "duplicate_document_id", "REJECT"))
            continue
        seen_ids.add(document_id)

        route = _safe_route(str(row.get("route_path") or ""))
        doc_dir = originals_root / route / document_id
        suffix = source_path.suffix.lower() or ".bin"
        source_dest = doc_dir / ("source" + suffix)
        copy_mode = _link_or_copy(source_path, source_dest)
        copy_modes[copy_mode] += 1

        extra_assets: list[dict[str, Any]] = []
        raw_html_value = row.get("raw_html_path")
        if raw_html_value:
            raw_html = Path(str(raw_html_value)).expanduser()
            if raw_html.exists() and raw_html.is_file():
                expected_raw_sha = str(row.get("raw_html_sha256") or "").strip().lower()
                actual_raw_sha = _sha256(raw_html)
                if not expected_raw_sha or expected_raw_sha == actual_raw_sha:
                    raw_dest = doc_dir / "source_raw.html"
                    raw_mode = _link_or_copy(raw_html, raw_dest)
                    copy_modes[raw_mode] += 1
                    extra_assets.append({
                        "kind": "raw_html_snapshot",
                        "path": str(raw_dest.relative_to(package_root)),
                        "sha256": actual_raw_sha,
                        "copy_mode": raw_mode,
                    })

        classification_payload = dict(row)
        classification_payload.update({
            "document_id": document_id,
            "paper_crawler_status": "READY_FOR_HANDOFF",
            "tunnelbookai_status": "NOT_INGESTED",
            "handoff_source_path": str(source_dest.relative_to(package_root)),
            "source_sha256": actual_sha,
            "extra_assets": extra_assets,
        })
        (doc_dir / "classification.json").write_text(
            json.dumps(classification_payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        metadata = {
            "schema_version": "1.1",
            "document_id": document_id,
            "canonical_id": row.get("canonical_id") or "CAN_" + actual_sha[:20].upper(),
            "title": row.get("title"),
            "authors": row.get("authors") or [],
            "year": row.get("year"),
            "publisher": row.get("publisher"),
            "doi": row.get("doi"),
            "document_type": row.get("document_type"),
            "normalized_document_type": row.get("normalized_document_type"),
            "source_tier": row.get("source_tier"),
            "evidence_level": row.get("evidence_level"),
            "source_class": row.get("source_class"),
            "authority_tier": row.get("authority_tier"),
            "evidence_priority": row.get("evidence_priority"),
            "primary_section": row.get("primary_section"),
            "book_sections": row.get("book_sections") or [],
            "topics": row.get("topics") or [],
            "classification_confidence": row.get("classification_confidence"),
            "classification_status": status,
            "route_path": str(route),
            "source_sha256": actual_sha,
            "source_filename": source_path.name,
            "source_url": row.get("source_url"),
            "landing_url": row.get("landing_url"),
            "pdf_url": row.get("pdf_url"),
            "discovery_source": row.get("discovery_source"),
            "discovery_query": row.get("discovery_query"),
            "acquisition_status": row.get("acquisition_status"),
            "metadata_only": bool(row.get("metadata_only", False)),
            "extra_assets": extra_assets,
            "paper_crawler_status": "READY_FOR_HANDOFF",
            "tunnelbookai_status": "NOT_INGESTED",
        }
        if "piarc" in str(row.get("source_url") or row.get("landing_url") or "").casefold():
            metadata["parent_document"] = row.get("parent_document") or "PIARC Road Tunnels Manual"
            metadata["section_url"] = row.get("source_url") or row.get("landing_url")
            metadata["section_title"] = row.get("title")
        (doc_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

        manifest_row = {
            **metadata,
            "source_path": str(source_dest.relative_to(package_root)),
            "classification_path": str((doc_dir / "classification.json").relative_to(package_root)),
            "metadata_path": str((doc_dir / "metadata.json").relative_to(package_root)),
            "copy_mode": copy_mode,
        }
        manifest.append(manifest_row)
        status_counts[status] += 1
        route_counts[str(route)] += 1

    manifest_path = registry_root / "manifest.jsonl"
    with manifest_path.open("w", encoding="utf-8") as handle:
        for row in manifest:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    handoff_manifest = []
    for row in manifest:
        handoff_manifest.append({
            "document_id": row.get("document_id"),
            "canonical_id": row.get("canonical_id") or "CAN_" + str(row.get("source_sha256") or "")[:20].upper(),
            "title": row.get("title"), "authors": row.get("authors") or [], "year": row.get("year"),
            "doi": row.get("doi"), "source_url": row.get("source_url"),
            "resolved_url": row.get("pdf_url") or row.get("landing_url") or row.get("source_url"),
            "local_path": row.get("source_path"), "sha256": row.get("source_sha256"),
            "source_name": row.get("discovery_source"), "source_tier": row.get("source_tier"),
            "document_type": row.get("normalized_document_type"), "primary_section": row.get("primary_section"),
            "secondary_sections": [s.get("id") for s in row.get("book_sections") or [] if s.get("id") != row.get("primary_section")],
            "classification_status": row.get("classification_status"),
            "classification_confidence": row.get("classification_confidence"),
            "evidence_level": row.get("evidence_level"), "acquisition_status": row.get("acquisition_status"),
            "handoff_status": "READY_FOR_HANDOFF",
            "provenance": {key: row.get(key) for key in ("source_url", "landing_url", "pdf_url", "discovery_source", "discovery_query", "doi", "publisher") if row.get(key)},
        })
    _write_jsonl(registry_root / "handoff_manifest.jsonl", handoff_manifest)

    checksums_path = registry_root / "checksums.sha256"
    with checksums_path.open("w", encoding="utf-8") as handle:
        for row in manifest:
            handle.write(f"{row['source_sha256']}  {row['source_path']}\n")
            for asset in row.get("extra_assets") or []:
                if asset.get("sha256") and asset.get("path"):
                    handle.write(f"{asset['sha256']}  {asset['path']}\n")

    handoff_report = {
        "schema_version": "1.1",
        "package": package_name,
        "source_root": str(source_root),
        "package_root": str(package_root),
        "input_classifications": len(rows),
        "ready_for_handoff": len(manifest),
        "rejected": len(rejected),
        "status_counts": dict(status_counts),
        "route_counts": dict(route_counts),
        "copy_modes": dict(copy_modes),
        "rejections": rejected,
        "gate_meaning": "READY_FOR_HANDOFF means safe and sufficiently classified for TunnelBookAI processing; it is not final evidence approval.",
    }
    (audit_root / "handoff_audit.json").write_text(
        json.dumps(handoff_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    _write_jsonl(audit_root / "review_queue.jsonl", review_queue)
    _write_jsonl(audit_root / "rejected_manifest.jsonl", rejected)
    review_columns = ["document_id", "title", "source", "document_type", "source_tier", "primary_section", "proposed_secondary_sections", "confidence", "evidence_level", "reason_for_review", "URL", "local_path"]
    with (audit_root / "review_queue.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=review_columns)
        writer.writeheader()
        for entry in review_queue:
            source_row = next((row for row in rows if (row.get("document_key") or row.get("doi") or row.get("source_sha256")) == entry.get("document_id")), {})
            writer.writerow({
                "document_id": entry.get("document_id"), "title": entry.get("title"),
                "source": entry.get("discovery_source"), "document_type": source_row.get("normalized_document_type") or source_row.get("document_type"),
                "source_tier": source_row.get("source_tier"), "primary_section": entry.get("primary_section"),
                "proposed_secondary_sections": ";".join(str(s.get("id")) for s in source_row.get("book_sections") or [] if s.get("id") != entry.get("primary_section")),
                "confidence": source_row.get("classification_confidence"), "evidence_level": source_row.get("evidence_level"),
                "reason_for_review": entry.get("reason"), "URL": source_row.get("source_url") or source_row.get("landing_url"),
                "local_path": entry.get("source_path"),
            })
    (registry_root / "handoff_contract.json").write_text(
        json.dumps({
            "schema_version": "1.1",
            "producer": "paper-crawler-agent",
            "consumer": "TunnelBookAI",
            "manifest": "00_registry/manifest.jsonl",
            "handoff_manifest": "00_registry/handoff_manifest.jsonl",
            "checksums": "00_registry/checksums.sha256",
            "source_tree": "01_originals",
            "audit": "99_audit/handoff_audit.json",
            "review_queue": "99_audit/review_queue.jsonl",
            "review_queue_csv": "99_audit/review_queue.csv",
            "rejected_manifest": "99_audit/rejected_manifest.jsonl",
            "provenance_fields": ["source_url", "landing_url", "pdf_url", "discovery_source", "discovery_query", "doi", "publisher"],
            "consumer_rule": "TunnelBookAI must revalidate SHA256 and perform full-text conversion, quality audit, final section classification and evidence gating before corpus ingest.",
        }, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"READY_FOR_HANDOFF: {len(manifest)}")
    print(f"Rejected by handoff gate: {len(rejected)}")
    print(f"Package: {package_root}")
    return handoff_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export classified PaperCrawler sources for TunnelBookAI.")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--destination", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    export_handoff(args.output_dir, destination=args.destination)


if __name__ == "__main__":
    main()
