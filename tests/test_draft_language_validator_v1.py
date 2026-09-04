"""Draft Language Validator v1 - detection, the term/clause boundary, and failing closed.

The rule this suite defends is narrow and easy to get wrong in either direction. A Turkish
sentence that says 'shotcrete' is Turkish. An English sentence that says 'püskürtme beton' is
English. Everything here is an assertion about which side of that line a case falls on, plus the
structural claims the contract makes about itself - that the lexicons live in the artifact and
that no model is consulted.
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


lang = _load("draft_language_validator_v1", "scripts/51_draft_language_validator_v1.py")

CONTRACT = lang.build_contract("tr")

TURKISH = "Püskürtme betonun basınç dayanım sınıfı minimum C25/30 MPa sınıfında olacaktır."
ENGLISH = ("The typical thickness of an initial shotcrete lining ranges from 4 to 16 inches "
           "(100 to 400 mm).")
FAILED_UNIT = ("In some specific rock conditions, such as crushed or squeezing rock, the "
               "thickness may be 12 inches (300 mm) and more.")


def failures(text, material=True, unit_type="PARAGRAPH_SENTENCE", section_language="tr"):
    return lang.validate_unit("U-X-P01-S01", unit_type, material, section_language, text, [],
                              CONTRACT)


class Contract(unittest.TestCase):
    def test_contract_carries_every_field_the_phase_requires(self):
        for field in ("contract_version", "section_language", "allowed_visible_languages",
                      "source_claim_languages", "translation_policy", "proper_noun_policy",
                      "technical_term_policy", "failure_codes", "detector_version"):
            self.assertIn(field, CONTRACT)

    def test_the_detector_is_not_a_model(self):
        """§28. A model judge would be more fluent and would have no auditable failure mode."""
        self.assertFalse(CONTRACT["detector"]["llm_judge"])

    def test_lexicons_live_in_the_contract_not_in_the_code(self):
        """Behaviour has to be readable from an artifact, not from a diff of the detector."""
        detector = CONTRACT["detector"]
        for key in ("turkish_function_words", "english_function_words", "neutral_domain_terms",
                    "english_orthography_digraphs", "turkish_letters"):
            self.assertTrue(detector[key])

    def test_section_language_is_turkish_and_only_turkish_is_visible(self):
        self.assertEqual(CONTRACT["section_language"], "tr")
        self.assertEqual(CONTRACT["allowed_visible_languages"], ["tr"])

    def test_both_source_languages_are_permitted_as_evidence(self):
        """Half this section's claims are English. That is a fact about the corpus, not a defect."""
        self.assertEqual(sorted(CONTRACT["source_claim_languages"]), ["en", "tr"])

    def test_the_validator_never_translates(self):
        self.assertFalse(CONTRACT["enforcement"]["auto_translation_repair"])

    def test_contract_is_deterministic(self):
        """No timestamp. A freeze whose SHA moves on every re-author is not a freeze."""
        self.assertEqual(json.dumps(lang.build_contract("tr"), sort_keys=True),
                         json.dumps(lang.build_contract("tr"), sort_keys=True))


class Detection(unittest.TestCase):
    def test_turkish_technical_prose_is_turkish(self):
        self.assertEqual(lang.detect(TURKISH, CONTRACT).language, "tr")

    def test_english_prose_is_english(self):
        self.assertEqual(lang.detect(ENGLISH, CONTRACT).language, "en")

    def test_a_faithful_turkish_paraphrase_of_an_english_claim_is_turkish(self):
        text = ("İlk püskürtme beton kaplamasının tipik kalınlığı, zemin koşullarına ve tünel "
                "açıklığının boyutuna bağlı olarak 4 ila 16 inç (100 ila 400 mm) arasında "
                "değişmektedir.")
        self.assertEqual(lang.detect(text, CONTRACT).language, "tr")
        self.assertFalse(failures(text))

    def test_domain_terms_do_not_make_turkish_prose_english(self):
        """§24. shotcrete, MPa, C25/30, FHWA, TS 4559 are the vocabulary of the field."""
        for term in ("shotcrete", "flashcrete", "MPa", "C25/30", "FHWA", "TS 4559", "kg/m³"):
            text = f"Püskürtme beton uygulamasında {term} değeri dikkate alınmaktadır."
            with self.subTest(term=term):
                self.assertFalse(failures(text), term)

    def test_a_borrowed_term_is_permitted_but_a_borrowed_clause_is_not(self):
        """§27. The boundary the whole detector exists to draw."""
        self.assertFalse(failures(
            "Flashcrete, aktif destek olarak kabul edilmez ve ilk püskürtme beton kaplaması ile "
            "takip edilir."))
        self.assertTrue(failures(
            "Flashcrete is not considered an active support and is normally followed by a "
            "systematically applied initial shotcrete lining."))

    def test_reference_numbers_are_masked_rather_than_scored(self):
        detection = lang.detect("Tablo-351-5 ve TS 4559 hükümleri uygulanır.", CONTRACT)
        self.assertEqual(detection.language, "tr")


