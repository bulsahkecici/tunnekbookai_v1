"""Per-document ingest state machine with atomic persistence (task §54, §55, §56).

State is stored document-level in audit/ingest_state.jsonl (one JSON object per document,
rewritten atomically on every transition). Resume = skip documents already past a stage
unless --force-reprocess. Original archive is never rebuilt on reprocess.
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path


class State(str, Enum):
    DISCOVERED = "DISCOVERED"
    QUEUED = "QUEUED"
    ORIGINAL_ARCHIVED = "ORIGINAL_ARCHIVED"
    EXTRACTING = "EXTRACTING"
    EXTRACTED = "EXTRACTED"
    ASSETS_EXTRACTED = "ASSETS_EXTRACTED"
    OCR_COMPLETED = "OCR_COMPLETED"
    METADATA_COMPLETED = "METADATA_COMPLETED"
    DEDUP_COMPLETED = "DEDUP_COMPLETED"
    CLASSIFIED = "CLASSIFIED"
    QUALITY_GATED = "QUALITY_GATED"
    STAGED = "STAGED"
    CHUNKING = "CHUNKING"
    CHUNKED = "CHUNKED"
    CHUNK_QUALITY_GATED = "CHUNK_QUALITY_GATED"
    EMBEDDING_READY = "EMBEDDING_READY"
    REVIEW = "REVIEW"
    REJECTED = "REJECTED"
    DUPLICATE = "DUPLICATE"
    FAILED = "FAILED"
    ALREADY_PROCESSED = "ALREADY_PROCESSED"


# linear happy-path order for resume comparison
_ORDER = [
    State.DISCOVERED, State.QUEUED, State.ORIGINAL_ARCHIVED, State.EXTRACTING, State.EXTRACTED,
    State.ASSETS_EXTRACTED, State.OCR_COMPLETED, State.METADATA_COMPLETED, State.DEDUP_COMPLETED,
    State.CLASSIFIED, State.QUALITY_GATED, State.STAGED,
    State.CHUNKING, State.CHUNKED, State.CHUNK_QUALITY_GATED, State.EMBEDDING_READY,
]
# STAGED is no longer terminal: chunking continues past it (§65, §66). Resume compatibility
# is preserved because rank() still orders every pre-existing state identically.
_TERMINAL = {
    State.EMBEDDING_READY, State.REVIEW, State.REJECTED, State.DUPLICATE,
    State.ALREADY_PROCESSED,
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rank(state: State) -> int:
    try:
        return _ORDER.index(state)
    except ValueError:
        return -1


class IngestState:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._rows: dict[str, dict] = {}
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    row = json.loads(line)
                    self._rows[row["document_id"]] = row

    def get(self, document_id: str) -> dict | None:
        return self._rows.get(document_id)

    def state_of(self, document_id: str) -> State | None:
        row = self._rows.get(document_id)
        return State(row["state"]) if row else None

    def is_terminal(self, document_id: str) -> bool:
        s = self.state_of(document_id)
        return s in _TERMINAL if s else False

    def transition(self, document_id: str, state: State, *, source_kind: str | None = None,
                   sha256: str | None = None, detail: dict | None = None,
                   error: str | None = None, warnings: list[str] | None = None) -> dict:
        row = self._rows.setdefault(document_id, {
            "document_id": document_id, "history": [], "created_at": _now(),
        })
        if source_kind:
            row.setdefault("source_kinds", [])
            if source_kind not in row["source_kinds"]:
                row["source_kinds"].append(source_kind)
        if sha256:
            row["sha256"] = sha256
        row["state"] = state.value
        row["updated_at"] = _now()
        if error is not None:
            row["error"] = error
        if warnings:
            row.setdefault("warnings", [])
            row["warnings"] = sorted(set(row["warnings"]) | set(warnings))
        if detail:
            row.setdefault("detail", {}).update(detail)
        row["history"].append({"state": state.value, "at": row["updated_at"]})
        self._flush()
        return row

    def _flush(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(dir=str(self.path.parent), suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                for row in self._rows.values():
                    handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            os.replace(tmp_name, self.path)
        except BaseException:
            Path(tmp_name).unlink(missing_ok=True)
            raise

    def all_rows(self) -> list[dict]:
        return list(self._rows.values())
