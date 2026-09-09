"""Operator CLI for controlled canonical promotion."""

from __future__ import annotations

import argparse
import json
from typing import Any

from tunnelbookai.book.errors import BookEngineError

from .errors import ATOMIC_EXIT, POLICY_EXIT, CanonicalError
from .paths import CanonicalContext
from .promotion import apply_plan, build_plan
from .verifier import inspect_canonical


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="python -m tunnelbookai.canonical")
    sub = root.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan", help="validate staging and write a deterministic dry-run plan")
    plan.add_argument("--document-id", action="append", default=[])
    plan.add_argument("--document-id-file")
    plan.add_argument("--json", action="store_true")
    apply = sub.add_parser("apply", help="apply one exact approved plan")
    apply.add_argument("--plan", required=True)
    apply.add_argument("--approve")
    apply.add_argument("--json", action="store_true")
    for name in ("verify", "status"):
        child = sub.add_parser(name)
        child.add_argument("--json", action="store_true")
    return root


def _print(payload: dict[str, Any], *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if "plan_id" in payload:
        print(f"CANONICAL PROMOTION PLAN {payload['plan_id']}")
        print(f"Applicable: {payload.get('applicable')}")
        for row in payload.get("candidates", []):
            print(
                f"  {row['action']:22} {row['document_id']} "
                f"source={row.get('source_sha256') or '-'} chunks={row.get('chunk_count', 0)}"
            )
        if payload.get("plan_path"):
            print(f"Plan file: {payload['plan_path']}")
        print("DRY RUN — canonical, originals, processing, and staging were not changed.")
        return
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    json_output = bool(getattr(args, "json", False))
    try:
        context = CanonicalContext.load()
        if args.command == "plan":
            document_ids = list(args.document_id)
            if args.document_id_file:
                from pathlib import Path
                from tunnelbookai.population.models import identity, load_object

                selector_path = Path(args.document_id_file)
                if not selector_path.is_absolute():
                    selector_path = context.root / selector_path
                expected_root = (context.root / "audit" / "corpus_population" / "promotion_batches").resolve()
                if (
                    selector_path.resolve().parent != expected_root
                    or selector_path.is_symlink()
                    or not selector_path.is_file()
                ):
                    raise CanonicalError(
                        "INVALID_CANONICAL_PROMOTION_PLAN",
                        "document ID selector must be a regular population promotion-batch file",
                    )
                selector = load_object(selector_path)
                expected_fields = {
                    "selector_id", "schema_version", "contract_version", "staging_audit_id",
                    "ordinal", "document_ids", "materialized_bytes", "generated_at",
                }
                if set(selector) != expected_fields:
                    raise CanonicalError(
                        "INVALID_CANONICAL_PROMOTION_PLAN", "document ID selector fields differ"
                    )
                document_values = selector.get("document_ids")
                if (
                    selector.get("schema_version") != "1.0"
                    or selector.get("contract_version") != "corpus-population-v1"
                    or not isinstance(selector.get("ordinal"), int)
                    or selector["ordinal"] < 1
                    or not isinstance(selector.get("materialized_bytes"), int)
                    or selector["materialized_bytes"] < 0
                    or not isinstance(document_values, list)
                    or not document_values
                    or not all(isinstance(value, str) for value in document_values)
                    or document_values != sorted(set(document_values))
                    or len(str(selector.get("staging_audit_id") or "")) != 68
                    or not str(selector.get("staging_audit_id") or "").startswith("CSA_")
                    or any(
                        char not in "0123456789abcdef"
                        for char in str(selector["staging_audit_id"])[4:]
                    )
                ):
                    raise CanonicalError(
                        "INVALID_CANONICAL_PROMOTION_PLAN", "document ID selector values are invalid"
                    )
                semantic = {
                    key: selector[key]
                    for key in (
                        "schema_version", "contract_version", "staging_audit_id",
                        "ordinal", "document_ids",
                    )
                }
                if selector.get("selector_id") != identity("CPP_", semantic):
                    raise CanonicalError(
                        "INVALID_CANONICAL_PROMOTION_PLAN", "document ID selector identity mismatch"
                    )
                document_ids.extend(str(value) for value in document_values)
            plan = build_plan(context=context, document_ids=document_ids)
            payload = plan.to_dict()
            payload["plan_path"] = context.relative(context.audit_root / "plans" / f"{plan.plan_id}.json")
            _print(payload, json_output=json_output)
            return 0 if plan.applicable else POLICY_EXIT
        if args.command == "apply":
            _print(apply_plan(args.plan, approve=args.approve, context=context), json_output=json_output)
            return 0
        inventory = inspect_canonical(context=context)
        payload = inventory.to_dict()
        payload["command"] = args.command
        _print(payload, json_output=json_output)
        return 0 if inventory.state.value in {"EMPTY", "READY"} else POLICY_EXIT
    except CanonicalError as exc:
        _print({"status": "BLOCKED", "reason_code": exc.code, "detail": str(exc), "details": exc.details}, json_output=True)
        return ATOMIC_EXIT if exc.code == "ATOMIC_PROMOTION_FAILED" else POLICY_EXIT
    except BookEngineError as exc:
        _print({"status": "BLOCKED", "reason_code": exc.code, "detail": str(exc), "details": exc.details}, json_output=True)
        return POLICY_EXIT


__all__ = ["main", "parser"]
