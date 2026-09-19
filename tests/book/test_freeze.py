from __future__ import annotations

import unittest

from tunnelbookai.book.errors import BookEngineError
from tunnelbookai.book.freeze import _citation_integrity, _freeze_checks, record_operator_approval

from tests.canonical.fixtures import SyntheticRepo


class SectionFreezeTests(unittest.TestCase):
    def test_operator_approval_requires_an_audited_active_draft(self):
        repo = SyntheticRepo()
        try:
            with self.assertRaises(BookEngineError) as caught:
                record_operator_approval("1.1", repo.root, note="Okudum.")
            self.assertEqual(caught.exception.code, "OPERATOR_APPROVAL_PREREQUISITE_MISSING")
            with self.assertRaises(BookEngineError) as caught:
                record_operator_approval("1.1", repo.root, note="   ")
            self.assertEqual(caught.exception.code, "OPERATOR_APPROVAL_NOTE_REQUIRED")
        finally:
            repo.close()

    def test_citation_integrity_reconstructs_claim_provenance(self):
        sentence_map = {"sentences": [{
            "sentence_id": "1.1-S001", "claim_ids": ["CLM_1"],
        }]}
        registry = {"claims": [{
            "claim_id": "CLM_1", "document_id": "ING_1", "locator": "ING_1:CH_1:p1",
        }]}
        evidence = [{
            "sentence_id": "1.1-S001", "status": "SUPPORTED",
            "supporting_claim_ids": ["CLM_1"], "supporting_document_ids": ["ING_1"],
            "source_locators": ["ING_1:CH_1:p1"],
        }]
        result = _citation_integrity(sentence_map, evidence, registry)
        self.assertEqual(result["decision"], "PASS")
        self.assertEqual(result["errors"], [])

    def test_every_contractual_gate_must_pass(self):
        checks = _freeze_checks(
            section_id="1.1",
            evidence={"audit_decision": "PASS", "material_issue_count": 0},
            coverage={"status": "COMPLETE", "question_count": 50},
            editorial={"audit_decision": "PASS", "audit_id": "EDA_1"},
            citation={"decision": "PASS"},
            required_analysis_artifacts=[],
            expected_questions=50,
            operator_approval={"draft_id": "DRF_x", "draft_sha256": "abc", "editorial_audit_id": "EDA_1", "note": "Okudum; bölüm olarak kabul."},
            draft={"draft_id": "DRF_x", "draft_sha256": "abc"},
        )
        self.assertEqual(set(checks.values()), {"PASS"})
        # No approval, or an approval for another draft/edit round, holds the freeze.
        self.assertEqual(_freeze_checks(
            section_id="1.1",
            evidence={"audit_decision": "PASS", "material_issue_count": 0},
            coverage={"status": "COMPLETE", "question_count": 50},
            editorial={"audit_decision": "PASS", "audit_id": "EDA_1"},
            citation={"decision": "PASS"},
            required_analysis_artifacts=[],
            expected_questions=50,
        )["OPERATOR_READ_APPROVAL_PASS"], "HOLD")
        self.assertEqual(_freeze_checks(
            section_id="1.1",
            evidence={"audit_decision": "PASS", "material_issue_count": 0},
            coverage={"status": "COMPLETE", "question_count": 50},
            editorial={"audit_decision": "PASS", "audit_id": "EDA_2"},
            citation={"decision": "PASS"},
            required_analysis_artifacts=[],
            expected_questions=50,
            operator_approval={"draft_id": "DRF_x", "draft_sha256": "abc", "editorial_audit_id": "EDA_1", "note": "eski tur"},
            draft={"draft_id": "DRF_x", "draft_sha256": "abc"},
        )["OPERATOR_READ_APPROVAL_PASS"], "HOLD")
        checks = _freeze_checks(
            section_id="1.1",
            evidence={"audit_decision": "PASS", "material_issue_count": 0},
            coverage={"status": "COMPLETE", "question_count": 50},
            editorial={"audit_decision": "PASS", "audit_id": "EDA_1"},
            citation={"decision": "PASS"},
            required_analysis_artifacts=[{"status": "AVAILABLE"}],
            expected_questions=50,
        )
        self.assertEqual(checks["REQUIRED_ANALYSIS_ARTIFACTS_SATISFIED"], "HOLD")
        checks = _freeze_checks(
            section_id="1.1",
            evidence={"audit_decision": "PASS", "material_issue_count": 0},
            coverage={"status": "COMPLETE", "question_count": 50},
            editorial={"audit_decision": "PASS", "audit_id": "EDA_1"},
            citation={"decision": "PASS"},
            required_analysis_artifacts=[],
            expected_questions=17,
        )
        self.assertEqual(checks["QUESTION_COVERAGE_AUDIT_COMPLETE"], "HOLD")


if __name__ == "__main__":
    unittest.main()
