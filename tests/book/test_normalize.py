from __future__ import annotations

import json
import unittest

from tunnelbookai.book.errors import InputValidationError
from tunnelbookai.book.inputs import load_book_inputs
from tunnelbookai.book.normalize import normalize_book_inputs, parse_draft

from tests.canonical.fixtures import SyntheticRepo


DRAFT = """# Test draft

## Nasıl düzenlenir
Serbest metin.

## 1 GİRİŞ {chapter}

## 1.1 Tünelin Tanımı {keep}
[corpus: 2/1]

1. Tünel nasıl tanımlanır?
2. Tünel ile galeri arasındaki fark nedir?
3. Tünel kesitinin bölümleri nelerdir?
4. Tünel neden yapılır?
5. Tünel türleri nelerdir?

## 1.2 Eski Başlık {inactive: tez yapısı}

## 3 TARİHÇE {chapter}

## 3.1 Yeni Başlık {new}

1. Soru bir?
2. Soru iki?
3. Soru üç?
4. Soru dört?
5. Soru beş?
6. Soru altı?

## 7 BULGULAR {chapter}

## 7.1 Bulgular {keep, human-analysis}

1. Hangi veriler toplandı?
2. Sonuçlar nedir?
3. Öneriler nelerdir?
4. Sınırlılıklar nelerdir?
5. Karşılaştırma nasıl yapıldı?
"""


class NormalizeInputsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = SyntheticRepo()

    def tearDown(self) -> None:
        self.repo.close()

    def test_parse_draft_reads_tags_questions_and_modifiers(self):
        sections = parse_draft(DRAFT)
        by_id = {section.section_id: section for section in sections}
        self.assertEqual([s.section_id for s in sections], ["1", "1.1", "1.2", "3", "3.1", "7", "7.1"])
        self.assertEqual(by_id["1.2"].inactive_reason, "tez yapısı")
        self.assertFalse(by_id["1.2"].active)
        self.assertTrue(by_id["7.1"].human_analysis)
        self.assertEqual(len(by_id["3.1"].questions), 6)

    def test_normalized_inputs_load_under_v2_contract(self):
        draft = self.repo.root / "book/question_bank/drafts/test_draft.md"
        draft.write_text(DRAFT, encoding="utf-8")
        result = normalize_book_inputs(self.repo.root, draft_path="book/question_bank/drafts/test_draft.md")
        self.assertEqual(result["expected_structure"]["total_questions"], 16)
        self.assertEqual(result["expected_structure"]["question_bank_sections"], 3)
        self.assertEqual(result["expected_structure"]["inactive_headings"], 1)
        self.assertEqual(result["minimum_answered_count"], 10)
        inputs = load_book_inputs(self.repo.root)
        self.assertEqual(inputs.contract.schema_version, "2.0")
        self.assertEqual(inputs.question_section_ids, ("1.1", "3.1", "7.1"))
        self.assertTrue(inputs.requires_human_analysis("7.1"))
        self.assertFalse(inputs.requires_human_analysis("1.1"))
        self.assertEqual(inputs.contract.section_target(6), 4)
        contract = json.loads((self.repo.root / "book/config/book_contract.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["publication_policy"]["required_question_audits"], 16)
        self.assertEqual(inputs.scope_by_id["1.2"]["inactive_reason"], "tez yapısı")
        self.assertEqual(inputs.scope_by_id["3.1"]["origin"], "new")

    def test_draft_errors_fail_closed_with_line_numbers(self):
        with self.assertRaises(InputValidationError) as caught:
            parse_draft(DRAFT.replace("## 1.2 Eski Başlık {inactive: tez yapısı}", "## 1.2 Eski Başlık {inactive: tez yapısı}\n\n1. Kaçak soru?"))
        self.assertEqual(caught.exception.details["line"], 19)
        with self.assertRaises(InputValidationError):
            parse_draft(DRAFT.replace("{keep}", ""))
        with self.assertRaises(InputValidationError):
            normalize_book_inputs(self.repo.root, draft_path="book/question_bank/drafts/missing.md")


if __name__ == "__main__":
    unittest.main()
