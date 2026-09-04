"""Architecture V2 — the invariants each of M1 through M5 exists to hold.

The static containment proof is the phase's gate and it runs as a script. These tests are the
other half: they check the properties the proof assumes, the ones a passing proof could hide, and
the phase constraints the proof does not speak to.

Three things they deliberately do not do. They do not re-run the proof and assert it passed —
that would test the recording, not the property. They do not test the renderer against a fixed
expected string, because pinning surfaces would make the contract unchangeable rather than
correct. And they do not construct a plan by hand where the contract can enumerate one, because a
hand-picked plan is a sample and the whole claim of this architecture is about the universe.
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

ARCH_V2 = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "architecture_v2"
ACCEPTANCE = ARCH_V2 / "contracts" / "architecture_v2_acceptance_contract_v1.json"
PLAN_CONTRACT = ARCH_V2 / "contracts" / "semantic_plan_ir_contract_v2.json"
REALIZATION_CONTRACT = ARCH_V2 / "contracts" / "claim_realization_contract_v2.json"
MORPHOLOGY_CONTRACT = ARCH_V2 / "contracts" / "turkish_morphology_v2.json"
PROOF = ARCH_V2 / "audits" / "static_containment_proof_v2.json"
NEGATIVES = ARCH_V2 / "fixtures" / "negative_fixtures_v2.json"
UNIVERSE = ARCH_V2 / "fixtures" / "realization_universe_v2.json"
ACCEPTANCE_MANIFEST = ROOT / "data" / "book" / "manifests" / "architecture_v2_acceptance_contract_v1.json"


def _load(name: str, filename: str):
    path = ROOT / "scripts" / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


V1 = _load("av2_v1", "49_section_draft_validator_v1.py")
V1_2 = _load("av2_v1_2", "54_section_draft_validator_v1_2.py")
PLAN_IR = _load("av2_plan_ir", "59_semantic_plan_ir_contract_v2.py")
REAL = _load("av2_real", "60_claim_realization_contract_v2.py")
MORPH = _load("av2_morph", "61_turkish_morphology_v2.py")
RENDER = _load("av2_render", "62_deterministic_surface_renderer_v2.py")

BUNDLE = V1.load_bundle()
REALIZATION = REAL.RealizationContract.load()


# ================================================================ M1

class PlanIRProseExclusionTest(unittest.TestCase):
    """The plan carries symbolic choices. Every route a word could take in is closed."""

    def _slot(self, **overrides):
        slot = {"slot_id": "S01", "claim_id": "SEC-02-2-C-001",
                "realization_role": "CLAIM_STATEMENT"}
        slot.update(overrides)
        return slot

    def _plan(self, slots):
        return {"section_id": "SEC-02-2", "plan_id": "P-T", "plan_version": "t", "language": "tr",
                "subsections": [{"subsection_id": "SEC-02-2-A", "paragraph_groups": [
                    {"paragraph_id": "P01", "slots": slots}]}]}

    def test_named_prose_field_is_rejected(self):
        for name in ("text", "prose", "sentence", "free_text", "wording"):
            with self.assertRaises(PLAN_IR.PlanRejection) as caught:
                PLAN_IR.parse_plan(self._plan([self._slot(**{name: "Bir cümle."})]))
            self.assertIn(caught.exception.code,
                          ("PLAN_PROSE_FIELD", "PLAN_UNKNOWN_FIELD"), name)

    def test_prose_under_an_innocent_field_name_is_rejected(self):
        """The blocklist is the tripwire; requiring every key to be declared is the defence."""
        with self.assertRaises(PLAN_IR.PlanRejection) as caught:
            PLAN_IR.parse_plan(self._plan([self._slot(note="Bu tablo sınıfı belirler.")]))
        self.assertEqual("PLAN_UNKNOWN_FIELD", caught.exception.code)

    def test_an_id_cannot_carry_a_sentence(self):
        with self.assertRaises(PLAN_IR.PlanRejection) as caught:
            PLAN_IR.parse_plan(self._plan([self._slot(slot_id="Püskürtme beton yeterlidir.")]))
        self.assertEqual("PLAN_PROSE_FIELD", caught.exception.code)

    def test_no_declared_field_admits_free_text(self):
        """Every leaf type in the schema is an id, an id list or the closed role enum."""
        for kind in PLAN_IR.SLOT_LEAF_TYPES.values():
            self.assertIn(kind, ("id", "id_list", "role"))

    def test_role_set_is_closed_with_no_escape_hatch(self):
        for forbidden in ("FREEFORM", "OTHER", "GENERIC", "CUSTOM"):
            self.assertNotIn(forbidden, PLAN_IR.REALIZATION_ROLES)
            with self.assertRaises(PLAN_IR.PlanRejection) as caught:
                PLAN_IR.parse_plan(self._plan([self._slot(realization_role=forbidden)]))
            self.assertEqual("PLAN_FORBIDDEN_ROLE", caught.exception.code)

    def test_unknown_role_rejects_rather_than_defaulting(self):
        with self.assertRaises(PLAN_IR.PlanRejection) as caught:
            PLAN_IR.parse_plan(self._plan([self._slot(realization_role="NARRATIVE")]))
        self.assertEqual("PLAN_UNKNOWN_ROLE", caught.exception.code)


class PlanValidationTest(unittest.TestCase):
    """What must be provable before a word is rendered."""

    def _validate(self, slots):
        plan = PLAN_IR.parse_plan({
            "section_id": "SEC-02-2", "plan_id": "P-V", "plan_version": "t", "language": "tr",
            "subsections": [{"subsection_id": "SEC-02-2-A", "paragraph_groups": [
                {"paragraph_id": "P01", "slots": slots}]}]})
        return PLAN_IR.validate_plan(plan, BUNDLE, REALIZATION)

    def _slot(self, claim_id, role, **extra):
        return {"slot_id": f"S-{claim_id}-{role}"[:60], "claim_id": claim_id,
                "realization_role": role, **extra}

    def test_source_key_from_another_claim_is_rejected(self):
        other = sorted(BUNDLE.allowlist["SEC-02-2-C-009"].get("source_keys") or [])
        result = self._validate([self._slot("SEC-02-2-C-001", "CLAIM_STATEMENT",
                                            citation_source_keys=other)])
        self.assertIn("PLAN_SOURCE_KEY_NOT_OWNED", {f["code"] for f in result.failures})

    def test_numeric_addressed_through_another_claim_is_rejected(self):
        result = self._validate([self._slot("SEC-02-2-C-001", "CLAIM_STATEMENT",
                                            numeric_fact_ids=["SEC-02-2-C-009#NUM0"])])
        self.assertIn("PLAN_NUMERIC_NOT_REGISTERED", {f["code"] for f in result.failures})

    def test_unregistered_numeric_index_is_rejected(self):
        result = self._validate([self._slot("SEC-02-2-C-001", "CLAIM_STATEMENT",
                                            numeric_fact_ids=["SEC-02-2-C-001#NUM9"])])
        self.assertIn("PLAN_NUMERIC_NOT_REGISTERED", {f["code"] for f in result.failures})

    def test_denylisted_claim_is_rejected(self):
        denylisted = sorted(BUNDLE.denylist)
        if not denylisted:
            self.skipTest("no denylisted claim in this section")
        result = self._validate([self._slot(denylisted[0], "CLAIM_STATEMENT")])
        self.assertIn("PLAN_CLAIM_DENYLISTED", {f["code"] for f in result.failures})

    def test_relation_beyond_independent_is_rejected(self):
        result = self._validate([self._slot("SEC-02-2-C-001", "CLAIM_STATEMENT",
                                            relation_constraint_ids=["SOURCE_SUPPORTED_RELATION"])])
        codes = {f["code"] for f in result.failures}
        self.assertTrue(codes & {"PLAN_RELATION_NOT_ALLOWED",
                                 "PLAN_RELATION_NOT_SOURCE_SUPPORTED"})

    def test_registered_qualifier_is_mandatory_wherever_its_claim_is_stated(self):
        result = self._validate([self._slot("SEC-02-2-C-002", "CLAIM_STATEMENT")])
        self.assertIn("PLAN_PARAGRAPH_QUALIFIER_MISSING", {f["code"] for f in result.failures})

    def test_paragraph_scoped_condition_needs_its_own_slot(self):
        result = self._validate([self._slot("SEC-02-2-P0-001", "CLAIM_STATEMENT")])
        self.assertIn("PLAN_PARAGRAPH_CONDITION_MISSING", {f["code"] for f in result.failures})

    def test_supporting_role_cannot_stand_alone(self):
        result = self._validate([self._slot("SEC-02-2-C-009", "QUALIFIER_SCOPE")])
        self.assertIn("PLAN_SUPPORTING_ROLE_WITHOUT_STATEMENT",
                      {f["code"] for f in result.failures})

    def test_unrealizable_pair_is_rejected_at_plan_validation(self):
        result = self._validate([self._slot("SEC-02-2-C-001", "EXEMPLIFICATION")])
        self.assertIn("PLAN_ROLE_UNREALIZABLE", {f["code"] for f in result.failures})

    def test_scope_computation_has_one_implementation(self):
        """M1 and M2 must not come to disagree about which conditions are sentence-internal."""
        claim = BUNDLE.allowlist["SEC-02-2-P0-001"]
        self.assertEqual(PLAN_IR.unit_scoped_conditions(claim, BUNDLE),
                         REAL.unit_scoped_conditions(claim, BUNDLE))


# ================================================================ M2

class RealizationContractTest(unittest.TestCase):

    def test_every_claim_and_role_has_a_verdict(self):
        claims = {c for c, _ in REALIZATION._by_key}
        self.assertEqual(len(claims) * len(REAL.ROLES), len(REALIZATION._by_key))
        for entry in REALIZATION.payload["entries"]:
            self.assertIn(entry["status"], ("REALIZABLE", "UNREALIZABLE"))

    def test_unrealizable_entries_state_a_reason_and_carry_no_segments(self):
        for entry in REALIZATION.payload["entries"]:
            if entry["status"] == "UNREALIZABLE":
                self.assertTrue(entry["reason"], entry["claim_id"])
                self.assertEqual([], entry["segments"])

    def test_every_frozen_text_segment_is_a_verbatim_claim_field(self):
        """No paraphrase. A segment must be findable, byte for byte, in the claim record."""
        for entry in REALIZATION.payload["entries"]:
            claim = BUNDLE.allowlist.get(entry["claim_id"]) or {}
            haystack = json.dumps(claim, ensure_ascii=False)
            for segment in entry["segments"]:
                if segment["kind"] == "FROZEN_TEXT":
                    self.assertIn(segment["value"].split(";")[0].strip()[:40], haystack,
                                  f"{entry['claim_id']}/{entry['realization_role']}")

    def test_every_gloss_token_is_frozen_for_that_claim(self):
        for entry in REALIZATION.payload["entries"]:
            allowed = REAL.frozen_glosses(BUNDLE, entry["claim_id"])
            for segment in entry["segments"]:
                if segment["kind"] == "GLOSS":
                    self.assertIn(V1.fold(segment["token"]), allowed,
                                  f"{entry['claim_id']}: {segment['token']}")

    def test_every_scaffold_token_is_grammar_the_support_test_ignores(self):
        for row in REALIZATION.payload["scaffold"]["tokens"]:
            self.assertTrue(row["admissible"], row["token"])
            self.assertTrue(row["below_content_minimum"] or row["in_function_lexicon"],
                            row["token"])
            self.assertFalse(row["is_prohibited_marker"], row["token"])
            self.assertFalse(row["is_attribution_marker"], row["token"])

    def test_no_relation_connective_is_scaffold(self):
        scaffold = {V1.fold(t) for t in REAL.SCAFFOLD_TOKENS}
        for phrase in ("bu nedenle", "dolayısıyla", "bunun sonucunda", "sayesinde",
                       "böylece", "ancak", "buna karşın"):
            self.assertNotIn(V1.fold(phrase), scaffold)

    def test_every_licensed_numeric_is_one_the_validator_licenses(self):
        for entry in REALIZATION.payload["entries"]:
            allowed = V1.licensed_numerics([entry["claim_id"]], BUNDLE)
            for segment in entry["segments"]:
                if segment["kind"] == "LICENSED_NUMERIC":
                    pair = (V1._normalise_value(segment["value"]),
                            V1.fold(segment["unit"]).replace("³", "3"))
                    self.assertIn(pair, allowed, f"{entry['claim_id']}: {pair}")

    def test_the_contract_is_not_trivially_empty(self):
        """A contract that refuses everything would pass the proof and be useless."""
        self.assertGreater(REALIZATION.payload["totals"]["realizable"], 50)
        roles = {role for _, role in REALIZATION.realizable_pairs()}
        self.assertEqual(set(REAL.ROLES), roles)

    def test_lexicons_and_glosses_are_untouched(self):
        contract = _json(ROOT / "data/book/drafting/contracts/section_drafting_contract_v1.json")
        for word in ("ifade", "sağlar", "durumlarında", "örneğin", "kayaç", "spesifik"):
            self.assertNotIn(word, set(contract["function_lexicon"]), word)
        self.assertEqual(3, len(contract["translation_glosses"]))


# ================================================================ M3

class MorphologyTest(unittest.TestCase):

    def test_every_fixture_passes(self):
        for fixture in MORPH.run_fixtures():
            self.assertTrue(fixture["passed"],
                            f"{fixture['operation']}({fixture['stem']!r}) -> "
                            f"{fixture['actual']!r} != {fixture['expected']!r}")

    def test_every_fixture_names_a_frozen_witness(self):
        """A rule with no frozen SEC-02-2 witness does not belong in the module."""
        for fixture in MORPH.FIXTURES:
            self.assertTrue(fixture["witness"])
            self.assertIn("SEC-02-2", fixture["witness"])

    def test_abbreviation_harmony_is_data_not_inference(self):
        """'mm' and 'MPa' contain no vowel; guessing gives mm'dır, which nothing downstream sees."""
        self.assertEqual("mm'dir", MORPH.copula("mm"))
        self.assertEqual("MPa'dır", MORPH.copula("MPa"))
        with self.assertRaises(MORPH.MorphologyError):
            MORPH.copula("XYZ")

    def test_functions_are_pure(self):
        probe = MORPH.determinism_probe()
        self.assertTrue(probe["identical"])

    def test_scope_stays_bounded(self):
        self.assertTrue(MORPH.NOT_IMPLEMENTED)
        self.assertLessEqual(len(MORPH.SUFFIXES), 10)


