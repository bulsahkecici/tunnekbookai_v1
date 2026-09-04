"""Stable document identity (task §8).

Identity key = content SHA256. The engine-facing document_id is derived from it and is
stable and globally unique. A mapping file (audit/document_id_map.jsonl) links the identity
to any pre-existing ids the same physical file already has:

  - DOC######            legacy numeric id from scripts/01_inventory.py
  - CAN_/PC_ ids         crawler canonical/document ids
  - ingest document_id   ING_<first 20 hex of sha256>

The same SHA arriving from both the crawler and the manual inbox resolves to ONE document
with TWO provenance sources (see sources/ and audit/source_registry.jsonl).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

_ID_PREFIX = "ING_"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def document_id_for_sha256(sha256: str) -> str:
    if len(sha256) != 64 or not all(c in "0123456789abcdef" for c in sha256.lower()):
        raise ValueError(f"not a sha256 hex digest: {sha256!r}")
    return _ID_PREFIX + sha256.lower()[:20]


def document_id_for_file(path: Path) -> tuple[str, str]:
    sha = sha256_file(path)
    return document_id_for_sha256(sha), sha


class DocumentIdMap:
    """Append-only jsonl: {"document_id", "sha256", "aliases": {"legacy": [...], "crawler": [...]}}."""

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

    def register(self, document_id: str, sha256: str, alias_kind: str | None = None,
                 alias_value: str | None = None) -> dict:
        row = self._rows.setdefault(
            document_id, {"document_id": document_id, "sha256": sha256, "aliases": {}}
        )
        if alias_kind and alias_value:
            bucket = row["aliases"].setdefault(alias_kind, [])
            if alias_value not in bucket:
                bucket.append(alias_value)
        return row

    def flush(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            for row in self._rows.values():
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        tmp.replace(self.path)
