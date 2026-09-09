"""Deterministic loader for every frozen Book Production Engine input."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from .contract import BookContract, load_book_contract, resolve_project_path, sha256_file
from .errors import ContractValidationError, InputValidationError


@dataclass(frozen=True)
class BookInputs:
    contract: BookContract
    scope: tuple[Mapping[str, Any], ...]
    questions: tuple[Mapping[str, Any], ...]
    question_bank_index: Mapping[str, Any]
    scope_by_id: Mapping[str, Mapping[str, Any]]
    questions_by_section: Mapping[str, tuple[Mapping[str, Any], ...]]
    identities: Mapping[str, str]

    @property
    def question_section_ids(self) -> tuple[str, ...]:
        return tuple(row["section_id"] for row in self.scope if row.get("is_question_bank_section"))


def _read_json(path: Path, label: str) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InputValidationError(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, Mapping):
        raise InputValidationError(f"{label} root must be an object")
    return value


def _check_authority(contract: BookContract, name: str) -> Path:
    entry = contract.authorities[name]
    path = contract.authority_path(name)
    if not path.is_file():
        raise InputValidationError(f"missing authority: {name}", details={"path": str(path)})
    actual = sha256_file(path)
    expected = str(entry.get("sha256") or "")
    if actual != expected:
        raise InputValidationError(
            f"authority hash mismatch: {name}",
            details={"path": str(path), "expected": expected, "actual": actual},
        )
    return path


def _load_jsonl(path: Path) -> tuple[Mapping[str, Any], ...]:
    rows: list[Mapping[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise InputValidationError(f"cannot read question bank: {exc}") from exc
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise InputValidationError(
                "question bank contains invalid JSON",
                details={"line": line_number, "error": str(exc)},
            ) from exc
        if not isinstance(row, Mapping):
            raise InputValidationError(
                "question bank row must be an object", details={"line": line_number}
            )
        rows.append(MappingProxyType(dict(row)))
    return tuple(rows)


def _validate_scope(scope_payload: Mapping[str, Any], contract: BookContract) -> tuple[Mapping[str, Any], ...]:
    raw = scope_payload.get("sections")
    if not isinstance(raw, list) or not all(isinstance(row, Mapping) for row in raw):
        raise InputValidationError("scope.sections must be an object array")
    rows = tuple(MappingProxyType(dict(row)) for row in raw)
    expected = contract.expected_structure
    ids = [str(row.get("section_id") or "") for row in rows]
    if any(not section_id for section_id in ids) or len(ids) != len(set(ids)):
        raise InputValidationError("scope section IDs must be non-empty and unique")
    if len(rows) != expected["structural_headings"] or scope_payload.get("section_count") != len(rows):
        raise InputValidationError("scope must contain exactly 66 structural headings")
    top_level = [row for row in rows if row.get("parent_section") is None]
    if len(top_level) != expected["top_level_chapters"]:
        raise InputValidationError("scope must contain exactly 7 top-level chapters")
    if scope_payload.get("top_level_section_count") != len(top_level):
        raise InputValidationError("scope top-level chapter metadata is inconsistent")
    question_sections = [row for row in rows if row.get("is_question_bank_section") is True]
    if len(question_sections) != expected["question_bank_sections"]:
        raise InputValidationError("scope must identify exactly 59 question-bank sections")
    if scope_payload.get("question_bank_section_count") != len(question_sections):
        raise InputValidationError("scope question-bank section metadata is inconsistent")
    for row in rows:
        section_id = str(row["section_id"])
        expected_parent = ".".join(section_id.split(".")[:-1]) or None
        if not str(row.get("title") or "").strip():
            raise InputValidationError(
                "scope heading title is empty", details={"section_id": section_id}
            )
        if row.get("level") != len(section_id.split(".")):
            raise InputValidationError(
                "scope heading level is invalid", details={"section_id": section_id}
            )
        if row.get("parent_section") != expected_parent:
            raise InputValidationError(
                "scope parent relationship is invalid", details={"section_id": section_id}
            )
        # The frozen source intentionally omits ellipsis-only headings.  A declared
        # parent may therefore be absent; we validate the declared relationship but
        # never invent the missing heading.
        if row.get("active") is not True or row.get("placeholder") is not False:
            raise InputValidationError(
                "scope contains an inactive or placeholder heading", details={"section_id": section_id}
            )
        expected_questions = expected["questions_per_section"] if row.get("is_question_bank_section") is True else 0
        if row.get("question_count") != expected_questions:
            raise InputValidationError(
                "scope heading question count is invalid", details={"section_id": section_id}
            )
    return rows


def _validate_questions(
    questions: tuple[Mapping[str, Any], ...],
    scope_by_id: Mapping[str, Mapping[str, Any]],
    index: Mapping[str, Any],
    contract: BookContract,
) -> Mapping[str, tuple[Mapping[str, Any], ...]]:
    expected = contract.expected_structure
    if len(questions) != expected["total_questions"]:
        raise InputValidationError("question bank must contain exactly 2950 questions")
    ids = [str(row.get("question_id") or "") for row in questions]
    if any(not question_id for question_id in ids) or len(ids) != len(set(ids)):
        raise InputValidationError("question IDs must be non-empty and unique")
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in questions:
        section_id = str(row.get("section_id") or "")
        scope = scope_by_id.get(section_id)
        if scope is None or scope.get("is_question_bank_section") is not True:
            raise InputValidationError(
                "question maps outside the authoritative question sections",
                details={"question_id": row.get("question_id"), "section_id": section_id},
            )
        if row.get("active") is not True or not str(row.get("question") or "").strip():
            raise InputValidationError(
                "question must be active and non-empty", details={"question_id": row.get("question_id")}
            )
        if row.get("section_title") != scope.get("title"):
            raise InputValidationError(
                "question section title does not match scope",
                details={"question_id": row.get("question_id"), "section_id": section_id},
            )
        grouped.setdefault(section_id, []).append(row)

    section_counts = Counter(str(row.get("section_id") or "") for row in questions)
    expected_section_ids = {
        section_id for section_id, row in scope_by_id.items() if row.get("is_question_bank_section") is True
    }
    if set(grouped) != expected_section_ids:
        raise InputValidationError("question bank section set does not match scope")
    per_section = expected["questions_per_section"]
    for section_id in sorted(grouped, key=lambda value: tuple(int(p) for p in value.split("."))):
        rows = grouped[section_id]
        if section_counts[section_id] != per_section:
            raise InputValidationError(
                "each question-bank section must contain exactly 50 questions",
                details={"section_id": section_id, "actual": section_counts[section_id]},
            )
        numbers = sorted(row.get("question_number") for row in rows)
        if numbers != list(range(1, per_section + 1)):
            raise InputValidationError(
                "question number sequence is invalid", details={"section_id": section_id}
            )
        for row in rows:
            expected_id = f"{section_id}-Q{int(row['question_number']):02d}"
            if row.get("question_id") != expected_id:
                raise InputValidationError(
                    "question ID does not match its section and number",
                    details={"expected": expected_id, "actual": row.get("question_id")},
                )

    if index.get("total_sections") != expected["question_bank_sections"]:
        raise InputValidationError("question-bank index section count is invalid")
    if index.get("total_questions") != expected["total_questions"]:
        raise InputValidationError("question-bank index total is invalid")
    if index.get("expected_questions_per_section") != per_section:
        raise InputValidationError("question-bank index per-section count is invalid")
    index_sections = index.get("sections")
    if not isinstance(index_sections, Mapping) or set(index_sections) != expected_section_ids:
        raise InputValidationError("question-bank index section map is invalid")
    for section_id, detail in index_sections.items():
        if not isinstance(detail, Mapping):
            raise InputValidationError("question-bank index section detail must be an object")
        if detail.get("section_title") != scope_by_id[section_id].get("title"):
            raise InputValidationError("question-bank index title does not match scope")
        if detail.get("question_count") != per_section:
            raise InputValidationError("question-bank index section count is invalid")
        if detail.get("first_question_id") != f"{section_id}-Q01" or detail.get("last_question_id") != f"{section_id}-Q50":
            raise InputValidationError("question-bank index boundary IDs are invalid")
    return MappingProxyType({key: tuple(value) for key, value in grouped.items()})


def _validate_integrity_audit(audit: Mapping[str, Any]) -> None:
    if audit.get("decision") != "PASS":
        raise InputValidationError("question-bank integrity audit is not PASS")
    checks = audit.get("checks")
    if not isinstance(checks, Mapping) or not checks:
        raise InputValidationError("question-bank integrity checks are missing")
    failed = sorted(name for name, value in checks.items() if not isinstance(value, Mapping) or value.get("passed") is not True)
    if failed:
        raise InputValidationError("question-bank integrity contains failed checks", details=failed)


def _validate_source_manifest(manifest: Mapping[str, Any], contract: BookContract) -> None:
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise InputValidationError("book source manifest is empty or invalid")
    roles: set[str] = set()
    for entry in files:
        if not isinstance(entry, Mapping):
            raise InputValidationError("book source manifest entry must be an object")
        role = str(entry.get("role") or "")
        if not role or role in roles:
            raise InputValidationError("book source manifest roles must be non-empty and unique")
        roles.add(role)
        try:
            path = resolve_project_path(
                contract.project_root, entry.get("path"), field=f"source_manifest.{role}.path"
            )
        except ContractValidationError as exc:
            raise InputValidationError(str(exc)) from exc
        expected = str(entry.get("sha256") or "")
        if not path.is_file() or sha256_file(path) != expected:
            raise InputValidationError(
                "human-readable book authority is missing or changed",
                details={"role": role, "path": str(path)},
            )
    if roles != {"scope_source", "question_bank_source"}:
        raise InputValidationError("book source manifest must identify scope and question-bank sources")


def load_book_inputs(
    project_root: Path = Path(__file__).resolve().parents[2],
    contract_path: Path | str = Path("book/config/book_contract.json"),
) -> BookInputs:
    """Load and validate the complete frozen input graph, or fail closed."""

    root = Path(project_root).resolve()
    try:
        contract = load_book_contract(root, contract_path)
    except ContractValidationError:
        raise
    paths = {name: _check_authority(contract, name) for name in contract.authorities}
    scope_payload = _read_json(paths["scope"], "scope")
    scope = _validate_scope(scope_payload, contract)
    scope_by_id = MappingProxyType({str(row["section_id"]): row for row in scope})
    questions = _load_jsonl(paths["question_bank"])
    index = _read_json(paths["question_bank_index"], "question-bank index")
    questions_by_section = _validate_questions(questions, scope_by_id, index, contract)
    integrity = _read_json(paths["question_bank_integrity"], "question-bank integrity audit")
    _validate_integrity_audit(integrity)
    source_manifest = _read_json(paths["source_manifest"], "book source manifest")
    _validate_source_manifest(source_manifest, contract)
    identities = MappingProxyType({
        "book_contract_sha256": contract.contract_sha256,
        "scope_sha256": sha256_file(paths["scope"]),
        "question_bank_sha256": sha256_file(paths["question_bank"]),
        "question_bank_index_sha256": sha256_file(paths["question_bank_index"]),
        "question_bank_integrity_sha256": sha256_file(paths["question_bank_integrity"]),
        "source_manifest_sha256": sha256_file(paths["source_manifest"]),
    })
    return BookInputs(
        contract=contract,
        scope=scope,
        questions=questions,
        question_bank_index=MappingProxyType(dict(index)),
        scope_by_id=scope_by_id,
        questions_by_section=questions_by_section,
        identities=identities,
    )
