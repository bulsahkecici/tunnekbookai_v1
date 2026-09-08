"""Tests for SEC-02-2 Draft Readiness Closure v1.

These assert the closure protocol and the safety properties, not the conclusion. A run that
reached READY_FOR_DRAFT by loosening something would fail here; a run that honestly reached
NOT_READY would pass, because the point of the suite is that whatever verdict is reported is the
one the frozen contract actually produces.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "book" / "sec_02_2_readiness_closure"
ACCEPTANCE = ROOT / "data" / "metadata" / "sec_02_2_draft_readiness_acceptance_v1.json"
MANIFEST = ROOT / "data" / "book" / "manifests" / "sec_02_2_draft_readiness_closure_v1.json"
REPORT = ROOT / "reports" / "sec_02_2_draft_readiness_closure_v1.md"
P0_REPORT = ROOT / "reports" / "p0_evidence_gap_resolution_v1.md"

REQUIRED_TOPICS = ("çimento dozajı", "kaplama kalınlığı", "dayanım sınıfı")
SCOPED_QUESTIONS = ("Q-02-2-03", "Q-02-2-04", "Q-02-2-06")
CRITICALITY = {"CRITICAL", "IMPORTANT_NON_BLOCKING", "OPTIONAL"}
READINESS_USE = {"REQUIRED_CORE", "SUPPORTED_CONTEXT", "OPTIONAL_ENRICHMENT", "DO_NOT_DRAFT"}
WORKAROUND = {"omit_optional_material", "state_supported_narrower_claim",
              "preserve_context_qualifier", "separate_conflicting_contexts", "NONE"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


class ClosureArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_json(MANIFEST)
        cls.acceptance = load_json(ACCEPTANCE)
        cls.topics = load_json(OUT / "audits" / "required_topic_coverage_v1.json")
        cls.gaps = load_jsonl(OUT / "audits" / "p1_p2_gap_closure_v1.jsonl")
        cls.numerics = load_jsonl(OUT / "audits" / "numeric_closure_v1.jsonl")
        cls.contexts = load_jsonl(OUT / "audits" / "context_difference_closure_v1.jsonl")
        cls.syntheses = load_jsonl(OUT / "audits" / "dropped_synthesis_closure_v1.jsonl")
        cls.limitations = load_jsonl(OUT / "audits" / "section_limitations_v1.jsonl")
        cls.consistency = load_json(OUT / "audits" / "p0_manifest_consistency_v1.json")
        cls.allowlist = load_jsonl(OUT / "claims" / "draft_claim_allowlist_v1.jsonl")
        cls.denylist = load_jsonl(OUT / "claims" / "draft_claim_denylist_v1.jsonl")
        cls.universe = load_jsonl(OUT / "claims" / "claim_universe_v1.jsonl")
        cls.mappings = load_jsonl(OUT / "evidence" / "closure_span_mappings_v1.jsonl")
        cls.bundle = load_json(OUT / "bundle" / "SEC-02-2.json")


# ---------------------------------------------------------------- 5 / 49: the contract

class TestAcceptanceContract(ClosureArtifacts):
    def test_acceptance_contract_exists_and_is_referenced_by_the_manifest(self):
        self.assertTrue(ACCEPTANCE.exists())
        self.assertEqual(self.manifest["acceptance_contract"],
                         "data/metadata/sec_02_2_draft_readiness_acceptance_v1.json")

    def test_contract_was_authored_before_results(self):
        self.assertTrue(self.acceptance["authored_before_results"])
        self.assertTrue(self.manifest["acceptance_authored_before_results"])
        self.assertTrue(
            self.manifest["go_conditions"]["acceptance_contract_authored_before_results"])

    def test_contract_names_all_three_required_topics(self):
        self.assertEqual(tuple(self.acceptance["required_topics"]), REQUIRED_TOPICS)

    def test_contract_binds_every_required_topic_to_at_least_one_question(self):
        for topic in REQUIRED_TOPICS:
            self.assertTrue(self.acceptance["topic_question_binding"][topic])

    def test_contract_does_not_treat_ready_with_limitations_as_ready_for_draft(self):
        self.assertNotEqual(self.acceptance["ready_for_draft_conditions"],
                            self.acceptance["ready_with_limitations_conditions"])
        self.assertIn("READY_WITH_LIMITATIONS is not READY_FOR_DRAFT",
                      self.acceptance["why_this_contract_exists"])

    def test_contract_forbids_knowledge_fill_and_prose(self):
        joined = " ".join(self.acceptance["prohibitions"])
        for forbidden in ("prose", "model memory", "web", "invented"):
            self.assertIn(forbidden, joined)

    def test_contract_declares_zero_default_budgets(self):
        budgets = self.acceptance["budgets"]
        self.assertEqual(budgets["generation_calls_default"], 0)
        self.assertEqual(budgets["retrieval_calls_default"], 0)
        self.assertFalse(budgets["same_question_retry_permitted"])
        self.assertLessEqual(budgets["retrieval_experiment_top_k_max"], 40)


# ---------------------------------------------------------------- 58: required topics

class TestRequiredTopics(ClosureArtifacts):
    def test_all_three_required_topics_are_rows_in_the_matrix(self):
        self.assertEqual({row["topic"] for row in self.topics}, set(REQUIRED_TOPICS))

    def test_every_topic_row_carries_a_coverage_status_from_the_vocabulary(self):
        for row in self.topics:
            self.assertIn(row["coverage_status"],
                          {"COMPLETE", "COMPLETE_WITH_QUALIFIER", "INCOMPLETE"})

    def test_incomplete_topics_state_a_blocking_reason(self):
        for row in self.topics:
            if row["coverage_status"] == "INCOMPLETE":
                self.assertTrue(row["blocking_reason"])
            else:
                self.assertIsNone(row["blocking_reason"])

    def test_covered_topics_rest_on_a_required_core_allowlisted_claim(self):
        allowed = {row["claim_id"] for row in self.allowlist}
        for row in self.topics:
            if row["coverage_status"] == "INCOMPLETE":
                continue
            self.assertTrue(row["required_core_claim_ids"], row["topic"])
            for claim_id in row["required_core_claim_ids"]:
                self.assertIn(claim_id, allowed)

    def test_topic_coverage_never_rests_on_a_derived_numeric(self):
        for row in self.topics:
            if row["coverage_status"] != "INCOMPLETE":
                self.assertNotEqual(row["numeric_status"],
                                    "DERIVED_PRESENTED_AS_SOURCE_STATED")


# ---------------------------------------------------------------- 51 / 59: the verdict

class TestReadinessVerdict(ClosureArtifacts):
    def test_readiness_is_from_the_allowed_vocabulary(self):
        self.assertIn(self.manifest["final_readiness"],
                      {"READY_FOR_DRAFT", "READY_WITH_LIMITATIONS", "NOT_READY"})

    def test_ready_for_draft_implies_the_full_contract_is_met(self):
        if self.manifest["final_readiness"] != "READY_FOR_DRAFT":
            self.skipTest("section is not READY_FOR_DRAFT")
        for row in self.topics:
            self.assertIn(row["coverage_status"], {"COMPLETE", "COMPLETE_WITH_QUALIFIER"})
        self.assertEqual(self.manifest["critical_limitations"], 0)
        self.assertEqual(
            [n for n in self.numerics
             if n["criticality"] == "CRITICAL"
             and n["current_status"] in {"UNSUPPORTED", "PARTIALLY_SUPPORTED",
                                         "CONTEXT_DIFFERENT"}], [])
        self.assertEqual(
            [c for c in self.contexts
             if c["final_status"] in {"BLOCKING_CONFLICT", "INSUFFICIENT_TO_DECIDE"}], [])
        self.assertEqual(
            [s for s in self.syntheses
             if s["final_status"] == "BLOCKING_MISSING_SYNTHESIS"], [])
        self.assertEqual(self.manifest["readiness_blocking_reasons"], [])

    def test_ready_for_draft_is_not_granted_on_p0_alone(self):
        """Rule 51. All P0 resolved must be insufficient on its own - the contract has to also
        require topic coverage, which is exactly what the previous phase's did not."""
        conditions = " ".join(self.acceptance["ready_for_draft_conditions"])
        self.assertIn("required topic", conditions)
        self.assertIn("P0", conditions)

    def test_not_ready_states_blocking_reasons(self):
        if self.manifest["final_readiness"] != "NOT_READY":
            self.skipTest("section is not NOT_READY")
        self.assertTrue(self.manifest["readiness_blocking_reasons"])

    def test_p0_questions_did_not_regress(self):
        self.assertEqual(self.manifest["p0_regressions"], [])
        for status in self.manifest["p0_status"].values():
            self.assertEqual(status, "RESOLVED")

    def test_ready_with_limitations_states_an_explicit_demotion_reason(self):
        if self.manifest["final_readiness"] != "READY_WITH_LIMITATIONS":
            self.skipTest("section is not READY_WITH_LIMITATIONS")
        assessment = self.bundle["readiness_assessment"]
        self.assertTrue(assessment["demotion_reason"],
                        "a demotion below READY_FOR_DRAFT must say why, not merely happen")
        self.assertTrue(assessment["composition_constraints"])
        self.assertTrue(self.manifest["readiness_non_blocking_limitations"])

    def test_composition_constraints_correspond_to_real_closure_records(self):
        assessment = self.bundle["readiness_assessment"]
        known = ({c["context_difference_id"] for c in self.contexts}
                 | {s["synthesis_id"] for s in self.syntheses})
        for constraint in assessment.get("composition_constraints", []):
            self.assertIn(constraint, known)

    def test_drafting_is_disabled_regardless_of_verdict(self):
        self.assertFalse(self.manifest["drafting_enabled"])
        self.assertFalse(self.bundle["drafting_enabled"])
        self.assertFalse(self.acceptance["drafting_enabled"])
        self.assertTrue(self.manifest["go_conditions"]["drafting_disabled"])

    def test_readiness_verdict_agrees_between_manifest_and_bundle(self):
        self.assertEqual(self.manifest["final_readiness"],
                         self.bundle["readiness_assessment"]["readiness"])


