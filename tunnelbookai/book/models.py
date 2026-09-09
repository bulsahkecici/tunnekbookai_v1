"""Typed semantic states and traceability records for book production."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Iterable, Mapping

from .errors import ReferenceIntegrityError


class QuestionEvidenceStatus(StrEnum):
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    UNSUPPORTED = "UNSUPPORTED"


class QuestionCoverageStatus(StrEnum):
    ANSWERED = "ANSWERED"
    PARTIAL = "PARTIAL"
    NOT_ANSWERED = "NOT_ANSWERED"


class SectionReadinessStatus(StrEnum):
    READY = "READY"
    READY_WITH_LIMITATIONS = "READY_WITH_LIMITATIONS"
    EVIDENCE_GAP = "EVIDENCE_GAP"
    HUMAN_ANALYSIS_ARTIFACT_REQUIRED = "HUMAN_ANALYSIS_ARTIFACT_REQUIRED"
    BLOCKED = "BLOCKED"


class FreezeStatus(StrEnum):
    NOT_FROZEN = "NOT_FROZEN"
    FREEZE_ELIGIBLE = "FREEZE_ELIGIBLE"
    FROZEN = "FROZEN"
    INTEGRITY_FAILED = "INTEGRITY_FAILED"
    UNFROZEN = "UNFROZEN"


class AnalysisArtifactStatus(StrEnum):
    NOT_REQUIRED = "NOT_REQUIRED"
    REQUIRED_MISSING = "REQUIRED_MISSING"
    AVAILABLE = "AVAILABLE"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class EvidenceType(StrEnum):
    LITERATURE_EVIDENCE = "LITERATURE_EVIDENCE"
    PROJECT_ANALYSIS_EVIDENCE = "PROJECT_ANALYSIS_EVIDENCE"
    HUMAN_ANALYSIS_ARTIFACT = "HUMAN_ANALYSIS_ARTIFACT"


class StatementEvidenceStatus(StrEnum):
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    UNSUPPORTED = "UNSUPPORTED"
    NON_FACTUAL_OR_EDITORIAL = "NON_FACTUAL_OR_EDITORIAL"


class StageStatus(StrEnum):
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    BLOCKED = "BLOCKED"
    COMPLETE = "COMPLETE"


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ReferenceIntegrityError(f"{field} must be a non-empty string")
    return text


def _text_tuple(value: Any, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, (list, tuple)):
        raise ReferenceIntegrityError(f"{field} must be an array")
    values = tuple(_required_text(item, field) for item in value)
    if len(values) != len(set(values)):
        raise ReferenceIntegrityError(f"{field} must not contain duplicates")
    return values


@dataclass(frozen=True)
class AnswerSpan:
    section_file: str
    paragraph_or_sentence_ids: tuple[str, ...]

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "AnswerSpan":
        span = cls(
            section_file=_required_text(payload.get("section_file"), "section_file"),
            paragraph_or_sentence_ids=_text_tuple(
                payload.get("paragraph_or_sentence_ids"), "paragraph_or_sentence_ids"
            ),
        )
        if not span.paragraph_or_sentence_ids:
            raise ReferenceIntegrityError("an answer span must identify a paragraph or sentence")
        return span


@dataclass(frozen=True)
class QuestionCoverageResult:
    question_id: str
    section_id: str
    question: str
    status: QuestionCoverageStatus
    answer_spans: tuple[AnswerSpan, ...]
    supporting_claim_ids: tuple[str, ...]
    supporting_document_ids: tuple[str, ...]
    source_locators: tuple[str, ...]
    confidence: float
    reason: str

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "QuestionCoverageResult":
        try:
            status = QuestionCoverageStatus(str(payload.get("status") or ""))
        except ValueError as exc:
            raise ReferenceIntegrityError("question coverage status is invalid") from exc
        raw_spans = payload.get("answer_spans") or []
        if not isinstance(raw_spans, list):
            raise ReferenceIntegrityError("answer_spans must be an array")
        try:
            confidence = float(payload.get("confidence", 0.0))
        except (TypeError, ValueError) as exc:
            raise ReferenceIntegrityError("confidence must be numeric") from exc
        if not 0.0 <= confidence <= 1.0:
            raise ReferenceIntegrityError("confidence must be between 0 and 1")
        result = cls(
            question_id=_required_text(payload.get("question_id"), "question_id"),
            section_id=_required_text(payload.get("section_id"), "section_id"),
            question=_required_text(payload.get("question"), "question"),
            status=status,
            answer_spans=tuple(AnswerSpan.from_mapping(item) for item in raw_spans),
            supporting_claim_ids=_text_tuple(
                payload.get("supporting_claim_ids"), "supporting_claim_ids"
            ),
            supporting_document_ids=_text_tuple(
                payload.get("supporting_document_ids"), "supporting_document_ids"
            ),
            source_locators=_text_tuple(payload.get("source_locators"), "source_locators"),
            confidence=confidence,
            reason=str(payload.get("reason") or "").strip(),
        )
        if result.status is QuestionCoverageStatus.ANSWERED:
            missing = [
                name
                for name, value in (
                    ("answer_spans", result.answer_spans),
                    ("supporting_claim_ids", result.supporting_claim_ids),
                    ("supporting_document_ids", result.supporting_document_ids),
                    ("source_locators", result.source_locators),
                )
                if not value
            ]
            if missing:
                raise ReferenceIntegrityError(
                    "ANSWERED requires traceable spans and evidence identities",
                    details={"missing": missing, "question_id": result.question_id},
                )
        return result


@dataclass(frozen=True)
class EvidenceClaim:
    claim_id: str
    claim_text: str
    document_id: str
    chunk_id: str
    locator: str
    section_id: str
    evidence_strength: str
    authority_class: str
    provenance_status: str
    qualifiers: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "EvidenceClaim":
        return cls(
            claim_id=_required_text(payload.get("claim_id"), "claim_id"),
            claim_text=_required_text(payload.get("claim_text"), "claim_text"),
            document_id=_required_text(payload.get("document_id"), "document_id"),
            chunk_id=_required_text(payload.get("chunk_id"), "chunk_id"),
            locator=_required_text(payload.get("locator"), "locator"),
            section_id=_required_text(payload.get("section_id"), "section_id"),
            evidence_strength=_required_text(payload.get("evidence_strength"), "evidence_strength"),
            authority_class=_required_text(payload.get("authority_class"), "authority_class"),
            provenance_status=_required_text(payload.get("provenance_status"), "provenance_status"),
            qualifiers=_text_tuple(payload.get("qualifiers"), "qualifiers"),
            conditions=_text_tuple(payload.get("conditions"), "conditions"),
            limitations=_text_tuple(payload.get("limitations"), "limitations"),
        )


def validate_result_references(
    result: QuestionCoverageResult,
    *,
    expected_section_id: str,
    known_claim_ids: Iterable[str],
    known_document_ids: Iterable[str],
    known_locators: Iterable[str],
    known_span_ids: Iterable[str],
    allowed_section_files: Iterable[str],
) -> None:
    """Reject scope mismatches and references not present in admitted evidence."""

    if result.section_id != expected_section_id:
        raise ReferenceIntegrityError(
            "question result section does not match the target section",
            details={"expected": expected_section_id, "actual": result.section_id},
        )
    checks = (
        ("claim_ids", result.supporting_claim_ids, set(known_claim_ids)),
        ("document_ids", result.supporting_document_ids, set(known_document_ids)),
        ("locators", result.source_locators, set(known_locators)),
    )
    invalid = {name: sorted(set(actual) - known) for name, actual, known in checks}
    known_ids = set(known_span_ids)
    allowed_files = set(allowed_section_files)
    invalid_span_ids = sorted({
        span_id
        for span in result.answer_spans
        for span_id in span.paragraph_or_sentence_ids
        if span_id not in known_ids
    })
    invalid_section_files = sorted({
        span.section_file for span in result.answer_spans if span.section_file not in allowed_files
    })
    if invalid_span_ids:
        invalid["answer_span_ids"] = invalid_span_ids
    if invalid_section_files:
        invalid["section_files"] = invalid_section_files
    invalid = {name: values for name, values in invalid.items() if values}
    if invalid:
        raise ReferenceIntegrityError("question result references unknown evidence", details=invalid)
