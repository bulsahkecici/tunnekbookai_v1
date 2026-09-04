from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/architecture_v2_2_retry_v1"


def load(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TestFrozenGate(unittest.TestCase):
    def test_preflight_has_zero_live_drift(self):
        preflight = load("audits/frozen_preflight_v1.json")
        self.assertEqual(preflight["drift_count"], 0)
        self.assertEqual(len(preflight["artifacts"]), 49)
        for relative, expected in preflight["artifacts"].items():
            self.assertEqual(sha256(ROOT / relative), expected)

    def test_retry_acceptance_contract_is_frozen(self):
        freeze = load("audits/acceptance_freeze_v1.json")
        self.assertTrue(freeze["frozen_before_integration_and_rendering"])
        self.assertEqual(sha256(ROOT / freeze["contract_path"]), freeze["contract_sha256"])

    def test_fallback_acceptance_sha_is_unchanged(self):
        path = ROOT / "data/book/drafting/technical_term_fallback_v1/contracts/technical_term_original_language_fallback_acceptance_contract_v1.json"
        self.assertEqual(sha256(path), "b438197c9b0fd14cd2a39822b0729895c81017a44f022432a3b8b75a2e10a672")


class TestRetryConstruction(unittest.TestCase):
    def test_plan_is_deterministic_not_model_generated(self):
        plan = load("plan/integration_plan_v2_2_retry_v1.json")
        self.assertFalse(plan["model_generated"])
        self.assertEqual(plan["required_topics"], ["dayanım sınıfı", "çimento dozajı", "kaplama kalınlığı"])

    def test_retry_universe_is_loadable(self):
        universe = load("contracts/planner_option_universe_v2_2_retry_v1.json")
        self.assertEqual(universe["build_status"], "LOADABLE")
        self.assertEqual(universe["unrealizable_roles"], 0)

    def test_renderer_module_has_no_target_specific_branch(self):
        source = (ROOT / "scripts/75_architecture_v2_2_retry_integration_v1.py").read_text(encoding="utf-8")
        self.assertNotIn("Swelling Rock", source)
        self.assertNotIn("SEC-02-2-P0-008", source)


class TestFailureClosure(unittest.TestCase):
    def test_exact_validator_failure_is_preserved(self):
        audit = load("audits/failure_evidence_v1.json")
        self.assertEqual(audit["failure_histogram"], {"CONDITION_DROPPED": 1})
        self.assertEqual(audit["rejected_units"][0]["unit_id"], "U-C-P02-S02")
        self.assertFalse(audit["repair_attempted"])

    def test_fallback_passed_but_blocker_surface_is_five_of_six(self):
        audit = load("audits/integration_audit_v1.json")
        self.assertEqual(audit["swelling_rock"]["fallback_status"], "PASS")
        self.assertEqual(audit["technical_blockers_surface_validated"], "5/6")
        self.assertEqual(audit["factual_completeness"], "FAIL_REQUIRED_UNIT_REJECTED")

    def test_no_rejected_draft_was_stored(self):
        self.assertEqual(list(BASE.rglob("*.md")), [])
        self.assertEqual(load("audits/failure_evidence_v1.json")["stored_draft_artifacts"], 0)

    def test_acceptance_is_closed_no_go(self):
        result = load("audits/acceptance_results_v1.json")
        self.assertEqual(result["verdict"], "CLOSED_NO_GO")
        self.assertEqual(result["summary"]["failed"], 6)

    def test_postflight_has_zero_drift(self):
        postflight = load("audits/frozen_postflight_v1.json")
        self.assertEqual(postflight["drift_count"], 0)
        self.assertTrue(postflight["acceptance_contract_unamended"])

    def test_manifest_hashes_and_accounting(self):
        path = ROOT / "data/book/manifests/sec_02_2_architecture_v2_2_technical_style_integration_retry_v1.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "CLOSED_NO_GO")
        for artifact in manifest["artifacts"].values():
            self.assertEqual(sha256(ROOT / artifact["path"]), artifact["sha256"])
        self.assertEqual(manifest["accounting"]["generation_calls"], 0)
        self.assertEqual(manifest["accounting"]["stored_drafts"], 0)


if __name__ == "__main__":
    unittest.main()