# ================================================================ M4

class RendererTest(unittest.TestCase):

    def _case(self, index: int = 0) -> dict:
        return _json(UNIVERSE)["cases"][index]["plan"]

    def test_renderer_is_byte_deterministic(self):
        plan = self._case()
        first = RENDER.render_bytes(RENDER.render_from_raw(plan, REALIZATION, BUNDLE))
        for _ in range(3):
            self.assertEqual(first, RENDER.render_bytes(
                RENDER.render_from_raw(plan, REALIZATION, BUNDLE)))

    def test_renderer_refuses_an_invalid_plan_rather_than_rendering_partially(self):
        plan = {"section_id": "SEC-02-2", "plan_id": "P-BAD", "plan_version": "t",
                "language": "tr", "subsections": [{"subsection_id": "SEC-02-2-A",
                "paragraph_groups": [{"paragraph_id": "P01", "slots": [
                    {"slot_id": "S1", "claim_id": "SEC-02-2-C-999",
                     "realization_role": "CLAIM_STATEMENT"}]}]}]}
        with self.assertRaises(RENDER.RenderRefusal) as caught:
            RENDER.render_from_raw(plan, REALIZATION, BUNDLE)
        self.assertEqual("RENDER_PLAN_INVALID", caught.exception.code)

    def test_ownership_guard_catches_an_unlicensed_token(self):
        """The guard runs on the finished string, so a bad contract entry cannot slip through."""
        with self.assertRaises(RENDER.RenderRefusal) as caught:
            RENDER._ownership_guard(
                "Püskürtme beton gerekli dayanımı sağlar ve ekonomiktir.",
                "SEC-02-2-C-001", "S-probe", BUNDLE)
        self.assertEqual("RENDER_UNLICENSED_TOKEN", caught.exception.code)

    def test_every_rendered_unit_declares_exactly_one_claim(self):
        """Merging claims would give a unit the union of two pools, which is how vocabulary leaks."""
        for case in _json(UNIVERSE)["cases"][:40]:
            payload = RENDER.render_from_raw(case["plan"], REALIZATION, BUNDLE)
            for unit in payload["units"]:
                self.assertEqual(1, len(unit["claim_ids"]), unit["unit_id"])

    def test_no_unit_asserts_a_relation(self):
        for case in _json(UNIVERSE)["cases"][:40]:
            payload = RENDER.render_from_raw(case["plan"], REALIZATION, BUNDLE)
            for unit in payload["units"]:
                self.assertEqual("INDEPENDENT", unit["relationship_type"])

    def test_no_packet_local_handle_is_ever_rendered(self):
        for case in _json(UNIVERSE)["cases"]:
            payload = RENDER.render_from_raw(case["plan"], REALIZATION, BUNDLE)
            for unit in payload["units"]:
                self.assertIsNone(V1.PACKET_EID_RE.search(unit["text"]), unit["unit_id"])

    def test_citations_use_only_the_declaring_claim_source_keys(self):
        for case in _json(UNIVERSE)["cases"]:
            payload = RENDER.render_from_raw(case["plan"], REALIZATION, BUNDLE)
            for unit in payload["units"]:
                registered = set(BUNDLE.allowlist[unit["claim_ids"][0]].get("source_keys") or [])
                self.assertTrue(set(unit["source_keys"]) <= registered, unit["unit_id"])


