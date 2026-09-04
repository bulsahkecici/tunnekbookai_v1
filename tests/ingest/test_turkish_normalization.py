"""Turkish text-normalization regression guard (task §13).

Two bugs of the same family have now been found in this project:

    1. `dedup.normalize_title("Bakımı") == "bak m"` — the dotless ı has no NFKD
       decomposition and was being stripped as a non-ASCII character, so Turkish title
       dedup silently failed. Fixed before this task; guarded here so it stays fixed.
    2. `classify.rules.normalize` folded "KAZI" to "kazi" but left "kazı" as "kazı", so an
       ALL-CAPS Turkish heading never matched its lowercase taxonomy term. Turkish headings
       and titles are very frequently ALL CAPS in this corpus. Fixed by this task.

Both normalizers now share one fold table (`tunnelbookai/ingest/textfold.py`), and the
tests below assert the property that made them wrong: uppercase and lowercase Turkish must
land on the same normalized form, and no Turkish letter may vanish.
"""

from __future__ import annotations

import unittest

from tunnelbookai.ingest.classify.rules import DocumentEvidence, normalize, score_sections
from tunnelbookai.ingest.classify.taxonomy import load_taxonomy
from tunnelbookai.ingest.dedup import normalize_title
from tunnelbookai.ingest.textfold import fold_turkish

# every letter §13 names, in both cases
TURKISH_LETTERS = ["ı", "İ", "i", "I", "ş", "Ş", "ğ", "Ğ", "ü", "Ü", "ö", "Ö", "ç", "Ç"]

# uppercase / lowercase pairs that must normalize identically
CASE_PAIRS = [
    ("IŞIK", "ışık"),
    ("ISPARTA", "ısparta"),
    ("İSTANBUL", "istanbul"),
    ("KAZI", "kazı"),
    ("TÜNEL BAKIMI", "tünel bakımı"),
    ("TÜNELLERİN SINIFLANDIRILMASI", "Tünellerin Sınıflandırılması"),
    ("ŞAFT AÇMA YÖNTEMİ", "şaft açma yöntemi"),
    ("GEÇİŞ ÖLÇÜMÜ", "geçiş ölçümü"),
    ("SIĞ TÜNEL", "sığ tünel"),
    ("ÇIĞ", "çığ"),
]


class FoldTableTests(unittest.TestCase):
    def test_dotted_and_dotless_i_collapse_to_one_letter(self):
        self.assertEqual(fold_turkish("ı"), "i")
        self.assertEqual(fold_turkish("İ"), "i")
        self.assertEqual(fold_turkish("i"), "i")
        self.assertEqual(fold_turkish("I"), "I")

    def test_other_turkish_letters_are_left_to_nfkd(self):
        for letter in ("ş", "ğ", "ü", "ö", "ç", "Ş", "Ğ", "Ü", "Ö", "Ç"):
            with self.subTest(letter=letter):
                self.assertEqual(fold_turkish(letter), letter)

    def test_one_shared_table_is_used_by_both_normalizers(self):
        import tunnelbookai.ingest.classify.rules as rules
        import tunnelbookai.ingest.dedup as dedup
        self.assertIs(rules.fold_turkish, dedup.fold_turkish)


class TitleNormalizationRegressionTests(unittest.TestCase):
    """Regression 1 — the dotless-ı bug in `normalize_title`."""

    def test_dotless_i_is_never_stripped(self):
        self.assertEqual(normalize_title("Bakımı"), "bakimi")
        self.assertEqual(normalize_title("  Tünel   Bakımı!  "), "tunel bakimi")
        self.assertNotIn(" m", normalize_title("Bakımı"))

    def test_every_turkish_letter_survives_normalization(self):
        for letter in TURKISH_LETTERS:
            with self.subTest(letter=letter):
                result = normalize_title(f"tunel {letter} bakim")
                self.assertNotEqual(result, "tunel bakim",
                                    f"{letter!r} was dropped instead of folded")
                self.assertEqual(len(result.split()), 3)

    def test_case_pairs_normalize_identically(self):
        for upper, lower in CASE_PAIRS:
            with self.subTest(pair=(upper, lower)):
                self.assertEqual(normalize_title(upper), normalize_title(lower))

    def test_normalized_titles_are_pure_ascii_words(self):
        for upper, _ in CASE_PAIRS:
            with self.subTest(value=upper):
                self.assertTrue(normalize_title(upper).isascii())

    def test_distinct_turkish_titles_do_not_collide(self):
        self.assertNotEqual(normalize_title("Tünel Kazısı"), normalize_title("Tünel Kaynağı"))
        self.assertNotEqual(normalize_title("sığ tünel"), normalize_title("sağ tünel"))


class DedupMatchingRegressionTests(unittest.TestCase):
    """The point of the fold: Turkish titles that differ only in case are one document."""

    def test_all_caps_and_mixed_case_titles_match(self):
        for upper, lower in CASE_PAIRS:
            with self.subTest(pair=(upper, lower)):
                self.assertTrue(normalize_title(upper))
                self.assertEqual(normalize_title(upper), normalize_title(lower))

    def test_punctuation_and_spacing_do_not_break_matching(self):
        self.assertEqual(
            normalize_title("TÜNELLERİN SINIFLANDIRILMASI"),
            normalize_title("  Tünellerin,  Sınıflandırılması!  "))


class ClassificationMatchingRegressionTests(unittest.TestCase):
    """Regression 2 — ALL-CAPS Turkish headings must match lowercase taxonomy terms."""

    def test_normalize_is_case_symmetric_for_turkish(self):
        for upper, lower in CASE_PAIRS:
            with self.subTest(pair=(upper, lower)):
                self.assertEqual(normalize(upper), normalize(lower))

    def test_uppercase_heading_contains_lowercase_term(self):
        term = "tünellerin sınıflandırılması"
        heading = "3. TÜNELLERİN SINIFLANDIRILMASI VE TASARIM ESASLARI"
        self.assertIn(normalize(term), normalize(heading))

    def test_every_turkish_taxonomy_term_matches_its_own_uppercase_form(self):
        taxonomy = load_taxonomy()
        checked = 0
        for section in taxonomy.sections.values():
            for term in list(section.strong_terms) + list(section.medium_terms):
                if not any(letter in term for letter in "ıİşğüöçIŞĞÜÖÇ"):
                    continue
                checked += 1
                with self.subTest(section=section.section_id, term=term):
                    self.assertIn(normalize(term), normalize(term.upper()))
        self.assertGreater(checked, 0, "taxonomy holds no Turkish terms to check")

    def test_all_caps_turkish_title_still_scores_its_section(self):
        taxonomy = load_taxonomy()
        term = next(
            (t for section in taxonomy.sections.values() if section.active
             for t in list(section.strong_terms) + list(section.medium_terms)
             if "ı" in t and len(t) > 8),
            None,
        )
        if term is None:
            self.skipTest("taxonomy holds no long Turkish term with a dotless i")
        lower = score_sections(DocumentEvidence(title=term, body=term), taxonomy=taxonomy)
        upper = score_sections(
            DocumentEvidence(title=term.upper(), body=term.upper()), taxonomy=taxonomy)
        self.assertTrue(lower, f"no section scored for {term!r}")
        self.assertEqual([s.section_id for s in lower], [s.section_id for s in upper])


if __name__ == "__main__":
    unittest.main()
