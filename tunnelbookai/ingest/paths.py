"""Path resolution for the Unified Ingest Engine.

Reads config/paths.json (the existing authoritative root map) and layers the ingest-specific
roots on top. Never hard-codes a user-absolute path (project-root contract, docs/architecture.md).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def relpath(path: Path, base: Path | None = None) -> str:
    """POSIX path relative to `base`, or the absolute path when outside it (e.g. tmp dirs in tests).

    `base` is read from the module global at CALL time rather than captured as a default, so
    an isolated run (tests, a relocated project root) resolves against the root in force.
    """
    base = base if base is not None else PROJECT_ROOT
    path = Path(path)
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _load_paths_json() -> dict[str, str]:
    data = json.loads((PROJECT_ROOT / "config" / "paths.json").read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if isinstance(v, str)}


@dataclass(frozen=True)
class IngestPaths:
    root: Path = PROJECT_ROOT

    @cached_property
    def _map(self) -> dict[str, str]:
        return _load_paths_json()

    def _p(self, key: str, default: str) -> Path:
        return self.root / self._map.get(key, default)

    # existing roots (from config/paths.json)
    @property
    def corpus_root(self) -> Path:
        return self._p("corpus_root", "corpus")

    @property
    def canonical_corpus_root(self) -> Path:
        return self._p("canonical_corpus_root", "corpus/canonical")

    @property
    def corpus_staging_root(self) -> Path:
        return self._p("corpus_staging_root", "corpus/staging")

    @property
    def corpus_metadata_root(self) -> Path:
        return self._p("corpus_metadata_root", "corpus/metadata")

    @property
    def handoff_root(self) -> Path:
        return self._p("handoff_root", "handoff")

    @property
    def audit_root(self) -> Path:
        return self._p("audit_root", "audit")

    @property
    def reports_root(self) -> Path:
        return self._p("reports_root", "reports")

    @property
    def book_root(self) -> Path:
        return self._p("book_root", "book")

    # ingest-specific roots
    @property
    def incoming_root(self) -> Path:
        return self.root / "incoming"

    @property
    def incoming_papercrawler_releases(self) -> Path:
        return self.root / "incoming" / "papercrawler" / "releases"

    @property
    def incoming_manual_inbox(self) -> Path:
        return self.root / "incoming" / "manual" / "inbox"

    @property
    def incoming_manual_root(self) -> Path:
        return self.root / "incoming" / "manual"

    @property
    def quarantine_root(self) -> Path:
        return self.root / "incoming" / "quarantine"

    @property
    def originals_root(self) -> Path:
        return self.root / "originals"

    @property
    def processing_root(self) -> Path:
        return self.root / "processing"

    @property
    def config_root(self) -> Path:
        return self.root / "config"

    # audit artifacts
    @property
    def ingest_state_path(self) -> Path:
        return self.audit_root / "ingest_state.jsonl"

    @property
    def ingest_manifest_path(self) -> Path:
        return self.audit_root / "ingest_manifest.jsonl"

    @property
    def source_registry_path(self) -> Path:
        return self.audit_root / "source_registry.jsonl"

    @property
    def document_id_map_path(self) -> Path:
        return self.audit_root / "document_id_map.jsonl"

    @property
    def unified_ingest_quality_path(self) -> Path:
        return self.audit_root / "unified_ingest_quality.json"

    def processing_bundle(self, document_id: str) -> Path:
        return self.processing_root / document_id

    def original_dir(self, document_id: str) -> Path:
        return self.originals_root / document_id


PATHS = IngestPaths()
