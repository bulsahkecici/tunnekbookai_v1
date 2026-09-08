"""Tests for the SEC-02-2 claim composition validator.

These exercise the validator directly against hand-written draft units rather than replaying the
fixture file, so a bug that was accidentally baked into both the fixtures and the validator still
surfaces here. The cases are synthetic and several are deliberately wrong; none is SEC-02-2 prose.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "book" / "sec_02_2_limitation_resolution"


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validator = _load("composition_validator_under_test",
                  "scripts/46_sec_02_2_claim_composition_validator_v1.py")


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


class ValidatorCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = validator.load_contract()
        cls.keys = {row["claim_id"]: row["source_keys"]
                    for row in read_jsonl(OUT / "claims" / "composition_safe_allowlist_v1.jsonl")}

    def check(self, claim_ids, text, *, cite=True):
        citations = {cid: self.keys.get(cid, []) for cid in claim_ids} if cite else {}
        return validator.validate(claim_ids, [text], citations, self.contract)


# ---------------------------------------------------------------- 62: CF-P0-001 qualifier

class TestMandatoryQualifier(ValidatorCase):
    def test_qualified_360_passes(self):
        result = self.check(
            ["SEC-02-2-P0-002"],
            "Tablo-308-23-b kapsamındaki genel beton için, yüksek dayanımlı beton dışında "
            "maksimum çimento miktarı 360 kg/m³'tür.")
        self.assertTrue(result.valid, result.failure_codes)

    def test_unqualified_360_fails_with_unqualified_scope(self):
        result = self.check(["SEC-02-2-P0-002"], "Maksimum çimento miktarı 360 kg/m³'tür.")
        self.assertFalse(result.valid)
        self.assertIn("UNQUALIFIED_SCOPE", result.failure_codes)

    def test_360_attributed_to_shotcrete_fails_as_ambiguous_scope(self):
        result = self.check(["SEC-02-2-P0-002"],
                            "Püskürtme beton için maksimum çimento miktarı 360 kg/m³'tür.")
        self.assertFalse(result.valid)
        self.assertIn("AMBIGUOUS_SCOPE", result.failure_codes)

    def test_the_mandatory_qualifier_text_itself_passes(self):
        """The trap. The required qualifier ends '...püskürtme beton şartnamesi değildir', so a
        wrong-scope check without negation handling would reject the form the contract mandates."""
        result = self.check(
            ["SEC-02-2-P0-002"],
            "Tablo-308-23-b, etki sınıflarına göre projelendirmede esas alınacak GENEL beton "
            "özelliklerine ilişkindir ve püskürtme beton şartnamesi değildir; bu tabloya göre "
            "maksimum çimento miktarı 360 kg/m³'tür.")
        self.assertTrue(result.valid, result.failure_codes)

    def test_mirror_misattribution_of_350_to_general_concrete_fails(self):
        result = self.check(["SEC-02-2-R001"],
                            "Genel beton için minimum çimento miktarı 350 kg/m³'tür.")
        self.assertFalse(result.valid)
        self.assertIn("AMBIGUOUS_SCOPE", result.failure_codes)

    def test_bare_shotcrete_minimum_is_permitted(self):
        """Enforcement is asymmetric on purpose: the section's subject is shotcrete, so a reader
        who supplies the missing scope for 350 supplies the right one."""
        result = self.check(["SEC-02-2-R001"],
                            "Kuru sistemde çimento miktarı 350 kg/m³'ten az olmamalıdır.")
        self.assertTrue(result.valid, result.failure_codes)

    def test_exposure_class_alone_does_not_assert_general_concrete(self):
        """'etki sınıfları' appears in Tablo-308-23-b's title AND in SEC-02-2-P0-005, a shotcrete
        durability claim. It cannot discriminate scope and must not be treated as if it could."""
        result = self.check(
            ["SEC-02-2-P0-005"],
            "Dış çevresel etki sınıfları gereksinimlerine göre püskürtme betonda belirlenen "
            "çimento miktarı, durabilite nedeniyle 350 kg/m³'ün altında kalmamalıdır.")
        self.assertTrue(result.valid, result.failure_codes)


# ---------------------------------------------------------------- 63/64/68: SYN-001

class TestForbiddenSynthesis(ValidatorCase):
    def test_historical_compound_fails(self):
        result = self.check(
            ["SEC-02-2-P0-002", "SEC-02-2-P0-003"],
            "Yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m³ olarak belirtilse "
            "de, püskürtme beton spesifikasyonlarında minimum 350/400 kg/m³ öngörülmüştür.")
        self.assertFalse(result.valid)
        self.assertIn("FORBIDDEN_SYNTHESIS", result.failure_codes)

    def test_same_sentence_fails_even_with_correct_scopes_and_no_listed_connector(self):
        """The structural half of the rule. 'iken' is in no connector list in this contract; the
        juxtaposition is the defect, so the case is caught anyway."""
        result = self.check(
            ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
            "Tablo-308-23-b kapsamındaki genel betonda maksimum 360 kg/m³ iken yaş sistem "
            "püskürtme betonda minimum 400 kg/m³ gerekmektedir.")
        self.assertFalse(result.valid)
        self.assertIn("FORBIDDEN_SYNTHESIS", result.failure_codes)

    def test_semicolon_does_not_launder_the_juxtaposition(self):
        result = self.check(
            ["SEC-02-2-P0-002", "SEC-02-2-R001"],
            "Genel betonda maksimum çimento 360 kg/m³'tür; buna rağmen kuru sistem püskürtme "
            "betonda minimum 350 kg/m³ aranır.")
        self.assertFalse(result.valid)
        self.assertIn("FORBIDDEN_SYNTHESIS", result.failure_codes)

    def test_asserted_contradiction_fails(self):
        """CF-P0-001 is a CONTEXT_DIFFERENCE, not a TRUE_CONFLICT, so no record licenses this."""
        result = self.check(
            ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
            "Tablo-308-23-b'deki 360 kg/m³ değeri ile yaş sistem için verilen 400 kg/m³ değeri "
            "çelişmektedir.")
        self.assertFalse(result.valid)
        self.assertIn("FORBIDDEN_SYNTHESIS", result.failure_codes)

    def test_english_concessive_fails(self):
        result = self.check(
            ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
            "Although the general maximum is 360 kg/m³, the wet-system shotcrete minimum is "
            "400 kg/m³.")
        self.assertFalse(result.valid)
        self.assertIn("FORBIDDEN_SYNTHESIS", result.failure_codes)

    def test_cross_sentence_connector_fails(self):
        result = self.check(
            ["SEC-02-2-P0-002", "SEC-02-2-P0-003"],
            "Genel beton için maksimum 360 kg/m³ öngörülmüştür. Buna rağmen, püskürtme beton "
            "spesifikasyonlarında kuru sistem için minimum 350 kg/m³ ve yaş sistem için minimum "
            "400 kg/m³ öngörülmüştür.")
        self.assertFalse(result.valid)
        self.assertIn("UNSUPPORTED_RELATION", result.failure_codes)

    def test_separate_scoped_sentences_pass(self):
        """The safe representation SYN-001 prescribes. If this failed, the contract would be
        forbidding the section rather than protecting it."""
        result = self.check(
            ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
            "Tablo-308-23-b kapsamındaki genel beton için maksimum çimento miktarı 360 kg/m³'tür. "
            "Yaş sistem püskürtme betonda çimento miktarı 400 kg/m³'ten az olmamalıdır.")
        self.assertTrue(result.valid, result.failure_codes)

    def test_three_scoped_claims_as_list_items_pass(self):
        result = self.check(
            ["SEC-02-2-P0-002", "SEC-02-2-R001", "SEC-02-2-P0-001"],
            "Tablo-308-23-b kapsamındaki genel beton için maksimum çimento miktarı 360 kg/m³'tür.\n"
            "- Kuru sistem püskürtme betonda minimum çimento miktarı 350 kg/m³'tür.\n"
            "- Yaş sistem püskürtme betonda minimum çimento miktarı 400 kg/m³'tür.")
        self.assertTrue(result.valid, result.failure_codes)


# ---------------------------------------------------------------- 67: 350 vs 400

class TestSourceSupportedComparison(ValidatorCase):
    def test_dry_versus_wet_comparison_passes(self):
        result = self.check(
            ["SEC-02-2-R001", "SEC-02-2-P0-001"],
            "Kuru sistem için minimum 350 kg/m³, yaş sistem için minimum 400 kg/m³ çimento "
            "dozajı aranmaktadır.")
        self.assertTrue(result.valid, result.failure_codes)

    def test_collapsing_the_system_distinction_into_a_range_fails(self):
        result = self.check(
            ["SEC-02-2-R001", "SEC-02-2-P0-001"],
            "Püskürtme betonda minimum çimento dozajı 350 kg/m³ ile 400 kg/m³ arasında "
            "değişmektedir.")
        self.assertFalse(result.valid)
        self.assertIn("AMBIGUOUS_SCOPE", result.failure_codes)

    def test_invented_interval_fails(self):
        result = self.check(["SEC-02-2-P0-003"],
                            "Püskürtme betonda çimento dozajı 350 ila 400 kg/m³ arasındadır.")
        self.assertFalse(result.valid)
        self.assertIn("FORBIDDEN_SYNTHESIS", result.failure_codes)


# ---------------------------------------------------------------- 65/66: derived numeric

class TestDerivedNumeric(ValidatorCase):
    def test_15_cm_passes(self):
        result = self.check(
            ["SEC-02-2-C-003"],
            "Bir defada uygulanacak püskürtme betonunun maksimum kalınlığı 15 cm'yi "
            "geçmeyecektir.")
        self.assertTrue(result.valid, result.failure_codes)

    def test_150_mm_attributed_to_the_source_fails(self):
        result = self.check(
            ["SEC-02-2-C-003"],
            "Kaynak, bir defada uygulanacak maksimum kalınlığı 150 mm olarak vermektedir.")
        self.assertFalse(result.valid)
        self.assertIn("DERIVED_VALUE_AS_SOURCE_STATED", result.failure_codes)

    def test_requirement_restated_in_the_derived_unit_fails(self):
        result = self.check(
            ["SEC-02-2-C-003"],
            "Bir defada uygulanacak püskürtme betonunun maksimum kalınlığı 150 mm'yi "
            "geçmeyecektir.")
        self.assertFalse(result.valid)
        self.assertIn("DERIVED_VALUE_AS_SOURCE_STATED", result.failure_codes)

    def test_source_stated_clay_zone_150_mm_still_passes(self):
        """The exemption that matters: this 150 mm IS source-stated, in a different clause with
        different provenance. A guard keyed on the string would reject a true, cited claim."""
        result = self.check(
            ["SEC-02-2-C-009"],
            "Kil zonlu tabakalar üzerine püskürtme beton uygulamasında ilk katman genellikle "
            "100-150 mm'dir.")
        self.assertTrue(result.valid, result.failure_codes)

    def test_15_cm_mesh_spacing_is_not_a_thickness_claim(self):
        result = self.check(
            ["SEC-02-2-C-017"],
            "Bir maden işletmesinde 7 mm kalınlığında ve 15 cm x 15 cm göz aralıklı çelik hasır "
            "kullanılmaktadır.")
        self.assertTrue(result.valid, result.failure_codes)


# ---------------------------------------------------------------- unit-scoped detection

class TestUnitScopedDetection(ValidatorCase):
    def test_400_mm_is_not_the_400_kg_per_m3_cement_minimum(self):
        """The regression that motivated unit-scoped matching: '4 to 16 inches (100 to 400 mm)'
        shares a numeral with the wet-system cement minimum and nothing else."""
        result = self.check(
            ["SEC-02-2-P0-007"],
            "The typical thickness of an initial shotcrete lining ranges from 4 to 16 inches "
            "(100 to 400 mm).")
        self.assertTrue(result.valid, result.failure_codes)

    def test_lining_thickness_claims_may_share_a_sentence(self):
        result = self.check(
            ["SEC-02-2-P0-007", "SEC-02-2-P0-008"],
            "The typical thickness of an initial shotcrete lining ranges from 4 to 16 inches "
            "(100 to 400 mm). In crushed or squeezing rock the thickness may be 12 inches "
            "(300 mm) and more.")
        self.assertTrue(result.valid, result.failure_codes)

    def test_mesh_bar_counts_are_not_cement_figures(self):
        result = self.check(
            ["SEC-02-2-C-013", "SEC-02-2-C-014"],
            "(R) tipi hasır çelik 15 adet boy ve 20 adet en çubuktan oluşur. (Q) tipi hasır "
            "çelik 15 adet boy ve 33 adet en çubuktan oluşur.")
        self.assertTrue(result.valid, result.failure_codes)


# ---------------------------------------------------------------- 70/71/72/73: admissibility

class TestAdmissibility(ValidatorCase):
    def test_superseded_claim_cannot_pass(self):
        result = self.check(["SEC-02-2-R003"],
                            "Genel sınırlama olarak maksimum çimento miktarı belirtilmiştir.")
        self.assertFalse(result.valid)
        self.assertIn("CLAIM_SUPERSEDED", result.failure_codes)

    def test_unsupported_claim_cannot_pass(self):
        result = self.check(["SEC-02-2-R011"],
                            "Kat sayısı ve kalınlıkları kullanılan sisteme bağlı olarak değişir.")
        self.assertFalse(result.valid)
        self.assertIn("CLAIM_UNSUPPORTED", result.failure_codes)

    def test_unknown_claim_id_cannot_pass(self):
        result = self.check(["SEC-02-2-C-999"], "Bir iddia.")
        self.assertFalse(result.valid)
        self.assertIn("CLAIM_NOT_ALLOWLISTED", result.failure_codes)

    def test_missing_citation_key_fails(self):
        result = self.check(
            ["SEC-02-2-C-001"],
            "Püskürtme betonun basınç dayanım sınıfı minimum C25/30 MPa sınıfında olacaktır.",
            cite=False)
        self.assertFalse(result.valid)
        self.assertIn("MISSING_SOURCE_KEY", result.failure_codes)

    def test_citation_key_belonging_to_another_claim_fails(self):
        result = validator.validate(
            ["SEC-02-2-C-001"],
            ["Püskürtme betonun basınç dayanım sınıfı minimum C25/30 MPa sınıfında olacaktır."],
            {"SEC-02-2-C-001": self.keys["SEC-02-2-P0-007"][:1]}, self.contract)
        self.assertFalse(result.valid)
        self.assertIn("MISSING_SOURCE_KEY", result.failure_codes)

    def test_every_allowlisted_claim_resolves_to_a_source_key(self):
        for claim_id, keys in self.keys.items():
            self.assertTrue(keys, claim_id)


# ---------------------------------------------------------------- 42: fail closed

class TestFailClosed(ValidatorCase):
    def test_multiple_independent_defects_are_all_reported(self):
        result = self.check(
            ["SEC-02-2-P0-002", "SEC-02-2-C-003"],
            "Maksimum çimento miktarı 360 kg/m³'tür. Bir defada uygulanacak maksimum kalınlık "
            "150 mm'dir.")
        self.assertFalse(result.valid)
        self.assertIn("UNQUALIFIED_SCOPE", result.failure_codes)
        self.assertIn("DERIVED_VALUE_AS_SOURCE_STATED", result.failure_codes)

    def test_result_carries_required_actions_and_never_a_rewrite(self):
        result = self.check(["SEC-02-2-P0-002"], "Maksimum çimento miktarı 360 kg/m³'tür.")
        self.assertTrue(result.required_actions)
        payload = result.as_dict()
        for forbidden in ("rewritten_text", "suggested_text", "repaired", "corrected_text"):
            self.assertNotIn(forbidden, payload)

    def test_failure_codes_come_from_the_declared_vocabulary(self):
        result = self.check(
            ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
            "Genel betonda maksimum 360 kg/m³ iken yaş sistemde minimum 400 kg/m³ gerekir.")
        for code in result.failure_codes:
            self.assertIn(code, validator.FAILURE_CODES)

    def test_validation_is_deterministic(self):
        text = ("Genel betonda maksimum 360 kg/m³ iken yaş sistemde minimum 400 kg/m³ gerekir.")
        first = self.check(["SEC-02-2-P0-002", "SEC-02-2-P0-001"], text)
        second = self.check(["SEC-02-2-P0-002", "SEC-02-2-P0-001"], text)
        self.assertEqual(first.as_dict(), second.as_dict())

    def test_empty_unit_with_valid_claims_passes(self):
        result = self.check(["SEC-02-2-C-001"], "")
        self.assertTrue(result.valid, result.failure_codes)


# ---------------------------------------------------------------- adversarial

class TestEvasionResistance(ValidatorCase):
    """Constructions no fixture enumerates.

    These exist because a rule that only catches the cases its author imagined is not a rule, it
    is a filter. Each of these joins the 360 maximum to a shotcrete minimum by a device that
    appears in no connector list in the contract; all of them are caught by the same-sentence
    prohibition, which is exactly what that prohibition is for.
    """

    CROSS_SCOPE = ["SEC-02-2-P0-002", "SEC-02-2-P0-001"]

    def assert_rejected(self, text):
        result = self.check(self.CROSS_SCOPE, text)
        self.assertFalse(result.valid, f"evasion passed: {text}")
        self.assertIn("FORBIDDEN_SYNTHESIS", result.failure_codes)

    def test_em_dash_juxtaposition(self):
        self.assert_rejected("Genel betonda maksimum 360 kg/m³ — yaş sistemde minimum "
                             "400 kg/m³.")

    def test_parenthetical_juxtaposition(self):
        self.assert_rejected("Genel betonda maksimum 360 kg/m³ (yaş sistemde minimum "
                             "400 kg/m³).")

    def test_bare_comma_list(self):
        self.assert_rejected("Maksimum 360 kg/m³, minimum 400 kg/m³.")

    def test_ise_contrast_particle(self):
        self.assert_rejected("Genel betonda maksimum 360 kg/m³, yaş sistemde ise minimum "
                             "400 kg/m³.")

    def test_interrogative_form(self):
        self.assert_rejected("Genel betonda maksimum 360 kg/m³ iken yaş sistemde neden minimum "
                             "400 kg/m³?")

    def test_unit_written_without_superscript(self):
        self.assert_rejected("Genel betonda maksimum 360 kg/m3 iken yaş sistemde minimum "
                             "400 kg/m3.")

    def test_unit_written_with_stray_spacing(self):
        self.assert_rejected("Genel betonda maksimum 360 kg / m 3 iken yaş sistemde minimum "
                             "400 kg / m 3.")

    def test_derived_value_without_a_space_before_the_unit(self):
        result = self.check(["SEC-02-2-C-003"], "Bir defada maksimum 150mm uygulanır.")
        self.assertFalse(result.valid)
        self.assertIn("DERIVED_VALUE_AS_SOURCE_STATED", result.failure_codes)

    def test_derived_value_via_passive_attribution(self):
        result = self.check(["SEC-02-2-C-003"],
                            "Maksimum kalınlık şartnamede 150 mm olarak verilmiştir.")
        self.assertFalse(result.valid)
        self.assertIn("DERIVED_VALUE_AS_SOURCE_STATED", result.failure_codes)


# ---------------------------------------------------------------- sentence splitting

class TestSentenceSplitting(unittest.TestCase):
    def test_decimals_are_not_sentence_boundaries(self):
        parts = validator.sentences("Standart çelik hasır 5.00 x 2.15 m ebadındadır.")
        self.assertEqual(len(parts), 1)

    def test_section_numbers_are_not_sentence_boundaries(self):
        parts = validator.sentences("Kısım 351.08.11 uyarınca uygulanır.")
        self.assertEqual(len(parts), 1)

    def test_semicolon_is_not_a_boundary(self):
        parts = validator.sentences("A 360 kg/m³'tür; B 400 kg/m³'tür.")
        self.assertEqual(len(parts), 1)

    def test_list_items_are_boundaries(self):
        parts = validator.sentences("Başlık:\n- Birinci madde\n- İkinci madde")
        self.assertEqual(len(parts), 3)

    def test_unit_folding_is_variant_tolerant(self):
        for variant in ("360 kg/m³", "360 kg/m3", "360 kg / m 3"):
            self.assertTrue(
                validator.figure_pattern("360", "kg/m³").search(validator.fold(variant)),
                variant)

    def test_digit_boundary_prevents_substring_matches(self):
        self.assertFalse(
            validator.figure_pattern("150", "mm").search(validator.fold("2150 mm")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
