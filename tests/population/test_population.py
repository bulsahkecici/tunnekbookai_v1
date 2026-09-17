from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tunnelbookai.population.batching import plan_batches
from tunnelbookai.population.audit import build_staging_audit
from tunnelbookai.population.inventory import build_inventory
from tunnelbookai.population.manual_import import apply_import_plan, build_import_plan
from tunnelbookai.population.models import atomic_json
from tunnelbookai.population.runner import run_batch
from tunnelbookai.ingest.cli import STOPPED_EXIT_CODE


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class PopulationRepo:
    def __init__(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        shutil.copytree(PROJECT_ROOT / "config", self.root / "config")
        shutil.copytree(PROJECT_ROOT / "book", self.root / "book")
        for relative in (
            "incoming/manual/inbox", "incoming/papercrawler/releases", "originals",
            "processing", "corpus/staging", "corpus/canonical", "audit", "reports",
        ):
            (self.root / relative).mkdir(parents=True, exist_ok=True)
        (self.root / "incoming/manual/inbox/source.txt").write_text("tunnel evidence\n", encoding="utf-8")
        (self.root / "incoming/manual/inbox/archive.zip").write_bytes(b"not an OOXML package")

    def close(self):
        self.temporary.cleanup()


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.repo = PopulationRepo()

    def tearDown(self):
        self.repo.close()

    def test_inventory_is_deterministic_and_reports_unsupported(self):
        first = build_inventory(self.repo.root, write=True)
        second = build_inventory(self.repo.root, write=False)
        self.assertEqual(first["inventory_id"], second["inventory_id"])
        self.assertEqual(first["summary"]["unique_documents"], 2)
        self.assertEqual(first["summary"]["by_classification"], {"NEW": 1, "UNSUPPORTED": 1})

    def test_batch_plan_excludes_unsupported_and_is_deterministic(self):
        inventory = build_inventory(self.repo.root, write=True)
        first = plan_batches(inventory["inventory_path"], self.repo.root, write=False)
        second = plan_batches(inventory["inventory_path"], self.repo.root, write=False)
        self.assertEqual(
            [row["batch_id"] for row in first["batches"]],
            [row["batch_id"] for row in second["batches"]],
        )
        self.assertEqual(first["summary"]["documents"], 1)
        self.assertEqual(first["summary"]["batches"], 1)

    def test_staging_audit_is_blocked_until_ingest_is_accounted(self):
        inventory = build_inventory(self.repo.root, write=True)
        planned = plan_batches(inventory["inventory_path"], self.repo.root, write=True)
        with self.assertRaisesRegex(RuntimeError, "INGEST_ACCOUNTED"):
            build_staging_audit(planned["run"]["run_path"], self.repo.root)

    def test_batch_runner_checkpoints_one_serial_attempt(self):
        from tests.canonical.fixtures import SyntheticRepo
        from tunnelbookai.canonical.paths import CanonicalContext
        from tunnelbookai.canonical.promotion import apply_plan, build_plan

        repo = SyntheticRepo()
        try:
            shutil.copytree(PROJECT_ROOT / "config", repo.root / "config", dirs_exist_ok=True)
            (repo.root / "incoming/manual/inbox/source.txt").write_text(
                "tunnel evidence\n", encoding="utf-8"
            )
            context = CanonicalContext.load(repo.root)
            canonical_plan = build_plan(context=context)
            apply_plan(
                repo.root / f"audit/canonical_promotions/plans/{canonical_plan.plan_id}.json",
                approve=canonical_plan.plan_id,
                context=context,
            )
            inventory = build_inventory(repo.root, write=True)
            planned = plan_batches(inventory["inventory_path"], repo.root, write=True)
            batch = planned["batches"][0]
            result = run_batch(batch["batch_path"], repo.root, resume=True)
            self.assertEqual(result["exit_code"], 0)
            self.assertTrue(result["canonical_preserved"])
            run = json.loads(
                (repo.root / planned["run"]["run_path"]).read_text(encoding="utf-8")
            )
            self.assertEqual(run["attempt_ids"], [result["attempt_id"]])
            selected_id = next(
                row["document_id"] for row in inventory["documents"]
                if row["classification"] == "NEW"
            )
            self.assertNotEqual(run["documents"][selected_id]["disposition"], "PENDING")
            attempt = repo.root / "audit/corpus_population/attempts" / f"{result['attempt_id']}.json"
            self.assertEqual(json.loads(attempt.read_text())["status"], "COMPLETED")
        finally:
            repo.close()

    def test_safe_stop_pauses_without_completing_batch_and_resume_finishes(self):
        from tests.canonical.fixtures import SyntheticRepo
        from tunnelbookai.canonical.paths import CanonicalContext
        from tunnelbookai.canonical.promotion import apply_plan, build_plan

        repo = SyntheticRepo()
        try:
            shutil.copytree(PROJECT_ROOT / "config", repo.root / "config", dirs_exist_ok=True)
            (repo.root / "incoming/manual/inbox/source.txt").write_text(
                "checkpoint evidence\n", encoding="utf-8"
            )
            context = CanonicalContext.load(repo.root)
            canonical_plan = build_plan(context=context)
            apply_plan(
                repo.root / f"audit/canonical_promotions/plans/{canonical_plan.plan_id}.json",
                approve=canonical_plan.plan_id,
                context=context,
            )
            inventory = build_inventory(repo.root, write=True)
            planned = plan_batches(inventory["inventory_path"], repo.root, write=True)
            batch = planned["batches"][0]
            selected_id = batch["documents"][0]["document_id"]

            def paused_run(_inputs, **kwargs):
                kwargs["progress_callback"]({"event": "DOCUMENT_STARTED", "document_id": selected_id})
                kwargs["outcome_callback"]({
                    "document_id": selected_id,
                    "disposition": "STAGED",
                    "engine_state": "EMBEDDING_READY",
                })
                return STOPPED_EXIT_CODE

            with mock.patch("tunnelbookai.population.runner.run_selected", side_effect=paused_run):
                paused = run_batch(batch["batch_path"], repo.root, stop_requested=lambda: True)
            self.assertEqual(paused["status"], "PAUSED")
            run_path = repo.root / planned["run"]["run_path"]
            run = json.loads(run_path.read_text(encoding="utf-8"))
            self.assertEqual(run["state"], "PAUSED")
            self.assertNotIn(batch["batch_id"], run["completed_batches"])
            self.assertEqual(run["documents"][selected_id]["disposition"], "STAGED")

            def completed_run(_inputs, **kwargs):
                kwargs["outcome_callback"]({
                    "document_id": selected_id,
                    "disposition": "ALREADY_PROCESSED",
                    "engine_state": "EMBEDDING_READY",
                })
                return 0

            with mock.patch("tunnelbookai.population.runner.run_selected", side_effect=completed_run):
                resumed = run_batch(batch["batch_path"], repo.root, resume=True)
            self.assertEqual(resumed["status"], "COMPLETED")
            run = json.loads(run_path.read_text(encoding="utf-8"))
            self.assertIn(batch["batch_id"], run["completed_batches"])
            attempt_statuses = [
                json.loads((repo.root / "audit/corpus_population/attempts" / f"{item}.json").read_text())["status"]
                for item in run["attempt_ids"]
            ]
            self.assertEqual(attempt_statuses, ["PAUSED", "COMPLETED"])
        finally:
            repo.close()

    def test_failed_batch_resume_selects_only_unresolved_checkpoints(self):
        from tests.canonical.fixtures import SyntheticRepo
        from tunnelbookai.canonical.paths import CanonicalContext
        from tunnelbookai.canonical.promotion import apply_plan, build_plan

        repo = SyntheticRepo()
        try:
            shutil.copytree(PROJECT_ROOT / "config", repo.root / "config", dirs_exist_ok=True)
            (repo.root / "incoming/manual/inbox/source.txt").write_text(
                "retry checkpoint evidence\n", encoding="utf-8"
            )
            context = CanonicalContext.load(repo.root)
            canonical_plan = build_plan(context=context)
            apply_plan(
                repo.root / f"audit/canonical_promotions/plans/{canonical_plan.plan_id}.json",
                approve=canonical_plan.plan_id,
                context=context,
            )
            inventory = build_inventory(repo.root, write=True)
            planned = plan_batches(inventory["inventory_path"], repo.root, write=True)
            batch = planned["batches"][0]
            run_path = repo.root / planned["run"]["run_path"]
            run = json.loads(run_path.read_text(encoding="utf-8"))
            document_id = batch["documents"][0]["document_id"]
            run["documents"][document_id] = {
                "document_id": document_id,
                "disposition": "STAGED",
                "engine_state": "STAGED",
                "chunk_quality_status": "FAIL",
            }
            atomic_json(run_path, run)

            with mock.patch("tunnelbookai.population.runner.run_selected", return_value=0) as selected:
                result = run_batch(batch["batch_path"], repo.root, resume=True)

            self.assertEqual(result["status"], "COMPLETED")
            self.assertEqual(selected.call_args.args[0], [])
        finally:
            repo.close()

    def test_batch_rejects_config_changed_after_inventory(self):
        from tests.canonical.fixtures import SyntheticRepo
        from tunnelbookai.canonical.paths import CanonicalContext
        from tunnelbookai.canonical.promotion import apply_plan, build_plan

        repo = SyntheticRepo()
        try:
            shutil.copytree(PROJECT_ROOT / "config", repo.root / "config", dirs_exist_ok=True)
            (repo.root / "incoming/manual/inbox/source.txt").write_text(
                "pinned configuration evidence\n", encoding="utf-8"
            )
            context = CanonicalContext.load(repo.root)
            canonical_plan = build_plan(context=context)
            apply_plan(
                repo.root / f"audit/canonical_promotions/plans/{canonical_plan.plan_id}.json",
                approve=canonical_plan.plan_id,
                context=context,
            )
            inventory = build_inventory(repo.root, write=True)
            planned = plan_batches(inventory["inventory_path"], repo.root, write=True)
            batch = planned["batches"][0]
            classification = repo.root / "config/classification.yaml"
            classification.write_text(
                classification.read_text(encoding="utf-8") + "\n# changed after planning\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                RuntimeError, "config changed since population inventory: config/classification.yaml"
            ):
                run_batch(batch["batch_path"], repo.root)

            run = json.loads(
                (repo.root / planned["run"]["run_path"]).read_text(encoding="utf-8")
            )
            self.assertEqual(run["attempt_ids"], [])
        finally:
            repo.close()

    def test_default_manual_discovery_does_not_include_parent_files(self):
        from tunnelbookai.ingest.config import IngestConfig
        from tunnelbookai.ingest.sources.manual_inbox import discover

        (self.repo.root / "incoming/manual/outside.txt").write_text("outside", encoding="utf-8")
        values = {}
        import yaml
        for name in ("ingest", "ocr", "vision", "metadata", "classification", "quality_gate", "chunking", "models"):
            values[name] = yaml.safe_load((self.repo.root / "config" / f"{name}.yaml").read_text()) or {}
        config = IngestConfig(**values)
        found = discover(config, self.repo.root / "incoming/manual/inbox")
        self.assertNotIn("outside.txt", {path.input_path.name for path in found})


class ManualImportTests(unittest.TestCase):
    def setUp(self):
        self.repo = PopulationRepo()
        self.source_temp = tempfile.TemporaryDirectory()
        self.source = Path(self.source_temp.name)
        (self.source / "nested").mkdir()
        (self.source / "nested/report.pdf").write_bytes(b"%PDF synthetic")

    def tearDown(self):
        self.source_temp.cleanup()
        self.repo.close()

    def test_plan_apply_preserves_tree_and_is_idempotent(self):
        plan = build_import_plan(self.source, self.repo.root, write=True)
        result = apply_import_plan(
            self.source, plan["plan_path"], approve=plan["plan_id"], project_root=self.repo.root
        )
        self.assertEqual(result["status"], "APPLIED")
        self.assertEqual(
            (self.repo.root / "incoming/manual/inbox/nested/report.pdf").read_bytes(),
            b"%PDF synthetic",
        )
        second = build_import_plan(self.source, self.repo.root, write=False)
        self.assertEqual(second["summary"]["idempotent"], 1)

    def test_collision_fails_closed(self):
        destination = self.repo.root / "incoming/manual/inbox/nested/report.pdf"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(b"different")
        plan = build_import_plan(self.source, self.repo.root, write=False)
        self.assertFalse(plan["applicable"])
        self.assertEqual(plan["summary"]["collisions"], 1)

    def test_symlink_is_reported_and_not_planned(self):
        outside = self.source / "outside.pdf"
        outside.write_bytes(b"outside")
        link = self.source / "linked.pdf"
        link.symlink_to(outside)
        plan = build_import_plan(self.source, self.repo.root, write=False)
        self.assertIn({"path": "linked.pdf", "reason": "SYMLINK"}, plan["ignored"])
        self.assertNotIn("linked.pdf", {row["path"] for row in plan["records"]})

    def test_symlink_archive_root_is_rejected(self):
        link = self.source.parent / "source-link"
        link.symlink_to(self.source, target_is_directory=True)
        try:
            with self.assertRaisesRegex(ValueError, "must not be a symlink"):
                build_import_plan(link, self.repo.root, write=False)
        finally:
            link.unlink(missing_ok=True)


class IngestSafetyTests(unittest.TestCase):
    def setUp(self):
        from tests.canonical.fixtures import SyntheticRepo

        self.repo = SyntheticRepo()

    def tearDown(self):
        self.repo.close()

    def test_already_canonical_input_is_skipped_before_any_upstream_write(self):
        from tunnelbookai.canonical.paths import CanonicalContext
        from tunnelbookai.canonical.promotion import apply_plan, build_plan
        from tunnelbookai.canonical.verifier import inspect_canonical
        from tunnelbookai.ingest import cli
        from tunnelbookai.ingest.ids import sha256_file
        from tunnelbookai.ingest.paths import IngestPaths
        from tunnelbookai.ingest.sources import DiscoveredInput

        context = CanonicalContext.load(self.repo.root)
        plan = build_plan(context=context)
        apply_plan(
            self.repo.root / f"audit/canonical_promotions/plans/{plan.plan_id}.json",
            approve=plan.plan_id,
            context=context,
        )
        original_json = self.repo.root / f"originals/{self.repo.document_id}/original.json"
        before = sha256_file(original_json)
        source = next((self.repo.root / "originals" / self.repo.document_id).glob("source.*"))
        item = DiscoveredInput(
            input_path=source,
            source_kind="MANUAL_INTERNAL",
            provenance={"source_kind": "MANUAL_INTERNAL"},
        )
        paths = IngestPaths(self.repo.root)
        with mock.patch.object(cli, "PATHS", paths):
            code = cli._run([item], [], SimpleNamespace(force_reprocess=False))
        self.assertEqual(code, 0)
        self.assertEqual(sha256_file(original_json), before)
        self.assertTrue(inspect_canonical(project_root=self.repo.root).ready)

    def test_terminal_state_requires_complete_artifacts(self):
        from tunnelbookai.ingest import cli
        from tunnelbookai.ingest.ids import sha256_file
        from tunnelbookai.ingest.paths import IngestPaths
        from tunnelbookai.ingest.state import IngestState

        paths = IngestPaths(self.repo.root)
        source = next((self.repo.root / "originals" / self.repo.document_id).glob("source.*"))
        state = IngestState(self.repo.root / "audit/ingest_state.jsonl")
        with mock.patch.object(cli, "PATHS", paths):
            self.assertTrue(cli._terminal_artifacts_complete(state, self.repo.document_id, sha256_file(source)))
            (self.repo.root / f"processing/{self.repo.document_id}/chunks/embedding_ready.jsonl").unlink()
            self.assertFalse(cli._terminal_artifacts_complete(state, self.repo.document_id, sha256_file(source)))


class AuditTests(unittest.TestCase):
    def test_staging_audit_is_deterministic_and_builds_selector(self):
        from tests.canonical.fixtures import SyntheticRepo

        repo = SyntheticRepo()
        try:
            shutil.copytree(PROJECT_ROOT / "config", repo.root / "config", dirs_exist_ok=True)
            source = next((repo.root / "originals" / repo.document_id).glob("source.*"))
            shutil.copyfile(source, repo.root / "incoming/manual/inbox/candidate.pdf")
            inventory = build_inventory(repo.root, write=True)
            planned = plan_batches(inventory["inventory_path"], repo.root, write=True)
            run_path = repo.root / planned["run"]["run_path"]
            run = json.loads(run_path.read_text(encoding="utf-8"))
            run["documents"][repo.document_id] = {
                "disposition": "ALREADY_PROCESSED",
                "engine_state": "EMBEDDING_READY",
            }
            run["state"] = "INGEST_ACCOUNTED"
            atomic_json(run_path, run)
            first = build_staging_audit(run_path, repo.root, write=False)
            second = build_staging_audit(run_path, repo.root, write=True)
            self.assertEqual(first["audit_id"], second["audit_id"])
            self.assertEqual(second["canonical_actions"], {"PROMOTE": 1})
            self.assertEqual(second["chunks_total"], 1)
            self.assertEqual(second["retrieval_ready_chunks"], 1)
            self.assertEqual(len(second["promotion_batches"]), 1)
            self.assertEqual(second["promotion_batches"][0]["document_ids"], [repo.document_id])
        finally:
            repo.close()


if __name__ == "__main__":
    unittest.main()
