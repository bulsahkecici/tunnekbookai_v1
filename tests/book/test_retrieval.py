from __future__ import annotations

import unittest

from tunnelbookai.book.retrieval import build_index, inspect_index, search_index
from tunnelbookai.canonical.paths import CanonicalContext
from tunnelbookai.canonical.promotion import apply_plan, build_plan

from tests.canonical.fixtures import SyntheticRepo


class FakeEmbeddingClient:
    model = "text-embedding-baai-bge-m3-568m"

    def available(self) -> bool:
        return True

    def embed(self, text: str) -> list[float]:
        lowered = text.casefold()
        return [1.0, 0.5 if "evidence" in lowered else 0.1, 0.25]

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [self.embed(text) for text in texts]


class RetrievalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = SyntheticRepo()
        context = CanonicalContext.load(self.repo.root)
        plan = build_plan(context=context)
        apply_plan(context.audit_root / "plans" / f"{plan.plan_id}.json", approve=plan.plan_id, context=context)

    def tearDown(self) -> None:
        self.repo.close()

    def test_build_verify_and_search_are_bound_to_canonical(self):
        built = build_index(self.repo.root, batch_size=1, client=FakeEmbeddingClient())
        self.assertEqual(built["status"], "BUILT")
        self.assertEqual(built["vector_count"], 1)
        status = inspect_index(self.repo.root)
        self.assertTrue(status.ready, status.reason)
        result = search_index(
            "synthetic evidence", self.repo.root,
            section=self.repo.section_id, top_k=1, client=FakeEmbeddingClient(),
        )
        self.assertEqual(result["results"][0]["document_id"], self.repo.document_id)
        self.assertEqual(result["results"][0]["section_id"], self.repo.section_id)

    def test_status_fails_closed_when_shard_changes(self):
        built = build_index(self.repo.root, batch_size=1, client=FakeEmbeddingClient())
        vector_path = self.repo.root / built["shards"][0]["vectors_path"]
        vector_path.write_bytes(vector_path.read_bytes() + b"changed")
        status = inspect_index(self.repo.root)
        self.assertFalse(status.ready)
        self.assertIn("hash mismatch", status.reason)


if __name__ == "__main__":
    unittest.main()
