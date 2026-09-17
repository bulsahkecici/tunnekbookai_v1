from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tunnelbookai.dashboard.improvements import _improve_one, build_state
from tunnelbookai.ingest.chunking import manifest as manifest_module
from tunnelbookai.ingest.chunking import tokenizer
from tunnelbookai.ingest.chunking.policy import ChunkPolicy, TEXT_CHUNK, chunk_id
from tunnelbookai.population.models import atomic_json


class ImprovementTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.document_id = "ING_improve"
        self.run_path = self.root / "audit/corpus_population/runs/CPR_test.json"
        self.bundle = self.root / "processing" / self.document_id
        (self.bundle / "chunks").mkdir(parents=True)
        self.staging = self.root / "corpus/staging/v2" / self.document_id
        self.staging.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def _fixture(self):
        old_policy = ChunkPolicy(policy_version="structure-aware-v1")
        text = "kelime " * 1300
        chunk = {
            "chunk_id": chunk_id(self.document_id, TEXT_CHUNK, ["PARA1"], text, old_policy),
            "document_id": self.document_id,
            "chunk_type": TEXT_CHUNK,
            "final_primary_section": "2.1",
            "final_secondary_sections": [],
            "heading_path": ["Deneme"],
            "page_start": 1,
            "page_end": 2,
            "source_elements": ["PARA1"],
            "text": text,
            "token_count": tokenizer.count(text),
            "provenance": {"original_sha256": "a" * 64, "source_kind": "MANUAL_INTERNAL"},
            "chunk_schema_version": old_policy.schema_version,
            "chunk_policy_version": old_policy.policy_version,
            "tokenizer": old_policy.tokenizer_name,
            "ordinal": 1,
        }
        (self.bundle / "chunks/chunk_manifest.jsonl").write_text(
            json.dumps(chunk) + "\n", encoding="utf-8"
        )
        ready = manifest_module.build_rows([chunk], old_policy, document_staged=True)
        (self.bundle / "chunks/embedding_ready.jsonl").write_text(
            "".join(json.dumps(row) + "\n" for row in ready), encoding="utf-8"
        )
        atomic_json(self.bundle / "chunk_quality.json", {
            "status": "WARN", "warnings": [f"CHUNK_OVER_MAX:{chunk['chunk_id']}:1300"],
            "errors": [], "chunk_count": 1,
        })
        atomic_json(self.staging / "bundle.json", {"document_id": self.document_id, "chunk_count": 1})
        atomic_json(self.staging / "chunk_quality.json", {"status": "WARN"})
        run = {
            "documents": {self.document_id: {
                "disposition": "STAGED", "chunk_count": 1,
                "warnings": [f"CHUNK_OVER_MAX:{chunk['chunk_id']}:1300"],
            }}
        }
        self.run_path.parent.mkdir(parents=True)
        atomic_json(self.run_path, run)
        return run

    def test_plan_discovers_warning_driven_candidate(self):
        self._fixture()
        state = build_state(self.run_path, self.root)
        self.assertEqual(state["total_candidates"], 1)
        self.assertEqual(state["candidates"][0]["action"], "RECHUNK")

    def test_improvement_splits_at_soft_max_and_keeps_retrieval(self):
        run = self._fixture()
        policy = ChunkPolicy(policy_version="structure-aware-v2")
        result = _improve_one(
            self.root, run, self.document_id, policy, self.root / "backup"
        )
        self.assertEqual(result["after_over_max"], 0)
        self.assertGreater(result["after_chunks"], result["before_chunks"])
        chunks = [
            json.loads(line) for line in
            (self.bundle / "chunks/chunk_manifest.jsonl").read_text().splitlines()
        ]
        self.assertTrue(all(chunk["token_count"] <= policy.max_tokens for chunk in chunks))
        self.assertTrue(all(chunk["chunk_policy_version"] == "structure-aware-v2" for chunk in chunks))
        self.assertTrue((self.root / "backup" / self.document_id / "chunk_manifest.jsonl").is_file())

    def test_historical_ready_rows_remain_eligible_without_staging_copy(self):
        run = self._fixture()
        for path in self.staging.iterdir():
            path.unlink()
        self.staging.rmdir()
        policy = ChunkPolicy(policy_version="structure-aware-v2")
        result = _improve_one(
            self.root, run, self.document_id, policy, self.root / "backup"
        )
        self.assertGreater(result["retrieval_ready"], 0)

    def test_repeated_improvement_keeps_split_chunk_identities_valid(self):
        run = self._fixture()
        policy = ChunkPolicy(policy_version="structure-aware-v2")
        _improve_one(self.root, run, self.document_id, policy, self.root / "backup-one")
        _improve_one(self.root, run, self.document_id, policy, self.root / "backup-two")
        chunks = [
            json.loads(line) for line in
            (self.bundle / "chunks/chunk_manifest.jsonl").read_text().splitlines()
        ]
        for row in chunks:
            expected = chunk_id(
                self.document_id, row["chunk_type"], row["source_elements"], row["text"],
                policy, row.get("chunk_identity_part"),
            )
            self.assertEqual(row["chunk_id"], expected)


if __name__ == "__main__":
    unittest.main()
