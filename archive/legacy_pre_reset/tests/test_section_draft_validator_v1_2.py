"""Section Draft Validator v1.2 - the DF-01 tightening, and what it must not have broken.

Three jobs.

The QV cases pin the new behaviour: DF-01's false pass is closed, the scope-limiting meaning is
accepted when it is actually said, and neither a verbatim canonical copy nor padding built out of
claim vocabulary discharges the qualifier.

The inheritance cases are the tripwires. A tightening is only safe if it is additive, so they
assert that nothing v1.1 rejected is now accepted, that no code was renamed or removed, that no
inherited stage moved, and that scripts/49 and scripts/52 are byte-identical to what analysis v2
hashed. If stage L ever starts answering for a unit that declares no registered claim, the QV-H
cases fail.

The registry cases assert the fail-closed integrity properties, including the general form of
DF-01 itself: an entry whose own canonical claim satisfies its constructions is refused, because
such an entry cannot tell semantic realisation from verbatim reproduction.
"""

from __future__ import annotations

import copy
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
PHASE_DIR = SECTION_DIR / "qualifier_validation_v1"

QUALIFIER_SEMANTICS = PHASE_DIR / "contracts" / "draft_qualifier_semantics_v1.json"
REPRODUCTION = PHASE_DIR / "audits" / "df_01_reproduction_v1.json"
AUDIT = PHASE_DIR / "audits" / "qualifier_validation_tightening_audit_v1.json"
FIXTURE_RESULTS = PHASE_DIR / "fixtures" / "qualifier_semantics_fixture_results_v1.json"
MANIFEST = BOOK / "manifests" / "sec_02_2_qualifier_validation_tightening_v1.json"
REPORT = ROOT / "reports" / "sec_02_2_qualifier_validation_tightening_v1.md"
CONTRACT_V1_2 = DRAFTING / "contracts" / "draft_validation_contract_v1_2.json"
ANALYSIS_V2 = SECTION_DIR / "analysis_v2" / "audits" / "attempt_2_failure_analysis_v1.json"


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


V1 = _load("v1_2_test_validator_v1", "scripts/49_section_draft_validator_v1.py")
V11 = _load("v1_2_test_validator_v1_1", "scripts/52_section_draft_validator_v1_1.py")
V12 = _load("v1_2_test_validator_v1_2", "scripts/54_section_draft_validator_v1_2.py")
PHASE = _load("v1_2_test_phase", "scripts/55_sec_02_2_qualifier_validation_tightening_v1.py")

BUNDLE = V12.load_bundle()
ENTRIES = V12.load_qualifier_semantics()
CONSTRAINTS = V12.load_semantic_constraints()
C009 = BUNDLE.allowlist["SEC-02-2-C-009"]
C009_CANONICAL = C009["canonical_claim"]
SCOPE_UNIT = PHASE.C009_PROBES["C009_scope_unit"]


def unit(unit_id: str, text: str, claim_id: str = "SEC-02-2-C-009"):
    source_keys = list(BUNDLE.allowlist[claim_id]["source_keys"])
    return V1.DraftUnit(
        unit_id=unit_id, unit_type="PARAGRAPH_SENTENCE", text=text, material=True,
        claim_ids=[claim_id], source_keys=source_keys, relationship_type="INDEPENDENT",
        citation_intents=[{"claim_id": claim_id, "source_keys": source_keys}])


def codes(unit_id: str, text: str, paragraph: str, claim_id: str = "SEC-02-2-C-009"):
    return {(f.code, f.stage) for f in V12.validate_unit(
        unit(unit_id, text, claim_id), paragraph, BUNDLE, constraints=CONSTRAINTS,
        qualifier_semantics=ENTRIES)}


