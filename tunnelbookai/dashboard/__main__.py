from __future__ import annotations

import argparse

from .server import serve


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m tunnelbookai.dashboard")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--run", help="population run JSON; defaults to the newest run")
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        parser.error("dashboard may bind only to a loopback host")
    serve(host=args.host, port=args.port, run_path=args.run)
    return 0


raise SystemExit(main())
