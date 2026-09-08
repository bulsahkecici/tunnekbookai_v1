from __future__ import annotations

import csv
import importlib.util
import json
import math
import os
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIVE = os.environ.get("TUNNELBOOK_QDRANT_LIVE") == "1"


def load_module():
    spec = importlib.util.spec_from_file_location("retrieval_evaluation",
                                                  ROOT / "scripts/16_retrieval_evaluation.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


evaluation = load_module()

PROTECTED_BASELINE = {
    "data/embeddings/bge_m3_dense.npy": "99e3b79033a996ffb08b4b742faf68ec217a5a49d0cfdb05175996d65de1d4d3",
    "data/embeddings/bge_m3_chunk_ids.json": "7497af0d7d7032eb4c2400f74f6f1f694ab80ce3a594be416bd66bd808cf86bd",
    "data/metadata/full_embedding_manifest.csv": "68be1f5fa0b7b6078cd9f492a8732aa796b2ab6536c4b76454e5a37bd41bc32a",
    "data/chunks/chunks.jsonl": "e751fcfc3cc6828b05f75f494fd9a31b44388abda9daf83fb9581581ef79df5b",
    "data/chunks_recovery/chunks.jsonl": "835fc871ee53253d4d95eca14c7c13d908f7d06e559cf657f71c954196fd07f7",
}

_CACHE: dict[str, object] = {}


def benchmark():
    if "rows" not in _CACHE:
        rows, problems = evaluation.build_benchmark(ROOT)
        _CACHE["rows"], _CACHE["problems"] = rows, problems
    return _CACHE["rows"], _CACHE["problems"]


def frozen_queries():
    path = ROOT / "data/evaluation/retrieval_queries_v1.jsonl"
    if not path.is_file():
        return None
    return evaluation.read_jsonl(path)


def metrics_file():
    path = ROOT / "data/evaluation/dense_v1_metrics.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


class TestBenchmarkSchema(unittest.TestCase):
    def test_benchmark_builds_without_problems(self):
        rows, problems = benchmark()
        self.assertEqual(problems, [])
        self.assertGreaterEqual(len(rows), 80)

    def test_required_fields_present(self):
        rows, _ = benchmark()
        required = {"query_id", "query", "language", "query_type", "difficulty", "topic",
                    "gold_document_ids", "gold_chunk_ids", "acceptable_document_ids",
                    "acceptable_chunk_ids", "source_evidence", "annotation_method", "notes"}
        for row in rows:
            self.assertTrue(required.issubset(set(row.keys())), row["query_id"])

    def test_query_ids_unique(self):
        rows, _ = benchmark()
        identifiers = [row["query_id"] for row in rows]
        self.assertEqual(len(set(identifiers)), len(identifiers))

    def test_query_text_unique(self):
        rows, _ = benchmark()
        texts = [row["query"].strip().lower() for row in rows]
        self.assertEqual(len(set(texts)), len(texts))

    def test_every_query_has_gold(self):
        rows, _ = benchmark()
        self.assertEqual([row["query_id"] for row in rows if not row["gold_chunk_ids"]], [])

    def test_gold_chunks_exist_in_index(self):
        rows, _ = benchmark()
        known = {record["chunk_id"] for record in evaluation.load_corpus(ROOT)}
        for row in rows:
            missing = [chunk_id for chunk_id in row["gold_chunk_ids"] if chunk_id not in known]
            self.assertEqual(missing, [], row["query_id"])

    def test_gold_documents_exist(self):
        rows, _ = benchmark()
        known = {record["document_id"] for record in evaluation.load_corpus(ROOT)}
        for row in rows:
            self.assertTrue(set(row["gold_document_ids"]).issubset(known), row["query_id"])

    def test_gold_is_subset_of_acceptable(self):
        rows, _ = benchmark()
        for row in rows:
            self.assertTrue(set(row["gold_chunk_ids"]).issubset(set(row["acceptable_chunk_ids"])),
                            row["query_id"])

    def test_both_languages_represented(self):
        rows, _ = benchmark()
        languages = Counter(row["language"] for row in rows)
        self.assertGreaterEqual(languages["tr"] / len(rows), 0.35)
        self.assertGreaterEqual(languages["en"] / len(rows), 0.35)

    def test_query_types_are_stratified(self):
        rows, _ = benchmark()
        types = Counter(row["query_type"] for row in rows)
        for expected in ("definition", "design", "construction", "geotechnical", "operations",
                         "safety", "regulation", "numeric", "named_entity", "source_specific"):
            self.assertGreaterEqual(types[expected], 5, expected)

    def test_smoke_queries_do_not_dominate(self):
        rows, _ = benchmark()
        reused = sum(row["reused_smoke_query"] for row in rows)
        self.assertLessEqual(reused / len(rows), 0.15)

    def test_source_evidence_present_for_every_query(self):
        rows, _ = benchmark()
        for row in rows:
            self.assertTrue(row["source_evidence"], row["query_id"])
            self.assertIn("chunk_id", row["source_evidence"][0])

    def test_annotation_method_is_lexical_not_embedding(self):
        rows, _ = benchmark()
        for row in rows:
            self.assertIn("anchor", row["annotation_method"])
            self.assertNotIn("embedding", row["annotation_method"])
            self.assertNotIn("similarity", row["annotation_method"])

    def test_gold_sets_are_discriminating(self):
        """Gold must not cover so much of the corpus that Recall@k is trivially 1."""
        rows, _ = benchmark()
        sizes = sorted(len(row["gold_chunk_ids"]) for row in rows)
        median = sizes[len(sizes) // 2]
        self.assertLess(median, 40)
        self.assertLess(max(sizes), 400)

    def test_benchmark_build_is_deterministic(self):
        first, _ = evaluation.build_benchmark(ROOT)
        second, _ = evaluation.build_benchmark(ROOT)
        self.assertEqual([row["query_id"] for row in first], [row["query_id"] for row in second])
        self.assertEqual([row["gold_chunk_ids"] for row in first], [row["gold_chunk_ids"] for row in second])


class TestBenchmarkFreeze(unittest.TestCase):
    def test_frozen_file_matches_manifest_hash(self):
        path = ROOT / "data/evaluation/retrieval_queries_v1.jsonl"
        manifest_path = ROOT / "data/evaluation/retrieval_benchmark_v1_manifest.json"
        if not (path.is_file() and manifest_path.is_file()):
            self.skipTest("benchmark not frozen yet")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(evaluation.sha256(path.read_bytes()), manifest["sha256"])
        self.assertEqual(manifest["query_count"], len(evaluation.read_jsonl(path)))

    def test_manifest_records_provenance(self):
        manifest_path = ROOT / "data/evaluation/retrieval_benchmark_v1_manifest.json"
        if not manifest_path.is_file():
            self.skipTest("benchmark not frozen yet")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for field in ("benchmark_version", "query_count", "sha256", "embedding_model",
                      "model_revision", "annotation_policy"):
            self.assertIn(field, manifest)
        self.assertEqual(manifest["model_revision"], evaluation.MODEL_REVISION)

    def test_frozen_benchmark_matches_current_build(self):
        frozen = frozen_queries()
        if frozen is None:
            self.skipTest("benchmark not frozen yet")
        rows, _ = benchmark()
        self.assertEqual([row["query_id"] for row in frozen], [row["query_id"] for row in rows])


class TestMetricFunctions(unittest.TestCase):
    def hits(self, chunk_ids):
        return [{"rank": index + 1, "chunk_id": chunk_id, "document_id": chunk_id.split("-")[0],
                 "is_low_content": False, "score": 1.0 - index * 0.01, "contains_table": False}
                for index, chunk_id in enumerate(chunk_ids)]

    def row(self, gold, acceptable=None):
        return {"gold_chunk_ids": gold, "acceptable_chunk_ids": acceptable or gold,
                "gold_document_ids": [c.split("-")[0] for c in gold],
                "acceptable_document_ids": [c.split("-")[0] for c in (acceptable or gold)]}

    def test_recall_at_k(self):
        hits = self.hits([f"D{i}-C{i}" for i in range(20)])
        metrics = evaluation.query_metrics(hits, self.row(["D3-C3"]))
        self.assertEqual(metrics["recall@1"], 0.0)
        self.assertEqual(metrics["recall@5"], 1.0)
        self.assertEqual(metrics["recall@10"], 1.0)

    def test_recall_zero_when_absent(self):
        hits = self.hits([f"D{i}-C{i}" for i in range(20)])
        metrics = evaluation.query_metrics(hits, self.row(["ZZ-C1"]))
        self.assertEqual(metrics["recall@10"], 0.0)
        self.assertEqual(metrics["mrr@10"], 0.0)

    def test_mrr_uses_first_relevant_rank(self):
        hits = self.hits(["A-C1", "B-C1", "C-C1"])
        self.assertAlmostEqual(evaluation.query_metrics(hits, self.row(["B-C1"]))["mrr@10"], 0.5)
        self.assertAlmostEqual(evaluation.query_metrics(hits, self.row(["A-C1"]))["mrr@10"], 1.0)

    def test_ndcg_rewards_higher_ranks(self):
        hits = self.hits(["A-C1", "B-C1", "C-C1"])
        high = evaluation.ndcg_at_k(hits, {"A-C1"}, {"A-C1"}, 10)
        low = evaluation.ndcg_at_k(hits, {"C-C1"}, {"C-C1"}, 10)
        self.assertGreater(high, low)
        self.assertAlmostEqual(high, 1.0)

    def test_ndcg_is_zero_without_relevant(self):
        hits = self.hits(["A-C1", "B-C1"])
        self.assertEqual(evaluation.ndcg_at_k(hits, {"Z-C1"}, {"Z-C1"}, 10), 0.0)

    def test_document_level_metrics(self):
        hits = self.hits(["A-C1", "B-C2", "C-C3"])
        metrics = evaluation.query_metrics(hits, self.row(["B-C9"]))
        self.assertEqual(metrics["recall@10"], 0.0)
        self.assertEqual(metrics["doc_recall@10"], 1.0)
        self.assertAlmostEqual(metrics["doc_mrr@10"], 0.5)

    def test_unique_document_counting(self):
        hits = self.hits(["A-C1", "A-C2", "A-C3", "B-C1", "C-C1"])
        metrics = evaluation.query_metrics(hits, self.row(["A-C1"]))
        self.assertEqual(metrics["unique_docs@5"], 3)

    def test_percentile_and_distribution(self):
        values = [float(v) for v in range(1, 101)]
        self.assertAlmostEqual(evaluation.percentile(values, .5), 50.5)
        dist = evaluation.distribution(values)
        self.assertEqual(dist["min"], 1.0)
        self.assertEqual(dist["max"], 100.0)


class TestSimulations(unittest.TestCase):
    def entry(self, chunk_ids, gold, low=None, scores=None):
        low = low or set()
        hits = [{"rank": i + 1, "chunk_id": c, "document_id": c.split("-")[0],
                 "is_low_content": c in low, "contains_table": False,
                 "score": scores[i] if scores else 1.0 - i * 0.05}
                for i, c in enumerate(chunk_ids)]
        row = {"gold_chunk_ids": gold, "acceptable_chunk_ids": gold,
               "gold_document_ids": [c.split("-")[0] for c in gold],
               "acceptable_document_ids": [c.split("-")[0] for c in gold]}
        return {"hits": hits, "row": row, "exact_ids": list(range(len(chunk_ids)))}

    def test_threshold_simulation_reduces_kept_results(self):
        entries = [self.entry(["A-C1", "B-C1", "C-C1"], ["A-C1"], scores=[0.9, 0.5, 0.2])]
        low = evaluation.simulate_threshold(entries, 0.30)
        high = evaluation.simulate_threshold(entries, 0.80)
        self.assertGreater(low["kept_results"], high["kept_results"])
        self.assertEqual(high["kept_results"], 1)

    def test_threshold_records_no_result_queries(self):
        entries = [self.entry(["A-C1"], ["A-C1"], scores=[0.2])]
        result = evaluation.simulate_threshold(entries, 0.90)
        self.assertEqual(result["queries_with_no_result"], 1)
        self.assertEqual(result["no_result_rate"], 1.0)

    def test_low_content_exclusion_removes_flagged_hits(self):
        entries = [self.entry(["L-C1", "A-C1"], ["A-C1"], low={"L-C1"})]
        baseline = evaluation.simulate_low_content(entries, "baseline")
        excluded = evaluation.simulate_low_content(entries, "exclude")
        self.assertGreater(baseline["low_content@5"], excluded["low_content@5"])
        self.assertEqual(excluded["recall@1"], 1.0)

    def test_low_content_penalty_reorders(self):
        entries = [self.entry(["L-C1", "A-C1"], ["A-C1"], low={"L-C1"}, scores=[0.60, 0.58])]
        penalised = evaluation.simulate_low_content(entries, "penalty", 0.05)
        self.assertEqual(penalised["recall@1"], 1.0)

    def test_diversity_cap_limits_per_document(self):
        entries = [self.entry(["A-C1", "A-C2", "A-C3", "B-C1"], ["B-C1"])]
        capped = evaluation.simulate_diversity(entries, 1)
        self.assertEqual(capped["recall@5"], 1.0)
        self.assertGreaterEqual(capped["unique_docs@5"], 2)

    def test_ann_recall_perfect_when_identical(self):
        entry = self.entry([f"A-C{i}" for i in range(20)], ["A-C0"])
        for index, hit in enumerate(entry["hits"]):
            hit["point_id"] = index
        result = evaluation.ann_recall([entry])
        self.assertAlmostEqual(result["ann_recall@10"], 1.0)
        self.assertAlmostEqual(result["top1_agreement"], 1.0)

    def test_ann_recall_detects_divergence(self):
        entry = self.entry([f"A-C{i}" for i in range(20)], ["A-C0"])
        for index, hit in enumerate(entry["hits"]):
            hit["point_id"] = index + 100
        result = evaluation.ann_recall([entry])
        self.assertEqual(result["ann_recall@10"], 0.0)


class TestFailureClassification(unittest.TestCase):
    def test_cross_lingual_takes_priority(self):
        entry = {"row": {"cross_lingual": True, "gold_document_ids": [], "gold_chunk_ids": ["X"],
                         "query_type": "design"},
                 "hits": [], "exact_ids": []}
        self.assertEqual(evaluation.classify_failure(entry, {}), "cross_lingual")

    def test_chunk_boundary_when_document_found(self):
        hits = [{"chunk_id": "A-C9", "document_id": "A", "is_low_content": False,
                 "contains_table": False, "point_id": 1}]
        entry = {"row": {"cross_lingual": False, "gold_document_ids": ["A"], "gold_chunk_ids": ["A-C1"],
                         "query_type": "design"}, "hits": hits, "exact_ids": [1]}
        self.assertEqual(evaluation.classify_failure(entry, {}), "chunk_boundary")

    def test_failure_csv_structure(self):
        path = ROOT / "data/evaluation/dense_v1_failures.csv"
        if not path.is_file():
            self.skipTest("failures not generated yet")
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        required = {"query_id", "query", "language", "query_type", "difficulty", "likely_cause"}
        if rows:
            self.assertTrue(required.issubset(set(rows[0].keys())))
            for row in rows:
                self.assertTrue(row["likely_cause"])


class TestResultsArtifacts(unittest.TestCase):
    def test_results_jsonl_structure(self):
        path = ROOT / "data/evaluation/dense_v1_results.jsonl"
        if not path.is_file():
            self.skipTest("results not generated yet")
        rows = evaluation.read_jsonl(path)
        required = {"query_id", "query", "rank", "score", "point_id", "chunk_id", "document_id",
                    "source_kind", "is_low_content", "heading", "section_path", "gold_chunk_match",
                    "acceptable_chunk_match", "gold_document_match", "acceptable_document_match"}
        self.assertTrue(required.issubset(set(rows[0].keys())))

    def test_results_are_ordered_by_rank_within_query(self):
        path = ROOT / "data/evaluation/dense_v1_results.jsonl"
        if not path.is_file():
            self.skipTest("results not generated yet")
        grouped: dict[str, list[int]] = {}
        for row in evaluation.read_jsonl(path):
            grouped.setdefault(row["query_id"], []).append(row["rank"])
        for query_id, ranks in grouped.items():
            self.assertEqual(ranks, sorted(ranks), query_id)
            self.assertEqual(ranks[0], 1, query_id)

    def test_results_scores_are_descending(self):
        path = ROOT / "data/evaluation/dense_v1_results.jsonl"
        if not path.is_file():
            self.skipTest("results not generated yet")
        grouped: dict[str, list[float]] = {}
        for row in evaluation.read_jsonl(path):
            grouped.setdefault(row["query_id"], []).append(row["score"])
        for query_id, scores in grouped.items():
            self.assertEqual(scores, sorted(scores, reverse=True), query_id)

    def test_metrics_file_has_required_sections(self):
        metrics = metrics_file()
        if metrics is None:
            self.skipTest("metrics not generated yet")
        for section in ("overall", "by_language", "by_difficulty", "by_query_type", "score_distribution",
                        "thresholds", "low_content", "diversity", "ann", "latency"):
            self.assertIn(section, metrics)

    def test_metrics_are_in_valid_range(self):
        metrics = metrics_file()
        if metrics is None:
            self.skipTest("metrics not generated yet")
        for key, value in metrics["overall"].items():
            if key.startswith(("recall", "acceptable", "doc_recall", "precision", "mrr", "ndcg", "doc_mrr")):
                self.assertGreaterEqual(value, 0.0, key)
                self.assertLessEqual(value, 1.0, key)

    def test_recall_is_monotonic_in_k(self):
        metrics = metrics_file()
        if metrics is None:
            self.skipTest("metrics not generated yet")
        overall = metrics["overall"]
        values = [overall[f"recall@{k}"] for k in (1, 3, 5, 10, 20)]
        self.assertEqual(values, sorted(values))


class TestProtectedInputs(unittest.TestCase):
    def test_protected_artifacts_unchanged(self):
        for relative, expected in PROTECTED_BASELINE.items():
            self.assertEqual(evaluation.sha256((ROOT / relative).read_bytes()), expected,
                             f"protected artefact modified: {relative}")

    def test_protected_state_stable(self):
        self.assertEqual(evaluation.protected_state(ROOT), evaluation.protected_state(ROOT))


@unittest.skipUnless(LIVE, "set TUNNELBOOK_QDRANT_LIVE=1 for live retrieval tests")
class TestLiveRetrieval(unittest.TestCase):
    def test_query_embedding_is_deterministic(self):
        import numpy
        first, _, _ = evaluation.embed_queries(["tunnel ventilation design"])
        second, _, _ = evaluation.embed_queries(["tunnel ventilation design"])
        self.assertLess(float(numpy.abs(first - second).max()), 1e-5)

    def test_query_embedding_is_unit_normalised(self):
        import numpy
        vectors, _, _ = evaluation.embed_queries(["shotcrete lining"])
        self.assertAlmostEqual(float(numpy.linalg.norm(vectors[0])), 1.0, places=4)

    def test_exact_numpy_retrieval_matches_stored_vectors(self):
        import numpy
        vectors = numpy.load(ROOT / "data/embeddings/bge_m3_dense.npy")
        query, _, _ = evaluation.embed_queries(["NATM"])
        scores = vectors @ query[0]
        self.assertEqual(scores.shape[0], vectors.shape[0])
        self.assertLessEqual(float(scores.max()), 1.0001)


if __name__ == "__main__":
    unittest.main()
