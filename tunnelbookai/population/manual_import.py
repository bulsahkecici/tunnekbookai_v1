"""Copy-only, exact-plan import of an external manual source archive."""

from __future__ import annotations

from collections import Counter
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from tunnelbookai.ingest.ids import sha256_file
from tunnelbookai.ingest.format_registry import detect, is_supported
from tunnelbookai.ingest.office_renderer import find_libreoffice
from tunnelbookai.ingest.paths import IngestPaths, PROJECT_ROOT

from .models import CONTRACT_VERSION, SCHEMA_VERSION, atomic_json, identity, load_object, now

_IGNORED = {".ds_store", ".gitkeep", "readme.md"}


def _has_symlink_component(path: Path, stop: Path) -> bool:
    current = path
    while current != stop and current != current.parent:
        if current.exists() and current.is_symlink():
            return True
        current = current.parent
    return False


def _scan(source_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    rows: list[dict[str, Any]] = []
    ignored: list[dict[str, str]] = []
    for path in sorted(source_root.rglob("*")):
        relative = path.relative_to(source_root)
        rel = relative.as_posix()
        if path.is_symlink():
            ignored.append({"path": rel, "reason": "SYMLINK"})
            continue
        if any(part.startswith(".") for part in relative.parts):
            if path.is_file():
                ignored.append({"path": rel, "reason": "HIDDEN"})
            continue
        if not path.is_file():
            continue
        if path.name.lower() in _IGNORED:
            ignored.append({"path": rel, "reason": "IGNORED_NAME"})
            continue
        if path.name.startswith("~$"):
            ignored.append({"path": rel, "reason": "OFFICE_TEMPORARY"})
            continue
        rows.append({"path": rel, "size": path.stat().st_size, "sha256": sha256_file(path)})
    return rows, ignored


def build_import_plan(
    source_root: Path | str, project_root: Path | str | None = None, *, write: bool = True,
) -> dict[str, Any]:
    root = Path(project_root or PROJECT_ROOT).resolve()
    supplied_source = Path(source_root).expanduser()
    if supplied_source.is_symlink():
        raise ValueError("manual import source must not be a symlink")
    source = supplied_source.resolve()
    if not source.is_dir():
        raise ValueError("manual import source must be a real directory")
    inbox = IngestPaths(root).incoming_manual_inbox.resolve()
    if source == inbox or inbox in source.parents or source in inbox.parents:
        raise ValueError("manual import source and inbox must be separate trees")
    sources, ignored = _scan(source)
    records = []
    libreoffice_available = find_libreoffice() is not None
    for row in sources:
        detection = detect(source / row["path"])
        destination = inbox / row["path"]
        action = "COPY"
        if _has_symlink_component(destination, inbox):
            action = "PATH_COLLISION"
        elif destination.exists():
            if destination.is_symlink() or not destination.is_file():
                action = "PATH_COLLISION"
            elif destination.stat().st_size == row["size"] and sha256_file(destination) == row["sha256"]:
                action = "IDEMPOTENT_NO_CHANGE"
            else:
                action = "PATH_COLLISION"
        records.append({
            **row,
            "format": detection.fmt.value,
            "supported": is_supported(
                detection, libreoffice_available=libreoffice_available
            ),
            "action": action,
        })
    sha_counts = Counter(row["sha256"] for row in records)
    exact_sha_groups = [
        {
            "sha256": sha,
            "paths": sorted(row["path"] for row in records if row["sha256"] == sha),
        }
        for sha, count in sorted(sha_counts.items()) if count > 1
    ]
    semantic = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "kind": "MANUAL_IMPORT",
        "records": records,
        "ignored": ignored,
        "exact_sha_groups": exact_sha_groups,
    }
    plan_id = identity("CMI_", semantic)
    payload = {
        "plan_id": plan_id,
        **semantic,
        "applicable": not any(row["action"] == "PATH_COLLISION" for row in records),
        "generated_at": now(),
        "summary": {
            "copy": sum(row["action"] == "COPY" for row in records),
            "idempotent": sum(row["action"] == "IDEMPOTENT_NO_CHANGE" for row in records),
            "collisions": sum(row["action"] == "PATH_COLLISION" for row in records),
            "ignored": len(ignored),
            "supported": sum(bool(row["supported"]) for row in records),
            "unsupported": sum(not bool(row["supported"]) for row in records),
            "bytes_to_copy": sum(row["size"] for row in records if row["action"] == "COPY"),
        },
    }
    if write:
        path = root / "audit" / "corpus_population" / "manual_imports" / f"{plan_id}.json"
        if not path.exists():
            atomic_json(path, payload, readonly=True)
        payload["plan_path"] = path.relative_to(root).as_posix()
    return payload


def apply_import_plan(
    source_root: Path | str, plan_path: Path | str, *, approve: str | None,
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    root = Path(project_root or PROJECT_ROOT).resolve()
    supplied_source = Path(source_root).expanduser()
    if supplied_source.is_symlink():
        raise ValueError("manual import source must not be a symlink")
    source = supplied_source.resolve()
    path = Path(plan_path)
    path = path if path.is_absolute() else root / path
    plans = (root / "audit" / "corpus_population" / "manual_imports").resolve()
    if path.resolve().parent != plans or path.is_symlink() or not path.is_file():
        raise ValueError("manual import plan must be a regular file in the import-plan root")
    stored = load_object(path)
    plan_id = str(stored.get("plan_id") or "")
    if approve != plan_id:
        raise ValueError("manual import requires --approve with the exact plan ID")
    current = build_import_plan(source, root, write=False)
    for value in (stored, current):
        value.pop("generated_at", None)
        value.pop("plan_path", None)
    if stored != current:
        raise ValueError("manual import plan is stale")
    if not current["applicable"]:
        raise ValueError("manual import plan contains path collisions")

    inbox = IngestPaths(root).incoming_manual_inbox
    inbox.mkdir(parents=True, exist_ok=True)
    transaction = Path(tempfile.mkdtemp(prefix=f".manual-import-{plan_id}-", dir=inbox.parent))
    added: list[Path] = []
    try:
        for row in current["records"]:
            if row["action"] != "COPY":
                continue
            src = source / row["path"]
            if src.is_symlink() or not src.is_file() or src.stat().st_size != row["size"] or sha256_file(src) != row["sha256"]:
                raise ValueError(f"manual import source changed: {row['path']}")
            temporary = transaction / row["path"]
            temporary.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, temporary)
            if temporary.stat().st_size != row["size"] or sha256_file(temporary) != row["sha256"]:
                raise ValueError(f"manual import copy verification failed: {row['path']}")
        for row in current["records"]:
            if row["action"] != "COPY":
                continue
            destination = inbox / row["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                raise ValueError(f"manual import destination appeared during apply: {row['path']}")
            os.replace(transaction / row["path"], destination)
            added.append(destination)
        result = {
            "status": "APPLIED",
            "plan_id": plan_id,
            "copied": len(added),
            "idempotent": current["summary"]["idempotent"],
            "finished_at": now(),
        }
        audit = root / "audit" / "corpus_population" / "manual_import_applies" / f"{plan_id}.json"
        atomic_json(audit, result, readonly=True)
        result["audit_path"] = audit.relative_to(root).as_posix()
        return result
    except BaseException:
        for destination in reversed(added):
            destination.unlink(missing_ok=True)
        raise
    finally:
        shutil.rmtree(transaction, ignore_errors=True)


__all__ = ["apply_import_plan", "build_import_plan"]
