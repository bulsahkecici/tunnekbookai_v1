"""Strict identities and serialization helpers for Corpus Population V1."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "corpus-population-v1"


class PopulationState(StrEnum):
    INVENTORIED = "INVENTORIED"
    READY_TO_INGEST = "READY_TO_INGEST"
    INGESTING = "INGESTING"
    INGEST_ACCOUNTED = "INGEST_ACCOUNTED"
    STAGING_AUDITED = "STAGING_AUDITED"
    PROMOTION_PENDING_APPROVAL = "PROMOTION_PENDING_APPROVAL"
    PROMOTING = "PROMOTING"
    CANONICAL_READY = "CANONICAL_READY"
    BLOCKED = "BLOCKED"


class Disposition(StrEnum):
    PENDING = "PENDING"
    STAGED = "STAGED"
    ALREADY_PROCESSED = "ALREADY_PROCESSED"
    ALREADY_CANONICAL = "ALREADY_CANONICAL"
    DUPLICATE = "DUPLICATE"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    REJECTED = "REJECTED"
    UNSUPPORTED = "UNSUPPORTED"
    FAILED = "FAILED"
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def deterministic_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def identity(prefix: str, value: Any) -> str:
    return prefix + hashlib.sha256(deterministic_text(value).encode("utf-8")).hexdigest()


def atomic_json(path: Path, value: Any, *, readonly: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(deterministic_text(value))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        if readonly:
            path.chmod(0o444)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value