# ================================================================ M5

class StaticContainmentProofTest(unittest.TestCase):

    def setUp(self):
        self.proof = _json(PROOF)

    def test_proof_passed_on_a_non_trivial_universe(self):
        self.assertEqual("PASS", self.proof["status"])
        self.assertGreater(self.proof["universe"]["enumerated_cases"], 100)
        self.assertGreater(self.proof["universe"]["rendered_units"], 200)

    def test_zero_tolerance_codes_are_all_zero(self):
        self.assertEqual({}, self.proof["zero_tolerance_violations"])
        self.assertEqual({}, self.proof["failure_histogram"])

    def test_no_false_accepts_and_no_false_rejects(self):
        self.assertEqual([], self.proof["false_rejects"])
        self.assertEqual([], self.proof["false_accepts"])

    def test_unrealizable_pairs_are_refused_not_silently_skipped(self):
        refusals = self.proof["unrealizable_refusals"]
        self.assertEqual(refusals["checked"], refusals["refused"])
        self.assertEqual([], refusals["leaked"])

    def test_every_negative_fixture_rejects(self):
        negatives = _json(NEGATIVES)
        self.assertEqual(negatives["count"], negatives["rejected"])
        self.assertEqual([], negatives["false_accepts"])

    def test_the_three_semantic_attacks_are_unconstructible_and_rejected(self):
        negatives = {f["fixture_id"]: f for f in _json(NEGATIVES)["fixtures"]}
        for fixture_id in ("NEG-16", "NEG-17", "NEG-18"):
            fixture = negatives[fixture_id]
            self.assertFalse(fixture["renderer_can_construct"], fixture_id)
            self.assertEqual("REJECT", fixture["validator_status"], fixture_id)
            self.assertTrue(fixture["expected_code_seen"], fixture_id)

    def test_determinism_holds_across_processes(self):
        determinism = self.proof["determinism"]
        self.assertTrue(determinism["in_process_identical"])
        self.assertTrue(determinism["cross_process_identical"])

    def test_proof_ran_against_the_unchanged_validator(self):
        self.assertEqual("tunnelbook-section-draft-validator-v1.2",
                         self.proof["validator_version"])


