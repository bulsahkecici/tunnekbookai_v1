"""Empty-corpus readiness gate for TunnelBookAI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def _files(path: Path) -> list[Path]:
    return [p for p in path.rglob("*") if p.is_file() and p.name != ".gitkeep"] if path.is_dir() else []


def evaluate() -> dict[str, Any]:
    canonical = _files(ROOT / "corpus" / "canonical")
    staging = _files(ROOT / "corpus" / "staging")
    originals = _files(ROOT / "originals")
    processing = _files(ROOT / "processing")
    chunks = [p for p in processing if "/chunks/" in p.as_posix()]
    embeddings = _files(ROOT / "data" / "embeddings") + _files(ROOT / "data" / "embeddings_pilot")
    vectors = _files(ROOT / "data" / "qdrant_storage") + _files(ROOT / "data" / "qdrant_snapshots")
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
    }
    output = ROOT / "audit" / "empty_corpus_reset_gate.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False, indent=2))
