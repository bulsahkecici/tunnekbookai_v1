"""Independent, disk-based verification of the active canonical snapshot."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .eligibility import document_digest, validate_chunk_files
from .errors import CanonicalError
from .hashing import canonical_sha256, deterministic_json_text, load_json, load_jsonl, semantic_file_sha256, sha256_file
from .models import (
    CONTRACT_VERSION, SCHEMA_VERSION, CanonicalDocumentRecord, CanonicalInventory,
    CanonicalManifest, CanonicalSnapshot, CanonicalState, require_exact_keys,
)
from .paths import CanonicalContext, require_regular, resolve_declared, validate_document_id, validate_sha256


MANIFEST_KEYS = {
    "schema_version", "contract_version", "document_count", "chunk_count",
    "retrieval_ready_chunk_count", "canonical_corpus_digest", "documents",
}
DOCUMENT_KEYS = {
    "document_id", "document_digest", "source_sha256", "source_kind", "format", "original",
    "upstream", "quality", "classification", "provenance", "document", "chunks", "artifacts",
    "canonical_files", "promotion_plan_id",
}


def corpus_digest(documents: list[Mapping[str, Any]]) -> str:
    return canonical_sha256({
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "documents": [
            {
                "document_id": row["document_id"],
                "document_digest": row["document_digest"],
                "source_sha256": row["source_sha256"],
            }
            for row in sorted(documents, key=lambda item: str(item["document_id"]))
        ],
    })


def build_manifest(documents: list[Mapping[str, Any]]) -> CanonicalManifest:
    ordered = sorted((dict(row) for row in documents), key=lambda item: str(item["document_id"]))
    return CanonicalManifest(
        documents=tuple(CanonicalDocumentRecord(row) for row in ordered),
        canonical_corpus_digest=corpus_digest(ordered),
        chunk_count=sum(int(row["chunks"]["count"]) for row in ordered),
        retrieval_ready_chunk_count=sum(int(row["chunks"]["retrieval_ready_count"]) for row in ordered),
    )


def parse_manifest(payload: Any) -> CanonicalManifest:
    root = require_exact_keys(payload, MANIFEST_KEYS, label="canonical manifest")
    if root["schema_version"] != SCHEMA_VERSION or root["contract_version"] != CONTRACT_VERSION:
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", "unsupported manifest version")
    rows = root["documents"]
    if not isinstance(rows, list) or not rows:
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", "manifest documents must be non-empty")
    for field in ("document_count", "chunk_count", "retrieval_ready_chunk_count"):
        if not isinstance(root[field], int) or isinstance(root[field], bool) or root[field] < 0:
            raise CanonicalError("CANONICAL_MANIFEST_INVALID", f"{field} must be a non-negative integer")
    documents: list[CanonicalDocumentRecord] = []
    for index, value in enumerate(rows):
        row = require_exact_keys(value, DOCUMENT_KEYS, label=f"documents[{index}]")
        documents.append(CanonicalDocumentRecord(dict(row)))
    manifest = CanonicalManifest(
        documents=tuple(documents), canonical_corpus_digest=str(root["canonical_corpus_digest"]),
        chunk_count=int(root["chunk_count"]),
        retrieval_ready_chunk_count=int(root["retrieval_ready_chunk_count"]),
    )
    if root["document_count"] != len(documents):
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", "document count mismatch")
    return manifest


def _canonical_file(context: CanonicalContext, value: object) -> Path:
    return resolve_declared(
        context, value, root=context.canonical_root, code="CANONICAL_MANIFEST_INVALID",
    )


def _verify_document(context: CanonicalContext, row: Mapping[str, Any]) -> tuple[int, int]:
    document_id = validate_document_id(str(row["document_id"]))
    source_sha = validate_sha256(str(row["source_sha256"]), code="CANONICAL_MANIFEST_INVALID")
    digest = validate_sha256(str(row["document_digest"]), code="CANONICAL_MANIFEST_INVALID")
    expected_base = context.canonical_root / "objects" / document_id / digest
    files = row["canonical_files"]
    if not isinstance(files, list) or not files:
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", f"canonical file inventory missing: {document_id}")
    seen_paths: set[str] = set()
    for identity in files:
        if not isinstance(identity, Mapping):
            raise CanonicalError("CANONICAL_MANIFEST_INVALID", "file identity is not an object")
        path = require_regular(_canonical_file(context, identity.get("path")), code="CANONICAL_MANIFEST_INVALID")
        if expected_base.resolve() not in path.parents:
            raise CanonicalError("CANONICAL_PATH_ESCAPE", f"object file outside content-addressed bundle: {path}")
        relative = context.relative(path)
        if relative in seen_paths:
            raise CanonicalError("CANONICAL_MANIFEST_INVALID", f"duplicate canonical file: {relative}")
        seen_paths.add(relative)
        if path.stat().st_size != identity.get("size") or sha256_file(path) != identity.get("sha256"):
            raise CanonicalError("CANONICAL_MANIFEST_INVALID", f"canonical file bytes changed: {relative}")
        if semantic_file_sha256(path) != identity.get("semantic_sha256"):
            raise CanonicalError("CANONICAL_MANIFEST_INVALID", f"canonical file semantics changed: {relative}")
    actual_paths = {
        context.relative(path) for path in expected_base.rglob("*") if path.is_file()
    }
    if actual_paths != seen_paths:
        raise CanonicalError(
            "CANONICAL_MANIFEST_INVALID", f"canonical object file inventory differs: {document_id}",
            details={"missing": sorted(seen_paths - actual_paths), "unexpected": sorted(actual_paths - seen_paths)},
        )
    by_role = {str(item.get("role")): item for item in files if isinstance(item, Mapping)}
    if len(by_role) != len(files):
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", f"duplicate canonical file role: {document_id}")
    required_roles = {
        "document.md", "metadata.json", "metadata_provenance.json", "classification.json",
        "quality_gate.json", "provenance.json", "extraction_report.json", "chunk_quality.json",
        "chunks/chunk_manifest.jsonl", "chunks/embedding_ready.jsonl", "chunks/chunk_identities.jsonl",
    }
    if set(by_role) != required_roles:
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", f"canonical file roles differ: {document_id}")
    expected_artifacts = [
        by_role[role] for role in sorted(required_roles - {
            "document.md", "chunks/chunk_manifest.jsonl", "chunks/embedding_ready.jsonl",
            "chunks/chunk_identities.jsonl",
        })
    ]
    if list(row.get("artifacts") or []) != expected_artifacts or row.get("document") != by_role["document.md"]:
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", f"canonical role references differ: {document_id}")

    original = row["original"]
    if not isinstance(original, Mapping):
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", "original identity is invalid")
    source_path = require_regular(
        resolve_declared(context, original.get("source_path"), root=context.paths.originals_root, code="ORIGINAL_SOURCE_MISSING"),
        code="ORIGINAL_SOURCE_MISSING",
    )
    original_meta = require_regular(
        resolve_declared(context, original.get("metadata_path"), root=context.paths.originals_root, code="ORIGINAL_SOURCE_MISSING"),
        code="ORIGINAL_SOURCE_MISSING",
    )
    if sha256_file(source_path) != source_sha or original.get("source_sha256") != source_sha:
        raise CanonicalError("SOURCE_SHA_MISMATCH", f"canonical source changed: {document_id}")
    if sha256_file(original_meta) != original.get("metadata_sha256"):
        raise CanonicalError("SOURCE_SHA_MISMATCH", f"original metadata changed: {document_id}")

    classification = row["classification"]
    chunks = row["chunks"]
    if not isinstance(classification, Mapping) or not isinstance(chunks, Mapping):
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", "classification or chunks record is invalid")
    quality = row["quality"]
    provenance_record = row["provenance"]
    if not isinstance(quality, Mapping) or not isinstance(provenance_record, Mapping):
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", "quality or provenance record is invalid")
    quality_file = by_role["quality_gate.json"]
    classification_file = by_role["classification.json"]
    provenance_file = by_role["provenance.json"]
    if (
        quality.get("decision") != "GO" or quality.get("artifact_path") != quality_file["path"]
        or quality.get("artifact_sha256") != quality_file["semantic_sha256"]
        or classification.get("artifact_path") != classification_file["path"]
        or classification.get("artifact_sha256") != classification_file["semantic_sha256"]
        or provenance_record.get("path") != provenance_file["path"]
        or provenance_record.get("semantic_sha256") != provenance_file["semantic_sha256"]
    ):
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", f"canonical sidecar references differ: {document_id}")
    quality_payload = load_json(_canonical_file(context, quality_file["path"]), code="CANONICAL_MANIFEST_INVALID")
    classification_payload = load_json(_canonical_file(context, classification_file["path"]), code="CANONICAL_MANIFEST_INVALID")
    provenance_payload = load_json(_canonical_file(context, provenance_file["path"]), code="CANONICAL_MANIFEST_INVALID")
    metadata_payload = load_json(_canonical_file(context, by_role["metadata.json"]["path"]), code="CANONICAL_MANIFEST_INVALID")
    if (
        quality_payload.get("document_id") != document_id or quality_payload.get("decision") != "GO"
        or quality_payload.get("reject_reasons") or quality_payload.get("review_reasons")
        or classification_payload.get("final_primary_section") != classification.get("primary_section")
        or list(classification_payload.get("final_secondary_sections") or []) != list(classification.get("secondary_sections") or [])
        or provenance_payload.get("document_id") != document_id or not provenance_payload.get("sources")
        or metadata_payload.get("document_id") != document_id or metadata_payload.get("original_sha256") != source_sha
    ):
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", f"canonical sidecar content differs: {document_id}")
    manifest_path = require_regular(_canonical_file(context, chunks.get("manifest_path")), code="CHUNK_INTEGRITY_FAILED")
    ready_path = require_regular(_canonical_file(context, chunks.get("retrieval_manifest_path")), code="CHUNK_INTEGRITY_FAILED")
    identities_path = require_regular(_canonical_file(context, chunks.get("identities_path")), code="CHUNK_INTEGRITY_FAILED")
    identities, ready_count, identity_digest, identity_payload = validate_chunk_files(
        context, document_id, source_sha, str(classification.get("primary_section") or ""),
        list(classification.get("secondary_sections") or []), manifest_path, ready_path,
    )
    stored_identities = load_jsonl(identities_path, code="CHUNK_INTEGRITY_FAILED")
    if stored_identities != identities or sha256_file(identities_path) != chunks.get("identities_sha256"):
        raise CanonicalError("CHUNK_INTEGRITY_FAILED", f"chunk identity ledger mismatch: {document_id}")
    if (
        chunks.get("count") != len(identities) or chunks.get("retrieval_ready_count") != ready_count
        or chunks.get("identity_digest") != identity_digest
        or chunks.get("manifest_sha256") != sha256_file(manifest_path)
        or chunks.get("retrieval_manifest_sha256") != sha256_file(ready_path)
    ):
        raise CanonicalError("CHUNK_INTEGRITY_FAILED", f"chunk record mismatch: {document_id}")
    if document_digest(row) != digest:
        raise CanonicalError("CANONICAL_DIGEST_MISMATCH", f"document digest mismatch: {document_id}")
    return len(identities), ready_count


def load_snapshot(
    project_root: Path | str | None = None, *, context: CanonicalContext | None = None,
) -> CanonicalSnapshot:
    context = context or CanonicalContext.load(project_root)
    inventory = inspect_canonical(context=context)
    if not inventory.ready:
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", "canonical corpus is not READY", details=inventory.to_dict())
    manifest = parse_manifest(load_json(context.manifest_path, code="CANONICAL_MANIFEST_INVALID"))
    return CanonicalSnapshot(inventory, manifest)


def inspect_canonical(
    project_root: Path | str | None = None, *, context: CanonicalContext | None = None,
) -> CanonicalInventory:
    context = context or CanonicalContext.load(project_root)
    manifest_rel = context.relative(context.manifest_path)
    if not context.canonical_root.is_dir():
        return CanonicalInventory(CanonicalState.INVALID, 0, 0, 0, manifest_rel, None, None, ("CANONICAL_ROOT_MISSING",))
    material = [path for path in context.canonical_root.rglob("*") if path.is_file() and path.name != ".gitkeep"]
    if not material:
        return CanonicalInventory(CanonicalState.EMPTY, 0, 0, 0, manifest_rel, None, None, ("CANONICAL_CORPUS_EMPTY",))
    if not context.manifest_path.is_file():
        return CanonicalInventory(CanonicalState.INVALID, 0, 0, 0, manifest_rel, None, None, ("CANONICAL_NOT_EMPTY_WITHOUT_MANIFEST",))
    try:
        unexpected_top = [
            path for path in context.canonical_root.iterdir()
            if path.name not in {".gitkeep", "canonical_manifest.json", "objects"}
        ]
        if unexpected_top:
            raise CanonicalError(
                "CANONICAL_MANIFEST_INVALID", "unexpected material in canonical root",
                details=[context.relative(path) for path in unexpected_top],
            )
        payload = load_json(context.manifest_path, code="CANONICAL_MANIFEST_INVALID")
        if context.manifest_path.read_text(encoding="utf-8") != deterministic_json_text(payload):
            raise CanonicalError("CANONICAL_MANIFEST_INVALID", "manifest is not deterministically serialized")
        manifest = parse_manifest(payload)
        records = [record.to_dict() for record in manifest.documents]
        ids = [row["document_id"] for row in records]
        shas = [row["source_sha256"] for row in records]
        if len(ids) != len(set(ids)) or len(shas) != len(set(shas)):
            raise CanonicalError("CANONICAL_MANIFEST_INVALID", "duplicate document ID or source SHA")
        chunk_count = ready_count = 0
        for row in records:
            chunks, ready = _verify_document(context, row)
            chunk_count += chunks
            ready_count += ready
        expected_digest = corpus_digest(records)
        if manifest.canonical_corpus_digest != expected_digest:
            raise CanonicalError("CANONICAL_DIGEST_MISMATCH", "canonical corpus digest mismatch")
        if manifest.chunk_count != chunk_count or manifest.retrieval_ready_chunk_count != ready_count:
            raise CanonicalError("CANONICAL_MANIFEST_INVALID", "canonical aggregate count mismatch")
        active_bases = {
            (context.canonical_root / "objects" / str(row["document_id"]) / str(row["document_digest"])).resolve()
            for row in records
        }
        all_bases = {
            path.resolve() for path in (context.canonical_root / "objects").glob("*/*") if path.is_dir()
        } if (context.canonical_root / "objects").is_dir() else set()
        warnings = tuple(f"UNREFERENCED_CANONICAL_OBJECT:{context.relative(path)}" for path in sorted(all_bases - active_bases))
        return CanonicalInventory(
            CanonicalState.READY, len(records), chunk_count, ready_count, manifest_rel,
            sha256_file(context.manifest_path), expected_digest, (), warnings,
        )
    except (CanonicalError, OSError, UnicodeError, ValueError, TypeError) as exc:
        code = exc.code if isinstance(exc, CanonicalError) else "CANONICAL_MANIFEST_INVALID"
        return CanonicalInventory(
            CanonicalState.INVALID, 0, 0, 0, manifest_rel,
            sha256_file(context.manifest_path) if context.manifest_path.is_file() else None,
            None, (code, str(exc)),
        )


def require_ready(project_root: Path | str | None = None) -> CanonicalSnapshot:
    return load_snapshot(project_root)


__all__ = ["build_manifest", "corpus_digest", "inspect_canonical", "load_snapshot", "parse_manifest", "require_ready"]