# ---------------------------------------------------------------- 60 / 37: allowlist

class TestAllowlist(ClosureArtifacts):
    def test_allowlist_is_non_empty(self):
        self.assertTrue(self.allowlist)

    def test_every_allowlisted_claim_is_supported_and_citation_ready(self):
        for row in self.allowlist:
            self.assertEqual(row["support_status"], "SUPPORTED", row["claim_id"])
            self.assertTrue(row["citation_ready"], row["claim_id"])

    def test_every_allowlisted_claim_is_traceable(self):
        for row in self.allowlist:
            self.assertTrue(row["source_keys"], row["claim_id"])
            for key in row["source_keys"]:
                self.assertRegex(key, r"^SRC-DOC\d+-[0-9a-f]{12}$")
            self.assertTrue(row["spans_verified"], row["claim_id"])

    def test_no_allowlisted_claim_is_superseded(self):
        for row in self.allowlist:
            self.assertEqual(row["superseded_by"], [], row["claim_id"])

    def test_no_allowlisted_claim_carries_a_do_not_draft_use(self):
        for row in self.allowlist:
            self.assertIn(row["readiness_use"], READINESS_USE)
            self.assertNotEqual(row["readiness_use"], "DO_NOT_DRAFT", row["claim_id"])

    def test_allowlisted_numerics_are_source_stated(self):
        for row in self.allowlist:
            for numeric in row["numeric"]:
                self.assertFalse(numeric.get("derived") and numeric.get("source_stated"),
                                 f"{row['claim_id']}: {numeric}")

    def test_allowlist_and_denylist_are_disjoint(self):
        allowed = {row["claim_id"] for row in self.allowlist}
        denied = {row["claim_id"] for row in self.denylist}
        self.assertEqual(allowed & denied, set())

    def test_allowlist_rows_are_claims_and_not_prose(self):
        """Rule 39. A canonical claim is a proposition, not a paragraph."""
        for row in self.allowlist:
            claim = row["canonical_claim"]
            self.assertLess(len(claim), 400, row["claim_id"])
            self.assertNotIn("\n", claim)

    def test_no_duplicate_claim_ids_in_the_allowlist(self):
        ids = [row["claim_id"] for row in self.allowlist]
        self.assertEqual(len(ids), len(set(ids)))


