from __future__ import annotations

import unittest

from tunnelbookai.book.lexical import focused_window, noise_flags, repair_broken_spacing, token_jaccard, tokenize
from tunnelbookai.book.retrieval import HybridRetriever, RetrievalPolicy, build_index, inspect_index, search_index
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
        self.assertEqual(built["lexical"]["row_count"], 1)
        self.assertIsNotNone(status.lexical)
        permissive = RetrievalPolicy(min_chars=0)
        result = search_index(
            "synthetic evidence", self.repo.root,
            section=self.repo.section_id, top_k=1, client=FakeEmbeddingClient(), policy=permissive,
        )
        self.assertEqual(result["results"][0]["document_id"], self.repo.document_id)
        self.assertEqual(result["results"][0]["section_id"], self.repo.section_id)
        self.assertEqual(result["results"][0]["dense_rank"], 1)
        self.assertEqual(result["results"][0]["lexical_rank"], 1)
        self.assertEqual(result["lexical_index_id"], built["lexical"]["lexical_index_id"])

    def test_noise_policy_excludes_short_rows_and_rebuild_is_idempotent(self):
        build_index(self.repo.root, batch_size=1, client=FakeEmbeddingClient())
        again = build_index(self.repo.root, batch_size=1, client=FakeEmbeddingClient())
        self.assertEqual(again["status"], "NO_CHANGE")
        # The fixture row is 84 characters: the default policy (150) excludes it, so hybrid
        # search must return nothing rather than promote a below-threshold row.
        result = search_index("synthetic evidence", self.repo.root, top_k=1, client=FakeEmbeddingClient())
        self.assertEqual(result["results"], [])
        retriever = HybridRetriever(self.repo.root, client=FakeEmbeddingClient(), policy=RetrievalPolicy(min_chars=0))
        self.assertIn("retrieval_policy", retriever.identity)
        self.assertEqual(retriever.search(["synthetic evidence"], ["nothing matches lexically"], top_k=1)[0][0]["lexical_rank"], None)

    def test_focused_window_selects_the_query_bearing_passage(self):
        text = ("Önceki bölümün kuyruğu burada devam eder ve konuyla ilgisizdir. " * 6) + (
            "Batırılmış tüneller karada inşa edilen tüplerin deniz tabanına indirilmesiyle yapılır. "
            "Su altında açılan tüneller iki tipe ayrılır. "
        ) + ("Sonraki bölüm başka bir konuyu anlatır. " * 6)
        window = focused_window(text, "Su altında açılan tüneller batırılmış tüp", chars=220)
        self.assertIn("Batırılmış tüneller", window)
        self.assertLessEqual(len(window), 220)
        self.assertEqual(focused_window("kısa metin.", "sorgu", chars=100), "kısa metin.")
        self.assertGreater(token_jaccard(window, window + " ek."), 0.8)
        self.assertLess(token_jaccard("tünel kazı destek", "maliyet enerji bakım"), 0.1)

    def test_rebuild_after_canonical_change_reuses_unchanged_vectors(self):
        first = build_index(self.repo.root, batch_size=1, client=FakeEmbeddingClient())
        self.assertEqual(first["reused_vector_count"], 0)
        # Promote a second document: the canonical digest changes, the old index is stale,
        # but the unchanged row's vector must be reused rather than re-embedded.
        self.repo.add_candidate(b"a second synthetic canonical evidence document", title="second synthetic evidence")
        context = CanonicalContext.load(self.repo.root)
        plan = build_plan(context=context)
        apply_plan(context.audit_root / "plans" / f"{plan.plan_id}.json", approve=plan.plan_id, context=context)
        self.assertFalse(inspect_index(self.repo.root).ready)
        second = build_index(self.repo.root, batch_size=1, client=FakeEmbeddingClient())
        self.assertEqual(second["status"], "BUILT")
        self.assertEqual(second["vector_count"], 2)
        self.assertEqual(second["reused_vector_count"], 1)
        self.assertTrue(inspect_index(self.repo.root).ready)

    def test_lexical_tokeniser_folds_turkish_and_repairs_spacing(self):
        self.assertEqual(tokenize("KAZI kazı Tünellerin tünel"), ["kazi", "kazi", "tunel", "tunel"])
        self.assertEqual(repair_broken_spacing("k ı salmas ı ve"), "kısalmasıve")
        self.assertEqual(repair_broken_spacing("k ı salmas ı ve", join_right=False), "kı salması ve")
        toc = "\n".join(f"{n}. Başlık {'.' * 12} {n * 3}" for n in range(1, 6))
        self.assertTrue(noise_flags(toc)["toc_like"])
        self.assertFalse(noise_flags("Düz bir paragraf metni. Gerçek cümleler içerir.")["toc_like"])

    def test_status_fails_closed_when_shard_changes(self):
        built = build_index(self.repo.root, batch_size=1, client=FakeEmbeddingClient())
        vector_path = self.repo.root / built["shards"][0]["vectors_path"]
        vector_path.write_bytes(vector_path.read_bytes() + b"changed")
        status = inspect_index(self.repo.root)
        self.assertFalse(status.ready)
        self.assertIn("hash mismatch", status.reason)


if __name__ == "__main__":
    unittest.main()
