"""Background entry point for targeted warning-driven improvements."""

from __future__ import annotations

import argparse

from tunnelbookai.ingest.paths import PROJECT_ROOT

from .improvements import execute


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    return execute(args.run, PROJECT_ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
