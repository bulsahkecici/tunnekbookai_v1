from __future__ import annotations

import unittest

from tunnelbookai.book.errors import BookEngineError
from tunnelbookai.book.revision import _plan_revision


class SectionRevisionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sentence_map = {
            "section_id": "1.1",
            "paragraphs": [
                {"paragraph_id": "1.1-P001", "sentence_ids": ["1.1-S001", "1.1-S002"]},
                {"paragraph_id": "1.1-P002", "sentence_ids": ["1.1-S003"]},
            ],
            "sentences": [
                self._sentence("1.1-S001", "1.1-P001", "Tünel yeraltında kazı ve destekleme ile oluşturulan bir yapıdır.", "Q01"),
                self._sentence("1.1-S002", "1.1-P001", "Bu cümle canonical pasajın kapsamını aşmaktadır.", "Q02"),
                self._sentence("1.1-S003", "1.1-P002", "Tünel, yeraltında kazı ve destekleme ile oluşturulan bir yapıdır.", "Q03"),
            ],
        }
        self.reviews = [
            self._review("1.1-S001", self.sentence_map["sentences"][0]["text"], "SUPPORTED"),
            self._review("1.1-S002", self.sentence_map["sentences"][1]["text"], "PARTIAL"),
            self._review("1.1-S003", self.sentence_map["sentences"][2]["text"], "SUPPORTED"),
        ]

    @staticmethod
    def _sentence(sentence_id, paragraph_id, text, question):
        return {
            "sentence_id": sentence_id, "paragraph_id": paragraph_id, "text": text,
            "claim_ids": ["CLM_1"], "question_ids": [question],
            "document_ids": ["ING_1"], "source_locators": ["ING_1:CH_1"],
            "audit_status": "PENDING_POSTWRITING_EVIDENCE_AUDIT",
        }

    @staticmethod
    def _review(sentence_id, text, status):
        return {
            "sentence_id": sentence_id, "sentence": text, "status": status,
            "reason_code": "DIRECT_SUPPORT" if status == "SUPPORTED" else "CLAIM_OVERREACH",
        }

    def test_removes_material_issue_and_merges_repetition_without_losing_links(self):
        paragraphs, actions = _plan_revision(self.sentence_map, self.reviews)
        self.assertEqual(sum(len(row) for row in paragraphs), 1)
        retained = paragraphs[0][0]
        self.assertEqual(retained["question_ids"], ["Q01", "Q03"])
        self.assertEqual(retained["sentence_id"], "1.1-S001")
        self.assertEqual(
            [row["action"] for row in actions],
            ["KEPT", "REMOVED_EVIDENCE_ISSUE", "MERGED_REDUNDANT"],
        )
        self.assertEqual(actions[2]["target_sentence_id"], "1.1-S001")

    def test_review_must_exactly_cover_sentence_map(self):
        with self.assertRaisesRegex(BookEngineError, "exactly cover"):
            _plan_revision(self.sentence_map, self.reviews[:-1])


if __name__ == "__main__":
    unittest.main()
