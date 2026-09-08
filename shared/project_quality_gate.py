"""Empty-corpus readiness gate for TunnelBookAI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

SUPPORTED_SCRIPTS = {
    "ingest_incoming.py",
    "probe_models.py",
    "promote_staging.py",
    "reset_legacy_state.py",
}

LEGACY_ACTIVE_PATHS = (
    "crawler",
    "docs/legacy_tunnelbookai",
    "tunnelbookai_v1_book_inputs",
    "config/book_qa.yaml",
    "config/book_sections.json",
    "config/config.yaml",
    "config/metadata_llm.yaml",
    "config/metadata_llm_review.json",
    "data/academic",
    "data/corpus_final",
    "data/discovery",
    "data/institutional",
    "data/metadata",
    "data/news",
)

LEGACY_RUNTIME_MARKERS = (
    "data/markdown_full_docling",
    "data/corpus_final",
    "data/embeddings",
    "data/qdrant_storage",
    "data/qdrant_snapshots",
    "data/retrieval",
    "data/production",
    "incoming/" + "crawler/releases",
)


def _files(path: Path) -> list[Path]:
    return [p for p in path.rglob("*") if p.is_file() and p.name != ".gitkeep"] if path.is_dir() else []


def _active_legacy_references() -> list[str]:
    """Find pre-reset runtime references outside the explicit archive/history areas."""
    hits: list[str] = []
    roots = (ROOT / "scripts", ROOT / "tunnelbookai", ROOT / "config")
    old_model = "qwen3" + ".6-35b-a3b-mlx"
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            markers = [marker for marker in LEGACY_RUNTIME_MARKERS if marker in text]
            if old_model in text:
                markers.append(old_model)
            hits.extend(f"{path.relative_to(ROOT)}:{marker}" for marker in markers)
    return sorted(hits)


def evaluate() -> dict[str, Any]:
    canonical = _files(ROOT / "corpus" / "canonical")
    staging = _files(ROOT / "corpus" / "staging")
    originals = _files(ROOT / "originals")
    processing = _files(ROOT / "processing")
    chunks = [p for p in processing if "/chunks/" in p.as_posix()]
    embeddings = _files(ROOT / "data" / "embeddings") + _files(ROOT / "data" / "embeddings_pilot")
    vectors = _files(ROOT / "data" / "qdrant_storage") + _files(ROOT / "data" / "qdrant_snapshots")
    active_scripts = sorted(p.name for p in (ROOT / "scripts").glob("*.py"))
    legacy_active_paths = [path for path in LEGACY_ACTIVE_PATHS if (ROOT / path).exists()]
    legacy_references = _active_legacy_references()
    checks = {
        "canonical_documents": len(canonical) == 0,
        "staging_documents": len(staging) == 0,
        "original_documents": len(originals) == 0,
        "processed_documents": len(processing) == 0,
        "chunks": len(chunks) == 0,
        "embeddings": len(embeddings) == 0,
        "vectors": len(vectors) == 0,
        "legacy_crawler_removed": not (ROOT / "crawler").exists(),
        "papercrawler_input_ready": (ROOT / "incoming" / "papercrawler" / "releases").is_dir(),
        "manual_input_ready": (ROOT / "incoming" / "manual" / "inbox").is_dir(),
        "active_scripts_current": set(active_scripts) == SUPPORTED_SCRIPTS,
        "legacy_topology_isolated": not legacy_active_paths,
        "legacy_runtime_references_absent": not legacy_references,
    }
    result = {
        "decision": "GO" if all(checks.values()) else "NO_GO",
        "canonical_documents": len(canonical), "staging_documents": len(staging),
        "processed_documents": len(processing), "original_documents": len(originals),
        "chunks": len(chunks), "embeddings": len(embeddings), "vectors": len(vectors),
        "legacy_crawler_present": (ROOT / "crawler").exists(),
        "legacy_corpus_present": bool(canonical or staging or originals or processing),
        "legacy_vector_state_present": bool(embeddings or vectors),
        "papercrawler_input_ready": checks["papercrawler_input_ready"],
        "manual_input_ready": checks["manual_input_ready"], "checks": checks,
        "active_scripts": active_scripts,
        "legacy_active_paths": legacy_active_paths,
        "legacy_runtime_references": legacy_references,
    }
    output = ROOT / "audit" / "empty_corpus_reset_gate.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False, indent=2))
