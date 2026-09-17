"""Population staging audit and final canonical-readiness reporting."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from tunnelbookai.canonical.eligibility import inspect_candidate
from tunnelbookai.canonical.hashing import load_json as canonical_load_json
from tunnelbookai.canonical.paths import CanonicalContext
from tunnelbookai.ingest.dedup import SourceRegistry, active_document_ids
from tunnelbookai.canonical.verifier import inspect_canonical, parse_manifest
from tunnelbookai.ingest.paths import PROJECT_ROOT
from tunnelbookai.ingest.staging import STAGING_COPY_FILES

from .batching import build_promotion_batches
from .models import CONTRACT_VERSION, PopulationState, SCHEMA_VERSION, atomic_json, identity, load_object, now


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def _existing_canonical(context: CanonicalContext) -> list[dict[str, Any]]:
    inventory = inspect_canonical(context=context)
    if inventory.state.value == "INVALID":
        raise RuntimeError("canonical corpus is INVALID")
    if not inventory.ready:
        return []
    manifest = parse_manifest(canonical_load_json(context.manifest_path, code="CANONICAL_MANIFEST_INVALID"))
    return [record.to_dict() for record in manifest.documents]


def _load_run(root: Path, run_path: Path | str) -> tuple[Path, dict[str, Any]]:
    source = Path(run_path)
    source = source if source.is_absolute() else root / source
    run_root = (root / "audit" / "corpus_population" / "runs").resolve()
    if source.is_symlink() or not source.is_file() or source.resolve().parent != run_root:
        raise ValueError("population run must be a regular file in the run root")
    run = load_object(source)
    from .batching import _verify_run
    _verify_run(run)
    return source, run


def build_staging_audit(
    run_path: Path | str, project_root: Path | str | None = None, *, write: bool = True,
) -> dict[str, Any]:
    root = Path(project_root or PROJECT_ROOT).resolve()
    source, run = _load_run(root, run_path)
    allowed_states = {
        PopulationState.INGEST_ACCOUNTED.value,
        PopulationState.STAGING_AUDITED.value,
        PopulationState.PROMOTION_PENDING_APPROVAL.value,
        PopulationState.PROMOTING.value,
        PopulationState.CANONICAL_READY.value,
    }
    if run.get("state") not in allowed_states:
        raise RuntimeError("staging audit requires an INGEST_ACCOUNTED population run")
    unresolved = [
        document_id for document_id, status in run["documents"].items()
        if status.get("disposition") in {"PENDING", "RECOVERY_REQUIRED", "FAILED", "NEEDS_REVIEW"}
        and not status.get("accounted_exclusion")
    ]
    if unresolved:
        raise RuntimeError(f"population run has {len(unresolved)} unaccounted documents")
    inventory = load_object(
        root / "audit" / "corpus_population" / "inventories" / f"{run['inventory_id']}.json"
    )
    from .batching import _verify_inventory
    _verify_inventory(inventory)
    context = CanonicalContext.load(root)
    existing = _existing_canonical(context)
    source_registry = SourceRegistry(
        context.paths.source_registry_path,
        active_document_ids=active_document_ids(root),
    )
    document_quality: Counter[str] = Counter()
    chunk_quality: Counter[str] = Counter()
    dispositions: Counter[str] = Counter()
    canonical_actions: Counter[str] = Counter()
    primary: dict[str, dict[str, int]] = defaultdict(lambda: {"documents": 0, "chunks": 0})
    secondary: dict[str, dict[str, int]] = defaultdict(lambda: {"document_associations": 0, "chunk_associations": 0})
    candidates: list[dict[str, Any]] = []
    ineligible: list[dict[str, Any]] = []
    exceptions: list[dict[str, Any]] = []
    chunks_total = ready_total = 0

    for document_id, status in sorted(run["documents"].items()):
        dispositions[str(status.get("disposition") or "PENDING")] += 1
        processing = root / "processing" / document_id
        gate = _read_json(processing / "quality_gate.json")
        chunk = _read_json(processing / "chunk_quality.json")
        classification = _read_json(processing / "classification.json")
        if gate.get("decision"):
            document_quality[str(gate["decision"])] += 1
        if chunk.get("status"):
            chunk_quality[str(chunk["status"])] += 1
        if status.get("disposition") in {"FAILED", "NEEDS_REVIEW", "REJECTED", "UNSUPPORTED", "DUPLICATE"}:
            exceptions.append({
                "document_id": document_id,
                "disposition": status.get("disposition"),
                "engine_state": status.get("engine_state"),
                "quality_reject_reasons": gate.get("reject_reasons") or [],
                "quality_review_reasons": gate.get("review_reasons") or [],
                "chunk_errors": chunk.get("errors") or [],
                "accounted_exclusion": status.get("accounted_exclusion"),
            })
        count = int(chunk.get("chunk_count") or 0)
        ready_path = processing / "chunks" / "embedding_ready.jsonl"
        ready_count = 0
        if ready_path.is_file():
            ready_count = sum(
                1 for line in ready_path.read_text(encoding="utf-8").splitlines()
                if line.strip() and json.loads(line).get("eligible") is True
            )
        chunks_total += count
        ready_total += ready_count
        section = classification.get("final_primary_section")
        if section:
            primary[str(section)]["documents"] += 1
            primary[str(section)]["chunks"] += count
        for section_id in classification.get("final_secondary_sections") or []:
            secondary[str(section_id)]["document_associations"] += 1
            secondary[str(section_id)]["chunk_associations"] += count

        staging = root / "corpus" / "staging" / "v2" / document_id
        if not staging.is_dir():
            continue
        candidate = inspect_candidate(
            context,
            staging,
            existing_documents=existing,
            source_registry=source_registry,
        )
        canonical_actions[candidate.action.value] += 1
        size = 0
        if candidate.action.value == "PROMOTE":
            paths = [staging / "document.md", *(staging / name for name in STAGING_COPY_FILES)]
            paths += [
                processing / "chunks" / "chunk_manifest.jsonl",
                processing / "chunks" / "embedding_ready.jsonl",
            ]
            size = sum(path.stat().st_size for path in paths if path.is_file())
            candidates.append({
                "document_id": document_id,
                "size": size,
                "chunk_count": candidate.chunk_count,
                "retrieval_ready_chunk_count": candidate.retrieval_ready_chunk_count,
            })
        elif candidate.action.value == "REJECTED":
            ineligible.append({
                "document_id": document_id,
                "reason_codes": list(candidate.validations),
                "warnings": list(candidate.warnings),
            })

    semantic = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "run_id": run["run_id"],
        "inventory_id": run["inventory_id"],
        "canonical_before": run["canonical_before"],
        "selected_documents": len(run["documents"]),
        "dispositions": dict(sorted(dispositions.items())),
        "physically_staged_documents": sum(canonical_actions.values()),
        "canonical_actions": dict(sorted(canonical_actions.items())),
        "document_quality": dict(sorted(document_quality.items())),
        "chunk_quality": dict(sorted(chunk_quality.items())),
        "chunks_total": chunks_total,
        "retrieval_ready_chunks": ready_total,
        "primary_section_distribution": dict(sorted(primary.items())),
        "secondary_section_associations": dict(sorted(secondary.items())),
        "promotion_candidates": candidates,
        "ineligible_staging": ineligible,
        "exceptions": exceptions,
    }
    audit_id = identity("CSA_", semantic)
    payload = {"audit_id": audit_id, **semantic, "generated_at": now()}
    if write:
        path = root / "audit" / "corpus_population" / "staging_audits" / f"{audit_id}.json"
        if not path.exists():
            atomic_json(path, payload, readonly=True)
        payload["audit_path"] = path.relative_to(root).as_posix()
        selectors = build_promotion_batches(payload, root, write=True)
        payload["promotion_batches"] = selectors
        if audit_id not in run["staging_audit_ids"]:
            run["staging_audit_ids"].append(audit_id)
        run["state"] = (
            PopulationState.PROMOTION_PENDING_APPROVAL.value
            if candidates else PopulationState.STAGING_AUDITED.value
        )
        run["updated_at"] = now()
        atomic_json(source, run)
    return payload


def build_readiness_report(
    run_path: Path | str, project_root: Path | str | None = None, *, write: bool = True,
) -> dict[str, Any]:
    root = Path(project_root or PROJECT_ROOT).resolve()
    source, run = _load_run(root, run_path)
    inventory = load_object(
        root / "audit" / "corpus_population" / "inventories" / f"{run['inventory_id']}.json"
    )
    from .batching import _verify_inventory
    _verify_inventory(inventory)
    canonical = inspect_canonical(project_root=root).to_dict()
    dispositions = Counter(str(row.get("disposition") or "PENDING") for row in run["documents"].values())
    records: list[dict[str, Any]] = []
    if canonical.get("ready"):
        context = CanonicalContext.load(root)
        manifest = parse_manifest(canonical_load_json(context.manifest_path, code="CANONICAL_MANIFEST_INVALID"))
        records = [record.to_dict() for record in manifest.documents]
    channel_distribution = Counter(str(row.get("source_kind") or "UNKNOWN") for row in records)
    format_distribution = Counter(str(row.get("format") or "UNKNOWN") for row in records)
    section_distribution: dict[str, dict[str, int]] = defaultdict(lambda: {"documents": 0, "chunks": 0})
    secondary_distribution: dict[str, dict[str, int]] = defaultdict(
        lambda: {"document_associations": 0, "chunk_associations": 0}
    )
    provenance_channels: Counter[str] = Counter()
    for row in records:
        section = str(row["classification"]["primary_section"])
        section_distribution[section]["documents"] += 1
        section_distribution[section]["chunks"] += int(row["chunks"]["count"])
        for secondary in row["classification"].get("secondary_sections") or []:
            secondary_distribution[str(secondary)]["document_associations"] += 1
            secondary_distribution[str(secondary)]["chunk_associations"] += int(row["chunks"]["count"])
        provenance = _read_json(root / str(row["provenance"]["path"]))
        for kind in {
            str(item.get("kind") or item.get("source_kind") or "UNKNOWN")
            for item in provenance.get("sources") or [] if isinstance(item, dict)
        }:
            provenance_channels[kind] += 1
    unresolved = sum(
        1 for row in run["documents"].values()
        if row.get("disposition") in {"PENDING", "RECOVERY_REQUIRED", "FAILED", "NEEDS_REVIEW"}
        and not row.get("accounted_exclusion")
    )
    required_canonical = {
        document_id for document_id, row in run["documents"].items()
        if row.get("disposition") in {"STAGED", "ALREADY_PROCESSED", "ALREADY_CANONICAL"}
    }
    canonical_ids = {str(row["document_id"]) for row in records}
    missing_canonical = sorted(required_canonical - canonical_ids)
    ready = bool(
        canonical.get("ready") and unresolved == 0 and not missing_canonical
        and run.get("staging_audit_ids")
    )
    promotion_plan_ids = sorted({
        str(row.get("promotion_plan_id")) for row in records if row.get("promotion_plan_id")
    })
    promotion_applies = []
    for path in sorted((root / "audit" / "canonical_promotions" / "applies").glob("CPA_*.json")):
        value = _read_json(path)
        if value.get("plan_id") in promotion_plan_ids:
            promotion_applies.append({
                "promotion_id": value.get("promotion_id"),
                "plan_id": value.get("plan_id"),
                "result": value.get("result"),
            })
    recovery_documents = [
        row for row in inventory["documents"] if row["classification"] == "RECOVERY_REQUIRED"
    ]
    recovery_outcomes = Counter(
        str(run["documents"][row["document_id"]].get("disposition") or "PENDING")
        for row in recovery_documents
    )
    manual_import_applies = sorted(
        path.stem
        for path in (root / "audit" / "corpus_population" / "manual_import_applies").glob("CMI_*.json")
    )
    staging_audit = {}
    if run.get("staging_audit_ids"):
        latest = str(run["staging_audit_ids"][-1])
        staging_audit = _read_json(
            root / "audit" / "corpus_population" / "staging_audits" / f"{latest}.json"
        )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "run_id": run["run_id"],
        "generated_at": now(),
        "ready_for_retrieval_milestone": ready,
        "canonical": canonical,
        "population_dispositions": dict(sorted(dispositions.items())),
        "missing_canonical_document_ids": missing_canonical,
        "promotion_plan_ids": promotion_plan_ids,
        "promotion_apply_audits": promotion_applies,
        "source_channel_distribution": dict(sorted(channel_distribution.items())),
        "provenance_channel_associations": dict(sorted(provenance_channels.items())),
        "file_type_distribution": dict(sorted(format_distribution.items())),
        "section_distribution": dict(sorted(section_distribution.items())),
        "secondary_section_associations": dict(sorted(secondary_distribution.items())),
        "paper_crawler_releases": inventory["papercrawler_releases"],
        "manual_import_apply_ids": manual_import_applies,
        "manual_inventory": inventory["manual_summary"],
        "recovery": {
            "selected": len(recovery_documents),
            "outcomes": dict(sorted(recovery_outcomes.items())),
            "out_of_scope_ledger_only": len(inventory["ledger_only"]),
        },
        "staging_audit_id": staging_audit.get("audit_id"),
        "staging_exceptions": staging_audit.get("exceptions") or [],
        "retrieval": "NOT_IMPLEMENTED",
        "prewriting_evidence_audit": "NOT_IMPLEMENTED",
        "book_writing": "NOT_IMPLEMENTED",
    }
    if write:
        json_path = root / "audit" / "corpus_population" / "readiness" / f"{run['run_id']}.json"
        atomic_json(json_path, payload)
        report_path = root / "reports" / "corpus_population_readiness.md"
        lines = [
            "# Corpus Population V1 Readiness",
            "",
            f"Run: `{run['run_id']}`",
            f"Inventory: `{run['inventory_id']}`",
            f"Staging audit: `{staging_audit.get('audit_id')}`",
            f"Ready for Book Retrieval Layer V1: **{str(ready).upper()}**",
            "",
            f"Canonical state: **{canonical['state']}**",
            f"Canonical documents: **{canonical['document_count']}**",
            f"Canonical chunks: **{canonical['chunk_count']}**",
            f"Retrieval-ready chunks: **{canonical['retrieval_ready_chunk_count']}**",
            f"Canonical manifest SHA-256: `{canonical.get('manifest_sha256')}`",
            f"Canonical corpus digest: `{canonical.get('corpus_digest')}`",
            f"Selected inputs: **{len(run['documents'])}**",
            f"Unresolved inputs: **{unresolved}**",
            f"Recovered-input outcomes: `{dict(sorted(recovery_outcomes.items()))}`",
            "",
            "Retrieval, pre-writing evidence audit, and book writing remain `NOT_IMPLEMENTED`.",
        ]
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        payload["report_path"] = report_path.relative_to(root).as_posix()
        run["canonical_after"] = {
            "state": canonical["state"],
            "manifest_sha256": canonical.get("manifest_sha256"),
            "corpus_digest": canonical.get("corpus_digest"),
        }
        run["promotion_plan_ids"] = promotion_plan_ids
        if ready:
            run["state"] = PopulationState.CANONICAL_READY.value
        run["updated_at"] = now()
        atomic_json(source, run)
    return payload


__all__ = ["build_readiness_report", "build_staging_audit"]
