from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path

from tunnelbookai.ingest.chunking.policy import ChunkPolicy, chunk_id
from tunnelbookai.ingest.chunking.tokenizer import count
from tunnelbookai.ingest.ids import document_id_for_sha256
from tunnelbookai.ingest.staging import BUNDLE_SHAPE, STAGING_COPY_FILES, STAGING_VERSION
from shared.project_quality_gate import SUPPORTED_SCRIPTS


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


class SyntheticRepo:
    def __init__(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        shutil.copytree(
            PROJECT_ROOT / "book", self.root / "book",
            ignore=shutil.ignore_patterns("retrieval"),
        )
        (self.root / "config").mkdir()
        for name in ("paths.json", "models.yaml"):
            shutil.copyfile(PROJECT_ROOT / "config" / name, self.root / "config" / name)
        for relative in (
            "corpus/canonical", "corpus/staging/v2", "originals", "processing", "audit", "scripts",
            "incoming/papercrawler/releases", "incoming/manual/inbox",
        ):
            (self.root / relative).mkdir(parents=True, exist_ok=True)
        (self.root / "corpus/canonical/.gitkeep").touch()
        for name in SUPPORTED_SCRIPTS:
            (self.root / "scripts" / name).touch()
        scope = json.loads((self.root / "book/scope/normalized/book_scope.json").read_text(encoding="utf-8"))
        self.section_id = str(scope["sections"][0]["section_id"])
        self.document_id = self.add_candidate(b"synthetic canonical evidence")

    def close(self) -> None:
        self.temporary.cleanup()

    def add_candidate(self, source: bytes) -> str:
        source_sha = hashlib.sha256(source).hexdigest()
        document_id = document_id_for_sha256(source_sha)
        original = self.root / "originals" / document_id
        processing = self.root / "processing" / document_id
        staging = self.root / "corpus/staging" / STAGING_VERSION / document_id
        for path in (original, processing / "normalized", processing / "chunks", staging):
            path.mkdir(parents=True, exist_ok=True)
        source_path = original / "source.pdf"
        source_path.write_bytes(source)
        write_json(original / "original.json", {
            "document_id": document_id, "original_filename": "source.pdf",
            "original_sha256": source_sha, "source_kind": "MANUAL_INTERNAL", "format": "PDF",
            "mime_type": "application/pdf", "archive_path": f"originals/{document_id}/source.pdf",
        })
        metadata = {
            "document_id": document_id, "source_kind": "MANUAL_INTERNAL", "original_filename": "source.pdf",
            "original_sha256": source_sha, "format": "PDF", "mime_type": "application/pdf",
            "confidentiality": "INTERNAL", "document_status": "FINAL", "ingest_method": "manual",
            "title": "Synthetic evidence", "authors": [], "organization": None, "department": None,
            "document_date": None, "revision": None, "language": "en", "document_type": None,
            "topics": [], "source_url": None, "doi": None, "final_primary_section": self.section_id,
            "final_secondary_sections": [], "final_section_confidence": 1.0,
            "final_evidence_level": "FULL_TEXT", "content_capabilities": {"text": True}, "schema_version": "1.0",
        }
        classification = {
            "final_primary_section": self.section_id, "final_secondary_sections": [],
            "final_section_confidence": 1.0, "classification_methods": ["heading_rules"],
            "section_evidence": {}, "candidates": [], "embedding_status": "DISABLED",
            "embedding_model": None, "arbiter_status": "DISABLED", "arbiter_reason": None,
            "arbiter_model": None, "decision_path": "deterministic", "warnings": [],
            "taxonomy_source": "book/scope/normalized/book_scope.json",
        }
        sidecars = {
            "metadata.json": metadata,
            "metadata_provenance.json": {"document_id": document_id, "fields": []},
            "classification.json": classification,
            "quality_gate.json": {"document_id": document_id, "decision": "GO", "checks": {}, "reject_reasons": [], "review_reasons": [], "notes": []},
            "provenance.json": {"document_id": document_id, "sources": [{"kind": "MANUAL_INTERNAL"}], "original": {"original_sha256": source_sha}},
            "extraction_report.json": {"document_id": document_id, "format": "PDF", "errors": [], "warnings": []},
            "chunk_quality.json": {"document_id": document_id, "status": "PASS", "chunk_count": 1, "policy": {"chunk_schema_version": "1.0", "chunk_policy_version": "structure-aware-v1"}, "errors": [], "warnings": []},
        }
        text = "Synthetic evidence paragraph with enough content for a deterministic retrieval row."
        policy = ChunkPolicy()
        chunk = {
            "chunk_id": chunk_id(document_id, "TEXT_CHUNK", ["E1"], text, policy),
            "document_id": document_id, "chunk_type": "TEXT_CHUNK", "final_primary_section": self.section_id,
            "final_secondary_sections": [], "heading_path": [], "page_start": 1, "page_end": 1,
            "slide_number": None, "sheet_name": None, "cell_range": None, "source_elements": ["E1"],
            "text": text, "token_count": count(text),
            "provenance": {"original_sha256": source_sha, "source_kind": "MANUAL_INTERNAL", "format": "PDF", "evidence_level": "FULL_TEXT"},
            "chunk_schema_version": policy.schema_version, "chunk_policy_version": policy.policy_version,
            "tokenizer": policy.tokenizer_name, "ordinal": 0,
        }
        ready = {
            "chunk_id": chunk["chunk_id"], "document_id": document_id, "chunk_type": "TEXT_CHUNK",
            "section_id": self.section_id, "secondary_section_ids": [], "ordinal": 0,
            "text_path": None, "embedding_text": text, "token_count": count(text), "page_start": 1,
            "page_end": 1, "slide_number": None, "sheet_name": None, "provenance": chunk["provenance"],
            "chunk_schema_version": policy.schema_version, "chunk_policy_version": policy.policy_version,
            "eligible": True, "reason": "READY",
        }
        document_text = "# Synthetic evidence\n\n" + text + "\n"
        (processing / "normalized/document.md").write_text(document_text, encoding="utf-8")
        for name, value in sidecars.items():
            write_json(processing / name, value)
        write_jsonl(processing / "chunks/chunk_manifest.jsonl", [chunk])
        write_jsonl(processing / "chunks/embedding_ready.jsonl", [ready])
        shutil.copyfile(processing / "normalized/document.md", staging / "document.md")
        for name in STAGING_COPY_FILES:
            shutil.copyfile(processing / name, staging / name)
        write_json(staging / "bundle.json", {
            "bundle_shape": BUNDLE_SHAPE, "staging_version": STAGING_VERSION,
            "document_id": document_id, "original_sha256": source_sha, "source_kind": "MANUAL_INTERNAL",
            "format": "PDF", "title": "Synthetic evidence", "final_primary_section": self.section_id,
            "final_secondary_sections": [], "final_section_confidence": 1.0,
            "final_evidence_level": "FULL_TEXT", "content_capabilities": {"text": True},
            "quality_decision": "GO", "processing_bundle": f"processing/{document_id}",
            "original_archive": f"originals/{document_id}",
            "chunks_authoritative_path": f"processing/{document_id}/chunks/chunk_manifest.jsonl",
            "chunk_count": 1, "chunk_quality_status": "PASS", "canonical_promoted": False,
        })
        self._append_ledger("source_registry.jsonl", {
            "document_id": document_id, "sha256": source_sha, "doi": None, "url": None,
            "title": "synthetic evidence", "year": None, "organization": None, "authors": [],
            "title_is_weak": False, "state": "DEDUP_COMPLETED", "source_kinds": ["MANUAL_INTERNAL"],
            "provenance_sources": [{"kind": "MANUAL_INTERNAL"}], "provenance_source_count": 1,
        })
        self._append_ledger("document_id_map.jsonl", {"document_id": document_id, "sha256": source_sha, "aliases": {}})
        self._append_ledger("ingest_manifest.jsonl", {
            "document_id": document_id, "sha256": source_sha, "status": "EMBEDDING_READY",
            "quality_decision": "GO", "duplicate_of": None,
        })
        self._append_ledger("ingest_state.jsonl", {"document_id": document_id, "sha256": source_sha, "state": "EMBEDDING_READY"})
        return document_id

    def _append_ledger(self, name: str, row: dict) -> None:
        path = self.root / "audit" / name
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
