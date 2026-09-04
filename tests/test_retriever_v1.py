from __future__ import annotations

import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = os.environ.get("TUNNELBOOK_QDRANT_LIVE") == "1"


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module          # dataclasses need the module registered before exec
    spec.loader.exec_module(module)
    return module


retriever = load("retriever_v1", "scripts/19_retriever_v1.py")

PROTECTED = {
    "data/embeddings/bge_m3_dense.npy": "99e3b79033a996ffb08b4b742faf68ec217a5a49d0cfdb05175996d65de1d4d3",
    "data/chunks/chunks.jsonl": "e751fcfc3cc6828b05f75f494fd9a31b44388abda9daf83fb9581581ef79df5b",
    "data/chunks_recovery/chunks.jsonl": "835fc871ee53253d4d95eca14c7c13d908f7d06e559cf657f71c954196fd07f7",
    "data/evaluation/retrieval_queries_v1.jsonl":
        "90aac5f98a75373fea0a0c6d04527a0e68231bd368a2d2b20fcc83ea78b71dd6",
}

_C: dict = {}


def client():
    if "r" not in _C:
        try:
            instance = retriever.RetrieverV1()
            instance.health()
            _C["r"] = instance
        except Exception as error:
            raise unittest.SkipTest(f"retriever unavailable: {error}")
    return _C["r"]


class TestReleaseConfig(unittest.TestCase):
    def test_retriever_is_dense_v1(self):
        self.assertEqual(retriever.RETRIEVER, "DENSE_V1")
        self.assertEqual(retriever.release_config()["retriever"], "DENSE_V1")

    def test_model_revision_pinned(self):
        self.assertEqual(retriever.DENSE_MODEL, "BAAI/bge-m3")
        self.assertEqual(retriever.DENSE_MODEL_REVISION,
                         "5617a9f61b028005a4858fdac845db406aefb181")

    def test_dimension_and_distance(self):
        config = retriever.release_config()
        self.assertEqual(config["embedding_dimension"], 1024)
        self.assertEqual(config["distance"], "COSINE")
        self.assertEqual(config["max_sequence_length"], 8192)

    def test_no_query_prefix(self):
        config = retriever.release_config()
        self.assertIsNone(config["query_prefix"])
        self.assertIsNone(config["document_prefix"])
        self.assertEqual(config["pooling"], "cls")
        self.assertEqual(config["normalization"], "l2")

    def test_collection_name(self):
        self.assertEqual(retriever.QDRANT_COLLECTION, "tunnelbook_dense_v1")
        self.assertEqual(retriever.EXPECTED_POINTS, 5992)

    def test_all_experimental_components_disabled(self):
        config = retriever.release_config()
        for flag in ("automatic_translation", "automatic_language_filter", "bm25", "rrf",
                     "reranker", "neighbor_expansion"):
            self.assertFalse(config[flag], flag)
        for none_field in ("score_threshold", "low_content_penalty", "document_cap"):
            self.assertIsNone(config[none_field], none_field)

    def test_top_k_bounds(self):
        self.assertEqual(retriever.DEFAULT_TOP_K, 10)
        self.assertEqual(retriever.MAXIMUM_TOP_K, 100)


