"""Original preservation (task §7).

The first real operation on any incoming file is: SHA256 -> immutable archive.

  originals/<document_id>/
      source.<ext>       (byte-identical copy; read-only permissions)
      original.json       (document_id, original_filename, original_sha256, source_kind,
                           received_at, file_size, mime_type)

The original is never modified, renamed, re-converted or overwritten. Reprocessing reuses
the existing archive; a SHA mismatch on an existing archive is a hard error.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
from datetime import datetime, timezone
from pathlib import Path

from .format_registry import detect
from .ids import document_id_for_file, sha256_file
from .paths import PATHS, relpath


class ArchiveConflict(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _make_readonly(path: Path) -> None:
    try:
        path.chmod(path.stat().st_mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
    except OSError:
        pass


def archive_original(src: Path, *, source_kind: str, received_at: str | None = None,
                     originals_root: Path | None = None) -> dict:
    """Copy `src` into the immutable originals archive. Idempotent by content SHA256."""
    src = Path(src)
    if not src.is_file():
        raise FileNotFoundError(src)

    document_id, sha = document_id_for_file(src)
    det = detect(src)
    root = originals_root or PATHS.originals_root
    dest_dir = root / document_id
    ext = src.suffix.lower() or ""
    dest = dest_dir / f"source{ext}"

    if dest.exists():
        existing_sha = sha256_file(dest)
        if existing_sha != sha:
            raise ArchiveConflict(
                f"{dest} exists with sha256 {existing_sha} but incoming file is {sha}"
            )
        mode = "existing"
    else:
        dest_dir.mkdir(parents=True, exist_ok=True)
        tmp = dest_dir / (dest.name + ".tmp")
        shutil.copy2(src, tmp)
        os.replace(tmp, dest)
        _make_readonly(dest)
        mode = "copied"

    meta = {
        "document_id": document_id,
        "original_filename": src.name,
        "original_sha256": sha,
        "source_kind": source_kind,
        "received_at": received_at or _now(),
        "file_size": src.stat().st_size,
        "mime_type": det.mime_type,
        "format": det.fmt.value,
        "is_legacy_format": det.is_legacy,
        "archive_mode": mode,
        "archive_path": relpath(dest),
    }
    meta_path = dest_dir / "original.json"
    prev = None
    if meta_path.exists():
        prev = json.loads(meta_path.read_text(encoding="utf-8"))
        # preserve the earliest received_at; record every distinct source_kind
        meta["received_at"] = prev.get("received_at", meta["received_at"])
        kinds = set(prev.get("source_kinds", [prev.get("source_kind")])) | {source_kind}
        meta["source_kinds"] = sorted(k for k in kinds if k)
    else:
        meta["source_kinds"] = [source_kind]
    # A reprocess of an already-archived document must leave this sidecar's bytes
    # untouched when nothing actually changed: canonical promotion pins its SHA256,
    # and a gratuitous rewrite (even byte-identical in substance) breaks that fingerprint.
    # `archive_mode` describes this call's own outcome ("copied" vs "existing"), not a
    # property of the document, so it never by itself justifies a rewrite.
    if prev is None or prev != {**meta, "archive_mode": prev.get("archive_mode")}:
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta
