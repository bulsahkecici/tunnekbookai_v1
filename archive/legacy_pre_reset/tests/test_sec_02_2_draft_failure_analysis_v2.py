"""SEC-02-2 Draft Failure Analysis v2 - the regression cases the analysis says are required.

Two jobs. The RC-A and RC-B cases pin the behaviour a future attempt #3 must not have changed:
what still fails, what already passes, and which vocabulary is licensed. They are tripwires
against a remediation that makes the pilot pass by loosening something, which is why several of
them assert a *rejection* rather than an acceptance.

The rest audits this phase's own artifacts - that the analysis reached a conclusion its recorded
evidence supports, that it generated nothing, and that it left the frozen inputs alone.
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
REMEDIATION = SECTION_DIR / "remediation_v1"
ANALYSIS = SECTION_DIR / "analysis_v2"

FAILURE_ANALYSIS = ANALYSIS / "audits" / "attempt_2_failure_analysis_v1.json"
MANIFEST = BOOK / "manifests" / "sec_02_2_draft_failure_analysis_v2.json"
REPORT = ROOT / "reports" / "sec_02_2_draft_failure_analysis_v2.md"
REJECTED_2 = REMEDIATION / "rejected" / "pilot_attempt_2_validation.json"
RAW_ATTEMPT_2 = REMEDIATION / "raw" / "sec_02_2_draft_raw_attempt_2.json"
DRAFTING_CONTRACT = DRAFTING / "contracts" / "section_drafting_contract_v1.json"
SEMANTIC_CONSTRAINTS = REMEDIATION / "contracts" / "draft_semantic_constraints_v1.json"


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


V1 = _load("test_analysis_v2_validator_v1", "scripts/49_section_draft_validator_v1.py")
V11 = _load("test_analysis_v2_validator_v1_1", "scripts/52_section_draft_validator_v1_1.py")
PHASE = _load("test_analysis_v2_phase", "scripts/53_sec_02_2_draft_failure_analysis_v2.py")

BUNDLE = V11.load_bundle()
CONSTRAINTS = V11.load_semantic_constraints()
C002 = BUNDLE.allowlist["SEC-02-2-C-002"]
C001_CANONICAL = BUNDLE.allowlist["SEC-02-2-C-001"]["canonical_claim"]


def unit(unit_id: str, text: str, claim_id: str = "SEC-02-2-C-002"):
    source_keys = list(BUNDLE.allowlist[claim_id]["source_keys"])
    return V1.DraftUnit(
        unit_id=unit_id, unit_type="PARAGRAPH_SENTENCE", text=text, material=True,
        claim_ids=[claim_id], source_keys=source_keys, relationship_type="INDEPENDENT",
        citation_intents=[{"claim_id": claim_id, "source_keys": source_keys}])


def codes(unit_id: str, text: str, paragraph: str, claim_id: str = "SEC-02-2-C-002"):
    return {(f.code, f.stage) for f in V11.validate_unit(
        unit(unit_id, text, claim_id), paragraph, BUNDLE, constraints=CONSTRAINTS)}


class QualifierBoundaryRegressions(unittest.TestCase):
    """RC-A1..A6. SEC-02-2-C-002's acceptance-criteria boundary."""

    def test_rc_a1_attempt_2_shape_is_still_rejected(self):
        canonical = C002["canonical_claim"]
        paragraph = f"{C001_CANONICAL} {canonical}"
        found = codes("U-A-P01-S02", canonical, paragraph)
        self.assertIn(("QUALIFIER_DROPPED", "E_conditions"), found)
        self.assertIn(("QUALIFIER_DROPPED", "K_semantic"), found)

    def test_rc_a2_two_bound_units_validate(self):
        identity = PHASE.C002_PROBES["C002_identity_unit"]
        canonical = C002["canonical_claim"]
        paragraph = f"{C001_CANONICAL} {identity} {canonical}"
        self.assertEqual(set(), codes("U-A-P01-S02", identity, paragraph))
        self.assertEqual(set(), codes("U-A-P01-S03", canonical, paragraph))

    def test_rc_a3_single_unit_combined_validates(self):
        combined = PHASE.C002_PROBES["C002_single_unit_combined"]
        paragraph = f"{C001_CANONICAL} {combined}"
        self.assertEqual(set(), codes("U-A-P01-S02", combined, paragraph))

    def test_rc_a4_identity_unit_without_conditions_fails(self):
        """A split that drops the claim's own conditions trades one failure for another."""
        bare = PHASE.C002_PROBES["C002_identity_unit_without_conditions"]
        canonical = C002["canonical_claim"]
        paragraph = f"{C001_CANONICAL} {bare} {canonical}"
        found = codes("U-A-P01-S02", bare, paragraph)
        self.assertIn(("CONDITION_DROPPED", "E_conditions"), found)

    def test_rc_a5_forbidden_attribution_still_fails(self):
        """The attempt-#1 failure mode. Widening the required meaning must not open this."""
        forbidden = ("Tablo-351-5'e göre püskürtme betonun basınç dayanım sınıfı C25/30'dur; "
                     "28 günlük karot numunelerinde kabul kriteri sağlanır.")
        paragraph = f"{C001_CANONICAL} {forbidden}"
        found = codes("U-A-P01-S02", forbidden, paragraph)
        self.assertIn(("SEMANTIC_SCOPE_MISMATCH", "K_semantic"), found)

    def test_rc_a6_dsc_c002_001_is_unchanged(self):
        constraint = json.loads(SEMANTIC_CONSTRAINTS.read_text(encoding="utf-8"))["constraints"][0]
        self.assertEqual("DSC-C002-001", constraint["constraint_id"])
        self.assertEqual("paragraph", constraint["required_meaning_markers"]["scope"])
        self.assertEqual(
            ["kabul kriter", "kabul ölçüt", "kabul şart", "kabul koşul", "kalite kontrol",
             "kabul deney", "acceptance criteri", "acceptance test"],
            constraint["required_meaning_markers"]["any_of"])
        self.assertEqual("QUALIFIER_DROPPED", constraint["missing_qualifier_code"])