class QualifierSemanticsRegressions(unittest.TestCase):
    """QV-A..D. The DF-01 boundary for SEC-02-2-C-009."""

    def test_qv_a_attempt_2_wording_is_now_rejected(self):
        """The frozen DF-01 case, at the wording and paragraph attempt #2 actually produced."""
        reproduction = json.loads(REPRODUCTION.read_text(encoding="utf-8"))
        target = reproduction["target"]
        found = codes("U-D-P01-S03", target["unit_text"], target["paragraph_text"])
        self.assertIn(("QUALIFIER_DROPPED", "L_qualifier_semantics"), found)

    def test_qv_a_was_a_false_pass_under_v1_1(self):
        """Without this, QV-A proves nothing: it has to have passed before."""
        reproduction = json.loads(REPRODUCTION.read_text(encoding="utf-8"))
        target = reproduction["target"]
        self.assertEqual([], target["v1_1_failures"])
        self.assertTrue(target["stage_e_anchor_score"]["stage_e_preserved"])
        self.assertTrue(target["unit_is_verbatim_canonical"])

    def test_qv_b_stating_the_meaning_validates(self):
        paragraph = f"{C009_CANONICAL} {SCOPE_UNIT}"
        self.assertEqual(set(), codes("U-D-P01-S03", C009_CANONICAL, paragraph))
        self.assertEqual(set(), codes("U-D-P01-S04", SCOPE_UNIT, paragraph))

    def test_qv_b_either_construction_alone_suffices(self):
        """A false reject is as much a defect as the false pass being closed.

        Scored at stage L, which is what these probes are about. `C009_non_generality_only` is
        phrased without the clay-zone reference on purpose - to show the non-generality
        construction standing on its own - and v1's condition rule rejects it for that at unit
        scope. That rejection is inherited, correct, and not stage L's to answer for.
        """
        for name in ("C009_exclusivity_only", "C009_non_generality_only"):
            with self.subTest(construction=name):
                probe = PHASE.C009_PROBES[name]
                paragraph = f"{C009_CANONICAL} {probe}"
                self.assertEqual([], V12.stage_l_qualifier_semantics(
                    unit("U-D-P01-S04", probe), paragraph, BUNDLE, ENTRIES))
                self.assertEqual([], V12.stage_l_qualifier_semantics(
                    unit("U-D-P01-S03", C009_CANONICAL), paragraph, BUNDLE, ENTRIES))

    def test_qv_c_canonical_sentence_alone_is_rejected(self):
        found = codes("U-D-P01-S03", C009_CANONICAL, C009_CANONICAL)
        self.assertIn(("QUALIFIER_DROPPED", "L_qualifier_semantics"), found)

    def test_qv_d_lexical_padding_is_rejected(self):
        """Claim vocabulary without the scope meaning. Stage E still scores it preserved."""
        padding = PHASE.C009_PROBES["C009_lexical_padding"]
        paragraph = f"{C009_CANONICAL} {padding}"
        score = PHASE._qualifier_anchor_score(C009, paragraph)
        self.assertTrue(score["stage_e_preserved"], "the probe must still fool stage E")
        self.assertEqual(set(), {(f.code, f.stage) for f in V11.validate_unit(
            unit("U-D-P01-S03", C009_CANONICAL), paragraph, BUNDLE, constraints=CONSTRAINTS)})
        self.assertIn(("QUALIFIER_DROPPED", "L_qualifier_semantics"),
                      codes("U-D-P01-S03", C009_CANONICAL, paragraph))

    def test_qv_d_asserted_generalisation_is_a_scope_mismatch(self):
        generalised = PHASE.C009_PROBES["C009_generalised"]
        found = codes("U-D-P01-S04", generalised, f"{C009_CANONICAL} {generalised}")
        self.assertIn(("SEMANTIC_SCOPE_MISMATCH", "L_qualifier_semantics"), found)

    def test_genellikle_does_not_satisfy_the_generality_group(self):
        """The claim's own 'genellikle' must not read as 'genel', or DF-01 returns."""
        entry = ENTRIES[0]
        self.assertEqual([], V12.realised_constructions(entry, C009_CANONICAL))


class C002BehaviourPreserved(unittest.TestCase):
    """QV-E..F. Stage L must leave DSC-C002-001's boundary exactly where it was."""

    def setUp(self):
        self.c001 = BUNDLE.allowlist["SEC-02-2-C-001"]["canonical_claim"]
        self.c002 = BUNDLE.allowlist["SEC-02-2-C-002"]["canonical_claim"]

    def test_qv_e_historical_bad_form_still_rejected(self):
        found = codes("U-A-P01-S02", self.c002, f"{self.c001} {self.c002}", "SEC-02-2-C-002")
        self.assertIn(("QUALIFIER_DROPPED", "E_conditions"), found)
        self.assertIn(("QUALIFIER_DROPPED", "K_semantic"), found)

    def test_qv_e_forbidden_attribution_still_rejected(self):
        forbidden = PHASE.C002_FORBIDDEN_ATTRIBUTION
        found = codes("U-A-P01-S02", forbidden, f"{self.c001} {forbidden}", "SEC-02-2-C-002")
        self.assertIn(("SEMANTIC_SCOPE_MISMATCH", "K_semantic"), found)

    def test_qv_f_corrected_forms_still_validate(self):
        identity = PHASE.C002_PROBES["C002_identity_unit"]
        combined = PHASE.C002_PROBES["C002_single_unit_combined"]
        split = f"{self.c001} {identity} {self.c002}"
        self.assertEqual(set(), codes("U-A-P01-S02", identity, split, "SEC-02-2-C-002"))
        self.assertEqual(set(), codes("U-A-P01-S03", self.c002, split, "SEC-02-2-C-002"))
        self.assertEqual(set(), codes("U-A-P01-S02", combined, f"{self.c001} {combined}",
                                      "SEC-02-2-C-002"))

    def test_stage_l_is_silent_on_c002(self):
        """C-002 carries no registered qualifier entry; stage L must not answer for it."""
        for text in (self.c002, PHASE.C002_PROBES["C002_identity_unit"]):
            with self.subTest(text=text[:40]):
                self.assertEqual([], V12.stage_l_qualifier_semantics(
                    unit("U-A-P01-S02", text, "SEC-02-2-C-002"), text, BUNDLE, ENTRIES))


