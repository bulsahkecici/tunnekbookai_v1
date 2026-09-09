"""Operator CLI for Corpus Population V1."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from tunnelbookai.ingest.paths import PROJECT_ROOT

from .audit import build_readiness_report, build_staging_audit
from .batching import plan_batches
from .inventory import build_inventory
from .manual_import import apply_import_plan, build_import_plan
from .models import PopulationState, atomic_json, load_object, now
from .runner import run_batch


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="python -m tunnelbookai.population")
    sub = root.add_subparsers(dest="command", required=True)

    inventory = sub.add_parser("inventory")
    inventory.add_argument("--json", action="store_true")

    manual_plan = sub.add_parser("manual-import-plan")
    manual_plan.add_argument("--from", dest="source", required=True)
    manual_plan.add_argument("--json", action="store_true")

    manual_apply = sub.add_parser("manual-import-apply")
    manual_apply.add_argument("--from", dest="source", required=True)
    manual_apply.add_argument("--plan", required=True)
    manual_apply.add_argument("--approve", required=True)
    manual_apply.add_argument("--json", action="store_true")

    batches = sub.add_parser("plan-batches")
    batches.add_argument("--inventory", required=True)
    batches.add_argument("--json", action="store_true")

    execute = sub.add_parser("run-batch")
    execute.add_argument("--batch", required=True)
    execute.add_argument("--resume", action="store_true")
    execute.add_argument("--force-reprocess", action="store_true")
    execute.add_argument("--json", action="store_true")

    for name in ("status", "staging-audit", "readiness"):
        child = sub.add_parser(name)
        child.add_argument("--run", required=True)
        child.add_argument("--json", action="store_true")

    account = sub.add_parser("account-exclusion")
    account.add_argument("--run", required=True)
    account.add_argument("--document-id", required=True)
    account.add_argument("--reason", required=True)
    account.add_argument("--json", action="store_true")
    return root


def _print(value: dict[str, Any], json_output: bool) -> None:
    if json_output:
        print(json.dumps(value, ensure_ascii=False, indent=2))
        return
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _run_path(value: str) -> Path:
    path = Path(value)
    path = path if path.is_absolute() else PROJECT_ROOT / path
    run_root = (PROJECT_ROOT / "audit" / "corpus_population" / "runs").resolve()
    if path.is_symlink() or not path.is_file() or path.resolve().parent != run_root:
        raise ValueError("population run must be a regular file in the run root")
    return path


def _status(path: Path) -> dict[str, Any]:
    run = load_object(path)
    from .batching import _verify_run
    _verify_run(run)
    dispositions = Counter(
        str(row.get("disposition") or "PENDING") for row in run["documents"].values()
    )
    return {
        "run_id": run["run_id"],
        "state": run["state"],
        "batches": len(run["batch_ids"]),
        "completed_batches": len(run["completed_batches"]),
        "failed_batches": len(run["failed_batches"]),
        "attempt_ids": run.get("attempt_ids", []),
        "dispositions": dict(sorted(dispositions.items())),
        "staging_audit_ids": run["staging_audit_ids"],
        "promotion_plan_ids": run["promotion_plan_ids"],
        "canonical_before": run["canonical_before"],
        "canonical_after": run["canonical_after"],
    }


def _account(path: Path, document_id: str, reason: str) -> dict[str, Any]:
    run = load_object(path)
    from .batching import _verify_run
    _verify_run(run)
    if not reason.strip():
        raise ValueError("accounted exclusion requires a non-empty reason")
    if document_id not in run["documents"]:
        raise ValueError(f"document is not part of the population run: {document_id}")
    row = run["documents"][document_id]
    if row.get("disposition") not in {"FAILED", "NEEDS_REVIEW", "REJECTED", "UNSUPPORTED", "DUPLICATE"}:
        raise ValueError("only failed, review, rejected, unsupported, or duplicate outcomes can be excluded")
    row["accounted_exclusion"] = {"reason": reason, "recorded_at": now()}
    unresolved = [
        value for value in run["documents"].values()
        if value.get("disposition") in {"PENDING", "RECOVERY_REQUIRED", "FAILED", "NEEDS_REVIEW"}
        and not value.get("accounted_exclusion")
    ]
    if not unresolved:
        run["state"] = PopulationState.INGEST_ACCOUNTED.value
    run["updated_at"] = now()
    atomic_json(path, run)
    return {"status": "ACCOUNTED_EXCLUSION", "run_id": run["run_id"], "document_id": document_id}


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "inventory":
            result = build_inventory()
        elif args.command == "manual-import-plan":
            result = build_import_plan(args.source)
        elif args.command == "manual-import-apply":
            result = apply_import_plan(args.source, args.plan, approve=args.approve)
        elif args.command == "plan-batches":
            result = plan_batches(args.inventory)
        elif args.command == "run-batch":
            result = run_batch(
                args.batch, resume=args.resume, force_reprocess=args.force_reprocess
            )
        elif args.command == "status":
            result = _status(_run_path(args.run))
        elif args.command == "staging-audit":
            result = build_staging_audit(args.run)
        elif args.command == "readiness":
            result = build_readiness_report(args.run)
        else:
            result = _account(_run_path(args.run), args.document_id, args.reason)
        _print(result, bool(getattr(args, "json", False)))
        return 0
    except Exception as exc:
        _print(
            {"status": "BLOCKED", "reason_code": type(exc).__name__, "detail": str(exc)},
            True,
        )
        return 2


__all__ = ["main", "parser"]
