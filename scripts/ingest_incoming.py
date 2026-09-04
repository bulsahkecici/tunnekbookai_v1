#!/usr/bin/env python3
"""Thin entrypoint for the Unified Ingest Engine. See tunnelbookai/ingest/cli.py.

Run with the project venv:  .venv/bin/python scripts/ingest_incoming.py --source all --dry-run
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

if sys.version_info[:2] >= (3, 14):
    sys.stderr.write(
        "warning: the ingest engine expects Python 3.12 (.venv). "
        f"Running under {sys.version.split()[0]}.\n"
    )

from tunnelbookai.ingest.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
