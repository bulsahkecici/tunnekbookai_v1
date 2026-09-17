"""Stage registry for implemented and intentionally pending production steps."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .models import StageStatus


STAGES = (
    "BOOK_RETRIEVAL_INDEX",
    "PREWRITING_EVIDENCE_AUDIT",
    "SECTION_EVIDENCE_PACKET",
    "SECTION_WRITER",
    "POSTWRITING_EVIDENCE_AUDIT",
    "QUESTION_COVERAGE_AUDIT",
    "EDITORIAL_AUDIT",
    "SECTION_FREEZE",
    "BOOK_ASSEMBLY",
)


@dataclass(frozen=True)
class StageResult:
    stage: str
    status: StageStatus
    reason_code: str
    section_id: str | None = None
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["status"] = self.status.value
        return result


def not_implemented(stage: str, *, section_id: str | None = None) -> StageResult:
    if stage not in STAGES:
        raise ValueError(f"unknown book stage: {stage}")
    return StageResult(
        stage=stage,
        status=StageStatus.NOT_IMPLEMENTED,
        reason_code="NOT_IMPLEMENTED",
        section_id=section_id,
        detail="This stage is declared but intentionally not implemented in the foundation milestone.",
    )