# ================================================================ phase constraints

class PhaseConstraintTest(unittest.TestCase):

    def test_acceptance_contract_was_frozen_before_implementation(self):
        contract = _json(ACCEPTANCE)
        self.assertTrue(contract["authored_before_implementation"])
        manifest = _json(ACCEPTANCE_MANIFEST)
        self.assertEqual(manifest["contract_sha256"],
                         hashlib.sha256(ACCEPTANCE.read_bytes()).hexdigest())

    def test_proof_records_the_acceptance_contract_it_was_judged_against(self):
        self.assertEqual(_json(PROOF)["acceptance_contract_sha256"],
                         hashlib.sha256(ACCEPTANCE.read_bytes()).hexdigest())

    def test_every_zero_tolerance_code_the_contract_names_is_measured(self):
        named = set(_json(ACCEPTANCE)["acceptance_conditions"]
                    ["AC-07_static_containment_proof"]["zero_tolerance_codes"])
        measured = set(_load("av2_proof", "63_static_containment_proof_v2.py").ZERO_TOLERANCE)
        self.assertEqual(named, measured)

    def test_no_generation_retrieval_or_writes(self):
        accounting = _json(PROOF)["accounting"]
        for key in ("generation_calls", "retrieval_calls", "qdrant_writes", "corpus_reads",
                    "post_render_model_passes"):
            self.assertEqual(0, accounting[key], key)
        self.assertEqual("NONE", accounting["rendered_pilot"])
        self.assertEqual([], accounting["validators_weakened"])

    def test_no_module_in_this_phase_can_call_a_model(self):
        """Purity by inspection: nothing in the render path imports a client or opens a socket."""
        forbidden = ("openai", "anthropic", "requests", "httpx", "urllib.request", "socket",
                     "qdrant", "random", "torch", "transformers")
        for filename in ("59_semantic_plan_ir_contract_v2.py",
                         "60_claim_realization_contract_v2.py",
                         "61_turkish_morphology_v2.py",
                         "62_deterministic_surface_renderer_v2.py"):
            source = (ROOT / "scripts" / filename).read_text(encoding="utf-8")
            for name in forbidden:
                self.assertNotIn(f"import {name}", source, f"{filename}: {name}")

    def test_frozen_validators_are_byte_identical(self):
        recorded = _json(ROOT / "data/book/manifests/sec_02_2_drafting_approach_rethink_v1.json")
        rethink = _load("av2_rethink", "57_sec_02_2_drafting_approach_rethink_v1.py")
        for name, sha in recorded["frozen_inputs_sha256"].items():
            path = rethink.FROZEN_INPUTS[name]
            self.assertEqual(sha, hashlib.sha256(path.read_bytes()).hexdigest(), name)

    def test_preserved_attempts_are_unchanged(self):
        rejection = _json(ROOT / "data/book/drafting/sec_02_2/attempt_3/rejected"
                                 "/pilot_attempt_3_validation.json")
        self.assertEqual("REJECT", rejection["status"])
        self.assertFalse(rejection["repaired"])
        self.assertFalse(rejection["rendered"])

    def test_nothing_authorises_a_pilot(self):
        contract = _json(ACCEPTANCE)
        self.assertIn("ARCHITECTURE V2 PILOT #1", contract["does_not_authorise"])
        self.assertIn("no plan in this file came from a model", _json(PROOF)["note"])


if __name__ == "__main__":
    unittest.main()
