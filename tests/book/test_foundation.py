from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

from tunnelbookai.book.canonical import CanonicalEvidenceAccess
from tunnelbookai.book.contract import load_book_contract, sha256_file, validate_contract_payload
from tunnelbookai.book.coverage import coverage_summary_from_counts, section_target_summary
from tunnelbookai.book.errors import (
    ContractValidationError,
    EvidenceBoundaryError,
    InputValidationError,
    ReferenceIntegrityError,
)
from tunnelbookai.book.inputs import load_book_inputs
from tunnelbookai.book.models import (
    QuestionCoverageResult,
    QuestionCoverageStatus,
    StageStatus,
    validate_result_references,
)
from tunnelbookai.book.stages import STAGES, not_implemented
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.model_capability import UNAVAILABLE, probe


ROOT = Path(__file__).resolve().parents[2]


class FoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inputs = load_book_inputs(ROOT)

    def test_contract_and_complete_input_graph_validate(self):
        self.assertEqual(len(self.inputs.scope), 66)
        self.assertEqual(len(self.inputs.question_section_ids), 59)
        self.assertEqual(len(self.inputs.questions), 2950)
        self.assertTrue(all(len(rows) == 50 for rows in self.inputs.questions_by_section.values()))
        self.assertEqual(self.inputs.contract.coverage_policy["global"]["minimum_answered_count"], 1770)

    def test_contract_rejects_lower_publication_threshold(self):
        payload = copy.deepcopy(self.inputs.contract.payload)
        payload["coverage_policy"]["global"]["minimum_answered_count"] = 1769
        with self.assertRaises(ContractValidationError):
            validate_contract_payload(
                payload, project_root=ROOT, contract_path=self.inputs.contract.path
            )

    def test_partial_does_not_count_and_1770_is_exact_threshold(self):
        below = coverage_summary_from_counts(
            answered=1769, partial=1181, not_answered=0,
            expected_total=2950, minimum_answered_count=1770, minimum_coverage=0.6,
        )
        self.assertFalse(below.publication_gate_passed)
        self.assertAlmostEqual(below.coverage, 1769 / 2950)
        exact = coverage_summary_from_counts(
            answered=1770, partial=1180, not_answered=0,
            expected_total=2950, minimum_answered_count=1770, minimum_coverage=0.6,
        )
        self.assertTrue(exact.publication_gate_passed)
        self.assertEqual(exact.coverage, 0.6)

    def test_incomplete_global_audit_cannot_pass(self):
        result = coverage_summary_from_counts(
            answered=1770, partial=0, not_answered=0,
            expected_total=2950, minimum_answered_count=1770, minimum_coverage=0.6,
        )
        self.assertFalse(result.complete_audit)
        self.assertFalse(result.publication_gate_passed)

    def test_section_target_is_preferred_not_hard_gate(self):
        statuses = [QuestionCoverageStatus.ANSWERED] * 30 + [QuestionCoverageStatus.PARTIAL] * 20
        summary = section_target_summary(statuses, self.inputs.contract)
        self.assertTrue(summary["target_met"])
        self.assertFalse(summary["hard_gate"])
        self.assertEqual(summary["answered"], 30)

    def test_answered_requires_span_claim_document_and_locator(self):
        base = {
            "question_id": "1.1-Q01",
            "section_id": "1.1",
            "question": "Question",
            "status": "ANSWERED",
            "answer_spans": [],
            "supporting_claim_ids": [],
            "supporting_document_ids": [],
            "source_locators": [],
            "confidence": 0.8,
        }
        with self.assertRaises(ReferenceIntegrityError):
            QuestionCoverageResult.from_mapping(base)

    def test_evidence_reference_and_section_integrity(self):
        result = QuestionCoverageResult.from_mapping({
            "question_id": "1.1-Q01",
            "section_id": "1.1",
            "question": "Question",
            "status": "ANSWERED",
            "answer_spans": [{
                "section_file": "book/drafts/1.1.md",
                "paragraph_or_sentence_ids": ["1.1-S001"],
            }],
            "supporting_claim_ids": ["CLM-1"],
            "supporting_document_ids": ["ING-1"],
            "source_locators": ["p. 3"],
            "confidence": 0.8,
        })
        validate_result_references(
            result, expected_section_id="1.1", known_claim_ids={"CLM-1"},
            known_document_ids={"ING-1"}, known_locators={"p. 3"},
            known_span_ids={"1.1-S001"}, allowed_section_files={"book/drafts/1.1.md"},
        )
        with self.assertRaises(ReferenceIntegrityError):
            validate_result_references(
                result, expected_section_id="1.1", known_claim_ids={"CLM-1"},
                known_document_ids={"ING-OTHER"}, known_locators={"p. 3"},
                known_span_ids={"1.1-S001"}, allowed_section_files={"book/drafts/1.1.md"},
            )
        with self.assertRaises(ReferenceIntegrityError):
            validate_result_references(
                result, expected_section_id="2.2.1", known_claim_ids={"CLM-1"},
                known_document_ids={"ING-1"}, known_locators={"p. 3"},
                known_span_ids={"1.1-S001"}, allowed_section_files={"book/drafts/1.1.md"},
            )
        with self.assertRaises(ReferenceIntegrityError):
            validate_result_references(
                result, expected_section_id="1.1", known_claim_ids={"CLM-1"},
                known_document_ids={"ING-1"}, known_locators={"p. 3"},
                known_span_ids={"1.1-S999"}, allowed_section_files={"book/final/1.1.md"},
            )

    def test_noncanonical_evidence_path_is_rejected(self):
        access = CanonicalEvidenceAccess(self.inputs.contract)
        with self.assertRaises(EvidenceBoundaryError):
            access.assert_canonical_path(ROOT / "processing" / "ING-any" / "chunks.jsonl")
        # Evidence-boundary validation is independent of whether the live, verified
        # canonical snapshot is EMPTY or READY. Corpus Population starts from READY.
        self.assertEqual(access.inspect().state, "READY")

    def test_every_unimplemented_stage_reports_not_implemented(self):
        for stage in STAGES:
            result = not_implemented(stage, section_id="1.1")
            self.assertEqual(result.status, StageStatus.NOT_IMPLEMENTED)
            self.assertEqual(result.reason_code, "NOT_IMPLEMENTED")

    def test_model_unavailable_is_explicit_and_has_no_fallback(self):
        with mock.patch(
            "tunnelbookai.ingest.model_capability.LocalEmbeddingClient.available",
            return_value=False,
        ), mock.patch(
            "tunnelbookai.ingest.model_capability.LocalChatClient.has_model",
            return_value=False,
        ):
            result = probe(load_config())
        self.assertEqual(result["decision"], UNAVAILABLE)
        self.assertEqual(result["embedding"]["status"], UNAVAILABLE)
        self.assertEqual(result["llm"]["status"], UNAVAILABLE)

    def test_active_audit_schema_states_match_contract(self):
        pre = json.loads(
            (ROOT / "book/audits/schemas/prewriting_evidence_audit.schema.json").read_text()
        )
        post = json.loads(
            (ROOT / "book/audits/schemas/postwriting_chapter_audit.schema.json").read_text()
        )
        self.assertEqual(
            set(pre["properties"]["status"]["enum"]),
            set(self.inputs.contract.payload["evidence_policy"]["prewriting_states"]),
        )
        self.assertEqual(
            set(post["properties"]["status"]["enum"]),
            set(self.inputs.contract.coverage_policy["allowed_states"]),
        )


class IsolatedInputFailureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        files = [
            "book/config/book_contract.json",
            "book/scope/normalized/book_scope.json",
            "book/question_bank/normalized/question_bank.jsonl",
            "book/question_bank/normalized/question_bank_index.json",
            "book/audits/question_bank_integrity.json",
            "book/audits/source_manifest.json",
            "book/scope/source/Calisma_Kapsami_Tasarisi_17.10.2025.rtf",
            "book/question_bank/source/Tunel_Kitabi_Kapsam_Kontrol_Soru_Bankasi.docx",
            "config/models.yaml",
        ]
        for relative in files:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _refresh_contract_hash(self, authority: str) -> None:
        contract_path = self.root / "book/config/book_contract.json"
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        relative = contract["authorities"][authority]["path"]
        contract["authorities"][authority]["sha256"] = sha256_file(self.root / relative)
        contract_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_hash_mismatch_is_rejected_before_parsing(self):
        path = self.root / "book/question_bank/normalized/question_bank_index.json"
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        with self.assertRaises(InputValidationError):
            load_book_inputs(self.root)

    def test_question_count_mutation_is_rejected_even_with_updated_hash(self):
        path = self.root / "book/question_bank/normalized/question_bank.jsonl"
        lines = path.read_text(encoding="utf-8").splitlines()
        path.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
        self._refresh_contract_hash("question_bank")
        with self.assertRaises(InputValidationError):
            load_book_inputs(self.root)

    def test_remote_model_endpoint_is_rejected(self):
        models_path = self.root / "config/models.yaml"
        models = yaml.safe_load(models_path.read_text(encoding="utf-8"))
        models["llm"]["default_endpoint"] = "https://api.example.com/v1"
        models_path.write_text(yaml.safe_dump(models, sort_keys=False), encoding="utf-8")
        contract_path = self.root / "book/config/book_contract.json"
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        contract["model_policy"]["authority_sha256"] = sha256_file(models_path)
        contract_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        with self.assertRaises(ContractValidationError):
            load_book_contract(self.root)


if __name__ == "__main__":
    unittest.main()
