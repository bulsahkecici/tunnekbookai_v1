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

import json
from dataclasses import dataclass
from pathlib import Path

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


def _schema_major(value: str) -> int:
    try:
        return int(str(value).split(".", 1)[0])
    except (ValueError, AttributeError):
        return -1


def find_release_dirs(releases_root: Path | None = None) -> list[Path]:
    root = releases_root or PATHS.incoming_papercrawler_releases
    if not root.is_dir():
        return []
    out = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / "00_registry" / "handoff_contract.json").is_file():
            out.append(child)
    return out


def consume_release(release_dir: Path) -> ContractResult:
    registry = release_dir / "00_registry"
    contract_path = registry / "handoff_contract.json"
    blockers: list[str] = []
    accepted: list[DiscoveredInput] = []
    skipped: list[dict] = []

    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    schema_version = str(contract.get("schema_version", ""))
    major = _schema_major(schema_version)
    if contract.get("producer") != PRODUCER:
        blockers.append(f"wrong_producer:{contract.get('producer')!r}")
    if major != 2:
        blockers.append(f"unsupported_contract_schema:{schema_version}")

    manifest_name = contract.get("handoff_manifest", "00_registry/handoff_manifest.jsonl")
    records = _read_jsonl(release_dir / manifest_name)
    if not records:
        blockers.append("handoff_manifest_missing_or_empty")

    if blockers:
        return ContractResult(release_dir, schema_version, [], [], blockers)

    seen_ids: set[str] = set()
    for rec in records:
        cid = rec.get("canonical_id") or rec.get("document_id") or ""
        pcs = rec.get("paper_crawler_status") or rec.get("handoff_status")
        tbs = rec.get("tunnelbookai_status", "NOT_INGESTED")

        if cid in seen_ids:
            skipped.append({"canonical_id": cid, "reason": "duplicate_canonical_id"})
            continue
        seen_ids.add(cid)

        if pcs != READY:
            skipped.append({"canonical_id": cid, "reason": f"status_{pcs}"})
            continue
        if tbs != "NOT_INGESTED":
            skipped.append({"canonical_id": cid, "reason": f"tunnelbookai_status_{tbs}"})
            continue

        local_rel = rec.get("local_path") or ""
        local = release_dir / local_rel
        if not local.is_file():
            skipped.append({"canonical_id": cid, "reason": "source_missing"})
            continue
        declared_sha = (rec.get("sha256") or "").lower()
        actual_sha = sha256_file(local)
        if declared_sha and declared_sha != actual_sha:
            skipped.append({"canonical_id": cid, "reason": "sha256_mismatch"})
            continue
        provenance = rec.get("provenance") or {}
        if not provenance:
            skipped.append({"canonical_id": cid, "reason": "provenance_missing"})
            continue

        deprecated = [key for key in DEPRECATED_SECTION_FIELDS if key in rec]
        accepted.append(DiscoveredInput(
            input_path=local,
            source_kind=SOURCE_KIND,
            provenance={
                "source_kind": SOURCE_KIND,
                "producer": PRODUCER,
                "release": release_dir.name,
                "canonical_id": cid,
                "producer_document_id": rec.get("document_id"),
                "declared_sha256": declared_sha or actual_sha,
                "provenance": provenance,
                "contract_schema_version": schema_version,
            },
            crawler_record=rec,
            notes=[f"DEPRECATED_PRODUCER_SECTION_FIELD:{key}" for key in deprecated],
        ))

    return ContractResult(release_dir, schema_version, accepted, skipped, [])


def discover(*, releases_root: Path | None = None) -> list[ContractResult]:
    return [consume_release(d) for d in find_release_dirs(releases_root)]