class TestNoHiddenDependencies(unittest.TestCase):
    """Assert on executable code, not prose.

    The module docstring deliberately names BM25, reranking and translation to record why each was
    excluded; grepping raw text would flag that documentation. These tests parse the AST instead, so
    they catch a real dependency and ignore an explanatory comment.
    """

    def tree(self):
        import ast
        return ast.parse((ROOT / "scripts/19_retriever_v1.py").read_text(encoding="utf-8"))

    def imported_names(self):
        import ast
        names = set()
        for node in ast.walk(self.tree()):
            if isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module or "")
                names.update(alias.name for alias in node.names)
        return names

    def code_without_docstrings(self):
        """Executable logic only.

        Docstrings are stripped (they document what was excluded) and `release_config` is excluded
        too: its keys are the disable flags themselves (`"bm25": False`), so their presence is
        evidence the feature is off, not evidence it is used. The flags are asserted separately.
        """
        import ast
        tree = self.tree()
        tree.body = [node for node in tree.body
                     if not (isinstance(node, ast.FunctionDef) and node.name == "release_config")]
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if (node.body and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, ast.Constant)
                        and isinstance(node.body[0].value.value, str)):
                    node.body.pop(0)
        return ast.unparse(tree)

    def test_disable_flags_are_all_false(self):
        config = retriever.release_config()
        for flag in ("bm25", "rrf", "reranker", "neighbor_expansion", "automatic_translation",
                     "automatic_language_filter"):
            self.assertIs(config[flag], False, flag)

    def test_does_not_import_experimental_scripts(self):
        names = " ".join(self.imported_names())
        for forbidden in ("17_retrieval_improvement", "18_language_aware_retrieval",
                          "16_retrieval_evaluation", "retrieval_improvement",
                          "language_aware", "retrieval_evaluation"):
            self.assertNotIn(forbidden, names)

    def test_imports_are_minimal_and_expected(self):
        allowed = {"hashlib", "os", "dataclasses", "dataclass", "asdict", "field", "pathlib",
                   "Path", "typing", "Any", "__future__", "annotations", "torch", "transformers",
                   "AutoModel", "AutoTokenizer", "qdrant_client", "QdrantClient", "models",
                   "json", "sys"}
        self.assertTrue(self.imported_names().issubset(allowed),
                        f"unexpected imports: {self.imported_names() - allowed}")

    def test_no_bm25_or_fusion_logic_in_code(self):
        code = self.code_without_docstrings().lower()
        for forbidden in ("bm25", "rrf", "reciprocal", "idf", "postings"):
            self.assertNotIn(forbidden, code)

    def test_no_translation_or_reranker_in_code(self):
        code = self.code_without_docstrings().lower()
        for forbidden in ("lmstudio", "localhost:1234", "chat/completions", "translat",
                          "sequenceclassification", "rerank", "cross_encoder"):
            self.assertNotIn(forbidden, code)

    def test_no_language_detection_in_code(self):
        code = self.code_without_docstrings().lower()
        for forbidden in ("detect(", "languagedetector", "log_odds", "logodds"):
            self.assertNotIn(forbidden, code)

    def test_no_automatic_language_filtering(self):
        self.assertFalse(retriever.release_config()["automatic_language_filter"])
        # language exists only as an explicit caller-supplied filter
        self.assertIn("language", retriever.SUPPORTED_FILTERS)
        self.assertIsNone(retriever._build_filter(None))


class TestFilters(unittest.TestCase):
    def test_supported_filters(self):
        for field in ("document_id", "language", "document_type", "authority_level",
                      "year", "source_kind"):
            self.assertIn(field, retriever.SUPPORTED_FILTERS)

    def test_no_filter_returns_none(self):
        self.assertIsNone(retriever._build_filter(None))
        self.assertIsNone(retriever._build_filter({}))

    def test_unsupported_filter_rejected(self):
        with self.assertRaises(ValueError):
            retriever._build_filter({"nonexistent_field": "x"})

    def test_filter_builds_for_supported_field(self):
        built = retriever._build_filter({"document_id": "DOC000041"})
        self.assertIsNotNone(built)


