import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/83_prewriting_repository_evidence_discovery_admission_remediation_v1.py"
OUT = ROOT / "data/book/prewriting_repository_evidence_discovery_admission_remediation_v1"
SPEC = importlib.util.spec_from_file_location("remediation", SCRIPT)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def tree_hashes():
    result = {}
    for path in sorted(OUT.glob("*.json")):
        result[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


class RemediationUnitTests(unittest.TestCase):
    def test_positive_complete_claim_is_admissible(self):
        admitted, reasons = MOD.final_admission_decision({
            "granularity": "CLAIM_LEVEL_CONTENT_SUPPORT", "authority_status": "ACCEPTABLE",
            "provenance_status": "COMPLETE", "scope_validated": True,
        })
        self.assertTrue(admitted)
        self.assertEqual(reasons, [])

    def test_positive_scoped_candidate(self):
        valid, reason = MOD.validate_scoped_candidate(
            {"section_id": "S1", "research_question_id": "RQ1", "evidence_need_id": "EN1"}, "S1", "RQ1"
        )
        self.assertTrue(valid)
        self.assertEqual(reason, "SCOPED")

    def test_positive_contract_is_frozen(self):
        contract = json.loads((OUT / "remediation_acceptance_contract_v1.json").read_text())
        self.assertTrue(contract["frozen_before_implementation"])

    def test_positive_visual_discovery_executed(self):
        audit = json.loads((OUT / "visual_discovery_audit_v1.json").read_text())
        self.assertTrue(audit["discovery_executed"])
        self.assertGreater(audit["candidate_count"], 0)

    def test_positive_all_defect_counts_are_accounted_for(self):
        audit = json.loads((OUT / "remediation_acceptance_audit_v1.json").read_text())
        self.assertEqual((audit["discovery_gap_resolved"], audit["granularity_mismatch_resolved"], audit["provenance_gap_resolved"]), (172, 37, 2))

    def test_negative_topical_match_is_not_admissible(self):
        admitted, reasons = MOD.final_admission_decision({
            "granularity": "EVIDENCE_NEED_MATCH", "authority_status": "ACCEPTABLE",
            "provenance_status": "COMPLETE", "scope_validated": True,
        })
        self.assertFalse(admitted)
        self.assertIn("CLAIM_LEVEL_CONTENT_SUPPORT_NOT_VALIDATED", reasons)

    def test_negative_unvalidated_authority_fails_closed(self):
        admitted, reasons = MOD.final_admission_decision({
            "granularity": "CLAIM_LEVEL_CONTENT_SUPPORT", "authority_status": "NOT_VALIDATED",
            "provenance_status": "COMPLETE", "scope_validated": True,
        })
        self.assertFalse(admitted)
        self.assertIn("AUTHORITY_NOT_VALIDATED", reasons)

    def test_negative_incomplete_provenance_fails_closed(self):
        admitted, reasons = MOD.final_admission_decision({
            "granularity": "CLAIM_LEVEL_CONTENT_SUPPORT", "authority_status": "ACCEPTABLE",
            "provenance_status": "INCOMPLETE", "scope_validated": True,
        })
        self.assertFalse(admitted)
        self.assertIn("PROVENANCE_NOT_COMPLETE", reasons)

    def test_negative_cross_section_reuse_is_rejected(self):
        valid, reason = MOD.validate_scoped_candidate(
            {"section_id": "S1", "research_question_id": "RQ1", "evidence_need_id": "EN1"}, "S2", "RQ1"
        )
        self.assertFalse(valid)
        self.assertEqual(reason, "SECTION_SCOPE_MISMATCH")

    def test_negative_cross_question_reuse_is_rejected(self):
        valid, reason = MOD.validate_scoped_candidate(
            {"section_id": "S1", "research_question_id": "RQ1", "evidence_need_id": "EN1"}, "S1", "RQ2"
        )
        self.assertFalse(valid)
        self.assertEqual(reason, "RESEARCH_QUESTION_SCOPE_MISMATCH")

    def test_negative_missing_evidence_need_is_rejected(self):
        valid, reason = MOD.validate_scoped_candidate(
            {"section_id": "S1", "research_question_id": "RQ1"}, "S1", "RQ1"
        )
        self.assertFalse(valid)
        self.assertEqual(reason, "EVIDENCE_NEED_MISSING")


class RemediationDeterminismTests(unittest.TestCase):
    def test_rerun_is_byte_deterministic(self):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
        first = tree_hashes()
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
        self.assertEqual(first, tree_hashes())


if __name__ == "__main__":
    unittest.main()
