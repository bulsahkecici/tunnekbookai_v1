"""Typed public models for canonical plans, manifests, audits, and inventory."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any, Mapping

from .errors import CanonicalError


SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "controlled-canonical-promotion-v1"


class CanonicalState(StrEnum):
    EMPTY = "EMPTY"
    READY = "READY"
    INVALID = "INVALID"


class CandidateAction(StrEnum):
    PROMOTE = "PROMOTE"
    IDEMPOTENT_NO_CHANGE = "IDEMPOTENT_NO_CHANGE"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class FileIdentity:
    path: str
    size: int
    sha256: str
    semantic_sha256: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CanonicalDocumentRecord:
    payload: Mapping[str, Any]

    @property
    def document_id(self) -> str:
        return str(self.payload["document_id"])

    @property
    def document_digest(self) -> str:
        return str(self.payload["document_digest"])

    def to_dict(self) -> dict[str, Any]:
        return dict(self.payload)


@dataclass(frozen=True)
class CanonicalPromotionCandidate:
    document_id: str
    action: CandidateAction
    source_sha256: str | None
    chunk_count: int
    retrieval_ready_chunk_count: int
    document_digest: str | None
    input_files: tuple[FileIdentity, ...] = ()
    validations: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    record: Mapping[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "document_id": self.document_id,
            "action": self.action.value,
            "source_sha256": self.source_sha256,
            "chunk_count": self.chunk_count,
            "retrieval_ready_chunk_count": self.retrieval_ready_chunk_count,
            "document_digest": self.document_digest,
            "input_files": [item.to_dict() for item in self.input_files],
            "validations": list(self.validations),
            "warnings": list(self.warnings),
            "record": dict(self.record) if self.record is not None else None,
        }


@dataclass(frozen=True)
class CanonicalPromotionPlan:
    plan_id: str
    selector: Mapping[str, Any]
    authorities: Mapping[str, str]
    before: Mapping[str, Any]
    candidates: tuple[CanonicalPromotionCandidate, ...]
    applicable: bool
    expected_after: Mapping[str, Any]
    schema_version: str = SCHEMA_VERSION
    contract_version: str = CONTRACT_VERSION

    def body(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "contract_version": self.contract_version,
            "selector": dict(self.selector),
            "authorities": dict(self.authorities),
            "before": dict(self.before),
            "candidates": [candidate.to_dict() for candidate in self.candidates],
            "applicable": self.applicable,
            "expected_after": dict(self.expected_after),
        }

    def to_dict(self) -> dict[str, Any]:
        return {"plan_id": self.plan_id, **self.body()}


@dataclass(frozen=True)
class CanonicalManifest:
    documents: tuple[CanonicalDocumentRecord, ...]
    canonical_corpus_digest: str
    chunk_count: int
    retrieval_ready_chunk_count: int
    schema_version: str = SCHEMA_VERSION
    contract_version: str = CONTRACT_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "contract_version": self.contract_version,
            "document_count": len(self.documents),
            "chunk_count": self.chunk_count,
            "retrieval_ready_chunk_count": self.retrieval_ready_chunk_count,
            "canonical_corpus_digest": self.canonical_corpus_digest,
            "documents": [row.to_dict() for row in self.documents],
        }


@dataclass(frozen=True)
class CanonicalInventory:
    state: CanonicalState
    document_count: int
    chunk_count: int
    retrieval_ready_chunk_count: int
    manifest_path: str
    manifest_sha256: str | None
    corpus_digest: str | None
    reasons: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @property
    def ready(self) -> bool:
        return self.state is CanonicalState.READY

    @property
    def retrieval_allowed(self) -> bool:
        return self.ready

    def to_dict(self) -> dict[str, Any]:
        return {
            "state": self.state.value,
            "document_count": self.document_count,
            "chunk_count": self.chunk_count,
            "retrieval_ready_chunk_count": self.retrieval_ready_chunk_count,
            "manifest_path": self.manifest_path,
            "manifest_sha256": self.manifest_sha256,
            "corpus_digest": self.corpus_digest,
            "reasons": list(self.reasons),
            "warnings": list(self.warnings),
            "ready": self.ready,
            "retrieval_allowed": self.retrieval_allowed,
        }


@dataclass(frozen=True)
class CanonicalSnapshot:
    inventory: CanonicalInventory
    manifest: CanonicalManifest


@dataclass(frozen=True)
class CanonicalPromotionAudit:
    payload: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return dict(self.payload)


def require_exact_keys(value: Any, expected: set[str], *, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", f"{label} must be an object")
    actual = set(value)
    if actual != expected:
        raise CanonicalError(
            "CANONICAL_MANIFEST_INVALID", f"{label} fields differ",
            details={"missing": sorted(expected - actual), "unknown": sorted(actual - expected)},
        )
    return value