class TestValidation(unittest.TestCase):
    def test_empty_query_rejected(self):
        instance = retriever.RetrieverV1(lazy=True)
        for bad in ("", "   ", None):
            with self.assertRaises(ValueError):
                instance.retrieve(bad)

    def test_invalid_top_k_rejected(self):
        instance = retriever.RetrieverV1(lazy=True)
        for bad in (0, -1, 1.5):
            with self.assertRaises(ValueError):
                instance.retrieve("tunnel", top_k=bad)

    def test_top_k_above_maximum_rejected(self):
        instance = retriever.RetrieverV1(lazy=True)
        with self.assertRaises(ValueError):
            instance.retrieve("tunnel", top_k=retriever.MAXIMUM_TOP_K + 1)

    def test_query_too_long_is_explicit_error(self):
        self.assertTrue(issubclass(retriever.QueryTooLong, ValueError))
        source = (ROOT / "scripts/19_retriever_v1.py").read_text(encoding="utf-8")
        self.assertIn("Refusing to truncate silently", source)

    def test_unavailable_is_explicit_error(self):
        self.assertTrue(issubclass(retriever.RetrieverUnavailable, RuntimeError))
        instance = retriever.RetrieverV1(qdrant_url="http://127.0.0.1:59999", lazy=True)
        with self.assertRaises(retriever.RetrieverUnavailable):
            instance._ensure_client()


class TestResultSchema(unittest.TestCase):
    def test_result_exposes_required_fields(self):
        required = {"rank", "score", "point_id", "chunk_id", "document_id", "text", "title",
                    "heading", "section_path", "source_kind", "citation_mode", "provenance_status",
                    "original_page_start", "original_page_end", "slide_start", "slide_end",
                    "source_relative_path", "language", "document_type", "authority_level",
                    "year", "topics", "contains_table", "contains_formula_placeholder",
                    "contains_image_placeholder", "is_low_content"}
        self.assertTrue(required.issubset(set(retriever.RetrievalResult.__dataclass_fields__)))

    def test_result_is_immutable(self):
        self.assertTrue(retriever.RetrievalResult.__dataclass_params__.frozen)


class TestReleaseArtifacts(unittest.TestCase):
    def release(self):
        path = ROOT / "data/metadata/retriever_v1_release.json"
        if not path.is_file():
            self.skipTest("release descriptor not written")
        return json.loads(path.read_text(encoding="utf-8"))

    def test_release_is_frozen_dense_v1(self):
        release = self.release()
        self.assertEqual(release["retriever"], "DENSE_V1")
        self.assertEqual(release["status"], "frozen")
        self.assertEqual(release["qdrant_exact_points"], 5992)

    def test_release_records_script_hash(self):
        release = self.release()
        self.assertEqual(release["retriever_script_sha256"], retriever.script_sha256())

    def test_release_dense_metrics_match_baseline(self):
        release = self.release()
        expected = {"recall@1": 0.4386, "recall@5": 0.6842, "recall@10": 0.7632,
                    "mrr@10": 0.5383, "ndcg@10": 0.5231, "doc_recall@10": 0.8596}
        for key, value in expected.items():
            self.assertAlmostEqual(release["dense_baseline_metrics"][key], value, delta=0.0002)

    def test_release_records_crosslingual_metrics(self):
        release = self.release()
        self.assertAlmostEqual(release["crosslingual_probe_v2_metrics"]["recall@10"], 0.2593, delta=0.001)

    def test_historical_candidate_not_modified(self):
        candidate = json.loads((ROOT / "data/metadata/retriever_v1_candidate.json")
                               .read_text(encoding="utf-8"))
        self.assertEqual(candidate["retriever"], "HYBRID_RRF_30")
        self.assertEqual(candidate["status"], "candidate_pending_freeze")

    def test_selection_history_records_supersession(self):
        path = ROOT / "data/metadata/retriever_selection_history.json"
        if not path.is_file():
            self.skipTest("selection history not written")
        history = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(history["final_release"], "DENSE_V1")
        self.assertEqual(history["candidate"], "HYBRID_RRF_30")
        self.assertEqual(history["candidate_status"], "not_released")
        self.assertEqual(history["reason_not_released"], "cross_lingual_regression")

    def test_manifest_hashes_present(self):
        path = ROOT / "data/metadata/retriever_v1_manifest.json"
        if not path.is_file():
            self.skipTest("manifest not written")
        manifest = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["qdrant_exact_points"], 5992)
        for artifact in ("scripts/19_retriever_v1.py", "data/embeddings/bge_m3_dense.npy"):
            self.assertIn(artifact, manifest["artifacts"])