class SupportContainmentRegressions(unittest.TestCase):
    """RC-B1..B4. SEC-02-2-P0-008's cross-lingual vocabulary."""

    def setUp(self):
        self.pool = V1.licensed_tokens(["SEC-02-2-P0-008"], BUNDLE)

    def test_rc_b1_attempt_2_sentence_still_fails_on_exactly_two_words(self):
        text = PHASE.P0_008_PROBES["P0008_attempt_2_actual"]
        self.assertEqual(["kayaç", "spesifik"], V1.unlicensed(text, self.pool, BUNDLE))

    def test_rc_b1_matches_what_the_rejection_recorded(self):
        rejection = json.loads(REJECTED_2.read_text(encoding="utf-8"))
        rejected = [u for u in rejection["rejected_units"] if u["unit_id"] == "U-C-P01-S02"][0]
        self.assertEqual(["UNSUPPORTED_PROPOSITION"], rejected["failure_codes"])
        self.assertEqual("kayaç, spesifik", rejected["failures"][0]["evidence"])

    def test_rc_b2_licensed_renderings_have_no_unlicensed_words(self):
        for name in ("P0008_kaya_for_kayac", "P0008_belirli", "P0008_bazi_belirli"):
            with self.subTest(rendering=name):
                self.assertEqual([], V1.unlicensed(PHASE.P0_008_PROBES[name], self.pool, BUNDLE))

    def test_rc_b3_kayac_stays_unlicensed_and_kaya_stays_licensed(self):
        """A widening tripwire. If 'kayaç' ever becomes licensed, something widened the pool."""
        def licensed(word: str) -> bool:
            folded = V1.fold(word)
            return any(V1.prefix_agreement(folded, token) for token in self.pool)
        self.assertFalse(licensed("kayaç"))
        self.assertFalse(licensed("spesifik"))
        self.assertTrue(licensed("kaya"))
        self.assertTrue(licensed("belirli"))

    def test_rc_b4_frozen_glosses_are_unchanged(self):
        glosses = json.loads(DRAFTING_CONTRACT.read_text(encoding="utf-8"))["translation_glosses"]
        self.assertEqual(
            ["bazı", "belirli", "kaya", "koşullarında", "koşulları", "ezilmiş", "parçalanmış",
             "sıkışan", "sıkışma", "kalınlık", "kalınlığı", "daha", "fazla", "olabilmektedir",
             "olabilir", "tünel", "boyutuna", "bağlı", "inç", "milimetre"],
            glosses["SEC-02-2-P0-008"])


