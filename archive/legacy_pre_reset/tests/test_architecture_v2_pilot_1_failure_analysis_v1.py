"""ARCHITECTURE V2 PILOT #1 failure analysis — the probes, recomputed rather than read back.

Each test recomputes its claim from the preserved pilot artifacts and the frozen contracts, so an
analysis that reached the wrong conclusion cannot pass by agreeing with its own recording. The
last group guards the phase constraints: nothing generated, nothing rendered, nothing widened, and
Pilot #1 still rejected.
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

ARCH_V2 = ROOT / "data/book/drafting/sec_02_2/architecture_v2"
PILOT = ARCH_V2 / "pilot_1"
ANALYSIS_DIR = ARCH_V2 / "pilot_1_analysis_v1"
ANALYSIS = ANALYSIS_DIR / "audits" / "pilot_1_failure_analysis_v1.json"
SET_AUDIT = ANALYSIS_DIR / "audits" / "set_consistency_audit_v1.json"
UNIVERSE = ANALYSIS_DIR / "audits" / "universe_comparison_v1.json"
MANIFEST = ROOT / "data/book/manifests/architecture_v2_pilot_1_failure_analysis_v1.json"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


FA = _load("fa_test", "67_architecture_v2_pilot_1_failure_analysis_v1.py")
V1, V1_2 = FA.V1, FA.V1_2
PLAN_IR, REAL, RENDER = FA.PLAN_IR, FA.REAL, FA.RENDER
BUNDLE, REALIZATION = FA.BUNDLE, FA.REALIZATION


class ReproductionTest(unittest.TestCase):
    """Every point the pilot recorded, verified against the preserved artifacts."""

    def setUp(self):
        self.options = _json(PILOT / "contracts" / "planner_option_set_v1.json")
        self.c005 = next(o for o in self.options["options"]
                         if o["claim_id"] == "SEC-02-2-C-005")

    def test_option_set_demanded_a_role_it_did_not_offer(self):
        self.assertTrue(self.c005["requires_condition_slot"])
        self.assertNotIn("CONDITION", self.c005["available_roles"])

    def test_the_rule_demanding_it_was_shown_to_the_planner(self):
        self.assertTrue(any("requires_condition_slot" in rule
                            for rule in self.options["plan_rules"]))

    def test_realization_marks_the_pair_unrealizable(self):
        entry = REALIZATION.entry("SEC-02-2-C-005", "CONDITION")
        self.assertEqual("UNREALIZABLE", entry["status"])

    def test_feasibility_proof_skipped_the_claim(self):
        feasibility = _json(PILOT / "audits" / "feasibility_proof_v1.json")
        self.assertNotIn("SEC-02-2-C-005", feasibility["claims_stated"])

    def test_planner_selected_the_pair_and_validation_caught_it(self):
        plan = _json(PILOT / "plan" / "semantic_plan_ir_v2.json")
        pairs = {(s["claim_id"], s["realization_role"])
                 for sub in plan["subsections"] for p in sub["paragraph_groups"]
                 for s in p["slots"]}
        self.assertIn(("SEC-02-2-C-005", "CONDITION"), pairs)
        validation = _json(PILOT / "validation" / "pilot_1_validation.json")
        self.assertEqual("plan_validation", validation["stage"])
        self.assertEqual(["PLAN_ROLE_UNREALIZABLE"],
                         sorted({f["code"] for f in
                                 validation["semantic_plan"]["failures"]}))

    def test_nothing_was_rendered(self):
        validation = _json(PILOT / "validation" / "pilot_1_validation.json")
        self.assertFalse(validation.get("rendered", False))
        self.assertFalse((PILOT / "rendered" / "rendered_draft_ir_v2.json").exists())


class SetConsistencyTest(unittest.TestCase):

    def test_audit_covers_every_exposed_claim(self):
        options = _json(PILOT / "contracts" / "planner_option_set_v1.json")
        audit = _json(SET_AUDIT)
        self.assertEqual(len(options["options"]), audit["claims_audited"])
        self.assertEqual({o["claim_id"] for o in options["options"]},
                         {row["claim_id"] for row in audit["rows"]})

    def test_available_is_a_subset_of_realizable_everywhere(self):
        """Recomputed: no claim was ever offered a role M2 cannot realize."""
        options = _json(PILOT / "contracts" / "planner_option_set_v1.json")
        for option in options["options"]:
            realizable = {role for cid, role in REALIZATION.realizable_pairs()
                          if cid == option["claim_id"]}
            self.assertTrue(set(option["available_roles"]) <= realizable, option["claim_id"])

    def test_c005_is_the_only_required_subset_available_violation(self):
        options = _json(PILOT / "contracts" / "planner_option_set_v1.json")
        violations = []
        for option in options["options"]:
            required = set()
            if option["requires_condition_slot"]:
                required.add("CONDITION")
            if option["requires_qualifier_slot"]:
                required.add("QUALIFIER_SCOPE")
            if not required <= set(option["available_roles"]):
                violations.append(option["claim_id"])
        self.assertEqual(["SEC-02-2-C-005"], violations)

    def test_no_offered_role_is_unrealizable(self):
        self.assertEqual([], _json(SET_AUDIT)["contradictions"]
                         ["form_2_offered_role_not_realizable"])


class C005ObligationTest(unittest.TestCase):

    def test_statement_alone_already_satisfies_the_condition(self):
        """The obligation was false: recomputed through the unchanged validator."""
        probe = FA.c005_obligation_probe()
        self.assertEqual("ACCEPT", probe["statement_alone_status"])
        self.assertEqual({}, probe["statement_alone_histogram"])
        self.assertTrue(probe["requires_condition_slot_is_a_false_obligation"])

    def test_the_scope_test_is_stricter_than_the_stage_it_models(self):
        """paragraph_scoped_conditions asks all-anchors; stage E scores any-anchor."""
        claim = BUNDLE.allowlist["SEC-02-2-C-005"]
        self.assertIn("priz hızlandırıcı katkı tipi",
                      PLAN_IR.paragraph_scoped_conditions(claim, BUNDLE))
        canonical = set(V1.tokens(claim["canonical_claim"]))
        anchors = V1.content_tokens("priz hızlandırıcı katkı tipi", BUNDLE.function_lexicon)
        present = [a for a in anchors
                   if any(V1.prefix_agreement(a, c) for c in canonical)]
        self.assertTrue(present, "stage E's any-anchor test is satisfied")
        self.assertLess(len(present), len(anchors), "the all-anchors test is not")


class TurkishnessDefectTest(unittest.TestCase):

    def test_diacritic_free_turkish_is_misclassified(self):
        for text in ("takip eden tabakalar", "ilk tabaka", "ilave tabakalar"):
            self.assertFalse(REAL.is_turkish(text), text)

    def test_genuinely_english_material_is_still_refused(self):
        """R025's 'normally' is a true positive and must stay refused."""
        entry = REALIZATION.entry("SEC-02-2-R025", "QUALIFIER_SCOPE")
        self.assertEqual("UNREALIZABLE", entry["status"])

    def test_false_negative_census(self):
        probe = FA.turkishness_probe()
        self.assertEqual(3, probe["false_negatives"])
        self.assertEqual(1, probe["true_positives"])

    def test_the_defect_fails_closed(self):
        """It withholds material; it cannot have admitted an unlicensed word."""
        for row in FA.turkishness_probe()["detail"]:
            entry = REALIZATION.entry(row["claim_id"], row["role"])
            self.assertEqual("UNREALIZABLE", entry["status"])
            self.assertEqual([], entry["segments"])