class InheritedBehaviour(unittest.TestCase):
    """QV-G..H. v1.2 decides everything v1.1 decided, identically, apart from DF-01."""

    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads(AUDIT.read_text(encoding="utf-8"))

    def test_no_code_renamed_removed_or_reordered(self):
        inherited = V12.REJECTION_CODES[:len(V11.REJECTION_CODES)]
        self.assertEqual(list(V11.REJECTION_CODES), list(inherited))
        self.assertEqual((), V12.NEW_REJECTION_CODES)

    def test_no_inherited_stage_moved(self):
        self.assertEqual(list(V11.STAGES),
                         [s for s in V12.STAGES if s != "L_qualifier_semantics"])
        self.assertEqual("K_semantic", V12.STAGES[V12.STAGES.index("L_qualifier_semantics") - 1])

    def test_attempt_2_gains_exactly_one_rejection(self):
        inherited = self.audit["inherited_behaviour"]
        self.assertEqual(["U-D-P01-S03"], inherited["newly_rejected"])
        self.assertEqual([], inherited["newly_accepted"])
        self.assertTrue(inherited["no_unit_newly_accepted"])

    def test_qv_h_unrelated_units_are_not_newly_rejected(self):
        rows = [r for r in json.loads(FIXTURE_RESULTS.read_text(encoding="utf-8"))["rows"]
                if str(r["case_id"]).startswith("QV-H-")]
        self.assertTrue(rows)
        for row in rows:
            with self.subTest(case=row["case_id"]):
                self.assertEqual("PASS", row["outcome"])
                self.assertTrue(row["actual_valid"])

    def test_stage_l_is_silent_for_unregistered_claims(self):
        """The structural guarantee behind QV-H, asserted directly rather than by sampling."""
        registered = {e["claim_id"] for e in ENTRIES}
        for claim_id, claim in BUNDLE.allowlist.items():
            if claim_id in registered:
                continue
            text = claim.get("canonical_claim") or ""
            with self.subTest(claim=claim_id):
                self.assertEqual([], V12.stage_l_qualifier_semantics(
                    unit("U-X-P01-S01", text, claim_id), text, BUNDLE, ENTRIES))

    def test_non_material_units_are_untouched(self):
        u = unit("U-X-P01-S01", C009_CANONICAL)
        u.material = False
        self.assertEqual([], V12.stage_l_qualifier_semantics(u, C009_CANONICAL, BUNDLE, ENTRIES))

    def test_prior_validator_versions_are_byte_identical(self):
        recorded = json.loads(ANALYSIS_V2.read_text(encoding="utf-8"))["frozen_inputs"]["sha256"]
        for name, relative in (("draft_validator_v1", "scripts/49_section_draft_validator_v1.py"),
                               ("draft_validator_v1_1",
                                "scripts/52_section_draft_validator_v1_1.py")):
            with self.subTest(validator=name):
                self.assertEqual(recorded[name],
                                 hashlib.sha256((ROOT / relative).read_bytes()).hexdigest())


