"""Canonical TunnelBookAI V1 paths and legacy migration remapping."""

from __future__ import annotations

import os
from pathlib import Path

CRAWLER_SRC_ROOT = Path(__file__).resolve().parent
CRAWLER_ROOT = CRAWLER_SRC_ROOT.parent
PROJECT_ROOT = CRAWLER_ROOT.parent

CRAWLER_CONFIG_ROOT = CRAWLER_ROOT / "config"
CORPUS_ROOT = PROJECT_ROOT / "corpus"
CANONICAL_CORPUS_ROOT = CORPUS_ROOT / "canonical"
CORPUS_METADATA_ROOT = CORPUS_ROOT / "metadata"
CORPUS_SIDECARS_ROOT = CORPUS_ROOT / "sidecars"
DATA_ROOT = PROJECT_ROOT / "data"
DOWNLOADS_ROOT = DATA_ROOT / "downloads"
HANDOFF_ROOT = PROJECT_ROOT / "handoff"
BOOK_ROOT = PROJECT_ROOT / "book"
REPORTS_ROOT = PROJECT_ROOT / "reports"
AUDIT_ROOT = PROJECT_ROOT / "audit"

LEGACY_PATH_PREFIXES = {
    (PROJECT_ROOT.parent / "paper-crawler-agent" / "tunel_makaleleri").as_posix(): DOWNLOADS_ROOT,
    (PROJECT_ROOT.parent / "tunnel" / "_TunnelBookAI" / "data" / "corpus_final").as_posix(): CANONICAL_CORPUS_ROOT,
    (PROJECT_ROOT.parent / "tunnel" / "_TunnelBookAI" / "data" / "metadata").as_posix(): CORPUS_METADATA_ROOT,
    (PROJECT_ROOT.parent / "tunnel" / "_TunnelBookAI" / "data" / "temp" / "full_docling_chunks").as_posix(): CORPUS_SIDECARS_ROOT / "full_docling_chunks",
}


def crawler_output_root() -> Path:
    """Return the configured crawler staging root, defaulting inside this project."""
    return Path(os.getenv("TUNNEL_PAPERS_DIR", str(DOWNLOADS_ROOT))).expanduser().resolve()


def resolve_local_path(value: str | Path | None) -> Path | None:
    """Resolve an existing path, remapping recorded legacy roots after migration."""
    if value in (None, ""):
        return None
    candidate = Path(str(value)).expanduser()
    raw = candidate.as_posix()
    for legacy, replacement in LEGACY_PATH_PREFIXES.items():
        if raw == legacy or raw.startswith(legacy + "/"):
            relative = raw[len(legacy):].lstrip("/")
            migrated = replacement / relative
            return migrated.resolve()
    if candidate.exists():
        return candidate.resolve()
    return candidate.resolve()
