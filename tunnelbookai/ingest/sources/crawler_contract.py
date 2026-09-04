"""PaperCrawler handoff contract consumer (task §5, §72).

Supports handoff contract schema **major 2** (current PaperCrawler V1.0.0). The legacy
migrated package on disk is schema 1.1 and is accepted only with allow_legacy_1x=True,
with its field names remapped on read and never re-emitted:

    primary_section            -> provisional_primary_section
    book_sections              -> provisional_secondary_sections (ids)
    classification_confidence  -> provisional_section_confidence
    evidence_level             -> crawler_evidence_level

Per-record gate (before a record becomes a DiscoveredInput):
    producer == "paper-crawler-agent"
    paper_crawler_status == "READY_FOR_HANDOFF"
    tunnelbookai_status == "NOT_INGESTED"
    local source file exists
    sha256(local file) == record sha256
    provenance present and non-empty

METADATA_REFERENCE / RETRY_ACQUISITION / MANUAL_REVIEW / AUTO_REJECT records are skipped
(not ingested as content). provisional_* and crawler_evidence_level are preserved into
provenance; the final section/evidence are computed later by TunnelBookAI, never trusted
from the crawler.
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

_PRESERVED_PROVISIONAL = (
    "provisional_primary_section", "provisional_secondary_sections",
    "provisional_section_confidence", "provisional_classification_status",
    "provisional_document_type", "provisional_source_tier",
    "crawler_evidence_level",
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


def _remap_legacy(rec: dict) -> dict:
    out = dict(rec)
    out.setdefault("provisional_primary_section", rec.get("primary_section"))
    if "provisional_secondary_sections" not in out:
        bs = rec.get("book_sections") or []
        ids = [b.get("id") for b in bs if isinstance(b, dict) and b.get("id")]
        out["provisional_secondary_sections"] = [i for i in ids if i != out.get("provisional_primary_section")]
    out.setdefault("provisional_section_confidence", rec.get("classification_confidence"))
    out.setdefault("crawler_evidence_level", rec.get("evidence_level"))
    out.setdefault("provisional_classification_status", rec.get("classification_status"))
    out.setdefault("source_kind", SOURCE_KIND)
    return out


def _schema_major(value: str) -> int:
    try:
        return int(str(value).split(".", 1)[0])
    except (ValueError, AttributeError):
        return -1


def find_release_dirs(releases_root: Path | None = None) -> list[Path]:
    root = releases_root or PATHS.incoming_crawler_releases
    if not root.is_dir():
        return []
    out = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / "00_registry" / "handoff_contract.json").is_file():
            out.append(child)
    return out


def consume_release(release_dir: Path, *, allow_legacy_1x: bool = False) -> ContractResult:
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
    if major == 2:
        pass
    elif major == 1 and allow_legacy_1x:
        pass
    else:
        blockers.append(f"unsupported_contract_schema:{schema_version}")

    manifest_name = contract.get("handoff_manifest", "00_registry/handoff_manifest.jsonl")
    records = _read_jsonl(release_dir / manifest_name)
    if not records:
        blockers.append("handoff_manifest_missing_or_empty")

    if blockers:
        return ContractResult(release_dir, schema_version, [], [], blockers)

    seen_ids: set[str] = set()
    for rec in records:
        if major == 1:
            rec = _remap_legacy(rec)
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

        preserved = {k: rec.get(k) for k in _PRESERVED_PROVISIONAL if k in rec}
        accepted.append(DiscoveredInput(
            input_path=local,
            source_kind=SOURCE_KIND,
            provenance={
                "source_kind": SOURCE_KIND,
                "producer": PRODUCER,
                "release": release_dir.name,
                "canonical_id": cid,
                "crawler_document_id": rec.get("document_id"),
                "declared_sha256": declared_sha or actual_sha,
                "provenance": provenance,
                "crawler_provisional": preserved,
                "contract_schema_version": schema_version,
            },
            crawler_record=rec,
            notes=[],
        ))

    return ContractResult(release_dir, schema_version, accepted, skipped, [])


def discover(*, allow_legacy_1x: bool = False,
             releases_root: Path | None = None) -> list[ContractResult]:
    return [consume_release(d, allow_legacy_1x=allow_legacy_1x)
            for d in find_release_dirs(releases_root)]
