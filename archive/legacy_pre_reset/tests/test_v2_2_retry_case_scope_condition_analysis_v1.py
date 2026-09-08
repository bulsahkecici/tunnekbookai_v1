from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/architecture_v2_2_retry_case_scope_analysis_v1"


def load(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def analysis_module():
    path = ROOT / "scripts/76_v2_2_retry_case_scope_condition_analysis_v1.py"
    spec = importlib.util.spec_from_file_location("case_scope_analysis_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestAcceptanceFreeze(unittest.TestCase):
    def test_contract_was_frozen_before_probes(self):
        freeze = load("audits/acceptance_freeze_v1.json")
        self.assertTrue(freeze["frozen_before_probes_and_findings"])
        self.assertEqual(sha(ROOT / freeze["contract_path"]), freeze["contract_sha256"])


class TestConditionScopeProbes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = analysis_module().analyse()

    def test_exact_preserved_failure_is_reproduced(self):
        self.assertEqual(self.result["preserved_allocation"], {
            "failure_codes": ["CONDITION_DROPPED"], "conditions": ["In some"], "status": "REJECT"})

    def test_unit_and_paragraph_scope_are_distinguished(self):
        self.assertEqual(self.result["different_paragraph_control"]["conditions"],
                         ["In some", "dependent on tunnel size"])
        self.assertEqual(self.result["unit_condition_realized_control"]["status"], "ACCEPT")
        self.assertEqual(self.result["paragraph_scope_counterfactual"]["status"], "ACCEPT")

    def test_analysis_executes_no_prohibited_path(self):
        self.assertEqual(set(self.result["counts"].values()), {0})
        source = (ROOT / "scripts/76_v2_2_retry_case_scope_condition_analysis_v1.py").read_text()
        self.assertNotIn("scripts/75_", source)
        self.assertNotIn("render_markdown", source)


class TestAllocationFinding(unittest.TestCase):
    def test_role_sets_pass_but_condition_set_fails(self):
        audit = load("audits/allocation_audit_v1.json")
        sets = audit["set_relationships"]
        self.assertTrue(sets["required_roles_subset_available_roles"])
        self.assertTrue(sets["available_roles_subset_realizable_roles"])
        self.assertFalse(sets["required_conditions_subset_allocated_conditions"])
        self.assertFalse(audit["instruction_set_satisfiable_as_constructed"])

    def test_fallback_validator_and_observed_renderer_are_not_at_fault(self):
        audit = load("audits/allocation_audit_v1.json")
        self.assertFalse(audit["terminology_fallback_fault"])
        self.assertFalse(audit["validator_fault"])
        self.assertFalse(audit["renderer_fault_for_observed_failure"])

    def test_affected_universe_has_no_unexamined_contradiction(self):
        audit = load("audits/hidden_contradictions_v1.json")
        self.assertEqual(audit["unexamined_related_contradictions"], 0)
        self.assertEqual(len(audit["contradictions"]), 3)


if __name__ == "__main__":
    unittest.main()
