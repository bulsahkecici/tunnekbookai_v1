"""Operator CLI for validated book inputs and declared foundation stages."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .errors import BookEngineError
from .coverage_audit import run_coverage_audit
from .evidence_review import run_evidence_review
from .editorial import run_editorial_audit
from .freeze import record_operator_approval, run_freeze
from .inputs import BookInputs, load_book_inputs
from .normalize import normalize_book_inputs
from .preparation import prepare_sections
from .prewriting import run_prewriting_audit
from .retrieval import build_index, search_index
from .revision import run_revision
from .stages import not_implemented
from .status import build_status
from .writer import run_section_writer


SECTION_COMMANDS = {
    "evidence-audit": "PREWRITING_EVIDENCE_AUDIT",
    "prepare": "SECTION_EVIDENCE_PACKET",
    "write": "SECTION_WRITER",
    "evidence-review": "POSTWRITING_EVIDENCE_AUDIT",
    "coverage-audit": "QUESTION_COVERAGE_AUDIT",
    "revise": "SECTION_REVISION",
    "editorial-audit": "EDITORIAL_AUDIT",
    "freeze": "SECTION_FREEZE",
}
GLOBAL_COMMANDS = {
    "assemble": "BOOK_ASSEMBLY",
}


def _validation_payload(inputs: BookInputs) -> dict[str, Any]:
    return {
        "decision": "PASS",
        "contract_version": inputs.contract.payload["contract_version"],
        "scope_sections": len(inputs.scope),
        "question_bank_sections": len(inputs.question_section_ids),
        "total_questions": len(inputs.questions),
        "global_minimum_answered_count": inputs.contract.coverage_policy["global"]["minimum_answered_count"],
        "global_minimum_coverage": inputs.contract.coverage_policy["global"]["minimum_coverage"],
        "identities": dict(inputs.identities),
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="python -m tunnelbookai.book")
    sub = root.add_subparsers(dest="command", required=True)
    for name in ("validate", "status"):
        child = sub.add_parser(name)
        child.add_argument("--json", action="store_true")
    for name in GLOBAL_COMMANDS:
        sub.add_parser(name)
    approve = sub.add_parser("approve-section")
    approve.add_argument("--section", required=True)
    approve.add_argument("--note", required=True, help="what was read and why it is acceptable as a book section")
    approve.add_argument("--approver")
    normalize = sub.add_parser("normalize-inputs")
    normalize.add_argument("--draft", default="book/question_bank/drafts/question_bank_v2_draft.md")
    normalize.add_argument("--minimum-coverage", type=float, default=0.6)
    build = sub.add_parser("build-index")
    build.add_argument("--batch-size", type=int, default=32)
    build.add_argument("--no-resume", action="store_true")
    search = sub.add_parser("search")
    search.add_argument("--query", required=True)
    search.add_argument("--section")
    search.add_argument("--top-k", type=int, default=10)
    for name in SECTION_COMMANDS:
        child = sub.add_parser(name)
        if name in {"evidence-audit", "prepare"}:
            target = child.add_mutually_exclusive_group(required=True)
            target.add_argument("--section")
            target.add_argument("--all", action="store_true")
            if name == "evidence-audit":
                child.add_argument("--batch-size", type=int, default=8)
                child.add_argument("--top-k", type=int, default=8)
        else:
            child.add_argument("--section", required=True)
            if name in {"write", "evidence-review", "coverage-audit"}:
                child.add_argument("--batch-size", type=int, default=8)
    return root


def _print(payload: dict[str, Any], *, json_output: bool = True) -> None:
    if json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print("BOOK INPUT VALIDATION: PASS")
    print(f"{payload['question_bank_sections']} question-bank sections / {payload['total_questions']} questions")
    print(
        f"Publication coverage hard gate: {payload['global_minimum_answered_count']} answered "
        f"/ {payload['global_minimum_coverage']:.0%}"
    )


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "normalize-inputs":
            # Runs before input loading on purpose: it is the command that produces the
            # inputs the loader validates, and re-seals the contract with their hashes.
            from pathlib import Path

            result = normalize_book_inputs(Path(__file__).resolve().parents[2], draft_path=args.draft, minimum_coverage=args.minimum_coverage)
            _print({**result, "validation": _validation_payload(load_book_inputs())})
            return 0
        inputs = load_book_inputs()
        if args.command == "validate":
            _print(_validation_payload(inputs), json_output=args.json)
            return 0
        if args.command == "status":
            _print(build_status(inputs), json_output=True)
            return 0
        if args.command == "build-index":
            def progress(payload: dict[str, Any]) -> None:
                print(json.dumps({"event": "INDEX_PROGRESS", **payload}, ensure_ascii=False), file=sys.stderr, flush=True)
            _print(build_index(batch_size=args.batch_size, resume=not args.no_resume, progress=progress))
            return 0
        if args.command == "search":
            if args.section and args.section not in inputs.scope_by_id:
                raise BookEngineError(
                    "UNKNOWN_SECTION", f"section is not present in authoritative scope: {args.section}"
                )
            _print(search_index(args.query, section=args.section, top_k=args.top_k))
            return 0
        if args.command == "evidence-audit":
            if args.section and args.section not in inputs.questions_by_section:
                raise BookEngineError(
                    "UNKNOWN_SECTION", f"section is not a question-bank section: {args.section}"
                )
            def audit_progress(payload: dict[str, Any]) -> None:
                print(json.dumps({"event": "EVIDENCE_AUDIT_PROGRESS", **payload}, ensure_ascii=False), file=sys.stderr, flush=True)
            _print(run_prewriting_audit(
                section_ids=None if args.all else [args.section],
                batch_size=args.batch_size,
                top_k=args.top_k,
                progress=audit_progress,
            ))
            return 0
        if args.command == "prepare":
            if args.section and args.section not in inputs.questions_by_section:
                raise BookEngineError(
                    "UNKNOWN_SECTION", f"section is not a question-bank section: {args.section}"
                )
            def preparation_progress(payload: dict[str, Any]) -> None:
                print(json.dumps({"event": "SECTION_PREPARATION_PROGRESS", **payload}, ensure_ascii=False), file=sys.stderr, flush=True)
            _print(prepare_sections(
                section_ids=None if args.all else [args.section],
                progress=preparation_progress,
            ))
            return 0
        if args.command == "write":
            if args.section not in inputs.questions_by_section:
                raise BookEngineError(
                    "UNKNOWN_SECTION", f"section is not a question-bank section: {args.section}"
                )
            def writer_progress(payload: dict[str, Any]) -> None:
                print(json.dumps({"event": "SECTION_WRITER_PROGRESS", **payload}, ensure_ascii=False), file=sys.stderr, flush=True)
            result = run_section_writer(
                args.section,
                batch_size=args.batch_size,
                progress=writer_progress,
            )
            _print(result)
            return 0 if result.get("status") != "BLOCKED" else 2
        if args.command == "evidence-review":
            if args.section not in inputs.questions_by_section:
                raise BookEngineError(
                    "UNKNOWN_SECTION", f"section is not a question-bank section: {args.section}"
                )
            def evidence_review_progress(payload: dict[str, Any]) -> None:
                print(json.dumps({"event": "POSTWRITING_EVIDENCE_PROGRESS", **payload}, ensure_ascii=False), file=sys.stderr, flush=True)
            _print(run_evidence_review(
                args.section,
                batch_size=args.batch_size,
                progress=evidence_review_progress,
            ))
            return 0
        if args.command == "coverage-audit":
            if args.section not in inputs.questions_by_section:
                raise BookEngineError(
                    "UNKNOWN_SECTION", f"section is not a question-bank section: {args.section}"
                )
            def coverage_progress(payload: dict[str, Any]) -> None:
                print(json.dumps({"event": "QUESTION_COVERAGE_PROGRESS", **payload}, ensure_ascii=False), file=sys.stderr, flush=True)
            _print(run_coverage_audit(
                args.section,
                batch_size=args.batch_size,
                progress=coverage_progress,
            ))
            return 0
        if args.command == "revise":
            if args.section not in inputs.questions_by_section:
                raise BookEngineError(
                    "UNKNOWN_SECTION", f"section is not a question-bank section: {args.section}"
                )
            _print(run_revision(args.section))
            return 0
        if args.command == "editorial-audit":
            if args.section not in inputs.questions_by_section:
                raise BookEngineError(
                    "UNKNOWN_SECTION", f"section is not a question-bank section: {args.section}"
                )
            _print(run_editorial_audit(args.section))
            return 0
        if args.command == "approve-section":
            if args.section not in inputs.questions_by_section:
                raise BookEngineError("UNKNOWN_SECTION", f"section is not a question-bank section: {args.section}")
            _print(record_operator_approval(args.section, note=args.note, approver=args.approver))
            return 0
        if args.command == "freeze":
            if args.section not in inputs.questions_by_section:
                raise BookEngineError(
                    "UNKNOWN_SECTION", f"section is not a question-bank section: {args.section}"
                )
            _print(run_freeze(args.section))
            return 0
        if args.command in SECTION_COMMANDS:
            if args.section not in inputs.scope_by_id:
                raise BookEngineError(
                    "UNKNOWN_SECTION", f"section is not present in authoritative scope: {args.section}"
                )
            result = not_implemented(SECTION_COMMANDS[args.command], section_id=args.section)
        else:
            result = not_implemented(GLOBAL_COMMANDS[args.command])
        _print(result.to_dict())
        return 3
    except BookEngineError as exc:
        _print({"status": "BLOCKED", "reason_code": exc.code, "detail": str(exc), "details": exc.details})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
