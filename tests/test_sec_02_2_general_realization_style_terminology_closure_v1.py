from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/81_sec_02_2_general_realization_style_terminology_closure_v1.py"
CONTRACT = ROOT / "data/book/drafting/sec_02_2/general_realization_style_terminology_closure_v1/contracts/general_closure_contract_v1.json"
AUDIT = ROOT / "data/book/drafting/sec_02_2/general_realization_style_terminology_closure_v1/audits/general_closure_audit_v1.json"
SPEC = importlib.util.spec_from_file_location("general_closure_v1", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class TestGeneralClosure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = MODULE.evaluate()

    def test_phase_closes_go(self):
        self.assertEqual("CLOSED_GO", self.result["status"])
        self.assertEqual(0, self.result["fixtures"]["false_accepts"])
        self.assertEqual(0, self.result["fixtures"]["false_rejects"])
        self.assertEqual(0, self.result["fixtures"]["code_mismatches"])
        self.assertEqual(0, self.result["fixtures"]["advisory_mismatches"])

    def test_positive_passes_and_negative_rejects(self):
        rows = self.result["fixtures"]["results"]
        self.assertTrue(all(row["actual"] == row["expected"] for row in rows))
        self.assertEqual(3, self.result["fixtures"]["positive_count"])
        self.assertEqual(4, self.result["fixtures"]["negative_count"])

    def test_prior_patterns_are_closed(self):
        disposition = self.result["failure_pattern_disposition"]
        self.assertEqual("REJECT_PRE_RELEASE", disposition["semantic_subject_misbinding"])
        self.assertEqual("REJECT_PRE_OR_POST_RENDER", disposition["fragment_and_note_label_projection"])
        self.assertEqual("REJECT_PRE_OR_POST_RENDER", disposition["free_terminology_variant"])
        self.assertEqual("DETECTED_ADVISORY", disposition["strength_class_unit_redundancy"])

    def test_preserves_prior_closures_and_frozen_inputs(self):
        self.assertEqual("6/6", self.result["preservation"]["six_technical_blockers"])
        self.assertEqual("25/25", self.result["preservation"]["condition_requirements"])
        self.assertEqual("2/2", self.result["preservation"]["dependency_requirements"])
        self.assertEqual("PASS", self.result["frozen_integrity"]["status"])
        self.assertEqual(0, self.result["frozen_integrity"]["drift"])

    def test_general_not_claim_specific_and_no_rewrite(self):
        source = SCRIPT.read_text(encoding="utf-8") + CONTRACT.read_text(encoding="utf-8")
        self.assertNotIn("SEC-02-2-C-002", source)
        self.assertNotIn("U-A-P02-S02", source)
        self.assertEqual({0}, set(self.result["accounting"].values()))

    def test_fresh_process_is_deterministic(self):
        first = subprocess.check_output([sys.executable, str(SCRIPT)], cwd=ROOT)
        second = subprocess.check_output([sys.executable, str(SCRIPT)], cwd=ROOT)
        self.assertEqual(first, second)
        self.assertEqual(self.result, json.loads(first))

    def test_recorded_audit_matches_gate(self):
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(self.result["status"], audit["status"])
        self.assertEqual(self.result["next_phase"], audit["next_phase"])
        self.assertEqual(self.result["frozen_integrity"]["drift"], audit["frozen_integrity"]["drift"])
        self.assertEqual(self.result["fixtures"]["false_accepts"], audit["fixture_results"]["false_accepts"])
        self.assertEqual(self.result["failure_pattern_disposition"], audit["failure_pattern_disposition"])


if __name__ == "__main__":
    unittest.main()
