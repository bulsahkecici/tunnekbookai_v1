from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tunnelbookai.dashboard.section_review import apply_review
from tunnelbookai.population.models import atomic_json


class SectionReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.run_path = self.root / "audit/corpus_population/runs/CPR_test.json"
        self.spec_path = self.root / "audit/dashboard/review.json"

    def tearDown(self):
        self.temp.cleanup()

    def _document(self, document_id: str, primary: str) -> None:
        processing = self.root / "processing" / document_id
        staging = self.root / "corpus/staging/v2" / document_id
        (processing / "chunks").mkdir(parents=True)
        staging.mkdir(parents=True)
        classification = {
            "document_id": document_id, "final_primary_section": primary,
            "final_secondary_sections": [], "final_section_confidence": 0.8,
        }
        metadata = {**classification, "original_sha256": "a" * 64}
        chunk = {
            "chunk_id": f"CHK_{document_id}", "document_id": document_id,
            "chunk_type": "TEXT_CHUNK", "ordinal": 1, "text": "tünel " * 100,
            "token_count": 100, "heading_path": [], "source_elements": ["P1"],
            "final_primary_section": primary, "final_secondary_sections": [],
        }
        atomic_json(processing / "classification.json", classification)
        atomic_json(processing / "metadata.json", metadata)
        atomic_json(processing / "quality_gate.json", {
            "document_id": document_id, "decision": "GO", "reject_reasons": [],
            "review_reasons": [],
        })
        atomic_json(processing / "chunk_quality.json", {
            "document_id": document_id, "status": "PASS", "chunk_count": 1,
        })
        (processing / "chunks/chunk_manifest.jsonl").write_text(
            json.dumps(chunk) + "\n", encoding="utf-8",
        )
        (processing / "chunks/embedding_ready.jsonl").write_text("", encoding="utf-8")
        atomic_json(staging / "metadata.json", metadata)
        atomic_json(staging / "classification.json", classification)
        atomic_json(staging / "bundle.json", {
            "document_id": document_id, "chunk_count": 1,
            "final_primary_section": primary, "final_secondary_sections": [],
        })

    def test_updates_projections_and_quarantines_recoverably(self):
        self._document("ING_update", "3")
        self._document("ING_quarantine", "6")
        self.run_path.parent.mkdir(parents=True)
        atomic_json(self.run_path, {
            "documents": {
                "ING_update": {"disposition": "STAGED", "quality_decision": "GO"},
                "ING_quarantine": {"disposition": "STAGED", "quality_decision": "GO"},
            },
            "staging_audit_ids": ["old"], "promotion_plan_ids": ["old"],
        })
        (self.root / "audit").mkdir(exist_ok=True)
        (self.root / "audit/ingest_manifest.jsonl").write_text(
            "".join(json.dumps({
                "document_id": value, "status": "EMBEDDING_READY",
                "quality_decision": "GO", "staging_path": f"corpus/staging/v2/{value}",
                "embedding_ready_chunks": 1,
            }) + "\n" for value in ("ING_update", "ING_quarantine")), encoding="utf-8",
        )
        (self.root / "audit/ingest_state.jsonl").write_text(
            "".join(json.dumps({
                "document_id": value, "state": "EMBEDDING_READY", "history": [],
            }) + "\n" for value in ("ING_update", "ING_quarantine")), encoding="utf-8",
        )
        atomic_json(self.root / "audit/dashboard/improvements.json", {"status": "FINISHED"})
        atomic_json(self.spec_path, {
            "schema_version": "1.0", "review_id": "MSR_test",
            "expected_scope_count": 2, "scope": ["3", "6"],
            "directives": [
                {"document_id": "ING_update", "action": "UPDATE", "expected_primary": "3",
                 "primary": "4", "secondary": ["6.1"], "reason": "manual correction"},
                {"document_id": "ING_quarantine", "action": "QUARANTINE",
                 "reason_code": "OUT_OF_SCOPE", "reason": "unrelated"},
            ],
        })

        result = apply_review(self.spec_path, self.run_path, self.root)

        self.assertEqual(result["updated"], 1)
        self.assertEqual(result["quarantined"], 1)
        updated = json.loads((self.root / "processing/ING_update/classification.json").read_text())
        self.assertEqual(updated["final_primary_section"], "4")
        self.assertEqual(updated["final_secondary_sections"], ["6.1"])
        self.assertFalse((self.root / "corpus/staging/v2/ING_quarantine").exists())
        self.assertTrue((self.root / result["quarantine_root"] / "ING_quarantine").is_dir())
        manifest = {
            row["document_id"]: row for row in (
                json.loads(line) for line in
                (self.root / "audit/ingest_manifest.jsonl").read_text().splitlines()
            )
        }
        self.assertEqual(manifest["ING_update"]["final_secondary_sections"], ["6.1"])
        self.assertEqual(manifest["ING_quarantine"]["status"], "REJECTED")
        self.assertIsNone(manifest["ING_quarantine"]["staging_path"])
        run = json.loads(self.run_path.read_text())
        self.assertEqual(run["staging_audit_ids"], [])
        self.assertTrue(run["documents"]["ING_quarantine"]["accounted_exclusion"])


if __name__ == "__main__":
    unittest.main()
