"""Deterministic inventory for manual inputs, PaperCrawler packs, and runtime identities."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from tunnelbookai.canonical.verifier import inspect_canonical, parse_manifest
from tunnelbookai.canonical.hashing import load_json as load_canonical_json
from tunnelbookai.ingest.config import IngestConfig
from tunnelbookai.ingest.format_registry import detect, is_supported
from tunnelbookai.ingest.ids import document_id_for_file, sha256_file
from tunnelbookai.ingest.office_renderer import find_libreoffice
from tunnelbookai.ingest.paths import IngestPaths, PROJECT_ROOT
from tunnelbookai.ingest.sources import papercrawler_contract

from .models import CONTRACT_VERSION, SCHEMA_VERSION, atomic_json, identity, now

_CONFIGS = ("ingest", "ocr", "vision", "metadata", "classification", "quality_gate", "chunking", "models")
_IGNORE_NAMES = {"readme.md", ".gitkeep", ".ds_store"}


def _config(root: Path) -> IngestConfig:
    values: dict[str, dict[str, Any]] = {}
    for name in _CONFIGS:
        path = root / "config" / f"{name}.yaml"
        value = yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else {}
        values[name] = value if isinstance(value, dict) else {}
    return IngestConfig(**values)


def _relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if isinstance(value, dict):
                rows.append(value)
    return rows


def _object(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def _strict_jsonl(path: Path) -> list[dict[str, Any]] | None:
    if not path.is_file() or path.is_symlink():
        return None
    rows: list[dict[str, Any]] = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                return None
            rows.append(value)
    except (OSError, ValueError):
        return None
    return rows


def _manual_ignored(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not root.is_dir():
        return rows
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        reason = None
        if path.is_symlink():
            reason = "SYMLINK"
        elif any(part.startswith(".") for part in relative.parts):
            reason = "HIDDEN"
        elif path.is_file() and path.name.lower() in _IGNORE_NAMES:
            reason = "IGNORED_NAME"
        elif path.is_file() and path.name.startswith("~$"):
            reason = "OFFICE_TEMPORARY"
        if reason:
            rows.append({"path": f"incoming/manual/inbox/{relative.as_posix()}", "reason": reason})
    return rows


def _artifact_status(root: Path, document_id: str, sha256: str) -> dict[str, bool]:
    original = root / "originals" / document_id
    processing = root / "processing" / document_id
    staging = root / "corpus" / "staging" / "v2" / document_id
    sources = [path for path in original.glob("source.*") if path.is_file() and not path.is_symlink()]
    try:
        source_ok = len(sources) == 1 and sha256_file(sources[0]) == sha256
    except OSError:
        source_ok = False
    original_metadata = _object(original / "original.json")
    processing_metadata = _object(processing / "metadata.json")
    quality = _object(processing / "quality_gate.json")
    chunk_rows = _strict_jsonl(processing / "chunks" / "chunk_manifest.jsonl")
    ready_rows = _strict_jsonl(processing / "chunks" / "embedding_ready.jsonl")
    bundle = _object(staging / "bundle.json")
    chunk_ids = {
        str(row.get("chunk_id")) for row in (chunk_rows or []) if row.get("chunk_id")
    }
    return {
        "original": bool(
            source_ok
            and original_metadata.get("document_id") == document_id
            and original_metadata.get("original_sha256") == sha256
        ),
        "processing_metadata": bool(
            processing_metadata.get("document_id") == document_id
            and processing_metadata.get("original_sha256") == sha256
        ),
        "processing_quality": bool(
            quality.get("document_id") == document_id
            and quality.get("decision") in {"GO", "REVIEW", "REJECT"}
        ),
        "processing_chunks": bool(
            chunk_rows
            and all(
                row.get("document_id") == document_id
                and (row.get("provenance") or {}).get("original_sha256") == sha256
                for row in chunk_rows
            )
        ),
        "embedding_ready": bool(
            ready_rows
            and all(
                row.get("document_id") == document_id and row.get("chunk_id") in chunk_ids
                for row in ready_rows
            )
        ),
        "staging": bool(
            bundle.get("document_id") == document_id
            and bundle.get("original_sha256") == sha256
        ),
    }


def _canonical_documents(root: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    if not (root / "book" / "config" / "book_contract.json").is_file():
        if (root / "corpus" / "canonical" / "canonical_manifest.json").is_file():
            raise RuntimeError("canonical manifest exists but Book Contract is unavailable")
        return {
            "state": "EMPTY", "document_count": 0, "chunk_count": 0,
            "retrieval_ready_chunk_count": 0, "manifest_sha256": None,
            "corpus_digest": None, "ready": False, "retrieval_allowed": False,
            "reasons": ["CANONICAL_CORPUS_EMPTY"], "warnings": [],
        }, {}
    inventory = inspect_canonical(project_root=root)
    summary = inventory.to_dict()
    documents: dict[str, dict[str, Any]] = {}
    if inventory.ready:
        context_path = root / "corpus" / "canonical" / "canonical_manifest.json"
        manifest = parse_manifest(load_canonical_json(context_path, code="CANONICAL_MANIFEST_INVALID"))
        documents = {record.document_id: record.to_dict() for record in manifest.documents}
    return summary, documents


def build_inventory(project_root: Path | str | None = None, *, write: bool = True) -> dict[str, Any]:
    root = Path(project_root or PROJECT_ROOT).resolve()
    paths = IngestPaths(root)
    config = _config(root)
    libreoffice = find_libreoffice()
    canonical, canonical_documents = _canonical_documents(root)
    canonical_by_sha = {row["source_sha256"]: row for row in canonical_documents.values()}

    state_rows = _jsonl(paths.ingest_state_path)
    manifest_rows = _jsonl(paths.ingest_manifest_path)
    registry_rows = _jsonl(paths.source_registry_path)
    state_by_id = {str(row.get("document_id")): row for row in state_rows}
    manifest_by_id = {str(row.get("document_id")): row for row in manifest_rows}
    registry_by_id = {str(row.get("document_id")): row for row in registry_rows}

    aliases: list[dict[str, Any]] = []
    for input_path in sorted(paths.incoming_manual_inbox.rglob("*")):
        relative = input_path.relative_to(paths.incoming_manual_inbox)
        if (
            input_path.is_symlink()
            or not input_path.is_file()
            or input_path.name.lower() in _IGNORE_NAMES
            or input_path.name.startswith("~$")
            or any(part.startswith(".") for part in relative.parts)
        ):
            continue
        det = detect(input_path)
        try:
            size = input_path.stat().st_size
            document_id, sha = document_id_for_file(input_path)
            error = None
        except Exception as exc:
            document_id, sha, size, error = "", "", None, f"{type(exc).__name__}:{exc}"
        aliases.append({
            "document_id": document_id,
            "sha256": sha,
            "source_kind": "MANUAL_INTERNAL",
            "release": None,
            "path": _relative(root, input_path),
            "size": size,
            "format": det.fmt.value,
            "supported": bool(not error and is_supported(det, libreoffice_available=libreoffice is not None)),
            "error": error,
        })

    release_rows: list[dict[str, Any]] = []
    for result in papercrawler_contract.discover(releases_root=paths.incoming_papercrawler_releases):
        accepted_aliases = []
        for item in result.accepted:
            det = detect(item.input_path)
            document_id, sha = document_id_for_file(item.input_path)
            row = {
                "document_id": document_id,
                "sha256": sha,
                "source_kind": item.source_kind,
                "release": result.release_dir.name,
                "path": _relative(root, item.input_path),
                "size": item.input_path.stat().st_size,
                "format": det.fmt.value,
                "supported": is_supported(det, libreoffice_available=libreoffice is not None),
                "error": None,
            }
            aliases.append(row)
            accepted_aliases.append(row)
        release_rows.append({
            "release": result.release_dir.name,
            "schema_version": result.schema_version,
            "status": "BLOCKED_RELEASE" if result.blockers else "ACCEPTED",
            "accepted": len(accepted_aliases),
            "accepted_bytes": sum(int(row["size"]) for row in accepted_aliases),
            "formats": dict(sorted(Counter(row["format"] for row in accepted_aliases).items())),
            "skipped": result.skipped,
            "blockers": result.blockers,
        })

    grouped: dict[str, list[dict[str, Any]]] = {}
    unreadable: list[dict[str, Any]] = []
    for row in aliases:
        if not row["document_id"]:
            unreadable.append(row)
        else:
            grouped.setdefault(row["document_id"], []).append(row)

    documents: list[dict[str, Any]] = []
    for document_id, source_aliases in sorted(grouped.items()):
        shas = {str(row["sha256"]) for row in source_aliases}
        if len(shas) != 1:
            raise ValueError(f"document identity collision: {document_id}")
        sha = next(iter(shas))
        artifact = _artifact_status(root, document_id, sha)
        state = state_by_id.get(document_id, {}).get("state")
        ledger_known = document_id in state_by_id or document_id in manifest_by_id or document_id in registry_by_id
        complete = all(artifact.values()) and state == "EMBEDDING_READY"
        supported = all(bool(row["supported"]) for row in source_aliases)
        if sha in canonical_by_sha:
            classification = "ALREADY_CANONICAL"
        elif not supported:
            classification = "UNSUPPORTED"
        elif complete:
            classification = "REUSABLE_COMPLETE"
        elif ledger_known:
            classification = "RECOVERY_REQUIRED"
        else:
            classification = "NEW"
        sorted_aliases = sorted(
            source_aliases,
            key=lambda row: (str(row["source_kind"]), str(row["release"]), str(row["path"])),
        )
        for index, alias in enumerate(sorted_aliases):
            alias["alias_classification"] = "PRIMARY" if index == 0 else "EXACT_SOURCE_ALIAS"
        documents.append({
            "document_id": document_id,
            "sha256": sha,
            "classification": classification,
            "format": source_aliases[0]["format"],
            "size": source_aliases[0]["size"],
            "supported": supported,
            "source_aliases": sorted_aliases,
            "artifact_status": artifact,
            "ledger": {
                "state": state,
                "ingest_manifest": document_id in manifest_by_id,
                "source_registry": document_id in registry_by_id,
            },
        })

    incoming_ids = {row["document_id"] for row in documents}
    all_ledger_ids = set(state_by_id) | set(manifest_by_id) | set(registry_by_id)
    ledger_only = []
    for document_id in sorted(all_ledger_ids - incoming_ids):
        sha = str(
            state_by_id.get(document_id, {}).get("sha256")
            or manifest_by_id.get(document_id, {}).get("sha256")
            or registry_by_id.get(document_id, {}).get("sha256")
            or ""
        )
        status = _artifact_status(root, document_id, sha) if sha else {}
        ledger_only.append({"document_id": document_id, "sha256": sha, "artifact_status": status})

    config_files = [root / "config" / f"{name}.yaml" for name in (*_CONFIGS, "population")]
    config_identities = {
        _relative(root, path): sha256_file(path) for path in config_files if path.is_file()
    }
    manual_aliases = [row for row in aliases if row["source_kind"] == "MANUAL_INTERNAL"]
    manual_ignored = _manual_ignored(paths.incoming_manual_inbox)
    ignored_reasons = Counter(row["reason"] for row in manual_ignored)
    manual_summary = {
        "files": len(manual_aliases),
        "bytes": sum(int(row.get("size") or 0) for row in manual_aliases),
        "formats": dict(sorted(Counter(str(row["format"]) for row in manual_aliases).items())),
        "supported": sum(bool(row["supported"]) for row in manual_aliases),
        "unsupported": sum(not bool(row["supported"]) for row in manual_aliases),
        "ignored": sum(ignored_reasons.values()),
        "ignored_reasons": dict(sorted(ignored_reasons.items())),
        "unreadable": sum(bool(row.get("error")) for row in manual_aliases),
        "path_collisions": 0,
    }
    exact_sha_groups = [
        {
            "document_id": row["document_id"],
            "sha256": row["sha256"],
            "aliases": len(row["source_aliases"]),
        }
        for row in documents if len(row["source_aliases"]) > 1
    ]
    semantic = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "config_identities": dict(sorted(config_identities.items())),
        "canonical_before": {
            "state": canonical["state"],
            "manifest_sha256": canonical.get("manifest_sha256"),
            "corpus_digest": canonical.get("corpus_digest"),
        },
        "documents": documents,
        "unreadable": unreadable,
        "manual_ignored": manual_ignored,
        "manual_summary": manual_summary,
        "exact_sha_groups": exact_sha_groups,
        "papercrawler_releases": release_rows,
        "ledger_only": ledger_only,
    }
    inventory_id = identity("CPI_", semantic)
    payload = {
        "inventory_id": inventory_id,
        **semantic,
        "generated_at": now(),
        "summary": {
            "manual_aliases": sum(1 for row in aliases if row["source_kind"] == "MANUAL_INTERNAL"),
            "papercrawler_aliases": sum(1 for row in aliases if row["source_kind"] == "EXTERNAL_DISCOVERY"),
            "unique_documents": len(documents),
            "total_authoritative_bytes": sum(int(row["size"] or 0) for row in documents),
            "by_classification": dict(sorted(Counter(row["classification"] for row in documents).items())),
            "exact_aliases": sum(len(row["source_aliases"]) - 1 for row in documents),
            "unreadable": len(unreadable),
            "ledger_only": len(ledger_only),
        },
    }
    if write:
        output = paths.audit_root / "corpus_population" / "inventories" / f"{inventory_id}.json"
        if output.exists():
            existing = json.loads(output.read_text(encoding="utf-8"))
            existing.pop("generated_at", None)
            comparison = dict(payload)
            comparison.pop("generated_at", None)
            if existing != comparison:
                raise ValueError(f"existing inventory identity differs: {output}")
        else:
            atomic_json(output, payload, readonly=True)
        payload["inventory_path"] = _relative(root, output)
    return payload


__all__ = ["build_inventory"]
