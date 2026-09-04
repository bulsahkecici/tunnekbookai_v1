"""Section Draft Validator v1 - schema, stages, and the delegation boundary.

Two things get asserted here that the contract tests do not reach:

**The schema is strict.** A DraftIR with a missing `material` flag must raise, not default to
False, because a unit that defaults to non-material is prose that was never support-checked and
carries no visible sign of it.

**Delegation is real.** Stage F calls the frozen composition validator; it does not re-implement
it. The test for that compares the two modules' verdicts on the same input rather than trusting
the call site, because a re-implementation would still pass a call-site test.
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


validator = _load("section_draft_validator_v1", "scripts/49_section_draft_validator_v1.py")
composition = _load("composition_validator_v1",
                    "scripts/46_sec_02_2_claim_composition_validator_v1.py")

KTS = "SRC-DOC000236-8dfa5f799b50"
KGM = "SRC-DOC000087-8d778c37de30"


def raw_unit(**over):
    base = {"unit_id": "U-A-P01-S01", "unit_type": "PARAGRAPH_SENTENCE",
            "text": "Püskürtme betonun basınç dayanım sınıfı minimum C25/30 sınıfındadır.",
            "material": True, "claim_ids": ["SEC-02-2-C-001"], "source_keys": [KTS],
            "relationship_type": "INDEPENDENT",
            "citation_intents": [{"claim_id": "SEC-02-2-C-001", "source_keys": [KTS]}]}
    base.update(over)
    return base


def raw_ir(*units, **over):
    base = {"section_id": "SEC-02-2", "draft_id": "T", "draft_version": "v1", "language": "tr",
            "title": "Püskürtme Beton", "units": list(units) or [raw_unit()]}
    base.update(over)
    return base


class Schema(unittest.TestCase):
    def test_a_valid_draft_parses(self):
        ir = validator.parse_draft_ir(raw_ir())
        self.assertEqual(ir.section_id, "SEC-02-2")
        self.assertEqual(len(ir.units), 1)
        self.assertTrue(ir.units[0].material)

    def test_a_json_string_parses(self):
        ir = validator.parse_draft_ir(json.dumps(raw_ir(), ensure_ascii=False))
        self.assertEqual(ir.draft_id, "T")

    def test_invalid_json_raises_rather_than_being_repaired(self):
        with self.assertRaises(validator.DraftSchemaError):
            validator.parse_draft_ir("{not json")

    def test_a_missing_material_flag_raises(self):
        """Defaulting it to False would produce prose nothing support-checked."""
        unit = raw_unit()
        del unit["material"]
        with self.assertRaises(validator.DraftSchemaError):
            validator.parse_draft_ir(raw_ir(unit))

    def test_every_required_top_level_field_is_required(self):
        for field in ("section_id", "draft_id", "draft_version", "language", "title", "units"):
            with self.subTest(field=field):
                payload = raw_ir()
                del payload[field]
                with self.assertRaises(validator.DraftSchemaError):
                    validator.parse_draft_ir(payload)

    def test_a_wrong_section_id_raises(self):
        with self.assertRaises(validator.DraftSchemaError):
            validator.parse_draft_ir(raw_ir(section_id="SEC-03-1"))

    def test_an_unknown_unit_type_raises(self):
        with self.assertRaises(validator.DraftSchemaError):
            validator.parse_draft_ir(raw_ir(raw_unit(unit_type="FOOTNOTE")))

    def test_a_forbidden_relationship_type_raises(self):
        for relationship in ("FORBIDDEN_SYNTHESIS", "UNKNOWN_RELATION"):
            with self.subTest(relationship=relationship):
                with self.assertRaises(validator.DraftSchemaError):
                    validator.parse_draft_ir(raw_ir(raw_unit(relationship_type=relationship)))

    def test_a_malformed_unit_id_raises(self):
        for unit_id in ("U-A-1-1", "unit-1", "U-A-P1-S1", "U-A-P01"):
            with self.subTest(unit_id=unit_id):
                with self.assertRaises(validator.DraftSchemaError):
                    validator.parse_draft_ir(raw_ir(raw_unit(unit_id=unit_id)))

    def test_duplicate_unit_ids_raise(self):
        with self.assertRaises(validator.DraftSchemaError):
            validator.parse_draft_ir(raw_ir(raw_unit(), raw_unit()))

    def test_an_empty_unit_list_raises(self):
        with self.assertRaises(validator.DraftSchemaError):
            validator.parse_draft_ir(raw_ir(units=[]))

    def test_paragraph_id_is_recoverable_from_unit_id(self):
        ir = validator.parse_draft_ir(raw_ir(raw_unit(unit_id="U-B-P02-S07")))
        self.assertEqual(ir.units[0].paragraph_id, "U-B-P02")


class Primitives(unittest.TestCase):
    def test_turkish_dotted_i_folds_before_lowercasing(self):
        """Python's str.lower() turns 'İ' into 'i' plus a combining dot, which then mismatches."""
        self.assertEqual(validator.fold("İlk Tabaka"), "ilk tabaka")
        self.assertIn("ilk", validator.tokens("İlk tabaka ince olmalıdır"))

    def test_prefix_agreement_crosses_the_k_to_g_mutation(self):
        self.assertTrue(validator.prefix_agreement("kalınlık", "kalınlığı"))
        self.assertTrue(validator.prefix_agreement("beton", "betonun"))
        self.assertFalse(validator.prefix_agreement("ekonomik", "beton"))

    def test_short_tokens_need_exact_agreement(self):
        self.assertFalse(validator.prefix_agreement("kil", "kile"))
        self.assertTrue(validator.prefix_agreement("kil", "kil"))

    def test_table_and_clause_numbers_are_not_read_as_quantities(self):
        self.assertEqual(validator.extract_numerics("Tablo-351-5 ve §351.08.10.02"), [])
        self.assertEqual(validator.extract_numerics("C25/30 sınıfı"), [])

    def test_ranges_are_expanded_into_their_endpoints(self):
        found = dict(validator.extract_numerics("yaklaşık 3-5 saattir"))
        self.assertEqual(found["3-5"], "saat")
        self.assertEqual(found["3"], "saat")
        self.assertEqual(found["5"], "saat")

    def test_word_ranges_are_read_too(self):
        found = validator.extract_numerics("4 ila 16 inç (100 ila 400 mm)")
        self.assertIn(("16", "inches"), found)
        self.assertIn(("4", "inches"), found)
        self.assertIn(("400", "mm"), found)

    def test_turkish_suffixes_do_not_hide_a_unit(self):
        self.assertIn(("3-5", "saat"), validator.extract_numerics("3-5 saattir"))
        self.assertIn(("150", "mm"), validator.extract_numerics("150 mm'dir"))

    def test_a_digit_boundary_stops_a_substring_match(self):
        self.assertNotIn(("150", "mm"), validator.extract_numerics("2150 mm"))

    def test_a_short_marker_needs_a_word_boundary(self):
        """'zor' must not match inside 'zorundadır', which is a modality, not an evaluation."""
        self.assertFalse(validator._marker_present("zor", "olmak zorundadır"))
        self.assertTrue(validator._marker_present("zor", "bu zor bir uygulamadır"))

    def test_a_long_marker_may_carry_a_suffix(self):
        self.assertTrue(validator._marker_present("ekonomik", "en ekonomiktir"))


