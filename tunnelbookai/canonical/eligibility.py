"""Read-only verification of Unified Ingest staging candidates."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Iterable, Mapping

from tunnelbookai.ingest.chunking.policy import ChunkPolicy, chunk_id
from tunnelbookai.ingest.dedup import DedupKey, SourceRegistry, active_document_ids
from tunnelbookai.ingest.ids import document_id_for_sha256
from tunnelbookai.ingest.metadata.schema import validate as validate_metadata
from tunnelbookai.ingest.staging import BUNDLE_SHAPE, STAGING_COPY_FILES, STAGING_VERSION

from .errors import CanonicalError
from .hashing import canonical_json_bytes, canonical_sha256, load_json, load_jsonl, semantic_file_sha256, sha256_file
from .models import CandidateAction, CanonicalPromotionCandidate, CONTRACT_VERSION, FileIdentity
from .paths import CanonicalContext, require_regular, resolve_declared, validate_document_id, validate_sha256


def _identity(context: CanonicalContext, path: Path) -> FileIdentity:
    require_regular(path, code="INVALID_STAGING_BUNDLE")
    return FileIdentity(
        path=context.relative(path), size=path.stat().st_size, sha256=sha256_file(path),
        semantic_sha256=semantic_file_sha256(path),
    )


def _future_identity(context: CanonicalContext, path: Path, source: Path) -> dict[str, Any]:
    identity = _identity(context, source)
    return {
        "path": context.relative(path), "size": identity.size,
        "sha256": identity.sha256, "semantic_sha256": identity.semantic_sha256,
    }


def _require_mapping(value: Any, *, code: str, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CanonicalError(code, f"{label} must be an object")
    return value


def _ledger_rows(context: CanonicalContext, path: Path, document_id: str, source_sha: str) -> list[dict[str, Any]]:
    rows = load_jsonl(path, code="UPSTREAM_DEDUP_VERIFICATION_FAILED") if path.is_file() else []
    return [row for row in rows if row.get("document_id") == document_id or row.get("sha256") == source_sha]


def _ledger_identity(context: CanonicalContext, document_id: str, source_sha: str) -> tuple[str, dict[str, list[dict[str, Any]]]]:
    names = {
        "source_registry": context.paths.source_registry_path,
        "document_id_map": context.paths.document_id_map_path,
        "ingest_manifest": context.paths.ingest_manifest_path,
        "ingest_state": context.paths.ingest_state_path,
    }
    selected = {name: _ledger_rows(context, path, document_id, source_sha) for name, path in names.items()}
    return canonical_sha256(selected), selected


def _validate_ledgers(context: CanonicalContext, metadata: dict[str, Any], source_sha: str) -> str:
    document_id = str(metadata["document_id"])
    digest, selected = _ledger_identity(context, document_id, source_sha)
    for name in ("source_registry", "document_id_map", "ingest_manifest", "ingest_state"):
        own = [row for row in selected[name] if row.get("document_id") == document_id]
        if len(own) != 1 or own[0].get("sha256") != source_sha:
            raise CanonicalError(
                "UPSTREAM_DEDUP_VERIFICATION_FAILED", f"{name} does not uniquely agree with candidate",
            )
    registry_row = next(row for row in selected["source_registry"] if row.get("document_id") == document_id)
    if registry_row.get("duplicate_of"):
        raise CanonicalError("UPSTREAM_DEDUP_VERIFICATION_FAILED", "source registry marks candidate duplicate")
    ingest_row = next(row for row in selected["ingest_manifest"] if row.get("document_id") == document_id)
    state_row = next(row for row in selected["ingest_state"] if row.get("document_id") == document_id)
    id_row = next(row for row in selected["document_id_map"] if row.get("document_id") == document_id)
    if ingest_row.get("duplicate_of") or ingest_row.get("quality_decision") != "GO":
        raise CanonicalError("UPSTREAM_DEDUP_VERIFICATION_FAILED", "ingest manifest is not uniquely eligible")
    if state_row.get("state") != "EMBEDDING_READY" or id_row.get("sha256") != source_sha:
        raise CanonicalError("UPSTREAM_DEDUP_VERIFICATION_FAILED", "ingest state or document map is inconsistent")
    match = SourceRegistry(
        context.paths.source_registry_path,
        active_document_ids=active_document_ids(context.root),
    ).find(DedupKey.from_metadata(metadata))
    if match is not None and match.strength in {"EXACT", "STRONG"}:
        raise CanonicalError(
            "UPSTREAM_DEDUP_VERIFICATION_FAILED",
            f"upstream duplicate {match.rule}:{match.document_id}",
        )
    return digest


def validate_chunk_files(
    context: CanonicalContext, document_id: str, source_sha: str, primary: str,
    secondary: list[str], chunk_path: Path, ready_path: Path,
) -> tuple[list[dict[str, Any]], int, str, bytes]:
    chunks = load_jsonl(chunk_path, code="CHUNK_INTEGRITY_FAILED")
    ready_rows = load_jsonl(ready_path, code="CHUNK_INTEGRITY_FAILED")
    if not chunks or len(chunks) != len(ready_rows):
        raise CanonicalError("CHUNK_INTEGRITY_FAILED", "chunk and retrieval row counts differ or are empty")
    ready_by_id: dict[str, dict[str, Any]] = {}
    for row in ready_rows:
        cid = str(row.get("chunk_id") or "")
        if not cid or cid in ready_by_id:
            raise CanonicalError("CHUNK_INTEGRITY_FAILED", f"duplicate retrieval row: {cid}")
        ready_by_id[cid] = row
    identities: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in chunks:
        cid = str(row.get("chunk_id") or "")
        if not cid or cid in seen or cid not in ready_by_id:
            raise CanonicalError("CHUNK_INTEGRITY_FAILED", f"invalid or duplicate chunk id: {cid}")
        seen.add(cid)
        provenance = _require_mapping(row.get("provenance"), code="CHUNK_INTEGRITY_FAILED", label="chunk provenance")
        if row.get("document_id") != document_id or provenance.get("original_sha256") != source_sha:
            raise CanonicalError("CHUNK_INTEGRITY_FAILED", f"chunk identity mismatch: {cid}")
        if row.get("final_primary_section") != primary or list(row.get("final_secondary_sections") or []) != secondary:
            raise CanonicalError("CHUNK_INTEGRITY_FAILED", f"chunk classification mismatch: {cid}")
        policy = ChunkPolicy(
            schema_version=str(row.get("chunk_schema_version") or ""),
            policy_version=str(row.get("chunk_policy_version") or ""),
        )
        expected = chunk_id(
            document_id, str(row.get("chunk_type") or ""), list(row.get("source_elements") or []),
            str(row.get("text") or ""), policy,
        )
        if cid != expected:
            raise CanonicalError("CHUNK_INTEGRITY_FAILED", f"chunk id does not recompute: {cid}")
        ready = ready_by_id[cid]
        if ready.get("document_id") != document_id or ready.get("section_id") != primary:
            raise CanonicalError("CHUNK_INTEGRITY_FAILED", f"retrieval row mismatch: {cid}")
        identities.append({
            "chunk_id": cid,
            "chunk_sha256": canonical_sha256(row),
            "retrieval_row_sha256": canonical_sha256(ready),
        })
    identities.sort(key=lambda item: item["chunk_id"])
    payload = b"".join(canonical_json_bytes(row) + b"\n" for row in identities)
    ready_count = sum(1 for row in ready_rows if row.get("eligible") is True)
    if ready_count < 1:
        raise CanonicalError("CHUNK_INTEGRITY_FAILED", "candidate has no eligible retrieval chunks")
    return identities, ready_count, canonical_sha256(identities), payload


def document_digest(record: Mapping[str, Any]) -> str:
    projection = {
        "contract_version": CONTRACT_VERSION,
        "document_id": record["document_id"],
        "source_sha256": record["source_sha256"],
        "source_kind": record["source_kind"],
        "format": record["format"],
        "document_semantic_sha256": record["document"]["semantic_sha256"],
        "artifact_semantic_sha256": {
            item["role"]: item["semantic_sha256"] for item in record["artifacts"]
        },
        "chunk_count": record["chunks"]["count"],
        "retrieval_ready_chunk_count": record["chunks"]["retrieval_ready_count"],
        "chunk_identity_digest": record["chunks"]["identity_digest"],
    }
    return canonical_sha256(projection)


def inspect_candidate(
    context: CanonicalContext, staging_dir: Path, *, existing_documents: Iterable[Mapping[str, Any]] = (),
) -> CanonicalPromotionCandidate:
    document_id = staging_dir.name
    try:
        validate_document_id(document_id)
        if staging_dir.is_symlink() or staging_dir.parent.resolve() != (context.paths.corpus_staging_root / STAGING_VERSION).resolve():
            raise CanonicalError("CANONICAL_PATH_ESCAPE", "candidate is not a direct v2 staging child")
        bundle_path = require_regular(staging_dir / "bundle.json", code="INVALID_STAGING_BUNDLE")
        bundle = dict(_require_mapping(load_json(bundle_path, code="INVALID_STAGING_BUNDLE"), code="INVALID_STAGING_BUNDLE", label="bundle"))
        if bundle.get("bundle_shape") != BUNDLE_SHAPE or bundle.get("staging_version") != STAGING_VERSION:
            raise CanonicalError("INVALID_STAGING_BUNDLE", "unsupported staging contract")
        if bundle.get("document_id") != document_id:
            raise CanonicalError("INVALID_STAGING_BUNDLE", "directory and bundle document IDs differ")
        source_sha = validate_sha256(str(bundle.get("original_sha256") or ""))
        if document_id_for_sha256(source_sha) != document_id:
            raise CanonicalError("SOURCE_SHA_MISMATCH", "document ID is not derived from source SHA")

        processing = resolve_declared(
            context, bundle.get("processing_bundle"), root=context.paths.processing_root,
            code="PROCESSING_IDENTITY_MISMATCH",
        )
        original_dir = resolve_declared(
            context, bundle.get("original_archive"), root=context.paths.originals_root,
            code="ORIGINAL_SOURCE_MISSING",
        )
        expected_processing = (context.paths.processing_root / document_id).resolve()
        expected_original = (context.paths.originals_root / document_id).resolve()
        if processing != expected_processing or original_dir != expected_original:
            raise CanonicalError("PROCESSING_IDENTITY_MISMATCH", "upstream bundle path does not match document ID")

        original_json_path = require_regular(original_dir / "original.json", code="ORIGINAL_SOURCE_MISSING")
        original = dict(_require_mapping(load_json(original_json_path), code="ORIGINAL_SOURCE_MISSING", label="original.json"))
        source_path = require_regular(
            resolve_declared(
                context, original.get("archive_path"), root=original_dir,
                code="ORIGINAL_SOURCE_MISSING",
            ),
            code="ORIGINAL_SOURCE_MISSING",
        )
        if source_path.parent != original_dir.resolve() or not source_path.name.startswith("source"):
            raise CanonicalError("CANONICAL_PATH_ESCAPE", "unsafe original archive path")
        if original.get("document_id") != document_id or original.get("original_sha256") != source_sha:
            raise CanonicalError("SOURCE_SHA_MISMATCH", "original.json identity mismatch")
        if sha256_file(source_path) != source_sha:
            raise CanonicalError("SOURCE_SHA_MISMATCH", "original source bytes changed")

        required_staged = [staging_dir / "document.md", *(staging_dir / name for name in STAGING_COPY_FILES)]
        for path in required_staged:
            require_regular(path, code="INVALID_STAGING_BUNDLE")
            if staging_dir.resolve() not in path.resolve().parents:
                raise CanonicalError("CANONICAL_PATH_ESCAPE", f"staging artifact escapes bundle: {path}")
        processing_sources: dict[str, Path] = {
            "document.md": processing / "normalized" / "document.md",
            **{name: processing / name for name in STAGING_COPY_FILES},
        }
        for staged in required_staged:
            authoritative = require_regular(processing_sources[staged.name], code="PROCESSING_IDENTITY_MISMATCH")
            if processing.resolve() not in authoritative.resolve().parents:
                raise CanonicalError("CANONICAL_PATH_ESCAPE", f"processing artifact escapes bundle: {authoritative}")
            if sha256_file(staged) != sha256_file(authoritative):
                raise CanonicalError("PROCESSING_IDENTITY_MISMATCH", f"staging differs from processing: {staged.name}")

        metadata = dict(_require_mapping(load_json(processing / "metadata.json"), code="INVALID_STAGING_BUNDLE", label="metadata"))
        problems = validate_metadata(metadata)
        if problems or metadata.get("document_id") != document_id or metadata.get("original_sha256") != source_sha:
            raise CanonicalError("INVALID_STAGING_BUNDLE", "metadata is invalid", details=problems)
        if metadata.get("source_kind") != bundle.get("source_kind") or metadata.get("format") != bundle.get("format"):
            raise CanonicalError("INVALID_STAGING_BUNDLE", "metadata and staging source fields differ")

        metadata_provenance = _require_mapping(load_json(processing / "metadata_provenance.json"), code="PROVENANCE_VERIFICATION_FAILED", label="metadata provenance")
        if metadata_provenance.get("document_id") != document_id or not isinstance(metadata_provenance.get("fields"), list):
            raise CanonicalError("PROVENANCE_VERIFICATION_FAILED", "metadata provenance is invalid")
        provenance = _require_mapping(load_json(processing / "provenance.json"), code="PROVENANCE_VERIFICATION_FAILED", label="provenance")
        if provenance.get("document_id") != document_id or not provenance.get("sources"):
            raise CanonicalError("PROVENANCE_VERIFICATION_FAILED", "provenance source chain is missing")
        provenance_original = _require_mapping(provenance.get("original"), code="PROVENANCE_VERIFICATION_FAILED", label="provenance original")
        if provenance_original.get("original_sha256") != source_sha:
            raise CanonicalError("PROVENANCE_VERIFICATION_FAILED", "provenance source SHA differs")

        classification = _require_mapping(load_json(processing / "classification.json"), code="CLASSIFICATION_INVALID", label="classification")
        primary = str(classification.get("final_primary_section") or "")
        secondary = [str(value) for value in classification.get("final_secondary_sections") or []]
        confidence = classification.get("final_section_confidence")
        valid_sections = context.book_inputs.scope_by_id
        if (
            primary not in valid_sections or len(secondary) != len(set(secondary))
            or primary in secondary or any(value not in valid_sections for value in secondary)
            or not isinstance(confidence, (int, float)) or isinstance(confidence, bool)
            or not 0 <= float(confidence) <= 1
            or classification.get("taxonomy_source") != "book/scope/normalized/book_scope.json"
        ):
            raise CanonicalError("CLASSIFICATION_INVALID", "classification is not valid against frozen scope")
        if metadata.get("final_primary_section") != primary or list(metadata.get("final_secondary_sections") or []) != secondary:
            raise CanonicalError("CLASSIFICATION_INVALID", "classification and metadata differ")
        if bundle.get("final_primary_section") != primary or list(bundle.get("final_secondary_sections") or []) != secondary:
            raise CanonicalError("CLASSIFICATION_INVALID", "classification and staging bundle differ")

        quality = _require_mapping(load_json(processing / "quality_gate.json"), code="QUALITY_NOT_ELIGIBLE", label="quality")
        if (
            quality.get("document_id") != document_id or quality.get("decision") != "GO"
            or quality.get("reject_reasons") or quality.get("review_reasons")
        ):
            raise CanonicalError("QUALITY_NOT_ELIGIBLE", "document quality gate is not clean GO")
        chunk_quality = _require_mapping(load_json(processing / "chunk_quality.json"), code="CHUNK_INTEGRITY_FAILED", label="chunk quality")
        if chunk_quality.get("document_id") != document_id or chunk_quality.get("status") not in {"PASS", "WARN"} or chunk_quality.get("errors"):
            raise CanonicalError("CHUNK_INTEGRITY_FAILED", "chunk quality is not eligible")

        chunk_path = resolve_declared(
            context, bundle.get("chunks_authoritative_path"), root=processing,
            code="CHUNK_INTEGRITY_FAILED",
        )
        expected_chunk_path = processing / "chunks" / "chunk_manifest.jsonl"
        if chunk_path != expected_chunk_path.resolve():
            raise CanonicalError("CHUNK_INTEGRITY_FAILED", "unexpected authoritative chunk path")
        ready_path = require_regular(processing / "chunks" / "embedding_ready.jsonl", code="CHUNK_INTEGRITY_FAILED")
        if processing.resolve() not in ready_path.resolve().parents:
            raise CanonicalError("CANONICAL_PATH_ESCAPE", "embedding-ready manifest escapes processing")
        identities, ready_count, identity_digest, identity_payload = validate_chunk_files(
            context, document_id, source_sha, primary, secondary,
            require_regular(chunk_path, code="CHUNK_INTEGRITY_FAILED"), ready_path,
        )
        if bundle.get("chunk_count") != len(identities) or chunk_quality.get("chunk_count") != len(identities):
            raise CanonicalError("CHUNK_INTEGRITY_FAILED", "declared chunk counts differ")

        ledger_digest = _validate_ledgers(context, metadata, source_sha)
        inputs = [
            _identity(context, bundle_path), _identity(context, original_json_path), _identity(context, source_path),
            *(_identity(context, path) for path in required_staged),
            *(_identity(context, path) for path in processing_sources.values()),
            _identity(context, chunk_path), _identity(context, ready_path),
        ]
        unique_inputs = {item.path: item for item in inputs}
        processing_identity = canonical_sha256({
            name: sha256_file(path) for name, path in sorted(processing_sources.items())
        } | {"chunks/chunk_manifest.jsonl": sha256_file(chunk_path), "chunks/embedding_ready.jsonl": sha256_file(ready_path)})
        staging_identity = canonical_sha256({item.path: item.sha256 for item in inputs if item.path.startswith(context.relative(staging_dir) + "/")})

        object_base = context.canonical_root / "objects" / document_id / "PENDING"
        source_map = {
            "document.md": staging_dir / "document.md",
            **{name: staging_dir / name for name in STAGING_COPY_FILES},
            "chunks/chunk_manifest.jsonl": chunk_path,
            "chunks/embedding_ready.jsonl": ready_path,
        }
        canonical_files = [
            {"role": name, **_future_identity(context, object_base / name, source)}
            for name, source in sorted(source_map.items())
        ]
        identity_future = object_base / "chunks" / "chunk_identities.jsonl"
        canonical_files.append({
            "role": "chunks/chunk_identities.jsonl", "path": context.relative(identity_future),
            "size": len(identity_payload), "sha256": hashlib.sha256(identity_payload).hexdigest(),
            "semantic_sha256": canonical_sha256(identities),
        })
        artifacts = [item for item in canonical_files if item["role"] not in {"document.md", "chunks/chunk_manifest.jsonl", "chunks/embedding_ready.jsonl", "chunks/chunk_identities.jsonl"}]
        record: dict[str, Any] = {
            "document_id": document_id,
            "source_sha256": source_sha,
            "source_kind": metadata["source_kind"],
            "format": metadata["format"],
            "original": {
                "source_path": context.relative(source_path), "metadata_path": context.relative(original_json_path),
                "metadata_sha256": sha256_file(original_json_path), "source_sha256": source_sha,
            },
            "upstream": {
                "processing_path": context.relative(processing), "processing_identity": processing_identity,
                "staging_path": context.relative(staging_dir), "staging_version": STAGING_VERSION,
                "staging_bundle_sha256": sha256_file(bundle_path), "staging_identity": staging_identity,
                "ingest_ledger_identity": ledger_digest,
            },
            "quality": {"decision": "GO", "artifact_path": next(item["path"] for item in artifacts if item["role"] == "quality_gate.json"), "artifact_sha256": semantic_file_sha256(processing / "quality_gate.json")},
            "classification": {
                "primary_section": primary, "secondary_sections": secondary, "confidence": float(confidence),
                "artifact_path": next(item["path"] for item in artifacts if item["role"] == "classification.json"),
                "artifact_sha256": semantic_file_sha256(processing / "classification.json"),
            },
            "provenance": {"path": next(item["path"] for item in artifacts if item["role"] == "provenance.json"), "semantic_sha256": semantic_file_sha256(processing / "provenance.json")},
            "document": next(item for item in canonical_files if item["role"] == "document.md"),
            "chunks": {
                "count": len(identities), "retrieval_ready_count": ready_count,
                "manifest_path": next(item["path"] for item in canonical_files if item["role"] == "chunks/chunk_manifest.jsonl"),
                "manifest_sha256": sha256_file(chunk_path),
                "retrieval_manifest_path": next(item["path"] for item in canonical_files if item["role"] == "chunks/embedding_ready.jsonl"),
                "retrieval_manifest_sha256": sha256_file(ready_path),
                "identities_path": context.relative(identity_future),
                "identities_sha256": hashlib.sha256(identity_payload).hexdigest(),
                "identity_digest": identity_digest,
            },
            "artifacts": artifacts,
            "canonical_files": sorted(canonical_files, key=lambda item: item["path"]),
        }
        digest = document_digest(record)
        real_base = context.canonical_root / "objects" / document_id / digest
        pending_prefix = context.relative(object_base)
        real_prefix = context.relative(real_base)
        def replace_paths(value: Any) -> Any:
            if isinstance(value, dict):
                return {key: replace_paths(child) for key, child in value.items()}
            if isinstance(value, list):
                return [replace_paths(child) for child in value]
            if isinstance(value, str) and value.startswith(pending_prefix):
                return real_prefix + value[len(pending_prefix):]
            return value
        record = replace_paths(record)
        record["document_digest"] = digest

        existing_by_id = {str(row.get("document_id")): row for row in existing_documents}
        existing_by_sha = {str(row.get("source_sha256")): row for row in existing_documents}
        if document_id in existing_by_id:
            if existing_by_id[document_id].get("document_digest") == digest:
                action = CandidateAction.IDEMPOTENT_NO_CHANGE
            else:
                raise CanonicalError("DOCUMENT_ID_CONFLICT", "canonical document ID has different identity")
        elif source_sha in existing_by_sha:
            raise CanonicalError("EXACT_SOURCE_DUPLICATE", "source SHA is already canonical under another document ID")
        else:
            action = CandidateAction.PROMOTE

        return CanonicalPromotionCandidate(
            document_id=document_id, action=action, source_sha256=source_sha,
            chunk_count=len(identities), retrieval_ready_chunk_count=ready_count,
            document_digest=digest, input_files=tuple(sorted(unique_inputs.values(), key=lambda item: item.path)),
            validations=("IDENTITY", "ORIGINAL", "PROCESSING", "METADATA", "PROVENANCE", "CLASSIFICATION", "QUALITY", "CHUNKS", "DEDUP"),
            warnings=tuple(str(value) for value in chunk_quality.get("warnings") or []), record=record,
        )
    except CanonicalError as exc:
        return CanonicalPromotionCandidate(
            document_id=document_id, action=CandidateAction.REJECTED, source_sha256=None,
            chunk_count=0, retrieval_ready_chunk_count=0, document_digest=None,
            validations=(exc.code,), warnings=(str(exc),), record=None,
        )


def discover_candidates(
    context: CanonicalContext, document_ids: Iterable[str] | None = None,
    *, existing_documents: Iterable[Mapping[str, Any]] = (),
) -> tuple[CanonicalPromotionCandidate, ...]:
    root = context.paths.corpus_staging_root / STAGING_VERSION
    selected = sorted(set(document_ids or []))
    if selected:
        directories = [root / validate_document_id(document_id) for document_id in selected]
    elif root.is_dir():
        directories = sorted(path for path in root.iterdir() if path.is_dir() or path.is_symlink())
    else:
        directories = []
    return tuple(inspect_candidate(context, path, existing_documents=existing_documents) for path in directories)


__all__ = ["discover_candidates", "document_digest", "inspect_candidate", "validate_chunk_files"]
