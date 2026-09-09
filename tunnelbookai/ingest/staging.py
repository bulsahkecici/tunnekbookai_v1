"""Staging for quality-approved documents (task §33, §46).

The unified engine writes approved candidates to a versioned subtree:

    corpus/staging/v2/<document_id>/
        bundle.json           the authoritative manifest for this staged document
        metadata.json         copy of processing/<id>/metadata.json
        classification.json   copy of processing/<id>/classification.json
        quality_gate.json     copy of processing/<id>/quality_gate.json
        provenance.json       copy of processing/<id>/provenance.json
        document.md           copy of the normalized markdown (retrieval representation)
        chunks -> reference   chunks stay authoritative in processing/<id>/chunks/ (§49)

Copies (not moves) — the processing bundle stays intact. Canonical promotion never happens
here (§46, §47).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .chunking.chunker import CHUNKS_DIRNAME, MANIFEST_NAME
from .paths import PATHS, relpath

STAGING_VERSION = "v2"
BUNDLE_SHAPE = "unified_ingest_v1"

STAGING_COPY_FILES = ("metadata.json", "metadata_provenance.json", "classification.json",
                      "quality_gate.json", "provenance.json", "extraction_report.json",
                      "chunk_quality.json")
# Compatibility for older callers; canonical promotion imports the public name above.
_COPY_FILES = STAGING_COPY_FILES


def staging_root() -> Path:
    return PATHS.corpus_staging_root / STAGING_VERSION


def staging_dir(document_id: str) -> Path:
    return staging_root() / document_id


def stage_document(
    *,
    document_id: str,
    bundle: Path,
    metadata: dict[str, Any],
    classification: dict[str, Any],
    gate: dict[str, Any],
    evidence_level: str,
    chunk_count: int,
    chunk_quality_status: str | None,
) -> tuple[Path, list[str]]:
    """Materialize the staging bundle. Returns (path, warnings). Never writes canonical."""
    warnings: list[str] = []
    target = staging_dir(document_id)
    target.mkdir(parents=True, exist_ok=True)

    for name in STAGING_COPY_FILES:
        source = bundle / name
        if source.is_file():
            shutil.copy2(source, target / name)

    normalized_md = bundle / "normalized" / "document.md"
    if normalized_md.is_file():
        shutil.copy2(normalized_md, target / "document.md")
    else:
        warnings.append("STAGING_NO_NORMALIZED_MARKDOWN")

    chunk_manifest = bundle / CHUNKS_DIRNAME / MANIFEST_NAME
    bundle_doc = {
        "bundle_shape": BUNDLE_SHAPE,
        "staging_version": STAGING_VERSION,
        "document_id": document_id,
        "original_sha256": metadata.get("original_sha256"),
        "source_kind": metadata.get("source_kind"),
        "format": metadata.get("format"),
        "title": metadata.get("title"),
        "final_primary_section": classification.get("final_primary_section"),
        "final_secondary_sections": classification.get("final_secondary_sections", []),
        "final_section_confidence": classification.get("final_section_confidence"),
        "final_evidence_level": evidence_level,
        "content_capabilities": metadata.get("content_capabilities", {}),
        "quality_decision": gate.get("decision"),
        "processing_bundle": relpath(bundle),
        "original_archive": relpath(PATHS.original_dir(document_id)),
        # chunks stay authoritative in processing/<id>/chunks/ — staging only references them
        "chunks_authoritative_path": relpath(chunk_manifest) if chunk_manifest.is_file() else None,
        "chunk_count": chunk_count,
        "chunk_quality_status": chunk_quality_status,
        "canonical_promoted": False,
    }
    (target / "bundle.json").write_text(
        json.dumps(bundle_doc, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return target, warnings


def legacy_bundles() -> list[str]:
    """Names of the pre-existing flat staging bundles, which must never be modified (§33)."""
    root = PATHS.corpus_staging_root
    if not root.is_dir():
        return []
    return sorted(p.name for p in root.iterdir()
                  if p.is_dir() and p.name != STAGING_VERSION)
