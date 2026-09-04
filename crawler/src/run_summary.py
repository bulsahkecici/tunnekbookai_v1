#!/usr/bin/env python3
"""Write machine-readable and Markdown summaries of one PaperCrawler pipeline run."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
import tunnel_harvest as harvest


def _read(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def _jsonl_count(path: Path) -> int:
    try:
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    except OSError:
        return 0


def write(output_dir: str | Path | None = None) -> dict[str, Any]:
    if output_dir is not None:
        harvest.set_output_dir(output_dir)
    root = harvest.OUTPUT_DIR
    audit = root / "audit"
    discovery = _read(audit / "discovery_audit.json")
    classification = _read(audit / "classification_audit.json")
    dedup = _read(audit / "source_dedup_version_audit.json")
    gap = _read(audit / "gap_discovery_audit.json")
    handoff = _read(root / "exports" / "TunnelBookAI_Source_Pack" / "99_audit" / "handoff_audit.json")
    handoff_audit = root / "exports" / "TunnelBookAI_Source_Pack" / "99_audit"
    acquisition = discovery.get("acquisition_counts") or {}
    coverage = classification.get("handoff_candidate_section_coverage") or {}
    with (Path(__file__).resolve().parent / "config" / "coverage_targets.yaml").open("r", encoding="utf-8") as handle:
        targets = (yaml.safe_load(handle) or {}).get("sections") or {}
    gaps = sorted(
        [{"section": sid, "current": int(coverage.get(sid) or 0), "target": int(target), "gap": max(0, int(target) - int(coverage.get(sid) or 0))} for sid, target in targets.items()],
        key=lambda item: item["gap"], reverse=True,
    )
    summary = {
        "discovery": {"queries": discovery.get("queries", 0), "discovered": discovery.get("discovered_unique", 0), "rejected_irrelevant": discovery.get("rejected_irrelevant", 0), "relevant_candidates": discovery.get("relevant_candidates", 0)},
        "acquisition": acquisition,
        "classification": {key: classification.get(key, 0) for key in ("documents", "rules_embedding_only_count", "qwen_reviewed_count", "qwen_review_rate", "manual_review_count", "irrelevant_rejected_count")},
        "handoff": {
            **{key: handoff.get(key, 0) for key in ("ready_for_handoff", "rejected")},
            "review_queue": _jsonl_count(handoff_audit / "review_queue.jsonl"),
            "rejected_manifest": _jsonl_count(handoff_audit / "rejected_manifest.jsonl"),
        },
        "coverage": {"sections_below_target": sum(1 for item in gaps if item["gap"]), "worst_10_gaps": gaps[:10]},
        "dedup": {key: dedup.get(key, 0) for key in ("exact_duplicate_groups", "same_doi_groups", "canonical_url_groups", "fuzzy_review_pairs")},
        "gap_search": {key: gap.get(key) for key in ("gap_search_completed", "catalog_additions", "provider_degraded", "gap_additions_reason")},
    }
    (audit / "run_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# PaperCrawler Run Summary", "", "## Discovery", f"- Queries: {summary['discovery']['queries']}", f"- Discovered: {summary['discovery']['discovered']}", f"- Rejected irrelevant: {summary['discovery']['rejected_irrelevant']}", f"- Relevant candidates: {summary['discovery']['relevant_candidates']}", "", "## Acquisition"]
    lines += [f"- {key}: {value}" for key, value in sorted(acquisition.items())]
    lines += ["", "## Classification", f"- Rules + embedding only: {summary['classification']['rules_embedding_only_count']}", f"- Qwen reviewed: {summary['classification']['qwen_reviewed_count']} ({summary['classification']['qwen_review_rate']:.1%})", f"- Needs manual review: {summary['classification']['manual_review_count']}", f"- Rejected irrelevant: {summary['classification']['irrelevant_rejected_count']}", "", "## Handoff", f"- READY_FOR_HANDOFF: {summary['handoff']['ready_for_handoff']}", f"- Rejected: {summary['handoff']['rejected']}", f"- Review queue: {summary['handoff']['review_queue']}", f"- Rejected manifest: {summary['handoff']['rejected_manifest']}", "", "## Coverage", f"- Sections below target: {summary['coverage']['sections_below_target']}"]
    lines += [f"- {item['section']}: {item['current']}/{item['target']} (gap {item['gap']})" for item in gaps[:10]]
    lines += ["", "## Dedup", *[f"- {key}: {value}" for key, value in summary["dedup"].items()], ""]
    (audit / "run_summary.md").write_text("\n".join(lines), encoding="utf-8")
    return summary
