from __future__ import annotations

import importlib.util
import json
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = os.environ.get("TUNNELBOOK_QDRANT_LIVE") == "1"


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


lang = load("language_aware", "scripts/18_language_aware_retrieval.py")
improvement = load("improvement", "scripts/17_retrieval_improvement.py")
evaluation = load("evaluation", "scripts/16_retrieval_evaluation.py")

PROTECTED_BASELINE = {
    "data/embeddings/bge_m3_dense.npy": "99e3b79033a996ffb08b4b742faf68ec217a5a49d0cfdb05175996d65de1d4d3",
    "data/chunks/chunks.jsonl": "e751fcfc3cc6828b05f75f494fd9a31b44388abda9daf83fb9581581ef79df5b",
    "data/evaluation/retrieval_queries_v1.jsonl":
        "90aac5f98a75373fea0a0c6d04527a0e68231bd368a2d2b20fcc83ea78b71dd6",
}

_C: dict = {}


def detector():
    if "d" not in _C:
        _C["r"] = evaluation.load_corpus(ROOT)
        _C["d"] = lang.LanguageDetector(_C["r"], improvement.tokenize)
    return _C["d"]


def records():
    detector()
    return _C["r"]


class TestDetector(unittest.TestCase):
    def test_turkish_detected(self):
        for q in ["tünel havalandırma sistemi", "kaya bulonu çekme deneyi", "püskürtme beton uygulaması"]:
            self.assertEqual(detector().detect(q)["language"], "tr", q)

    def test_english_detected(self):
        for q in ["tunnel ventilation system", "rock bolt pull out test", "shotcrete application"]:
            self.assertEqual(detector().detect(q)["language"], "en", q)

    def test_acronym_only_is_unknown(self):
        for q in ["TBM", "NATM RMR GSI", "EN 1997", "ASTM D1586", "KGM", "351.08.07"]:
            self.assertEqual(detector().detect(q)["language"], "unknown", q)

    def test_technical_token_classification(self):
        d = detector()
        for token in ("TBM", "NATM", "EN", "1997", "D1586", "351.08.07"):
            self.assertTrue(d.technical(token), token)
        for token in ("tunnel", "havalandırma", "design"):
            self.assertFalse(d.technical(token), token)

    def test_detection_is_deterministic(self):
        d = detector()
        for q in ["tünel drenaj sistemi", "tunnel drainage system", "TBM"]:
            self.assertEqual(d.detect(q), d.detect(q))

    def test_turkish_diacritic_is_decisive(self):
        self.assertEqual(detector().detect("şev stabilitesi")["reason"], "turkish_diacritic")

    def test_detector_uses_no_gold_information(self):
        source = (ROOT / "scripts/18_language_aware_retrieval.py").read_text(encoding="utf-8")
        detect_src = source[source.index("def detect(self"):source.index("# ------", source.index("def detect(self"))]
        for forbidden in ("gold_", "gold_chunk", "gold_document", "benchmark"):
            self.assertNotIn(forbidden, detect_src)

    def test_audit_file_shape(self):
        path = ROOT / "data/evaluation/language_detector_audit.jsonl"
        if not path.is_file():
            self.skipTest("audit not generated")
        rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertGreaterEqual(len(rows), 50)
        self.assertGreaterEqual(sum(1 for r in rows if r["expected"] == "tr"), 20)
        self.assertGreaterEqual(sum(1 for r in rows if r["expected"] == "en"), 20)
        self.assertGreaterEqual(sum(1 for r in rows if r["expected"] == "unknown"), 10)


class TestRouting(unittest.TestCase):
    def test_same_language_bm25_filters_by_metadata(self):
        recs = records()
        index, _ = improvement.build_bm25(ROOT, recs)
        languages = [(r.get("language") or "unknown").lower() for r in recs]
        order, pool = lang.same_language_bm25(index, improvement.tokenize,
                                              "püskürtme beton", languages, "tr", 20)
        self.assertTrue(order)
        for position in order:
            self.assertEqual(languages[position], "tr")

    def test_unknown_language_returns_empty_bm25(self):
        recs = records()
        index, _ = improvement.build_bm25(ROOT, recs)
        languages = [(r.get("language") or "unknown").lower() for r in recs]
        order, _ = lang.same_language_bm25(index, improvement.tokenize, "TBM", languages, "unknown", 20)
        self.assertEqual(order, [])

    def test_dense_protection_preserves_head(self):
        dense = [10, 11, 12, 13, 14]
        fused = [99, 12, 10, 77]
        out = lang.dense_protected(dense, fused, 3)
        self.assertEqual(out[:3], [10, 11, 12])
        self.assertEqual(len(out), len(set(out)))

    def test_dense_protection_depth_five(self):
        dense = list(range(10))
        out = lang.dense_protected(dense, [99, 5, 1], 5)
        self.assertEqual(out[:5], [0, 1, 2, 3, 4])

    def test_rrf_deterministic(self):
        a = improvement.rrf([[1, 2, 3], [3, 1]], 30)
        b = improvement.rrf([[1, 2, 3], [3, 1]], 30)
        self.assertEqual(a, b)
        self.assertEqual(improvement.fused_order(a, {1: 0, 2: 1, 3: 2}),
                         improvement.fused_order(b, {1: 0, 2: 1, 3: 2}))

    def test_predeclared_constants(self):
        self.assertEqual(lang.LANG_MARGIN, 2.0)
        self.assertEqual(lang.GATE_MIN_TERMS, 2)
        self.assertEqual(lang.PROTECT_DEPTHS, (3, 5))


