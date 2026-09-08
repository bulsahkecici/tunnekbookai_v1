#!/usr/bin/env python3
"""Recompute deterministic coverage/reconciliation views without model calls."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "crawler" / "src"))

import coverage_policy


def main() -> int:
    output = ROOT / "data" / "downloads"
    index_path = output / "classification_index.jsonl"
    audit_path = output / "audit" / "classification_audit.json"
    rows = [json.loads(line) for line in index_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    audit["coverage"] = coverage_policy.calculate(rows)
    audit["coverage_recomputed_at"] = datetime.now(timezone.utc).isoformat()
    audit["coverage_source_sha256"] = hashlib.sha256(index_path.read_bytes()).hexdigest()
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(audit["coverage"]["totals"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
