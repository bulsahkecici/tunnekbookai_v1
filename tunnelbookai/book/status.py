"""Read-only operational status for the book-production foundation."""

from __future__ import annotations

from typing import Any

from tunnelbookai.canonical.paths import CanonicalContext
from tunnelbookai.canonical.verifier import inspect_canonical
from .inputs import BookInputs


def build_status(inputs: BookInputs) -> dict[str, Any]:
    inventory = inspect_canonical(context=CanonicalContext.load(book_inputs=inputs))
    retrieval_manifest = inputs.contract.project_root / "book" / "retrieval" / "index_manifest.json"
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
        "retrieval_index_ready": retrieval_manifest.is_file() and inventory.ready,
        "section_states": {
            "READY": 0,
            "EVIDENCE_GAP": 0,
            "DRAFTED": 0,
            "AUDIT_HOLD": 0,
            "FROZEN": 0,
            "NOT_STARTED": len(inputs.scope),
        },
        "frozen_count": 0,
        "required_heading_count": inputs.contract.expected_structure["structural_headings"],
        "questions_pre_audited": 0,
        "final_questions_audited": 0,
        "final_question_coverage": None,
        "publication_eligible": False,
        "publication_blockers": [
            "BOOK_PRODUCTION_STAGES_NOT_IMPLEMENTED",
            "CANONICAL_CORPUS_NOT_READY" if not inventory.ready else "NO_FROZEN_SECTIONS",
            "GLOBAL_QUESTION_COVERAGE_NOT_AUDITED",
        ],
    }
