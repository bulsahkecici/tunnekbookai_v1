from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))

import book_qa


class BookQaIntegrityTests(unittest.TestCase):
    def test_scope_and_question_bank_load(self):
        scope = book_qa.load_scope()
        questions = book_qa.load_questions()
        self.assertEqual(len(questions), sum(int(row.get("question_count") or 0) for row in scope.values()))

    def test_question_ids_are_unique_and_mapped(self):
        audit = book_qa.validate()
        self.assertFalse(audit["duplicate_question_ids"])
        self.assertFalse(audit["orphan_sections"])

    def test_parent_sections_are_canonical(self):
        self.assertFalse(book_qa.validate()["parent_section_errors"])

    def test_source_files_unchanged(self):
        self.assertFalse(book_qa.validate()["source_hash_errors"])

    def test_crawler_taxonomy_matches_book_scope(self):
        audit = book_qa.validate()
        self.assertFalse(audit["question_sections_missing_from_taxonomy"])
        self.assertFalse(audit["taxonomy_sections_missing_from_scope"])
        self.assertFalse(audit["taxonomy_title_mismatches"])

    def test_question_coverage_is_derived(self):
        rows = [
            {"section_id": "1.1", "evidence_status": "SUPPORTED"},
            {"section_id": "1.1", "evidence_status": "NO_EVIDENCE"},
        ]
        result = book_qa.question_coverage("1.1", rows, corpus_eligible_documents=3)
        self.assertEqual(result["question_coverage"]["support_rate"], 0.5)

    def test_question_gap_uses_concepts_not_full_question(self):
        question = "Tünel havalandırma sistemlerinde enerji tüketimi nasıl azaltılır?"
        concepts = book_qa.technical_concepts(question)
        self.assertIn("havalandırma", concepts)
        self.assertNotIn(question.casefold(), concepts)

    def test_chapter_gate_rejects_unsupported_claim(self):
        result = book_qa.chapter_gate("1.1", [{"section_id": "1.1", "chapter_status": "UNSUPPORTED_CLAIM"}])
        self.assertEqual(result["decision"], "NO_GO")


if __name__ == "__main__":
    unittest.main()
