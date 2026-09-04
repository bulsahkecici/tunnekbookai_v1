from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/technical_remediation_v1"


def load(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rejected(rule_id: str, payload: dict) -> bool:
    if rule_id == "TV-SCOPE-001":
        return not set(payload["mandatory_binding_ids"]) <= set(
            payload["paragraph_scope_binding_ids"])
    if rule_id == "TV-CASE-001":
        return (not set(payload["required_case_ids"]) <= set(payload["planned_case_ids"])
                or payload["required_dependency"] not in payload["planned_dependencies"])
    if rule_id == "TV-CITE-001":
        return not set(payload["selected_source_keys"]) <= set(payload["permitted_source_keys"])
    if rule_id == "TV-BOUND-001":
        return payload["boundary_required"] and not payload["boundary_allocated"]
    if rule_id == "TV-CRITERION-001":
        return (payload["semantic_subject"] != payload["required_subject"]
                or payload["semantic_subject"] in payload["forbidden_subjects"])
    if rule_id == "TV-CONSEQUENCE-001":
        return (payload["linked_consequence_required"]
                and not payload["linked_consequence_present"])
    if rule_id == "TV-SURFACE-001":
        return payload["rendered_units"] != 0 or payload["draft_artifacts"] != 0
    raise AssertionError(f"unknown rule {rule_id}")


class TestAcceptanceAndFrozenPreflight(unittest.TestCase):
    def test_acceptance_was_frozen_before_outputs(self):
        acceptance = load("contracts/technical_remediation_acceptance_contract_v1.json")
        freeze = load("audits/acceptance_freeze_v1.json")
        self.assertTrue(acceptance["authored_before_results"])
        self.assertEqual(len(acceptance["conditions"]), 20)
        self.assertEqual(sha256(ROOT / freeze["acceptance_contract_path"]),
                         freeze["acceptance_contract_sha256"])
        self.assertFalse(freeze["amendable_after_results"])

    def test_frozen_preflight_and_postflight_are_byte_exact(self):
        preflight = load("audits/frozen_preflight_v1.json")
        self.assertEqual(preflight["status"], "PASS")
        self.assertEqual(preflight["drift_count"], 0)
        for relative, expected in preflight["artifacts"].items():
            with self.subTest(path=relative):
                self.assertEqual(sha256(ROOT / relative), expected)


class TestScopeAndClaimRemediation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load("contracts/technical_claim_scope_remediation_contract_v1.json")

    def test_scope_bindings_close_wet_and_repair_contexts(self):
        bindings = {item["claim_id"]: item for item in self.contract["scope_bindings"]}
        self.assertEqual(bindings["SEC-02-2-C-004"]["new_system_scope"], "wet_system")
        self.assertEqual(bindings["SEC-02-2-C-005"]["new_system_scope"], "wet_system")
        self.assertEqual(bindings["SEC-02-2-C-012"]["new_system_scope"], "repair_work")
        self.assertTrue(all(item["mandatory"] for item in bindings.values()))
        self.assertEqual({item["chunk_id"] for item in bindings.values()},
                         {"DOC000087-C0279", "DOC000087-C0281"})

    def test_named_rock_cases_and_dependency_are_complete(self):
        extension = self.contract["condition_extensions"][0]
        self.assertEqual(extension["claim_id"], "SEC-02-2-P0-008")
        self.assertEqual({case["case_id"] for case in extension["named_source_cases"]},
                         {"ROCK-CRUSHED", "ROCK-SQUEEZING", "ROCK-SWELLING"})
        self.assertEqual(extension["shared_criterion"]["dependency"],
                         "dependent on tunnel size")
        self.assertEqual(extension["generic_gloss_entries_added"], 0)

    def test_500_boundary_and_consequence_are_source_backed(self):
        claim = self.contract["new_claims"][0]
        self.assertEqual(claim["claim_id"], "SEC-02-2-C-018")
        self.assertEqual(claim["numeric"], [{"value": "500", "unit": "kg/m³",
                                             "role": "maximum", "source_stated": True}])
        self.assertEqual(claim["chunk_id"], "DOC000236-C0267")
        self.assertTrue(claim["linked_consequence"])
        self.assertEqual(self.contract["totals"]["frozen_claims_modified"], 0)

    def test_no_gloss_or_lexicon_widening(self):
        totals = self.contract["totals"]
        self.assertEqual(totals["gloss_entries_added"], 0)
        self.assertEqual(totals["lexicon_entries_added"], 0)


class TestRealizationAndAllocation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.realization = load("contracts/technical_realization_contract_v1.json")
        cls.citations = load("contracts/citation_allocation_contract_v2.json")

    def test_scope_guards_fail_closed(self):
        entries = {entry["claim_id"]: entry for entry in self.realization["entries"]
                   if entry["role"] == "SCOPE_BINDING"}
        self.assertEqual(set(entries), {"SEC-02-2-C-004", "SEC-02-2-C-005",
                                        "SEC-02-2-C-012"})
        self.assertTrue(all(not entry["surface_eligible_without_binding"]
                            for entry in entries.values()))

    def test_c002_criterion_subject_is_numeric_facts(self):
        entry = next(item for item in self.realization["entries"]
                     if item["claim_id"] == "SEC-02-2-C-002")
        self.assertEqual(entry["semantic_subject"], "criterion_fact_ids")
        self.assertEqual(len(entry["criterion_fact_ids"]), 2)
        self.assertIn("strength_class", entry["forbidden_semantic_subjects"])
        self.assertFalse(entry["surface_eligible_when_subject_is_class"])

    def test_citation_allocation_removes_tokluk_key(self):
        wrong = "SRC-DOC000087-e7393bf8138a"
        right = "SRC-DOC000236-0229b854f373"
        registry = {row["source_key"]: row for row in
                    (json.loads(line) for line in
                     (ROOT / "data/book/source_registry_v1.jsonl").read_text(
                         encoding="utf-8").splitlines())}
        self.assertEqual(registry[wrong]["section_path"],
                         "Tokluk İndeksi - Enerji Depolama Kapasitesi:")
        self.assertEqual(registry[right]["section_path"], "351.04.01 Çimento")
        for allocation in self.citations["allocations"]:
            self.assertNotIn(wrong, allocation["selected_source_keys"])
            self.assertEqual(allocation["selected_source_keys"], [right])
        self.assertEqual(self.citations["result"]["misleading_allocations_remaining"], 0)
        self.assertFalse(self.citations["source_registry_modified"])

    def test_no_surface_was_authorised_or_emitted(self):
        self.assertEqual(self.realization["totals"]["rendered_units"], 0)
        self.assertEqual(list(BASE.rglob("*.md")), [])


class TestProofsAndNegativeFixtures(unittest.TestCase):
    def test_all_negative_fixtures_reject_under_general_rules(self):
        fixtures = load("fixtures/negative_fixtures_v1.json")
        validation = load("contracts/technical_remediation_validation_contract_v1.json")
        codes = {rule["rule_id"]: rule["failure_code"] for rule in validation["rules"]}
        for fixture in fixtures["fixtures"]:
            with self.subTest(fixture=fixture["fixture_id"]):
                self.assertTrue(rejected(fixture["rule_id"], fixture["input"]))
                self.assertEqual(codes[fixture["rule_id"]],
                                 fixture["expected_failure_code"])
                self.assertEqual(fixture["result"], "REJECT")
        self.assertEqual(fixtures["summary"], {"fixtures": 9, "rejected": 9,
                                                "false_accepts": 0,
                                                "false_rejects": 0})

    def test_static_proof_has_zero_tolerance_results(self):
        proof = load("audits/static_containment_proof_v1.json")
        self.assertEqual(proof["status"], "PASS")
        self.assertEqual(proof["additive_delta"]["new_surface_forms"], 0)
        self.assertEqual(proof["result"], {"false_accepts": 0, "false_rejects": 0,
                                            "unrealizable_leaks": 0,
                                            "validator_failure_projection": {}})

    def test_feasibility_and_style_projection_pass(self):
        proof = load("audits/feasibility_proof_v1.json")
        self.assertEqual(proof["status"], "PASS")
        self.assertFalse(proof["surface_rendered"])
        self.assertEqual(proof["result"]["required_topics"], "3/3")
        self.assertEqual(proof["result"]["blockers_structurally_closed"], "6/6")
        self.assertTrue(proof["result"]["style_structurally_satisfiable"])

    def test_all_six_blockers_are_closed_with_root_causes(self):
        audit = load("audits/blocker_closure_audit_v1.json")
        self.assertEqual(audit["summary"], {"blocking_findings": 6, "closed": 6,
                                             "open": 0, "new_blocking_findings": 0})
        expected = {"claim_selection", "scope_binding", "realization_contract",
                    "citation_allocation"}
        self.assertTrue(expected <= {item["primary_root_cause"]
                                     for item in audit["blockers"]})
        self.assertTrue(all(item["disposition"] == "CLOSED"
                            for item in audit["blockers"]))


class TestOutcomeManifest(unittest.TestCase):
    def test_acceptance_results_close_all_frozen_conditions(self):
        results = load("audits/acceptance_results_v1.json")
        self.assertEqual(results["verdict"], "CLOSED_GO")
        self.assertEqual(results["summary"], {"conditions": 20, "passed": 20,
                                               "failed": 0, "unmet": []})
        self.assertTrue(all(item["status"] == "PASS" for item in results["conditions"]))

    def test_manifest_hashes_and_accounting(self):
        manifest = json.loads((ROOT / "data/book/manifests/sec_02_2_technical_claim_scope_citation_remediation_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "CLOSED_GO")
        for artifact in manifest["artifacts"].values():
            with self.subTest(path=artifact["path"]):
                self.assertEqual(sha256(ROOT / artifact["path"]), artifact["sha256"])
        for field, value in manifest["accounting"].items():
            self.assertEqual(value, 0, field)
        self.assertEqual(manifest["frozen_integrity"]["drift_count"], 0)


if __name__ == "__main__":
    unittest.main()