class Registry(unittest.TestCase):
    def test_the_union_covers_keys_from_both_frozen_registries(self):
        """The 360 kg/m³ claim's provenance lives only in the P0 registry."""
        registry = validator.load_source_registry()
        self.assertIn("SRC-DOC000236-4bfaac5ac12c", registry)
        self.assertIn("SRC-DOC000087-7646b05ab1bd", registry)
        self.assertIn(KTS, registry)

    def test_every_allowlisted_claims_source_keys_resolve(self):
        registry = validator.load_source_registry()
        allowlist = validator._read_jsonl(validator.ALLOWLIST_PATH)
        missing = sorted({key for row in allowlist for key in row["source_keys"]
                          if key not in registry})
        self.assertEqual(missing, [])


class Delegation(unittest.TestCase):
    """Stage F must call the frozen validator, not carry its own copy of the rules."""

    @classmethod
    def setUpClass(cls):
        cls.bundle = validator.load_bundle()

    def test_composition_verdicts_agree_with_the_frozen_validator(self):
        cases = [
            ("Maksimum çimento miktarı 360 kg/m³'tür.", ["SEC-02-2-P0-002"]),
            ("Tablo-308-23-b'ye göre genel betonda maksimum çimento miktarı 360 kg/m³ olmasına "
             "rağmen kuru sistemde minimum 350 kg/m³ aranmaktadır.",
             ["SEC-02-2-P0-002", "SEC-02-2-R001"]),
            ("Bir defada uygulanacak kalınlık 150 mm'yi geçmeyecektir.", ["SEC-02-2-C-003"]),
        ]
        for text, claim_ids in cases:
            with self.subTest(text=text[:40]):
                keys = {c: validator.load_bundle().allowlist[c]["source_keys"] for c in claim_ids}
                direct = composition.validate(claim_ids, [text], keys,
                                              self.bundle.composition_contract)
                unit = validator.DraftUnit(
                    unit_id="U-A-P01-S01", unit_type="PARAGRAPH_SENTENCE", text=text,
                    material=True, claim_ids=claim_ids,
                    source_keys=sorted({k for v in keys.values() for k in v}),
                    citation_intents=[{"claim_id": c, "source_keys": v}
                                      for c, v in keys.items()])
                staged = validator.stage_f_composition(unit, text, self.bundle)
                expected = {validator.COMPOSITION_CODE_MAP.get(code, code)
                            for code in direct.failure_codes}
                self.assertEqual({f.code for f in staged}, expected)

    def test_the_frozen_composition_regression_still_passes(self):
        fixtures = validator._read_jsonl(
            ROOT / "data" / "evaluation" / "sec_02_2_claim_composition_v1.jsonl")
        result = composition.run_fixtures(fixtures, self.bundle.composition_contract)
        self.assertEqual(result["total"], 71)
        self.assertTrue(result["all_pass"])
        self.assertEqual(result["false_accepts"], [])
        self.assertEqual(result["false_rejects"], [])


