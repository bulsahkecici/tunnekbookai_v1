"""Deterministic JSON and identity helpers for canonical artifacts."""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any, Iterable

from .errors import CanonicalError


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise CanonicalError("INVALID_CANONICAL_JSON", str(exc)) from exc


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise CanonicalError("INVALID_CANONICAL_JSON", f"duplicate JSON key: {key}")
        out[key] = value
    return out


def _reject_constant(value: str) -> None:
    raise CanonicalError("INVALID_CANONICAL_JSON", f"invalid JSON number: {value}")


def loads_strict(text: str, *, code: str = "INVALID_CANONICAL_JSON") -> Any:
    try:
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_reject_constant)
    except CanonicalError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise CanonicalError(code, str(exc)) from exc
    return value


def load_json(path: Path, *, code: str = "INVALID_CANONICAL_JSON") -> Any:
    try:
        return loads_strict(path.read_text(encoding="utf-8"), code=code)
    except OSError as exc:
        raise CanonicalError(code, f"cannot read {path}: {exc}") from exc


def load_jsonl(path: Path, *, code: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise CanonicalError(code, f"cannot read {path}: {exc}") from exc
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        value = loads_strict(line, code=code)
        if not isinstance(value, dict):
            raise CanonicalError(code, f"{path}:{number} is not an object")
        rows.append(value)
    return rows


def semantic_file_sha256(path: Path) -> str:
    if path.suffix == ".json":
        return canonical_sha256(load_json(path))
    if path.suffix == ".jsonl":
        return canonical_sha256(load_jsonl(path, code="INVALID_CANONICAL_JSON"))
    return sha256_file(path)


def deterministic_json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def write_deterministic_json(path: Path, value: Any) -> None:
    payload = deterministic_json_text(value).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def write_identity_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        for row in rows:
            handle.write(canonical_json_bytes(row) + b"\n")
        handle.flush()
        os.fsync(handle.fileno())


def ensure_finite_numbers(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise CanonicalError("INVALID_CANONICAL_JSON", "non-finite number")
    if isinstance(value, dict):
        for child in value.values():
            ensure_finite_numbers(child)
    elif isinstance(value, list):
        for child in value:
            ensure_finite_numbers(child)
