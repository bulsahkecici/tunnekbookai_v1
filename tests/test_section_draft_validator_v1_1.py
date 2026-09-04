"""Section Draft Validator v1.1 - inheritance, the two new stages, and the no-weakening promise.

The load-bearing claim of this phase is that v1.1 is v1 plus two rules, never v1 minus anything.
That claim is not asserted here, it is tested three ways: v1's file is unchanged on disk, every
one of v1's codes and stages survives into v1.1, and all 107 of v1's fixtures still score
identically. A remediation that quietly relaxed a threshold would pass a hand-written assertion
about its own intent and fail these.

The rest is the new behaviour: an English unit fails as a language failure rather than by
accident, and a claim whose scope is a design table cannot be drafted as the source of the
requirement the table tests.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


v1 = _load("section_draft_validator_v1", "scripts/49_section_draft_validator_v1.py")
v11 = _load("section_draft_validator_v1_1", "scripts/52_section_draft_validator_v1_1.py")
lang = _load("draft_language_validator_v1", "scripts/51_draft_language_validator_v1.py")

FIXTURES = ROOT / "data" / "evaluation" / "sec_02_2_draft_failure_remediation_v1.jsonl"
V1_FIXTURES = ROOT / "data" / "evaluation" / "section_drafting_contract_v1.jsonl"
CONSTRAINTS_PATH = (ROOT / "data" / "book" / "drafting" / "sec_02_2" / "remediation_v1"
                    / "contracts" / "draft_semantic_constraints_v1.json")

KGM_C002 = "SRC-DOC000087-ea64db4f1a7f"
KTS_C001 = "SRC-DOC000236-8dfa5f799b50"
FHWA_C = "SRC-DOC000047-d5c60204e247"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def bundle():
    return v11.load_bundle()


def constraints():
    return v11.load_semantic_constraints()


def unit(text, claims, keys, material=True, unit_type="PARAGRAPH_SENTENCE"):
    return v11.DraftUnit(
        unit_id="U-X-P01-S01", unit_type=unit_type, text=text, material=material,
        claim_ids=list(claims), source_keys=list(keys), relationship_type="INDEPENDENT",
        citation_intents=[{"claim_id": c, "source_keys": list(keys)} for c in claims])


def codes(text, claims, keys, paragraph=None, material=True, unit_type="PARAGRAPH_SENTENCE",
          section_language="tr"):
    u = unit(text, claims, keys, material, unit_type)
    failures = v11.validate_unit(u, paragraph or text, bundle(), section_language,
                                 lang.load_contract(), constraints())
    return sorted({f.code for f in failures})


class NoWeakening(unittest.TestCase):
    def test_v1_is_still_on_disk_unmodified(self):
        manifest = json.loads((ROOT / "data" / "book" / "manifests"
                               / "section_drafting_contract_v1.json").read_text(encoding="utf-8"))
        import hashlib
        actual = hashlib.sha256(
            (ROOT / "scripts" / "49_section_draft_validator_v1.py").read_bytes()).hexdigest()
        self.assertEqual(actual, manifest["draft_validator_sha"])

    def test_every_v1_rejection_code_survives(self):
        """Dropping a code would silently retire every fixture that depended on it."""
        for code in v1.REJECTION_CODES:
            self.assertIn(code, v11.REJECTION_CODES)

    def test_every_v1_stage_survives(self):
        for stage in v1.STAGES:
            self.assertIn(stage, v11.STAGES)

    def test_only_the_three_declared_codes_are_added(self):
        added = [c for c in v11.REJECTION_CODES if c not in v1.REJECTION_CODES]
        self.assertEqual(added, ["LANGUAGE_MISMATCH", "LANGUAGE_AMBIGUOUS",
                                 "SEMANTIC_SCOPE_MISMATCH"])

    def test_language_runs_before_any_accept(self):
        """§34. Ordering is declared, and the declaration has to match the module."""
        order = list(v11.STAGES)
        self.assertLess(order.index("J_language"), order.index("F_composition"))
        self.assertIn("K_semantic", order)

    def test_all_107_v1_fixtures_score_identically_under_v1_1(self):
        rows = [dict(f, fixture_scope="draft", section_language="tr")
                for f in read_jsonl(V1_FIXTURES)]
        result = v11.run_fixtures(rows, bundle(), lang.load_contract(), constraints())
        self.assertEqual(result["false_accepts"], [])
        self.assertEqual(result["false_rejects"], [])
        self.assertEqual(result["code_mismatches"], [])
        self.assertTrue(result["all_pass"])

    def test_v1_1_rejects_everything_v1_rejects(self):
        """A unit v1 refuses cannot become acceptable by being run through the newer validator."""
        for fixture in read_jsonl(V1_FIXTURES):
            if fixture["expected_valid"]:
                continue
            u = unit(fixture["text"], fixture.get("claim_ids", []),
                     fixture.get("source_keys", []), fixture.get("material", True),
                     fixture.get("unit_type", "PARAGRAPH_SENTENCE"))
            u.citation_intents = list(fixture.get("citation_intents", []))
            u.relationship_type = fixture.get("relationship_type", "INDEPENDENT")
            paragraph = fixture.get("paragraph_text") or u.text
            with self.subTest(case=fixture["case_id"]):
                self.assertTrue(v11.validate_unit(u, paragraph, bundle(), "tr",
                                                  lang.load_contract(), constraints()))


class LanguageStage(unittest.TestCase):
    def test_an_english_material_unit_fails_as_a_language_failure(self):
        text = ("The typical thickness of an initial shotcrete lining ranges from 4 to 16 inches "
                "(100 to 400 mm).")
        self.assertIn("LANGUAGE_MISMATCH",
                      codes(text, ["SEC-02-2-P0-007"],
                            ["SRC-DOC000047-72f96c5daace", "SRC-DOC000047-838e92811f43"]))

    def test_a_faithful_turkish_rendering_of_the_same_claim_passes(self):
        text = ("Ezilmiş veya sıkışan kaya gibi bazı kaya koşullarında, tünel boyutuna bağlı "
                "olarak kalınlık 12 inç (300 mm) ve daha fazla olabilmektedir.")
        self.assertEqual(codes(text, ["SEC-02-2-P0-008"], [FHWA_C]), [])

    def test_dropping_the_tunnel_size_condition_is_a_condition_failure(self):
        text = ("Ezilmiş veya sıkışan kaya gibi bazı kaya koşullarında kalınlık 12 inç (300 mm) "
                "ve daha fazla olabilmektedir.")
        self.assertIn("CONDITION_DROPPED", codes(text, ["SEC-02-2-P0-008"], [FHWA_C]))

    def test_the_condition_check_does_not_require_english_words(self):
        """§49. A Turkish paraphrase cannot retain an English anchor and must not have to."""
        text = ("Ezilmiş veya sıkışan kaya gibi bazı kaya koşullarında, tünel boyutuna bağlı "
                "olarak kalınlık 12 inç (300 mm) ve daha fazla olabilmektedir.")
        self.assertNotIn("tunnel", text.lower())
        self.assertEqual(codes(text, ["SEC-02-2-P0-008"], [FHWA_C]), [])

    def test_language_is_taken_from_the_draft_not_assumed(self):
        ir = v11.parse_draft_ir({
            "section_id": "SEC-02-2", "draft_id": "T", "draft_version": "v1", "language": "tr",
            "title": "T", "units": [{
                "unit_id": "U-A-P01-S01", "unit_type": "PARAGRAPH_SENTENCE",
                "text": "In some specific rock conditions the thickness may be more.",
                "material": True, "claim_ids": ["SEC-02-2-P0-008"], "source_keys": [FHWA_C],
                "citation_intents": [{"claim_id": "SEC-02-2-P0-008", "source_keys": [FHWA_C]}]}]})
        result = v11.validate_draft(ir, bundle(), lang.load_contract(), constraints())
        self.assertEqual(result.status, "REJECT")
        self.assertIn("LANGUAGE_MISMATCH", result.failure_codes)


class SemanticStage(unittest.TestCase):
    def test_the_constraint_registry_is_frozen_and_declares_both_meanings(self):
        payload = json.loads(CONSTRAINTS_PATH.read_text(encoding="utf-8"))
        constraint = payload["constraints"][0]
        self.assertEqual(constraint["constraint_id"], "DSC-C002-001")
        self.assertEqual(constraint["claim_id"], "SEC-02-2-C-002")
        self.assertEqual(constraint["type"], "QUALIFIER_PRESERVATION")
        self.assertIn("acceptance criteria", constraint["required_meaning"])
        self.assertIn("establishes or defines", constraint["forbidden_meaning"])

    def test_acceptance_values_without_the_qualifier_are_rejected(self):
        text = ("Tablo-351-5'e göre C25/30 sınıfı püskürtme betonda 28 günlük karot numunelerde "
                "bireysel minimum dayanım 22,5 MPa'dır.")
        u = unit(text, ["SEC-02-2-C-002"], [KGM_C002])
        failures = v11.stage_k_semantic(u, text, bundle(), constraints())
        self.assertEqual({f.code for f in failures}, {"QUALIFIER_DROPPED"})

    def test_the_qualifier_may_live_in_a_neighbouring_sentence(self):
        """A qualifier is outside the claim's own sentence by definition; the scope follows that."""
        text = "Bireysel minimum dayanım 22,5 MPa'dır."
        paragraph = ("Tablo-351-5, C25/30 sınıfı püskürtme betona ait 28 günlük karot "
                     "numunelerinin kabul kriterlerini verir. " + text)
        u = unit(text, ["SEC-02-2-C-002"], [KGM_C002])
        self.assertEqual(v11.stage_k_semantic(u, paragraph, bundle(), constraints()), [])

    def test_presenting_the_table_as_the_source_of_the_class_is_rejected(self):
        text = "Tablo-351-5'e göre püskürtme betonun minimum dayanım sınıfı C25/30'dur."
        u = unit(text, ["SEC-02-2-C-002"], [KGM_C002])
        failures = v11.stage_k_semantic(u, text, bundle(), constraints())
        self.assertIn("SEMANTIC_SCOPE_MISMATCH", {f.code for f in failures})

    def test_the_claims_own_canonical_wording_is_not_the_forbidden_meaning(self):
        """Self-consistency: a rule that rejects the source's own sentence is broken, not strict."""
        allowlist = {row["claim_id"]: row for row in read_jsonl(
            ROOT / "data" / "book" / "sec_02_2_limitation_resolution" / "claims"
            / "composition_safe_allowlist_v1.jsonl")}
        canonical = allowlist["SEC-02-2-C-002"]["canonical_claim"]
        u = unit(canonical, ["SEC-02-2-C-002"], [KGM_C002])
        failures = v11.stage_k_semantic(u, canonical, bundle(), constraints())
        self.assertNotIn("SEMANTIC_SCOPE_MISMATCH", {f.code for f in failures})

    def test_the_class_requirement_claim_itself_is_untouched_by_the_rule(self):
        text = "Püskürtme betonun basınç dayanım sınıfı minimum C25/30 MPa sınıfında olacaktır."
        self.assertEqual(codes(text, ["SEC-02-2-C-001"], [KTS_C001]), [])

    def test_the_rule_is_keyed_on_scope_not_on_the_pilots_wording(self):
        """§11. No executable string in the validator carries the pilot's sentence.

        Docstrings are excluded deliberately: explaining which sentence motivated a rule is how a
        reader understands it, and the prohibition is against *matching* on that sentence. So the
        check walks the AST and looks at the literals the code actually evaluates.
        """
        import ast
        tree = ast.parse((ROOT / "scripts" / "52_section_draft_validator_v1_1.py")
                         .read_text(encoding="utf-8"))
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                doc = ast.get_docstring(node, clean=False)
                if doc:
                    docstrings.add(doc)
        literals = [n.value for n in ast.walk(tree)
                    if isinstance(n, ast.Constant) and isinstance(n.value, str)
                    and n.value not in docstrings]
        for literal in literals:
            self.assertNotIn("22,5", literal)
            self.assertNotIn("351-5", literal)
        constraint = constraints()[0]
        self.assertEqual(constraint["requirement_scope_marker"], "design_table")

    def test_removing_the_constraint_removes_the_rule(self):
        """The behavioural form of the same claim: the rule lives in the registry, not the code."""
        text = "Tablo-351-5'e göre püskürtme betonun minimum dayanım sınıfı C25/30'dur."
        u = unit(text, ["SEC-02-2-C-002"], [KGM_C002])
        self.assertTrue(v11.stage_k_semantic(u, text, bundle(), constraints()))
        self.assertEqual(v11.stage_k_semantic(u, text, bundle(), []), [])

    def test_a_constraint_only_binds_a_claim_whose_scope_matches(self):
        stale = dict(constraints()[0], claim_id="SEC-02-2-C-001")
        u = unit("Tablo-351-5'e göre dayanım sınıfı C25/30'dur.", ["SEC-02-2-C-001"], [KTS_C001])
        self.assertEqual(v11.stage_k_semantic(u, u.text, bundle(), [stale]), [])


