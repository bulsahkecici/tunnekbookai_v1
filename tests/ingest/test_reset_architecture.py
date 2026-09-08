"""Tests for the post-reset authority boundaries and empty bootstrap state."""

from __future__ import annotations

import unittest
from pathlib import Path

from shared.project_quality_gate import evaluate
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.model_capability import UNAVAILABLE, probe


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

    def test_exact_local_models_are_centralized(self):
        models = load_config().models
        self.assertEqual(models["embedding"]["model"], "text-embedding-baai-bge-m3-568m")
        self.assertEqual(models["llm"]["model"], "qwen/qwen3.8-27b")
        self.assertEqual(models["embedding"]["default_endpoint"], "http://127.0.0.1:1234/v1")
        self.assertEqual(models["llm"]["default_endpoint"], "http://127.0.0.1:1234/v1")

    def test_unavailable_local_service_is_explicit_not_a_fallback(self):
        result = probe(load_config())
        self.assertIn(result["decision"], {"AVAILABLE", UNAVAILABLE})
        if result["decision"] == UNAVAILABLE:
            self.assertEqual(result["embedding"]["status"], UNAVAILABLE)
            self.assertEqual(result["llm"]["status"], UNAVAILABLE)
