"""Deterministic book scope/question-bank integrity and QA architecture.

This module validates structure only.  It never asks an LLM to answer questions
and never treats model knowledge or topical similarity as evidence.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT = PROJECT_ROOT / "book"
TAXONOMY_PATH = PROJECT_ROOT / "config" / "taxonomy.yaml"

EVIDENCE_STATUSES = {
    "SUPPORTED", "PARTIALLY_SUPPORTED", "INSUFFICIENT_EVIDENCE",
    "NO_EVIDENCE", "NOT_EVALUATED",
}
CHAPTER_STATUSES = {
    "ANSWERED", "PARTIALLY_ANSWERED", "NOT_ANSWERED",
    "UNSUPPORTED_CLAIM", "NOT_APPLICABLE",
}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_scope(book_root: Path = BOOK_ROOT) -> dict[str, dict[str, Any]]:
    payload = _json(book_root / "scope" / "normalized" / "book_scope.json")
    return {str(row["section_id"]): row for row in payload.get("sections") or []}


def load_questions(book_root: Path = BOOK_ROOT) -> list[dict[str, Any]]:
    path = book_root / "question_bank" / "normalized" / "question_bank.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_taxonomy(path: Path = TAXONOMY_PATH) -> dict[str, dict[str, Any]]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {str(key): row for key, row in (value.get("sections") or {}).items()}


def validate(book_root: Path = BOOK_ROOT, taxonomy_path: Path = TAXONOMY_PATH) -> dict[str, Any]:
    scope = load_scope(book_root)
    questions = load_questions(book_root)
    taxonomy = load_taxonomy(taxonomy_path)
    ids = [str(row.get("question_id") or "") for row in questions]
    duplicates = sorted(key for key, count in Counter(ids).items() if key and count > 1)
    orphans = sorted({str(row.get("section_id") or "") for row in questions} - set(scope))
    title_mismatches = sorted({
        str(row.get("section_id") or "") for row in questions
        if str(row.get("section_title") or "") != str(scope.get(str(row.get("section_id") or ""), {}).get("title") or "")
    })
    parent_errors = []
    for sid, row in scope.items():
        expected = ".".join(sid.split(".")[:-1]) or None
        if row.get("parent_section") != expected:
            parent_errors.append(sid)
    question_sections = {str(row.get("section_id") or "") for row in questions}
    taxonomy_missing = sorted(question_sections - set(taxonomy))
    taxonomy_orphans = sorted(set(taxonomy) - set(scope))
    taxonomy_title_mismatches = sorted(
        sid for sid in set(taxonomy) & set(scope)
        if str(taxonomy[sid].get("title") or "") != str(scope[sid].get("title") or "")
    )
    source_hash_errors = []
    manifest = _json(book_root / "audits" / "source_manifest.json")
    for entry in manifest.get("files") or []:
        path = PROJECT_ROOT / str(entry.get("path") or "")
        if not path.is_file() or _sha256(path) != str(entry.get("sha256") or ""):
            source_hash_errors.append(str(entry.get("path") or ""))
    section_counts = Counter(str(row.get("section_id") or "") for row in questions)
    index = _json(book_root / "question_bank" / "normalized" / "question_bank_index.json")
    count_mismatches = sorted(
        sid for sid, detail in (index.get("sections") or {}).items()
        if section_counts[str(sid)] != int(detail.get("question_count") or 0)
    )
    blocking = {
        "duplicate_question_ids": duplicates,
        "orphan_sections": orphans,
        "section_title_mismatches": title_mismatches,
        "parent_section_errors": parent_errors,
        "question_sections_missing_from_taxonomy": taxonomy_missing,
        "taxonomy_sections_missing_from_scope": taxonomy_orphans,
        "taxonomy_title_mismatches": taxonomy_title_mismatches,
        "question_count_mismatches": count_mismatches,
        "source_hash_errors": source_hash_errors,
    }
    return {
        "schema_version": "1.0",
        "decision": "PASS" if not any(blocking.values()) else "FAIL",
        "scope_sections": len(scope),
        "question_bank_sections": len(question_sections),
        "total_questions": len(questions),
        "expected_total_questions_from_index": int(index.get("total_questions") or 0),
        "full_question_bank_llm_evaluation_executed": False,
        **blocking,
    }


def question_coverage(
    section_id: str,
    evaluations: Iterable[dict[str, Any]],
    *, corpus_eligible_documents: int,
) -> dict[str, Any]:
    rows = [row for row in evaluations if str(row.get("section_id") or "") == section_id]
    counts = Counter(str(row.get("evidence_status") or "NOT_EVALUATED") for row in rows)
    unknown = sorted(set(counts) - EVIDENCE_STATUSES)
    if unknown:
        raise ValueError(f"invalid evidence statuses: {unknown}")
    total = len(rows)
    supported = counts["SUPPORTED"]
    return {
        "section_id": section_id,
        "document_coverage": {"corpus_eligible_documents": int(corpus_eligible_documents)},
        "question_coverage": {
            "total_questions": total,
            "supported": supported,
            "partial": counts["PARTIALLY_SUPPORTED"],
            "insufficient": counts["INSUFFICIENT_EVIDENCE"],
            "no_evidence": counts["NO_EVIDENCE"],
            "not_evaluated": counts["NOT_EVALUATED"],
            "support_rate": round(supported / total, 4) if total else 0.0,
        },
    }


def technical_concepts(question: str, *, limit: int = 8) -> list[str]:
    """Create safe query concepts; never use the full question as a search query."""
    stop = {"nedir", "nasıl", "nelerdir", "hangi", "neden", "için", "olan", "olarak", "bir", "ve", "ile", "bu", "şu", "midir", "açıklanır"}
    tokens = re.findall(r"[\wçğıöşüÇĞİÖŞÜ-]+", question.casefold())
    return list(dict.fromkeys(token for token in tokens if len(token) > 3 and token not in stop))[:limit]


def chapter_gate(section_id: str, evaluations: Iterable[dict[str, Any]], *, minimum_answer_rate: float = 0.90) -> dict[str, Any]:
    rows = [row for row in evaluations if str(row.get("section_id") or "") == section_id]
    counts = Counter(str(row.get("chapter_status") or "NOT_ANSWERED") for row in rows)
    unknown = sorted(set(counts) - CHAPTER_STATUSES)
    if unknown:
        raise ValueError(f"invalid chapter statuses: {unknown}")
    applicable = len(rows) - counts["NOT_APPLICABLE"]
    rate = counts["ANSWERED"] / applicable if applicable else 0.0
    unsupported = counts["UNSUPPORTED_CLAIM"]
    decision = "GO" if rate >= minimum_answer_rate and not unsupported else ("CONDITIONAL_GO" if not unsupported else "NO_GO")
    return {
        "section_id": section_id,
        "total_questions": len(rows),
        "answered": counts["ANSWERED"],
        "partially_answered": counts["PARTIALLY_ANSWERED"],
        "not_answered": counts["NOT_ANSWERED"],
        "answer_rate": round(rate, 4),
        "unsupported_claims": unsupported,
        "decision": decision,
    }


def write_integrity_audit(destination: Path | None = None) -> dict[str, Any]:
    result = validate()
    path = destination or BOOK_ROOT / "audits" / "taxonomy_integration.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(write_integrity_audit(), ensure_ascii=False, indent=2))
