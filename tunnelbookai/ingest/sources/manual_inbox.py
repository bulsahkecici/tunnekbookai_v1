"""Manual / internal document inbox (task §6).

No handoff contract required. The engine derives SHA256, MIME, format, filename, size,
ingest timestamp and source_kind = MANUAL_INTERNAL. Provenance is never lost: the relative
inbox path and drop time are recorded.

Files are discovered only under incoming/manual/inbox/ recursively. README.md, Office
temporary files, dotfiles, hidden directory trees, and symlinks are ignored.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ..config import IngestConfig
from ..format_registry import detect
from ..paths import PATHS, relpath
from . import DiscoveredInput

SOURCE_KIND = "MANUAL_INTERNAL"
_IGNORE_NAMES = {"readme.md", ".gitkeep", ".ds_store"}


def _mtime_iso(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(timespec="seconds")


def discover(config: IngestConfig, manual_root: Path | None = None) -> list[DiscoveredInput]:
    root = manual_root or PATHS.incoming_manual_inbox
    if not root.is_dir():
        return []
    supported = config.supported_extensions | config.legacy_extensions
    found: list[DiscoveredInput] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if path.is_symlink() or not path.is_file():
            continue
        if (
            path.name.lower() in _IGNORE_NAMES
            or path.name.startswith("~$")
            or any(part.startswith(".") for part in relative.parts)
        ):
            continue
        rel = relpath(path)
        det = detect(path)
        ext = path.suffix.lower()
        notes: list[str] = []
        if ext not in supported and det.fmt.value == "UNKNOWN":
            notes.append("UNSUPPORTED_FORMAT")
        found.append(DiscoveredInput(
            input_path=path,
            source_kind=SOURCE_KIND,
            provenance={
                "source_kind": SOURCE_KIND,
                "inbox_relative_path": rel,
                "dropped_at": _mtime_iso(path),
                "original_filename": path.name,
                "detected_format": det.fmt.value,
                "mime_type": det.mime_type,
            },
            notes=notes,
        ))
    return found
