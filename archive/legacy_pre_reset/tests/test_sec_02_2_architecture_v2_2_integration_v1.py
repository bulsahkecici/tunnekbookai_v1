from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/architecture_v2_2"


def load(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_integration():
    script = ROOT / "scripts/72_architecture_v2_2_integration.py"
    spec = importlib.util.spec_from_file_location("architecture_v2_2_integration", script)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestFrozenGate(unittest.TestCase):
    def test_acceptance_contract_is_frozen_at_recorded_sha(self):
        freeze = load("audits/acceptance_freeze_v1.json")
        self.assertTrue(freeze["authored_before_implementation"])
        self.assertFalse(freeze["amendable_after_results"])
        self.assertEqual(sha256(ROOT / freeze["acceptance_contract_path"]),
                         freeze["acceptance_contract_sha256"])
        acceptance = load("contracts/architecture_v2_2_integration_acceptance_contract_v1.json")
        self.assertEqual(len(acceptance["conditions"]), 24)

    def test_all_frozen_inputs_remain_byte_exact(self):
        preflight = load("audits/frozen_preflight_v1.json")
        self.assertEqual(preflight["status"], "PASS")
        self.assertEqual(preflight["drift_count"], 0)
        for relative, expected in preflight["artifacts"].items():
            with self.subTest(path=relative):
                self.assertEqual(sha256(ROOT / relative), expected)


class TestV22Contracts(unittest.TestCase):
    def test_plan_contract_adds_only_declared_structural_roles(self):
        plan = load("contracts/semantic_plan_ir_contract_v2_2.json")
        self.assertEqual(plan["new_node_types"],
                         ["SECTION_HEADING", "SUBSECTION_HEADING", "SCOPE_NODE"])
        self.assertEqual(plan["new_roles"],
                         ["CASE_SCOPE", "CONDITIONAL_MAXIMUM",
                          "ACCEPTANCE_CRITERIA_SCOPE"])
        self.assertEqual(plan["planner_output_prose_fields"], 0)
        self.assertEqual(plan["model_style_fields"], 0)

    def test_scope_and_factual_realizations_are_preserved(self):
        realization = load("contracts/claim_realization_contract_v2_2.json")
        entries = {entry["entry_id"]: entry for entry in realization["entries"]}
        self.assertEqual(entries["V22-SCOPE-WET-001"]["governed_claim_ids"],
                         ["SEC-02-2-C-004", "SEC-02-2-C-005"])
        self.assertEqual(entries["V22-SCOPE-REPAIR-001"]["governed_claim_ids"],
                         ["SEC-02-2-C-012"])
        self.assertEqual(entries["V22-C018-MAX-001"]["numeric_fact"],
                         {"value": "500", "unit": "kg/m³", "role": "maximum"})
        self.assertTrue(entries["V22-C018-MAX-001"]["linked_consequence"])
        self.assertEqual(entries["V22-C002-CRITERION-001"]["semantic_subject"],
                         "criterion_fact_ids")
        self.assertEqual(realization["totals"]["gloss_entries_added"], 0)
        self.assertEqual(realization["totals"]["lexicon_entries_added"], 0)

    def test_p0008_is_preserved_but_fails_closed_on_unresolved_term(self):
        realization = load("contracts/claim_realization_contract_v2_2.json")
        entry = next(item for item in realization["entries"]
                     if item["entry_id"] == "V22-P0008-CASE-001")
        self.assertEqual({item["case_id"] for item in entry["case_terms"]},
                         {"ROCK-CRUSHED", "ROCK-SQUEEZING", "ROCK-SWELLING"})
        unresolved = [item for item in entry["case_terms"]
                      if item["status"] == "UNRESOLVED"]
        self.assertEqual([item["case_id"] for item in unresolved], ["ROCK-SWELLING"])
        self.assertIsNone(unresolved[0]["turkish_term"])
        self.assertEqual(entry["status"], "UNREALIZABLE")

    def test_book_style_is_frozen_and_deterministic(self):
        style = load("contracts/deterministic_book_style_integration_v2_2.json")
        parent = json.loads((ROOT / "data/book/drafting/contracts/book_style_contract_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(style["subsection_headings"], parent["sec_02_2_heading_map"])
        self.assertEqual(style["subsection_order"], ["A", "B", "C", "D"])
        self.assertTrue(style["placement_rules"]["scope_before_governed_claim"])
        self.assertEqual(style["model_style_pass"], "FORBIDDEN")
        self.assertTrue(style["deterministic"])
        self.assertEqual(style["redundancy_suppression"][0]["claim_id"],
                         "SEC-02-2-P0-006")

    def test_citation_allocation_is_correct(self):
        citations = json.loads((ROOT / "data/book/drafting/sec_02_2/technical_remediation_v1/contracts/citation_allocation_contract_v2.json").read_text(encoding="utf-8"))
        for allocation in citations["allocations"]:
            self.assertEqual(allocation["selected_source_keys"],
                             ["SRC-DOC000236-0229b854f373"])
            self.assertNotIn("SRC-DOC000087-e7393bf8138a",
                             allocation["selected_source_keys"])
        self.assertEqual(citations["result"]["misleading_allocations_remaining"], 0)

    def test_renderer_contract_has_no_free_form_or_model_branch(self):
        renderer = load("contracts/deterministic_renderer_contract_v2_2.json")
        self.assertFalse(renderer["free_form_text_branch"])
        self.assertFalse(renderer["model_call_branch"])
        self.assertFalse(renderer["post_render_style_branch"])
        self.assertTrue(renderer["frozen_renderer_modified"] is False)


class TestCanonicalUniverseRefusal(unittest.TestCase):
    def test_universe_refuses_required_unrealizable_case_scope(self):
        universe = load("contracts/planner_option_universe_v2_2.json")
        self.assertTrue(universe["canonical"])
        self.assertFalse(universe["second_universe_exists"])
        self.assertEqual(universe["build_status"], "REFUSED")
        self.assertEqual(universe["refusal_code"], "V22_REQUIRED_ROLE_UNREALIZABLE")
        self.assertEqual(universe["violations"][0]["required_not_available"], ["CASE_SCOPE"])
        self.assertFalse(universe["planner_payload_authorised"])

    def test_integration_evaluator_returns_exact_refusal(self):
        module = load_integration()
        result = module.evaluate()
        self.assertEqual(result["status"], "NO_GO")
        self.assertEqual(result["failures"][0]["code"],
                         "V22_REQUIRED_ROLE_UNREALIZABLE")
        self.assertEqual(result["failures"][0]["entry_status"], "UNREALIZABLE")
        self.assertFalse(result["planner_payload_authorised"])
        self.assertFalse(result["section_draft_render_authorised"])

    def test_refusal_is_byte_deterministic_in_and_out_of_process(self):
        module = load_integration()
        in_process = [module.canonical_bytes(module.evaluate()) for _ in range(3)]
        self.assertEqual(len(set(in_process)), 1)
        command = [sys.executable, str(ROOT / "scripts/72_architecture_v2_2_integration.py")]
        fresh = [subprocess.run(command, cwd=ROOT, check=True, capture_output=True).stdout
                 for _ in range(3)]
        self.assertEqual(len(set(fresh)), 1)
        self.assertEqual(fresh[0], in_process[0])
        self.assertEqual(hashlib.sha256(fresh[0]).hexdigest(),
                         "1ab1a08a33658875a1e1fb4684690eafa3b45c4d8bbdc0f1e6d6a2267b70b614")


class TestProofsAndFixtures(unittest.TestCase):
    def test_negative_fixtures_cover_required_classes(self):
        fixtures = load("fixtures/negative_fixtures_v1.json")
        plan = load("contracts/semantic_plan_ir_contract_v2_2.json")
        declared = set(plan["failure_codes"])
        self.assertEqual(fixtures["summary"], {"fixtures": 9, "rejected": 9,
                                                "false_accepts": 0,
                                                "false_rejects": 0})
        for fixture in fixtures["fixtures"]:
            with self.subTest(fixture=fixture["fixture_id"]):
                self.assertEqual(fixture["result"], "REJECT")
                self.assertIn(fixture["expected_code"], declared)

    def test_static_proof_and_validator_fail_closed_before_surface(self):
        proof = load("audits/static_containment_proof_v2_2.json")
        self.assertEqual(proof["status"], "NOT_RUN_FAIL_CLOSED")
        self.assertEqual(proof["admitted_surface_units"], 0)
        self.assertEqual(proof["draft_validator_v1_2_histogram"], {})
        self.assertEqual(proof["unrealizable_leaks"], 0)
        self.assertFalse(proof["gate_satisfied"])

    def test_feasibility_and_style_fail_only_on_term_gap(self):
        proof = load("audits/feasibility_proof_v2_2.json")
        self.assertEqual(proof["status"], "FAIL")
        self.assertEqual(proof["technical_blockers"]["semantic_contract_closed"], "6/6")
        self.assertEqual(proof["technical_blockers"]["surface_integration_ready"], "5/6")
        self.assertEqual(proof["book_style_projection"]["terminology_consistency"],
                         "FAIL_UNRESOLVED_TERM")
        self.assertFalse(proof["complete_plan_exists"])
        self.assertFalse(proof["draft_artifact_emitted"])

    def test_no_section_draft_artifact_was_created(self):
        self.assertEqual(list(BASE.rglob("*.md")), [])
        pilot = (ROOT / "data/book/drafting/sec_02_2/architecture_v2/pilot_2/rendered/"
                 "sec_02_2_pilot_2_draft.md")
        self.assertEqual(sha256(pilot),
                         "4994c5db7d0fc6615ae54150165371bcda4efe7526d3a3904b6c4e07547ecd07")


class TestOutcomeManifest(unittest.TestCase):
    def test_frozen_acceptance_results_require_no_go(self):
        results = load("audits/acceptance_results_v1.json")
        self.assertEqual(results["verdict"], "CLOSED_NO_GO")
        self.assertEqual(results["summary"]["passed"], 18)
        self.assertEqual(results["summary"]["failed"], 6)
        self.assertEqual(set(results["summary"]["unmet"]),
                         {"AC-V22-03", "AC-V22-07", "AC-V22-17", "AC-V22-18",
                          "AC-V22-19", "AC-V22-21"})

    def test_manifest_hashes_status_and_accounting(self):
        manifest_path = ROOT / "data/book/manifests/sec_02_2_architecture_v2_2_technical_style_integration_v1.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "CLOSED_NO_GO")
        for artifact in manifest["artifacts"].values():
            with self.subTest(path=artifact["path"]):
                self.assertEqual(sha256(ROOT / artifact["path"]), artifact["sha256"])
        for field, value in manifest["accounting"].items():
            if field == "targeted_evidence_artifact_reads":
                self.assertEqual(value, 5)
            else:
                self.assertEqual(value, 0, field)
        self.assertEqual(manifest["frozen_integrity"]["drift_count"], 0)


if __name__ == "__main__":
    unittest.main()
