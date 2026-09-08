from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/technical_draft_reaudit_v2"
SCRIPT = ROOT / "scripts/79_sec_02_2_technical_draft_reaudit_v2.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


spec = importlib.util.spec_from_file_location("technical_reaudit_v2", SCRIPT)
reaudit = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = reaudit
spec.loader.exec_module(reaudit)


class TestTechnicalDraftReauditV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = reaudit.evaluate()

    def test_acceptance_contract_is_frozen_and_hash_bound(self):
        contract = load(BASE / "contracts/technical_draft_reaudit_acceptance_contract_v2.json")
        self.assertTrue(contract["frozen_before_audit"])
        for row in contract["inputs"]:
            self.assertEqual(reaudit.sha256(ROOT / row["path"]), row["sha256"])

    def test_reaudit_is_no_go_with_three_blocking_findings(self):
        self.assertEqual(self.result["status"], "CLOSED_NO_GO")
        self.assertEqual(len(self.result["blocking_findings"]), 3)

    def test_six_prior_blockers_are_independently_checked(self):
        status = self.result["six_blocker_status"]
        self.assertEqual((status["closed"], status["total"]), (5, 6))
        self.assertEqual(status["checks"]["TDA-006"], "REOPENED")

    def test_citation_allocation_passes_but_one_surface_is_ambiguous(self):
        citation = self.result["citation_support"]
        self.assertEqual(citation["claim_source_intents"], "19/19")
        self.assertEqual(citation["misleading_cement_allocations"], 0)
        self.assertEqual(citation["unambiguous_surface_units"], "18/19")

    def test_scope_cases_dependency_and_fallback_pass(self):
        result = self.result["terminology_scope"]
        self.assertEqual(result["scope_bindings"], "3/3 PASS")
        self.assertEqual(result["p0_008_cases_dependency"], "PASS")
        self.assertEqual(result["unresolved_term_fallback"], "PASS")

    def test_style_and_terminology_fail_closed(self):
        self.assertEqual(self.result["book_style"]["status"], "FAIL")
        self.assertEqual(self.result["terminology_scope"]["layer_terminology"], "FAIL")

    def test_validator_result_is_preserved(self):
        validation = self.result["validation"]
        self.assertEqual(validation["status"], "ACCEPT")
        self.assertEqual(validation["failure_histogram"], {})
        self.assertEqual(validation["rejected_units"], [])

    def test_no_mutating_or_external_accounting(self):
        self.assertEqual(set(self.result["accounting"].values()), {0})

    def test_output_is_deterministic_in_fresh_process(self):
        local = reaudit.canonical_bytes(reaudit.evaluate())
        fresh = subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True).stdout
        self.assertEqual(local, fresh)
        self.assertEqual(hashlib.sha256(local).hexdigest(), hashlib.sha256(fresh).hexdigest())


if __name__ == "__main__":
    unittest.main()
