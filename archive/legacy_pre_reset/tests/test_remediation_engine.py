import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import remediation_engine as engine
from scripts import section_evidence_remediation as ser


def _candidate(chunk_id, text):
    return {
        "chunk_id": chunk_id,
        "document_id": f"DOC-{chunk_id}",
        "source_relative_path": f"corpus/{chunk_id}.md",
        "locator": "page:1",
        "source_type": "PRIMARY",
        "authority_state": "VERIFIED",
        "text": text,
    }


def _claim_response(claim_text):
    return {
        "claims": [
            {
                "claim_text": claim_text,
                "document_id": "IGNORED",
                "source_relative_path": "IGNORED",
                "locator": "IGNORED",
                "scope": "IN_SCOPE",
                "qualifier": None,
                "source_type": "IGNORED",
                "authority_state": "IGNORED",
                "support_status": "SUPPORTED",
                "section_applicability": "DIRECT",
                "disposition": "ADMITTED_STRONG",
                "reason": "matches candidate text",
            }
        ]
    }


class RemediationEngineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.cdir = engine.checkpoint_dir(self.root, "CH-Z-S99")

    def tearDown(self):
        self.tmp.cleanup()

    def test_checkpoint_written_on_success(self):
        candidates = [_candidate("c1", "some evidence text")]
        with mock.patch.object(ser, "smoke_test_local_llm", return_value=None), mock.patch.object(
            ser, "_native_chat_json", return_value=_claim_response("some evidence text")
        ):
            claims, statuses = engine.classify_claims_checkpointed(
                candidates, "m1", "http://127.0.0.1:1234/v1", self.cdir, resume=False,
            )
        self.assertEqual(len(claims), 1)
        self.assertEqual(statuses[0]["status"], "CLASSIFIED")
        checkpoints = list(self.cdir.glob("*.json"))
        self.assertEqual(len(checkpoints), 1)

    def test_resume_reuses_checkpoint_without_calling_llm(self):
        candidates = [_candidate("c1", "some evidence text")]
        with mock.patch.object(ser, "smoke_test_local_llm", return_value=None), mock.patch.object(
            ser, "_native_chat_json", return_value=_claim_response("some evidence text")
        ) as mocked:
            engine.classify_claims_checkpointed(
                candidates, "m1", "http://127.0.0.1:1234/v1", self.cdir, resume=False,
            )
            self.assertEqual(mocked.call_count, 1)

        with mock.patch.object(ser, "smoke_test_local_llm", return_value=None), mock.patch.object(
            ser, "_native_chat_json"
        ) as mocked_resume:
            claims, statuses = engine.classify_claims_checkpointed(
                candidates, "m1", "http://127.0.0.1:1234/v1", self.cdir, resume=True,
            )
            mocked_resume.assert_not_called()
        self.assertEqual(len(claims), 1)
        self.assertEqual(statuses[0]["source"], "checkpoint")

    def test_later_failure_does_not_discard_earlier_success(self):
        candidates = [_candidate("c1", "good text"), _candidate("c2", "bad text")]

        def side_effect(model, api_base, system_prompt, input_text):
            if "c2" in input_text or "bad text" in input_text:
                raise ser.RemediationError("LOCAL_LLM_CLASSIFICATION_FAILED: timeout")
            return _claim_response("good text")

        with mock.patch.object(ser, "smoke_test_local_llm", return_value=None), mock.patch.object(
            ser, "_native_chat_json", side_effect=side_effect
        ):
            claims, statuses = engine.classify_claims_checkpointed(
                candidates, "m1", "http://127.0.0.1:1234/v1", self.cdir, resume=False,
            )
        self.assertEqual(len(claims), 1)
        status_by_key = {s["candidate_id"]: s["status"] for s in statuses}
        self.assertEqual(status_by_key["c1"], "CLASSIFIED")
        self.assertEqual(status_by_key["c2"], "DEPENDENCY_FAILURE")

    def test_dependency_failure_is_not_true_corpus_evidence_gap(self):
        statuses = [
            {"candidate_key": "k1", "candidate_id": "c1", "status": "CLASSIFIED", "elapsed_seconds": 1.0},
            {"candidate_key": "k2", "candidate_id": "c2", "status": "DEPENDENCY_FAILURE", "elapsed_seconds": 1.0},
        ]
        readiness = engine.determine_readiness_checkpointed([], statuses, use_local_llm=True)
        self.assertEqual(readiness, "DEPENDENCY_FAILURE")
        self.assertNotEqual(readiness, "TRUE_CORPUS_EVIDENCE_GAP")

    def test_no_dependency_failure_falls_back_to_deterministic_readiness(self):
        statuses = [
            {"candidate_key": "k1", "candidate_id": "c1", "status": "CLASSIFIED", "elapsed_seconds": 1.0},
        ]
        readiness = engine.determine_readiness_checkpointed([], statuses, use_local_llm=True)
        self.assertEqual(readiness, "TRUE_CORPUS_EVIDENCE_GAP")

    def test_validate_outputs_accepts_dependency_failure_readiness(self):
        engine.validate_outputs_checkpointed([], [], "DEPENDENCY_FAILURE", None)

    def test_validate_outputs_rejects_unknown_readiness(self):
        with self.assertRaises(ser.RemediationError):
            engine.validate_outputs_checkpointed([], [], "NOT_A_REAL_STATUS", None)


if __name__ == "__main__":
    unittest.main()
