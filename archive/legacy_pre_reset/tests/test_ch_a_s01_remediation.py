from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ch_a_s01_remediation.py"
SPEC = importlib.util.spec_from_file_location("ch_a_s01_remediation", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class RemediationTests(unittest.TestCase):
    class FakeResponse:
        def __init__(self, body: dict) -> None:
            self.payload = json.dumps(body).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback) -> None:
            return None

        def read(self) -> bytes:
            return self.payload

    def test_loopback_endpoint_accepted(self) -> None:
        for url in ("http://127.0.0.1:1234/v1", "http://localhost:1234/v1", "http://[::1]:1234/v1"):
            with self.subTest(url=url):
                self.assertEqual(MODULE.validate_local_endpoint(url), url)

    def test_remote_endpoint_rejected(self) -> None:
        for url in ("https://api.openai.com/v1", "http://192.168.1.4:1234/v1", "http://localhost.evil.test:1234/v1"):
            with self.subTest(url=url), self.assertRaises(RuntimeError):
                MODULE.validate_local_endpoint(url)

    def test_candidate_deduplication_merges_query_hits(self) -> None:
        rows = [
            {"chunk_id": "C1", "document_id": "D1", "text": "same", "query": "a", "retrieval_rank": 2, "retrieval_score": 0.8},
            {"chunk_id": "C1", "document_id": "D1", "text": "same", "query": "b", "retrieval_rank": 1, "retrieval_score": 0.9},
            {"chunk_id": "C2", "document_id": "D2", "text": "other", "query": "a", "retrieval_rank": 1, "retrieval_score": 0.7},
        ]
        result = MODULE.deduplicate_candidates(rows, 15)
        self.assertEqual([row["chunk_id"] for row in result], ["C1", "C2"])
        self.assertEqual(len(result[0]["retrieval_hits"]), 2)

    def test_safe_readiness_behavior(self) -> None:
        self.assertEqual(MODULE.determine_readiness([], False), "NEEDS_LOCAL_REVIEW")
        self.assertEqual(MODULE.determine_readiness([], True), "TRUE_CORPUS_EVIDENCE_GAP")
        one = [{"disposition": "ADMITTED_STRONG", "document_id": "D1", "locator": "page:1"}]
        self.assertEqual(MODULE.determine_readiness(one, True), "TRUE_CORPUS_EVIDENCE_GAP")

    def test_versioned_output_naming(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            name = "ch_a_s01_candidates.jsonl"
            self.assertEqual(MODULE.versioned_path(base, name, "STAMP").name, name)
            (base / name).write_text("existing", encoding="utf-8")
            self.assertEqual(MODULE.versioned_path(base, name, "STAMP").name, "ch_a_s01_candidates_STAMP.jsonl")
            (base / "ch_a_s01_candidates_STAMP.jsonl").write_text("existing", encoding="utf-8")
            self.assertEqual(MODULE.versioned_path(base, name, "STAMP").name, "ch_a_s01_candidates_STAMP_v2.jsonl")

    def test_no_unrelated_section_processing(self) -> None:
        with self.assertRaisesRegex(MODULE.RemediationError, "unrelated section"):
            MODULE.validate_outputs([{"section_id": "CH-A-S02"}], [], "NEEDS_LOCAL_REVIEW", None)

    def test_native_response_uses_message_not_reasoning(self) -> None:
        body = {"output": [
            {"type": "reasoning", "content": "not the answer"},
            {"type": "message", "content": ' {"status":"OK"} '},
        ]}
        self.assertEqual(MODULE._extract_final_text(body), '{"status":"OK"}')

    def test_native_response_with_only_message(self) -> None:
        body = {"output": [{"type": "message", "content": '{"status":"OK"}'}]}
        self.assertEqual(MODULE._extract_final_text(body), '{"status":"OK"}')

    def test_native_response_missing_output(self) -> None:
        self.assertIsNone(MODULE._extract_final_text({}))

    def test_native_response_empty_output(self) -> None:
        self.assertIsNone(MODULE._extract_final_text({"output": []}))

    @patch.object(MODULE.urllib.request, "urlopen")
    def test_invalid_json_model_content_fails_closed(self, urlopen) -> None:
        urlopen.return_value = self.FakeResponse({
            "output": [{"type": "message", "content": "not JSON"}],
        })
        with self.assertRaisesRegex(MODULE.RemediationError, "^LOCAL_LLM_CLASSIFICATION_FAILED"):
            MODULE._native_chat_json("model", "http://127.0.0.1:1234/v1", "system", "input")

    @patch.object(MODULE.urllib.request, "urlopen")
    def test_transport_failure_is_not_evidence_gap(self, urlopen) -> None:
        urlopen.side_effect = urllib.error.URLError("offline")
        with self.assertRaises(MODULE.RemediationError) as raised:
            MODULE.classify_claims_local([], "model", "http://127.0.0.1:1234/v1")
        self.assertIn("LOCAL_LLM_CLASSIFICATION_FAILED", str(raised.exception))
        self.assertNotIn("TRUE_CORPUS_EVIDENCE_GAP", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
