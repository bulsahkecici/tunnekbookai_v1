"""Read-only operational status for the book-production foundation."""

from __future__ import annotations

import json
from typing import Any

from tunnelbookai.canonical.paths import CanonicalContext
from tunnelbookai.canonical.verifier import inspect_canonical
from .inputs import BookInputs
from .evidence_review import inspect_evidence_reviews
from .editorial import inspect_editorial_audits
from .freeze import inspect_freezes
from .coverage import coverage_summary_from_counts
from .coverage_audit import inspect_coverage_audits
from .preparation import inspect_preparation
from .retrieval import inspect_index
from .writer import inspect_drafts


def build_status(inputs: BookInputs) -> dict[str, Any]:
    inventory = inspect_canonical(context=CanonicalContext.load(book_inputs=inputs))
    retrieval = inspect_index(inputs.contract.project_root)
    audit_path = inputs.contract.project_root / "audit" / "book" / "prewriting_evidence_audit.json"
    prewriting: dict[str, Any] = {}
    if audit_path.is_file():
        try:
            candidate = json.loads(audit_path.read_text(encoding="utf-8"))
            manifest = retrieval.manifest or {}
            if (
                candidate.get("question_bank_sha256") == inputs.identities["question_bank_sha256"]
                and candidate.get("canonical_corpus_digest") == inventory.corpus_digest
                and candidate.get("retrieval_index_id") == manifest.get("index_id")
            ):
                prewriting = candidate
        except (OSError, ValueError, json.JSONDecodeError):
            prewriting = {}
    section_states = {
        "READY": 0,
        "READY_WITH_LIMITATIONS": 0,
        "EVIDENCE_GAP": 0,
        "DRAFTED": 0,
        "AUDIT_HOLD": 0,
        "FROZEN": 0,
        "NOT_STARTED": len(inputs.scope) - int(prewriting.get("sections_audited") or 0),
    }
    for section in prewriting.get("sections") or []:
        readiness = str(section.get("readiness") or "")
        if readiness in section_states:
            section_states[readiness] += 1
    preparation = inspect_preparation(inputs.contract.project_root, inputs=inputs)
    drafts = inspect_drafts(inputs.contract.project_root, preparation=preparation)
    for draft in drafts:
        section_id = str(draft.get("section_id") or "")
        prewriting_section = next(
            (row for row in prewriting.get("sections") or [] if row.get("section_id") == section_id),
            None,
        )
        if prewriting_section:
            readiness = str(prewriting_section.get("readiness") or "")
            if readiness in section_states and section_states[readiness] > 0:
                section_states[readiness] -= 1
        section_states["DRAFTED"] += 1
    evidence_reviews = inspect_evidence_reviews(inputs.contract.project_root, drafts=drafts)
    for review in evidence_reviews:
        if review.get("audit_decision") == "REVISION_REQUIRED":
            if section_states["DRAFTED"] > 0:
                section_states["DRAFTED"] -= 1
            section_states["AUDIT_HOLD"] += 1
    coverage_audits = inspect_coverage_audits(
        inputs.contract.project_root, evidence_reviews=evidence_reviews
    )
    editorial_audits = inspect_editorial_audits(
        inputs.contract.project_root, coverage_audits=coverage_audits
    )
    freezes = inspect_freezes(inputs.contract.project_root, editorial_audits=editorial_audits)
    for frozen in freezes:
        if section_states["DRAFTED"] > 0:
            section_states["DRAFTED"] -= 1
        section_states["FROZEN"] += 1
    answered = sum(int(row.get("answered") or 0) for row in coverage_audits)
    partial = sum(int(row.get("partial") or 0) for row in coverage_audits)
    not_answered = sum(int(row.get("not_answered") or 0) for row in coverage_audits)
    global_policy = inputs.contract.coverage_policy["global"]
    publication = inputs.contract.payload["publication_policy"]
    final_coverage = coverage_summary_from_counts(
        answered=answered,
        partial=partial,
        not_answered=not_answered,
        expected_total=inputs.contract.expected_structure["total_questions"],
        minimum_answered_count=global_policy["minimum_answered_count"],
        minimum_coverage=global_policy["minimum_coverage"],
        failure_status=publication["failure_status"],
    ).to_dict()
    blockers = ["GLOBAL_QUESTION_COVERAGE_NOT_AUDITED"]
    if len(freezes) < inputs.contract.expected_structure["question_bank_sections"]:
        blockers.insert(0, "UNFROZEN_SECTIONS")
    if prewriting.get("status") != "COMPLETE":
        blockers.insert(0, "PREWRITING_EVIDENCE_AUDIT_INCOMPLETE")
    return {
        "schema_version": "1.0",
        "book_inputs_valid": True,
        "input_counts": {
            "structural_headings": len(inputs.scope),
            "question_bank_sections": len(inputs.question_section_ids),
            "questions": len(inputs.questions),
        },
        "input_identities": dict(inputs.identities),
        "canonical": inventory.to_dict(),
        "retrieval_index_ready": retrieval.ready and inventory.ready,
        "retrieval_index": retrieval.to_dict(),
        "section_states": section_states,
        "frozen_count": len(freezes),
        "required_heading_count": inputs.contract.expected_structure["structural_headings"],
        "questions_pre_audited": int(prewriting.get("questions_audited") or 0),
        "prewriting_evidence_audit": prewriting or None,
        "sections_prepared": int((preparation or {}).get("sections_prepared") or 0),
        "section_preparation": preparation,
        "drafted_count": len(drafts),
        "active_drafts": drafts,
        "postwriting_evidence_review_count": len(evidence_reviews),
        "postwriting_evidence_reviews": evidence_reviews,
        "section_coverage_audit_count": len(coverage_audits),
        "section_coverage_audits": coverage_audits,
        "section_editorial_audit_count": len(editorial_audits),
        "section_editorial_audits": editorial_audits,
        "active_freezes": freezes,
        "final_questions_audited": answered + partial + not_answered,
        "final_question_coverage": final_coverage,
        "publication_eligible": False,
        "publication_blockers": blockers,
    }
