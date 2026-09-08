#!/usr/bin/env python3
"""Verify the exact loopback models configured for TunnelBookAI."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tunnelbookai.ingest.config import load_config  # noqa: E402
from tunnelbookai.ingest.model_capability import AVAILABLE, probe  # noqa: E402


def main() -> int:
    result = probe(load_config())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["decision"] == AVAILABLE else 2


if __name__ == "__main__":
    raise SystemExit(main())
