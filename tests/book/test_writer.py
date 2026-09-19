from __future__ import annotations

import unittest

from tunnelbookai.book.writer import _claims_for_questions, _link_questions, _validate_batch, _validate_plan


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
            {"claim_id": "CLM_1", "claim_text": "Passage one.", "supporting_question_ids": ["1.1-Q01"]},
            {"claim_id": "CLM_2", "claim_text": "Passage two.", "supporting_question_ids": ["1.1-Q02"]},
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

    def test_question_tags_are_optional_unless_strict_coverage_is_requested(self):
        paragraphs = _validate_batch({"paragraphs": [{"sentences": [
            {"t": "Yeterince uzun teknik bir cümledir.", "c": [2], "q": []},
        ]}]}, self.questions, self.claims)
        self.assertEqual(paragraphs[0][0]["question_ids"], [])
        claim_by_id = {row["claim_id"]: row for row in self.claims}
        linked = _link_questions(paragraphs[0][0], claim_by_id, ["1.1-Q01", "1.1-Q02"])
        self.assertEqual(linked, ["1.1-Q02"])
        with self.assertRaisesRegex(ValueError, "cover every eligible question"):
            _validate_batch({"paragraphs": [{"sentences": [
                {"t": "Yeterince uzun teknik bir cümledir.", "c": [1], "q": [1]},
            ]}]}, self.questions, self.claims, require_question_coverage=True)

    def test_plan_requires_valid_theme_references(self):
        themes = _validate_plan({"themes": [
            {"title": "Tanım", "c": [1], "q": [1]},
            {"title": "Sınırlar", "c": [2], "q": []},
        ]}, self.questions, self.claims)
        self.assertEqual(themes[0]["claim_ids"], ["CLM_1"])
        self.assertEqual(themes[1]["question_ids"], [])
        with self.assertRaisesRegex(ValueError, "theme claim reference"):
            _validate_plan({"themes": [{"title": "Tema A", "c": [9], "q": []}, {"title": "Tema B", "c": [1], "q": []}]}, self.questions, self.claims)
        with self.assertRaisesRegex(ValueError, "duplicate theme titles"):
            _validate_plan({"themes": [{"title": "Tema A", "c": [1], "q": []}, {"title": "tema a", "c": [2], "q": []}]}, self.questions, self.claims)

    def test_packet_cannot_reference_unregistered_claim(self):
        with self.assertRaisesRegex(Exception, "unknown claims"):
            _claims_for_questions(self.questions, {"CLM_1": self.claims[0]})


if __name__ == "__main__":
    unittest.main()
