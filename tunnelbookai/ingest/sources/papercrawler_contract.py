"""PaperCrawler schema-2.x Source Pack consumer.

Producer book-section fields are optional compatibility residue. They are not required,
trusted, mapped into the internal source model, or used by TunnelBookAI classification.

Per-record gate (before a record becomes a DiscoveredInput):
    producer == "paper-crawler-agent"
    paper_crawler_status == "READY_FOR_HANDOFF"
    tunnelbookai_status == "NOT_INGESTED"
    local source file exists
    sha256(local file) == record sha256
    provenance present and non-empty

METADATA_REFERENCE / RETRY_ACQUISITION / MANUAL_REVIEW / AUTO_REJECT records are skipped.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..ids import sha256_file
from ..paths import PATHS
from . import DiscoveredInput

SOURCE_KIND = "EXTERNAL_DISCOVERY"
PRODUCER = "paper-crawler-agent"
READY = "READY_FOR_HANDOFF"

DEPRECATED_SECTION_FIELDS = (
    "provisional_primary_section", "provisional_secondary_sections", "book_sections",
    "primary_section", "secondary_section", "secondary_sections", "chapter", "chapter_id",
    "toc_section", "parent_section", "crawler_section",
)


@dataclass
class ContractResult:
    release_dir: Path
    schema_version: str
    accepted: list[DiscoveredInput]
    skipped: list[dict]        # {canonical_id, reason}
    blockers: list[str]        # release-level fatal problems


def _read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _schema_parts(value: str) -> tuple[int, int]:
    try:
        parts = str(value).split(".", 1)
        return int(parts[0]), int(parts[1]) if len(parts) > 1 else 0
    except (ValueError, AttributeError):
        return -1, -1


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def _safe_file(release_dir: Path, relative: Any) -> Path | None:
    value = str(relative or "")
    rel = Path(value)
    if not value or rel.is_absolute() or ".." in rel.parts:
        return None
    root = release_dir.resolve()
    resolved = (release_dir / rel).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return None
    return resolved


def _manifest_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _checksum_ledger(release_dir: Path, relative: Any) -> tuple[dict[str, str], list[str]]:
    path = _safe_file(release_dir, relative)
    if path is None or not path.is_file():
        return {}, ["checksums_missing_or_unsafe"]
    values: dict[str, str] = {}
    errors: list[str] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            declared, relative_path = line.split("  ", 1)
        except ValueError:
            errors.append(f"checksums_invalid_line:{number}")
            continue
        target = _safe_file(release_dir, relative_path)
        if target is None:
            errors.append(f"checksums_unsafe_path:{relative_path}")
            continue
        if relative_path in values:
            errors.append(f"checksums_duplicate_path:{relative_path}")
            continue
        values[relative_path] = declared.lower()
        if not target.is_file() or sha256_file(target) != declared.lower():
            errors.append(f"checksums_mismatch:{relative_path}")
    return values, errors


def find_release_dirs(
    releases_root: Path | None = None, *, release_id: str | None = None,
) -> list[Path]:
    root = releases_root or PATHS.incoming_papercrawler_releases
    if not root.is_dir():
        return []
    out = []
    for child in sorted(root.iterdir()):
        if child.name.startswith(".") or child.name.endswith(".partial"):
            continue
        if release_id is not None and child.name != release_id:
            continue
        if child.is_dir() and (child / "00_registry" / "handoff_contract.json").is_file():
            out.append(child)
    return out


def consume_release(release_dir: Path) -> ContractResult:
    release_dir = Path(release_dir)
    registry = release_dir / "00_registry"
    contract = _read_json(registry / "handoff_contract.json")
    blockers: list[str] = []
    accepted: list[DiscoveredInput] = []
    skipped: list[dict] = []

    schema_version = str(contract.get("schema_version", ""))
    major, minor = _schema_parts(schema_version)
    strict_release = major == 2 and minor >= 1
    if contract.get("producer") != PRODUCER:
        blockers.append(f"wrong_producer:{contract.get('producer')!r}")
    if major != 2:
        blockers.append(f"unsupported_contract_schema:{schema_version}")

    manifest_name = contract.get("handoff_manifest", "00_registry/handoff_manifest.jsonl")
    manifest_path = _safe_file(release_dir, manifest_name)
    if manifest_path is None:
        blockers.append("handoff_manifest_path_unsafe")
        records = []
    else:
        try:
            records = _read_jsonl(manifest_path)
        except (OSError, ValueError, json.JSONDecodeError):
            records = []
            blockers.append("handoff_manifest_invalid")
    if not records:
        blockers.append("handoff_manifest_missing_or_empty")

    release_metadata = _read_json(registry / "release_metadata.json")
    quality_rel = contract.get("quality_gate", "99_audit/handoff_quality_gate.json")
    quality_path = _safe_file(release_dir, quality_rel)
    quality = _read_json(quality_path) if quality_path is not None else {}
    ledger: dict[str, str] = {}
    if strict_release:
        complete = _read_json(registry / "RELEASE_COMPLETE.json")
        if complete.get("status") != "COMPLETE":
            blockers.append("release_not_complete")
        if quality.get("decision") != "GO":
            blockers.append("handoff_quality_gate_not_go")
        if not release_metadata:
            blockers.append("release_metadata_missing")
        expected_release_id = release_dir.name.removesuffix(".partial")
        if release_metadata.get("release_id") != expected_release_id:
            blockers.append("release_id_mismatch")
        if manifest_path is not None and manifest_path.is_file():
            actual_manifest_sha = _manifest_sha256(manifest_path)
            fingerprints = {
                str(contract.get("manifest_sha256") or ""),
                str(release_metadata.get("manifest_sha256") or ""),
                str(quality.get("manifest_sha256") or ""),
            }
            if "" in fingerprints or fingerprints != {actual_manifest_sha}:
                blockers.append("manifest_fingerprint_mismatch")
        ledger, ledger_errors = _checksum_ledger(
            release_dir, contract.get("checksums", "00_registry/checksums.sha256")
        )
        blockers.extend(ledger_errors)
        checksum_path = _safe_file(
            release_dir, contract.get("checksums", "00_registry/checksums.sha256")
        )
        if (
            checksum_path is None
            or not checksum_path.is_file()
            or not complete.get("checksums_sha256")
            or sha256_file(checksum_path) != complete.get("checksums_sha256")
        ):
            blockers.append("checksums_fingerprint_mismatch")
        if str(quality_rel) not in ledger:
            blockers.append("quality_gate_not_checksummed")
    else:
        checksum_rel = contract.get("checksums", "00_registry/checksums.sha256")
        checksum_path = _safe_file(release_dir, checksum_rel)
        if checksum_path is not None and checksum_path.is_file():
            ledger, ledger_errors = _checksum_ledger(release_dir, checksum_rel)
            blockers.extend(ledger_errors)

    canonical_ids = [str(rec.get("canonical_id") or rec.get("document_id") or "") for rec in records]
    document_ids = [str(rec.get("document_id") or "") for rec in records]
    declared_shas = [str(rec.get("sha256") or "") for rec in records]
    if "" in canonical_ids or len(canonical_ids) != len(set(canonical_ids)):
        blockers.append("duplicate_or_missing_canonical_id")
    if "" in document_ids or len(document_ids) != len(set(document_ids)):
        blockers.append("duplicate_or_missing_document_id")
    if "" in declared_shas or len(declared_shas) != len(set(declared_shas)):
        blockers.append("duplicate_or_missing_sha256")

    if blockers:
        return ContractResult(release_dir, schema_version, [], [], sorted(set(blockers)))

    for rec in records:
        cid = rec.get("canonical_id") or rec.get("document_id") or ""
        pcs = rec.get("paper_crawler_status") or rec.get("handoff_status")
        tbs = rec.get("tunnelbookai_status", "NOT_INGESTED")
        if pcs != READY:
            skipped.append({"canonical_id": cid, "reason": f"status_{pcs}"})
            continue
        if tbs != "NOT_INGESTED":
            skipped.append({"canonical_id": cid, "reason": f"tunnelbookai_status_{tbs}"})
            continue

        representation = rec.get("source_representation") or {}
        authoritative_rel = representation.get("original_or_raw") or rec.get("local_path") or ""
        local = _safe_file(release_dir, authoritative_rel)
        if local is None:
            skipped.append({"canonical_id": cid, "reason": "unsafe_authoritative_path"})
            continue
        if not local.is_file():
            skipped.append({"canonical_id": cid, "reason": "authoritative_source_missing"})
            continue
        declared_sha = str(representation.get("original_or_raw_sha256") or "").lower()
        if not declared_sha and authoritative_rel == rec.get("local_path"):
            declared_sha = str(rec.get("sha256") or "").lower()
        if not declared_sha:
            declared_sha = ledger.get(str(authoritative_rel), "")
        if not declared_sha:
            skipped.append({"canonical_id": cid, "reason": "authoritative_sha256_missing"})
            continue
        actual_sha = sha256_file(local)
        if declared_sha != actual_sha:
            reason = "authoritative_sha256_mismatch" if strict_release else "sha256_mismatch"
            skipped.append({"canonical_id": cid, "reason": reason})
            continue
        if strict_release and (
            rec.get("local_path") != authoritative_rel
            or str(rec.get("sha256") or "").lower() != declared_sha
        ):
            skipped.append({"canonical_id": cid, "reason": "authoritative_source_fields_inconsistent"})
            continue
        provenance = rec.get("provenance") or {}
        if not provenance:
            skipped.append({"canonical_id": cid, "reason": "provenance_missing"})
            continue

        deprecated = [key for key in DEPRECATED_SECTION_FIELDS if key in rec]
        selection = (
            "source_representation.original_or_raw"
            if representation.get("original_or_raw") else "legacy_local_path"
        )
        accepted.append(DiscoveredInput(
            input_path=local,
            source_kind=SOURCE_KIND,
            provenance={
                "source_kind": SOURCE_KIND,
                "producer": PRODUCER,
                "release": release_dir.name,
                "release_metadata": release_metadata,
                "canonical_id": cid,
                "producer_document_id": rec.get("document_id"),
                "declared_sha256": declared_sha,
                "authoritative_source": {
                    "selection": selection,
                    "path": str(authoritative_rel),
                    "sha256": declared_sha,
                },
                "provenance": provenance,
                "producer_provenance": provenance,
                "contract_schema_version": schema_version,
            },
            crawler_record=rec,
            notes=[f"DEPRECATED_PRODUCER_SECTION_FIELD:{key}" for key in deprecated],
        ))

    if strict_release and skipped:
        reasons = sorted({str(row.get("reason") or "unknown") for row in skipped})
        return ContractResult(
            release_dir, schema_version, [], skipped,
            [f"record_validation_failed:{reason}" for reason in reasons],
        )
    return ContractResult(release_dir, schema_version, accepted, skipped, [])


def discover(
    *, releases_root: Path | None = None, release_id: str | None = None,
) -> list[ContractResult]:
    return [consume_release(d) for d in find_release_dirs(releases_root, release_id=release_id)]