class Mappings(unittest.TestCase):
    def test_every_registered_rendering_is_licensed_by_the_frozen_contract(self):
        """§50. A mapping able to introduce new anchors would be a loosening in disguise."""
        check = v11.mapping_consistency(bundle())
        self.assertTrue(check["consistent"], check["unlicensed_anchors"])
        self.assertGreaterEqual(check["mapping_count"], 3)

    def test_mappings_are_declared_rather_than_derived_at_runtime(self):
        payload = json.loads(v11.CROSS_LINGUAL_PATH.read_text(encoding="utf-8"))
        self.assertFalse(payload["policy"]["runtime_invention"])
        mapping = next(m for m in payload["mappings"]
                       if m["source_condition"] == "dependent on tunnel size")
        self.assertIn("tünel boyutuna bağlı olarak", mapping["approved_target_renderings"])
        for field in ("numeric_invariants", "modality_invariants", "scope_invariants",
                      "source_keys"):
            self.assertIn(field, mapping)


class Fixtures(unittest.TestCase):
    def test_the_remediation_fixture_set_passes_whole(self):
        rows = read_jsonl(FIXTURES)
        self.assertGreaterEqual(len(rows), 40)
        result = v11.run_fixtures(rows, bundle(), lang.load_contract(), constraints())
        self.assertEqual(result["false_accepts"], [])
        self.assertEqual(result["false_rejects"], [])
        self.assertEqual(result["code_mismatches"], [])
        self.assertEqual(result["language_false_accepts"], [])
        self.assertEqual(result["language_false_rejects"], [])
        self.assertTrue(result["all_pass"])

    def test_the_set_carries_both_polarities_in_quantity(self):
        result = v11.run_fixtures(read_jsonl(FIXTURES), bundle(), lang.load_contract(),
                                  constraints())
        self.assertGreaterEqual(result["positive"], 15)
        self.assertGreaterEqual(result["negative"], 15)

    def test_corrected_synthetics_of_both_failed_units_pass(self):
        rows = [f for f in read_jsonl(FIXTURES) if f.get("category") == "corrected_synthetic"]
        self.assertEqual(len(rows), 2)
        result = v11.run_fixtures(rows, bundle(), lang.load_contract(), constraints())
        self.assertTrue(result["all_pass"])
        self.assertEqual(result["positive"], 2)


if __name__ == "__main__":
    unittest.main()
