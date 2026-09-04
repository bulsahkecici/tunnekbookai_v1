#!/usr/bin/env python3
"""Promote quality-approved staging bundles toward the canonical corpus (task §47).

DEFAULT IS A DRY RUN. Nothing is written without an explicit `--apply`, and even then this
script refuses to touch `corpus/canonical/` unless `--target` names a different directory:
canonical promotion is owned by `scripts/08_final_corpus.py` and by a human decision, not by
the ingest engine (§2, §46).

    .venv/bin/python scripts/promote_staging.py                  # dry run, prints a plan
    .venv/bin/python scripts/promote_staging.py --document-id ING_...
    .venv/bin/python scripts/promote_staging.py --apply --target corpus/promoted_v2
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tunnelbookai.ingest.paths import PATHS, relpath          # noqa: E402
from tunnelbookai.ingest.staging import STAGING_VERSION, staging_root  # noqa: E402

CANONICAL_GUARD = "corpus/canonical"


def load_bundles(document_id: str | None) -> list[dict]:
    root = staging_root()
    if not root.is_dir():
        return []
    bundles: list[dict] = []
    for directory in sorted(root.iterdir()):
        if not directory.is_dir():
            continue
        if document_id and directory.name != document_id:
            continue
        manifest = directory / "bundle.json"
        if not manifest.is_file():
            bundles.append({"document_id": directory.name, "path": relpath(directory),
                            "eligible": False, "reason": "NO_BUNDLE_MANIFEST"})
            continue
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        reasons: list[str] = []
        if payload.get("quality_decision") != "GO":
            reasons.append(f"QUALITY_DECISION_{payload.get('quality_decision')}")
        if not payload.get("final_primary_section"):
            reasons.append("NO_FINAL_SECTION")
        if payload.get("chunk_quality_status") == "FAIL":
            reasons.append("CHUNK_QUALITY_FAIL")
        if not payload.get("original_sha256"):
            reasons.append("NO_ORIGINAL_SHA256")
        bundles.append({
            "document_id": payload.get("document_id", directory.name),
            "path": relpath(directory),
            "title": payload.get("title"),
            "format": payload.get("format"),
            "final_primary_section": payload.get("final_primary_section"),
            "final_evidence_level": payload.get("final_evidence_level"),
            "chunk_count": payload.get("chunk_count"),
            "eligible": not reasons,
            "reason": "ELIGIBLE" if not reasons else ";".join(reasons),
        })
    return bundles


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="promote_staging",
        description="Promote unified-ingest staging bundles. Dry run unless --apply.")
    parser.add_argument("--apply", action="store_true",
                        help="actually copy the bundles (default: dry run)")
    parser.add_argument("--target", default="corpus/promoted_v2",
                        help="destination directory; may never be corpus/canonical")
    parser.add_argument("--document-id", default=None)
    parser.add_argument("--json", action="store_true", help="print the plan as JSON")
    args = parser.parse_args(argv)

    target = (PATHS.root / args.target).resolve()
    canonical = (PATHS.root / CANONICAL_GUARD).resolve()
    if target == canonical or canonical in target.parents:
        print("REFUSED: this script never writes into corpus/canonical/ (task §2, §47).")
        return 2

    bundles = load_bundles(args.document_id)
    eligible = [b for b in bundles if b["eligible"]]
    blocked = [b for b in bundles if not b["eligible"]]

    plan = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mode": "apply" if args.apply else "dry-run",
        "staging_source": relpath(staging_root()),
        "staging_version": STAGING_VERSION,
        "target": relpath(target),
        "eligible": len(eligible),
        "blocked": len(blocked),
        "bundles": bundles,
    }

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print("TUNNELBOOKAI STAGING PROMOTION")
        print("=" * 40)
        print(f"Mode:            {plan['mode'].upper()}")
        print(f"Staging source:  {plan['staging_source']}")
        print(f"Target:          {plan['target']}")
        print(f"Eligible:        {len(eligible)}")
        print(f"Blocked:         {len(blocked)}")
        for bundle in bundles:
            mark = "+" if bundle["eligible"] else "-"
            print(f"  {mark} {bundle['document_id']}  "
                  f"section={bundle.get('final_primary_section') or '-':8} {bundle['reason']}")

    if not args.apply:
        print("\nDRY RUN — nothing was written. Re-run with --apply to copy the eligible bundles.")
        return 0

    copied = 0
    for bundle in eligible:
        source = PATHS.root / bundle["path"]
        destination = target / bundle["document_id"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
        copied += 1
    print(f"\nCopied {copied} bundle(s) into {relpath(target)}. Canonical corpus untouched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