class TestIntegrity(unittest.TestCase):
    def test_protected_artifacts_unchanged(self):
        for rel, expected in PROTECTED_BASELINE.items():
            self.assertEqual(lang.sha256((ROOT / rel).read_bytes()), expected, rel)

    def test_benchmark_v1_unchanged(self):
        manifest = json.loads((ROOT / "data/evaluation/retrieval_benchmark_v1_manifest.json")
                              .read_text(encoding="utf-8"))
        actual = lang.sha256((ROOT / "data/evaluation/retrieval_queries_v1.jsonl").read_bytes())
        self.assertEqual(actual, manifest["sha256"])
        self.assertEqual(manifest["query_count"], 114)

    def test_probe_v2_unchanged(self):
        rows = lang.read_jsonl(ROOT / "data/evaluation/crosslingual_probe_v2.jsonl")
        self.assertEqual(len(rows), 27)
        for r in rows:
            self.assertTrue(r["cross_lingual"])
            self.assertNotEqual(r["language"], r["gold_language"])

    def test_existing_candidate_not_overwritten(self):
        c = json.loads((ROOT / "data/metadata/retriever_v1_candidate.json").read_text(encoding="utf-8"))
        self.assertEqual(c["retriever"], "HYBRID_RRF_30")
        self.assertEqual(c["status"], "candidate_pending_freeze")

    def test_bm25_core_index_not_mutated(self):
        stats = json.loads((ROOT / "data/retrieval/bm25_v1/index_stats.json").read_text(encoding="utf-8"))
        self.assertEqual(stats["documents"], 5992)
        self.assertEqual(stats["bm25_version"], "bm25plus-v1")

    def test_routing_metadata_is_separate(self):
        path = ROOT / "data/retrieval/language_routing_v1/routing_stats.json"
        if not path.is_file():
            self.skipTest("routing metadata not generated")
        self.assertTrue(str(path).endswith("language_routing_v1/routing_stats.json"))


class TestResults(unittest.TestCase):
    def metrics(self):
        path = ROOT / "data/evaluation/language_aware_retrieval_metrics.json"
        if not path.is_file():
            self.skipTest("metrics not generated")
        return json.loads(path.read_text(encoding="utf-8"))

    def test_all_variants_evaluated_on_both_benchmarks(self):
        m = self.metrics()
        for name in ("DENSE_V1", "HYBRID_RRF_30", "LANG_HYBRID_SAME_RRF30",
                     "LANG_HYBRID_GATED_RRF30", "LANG_HYBRID_DENSE_PROTECTED_3"):
            self.assertIn(name, m["benchmark_v1"])
            self.assertIn(name, m["probe_v2"])

    def test_results_jsonl_covers_both_benchmarks(self):
        path = ROOT / "data/evaluation/language_aware_retrieval_results.jsonl"
        if not path.is_file():
            self.skipTest("results not generated")
        rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertEqual({r["benchmark"] for r in rows}, {"v1", "probe_v2"})

    def test_metrics_in_valid_range(self):
        m = self.metrics()
        for section in ("benchmark_v1", "probe_v2", "monolingual_v1"):
            for values in m[section].values():
                for k, v in values.items():
                    self.assertGreaterEqual(v, 0.0)
                    self.assertLessEqual(v, 1.0)

    def test_qdrant_read_only(self):
        m = self.metrics()
        self.assertEqual(m["qdrant"]["before"], 5992)
        self.assertEqual(m["qdrant"]["after"], 5992)

    def test_no_protected_change_recorded(self):
        self.assertEqual(self.metrics()["protected_changed"], [])


@unittest.skipUnless(LIVE, "set TUNNELBOOK_QDRANT_LIVE=1")
class TestLive(unittest.TestCase):
    def test_collection_unchanged(self):
        from qdrant_client import QdrantClient
        c = QdrantClient(url=lang.REST_URL, timeout=60)
        self.assertEqual(c.count(collection_name=lang.COLLECTION, exact=True).count, 5992)


if __name__ == "__main__":
    unittest.main()
