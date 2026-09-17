"""Persistent control and status projection for the local dashboard."""

from __future__ import annotations

import os
import subprocess
import sys
import threading
from collections import Counter, deque
from pathlib import Path
from typing import Any

from tunnelbookai.ingest.paths import PROJECT_ROOT
from tunnelbookai.population.batching import _verify_run
from tunnelbookai.population.models import atomic_json, load_object, now

CONTROL_SCHEMA = "1.0"
ACTIVE_STATES = {"STARTING", "RUNNING", "STOP_REQUESTED"}


def dashboard_root(project_root: Path) -> Path:
    return project_root.resolve() / "audit" / "dashboard"


def resolve_run(value: str | Path | None, project_root: Path | str | None = None) -> Path:
    root = Path(project_root or PROJECT_ROOT).resolve()
    runs_root = (root / "audit" / "corpus_population" / "runs").resolve()
    if value is None:
        candidates = [path for path in runs_root.glob("CPR_*.json") if path.is_file()]
        if not candidates:
            raise ValueError("no corpus population run exists")
        path = max(candidates, key=lambda item: item.stat().st_mtime_ns)
    else:
        path = Path(value)
        path = path if path.is_absolute() else root / path
    if path.is_symlink() or not path.is_file() or path.resolve().parent != runs_root:
        raise ValueError("dashboard run must be a regular file in the population run root")
    payload = load_object(path)
    _verify_run(payload)
    return path.resolve()


def control_path(project_root: Path) -> Path:
    return dashboard_root(project_root) / "control.json"


def stop_path(project_root: Path) -> Path:
    return dashboard_root(project_root) / "stop.request"


def log_path(project_root: Path) -> Path:
    return dashboard_root(project_root) / "worker.log"


def pid_alive(pid: Any) -> bool:
    try:
        value = int(pid)
        if value <= 0:
            return False
        os.kill(value, 0)
        return True
    except (TypeError, ValueError, ProcessLookupError, PermissionError):
        return False


def initial_control(run_path: Path, project_root: Path) -> dict[str, Any]:
    project_root = project_root.resolve()
    run_path = run_path.resolve()
    return {
        "schema_version": CONTROL_SCHEMA,
        "run_path": run_path.relative_to(project_root).as_posix(),
        "status": "IDLE",
        "worker_pid": None,
        "current_batch_id": None,
        "current_document_id": None,
        "message": "İşlem başlatılmaya hazır.",
        "last_error": None,
        "started_at": None,
        "updated_at": now(),
    }


def load_control(run_path: Path, project_root: Path) -> dict[str, Any]:
    project_root = project_root.resolve()
    run_path = run_path.resolve()
    path = control_path(project_root)
    expected_run = run_path.relative_to(project_root).as_posix()
    if not path.is_file():
        value = initial_control(run_path, project_root)
        atomic_json(path, value)
        return value
    value = load_object(path)
    if value.get("schema_version") != CONTROL_SCHEMA or value.get("run_path") != expected_run:
        value = initial_control(run_path, project_root)
        atomic_json(path, value)
        return value
    if value.get("status") in ACTIVE_STATES and not pid_alive(value.get("worker_pid")):
        value.update({
            "status": "INTERRUPTED",
            "worker_pid": None,
            "current_batch_id": None,
            "current_document_id": None,
            "message": "Önceki worker kesildi; checkpoint üzerinden devam edilebilir.",
            "updated_at": now(),
        })
        atomic_json(path, value)
    return value


def update_control(project_root: Path, **changes: Any) -> dict[str, Any]:
    project_root = project_root.resolve()
    path = control_path(project_root)
    value = load_object(path)
    value.update(changes)
    value["updated_at"] = now()
    atomic_json(path, value)
    return value


def run_projection(run_path: Path, project_root: Path) -> dict[str, Any]:
    project_root = project_root.resolve()
    run_path = run_path.resolve()
    run = load_object(run_path)
    _verify_run(run)
    control = load_control(run_path, project_root)
    dispositions = Counter(
        str(row.get("disposition") or "PENDING") for row in run["documents"].values()
    )
    pending_states = {"PENDING", "RECOVERY_REQUIRED"}
    processed = sum(count for state, count in dispositions.items() if state not in pending_states)
    total = len(run["documents"])
    recent = []
    for document_id, row in reversed(list(run["documents"].items())):
        if str(row.get("disposition") or "PENDING") in pending_states:
            continue
        recent.append({
            "document_id": document_id,
            "disposition": row.get("disposition"),
            "section": row.get("final_primary_section"),
            "chunks": row.get("chunk_count", 0),
            "warnings": row.get("warnings", [])[:3],
        })
        if len(recent) == 12:
            break
    return {
        "control": control,
        "run": {
            "run_id": run["run_id"],
            "state": run["state"],
            "total_batches": len(run["batch_ids"]),
            "completed_batches": len(run["completed_batches"]),
            "failed_batches": len(run["failed_batches"]),
            "total_documents": total,
            "processed_documents": processed,
            "progress_percent": round((processed / total * 100.0) if total else 0.0, 2),
            "dispositions": dict(sorted(dispositions.items())),
            "recent_documents": recent,
        },
    }


def recent_logs(project_root: Path, limit: int = 120) -> list[str]:
    project_root = project_root.resolve()
    path = log_path(project_root)
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return list(deque((line.rstrip() for line in handle), maxlen=limit))


def start_worker(run_path: Path, project_root: Path) -> dict[str, Any]:
    project_root = project_root.resolve()
    run_path = run_path.resolve()
    current = load_control(run_path, project_root)
    if current.get("status") in ACTIVE_STATES and pid_alive(current.get("worker_pid")):
        raise RuntimeError("worker is already running")
    stop_path(project_root).unlink(missing_ok=True)
    root = dashboard_root(project_root)
    root.mkdir(parents=True, exist_ok=True)
    log_handle = log_path(project_root).open("a", encoding="utf-8")
    command = [
        sys.executable,
        "-m",
        "tunnelbookai.dashboard.worker",
        "--run",
        run_path.relative_to(project_root).as_posix(),
    ]
    process = subprocess.Popen(
        command,
        cwd=project_root,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    log_handle.close()
    value = update_control(
        project_root,
        status="STARTING",
        worker_pid=process.pid,
        current_batch_id=None,
        current_document_id=None,
        message="Worker başlatılıyor…",
        last_error=None,
        started_at=now(),
    )
    threading.Thread(target=process.wait, daemon=True).start()
    return value


def request_stop(run_path: Path, project_root: Path) -> dict[str, Any]:
    project_root = project_root.resolve()
    run_path = run_path.resolve()
    current = load_control(run_path, project_root)
    if current.get("status") not in ACTIVE_STATES or not pid_alive(current.get("worker_pid")):
        raise RuntimeError("running worker not found")
    path = stop_path(project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    return update_control(
        project_root,
        status="STOP_REQUESTED",
        message="Güvenli durdurma istendi; aktif belge checkpoint sonrası tamamlanacak.",
    )


__all__ = [
    "CONTROL_SCHEMA", "control_path", "dashboard_root", "initial_control", "load_control",
    "log_path", "pid_alive", "recent_logs", "request_stop", "resolve_run", "run_projection",
    "start_worker", "stop_path", "update_control",
]
