"""Configured roots and strict path-boundary checks for canonical promotion."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from tunnelbookai.book.inputs import BookInputs, load_book_inputs
from tunnelbookai.ingest.paths import IngestPaths

from .errors import CanonicalError


DOCUMENT_ID_RE = re.compile(r"^ING_[0-9a-f]{20}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class CanonicalContext:
    root: Path
    paths: IngestPaths
    book_inputs: BookInputs
    canonical_root: Path
    manifest_path: Path
    audit_root: Path

    @classmethod
    def load(cls, project_root: Path | str | None = None, *, book_inputs: BookInputs | None = None) -> "CanonicalContext":
        root = Path(
            project_root or (book_inputs.contract.project_root if book_inputs else Path(__file__).resolve().parents[2])
        ).resolve()
        inputs = book_inputs or load_book_inputs(root)
        paths = IngestPaths(root)
        evidence = inputs.contract.payload["evidence_policy"]
        canonical = (root / str(evidence["canonical_root"])).resolve()
        manifest = (root / str(evidence["canonical_manifest"])).resolve()
        if canonical != paths.canonical_corpus_root.resolve() or manifest.parent != canonical:
            raise CanonicalError(
                "CANONICAL_CONFIGURATION_MISMATCH",
                "Book Contract and config/paths.json disagree on canonical authority",
            )
        return cls(root, paths, inputs, canonical, manifest, paths.audit_root / "canonical_promotions")

    def relative(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError as exc:
            raise CanonicalError("CANONICAL_PATH_ESCAPE", f"path escapes project: {path}") from exc


def validate_document_id(document_id: str) -> str:
    if not DOCUMENT_ID_RE.fullmatch(document_id):
        raise CanonicalError("INVALID_STAGING_BUNDLE", f"invalid document_id: {document_id}")
    return document_id


def validate_sha256(value: str, *, code: str = "SOURCE_SHA_MISMATCH") -> str:
    if not SHA256_RE.fullmatch(value):
        raise CanonicalError(code, f"invalid SHA-256: {value!r}")
    return value


def resolve_declared(context: CanonicalContext, value: object, *, root: Path, code: str) -> Path:
    relative = Path(str(value or ""))
    if not str(value or "").strip() or relative.is_absolute() or ".." in relative.parts:
        raise CanonicalError("CANONICAL_PATH_ESCAPE", f"unsafe declared path: {value!r}")
    candidate = context.root / relative
    resolved_root = root.resolve()
    resolved = candidate.resolve()
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise CanonicalError("CANONICAL_PATH_ESCAPE", f"path escapes {root}: {value}")
    _reject_symlink_chain(candidate, context.root)
    return resolved


def _reject_symlink_chain(path: Path, stop: Path) -> None:
    current = path
    stop = stop.resolve()
    while current != stop and current != current.parent:
        if current.exists() and current.is_symlink():
            raise CanonicalError("CANONICAL_PATH_ESCAPE", f"symlink is not allowed: {current}")
        current = current.parent


def require_regular(path: Path, *, code: str) -> Path:
    if not path.is_file() or path.is_symlink():
        raise CanonicalError(code, f"required regular file is missing: {path}")
    return path
