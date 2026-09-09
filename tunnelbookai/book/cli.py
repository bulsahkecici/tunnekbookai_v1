"""Operator CLI for validated book inputs and declared foundation stages."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .errors import BookEngineError
from .inputs import BookInputs, load_book_inputs
from .stages import not_implemented
from .status import build_status


SECTION_COMMANDS = {
    "evidence-audit": "PREWRITING_EVIDENCE_AUDIT",
    "prepare": "SECTION_EVIDENCE_PACKET",
    "write": "SECTION_WRITER",
    "evidence-review": "POSTWRITING_EVIDENCE_AUDIT",
    "coverage-audit": "QUESTION_COVERAGE_AUDIT",
    "editorial-audit": "EDITORIAL_AUDIT",
    "freeze": "SECTION_FREEZE",
}
GLOBAL_COMMANDS = {
    "build-index": "BOOK_RETRIEVAL_INDEX",
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
    for name in SECTION_COMMANDS:
        child = sub.add_parser(name)
        child.add_argument("--section", required=True)
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
        inputs = load_book_inputs()
        if args.command == "validate":
            _print(_validation_payload(inputs), json_output=args.json)
            return 0
        if args.command == "status":
            _print(build_status(inputs), json_output=True)
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
