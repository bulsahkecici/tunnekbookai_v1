"""Tests for the post-reset authority boundaries and empty bootstrap state."""

from __future__ import annotations

import unittest
from pathlib import Path

from shared.project_quality_gate import evaluate
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.model_capability import UNAVAILABLE, probe
from tunnelbookai.ingest.metadata import vocabularies


ROOT = Path(__file__).resolve().parents[2]


class ResetArchitectureTests(unittest.TestCase):
    def test_empty_corpus_gate_passes(self):
        result = evaluate()
        self.assertEqual(result["decision"], "GO")
        self.assertFalse(result["legacy_crawler_present"])
        self.assertFalse(result["legacy_corpus_present"])
        self.assertFalse(result["legacy_vector_state_present"])

    def test_papercrawler_is_an_input_not_an_internal_component(self):
        self.assertTrue((ROOT / "incoming" / "papercrawler" / "releases").is_dir())
        self.assertFalse((ROOT / "crawler").exists())

    def test_legacy_runtime_is_isolated_from_active_topology(self):
        result = evaluate()
        self.assertTrue(result["checks"]["active_scripts_current"])
        self.assertTrue(result["checks"]["legacy_topology_isolated"])
        self.assertTrue(result["checks"]["legacy_runtime_references_absent"])
        self.assertEqual(result["legacy_active_paths"], [])
        self.assertEqual(result["legacy_runtime_references"], [])

    def test_exact_local_models_are_centralized(self):
        models = load_config().models
        self.assertEqual(models["embedding"]["model"], "text-embedding-baai-bge-m3-568m")
        self.assertEqual(models["llm"]["model"], "qwen/qwen3.8-27b")
        self.assertEqual(models["embedding"]["default_endpoint"], "http://127.0.0.1:1234/v1")
        self.assertEqual(models["llm"]["default_endpoint"], "http://127.0.0.1:1234/v1")
        metadata = load_config().metadata["llm_enrichment"]
        self.assertNotIn("model", metadata)
        self.assertNotIn("base_url", metadata)

    def test_metadata_vocabularies_are_package_owned(self):
        self.assertIn("technical_report", vocabularies.DOCUMENT_TYPES)
        self.assertEqual(vocabularies.infer_language("kısa metin", ""), ("unknown", "low"))

    def test_unavailable_local_service_is_explicit_not_a_fallback(self):
        result = probe(load_config())
        self.assertIn(result["decision"], {"AVAILABLE", UNAVAILABLE})
        if result["decision"] == UNAVAILABLE:
            self.assertEqual(result["embedding"]["status"], UNAVAILABLE)
            self.assertEqual(result["llm"]["status"], UNAVAILABLE)
