import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/80_sec_02_2_technical_draft_reaudit_v2_failure_analysis.py"
SPEC = importlib.util.spec_from_file_location("failure_analysis", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TestFailureAnalysis(unittest.TestCase):
    def setUp(self):
        self.result = MODULE.evaluate()

    def test_analysis_closes_go(self):
        self.assertEqual("CLOSED_GO", self.result["status"])
        self.assertEqual("PASS", self.result["input_hashes"]["status"])

    def test_all_findings_are_reproduced(self):
        self.assertTrue(all(self.result["probes"].values()))

    def test_blockers_are_independently_causal(self):
        for finding in ("RA2-B01", "RA2-B02", "RA2-B03"):
            self.assertTrue(self.result["causes"][finding]["independently_blocking"])
        self.assertFalse(self.result["causes"]["RA2-A01"]["independently_blocking"])

    def test_fault_boundaries_are_explicit(self):
        self.assertEqual("COVERAGE_GAP_NOT_EXECUTION_DEFECT", self.result["validator_fault"]["kind"])
        self.assertEqual(["RA2-B01", "RA2-B02"], self.result["renderer_fault"]["scope"])
        self.assertFalse(self.result["style_contract_fault"])

    def test_remediation_is_general_and_non_mutating(self):
        remediation = self.result["smallest_general_remediation"]
        self.assertEqual(0, remediation["claim_specific_rules"])
        self.assertEqual(0, sum(self.result["accounting"].values()))

    def test_fresh_process_is_deterministic(self):
        first = subprocess.check_output([sys.executable, str(SCRIPT)], cwd=ROOT)
        second = subprocess.check_output([sys.executable, str(SCRIPT)], cwd=ROOT)
        self.assertEqual(first, second)
        self.assertEqual(self.result, json.loads(first))


if __name__ == "__main__":
    unittest.main()
