#!/usr/bin/env python3
"""Coverage accounting with explicit status/evidence dimensions and parent roll-up."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Iterable

import corpus_policy
import relevance_engine


def section_ancestors(section_id: str) -> list[str]:
    parts = [part for part in str(section_id).split(".") if part]
    return [".".join(parts[:index]) for index in range(1, len(parts) + 1)]


def record_sections(record: dict[str, Any]) -> set[str]:
    sections = {str(record.get("primary_section") or "").strip()}
    sections.update(str(row.get("id") or "").strip() for row in (record.get("book_sections") or []) if isinstance(row, dict))
    expanded = {ancestor for sid in sections if sid for ancestor in section_ancestors(sid)}
    return expanded


def calculate(records: Iterable[dict[str, Any]], *, include_review_in_discovered: bool = True) -> dict[str, Any]:
    metrics: defaultdict[str, Counter[str]] = defaultdict(Counter)
    totals: Counter[str] = Counter()
    for record in records:
        status = str(record.get("classification_status") or "")
        decision, _ = corpus_policy.handoff_decision(record)
        evidence = str(record.get("evidence_level") or corpus_policy.evidence_level(record))
        is_rejected = decision == "REJECT"
        is_review = decision == "REVIEW"
        discovered = not is_rejected and (include_review_in_discovered or not is_review)
        relevance_status = relevance_engine.evaluate(
            record, text_override=str(record.get("abstract") or "")
        ).get("relevance_status")
        eligible = (
            decision == "AUTO_HANDOFF"
            and bool(record.get("handoff_candidate", False))
            and relevance_status in {"STRONG", "PROBABLE"}
        )
        dimensions = {
            "discovered_count": discovered,
            "classified_count": True,
            "accepted_count": status in corpus_policy.AUTO_HANDOFF,
            "review_count": is_review,
            "corpus_eligible_count": eligible,
            "fulltext_count": evidence in {"FULL_TEXT", "PDF_EXTRACT", "WEBPAGE_TEXT"},
        }
        for name, enabled in dimensions.items():
            if enabled:
                totals[name] += 1
        for sid in record_sections(record):
            for name, enabled in dimensions.items():
                if enabled:
                    metrics[sid][name] += 1
    return {
        "policy_version": "1.0",
        "parent_aggregation": True,
        "totals": dict(totals),
        "sections": {sid: dict(values) for sid, values in sorted(metrics.items())},
    }
