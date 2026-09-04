"""Tests for Book Pipeline Extractor v1.1 - materiality, propositions, clauses, numerics.

These are the behavioural contract of the extractor. Every case below is either a defect the pilot
manual audit actually found, or a control that must not regress while the defect is fixed - a
materiality rule that passes only by dropping everything is not a fix.
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "extractor_v1_1", ROOT / "scripts/42_book_pipeline_extractor_v1_1.py")
E = importlib.util.module_from_spec(_spec)
sys.modules["extractor_v1_1"] = E
_spec.loader.exec_module(E)


def result(text, language="tr"):
    return E.analyse_unit(text, language).result


def reason(text, language="tr"):
    return E.analyse_unit(text, language).reason


class TestMaterialityBug(unittest.TestCase):
    """The citation-handle digit bug: [E001] contains 001, and v1 read that as a number."""

    def test_bare_label_with_handle_is_not_a_proposition(self):
        self.assertEqual(result("* Püskürtme Beton [E001]"), "NON_PROPOSITION")
        self.assertEqual(reason("* Püskürtme Beton [E001]"), "bare_label_no_predicate")

    def test_many_handles_do_not_make_a_label_material(self):
        self.assertEqual(result("Kaya Bulonu [E100][E200][E300]"), "NON_PROPOSITION")

    def test_handles_are_stripped_before_any_numeric_test(self):
        self.assertNotIn("001", E.strip_handles("Püskürtme Beton [E001]"))
        self.assertFalse(E.has_numeric_statement(E.strip_handles("Püskürtme Beton [E001]")))

    def test_is_material_is_false_for_the_historical_defect(self):
        self.assertFalse(E.is_material("* Püskürtme Beton [E001]", "tr"))

    def test_real_numeric_claim_with_a_handle_survives(self):
        self.assertEqual(result("Püskürtme beton kalınlığı 15 cm'dir [E001]."), "PROPOSITION")


class TestBareLabels(unittest.TestCase):
    def test_historical_bare_labels_are_non_propositions(self):
        for label in ("Püskürtme Beton", "Çelik İksa", "Temel Kiriş Betonu",
                      "Şemsiye Kemer Uygulaması", "Kaya Bulonu (Saplaması)",
                      "Süren (Boru veya Demir Çubuk)", "Kaplama Betonu/Kemer Betonu/Nihai Beton"):
            with self.subTest(label=label):
                self.assertEqual(result(label), "NON_PROPOSITION", label)

    def test_qualifier_on_a_label_is_still_a_label(self):
        self.assertEqual(result("İç hasır çelik tabakası (bazı durumlarda)"), "NON_PROPOSITION")

    def test_headings_are_non_propositions(self):
        for heading in ("*1. Kat Kalınlıkları ve Uygulama Sırası:**",
                        "*3. Genel Proje ve Ekonomik Kriterler**",
                        "*RMR (Rock Mass Rating) Sınıflamasına Göre:**"):
            with self.subTest(heading=heading):
                self.assertEqual(result(heading), "NON_PROPOSITION", heading)

    def test_english_heading_is_a_non_proposition(self):
        self.assertEqual(result("*5. Specific Cost Breakdown (HS2 Example)**", "en"),
                         "NON_PROPOSITION")

    def test_english_participle_in_a_title_case_phrase_is_adjectival(self):
        self.assertEqual(result("Steel Fibre Reinforced Shotcrete", "en"), "NON_PROPOSITION")

    def test_plural_noun_is_not_a_plural_verb(self):
        # "Kriterler" is kriter+ler; "önlerler" is a verb. The suffix cannot tell them apart, so
        # the -lar/-ler family is not a predicate signal at all.
        self.assertEqual(result("Ekonomik Kriterler"), "NON_PROPOSITION")
        self.assertEqual(result("Kaya bulonları deformasyonları azaltırlar."), "PROPOSITION")

    def test_adjectival_mali_is_not_the_necessitative(self):
        self.assertEqual(result("C1 Grubu (Kaya patlamalı)"), "NON_PROPOSITION")
        self.assertEqual(result("Bu tabaka 100 mm'yi geçmemelidir."), "PROPOSITION")

    def test_lead_in_is_a_non_proposition(self):
        self.assertEqual(reason("Bu sistemin elemanları şunlardır:"), "lead_in_or_heading")
        self.assertEqual(
            reason("Delme-patlatma yöntemiyle tünel inşasında izlenen sıralama şu şekildedir:"),
            "lead_in_or_heading")

    def test_trailing_lead_in_does_not_cancel_a_preceding_assertion(self):
        self.assertEqual(
            result("The function of a membrane is to prevent groundwater inflow. "
                   "Specifically, it serves to:", "en"), "PROPOSITION")

    def test_table_blob_is_a_non_proposition(self):
        blob = "| Cost | A | B |\n|---|---|---|\n| Design | Lower | Higher |"
        self.assertEqual(reason(blob, "en"), "table_fragment")


class TestPropositionsSurvive(unittest.TestCase):
    """Fixing false positives by deleting evidence is its own failure."""

    def test_numeric_proposition_without_a_finite_verb_survives(self):
        verdict = E.analyse_unit("I. Sınıf (Çok iyi kaya): Tam kesit kazı ile 3 m ilerleme.", "tr")
        self.assertEqual(verdict.result, "PROPOSITION")
        self.assertEqual(verdict.reason, "numeric_statement")

    def test_turkish_infinitive_purpose_statements_survive(self):
        self.assertEqual(
            result("Kazılan yüzeylerin hava ve su ile temasını keserek yüzey bozunmasını "
                   "önlemek."), "PROPOSITION")

    def test_turkish_passive_aorist_survives(self):
        self.assertEqual(
            result("Açılan deliklere önceden hesaplanmış miktarda patlayıcılar yerleştirilir."),
            "PROPOSITION")

    def test_english_propositions_survive(self):
        for text in ("The value of 1.5 represents the trade-off limit between the two methods.",
                     "The specified thickness for flashcrete is typically 30 to 50 mm.",
                     "The ARAr average is between 15 - 30 meters per day."):
            with self.subTest(text=text):
                self.assertEqual(result(text, "en"), "PROPOSITION", text)

    def test_whole_pilot_population_keeps_its_propositions(self):
        notes = {n["note_id"]: n for n in E.load_original_notes()}
        rows = E.load_note_audit()
        dropped = {r["original_note_id"] for r in rows
                   if E.analyse_unit(r["original_claim"],
                                     notes[r["original_note_id"]]["claim_language"]
                                     ).result == "NON_PROPOSITION"}
        flagged = {r["original_note_id"] for r in rows
                   if r["recommended_action"] == "narrow_claim"}
        # Every fragment the auditors flagged is caught...
        self.assertEqual(flagged - dropped, set())
        # ...and the population is not gutted: most claims are still propositions.
        self.assertLess(len(dropped), len(rows) / 3)


class TestParentContextReconstruction(unittest.TestCase):
    def test_lead_in_and_heading_are_recovered(self):
        runs = E.load_runs()
        context = E.parent_context("Püskürtme Beton", runs["Q-02-1-01"]["accepted_answer"])
        self.assertIsNotNone(context)
        self.assertIn("elemanları şunlardır", context["lead_in"])
        self.assertEqual(context["heading"], "Birincil Destekleme Sistemi")

    def test_reconstruction_produces_the_documented_proposition(self):
        runs = E.load_runs()
        context = E.parent_context("Püskürtme Beton", runs["Q-02-1-01"]["accepted_answer"])
        claim = E.reconstruct_proposition("Püskürtme Beton", context, "tr")
        self.assertEqual(claim, "Püskürtme Beton, Birincil Destekleme Sistemi elemanlarından "
                                "biridir.")
        self.assertEqual(E.analyse_unit(claim, "tr").result, "PROPOSITION")

    def test_reconstruction_alone_never_confers_support(self):
        remediator = _remediator()
        reconstructed = [r for r in remediator.non_proposition_rows
                         if r["decision"] == "RECONSTRUCT_FROM_PARENT_CONTEXT"]
        self.assertTrue(reconstructed)
        for row in reconstructed:
            self.assertTrue(row["requires_support_validation"])
            self.assertEqual(row["proposition_origin"], "parent_child_reconstruction")
            self.assertIn(row["reconstruction_support_status"],
                          ("SUPPORTED", "PARTIALLY_SUPPORTED", "INSUFFICIENT_EVIDENCE"))


class TestClauseDecomposition(unittest.TestCase):
    def test_q_02_1_06_n06_decomposes_into_three(self):
        clauses = E.decompose_clauses(
            "Bu elemanlar, tünelin duraylılığını sağlamak, su geçirimsizliğini temin etmek ve "
            "işletme ekonomisi (sürtünmenin azalması) açısından gereklidir.", "tr",
            "Q-02-1-06-N06")
        self.assertEqual(len(clauses), 3)
        self.assertIn("duraylılığını", clauses[0].clause_text)
        self.assertIn("geçirimsizliğini", clauses[1].clause_text)
        self.assertIn("işletme ekonomisi", clauses[2].clause_text)

    def test_condition_label_travels_onto_every_part(self):
        clauses = E.decompose_clauses("B1 Sınıfı: Üst yarı kazısında 2,0-3,0 m, alt yarıda 4,0 m.",
                                      "tr", "N")
        self.assertEqual(len(clauses), 2)
        for clause in clauses:
            self.assertIn("B1 Sınıfı", clause.clause_text)

    def test_roman_numeral_rock_class_is_not_lost(self):
        clauses = E.decompose_clauses(
            "III. Sınıf (Orta kaya): Üst/alt yarı ayrı ayrı kazılır, 1,5-3 m'lik ilerleme.",
            "tr", "N")
        self.assertEqual(len(clauses), 2)
        for clause in clauses:
            self.assertIn("III. Sınıf", clause.clause_text)

    def test_does_not_split_inside_brackets_or_onto_subordinators(self):
        clauses = E.decompose_clauses(
            "Act as a Debonding Layer: In double-lining applications, the flexible membrane acts "
            "as a debonding layer between the initial support (e.g., shotcrete) and the final "
            "lining, which reduces shrinkage cracking in the final concrete.", "en", "N")
        self.assertEqual(len(clauses), 1)

    def test_does_not_split_a_subject_away_from_its_measurement(self):
        clauses = E.decompose_clauses(
            "Bu tabakanın tercihen kalınlığı yaklaşık 60 mm, maksimum 100 mm olmalıdır.", "tr", "N")
        self.assertEqual(len(clauses), 1)

    def test_splits_contrastive_clauses(self):
        clauses = E.decompose_clauses(
            "Çelik iksa çevre kayasına destek olur ancak kaya kütlesini güçlendirmez.", "tr", "N")
        self.assertEqual(len(clauses), 2)

    def test_does_not_split_a_conjoined_subject(self):
        clauses = E.decompose_clauses("Kaya bulonları ve püskürtme beton birlikte kullanılır.",
                                      "tr", "N")
        self.assertEqual(len(clauses), 1)


class TestSupportAggregation(unittest.TestCase):
    def test_supported_requires_every_material_clause(self):
        self.assertEqual(E.aggregate_note_status(["SUPPORTED", "SUPPORTED"]), "SUPPORTED")

    def test_compound_claim_with_one_supported_clause_is_not_supported(self):
        self.assertEqual(
            E.aggregate_note_status(["UNSUPPORTED", "UNSUPPORTED", "SUPPORTED"]),
            "PARTIALLY_SUPPORTED")

    def test_only_partial_clauses_is_not_partial_support(self):
        self.assertEqual(
            E.aggregate_note_status(["PARTIALLY_SUPPORTED", "PARTIALLY_SUPPORTED"]),
            "INSUFFICIENT_EVIDENCE")

    def test_thresholds_are_not_loosened_from_the_frozen_audit(self):
        self.assertEqual(E.CLAUSE_SUPPORTED_COVERAGE, 0.50)
        self.assertEqual(E.CLAUSE_PARTIAL_COVERAGE, 0.25)
        self.assertGreater(E.UPGRADE_COVERAGE, E.CLAUSE_SUPPORTED_COVERAGE)


class TestNumeric(unittest.TestCase):
    def test_derived_conversion_is_marked_derived(self):
        facts = E.extract_numeric("Bir defada uygulanacak püskürtme betonunun maksimum kalınlığı "
                                  "15 cm'yi (150 mm) geçmemelidir.")
        source = [f for f in facts if not f["derived"]]
        derived = [f for f in facts if f["derived"]]
        self.assertEqual([f["value"] for f in source], ["15"])
        self.assertEqual([f["value"] for f in derived], ["150"])
        self.assertEqual(derived[0]["derived_from_value"], "15")
        self.assertEqual(derived[0]["derived_from_unit"], "cm")

    def test_converted_range_is_derived_at_both_ends(self):
        facts = E.extract_numeric("The typical thickness ranges from 4 to 16 inches "
                                  "(100 to 400 mm).")
        derived = [f for f in facts if f["derived"]]
        self.assertEqual(sorted(E.numeric_literals(derived)), ["100", "400"])

    def test_ranges_keep_both_ends(self):
        facts = E.extract_numeric("Üst yarı 1,5-2,0 m ile sınırlanır.")
        self.assertEqual(facts[0]["minimum"], "1.5")
        self.assertEqual(facts[0]["maximum"], "2.0")

    def test_value_absent_from_evidence_is_not_supported(self):
        ok, missing = E.numbers_present(["360", "400"], ["minimum 350 kg/m³ olmalıdır"])
        self.assertFalse(ok)
        self.assertEqual(sorted(missing), ["360", "400"])

    def test_single_digit_enumerators_are_not_treated_as_measurements(self):
        ok, _ = E.numbers_present(["1"], ["hiçbir sayı yok"])
        self.assertTrue(ok)


class TestModalityAndConditions(unittest.TestCase):
    def test_suffixed_necessitative_is_modality(self):
        self.assertTrue(E.MODALITY_TR.search("Bu ek tabakalar üç günde tamamlanmalıdır."))

    def test_span_without_the_modality_does_not_carry_a_requirement(self):
        self.assertFalse(E.modality_preserved("tabakalar tamamlanmalıdır",
                                              "tabakalar üç günü geçmeyen bir süre", "tr"))
        self.assertTrue(E.modality_preserved("tabakalar tamamlanmalıdır",
                                             "tabakalar tamamlanmalıdır", "tr"))

    def test_non_normative_clause_is_unaffected(self):
        self.assertTrue(E.modality_preserved("çelik iksa kullanılır", "çelik iksa", "tr"))

    def test_condition_binding_requires_the_condition_near_the_span(self):
        clause = E.decompose_clauses("B1 Sınıfı: alt yarıda 4,0 m.", "tr", "N")[0]
        near = "B1 Sınıfı için ilerleme adımı: alt yarıda 4,0 m olarak sınırlanmıştır."
        far = "Genel uygulamada alt yarıda 4,0 m kullanılır." + (" x" * 500) + " B1 Sınıfı"
        self.assertTrue(E.condition_bound(clause, "alt yarıda 4,0 m", near))
        self.assertFalse(E.condition_bound(clause, "alt yarıda 4,0 m", far))


class TestCrossLingual(unittest.TestCase):
    def test_every_authored_span_resolves_in_its_frozen_chunk(self):
        notes = E.load_original_notes()
        universe = E.EvidenceUniverse(notes)
        failures = E.verify_cross_lingual_spans(universe, {n["note_id"]: n for n in notes})
        self.assertEqual(failures, [], "an authored cross-lingual span was not found in evidence")

    def test_all_eleven_cross_lingual_notes_are_mapped(self):
        self.assertEqual(len(E.CROSS_LINGUAL_MAPPINGS), 11)

    def test_mapping_statuses_are_from_the_allowed_set(self):
        for entries in E.CROSS_LINGUAL_MAPPINGS.values():
            for entry in entries:
                self.assertIn(entry["status"], E.CROSS_LINGUAL_STATUSES)
                self.assertTrue(entry["translator_note"].strip())

    def test_lexical_overlap_can_never_upgrade_a_cross_lingual_clause(self):
        clause = E.decompose_clauses("Karar noktası 3-5 km civarındadır.", "tr", "N")[0]
        computed = {"status": "SUPPORTED", "coverage": 1.0, "span": "3-5 km",
                    "numeric_ok": True, "derived_unsupported": []}
        self.assertFalse(E.upgrade_allowed(clause, computed, cross_lingual=True))

    def test_moved_threshold_is_recorded_as_unsupported(self):
        entries = E.CROSS_LINGUAL_MAPPINGS["Q-02-3-01-N03"]
        moved = [e for e in entries if "1,5'in altındaysa" in e["clause"]]
        self.assertEqual(len(moved), 1)
        self.assertEqual(moved[0]["status"], "NOT_SUPPORTED")


class TestRegressionSuite(unittest.TestCase):
    def test_suite_is_large_enough_and_covers_the_required_categories(self):
        cases = E.build_regression_suite(_remediator())
        self.assertGreaterEqual(len(cases), 50)
        categories = {c["category"] for c in cases}
        for required in ("bare_label", "citation_handle_digits", "heading", "numeric_proposition",
                         "compound_claim", "cross_lingual", "requirement", "table_fragment",
                         "short_proposition"):
            self.assertIn(required, categories, required)

    def test_suite_passes(self):
        result = E.run_regression(E.build_regression_suite(_remediator()))
        self.assertEqual(result["failed"], 0, result["failures"])

    def test_materiality_targets_are_zero(self):
        cases = E.build_regression_suite(_remediator())
        failures = E.run_regression(cases)["failures"]
        ids = {f["case_id"] for f in failures}
        for case in cases:
            if case["case_type"] != "materiality":
                continue
            if case["expected_result"] == "NON_PROPOSITION":
                self.assertNotIn(case["case_id"], ids, "a label became material")
            else:
                self.assertNotIn(case["case_id"], ids, "a real proposition was dropped")


_CACHE = {}


def _remediator():
    if "r" not in _CACHE:
        _CACHE["r"] = E.Remediator().run()
    return _CACHE["r"]


if __name__ == "__main__":
    unittest.main()
