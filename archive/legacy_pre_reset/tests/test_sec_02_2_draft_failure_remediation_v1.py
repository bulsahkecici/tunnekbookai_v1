"""SEC-02-2 Draft Failure Remediation v1 - the phase's own artifacts.

This suite audits what the run wrote rather than what the modules can do. It asks whether the
freeze is a freeze, whether the root-cause file reaches a conclusion the evidence in it supports,
whether the additive contracts really are additive, and - once attempt #2 exists - whether the
outcome recorded matches the outcome the validator reached.

The attempt-#2 assertions are conditional on the artifacts existing. That is not laxity: the
suite is a gate precondition as well as a post-run audit, so it has to be runnable before the one
authorised generation is spent. What it will not do is pass silently on a run that generated and
then failed to record the result, which is why every conditional branch asserts something.
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
CONTRACTS = DRAFTING / "contracts"
SECTION_DIR = DRAFTING / "sec_02_2"
REMEDIATION = SECTION_DIR / "remediation_v1"

LANGUAGE_CONTRACT = CONTRACTS / "draft_language_contract_v1.json"
VALIDATION_V1 = CONTRACTS / "draft_validation_contract_v1.json"
VALIDATION_V1_1 = CONTRACTS / "draft_validation_contract_v1_1.json"
PLAN_V1 = SECTION_DIR / "draft_plan_v1.json"
PLAN_V1_1 = SECTION_DIR / "draft_plan_v1_1.json"
PROMPT_V1 = ROOT / "data" / "metadata" / "section_drafting_system_prompt_v1.txt"
PROMPT_V1_1 = ROOT / "data" / "metadata" / "section_drafting_system_prompt_v1_1.txt"
ROOT_CAUSE = REMEDIATION / "audits" / "pilot_failure_root_cause_v1.json"
FREEZE = REMEDIATION / "audits" / "historical_pilot_freeze_v1.json"
REMEDIATION_AUDIT = REMEDIATION / "audits" / "sec_02_2_remediation_audit_v1.json"
CONSTRAINTS = REMEDIATION / "contracts" / "draft_semantic_constraints_v1.json"
MAPPINGS = REMEDIATION / "contracts" / "cross_lingual_condition_mappings_v1.json"
RAW_ATTEMPT_2 = REMEDIATION / "raw" / "sec_02_2_draft_raw_attempt_2.json"
ACCEPTED_IR = REMEDIATION / "accepted" / "sec_02_2_draft_ir_v1_1.json"
REJECTED = REMEDIATION / "rejected" / "pilot_attempt_2_validation.json"
RENDERED = SECTION_DIR / "rendered" / "sec_02_2_pilot_v1_1.md"
FIXTURES = ROOT / "data" / "evaluation" / "sec_02_2_draft_failure_remediation_v1.jsonl"
MANIFEST = BOOK / "manifests" / "sec_02_2_draft_failure_remediation_v1.json"
PARENT_MANIFEST = BOOK / "manifests" / "section_drafting_contract_v1.json"
REPORT = ROOT / "reports" / "sec_02_2_draft_failure_remediation_v1.md"
HISTORICAL_RAW = SECTION_DIR / "raw" / "sec_02_2_draft_raw_v1.json"

FAILED_UNITS = ("U-A-P01-S03", "U-C-P01-S03")
ROOT_CAUSE_CLASSES = ("PROMPT_INSTRUCTION_GAP", "DRAFT_IR_SCHEMA_GAP",
                      "GENERATOR_COMPLIANCE_FAILURE", "VALIDATOR_COVERAGE_GAP",
                      "LANGUAGE_VALIDATION_GAP", "SERIALIZATION_GAP")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Artifacts(unittest.TestCase):
    def test_every_required_artifact_exists(self):
        for path in (LANGUAGE_CONTRACT, VALIDATION_V1_1, PLAN_V1_1, PROMPT_V1_1, ROOT_CAUSE,
                     FREEZE, CONSTRAINTS, MAPPINGS, FIXTURES,
                     ROOT / "scripts" / "50_sec_02_2_draft_failure_remediation_v1.py",
                     ROOT / "scripts" / "51_draft_language_validator_v1.py",
                     ROOT / "scripts" / "52_section_draft_validator_v1_1.py"):
            self.assertTrue(path.exists(), path)

    def test_the_output_directory_has_every_declared_subdirectory(self):
        for name in ("audits", "contracts", "fixtures", "raw", "accepted", "rejected"):
            self.assertTrue((REMEDIATION / name).is_dir(), name)


class VersionsAreAdditive(unittest.TestCase):
    def test_v1_contracts_are_not_mutated_in_place(self):
        """§30. v1.1 is a new file; v1 stays exactly as the drafting phase left it."""
        parent = load(PARENT_MANIFEST)
        self.assertEqual(sha(VALIDATION_V1), parent["draft_validation_contract_sha"])
        self.assertEqual(sha(PLAN_V1), parent["draft_plan_sha"])
        self.assertEqual(sha(PROMPT_V1), parent["drafting_prompt_sha"])

    def test_v1_1_declares_its_parent(self):
        contract = load(VALIDATION_V1_1)
        self.assertEqual(contract["version"], "tunnelbook-draft-validation-contract-v1.1")
        self.assertEqual(contract["parent_version"], "tunnelbook-draft-validation-contract-v1")

    def test_v1_1_removes_and_weakens_nothing(self):
        contract = load(VALIDATION_V1_1)
        self.assertEqual(contract["change_scope"]["removed"], [])
        self.assertEqual(contract["change_scope"]["weakened"], [])
        self.assertEqual(contract["change_scope"]["renamed_codes"], [])
        for code in load(VALIDATION_V1)["rejection_codes"]:
            self.assertIn(code, contract["rejection_codes"])

    def test_the_new_codes_are_exactly_the_three_declared(self):
        contract = load(VALIDATION_V1_1)
        self.assertEqual(sorted(contract["new_rejection_codes"]),
                         ["LANGUAGE_AMBIGUOUS", "LANGUAGE_MISMATCH", "SEMANTIC_SCOPE_MISMATCH"])

    def test_plan_v1_1_keeps_v1s_claim_allocation(self):
        """The remediation repairs how claims are drafted, not which claims are drafted."""
        self.assertEqual(load(PLAN_V1_1)["claim_allocation"], load(PLAN_V1)["claim_allocation"])
        self.assertEqual(load(PLAN_V1_1)["subsections"], load(PLAN_V1)["subsections"])

    def test_plan_v1_1_adds_every_field_the_phase_requires(self):
        plan = load(PLAN_V1_1)
        for field in ("semantic_constraints", "language_policy",
                      "claim_translation_requirements", "required_condition_fields",
                      "required_qualifier_fields"):
            self.assertIn(field, plan)
        self.assertTrue(plan["semantic_constraints"])
        self.assertTrue(plan["claim_translation_requirements"])

    def test_prompt_v1_1_is_v1_plus_the_new_instructions(self):
        v1 = PROMPT_V1.read_text(encoding="utf-8")
        v11 = PROMPT_V1_1.read_text(encoding="utf-8")
        self.assertGreater(len(v11), len(v1))
        for anchor in ("DİL (ZORUNLU)", "KOŞULLAR ZORUNLU ANLAMDIR",
                       "NİTELEYİCİLER ZORUNLU ANLAMDIR", "ÖNERMEYE ÖZEL ANLAM KISITLARI"):
            self.assertIn(anchor, v11)
        # Nothing v1 prohibited is missing from v1.1.
        for prohibition in ("EKLENMESİ YASAK OLANLAR", "SAYILAR", "KİPLİK (MODALİTE)",
                            "ATIF BAĞLAMA"):
            self.assertIn(prohibition, v11)

    def test_the_prompt_does_not_carry_the_c002_rule_as_its_only_defence(self):
        """§40. The general rule must hold for every claim; C-002 is an addition to it."""
        v11 = PROMPT_V1_1.read_text(encoding="utf-8")
        self.assertIn("Listelenen her koşul", v11)
        self.assertIn("qualifiers", v11)


class Freeze(unittest.TestCase):
    def test_the_historical_raw_output_is_untouched(self):
        parent = load(PARENT_MANIFEST)
        raw = load(HISTORICAL_RAW)
        self.assertEqual(
            hashlib.sha256(raw["raw_text"].encode("utf-8")).hexdigest(),
            parent["raw_draft_sha"])

    def test_the_freeze_checked_every_frozen_input(self):
        freeze = load(FREEZE)
        self.assertTrue(freeze["all_unchanged"], freeze["changed"])
        self.assertGreaterEqual(freeze["check_count"], 15)
        names = {c["name"] for c in freeze["checks"]}
        for required in ("composition-safe allowlist", "composition denylist",
                         "claim pair constraints", "composition validator (scripts/46)",
                         "section drafting contract v1", "book citation rendering contract v1",
                         "draft validation contract v1",
                         "historical rejected pilot raw output",
                         "historical pilot draft audit",
                         "section draft validator v1 (scripts/49)"):
            self.assertIn(required, names)

    def test_the_freeze_compares_against_the_drafting_phases_own_manifest(self):
        """A freeze certified from whatever is on disk detects nothing."""
        freeze = load(FREEZE)
        anchored = [c for c in freeze["checks"]
                    if c["baseline"] == "section_drafting_contract_v1_manifest"]
        self.assertGreaterEqual(len(anchored), 10)
        for check in anchored:
            self.assertEqual(check["expected_sha256"], check["actual_sha256"])

    def test_the_rejected_draft_ir_sha_is_recorded(self):
        freeze = load(FREEZE)
        self.assertEqual(len(freeze["historical_rejected_draft_ir_sha256"]), 64)
        self.assertEqual(freeze["historical_pilot_status"], "ATTEMPTED / REJECTED")


class RootCause(unittest.TestCase):
    def test_both_failed_units_are_root_caused(self):
        audit = load(ROOT_CAUSE)
        self.assertEqual(sorted(r["unit_id"] for r in audit["failed_units"]),
                         sorted(FAILED_UNITS))

    def test_every_required_field_is_recorded_per_unit(self):
        for row in load(ROOT_CAUSE)["failed_units"]:
            for field in ("unit_id", "claim_ids", "source_keys", "original_generated_text",
                          "failure_codes", "root_cause_class", "generator_input_present",
                          "validator_behavior_correct", "remediation_target"):
                self.assertIn(field, row)
            for claim in row["claims"]:
                for field in ("canonical_claim", "required_conditions", "required_qualifiers",
                              "actual_conditions", "actual_qualifiers"):
                    self.assertIn(field, claim)

    def test_root_causes_use_only_the_declared_classes(self):
        for row in load(ROOT_CAUSE)["failed_units"]:
            self.assertIn(row["root_cause_class"], ROOT_CAUSE_CLASSES)
            for cls in row["root_cause_classes"]:
                self.assertIn(cls, ROOT_CAUSE_CLASSES)

    def test_the_validator_is_not_blamed_for_a_correct_rejection(self):
        """§6. Both units were rejected and both deserved it."""
        audit = load(ROOT_CAUSE)
        self.assertTrue(audit["validator_behaviour"]["rejection_was_correct"])
        for row in audit["failed_units"]:
            self.assertTrue(row["validator_behavior_correct"])
            self.assertNotEqual(row["root_cause_class"], "VALIDATOR_COVERAGE_GAP")

    def test_the_drafting_input_carried_what_the_writer_needed(self):
        """If the input had been missing the condition, the remediation would be elsewhere."""
        for row in load(ROOT_CAUSE)["failed_units"]:
            self.assertTrue(row["generator_input_present"])

    def test_c002s_semantic_note_was_not_supplied_to_the_first_writer(self):
        """§7. That absence is the finding, and it is recorded as an absence."""
        audit = load(ROOT_CAUSE)
        row = next(r for r in audit["failed_units"] if r["unit_id"] == "U-A-P01-S03")
        claim = next(c for c in row["claims"] if c["claim_id"] == "SEC-02-2-C-002")
        self.assertFalse(claim["generator_input_present"]["semantic_note_supplied"])
        self.assertIn("acceptance criteria",
                      claim["generator_input_present"]["semantic_note_text"])

    def test_the_language_gap_is_evidenced_not_asserted(self):
        """U-C-P01-S02 is the proof: English prose that passed all nine v1 stages."""
        audit = load(ROOT_CAUSE)
        self.assertIn("U-C-P01-S02", audit["language_gap_evidence"]
                      ["english_units_v1_did_not_reject"])
        sweep = {row["unit_id"]: row for row in audit["language_sweep"]}
        self.assertEqual(sweep["U-C-P01-S02"]["detected_language"], "en")
        self.assertTrue(sweep["U-C-P01-S02"]["would_fail_v1_1_language"])

    def test_the_dropped_condition_and_qualifier_are_identified_by_name(self):
        audit = load(ROOT_CAUSE)
        thickness = next(r for r in audit["failed_units"] if r["unit_id"] == "U-C-P01-S03")
        dropped = [c["condition"] for claim in thickness["claims"]
                   for c in claim["actual_conditions"] if not c["preserved"]]
        self.assertIn("dependent on tunnel size", dropped)
        strength = next(r for r in audit["failed_units"] if r["unit_id"] == "U-A-P01-S03")
        dropped_q = [q["qualifier"] for claim in strength["claims"]
                     for q in claim["actual_qualifiers"] if not q["preserved"]]
        self.assertEqual(len(dropped_q), 1)
        self.assertIn("kabul kriteri", dropped_q[0])


class Constraints(unittest.TestCase):
    def test_the_c002_constraint_is_frozen_with_both_meanings(self):
        constraint = load(CONSTRAINTS)["constraints"][0]
        self.assertEqual(constraint["constraint_id"], "DSC-C002-001")
        self.assertEqual(constraint["claim_id"], "SEC-02-2-C-002")
        self.assertEqual(constraint["type"], "QUALIFIER_PRESERVATION")
        self.assertTrue(constraint["required_meaning"])
        self.assertTrue(constraint["forbidden_meaning"])

    def test_the_safe_relationship_names_both_claims_and_forbids_the_inference(self):
        """§9. C-002 does not prove C-001, and no approved relationship says it does."""
        relationship = load(CONSTRAINTS)["constraints"][0]["safe_relationship"]
        self.assertEqual(relationship["requirement_claim_id"], "SEC-02-2-C-001")
        self.assertEqual(relationship["acceptance_claim_id"], "SEC-02-2-C-002")
        self.assertIn("must not imply", relationship["rule"])

    def test_the_mapping_declares_the_tunnel_size_rendering(self):
        mappings = load(MAPPINGS)["mappings"]
        mapping = next(m for m in mappings
                       if m["source_condition"] == "dependent on tunnel size")
        self.assertIn("tünel boyutuna bağlı olarak", mapping["approved_target_renderings"])
        for field in ("mapping_id", "claim_id", "source_language", "target_language",
                      "source_condition", "approved_target_renderings", "numeric_invariants",
                      "modality_invariants", "scope_invariants", "source_keys"):
            self.assertIn(field, mapping)


class Fixtures(unittest.TestCase):
    def test_at_least_forty_new_fixtures(self):
        rows = [json.loads(l) for l in FIXTURES.read_text(encoding="utf-8").splitlines()
                if l.strip()]
        self.assertGreaterEqual(len(rows), 40)

    def test_the_categories_the_phase_requires_are_all_present(self):
        rows = [json.loads(l) for l in FIXTURES.read_text(encoding="utf-8").splitlines()
                if l.strip()]
        categories = {r["category"] for r in rows}
        for required in ("language_positive", "language_negative", "language_ambiguous",
                         "c002_qualifier_positive", "c002_qualifier_negative",
                         "cross_lingual_condition_positive", "cross_lingual_condition_negative",
                         "corrected_synthetic"):
            self.assertIn(required, categories)

    def test_the_historical_fixtures_are_not_deleted(self):
        """§ABSOLUTE PROHIBITIONS: the failed cases stay, as cases."""
        v1_fixtures = ROOT / "data" / "evaluation" / "section_drafting_contract_v1.jsonl"
        rows = [json.loads(l) for l in v1_fixtures.read_text(encoding="utf-8").splitlines()
                if l.strip()]
        self.assertEqual(len(rows), 107)


class Outcome(unittest.TestCase):
    def test_the_manifest_records_the_phase_honestly(self):
        if not MANIFEST.exists():
            self.skipTest("manifest not written yet; the phase has not been run")
        manifest = load(MANIFEST)
        for field in ("version", "parent_drafting_contract_version",
                      "parent_validation_contract_version", "draft_validation_contract_v1_1_sha",
                      "draft_language_contract_sha", "draft_language_validator_sha",
                      "draft_validator_v1_1_sha", "drafting_prompt_v1_1_sha",
                      "draft_plan_v1_1_sha", "root_cause_audit_sha", "cross_lingual_mapping_sha",
                      "fixture_sha", "historical_pilot_raw_sha", "generation_calls",
                      "retrieval_calls", "qdrant_writes", "test_counts", "false_accepts",
                      "false_rejects", "frozen_integrity", "pilot_status", "status",
                      "next_phase"):
            self.assertIn(field, manifest)
        self.assertEqual(manifest["retrieval_calls"], 0)
        self.assertEqual(manifest["qdrant_writes"], 0)
        self.assertEqual(manifest["false_accepts"], 0)
        self.assertEqual(manifest["false_rejects"], 0)
        self.assertEqual(manifest["automatic_retries"], 0)

    def test_no_more_than_one_generation_was_spent(self):
        if not MANIFEST.exists():
            self.skipTest("manifest not written yet")
        self.assertLessEqual(load(MANIFEST)["generation_calls"], 1)

    def test_the_raw_attempt_matches_its_recorded_sha(self):
        if not RAW_ATTEMPT_2.exists():
            self.skipTest("attempt #2 has not been generated")
        raw = load(RAW_ATTEMPT_2)
        self.assertEqual(hashlib.sha256(raw["raw_text"].encode("utf-8")).hexdigest(),
                         raw["raw_text_sha256"])
        self.assertEqual(raw["attempt"], 2)
        self.assertEqual(raw["temperature"], 0.0)
        self.assertEqual(raw["seed"], 11)

    def test_the_recorded_verdict_matches_the_artifacts_on_disk(self):
        if not MANIFEST.exists():
            self.skipTest("manifest not written yet")
        manifest = load(MANIFEST)
        status = manifest["pilot_status"]
        if status == "SEC-02-2 PILOT_DRAFT_ACCEPTED":
            self.assertTrue(ACCEPTED_IR.exists())
            self.assertTrue(RENDERED.exists())
            self.assertEqual(manifest["attempt_2_failed_units"], 0)
            self.assertTrue(manifest["attempt_gate"]["accept"])
        elif status == "SEC-02-2 PILOT_DRAFT_REJECTED":
            self.assertTrue(REJECTED.exists())
            self.assertFalse(RENDERED.exists(),
                             "a rejected pilot must not be rendered")
            self.assertFalse(load(REJECTED)["regenerated"])
        else:
            self.assertEqual(status, "NOT_ATTEMPTED")
            self.assertEqual(manifest["generation_calls"], 0)

    def test_an_accepted_pilot_is_not_called_final(self):
        if not MANIFEST.exists() or load(MANIFEST)["pilot_status"] != \
                "SEC-02-2 PILOT_DRAFT_ACCEPTED":
            self.skipTest("no accepted pilot")
        manifest = load(MANIFEST)
        self.assertIn("NOT FINAL MANUSCRIPT", manifest["final_decision"])
        self.assertNotIn("FINAL_SECTION", manifest["pilot_status"])

    def test_the_report_carries_every_required_section(self):
        if not REPORT.exists():
            self.skipTest("report not written yet")
        text = REPORT.read_text(encoding="utf-8")
        for heading in ("## Executive Decision", "## Historical Pilot Failure",
                        "## Why the Rejection Was Correct", "## Frozen Inputs",
                        "## Root Cause — U-A-P01-S03", "## Root Cause — U-C-P01-S03",
                        "## C-002 Semantic Boundary", "## Condition Preservation",
                        "## Cross-Lingual Condition Mapping", "## Draft Language Contract",
                        "## Language Validator", "## Draft Validation Contract v1.1",
                        "## Draft Validator v1.1", "## Drafting Prompt v1.1",
                        "## Draft Plan v1.1", "## Regression Fixtures",
                        "## Historical Regression", "## Frozen Integrity",
                        "## Attempt #2 Authorization", "## Attempt #2 Raw Generation",
                        "## Attempt #2 Validation", "## Required Topic Coverage",
                        "## Language Audit", "## Condition Audit", "## Qualifier Audit",
                        "## Composition Audit", "## Citation Audit", "## Numeric Audit",
                        "## Rendered Pilot", "## Final Decision", "## Next Phase"):
            self.assertIn(heading, text, heading)

    def test_an_accepted_draft_is_turkish_throughout(self):
        if not ACCEPTED_IR.exists():
            self.skipTest("no accepted DraftIR")
        spec = importlib.util.spec_from_file_location(
            "draft_language_validator_v1", ROOT / "scripts" / "51_draft_language_validator_v1.py")
        lang = importlib.util.module_from_spec(spec)
        sys.modules["draft_language_validator_v1"] = lang
        spec.loader.exec_module(lang)
        contract = lang.load_contract()
        ir = load(ACCEPTED_IR)
        self.assertEqual(ir["language"], "tr")
        for unit in ir["units"]:
            with self.subTest(unit=unit["unit_id"]):
                self.assertEqual(lang.validate_unit(
                    unit["unit_id"], unit["unit_type"], unit["material"], ir["language"],
                    unit["text"], unit["claim_ids"], contract), [])

    def test_the_remediation_audit_reports_every_required_metric(self):
        if not REMEDIATION_AUDIT.exists():
            self.skipTest("no remediation audit; attempt #2 has not been validated")
        audit = load(REMEDIATION_AUDIT)
        for field in ("historical_failed_units", "root_causes", "new_semantic_constraints",
                      "new_language_rules", "new_failure_codes", "new_fixtures",
                      "historical_tests_run", "new_tests_run", "language_validation_results",
                      "condition_validation_results", "qualifier_validation_results",
                      "generation_attempts_in_this_phase", "attempt_2_units",
                      "attempt_2_material_units", "attempt_2_failed_units",
                      "required_topic_coverage", "citation_coverage", "language_compliance",
                      "condition_compliance", "qualifier_compliance", "composition_failures",
                      "numeric_failures", "citation_failures"):
            self.assertIn(field, audit)


if __name__ == "__main__":
    unittest.main()
