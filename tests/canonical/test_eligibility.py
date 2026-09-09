from __future__ import annotations

import json
import unittest

from tunnelbookai.canonical.eligibility import inspect_candidate
from tunnelbookai.canonical.paths import CanonicalContext

from .fixtures import SyntheticRepo, write_json


class EligibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = SyntheticRepo()
        self.context = CanonicalContext.load(self.repo.root)
        self.staging = self.repo.root / f"corpus/staging/v2/{self.repo.document_id}"
        self.processing = self.repo.root / f"processing/{self.repo.document_id}"

    def tearDown(self) -> None:
        self.repo.close()

    def action_after(self, mutation) -> tuple[str, tuple[str, ...]]:
        mutation()
        result = inspect_candidate(self.context, self.staging)
        return result.action.value, result.validations

    def test_valid_candidate(self):
        result = inspect_candidate(self.context, self.staging)
        self.assertEqual(result.action.value, "PROMOTE")
        self.assertEqual((result.chunk_count, result.retrieval_ready_chunk_count), (1, 1))

    def test_original_filename_may_differ_from_content_addressed_archive_name(self):
        original = self.repo.root / "originals" / self.repo.document_id / "original.json"
        value = json.loads(original.read_text())
        value["original_filename"] = "operator supplied report.pdf"
        write_json(original, value)
        result = inspect_candidate(self.context, self.staging)
        self.assertEqual(result.action.value, "PROMOTE")

    def test_missing_original_rejected(self):
        action, codes = self.action_after(lambda: (self.repo.root / f"originals/{self.repo.document_id}/source.pdf").unlink())
        self.assertEqual(action, "REJECTED")
        self.assertIn("ORIGINAL_SOURCE_MISSING", codes)

    def test_quality_not_go_rejected(self):
        def mutate():
            for path in (self.processing / "quality_gate.json", self.staging / "quality_gate.json"):
                value = json.loads(path.read_text())
                value["decision"] = "REVIEW"
                value["review_reasons"] = ["TEST"]
                write_json(path, value)
        action, codes = self.action_after(mutate)
        self.assertEqual(action, "REJECTED")
        self.assertIn("QUALITY_NOT_ELIGIBLE", codes)

    def test_invalid_classification_rejected(self):
        def mutate():
            for path in (self.processing / "classification.json", self.staging / "classification.json"):
                value = json.loads(path.read_text())
                value["final_primary_section"] = "999.999"
                write_json(path, value)
        action, codes = self.action_after(mutate)
        self.assertEqual(action, "REJECTED")
        self.assertIn("CLASSIFICATION_INVALID", codes)

    def test_duplicate_chunk_id_rejected(self):
        def mutate():
            path = self.processing / "chunks/chunk_manifest.jsonl"
            path.write_text(path.read_text() + path.read_text(), encoding="utf-8")
        action, codes = self.action_after(mutate)
        self.assertEqual(action, "REJECTED")
        self.assertIn("CHUNK_INTEGRITY_FAILED", codes)

    def test_processing_staging_mismatch_rejected(self):
        action, codes = self.action_after(lambda: (self.staging / "document.md").write_text("changed", encoding="utf-8"))
        self.assertEqual(action, "REJECTED")
        self.assertIn("PROCESSING_IDENTITY_MISMATCH", codes)

    def test_provenance_mismatch_rejected(self):
        def mutate():
            for path in (self.processing / "provenance.json", self.staging / "provenance.json"):
                value = json.loads(path.read_text())
                value["sources"] = []
                write_json(path, value)
        action, codes = self.action_after(mutate)
        self.assertEqual(action, "REJECTED")
        self.assertIn("PROVENANCE_VERIFICATION_FAILED", codes)

    def test_path_escape_rejected(self):
        bundle = self.staging / "bundle.json"
        value = json.loads(bundle.read_text())
        value["processing_bundle"] = "../processing"
        write_json(bundle, value)
        result = inspect_candidate(self.context, self.staging)
        self.assertEqual(result.action.value, "REJECTED")
        self.assertIn("CANONICAL_PATH_ESCAPE", result.validations)

    def test_upstream_ledger_only_duplicate_does_not_reject(self):
        registry = self.repo.root / "audit/source_registry.jsonl"
        own = json.loads(registry.read_text().splitlines()[0])
        own["document_id"] = "ING_" + "1" * 20
        with registry.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(own) + "\n")
        result = inspect_candidate(self.context, self.staging)
        self.assertEqual(result.action.value, "PROMOTE")

    def test_upstream_active_exact_duplicate_rejected(self):
        registry = self.repo.root / "audit/source_registry.jsonl"
        own = json.loads(registry.read_text().splitlines()[0])
        duplicate_id = "ING_" + "1" * 20
        own["document_id"] = duplicate_id
        with registry.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(own) + "\n")
        original = self.repo.root / "originals" / duplicate_id
        processing = self.repo.root / "processing" / duplicate_id
        original.mkdir(parents=True)
        processing.mkdir(parents=True)
        source = next((self.repo.root / "originals" / self.repo.document_id).glob("source.*"))
        duplicate_source = original / "source.pdf"
        duplicate_source.write_bytes(source.read_bytes())
        source_sha = own["sha256"]
        write_json(original / "original.json", {
            "document_id": duplicate_id,
            "original_sha256": source_sha,
            "archive_path": f"originals/{duplicate_id}/source.pdf",
        })
        write_json(processing / "metadata.json", {
            "document_id": duplicate_id,
            "original_sha256": source_sha,
        })
        result = inspect_candidate(self.context, self.staging)
        self.assertEqual(result.action.value, "REJECTED")
        self.assertIn("UPSTREAM_DEDUP_VERIFICATION_FAILED", result.validations)

    def test_chunk_warn_remains_eligible(self):
        for path in (self.processing / "chunk_quality.json", self.staging / "chunk_quality.json"):
            value = json.loads(path.read_text())
            value["status"] = "WARN"
            value["warnings"] = ["SYNTHETIC_WARNING"]
            write_json(path, value)
        result = inspect_candidate(self.context, self.staging)
        self.assertEqual(result.action.value, "PROMOTE")
        self.assertIn("SYNTHETIC_WARNING", result.warnings)


if __name__ == "__main__":
    unittest.main()
