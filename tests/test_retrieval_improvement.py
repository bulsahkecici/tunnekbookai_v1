from __future__ import annotations

import csv
import importlib.util
import json
import os
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIVE = os.environ.get("TUNNELBOOK_QDRANT_LIVE") == "1"


def load_module():
    spec = importlib.util.spec_from_file_location("retrieval_improvement",
                                                  ROOT / "scripts/17_retrieval_improvement.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


improvement = load_module()

PROTECTED_BASELINE = {
    "data/embeddings/bge_m3_dense.npy": "99e3b79033a996ffb08b4b742faf68ec217a5a49d0cfdb05175996d65de1d4d3",
    "data/metadata/full_embedding_manifest.csv": "68be1f5fa0b7b6078cd9f492a8732aa796b2ab6536c4b76454e5a37bd41bc32a",
    "data/chunks/chunks.jsonl": "e751fcfc3cc6828b05f75f494fd9a31b44388abda9daf83fb9581581ef79df5b",
    "data/chunks_recovery/chunks.jsonl": "835fc871ee53253d4d95eca14c7c13d908f7d06e559cf657f71c954196fd07f7",
}

_CACHE: dict[str, object] = {}


def corpus():
    if "records" not in _CACHE:
        evaluation = improvement.load_evaluation_module(ROOT)
        _CACHE["records"] = evaluation.load_corpus(ROOT)
    return _CACHE["records"]


class TestBenchmarkImmutability(unittest.TestCase):
    def test_benchmark_v1_sha_matches_manifest(self):
        path = ROOT / "data/evaluation/retrieval_queries_v1.jsonl"
        manifest = json.loads((ROOT / "data/evaluation/retrieval_benchmark_v1_manifest.json")
                              .read_text(encoding="utf-8"))
        self.assertEqual(improvement.sha256(path.read_bytes()), manifest["sha256"])
        self.assertEqual(manifest["query_count"], 114)

    def test_benchmark_v1_still_has_114_queries(self):
        rows = improvement.read_jsonl(ROOT / "data/evaluation/retrieval_queries_v1.jsonl")
        self.assertEqual(len(rows), 114)

    def test_probe_v2_is_a_separate_file(self):
        v1 = ROOT / "data/evaluation/retrieval_queries_v1.jsonl"
        v2 = ROOT / "data/evaluation/crosslingual_probe_v2.jsonl"
        if not v2.is_file():
            self.skipTest("probe v2 not generated yet")
        self.assertNotEqual(v1, v2)
        v1_ids = {row["query_id"] for row in improvement.read_jsonl(v1)}
        v2_ids = {row["query_id"] for row in improvement.read_jsonl(v2)}
        self.assertEqual(v1_ids & v2_ids, set())

    def test_protected_artifacts_unchanged(self):
        for relative, expected in PROTECTED_BASELINE.items():
            self.assertEqual(improvement.sha256((ROOT / relative).read_bytes()), expected, relative)


class TestTokenizer(unittest.TestCase):
    def test_preserves_section_numbers(self):
        self.assertIn("252.04", improvement.tokenize("Madde 252.04 hükümleri"))
        self.assertIn("351.08.07", improvement.tokenize("351.08.07 Püskürtmenin Uygulanması"))

    def test_preserves_standard_codes(self):
        tokens = improvement.tokenize("ASTM D1586 and EN 1997")
        self.assertIn("d1586", tokens)
        self.assertIn("1997", tokens)

    def test_preserves_ranges_and_units(self):
        tokens = improvement.tokenize("10-20 mm agrega")
        self.assertIn("10-20", tokens)
        self.assertIn("mm", tokens)

    def test_preserves_acronyms(self):
        for term in ("RMR", "GSI", "TBM", "NATM", "KGM"):
            self.assertIn(term.lower(), improvement.tokenize(f"{term} kullanılır"))

    def test_turkish_case_folding_is_consistent(self):
        self.assertEqual(improvement.tokenize("İSTANBUL"), improvement.tokenize("istanbul"))
        self.assertEqual(improvement.tokenize("ŞİŞLİ"), improvement.tokenize("şişli"))

    def test_no_stemming_applied(self):
        self.assertIn("tüneli", improvement.tokenize("tüneli"))
        self.assertIn("tünellerde", improvement.tokenize("tünellerde"))

    def test_tokenizer_is_deterministic(self):
        text = "Püskürtme beton 351.08.07 ve RMR 10-20 mm"
        self.assertEqual(improvement.tokenize(text), improvement.tokenize(text))


class TestBM25(unittest.TestCase):
    def small_index(self):
        docs = [improvement.tokenize(text) for text in
                ["tunnel ventilation system design",
                 "shotcrete lining application 351.08.07",
                 "rock bolt pull out test",
                 "tunnel ventilation fans and ducts"]]
        return improvement.BM25Plus(docs)

    def test_scores_rank_relevant_first(self):
        index = self.small_index()
        top = index.top(improvement.tokenize("ventilation"), 4)
        self.assertIn(top[0][0], (0, 3))

    def test_exact_code_match_is_found(self):
        index = self.small_index()
        top = index.top(improvement.tokenize("351.08.07"), 1)
        self.assertEqual(top[0][0], 1)

    def test_unknown_term_returns_nothing(self):
        index = self.small_index()
        self.assertEqual(index.top(improvement.tokenize("zzzznonexistent"), 5), [])

    def test_deterministic_tie_handling(self):
        index = self.small_index()
        first = index.top(improvement.tokenize("tunnel"), 4)
        second = index.top(improvement.tokenize("tunnel"), 4)
        self.assertEqual(first, second)
        indices = [item[0] for item in first]
        self.assertEqual(indices, sorted(indices, key=lambda i: (-dict(first)[i], i)))

    def test_index_stats_cover_full_corpus(self):
        path = ROOT / "data/retrieval/bm25_v1/index_stats.json"
        if not path.is_file():
            self.skipTest("bm25 index not built yet")
        stats = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(stats["documents"], 5992)
        self.assertEqual(stats["tokenizer"], "unicode_nfkc_casefold_no_stemming")

    def test_index_chunk_ids_match_corpus_exactly(self):
        path = ROOT / "data/retrieval/bm25_v1/chunk_ids.json"
        if not path.is_file():
            self.skipTest("bm25 index not built yet")
        stored = json.loads(path.read_text(encoding="utf-8"))
        expected = [record["chunk_id"] for record in corpus()]
        self.assertEqual(stored, expected)
        self.assertEqual(len(stored), 5992)

    def test_index_composition(self):
        records = corpus()
        kinds = Counter(record["source_kind"] for record in records)
        self.assertEqual(kinds["canonical_chunk"], 5980)
        self.assertEqual(kinds["recovery_chunk"], 12)


class TestFusion(unittest.TestCase):
    def test_rrf_prefers_consensus(self):
        fused = improvement.rrf([[1, 2, 3], [1, 3, 2]], 60)
        self.assertGreater(fused[1], fused[2])
        self.assertGreater(fused[1], fused[3])

    def test_rrf_uses_rank_not_score(self):
        fused = improvement.rrf([[7]], 60)
        self.assertAlmostEqual(fused[7], 1 / 61)

    def test_rrf_k_changes_weighting(self):
        low = improvement.rrf([[1, 2]], 10)
        high = improvement.rrf([[1, 2]], 100)
        self.assertGreater(low[1] - low[2], high[1] - high[2])

    def test_fused_order_is_deterministic_on_ties(self):
        fused = {5: 1.0, 3: 1.0, 9: 1.0}
        reference = {3: 0, 5: 1, 9: 2}
        self.assertEqual(improvement.fused_order(fused, reference), [3, 5, 9])

    def test_fused_order_respects_score_first(self):
        fused = {5: 2.0, 3: 1.0}
        self.assertEqual(improvement.fused_order(fused, {3: 0, 5: 1}), [5, 3])


class TestNeighbourExpansion(unittest.TestCase):
    def records(self):
        return [{"chunk_id": "DOC000001-C0001", "document_id": "DOC000001"},
                {"chunk_id": "DOC000001-C0002", "document_id": "DOC000001"},
                {"chunk_id": "DOC000001-C0003", "document_id": "DOC000001"},
                {"chunk_id": "DOC000002-C0001", "document_id": "DOC000002"}]

    def by_chunk(self):
        return {record["chunk_id"]: index for index, record in enumerate(self.records())}

    def test_adjacent_chunks_are_added(self):
        found = improvement.neighbours(1, self.records(), self.by_chunk())
        self.assertEqual(set(found), {0, 2})

    def test_no_cross_document_leakage(self):
        """DOC000001-C0003's numeric successor lives in another document and must not be pulled in."""
        found = improvement.neighbours(2, self.records(), self.by_chunk())
        for index in found:
            self.assertEqual(self.records()[index]["document_id"], "DOC000001")
        self.assertNotIn(3, found)

    def test_first_chunk_has_only_forward_neighbour(self):
        found = improvement.neighbours(0, self.records(), self.by_chunk())
        self.assertEqual(set(found), {1})

    def test_isolated_document_has_no_neighbours(self):
        self.assertEqual(improvement.neighbours(3, self.records(), self.by_chunk()), ())

    def test_expansion_preserves_original_order_first(self):
        expanded = improvement.neighbour_expand([1], self.records(), self.by_chunk(), 10)
        self.assertEqual(expanded[0], 1)

    def test_expansion_respects_limit(self):
        expanded = improvement.neighbour_expand([0, 1, 2], self.records(), self.by_chunk(), 2)
        self.assertEqual(len(expanded), 2)


class TestCrossLingualFreeze(unittest.TestCase):
    def test_translation_table_is_frozen_on_disk(self):
        path = ROOT / "data/evaluation/crosslingual_query_expansion_v1.json"
        if not path.is_file():
            self.skipTest("translations not generated yet")
        stored = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(stored, improvement.translation_table())

    def test_translation_records_required_fields(self):
        for item in improvement.translation_table():
            for field in ("query_id", "original", "translated", "source_language",
                          "target_language", "method"):
                self.assertIn(field, item)
            self.assertNotEqual(item["original"], item["translated"])
            self.assertNotEqual(item["source_language"], item["target_language"])

    def test_translations_cover_the_v1_cross_lingual_probes(self):
        rows = improvement.read_jsonl(ROOT / "data/evaluation/retrieval_queries_v1.jsonl")
        cross = {row["query_id"] for row in rows if row["cross_lingual"]}
        translated = {item["query_id"] for item in improvement.translation_table()}
        self.assertEqual(cross, translated)

    def test_probe_v2_uses_language_restricted_gold(self):
        path = ROOT / "data/evaluation/crosslingual_probe_v2.jsonl"
        if not path.is_file():
            self.skipTest("probe v2 not generated yet")
        rows = improvement.read_jsonl(path)
        self.assertGreaterEqual(len(rows), 20)
        for row in rows:
            self.assertTrue(row["cross_lingual"])
            self.assertNotEqual(row["language"], row["gold_language"])
            self.assertTrue(row["gold_chunk_ids"])
            self.assertIn("language_restricted", row["annotation_method"])

    def test_probe_v2_is_balanced(self):
        path = ROOT / "data/evaluation/crosslingual_probe_v2.jsonl"
        if not path.is_file():
            self.skipTest("probe v2 not generated yet")
        rows = improvement.read_jsonl(path)
        languages = Counter(row["language"] for row in rows)
        self.assertGreaterEqual(languages["tr"], 5)
        self.assertGreaterEqual(languages["en"], 5)


class TestBootstrap(unittest.TestCase):
    def test_bootstrap_is_reproducible(self):
        baseline = [0.0, 1.0] * 20
        variant = [1.0, 1.0] * 20
        first = improvement.bootstrap_delta(baseline, variant, samples=500)
        second = improvement.bootstrap_delta(baseline, variant, samples=500)
        self.assertEqual(first, second)

    def test_bootstrap_detects_clear_improvement(self):
        baseline = [0.0] * 50
        variant = [1.0] * 50
        result = improvement.bootstrap_delta(baseline, variant, samples=500)
        self.assertAlmostEqual(result["delta"], 1.0)
        self.assertTrue(result["significant"])

    def test_bootstrap_reports_no_significance_for_identical(self):
        values = [0.5] * 50
        result = improvement.bootstrap_delta(values, values, samples=500)
        self.assertAlmostEqual(result["delta"], 0.0)
        self.assertFalse(result["significant"])

    def test_bootstrap_interval_brackets_delta(self):
        baseline = [0.0, 1.0] * 25
        variant = [1.0, 0.0] * 25
        result = improvement.bootstrap_delta(baseline, variant, samples=500)
        self.assertLessEqual(result["ci_low"], result["delta"])
        self.assertGreaterEqual(result["ci_high"], result["delta"])


class TestArtifacts(unittest.TestCase):
    def test_metrics_file_structure(self):
        path = ROOT / "data/evaluation/retrieval_improvement_metrics.json"
        if not path.is_file():
            self.skipTest("improvement metrics not generated yet")
        metrics = json.loads(path.read_text(encoding="utf-8"))
        for section in ("variants", "bootstrap", "candidate_depth_recall", "reranker_headroom"):
            self.assertIn(section, metrics)
        self.assertIn("DENSE_V1", metrics["variants"])

    def test_all_variants_share_the_same_query_set(self):
        path = ROOT / "data/evaluation/retrieval_improvement_results.jsonl"
        if not path.is_file():
            self.skipTest("improvement results not generated yet")
        rows = improvement.read_jsonl(path)
        grouped = {}
        for row in rows:
            grouped.setdefault(row["variant"], set()).add(row["query_id"])
        sets = list(grouped.values())
        for other in sets[1:]:
            self.assertEqual(sets[0], other)

    def test_failure_transition_matrix_integrity(self):
        path = ROOT / "data/evaluation/failure_transition_matrix.csv"
        if not path.is_file():
            self.skipTest("transition matrix not generated yet")
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertTrue(rows)
        required = {"query_id", "baseline_cause"}
        self.assertTrue(required.issubset(set(rows[0].keys())))
        for row in rows:
            for key, value in row.items():
                if key.startswith("fixed_by_"):
                    self.assertIn(value, {"yes", "no"}, f"{row['query_id']}:{key}={value}")

    def test_reranker_identity_is_pinned(self):
        self.assertEqual(improvement.RERANKER_NAME, "BAAI/bge-reranker-v2-m3")
        self.assertEqual(improvement.RERANKER_REVISION,
                         "953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e")
        self.assertLessEqual(improvement.RERANKER_MAX_LENGTH, 8192)


@unittest.skipUnless(LIVE, "set TUNNELBOOK_QDRANT_LIVE=1 for live checks")
class TestLiveCollection(unittest.TestCase):
    def test_dense_collection_unchanged(self):
        from qdrant_client import QdrantClient
        client = QdrantClient(url=improvement.REST_URL, timeout=60)
        self.assertEqual(client.count(collection_name=improvement.COLLECTION, exact=True).count, 5992)


if __name__ == "__main__":
    unittest.main()
