"""Central coverage mathematics; PARTIAL never contributes to ANSWERED."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .contract import BookContract
from .errors import InputValidationError
from .models import QuestionCoverageResult, QuestionCoverageStatus


@dataclass(frozen=True)
class CoverageSummary:
    total: int
    answered: int
    partial: int
    not_answered: int
    coverage: float
    complete_audit: bool
    count_threshold_met: bool
    coverage_threshold_met: bool
    publication_gate_passed: bool
    book_status: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def coverage_summary_from_counts(
    *,
    answered: int,
    partial: int,
    not_answered: int,
    expected_total: int,
    minimum_answered_count: int,
    minimum_coverage: float,
    failure_status: str = "COVERAGE_REMEDIATION_REQUIRED",
) -> CoverageSummary:
    values = (answered, partial, not_answered)
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
        raise InputValidationError("coverage counts must be non-negative integers")
    total = sum(values)
    complete = total == expected_total
    coverage = answered / expected_total if expected_total else 0.0
    count_met = answered >= minimum_answered_count
    ratio_met = coverage >= minimum_coverage
    passed = complete and count_met and ratio_met
    return CoverageSummary(
        total=total,
        answered=answered,
        partial=partial,
        not_answered=not_answered,
        coverage=round(coverage, 8),
        complete_audit=complete,
        count_threshold_met=count_met,
        coverage_threshold_met=ratio_met,
        publication_gate_passed=passed,
        book_status="COVERAGE_GATE_PASS" if passed else failure_status,
    )


def global_coverage_summary(
    results: Iterable[QuestionCoverageResult], contract: BookContract
) -> CoverageSummary:
    rows = tuple(results)
    ids = [row.question_id for row in rows]
    if len(ids) != len(set(ids)):
        raise InputValidationError("global coverage results contain duplicate question IDs")
    counts = {state: 0 for state in QuestionCoverageStatus}
    for row in rows:
        counts[row.status] += 1
    policy = contract.coverage_policy["global"]
    publication = contract.payload["publication_policy"]
    return coverage_summary_from_counts(
        answered=counts[QuestionCoverageStatus.ANSWERED],
        partial=counts[QuestionCoverageStatus.PARTIAL],
        not_answered=counts[QuestionCoverageStatus.NOT_ANSWERED],
        expected_total=contract.expected_structure["total_questions"],
        minimum_answered_count=policy["minimum_answered_count"],
        minimum_coverage=policy["minimum_coverage"],
        failure_status=publication["failure_status"],
    )


def section_target_summary(
    statuses: Iterable[QuestionCoverageStatus | str], contract: BookContract, *, expected: int | None = None
) -> dict[str, object]:
    """Summarise one section's coverage; ``expected`` is that section's question count.

    V1 contracts fix every section at ``questions_per_section``; V2 sections vary, so the
    caller passes the count from scope and the preferred target is the coverage ratio.
    """

    values: list[QuestionCoverageStatus] = []
    for status in statuses:
        try:
            values.append(QuestionCoverageStatus(str(status)))
        except ValueError as exc:
            raise InputValidationError(f"invalid question coverage status: {status}") from exc
    if expected is None:
        expected = int(contract.expected_structure.get("questions_per_section") or len(values))
    if len(values) != expected:
        raise InputValidationError(f"section coverage requires exactly {expected} results")
    answered = values.count(QuestionCoverageStatus.ANSWERED)
    policy = contract.coverage_policy["section"]
    target = contract.section_target(expected)
    return {
        "total": len(values),
        "answered": answered,
        "partial": values.count(QuestionCoverageStatus.PARTIAL),
        "not_answered": values.count(QuestionCoverageStatus.NOT_ANSWERED),
        "coverage": round(answered / expected, 8),
        "preferred_target": target,
        "target_met": answered >= target and answered / expected >= policy["preferred_minimum_coverage"],
        "hard_gate": policy["hard_gate"],
    }
