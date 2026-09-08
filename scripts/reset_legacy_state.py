"""Idempotently verify the intentional empty-corpus bootstrap state.

This command deliberately does not delete source material. Destructive removal was a
one-time, recoverability-gated operation documented in reports/pre_reset_recoverability.md.
It recreates required empty-directory markers and then runs the authoritative reset gate.
"""

from __future__ import annotations

import json
from pathlib import Path

from shared.project_quality_gate import evaluate


ROOT = Path(__file__).resolve().parents[1]
MARKERS = (
    "corpus/canonical/.gitkeep",
    "corpus/staging/.gitkeep",
    "corpus/metadata/.gitkeep",
    "originals/.gitkeep",
    "processing/.gitkeep",
    "incoming/papercrawler/releases/.gitkeep",
    "incoming/quarantine/.gitkeep",
    "data/temporary/.gitkeep",
)


def main() -> int:
    for relative in MARKERS:
        marker = ROOT / relative
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch(exist_ok=True)
    result = evaluate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["decision"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