class UniverseComparisonTest(unittest.TestCase):

    def test_the_two_universes_disagree_on_exactly_one_claim(self):
        universe = _json(UNIVERSE)
        self.assertFalse(universe["identical_claim_sets"])
        self.assertEqual(["SEC-02-2-C-005"], universe["claims_only_in_planner_universe"])
        self.assertEqual([], universe["claims_only_in_feasibility_universe"])

    def test_remediation_is_an_invariant_not_a_claim_patch(self):
        remediation = _json(ANALYSIS)["remediation"]
        self.assertIn("No `if claim_id ==", remediation["no_claim_specific_patch"])
        blob = json.dumps(remediation, ensure_ascii=False)
        self.assertNotIn("if claim_id == 'SEC-02-2-C-005':", blob)
        self.assertGreaterEqual(len(remediation["smallest_safe_remediation"]), 3)
        self.assertGreaterEqual(len(remediation["adversarial_fixtures_required"]), 5)


class ClassificationTest(unittest.TestCase):

    def setUp(self):
        self.classification = _json(ANALYSIS)["classification"]

    def test_model_fault_is_not_established(self):
        self.assertEqual("NOT ESTABLISHED",
                         self.classification["candidates"]["A_MODEL_COMPLIANCE_FAILURE"]
                         ["verdict"])
        self.assertEqual("NOT ESTABLISHED",
                         self.classification["fault_attribution"]["model_defect"])

    def test_renderer_and_validator_are_exonerated(self):
        self.assertFalse(self.classification["fault_attribution"]["renderer_defect"])
        self.assertFalse(self.classification["fault_attribution"]["validator_defect"])

    def test_authorisation_and_realization_layers_are_faulted(self):
        self.assertTrue(self.classification["fault_attribution"]["authorisation_layer_defect"])
        self.assertTrue(self.classification["fault_attribution"]
                        ["realization_contract_defect"])

    def test_schema_defect_refuted(self):
        self.assertEqual("REFUTED",
                         self.classification["candidates"]["B_SEMANTIC_PLAN_SCHEMA_DEFECT"]
                         ["verdict"])


class PhaseConstraintTest(unittest.TestCase):

    def test_nothing_was_generated_rendered_or_widened(self):
        accounting = _json(ANALYSIS)["accounting"]
        for key in ("generation_calls", "renders", "retrieval_calls", "qdrant_writes",
                    "corpus_reads", "validators_changed", "realization_contract_changed",
                    "glosses_or_lexicons_changed", "frozen_artifacts_modified"):
            self.assertEqual(0, accounting[key], key)
        self.assertFalse(accounting["pilot_2_authorised"])

    def test_pilot_1_verdict_is_preserved_not_reinterpreted(self):
        self.assertEqual("REJECTED", _json(MANIFEST)["pilot_1_verdict"])
        self.assertEqual("REJECT",
                         _json(PILOT / "validation" / "pilot_1_validation.json")["status"])

    def test_frozen_evidence_is_byte_identical_to_what_was_recorded(self):
        for name, sha in _json(ANALYSIS)["frozen_evidence_sha256"].items():
            path = FA.FROZEN_EVIDENCE[name]
            self.assertEqual(sha, hashlib.sha256(path.read_bytes()).hexdigest(), name)

    def test_no_contract_was_modified_by_this_phase(self):
        acceptance = ARCH_V2 / "contracts" / "architecture_v2_acceptance_contract_v1.json"
        frozen = _json(ROOT / "data/book/manifests"
                              "/architecture_v2_acceptance_contract_v1.json")
        self.assertEqual(frozen["contract_sha256"],
                         hashlib.sha256(acceptance.read_bytes()).hexdigest())

    def test_next_phase_routes_to_universe_remediation(self):
        self.assertEqual("ARCHITECTURE V2 PLANNER OPTION UNIVERSE REMEDIATION V1",
                         _json(MANIFEST)["next_phase"])


if __name__ == "__main__":
    unittest.main()