class TestProtectedIntegrity(unittest.TestCase):
    def test_protected_artifacts_unchanged(self):
        import hashlib
        for rel, expected in PROTECTED.items():
            actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, rel)



class TestReleaseMetadataClosure(unittest.TestCase):
    """Closure defects found in external audit: a wrong created_at and stale manifest hashes."""

    def release_path(self):
        path = ROOT / "data/metadata/retriever_v1_release.json"
        if not path.is_file():
            self.skipTest("release descriptor not written")
        return path

    def release(self):
        return json.loads(self.release_path().read_text(encoding="utf-8"))

    def test_created_at_is_timezone_aware_iso8601(self):
        from datetime import datetime
        stamp = self.release()["created_at"]
        parsed = datetime.fromisoformat(stamp)
        self.assertIsNotNone(parsed.tzinfo, f"created_at is not timezone-aware: {stamp}")
        self.assertIsNotNone(parsed.utcoffset())

    def test_created_at_uses_istanbul_offset(self):
        from datetime import datetime, timedelta
        parsed = datetime.fromisoformat(self.release()["created_at"])
        self.assertEqual(parsed.utcoffset(), timedelta(hours=3),
                         "Europe/Istanbul is +03:00 on this date")

    def test_created_at_is_not_in_the_future(self):
        from datetime import datetime, timezone
        parsed = datetime.fromisoformat(self.release()["created_at"])
        self.assertLessEqual(parsed, datetime.now(timezone.utc),
                             "release timestamp must not be in the future")

    def test_created_at_is_the_freeze_date(self):
        self.assertTrue(self.release()["created_at"].startswith("2026-08-17"),
                        "freeze work occurred on 2026-08-17 Europe/Istanbul")

    def test_manifest_hash_of_release_is_current(self):
        import hashlib
        manifest = json.loads((ROOT / "data/metadata/retriever_v1_manifest.json")
                              .read_text(encoding="utf-8"))
        actual = hashlib.sha256(self.release_path().read_bytes()).hexdigest()
        self.assertEqual(manifest["artifacts"]["data/metadata/retriever_v1_release.json"], actual,
                         "stale manifest hash for the release descriptor")

    def test_all_manifest_hashes_are_current(self):
        import hashlib
        manifest = json.loads((ROOT / "data/metadata/retriever_v1_manifest.json")
                              .read_text(encoding="utf-8"))
        stale = []
        for relative, recorded in manifest["artifacts"].items():
            path = ROOT / relative
            if not path.is_file():
                stale.append(f"{relative} (missing)")
                continue
            if hashlib.sha256(path.read_bytes()).hexdigest() != recorded:
                stale.append(relative)
        self.assertEqual(stale, [], f"stale manifest hashes: {stale}")

    def test_manifest_covers_key_dependencies(self):
        manifest = json.loads((ROOT / "data/metadata/retriever_v1_manifest.json")
                              .read_text(encoding="utf-8"))
        for relative in ("scripts/19_retriever_v1.py", "data/embeddings/bge_m3_dense.npy",
                         "data/metadata/qdrant_dense_release.json",
                         "data/evaluation/retrieval_queries_v1.jsonl"):
            self.assertIn(relative, manifest["artifacts"])

    def test_production_script_hash_matches_module(self):
        import hashlib
        manifest = json.loads((ROOT / "data/metadata/retriever_v1_manifest.json")
                              .read_text(encoding="utf-8"))
        self.assertEqual(manifest["artifacts"]["scripts/19_retriever_v1.py"],
                         retriever.script_sha256())


