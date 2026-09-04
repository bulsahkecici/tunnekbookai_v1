from __future__ import annotations

import csv
import importlib.util
import json
import os
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Model download / inference is opt-in so the default suite stays offline and fast.
LIVE = os.environ.get("TUNNELBOOK_BGE_LIVE") == "1"


def load_module():
    spec = importlib.util.spec_from_file_location("bge_m3_preflight", ROOT / "scripts/12_bge_m3_preflight.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


preflight = load_module()

FROZEN_BASELINE = {
    "data/chunks/chunks.jsonl": "e751fcfc3cc6828b05f75f494fd9a31b44388abda9daf83fb9581581ef79df5b",
    "data/chunks_pilot/chunks.jsonl": "3f79b5c2897e5cae04d9ee0e3fa2b4f06a9a94ad4016ec637676d39ad5b55aaa",
    "data/metadata/chunk_manifest.csv": "e5aed214a30d21ed5819e5b34e332acf3ffe266752dc1e9f1c552968e01af7a8",
    "data/metadata/chunk_review_queue.csv": "37377745a46c206afdf39fbf0e187439f40db21e03e85f1538689e24ef3e00e3",
}

_CACHE: dict[str, object] = {}


def audit_rows():
    if "rows" not in _CACHE:
        path = ROOT / "data/metadata/bge_m3_tokenizer_audit.csv"
        with path.open(encoding="utf-8-sig", newline="") as handle:
            _CACHE["rows"] = list(csv.DictReader(handle))
    return _CACHE["rows"]


def chunks():
    if "chunks" not in _CACHE:
        _CACHE["chunks"] = preflight.load_chunks(ROOT)
    return _CACHE["chunks"]


class FakeTokenizer:
    """Offline stand-in with the shape the audit code depends on: batch call -> input_ids lists."""

    is_fast = True
    model_max_length = 8192

    def __call__(self, texts, **kwargs):
        return {"input_ids": [[0] * (len(text.split()) + 2) for text in texts]}


class TestProtectedArtifacts(unittest.TestCase):
    def test_frozen_chunk_artifacts_unchanged(self):
        for relative, expected in FROZEN_BASELINE.items():
            self.assertEqual(preflight.sha256((ROOT / relative).read_bytes()), expected,
                             f"frozen artefact modified: {relative}")

    def test_preflight_declares_frozen_and_protected_paths(self):
        self.assertIn("data/chunks/chunks.jsonl", preflight.FROZEN_ARTIFACTS)
        self.assertIn("data/corpus_normalized", preflight.PROTECTED_TREES)
        self.assertIn("data/corpus_final", preflight.PROTECTED_TREES)

    def test_frozen_state_is_stable_across_calls(self):
        self.assertEqual(preflight.frozen_state(ROOT), preflight.frozen_state(ROOT))


class TestTokenizerAudit(unittest.TestCase):
    def test_audit_covers_every_chunk(self):
        self.assertEqual(len(audit_rows()), 6039)
        self.assertEqual(len(audit_rows()), len(chunks()))

    def test_all_chunk_ids_unique(self):
        ids = [row["chunk_id"] for row in audit_rows()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_audit_ids_match_chunk_corpus_in_order(self):
        self.assertEqual([row["chunk_id"] for row in audit_rows()],
                         [chunk["chunk_id"] for chunk in chunks()])

    def test_no_silent_truncation(self):
        self.assertEqual([row["chunk_id"] for row in audit_rows() if int(row["over_model_limit"])], [])

    def test_every_count_is_positive(self):
        self.assertEqual([row["chunk_id"] for row in audit_rows() if int(row["bge_m3_token_count"]) <= 0], [])

    def test_audit_has_required_columns(self):
        required = {"chunk_id", "document_id", "lexical_token_count", "bge_m3_token_count", "difference", "ratio",
                    "over_1200", "over_1500", "over_model_limit", "contains_table",
                    "contains_formula_placeholder", "contains_image_placeholder", "provenance_status"}
        self.assertTrue(required.issubset(set(preflight.AUDIT_FIELDS)))
        self.assertTrue(required.issubset(set(audit_rows()[0].keys())))

    def test_difference_column_is_internally_consistent(self):
        for row in audit_rows()[:500]:
            self.assertEqual(int(row["difference"]),
                             int(row["bge_m3_token_count"]) - int(row["lexical_token_count"]))

    def test_tokenizer_counts_are_deterministic(self):
        sample = chunks()[:200]
        tokenizer = FakeTokenizer()
        self.assertEqual(preflight.tokenize_all(sample, tokenizer), preflight.tokenize_all(sample, tokenizer))

    def test_tokenize_all_returns_one_count_per_chunk(self):
        sample = chunks()[:64]
        self.assertEqual(len(preflight.tokenize_all(sample, FakeTokenizer())), len(sample))


class TestModelLimits(unittest.TestCase):
    def test_effective_max_length_takes_smallest_declared_limit(self):
        identity = {"tokenizer_model_max_length": 8192, "sentence_transformers_max_seq_length": 8192,
                    "config_max_position_embeddings": 8194}
        self.assertEqual(preflight.effective_max_length(identity), 8192)

    def test_effective_max_length_respects_a_tighter_library_limit(self):
        identity = {"tokenizer_model_max_length": 8192, "sentence_transformers_max_seq_length": 512,
                    "config_max_position_embeddings": 8194}
        self.assertEqual(preflight.effective_max_length(identity), 512)

    def test_effective_max_length_subtracts_positional_offset(self):
        identity = {"tokenizer_model_max_length": 100000, "sentence_transformers_max_seq_length": None,
                    "config_max_position_embeddings": 514}
        self.assertEqual(preflight.effective_max_length(identity), 512)

    def test_resolved_limit_is_recorded_as_8192(self):
        report = (ROOT / "reports/bge_m3_tokenizer_preflight.md")
        if not report.is_file():
            self.skipTest("tokenizer report not generated yet")
        self.assertIn("Effective embedding max length: 8192", report.read_text(encoding="utf-8"))


class TestPilotSelection(unittest.TestCase):
    def test_pilot_selection_is_deterministic(self):
        counts = [int(row["bge_m3_token_count"]) for row in audit_rows()]
        first = preflight.pilot_selection(chunks(), counts, 8192)
        second = preflight.pilot_selection(chunks(), counts, 8192)
        self.assertEqual(first, second)

    def test_pilot_selection_size_and_uniqueness(self):
        counts = [int(row["bge_m3_token_count"]) for row in audit_rows()]
        selection = preflight.pilot_selection(chunks(), counts, 8192)
        self.assertEqual(len(selection), preflight.PILOT_TARGET)
        self.assertEqual(len({index for _, index in selection}), len(selection))

    def test_pilot_selection_never_exceeds_model_limit(self):
        counts = [int(row["bge_m3_token_count"]) for row in audit_rows()]
        selection = preflight.pilot_selection(chunks(), counts, 8192)
        self.assertTrue(all(counts[index] <= 8192 for _, index in selection))

    def test_pilot_selection_is_stratified(self):
        counts = [int(row["bge_m3_token_count"]) for row in audit_rows()]
        reasons = {reason for reason, _ in preflight.pilot_selection(chunks(), counts, 8192)}
        for expected in ("short", "median_sized", "p90_sized", "longest_safe", "table", "turkish", "english"):
            self.assertIn(expected, reasons)


class TestPilotArtifacts(unittest.TestCase):
    def manifest(self):
        path = ROOT / "data/metadata/bge_m3_embedding_pilot_manifest.csv"
        if not path.is_file():
            self.skipTest("pilot manifest not generated yet")
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    def vectors(self):
        import numpy
        path = ROOT / "data/embeddings_pilot/bge_m3_dense.npy"
        if not path.is_file():
            self.skipTest("pilot vectors not generated yet")
        return numpy.load(path)

    def test_manifest_integrity(self):
        rows = self.manifest()
        self.assertEqual(len(rows), preflight.PILOT_TARGET)
        self.assertTrue(set(preflight.PILOT_FIELDS).issubset(set(rows[0].keys())))
        self.assertEqual(len({row["chunk_id"] for row in rows}), len(rows))

    def test_vector_dimensions_stable(self):
        vectors = self.vectors()
        self.assertEqual(vectors.shape[1], 1024)
        self.assertEqual(len({row["vector_dimension"] for row in self.manifest()}), 1)

    def test_vectors_are_finite(self):
        import numpy
        self.assertTrue(bool(numpy.isfinite(self.vectors()).all()))

    def test_no_nan_values(self):
        import numpy
        self.assertEqual(int(numpy.isnan(self.vectors()).sum()), 0)

    def test_no_inf_values(self):
        import numpy
        self.assertEqual(int(numpy.isinf(self.vectors()).sum()), 0)

    def test_no_empty_vectors(self):
        import numpy
        norms = numpy.linalg.norm(self.vectors(), axis=1)
        self.assertTrue(bool((norms > 0).all()))

    def test_vectors_are_unit_normalized(self):
        import numpy
        norms = numpy.linalg.norm(self.vectors(), axis=1)
        self.assertTrue(bool(numpy.allclose(norms, 1.0, atol=1e-4)), f"norm range {norms.min()}–{norms.max()}")

    def test_vector_chunk_mapping_is_exact(self):
        rows = self.manifest()
        vectors = self.vectors()
        path = ROOT / "data/embeddings_pilot/bge_m3_chunk_ids.json"
        if not path.is_file():
            self.skipTest("chunk id sidecar not generated yet")
        ids = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(len(ids), len(vectors))
        self.assertEqual(ids, [row["chunk_id"] for row in rows])
        self.assertEqual([int(row["vector_index"]) for row in rows], list(range(len(rows))))

    def test_manifest_chunk_ids_exist_in_corpus(self):
        known = {chunk["chunk_id"] for chunk in chunks()}
        self.assertTrue({row["chunk_id"] for row in self.manifest()}.issubset(known))

    def test_manifest_token_counts_match_audit(self):
        audit = {row["chunk_id"]: row["bge_m3_token_count"] for row in audit_rows()}
        for row in self.manifest():
            self.assertEqual(row["token_count"], audit[row["chunk_id"]])

    def test_manifest_records_model_identity(self):
        for row in self.manifest():
            self.assertEqual(row["model"], "BAAI/bge-m3")
            self.assertTrue(row["model_revision"])
            self.assertIn(row["device"], {"mps", "cpu"})


class TestUnusableDetection(unittest.TestCase):
    def test_glyph_sequences_flagged(self):
        chunk = {"text": "".join(f"/G{index % 90 + 10}" for index in range(40)), "chunk_id": "X", "document_id": "D"}
        self.assertEqual(preflight.unusable_chunks([chunk]), [chunk])

    def test_control_characters_flagged(self):
        chunk = {"text": "\x01\x02\x03" * 20, "chunk_id": "X", "document_id": "D"}
        self.assertEqual(preflight.unusable_chunks([chunk]), [chunk])

    def test_clean_text_not_flagged(self):
        chunk = {"text": "NATM support systems are used in tunnelling.", "chunk_id": "X", "document_id": "D"}
        self.assertEqual(preflight.unusable_chunks([chunk]), [])


@unittest.skipUnless(LIVE, "set TUNNELBOOK_BGE_LIVE=1 to run model-download tests")
class TestLiveModel(unittest.TestCase):
    def test_bge_m3_tokenizer_loads(self):
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(preflight.MODEL_NAME)
        self.assertEqual(tokenizer.model_max_length, 8192)

    def test_model_identity_resolves(self):
        identity = preflight.model_identity()
        self.assertEqual(identity["hidden_size"], 1024)
        self.assertEqual(preflight.effective_max_length(identity), 8192)


if __name__ == "__main__":
    unittest.main()