class Mismatch(unittest.TestCase):
    def test_the_pilot_unit_that_was_english_fails_as_a_language_failure(self):
        codes = {f.code for f in failures(FAILED_UNIT)}
        self.assertEqual(codes, {"LANGUAGE_MISMATCH"})

    def test_the_pilot_unit_v1_never_caught_now_fails(self):
        """U-C-P01-S02 passed all nine v1 stages. It is the reason this module exists."""
        self.assertTrue(failures(ENGLISH))

    def test_an_english_clause_inside_turkish_prose_is_a_mismatch(self):
        """§26. The unit-level score is Turkish here; only the clause pass can see the defect."""
        text = ("Kaplama kalınlığı bu bölümde ele alınmaktadır, the typical thickness of an "
                "initial shotcrete lining ranges from 100 to 400 mm, ve bu değerler tipiktir.")
        detection = lang.detect(text, CONTRACT)
        self.assertGreater(detection.unit_score["turkish"], 0)
        self.assertTrue(detection.english_clauses)
        self.assertEqual({f.code for f in failures(text)}, {"LANGUAGE_MISMATCH"})

    def test_mostly_english_with_one_turkish_term_is_still_english(self):
        text = "The thickness of the püskürtme beton lining ranges from 100 to 400 mm."
        self.assertEqual({f.code for f in failures(text)}, {"LANGUAGE_MISMATCH"})

    def test_the_failure_names_the_offending_clause(self):
        """A remediation input that says only 'wrong language' is not actionable."""
        failure = failures(FAILED_UNIT)[0]
        self.assertTrue(failure.evidence)
        self.assertEqual(failure.detected_language, "en")


class FailClosed(unittest.TestCase):
    def test_an_undetermined_material_unit_is_rejected(self):
        """§29. A material unit is an assertion; ambiguity about it is not tolerable."""
        codes = {f.code for f in failures("C25/30, 22,5 MPa, 25,5 MPa.")}
        self.assertEqual(codes, {"LANGUAGE_AMBIGUOUS"})

    def test_an_undetermined_non_material_unit_is_tolerated(self):
        """A two-word heading carries too little evidence to demand proof from."""
        self.assertFalse(failures("C25/30 / MPa", material=False, unit_type="HEADING"))

    def test_a_confidently_english_heading_is_still_rejected(self):
        self.assertTrue(failures("Shotcrete Lining Thickness and Layer Sequence in Tunnels",
                                 material=False, unit_type="HEADING"))

    def test_a_turkish_heading_passes(self):
        self.assertFalse(failures("Kaplama Kalınlığı ve Katman Düzeni", material=False,
                                  unit_type="HEADING"))


class Fixtures(unittest.TestCase):
    def test_language_scoped_fixtures_all_pass(self):
        path = ROOT / "data" / "evaluation" / "sec_02_2_draft_failure_remediation_v1.jsonl"
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()]
        cases = [r for r in rows if r.get("fixture_scope") == "language"]
        self.assertGreaterEqual(len(cases), 15)
        result = lang.run_fixtures(cases, CONTRACT)
        self.assertEqual(result["false_accepts"], [])
        self.assertEqual(result["false_rejects"], [])
        self.assertTrue(result["all_pass"])


if __name__ == "__main__":
    unittest.main()