class TestCitationInventory(unittest.TestCase):
    def inventory(self):
        path = ROOT / "data/metadata/retriever_v1_citation_inventory.json"
        if not path.is_file():
            self.skipTest("citation inventory not generated")
        return json.loads(path.read_text(encoding="utf-8"))

    def test_inventory_totals_match_collection(self):
        inventory = self.inventory()
        self.assertEqual(inventory["exact_points"], 5992)
        self.assertEqual(sum(inventory["citation_modes"].values()), 5992)
        self.assertEqual(sum(inventory["provenance_statuses"].values()), 5992)

    def test_inventory_lists_expected_modes(self):
        modes = self.inventory()["citation_modes"]
        for mode in ("pdf_page", "slide", "document_section", "table_or_sheet", "image",
                     "source_only"):
            self.assertIn(mode, modes)

    def test_inventory_records_no_fabricated_pages(self):
        section = self.inventory()["source_only_by_citation_mode"]
        self.assertEqual(section["fabricated_page_values"], 0)
        self.assertEqual(section["page_values_verbatim_in_own_text"]
                         + section["page_values_inherited_within_document"],
                         section["page_start_non_null"])

    def test_provenance_source_only_has_no_anchors(self):
        section = self.inventory()["source_only_by_provenance_status"]
        for field in ("page_start_non_null", "page_end_non_null", "slide_start_non_null",
                      "slide_end_non_null"):
            self.assertEqual(section[field], 0)


