from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/terminology_resolution_v1"


def load(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_validator():
    path = ROOT / "scripts/73_p0_008_claim_owned_terminology_resolution_v1.py"
    spec = importlib.util.spec_from_file_location("p0_008_terminology_resolution", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestFrozenGate(unittest.TestCase):
    def test_acceptance_contract_was_frozen_before_adjudication(self):
        freeze = load("audits/acceptance_freeze_v1.json")
        self.assertTrue(freeze["frozen_before_evidence_adjudication"])
        self.assertFalse(freeze["amendment_allowed"])
        self.assertEqual(sha256(ROOT / freeze["contract_path"]), freeze["contract_sha256"])

    def test_frozen_artifacts_have_zero_drift(self):
        preflight = load("audits/frozen_preflight_v1.json")
        self.assertEqual(preflight["drift_count"], 0)
        for relative, expected in preflight["artifacts"].items():
            with self.subTest(path=relative):
                self.assertEqual(sha256(ROOT / relative), expected)


class TestEvidenceDecision(unittest.TestCase):
    def test_exact_english_case_and_dependency_are_preserved(self):
        audit = load("audits/terminology_evidence_audit_v1.json")
        self.assertEqual(audit["source_label"], "Swelling Rock")
        self.assertTrue(audit["direct_evidence"]["exact_case_label_present"])
        self.assertTrue(audit["direct_evidence"]["tunnel_size_dependency_present"])

    def test_direct_source_has_no_turkish_equivalent(self):
        audit = load("audits/terminology_evidence_audit_v1.json")
        self.assertEqual(audit["direct_evidence"]["language"], "en")
        self.assertFalse(audit["direct_evidence"]["turkish_equivalent_present"])

    def test_approved_mapping_has_no_swelling_term(self):
        audit = load("audits/terminology_evidence_audit_v1.json")
        mapping = audit["approved_mapping_check"]
        self.assertEqual(mapping["approved_swelling_rock_terms"], [])
        self.assertEqual(mapping["competing_supported_terms"], [])
        self.assertEqual(audit["decision_class"], "CASE_3")

    def test_no_claim_owned_contract_created(self):
        audit = load("audits/terminology_evidence_audit_v1.json")
        self.assertIsNone(audit["claim_owned_term_selected"])
        self.assertFalse(audit["claim_owned_terminology_contract_created"])
        self.assertFalse((BASE / "contracts/p0_008_claim_owned_terminology_contract_v1.json").exists())

    def test_existing_case_mappings_are_unchanged(self):
        v22 = json.loads((ROOT / "data/book/drafting/sec_02_2/architecture_v2_2/contracts/claim_realization_contract_v2_2.json").read_text(encoding="utf-8"))
        entry = next(item for item in v22["entries"] if item["entry_id"] == "V22-P0008-CASE-001")
        terms = {item["case_id"]: item["turkish_term"] for item in entry["case_terms"]}
        self.assertEqual(terms["ROCK-CRUSHED"], "ezilmiş kaya")
        self.assertEqual(terms["ROCK-SQUEEZING"], "sıkışan kaya")


class TestNegativeFixtures(unittest.TestCase):
    def test_all_required_negative_classes_reject(self):
        validator = load_validator()
        fixtures = load("fixtures/negative_fixtures_v1.json")["fixtures"]
        self.assertEqual({item["class"] for item in fixtures}, {
            "unsupported_synonym", "english_term_leak", "cross_claim_terminology_borrowing",
            "wrong_case_mapping", "generic_rock_substitution",
        })
        for fixture in fixtures:
            with self.subTest(fixture=fixture["fixture_id"]):
                self.assertEqual(validator.validate_candidate(fixture["candidate"]), fixture["expected_code"])

    def test_evaluator_fails_closed(self):
        result = load_validator().evaluate()
        self.assertEqual(result["status"], "NO_GO")
        self.assertEqual(result["decision_class"], "CASE_3")
        self.assertIsNone(result["selected_term"])


class TestOutcome(unittest.TestCase):
    def test_no_generation_or_render_artifact_exists(self):
        self.assertEqual(list(BASE.rglob("*.md")), [])
        self.assertEqual(list(BASE.rglob("*render*")), [])

    def test_acceptance_result_is_no_go(self):
        result = load("audits/acceptance_results_v1.json")
        self.assertEqual(result["verdict"], "CLOSED_NO_GO")
        self.assertEqual(result["decision_class"], "CASE_3")

    def test_manifest_accounting_is_zero(self):
        manifest = json.loads((ROOT / "data/book/manifests/sec_02_2_p0_008_claim_owned_terminology_resolution_v1.json").read_text(encoding="utf-8"))
        for artifact in manifest["artifacts"].values():
            with self.subTest(path=artifact["path"]):
                self.assertEqual(sha256(ROOT / artifact["path"]), artifact["sha256"])
        for field, value in manifest["accounting"].items():
            if field == "targeted_evidence_records_read":
                self.assertEqual(value, 2)
            else:
                self.assertEqual(value, 0, field)


if __name__ == "__main__":
    unittest.main()
