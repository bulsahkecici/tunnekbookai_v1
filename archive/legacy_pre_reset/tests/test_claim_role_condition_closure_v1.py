from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/claim_role_condition_closure_v1"


def load(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def module():
    path = ROOT / "scripts/77_claim_role_condition_closure_v1.py"
    spec = importlib.util.spec_from_file_location("crcc_test_module", path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


class TestFreeze(unittest.TestCase):
    def test_preflight_is_zero_drift(self):
        audit = load("audits/frozen_preflight_v1.json")
        self.assertEqual(audit["status"], "PASS")
        self.assertEqual(audit["drift_count"], 0)
        self.assertEqual(len(audit["artifacts"]), 21)
        for relative, expected in audit["artifacts"].items():
            self.assertEqual(sha(ROOT / relative), expected)

    def test_acceptance_was_frozen_before_execution(self):
        freeze = load("audits/acceptance_freeze_v1.json")
        self.assertTrue(freeze["frozen_before_implementation_and_fixture_execution"])
        self.assertEqual(sha(ROOT / freeze["contract_path"]), freeze["contract_sha256"])

    def test_postflight_is_zero_drift(self):
        postflight = load("audits/frozen_postflight_v1.json")
        self.assertEqual(postflight["status"], "PASS")
        self.assertEqual(postflight["drift_count"], 0)
        self.assertEqual(postflight["artifacts_rehashed"], 21)


class TestGeneralContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = module()

    def test_contract_and_implementation_have_no_claim_branch(self):
        contract = (BASE / "contracts/claim_role_condition_closure_contract_v1.json").read_text()
        source = (ROOT / "scripts/77_claim_role_condition_closure_v1.py").read_text()
        self.assertNotIn("SEC-02-2-P0-008", contract)
        self.assertNotIn("SEC-02-2-P0-008", source)

    def test_complete_allocated_universe_closes(self):
        result = self.mod.validate(load("proof/allocated_role_condition_plan_v1.json"))
        self.assertEqual(result["status"], "ACCEPT")
        self.assertEqual(result["checked_instances"], 20)
        self.assertTrue(all(row["role_feasible"] for row in result["role_feasibility"]))
        universe = load("contracts/planner_option_universe_v2_2_condition_closed_v1.json")
        self.assertTrue(universe["realizable_role_subset_condition_closed"])
        self.assertEqual(universe["fully_feasible_instances"], 20)

    def test_fixture_gate(self):
        result = self.mod.evaluate_fixtures()
        self.assertEqual(result["positive_count"], 6)
        self.assertEqual(result["negative_count"], 10)
        self.assertEqual(result["false_accepts"], 0)
        self.assertEqual(result["false_rejects"], 0)
        self.assertEqual(result["code_mismatches"], 0)

    def test_each_negative_rejects_with_expected_code(self):
        fixtures = load("fixtures/closure_fixtures_v1.json")["fixtures"]
        for fixture in fixtures:
            result = self.mod.validate(fixture["plan"])
            self.assertEqual(result["status"], fixture["expected_status"], fixture["fixture_id"])
            self.assertTrue(set(fixture["expected_codes"]).issubset(result["failure_codes"]),
                            fixture["fixture_id"])


class TestP0008DerivedAllocation(unittest.TestCase):
    def test_historical_allocation_is_unconstructible(self):
        result = module().evaluate_fixtures()["results"]
        row = next(item for item in result if item["fixture_id"] == "NEG-CRCC-09-P0008-HISTORICAL-INVALID")
        self.assertEqual(row["actual_status"], "REJECT")
        self.assertIn("CRCC_CONDITION_OWNER_MISSING", row["failure_codes"])

    def test_safe_allocation_preserves_dependency_cases_and_fallback(self):
        audit = load("audits/p0_008_safe_allocation_v1.json")
        self.assertTrue(audit["dependency_closed"])
        self.assertTrue(audit["all_required_conditions_closed"])
        self.assertEqual([row["case_id"] for row in audit["cases"]],
                         ["ROCK-CRUSHED", "ROCK-SQUEEZING", "ROCK-SWELLING"])
        swelling = audit["cases"][2]
        self.assertEqual(swelling["status"], "ORIGINAL_TERM_UNRESOLVED")
        self.assertEqual(swelling["surface"], "**Swelling Rock**")

    def test_no_execution_counts_are_embedded_in_safe_allocation(self):
        audit = load("audits/p0_008_safe_allocation_v1.json")
        self.assertFalse(audit["visible_prose_created"])
        self.assertFalse(audit["retry_executed"])


class TestAcceptance(unittest.TestCase):
    def test_gate_is_closed_go_with_zero_operation_counts(self):
        result = load("audits/acceptance_results_v1.json")
        self.assertEqual(result["verdict"], "CLOSED_GO")
        self.assertEqual(result["failed"], 0)
        self.assertEqual(set(result["accounting"].values()), {0})


if __name__ == "__main__":
    unittest.main()