class DraftLevel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = validator.load_bundle()

    def test_one_rejected_unit_rejects_the_whole_draft(self):
        ir = validator.parse_draft_ir(raw_ir(
            raw_unit(),
            raw_unit(unit_id="U-A-P01-S02",
                     text="Bu yöntem her koşulda en ekonomik çözümdür.")))
        result = validator.validate_draft(ir, self.bundle)
        self.assertEqual(result.status, "REJECT")
        self.assertEqual(result.rejected_unit_ids, ["U-A-P01-S02"])
        self.assertEqual(ir.units[0].validation_status, "ACCEPT")

    def test_a_clean_draft_is_accepted(self):
        ir = validator.parse_draft_ir(raw_ir())
        result = validator.validate_draft(ir, self.bundle)
        self.assertEqual(result.status, "ACCEPT", result.failure_histogram)

    def test_paragraph_scope_is_grouped_by_unit_id(self):
        ir = validator.parse_draft_ir(raw_ir(
            raw_unit(unit_id="U-A-P01-S01"),
            raw_unit(unit_id="U-A-P01-S02",
                     text="Bir defada uygulanacak kalınlık 15 cm'yi geçmeyecektir.",
                     claim_ids=["SEC-02-2-C-003"], source_keys=[KGM],
                     citation_intents=[{"claim_id": "SEC-02-2-C-003", "source_keys": [KGM]}]),
            raw_unit(unit_id="U-B-P01-S01")))
        paragraphs = validator.paragraph_texts(ir)
        self.assertEqual(set(paragraphs), {"U-A-P01", "U-B-P01"})
        self.assertIn("15 cm", paragraphs["U-A-P01"])

    def test_every_rejection_code_is_declared(self):
        contract = json.loads(
            (ROOT / "data" / "book" / "drafting" / "contracts"
             / "draft_validation_contract_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(set(contract["rejection_codes"]), set(validator.REJECTION_CODES))


if __name__ == "__main__":
    unittest.main()
