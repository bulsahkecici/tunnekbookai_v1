"""Canonical ingest metadata schema (task §29, §31).

The schema is deliberately small and explicit. Every unknown value is `null` or the literal
`UNKNOWN` — nothing is ever invented (§31). Controlled vocabularies and deterministic
inference helpers live in the ingest package and have no legacy-pipeline dependency.
"""

from __future__ import annotations

from typing import Any

from . import vocabularies

CONFIDENTIALITY = {"PUBLIC", "INTERNAL", "RESTRICTED", "UNKNOWN"}
DOCUMENT_STATUS = {"FINAL", "APPROVED", "DRAFT", "WORKING_DOCUMENT", "UNKNOWN"}
SOURCE_KINDS = {"MANUAL_INTERNAL", "EXTERNAL_DISCOVERY"}

REQUIRED_FIELDS = (
    "document_id", "source_kind", "original_filename", "original_sha256",
    "format", "mime_type", "confidentiality", "document_status", "ingest_method",
)

NULLABLE_FIELDS = (
    "title", "organization", "department", "document_date", "revision", "language",
    "document_type", "source_url", "doi", "final_primary_section",
    "final_section_confidence", "final_evidence_level",
)


def empty_metadata(document_id: str) -> dict[str, Any]:
    return {
        "document_id": document_id,
        "source_kind": None,

        "original_filename": None,
        "original_sha256": None,

        "format": None,
        "mime_type": None,

        "title": None,
        "authors": [],
        "organization": None,
        "department": None,
        "document_date": None,
        "revision": None,
        "language": None,

        "document_type": None,
        "topics": [],

        "source_url": None,
        "doi": None,

        "confidentiality": "UNKNOWN",
        "document_status": "UNKNOWN",

        "ingest_method": None,

        "final_primary_section": None,
        "final_secondary_sections": [],
        "final_section_confidence": None,

        "final_evidence_level": None,
        "content_capabilities": {},

        "schema_version": "1.0",
    }


def validate(metadata: dict[str, Any]) -> list[str]:
    """Structural validation. Returns a list of problems; empty means valid (§44)."""
    problems: list[str] = []
    for field in REQUIRED_FIELDS:
        if metadata.get(field) in (None, ""):
            problems.append(f"MISSING_REQUIRED_FIELD:{field}")
    if metadata.get("confidentiality") not in CONFIDENTIALITY:
        problems.append(f"INVALID_CONFIDENTIALITY:{metadata.get('confidentiality')}")
    if metadata.get("document_status") not in DOCUMENT_STATUS:
        problems.append(f"INVALID_DOCUMENT_STATUS:{metadata.get('document_status')}")
    if metadata.get("source_kind") not in SOURCE_KINDS:
        problems.append(f"INVALID_SOURCE_KIND:{metadata.get('source_kind')}")
    if not isinstance(metadata.get("authors"), list):
        problems.append("INVALID_AUTHORS_NOT_LIST")
    if not isinstance(metadata.get("final_secondary_sections"), list):
        problems.append("INVALID_SECONDARY_SECTIONS_NOT_LIST")
    document_type = metadata.get("document_type")
    if document_type is not None:
        if document_type not in vocabularies.DOCUMENT_TYPES:
            problems.append(f"INVALID_DOCUMENT_TYPE:{document_type}")
    sha = metadata.get("original_sha256") or ""
    if sha and (len(sha) != 64 or not all(c in "0123456789abcdef" for c in sha.lower())):
        problems.append("INVALID_SHA256")
    confidence = metadata.get("final_section_confidence")
    if confidence is not None and not (0.0 <= float(confidence) <= 1.0):
        problems.append("INVALID_SECTION_CONFIDENCE")
    return problems
