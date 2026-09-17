from __future__ import annotations

import json
import os
import shutil
import threading
import unittest
import urllib.error
import urllib.request
from unittest import mock

from tests.population.test_population import PROJECT_ROOT, PopulationRepo
from tunnelbookai.dashboard.controller import (
    control_path,
    load_control,
    request_stop,
    resolve_run,
    run_projection,
    start_worker,
    stop_path,
)
from tunnelbookai.dashboard.server import DashboardServer, Handler
from tunnelbookai.dashboard.explorer import (
    document_projection,
    documents_projection,
    resolve_preview,
    review_projection,
    statistics_projection,
    update_review,
)
from tunnelbookai.population.batching import plan_batches
from tunnelbookai.population.inventory import build_inventory
from tunnelbookai.population.models import atomic_json


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.repo = PopulationRepo()
        inventory = build_inventory(self.repo.root, write=True)
        planned = plan_batches(inventory["inventory_path"], self.repo.root, write=True)
        self.run_path = self.repo.root / planned["run"]["run_path"]

    def tearDown(self):
        self.repo.close()

    def test_projection_and_control_are_persistent(self):
        selected = resolve_run(self.run_path, self.repo.root)
        payload = run_projection(selected, self.repo.root)
        self.assertEqual(payload["control"]["status"], "IDLE")
        self.assertEqual(payload["run"]["total_batches"], 1)
        self.assertEqual(payload["run"]["total_documents"], 2)
        self.assertTrue(control_path(self.repo.root).is_file())

    def test_stop_request_is_a_durable_file(self):
        control = load_control(self.run_path, self.repo.root)
        control.update({"status": "RUNNING", "worker_pid": os.getpid()})
        atomic_json(control_path(self.repo.root), control)
        result = request_stop(self.run_path, self.repo.root)
        self.assertEqual(result["status"], "STOP_REQUESTED")
        self.assertTrue(stop_path(self.repo.root).is_file())

    def test_start_uses_bound_run_and_resume_worker(self):
        class Process:
            pid = 43210

            def wait(self):
                return 0

        with mock.patch("subprocess.Popen", return_value=Process()) as popen:
            result = start_worker(self.run_path, self.repo.root)
        self.assertEqual(result["status"], "STARTING")
        command = popen.call_args.args[0]
        self.assertEqual(command[:3], [mock.ANY, "-m", "tunnelbookai.dashboard.worker"])
        self.assertIn(self.run_path.relative_to(self.repo.root).as_posix(), command)

    def test_explorer_lists_chunks_assets_statistics_and_reasons(self):
        run = json.loads(self.run_path.read_text(encoding="utf-8"))
        document_id = next(
            key for key, row in run["documents"].items() if row["disposition"] == "PENDING"
        )
        run["documents"][document_id].update({
            "disposition": "STAGED",
            "chunk_count": 1,
            "final_primary_section": "2.1",
            "warnings": ["CHART_EXTRACTION_DISABLED_BY_CONFIG", "CHUNK_UNDER_MIN:CH1:3"],
        })
        atomic_json(self.run_path, run)
        bundle = self.repo.root / "processing" / document_id
        (bundle / "normalized").mkdir(parents=True)
        (bundle / "chunks").mkdir()
        (bundle / "normalized/document.md").write_text("# Read only", encoding="utf-8")
        (bundle / "extraction_report.json").write_text(json.dumps({
            "page_count": 2,
            "tables": ["TABLE0001"],
            "figures": [],
            "charts": [],
            "slides": [],
            "sheets": [],
            "ocr_items": [],
            "text_char_count": 42,
            "normalized_markdown_path": f"processing/{document_id}/normalized/document.md",
            "capabilities": {"ocr": False},
            "warnings": ["CHART_EXTRACTION_DISABLED_BY_CONFIG"],
        }), encoding="utf-8")
        (bundle / "chunks/chunk_manifest.jsonl").write_text(json.dumps({
            "chunk_id": f"{document_id}_CH_1",
            "document_id": document_id,
            "chunk_type": "TEXT_CHUNK",
            "final_primary_section": "2.1",
            "ordinal": 1,
            "token_count": 3,
            "text": "tunnel evidence",
        }) + "\n", encoding="utf-8")

        listing = documents_projection(self.run_path, self.repo.root, disposition="STAGED")
        self.assertEqual(listing["total"], 1)
        detail = document_projection(self.run_path, self.repo.root, document_id)
        self.assertEqual(detail["chunk_items"][0]["text"], "tunnel evidence")
        self.assertIn("normalized/document.md", {row["name"] for row in detail["assets"]})
        stats = statistics_projection(self.run_path, self.repo.root)
        self.assertEqual(stats["assets"]["tables"], 1)
        self.assertEqual(stats["chunk_types"]["TEXT_CHUNK"], 1)
        self.assertEqual(stats["top_warnings"], [{"code": "CHUNK_UNDER_MIN", "count": 1}])
        self.assertEqual(stats["informational_warnings"], [
            {"code": "CHART_EXTRACTION_DISABLED_BY_CONFIG", "count": 1},
        ])
        self.assertIn("benzersiz belge", stats["warning_note"])

    def test_review_queue_is_persistent_without_moving_source(self):
        run = json.loads(self.run_path.read_text(encoding="utf-8"))
        document_id = next(
            key for key, row in run["documents"].items() if row["disposition"] == "PENDING"
        )
        run["documents"][document_id]["disposition"] = "RECOVERY_REQUIRED"
        atomic_json(self.run_path, run)
        source = self.repo.root / "incoming/manual/inbox/source.txt"
        before = source.read_bytes()
        queue = review_projection(self.run_path, self.repo.root)
        self.assertTrue(any(row["document_id"] == document_id for row in queue["documents"]))
        open_before = queue["open"]
        update_review(self.run_path, self.repo.root, document_id, "RESOLVED", "manual check")
        queue = review_projection(self.run_path, self.repo.root)
        self.assertEqual(queue["open"], open_before - 1)
        reviewed = next(row for row in queue["documents"] if row["document_id"] == document_id)
        self.assertEqual(reviewed["review_note"], "manual check")
        self.assertEqual(source.read_bytes(), before)

    def test_preview_rejects_traversal_and_symlinks(self):
        run = json.loads(self.run_path.read_text(encoding="utf-8"))
        document_id = next(iter(run["documents"]))
        bundle = self.repo.root / "processing" / document_id
        bundle.mkdir(parents=True)
        allowed = bundle / "document.md"
        allowed.write_text("safe", encoding="utf-8")
        resolved, kind = resolve_preview(self.repo.root, self.run_path, document_id, "document.md")
        self.assertEqual(resolved, allowed.resolve())
        self.assertEqual(kind, "text")
        with self.assertRaisesRegex(ValueError, "invalid preview path"):
            resolve_preview(self.repo.root, self.run_path, document_id, "../../config/ingest.yaml")
        symlink = bundle / "outside.md"
        try:
            symlink.symlink_to(self.repo.root / "README.md")
        except OSError:
            return
        with self.assertRaisesRegex(ValueError, "not found"):
            resolve_preview(self.repo.root, self.run_path, document_id, "outside.md")

    def test_http_status_and_control_token(self):
        try:
            server = DashboardServer(
                ("127.0.0.1", 0),
                Handler,
                project_root=self.repo.root,
                run_path=self.run_path,
            )
        except PermissionError:
            self.skipTest("runtime sandbox does not permit loopback sockets")
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            with urllib.request.urlopen(base + "/api/status", timeout=3) as response:
                payload = json.loads(response.read())
            self.assertIn("control_token", payload)
            with mock.patch("tunnelbookai.dashboard.server.search_index", return_value={
                "query": "tunnel cost", "results": [{"document_id": "ING_TEST"}],
            }) as search:
                with urllib.request.urlopen(
                    base + "/api/retrieval/search?q=tunnel%20cost&section=6&top_k=5",
                    timeout=3,
                ) as response:
                    retrieval = json.loads(response.read())
                self.assertEqual(retrieval["results"][0]["document_id"], "ING_TEST")
                search.assert_called_once_with(
                    "tunnel cost", self.repo.root, section="6", top_k=5,
                )
            request = urllib.request.Request(base + "/api/start", data=b"{}", method="POST")
            with self.assertRaises(urllib.error.HTTPError) as raised:
                urllib.request.urlopen(request, timeout=3)
            self.assertEqual(raised.exception.code, 403)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
