"""Positive and adversarial fixtures for phase 89's fail-closed rules."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/89_prewriting_repository_authority_status_residual_locator_remediation_v1.py"
SPEC = importlib.util.spec_from_file_location("phase89", SCRIPT)
PHASE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(PHASE)


def _status(**changes):
    value = {
        "support_status": "VERIFIED_SUPPORT",
        "provenance_status": "COMPLETE",
        "authority_status": "UNKNOWN",
        "scope_status": "VALID",
        "anchor_status": "UNIQUE",
        "qualifier_condition_modality_integrity": "PASS",
        "numeric_unit_date_integrity": "PASS",
    }
    value.update(changes)
    return value


def _claim():
    return {
        "claim_id": "CLM-TEST",
        "section_id": "SEC-TEST",
        "research_question_id": "RQ-TEST",
        "evidence_need_id": "EN-TEST",
        "provenance": {"document_id": "DOC000214", "source_relative_path": "source.pdf", "source_sha256": "abc"},
        "structured_normalized_semantic_proposition": {"source_faithful_canonical_text": "Exact supported proposition."},
        "support_anchor": {"exact_text": "Exact supported proposition."},
        "scope_validation": {"section_and_rq_match": True},
    }


def test_required_positive_and_negative_fixtures():
    # Positive: verified support remains useful but non-admissible with unknown authority.
    status = _status()
    assert PHASE.derive_admission(status) == "SUPPORTING_ONLY"

    # Positive: only explicit structured authority evidence can promote.
    assert PHASE.explicit_authority({"standard_identifier": "ISO-X", "document_type": "standard"})[:2] == (
        "STANDARD_SPECIFICATION", "SUITABLE")
    assert PHASE.explicit_authority({"organization": "Agency", "document_type": "official report"})[:2] == (
        "PRIMARY_OFFICIAL", "SUITABLE")
    assert PHASE.explicit_authority({"publisher": "Journal", "peer_reviewed": True})[:2] == (
        "PEER_REVIEWED", "SUITABLE")
    assert PHASE.explicit_authority({})[:2] == ("UNKNOWN_AUTHORITY", "UNKNOWN")

    claim = _claim()
    complete_chunk = {"chunk_id": "CHK-1", "text": "Exact supported proposition.",
                      "normalized_source_sha256": "def", "original_page_start": 20, "original_page_end": 20}
    assert PHASE.recover_bridge(claim, complete_chunk)["bridge_class"] == "BRIDGE_RESOLVED"
    partial_chunk = {**complete_chunk, "original_page_start": None, "original_page_end": None}
    assert PHASE.recover_bridge(claim, partial_chunk)["bridge_class"] == "PARTIAL_LOCATOR"

    candidates = {"candidates": [{"block_ref": "texts[89]", "page_no": 20},
                                  {"block_ref": "texts[90]", "page_no": 21}]}
    frozen = copy.deepcopy(claim)
    extracted = PHASE.reextract_occurrences(claim, candidates)
    assert len(extracted) == 2 and all(x["orthogonal_status"]["anchor_status"] == "UNIQUE" for x in extracted)
    assert claim == frozen  # historical record is never overwritten
    assert {x["locator"]["page_no"] for x in extracted} == {20, 21}

    # Negative: neither authority nor scope failure can mask independently verified support.
    verdict, _ = PHASE.support_verdict(claim, complete_chunk)
    assert verdict == "VERIFIED_SUPPORT"
    assert PHASE.derive_admission(_status(scope_status="INSUFFICIENT")) == "BLOCKED"
    assert PHASE.derive_admission(_status(authority_status="UNKNOWN")) == "SUPPORTING_ONLY"

    # Negative: filenames, legacy C/D labels, and body-like fields are not authority evidence.
    forbidden = {"filename": "official_iso_standard.pdf", "legacy_class": "C", "title": "Government manual"}
    assert PHASE.explicit_authority(forbidden)[:2] == ("UNKNOWN_AUTHORITY", "UNKNOWN")

    # Negative: similarity cannot establish provenance and occurrence choice is not guessed.
    similar = {**complete_chunk, "text": "A merely similar supported proposition."}
    assert PHASE.recover_bridge(claim, similar)["bridge_class"] == "MISSING_JOIN"
    assert len(PHASE.reextract_occurrences(claim, candidates)) == len(candidates["candidates"])

    # Negative: a project-specific scope failure cannot be universalized into admission.
    assert PHASE.derive_admission(_status(scope_status="INSUFFICIENT", authority_status="SUITABLE")) == "BLOCKED"

    contract = PHASE.load(PHASE.CONTRACT)
    assert contract["prohibitions"]["external_evidence"] is True
    assert contract["prohibitions"]["book_prose"] is True


if __name__ == "__main__":
    test_required_positive_and_negative_fixtures()
    print("PASS: required positive and negative fixtures")
