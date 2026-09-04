"""TunnelBookAI Evidence Note Contract v1 - the unit of auditable book evidence.

An EvidenceNote is the smallest reusable research unit: one factual proposition (or one tightly
related cluster) tied to literal spans in corpus evidence. Nothing downstream may cite anything
that is not a contract-valid note.

Policy is fail-closed and repair-free, exactly like the generation output contract. This module
validates and rejects; it never edits a claim, invents an evidence reference, supplies a missing
unit, softens a requirement's modality or reconciles a conflict.

Two identity rules matter more than any other:

  * Evidence ids are PACKET-LOCAL. "[E001]" is meaningless on its own - it only denotes a chunk in
    combination with the context_packet_sha of the packet that assigned it. Every evidence ref must
    therefore carry both, and the validator refuses a ref that carries only the handle.
  * Provenance must survive to the chunk. A note that cannot name its chunk_id and document_id
    cannot be cited in a book.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field, asdict
from typing import Any

CONTRACT_VERSION = "tunnelbook-evidence-note-contract-v1"
REPAIR_POLICY = "none_fail_closed"

NOTE_TYPES = ("definition", "fact", "mechanism", "design_principle", "construction_principle",
              "classification", "numeric", "formula", "requirement", "recommendation",
              "comparison", "risk", "failure_mode", "case_example", "historical", "uncertainty",
              "conflict")
SUPPORT_STATUSES = ("SUPPORTED", "PARTIALLY_SUPPORTED", "INSUFFICIENT_EVIDENCE",
                    "CONFLICTING_EVIDENCE", "REJECTED")
CONFIDENCES = ("high", "medium", "low")
SUPPORT_TYPES = ("direct", "numeric_direct", "definition_direct", "table_direct",
                 "multi_source_combination", "qualified", "partial")
CONFLICT_STATUSES = ("none", "conflicting", "resolved_by_evidence")

# Statuses that assert something about the world and therefore owe literal evidence.
ASSERTIVE_STATUSES = ("SUPPORTED", "PARTIALLY_SUPPORTED")

MODALITIES = ("must", "shall", "should", "may", "recommended", "minimum", "maximum", "required",
              "zorunlu", "gerekir", "gereklidir", "olmalıdır", "yapılmalıdır", "önerilir",
              "tavsiye", "en az", "en fazla", "asgari", "azami")
# Word-boundary anchored: "en az" must not match inside "en aza indirmek" (to minimise), and
# "en fazla" must not match inside "birden fazla" (more than one). A substring match here silently
# converts ordinary prose into a normative requirement.
MODALITY_PATTERN = re.compile(
    r"(?<!\w)(?:" + "|".join(re.escape(m) for m in MODALITIES) + r")(?!\w)", re.IGNORECASE)
# A markdown table pasted whole is not a proposition; it is many, and cannot be one claim.
TABLE_BLOB = re.compile(r"(\|\s*:?-{2,})")

# Source coordinates a note may never invent in its claim text. Coordinates belong in evidence
# refs, resolved from the packet - never asserted in prose the model produced.
COORDINATE_LEAK = re.compile(
    r"\b(?:DOC\d{6}|s\.\s?\d+|sayfa\s+\d+|page\s+\d+|p\.\s?\d+|slide\s+\d+|slayt\s+\d+)\b",
    re.IGNORECASE)
CHUNK_ID_LEAK = re.compile(r"\bDOC\d{6}-C\d{4}\b")
NUMBER = re.compile(r"\d+(?:[.,]\d+)?")


class EvidenceNoteContractError(ValueError):
    """The note cannot be validated under the given inputs."""


@dataclass
class EvidenceRef:
    """A packet-local evidence handle bound to the packet that gave it meaning."""
    evidence_id: str
    context_packet_sha: str
    chunk_id: str
    document_id: str
    citation_mode: str | None = None
    provenance_status: str | None = None
    retrieval_rank: int | None = None
    retrieval_score: float | None = None
    page_start: int | None = None
    page_end: int | None = None
    slide_start: int | None = None
    slide_end: int | None = None
    section_path: str | None = None
    title: str | None = None
    source_relative_path: str | None = None
    source_key: str | None = None            # stable book-level key from the source registry

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class LiteralSupport:
    evidence_id: str
    support_text: str
    support_type: str
    start_offset: int | None = None
    end_offset: int | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class NumericFact:
    value: str | None = None
    unit: str | None = None
    range: str | None = None
    minimum: str | None = None
    maximum: str | None = None
    mean: str | None = None
    median: str | None = None
    percentage: str | None = None
    direction: str | None = None
    condition: str | None = None
    source_evidence_ids: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class FormulaFact:
    formula_text: str | None = None
    variables: list[str] = field(default_factory=list)
    units: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    source_evidence_ids: list[str] = field(default_factory=list)
    incomplete: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceNote:
    note_id: str
    book_id: str
    chapter_id: str
    section_id: str
    question_id: str
    note_type: str
    claim: str
    claim_language: str
    support_status: str
    confidence: str
    evidence_refs: list[EvidenceRef] = field(default_factory=list)
    literal_support: list[LiteralSupport] = field(default_factory=list)
    source_count: int = 0
    source_diversity: dict[str, int] = field(default_factory=dict)
    qualifiers: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    exceptions: list[str] = field(default_factory=list)
    modality: str | None = None
    numeric_data: list[NumericFact] = field(default_factory=list)
    formula_data: list[FormulaFact] = field(default_factory=list)
    conflict_status: str = "none"
    conflict_refs: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    generation_trace: dict[str, Any] = field(default_factory=dict)
    review_status: str = "unreviewed"
    created_at: str | None = None

    def canonical_payload(self) -> dict[str, Any]:
        """Deterministic content view. Timestamps and review state are excluded from the hash so
        that re-reviewing a note does not change its identity."""
        payload = asdict(self)
        payload.pop("created_at", None)
        payload.pop("review_status", None)
        return payload

    def note_sha256(self) -> str:
        return hashlib.sha256(
            json.dumps(self.canonical_payload(), ensure_ascii=False, sort_keys=True)
            .encode("utf-8")).hexdigest()

    def as_dict(self) -> dict[str, Any]:
        return {**asdict(self), "note_sha256": self.note_sha256(),
                "contract_version": CONTRACT_VERSION}


@dataclass
class NoteValidation:
    note_id: str
    valid: bool
    failure_reasons: list[str]
    note_sha256: str | None
    contract_version: str = CONTRACT_VERSION
    repair_policy: str = REPAIR_POLICY

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalise_for_span_match(text: str) -> str:
    """The single normalisation used for literal-span matching.

    Evidence text carries newlines, markdown emphasis and table padding, so matching must be
    insensitive to whitespace and punctuation. This function is exported so that any producer of
    literal spans uses the SAME rule the validator applies - a producer and validator that
    normalise differently will manufacture spans the contract then rejects.
    """
    lowered = re.sub(r"\s+", " ", text).strip().lower()
    return re.sub(r"[^\w\s]", "", lowered)


def _text_contains(haystack: str, needle: str) -> bool:
    return normalise_for_span_match(needle) in normalise_for_span_match(haystack)


def validate_note(note: EvidenceNote, packet_evidence: dict[str, dict[str, Any]] | None = None,
                  known_chunks: set[str] | None = None) -> NoteValidation:
    """Validate one note. Fail-closed: returns a verdict, never a corrected note.

    `packet_evidence` maps "<context_packet_sha>::<evidence_id>" to the evidence record it denotes,
    which is the only way to check a packet-local handle honestly.
    """
    reasons: list[str] = []

    if not note.note_id:
        reasons.append("missing_note_id")
    if not (note.claim or "").strip():
        reasons.append("missing_claim")
    if note.note_type not in NOTE_TYPES:
        reasons.append("invalid_note_type")
    if note.support_status not in SUPPORT_STATUSES:
        reasons.append("invalid_support_status")
    if note.confidence not in CONFIDENCES:
        reasons.append("invalid_confidence")
    if note.conflict_status not in CONFLICT_STATUSES:
        reasons.append("invalid_conflict_status")
    for identifier, name in ((note.book_id, "book_id"), (note.chapter_id, "chapter_id"),
                             (note.section_id, "section_id"), (note.question_id, "question_id")):
        if not identifier:
            reasons.append(f"missing_{name}")

    assertive = note.support_status in ASSERTIVE_STATUSES

    # --- evidence refs -------------------------------------------------------------------
    if assertive and not note.evidence_refs:
        reasons.append("assertive_without_evidence_refs")
    for ref in note.evidence_refs:
        if not ref.evidence_id:
            reasons.append("evidence_ref_missing_evidence_id")
        if not ref.context_packet_sha:
            # A packet-local handle without its packet is not an identifier at all.
            reasons.append("evidence_ref_missing_context_packet_sha")
        if not ref.chunk_id or not ref.document_id:
            reasons.append("evidence_ref_missing_provenance")
        if known_chunks is not None and ref.chunk_id and ref.chunk_id not in known_chunks:
            reasons.append("unknown_chunk_identity")
        if packet_evidence is not None and ref.evidence_id and ref.context_packet_sha:
            key = f"{ref.context_packet_sha}::{ref.evidence_id}"
            record = packet_evidence.get(key)
            if record is None:
                reasons.append("evidence_id_absent_from_context_packet")
            else:
                if ref.chunk_id and record.get("chunk_id") and ref.chunk_id != record["chunk_id"]:
                    reasons.append("evidence_ref_chunk_mismatch")
                if (ref.document_id and record.get("document_id")
                        and ref.document_id != record["document_id"]):
                    reasons.append("evidence_ref_document_mismatch")

    if not note.provenance:
        reasons.append("missing_provenance")

    # --- literal support -----------------------------------------------------------------
    if assertive and not note.literal_support:
        reasons.append("missing_literal_support")
    referenced = {ref.evidence_id for ref in note.evidence_refs}
    for support in note.literal_support:
        if support.support_type not in SUPPORT_TYPES:
            reasons.append("invalid_support_type")
        if not (support.support_text or "").strip():
            reasons.append("empty_literal_support_text")
        if support.evidence_id not in referenced:
            reasons.append("literal_support_references_uncited_evidence")
        if packet_evidence is not None:
            matching = [ref for ref in note.evidence_refs if ref.evidence_id == support.evidence_id]
            for ref in matching:
                record = packet_evidence.get(f"{ref.context_packet_sha}::{ref.evidence_id}")
                if record and record.get("text") is not None:
                    if not _text_contains(record["text"], support.support_text):
                        # The quoted span must actually occur in the cited evidence.
                        reasons.append("literal_support_not_found_in_evidence")

    if note.confidence == "high" and not note.literal_support:
        reasons.append("high_confidence_without_literal_support")

    # --- claim hygiene -------------------------------------------------------------------
    if COORDINATE_LEAK.search(note.claim or "") or CHUNK_ID_LEAK.search(note.claim or ""):
        reasons.append("claim_contains_source_coordinates")
    if len(TABLE_BLOB.findall(note.claim or "")) >= 2:
        # A table blob would let many unverified values ride on one span.
        reasons.append("claim_is_table_blob_not_a_proposition")

    # --- numeric -------------------------------------------------------------------------
    if note.note_type == "numeric":
        if not note.numeric_data:
            reasons.append("numeric_note_without_numeric_data")
        for fact in note.numeric_data:
            has_value = any([fact.value, fact.range, fact.minimum, fact.maximum, fact.mean,
                             fact.median, fact.percentage])
            if not has_value:
                reasons.append("numeric_data_without_value")
            if not fact.source_evidence_ids:
                reasons.append("numeric_data_without_source")
            # The span must actually carry the value it is offered as evidence for. Without this,
            # a numeric note can be "supported" by an adjacent sentence containing no number.
            if note.support_status in ASSERTIVE_STATUSES and note.literal_support:
                claimed = [v for v in (fact.value, fact.minimum, fact.maximum, fact.mean,
                                       fact.median, fact.percentage) if v]
                spans = " ".join(sp.support_text for sp in note.literal_support
                                 if sp.evidence_id in fact.source_evidence_ids)
                normalised = spans.replace(",", ".")
                if claimed and not any(v.replace(",", ".") in normalised for v in claimed):
                    reasons.append("numeric_value_absent_from_literal_span")
            if fact.unit is None and fact.percentage is None:
                # Only demand a unit when the cited evidence actually carries one next to the value.
                if packet_evidence is not None and _source_has_unit(note, fact, packet_evidence):
                    reasons.append("numeric_note_lost_unit_present_in_source")
    for fact in note.numeric_data:
        for evidence_id in fact.source_evidence_ids:
            if evidence_id not in referenced:
                reasons.append("numeric_source_not_in_evidence_refs")

    # --- formulas ------------------------------------------------------------------------
    for formula in note.formula_data:
        if formula.incomplete and note.support_status == "SUPPORTED":
            reasons.append("incomplete_formula_marked_supported")
        if not formula.source_evidence_ids:
            reasons.append("formula_without_source")

    # --- requirements --------------------------------------------------------------------
    if note.note_type in ("requirement", "recommendation"):
        if not note.modality:
            reasons.append("requirement_without_modality")
        elif note.modality.lower() not in {m.lower() for m in MODALITIES}:
            reasons.append("invalid_modality")
        elif not MODALITY_PATTERN.search(note.claim or ""):
            # Modality must survive into the claim, not just sit in a field.
            reasons.append("requirement_modality_absent_from_claim")

    # --- conflicts -----------------------------------------------------------------------
    if note.conflict_status == "conflicting":
        if not note.conflict_refs:
            reasons.append("conflict_without_conflict_refs")
        if note.support_status not in ("CONFLICTING_EVIDENCE", "PARTIALLY_SUPPORTED"):
            reasons.append("conflict_status_inconsistent_with_support_status")
    if note.support_status == "CONFLICTING_EVIDENCE" and note.conflict_status != "conflicting":
        reasons.append("conflicting_evidence_without_conflict_status")

    # --- source counts -------------------------------------------------------------------
    distinct_documents = {ref.document_id for ref in note.evidence_refs if ref.document_id}
    if note.source_count and note.source_count != len(note.evidence_refs):
        reasons.append("source_count_mismatch")
    if note.source_diversity:
        declared = note.source_diversity.get("document_count")
        if declared is not None and declared != len(distinct_documents):
            reasons.append("source_diversity_document_count_mismatch")

    ordered = sorted(set(reasons))
    return NoteValidation(note_id=note.note_id, valid=not ordered, failure_reasons=ordered,
                          note_sha256=note.note_sha256() if not ordered else None)


def _source_has_unit(note: EvidenceNote, fact: NumericFact,
                     packet_evidence: dict[str, dict[str, Any]]) -> bool:
    """True when the cited evidence shows a unit adjacent to this value and the note dropped it."""
    unit_pattern = re.compile(
        r"\d+(?:[.,]\d+)?\s*(cm|mm|m|km|kg/m³|kg/m3|MPa|kN|kPa|bar|ppm|%|psi|ft|in|inch|inches|"
        r"saat|hour|hours|yıl|year|years)\b", re.IGNORECASE)
    value = (fact.value or fact.minimum or fact.maximum or "").strip()
    if not value:
        return False
    for ref in note.evidence_refs:
        if ref.evidence_id not in fact.source_evidence_ids:
            continue
        record = packet_evidence.get(f"{ref.context_packet_sha}::{ref.evidence_id}")
        if not record or record.get("text") is None:
            continue
        for match in unit_pattern.finditer(record["text"]):
            if value in match.group(0):
                return True
    return False


def validate_notes(notes, packet_evidence=None, known_chunks=None) -> dict[str, Any]:
    results = [validate_note(n, packet_evidence, known_chunks) for n in notes]
    invalid = [r for r in results if not r.valid]
    return {"contract_version": CONTRACT_VERSION, "repair_policy": REPAIR_POLICY,
            "total": len(results), "valid": len(results) - len(invalid), "invalid": len(invalid),
            "results": results,
            "failure_histogram": _histogram(r for result in results
                                            for r in result.failure_reasons)}


def _histogram(items) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return dict(sorted(counts.items()))


def contract_identity() -> dict[str, Any]:
    from pathlib import Path
    return {"contract_version": CONTRACT_VERSION, "repair_policy": REPAIR_POLICY,
            "implementation_sha256": hashlib.sha256(
                Path(__file__).read_bytes()).hexdigest(),
            "note_types": list(NOTE_TYPES), "support_statuses": list(SUPPORT_STATUSES),
            "support_types": list(SUPPORT_TYPES), "confidences": list(CONFIDENCES)}


if __name__ == "__main__":
    print(json.dumps(contract_identity(), indent=2, ensure_ascii=False))
