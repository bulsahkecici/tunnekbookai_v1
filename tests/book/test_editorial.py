from __future__ import annotations

import unittest

from tunnelbookai.book.editorial import _validate_model_review, deterministic_editorial_gate


class EditorialAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sentence_map = {
            "section_id": "1.1",
            "paragraphs": [{"paragraph_id": "1.1-P001", "sentence_ids": ["1.1-S001"]}],
            "sentences": [{
                "sentence_id": "1.1-S001", "paragraph_id": "1.1-P001",
                "text": "Tünel, yeraltında kazı ve destekleme ile oluşturulan bir mühendislik yapısıdır.",
            }],
        }
        self.markdown = (
            "# 1.1 Tünelin Tanımı\n\n"
            "Tünel, yeraltında kazı ve destekleme ile oluşturulan bir mühendislik yapısıdır.\n"
        )

    def test_clean_exact_draft_passes_deterministic_gate(self):
        result = deterministic_editorial_gate(
            self.markdown, self.sentence_map, section_title="Tünelin Tanımı"
        )
        self.assertEqual(result["decision"], "PASS")
        self.assertEqual(result["hard_blockers"], [])

    def test_draft_sentence_map_mismatch_is_a_hard_blocker(self):
        result = deterministic_editorial_gate(
            self.markdown.replace("mühendislik", "teknik"),
            self.sentence_map,
            section_title="Tünelin Tanımı",
        )
        self.assertEqual(result["decision"], "HOLD")
        self.assertIn("DRAFT_SENTENCE_MAP_MISMATCH", result["hard_blockers"])

    def test_model_hold_requires_a_concrete_action(self):
        payload = {"decision": "HOLD", **{field: [] for field in (
            "chronology_issues", "naming_ambiguities", "language_issues",
            "overgeneralizations", "structure_issues", "required_actions",
        )}}
        with self.assertRaisesRegex(ValueError, "disagree"):
            _validate_model_review(payload)


if __name__ == "__main__":
    unittest.main()
