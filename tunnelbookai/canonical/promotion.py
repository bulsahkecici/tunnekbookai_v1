"""Deterministic planning and explicitly approved atomic canonical promotion."""

from __future__ import annotations

import fcntl
import getpass
import os
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from tunnelbookai.ingest.staging import STAGING_COPY_FILES, STAGING_VERSION
from shared.project_quality_gate import inspect_legacy_isolation

from .eligibility import discover_candidates, validate_chunk_files
from .errors import CanonicalError
from .hashing import (
    canonical_sha256, deterministic_json_text, load_json, load_jsonl, sha256_file,
    write_deterministic_json, write_identity_jsonl,
)
from .models import (
    CONTRACT_VERSION, SCHEMA_VERSION, CandidateAction, CanonicalPromotionCandidate,
    CanonicalPromotionPlan, FileIdentity,
)
from .paths import CanonicalContext
from .verifier import build_manifest, inspect_canonical, parse_manifest


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    temporary = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(deterministic_json_text(value))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        _fsync_dir(path.parent)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _fsync_dir(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _authorities(context: CanonicalContext) -> dict[str, str]:
    values = dict(context.book_inputs.identities)
    paths_config = context.root / "config" / "paths.json"
    values["paths_sha256"] = sha256_file(paths_config)
    return dict(sorted(values.items()))


def _before(context: CanonicalContext) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    inventory = inspect_canonical(context=context)
    if inventory.state.value == "INVALID":
        raise CanonicalError("CANONICAL_MANIFEST_INVALID", "cannot plan against INVALID canonical state", details=inventory.to_dict())
    documents: list[dict[str, Any]] = []
    if inventory.ready:
        manifest = parse_manifest(load_json(context.manifest_path, code="CANONICAL_MANIFEST_INVALID"))
        documents = [record.to_dict() for record in manifest.documents]
    return {
        "state": inventory.state.value,
        "manifest_sha256": inventory.manifest_sha256,
        "canonical_corpus_digest": inventory.corpus_digest,
        "document_count": inventory.document_count,
        "chunk_count": inventory.chunk_count,
        "retrieval_ready_chunk_count": inventory.retrieval_ready_chunk_count,
    }, documents


def build_plan(
    project_root: Path | str | None = None, *, document_ids: Iterable[str] | None = None,
    write: bool = True, context: CanonicalContext | None = None,
) -> CanonicalPromotionPlan:
    context = context or CanonicalContext.load(project_root)
    isolation = inspect_legacy_isolation(context.root)
    if isolation["decision"] != "GO":
        raise CanonicalError(
            "INVALID_STAGING_BUNDLE", "active legacy topology or runtime references detected",
            details=isolation,
        )
    selected = tuple(sorted(set(document_ids or [])))
    before, existing = _before(context)
    candidates = discover_candidates(context, selected or None, existing_documents=existing)
    expected_by_id = {str(row["document_id"]): dict(row) for row in existing}
    for candidate in candidates:
        if candidate.action is CandidateAction.PROMOTE and candidate.record is not None:
            expected_by_id[candidate.document_id] = dict(candidate.record)
    expected_manifest = build_manifest(list(expected_by_id.values())) if expected_by_id else None
    expected_after = {
        "state": "READY" if expected_manifest else "EMPTY",
        "document_count": len(expected_by_id),
        "chunk_count": expected_manifest.chunk_count if expected_manifest else 0,
        "retrieval_ready_chunk_count": expected_manifest.retrieval_ready_chunk_count if expected_manifest else 0,
        "canonical_corpus_digest": expected_manifest.canonical_corpus_digest if expected_manifest else None,
        "document_digests": {
            document_id: row["document_digest"] for document_id, row in sorted(expected_by_id.items())
        },
    }
    applicable = bool(candidates) and all(candidate.action is not CandidateAction.REJECTED for candidate in candidates)
    prototype = CanonicalPromotionPlan(
        plan_id="", selector={"mode": "DOCUMENT_IDS" if selected else "ALL", "document_ids": list(selected)},
        authorities=_authorities(context), before=before, candidates=candidates,
        applicable=applicable, expected_after=expected_after,
    )
    plan_id = "CCP_" + canonical_sha256(prototype.body())
    plan = CanonicalPromotionPlan(
        plan_id=plan_id, selector=prototype.selector, authorities=prototype.authorities,
        before=prototype.before, candidates=prototype.candidates, applicable=prototype.applicable,
        expected_after=prototype.expected_after,
    )
    if write:
        path = context.audit_root / "plans" / f"{plan_id}.json"
        if path.exists():
            if path.read_text(encoding="utf-8") != deterministic_json_text(plan.to_dict()):
                raise CanonicalError("INVALID_CANONICAL_PROMOTION_PLAN", f"existing plan differs: {path}")
        else:
            _atomic_json(path, plan.to_dict())
            path.chmod(0o444)
    return plan


def _candidate_from_dict(value: Mapping[str, Any]) -> CanonicalPromotionCandidate:
    expected = {
        "document_id", "action", "source_sha256", "chunk_count", "retrieval_ready_chunk_count",
        "document_digest", "input_files", "validations", "warnings", "record",
    }
    if not isinstance(value, Mapping) or set(value) != expected:
        raise CanonicalError("INVALID_CANONICAL_PROMOTION_PLAN", "candidate schema is invalid")
    file_keys = {"path", "size", "sha256", "semantic_sha256"}
    if any(not isinstance(row, Mapping) or set(row) != file_keys for row in value.get("input_files") or []):
        raise CanonicalError("INVALID_CANONICAL_PROMOTION_PLAN", "input file identity schema is invalid")
    files = tuple(
        FileIdentity(
            path=str(row["path"]), size=int(row["size"]), sha256=str(row["sha256"]),
            semantic_sha256=str(row["semantic_sha256"]),
        )
        for row in value.get("input_files") or []
    )
    return CanonicalPromotionCandidate(
        document_id=str(value["document_id"]), action=CandidateAction(str(value["action"])),
        source_sha256=value.get("source_sha256"), chunk_count=int(value.get("chunk_count") or 0),
        retrieval_ready_chunk_count=int(value.get("retrieval_ready_chunk_count") or 0),
        document_digest=value.get("document_digest"), input_files=files,
        validations=tuple(value.get("validations") or []), warnings=tuple(value.get("warnings") or []),
        record=value.get("record"),
    )


def load_plan(context: CanonicalContext, path: Path | str) -> CanonicalPromotionPlan:
    candidate_path = Path(path)
    if not candidate_path.is_absolute():
        candidate_path = context.root / candidate_path
    resolved = candidate_path.resolve()
    plans_root = (context.audit_root / "plans").resolve()
    if resolved.parent != plans_root or resolved.is_symlink() or not resolved.is_file():
        raise CanonicalError("INVALID_CANONICAL_PROMOTION_PLAN", "plan must be a regular file in the canonical plans root")
    payload = load_json(resolved, code="INVALID_CANONICAL_PROMOTION_PLAN")
    if not isinstance(payload, Mapping):
        raise CanonicalError("INVALID_CANONICAL_PROMOTION_PLAN", "plan must be an object")
    required = {
        "plan_id", "schema_version", "contract_version", "selector", "authorities",
        "before", "candidates", "applicable", "expected_after",
    }
    if set(payload) != required or payload.get("schema_version") != SCHEMA_VERSION or payload.get("contract_version") != CONTRACT_VERSION:
        raise CanonicalError("INVALID_CANONICAL_PROMOTION_PLAN", "plan schema is invalid")
    plan = CanonicalPromotionPlan(
        plan_id=str(payload["plan_id"]), selector=dict(payload["selector"]),
        authorities=dict(payload["authorities"]), before=dict(payload["before"]),
        candidates=tuple(_candidate_from_dict(row) for row in payload["candidates"]),
        applicable=bool(payload["applicable"]), expected_after=dict(payload["expected_after"]),
    )
    if plan.plan_id != "CCP_" + canonical_sha256(plan.body()) or resolved.name != f"{plan.plan_id}.json":
        raise CanonicalError("INVALID_CANONICAL_PROMOTION_PLAN", "plan identity does not match its contents/path")
    if resolved.read_text(encoding="utf-8") != deterministic_json_text(payload):
        raise CanonicalError("INVALID_CANONICAL_PROMOTION_PLAN", "plan is not deterministically serialized")
    return plan


def _audit(
    context: CanonicalContext, promotion_id: str, *, plan_id: str | None, approval: str | None,
    started_at: str, result: str, before: Mapping[str, Any] | None = None,
    after: Mapping[str, Any] | None = None, candidates: Iterable[CanonicalPromotionCandidate] = (),
    error: CanonicalError | None = None,
) -> Path:
    path = context.audit_root / "applies" / f"{promotion_id}.json"
    payload = {
        "schema_version": SCHEMA_VERSION, "contract_version": CONTRACT_VERSION,
        "promotion_id": promotion_id, "plan_id": plan_id, "actor": getpass.getuser(),
        "approval": {"kind": "EXACT_PLAN_ID", "value": approval, "matched": bool(plan_id and approval == plan_id)},
        "started_at": started_at, "finished_at": _now(), "before": dict(before or {}),
        "after": dict(after or {}),
        "planned_candidates": [candidate.document_id for candidate in candidates],
        "applied_candidates": [candidate.document_id for candidate in candidates if candidate.action is CandidateAction.PROMOTE and result == "APPLIED"],
        "idempotent_candidates": [candidate.document_id for candidate in candidates if candidate.action is CandidateAction.IDEMPOTENT_NO_CHANGE],
        "rejected_candidates": [candidate.document_id for candidate in candidates if candidate.action is CandidateAction.REJECTED],
        "result": result,
        "error": {"code": error.code, "message": str(error), "details": error.details} if error else None,
    }
    if path.exists():
        raise CanonicalError("ATOMIC_PROMOTION_FAILED", f"immutable audit already exists: {path}")
    _atomic_json(path, payload)
    path.chmod(0o444)
    pending = context.audit_root / "pending" / f"{promotion_id}.json"
    pending.unlink(missing_ok=True)
    return path


def _promotion_id(plan_id: str | None) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = (plan_id or "NO_PLAN")[-10:]
    return f"CPA_{stamp}_{suffix}_{uuid.uuid4().hex[:8]}"


def _materialize_candidate(context: CanonicalContext, candidate: CanonicalPromotionCandidate, temporary_root: Path) -> Path:
    assert candidate.record is not None and candidate.document_digest is not None
    record = candidate.record
    document_id = candidate.document_id
    staging = context.paths.corpus_staging_root / STAGING_VERSION / document_id
    processing = context.paths.processing_root / document_id
    destination = temporary_root / document_id / candidate.document_digest
    destination.mkdir(parents=True)
    sources = {
        "document.md": staging / "document.md",
        **{name: staging / name for name in STAGING_COPY_FILES},
        "chunks/chunk_manifest.jsonl": processing / "chunks" / "chunk_manifest.jsonl",
        "chunks/embedding_ready.jsonl": processing / "chunks" / "embedding_ready.jsonl",
    }
    for relative, source in sources.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    classification = record["classification"]
    identities, _, _, _ = validate_chunk_files(
        context, document_id, str(candidate.source_sha256), str(classification["primary_section"]),
        list(classification["secondary_sections"]), destination / "chunks/chunk_manifest.jsonl",
        destination / "chunks/embedding_ready.jsonl",
    )
    write_identity_jsonl(destination / "chunks/chunk_identities.jsonl", identities)
    expected = {str(item["role"]): item for item in record["canonical_files"]}
    for relative, identity in expected.items():
        path = destination / relative
        if path.stat().st_size != identity["size"] or sha256_file(path) != identity["sha256"]:
            raise CanonicalError("ATOMIC_PROMOTION_FAILED", f"temporary copy identity mismatch: {relative}")
    return destination


def _make_readonly(path: Path) -> None:
    for child in sorted(path.rglob("*"), reverse=True):
        child.chmod(0o444 if child.is_file() else 0o555)
    path.chmod(0o555)


def _make_writable(path: Path) -> None:
    path.chmod(0o755)
    for child in path.rglob("*"):
        child.chmod(0o644 if child.is_file() else 0o755)


def apply_plan(
    plan_path: Path | str, *, approve: str | None, project_root: Path | str | None = None,
    context: CanonicalContext | None = None,
) -> dict[str, Any]:
    context = context or CanonicalContext.load(project_root)
    started = _now()
    plan: CanonicalPromotionPlan | None = None
    promotion_id = _promotion_id(None)
    try:
        plan = load_plan(context, plan_path)
        promotion_id = _promotion_id(plan.plan_id)
        pending = context.audit_root / "pending" / f"{promotion_id}.json"
        _atomic_json(pending, {
            "schema_version": SCHEMA_VERSION, "contract_version": CONTRACT_VERSION,
            "promotion_id": promotion_id, "plan_id": plan.plan_id, "started_at": started,
            "approval_value": approve, "state": "APPLYING",
        })
        if not approve:
            raise CanonicalError("PROMOTION_APPROVAL_REQUIRED", "apply requires --approve with the exact plan ID")
        if approve != plan.plan_id:
            raise CanonicalError("PROMOTION_APPROVAL_MISMATCH", "approval does not match plan ID")
        if not plan.applicable:
            raise CanonicalError("INVALID_CANONICAL_PROMOTION_PLAN", "blocked plan cannot be applied")

        context.audit_root.mkdir(parents=True, exist_ok=True)
        lock_path = context.audit_root / "canonical.lock"
        with lock_path.open("a+") as lock:
            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise CanonicalError("CANONICAL_PROMOTION_LOCKED", "another canonical apply holds the lock") from exc
            selected = plan.selector.get("document_ids") or None
            current = build_plan(context=context, document_ids=selected, write=False)
            if current.to_dict() != plan.to_dict():
                raise CanonicalError("STALE_CANONICAL_PROMOTION_PLAN", "promotion-relevant state changed after planning")
            before = dict(plan.before)
            _, existing_records = _before(context)
            promote = [candidate for candidate in current.candidates if candidate.action is CandidateAction.PROMOTE]
            if not promote:
                audit_path = _audit(
                    context, promotion_id, plan_id=plan.plan_id, approval=approve, started_at=started,
                    result="IDEMPOTENT_NO_CHANGE", before=before, after=before, candidates=current.candidates,
                )
                return {"status": "IDEMPOTENT_NO_CHANGE", "plan_id": plan.plan_id, "audit_path": context.relative(audit_path), "canonical": before}

            context.canonical_root.mkdir(parents=True, exist_ok=True)
            transaction_root = Path(tempfile.mkdtemp(prefix=f".canonical-{promotion_id}-", dir=str(context.canonical_root.parent)))
            added: list[Path] = []
            old_manifest = context.manifest_path.read_bytes() if context.manifest_path.is_file() else None
            committed = False
            try:
                temporary_objects = [_materialize_candidate(context, candidate, transaction_root) for candidate in promote]
                for candidate, temporary in zip(promote, temporary_objects):
                    final = context.canonical_root / "objects" / candidate.document_id / str(candidate.document_digest)
                    final.parent.mkdir(parents=True, exist_ok=True)
                    if final.exists():
                        raise CanonicalError("DOCUMENT_ID_CONFLICT", f"unexpected canonical object already exists: {final}")
                    os.replace(temporary, final)
                    _make_readonly(final)
                    _fsync_dir(final.parent)
                    added.append(final)

                records = {str(row["document_id"]): row for row in existing_records}
                for candidate in promote:
                    record = dict(candidate.record or {})
                    record["promotion_plan_id"] = plan.plan_id
                    records[candidate.document_id] = record
                manifest = build_manifest(list(records.values()))
                if manifest.canonical_corpus_digest != plan.expected_after["canonical_corpus_digest"]:
                    raise CanonicalError("STALE_CANONICAL_PROMOTION_PLAN", "materialized digest differs from plan")
                _atomic_json(context.manifest_path, manifest.to_dict())
                context.manifest_path.chmod(0o444)
                committed = True
                inventory = inspect_canonical(context=context)
                if not inventory.ready:
                    raise CanonicalError("ATOMIC_PROMOTION_FAILED", "post-commit verification failed", details=inventory.to_dict())
                audit_path = _audit(
                    context, promotion_id, plan_id=plan.plan_id, approval=approve, started_at=started,
                    result="APPLIED", before=before, after=inventory.to_dict(), candidates=current.candidates,
                )
                return {"status": "APPLIED", "plan_id": plan.plan_id, "audit_path": context.relative(audit_path), "canonical": inventory.to_dict()}
            except BaseException:
                if committed:
                    context.manifest_path.chmod(0o644)
                    if old_manifest is None:
                        context.manifest_path.unlink(missing_ok=True)
                    else:
                        fd, name = tempfile.mkstemp(prefix=".rollback-", dir=str(context.canonical_root))
                        with os.fdopen(fd, "wb") as handle:
                            handle.write(old_manifest)
                            handle.flush()
                            os.fsync(handle.fileno())
                        os.replace(name, context.manifest_path)
                for path in reversed(added):
                    if path.exists():
                        _make_writable(path)
                        shutil.rmtree(path)
                raise
            finally:
                if transaction_root.exists():
                    _make_writable(transaction_root)
                    shutil.rmtree(transaction_root)
    except CanonicalError as exc:
        candidates = plan.candidates if plan else ()
        try:
            audit_path = _audit(
                context, promotion_id, plan_id=plan.plan_id if plan else None, approval=approve,
                started_at=started, result="FAILED", before=plan.before if plan else {},
                candidates=candidates, error=exc,
            )
            exc.details = {"original": exc.details, "audit_path": context.relative(audit_path)}
        except CanonicalError:
            pass
        raise
    except BaseException as exc:
        wrapped = CanonicalError("ATOMIC_PROMOTION_FAILED", str(exc))
        try:
            _audit(
                context, promotion_id, plan_id=plan.plan_id if plan else None, approval=approve,
                started_at=started, result="FAILED", before=plan.before if plan else {},
                candidates=plan.candidates if plan else (), error=wrapped,
            )
        except CanonicalError:
            pass
        raise wrapped from exc


__all__ = ["apply_plan", "build_plan", "load_plan"]
