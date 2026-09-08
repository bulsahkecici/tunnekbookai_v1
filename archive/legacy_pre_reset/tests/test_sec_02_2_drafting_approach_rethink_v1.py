"""SEC-02-2 Drafting Approach Rethink v1 — the probes, and the guard rails on the phase itself.

Three jobs.

The census probes assert the finding the architecture decision rests on: containment failure is a
property of production mode. They recompute it from the preserved attempts rather than reading it
back out of this phase's own artifacts, so a wrong analysis cannot pass by agreeing with itself.

The boundary probes pin the facts the word classification depends on — that `durumlarda` is exempt
and `durumlarında` is not, that the pool licenses English record metadata — because those are the
claims a reader is most likely to want to check and least likely to believe on assertion.

The rest guards the phase's own constraints: nothing generated, nothing widened, no validator
touched, every frozen input byte-identical, and no artifact anywhere authorising an attempt #4.
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
RETHINK = SECTION_DIR / "rethink_v1"

ANALYSIS = RETHINK / "audits" / "drafting_approach_analysis_v1.json"
CENSUS = RETHINK / "probes" / "realization_mode_census_v1.json"
PROBES = RETHINK / "probes" / "containment_boundary_probes_v1.json"
MATRIX = RETHINK / "audits" / "architecture_comparison_matrix_v1.json"
ADR = RETHINK / "decisions" / "adr_001_drafting_architecture_v2.json"
MIGRATION = RETHINK / "audits" / "migration_plan_v1.json"
MANIFEST = BOOK / "manifests" / "sec_02_2_drafting_approach_rethink_v1.json"
REPORT = ROOT / "reports" / "sec_02_2_drafting_approach_rethink_v1.md"

RAW_ATTEMPT_1 = SECTION_DIR / "raw" / "sec_02_2_draft_raw_v1.json"
RAW_ATTEMPT_2 = SECTION_DIR / "remediation_v1" / "raw" / "sec_02_2_draft_raw_attempt_2.json"
RAW_ATTEMPT_3 = SECTION_DIR / "attempt_3" / "raw" / "sec_02_2_draft_raw_attempt_3.json"
DRAFTING_CONTRACT = DRAFTING / "contracts" / "section_drafting_contract_v1.json"


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


V1 = _load("draft_validator_v1_rethink_test", "scripts/49_section_draft_validator_v1.py")
RETHINK_MODULE = _load("rethink_v1_test",
                       "scripts/57_sec_02_2_drafting_approach_rethink_v1.py")
BUNDLE = V1.load_bundle()


# ================================================================ census

class RealizationModeCensusTest(unittest.TestCase):
    """P1 — recomputed from the preserved attempts, not read back from the analysis."""

    def _census(self, raw_path: Path) -> dict:
        modes = {"reproduced": [0, 0], "composed": [0, 0]}
        for unit in RETHINK_MODULE.draft_ir(raw_path)["units"]:
            if not unit.get("material"):
                continue
            mode = RETHINK_MODULE.realization_mode(unit, BUNDLE)
            content = V1.content_tokens(unit.get("text", ""), BUNDLE.function_lexicon)
            pool = V1.licensed_tokens(unit.get("claim_ids") or [], BUNDLE)
            stray = V1.unlicensed(unit.get("text", ""), pool, BUNDLE) if pool else []
            modes[mode][0] += len(content)
            modes[mode][1] += len(stray)
        return {mode: {"content": c, "unlicensed": u} for mode, (c, u) in modes.items()}

    def test_reproduction_never_leaves_the_pool(self):
        """The mode that draws its tokens from the pool by construction has never failed."""
        total_content = total_unlicensed = 0
        for raw in (RAW_ATTEMPT_1, RAW_ATTEMPT_2, RAW_ATTEMPT_3):
            reproduced = self._census(raw)["reproduced"]
            total_content += reproduced["content"]
            total_unlicensed += reproduced["unlicensed"]
        self.assertGreater(total_content, 400, "the reproduced sample must be large enough to "
                                               "carry the argument")
        self.assertEqual(0, total_unlicensed)

    def test_composition_fails_and_the_rate_did_not_respond_to_remediation(self):
        """The finding the decision rests on: instructions moved fidelity, not this."""
        rates = []
        for raw in (RAW_ATTEMPT_2, RAW_ATTEMPT_3):
            composed = self._census(raw)["composed"]
            self.assertGreater(composed["content"], 0)
            self.assertGreater(composed["unlicensed"], 0)
            rates.append(composed["unlicensed"] / composed["content"])
        # Plan v1.2 closed every attempt-#2 cause. If it had moved containment too, the two rates
        # would separate; they agree to within a percentage point.
        self.assertLess(abs(rates[0] - rates[1]), 0.01)
        self.assertGreater(min(rates), 0.05)

    def test_composed_unit_count_rose_as_fidelity_was_fixed(self):
        """Fidelity is only reachable by composition, so remediation buys exposure."""
        counts = []
        for raw in (RAW_ATTEMPT_1, RAW_ATTEMPT_2, RAW_ATTEMPT_3):
            units = [u for u in RETHINK_MODULE.draft_ir(raw)["units"] if u.get("material")]
            counts.append(sum(1 for u in units
                              if RETHINK_MODULE.realization_mode(u, BUNDLE) == "composed"))
        self.assertEqual(counts, sorted(counts))
        self.assertLess(counts[0], counts[-1])

    def test_attempt_1_is_the_control(self):
        """All reproduction, no containment failure — and rejected for fidelity instead."""
        census = self._census(RAW_ATTEMPT_1)
        self.assertEqual(0, census["composed"]["content"])
        self.assertEqual(0, census["reproduced"]["unlicensed"])
        histogram = _json(SECTION_DIR / "audits" / "sec_02_2_draft_audit_v1.json")
        self.assertNotIn("UNSUPPORTED_PROPOSITION", histogram["failure_histogram"])
        self.assertIn("QUALIFIER_DROPPED", histogram["failure_histogram"])

    def test_census_artifact_matches_a_fresh_computation(self):
        recorded = _json(CENSUS)["totals"]
        for mode in ("reproduced", "composed"):
            fresh = sum(self._census(raw)[mode]["unlicensed"]
                        for raw in (RAW_ATTEMPT_1, RAW_ATTEMPT_2, RAW_ATTEMPT_3))
            self.assertEqual(recorded[mode]["unlicensed"], fresh)


# ================================================================ boundary

class ContainmentBoundaryTest(unittest.TestCase):
    """P2/P3 — the facts the word classification stands on."""

    def test_durumlarinda_is_rejected_by_an_enumeration_gap(self):
        """One morpheme from an exempt form of the same lexeme. This is the whole finding."""
        lexicon = BUNDLE.function_lexicon
        self.assertIn(V1.fold("durumlarda"), lexicon)
        self.assertIn(V1.fold("durumunda"), lexicon)
        self.assertIn(V1.fold("durumda"), lexicon)
        self.assertNotIn(V1.fold("durumlarında"), lexicon)

    def test_exemption_and_licensing_use_different_matching_regimes(self):
        """Exact membership for grammar, prefix agreement for content, over Turkish."""
        self.assertTrue(V1.prefix_agreement(V1.fold("durumlarında"), V1.fold("durumlarda")))
        self.assertNotIn(V1.fold("durumlarında"), BUNDLE.function_lexicon)

    def test_pool_licenses_english_record_metadata(self):
        pool = V1.licensed_tokens(["SEC-02-2-C-002"], BUNDLE)
        for token in ("claim", "qualifier", "hence", "already"):
            self.assertIn(token, pool)

    def test_english_surface_form_licensed_where_its_turkish_realisation_is_not(self):
        pool = V1.licensed_tokens(["SEC-02-2-P0-008"], BUNDLE)
        self.assertIn("specific", pool)
        self.assertFalse(any(V1.prefix_agreement(V1.fold("spesifik"), t) for t in pool))

    def test_saglar_had_no_licensed_turkish_verb_available(self):
        """The case the licensed-alternative flag records as `true` and should not."""
        pool = V1.licensed_tokens(["SEC-02-2-C-002"], BUNDLE)
        self.assertIn("gives", pool)
        self.assertFalse(any(V1.prefix_agreement(V1.fold("sağlar"), t) for t in pool))

    def test_all_four_words_are_genuinely_unlicensed(self):
        """The rejections are correct as specified; this phase disputes the architecture."""
        for word, claim_id in (("ifade", "SEC-02-2-C-002"), ("sağlar", "SEC-02-2-C-002"),
                               ("durumlarında", "SEC-02-2-P0-008"),
                               ("örneğin", "SEC-02-2-P0-008")):
            pool = V1.licensed_tokens([claim_id], BUNDLE)
            self.assertNotIn(V1.fold(word), BUNDLE.function_lexicon, word)
            self.assertFalse(any(V1.prefix_agreement(V1.fold(word), t) for t in pool), word)


class WordClassificationTest(unittest.TestCase):

    def test_all_four_words_classified(self):
        words = {w["word"]: w for w in _json(PROBES)["classification"]["words"]}
        self.assertEqual({"ifade", "sağlar", "durumlarında", "örneğin"}, set(words))
        for word in words.values():
            self.assertTrue(set(word["categories"]) <= {"1", "2", "3", "4"})
            self.assertIn(word["primary"], word["categories"])

    def test_the_four_words_are_not_one_class(self):
        """A single remedy cannot be right for all four, which is the point of classifying."""
        words = _json(PROBES)["classification"]["words"]
        primaries = {w["primary"] for w in words}
        self.assertGreater(len(primaries), 1)

    def test_relationship_bearing_words_are_identified(self):
        words = {w["word"]: w for w in _json(PROBES)["classification"]["words"]}
        self.assertIn("3", words["sağlar"]["categories"])
        self.assertIn("3", words["ifade"]["categories"])

    def test_ifade_does_not_get_a_clean_bill_of_health(self):
        """It substitutes a metalinguistic predicate for a copula the qualifier states flatly."""
        words = {w["word"]: w for w in _json(PROBES)["classification"]["words"]}
        self.assertFalse(words["ifade"]["category_4_excluded"])


# ================================================================ the decision

class DecisionTest(unittest.TestCase):

    def test_architecture_a_rejected_and_d_selected(self):
        matrix = _json(MATRIX)
        self.assertEqual("D", matrix["selected"])
        options = {o["id"]: o for o in matrix["options"]}
        self.assertEqual({"A", "B", "C", "D"}, set(options))
        self.assertTrue(options["A"]["verdict"].startswith("REJECTED"))
        self.assertTrue(options["B"]["verdict"].startswith("REJECTED"))
        self.assertEqual("SELECTED", options["D"]["verdict"])

    def test_lexicon_widening_is_rejected_and_named_as_a_loosening(self):
        options = {o["id"]: o for o in _json(MATRIX)["options"]}
        self.assertTrue(options["B"]["weakens_stage_c"])
        self.assertIn("more permissive", options["B"]["weakening_stated_plainly"])

    def test_selected_option_does_not_weaken_stage_c(self):
        options = {o["id"]: o for o in _json(MATRIX)["options"]}
        self.assertFalse(options["D"]["weakens_stage_c"])
        self.assertIn("unchanged", options["D"]["stage_c_relationship"])

    def test_previous_inference_recorded_as_insufficient(self):
        superseded = _json(ANALYSIS)["refined_cause"]["superseded_inference"]
        self.assertIn("licensed_alternative_was_in_hand", superseded["inference"])
        self.assertTrue(superseded["status"].startswith("INSUFFICIENT"))
        self.assertGreaterEqual(len(superseded["why_insufficient"]), 3)

    def test_refined_cause_is_architectural_not_the_writer(self):
        cause = _json(ANALYSIS)["refined_cause"]
        self.assertTrue(cause["refined_cause_class"].startswith("ARCHITECTURAL"))
        self.assertIn("WRITER_VOCABULARY_CHOICE", cause["supersedes"])

    def test_the_untested_reading_is_recorded_rather_than_claimed_refuted(self):
        """All three attempts used one writer. Saying otherwise would overstate the evidence."""
        confound = _json(ANALYSIS)["refined_cause"]["confound_recorded"]
        self.assertEqual("CF-01", confound["id"])
        self.assertIn("UNTESTED", confound["consequence"])

    def test_adr_records_what_it_was_not_decided_on(self):
        adr = _json(ADR)
        self.assertEqual("ACCEPTED", adr["status"])
        self.assertGreaterEqual(len(adr["not_decided_on"]), 3)
        self.assertTrue(any("phase brief proposed it" in reason
                            for reason in adr["not_decided_on"]))

    def test_llm_owns_no_surface_word(self):
        migration = _json(MIGRATION)
        for forbidden in ("any surface word", "numeric rendering", "modality",
                          "citation strings", "morphology"):
            self.assertIn(forbidden, migration["llm_explicitly_not_responsible_for"])
        for owned in migration["renderer_responsibility"]:
            self.assertNotIn(owned, migration["llm_responsibility"])

    def test_implementation_phase_builds_before_it_writes(self):
        migration = _json(MIGRATION)
        self.assertIn("no prose", migration["principle"])
        self.assertIn("ARCHITECTURE V2 PILOT #1", migration["principle"])
        kinds = {a["kind"] for a in migration["new_artifacts"]}
        self.assertTrue({"contract", "module", "test harness"} <= kinds)


# ================================================================ phase constraints

class PhaseConstraintTest(unittest.TestCase):

    def test_nothing_was_generated_retrieved_or_written(self):
        accounting = _json(ANALYSIS)["accounting"]
        for key in ("generation_attempts", "retrieval_calls", "qdrant_writes", "corpus_reads",
                    "prose_rendered"):
            self.assertEqual(0, accounting[key], key)
        for key in ("validators_weakened", "lexicons_widened", "frozen_artifacts_modified"):
            self.assertEqual([], accounting[key], key)
        self.assertFalse(accounting["attempt_4_authorised"])

    def test_frozen_inputs_are_byte_identical_to_what_was_recorded(self):
        recorded = _json(ANALYSIS)["frozen_inputs"]["sha256"]
        for name, path in RETHINK_MODULE.FROZEN_INPUTS.items():
            self.assertEqual(recorded[name],
                             hashlib.sha256(path.read_bytes()).hexdigest(), name)

    def test_no_lexicon_was_widened(self):
        """The four words must still be outside the contract this phase declined to change."""
        contract = _json(DRAFTING_CONTRACT)
        lexicon = set(contract["function_lexicon"])
        for word in ("ifade", "sağlar", "durumlarında", "örneğin", "kayaç", "spesifik"):
            self.assertNotIn(word, lexicon, word)
        self.assertNotIn("ifade", contract["paraphrase_lexicon"])
        self.assertNotIn("sağlar", contract["paraphrase_lexicon"])

    def test_the_rejections_still_stand(self):
        rejection = _json(SECTION_DIR / "attempt_3" / "rejected"
                          / "pilot_attempt_3_validation.json")
        self.assertEqual("REJECT", rejection["status"])
        self.assertFalse(rejection["repaired"])
        self.assertFalse(rejection["rendered"])
        self.assertFalse(rejection["translated"])
        self.assertEqual(["U-A-P01-S03", "U-C-P01-S03"], sorted(rejection["rejected_unit_ids"]))

    def test_no_artifact_authorises_a_fourth_attempt(self):
        manifest = _json(MANIFEST)
        self.assertFalse(manifest["attempt_4_authorised"])
        self.assertEqual("retired", manifest["attempt_4_identifier"])
        self.assertEqual("ARCHITECTURE V2 PILOT #1", manifest["first_pilot_identifier"])
        for forbidden in _json(ADR)["does_not_authorise"]:
            self.assertIsInstance(forbidden, str)
        self.assertTrue(any("attempt #4" in item for item in _json(ADR)["does_not_authorise"]))

    def test_manifest_and_report_exist_and_agree(self):
        manifest = _json(MANIFEST)
        self.assertEqual("closed_go", manifest["status"])
        self.assertEqual("D", manifest["architecture_selected"])
        self.assertEqual("REJECTED", manifest["lexicon_widening"])
        self.assertEqual("SEC-02-2 DRAFTING ARCHITECTURE V2 IMPLEMENTATION",
                         manifest["next_phase"])
        self.assertTrue(REPORT.exists())
        self.assertEqual(manifest["analysis_sha256"],
                         hashlib.sha256(ANALYSIS.read_bytes()).hexdigest())

    def test_phase_is_reproducible(self):
        """Re-running the analysis must reach the same conclusions from the same evidence."""
        rebuilt = RETHINK_MODULE.build_analysis()
        recorded = _json(ANALYSIS)
        self.assertEqual(recorded["census"]["totals"], rebuilt["census"]["totals"])
        self.assertEqual(recorded["comparison_matrix"]["selected"],
                         rebuilt["comparison_matrix"]["selected"])
        self.assertEqual(recorded["refined_cause"]["refined_cause_class"],
                         rebuilt["refined_cause"]["refined_cause_class"])


if __name__ == "__main__":
    unittest.main()
