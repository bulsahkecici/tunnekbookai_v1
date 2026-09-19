"""Deterministic editorial hard gate with an advisory local-Qwen review."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from tunnelbookai.canonical.hashing import canonical_sha256, sha256_file
from tunnelbookai.ingest.classify.arbiter import LocalChatClient

from .coverage_audit import inspect_coverage_audits
from .errors import BookEngineError
from .evidence_review import inspect_evidence_reviews
from .inputs import load_book_inputs
from .prewriting import _llm_settings
from .writer import inspect_drafts


SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "editorial-audit-v1"
SOFTWARE_VERSION = "editorial-audit-v1"
PROMPT_VERSION = "qwen-editorial-advisory-v1"
POLICY = "MODEL_EDITORIAL_ADVISORY_DETERMINISTIC_HARD_GATE_V1"
ISSUE_FIELDS = (
    "chronology_issues", "naming_ambiguities", "language_issues",
    "overgeneralizations", "structure_issues", "required_actions",
)


SYSTEM_PROMPT = """Sen TunnelBookAI için yerel editoryal danışmansın.
Factual support yeniden değerlendirilmeyecek; cümle-kanıt auditi PASS kabul edilir.
Yalnız metnin kendi içinde kronoloji, adlandırma tutarlılığı, açık yazım/dilbilgisi,
gereksiz tekrar, kataloglaşma, kanıttan geniş görünen sentez ve paragraf akışı sorunlarını
incele. Harici bilgi kullanma; özel ad, tarih, sayı veya teknik iddiayı genel bilgine göre
düzeltme. Her bulguda verilen cümle/paragraf kimliğini belirt. Sorun yoksa dizileri boş ve
decision PASS döndür. Bulgular varsa decision HOLD ve somut required_actions döndür.
Yanıtı yalnız istenen JSON şemasında üret."""


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(value)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _read_json(path: Path, code: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BookEngineError(code, f"cannot read {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise BookEngineError(code, f"{path} root must be an object")
    return payload


def _response_schema() -> dict[str, Any]:
    issue_array = {
        "type": "array", "maxItems": 20,
        "items": {"type": "string", "minLength": 3, "maxLength": 600},
    }
    return {
        "type": "object", "additionalProperties": False,
        "required": ["decision", *ISSUE_FIELDS],
        "properties": {
            "decision": {"type": "string", "enum": ["PASS", "HOLD"]},
            **{field: issue_array for field in ISSUE_FIELDS},
        },
    }


def _validate_model_review(payload: Mapping[str, Any]) -> dict[str, Any]:
    decision = str(payload.get("decision") or "")
    if decision not in {"PASS", "HOLD"}:
        raise ValueError("editorial model decision is invalid")
    output: dict[str, Any] = {"decision": decision}
    for field in ISSUE_FIELDS:
        values = payload.get(field)
        if not isinstance(values, list) or any(not isinstance(value, str) or not value.strip() for value in values):
            raise ValueError(f"editorial model field is invalid: {field}")
        output[field] = [" ".join(value.split()) for value in values]
    has_findings = any(output[field] for field in ISSUE_FIELDS)
    if (decision == "PASS" and has_findings) or (decision == "HOLD" and not output["required_actions"]):
        raise ValueError("editorial model decision and findings disagree")
    return output


def _expected_markdown(title: str, sentence_map: Mapping[str, Any]) -> str:
    by_id = {str(row["sentence_id"]): row for row in sentence_map.get("sentences") or []}
    section_id = str(sentence_map.get("section_id") or "")
    lines = [f"# {section_id} {title}", ""]
    for paragraph in sentence_map.get("paragraphs") or []:
        ids = [str(value) for value in paragraph.get("sentence_ids") or []]
        if not ids or any(value not in by_id for value in ids):
            raise BookEngineError("EDITORIAL_INPUT_INVALID", "paragraph references an unknown sentence")
        lines.extend([" ".join(str(by_id[value]["text"]).strip() for value in ids), ""])
    return "\n".join(lines).rstrip() + "\n"


def deterministic_editorial_gate(
    markdown: str,
    sentence_map: Mapping[str, Any],
    *,
    section_title: str,
) -> dict[str, Any]:
    blockers: list[str] = []
    sentences = list(sentence_map.get("sentences") or [])
    sentence_ids = [str(row.get("sentence_id") or "") for row in sentences]
    paragraph_ids = [str(row.get("paragraph_id") or "") for row in sentence_map.get("paragraphs") or []]
    if not sentences:
        blockers.append("EMPTY_DRAFT")
    if len(sentence_ids) != len(set(sentence_ids)) or not all(sentence_ids):
        blockers.append("SENTENCE_ID_INTEGRITY_FAILED")
    if len(paragraph_ids) != len(set(paragraph_ids)) or not all(paragraph_ids):
        blockers.append("PARAGRAPH_ID_INTEGRITY_FAILED")
    try:
        if markdown != _expected_markdown(section_title, sentence_map):
            blockers.append("DRAFT_SENTENCE_MAP_MISMATCH")
    except BookEngineError:
        blockers.append("DRAFT_SENTENCE_MAP_MISMATCH")
    if "\ufffd" in markdown:
        blockers.append("UNICODE_REPLACEMENT_CHARACTER")
    body = [value.strip() for value in re.split(r"\n\s*\n", markdown) if value.strip()]
    body = [value for value in body if not value.startswith("#")]
    if not body:
        blockers.append("EMPTY_PROSE")
    if any(len(value) >= 80 and value[-1] not in ".!?;:)”’" for value in body):
        blockers.append("POSSIBLE_INCOMPLETE_PARAGRAPH")
    normalized_paragraphs = [re.sub(r"\s+", " ", value).casefold() for value in body if len(value) >= 80]
    if len(normalized_paragraphs) != len(set(normalized_paragraphs)):
        blockers.append("EXACT_DUPLICATE_PARAGRAPH")
    normalized_sentences = [re.sub(r"\s+", " ", str(row.get("text") or "")).strip().casefold() for row in sentences]
    if len(normalized_sentences) != len(set(normalized_sentences)):
        blockers.append("EXACT_DUPLICATE_SENTENCE")
    if re.search(r"\b([\wçğıöşü]+)\s+\1\b", markdown.casefold()):
        blockers.append("REPEATED_CONSECUTIVE_WORD")
    return {
        "decision": "PASS" if not blockers else "HOLD",
        "hard_blockers": blockers,
        "checks": {
            "draft_not_empty": bool(sentences),
            "sentence_ids_unique": len(sentence_ids) == len(set(sentence_ids)) and all(sentence_ids),
            "paragraph_ids_unique": len(paragraph_ids) == len(set(paragraph_ids)) and all(paragraph_ids),
            "draft_sentence_map_exact": "DRAFT_SENTENCE_MAP_MISMATCH" not in blockers,
            "unicode_clean": "UNICODE_REPLACEMENT_CHARACTER" not in blockers,
            "prose_complete": "POSSIBLE_INCOMPLETE_PARAGRAPH" not in blockers,
            "exact_duplicates_absent": not {"EXACT_DUPLICATE_PARAGRAPH", "EXACT_DUPLICATE_SENTENCE"} & set(blockers),
            "consecutive_word_repeat_absent": "REPEATED_CONSECUTIVE_WORD" not in blockers,
        },
    }


def _prompt(sentence_map: Mapping[str, Any]) -> str:
    by_id = {str(row["sentence_id"]): row for row in sentence_map["sentences"]}
    lines: list[str] = []
    for paragraph in sentence_map["paragraphs"]:
        paragraph_id = str(paragraph["paragraph_id"])
        lines.append(f"PARAGRAF [{paragraph_id}]")
        for sentence_id in paragraph["sentence_ids"]:
            lines.append(f"[{sentence_id}] {by_id[str(sentence_id)]['text']}")
        lines.append("")
    return "\n".join(lines)


def _write_report(path: Path, summary: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    model = result["model_editorial_review"]
    lines = [
        f"# Editoryal audit — {summary['section_id']}", "",
        f"- Nihai deterministik karar: **{summary['audit_decision']}**",
        f"- Deterministik blocker: **{len(result['hard_blockers'])}**",
        f"- Qwen danışman kararı: **{model['decision']}**",
        f"- Qwen gerekli eylem: **{len(model['required_actions'])}**", "",
        "Model bulguları danışman niteliğindedir; freeze kararını yeniden üretilebilir",
        "deterministik editoryal kapı verir.", "",
    ]
    for field in ISSUE_FIELDS:
        lines.append(f"## {field}")
        lines.append("")
        values = model[field]
        lines.extend([f"- {value}" for value in values] or ["- Yok."])
        lines.append("")
    _atomic_text(path, "\n".join(lines))


def run_editorial_audit(
    section_id: str,
    project_root: Path | str | None = None,
    *,
    llm_client: LocalChatClient | None = None,
) -> dict[str, Any]:
    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    inputs = load_book_inputs(root)
    drafts = inspect_drafts(root)
    evidence_reviews = inspect_evidence_reviews(root, drafts=drafts)
    coverage_audits = inspect_coverage_audits(root, evidence_reviews=evidence_reviews)
    draft = next((row for row in drafts if row["section_id"] == section_id), None)
    evidence = next((row for row in evidence_reviews if row["section_id"] == section_id), None)
    coverage = next((row for row in coverage_audits if row["section_id"] == section_id), None)
    if not draft or not evidence or evidence.get("audit_decision") != "PASS":
        raise BookEngineError("EVIDENCE_AUDIT_PASS_REQUIRED", f"passing evidence audit required for {section_id}")
    expected_questions = int(inputs.scope_by_id[section_id]["question_count"])
    if not coverage or coverage.get("status") != "COMPLETE" or int(coverage.get("question_count") or 0) != expected_questions:
        raise BookEngineError("QUESTION_COVERAGE_AUDIT_REQUIRED", f"complete coverage audit required for {section_id}")
    draft_path = root / str(draft["draft_path"])
    map_path = root / str(draft["sentence_map_path"])
    markdown = draft_path.read_text(encoding="utf-8")
    sentence_map = _read_json(map_path, "EDITORIAL_INPUT_INVALID")
    deterministic = deterministic_editorial_gate(markdown, sentence_map, section_title=str(draft["section_title"]))
    model, endpoint, model_configuration = _llm_settings(inputs)
    identity = {
        "section_id": section_id,
        "draft_id": draft["draft_id"], "draft_sha256": draft["draft_sha256"],
        "sentence_map_sha256": draft["sentence_map_sha256"],
        "evidence_review_id": evidence["audit_id"], "evidence_review_sha256": evidence["results_sha256"],
        "coverage_audit_id": coverage["audit_id"], "coverage_results_sha256": coverage["results_sha256"],
        "model_id": model, "model_configuration": model_configuration,
        "prompt_version": PROMPT_VERSION, "software_version": SOFTWARE_VERSION, "policy": POLICY,
    }
    audit_id = "EDA_" + canonical_sha256(identity)
    run_root = root / "audit" / "book" / "editorial" / audit_id
    result_path = run_root / "result.json"
    if result_path.is_file():
        result = _read_json(result_path, "EDITORIAL_AUDIT_INVALID")
    else:
        client = llm_client or LocalChatClient(endpoint, timeout=600.0)
        if not client.has_model(model):
            raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", f"exact Qwen model is unavailable: {model}")
        try:
            model_review = _validate_model_review(client.chat_json(
                model, SYSTEM_PROMPT, _prompt(sentence_map), response_schema=_response_schema(),
                max_tokens=4096, reasoning_effort="none",
            ))
        except Exception as exc:
            raise BookEngineError("EDITORIAL_AUDIT_FAILED", f"Qwen editorial audit failed: {type(exc).__name__}: {exc}") from exc
        result = {
            "schema_version": SCHEMA_VERSION, "contract_version": CONTRACT_VERSION,
            "section_id": section_id, "policy": POLICY,
            "deterministic_editorial_gate": deterministic["decision"],
            "hard_blockers": deterministic["hard_blockers"], "deterministic_checks": deterministic["checks"],
            "model_editorial_review": model_review,
            "audit_decision": deterministic["decision"],
        }
        _atomic_json(result_path, result)
    summary = {
        "schema_version": SCHEMA_VERSION, "contract_version": CONTRACT_VERSION,
        "stage": "EDITORIAL_AUDIT", "status": "COMPLETE", "audit_id": audit_id,
        "identity": identity, "updated_at": _now(), "section_id": section_id,
        "policy": POLICY, "audit_decision": result["audit_decision"],
        "model_decision": result["model_editorial_review"]["decision"],
        "hard_blocker_count": len(result["hard_blockers"]),
        "advisory_action_count": len(result["model_editorial_review"]["required_actions"]),
        "result_path": result_path.relative_to(root).as_posix(), "result_sha256": sha256_file(result_path),
    }
    _atomic_json(run_root / "manifest.json", summary)
    _atomic_json(root / "audit" / "book" / "editorial" / f"section_{section_id.replace('.', '_')}.json", summary)
    _write_report(root / "reports" / f"editorial_audit_{section_id.replace('.', '_')}.md", summary, result)
    return summary


def inspect_editorial_audits(
    project_root: Path | str | None = None,
    *,
    coverage_audits: Sequence[Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    coverage = list(coverage_audits) if coverage_audits is not None else inspect_coverage_audits(root)
    by_section = {str(row["section_id"]): row for row in coverage}
    active = root / "audit" / "book" / "editorial"
    output: list[dict[str, Any]] = []
    if not active.is_dir():
        return output
    for path in sorted(active.glob("section_*.json")):
        try:
            summary = _read_json(path, "EDITORIAL_AUDIT_INVALID")
            section_id = str(summary.get("section_id") or "")
            bound = by_section.get(section_id)
            identity = summary.get("identity") or {}
            result_path = (root / str(summary["result_path"])).resolve()
            boundary = (root / "audit" / "book" / "editorial").resolve()
            if (
                not bound or summary.get("status") != "COMPLETE"
                or identity.get("coverage_audit_id") != bound.get("audit_id")
                or identity.get("coverage_results_sha256") != bound.get("results_sha256")
                or boundary not in result_path.parents
                or sha256_file(result_path) != summary.get("result_sha256")
            ):
                continue
            output.append(summary)
        except (BookEngineError, OSError, KeyError, TypeError, ValueError):
            continue
    return output


__all__ = ["deterministic_editorial_gate", "inspect_editorial_audits", "run_editorial_audit"]
