"""Execute one deterministic batch through the existing Unified Ingest runner."""

from __future__ import annotations

import contextlib
import importlib
import shutil
import uuid
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from tunnelbookai.canonical.verifier import inspect_canonical
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.ids import document_id_for_file
from tunnelbookai.ingest.paths import PROJECT_ROOT
from tunnelbookai.ingest.runner import run_selected
from tunnelbookai.ingest.sources import manual_inbox, papercrawler_contract

from .models import CONTRACT_VERSION, PopulationState, SCHEMA_VERSION, atomic_json, load_object, now


@contextlib.contextmanager
def _ingest_root(root: Path):
    """Bind legacy module-level ingest paths to an explicit root for one serial run."""
    import tunnelbookai.ingest.paths as paths_module
    from tunnelbookai.ingest.classify import taxonomy as taxonomy_module
    from tunnelbookai.ingest.config import load_config as cached_load_config

    original_paths = paths_module.PATHS
    original_project_root = paths_module.PROJECT_ROOT
    isolated = paths_module.IngestPaths(root=root)
    modules = (
        "tunnelbookai.ingest.cli",
        "tunnelbookai.ingest.config",
        "tunnelbookai.ingest.original_archive",
        "tunnelbookai.ingest.pipeline",
        "tunnelbookai.ingest.staging",
        "tunnelbookai.ingest.sources.manual_inbox",
        "tunnelbookai.ingest.sources.papercrawler_contract",
    )
    saved: dict[str, Any] = {}
    paths_module.PATHS = isolated
    paths_module.PROJECT_ROOT = root
    for name in modules:
        module = importlib.import_module(name)
        if hasattr(module, "PATHS"):
            saved[name] = module.PATHS
            module.PATHS = isolated
    cached_load_config.cache_clear()
    taxonomy_module.load_taxonomy.cache_clear()
    try:
        yield
    finally:
        paths_module.PATHS = original_paths
        paths_module.PROJECT_ROOT = original_project_root
        for name, value in saved.items():
            importlib.import_module(name).PATHS = value
        cached_load_config.cache_clear()
        taxonomy_module.load_taxonomy.cache_clear()


def _canonical_projection(root: Path) -> dict[str, Any]:
    value = inspect_canonical(project_root=root).to_dict()
    if value["state"] != "READY":
        raise RuntimeError(f"population batch requires canonical READY, found {value['state']}")
    return {
        "state": value["state"],
        "manifest_sha256": value.get("manifest_sha256"),
        "corpus_digest": value.get("corpus_digest"),
    }


def _discover(root: Path, inventory: dict[str, Any], selected: set[str]):
    config = load_config()
    candidates = manual_inbox.discover(config, root / "incoming" / "manual" / "inbox")
    releases = {
        alias["release"]
        for row in inventory["documents"] if row["document_id"] in selected
        for alias in row["source_aliases"] if alias.get("release")
    }
    for release in sorted(releases):
        results = papercrawler_contract.discover(
            releases_root=root / "incoming" / "papercrawler" / "releases",
            release_id=str(release),
        )
        if len(results) != 1 or results[0].blockers:
            blockers = results[0].blockers if results else ["release_not_found"]
            raise RuntimeError(f"PaperCrawler release blocked: {release}: {blockers}")
        candidates.extend(results[0].accepted)
    found = []
    seen: set[tuple[str, str]] = set()
    for item in candidates:
        document_id, sha = document_id_for_file(item.input_path)
        if document_id not in selected:
            continue
        expected = next(row for row in inventory["documents"] if row["document_id"] == document_id)
        if sha != expected["sha256"]:
            raise RuntimeError(f"source changed since inventory: {document_id}")
        key = (document_id, str(item.input_path.resolve()))
        if key not in seen:
            found.append(item)
            seen.add(key)
    found_ids = {document_id_for_file(item.input_path)[0] for item in found}
    if found_ids != selected:
        raise RuntimeError(f"batch inputs missing: {sorted(selected - found_ids)}")
    return found


