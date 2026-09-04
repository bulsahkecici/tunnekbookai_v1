"""Field-level metadata provenance (task §30, §31).

Every value in the important-field set carries a record of where it came from:

    {"field", "value", "source", "confidence", "inferred", "reason"}

`source` is one of:

    original_file          filename / filesystem-visible facts
    document_heading       the document's own first heading
    document_content       a pattern found in the extracted text
    ooxml_properties       core.xml / workbook properties written by the authoring app
    crawler_manifest       the PaperCrawler handoff record
    local_llm              loopback Qwen suggestion (always inferred=true)
    not_found              no evidence — value stays null

`inferred=true` REQUIRES a `reason` and a `confidence` (§31). `record()` enforces that.
"""

from __future__ import annotations

from typing import Any

SOURCES = {
    "original_file", "document_heading", "document_content", "ooxml_properties",
    "crawler_manifest", "local_llm", "not_found",
}

CONFIDENCE_SCORE = {"high": 0.9, "medium": 0.6, "low": 0.3}


class ProvenanceError(ValueError):
    pass


def score(confidence: Any) -> float | None:
    if confidence is None:
        return None
    if isinstance(confidence, (int, float)):
        return round(float(confidence), 4)
    return CONFIDENCE_SCORE.get(str(confidence).lower())


def record(field: str, value: Any, *, source: str, confidence: Any = None,
           inferred: bool = False, reason: str | None = None) -> dict[str, Any]:
    if source not in SOURCES:
        raise ProvenanceError(f"unknown provenance source {source!r}")
    if inferred and not reason:
        raise ProvenanceError(f"inferred value for {field!r} requires a reason (§31)")
    resolved = score(confidence)
    if inferred and resolved is None:
        raise ProvenanceError(f"inferred value for {field!r} requires a confidence (§31)")
    return {
        "field": field,
        "value": value,
        "source": source,
        "confidence": resolved,
        "inferred": bool(inferred),
        "reason": reason,
    }


def not_found(field: str, reason: str = "no reliable evidence in the document") -> dict[str, Any]:
    return {"field": field, "value": None, "source": "not_found", "confidence": None,
            "inferred": False, "reason": reason}


class ProvenanceLog:
    """Collects provenance records and keeps the metadata dict in step with them."""

    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def set(self, metadata: dict[str, Any], field: str, value: Any, *, source: str,
            confidence: Any = None, inferred: bool = False, reason: str | None = None) -> None:
        entry = record(field, value, source=source, confidence=confidence,
                       inferred=inferred, reason=reason)
        self.records.append(entry)
        if value not in (None, "", []):
            metadata[field] = value

    def miss(self, field: str, reason: str = "no reliable evidence in the document") -> None:
        self.records.append(not_found(field, reason))

    def covered_fields(self) -> set[str]:
        return {r["field"] for r in self.records}

    def missing_required(self, required: list[str]) -> list[str]:
        return [f for f in required if f not in self.covered_fields()]

    def to_dict(self, document_id: str) -> dict[str, Any]:
        return {"document_id": document_id, "fields": self.records}