@unittest.skipUnless(LIVE, "set TUNNELBOOK_QDRANT_LIVE=1 for live retriever tests")
class TestLiveRetrieval(unittest.TestCase):
    def test_exact_point_count(self):
        health = client().health()
        self.assertEqual(health["exact_points"], 5992)
        self.assertTrue(health["healthy"])

    def test_query_vector_is_unit_normalised_1024(self):
        import numpy
        vector = client().embed_query("tunnel ventilation")
        self.assertEqual(vector.shape, (1024,))
        self.assertAlmostEqual(float(numpy.linalg.norm(vector)), 1.0, places=4)

    def test_deterministic_ranking(self):
        first = [r.chunk_id for r in client().retrieve("tunnel ventilation design", top_k=10)]
        second = [r.chunk_id for r in client().retrieve("tunnel ventilation design", top_k=10)]
        self.assertEqual(first, second)

    def test_scores_descending(self):
        scores = [r.score for r in client().retrieve("shotcrete", top_k=10)]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_payload_and_citation_present(self):
        for result in client().retrieve("tünel havalandırması", top_k=5):
            self.assertTrue(result.text)
            self.assertTrue(result.chunk_id)
            self.assertTrue(result.document_id)
            self.assertIsNotNone(result.citation_mode)
            self.assertIsNotNone(result.provenance_status)

    def test_source_only_provenance_status_has_no_anchor(self):
        """`provenance_status == source_only` is the field meaning "no resolvable anchor".

        Verified over the whole collection, not a lucky top-20: all 539 such chunks must have null
        page AND slide fields. Reading points directly is deliberate - a keyword query cannot be
        relied on to surface this class, and a vacuous pass would prove nothing.
        """
        from qdrant_client import models
        instance = client()
        instance._ensure_client()
        matched = 0
        offset = None
        while True:
            batch, offset = instance._client.scroll(
                collection_name=retriever.QDRANT_COLLECTION, limit=1024, offset=offset,
                scroll_filter=models.Filter(must=[models.FieldCondition(
                    key="provenance_status", match=models.MatchValue(value="source_only"))]),
                with_payload=["original_page_start", "original_page_end", "slide_start",
                              "slide_end", "chunk_id"], with_vectors=False)
            for record in batch:
                matched += 1
                for field in ("original_page_start", "original_page_end", "slide_start", "slide_end"):
                    self.assertIsNone(record.payload.get(field),
                                      f"{record.payload.get('chunk_id')}.{field} fabricated")
            if offset is None:
                break
        self.assertEqual(matched, 539, "source_only provenance population changed")
        self.assertGreater(matched, 0, "test would otherwise be vacuous")

    def test_source_only_citation_mode_contract(self):
        """`citation_mode == source_only` means cite-by-source, NOT "no page number".

        Measured against the frozen index: 71 such chunks, 50 of which legitimately carry
        source-derived page markers. Asserting page-is-None here would fail on real data, so the
        contract actually enforced is: slide fields always null, and no fabricated page values.
        """
        from qdrant_client import models
        instance = client()
        instance._ensure_client()
        matched = with_page = 0
        offset = None
        while True:
            batch, offset = instance._client.scroll(
                collection_name=retriever.QDRANT_COLLECTION, limit=1024, offset=offset,
                scroll_filter=models.Filter(must=[models.FieldCondition(
                    key="citation_mode", match=models.MatchValue(value="source_only"))]),
                with_payload=["original_page_start", "original_page_end", "slide_start",
                              "slide_end", "chunk_id"], with_vectors=False)
            for record in batch:
                matched += 1
                payload = record.payload
                self.assertIsNone(payload.get("slide_start"))
                self.assertIsNone(payload.get("slide_end"))
                if payload.get("original_page_start") is not None:
                    with_page += 1
                    self.assertIsNotNone(payload.get("original_page_end"))
                    self.assertGreaterEqual(payload["original_page_start"], 1)
            if offset is None:
                break
        self.assertEqual(matched, 71)
        self.assertEqual(with_page, 50)
        self.assertGreater(matched, 0, "test would otherwise be vacuous")

    def test_source_only_fixtures_retrievable_by_id(self):
        """Deterministic known chunks that are source_only in BOTH fields."""
        instance = client()
        instance._ensure_client()
        expected = ["DOC000237-C0001", "DOC000237-C0002", "DOC000239-C0001",
                    "DOC000246-C0001", "DOC000246-C0002", "DOC000254-C0001"]
        from qdrant_client import models
        records, _ = instance._client.scroll(
            collection_name=retriever.QDRANT_COLLECTION, limit=50,
            scroll_filter=models.Filter(must=[
                models.FieldCondition(key="citation_mode",
                                      match=models.MatchValue(value="source_only")),
                models.FieldCondition(key="provenance_status",
                                      match=models.MatchValue(value="source_only"))]),
            with_payload=["chunk_id", "original_page_start", "slide_start"], with_vectors=False)
        found = sorted(r.payload["chunk_id"] for r in records)
        self.assertEqual(found, expected)
        for record in records:
            self.assertIsNone(record.payload.get("original_page_start"))
            self.assertIsNone(record.payload.get("slide_start"))

    def test_explicit_document_filter(self):
        results = client().retrieve("tunnel", top_k=10, filters={"document_id": "DOC000041"})
        self.assertTrue(results)
        for result in results:
            self.assertEqual(result.document_id, "DOC000041")

    def test_explicit_language_filter(self):
        results = client().retrieve("tünel", top_k=10, filters={"language": "tr"})
        self.assertTrue(results)
        for result in results:
            self.assertEqual(result.language, "tr")

    def test_cross_lingual_not_auto_filtered(self):
        """A Turkish query must still be able to return English sources."""
        results = client().retrieve("tünel havalandırma sistemi tasarımı", top_k=50)
        self.assertTrue(any(r.language == "en" for r in results),
                        "auto language filtering would have removed all English results")

    def test_recovery_chunks_retrievable_with_provenance(self):
        results = client().retrieve("annual tunnel operating costs", top_k=10)
        recovery = [r for r in results if r.source_kind == "recovery_chunk"]
        self.assertTrue(recovery)
        for result in recovery:
            self.assertTrue(result.recovery_method)

    def test_low_content_flag_preserved(self):
        results = client().retrieve("Türkiye tünel haritası", top_k=20)
        self.assertTrue(all(isinstance(r.is_low_content, bool) for r in results))

    def test_top_k_respected(self):
        self.assertEqual(len(client().retrieve("tunnel", top_k=3)), 3)


if __name__ == "__main__":
    unittest.main()
