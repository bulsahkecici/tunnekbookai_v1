from __future__ import annotations

import unittest

from tunnelbookai.book.coverage_audit import _validate_results


class QuestionCoverageAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.question = {"question_id": "1.1-Q01", "section_id": "1.1", "question": "Tünel nedir?"}
        self.supported = {
            "sentence_id": "1.1-S001", "paragraph_id": "1.1-P001",
            "sentence": "Tünel yeraltında kazı ile oluşturulan bir yapıdır.", "status": "SUPPORTED",
            "supporting_claim_ids": ["CLM_1"], "supporting_document_ids": ["ING_1"],
            "source_locators": ["ING_1:CH_1:p1"],
        }

    def test_answered_projects_traceable_spans_and_evidence(self):
        rows = _validate_results({"results": [{"i": 1, "s": "A", "e": [1], "r": "D", "c": 90}]}, [self.question], [[self.supported]], draft_path="book/production/drafts/x/section.md")
        self.assertEqual(rows[0]["status"], "ANSWERED")
        self.assertEqual(rows[0]["answer_spans"][0]["paragraph_or_sentence_ids"], ["1.1-S001"])
        self.assertEqual(rows[0]["supporting_claim_ids"], ["CLM_1"])

    def test_answered_with_partial_sentence_is_conservatively_downgraded(self):
        partial = {**self.supported, "status": "PARTIAL"}
        rows = _validate_results({"results": [{"i": 1, "s": "A", "e": [1], "r": "D", "c": 80}]}, [self.question], [[partial]], draft_path="x")
        self.assertEqual(rows[0]["status"], "PARTIAL")
        self.assertEqual(rows[0]["reason"], "PARTIAL_ANSWER")

    def test_not_answered_has_no_spurious_references(self):
        rows = _validate_results({"results": [{"i": 1, "s": "N", "e": [1], "r": "N", "c": 95}]}, [self.question], [[self.supported]], draft_path="x")
        self.assertEqual(rows[0]["answer_spans"], [])
        self.assertEqual(rows[0]["supporting_claim_ids"], [])

    def test_partial_without_span_is_conservatively_not_answered(self):
        rows = _validate_results({"results": [{"i": 1, "s": "P", "e": [], "r": "P", "c": 70}]}, [self.question], [[self.supported]], draft_path="x")
        self.assertEqual(rows[0]["status"], "NOT_ANSWERED")
        self.assertEqual(rows[0]["reason"], "NO_ANSWER_SPAN")


if __name__ == "__main__":
    unittest.main()
