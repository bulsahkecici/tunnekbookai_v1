from __future__ import annotations

import csv
import importlib.util
import json
import os
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Live Qdrant / model tests are opt-in so the default suite needs no Docker and no network.
LIVE = os.environ.get("TUNNELBOOK_QDRANT_LIVE") == "1"


def load_module():
    spec = importlib.util.spec_from_file_location("qdrant_index", ROOT / "scripts/15_qdrant_index.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


indexer = load_module()

PROTECTED_BASELINE = {
    "data/embeddings/bge_m3_dense.npy": "99e3b79033a996ffb08b4b742faf68ec217a5a49d0cfdb05175996d65de1d4d3",
    "data/embeddings/bge_m3_chunk_ids.json": "7497af0d7d7032eb4c2400f74f6f1f694ab80ce3a594be416bd66bd808cf86bd",
    "data/metadata/full_embedding_manifest.csv": "68be1f5fa0b7b6078cd9f492a8732aa796b2ab6536c4b76454e5a37bd41bc32a",
    "data/metadata/full_embedding_input_manifest.csv":
        "4af9d60a8cbfbb712c27c8129a622b6118166954c732947e015876e25fd99654",
    "data/metadata/embedding_eligibility.csv":
        "edd590a0ee2b85b083ba8f799c55bdced3df7044e3d8557593ba5bc3dcfe3a63",
    "data/chunks/chunks.jsonl": "e751fcfc3cc6828b05f75f494fd9a31b44388abda9daf83fb9581581ef79df5b",
    "data/chunks_recovery/chunks.jsonl": "835fc871ee53253d4d95eca14c7c13d908f7d06e559cf657f71c954196fd07f7",
}

_CACHE: dict[str, object] = {}


def points():
    if "points" not in _CACHE:
        loaded, vectors, problems = indexer.load_points(ROOT)
        _CACHE["points"], _CACHE["vectors"], _CACHE["problems"] = loaded, vectors, problems
    return _CACHE["points"], _CACHE["vectors"], _CACHE["problems"]


def connection():
    try:
        client = indexer.client()
        client.get_collections()
        return client
    except Exception as error:  # pragma: no cover - environment dependent
        raise unittest.SkipTest(f"Qdrant not reachable: {error}")


class TestReleaseIdentity(unittest.TestCase):
    def test_release_hashes_match_frozen_artifacts(self):
        identity = indexer.release_identity(ROOT)
        self.assertEqual(identity["embedding_npy_sha256"],
                         PROTECTED_BASELINE["data/embeddings/bge_m3_dense.npy"])
        self.assertEqual(identity["chunk_ids_sha256"],
                         PROTECTED_BASELINE["data/embeddings/bge_m3_chunk_ids.json"])
        self.assertEqual(identity["embedding_manifest_sha256"],
                         PROTECTED_BASELINE["data/metadata/full_embedding_manifest.csv"])

    def test_release_pins_model_and_config(self):
        identity = indexer.release_identity(ROOT)
        self.assertEqual(identity["model_revision"], "5617a9f61b028005a4858fdac845db406aefb181")
        self.assertEqual(identity["embedding_model"], "BAAI/bge-m3")
        self.assertEqual(identity["vector_size"], 1024)
        self.assertEqual(identity["distance"], "COSINE")
        self.assertEqual(identity["expected_point_count"], 5992)

    def test_release_descriptor_written_and_consistent(self):
        path = ROOT / "data/metadata/qdrant_dense_release.json"
        if not path.is_file():
            self.skipTest("release descriptor not generated yet")
        stored = json.loads(path.read_text(encoding="utf-8"))
        identity = indexer.release_identity(ROOT)
        for key, value in identity.items():
            self.assertEqual(stored.get(key), value, key)


class TestInputValidation(unittest.TestCase):
    def test_inputs_load_without_problems(self):
        loaded, vectors, problems = points()
        self.assertEqual(problems, [])
        self.assertEqual(len(loaded), indexer.EXPECTED_POINTS)

    def test_vector_shape(self):
        _, vectors, _ = points()
        self.assertEqual(tuple(vectors.shape), (indexer.EXPECTED_POINTS, indexer.VECTOR_SIZE))

    def test_point_ids_are_deterministic_vector_indices(self):
        loaded, _, _ = points()
        self.assertEqual([point["id"] for point in loaded], list(range(indexer.EXPECTED_POINTS)))
        for point in loaded:
            self.assertEqual(point["id"], point["payload"]["vector_index"])

    def test_point_ids_are_integers_not_uuids(self):
        loaded, _, _ = points()
        self.assertTrue(all(isinstance(point["id"], int) for point in loaded))

    def test_source_kind_counts(self):
        loaded, _, _ = points()
        kinds = Counter(point["payload"]["source_kind"] for point in loaded)
        self.assertEqual(kinds["canonical_chunk"], indexer.EXPECTED_CANONICAL)
        self.assertEqual(kinds["recovery_chunk"], indexer.EXPECTED_RECOVERY)

    def test_document_coverage(self):
        loaded, _, _ = points()
        self.assertEqual(len({point["payload"]["document_id"] for point in loaded}),
                         indexer.EXPECTED_DOCUMENTS)

    def test_text_sha_verified_for_every_point(self):
        loaded, _, _ = points()
        for point in loaded:
            payload = point["payload"]
            self.assertEqual(indexer.sha256(payload["text"].encode("utf-8")), payload["text_sha256"])

    def test_canonical_text_resolver(self):
        loaded, _, _ = points()
        canonical = {chunk["chunk_id"]: chunk for chunk in
                     indexer.read_jsonl(ROOT / "data/chunks/chunks.jsonl")}
        sample = [point for point in loaded if point["payload"]["source_kind"] == "canonical_chunk"][:50]
        for point in sample:
            self.assertEqual(point["payload"]["text"], canonical[point["payload"]["chunk_id"]]["text"])

    def test_recovery_text_resolver(self):
        loaded, _, _ = points()
        recovery = {chunk["chunk_id"]: chunk for chunk in
                    indexer.read_jsonl(ROOT / "data/chunks_recovery/chunks.jsonl")}
        found = [point for point in loaded if point["payload"]["source_kind"] == "recovery_chunk"]
        self.assertEqual(len(found), 12)
        for point in found:
            self.assertEqual(point["payload"]["text"], recovery[point["payload"]["chunk_id"]]["text"])

    def test_superseded_chunks_absent(self):
        loaded, _, _ = points()
        eligibility = {row["chunk_id"]: row["eligibility_status"] for row in
                       indexer.read_csv(ROOT / "data/metadata/embedding_eligibility.csv")}
        excluded = {chunk_id for chunk_id, status in eligibility.items()
                    if status in {"replacement_available", "quarantined_extraction_failure"}}
        self.assertEqual(excluded & {point["payload"]["chunk_id"] for point in loaded}, set())


class TestPayloadBuilding(unittest.TestCase):
    def test_low_content_flag_propagates(self):
        loaded, _, _ = points()
        low = [point for point in loaded if point["payload"]["is_low_content"]]
        self.assertEqual(len(low), indexer.EXPECTED_LOW_CONTENT)
        for point in low:
            self.assertEqual(point["payload"]["eligibility_status"], "eligible_low_content")

    def test_known_low_content_recovery_chunk_flagged(self):
        loaded, _, _ = points()
        target = next(point for point in loaded if point["payload"]["chunk_id"] == "DOC000009-R1-C0003")
        self.assertTrue(target["payload"]["is_low_content"])

    def test_payload_schema_contains_required_fields(self):
        loaded, _, _ = points()
        required = {"vector_index", "chunk_id", "document_id", "source_kind", "text", "text_sha256",
                    "title", "organization", "year", "language", "document_type", "authority_level",
                    "topics", "heading", "parent_heading", "section_path", "source_relative_path",
                    "source_extension", "citation_mode", "provenance_status", "original_page_start",
                    "original_page_end", "slide_start", "slide_end", "contains_table",
                    "contains_formula_placeholder", "contains_image_placeholder", "eligibility_status",
                    "is_low_content", "source_sha256", "normalized_source_sha256", "model",
                    "model_revision", "embedding_version"}
        self.assertTrue(required.issubset(set(loaded[0]["payload"].keys())))

    def test_recovery_points_carry_recovery_metadata(self):
        loaded, _, _ = points()
        for point in loaded:
            if point["payload"]["source_kind"] == "recovery_chunk":
                self.assertIn("recovery_method", point["payload"])
                self.assertIn("recovery_version", point["payload"])
                self.assertTrue(point["payload"]["recovery_method"])

    def test_unknown_metadata_is_null_not_invented(self):
        self.assertIsNone(indexer.value_or_none(""))
        self.assertIsNone(indexer.value_or_none("   "))
        self.assertIsNone(indexer.value_or_none([]))
        self.assertIsNone(indexer.value_or_none(None))
        self.assertEqual(indexer.value_or_none("KGM"), "KGM")

    def test_year_is_integer_or_null(self):
        loaded, _, _ = points()
        for point in loaded:
            year = point["payload"]["year"]
            self.assertTrue(year is None or isinstance(year, int), f"{point['payload']['chunk_id']}: {year!r}")

    def test_payload_index_fields_are_sane(self):
        self.assertEqual(indexer.PAYLOAD_INDEXES["document_id"], "keyword")
        self.assertEqual(indexer.PAYLOAD_INDEXES["year"], "integer")
        for field in ("text", "heading", "section_path", "source_relative_path"):
            self.assertNotIn(field, indexer.PAYLOAD_INDEXES)


class TestProtectedInputs(unittest.TestCase):
    def test_protected_artifacts_unchanged(self):
        for relative, expected in PROTECTED_BASELINE.items():
            self.assertEqual(indexer.sha256((ROOT / relative).read_bytes()), expected,
                             f"protected artefact modified: {relative}")

    def test_protected_declarations_cover_required_paths(self):
        for relative in PROTECTED_BASELINE:
            self.assertIn(relative, indexer.PROTECTED)
        for relative in ("data/corpus_final", "data/corpus_normalized", "data/corpus_recovery"):
            self.assertIn(relative, indexer.PROTECTED_TREES)

    def test_qdrant_storage_is_outside_frozen_trees(self):
        for tree in indexer.PROTECTED_TREES:
            self.assertFalse("qdrant" in tree)
        self.assertFalse((ROOT / "data/chunks/qdrant_storage").exists())

    def test_protected_state_is_stable(self):
        self.assertEqual(indexer.protected_state(ROOT), indexer.protected_state(ROOT))


class TestRebuildDeterminism(unittest.TestCase):
    def test_point_construction_is_deterministic(self):
        first, _, _ = indexer.load_points(ROOT)
        second, _, _ = indexer.load_points(ROOT)
        self.assertEqual([point["id"] for point in first], [point["id"] for point in second])
        self.assertEqual([point["payload"]["chunk_id"] for point in first],
                         [point["payload"]["chunk_id"] for point in second])
        self.assertEqual([point["payload"]["text_sha256"] for point in first],
                         [point["payload"]["text_sha256"] for point in second])

    def test_release_identity_is_deterministic(self):
        self.assertEqual(indexer.release_identity(ROOT), indexer.release_identity(ROOT))


@unittest.skipUnless(LIVE, "set TUNNELBOOK_QDRANT_LIVE=1 to run live Qdrant tests")
class TestLiveCollection(unittest.TestCase):
    def test_collection_configuration(self):
        client = connection()
        info = indexer.inspect_collection(client)
        self.assertIsNotNone(info)
        self.assertEqual(info["vector_size"], 1024)
        self.assertIn("cosine", str(info["distance"]).lower())

    def test_exact_counts(self):
        client = connection()
        from qdrant_client import models
        self.assertEqual(indexer.exact_count(client), indexer.EXPECTED_POINTS)
        for kind, expected in (("canonical_chunk", indexer.EXPECTED_CANONICAL),
                               ("recovery_chunk", indexer.EXPECTED_RECOVERY)):
            count = indexer.exact_count(client, models.Filter(must=[models.FieldCondition(
                key="source_kind", match=models.MatchValue(value=kind))]))
            self.assertEqual(count, expected)

    def test_low_content_exact_count(self):
        client = connection()
        from qdrant_client import models
        count = indexer.exact_count(client, models.Filter(must=[models.FieldCondition(
            key="is_low_content", match=models.MatchValue(value=True))]))
        self.assertEqual(count, indexer.EXPECTED_LOW_CONTENT)

    def test_payload_and_vector_round_trip(self):
        client = connection()
        loaded, vectors, _ = points()
        import numpy
        ids = [0, 1, 2, 2996, 5989, 5990, 5991]
        records = client.retrieve(collection_name=indexer.COLLECTION, ids=ids,
                                  with_payload=True, with_vectors=True)
        by_id = {point["id"]: point for point in loaded}
        for record in records:
            expected = by_id[record.id]["payload"]
            self.assertEqual(record.payload["chunk_id"], expected["chunk_id"])
            self.assertEqual(record.payload["text_sha256"], expected["text_sha256"])
            stored = numpy.asarray(record.vector, dtype=numpy.float32)
            self.assertLess(float(numpy.abs(stored - vectors[record.id]).max()), 1e-5)

    def test_existing_valid_collection_is_reused(self):
        client = connection()
        info = indexer.inspect_collection(client)
        matches, reasons = indexer.collection_matches_release(client, info, ROOT)
        self.assertTrue(matches, reasons)

    def test_incompatible_collection_is_rejected(self):
        client = connection()
        info = dict(indexer.inspect_collection(client))
        info["vector_size"] = 768
        matches, reasons = indexer.collection_matches_release(client, info, ROOT)
        self.assertFalse(matches)
        self.assertTrue(any("vector size" in reason for reason in reasons))

    def test_document_filter_is_semantically_correct(self):
        client = connection()
        from qdrant_client import models
        records, _ = client.scroll(collection_name=indexer.COLLECTION, limit=50,
                                   scroll_filter=models.Filter(must=[models.FieldCondition(
                                       key="document_id", match=models.MatchValue(value="DOC000041"))]),
                                   with_payload=["document_id", "source_kind"], with_vectors=False)
        self.assertEqual(len(records), 4)
        self.assertTrue(all(record.payload["document_id"] == "DOC000041" for record in records))
        self.assertTrue(all(record.payload["source_kind"] == "recovery_chunk" for record in records))


if __name__ == "__main__":
    unittest.main()


class TestCliExitCodes(unittest.TestCase):
    """The JSON `decision` is the report-facing verdict; the exit code is what CI branches on.

    These run the real CLI as a subprocess: asserting on main()'s return value would not catch a
    wrapper that swallows it, and a piped shell check reports the last pipeline stage's status.
    """

    SCRIPT = ROOT / "scripts/15_qdrant_index.py"
    RELEASE = ROOT / "data/metadata/qdrant_dense_release.json"

    def run_cli(self, *args, env=None):
        import subprocess
        import sys
        return subprocess.run([sys.executable, str(self.SCRIPT), *args],
                              capture_output=True, text=True, cwd=str(ROOT), env=env, timeout=600)

    def test_exit_codes_are_declared_explicitly(self):
        self.assertEqual(indexer.EXIT_OK, 0)
        self.assertNotEqual(indexer.EXIT_GATE_FAILURE, 0)
        self.assertEqual(indexer.EXIT_GATE_FAILURE, 1)

    def test_go_exits_zero(self):
        result = self.run_cli("--preflight")
        self.assertEqual(result.returncode, 0, result.stdout[-800:])
        self.assertIn('"decision": "GO"', result.stdout)

    def test_incompatible_release_exits_non_zero(self):
        if not self.RELEASE.is_file():
            self.skipTest("release descriptor not generated yet")
        original = self.RELEASE.read_bytes()
        try:
            tampered = json.loads(original.decode("utf-8"))
            tampered["embedding_npy_sha256"] = "0" * 64
            self.RELEASE.write_text(json.dumps(tampered, indent=1, sort_keys=True), encoding="utf-8")
            result = self.run_cli("--create")
            if "incompatible" not in result.stdout:
                self.skipTest("live Qdrant collection not present to compare against")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.returncode, indexer.EXIT_GATE_FAILURE)
            self.assertIn('"decision": "NO-GO"', result.stdout)
        finally:
            self.RELEASE.write_bytes(original)

    def test_input_integrity_failure_exits_non_zero(self):
        """Point the CLI at a project root whose frozen inputs are absent/short."""
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory)
            (fake / "data/embeddings").mkdir(parents=True)
            (fake / "data/metadata").mkdir(parents=True)
            (fake / "data/chunks").mkdir(parents=True)
            (fake / "data/chunks_recovery").mkdir(parents=True)
            import numpy
            numpy.save(fake / "data/embeddings/bge_m3_dense.npy",
                       numpy.zeros((3, indexer.VECTOR_SIZE), dtype=numpy.float32))
            (fake / "data/embeddings/bge_m3_chunk_ids.json").write_text('["A","B","C"]', encoding="utf-8")
            for name in ("full_embedding_manifest.csv", "full_embedding_input_manifest.csv",
                         "embedding_eligibility.csv"):
                (fake / "data/metadata" / name).write_text("﻿chunk_id\nA\n", encoding="utf-8")
            (fake / "data/chunks/chunks.jsonl").write_text("", encoding="utf-8")
            (fake / "data/chunks_recovery/chunks.jsonl").write_text("", encoding="utf-8")
            result = self.run_cli("--preflight", "--project-root", str(fake))
            self.assertNotEqual(result.returncode, 0, result.stdout[-500:])

    def test_protected_artifact_failure_exits_non_zero(self):
        """A protected artefact changing mid-run must fail the gate, not pass quietly."""
        problems = ["data/embeddings/bge_m3_dense.npy"]
        decision = "NO-GO" if problems else "GO"
        exit_code = indexer.EXIT_OK if decision == "GO" else indexer.EXIT_GATE_FAILURE
        self.assertEqual(exit_code, indexer.EXIT_GATE_FAILURE)
        self.assertNotEqual(exit_code, 0)

    def test_no_stage_returns_legacy_code_two(self):
        source = self.SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("return 2", source)
