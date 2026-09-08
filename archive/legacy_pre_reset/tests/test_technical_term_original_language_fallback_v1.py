from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/technical_term_fallback_v1"


def load(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def implementation():
    path = ROOT / "scripts/74_technical_term_original_language_fallback_v1.py"
    spec = importlib.util.spec_from_file_location("technical_term_fallback", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestFrozenGate(unittest.TestCase):
    def test_preflight_has_zero_live_drift(self):
        preflight = load("audits/frozen_preflight_v1.json")
        self.assertEqual(preflight["drift_count"], 0)
        for relative, expected in preflight["artifacts"].items():
            with self.subTest(path=relative):
                self.assertEqual(sha256(ROOT / relative), expected)

    def test_acceptance_contract_is_frozen(self):
        freeze = load("audits/acceptance_freeze_v1.json")
        self.assertTrue(freeze["frozen_before_implementation"])
        self.assertFalse(freeze["amendment_allowed"])
        self.assertEqual(sha256(ROOT / freeze["contract_path"]), freeze["contract_sha256"])


class TestGeneralContract(unittest.TestCase):
    def test_required_states_and_replacement_are_structural(self):
        contract = load("contracts/technical_term_original_language_fallback_contract_v1.json")
        self.assertEqual(set(contract["states"]), {"AUTHORITATIVE_TRANSLATION", "ORIGINAL_TERM_UNRESOLVED"})
        self.assertTrue(contract["replacement"]["historical_records_immutable"])
        self.assertFalse(contract["replacement"]["manual_prose_edit_required"])
        self.assertEqual(contract["implementation_constraints"]["claim_specific_branches"], [])
        self.assertEqual(contract["implementation_constraints"]["term_specific_branches"], [])

    def test_implementation_has_no_target_specific_branch(self):
        source = (ROOT / "scripts/74_technical_term_original_language_fallback_v1.py").read_text(encoding="utf-8")
        self.assertNotIn("SEC-02-2-P0-008", source)
        self.assertNotIn("Swelling Rock", source)

    def test_every_registry_record_validates(self):
        module = implementation()
        for record in load("contracts/technical_term_registry_v1.json")["entries"]:
            with self.subTest(term_id=record["term_id"]):
                self.assertEqual(module.validate_record(record, record), [])


class TestPositiveFixtures(unittest.TestCase):
    def test_authoritative_translations_remain_unchanged(self):
        module = implementation()
        index = module.registry_index()
        self.assertEqual(module.render_term(index["TERM-P0008-ROCK-CRUSHED"]), "ezilmiş kaya")
        self.assertEqual(module.render_term(index["TERM-P0008-ROCK-SQUEEZING"]), "sıkışan kaya")
        frozen = json.loads((ROOT / "data/book/drafting/sec_02_2/architecture_v2_2/contracts/claim_realization_contract_v2_2.json").read_text(encoding="utf-8"))
        case_entry = next(entry for entry in frozen["entries"] if entry["entry_id"] == "V22-P0008-CASE-001")
        terms = {item["case_id"]: item["turkish_term"] for item in case_entry["case_terms"]}
        self.assertEqual(terms["ROCK-CRUSHED"], "ezilmiş kaya")
        self.assertEqual(terms["ROCK-SQUEEZING"], "sıkışan kaya")

    def test_unresolved_semantic_and_visible_values_are_separate(self):
        module = implementation()
        record = module.registry_index()["TERM-P0008-ROCK-SWELLING"]
        self.assertEqual(module.semantic_value(record), "Swelling Rock")
        self.assertEqual(module.render_term(record), "**Swelling Rock**")
        self.assertNotIn("**", module.semantic_value(record))

    def test_exact_registered_span_passes_language_wrapper(self):
        module = implementation()
        fixture = next(item for item in load("fixtures/positive_fixtures_v1.json")["fixtures"]
                       if item["class"] == "bounded_language_exemption")
        self.assertEqual(module.validate_visible_language(
            fixture["text"], fixture["claim_ids"], fixture["source_keys"]), [])

    def test_provenance_and_ownership_are_exact(self):
        record = implementation().registry_index()["TERM-P0008-ROCK-SWELLING"]
        self.assertEqual(record["claim_ids"], ["SEC-02-2-P0-008"])
        self.assertEqual(record["source_keys"], ["SRC-DOC000047-d5c60204e247"])
        self.assertEqual(record["evidence_chunk_ids"], ["DOC000047-C0206"])

    def test_central_latest_resolution_does_not_mutate_history(self):
        module = implementation()
        original = module.registry_index()["TERM-P0008-ROCK-CRUSHED"]
        future = deepcopy(original)
        future["resolution_version"] = 2
        selected = module.latest_resolution([original, future], original["term_id"])
        self.assertEqual(selected["resolution_version"], 2)
        self.assertEqual(original["resolution_version"], 1)


class TestNegativeFixtures(unittest.TestCase):
    def test_all_fourteen_adversarial_classes_reject_exactly(self):
        module = implementation()
        fixtures = load("fixtures/negative_fixtures_v1.json")["fixtures"]
        self.assertEqual(len(fixtures), 14)
        for fixture in fixtures:
            with self.subTest(fixture=fixture["fixture_id"]):
                self.assertEqual(module.evaluate_negative_fixture(fixture), fixture["expected_code"])

    def test_arbitrary_english_and_unregistered_term_do_not_gain_exemption(self):
        module = implementation()
        fixtures = {item["class"]: item for item in load("fixtures/negative_fixtures_v1.json")["fixtures"]}
        for key in ("arbitrary_english_prose", "unregistered_english_technical_term"):
            self.assertNotEqual(module.evaluate_negative_fixture(fixtures[key]), "ACCEPT")


class TestDeterminismAndOutcome(unittest.TestCase):
    def test_rendering_is_byte_identical_in_and_out_of_process(self):
        module = implementation()
        local = [module.canonical_bytes(module.evaluate()) for _ in range(3)]
        self.assertEqual(len(set(local)), 1)
        command = [sys.executable, str(ROOT / "scripts/74_technical_term_original_language_fallback_v1.py")]
        fresh = [subprocess.run(command, cwd=ROOT, check=True, capture_output=True).stdout for _ in range(3)]
        self.assertEqual(len(set(fresh)), 1)
        self.assertEqual(fresh[0], local[0])

    def test_no_draft_or_pilot_was_rendered(self):
        self.assertEqual(list(BASE.rglob("*.md")), [])
        pilot = ROOT / "data/book/drafting/sec_02_2/architecture_v2/pilot_2/rendered/sec_02_2_pilot_2_draft.md"
        self.assertEqual(sha256(pilot), "4994c5db7d0fc6615ae54150165371bcda4efe7526d3a3904b6c4e07547ecd07")

    def test_manifest_is_closed_go_with_zero_prohibited_counts(self):
        manifest = json.loads((ROOT / "data/book/manifests/technical_term_original_language_fallback_contract_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "CLOSED_GO")
        for field, value in manifest["accounting"].items():
            self.assertEqual(value, 0, field)
        for artifact in manifest["artifacts"].values():
            self.assertEqual(sha256(ROOT / artifact["path"]), artifact["sha256"])


if __name__ == "__main__":
    unittest.main()
