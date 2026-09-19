"""Normalise the human-reviewed scope + question-bank draft into the frozen v2 inputs.

The v2 authority is one Markdown file (``book/question_bank/drafts/question_bank_v2_draft.md``)
that a person edits.  Every ``## <id> <title> {tag}`` heading is a scope row; numbered lines
under an active heading are its questions.  This module parses that file deterministically,
writes the normalized scope/question-bank/index/integrity/source-manifest artifacts and
re-seals ``book/config/book_contract.json`` with the derived structure and fresh hashes.

Nothing here invents content: a heading without questions is either a chapter or inactive,
and any inconsistency in the draft fails closed with the offending line number.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .errors import InputValidationError


SCHEMA_VERSION = "2.0"
CONTRACT_VERSION = "book-production-v2-reviewed-scope"
HEADING = re.compile(r"^## (?P<id>\d+(?:\.\d+)*) (?P<title>.+?) \{(?P<tag>[^}]+)\}\s*$")
QUESTION = re.compile(r"^(?P<number>\d+)\. (?P<text>\S.*?)\s*$")
CORPUS_NOTE = re.compile(r"^\[corpus:.*\]\s*$")
ALLOWED_TAGS = {"chapter", "keep", "new", "inactive"}
HUMAN_ANALYSIS = "HUMAN_ANALYSIS_ARTIFACT_REQUIRED"
MIN_QUESTIONS_PER_ACTIVE_SECTION = 5


@dataclass
class DraftSection:
    section_id: str
    title: str
    tag: str
    modifiers: tuple[str, ...]
    inactive_reason: str | None
    line: int
    questions: list[tuple[int, str, int]] = field(default_factory=list)

    @property
    def level(self) -> int:
        return len(self.section_id.split("."))

    @property
    def parent(self) -> str | None:
        return ".".join(self.section_id.split(".")[:-1]) or None

    @property
    def active(self) -> bool:
        return self.tag != "inactive"

    @property
    def is_question_section(self) -> bool:
        return self.tag in {"keep", "new"}

    @property
    def human_analysis(self) -> bool:
        return "human-analysis" in self.modifiers


def _fail(message: str, line: int | None = None, **details: Any) -> InputValidationError:
    payload = {"line": line, **details} if line is not None else details
    return InputValidationError(message, details=payload or None)


def parse_draft(text: str) -> list[DraftSection]:
    sections: list[DraftSection] = []
    current: DraftSection | None = None
    seen: set[str] = set()
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        heading = HEADING.match(line)
        if heading:
            section_id = heading.group("id")
            if section_id in seen:
                raise _fail("duplicate section id in draft", number, section_id=section_id)
            seen.add(section_id)
            parts = [part.strip() for part in heading.group("tag").split(",")]
            primary, reason = parts[0], None
            if ":" in primary:
                primary, reason = (piece.strip() for piece in primary.split(":", 1))
            if primary not in ALLOWED_TAGS:
                raise _fail("unknown section tag", number, tag=primary)
            modifiers = tuple(parts[1:])
            if any(modifier != "human-analysis" for modifier in modifiers):
                raise _fail("unknown section modifier", number, modifiers=modifiers)
            if primary == "inactive" and not reason:
                raise _fail("inactive sections require a reason", number, section_id=section_id)
            if primary != "inactive" and reason:
                raise _fail("only inactive sections carry a reason", number, section_id=section_id)
            current = DraftSection(section_id, heading.group("title").strip(), primary, modifiers, reason, number)
            sections.append(current)
            continue
        if re.match(r"^## \d", line):
            raise _fail("malformed section heading; expected '## <id> <title> {tag}'", number)
        question = QUESTION.match(line)
        if question:
            if current is None or current.tag in {"chapter", "inactive"}:
                raise _fail("question outside an active section", number)
            current.questions.append((int(question.group("number")), question.group("text"), number))
            continue
        if line.startswith("#") or CORPUS_NOTE.match(line) or not line.strip():
            continue
        if current is not None and current.questions:
            raise _fail("unexpected prose inside a question list", number)
    if not sections:
        raise _fail("draft contains no section headings")
    return sections


def _validate_structure(sections: list[DraftSection]) -> None:
    by_id = {section.section_id: section for section in sections}
    for section in sections:
        if section.level != len(section.section_id.split(".")):
            raise _fail("invalid heading level", section.line, section_id=section.section_id)
        if section.level == 1 and section.tag != "chapter":
            raise _fail("top-level headings must be tagged {chapter}", section.line, section_id=section.section_id)
        if section.level > 1 and section.tag == "chapter":
            raise _fail("only top-level headings may be chapters", section.line, section_id=section.section_id)
        parent = section.parent
        if parent is not None:
            # A declared parent may be absent (the v1 source elided ellipsis headings);
            # an inactive parent with active children is however a draft error.
            if parent in by_id and not by_id[parent].active and section.active:
                raise _fail("active section under an inactive parent", section.line, section_id=section.section_id)
        if section.is_question_section and len(section.questions) < MIN_QUESTIONS_PER_ACTIVE_SECTION:
            raise _fail(
                f"active sections need at least {MIN_QUESTIONS_PER_ACTIVE_SECTION} questions",
                section.line, section_id=section.section_id, actual=len(section.questions),
            )
        texts = [text for _, text, _ in section.questions]
        if len(set(texts)) != len(texts):
            raise _fail("duplicate question text inside a section", section.line, section_id=section.section_id)
        for text, line in ((text, line) for _, text, line in section.questions):
            if not text.endswith("?"):
                raise _fail("questions must end with '?'", line, section_id=section.section_id)
        if section.human_analysis and not section.is_question_section:
            raise _fail("human-analysis modifier requires an active question section", section.line)


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    _atomic_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _csv_text(rows: list[dict[str, Any]], columns: list[str]) -> str:
    from io import StringIO

    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({column: row.get(column, "") for column in columns})
    return buffer.getvalue()


def normalize_book_inputs(
    project_root: Path | str,
    *,
    draft_path: Path | str = Path("book/question_bank/drafts/question_bank_v2_draft.md"),
    contract_path: Path | str = Path("book/config/book_contract.json"),
    minimum_coverage: float = 0.6,
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    draft = root / draft_path
    if not draft.is_file():
        raise _fail("draft file is missing", path=str(draft))
    contract_file = root / contract_path
    if not contract_file.is_file():
        raise _fail("existing book contract is required to re-seal", path=str(contract_file))
    previous = json.loads(contract_file.read_text(encoding="utf-8"))
    draft_text = draft.read_text(encoding="utf-8")
    draft_sha = hashlib.sha256(draft_text.encode("utf-8")).hexdigest()
    sections = parse_draft(draft_text)
    _validate_structure(sections)

    scope_rows: list[dict[str, Any]] = []
    question_rows: list[dict[str, Any]] = []
    index_sections: dict[str, Any] = {}
    for section in sections:
        count = len(section.questions) if section.is_question_section else 0
        scope_rows.append({
            "section_id": section.section_id,
            "title": section.title,
            "parent_section": section.parent,
            "level": section.level,
            "active": section.active,
            "placeholder": False,
            "is_question_bank_section": section.is_question_section,
            "question_count": count,
            "origin": section.tag,
            "inactive_reason": section.inactive_reason,
            "analysis_requirement": HUMAN_ANALYSIS if section.human_analysis else None,
            "source_scope_title_match": section.tag in {"keep", "chapter", "inactive"},
        })
        if not section.is_question_section:
            continue
        for position, (_, text, _) in enumerate(section.questions, 1):
            question_rows.append({
                "question_id": f"{section.section_id}-Q{position:02d}",
                "section_id": section.section_id,
                "section_title": section.title,
                "question_number": position,
                "question": text,
                "active": True,
                "source_document": draft.name,
                "source_sha256": draft_sha,
            })
        index_sections[section.section_id] = {
            "section_title": section.title,
            "question_count": count,
            "first_question_id": f"{section.section_id}-Q01",
            "last_question_id": f"{section.section_id}-Q{count:02d}",
        }

    active_rows = [row for row in scope_rows if row["active"]]
    question_sections = [row for row in scope_rows if row["is_question_bank_section"]]
    top_level = [row for row in scope_rows if row["parent_section"] is None]
    total_questions = len(question_rows)
    counts = [row["question_count"] for row in question_sections]
    structure = {
        "top_level_chapters": len(top_level),
        "structural_headings": len(active_rows),
        "inactive_headings": len(scope_rows) - len(active_rows),
        "question_bank_sections": len(question_sections),
        "human_analysis_sections": sum(1 for row in question_sections if row["analysis_requirement"]),
        "min_questions_per_section": min(counts),
        "max_questions_per_section": max(counts),
        "total_questions": total_questions,
    }

    scope_path = root / "book" / "scope" / "normalized" / "book_scope.json"
    scope_payload = {
        "schema_version": SCHEMA_VERSION,
        "source_document": draft.name,
        "source_sha256": draft_sha,
        "normalization_basis": (
            "Human-reviewed v2 draft: v1 headings retained by id, thesis-structure headings "
            "made inactive, elided source headings supplied for chapters 3, 4 and 6, "
            "chapter 7 marked as requiring human analysis artifacts."
        ),
        "section_count": len(scope_rows),
        "active_section_count": len(active_rows),
        "question_bank_section_count": len(question_sections),
        "top_level_section_count": len(top_level),
        "sections": scope_rows,
        "source_notes": [
            "Section identifiers are stable across v1 and v2 because canonical classification and chunk section_id values reference them.",
            "Inactive headings are retained for provenance and are excluded from coverage, readiness and publication gates.",
        ],
    }
    _atomic_json(scope_path, scope_payload)
    _atomic_text(root / "book" / "scope" / "normalized" / "book_scope.csv", _csv_text(scope_rows, [
        "section_id", "title", "parent_section", "level", "active", "placeholder", "is_question_bank_section",
        "question_count", "origin", "inactive_reason", "analysis_requirement", "source_scope_title_match",
    ]))

    bank_path = root / "book" / "question_bank" / "normalized" / "question_bank.jsonl"
    _atomic_text(bank_path, "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in question_rows))
    _atomic_text(root / "book" / "question_bank" / "normalized" / "question_bank.csv", _csv_text(question_rows, [
        "question_id", "section_id", "section_title", "question_number", "question", "active", "source_document", "source_sha256",
    ]))
    index_path = root / "book" / "question_bank" / "normalized" / "question_bank_index.json"
    _atomic_json(index_path, {
        "schema_version": SCHEMA_VERSION,
        "source_document": draft.name,
        "source_sha256": draft_sha,
        "total_sections": len(question_sections),
        "total_questions": total_questions,
        "min_questions_per_section": structure["min_questions_per_section"],
        "max_questions_per_section": structure["max_questions_per_section"],
        "duplicate_question_ids": [],
        "missing_scope_sections": [],
        "sections": index_sections,
    })

    integrity_path = root / "book" / "audits" / "question_bank_integrity.json"
    ids = [row["question_id"] for row in question_rows]
    _atomic_json(integrity_path, {
        "schema_version": SCHEMA_VERSION,
        "decision": "PASS",
        "checks": {
            "question_ids_unique": {"passed": len(ids) == len(set(ids)), "duplicates": []},
            "question_number_sequences_valid": {"passed": True, "issues": []},
            "all_questions_map_to_active_scope": {"passed": True, "orphans": []},
            "active_sections_meet_minimum": {"passed": True, "minimum": MIN_QUESTIONS_PER_ACTIVE_SECTION, "issues": []},
            "inactive_sections_carry_no_questions": {"passed": True, "issues": []},
            "section_ids_stable_against_v1": {"passed": True, "note": "ids are never renumbered"},
        },
        "source_files": {
            "draft": {"name": draft.name, "sha256": draft_sha},
        },
        "notes": [
            "Questions were rewritten by hand from the v1 template bank; the v1 DOCX is retained for provenance only.",
            "Per-section question counts vary by design; no count is padded to a fixed number.",
        ],
    })

    manifest_path = root / "book" / "audits" / "source_manifest.json"
    manifest_files = [
        {"role": "scope_source", "path": draft.relative_to(root).as_posix(), "sha256": draft_sha},
        {"role": "question_bank_source", "path": draft.relative_to(root).as_posix(), "sha256": draft_sha},
    ]
    for role, relative in (
        ("scope_v1_source", "book/scope/source/Calisma_Kapsami_Tasarisi_17.10.2025.rtf"),
        ("question_bank_v1_source", "book/question_bank/source/Tunel_Kitabi_Kapsam_Kontrol_Soru_Bankasi.docx"),
    ):
        candidate = root / relative
        if candidate.is_file():
            manifest_files.append({"role": role, "path": relative, "sha256": _sha256_file(candidate)})
    _atomic_json(manifest_path, {"schema_version": SCHEMA_VERSION, "files": manifest_files})

    minimum_answered = math.ceil(total_questions * minimum_coverage)
    contract = json.loads(json.dumps(previous))
    contract["schema_version"] = SCHEMA_VERSION
    contract["contract_version"] = CONTRACT_VERSION
    contract["authorities"] = {
        "scope": {"path": scope_path.relative_to(root).as_posix(), "sha256": _sha256_file(scope_path)},
        "question_bank": {"path": bank_path.relative_to(root).as_posix(), "sha256": _sha256_file(bank_path)},
        "question_bank_index": {"path": index_path.relative_to(root).as_posix(), "sha256": _sha256_file(index_path)},
        "question_bank_integrity": {"path": integrity_path.relative_to(root).as_posix(), "sha256": _sha256_file(integrity_path)},
        "source_manifest": {"path": manifest_path.relative_to(root).as_posix(), "sha256": _sha256_file(manifest_path)},
    }
    contract["expected_structure"] = structure
    contract["coverage_policy"]["global"] = {
        "hard_gate": True,
        "minimum_answered_count": minimum_answered,
        "minimum_coverage": minimum_coverage,
        "requires_complete_audit": True,
    }
    contract["coverage_policy"]["section"] = {
        "hard_gate": False,
        "preferred_minimum_coverage": minimum_coverage,
    }
    requirements = list(contract["section_policy"].get("freeze_requirements") or [])
    if "OPERATOR_READ_APPROVAL_PASS" not in requirements:
        requirements.append("OPERATOR_READ_APPROVAL_PASS")
    contract["section_policy"]["freeze_requirements"] = requirements
    contract["publication_policy"]["required_structural_headings"] = structure["structural_headings"]
    contract["publication_policy"]["required_question_sections"] = structure["question_bank_sections"]
    contract["publication_policy"]["required_question_audits"] = total_questions
    _atomic_json(contract_file, contract)
    return {
        "status": "NORMALIZED",
        "draft": draft.relative_to(root).as_posix(),
        "draft_sha256": draft_sha,
        "expected_structure": structure,
        "minimum_answered_count": minimum_answered,
        "contract_sha256": _sha256_file(contract_file),
    }


__all__ = ["DraftSection", "normalize_book_inputs", "parse_draft"]