# ---------------------------------------------------------------- 61: denylist

class TestDenylist(ClosureArtifacts):
    def test_denylist_is_non_empty_and_every_row_states_a_reason(self):
        self.assertTrue(self.denylist)
        for row in self.denylist:
            self.assertTrue(row["deny_reasons"], row["claim_id"])
            self.assertEqual(row["readiness_use"], "DO_NOT_DRAFT")

    def test_known_unsafe_items_are_denied_and_never_allowed(self):
        allowed = {row["claim_id"] for row in self.allowlist}
        denied = {row["claim_id"] for row in self.denylist}
        for unsafe in ("SEC-02-2-DENY-NUM-150MM", "SEC-02-2-DENY-SYN-001"):
            self.assertIn(unsafe, denied)
            self.assertNotIn(unsafe, allowed)

    def test_unsupported_prior_claims_did_not_leak_into_the_allowlist(self):
        allowed = {row["claim_id"] for row in self.allowlist}
        for row in self.universe:
            if row["support_status"] != "SUPPORTED" or not row["citation_ready"]:
                self.assertNotIn(row["claim_id"], allowed, row["claim_id"])

    def test_every_unresolved_clause_is_recorded_rather_than_dropped(self):
        unresolved = load_jsonl(OUT / "evidence" / "unresolved_after_packet_read_v1.jsonl")
        self.assertTrue(unresolved)
        denied = {row["claim_id"] for row in self.denylist}
        for row in unresolved:
            self.assertTrue(row["reason"])
            self.assertIn(f"SEC-02-2-DENY-{row['clause_id']}", denied)


