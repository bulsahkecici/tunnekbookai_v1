"""Apply evidence-backed manual section review decisions as one atomic workflow.

The workflow updates every derived section projection together, quarantines weak or
out-of-scope staging candidates without deleting their originals/processing bundles, and
invalidates promotion plans that describe the pre-review state.
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

from tunnelbookai.ingest.chunking import manifest as manifest_module
from tunnelbookai.ingest.chunking.policy import ChunkPolicy
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.staging import BUNDLE_SHAPE, STAGING_COPY_FILES, STAGING_VERSION
from tunnelbookai.population.models import atomic_json, load_object, now


SCHEMA_VERSION = "1.0"
TARGET_PREFIXES = ("3", "4", "6")


def _matches(section: Any, prefix: str) -> bool:
    value = str(section or "")
    return value == prefix or value.startswith(prefix + ".")


def _expected_primary_matches(current: Any, expected: Any) -> bool:
    if expected is None:
        return True
    values = expected if isinstance(expected, list) else [expected]
    return str(current) in {str(value) for value in values}


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _atomic_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _copy(source: Path, destination: Path) -> None:
    if source.is_file():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def _sync_ledgers(
    root: Path, results: list[dict[str, Any]], backup_root: Path, review_id: str,
) -> None:
    """Keep the resumable ingest ledgers aligned with the reviewed artifacts."""
    result_by_id = {str(row["document_id"]): row for row in results}
    reviewed_at = now()

    manifest_path = root / "audit" / "ingest_manifest.jsonl"
    manifest_rows = _load_jsonl(manifest_path)
    _copy(manifest_path, backup_root / "audit" / "ingest_manifest.jsonl")
    for row in manifest_rows:
        result = result_by_id.get(str(row.get("document_id")))
        if result is None:
            continue
        row["manual_review"] = {
            "review_id": review_id,
            "action": result["action"],
            "reason": result["reason"],
            "reviewed_at": reviewed_at,
        }
        if result["action"] == "UPDATED":
            row["final_primary_section"] = result["primary"]
            row["final_secondary_sections"] = result["secondary"]
            if result.get("quality_decision") == "GO":
                row["status"] = "EMBEDDING_READY"
                row["quality_decision"] = "GO"
                row["staging_path"] = f"corpus/staging/v2/{row['document_id']}"
        else:
            rejected = result["reason_code"] == "OUT_OF_SCOPE"
            row["status"] = "REJECTED" if rejected else "REVIEW"
            row["quality_decision"] = "REJECT" if rejected else "REVIEW"
            row["staging_path"] = None
            row["embedding_ready_chunks"] = 0
    _atomic_jsonl(manifest_path, manifest_rows)

    state_path = root / "audit" / "ingest_state.jsonl"
    state_rows = _load_jsonl(state_path)
    _copy(state_path, backup_root / "audit" / "ingest_state.jsonl")
    for row in state_rows:
        result = result_by_id.get(str(row.get("document_id")))
        if result is None:
            continue
        if result["action"] == "QUARANTINED":
            rejected = result["reason_code"] == "OUT_OF_SCOPE"
            state = "REJECTED" if rejected else "REVIEW"
            detail = {
                "review_id": review_id, "reason_code": result["reason_code"],
                "reason": result["reason"],
            }
        elif result.get("quality_decision") == "GO":
            state = "EMBEDDING_READY"
            detail = {
                "review_id": review_id, "reason": result["reason"],
                "resolved_review_reasons": result.get("resolved_review_reasons") or [],
            }
        else:
            continue
        row["state"] = state
        row["updated_at"] = reviewed_at
        row.setdefault("detail", {})["manual_section_review"] = detail
        row.setdefault("history", []).append({"state": state, "at": reviewed_at})
    _atomic_jsonl(state_path, state_rows)


def _scope(root: Path) -> set[str]:
    selected: set[str] = set()
    for path in (root / "corpus" / "staging" / "v2").glob("ING_*/metadata.json"):
        value = load_object(path)
        sections = [value.get("final_primary_section"), *(value.get("final_secondary_sections") or [])]
        if any(_matches(section, prefix) for section in sections for prefix in TARGET_PREFIXES):
            selected.add(str(value["document_id"]))
    return selected


def _staging_stats(root: Path) -> dict[str, Any]:
    primary: Counter[str] = Counter()
    documents = chunks = ready = 0
    for metadata_path in (root / "corpus" / "staging" / "v2").glob("ING_*/metadata.json"):
        metadata = load_object(metadata_path)
        bundle = load_object(metadata_path.parent / "bundle.json")
        document_id = str(metadata["document_id"])
        rows = _load_jsonl(root / "processing" / document_id / "chunks" / "embedding_ready.jsonl")
        documents += 1
        chunks += int(bundle.get("chunk_count") or 0)
        ready += sum(row.get("eligible") is True for row in rows)
        primary[str(metadata.get("final_primary_section") or "UNASSIGNED")] += 1
    return {
        "documents": documents,
        "chunks": chunks,
        "retrieval_ready_chunks": ready,
        "primary_sections": dict(sorted(primary.items())),
    }


def _materialize_staging(
    root: Path, processing: Path, staging: Path, metadata: dict[str, Any],
    classification: dict[str, Any], gate: dict[str, Any], chunk_count: int,
) -> None:
    staging.mkdir(parents=True, exist_ok=True)
    for name in STAGING_COPY_FILES:
        _copy(processing / name, staging / name)
    _copy(processing / "normalized" / "document.md", staging / "document.md")
    document_id = str(metadata["document_id"])
    atomic_json(staging / "bundle.json", {
        "bundle_shape": BUNDLE_SHAPE,
        "staging_version": STAGING_VERSION,
        "document_id": document_id,
        "original_sha256": metadata.get("original_sha256"),
        "source_kind": metadata.get("source_kind"),
        "format": metadata.get("format"),
        "title": metadata.get("title"),
        "final_primary_section": classification.get("final_primary_section"),
        "final_secondary_sections": classification.get("final_secondary_sections") or [],
        "final_section_confidence": classification.get("final_section_confidence"),
        "final_evidence_level": metadata.get("final_evidence_level"),
        "content_capabilities": metadata.get("content_capabilities") or {},
        "quality_decision": gate.get("decision"),
        "processing_bundle": processing.relative_to(root).as_posix(),
        "original_archive": f"originals/{document_id}",
        "chunks_authoritative_path": (
            processing / "chunks" / "chunk_manifest.jsonl"
        ).relative_to(root).as_posix(),
        "chunk_count": chunk_count,
        "chunk_quality_status": load_object(processing / "chunk_quality.json").get("status"),
        "canonical_promoted": False,
    })


def _manual_note(
    classification: dict[str, Any], *, review_id: str, action: str, reason: str,
    previous_primary: str | None, previous_secondary: list[str],
) -> None:
    classification["manual_review"] = {
        "review_id": review_id,
        "reviewer": "CODEX_FULL_TEXT_REVIEW",
        "action": action,
        "reason": reason,
        "previous_primary_section": previous_primary,
        "previous_secondary_sections": previous_secondary,
        "reviewed_at": now(),
    }
    classification["decision_path"] = "MANUAL_FULL_TEXT_REVIEW"


def _update_sections(
    root: Path, run: dict[str, Any], directive: dict[str, Any], policy: ChunkPolicy,
    backup_root: Path, review_id: str,
) -> dict[str, Any]:
    document_id = str(directive["document_id"])
    processing = root / "processing" / document_id
    staging = root / "corpus" / "staging" / "v2" / document_id
    classification = load_object(processing / "classification.json")
    metadata = load_object(processing / "metadata.json")
    gate = load_object(processing / "quality_gate.json")
    previous_primary = classification.get("final_primary_section")
    previous_secondary = list(classification.get("final_secondary_sections") or [])
    expected_primary = directive.get("expected_primary")
    if not _expected_primary_matches(previous_primary, expected_primary):
        raise RuntimeError(f"{document_id}: stale primary section {previous_primary!r}")

    primary = str(directive.get("primary") or previous_primary or "")
    if "secondary" in directive:
        secondary = [str(value) for value in directive["secondary"]]
    else:
        prefixes = [str(value) for value in directive.get("remove_secondary_prefixes") or []]
        secondary = [
            str(value) for value in previous_secondary
            if not any(_matches(value, prefix) for prefix in prefixes)
        ]
    secondary = list(dict.fromkeys(value for value in secondary if value != primary))
    if not primary:
        raise RuntimeError(f"{document_id}: update would clear the primary section")

    for relative in (
        "classification.json", "metadata.json", "quality_gate.json", "chunks/chunk_manifest.jsonl",
        "chunks/embedding_ready.jsonl",
    ):
        _copy(processing / relative, backup_root / document_id / "processing" / relative)
    if staging.is_dir():
        for name in (*STAGING_COPY_FILES, "bundle.json", "document.md"):
            _copy(staging / name, backup_root / document_id / "staging" / name)

    classification["final_primary_section"] = primary
    classification["final_secondary_sections"] = secondary
    classification["final_section_confidence"] = float(directive.get("confidence", 1.0))
    _manual_note(
        classification, review_id=review_id, action="UPDATE", reason=str(directive["reason"]),
        previous_primary=previous_primary, previous_secondary=previous_secondary,
    )
    metadata["final_primary_section"] = primary
    metadata["final_secondary_sections"] = secondary
    metadata["final_section_confidence"] = classification["final_section_confidence"]

    resolved = {str(value) for value in directive.get("resolve_review_reasons") or []}
    if resolved:
        gate["review_reasons"] = [
            value for value in gate.get("review_reasons") or [] if str(value) not in resolved
        ]
        if not gate["review_reasons"] and not (gate.get("reject_reasons") or []):
            gate["decision"] = "GO"

    chunks = _load_jsonl(processing / "chunks" / "chunk_manifest.jsonl")
    for chunk in chunks:
        chunk["final_primary_section"] = primary
        chunk["final_secondary_sections"] = secondary
    ready_rows = manifest_module.build_rows(chunks, policy, document_staged=True, chunk_quality_ok=True)

    atomic_json(processing / "classification.json", classification)
    atomic_json(processing / "metadata.json", metadata)
    atomic_json(processing / "quality_gate.json", gate)
    _atomic_jsonl(processing / "chunks" / "chunk_manifest.jsonl", chunks)
    _atomic_jsonl(processing / "chunks" / "embedding_ready.jsonl", ready_rows)
    if staging.is_dir():
        for name in STAGING_COPY_FILES:
            _copy(processing / name, staging / name)
        _copy(processing / "normalized" / "document.md", staging / "document.md")
        bundle = load_object(staging / "bundle.json")
        bundle["final_primary_section"] = primary
        bundle["final_secondary_sections"] = secondary
        bundle["final_section_confidence"] = classification["final_section_confidence"]
        atomic_json(staging / "bundle.json", bundle)
    elif directive.get("materialize_staging") and gate.get("decision") == "GO":
        _materialize_staging(
            root, processing, staging, metadata, classification, gate, len(chunks),
        )

    row = run["documents"].get(document_id)
    if row is not None:
        row["final_primary_section"] = primary
        row["embedding_ready_chunks"] = sum(value.get("eligible") is True for value in ready_rows)
        if gate.get("decision") == "GO":
            row["disposition"] = "STAGED"
            row["quality_decision"] = "GO"
            row["engine_state"] = "EMBEDDING_READY"
            row["state"] = "EMBEDDING_READY"
            row["staging_path"] = f"corpus/staging/v2/{document_id}"
            row["warnings"] = [
                value for value in row.get("warnings") or [] if str(value) not in resolved
            ]
    return {
        "document_id": document_id, "action": "UPDATED", "previous_primary": previous_primary,
        "previous_secondary": previous_secondary, "primary": primary, "secondary": secondary,
        "reason": directive["reason"], "quality_decision": gate.get("decision"),
        "resolved_review_reasons": sorted(resolved), "ready_rows": ready_rows,
    }


def _quarantine(
    root: Path, run: dict[str, Any], directive: dict[str, Any], policy: ChunkPolicy,
    backup_root: Path, quarantine_root: Path, review_id: str,
) -> dict[str, Any]:
    document_id = str(directive["document_id"])
    processing = root / "processing" / document_id
    staging = root / "corpus" / "staging" / "v2" / document_id
    classification = load_object(processing / "classification.json")
    gate = load_object(processing / "quality_gate.json")
    previous_primary = classification.get("final_primary_section")
    previous_secondary = list(classification.get("final_secondary_sections") or [])
    for relative in ("classification.json", "quality_gate.json", "chunks/embedding_ready.jsonl"):
        _copy(processing / relative, backup_root / document_id / "processing" / relative)
    if staging.is_dir():
        destination = quarantine_root / document_id
        if destination.exists():
            raise RuntimeError(f"{document_id}: quarantine destination already exists")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(staging), str(destination))

    reason_code = str(directive["reason_code"])
    _manual_note(
        classification, review_id=review_id, action="QUARANTINE",
        reason=str(directive["reason"]), previous_primary=previous_primary,
        previous_secondary=previous_secondary,
    )
    gate["decision"] = "REJECT" if reason_code == "OUT_OF_SCOPE" else "REVIEW"
    target = "reject_reasons" if gate["decision"] == "REJECT" else "review_reasons"
    gate.setdefault(target, [])
    marker = f"MANUAL_SECTION_REVIEW:{reason_code}"
    if marker not in gate[target]:
        gate[target].append(marker)
    chunks = _load_jsonl(processing / "chunks" / "chunk_manifest.jsonl")
    ready_rows = manifest_module.build_rows(chunks, policy, document_staged=False, chunk_quality_ok=True)
    atomic_json(processing / "classification.json", classification)
    atomic_json(processing / "quality_gate.json", gate)
    _atomic_jsonl(processing / "chunks" / "embedding_ready.jsonl", ready_rows)

    row = run["documents"].get(document_id)
    if row is not None:
        row["disposition"] = "REJECTED" if gate["decision"] == "REJECT" else "NEEDS_REVIEW"
        row["quality_decision"] = gate["decision"]
        row["staging_path"] = None
        row["embedding_ready_chunks"] = 0
        row.setdefault("warnings", [])
        if marker not in row["warnings"]:
            row["warnings"].append(marker)
        row["accounted_exclusion"] = {
            "reason": f"MANUAL_SECTION_REVIEW:{reason_code}", "recorded_at": now(),
        }
    return {
        "document_id": document_id, "action": "QUARANTINED", "reason_code": reason_code,
        "reason": directive["reason"], "previous_primary": previous_primary,
        "previous_secondary": previous_secondary, "ready_rows": ready_rows,
    }


def apply_review(spec_path: Path, run_path: Path, project_root: Path) -> dict[str, Any]:
    root = project_root.resolve()
    spec = load_object(spec_path.resolve())
    if spec.get("schema_version") != SCHEMA_VERSION:
        raise RuntimeError("unsupported manual section review schema")
    review_id = str(spec["review_id"])
    audit_path = root / "audit" / "dashboard" / "section_reviews" / f"{review_id}.json"
    if audit_path.is_file():
        return load_object(audit_path)

    directives = list(spec.get("directives") or [])
    directive_ids = [str(item["document_id"]) for item in directives]
    scope_before = (
        set(directive_ids) if spec.get("scope_mode") == "DIRECTIVES"
        else _scope(root) | {str(value) for value in spec.get("scope_inclusions") or []}
    )
    expected_count = int(spec.get("expected_scope_count") or 0)
    if len(scope_before) != expected_count:
        raise RuntimeError(f"stale review scope: expected {expected_count}, found {len(scope_before)}")
    if len(directive_ids) != len(set(directive_ids)) or not set(directive_ids) <= scope_before:
        raise RuntimeError("review directives are duplicated or outside the reviewed scope")
    for directive in directives:
        document_id = str(directive["document_id"])
        processing = root / "processing" / document_id
        staging = root / "corpus" / "staging" / "v2" / document_id
        required = [
            processing / "classification.json", processing / "metadata.json",
            processing / "quality_gate.json", processing / "chunks/chunk_manifest.jsonl",
        ]
        if not directive.get("materialize_staging"):
            required.append(staging / "bundle.json")
        missing = [path.relative_to(root).as_posix() for path in required if not path.is_file()]
        if missing:
            raise RuntimeError(f"{document_id}: required review artifacts missing: {missing}")
        classification = load_object(processing / "classification.json")
        if not _expected_primary_matches(
            classification.get("final_primary_section"), directive.get("expected_primary"),
        ):
            raise RuntimeError(
                f"{document_id}: stale primary section "
                f"{classification.get('final_primary_section')!r}"
            )

    stamp = now().replace(":", "").replace("+", "_")
    backup_root = root / "audit" / "dashboard" / "section_review_backups" / stamp
    quarantine_root = root / "audit" / "dashboard" / "section_review_quarantine" / stamp
    run = load_object(run_path.resolve())
    policy = ChunkPolicy.from_config(load_config())
    before = _staging_stats(root)
    results: list[dict[str, Any]] = []
    replacement_rows: list[dict[str, Any]] = []
    for directive in directives:
        if directive["action"] == "UPDATE":
            result = _update_sections(root, run, directive, policy, backup_root, review_id)
        elif directive["action"] == "QUARANTINE":
            result = _quarantine(
                root, run, directive, policy, backup_root, quarantine_root, review_id,
            )
        else:
            raise RuntimeError(f"unknown review action: {directive['action']}")
        replacement_rows.extend(result.pop("ready_rows"))
        results.append(result)

    touched = set(directive_ids)
    manifest_module.merge_into(
        root / "audit" / "embedding_ready_manifest.jsonl", replacement_rows,
        document_ids=touched,
    )
    _sync_ledgers(root, results, backup_root, review_id)
    run["staging_audit_ids"] = []
    run["promotion_plan_ids"] = []
    run["updated_at"] = now()
    atomic_json(run_path.resolve(), run)
    after = _staging_stats(root)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "review_id": review_id,
        "status": "APPLIED",
        "applied_at": now(),
        "scope": list(spec.get("scope") or []),
        "reviewed_documents": len(scope_before),
        "confirmed_unchanged": len(scope_before) - len(directives),
        "updated": sum(row["action"] == "UPDATED" for row in results),
        "quarantined": sum(row["action"] == "QUARANTINED" for row in results),
        "before": before,
        "after": after,
        "backup_root": backup_root.relative_to(root).as_posix(),
        "quarantine_root": quarantine_root.relative_to(root).as_posix(),
        "results": results,
    }
    atomic_json(audit_path, payload, readonly=True)
    dashboard_path = root / "audit" / "dashboard" / "improvements.json"
    if dashboard_path.is_file():
        dashboard = load_object(dashboard_path)
        dashboard_key = str(spec.get("dashboard_key") or "section_review")
        dashboard[dashboard_key] = {
            key: payload[key] for key in (
                "review_id", "status", "reviewed_documents", "confirmed_unchanged",
                "updated", "quarantined", "before", "after",
            )
        }
        if spec.get("dashboard_message"):
            dashboard["message"] = str(spec["dashboard_message"])
        elif dashboard_key == "targeted_recovery":
            dashboard["message"] = (
                f"Hedefli kaynak kurtarma uygulandı: {payload['updated']} resmi tam metin "
                "işlendi ve manuel bölüm doğrulamasıyla staging'e alındı."
            )
        elif dashboard_key == "section_3_research":
            dashboard["message"] = (
                f"Bölüm 3 PaperCrawler araştırması uygulandı: {payload['updated']} belge "
                "manuel eşlendi ve yeni tam metinler staging'e alındı."
            )
        else:
            dashboard["message"] = (
                f"Bölüm 3/4/6 manuel incelemesi uygulandı: {payload['reviewed_documents']} belge "
                f"incelendi, {payload['updated']} bölüm kaydı düzeltildi, "
                f"{payload['quarantined']} aday karantinaya alındı."
            )
        dashboard["updated_at"] = now()
        atomic_json(dashboard_path, dashboard)
    return payload


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Apply an audited manual section review")
    parser.add_argument("--spec", required=True)
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    result = apply_review(root / args.spec, root / args.run, root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