def run_batch(
    batch_path: Path | str, project_root: Path | str | None = None, *,
    resume: bool = True, force_reprocess: bool = False,
) -> dict[str, Any]:
    root = Path(project_root or PROJECT_ROOT).resolve()
    path = Path(batch_path)
    path = path if path.is_absolute() else root / path
    batch_root = (root / "audit" / "corpus_population" / "batches").resolve()
    if path.is_symlink() or not path.is_file() or path.resolve().parent != batch_root:
        raise ValueError("population batch must be a regular file in the batch root")
    batch = load_object(path)
    from .batching import _verify_batch
    _verify_batch(batch)
    run_id = str(batch.get("run_id") or "")
    run_path = root / "audit" / "corpus_population" / "runs" / f"{run_id}.json"
    run = load_object(run_path)
    if run.get("run_id") != run_id or batch["batch_id"] not in run.get("batch_ids", []):
        raise ValueError("population batch is not bound to its declared run")
    if run.get("inventory_id") != batch.get("inventory_id"):
        raise ValueError("population batch/run inventory mismatch")
    inventory_path = root / "audit" / "corpus_population" / "inventories" / f"{batch['inventory_id']}.json"
    inventory = load_object(inventory_path)
    from .batching import _verify_inventory, _verify_run
    _verify_inventory(inventory)
    _verify_run(run)
    before = _canonical_projection(root)
    if before != run["canonical_before"]:
        raise RuntimeError("canonical state changed since population planning")

    config = yaml.safe_load((root / "config" / "population.yaml").read_text(encoding="utf-8"))
    policy = config["batching"]
    source_bytes = int(batch["summary"]["source_bytes"])
    projected = source_bytes * int(policy["initial_processing_expansion_factor"])
    required_free = max(int(policy["minimum_free_bytes"]), projected * 3)
    free = shutil.disk_usage(root).free
    if free < required_free:
        raise RuntimeError(f"insufficient free space: required={required_free} available={free}")

    selected = {str(row["document_id"]) for row in batch["documents"]}
    with _ingest_root(root):
        inputs = _discover(root, inventory, selected)
    run["state"] = PopulationState.INGESTING.value
    run["updated_at"] = now()
    attempt_id = "CPE_" + uuid.uuid4().hex
    attempt_path = (
        root / "audit" / "corpus_population" / "attempts" / f"{attempt_id}.json"
    )
    attempt: dict[str, Any] = {
        "attempt_id": attempt_id,
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "run_id": run_id,
        "batch_id": batch["batch_id"],
        "status": "RUNNING",
        "started_at": now(),
        "canonical_before": before,
        "documents": {},
    }
    run.setdefault("attempt_ids", []).append(attempt_id)
    atomic_json(run_path, run)
    atomic_json(attempt_path, attempt)

    def checkpoint(outcome: dict[str, Any]) -> None:
        document_id = str(outcome["document_id"])
        run["documents"][document_id] = outcome
        attempt["documents"][document_id] = outcome
        run["updated_at"] = now()
        atomic_json(run_path, run)
        atomic_json(attempt_path, attempt)

    try:
        with _ingest_root(root):
            exit_code = run_selected(
                inputs,
                outcome_callback=checkpoint,
                resume=resume,
                force_reprocess=force_reprocess,
            )
    except BaseException as exc:
        attempt["status"] = "FAILED"
        attempt["error"] = f"{type(exc).__name__}: {exc}"[:1000]
        attempt["finished_at"] = now()
        attempt["summary"] = {
            "documents_checkpointed": len(attempt["documents"]),
            "dispositions": dict(sorted(Counter(
                str(row.get("disposition") or "UNKNOWN")
                for row in attempt["documents"].values()
            ).items())),
        }
        run["state"] = PopulationState.BLOCKED.value
        run["updated_at"] = now()
        if batch["batch_id"] not in run["failed_batches"]:
            run["failed_batches"].append(batch["batch_id"])
        atomic_json(run_path, run)
        atomic_json(attempt_path, attempt, readonly=True)
        raise
    try:
        after = _canonical_projection(root)
    except BaseException as exc:
        attempt["status"] = "FAILED"
        attempt["error"] = f"canonical post-check: {type(exc).__name__}: {exc}"[:1000]
        attempt["finished_at"] = now()
        run["state"] = PopulationState.BLOCKED.value
        run["updated_at"] = now()
        if batch["batch_id"] not in run["failed_batches"]:
            run["failed_batches"].append(batch["batch_id"])
        atomic_json(run_path, run)
        atomic_json(attempt_path, attempt, readonly=True)
        raise
    if after != before:
        attempt["status"] = "FAILED"
        attempt["error"] = "canonical identity changed during ingest batch"
        attempt["canonical_after"] = after
        attempt["finished_at"] = now()
        run["state"] = PopulationState.BLOCKED.value
        run["updated_at"] = now()
        if batch["batch_id"] not in run["failed_batches"]:
            run["failed_batches"].append(batch["batch_id"])
        atomic_json(run_path, run)
        atomic_json(attempt_path, attempt, readonly=True)
        raise RuntimeError("canonical identity changed during ingest batch")

    key = "completed_batches" if exit_code == 0 else "failed_batches"
    if batch["batch_id"] not in run[key]:
        run[key].append(batch["batch_id"])
    unresolved = [
        row for row in run["documents"].values()
        if row.get("disposition") in {"PENDING", "RECOVERY_REQUIRED", "FAILED", "NEEDS_REVIEW"}
        and not row.get("accounted_exclusion")
    ]
    if not unresolved:
        run["state"] = PopulationState.INGEST_ACCOUNTED.value
    elif exit_code:
        run["state"] = PopulationState.BLOCKED.value
    run["updated_at"] = now()
    atomic_json(run_path, run)
    attempt["status"] = "COMPLETED" if exit_code == 0 else "COMPLETED_WITH_FAILURES"
    attempt["exit_code"] = exit_code
    attempt["canonical_after"] = after
    attempt["finished_at"] = now()
    attempt["summary"] = {
        "documents_checkpointed": len(attempt["documents"]),
        "dispositions": dict(sorted(Counter(
            str(row.get("disposition") or "UNKNOWN")
            for row in attempt["documents"].values()
        ).items())),
    }
    atomic_json(attempt_path, attempt, readonly=True)
    return {
        "status": "COMPLETED" if exit_code == 0 else "COMPLETED_WITH_FAILURES",
        "exit_code": exit_code,
        "batch_id": batch["batch_id"],
        "run_id": run_id,
        "attempt_id": attempt_id,
        "canonical_preserved": True,
        "run_state": run["state"],
    }


__all__ = ["run_batch"]
