"""Deterministic population and canonical-promotion batch manifests."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from tunnelbookai.ingest.paths import PROJECT_ROOT

from .models import CONTRACT_VERSION, SCHEMA_VERSION, PopulationState, atomic_json, identity, load_object, now


def _config(root: Path) -> dict[str, Any]:
    value = yaml.safe_load((root / "config" / "population.yaml").read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _inventory_semantic(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: payload[key]
        for key in (
            "schema_version", "contract_version", "config_identities", "canonical_before",
            "documents", "unreadable", "manual_ignored", "manual_summary", "exact_sha_groups",
            "papercrawler_releases", "ledger_only",
        )
    }


def _verify_inventory(payload: dict[str, Any]) -> None:
    expected = {
        "inventory_id", "schema_version", "contract_version", "config_identities",
        "canonical_before", "documents", "unreadable", "manual_ignored", "manual_summary",
        "exact_sha_groups", "papercrawler_releases", "ledger_only", "generated_at", "summary",
    }
    if set(payload) != expected:
        raise ValueError("inventory fields differ from the population schema")
    if payload.get("schema_version") != SCHEMA_VERSION or payload.get("contract_version") != CONTRACT_VERSION:
        raise ValueError("unsupported population inventory schema")
    if not isinstance(payload.get("documents"), list) or not isinstance(payload.get("summary"), dict):
        raise ValueError("invalid population inventory field types")
    if payload.get("inventory_id") != identity("CPI_", _inventory_semantic(payload)):
        raise ValueError("inventory identity mismatch")


def _run_semantic(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: payload[key]
        for key in (
            "schema_version", "contract_version", "inventory_id", "canonical_before",
            "batch_ids",
        )
    }


def _verify_run(payload: dict[str, Any]) -> None:
    expected = {
        "run_id", "schema_version", "contract_version", "inventory_id", "canonical_before",
        "batch_ids", "created_at", "updated_at", "state", "documents", "completed_batches",
        "failed_batches", "attempt_ids", "staging_audit_ids", "promotion_plan_ids",
        "canonical_after",
    }
    if set(payload) != expected:
        raise ValueError("population run fields differ from the population schema")
    if payload.get("schema_version") != SCHEMA_VERSION or payload.get("contract_version") != CONTRACT_VERSION:
        raise ValueError("unsupported population run schema")
    if not isinstance(payload.get("documents"), dict) or not isinstance(payload.get("batch_ids"), list):
        raise ValueError("invalid population run field types")
    if payload.get("run_id") != identity("CPR_", _run_semantic(payload)):
        raise ValueError("population run identity mismatch")


def _verify_batch(payload: dict[str, Any]) -> None:
    expected = {
        "batch_id", "schema_version", "contract_version", "inventory_id", "source_group",
        "processing_class", "ordinal", "documents", "generated_at", "status", "summary",
        "run_id",
    }
    if set(payload) != expected:
        raise ValueError("population batch fields differ from the population schema")
    if payload.get("schema_version") != SCHEMA_VERSION or payload.get("contract_version") != CONTRACT_VERSION:
        raise ValueError("unsupported population batch schema")
    if not isinstance(payload.get("documents"), list) or not payload["documents"]:
        raise ValueError("population batch documents must be a non-empty list")
    semantic = {
        key: payload[key]
        for key in (
            "schema_version", "contract_version", "inventory_id", "source_group",
            "processing_class", "ordinal", "documents",
        )
    }
    if payload.get("batch_id") != identity("CPB_", semantic):
        raise ValueError("population batch identity mismatch")


def _group(document: dict[str, Any], heavy: set[str]) -> tuple[str, str]:
    aliases = document["source_aliases"]
    if any(row["source_kind"] == "MANUAL_INTERNAL" for row in aliases):
        source_group = "manual"
    else:
        source_group = "papercrawler:" + str(next(row["release"] for row in aliases if row.get("release")))
    return source_group, "heavy" if document["format"] in heavy else "light"


def _pack(rows: list[dict[str, Any]], *, max_documents: int, max_bytes: int) -> list[list[dict[str, Any]]]:
    batches: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_bytes = 0
    for row in sorted(rows, key=lambda item: item["document_id"]):
        size = int(row.get("size") or 0)
        if current and (len(current) >= max_documents or current_bytes + size > max_bytes):
            batches.append(current)
            current, current_bytes = [], 0
        current.append(row)
        current_bytes += size
        if size > max_bytes:
            batches.append(current)
            current, current_bytes = [], 0
    if current:
        batches.append(current)
    return batches


def plan_batches(
    inventory_path: Path | str, project_root: Path | str | None = None, *, write: bool = True,
) -> dict[str, Any]:
    root = Path(project_root or PROJECT_ROOT).resolve()
    source = Path(inventory_path)
    source = source if source.is_absolute() else root / source
    inventory_root = (root / "audit" / "corpus_population" / "inventories").resolve()
    if source.is_symlink() or not source.is_file() or source.resolve().parent != inventory_root:
        raise ValueError("population inventory must be a regular file in the inventory root")
    inventory = load_object(source)
    _verify_inventory(inventory)
    policy = _config(root)["batching"]
    heavy = set(policy["heavy_formats"])
    selected = [
        row for row in inventory["documents"]
        if row["classification"] not in {"ALREADY_CANONICAL", "UNSUPPORTED"}
    ]
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in selected:
        groups[_group(row, heavy)].append(row)

    batch_payloads: list[dict[str, Any]] = []
    release_schema = {
        f"papercrawler:{row['release']}": row.get("schema_version")
        for row in inventory["papercrawler_releases"]
    }

    def group_order(item):
        source_group, processing_class = item[0]
        if source_group == "manual":
            return (0, "", processing_class)
        compatibility = 1 if release_schema.get(source_group) == "2.0" else 2
        return (compatibility, source_group, processing_class)

    for (source_group, processing_class), documents in sorted(groups.items(), key=group_order):
        if processing_class == "heavy":
            max_documents = int(policy["heavy_max_documents"])
            max_bytes = int(policy["heavy_max_source_bytes"])
        else:
            max_documents = int(policy["light_max_documents"])
            max_bytes = int(policy["light_max_source_bytes"])
        for ordinal, packed in enumerate(
            _pack(documents, max_documents=max_documents, max_bytes=max_bytes), 1
        ):
            semantic = {
                "schema_version": SCHEMA_VERSION,
                "contract_version": CONTRACT_VERSION,
                "inventory_id": inventory["inventory_id"],
                "source_group": source_group,
                "processing_class": processing_class,
                "ordinal": ordinal,
                "documents": [
                    {
                        "document_id": row["document_id"],
                        "sha256": row["sha256"],
                        "format": row["format"],
                        "size": row["size"],
                    }
                    for row in packed
                ],
            }
            batch_id = identity("CPB_", semantic)
            batch_payloads.append({
                "batch_id": batch_id,
                **semantic,
                "generated_at": now(),
                "status": "PENDING",
                "summary": {
                    "documents": len(packed),
                    "source_bytes": sum(int(row.get("size") or 0) for row in packed),
                },
            })

    run_semantic = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "inventory_id": inventory["inventory_id"],
        "canonical_before": inventory["canonical_before"],
        "batch_ids": [row["batch_id"] for row in batch_payloads],
    }
    run_id = identity("CPR_", run_semantic)
    run = {
        "run_id": run_id,
        **run_semantic,
        "created_at": now(),
        "updated_at": now(),
        "state": PopulationState.READY_TO_INGEST.value,
        "documents": {
            row["document_id"]: {
                "disposition": (
                    "ALREADY_CANONICAL" if row["classification"] == "ALREADY_CANONICAL"
                    else "UNSUPPORTED" if row["classification"] == "UNSUPPORTED"
                    else "RECOVERY_REQUIRED" if row["classification"] == "RECOVERY_REQUIRED"
                    else "PENDING"
                ),
                "engine_state": row.get("ledger", {}).get("state"),
            }
            for row in inventory["documents"]
        },
        "completed_batches": [],
        "failed_batches": [],
        "attempt_ids": [],
        "staging_audit_ids": [],
        "promotion_plan_ids": [],
        "canonical_after": None,
    }
    if write:
        base = root / "audit" / "corpus_population"
        for batch in batch_payloads:
            batch["run_id"] = run_id
            path = base / "batches" / f"{batch['batch_id']}.json"
            if not path.exists():
                atomic_json(path, batch, readonly=True)
            else:
                _verify_batch(load_object(path))
            batch["batch_path"] = path.relative_to(root).as_posix()
        run_path = base / "runs" / f"{run_id}.json"
        if not run_path.exists():
            atomic_json(run_path, run)
        else:
            _verify_run(load_object(run_path))
        run["run_path"] = run_path.relative_to(root).as_posix()
    return {
        "run": run,
        "batches": batch_payloads,
        "summary": {
            "batches": len(batch_payloads),
            "documents": len(selected),
            "by_source_group": {
                key: sum(
                    batch["summary"]["documents"]
                    for batch in batch_payloads if batch["source_group"] == key
                )
                for key in sorted({batch["source_group"] for batch in batch_payloads})
            },
        },
    }


def build_promotion_batches(
    staging_audit: dict[str, Any], project_root: Path | str | None = None, *, write: bool = True,
) -> list[dict[str, Any]]:
    root = Path(project_root or PROJECT_ROOT).resolve()
    policy = _config(root)["promotion"]
    candidates = sorted(
        staging_audit.get("promotion_candidates") or [], key=lambda row: row["document_id"]
    )
    groups = _pack(
        candidates,
        max_documents=int(policy["max_documents"]),
        max_bytes=int(policy["max_materialized_bytes"]),
    )
    outputs = []
    for ordinal, group in enumerate(groups, 1):
        semantic = {
            "schema_version": SCHEMA_VERSION,
            "contract_version": CONTRACT_VERSION,
            "staging_audit_id": staging_audit["audit_id"],
            "ordinal": ordinal,
            "document_ids": [row["document_id"] for row in group],
        }
        selector_id = identity("CPP_", semantic)
        payload = {
            "selector_id": selector_id,
            **semantic,
            "materialized_bytes": sum(int(row.get("size") or 0) for row in group),
            "generated_at": now(),
        }
        if write:
            path = root / "audit" / "corpus_population" / "promotion_batches" / f"{selector_id}.json"
            if not path.exists():
                atomic_json(path, payload, readonly=True)
            payload["selector_path"] = path.relative_to(root).as_posix()
        outputs.append(payload)
    return outputs


__all__ = ["build_promotion_batches", "plan_batches"]
