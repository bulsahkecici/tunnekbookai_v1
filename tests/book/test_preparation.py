from __future__ import annotations

import unittest

from tunnelbookai.book.errors import BookEngineError
from tunnelbookai.book.preparation import _build_section_artifacts


class SectionPreparationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.identity = {
            "scope_sha256": "a" * 64,
            "question_bank_sha256": "b" * 64,
            "canonical_corpus_digest": "c" * 64,
            "retrieval_index_id": "BRI_test",
            "prewriting_audit_id": "PEA_test",
            "prewriting_results_sha256": "d" * 64,
            "embedding_model_id": "bge",
            "llm_model_id": "qwen",
            "model_configuration": "e" * 64,
            "software_version": "test",
        }
        self.provenance = {
            "document_id": "ING_1",
            "chunk_id": "ING_1_CH_1",
            "canonical_retrieval_path": "corpus/canonical/objects/ING_1/chunks/embedding_ready.jsonl",
            "canonical_line_number": 1,
            "selected_by_qwen": True,
        }
        self.locator = "ING_1:ING_1_CH_1:pages=2;canonical=x#L1"

    def _row(self, question_id: str, status: str, *, selected: bool = True):
        provenance = {**self.provenance, "selected_by_qwen": selected}
        return {
            "question_id": question_id,
            "section_id": "1.1",
            "question": f"Question {question_id}",
            "status": status,
            "reason_code": "DIRECT_ANSWER" if status == "SUPPORTED" else "PARTIAL_ONLY" if status == "PARTIAL" else "NO_DIRECT_SUPPORT",
            "confidence": 0.8,
            "source_locators": [self.locator],
            "authority_and_provenance": [provenance],
        }

    @staticmethod
    def _source_loader(provenance, locator):
        return {
            "document_id": provenance["document_id"],
            "chunk_id": provenance["chunk_id"],
            "claim_text": "Canonical evidence passage.",
            "locator": locator,
            "canonical_retrieval_path": provenance["canonical_retrieval_path"],
            "canonical_line_number": provenance["canonical_line_number"],
            "canonical_text_sha256": "f" * 64,
            "chunk_type": "TEXT_CHUNK",
            "source_section_id": "1",
            "secondary_section_ids": ["1.1"],
            "page_start": 2,
            "page_end": 2,
            "slide_number": None,
            "sheet_name": None,
            "source_kind": "MANUAL_INTERNAL",
            "evidence_level": "FULL_TEXT",
        }

    def test_selected_canonical_passage_is_deduplicated_and_bound_to_questions(self):
        rows = [
            self._row("1.1-Q01", "SUPPORTED"),
            self._row("1.1-Q02", "PARTIAL"),
            self._row("1.1-Q03", "UNSUPPORTED", selected=False),
        ]
        packet, registry = _build_section_artifacts(
            section_id="1.1",
            section_title="Tünelin Tanımı",
            readiness="READY_WITH_LIMITATIONS",
            section_rows=rows,
            identity=self.identity,
            source_loader=self._source_loader,
        )
        self.assertEqual(registry["claim_count"], 1)
        claim = registry["claims"][0]
        self.assertEqual(claim["evidence_strength"], "SUPPORTED")
        self.assertEqual(claim["supporting_question_ids"], ["1.1-Q01", "1.1-Q02"])
        self.assertIn("PARTIAL_FOR_ONE_OR_MORE_LINKED_QUESTIONS", claim["limitations"])
        self.assertEqual(packet["questions"][2]["allowed_claim_ids"], [])
        self.assertEqual(packet["questions"][2]["drafting_permission"], "NO_FACTUAL_ANSWER")
        self.assertFalse(packet["writer_constraints"]["unregistered_factual_claims_allowed"])

    def test_artifact_ids_are_deterministic(self):
        kwargs = {
            "section_id": "1.1",
            "section_title": "Tünelin Tanımı",
            "readiness": "READY_WITH_LIMITATIONS",
            "section_rows": [self._row("1.1-Q01", "SUPPORTED")],
            "identity": self.identity,
            "source_loader": self._source_loader,
        }
        first_packet, first_registry = _build_section_artifacts(**kwargs)
        second_packet, second_registry = _build_section_artifacts(**kwargs)
        self.assertEqual(first_packet, second_packet)
        self.assertEqual(first_registry, second_registry)

    def test_unsupported_question_cannot_receive_a_claim(self):
        with self.assertRaisesRegex(BookEngineError, "unsupported question"):
            _build_section_artifacts(
                section_id="1.1",
                section_title="Tünelin Tanımı",
                readiness="EVIDENCE_GAP",
                section_rows=[self._row("1.1-Q01", "UNSUPPORTED")],
                identity=self.identity,
                source_loader=self._source_loader,
            )


if __name__ == "__main__":
    unittest.main()