class AnalysisArtifacts(unittest.TestCase):
    """What this phase wrote, and what it did not do."""

    @classmethod
    def setUpClass(cls):
        cls.analysis = json.loads(FAILURE_ANALYSIS.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_phase_generated_nothing(self):
        for field in ("generation_attempts_in_this_phase", "retrieval_calls", "qdrant_writes",
                      "corpus_reads"):
            self.assertEqual(0, self.analysis[field], field)
        self.assertEqual([], self.analysis["validators_weakened"])
        self.assertFalse(self.manifest["attempt_3_authorised_here"])

    def test_frozen_inputs_are_all_present_and_hashed(self):
        freeze = self.analysis["frozen_inputs"]
        self.assertTrue(freeze["all_present"])
        self.assertEqual([], freeze["missing"])
        for name, sha in freeze["sha256"].items():
            self.assertRegex(sha, r"^[0-9a-f]{64}$", name)

    def test_frozen_input_hashes_still_match_disk(self):
        """The analysis is only evidence if what it read is what is there now."""
        for name, path in PHASE.FROZEN_INPUTS.items():
            with self.subTest(artifact=name):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                                 self.analysis["frozen_inputs"]["sha256"][name])

    def test_both_failed_units_are_analysed_and_classified(self):
        by_unit = {f["unit_id"]: f for f in self.analysis["failures"]}
        self.assertEqual({"U-A-P01-S02", "U-C-P01-S02"}, set(by_unit))
        for unit_id, failure in by_unit.items():
            with self.subTest(unit=unit_id):
                self.assertIn(failure["root_cause_class"], PHASE.ROOT_CAUSE_CLASSES)
                self.assertTrue(failure["validator_verdict_correct"])
                self.assertTrue(failure["regression_cases_required"])
                self.assertTrue(failure["smallest_safe_remediation"])

    def test_analysed_units_are_the_units_the_rejection_named(self):
        rejection = json.loads(REJECTED_2.read_text(encoding="utf-8"))
        self.assertEqual(sorted(rejection["rejected_unit_ids"]),
                         sorted(f["unit_id"] for f in self.analysis["failures"]))
        raw = json.loads(RAW_ATTEMPT_2.read_text(encoding="utf-8"))
        self.assertEqual(raw["raw_text_sha256"], self.analysis["attempt_2"]["raw_text_sha256"])

    def test_analysed_text_is_the_text_attempt_2_produced(self):
        ir = json.loads(json.loads(RAW_ATTEMPT_2.read_text(encoding="utf-8"))["raw_text"])
        texts = {u["unit_id"]: u["text"] for u in ir["units"]}
        for failure in self.analysis["failures"]:
            with self.subTest(unit=failure["unit_id"]):
                self.assertEqual(texts[failure["unit_id"]], failure["generated_text"])

    def test_payload_omission_is_refuted_by_the_reconstruction(self):
        payload = self.analysis["evidence"]["payload_reconstruction"]["SEC-02-2-C-002"]
        self.assertTrue(payload["canonical_claim_supplied"])
        self.assertTrue(payload["qualifiers_are_mandatory_flag"])
        self.assertEqual(["DSC-C002-001"], payload["semantic_constraint_ids"])
        self.assertEqual(C002["qualifiers"], payload["qualifiers_supplied"])
        self.assertFalse(payload["unit_slot_for_the_qualifier"])

    def test_verbatim_census_supports_the_representation_finding(self):
        census = self.analysis["evidence"]["verbatim_census"]
        self.assertEqual(14, census["verbatim_units"])
        self.assertEqual(16, census["single_claim_units"])
        self.assertEqual(["U-C-P01-S01", "U-C-P01-S02"], census["composed_unit_ids"])
        self.assertEqual(["en"], census["composed_claim_languages"])
        self.assertEqual(1, self.analysis["evidence"]["unit_allocation"]["max_units_per_claim"])

    def test_no_qualifier_meaning_reached_the_prose(self):
        survival = self.analysis["evidence"]["qualifier_survival"]
        self.assertEqual("0/2", survival["meaning_realised"])
        self.assertEqual("1/2", survival["stage_e_preservation"])
        self.assertTrue(survival["recorded_but_not_actioned"])

    def test_licensed_alternatives_were_found_for_p0_008(self):
        probes = self.analysis["evidence"]["p0_008_probes"]
        self.assertEqual(
            ["P0008_bazi_belirli", "P0008_belirli", "P0008_kaya_for_kayac"],
            probes["licensed_alternatives_that_existed"])
        self.assertFalse(probes["words"]["kayaç"]["licensed"])
        self.assertTrue(probes["words"]["kaya"]["licensed"])

    def test_representation_question_is_answered_without_altering_the_claim(self):
        finding = self.analysis["representation_question"]
        self.assertFalse(finding["claim_altered_by_this_phase"])
        self.assertEqual("one frozen claim, two bound downstream units", finding["answer"])
        self.assertTrue(finding["single_unit_combined_validates"])
        self.assertTrue(finding["two_bound_units_validate"])
        self.assertFalse(finding["careless_split_validates"])

    def test_recommendation_is_concrete_and_not_a_loosening(self):
        recommendation = self.analysis["recommendation"]
        self.assertFalse(recommendation["is_a_loosening"])
        self.assertTrue(recommendation["attempt_3_justified"])
        self.assertTrue(recommendation["attempt_3_conditions"])
        self.assertIn("plan change", recommendation["category"])

    def test_report_and_manifest_agree_with_the_analysis(self):
        self.assertEqual(hashlib.sha256(FAILURE_ANALYSIS.read_bytes()).hexdigest(),
                         self.manifest["failure_analysis_sha256"])
        self.assertEqual("closed_go", self.manifest["status"])
        self.assertTrue(self.manifest["validator_verdicts_correct"])
        report = REPORT.read_text(encoding="utf-8")
        self.assertIn("SEC-02-2 DRAFT FAILURE ANALYSIS V2 — CLOSED / GO", report)
        for unit_id in ("U-A-P01-S02", "U-C-P01-S02"):
            self.assertIn(unit_id, report)

    def test_nothing_was_rendered_or_accepted(self):
        self.assertFalse((SECTION_DIR / "rendered" / "sec_02_2_pilot_v1_1.md").exists())
        self.assertFalse((REMEDIATION / "accepted" / "sec_02_2_draft_ir_v1_1.json").exists())
        self.assertFalse((REMEDIATION / "raw" / "sec_02_2_draft_raw_attempt_3.json").exists())


if __name__ == "__main__":
    unittest.main()
