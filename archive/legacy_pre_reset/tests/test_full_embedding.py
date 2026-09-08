from __future__ import annotations

import csv
import importlib.util
import json
import os
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Model download / inference is opt-in so the default suite stays offline.
LIVE = os.environ.get("TUNNELBOOK_BGE_LIVE") == "1"


def load_module():
    spec = importlib.util.spec_from_file_location("full_embedding", ROOT / "scripts/14_full_embedding.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


embedder = load_module()

FROZEN_BASELINE = {
    "data/chunks/chunks.jsonl": "e751fcfc3cc6828b05f75f494fd9a31b44388abda9daf83fb9581581ef79df5b",
    "data/chunks_pilot/chunks.jsonl": "3f79b5c2897e5cae04d9ee0e3fa2b4f06a9a94ad4016ec637676d39ad5b55aaa",
    "data/chunks_recovery/chunks.jsonl": "835fc871ee53253d4d95eca14c7c13d908f7d06e559cf657f71c954196fd07f7",
    "data/metadata/full_embedding_input_manifest.csv":
        "4af9d60a8cbfbb712c27c8129a622b6118166954c732947e015876e25fd99654",
    "data/metadata/embedding_eligibility.csv":
        "edd590a0ee2b85b083ba8f799c55bdced3df7044e3d8557593ba5bc3dcfe3a63",
    "data/metadata/bge_m3_tokenizer_audit.csv":
        "e2f954becd99223602108be6b9085c563d519f787c753e378037241f393aee14",
}

_CACHE: dict[str, object] = {}


def inputs():
    if "items" not in _CACHE:
        items, problems = embedder.resolve_inputs(ROOT)
        _CACHE["items"], _CACHE["problems"] = items, problems
    return _CACHE["items"], _CACHE["problems"]


def vectors():
    import numpy
    path = ROOT / "data/embeddings/bge_m3_dense.npy"
    if not path.is_file():
        return None
    if "vectors" not in _CACHE:
        _CACHE["vectors"] = numpy.load(path)
    return _CACHE["vectors"]


def manifest():
    path = ROOT / "data/metadata/full_embedding_manifest.csv"
    if not path.is_file():
        return None
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class TestAuthoritativeInput(unittest.TestCase):
    def test_input_resolves_without_problems(self):
        items, problems = inputs()
        self.assertEqual(problems, [])
        self.assertEqual(len(items), embedder.EXPECTED_VECTORS)

    def test_vector_indices_unique_and_contiguous(self):
        items, _ = inputs()
        indices = [item["vector_index"] for item in items]
        self.assertEqual(len(set(indices)), len(indices))
        self.assertEqual(sorted(indices), list(range(len(items))))

    def test_chunk_ids_unique(self):
        items, _ = inputs()
        self.assertEqual(len({item["chunk_id"] for item in items}), len(items))

    def test_source_kind_composition(self):
        items, _ = inputs()
        kinds = Counter(item["source_kind"] for item in items)
        self.assertEqual(kinds["canonical_chunk"], embedder.EXPECTED_CANONICAL)
        self.assertEqual(kinds["recovery_chunk"], embedder.EXPECTED_RECOVERY)

    def test_document_coverage(self):
        items, _ = inputs()
        self.assertEqual(len({item["document_id"] for item in items}), embedder.EXPECTED_DOCUMENTS)

    def test_text_resolver_matches_manifest_hashes(self):
        items, _ = inputs()
        for item in items:
            self.assertEqual(embedder.sha256(str(item["text"]).encode("utf-8")), item["text_sha256"])

    def test_superseded_chunks_absent(self):
        items, _ = inputs()
        with (ROOT / "data/metadata/embedding_eligibility.csv").open(encoding="utf-8-sig", newline="") as handle:
            eligibility = list(csv.DictReader(handle))
        excluded = {row["chunk_id"] for row in eligibility
                    if row["eligibility_status"] in {"replacement_available", "quarantined_extraction_failure"}}
        self.assertEqual(excluded & {item["chunk_id"] for item in items}, set())

    def test_no_document_has_both_canonical_and_recovery(self):
        items, _ = inputs()
        canonical = {item["document_id"] for item in items if item["source_kind"] == "canonical_chunk"}
        recovery = {item["document_id"] for item in items if item["source_kind"] == "recovery_chunk"}
        self.assertEqual(canonical & recovery, set())

    def test_low_content_chunks_are_retained(self):
        """142 canonical low-content chunks, plus DOC000009-R1-C0003 (a blank recovered page)."""
        items, _ = inputs()
        low = [item for item in items if item["eligibility_status"] == "eligible_low_content"]
        kinds = Counter(item["source_kind"] for item in low)
        self.assertEqual(kinds["canonical_chunk"], 142)
        self.assertEqual(kinds["recovery_chunk"], 1)
        self.assertEqual(len(low), 143)


class TestBatching(unittest.TestCase):
    def items_with_tokens(self):
        return [{"vector_index": index, "chunk_id": f"C{index:04d}", "token_count": count}
                for index, count in enumerate([10, 5000, 20, 4000, 30, 100, 8000, 15, 60, 2000])]

    def test_batches_cover_every_item_exactly_once(self):
        items = self.items_with_tokens()
        batches = embedder.build_batches(items)
        flat = [item["chunk_id"] for batch in batches for item in batch]
        self.assertEqual(sorted(flat), sorted(item["chunk_id"] for item in items))
        self.assertEqual(len(flat), len(set(flat)))

    def test_batches_respect_token_budget(self):
        batches = embedder.build_batches(self.items_with_tokens())
        for batch in batches:
            longest = max(item["token_count"] for item in batch)
            self.assertTrue(len(batch) == 1 or len(batch) * longest <= embedder.TOKEN_BUDGET)
            self.assertLessEqual(len(batch), embedder.MAX_BATCH)

    def test_batching_groups_similar_lengths(self):
        batches = embedder.build_batches(self.items_with_tokens())
        for batch in batches:
            counts = [item["token_count"] for item in batch]
            if len(counts) > 1:
                self.assertLessEqual(max(counts) - min(counts), max(counts))

    def test_batching_is_deterministic(self):
        items = self.items_with_tokens()
        first = [[item["chunk_id"] for item in batch] for batch in embedder.build_batches(items)]
        second = [[item["chunk_id"] for item in batch] for batch in embedder.build_batches(items)]
        self.assertEqual(first, second)

    def test_vector_order_restored_after_bucketing(self):
        """Bucketing reorders work, but every vector_index must map back to its own chunk."""
        items = self.items_with_tokens()
        slots = [None] * len(items)
        for batch in embedder.build_batches(items):
            for item in batch:
                slots[item["vector_index"]] = item["chunk_id"]
        self.assertEqual(slots, [item["chunk_id"] for item in items])


class TestCheckpointing(unittest.TestCase):
    def cache(self):
        cache = ROOT / "data/embeddings/cache"
        if not cache.is_dir():
            self.skipTest("checkpoint cache not present")
        return cache

    def test_checkpoints_created_for_every_batch(self):
        cache = self.cache()
        metas = sorted(cache.glob("batch_*.json"))
        arrays = sorted(cache.glob("batch_*.npy"))
        self.assertGreater(len(metas), 0)
        self.assertEqual(len(metas), len(arrays))

    def test_checkpoint_records_required_identity_fields(self):
        cache = self.cache()
        meta = json.loads(sorted(cache.glob("batch_*.json"))[0].read_text(encoding="utf-8"))
        for field in ("start_index", "end_index", "chunk_ids", "input_hashes", "model_revision",
                      "vector_shape", "run_identity", "batch_identity"):
            self.assertIn(field, meta)

    def test_checkpoint_model_revision_is_pinned(self):
        cache = self.cache()
        for path in sorted(cache.glob("batch_*.json"))[:20]:
            meta = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(meta["model_revision"], embedder.MODEL_REVISION)

    def test_checkpoint_covers_all_vectors_exactly_once(self):
        cache = self.cache()
        ids = [chunk_id for path in sorted(cache.glob("batch_*.json"))
               for chunk_id in json.loads(path.read_text(encoding="utf-8"))["chunk_ids"]]
        self.assertEqual(len(ids), embedder.EXPECTED_VECTORS)
        self.assertEqual(len(set(ids)), embedder.EXPECTED_VECTORS)

    def test_stale_checkpoint_rejected_on_model_revision(self):
        import numpy
        import tempfile
        batch = [{"chunk_id": "C1", "text_sha256": "a" * 64, "vector_index": 0}]
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            vectors = numpy.zeros((1, embedder.EXPECTED_DIMENSION), dtype=numpy.float32)
            embedder.save_checkpoint(cache, 0, "identity-1", batch, vectors)
            self.assertIsNotNone(embedder.load_checkpoint(cache, 0, "identity-1", batch))
            meta_path = cache / "batch_00000.json"
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            meta["model_revision"] = "stale"
            meta_path.write_text(json.dumps(meta), encoding="utf-8")
            self.assertIsNone(embedder.load_checkpoint(cache, 0, "identity-1", batch))

    def test_stale_checkpoint_rejected_on_run_identity(self):
        import numpy
        import tempfile
        batch = [{"chunk_id": "C1", "text_sha256": "a" * 64, "vector_index": 0}]
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            embedder.save_checkpoint(cache, 0, "identity-1", batch,
                                     numpy.zeros((1, embedder.EXPECTED_DIMENSION), dtype=numpy.float32))
            self.assertIsNone(embedder.load_checkpoint(cache, 0, "identity-2", batch))

    def test_stale_checkpoint_rejected_on_changed_text(self):
        import numpy
        import tempfile
        batch = [{"chunk_id": "C1", "text_sha256": "a" * 64, "vector_index": 0}]
        changed = [{"chunk_id": "C1", "text_sha256": "b" * 64, "vector_index": 0}]
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            embedder.save_checkpoint(cache, 0, "identity-1", batch,
                                     numpy.zeros((1, embedder.EXPECTED_DIMENSION), dtype=numpy.float32))
            self.assertIsNone(embedder.load_checkpoint(cache, 0, "identity-1", changed))

    def test_checkpoint_rejected_on_wrong_shape(self):
        import numpy
        import tempfile
        batch = [{"chunk_id": "C1", "text_sha256": "a" * 64, "vector_index": 0},
                 {"chunk_id": "C2", "text_sha256": "b" * 64, "vector_index": 1}]
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            embedder.save_checkpoint(cache, 0, "identity-1", batch,
                                     numpy.zeros((1, embedder.EXPECTED_DIMENSION), dtype=numpy.float32))
            self.assertIsNone(embedder.load_checkpoint(cache, 0, "identity-1", batch))


class TestEmbeddingOutput(unittest.TestCase):
    def test_vectors_exist_with_expected_shape(self):
        array = vectors()
        if array is None:
            self.skipTest("embeddings not generated yet")
        self.assertEqual(array.shape, (embedder.EXPECTED_VECTORS, embedder.EXPECTED_DIMENSION))

    def test_dimension_is_1024(self):
        array = vectors()
        if array is None:
            self.skipTest("embeddings not generated yet")
        self.assertEqual(array.shape[1], 1024)

    def test_all_vectors_finite(self):
        import numpy
        array = vectors()
        if array is None:
            self.skipTest("embeddings not generated yet")
        self.assertTrue(bool(numpy.isfinite(array).all()))

    def test_no_nan_or_inf(self):
        import numpy
        array = vectors()
        if array is None:
            self.skipTest("embeddings not generated yet")
        self.assertEqual(int(numpy.isnan(array).sum()), 0)
        self.assertEqual(int(numpy.isinf(array).sum()), 0)

    def test_no_zero_vectors(self):
        import numpy
        array = vectors()
        if array is None:
            self.skipTest("embeddings not generated yet")
        self.assertEqual(int((numpy.linalg.norm(array, axis=1) == 0).sum()), 0)

    def test_vectors_are_unit_normalized(self):
        import numpy
        array = vectors()
        if array is None:
            self.skipTest("embeddings not generated yet")
        norms = numpy.linalg.norm(array, axis=1)
        self.assertTrue(bool(numpy.allclose(norms, 1.0, atol=1e-3)))

    def test_chunk_ids_sidecar_matches_vectors(self):
        array = vectors()
        path = ROOT / "data/embeddings/bge_m3_chunk_ids.json"
        if array is None or not path.is_file():
            self.skipTest("embeddings not generated yet")
        ids = json.loads(path.read_text(encoding="utf-8"))
        items, _ = inputs()
        self.assertEqual(len(ids), len(array))
        self.assertEqual(ids, [item["chunk_id"] for item in items])


class TestMappingIntegrity(unittest.TestCase):
    def test_manifest_matches_inputs_exactly(self):
        rows = manifest()
        if rows is None:
            self.skipTest("embedding manifest not generated yet")
        items, _ = inputs()
        self.assertEqual(len(rows), len(items))
        for row, item in zip(rows, items):
            self.assertEqual(int(row["vector_index"]), item["vector_index"])
            self.assertEqual(row["chunk_id"], item["chunk_id"])
            self.assertEqual(row["document_id"], item["document_id"])
            self.assertEqual(row["text_sha256"], item["text_sha256"])
            self.assertEqual(row["source_kind"], item["source_kind"])

    def test_manifest_has_required_fields(self):
        rows = manifest()
        if rows is None:
            self.skipTest("embedding manifest not generated yet")
        required = {"vector_index", "chunk_id", "document_id", "source_kind", "text_sha256",
                    "bge_m3_token_count", "embedding_dimension", "embedding_norm", "finite",
                    "model", "model_revision", "device", "eligibility_status", "provenance_status"}
        self.assertTrue(required.issubset(set(rows[0].keys())))

    def test_manifest_pins_model_revision(self):
        rows = manifest()
        if rows is None:
            self.skipTest("embedding manifest not generated yet")
        self.assertEqual({row["model_revision"] for row in rows}, {embedder.MODEL_REVISION})
        self.assertEqual({row["model"] for row in rows}, {embedder.MODEL_NAME})

    def test_recovery_mappings_verified_explicitly(self):
        rows = manifest()
        if rows is None:
            self.skipTest("embedding manifest not generated yet")
        recovery = [row for row in rows if row["source_kind"] == "recovery_chunk"]
        self.assertEqual(len(recovery), 12)
        items, _ = inputs()
        by_id = {item["chunk_id"]: item for item in items}
        for row in recovery:
            self.assertIn(row["chunk_id"], by_id)
            self.assertEqual(by_id[row["chunk_id"]]["text_sha256"], row["text_sha256"])
            self.assertLessEqual(int(row["bge_m3_token_count"]), embedder.MAX_LENGTH)

    def test_no_duplicate_ids_or_indices_in_manifest(self):
        rows = manifest()
        if rows is None:
            self.skipTest("embedding manifest not generated yet")
        self.assertEqual(len({row["chunk_id"] for row in rows}), len(rows))
        self.assertEqual(len({row["vector_index"] for row in rows}), len(rows))


class TestTokenSafety(unittest.TestCase):
    def test_manifest_token_counts_within_limit(self):
        rows = manifest()
        if rows is None:
            self.skipTest("embedding manifest not generated yet")
        over = [row["chunk_id"] for row in rows if int(row["bge_m3_token_count"]) > embedder.MAX_LENGTH]
        self.assertEqual(over, [])

    def test_canonical_counts_agree_with_preflight_audit(self):
        rows = manifest()
        if rows is None:
            self.skipTest("embedding manifest not generated yet")
        with (ROOT / "data/metadata/bge_m3_tokenizer_audit.csv").open(encoding="utf-8-sig", newline="") as handle:
            audit = {row["chunk_id"]: row["bge_m3_token_count"] for row in csv.DictReader(handle)}
        for row in rows:
            if row["source_kind"] == "canonical_chunk":
                self.assertEqual(row["bge_m3_token_count"], audit[row["chunk_id"]])

    def test_recovery_chunks_within_limit(self):
        recovery = [json.loads(line) for line in
                    (ROOT / "data/chunks_recovery/chunks.jsonl").read_text(encoding="utf-8").splitlines()
                    if line.strip()]
        self.assertEqual(len(recovery), 12)
        rows = manifest()
        if rows is None:
            self.skipTest("embedding manifest not generated yet")
        counts = {row["chunk_id"]: int(row["bge_m3_token_count"]) for row in rows}
        for chunk in recovery:
            self.assertLessEqual(counts[chunk["chunk_id"]], embedder.MAX_LENGTH)


class TestFrozenIntegrity(unittest.TestCase):
    def test_frozen_inputs_unchanged(self):
        for relative, expected in FROZEN_BASELINE.items():
            self.assertEqual(embedder.sha256((ROOT / relative).read_bytes()), expected,
                             f"frozen input modified: {relative}")

    def test_frozen_state_is_stable(self):
        self.assertEqual(embedder.frozen_state(ROOT), embedder.frozen_state(ROOT))

    def test_frozen_declarations_cover_required_paths(self):
        for relative in ("data/chunks/chunks.jsonl", "data/chunks_recovery/chunks.jsonl",
                         "data/metadata/full_embedding_input_manifest.csv"):
            self.assertIn(relative, embedder.FROZEN_INPUTS)
        for relative in ("data/corpus_final", "data/corpus_normalized", "data/corpus_recovery"):
            self.assertIn(relative, embedder.FROZEN_TREES)


@unittest.skipUnless(LIVE, "set TUNNELBOOK_BGE_LIVE=1 to run model-inference tests")
class TestLiveReproducibility(unittest.TestCase):
    def test_deterministic_sample_reembed_matches_stored_vectors(self):
        import numpy
        import torch
        from transformers import AutoModel, AutoTokenizer
        array = vectors()
        if array is None:
            self.skipTest("embeddings not generated yet")
        items, _ = inputs()
        tokenizer = AutoTokenizer.from_pretrained(embedder.MODEL_NAME, revision=embedder.MODEL_REVISION)
        model = AutoModel.from_pretrained(embedder.MODEL_NAME, revision=embedder.MODEL_REVISION)
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        model = model.to(device).eval()
        indices = list(range(0, len(items), len(items) // 12))[:12]
        repeat = embedder.embed_texts([str(items[i]["text"]) for i in indices], tokenizer, model, device)
        drift = numpy.abs(repeat - array[indices]).max()
        self.assertLess(float(drift), 1e-3)


if __name__ == "__main__":
    unittest.main()