# ---------------------------------------------------------------- 62: the 150 mm

class TestDerivedMillimetreConversion(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.allowlist = load_jsonl(OUT / "claims" / "draft_claim_allowlist_v1.jsonl")
        cls.denylist = load_jsonl(OUT / "claims" / "draft_claim_denylist_v1.jsonl")
        cls.numerics = load_jsonl(OUT / "audits" / "numeric_closure_v1.jsonl")

    def test_the_derived_150_mm_is_recorded_as_derived_only(self):
        record = next(n for n in self.numerics
                      if n["clause_id"] == "Q-02-2-04-N06-C01#derived")
        self.assertEqual(record["current_status"], "DERIVED_ONLY")
        self.assertTrue(record["derived"])
        self.assertEqual(record["derived_from_value"], "15")
        self.assertEqual(record["derived_from_unit"], "cm")
        self.assertFalse(record["citation_ready"])
        self.assertEqual(record["source_span"], "")

    def test_the_single_pass_maximum_is_allowlisted_only_in_centimetres(self):
        claim = next(r for r in self.allowlist if r["claim_id"] == "SEC-02-2-C-003")
        self.assertNotIn("150", claim["canonical_claim"])
        self.assertIn("15 cm", claim["canonical_claim"])
        self.assertEqual([n["unit"] for n in claim["numeric"]], ["cm"])
        self.assertEqual([n["value"] for n in claim["numeric"]], ["15"])
        self.assertTrue(all(n["source_stated"] and not n["derived"]
                            for n in claim["numeric"]))

    def test_no_allowlisted_claim_presents_150_mm_for_the_single_pass_clause(self):
        for row in self.allowlist:
            if row.get("question_id") != "Q-02-2-04":
                continue
            for numeric in row["numeric"]:
                if numeric["unit"] == "mm" and numeric["value"] == "150":
                    # Only permitted where the source states it as a range bound in its own
                    # right, which is the clay-zone clause, never the single-pass conversion.
                    self.assertEqual(row["claim_id"], "SEC-02-2-C-009")
                    self.assertTrue(numeric["source_stated"])
                    self.assertFalse(numeric["derived"])

    def test_the_150_mm_wording_is_on_the_denylist(self):
        row = next(r for r in self.denylist if r["claim_id"] == "SEC-02-2-DENY-NUM-150MM")
        self.assertIn("150 mm", row["canonical_claim"])
        self.assertIn("derived_numeric_presented_as_source_stated", row["deny_reasons"])
        self.assertFalse(row["citation_ready"])


# ---------------------------------------------------------------- 63: SYN-001

class TestDroppedSynthesis(ClosureArtifacts):
    def test_syn_001_is_closed_with_a_status_from_the_vocabulary(self):
        synthesis = next(s for s in self.syntheses if s["synthesis_id"] == "SYN-001")
        self.assertIn(synthesis["final_status"],
                      {"SAFE_TO_DROP", "REPLACE_WITH_SEPARATE_SUPPORTED_CLAIMS",
                       "BLOCKING_MISSING_SYNTHESIS"})

    def test_the_compound_never_becomes_draftable(self):
        allowed_text = " ".join(r["canonical_claim"] for r in self.allowlist)
        for connective in ("belirtilse de", "olmasına rağmen", "buna rağmen", "although"):
            self.assertNotIn(connective, allowed_text)

    def test_the_two_dosage_figures_never_share_one_allowlisted_claim(self):
        """360 is a general-concrete maximum and 400 a shotcrete minimum. A single claim holding
        both is the synthesis coming back."""
        for row in self.allowlist:
            values = {n.get("value") for n in row["numeric"]}
            self.assertFalse({"360", "400"} <= values, row["claim_id"])

    def test_components_remain_separately_available(self):
        allowed = {row["claim_id"] for row in self.allowlist}
        self.assertIn("SEC-02-2-P0-002", allowed)
        self.assertIn("SEC-02-2-P0-003", allowed)

    def test_the_drafting_rule_names_the_forbidden_connectives(self):
        synthesis = next(s for s in self.syntheses if s["synthesis_id"] == "SYN-001")
        self.assertIn("concessive", synthesis["future_drafting_rule"])
        self.assertTrue(synthesis["unsupported_relation"])


# ---------------------------------------------------------------- 64: CF-P0-001

class TestContextDifference(ClosureArtifacts):
    def test_cf_p0_001_is_closed_with_a_status_from_the_vocabulary(self):
        difference = next(c for c in self.contexts
                          if c["context_difference_id"] == "CF-P0-001")
        self.assertIn(difference["final_status"],
                      {"SAFE_CONTEXT_DIFFERENCE", "REQUIRES_QUALIFIER", "BLOCKING_CONFLICT",
                       "INSUFFICIENT_TO_DECIDE"})

    def test_retained_context_difference_keeps_both_sets_of_conditions_explicit(self):
        for difference in self.contexts:
            if difference["final_status"] in {"BLOCKING_CONFLICT", "INSUFFICIENT_TO_DECIDE"}:
                continue
            self.assertTrue(difference["conditions_a"])
            self.assertTrue(difference["conditions_b"])
            self.assertNotEqual(difference["conditions_a"], difference["conditions_b"])
            self.assertFalse(difference["same_scope"])
            self.assertTrue(difference["drafting_rule"])

    def test_a_qualifier_requiring_difference_puts_the_qualifier_on_the_claim(self):
        difference = next(c for c in self.contexts
                          if c["context_difference_id"] == "CF-P0-001")
        if difference["final_status"] != "REQUIRES_QUALIFIER":
            self.skipTest("CF-P0-001 does not require a qualifier")
        claim = next(r for r in self.allowlist if r["claim_id"] == difference["claim_a_id"])
        self.assertTrue(claim["qualifiers"], "the mandatory scope qualifier must travel with "
                                             "the claim, not only with the audit record")

    def test_no_silent_reconciliation_of_the_two_figures(self):
        difference = next(c for c in self.contexts
                          if c["context_difference_id"] == "CF-P0-001")
        self.assertIn("No averaging", difference["drafting_rule"])


# ---------------------------------------------------------------- 65: P1/P2 classification

class TestP1P2Classification(ClosureArtifacts):
    def test_each_scoped_question_has_exactly_one_closure_row(self):
        ids = [gap["question_id"] for gap in self.gaps]
        self.assertEqual(sorted(ids), sorted(SCOPED_QUESTIONS))

    def test_each_scoped_question_receives_an_explicit_criticality_and_disposition(self):
        for gap in self.gaps:
            self.assertIn(gap["criticality"], CRITICALITY, gap["question_id"])
            self.assertTrue(gap["disposition"], gap["question_id"])
            self.assertTrue(gap["reason"], gap["question_id"])
            self.assertEqual(gap["audit_method"], "manual_evidence_read")

    def test_manifest_records_the_same_dispositions(self):
        for question_id in SCOPED_QUESTIONS:
            self.assertIn(question_id, self.manifest["p1_p2_dispositions"])
            self.assertIn(self.manifest["p1_p2_dispositions"][question_id]["criticality"],
                          CRITICALITY)

    def test_every_gap_is_assessed_on_all_six_axes(self):
        axes = ("affects_required_topic_coverage", "affects_numeric_completeness",
                "affects_requirement_completeness", "affects_technical_correctness",
                "affects_safety_critical_meaning", "affects_objective_scope")
        for gap in self.gaps:
            for axis in axes:
                self.assertIsInstance(gap[axis], bool, f"{gap['question_id']}.{axis}")

    def test_a_question_touching_required_topic_coverage_cannot_be_optional(self):
        for gap in self.gaps:
            if gap["affects_required_topic_coverage"]:
                self.assertNotEqual(gap["criticality"], "OPTIONAL", gap["question_id"])

    def test_non_critical_classification_carries_one_of_the_two_permitted_classes(self):
        for gap in self.gaps:
            if gap["criticality"] == "CRITICAL":
                self.assertIsNone(gap["non_critical_class"], gap["question_id"])
            else:
                self.assertIn(gap["non_critical_class"],
                              {"NON_CRITICAL_ENRICHMENT", "OPTIONAL_DETAIL"},
                              gap["question_id"])

    def test_an_unresolved_critical_gap_would_block(self):
        for gap in self.gaps:
            if gap["criticality"] == "CRITICAL" and gap["disposition"] != "RESOLVED":
                self.assertNotEqual(self.manifest["final_readiness"], "READY_FOR_DRAFT")

    def test_q_02_2_03_is_treated_as_the_required_topic_carrier(self):
        gap = next(g for g in self.gaps if g["question_id"] == "Q-02-2-03")
        self.assertTrue(gap["required_by_plan"])
        self.assertTrue(gap["affects_required_topic_coverage"])
        self.assertEqual(gap["criticality"], "CRITICAL")

    def test_every_gap_read_the_whole_packet(self):
        for gap in self.gaps:
            self.assertGreaterEqual(gap["packet_items_read"], 19, gap["question_id"])


# ---------------------------------------------------------------- 66: manifest consistency

class TestManifestConsistency(ClosureArtifacts):
    def test_the_canonical_retrieval_gap_count_is_recorded_exactly_once(self):
        self.assertIsInstance(self.consistency["canonical_value"], int)
        self.assertEqual(self.manifest["canonical_retrieval_gap_count"],
                         self.consistency["canonical_value"])
        occurrences = REPORT.read_text(encoding="utf-8").count(
            self.consistency["canonical_statement"])
        self.assertEqual(occurrences, 1)

    def test_the_inconsistency_is_named_with_its_source_of_truth(self):
        self.assertTrue(self.consistency["inconsistency_found"])
        self.assertTrue(self.consistency["source_of_truth"])
        self.assertTrue(self.consistency["explanation"])
        self.assertGreaterEqual(len(self.consistency["intermediate_values_found"]), 3)

    def test_the_canonical_value_matches_the_p0_artifacts(self):
        expansions = load_jsonl(ROOT / "data" / "book" / "p0_resolution" / "audits" /
                                "p0_retrieval_expansion_v1.jsonl")
        confirmed = [e["clause_id"] for e in expansions if e.get("retrieval_gap_confirmed")]
        self.assertEqual(self.consistency["canonical_value"], len(confirmed))
        self.assertEqual(self.consistency["canonical_clause_ids"], sorted(confirmed))

    def test_the_impact_on_sec_02_2_is_stated(self):
        self.assertTrue(self.consistency["impact_on_sec_02_2"])

    def test_the_historical_p0_report_is_not_rewritten(self):
        self.assertFalse(self.consistency["historical_report_modified"])
        p0_manifest = load_json(ROOT / "data" / "book" / "manifests" /
                                "p0_evidence_gap_resolution_v1.json")
        for check in self.manifest["frozen_integrity"]["checks"]:
            if check["path"].endswith("p0_evidence_gap_resolution_v1.json"):
                self.assertTrue(check["unchanged"])
        self.assertEqual(p0_manifest["version"], "tunnelbook-p0-evidence-gap-resolution-v1")


# ---------------------------------------------------------------- 67: frozen integrity

class TestFrozenIntegrity(ClosureArtifacts):
    def test_all_frozen_inputs_are_byte_identical(self):
        self.assertTrue(self.manifest["frozen_integrity"]["all_unchanged"],
                        self.manifest["frozen_integrity"]["changed"])

    def test_the_named_frozen_components_are_all_checked(self):
        names = " ".join(c["name"] for c in self.manifest["frozen_integrity"]["checks"])
        for component in ("Retriever v1", "Prompt v5", "Output Contract v1.1",
                          "Production Grounded Generator v1", "Book Pipeline Extractor v1.1",
                          "P0 Evidence Gap Resolution v1", "source registry v1",
                          "corpus chunks"):
            self.assertIn(component, names)

    def test_every_p0_resolution_artifact_is_checked(self):
        paths = {c["path"] for c in self.manifest["frozen_integrity"]["checks"]}
        p0_manifest = load_json(ROOT / "data" / "book" / "manifests" /
                                "p0_evidence_gap_resolution_v1.json")
        for relative in p0_manifest["artifact_shas"]:
            self.assertIn(f"data/book/{relative}", paths)

    def test_the_source_registry_was_not_appended_to(self):
        check = next(c for c in self.manifest["frozen_integrity"]["checks"]
                     if c["path"] == "data/book/source_registry_v1.jsonl")
        self.assertTrue(check["unchanged"])

    def test_new_source_keys_went_to_this_phases_own_registry(self):
        path = OUT / "evidence" / "closure_source_registry_v1.jsonl"
        self.assertTrue(path.exists())
        for row in load_jsonl(path):
            self.assertEqual(row["registered_by"],
                             "tunnelbook-sec-02-2-draft-readiness-closure-v1")


# ---------------------------------------------------------------- 68: qdrant / budgets

class TestBudgets(ClosureArtifacts):
    def test_qdrant_is_unchanged_with_no_writes(self):
        self.assertEqual(self.manifest["qdrant_points_before"],
                         self.manifest["qdrant_points_after"])
        self.assertEqual(self.manifest["qdrant_writes"], 0)
        if self.manifest["qdrant_reachable"]:
            self.assertEqual(self.manifest["qdrant_points_before"],
                             self.manifest["qdrant_expected"])
        else:
            # An unobserved count must be reported as unknown, never silently as the expected
            # value. The claim that nothing was written stands on the phase having no write path.
            self.assertIsNone(self.manifest["qdrant_points_before"])
            self.assertIn("not reachable", self.manifest["qdrant_note"])
            self.assertEqual(self.manifest["retrieval_calls"], 0)

    def test_no_generation_and_no_retrieval(self):
        self.assertEqual(self.manifest["generation_calls"], 0)
        self.assertEqual(self.manifest["retrieval_calls"], 0)
        self.assertEqual(self.manifest["retrieval_expansion_attempts"], 0)
        self.assertTrue(self.manifest["production_retrieval_default_unchanged"])

    def test_source_policy_is_frozen_packet_only(self):
        self.assertEqual(self.manifest["source_policy"], "frozen_packet_only")


# ---------------------------------------------------------------- spans and provenance

class TestSpanIntegrity(ClosureArtifacts):
    def test_every_authored_span_was_verified_against_the_frozen_packet(self):
        self.assertTrue(self.mappings)
        unverified = [m["mapping_id"] for m in self.mappings if not m["span_verified"]]
        self.assertEqual(unverified, [])
        self.assertEqual(self.manifest["spans_unverified"], 0)

    def test_every_mapping_names_a_packet_sha_and_a_chunk(self):
        for mapping in self.mappings:
            self.assertTrue(mapping["context_packet_sha"], mapping["mapping_id"])
            self.assertRegex(mapping["chunk_id"], r"^DOC\d+-C\d+$")
            self.assertTrue(mapping["source_span"].strip(), mapping["mapping_id"])
            self.assertEqual(mapping["audit_method"], "manual_evidence_read")

    def test_every_mapping_belongs_to_a_question_in_scope(self):
        for mapping in self.mappings:
            self.assertIn(mapping["question_id"], SCOPED_QUESTIONS)

    def test_allowlisted_closure_claims_reference_only_verified_mappings(self):
        verified = {m["mapping_id"] for m in self.mappings if m["span_verified"]}
        for row in self.allowlist:
            for mapping_id in row["mapping_ids"]:
                self.assertIn(mapping_id, verified, row["claim_id"])


# ---------------------------------------------------------------- claim universe

class TestClaimUniverse(ClosureArtifacts):
    def test_no_duplicate_claim_ids(self):
        ids = [row["claim_id"] for row in self.universe]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_claim_carries_the_required_fields(self):
        required = ("claim_id", "canonical_claim", "question_id", "support_status",
                    "citation_ready", "source_keys", "numeric", "conditions", "qualifiers",
                    "supersedes", "superseded_by", "readiness_use")
        for row in self.universe:
            for field in required:
                self.assertIn(field, row, row["claim_id"])
            self.assertIn(row["readiness_use"], READINESS_USE, row["claim_id"])

    def test_superseded_claims_are_not_citation_ready(self):
        for row in self.universe:
            if row["superseded_by"]:
                self.assertFalse(row["citation_ready"], row["claim_id"])
                self.assertEqual(row["readiness_use"], "DO_NOT_DRAFT", row["claim_id"])

    def test_supersession_is_acyclic_and_resolves(self):
        ids = {row["claim_id"] for row in self.universe}
        for row in self.universe:
            for successor in row["superseded_by"]:
                self.assertIn(successor, ids, row["claim_id"])
                self.assertNotEqual(successor, row["claim_id"])

    def test_no_claim_counts_twice_for_a_topic(self):
        for row in self.universe:
            if row["superseded_by"]:
                self.assertIsNone(row["topic"], row["claim_id"])

    def test_no_carried_numeric_borrows_a_unit_from_another_question(self):
        """A bare value carried from a prior claim must not pick up a unit from a numeric-review
        row belonging to a different question. '400' in an inch/mm thickness claim is not
        400 kg/m3."""
        review = load_jsonl(ROOT / "data" / "book" / "p0_resolution" / "audits" /
                            "p0_numeric_review_v1.jsonl")
        units_by_question: dict[str, set] = {}
        for entry in review:
            units_by_question.setdefault(entry["question_id"], set()).add(
                (str(entry["value"]), entry["unit"]))
        for row in self.universe:
            for numeric in row["numeric"]:
                if numeric.get("role") != "carried" or not numeric.get("unit"):
                    continue
                signature = (str(numeric["value"]), numeric["unit"])
                for question_id, signatures in units_by_question.items():
                    if signature in signatures:
                        self.assertEqual(question_id, row["question_id"],
                                         f"{row['claim_id']} carries {signature} whose reviewed "
                                         f"unit belongs to {question_id}")

    def test_unitless_carried_values_are_labelled_rather_than_given_a_unit(self):
        for row in self.universe:
            for numeric in row["numeric"]:
                if numeric.get("unit") is None and numeric.get("role"):
                    self.assertEqual(numeric["role"], "unitless_reference_fragment",
                                     row["claim_id"])

    def test_universe_covers_prior_and_closure_claims(self):
        prior = load_jsonl(ROOT / "data" / "book" / "p0_resolution" / "claims" /
                           "SEC-02-2.jsonl")
        ids = {row["claim_id"] for row in self.universe}
        for row in prior:
            self.assertIn(row["claim_id"], ids)
        self.assertGreater(self.manifest["claims_closed_this_phase"], 0)


# ---------------------------------------------------------------- limitations

class TestLimitationRegister(ClosureArtifacts):
    def test_every_limitation_is_fully_specified(self):
        self.assertTrue(self.limitations)
        for row in self.limitations:
            self.assertTrue(row["limitation_id"])
            self.assertTrue(row["description"])
            self.assertTrue(row["drafting_impact"])
            self.assertIn(row["criticality"], CRITICALITY, row["limitation_id"])
            self.assertIn(row["allowed_workaround"], WORKAROUND, row["limitation_id"])
            self.assertEqual(row["audit_method"], "manual_evidence_read")

    def test_no_knowledge_fill_workaround(self):
        joined = " ".join(row["allowed_workaround"] for row in self.limitations).lower()
        for forbidden in ("knowledge", "memory", "web", "assume", "infer"):
            self.assertNotIn(forbidden, joined)

    def test_critical_limitations_are_counted_consistently(self):
        counted = sum(1 for row in self.limitations if row["criticality"] == "CRITICAL")
        self.assertEqual(counted, self.manifest["critical_limitations"])

    def test_the_four_carried_forward_limitations_are_all_addressed(self):
        """The P0 phase handed forward four. Each must appear in this register or in a closure
        record - none may vanish."""
        blob = json.dumps(self.limitations + self.contexts + self.syntheses + self.numerics,
                          ensure_ascii=False)
        for token in ("Q-02-2-03", "Q-02-2-04", "Q-02-2-06", "CF-P0-001", "SYN-001"):
            self.assertIn(token, blob + json.dumps(self.gaps, ensure_ascii=False))


# ---------------------------------------------------------------- report / no prose

class TestReportAndNoProse(ClosureArtifacts):
    def test_report_exists_with_every_required_section(self):
        text = REPORT.read_text(encoding="utf-8")
        for heading in ("# SEC-02-2 Draft Readiness Closure v1", "## Executive Decision",
                        "## Why READY_WITH_LIMITATIONS Was Not Enough", "## Frozen Inputs",
                        "## Acceptance Criteria", "## Required Topic Coverage", "## Q-02-2-03",
                        "## Q-02-2-04", "## Q-02-2-06", "## Unresolved Numeric Clause",
                        "## CF-P0-001", "## SYN-001", "## Claim Allowlist", "## Claim Denylist",
                        "## Limitation Register", "## Manifest Consistency Audit",
                        "## Generation / Retrieval Usage", "## Frozen Integrity", "## Tests",
                        "## Final Readiness Decision", "## Next Phase"):
            self.assertIn(heading, text)

    def test_no_section_or_chapter_prose_was_written(self):
        manuscript = ROOT / "data" / "book" / "manuscript"
        self.assertFalse(manuscript.exists(), "this phase must not start a manuscript")
        for path in OUT.rglob("*"):
            self.assertNotIn("draft", path.name.replace("draft_claim", ""))

    def test_next_phase_matches_the_verdict(self):
        route = self.manifest["next_phase"]["route"]
        readiness = self.manifest["final_readiness"]
        if readiness == "READY_FOR_DRAFT":
            self.assertIn("SECTION DRAFTING CONTRACT V1", route)
            self.assertIn("BOOK CITATION RENDERING CONTRACT V1", route)
        elif readiness == "READY_WITH_LIMITATIONS":
            self.assertIn("SEC-02-2 LIMITATION RESOLUTION V1", route)
        else:
            self.assertNotIn("SECTION DRAFTING CONTRACT V1", route)

    def test_manifest_reports_every_required_number(self):
        for key in ("total_candidate_claims", "allowlisted_claims", "denylisted_claims",
                    "required_topics_covered", "critical_limitations",
                    "important_non_blocking_limitations", "optional_limitations",
                    "numeric_unresolved", "context_differences", "unsafe_syntheses",
                    "generation_calls", "retrieval_calls"):
            self.assertIn(key, self.manifest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
