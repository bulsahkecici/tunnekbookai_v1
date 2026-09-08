"""Tests for SEC-02-2 Limitation Resolution v1.

These assert the contract and its enforcement rather than the verdict. A run that reached
READY_FOR_DRAFT by loosening a rule would fail here; a run that honestly stayed
READY_WITH_LIMITATIONS would pass, because what the suite checks is that whatever readiness is
reported is the one the rules and the regression suite actually produce.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "book" / "sec_02_2_limitation_resolution"
CLOSURE = ROOT / "data" / "book" / "sec_02_2_readiness_closure"
MANIFEST = ROOT / "data" / "book" / "manifests" / "sec_02_2_limitation_resolution_v1.json"
REPORT = ROOT / "reports" / "sec_02_2_limitation_resolution_v1.md"
FIXTURES = ROOT / "data" / "evaluation" / "sec_02_2_claim_composition_v1.jsonl"

REQUIRED_TOPICS = ("çimento dozajı", "kaplama kalınlığı", "dayanım sınıfı")
MATERIAL_SCOPES = {"general_concrete", "shotcrete", "dry_system_shotcrete",
                   "wet_system_shotcrete", "initial_shotcrete_lining", "steel_fibre_shotcrete",
                   "steel_mesh", "flashcrete"}
REQUIREMENT_SCOPES = {"maximum", "minimum", "typical_range", "recommended", "mandatory",
                      "design_table", "project_specific", "case_specific"}
RELATIONSHIP_TYPES = {"INDEPENDENT", "SAME_SCOPE_SUPPORT", "QUALIFIED_COMPARISON",
                      "SOURCE_SUPPORTED_RELATION", "FORBIDDEN_SYNTHESIS", "UNKNOWN_RELATION"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


class ResolutionArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_json(MANIFEST)
        cls.contract = load_json(
            OUT / "contracts" / "sec_02_2_claim_composition_contract_v1.json")
        cls.allowlist = load_jsonl(OUT / "claims" / "composition_safe_allowlist_v1.jsonl")
        cls.denylist = load_jsonl(OUT / "claims" / "composition_denylist_v1.jsonl")
        cls.pairs = load_jsonl(OUT / "claims" / "claim_pair_constraints_v1.jsonl")
        cls.regression = load_json(OUT / "audits" / "composition_regression_v1.json")
        cls.topics = load_json(
            OUT / "audits" / "required_topic_coverage_after_constraints_v1.json")
        cls.consistency = load_json(OUT / "audits" / "p0_manifest_consistency_carried_v1.json")
        cls.bundle = load_json(OUT / "bundle" / "sec_02_2_drafting_safety_bundle_v1.json")
        cls.fixtures = load_jsonl(FIXTURES)
        cls.closure_allowlist = load_jsonl(
            CLOSURE / "claims" / "draft_claim_allowlist_v1.jsonl")


# ---------------------------------------------------------------- the contract

class TestCompositionContract(ResolutionArtifacts):
    def test_contract_states_the_core_principle(self):
        principle = self.contract["core_principle"]
        for token in ("therefore", "although", "contradicts", "exception"):
            self.assertIn(token, principle)

    def test_every_allowlisted_claim_has_an_authored_scope(self):
        scoped = {row["claim_id"] for row in self.contract["claim_scopes"]}
        for claim in self.closure_allowlist:
            self.assertIn(claim["claim_id"], scoped)

    def test_every_scope_uses_the_declared_vocabulary(self):
        for scope in self.contract["claim_scopes"]:
            self.assertIn(scope["material_scope"], MATERIAL_SCOPES, scope["claim_id"])
            self.assertTrue(scope["requirement_scope"], scope["claim_id"])
            for requirement in scope["requirement_scope"]:
                self.assertIn(requirement, REQUIREMENT_SCOPES, scope["claim_id"])

    def test_every_scope_records_the_evidence_that_establishes_it(self):
        """Rule 8: do not infer scope if evidence does not establish it. A scope with no stated
        reason is an inference."""
        for scope in self.contract["claim_scopes"]:
            self.assertTrue(scope["scope_evidence"].strip(), scope["claim_id"])
            self.assertGreater(len(scope["scope_evidence"]), 40, scope["claim_id"])

    def test_cf_p0_001_scope_binding_is_encoded_exactly(self):
        by_id = {row["claim_id"]: row for row in self.contract["claim_scopes"]}
        self.assertEqual(by_id["SEC-02-2-P0-002"]["material_scope"], "general_concrete")
        self.assertIn("maximum", by_id["SEC-02-2-P0-002"]["requirement_scope"])
        self.assertEqual(by_id["SEC-02-2-R001"]["material_scope"], "dry_system_shotcrete")
        self.assertIn("minimum", by_id["SEC-02-2-R001"]["requirement_scope"])
        self.assertEqual(by_id["SEC-02-2-P0-001"]["material_scope"], "wet_system_shotcrete")
        self.assertIn("minimum", by_id["SEC-02-2-P0-001"]["requirement_scope"])

    def test_the_360_condition_is_recorded(self):
        by_id = {row["claim_id"]: row for row in self.contract["claim_scopes"]}
        self.assertIn("yüksek dayanımlı beton dışında", by_id["SEC-02-2-P0-002"]["conditions"])

    def test_exposure_class_is_not_a_general_concrete_marker(self):
        """It occurs in Tablo-308-23-b's title and in SEC-02-2-P0-005, a shotcrete claim, so it
        cannot discriminate between the two materials."""
        markers = " ".join(self.contract["scope_markers"]["general_concrete"]).lower()
        self.assertNotIn("etki sınıf", markers)
        self.assertNotIn("exposure class", markers)

    def test_negation_handling_is_declared_with_its_reason(self):
        self.assertTrue(self.contract["negation_markers"])
        self.assertIn("değildir", self.contract["negation_markers"])
        self.assertIn("püskürtme beton şartnamesi değildir",
                      self.contract["negation_rationale"])

    def test_contract_declares_determinism_and_fail_closed(self):
        self.assertIn("No LLM judge", self.contract["determinism"])
        self.assertIn("fail_closed", self.contract["failure_mode"])

    def test_contract_is_scoped_to_this_section(self):
        self.assertIn("SEC-02-2 only", self.contract["scope"])


# ---------------------------------------------------------------- rules

class TestRules(ResolutionArtifacts):
    def test_cf_p0_001_has_a_blocking_qualifier_rule(self):
        rules = [r for r in self.contract["mandatory_qualifier_rules"]
                 if r["origin_limitation"] == "CF-P0-001"]
        self.assertTrue(rules)
        for rule in rules:
            self.assertEqual(rule["severity"], "BLOCKING")

    def test_the_360_rule_forbids_both_bare_and_shotcrete_forms(self):
        rule = next(r for r in self.contract["mandatory_qualifier_rules"]
                    if r["claim_id"] == "SEC-02-2-P0-002")
        self.assertTrue(rule["enforce_unqualified"])
        self.assertIn("shotcrete", rule["forbidden_scopes"])
        self.assertIn("360", rule["forbidden_unqualified_form"])

    def test_mirror_rules_exist_for_the_shotcrete_minimums(self):
        for claim_id in ("SEC-02-2-R001", "SEC-02-2-P0-001"):
            rule = next(r for r in self.contract["mandatory_qualifier_rules"]
                        if r["claim_id"] == claim_id)
            self.assertIn("general_concrete", rule["forbidden_scopes"])
            self.assertFalse(rule["enforce_unqualified"],
                             "a bare shotcrete minimum inside a shotcrete section is terse, not "
                             "misleading; enforcing it would reject P0-005's own wording")

    def test_syn_001_has_a_blocking_rule_with_the_safe_representation(self):
        rule = next(r for r in self.contract["forbidden_synthesis_rules"]
                    if r["synthesis_id"] == "SYN-001")
        self.assertEqual(rule["severity"], "BLOCKING")
        self.assertEqual(rule["safe_representation"], "SEPARATE_SUPPORTED_CLAIMS")
        self.assertTrue(rule["forbidden_patterns"])
        self.assertEqual(len(rule["forbidden_patterns"]), len(rule["pattern_intent"]))

    def test_syn_001_components_are_all_allowlisted_separately(self):
        rule = next(r for r in self.contract["forbidden_synthesis_rules"]
                    if r["synthesis_id"] == "SYN-001")
        allowed = {row["claim_id"] for row in self.allowlist}
        for component in rule["component_claim_ids"]:
            self.assertIn(component, allowed)

    def test_derived_numeric_rule_pins_15cm_as_source_and_150mm_as_derived(self):
        rule = next(r for r in self.contract["derived_numeric_rules"]
                    if r["claim_id"] == "SEC-02-2-C-003")
        self.assertEqual((rule["source_value"], rule["source_unit"]), ("15", "cm"))
        self.assertEqual((rule["derived_value"], rule["derived_unit"]), ("150", "mm"))
        self.assertTrue(rule["derived"])
        self.assertFalse(rule["source_stated"])
        self.assertEqual(rule["drafting_policy"], "SOURCE_STATED_ONLY")
        self.assertEqual(rule["severity"], "BLOCKING")

    def test_derived_rule_exempts_the_source_stated_clay_zone_figure(self):
        rule = next(r for r in self.contract["derived_numeric_rules"]
                    if r["claim_id"] == "SEC-02-2-C-003")
        self.assertTrue(rule["exempt_context_markers"])
        self.assertIn("SEC-02-2-C-009", rule["exemption_reason"])

    def test_default_derived_policy_keeps_150mm_out_of_the_allowlist(self):
        self.assertEqual(self.contract["derived_numeric_default_policy"], "SOURCE_STATED_ONLY")
        for row in self.allowlist:
            for numeric in row["numeric"]:
                if numeric.get("unit") == "mm" and numeric.get("value") == "150":
                    self.assertEqual(row["claim_id"], "SEC-02-2-C-009")
                    self.assertTrue(numeric["source_stated"])
                    self.assertFalse(numeric["derived"])


# ---------------------------------------------------------------- 33/34/35/36: pairs

class TestPairConstraints(ResolutionArtifacts):
    def test_every_pair_uses_a_declared_relationship_type(self):
        for pair in self.pairs:
            self.assertIn(pair["relationship_policy"], RELATIONSHIP_TYPES)

    def test_360_versus_350_and_400_forbid_the_same_sentence(self):
        for right in ("SEC-02-2-R001", "SEC-02-2-P0-001"):
            pair = next(p for p in self.pairs
                        if {p["left_claim_id"], p["right_claim_id"]}
                        == {"SEC-02-2-P0-002", right})
            self.assertEqual(pair["relationship_policy"], "INDEPENDENT")
            self.assertFalse(pair["allowed_same_sentence"])
            self.assertTrue(pair["allowed_same_paragraph"])
            self.assertTrue(pair["required_qualifiers"])

    def test_350_versus_400_is_a_source_supported_comparison(self):
        pair = next(p for p in self.pairs
                    if {p["left_claim_id"], p["right_claim_id"]}
                    == {"SEC-02-2-R001", "SEC-02-2-P0-001"})
        self.assertEqual(pair["relationship_policy"], "SOURCE_SUPPORTED_RELATION")
        self.assertTrue(pair["allowed_same_sentence"])

    def test_every_pair_is_deterministic(self):
        for pair in self.pairs:
            self.assertFalse(pair["manual_review_required"], pair["constraint_id"])

    def test_every_pair_states_a_reason_and_an_action(self):
        for pair in self.pairs:
            self.assertGreater(len(pair["reason"]), 40, pair["constraint_id"])
            self.assertTrue(pair["required_action"], pair["constraint_id"])


# ---------------------------------------------------------------- 27/28/29/30/31: lists

class TestCompositionLists(ResolutionArtifacts):
    def test_allowlist_carries_every_required_field(self):
        required = ("claim_id", "canonical_claim", "topic", "scope", "conditions", "qualifiers",
                    "source_keys", "citation_ready", "composition_safe",
                    "mandatory_qualifier_rule_ids", "forbidden_synthesis_rule_ids",
                    "derived_numeric_rule_ids", "allowed_relationships",
                    "forbidden_relationships")
        for row in self.allowlist:
            for field in required:
                self.assertIn(field, row, row["claim_id"])

    def test_no_claim_was_lost_between_evidence_and_composition(self):
        """A constrained claim is still draftable. Losing one silently would shrink the section
        without anyone deciding to."""
        self.assertEqual({row["claim_id"] for row in self.allowlist},
                         {row["claim_id"] for row in self.closure_allowlist})

    def test_every_allowlisted_claim_is_composition_safe_and_cited(self):
        for row in self.allowlist:
            self.assertTrue(row["composition_safe"], row["claim_id"])
            self.assertTrue(row["citation_ready"], row["claim_id"])
            self.assertTrue(row["source_keys"], row["claim_id"])

    def test_claim_wording_was_not_rewritten(self):
        """Rule 29: do not rewrite claim wording merely to make composition easier."""
        original = {row["claim_id"]: row["canonical_claim"] for row in self.closure_allowlist}
        for row in self.allowlist:
            if row.get("parent_claim_id"):
                self.assertTrue(row["narrowing_reason"])
                self.assertTrue(row["scope_preserved"])
                self.assertTrue(row["support_preserved"])
            else:
                self.assertEqual(row["canonical_claim"], original[row["claim_id"]],
                                 row["claim_id"])

    def test_restricted_claims_carry_their_rules(self):
        rule_bearing = {"SEC-02-2-P0-002", "SEC-02-2-R001", "SEC-02-2-P0-001"}
        for row in self.allowlist:
            if row["claim_id"] in rule_bearing:
                self.assertTrue(row["mandatory_qualifier_rule_ids"], row["claim_id"])
        c003 = next(r for r in self.allowlist if r["claim_id"] == "SEC-02-2-C-003")
        self.assertIn("DN-001", c003["derived_numeric_rule_ids"])

    def test_the_360_claim_keeps_its_mandatory_qualifier_as_a_field(self):
        row = next(r for r in self.allowlist if r["claim_id"] == "SEC-02-2-P0-002")
        self.assertTrue(row["qualifiers"])
        self.assertIn("GENEL beton", row["qualifiers"][0])

    def test_denylist_covers_both_layers(self):
        layers = {row.get("deny_layer") for row in self.denylist}
        self.assertIn("evidence", layers)
        self.assertIn("composition", layers)

    def test_denylist_includes_the_required_composition_forms(self):
        ids = {row["claim_id"] for row in self.denylist}
        for required in ("SEC-02-2-DENY-COMP-SYN-001-COMPOUND",
                         "SEC-02-2-DENY-COMP-360-UNQUALIFIED",
                         "SEC-02-2-DENY-COMP-360-AS-SHOTCRETE",
                         "SEC-02-2-DENY-COMP-350-AS-GENERAL",
                         "SEC-02-2-DENY-COMP-CEMENT-RANGE",
                         "SEC-02-2-DENY-COMP-150MM-SOURCE-STATED"):
            self.assertIn(required, ids)

    def test_every_composition_denial_names_the_rule_that_enforces_it(self):
        for row in self.denylist:
            if row.get("deny_layer") == "composition":
                self.assertTrue(row.get("enforced_by"), row["claim_id"])

    def test_allowlist_and_denylist_are_disjoint(self):
        self.assertEqual({row["claim_id"] for row in self.allowlist}
                         & {row["claim_id"] for row in self.denylist}, set())


# ---------------------------------------------------------------- 44-47/78: fixtures

class TestRegressionSuite(ResolutionArtifacts):
    def test_at_least_sixty_cases(self):
        self.assertGreaterEqual(len(self.fixtures), 60)

    def test_both_polarities_are_well_represented(self):
        positive = [f for f in self.fixtures if f["expected_valid"]]
        negative = [f for f in self.fixtures if not f["expected_valid"]]
        self.assertGreaterEqual(len(positive), 20)
        self.assertGreaterEqual(len(negative), 20)

    def test_zero_false_accepts_and_false_rejects(self):
        self.assertEqual(self.regression["false_accepts"], [])
        self.assertEqual(self.regression["false_rejects"], [])
        self.assertEqual(self.regression["code_mismatches"], [])
        self.assertTrue(self.regression["all_pass"])

    def test_language_coverage_includes_english_connectors(self):
        languages = {f["language"] for f in self.fixtures}
        self.assertIn("tr", languages)
        self.assertIn("en", languages)

    def test_every_fixture_is_marked_synthetic(self):
        for fixture in self.fixtures:
            self.assertTrue(fixture["synthetic"], fixture["case_id"])
            self.assertTrue(fixture["tests"], fixture["case_id"])

    def test_historical_defects_are_all_caught(self):
        rows = {row["case_id"]: row for row in self.regression["rows"]}
        for case_id in ("NEG-360-01", "NEG-360-03", "NEG-SYN-01", "NEG-SYN-05", "NEG-SYN-08",
                        "NEG-SYN-11", "NEG-150MM-01", "NEG-150MM-02"):
            self.assertIn(case_id, rows)
            self.assertFalse(rows[case_id]["actual_valid"], case_id)
            self.assertEqual(rows[case_id]["outcome"], "PASS", case_id)

    def test_safe_arrangements_are_all_accepted(self):
        rows = {row["case_id"]: row for row in self.regression["rows"]}
        for case_id in ("POS-360-03", "POS-350-400-01", "POS-PARA-01", "POS-PARA-02",
                        "POS-150MM-EXEMPT-01", "POS-LINING-01", "POS-MESH-02"):
            self.assertIn(case_id, rows)
            self.assertTrue(rows[case_id]["actual_valid"], case_id)

    def test_fixture_citation_keys_match_the_claims_they_cite(self):
        keys = {row["claim_id"]: set(row["source_keys"]) for row in self.allowlist}
        for fixture in self.fixtures:
            if fixture["case_id"] in ("NEG-CIT-01", "NEG-CIT-02"):
                continue
            for claim_id, cited in fixture["citation_keys"].items():
                if claim_id in keys and cited:
                    self.assertTrue(set(cited) & keys[claim_id], fixture["case_id"])


# ---------------------------------------------------------------- 74: topics

class TestRequiredTopics(ResolutionArtifacts):
    def test_all_three_topics_are_present(self):
        self.assertEqual({row["topic"] for row in self.topics}, set(REQUIRED_TOPICS))

    def test_composition_removed_no_topic_support(self):
        for row in self.topics:
            self.assertNotEqual(row["coverage_status"], "INCOMPLETE", row["topic"])
            self.assertEqual(row["dropped_by_composition"], [], row["topic"])
            self.assertTrue(row["required_core_claim_ids"], row["topic"])

    def test_topic_core_claims_are_all_composition_safe(self):
        safe = {row["claim_id"] for row in self.allowlist if row["composition_safe"]}
        for row in self.topics:
            for claim_id in row["required_core_claim_ids"]:
                self.assertIn(claim_id, safe)


# ---------------------------------------------------------------- 52-55: readiness

class TestFinalReadiness(ResolutionArtifacts):
    def test_readiness_is_from_the_allowed_vocabulary(self):
        self.assertIn(self.manifest["final_readiness"],
                      {"READY_FOR_DRAFT", "READY_WITH_LIMITATIONS", "NOT_READY"})

    def test_ready_for_draft_implies_the_whole_contract_holds(self):
        if self.manifest["final_readiness"] != "READY_FOR_DRAFT":
            self.skipTest("section is not READY_FOR_DRAFT")
        self.assertEqual(self.manifest["required_topics_covered"], 3)
        self.assertEqual(self.manifest["false_accepts"], 0)
        self.assertEqual(self.manifest["false_rejects"], 0)
        self.assertEqual(self.manifest["readiness_blocking_reasons"], [])
        self.assertEqual(self.manifest["remaining_non_enforceable_limitations"], [])
        self.assertTrue(self.manifest["go_conditions"]["allowlist_denylist_disjoint"])
        self.assertTrue(self.manifest["go_conditions"]["pair_constraints_deterministic"])

    def test_ready_for_draft_requires_all_three_limitations_enforced(self):
        if self.manifest["final_readiness"] != "READY_FOR_DRAFT":
            self.skipTest("section is not READY_FOR_DRAFT")
        resolved = " ".join(self.manifest["resolved_composition_limitations"])
        for token in ("CF-P0-001", "SYN-001", "150 mm"):
            self.assertIn(token, resolved)

    def test_not_ready_states_blocking_reasons(self):
        if self.manifest["final_readiness"] != "NOT_READY":
            self.skipTest("section is not NOT_READY")
        self.assertTrue(self.manifest["readiness_blocking_reasons"])

    def test_p0_did_not_regress(self):
        parent = load_json(CLOSURE / "bundle" / "SEC-02-2.json")["readiness_assessment"]
        for status in parent["p0_status"].values():
            self.assertEqual(status, "RESOLVED")

    def test_drafting_is_not_authorized_regardless_of_readiness(self):
        """Rule 51. Even at READY_FOR_DRAFT, authorisation belongs to the next phase."""
        self.assertFalse(self.manifest["drafting_authorized"])
        self.assertFalse(self.manifest["drafting_enabled"])
        self.assertFalse(self.bundle["drafting_authorized"])
        self.assertFalse(self.bundle["drafting_enabled"])

    def test_bundle_and_manifest_agree(self):
        self.assertEqual(self.bundle["final_readiness"], self.manifest["final_readiness"])


# ---------------------------------------------------------------- 50: safety bundle

class TestSafetyBundle(ResolutionArtifacts):
    def test_bundle_carries_every_required_field(self):
        for field in ("section_id", "parent_readiness_bundle_sha",
                      "composition_contract_version", "composition_validator_version",
                      "allowlist_sha", "denylist_sha", "pair_constraints_sha",
                      "qualifier_rules", "forbidden_synthesis_rules", "derived_numeric_rules",
                      "remaining_limitations", "final_readiness", "drafting_authorized"):
            self.assertIn(field, self.bundle)

    def test_bundle_shas_match_the_files_on_disk(self):
        import hashlib

        def sha(path: Path) -> str:
            return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()

        self.assertEqual(self.bundle["allowlist_sha"],
                         sha(OUT / "claims" / "composition_safe_allowlist_v1.jsonl"))
        self.assertEqual(self.bundle["denylist_sha"],
                         sha(OUT / "claims" / "composition_denylist_v1.jsonl"))
        self.assertEqual(self.bundle["pair_constraints_sha"],
                         sha(OUT / "claims" / "claim_pair_constraints_v1.jsonl"))

    def test_bundle_points_at_the_parent_readiness_bundle(self):
        parent = load_json(CLOSURE / "bundle" / "SEC-02-2.json")
        self.assertEqual(self.bundle["parent_readiness_bundle_sha"], parent["bundle_sha"])


# ---------------------------------------------------------------- 56/57: integrity

class TestFrozenIntegrity(ResolutionArtifacts):
    def test_all_frozen_inputs_are_byte_identical(self):
        self.assertTrue(self.manifest["frozen_integrity"]["all_unchanged"],
                        self.manifest["frozen_integrity"]["changed"])

    def test_the_named_frozen_components_are_checked(self):
        names = " ".join(c["name"] for c in self.manifest["frozen_integrity"]["checks"])
        for component in ("Retriever v1", "Prompt v5", "Output Contract v1.1",
                          "Production Grounded Generator v1", "Book Pipeline Extractor v1.1",
                          "P0 Evidence Gap Resolution v1",
                          "SEC-02-2 Draft Readiness Closure v1", "source registry v1",
                          "corpus chunks"):
            self.assertIn(component, names)

    def test_every_closure_artifact_is_checked(self):
        paths = {c["path"] for c in self.manifest["frozen_integrity"]["checks"]}
        closure_manifest = load_json(
            ROOT / "data" / "book" / "manifests" / "sec_02_2_draft_readiness_closure_v1.json")
        for relative in closure_manifest["artifact_shas"]:
            self.assertIn(f"data/book/sec_02_2_readiness_closure/{relative}", paths)

    def test_all_three_source_registries_are_untouched(self):
        checks = {c["path"]: c for c in self.manifest["frozen_integrity"]["checks"]}
        for path in ("data/book/source_registry_v1.jsonl",
                     "data/book/p0_resolution/evidence/p0_source_registry_v1.jsonl",
                     "data/book/sec_02_2_readiness_closure/evidence/"
                     "closure_source_registry_v1.jsonl"):
            self.assertIn(path, checks)
            self.assertTrue(checks[path]["unchanged"], path)

    def test_manifest_consistency_is_carried_not_recomputed(self):
        carried = load_json(CLOSURE / "audits" / "p0_manifest_consistency_v1.json")
        self.assertEqual(self.consistency["canonical_value"], carried["canonical_value"])
        self.assertEqual(self.consistency["carried_from"],
                         "tunnelbook-sec-02-2-draft-readiness-closure-v1")
        self.assertFalse(self.consistency["historical_artifacts_modified"])

    def test_no_generation_no_retrieval_no_qdrant_writes(self):
        self.assertEqual(self.manifest["generation_calls"], 0)
        self.assertEqual(self.manifest["retrieval_calls"], 0)
        self.assertEqual(self.manifest["qdrant_writes"], 0)
        self.assertEqual(self.manifest["qdrant_points_before"],
                         self.manifest["qdrant_points_after"])
        if self.manifest["qdrant_reachable"]:
            self.assertEqual(self.manifest["qdrant_points_before"],
                             self.manifest["qdrant_expected"])
        else:
            self.assertIsNone(self.manifest["qdrant_points_before"])
            self.assertIn("not reachable", self.manifest["qdrant_note"])


# ---------------------------------------------------------------- 43/75: no prose

class TestNoProse(ResolutionArtifacts):
    def test_no_manuscript_artifact_exists(self):
        for candidate in ("manuscript", "drafts", "sections_drafted"):
            self.assertFalse((ROOT / "data" / "book" / candidate).exists(), candidate)

    def test_fixtures_are_not_stored_as_section_content(self):
        for path in OUT.rglob("*"):
            if path.is_file():
                self.assertNotIn("manuscript", path.name)
                self.assertNotIn("prose", path.name)

    def test_allowlist_rows_are_claims_not_paragraphs(self):
        for row in self.allowlist:
            self.assertLess(len(row["canonical_claim"]), 400, row["claim_id"])
            self.assertNotIn("\n", row["canonical_claim"])


# ---------------------------------------------------------------- 76/77: report

class TestReport(ResolutionArtifacts):
    def test_report_has_every_required_section(self):
        text = REPORT.read_text(encoding="utf-8")
        for heading in ("# SEC-02-2 Limitation Resolution v1", "## Executive Decision",
                        "## Why Composition Needed Its Own Gate", "## Frozen Inputs",
                        "## CF-P0-001", "## Scope Binding", "## Mandatory Qualifiers",
                        "## SYN-001", "## Forbidden Synthesis Rules", "## Derived Numeric Rule",
                        "## Composition-Safe Allowlist", "## Composition Denylist",
                        "## Claim Pair Constraints", "## Composition Validator",
                        "## Regression Fixtures",
                        "## Required Topic Coverage After Constraints",
                        "## Remaining Limitations", "## Frozen Integrity", "## Tests",
                        "## Final Readiness", "## Next Phase"):
            self.assertIn(heading, text)

    def test_manifest_reports_every_required_metric(self):
        for key in ("input_allowlist_claims", "composition_safe_allowlist_claims",
                    "composition_denylist_claims", "mandatory_qualifier_rules",
                    "forbidden_synthesis_rules", "claim_pair_constraints",
                    "derived_numeric_rules", "fixture_count", "positive_fixtures",
                    "negative_fixtures", "false_accepts", "false_rejects",
                    "required_topics_covered", "generation_calls", "retrieval_calls"):
            self.assertIn(key, self.manifest)

    def test_next_phase_matches_the_verdict(self):
        route = self.manifest["next_phase"]["route"]
        readiness = self.manifest["final_readiness"]
        if readiness == "READY_FOR_DRAFT":
            self.assertIn("SECTION DRAFTING CONTRACT V1", route)
            self.assertIn("BOOK CITATION RENDERING CONTRACT V1", route)
        else:
            self.assertNotIn("SECTION DRAFTING CONTRACT V1", route)


if __name__ == "__main__":
    unittest.main(verbosity=2)
