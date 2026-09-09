#!/usr/bin/env python3
"""Compatibility entry point; canonical authority lives in tunnelbookai.canonical."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tunnelbookai.canonical.cli import main as canonical_main  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="promote_staging")
    parser.add_argument("--document-id", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--apply", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--target", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.apply or args.target:
        print(json.dumps({
            "status": "BLOCKED",
            "reason_code": "LEGACY_PROMOTION_INTERFACE_RETIRED",
            "detail": "Use python -m tunnelbookai.canonical plan, then apply with --plan and --approve.",
        }, indent=2))
        return 2
    forwarded = ["plan"]
    for document_id in args.document_id:
        forwarded += ["--document-id", document_id]
    if args.json:
        forwarded.append("--json")
    return canonical_main(forwarded)


if __name__ == "__main__":
    raise SystemExit(main())