class RegistryIntegrity(unittest.TestCase):
    """The fail-closed properties. A registry that protects nothing must not pass quietly."""

    def test_registry_is_consistent(self):
        result = V12.registry_integrity(BUNDLE, ENTRIES)
        self.assertEqual([], result["problems"])
        self.assertTrue(result["consistent"])

    def test_qualifier_text_matches_the_frozen_qualifier(self):
        entry = ENTRIES[0]
        self.assertEqual(C009["qualifiers"][entry["qualifier_index"]], entry["qualifier_text"])

    def test_a_drifted_qualifier_is_refused(self):
        drifted = copy.deepcopy(ENTRIES[0])
        drifted["qualifier_text"] = drifted["qualifier_text"].replace("özgüdür", "özgü")
        self.assertFalse(V12.registry_integrity(BUNDLE, [drifted])["consistent"])

    def test_an_entry_its_own_canonical_claim_satisfies_is_refused(self):
        """DF-01 as a general property: no entry a verbatim copy would discharge."""
        vacuous = copy.deepcopy(ENTRIES[0])
        vacuous["required_constructions"]["items"] = [{
            "construction_id": "LEXICAL_ONLY",
            "clause_requires": [{"group_id": "anchor", "any_of": ["\\bkil\\w*"]}]}]
        result = V12.registry_integrity(BUNDLE, [vacuous])
        self.assertFalse(result["consistent"])
        self.assertIn("DF-01", " ".join(result["problems"]))

    def test_an_entry_on_the_wrong_claim_scope_is_refused(self):
        stale = copy.deepcopy(ENTRIES[0])
        stale["claim_scope_markers"]["any_of"] = ["design_table"]
        self.assertFalse(V12.registry_integrity(BUNDLE, [stale])["consistent"])

    def test_validate_draft_fails_closed_on_a_bad_registry(self):
        ir = PHASE.attempt_2_ir()
        broken = copy.deepcopy(ENTRIES[0])
        broken["claim_id"] = "SEC-02-2-C-999"
        with self.assertRaises(V12.QualifierRegistryError):
            V12.validate_draft(ir, BUNDLE, qualifier_semantics=[broken])


class PhaseArtifacts(unittest.TestCase):
    """What this phase wrote, and what it did not do."""

    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_gate_is_closed_go(self):
        self.assertEqual("CLOSED / GO", self.audit["gate"]["status"])
        self.assertEqual("closed_go", self.manifest["status"])

    def test_df_01_reproduced_in_four_steps(self):
        df = self.audit["df_01"]
        self.assertTrue(df["reproduced"])
        self.assertEqual([1, 2, 3, 4], [s["step"] for s in df["steps"]])
        for step in df["steps"]:
            with self.subTest(step=step["step"]):
                self.assertTrue(step["holds"])

    def test_phase_generated_nothing(self):
        for field in ("generation_attempts_in_this_phase", "retrieval_calls", "qdrant_writes",
                      "corpus_reads"):
            self.assertEqual(0, self.audit[field], field)
        self.assertEqual([], self.audit["validators_weakened"])
        self.assertFalse(self.audit["attempt_3_authorised_here"])
        self.assertFalse(self.audit["prose_rendered"])
        self.assertFalse(self.manifest["attempt_3_authorised_here"])

    def test_no_false_accepts_or_rejects(self):
        self.assertEqual([], self.audit["fixtures"]["false_accepts"])
        self.assertEqual([], self.audit["fixtures"]["false_rejects"])
        self.assertEqual([], self.audit["fixtures"]["code_mismatches"])
        self.assertTrue(self.audit["fixtures"]["all_pass"])

    def test_frozen_input_hashes_still_match_disk(self):
        for name, path in PHASE.FROZEN_INPUTS.items():
            with self.subTest(artifact=name):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                                 self.audit["frozen_inputs"]["sha256"][name])

    def test_contract_v1_2_declares_stage_l_and_widens_nothing(self):
        contract = json.loads(CONTRACT_V1_2.read_text(encoding="utf-8"))
        self.assertEqual("tunnelbook-draft-validation-contract-v1.2", contract["version"])
        self.assertEqual([], contract["change_scope"]["weakened"])
        self.assertEqual([], contract["change_scope"]["removed"])
        self.assertEqual([], contract["change_scope"]["renamed_codes"])
        self.assertEqual([], contract["new_rejection_codes"])
        self.assertIn("L_qualifier_semantics", contract["pipeline_order"])
        v11 = json.loads((DRAFTING / "contracts"
                          / "draft_validation_contract_v1_1.json").read_text(encoding="utf-8"))
        self.assertEqual(v11["rejection_codes"], contract["rejection_codes"])
        self.assertEqual(v11["pipeline_order"],
                         [s for s in contract["pipeline_order"] if s != "L_qualifier_semantics"])

    def test_report_exists(self):
        self.assertTrue(REPORT.exists())
        self.assertIn("CLOSED / GO", REPORT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
