"""Dependency-free, loopback-only HTTP server for the operations dashboard."""

from __future__ import annotations

import json
import mimetypes
import secrets
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

from tunnelbookai.book.errors import BookEngineError
from tunnelbookai.book.retrieval import inspect_index, search_index
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.model_capability import probe
from tunnelbookai.ingest.paths import PROJECT_ROOT

from .controller import recent_logs, request_stop, resolve_run, run_projection, start_worker
from .explorer import (
    document_projection,
    documents_projection,
    resolve_preview,
    review_projection,
    statistics_projection,
    update_review,
)
from .improvements import load_state as load_improvement_state
from .improvements import start_worker as start_improvement_worker

STATIC = Path(__file__).resolve().parent / "static"
MIME = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8"}


class DashboardServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address, handler, *, project_root: Path, run_path: Path):
        super().__init__(address, handler)
        self.project_root = project_root
        self.run_path = run_path
        self.control_token = secrets.token_urlsafe(32)
        self.action_lock = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    server: DashboardServer

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _loopback_host(self) -> bool:
        host = (self.headers.get("Host") or "").lower()
        hostname = host.rsplit(":", 1)[0].strip("[]")
        return hostname in {"127.0.0.1", "localhost", "::1"}

    def _guard_host(self) -> bool:
        if self._loopback_host():
            return True
        self._json({"error": "dashboard accepts loopback hosts only"}, HTTPStatus.FORBIDDEN)
        return False

    def _json(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(body)

    def _static(self, name: str) -> None:
        path = STATIC / name
        if not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", MIME[path.suffix])
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(body)

    def _preview(self, document_id: str, relative_path: str) -> None:
        try:
            path, kind = resolve_preview(
                self.server.project_root, self.server.run_path, document_id, relative_path
            )
        except ValueError as exc:
            self._json({"error": str(exc)}, HTTPStatus.NOT_FOUND)
            return
        body = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if kind == "text":
            content_type = f"{content_type}; charset=utf-8"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "private, max-age=30")
        self.send_header("Content-Disposition", f'inline; filename="{path.name.replace(chr(34), "")}"')
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if not self._guard_host():
            return
        parsed = urlsplit(self.path)
        query = parse_qs(parsed.query)
        path = parsed.path
        if path in {"/", "/index.html"}:
            self._static("index.html")
        elif path == "/app.js":
            self._static("app.js")
        elif path == "/styles.css":
            self._static("styles.css")
        elif path == "/api/status":
            payload = run_projection(self.server.run_path, self.server.project_root)
            payload["control_token"] = self.server.control_token
            self._json(payload)
        elif path == "/api/logs":
            self._json({"lines": recent_logs(self.server.project_root)})
        elif path == "/api/models":
            self._json(probe(load_config()))
        elif path == "/api/retrieval/status":
            self._json(inspect_index(self.server.project_root).to_dict())
        elif path == "/api/retrieval/search":
            query_text = (query.get("q") or [""])[0].strip()
            section = (query.get("section") or [""])[0].strip() or None
            try:
                top_k = int((query.get("top_k") or ["10"])[0])
                if len(query_text) > 1000:
                    raise ValueError("search query may not exceed 1000 characters")
                self._json(search_index(
                    query_text,
                    self.server.project_root,
                    section=section,
                    top_k=top_k,
                ))
            except ValueError as exc:
                self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            except BookEngineError as exc:
                self._json({"error": str(exc)}, HTTPStatus.SERVICE_UNAVAILABLE)
        elif path == "/api/documents":
            try:
                self._json(documents_projection(
                    self.server.run_path,
                    self.server.project_root,
                    query=(query.get("q") or [""])[0],
                    disposition=(query.get("disposition") or ["ALL"])[0],
                    page=int((query.get("page") or ["1"])[0]),
                    page_size=int((query.get("page_size") or ["50"])[0]),
                ))
            except (TypeError, ValueError) as exc:
                self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        elif path.startswith("/api/documents/"):
            document_id = path.removeprefix("/api/documents/")
            try:
                self._json(document_projection(
                    self.server.run_path, self.server.project_root, document_id
                ))
            except ValueError as exc:
                self._json({"error": str(exc)}, HTTPStatus.NOT_FOUND)
        elif path == "/api/statistics":
            self._json(statistics_projection(self.server.run_path, self.server.project_root))
        elif path == "/api/review":
            self._json(review_projection(self.server.run_path, self.server.project_root))
        elif path == "/api/improvements":
            self._json(load_improvement_state(self.server.run_path, self.server.project_root))
        elif path == "/api/preview":
            self._preview(
                (query.get("document_id") or [""])[0],
                (query.get("path") or [""])[0],
            )
        elif path == "/healthz":
            self._json({"status": "ok"})
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        if not self._guard_host():
            return
        if self.headers.get("X-TunnelBookAI-Control") != self.server.control_token:
            self._json({"error": "invalid control token"}, HTTPStatus.FORBIDDEN)
            return
        parsed = urlsplit(self.path)
        length = int(self.headers.get("Content-Length") or 0)
        if length > 4096:
            self._json({"error": "request too large"}, HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
            return
        body: dict[str, Any] = {}
        if length:
            try:
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict):
                    raise ValueError
            except (ValueError, json.JSONDecodeError):
                self._json({"error": "invalid JSON body"}, HTTPStatus.BAD_REQUEST)
                return
        try:
            with self.server.action_lock:
                if parsed.path in {"/api/start", "/api/resume"}:
                    value = start_worker(self.server.run_path, self.server.project_root)
                elif parsed.path == "/api/stop":
                    value = request_stop(self.server.run_path, self.server.project_root)
                elif parsed.path == "/api/review":
                    value = update_review(
                        self.server.run_path,
                        self.server.project_root,
                        str(body.get("document_id") or ""),
                        str(body.get("status") or ""),
                        str(body.get("note") or ""),
                    )
                elif parsed.path == "/api/improvements/start":
                    value = start_improvement_worker(
                        self.server.run_path, self.server.project_root
                    )
                else:
                    self.send_error(HTTPStatus.NOT_FOUND)
                    return
            self._json({"control": value})
        except (RuntimeError, ValueError) as exc:
            self._json({"error": str(exc)}, HTTPStatus.CONFLICT)


def serve(*, host: str = "127.0.0.1", port: int = 8765, run_path: str | None = None) -> None:
    project_root = PROJECT_ROOT.resolve()
    selected_run = resolve_run(run_path, project_root)
    server = DashboardServer((host, port), Handler, project_root=project_root, run_path=selected_run)
    print(f"TunnelBookAI dashboard: http://{host}:{server.server_port}", flush=True)
    print(f"Run: {selected_run.relative_to(project_root)}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


__all__ = ["DashboardServer", "Handler", "serve"]
