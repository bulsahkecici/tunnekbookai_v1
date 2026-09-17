from __future__ import annotations

import unittest

from tunnelbookai.book.writer import _claims_for_questions, _validate_batch


class SectionWriterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.questions = [
            {
                "question_id": "1.1-Q01",
                "question": "Tünel nasıl tanımlanır?",
                "evidence_status": "SUPPORTED",
                "drafting_permission": "DIRECT_WITH_CITATION",
                "allowed_claim_ids": ["CLM_1"],
            },
            {
                "question_id": "1.1-Q02",
                "question": "Tanımın sınırı nedir?",
                "evidence_status": "PARTIAL",
                "drafting_permission": "LIMITED_WITH_QUALIFIER",
                "allowed_claim_ids": ["CLM_2"],
            },
        ]
        self.claims = [
            {"claim_id": "CLM_1", "claim_text": "Passage one."},
            {"claim_id": "CLM_2", "claim_text": "Passage two."},
        ]

    def test_every_sentence_is_mapped_to_known_claims_and_questions(self):
        paragraphs = _validate_batch({"paragraphs": [{"sentences": [
            {"t": "Tünel yer altında oluşturulan bir mühendislik yapısıdır.", "c": [1], "q": [1]},
            {"t": "Bu tanım mevcut kanıtta yalnızca belirli bir çerçevede ele alınmıştır.", "c": [2], "q": [2]},
        ]}]}, self.questions, self.claims)
        self.assertEqual(paragraphs[0][0]["claim_ids"], ["CLM_1"])
        self.assertEqual(paragraphs[0][1]["question_ids"], ["1.1-Q02"])

    def test_unknown_claim_reference_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "claim reference"):
            _validate_batch({"paragraphs": [{"sentences": [
                {"t": "Yeterince uzun teknik bir cümledir.", "c": [3], "q": [1, 2]},
            ]}]}, self.questions, self.claims)

    def test_omitted_question_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cover every eligible question"):
            _validate_batch({"paragraphs": [{"sentences": [
                {"t": "Yeterince uzun teknik bir cümledir.", "c": [1], "q": [1]},
            ]}]}, self.questions, self.claims)

    def test_packet_cannot_reference_unregistered_claim(self):
        with self.assertRaisesRegex(Exception, "unknown claims"):
            _claims_for_questions(self.questions, {"CLM_1": self.claims[0]})


if __name__ == "__main__":
    unittest.main()
