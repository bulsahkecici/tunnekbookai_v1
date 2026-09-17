"""Targeted, auditable quality improvements driven by persisted warning codes.

Only derived chunk artifacts are changed automatically.  Originals, extracted text,
manual classification decisions and review decisions remain untouched.  Visual warnings
are reported as deferred because retrying the same extractor is not an improvement.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

from tunnelbookai.ingest.chunking import manifest as manifest_module
from tunnelbookai.ingest.chunking import quality as quality_module
from tunnelbookai.ingest.chunking import tokenizer
from tunnelbookai.ingest.chunking.chunker import (
    merge_short_text_chunks,
    read_chunks,
    split_chunks_to_soft_max,
)
from tunnelbookai.ingest.chunking.policy import ChunkPolicy, chunk_id, normalize_for_id
from tunnelbookai.ingest.config import load_config
from tunnelbookai.population.models import atomic_json, load_object, now


SCHEMA_VERSION = "1.0"
ACTIVE = {"STARTING", "RUNNING"}
AUTO_CODES = {"CHUNK_UNDER_MIN", "CHUNK_OVER_MAX"}
DEFERRED_CODES = {
    "EMBEDDED_MEDIA_VECTOR_SKIPPED",
    "FIGURE_IMAGE_UNAVAILABLE",
    "OFFICE_RENDER_NO_OUTPUT",
    "PPTX_SHAPE_FAILED",
    "PPTX_VECTOR_MEDIA_SKIPPED",
}


def _code(value: Any) -> str:
    return str(value).split(":", 1)[0]


def state_path(project_root: Path) -> Path:
    return project_root.resolve() / "audit" / "dashboard" / "improvements.json"


def log_path(project_root: Path) -> Path:
    return project_root.resolve() / "audit" / "dashboard" / "improvements.log"


def _pid_alive(pid: Any) -> bool:
    try:
        value = int(pid)
        if value <= 0:
            return False
        os.kill(value, 0)
        return True
    except (TypeError, ValueError, ProcessLookupError, PermissionError):
        return False


def _warning_codes(project_root: Path, document_id: str, row: dict[str, Any]) -> set[str]:
    values = list(row.get("warnings") or [])
    for name in ("extraction_report.json", "quality_gate.json", "chunk_quality.json"):
        path = project_root / "processing" / document_id / name
        if not path.is_file():
            continue
        payload = load_object(path)
        values.extend(payload.get("warnings") or [])
        values.extend(payload.get("review_reasons") or [])
    return {_code(value) for value in values}


def build_state(run_path: Path, project_root: Path) -> dict[str, Any]:
    project_root = project_root.resolve()
    run_path = run_path.resolve()
    run = load_object(run_path)
    candidates: list[dict[str, Any]] = []
    deferred = Counter()
    for document_id, row in run.get("documents", {}).items():
        codes = _warning_codes(project_root, document_id, row)
        auto = sorted(codes & AUTO_CODES)
        if auto and (project_root / "processing" / document_id / "chunks" / "chunk_manifest.jsonl").is_file():
            candidates.append({
                "document_id": document_id,
                "status": "PENDING",
                "action": "RECHUNK" if "CHUNK_OVER_MAX" in auto else "REVALIDATE",
                "warning_codes": auto,
                "before_chunk_count": int(row.get("chunk_count") or 0),
            })
        for code in codes & DEFERRED_CODES:
            deferred[code] += 1
    state = {
        "schema_version": SCHEMA_VERSION,
        "run_path": run_path.relative_to(project_root).as_posix(),
        "status": "READY",
        "worker_pid": None,
        "message": "Hedefli chunk iyileştirmesi başlatılmaya hazır.",
        "created_at": now(),
        "updated_at": now(),
        "started_at": None,
        "finished_at": None,
        "current_document_id": None,
        "total_candidates": len(candidates),
        "processed": 0,
        "improved": 0,
        "unchanged": 0,
        "failed": 0,
        "before": dict(sorted(Counter(
            code for item in candidates for code in item["warning_codes"]
        ).items())),
        "after": {},
        "deferred": dict(sorted(deferred.items())),
        "candidates": candidates,
        "recent": [],
        "backup_root": None,
        "staging_audit_id": None,
        "readiness_audit_id": None,
        "last_error": None,
    }
    atomic_json(state_path(project_root), state)
    return state


def load_state(run_path: Path, project_root: Path) -> dict[str, Any]:
    path = state_path(project_root)
    expected = run_path.resolve().relative_to(project_root.resolve()).as_posix()
    if not path.is_file():
        return build_state(run_path, project_root)
    state = load_object(path)
    if state.get("schema_version") != SCHEMA_VERSION or state.get("run_path") != expected:
        return build_state(run_path, project_root)
    if state.get("status") in ACTIVE and not _pid_alive(state.get("worker_pid")):
        state.update({
            "status": "INTERRUPTED",
            "worker_pid": None,
            "current_document_id": None,
            "message": "İyileştirme worker’ı kesildi; tamamlanan dosyalar korunuyor.",
            "updated_at": now(),
        })
        atomic_json(path, state)
    return state


def start_worker(run_path: Path, project_root: Path) -> dict[str, Any]:
    project_root = project_root.resolve()
    state = load_state(run_path, project_root)
    if state.get("status") in ACTIVE and _pid_alive(state.get("worker_pid")):
        raise RuntimeError("improvement worker is already running")
    if state.get("status") == "FINISHED":
        return state
    elif state.get("status") in {"FINISHED_WITH_FAILURES", "ERROR", "INTERRUPTED"}:
        retry = [item for item in state.get("candidates", []) if item.get("status") == "FAILED"]
        for item in retry:
            item["status"] = "PENDING"
            item.pop("error", None)
        state["processed"] = max(0, int(state.get("processed") or 0) - len(retry))
        state["failed"] = 0
    pending = [item for item in state.get("candidates", []) if item.get("status") == "PENDING"]
    if not pending:
        state["status"] = "FINISHED"
        state["message"] = "İyileştirilecek chunk adayı kalmadı."
        state["updated_at"] = now()
        atomic_json(state_path(project_root), state)
        return state
    log_path(project_root).parent.mkdir(parents=True, exist_ok=True)
    handle = log_path(project_root).open("a", encoding="utf-8")
    process = subprocess.Popen(
        [sys.executable, "-m", "tunnelbookai.dashboard.improvement_worker",
         "--run", run_path.resolve().relative_to(project_root).as_posix()],
        cwd=project_root,
        stdout=handle,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    handle.close()
    state.update({
        "status": "STARTING",
        "worker_pid": process.pid,
        "started_at": now(),
        "finished_at": None,
        "message": "Hedefli iyileştirme worker’ı başlatılıyor…",
        "updated_at": now(),
        "last_error": None,
    })
    atomic_json(state_path(project_root), state)
    return state


def queue_identity_repairs(
    run_path: Path, project_root: Path, document_ids: list[str]
) -> dict[str, Any]:
    """Queue a bounded retry for documents rejected only by chunk identity validation."""
    project_root = project_root.resolve()
    state = load_state(run_path, project_root)
    unique = sorted(set(document_ids))
    state.update({
        "status": "READY",
        "worker_pid": None,
        "message": "Canonical kimlik doğrulaması için sınırlı onarım hazır.",
        "total_candidates": len(unique),
        "processed": 0,
        "improved": 0,
        "unchanged": 0,
        "failed": 0,
        "before": {"CHUNK_ID_INTEGRITY": len(unique)},
        "after": {},
        "candidates": [{
            "document_id": document_id,
            "status": "PENDING",
            "action": "IDENTITY_REPAIR",
            "warning_codes": ["CHUNK_ID_INTEGRITY"],
            "before_chunk_count": 0,
        } for document_id in unique],
        "recent": [],
        "updated_at": now(),
        "last_error": None,
    })
    atomic_json(state_path(project_root), state)
    return state


def _atomic_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _migrate_and_split(chunks: list[dict[str, Any]], policy: ChunkPolicy) -> list[dict[str, Any]]:
    migrated: list[dict[str, Any]] = []
    for original in chunks:
        chunk = dict(original)
        chunk["chunk_schema_version"] = policy.schema_version
        chunk["chunk_policy_version"] = policy.policy_version
        chunk["tokenizer"] = policy.tokenizer_name
        chunk["token_count"] = tokenizer.count(str(chunk.get("text") or ""))
        chunk["chunk_id"] = chunk_id(
            str(chunk.get("document_id") or ""),
            str(chunk.get("chunk_type") or ""),
            list(chunk.get("source_elements") or []),
            str(chunk.get("text") or ""),
            policy,
            chunk.get("chunk_identity_part"),
        )
        migrated.append(chunk)
    # Existing manifests have already passed deduplication.  Re-deduplicating after
    # migration could incorrectly compare two newly split sibling parts.
    split = split_chunks_to_soft_max(migrated, policy)
    split = merge_short_text_chunks(split, policy)
    for ordinal, chunk in enumerate(split, start=1):
        chunk["ordinal"] = ordinal
    return split


def _copy_backup(source: Path, destination: Path) -> None:
    if source.is_file():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def consolidate_completed_state(
    state: dict[str, Any], project_root: Path, run: dict[str, Any]
) -> dict[str, Any]:
    """Project all completed passes as one dashboard result."""
    backups_root = project_root / "audit" / "dashboard" / "improvement_backups"
    earliest: dict[str, Path] = {}
    if backups_root.is_dir():
        for pass_root in sorted(path for path in backups_root.iterdir() if path.is_dir()):
            for document_root in sorted(path for path in pass_root.iterdir() if path.is_dir()):
                quality = document_root / "chunk_quality.json"
                if quality.is_file():
                    earliest.setdefault(document_root.name, quality)
    if not earliest:
        return state
    before = Counter()
    after = Counter()
    for document_id, quality_path in earliest.items():
        old_codes = {_code(value) for value in load_object(quality_path).get("warnings") or []}
        for code in old_codes & AUTO_CODES:
            before[code] += 1
        current_path = project_root / "processing" / document_id / "chunk_quality.json"
        current_codes = {
            _code(value) for value in load_object(current_path).get("warnings") or []
        }
        for code in current_codes & (AUTO_CODES | {"CHUNK_SHORT_STRUCTURAL"}):
            after[code] += 1
    deferred = Counter()
    for document_id, row in run.get("documents", {}).items():
        for code in _warning_codes(project_root, document_id, row) & DEFERRED_CODES:
            deferred[code] += 1
    state.update({
        "total_candidates": len(earliest),
        "processed": len(earliest),
        "improved": len(earliest),
        "unchanged": 0,
        "failed": 0,
        "before": dict(sorted(before.items())),
        "after": dict(sorted(after.items())),
        "deferred": dict(sorted(deferred.items())),
        "backup_root": backups_root.relative_to(project_root).as_posix(),
        "message": (
            f"İyileştirme tamamlandı: {len(earliest)} belge güncellendi, 0 başarısız. "
            "Metin kapsamı korundu; görsel adaylar güvenli yeniden işleme için ertelendi."
        ),
    })
    return state


def _improve_one(
    project_root: Path,
    run: dict[str, Any],
    document_id: str,
    policy: ChunkPolicy,
    backup_root: Path,
) -> dict[str, Any]:
    bundle = project_root / "processing" / document_id
    old_chunks = read_chunks(bundle)
    if not old_chunks:
        raise RuntimeError("chunk manifest is empty")
    trusted_refs = {
        str(ref) for chunk in old_chunks for ref in (chunk.get("source_elements") or []) if ref
    }
    new_chunks = _migrate_and_split(old_chunks, policy)
    old_coverage = normalize_for_id("\n".join(str(chunk.get("text") or "") for chunk in old_chunks))
    new_coverage = normalize_for_id("\n".join(str(chunk.get("text") or "") for chunk in new_chunks))
    if new_coverage != old_coverage:
        raise RuntimeError("normalized text coverage changed during chunk-only remediation")
    report = quality_module.evaluate(
        document_id=document_id,
        chunks=new_chunks,
        elements=[], tables=[], figures=[], sheets=[], slides=[],
        policy=policy,
        trusted_source_refs=trusted_refs,
    )
    if report["errors"]:
        raise RuntimeError("new chunk quality failed: " + "; ".join(report["errors"][:3]))

    old_ready_path = bundle / "chunks" / "embedding_ready.jsonl"
    old_ready = [
        json.loads(line) for line in old_ready_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ] if old_ready_path.is_file() else []
    old_eligible = sum(row.get("eligible") is True for row in old_ready)
    staging = project_root / "corpus" / "staging" / "v2" / document_id
    staged = staging.is_dir()
    # Some historical ALREADY_PROCESSED rows have no staging copy but already carry
    # eligible retrieval rows.  A chunk-only migration must preserve that established
    # eligibility instead of interpreting the absent convenience copy as a downgrade.
    ready_rows = manifest_module.build_rows(
        new_chunks, policy, document_staged=(staged or old_eligible > 0),
        chunk_quality_ok=True,
    )
    new_eligible = sum(row.get("eligible") is True for row in ready_rows)
    if old_eligible > 0 and new_eligible < 1:
        raise RuntimeError("all retrieval-ready chunks would become ineligible")

    backup = backup_root / document_id
    _copy_backup(bundle / "chunks" / "chunk_manifest.jsonl", backup / "chunk_manifest.jsonl")
    _copy_backup(old_ready_path, backup / "embedding_ready.jsonl")
    _copy_backup(bundle / "chunk_quality.json", backup / "chunk_quality.json")
    _copy_backup(staging / "bundle.json", backup / "staging_bundle.json")
    _copy_backup(staging / "chunk_quality.json", backup / "staging_chunk_quality.json")

    _atomic_jsonl(bundle / "chunks" / "chunk_manifest.jsonl", new_chunks)
    _atomic_jsonl(old_ready_path, ready_rows)
    atomic_json(bundle / "chunk_quality.json", report)
    if staged:
        atomic_json(staging / "chunk_quality.json", report)
        staged_bundle = load_object(staging / "bundle.json")
        staged_bundle["chunk_count"] = len(new_chunks)
        staged_bundle["chunk_quality_status"] = report["status"]
        atomic_json(staging / "bundle.json", staged_bundle)

    row = run["documents"][document_id]
    preserved = [
        value for value in (row.get("warnings") or [])
        if _code(value) not in AUTO_CODES | {"CHUNK_SHORT_STRUCTURAL"}
    ]
    row["warnings"] = preserved + list(report.get("warnings") or [])[:20]
    row["chunk_count"] = len(new_chunks)
    row["chunk_quality_status"] = report["status"]
    row["embedding_ready_chunks"] = new_eligible
    before_over = sum(int(chunk.get("token_count") or 0) > policy.max_tokens for chunk in old_chunks)
    after_over = sum(int(chunk.get("token_count") or 0) > policy.max_tokens for chunk in new_chunks)
    return {
        "document_id": document_id,
        "status": "IMPROVED" if before_over or old_chunks != new_chunks else "UNCHANGED",
        "before_chunks": len(old_chunks),
        "after_chunks": len(new_chunks),
        "before_over_max": before_over,
        "after_over_max": after_over,
        "retrieval_ready": new_eligible,
        "before_retrieval_ready": old_eligible,
        "warnings": list(report.get("warnings") or []),
    }


def execute(run_value: str, project_root: Path) -> int:
    project_root = project_root.resolve()
    run_path = (project_root / run_value).resolve()
    state = load_state(run_path, project_root)
    state.update({"status": "RUNNING", "message": "Chunk adayları iyileştiriliyor.", "updated_at": now()})
    stamp = now().replace(":", "").replace("+", "_")
    backup_root = project_root / "audit" / "dashboard" / "improvement_backups" / stamp
    state["backup_root"] = backup_root.relative_to(project_root).as_posix()
    atomic_json(state_path(project_root), state)
    policy = ChunkPolicy.from_config(load_config())
    run = load_object(run_path)
    all_ready_rows: list[dict[str, Any]] = []
    touched: set[str] = set()
    try:
        for candidate in state["candidates"]:
            if candidate.get("status") != "PENDING":
                continue
            document_id = candidate["document_id"]
            state.update({"current_document_id": document_id, "updated_at": now()})
            atomic_json(state_path(project_root), state)
            try:
                result = _improve_one(project_root, run, document_id, policy, backup_root)
                candidate.update(result)
                touched.add(document_id)
                ready_path = project_root / "processing" / document_id / "chunks" / "embedding_ready.jsonl"
                all_ready_rows.extend(
                    json.loads(line) for line in ready_path.read_text(encoding="utf-8").splitlines()
                    if line.strip()
                )
                if result["status"] == "IMPROVED":
                    state["improved"] += 1
                else:
                    state["unchanged"] += 1
                print(f"{document_id} {result['status']} chunks={result['before_chunks']}->{result['after_chunks']}", flush=True)
            except Exception as exc:
                candidate.update({"status": "FAILED", "error": f"{type(exc).__name__}: {exc}"[:500]})
                state["failed"] += 1
                print(f"{document_id} FAILED {type(exc).__name__}: {exc}", flush=True)
            state["processed"] += 1
            state["recent"] = ([{
                "document_id": candidate["document_id"],
                "status": candidate["status"],
                "action": candidate["action"],
            }] + state.get("recent", []))[:12]
            atomic_json(run_path, run)
            atomic_json(state_path(project_root), state)

        if touched:
            manifest_module.merge_into(
                project_root / "audit" / "embedding_ready_manifest.jsonl",
                all_ready_rows,
                document_ids=touched,
            )
            # Existing immutable audits and promotion plans describe the pre-improvement
            # chunk identities and must not be advertised as current.
            run["staging_audit_ids"] = []
            run["promotion_plan_ids"] = []
            run["updated_at"] = now()
            atomic_json(run_path, run)

        after = Counter()
        for candidate in state["candidates"]:
            for warning in candidate.get("warnings") or []:
                after[_code(warning)] += 1
        state["after"] = dict(sorted(after.items()))
        state.update({
            "status": "FINISHED" if not state["failed"] else "FINISHED_WITH_FAILURES",
            "worker_pid": None,
            "current_document_id": None,
            "finished_at": now(),
            "message": (
                f"İyileştirme tamamlandı: {state['improved']} güncellendi, "
                f"{state['failed']} başarısız. Görsel adaylar güvenli yeniden işleme için ertelendi."
            ),
            "updated_at": now(),
        })
        state = consolidate_completed_state(state, project_root, run)
        atomic_json(state_path(project_root), state)
        return 0 if not state["failed"] else 2
    except BaseException as exc:
        state.update({
            "status": "ERROR", "worker_pid": None, "current_document_id": None,
            "last_error": f"{type(exc).__name__}: {exc}"[:1000],
            "message": "İyileştirme beklenmeyen hata ile durdu.", "updated_at": now(),
        })
        atomic_json(state_path(project_root), state)
        raise


__all__ = [
    "build_state", "consolidate_completed_state", "execute", "load_state", "log_path",
    "queue_identity_repairs", "start_worker", "state_path",
]
