from __future__ import annotations

import unittest

from tunnelbookai.book.freeze import _citation_integrity, _freeze_checks


class SectionFreezeTests(unittest.TestCase):
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
            editorial={"audit_decision": "PASS"},
            citation={"decision": "PASS"},
            required_analysis_artifacts=[],
        )
        self.assertEqual(set(checks.values()), {"PASS"})
        checks = _freeze_checks(
            section_id="1.1",
            evidence={"audit_decision": "PASS", "material_issue_count": 0},
            coverage={"status": "COMPLETE", "question_count": 50},
            editorial={"audit_decision": "PASS"},
            citation={"decision": "PASS"},
            required_analysis_artifacts=[{"status": "AVAILABLE"}],
        )
        self.assertEqual(checks["REQUIRED_ANALYSIS_ARTIFACTS_SATISFIED"], "HOLD")


if __name__ == "__main__":
    unittest.main()
