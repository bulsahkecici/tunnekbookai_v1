from __future__ import annotations

import unittest

from tunnelbookai.book.prewriting import (
    _audit_with_split,
    _section_summary,
    _validate_llm_results,
)


class PrewritingEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.question = {
            "question_id": "6.1-Q01",
            "section_id": "6.1",
            "question": "Tünel maliyeti nedir?",
        }
        self.evidence = {
            "evidence_ref": "6.1-Q01:E1",
            "chunk_id": "ING_1_CH_1",
            "document_id": "ING_1",
            "canonical_retrieval_path": "corpus/canonical/objects/ING_1/chunks/embedding_ready.jsonl",
            "canonical_line_number": 1,
            "source_locator": "ING_1:ING_1_CH_1:pages=2;canonical=x#L1",
            "score": 0.72,
        }

    def test_qwen_references_are_projected_to_canonical_audit_row(self):
        rows = _validate_llm_results({"results": [{
            "i": 1, "s": "S", "e": [1], "r": "D", "c": 88,
        }]}, [self.question], [[self.evidence]])
        self.assertEqual(rows[0]["retrieved_chunk_ids"], ["ING_1_CH_1"])
        self.assertEqual(rows[0]["document_ids"], ["ING_1"])
        self.assertEqual(rows[0]["status"], "SUPPORTED")

    def test_supported_without_evidence_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "without evidence"):
            _validate_llm_results({"results": [{
                "i": 1, "s": "S", "e": [], "r": "D", "c": 80,
            }]}, [self.question], [[self.evidence]])

    def test_no_section_evidence_is_deterministically_unsupported(self):
        class Client:
            def chat_json(self, *args, **kwargs):  # pragma: no cover - must not run
                raise AssertionError("Qwen must not be called without evidence")

        rows = _audit_with_split(Client(), "qwen", "6.1", "Maliyet", [self.question], [[]])
        self.assertEqual(rows[0]["status"], "UNSUPPORTED")
        self.assertEqual(rows[0]["reason_code"], "NO_SECTION_EVIDENCE")

    def test_section_readiness_requires_thirty_supported_questions(self):
        rows = ([{"status": "SUPPORTED"}] * 29) + ([{"status": "PARTIAL"}] * 21)
        summary = _section_summary("6.1", "Maliyet", rows)
        self.assertFalse(summary["preferred_target_met"])
        self.assertEqual(summary["readiness"], "READY_WITH_LIMITATIONS")
        rows[29]["status"] = "SUPPORTED"
        self.assertTrue(_section_summary("6.1", "Maliyet", rows)["preferred_target_met"])


if __name__ == "__main__":
    unittest.main()
