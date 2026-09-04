"""SEC-02-2 Draft Plan v1.2 + Attempt #3 - what the plan may and may not be.

The plan cases are tripwires against the way a draft plan could quietly become a remediation of
the validator: the allocation rule has to select its claims from frozen data rather than name
them, the exposed vocabulary has to be byte-identical to the frozen glosses, and `kayaç` and
`spesifik` have to still be absent from everything this phase wrote.

The attempt cases assert the process rather than the verdict. Attempt #3 may be accepted or
rejected - that is what a pilot is - but either way exactly one generation was taken, the raw
output was preserved, nothing was repaired or regenerated, and no attempt #4 exists anywhere.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BOOK = ROOT / "data" / "book"
DRAFTING = BOOK / "drafting"
SECTION_DIR = DRAFTING / "sec_02_2"
ATTEMPT_DIR = SECTION_DIR / "attempt_3"

PLAN_V1_1 = SECTION_DIR / "draft_plan_v1_1.json"
PLAN_V1_2 = SECTION_DIR / "draft_plan_v1_2.json"
DRAFTING_CONTRACT = DRAFTING / "contracts" / "section_drafting_contract_v1.json"
PRE_GATE = ATTEMPT_DIR / "audits" / "pre_generation_gate_v1.json"
ATTEMPT_AUDIT = ATTEMPT_DIR / "audits" / "attempt_3_audit_v1.json"
RAW = ATTEMPT_DIR / "raw" / "sec_02_2_draft_raw_attempt_3.json"
REJECTED = ATTEMPT_DIR / "rejected" / "pilot_attempt_3_validation.json"
ACCEPTED = ATTEMPT_DIR / "accepted" / "sec_02_2_draft_ir_v1_2.json"
MANIFEST = BOOK / "manifests" / "sec_02_2_draft_plan_v1_2_attempt_3.json"
REPORT = ROOT / "reports" / "sec_02_2_draft_plan_v1_2_attempt_3.md"
REMEDIATION_MANIFEST = BOOK / "manifests" / "sec_02_2_draft_failure_remediation_v1.json"


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


V12 = _load("plan_test_validator_v1_2", "scripts/54_section_draft_validator_v1_2.py")
PHASE = _load("plan_test_phase", "scripts/56_sec_02_2_draft_plan_v1_2_attempt_3.py")

BUNDLE = V12.load_bundle()
ENTRIES = V12.load_qualifier_semantics()
PLAN = json.loads(PLAN_V1_2.read_text(encoding="utf-8"))
PARENT = json.loads(PLAN_V1_1.read_text(encoding="utf-8"))
CONTRACT = json.loads(DRAFTING_CONTRACT.read_text(encoding="utf-8"))


class PlanV1_2IsAdditive(unittest.TestCase):
    """Plan v1.1 is frozen; v1.2 adds and changes nothing else."""

    def test_plan_v1_1_is_byte_identical_to_its_recorded_sha(self):
        recorded = json.loads(REMEDIATION_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(recorded["draft_plan_v1_1_sha"],
                         hashlib.sha256(PLAN_V1_1.read_bytes()).hexdigest())

    def test_plan_v1_2_is_a_separate_artifact(self):
        self.assertEqual("tunnelbook-sec-02-2-draft-plan-v1.2", PLAN["version"])
        self.assertEqual(PARENT["version"], PLAN["parent_version"])
        self.assertNotEqual(PLAN_V1_1, PLAN_V1_2)

    def test_allocation_subsections_and_exclusions_are_unchanged(self):
        self.assertEqual(PARENT["subsections"], PLAN["subsections"])
        self.assertEqual(PARENT["claim_allocation"], PLAN["claim_allocation"])
        self.assertEqual(PARENT["excluded_claims"], PLAN["excluded_claims"])
        self.assertEqual(PARENT["required_topics"], PLAN["required_topics"])
        self.assertEqual(PARENT["semantic_constraints"], PLAN["semantic_constraints"])
        self.assertEqual(PARENT["language_policy"], PLAN["language_policy"])

    def test_change_scope_widens_and_weakens_nothing(self):
        self.assertEqual([], PLAN["change_scope"]["widened"])
        self.assertEqual([], PLAN["change_scope"]["weakened"])
        self.assertEqual(["unit_allocation",
                          "claim_translation_requirements.licensed_vocabulary",
                          "qualifier_semantics"], PLAN["change_scope"]["added"])

    def test_plan_validates_against_v1_2(self):
        self.assertEqual("tunnelbook-draft-validation-contract-v1.2",
                         PLAN["validation_contract_version"])
        self.assertEqual("tunnelbook-section-draft-validator-v1.2", PLAN["validator_version"])


class AllocationRuleIsGeneral(unittest.TestCase):
    """The rule reads frozen data. It must not be a list of claim names in disguise."""

    def setUp(self):
        self.allocation = PLAN["unit_allocation"]

    def test_rule_selects_c002_and_c009(self):
        self.assertEqual(["SEC-02-2-C-002", "SEC-02-2-C-009"],
                         sorted(self.allocation["selected_claim_ids"]))

    def test_selection_is_reproducible_from_the_frozen_allowlist(self):
        """Recompute the rule from scratch; it must select the same claims."""
        entry_by_claim = {e["claim_id"]: e for e in ENTRIES}
        selected = []
        for row in self.allocation["by_claim"]:
            claim = BUNDLE.allowlist[row["claim_id"]]
            reach = PHASE.qualifier_reachability(
                claim, entry_by_claim.get(row["claim_id"]), BUNDLE)
            if reach["needs_composed_slot"]:
                selected.append(row["claim_id"])
        self.assertEqual(sorted(self.allocation["selected_claim_ids"]), sorted(selected))

    def test_every_claim_without_a_qualifier_keeps_one_slot(self):
        for row in self.allocation["by_claim"]:
            claim = BUNDLE.allowlist[row["claim_id"]]
            if not (claim.get("qualifiers") or []):
                with self.subTest(claim=row["claim_id"]):
                    self.assertEqual(1, row["unit_slots"])

    def test_selected_claims_get_two_bound_slots(self):
        for row in self.allocation["by_claim"]:
            if row["claim_id"] not in self.allocation["selected_claim_ids"]:
                continue
            with self.subTest(claim=row["claim_id"]):
                self.assertEqual(2, row["unit_slots"])
                self.assertEqual({row["claim_id"]},
                                 {slot["claim_id"] for slot in row["slots"]})
                self.assertEqual(1, len({tuple(slot["source_keys"]) for slot in row["slots"]}))
                self.assertEqual({"INDEPENDENT"},
                                 {slot["relationship_type"] for slot in row["slots"]})

    def test_c002_stays_one_claim_with_two_slots(self):
        row = next(r for r in self.allocation["by_claim"] if r["claim_id"] == "SEC-02-2-C-002")
        roles = [slot["slot_role"] for slot in row["slots"]]
        self.assertEqual(["QUALIFIER_SCOPE", "CLAIM_STATEMENT"], roles)
        identity = row["slots"][0]
        self.assertEqual(list(BUNDLE.allowlist["SEC-02-2-C-002"]["conditions"]),
                         identity["must_also_carry_conditions"])
        self.assertIn("Tablo-351-5", identity["must_not_imply"])
        self.assertFalse(identity["has_canonical_sentence_to_copy"])
        # One claim, still. The allowlist is not touched by allocating two slots.
        self.assertEqual(1, len([c for c in BUNDLE.allowlist if c == "SEC-02-2-C-002"]))

    def test_c009_scope_slot_follows_its_claim_statement(self):
        row = next(r for r in self.allocation["by_claim"] if r["claim_id"] == "SEC-02-2-C-009")
        self.assertEqual(["CLAIM_STATEMENT", "QUALIFIER_SCOPE"],
                         [slot["slot_role"] for slot in row["slots"]])
        self.assertEqual("DQS-C009-001", row["slots"][1]["constraint_id"])

    def test_composed_slot_has_no_sentence_to_copy(self):
        for row in self.allocation["by_claim"]:
            for slot in row["slots"]:
                if slot["slot_role"] == "QUALIFIER_SCOPE":
                    with self.subTest(slot=slot["slot_id"]):
                        self.assertFalse(slot["has_canonical_sentence_to_copy"])
                        self.assertEqual("compose", slot["compose_or_reproduce"])


class LicensedVocabularyIsExposureNotWidening(unittest.TestCase):

    def setUp(self):
        self.glosses = CONTRACT["translation_glosses"]

    def test_vocabulary_is_byte_identical_to_the_frozen_glosses(self):
        for requirement in PLAN["claim_translation_requirements"]:
            with self.subTest(claim=requirement["claim_id"]):
                self.assertEqual(self.glosses[requirement["claim_id"]],
                                 requirement["licensed_vocabulary"])

    def test_no_forbidden_word_is_exposed_as_licensed_vocabulary(self):
        """The words attempt #2 failed on must not have been quietly added to the pool.

        Scoped to the vocabulary itself rather than to the whole file: the plan also names both
        words in `forbidden_additions_absent`, where naming them is the guard, not a breach.
        """
        exposed = {word for requirement in PLAN["claim_translation_requirements"]
                   for word in requirement["licensed_vocabulary"]}
        for word in ("kayaç", "spesifik"):
            with self.subTest(word=word):
                self.assertNotIn(word, exposed)
                self.assertTrue(PLAN["licensed_vocabulary_policy"]
                                ["forbidden_additions_absent"][word])

    def test_no_forbidden_word_reached_the_generation_payload(self):
        payload = PHASE.build_generation_payload_v1_2(PLAN, BUNDLE.allowlist)
        vocabulary = [word
                      for subsection in payload["subsections"]
                      for claim in subsection["claims"]
                      for word in claim.get("licensed_vocabulary", [])]
        for word in ("kayaç", "spesifik"):
            with self.subTest(word=word):
                self.assertNotIn(word, vocabulary)

    def test_exposure_did_not_change_what_the_validator_licenses(self):
        """RC-B3's assertion, restated against this phase's artifact."""
        pool = V12.base.licensed_tokens(["SEC-02-2-P0-008"], BUNDLE)

        def licensed(word: str) -> bool:
            return any(V12.prefix_agreement(V12.fold(word), token) for token in pool)

        self.assertFalse(licensed("kayaç"))
        self.assertFalse(licensed("spesifik"))
        self.assertTrue(licensed("kaya"))

    def test_glosses_on_disk_are_unchanged(self):
        recorded = json.loads(
            (BOOK / "manifests" / "sec_02_2_qualifier_validation_tightening_v1.json")
            .read_text(encoding="utf-8"))["frozen_inputs_sha256"]
        self.assertEqual(recorded["section_drafting_contract_v1"],
                         hashlib.sha256(DRAFTING_CONTRACT.read_bytes()).hexdigest())


class PreGenerationGate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.gate = json.loads(PRE_GATE.read_text(encoding="utf-8"))

    def test_gate_passed_before_any_generation(self):
        self.assertTrue(self.gate["gate"]["go"])
        self.assertEqual([], self.gate["gate"]["failed"])
        self.assertTrue(self.gate["attempt_3_authorised"])

    def test_every_suite_ran_and_passed(self):
        self.assertEqual("passed", self.gate["tests"]["status"])
        self.assertEqual([], self.gate["tests"]["missing_suites"])
        self.assertGreater(self.gate["tests"]["tests_run"], 300)

    def test_no_false_accepts_or_rejects(self):
        self.assertEqual([], self.gate["fixtures"]["false_accepts"])
        self.assertEqual([], self.gate["fixtures"]["false_rejects"])
        self.assertEqual([], self.gate["fixtures"]["code_mismatches"])
        self.assertEqual([], self.gate["fixtures"]["newly_failing_under_v1_2"])

    def test_frozen_artifacts_did_not_drift(self):
        self.assertEqual([], self.gate["frozen_integrity"]["drifted"])
        self.assertTrue(self.gate["frozen_integrity"]["all_unchanged"])

    def test_qualifier_registry_still_consistent(self):
        self.assertTrue(self.gate["registry_integrity"]["consistent"])


class AttemptThree(unittest.TestCase):
    """The process, not the verdict."""

    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.raw = json.loads(RAW.read_text(encoding="utf-8")) if RAW.exists() else None

    def test_exactly_one_generation_was_taken(self):
        self.assertEqual(1, self.manifest["generation_attempts_this_phase"])
        self.assertEqual(3, self.manifest["total_pilot_attempts"])
        self.assertEqual(0, self.manifest["automatic_retries"])
        self.assertFalse(self.manifest["attempt_4_authorised"])

    def test_frozen_writer_settings_were_used(self):
        self.assertEqual("qwen3.6-35b-a3b-mlx", self.raw["model_id"])
        self.assertEqual(0.0, self.raw["temperature"])
        self.assertEqual(11, self.raw["seed"])
        self.assertEqual(3, self.raw["attempt"])

    def test_raw_output_is_preserved_and_matches_its_sha(self):
        self.assertEqual(self.raw["raw_text_sha256"],
                         hashlib.sha256(self.raw["raw_text"].encode("utf-8")).hexdigest())

    def test_no_retrieval_no_qdrant_no_corpus(self):
        for field in ("retrieval_calls", "qdrant_writes", "corpus_reads"):
            self.assertEqual(0, self.manifest[field], field)
        self.assertEqual([], self.manifest["validators_weakened"])

    def test_verdict_artifact_matches_the_verdict(self):
        if self.manifest["attempt_3_status"] == "ACCEPT":
            self.assertTrue(ACCEPTED.exists())
            self.assertTrue(self.manifest["rendered"])
        else:
            self.assertTrue(REJECTED.exists())
            self.assertFalse(self.manifest["rendered"])
            rejection = json.loads(REJECTED.read_text(encoding="utf-8"))
            for field in ("repaired", "translated", "regenerated", "units_deleted", "rendered"):
                self.assertFalse(rejection[field], field)

    def test_validated_under_v1_2(self):
        self.assertEqual("tunnelbook-section-draft-validator-v1.2",
                         self.manifest["validator_version"])

    def test_report_exists(self):
        self.assertTrue(REPORT.exists())


if __name__ == "__main__":
    unittest.main()
