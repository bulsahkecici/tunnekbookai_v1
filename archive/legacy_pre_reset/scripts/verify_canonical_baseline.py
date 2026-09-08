#!/usr/bin/env python3
"""Recompute the canonical corpus integrity digest and fail on drift (task §2, §5, §91, §93).

Baseline captured 2026-09-02 in reports/unified_ingest_preimplementation_audit.md §5:

    canonical_md_count           = 214
    canonical_corpus_tree_digest = 6c49a13c0f3715ac54f44cb206a18096d596c80ad5ea47891dbeebd9bdef0470

The digest is sha256 over "".join(f"{sha256(file)}  {relpath}\n") for *.md files sorted
by POSIX relative path under corpus/canonical/.

The Unified Ingest Engine task must NOT change corpus/canonical/. Run this before and after
any ingest work; a non-zero exit means the frozen corpus was modified.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "corpus" / "canonical"

BASELINE_COUNT = 214
BASELINE_DIGEST = "6c49a13c0f3715ac54f44cb206a18096d596c80ad5ea47891dbeebd9bdef0470"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def tree_digest() -> tuple[str, int]:
    files = sorted((p for p in CANONICAL.rglob("*.md") if p.is_file()),
                   key=lambda p: p.relative_to(CANONICAL).as_posix())
    lines = "".join(f"{_sha256(p)}  {p.relative_to(CANONICAL).as_posix()}\n" for p in files)
    return hashlib.sha256(lines.encode("utf-8")).hexdigest(), len(files)


def main() -> int:
    digest, count = tree_digest()
    ok = digest == BASELINE_DIGEST and count == BASELINE_COUNT
    print(f"canonical_md_count:           {count} (baseline {BASELINE_COUNT})")
    print(f"canonical_corpus_tree_digest: {digest}")
    print(f"baseline:                     {BASELINE_DIGEST}")
    if ok:
        print("RESULT: PASS — canonical corpus unchanged")
        return 0
    print("RESULT: FAIL — canonical corpus differs from the frozen baseline")
    return 1


if __name__ == "__main__":
    sys.exit(main())
