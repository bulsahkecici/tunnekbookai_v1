"""Resumable post-writing question coverage audit for one drafted section."""

from __future__ import annotations

import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from tunnelbookai.canonical.hashing import canonical_sha256, sha256_file
from tunnelbookai.ingest.classify.arbiter import LocalChatClient

from .coverage import section_target_summary
from .errors import BookEngineError
from .evidence_review import inspect_evidence_reviews
from .inputs import load_book_inputs
from .models import QuestionCoverageResult, validate_result_references
from .preparation import inspect_preparation
from .prewriting import _llm_settings
from .writer import inspect_drafts


SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "question-coverage-audit-v1"
SOFTWARE_VERSION = "question-coverage-audit-v3"
PROMPT_VERSION = "qwen-question-coverage-v1"


SYSTEM_PROMPT = """Sen teknik kitap soru kapsam hakemisin.
Her soruyu yalnızca verilen TASLAK CÜMLELERİ ve onların bağımsız kanıt-audit durumuyla değerlendir.
ANSWERED: sorunun bütün maddi kapsamı doğrudan yanıtlanıyor; yalnızca SUPPORTED cümleleri seç.
PARTIAL: sorunun bir bölümü yanıtlanıyor veya yalnızca PARTIAL cümle bulunuyor.
NOT_ANSWERED: doğrudan yanıt yok. Genel bilgini kullanma ve cevap uydurma.
Kısa kodlar s=A/P/N; r=D(direct), C(composite), P(partial), N(no answer); c 0-100 güven.
e her soru altındaki S sıra numaralarıdır. Sonucu yalnızca istenen JSON şemasında döndür."""


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


def _atomic_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _read_json(path: Path, code: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BookEngineError(code, f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BookEngineError(code, f"{path} root must be an object")
    return value


def _read_jsonl(path: Path, code: str) -> list[dict[str, Any]]:
    try:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BookEngineError(code, f"cannot read {path}: {exc}") from exc


def _schema(question_count: int, max_sentences: int) -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False, "required": ["results"],
        "properties": {"results": {
            "type": "array", "minItems": question_count, "maxItems": question_count,
            "items": {
                "type": "object", "additionalProperties": False,
                "required": ["i", "s", "e", "r", "c"],
                "properties": {
                    "i": {"type": "integer", "minimum": 1, "maximum": question_count},
                    "s": {"type": "string", "enum": ["A", "P", "N"]},
                    "e": {"type": "array", "maxItems": 10, "items": {"type": "integer", "minimum": 1, "maximum": max_sentences}},
                    "r": {"type": "string", "enum": ["D", "C", "P", "N"]},
                    "c": {"type": "integer", "minimum": 0, "maximum": 100},
                },
            },
        }},
    }


def _prompt(questions: Sequence[Mapping[str, Any]], candidates: Sequence[Sequence[Mapping[str, Any]]]) -> str:
    lines: list[str] = []
    for index, (question, spans) in enumerate(zip(questions, candidates), 1):
        lines.append(f"SORU {index} [{question['question_id']}]: {question['question']}")
        for rank, span in enumerate(spans, 1):
            lines.append(
                f"S{rank} [{span['status']}] [{span['sentence_id']}]: {span['sentence']}"
            )
        if not spans:
            lines.append("TASLAK CÜMLESİ: YOK")
        lines.append("")
    return "\n".join(lines)


def _validate_results(
    payload: Mapping[str, Any],
    questions: Sequence[Mapping[str, Any]],
    candidates: Sequence[Sequence[Mapping[str, Any]]],
    *,
    draft_path: str,
) -> list[dict[str, Any]]:
    raw = payload.get("results")
    if not isinstance(raw, list) or len(raw) != len(questions):
        raise ValueError("Qwen coverage result count differs from the question batch")
    by_index: dict[int, Mapping[str, Any]] = {}
    for row in raw:
        if not isinstance(row, Mapping):
            raise ValueError("Qwen coverage result is not an object")
        index = int(row.get("i"))
        if index in by_index:
            raise ValueError("Qwen returned a duplicate question index")
        by_index[index] = row
    status_map = {"A": "ANSWERED", "P": "PARTIAL", "N": "NOT_ANSWERED"}
    reason_map = {"D": "DIRECT_ANSWER", "C": "COMPOSITE_ANSWER", "P": "PARTIAL_ANSWER", "N": "NO_ANSWER_SPAN"}
    output: list[dict[str, Any]] = []
    for index, (question, spans) in enumerate(zip(questions, candidates), 1):
        row = by_index.get(index)
        if row is None:
            raise ValueError(f"Qwen omitted question {index}")
        status = status_map.get(str(row.get("s") or ""), "")
        reason = reason_map.get(str(row.get("r") or ""), "")
        refs = [int(value) for value in row.get("e") or []]
        if not status or not reason or len(refs) != len(set(refs)) or any(value < 1 or value > len(spans) for value in refs):
            raise ValueError("Qwen returned an invalid coverage state/reference")
        selected = [spans[value - 1] for value in refs]
        if status == "ANSWERED" and not selected:
            raise ValueError("ANSWERED requires supported answer spans")
        if status == "ANSWERED" and any(value["status"] != "SUPPORTED" for value in selected):
            # A model may over-credit a span already classified PARTIAL by the
            # independent sentence-evidence audit.  Coverage can only move in the
            # conservative direction here; never promote a weak span to ANSWERED.
            status = "PARTIAL"
            reason = "PARTIAL_ANSWER"
        if status == "PARTIAL" and not selected:
            status = "NOT_ANSWERED"
            reason = "NO_ANSWER_SPAN"
        if status == "NOT_ANSWERED":
            selected = []
        confidence = float(row.get("c")) / 100.0
        claim_ids = list(dict.fromkeys(cid for span in selected for cid in span["supporting_claim_ids"]))
        document_ids = list(dict.fromkeys(did for span in selected for did in span["supporting_document_ids"]))
        locators = list(dict.fromkeys(loc for span in selected for loc in span["source_locators"]))
        sentence_ids = [str(span["sentence_id"]) for span in selected]
        result = {
            "question_id": str(question["question_id"]),
            "section_id": str(question["section_id"]),
            "question": str(question["question"]),
            "status": status,
            "answer_spans": [{"section_file": draft_path, "paragraph_or_sentence_ids": sentence_ids}] if sentence_ids else [],
            "supporting_claim_ids": claim_ids,
            "supporting_document_ids": document_ids,
            "source_locators": locators,
            "confidence": round(confidence, 4),
            "reason": reason,
        }
        QuestionCoverageResult.from_mapping(result)
        output.append(result)
    return output


def _audit_with_split(client, model, questions, candidates, draft_path):
    active = [(q, c) for q, c in zip(questions, candidates) if c]
    audited: list[dict[str, Any]] = []
    if active:
        qs = [value[0] for value in active]
        cs = [value[1] for value in active]
        try:
            response = client.chat_json(
                model, SYSTEM_PROMPT, _prompt(qs, cs),
                response_schema=_schema(len(qs), max(len(value) for value in cs)),
                max_tokens=min(8192, max(2048, len(qs) * 350)), reasoning_effort="none",
            )
            audited = _validate_results(response, qs, cs, draft_path=draft_path)
        except Exception:
            if len(active) == 1:
                raise
            middle = len(active) // 2
            audited = [
                *_audit_with_split(client, model, qs[:middle], cs[:middle], draft_path),
                *_audit_with_split(client, model, qs[middle:], cs[middle:], draft_path),
            ]
    by_id = {row["question_id"]: row for row in audited}
    output: list[dict[str, Any]] = []
    for question, spans in zip(questions, candidates):
        question_id = str(question["question_id"])
        if spans:
            output.append(by_id[question_id])
        else:
            output.append({
                "question_id": question_id, "section_id": str(question["section_id"]),
                "question": str(question["question"]), "status": "NOT_ANSWERED",
                "answer_spans": [], "supporting_claim_ids": [], "supporting_document_ids": [],
                "source_locators": [], "confidence": 1.0, "reason": "NO_ANSWER_SPAN",
            })
    return output


def _write_report(path: Path, summary: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> None:
    lines = [
        f"# Soru kapsam auditi — {summary['section_id']}", "",
        f"- ANSWERED: **{summary['answered']} / {summary['question_count']}**",
        f"- PARTIAL: **{summary['partial']}**", f"- NOT_ANSWERED: **{summary['not_answered']}**",
        f"- Kapsam: **{summary['coverage']:.0%}**", f"- Tercih hedefi ({summary.get('preferred_target')}/{summary['question_count']}): **{'PASS' if summary['target_met'] else 'FAIL'}**",
        "", "| Soru | Durum | Güven | Neden |", "|---|---|---:|---|",
    ]
    for row in rows:
        lines.append(f"| {row['question_id']} | {row['status']} | {float(row['confidence']):.0%} | {row['reason']} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def run_coverage_audit(section_id: str, project_root: Path | str | None = None, *, batch_size: int = 10, progress: Any = None, llm_client: LocalChatClient | None = None) -> dict[str, Any]:
    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    if batch_size < 1 or batch_size > 20:
        raise BookEngineError("INVALID_BATCH_SIZE", "coverage-audit batch size must be between 1 and 20")
    inputs = load_book_inputs(root)
    preparation = inspect_preparation(root, inputs=inputs)
    drafts = inspect_drafts(root, preparation=preparation)
    reviews = inspect_evidence_reviews(root, drafts=drafts)
    draft = next((row for row in drafts if row["section_id"] == section_id), None)
    review = next((row for row in reviews if row["section_id"] == section_id), None)
    if not draft or not review:
        raise BookEngineError("POSTWRITING_EVIDENCE_REVIEW_REQUIRED", f"complete evidence review required for {section_id}")
    prep_entry = next(row for row in preparation["sections"] if row["section_id"] == section_id)
    packet = _read_json(root / prep_entry["packet_path"], "SECTION_PREPARATION_INVALID")
    registry = _read_json(root / prep_entry["claim_registry_path"], "SECTION_PREPARATION_INVALID")
    sentence_map = _read_json(root / draft["sentence_map_path"], "SECTION_DRAFT_INVALID")
    review_rows = _read_jsonl(root / review["results_path"], "POSTWRITING_AUDIT_INVALID")
    review_by_id = {str(row["sentence_id"]): row for row in review_rows}
    candidates: list[list[dict[str, Any]]] = []
    for question in packet["questions"]:
        spans = []
        for sentence in sentence_map["sentences"]:
            if question["question_id"] not in sentence["question_ids"]:
                continue
            audited = review_by_id[str(sentence["sentence_id"])]
            if audited["status"] not in {"SUPPORTED", "PARTIAL"}:
                continue
            spans.append(audited)
        candidates.append(spans)
    model, endpoint, model_configuration = _llm_settings(inputs)
    identity = {
        "section_id": section_id, "draft_id": draft["draft_id"],
        "evidence_review_id": review["audit_id"], "evidence_review_sha256": review["results_sha256"],
        "question_bank_sha256": inputs.identities["question_bank_sha256"],
        "model_id": model, "model_configuration": model_configuration,
        "prompt_version": PROMPT_VERSION, "software_version": SOFTWARE_VERSION, "batch_size": batch_size,
    }
    audit_id = "QCA_" + canonical_sha256(identity)
    run_root = root / "audit" / "book" / "coverage" / audit_id
    client = llm_client or LocalChatClient(endpoint, timeout=600.0)
    questions = list(inputs.questions_by_section[section_id])
    results: list[dict[str, Any]] = []
    for batch_number, start in enumerate(range(0, len(questions), batch_size), 1):
        qs = questions[start:start + batch_size]
        cs = candidates[start:start + batch_size]
        checkpoint = run_root / "batches" / f"batch_{batch_number:03d}.json"
        rows = None
        if checkpoint.is_file():
            candidate = _read_json(checkpoint, "QUESTION_COVERAGE_AUDIT_INVALID")
            if candidate.get("question_ids") == [row["question_id"] for row in qs]:
                rows = candidate.get("results")
        if not isinstance(rows, list):
            if any(cs) and not client.has_model(model):
                raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", f"exact Qwen model is unavailable: {model}")
            try:
                rows = _audit_with_split(client, model, qs, cs, str(draft["draft_path"]))
            except Exception as exc:
                raise BookEngineError("QUESTION_COVERAGE_AUDIT_FAILED", f"Qwen coverage failed at batch {batch_number}: {type(exc).__name__}: {exc}") from exc
            _atomic_json(checkpoint, {"batch_number": batch_number, "question_ids": [row["question_id"] for row in qs], "results": rows})
        results.extend(rows)
        if progress:
            progress({"audit_id": audit_id, "section_id": section_id, "batch": batch_number, "batch_count": (len(questions)+batch_size-1)//batch_size, "questions_audited": len(results), "question_count": len(questions)})
    claim_ids = {str(row["claim_id"]) for row in registry["claims"]}
    document_ids = {str(row["document_id"]) for row in registry["claims"]}
    locators = {str(row["locator"]) for row in registry["claims"]}
    span_ids = {str(row["sentence_id"]) for row in sentence_map["sentences"]}
    for raw in results:
        result = QuestionCoverageResult.from_mapping(raw)
        validate_result_references(result, expected_section_id=section_id, known_claim_ids=claim_ids, known_document_ids=document_ids, known_locators=locators, known_span_ids=span_ids, allowed_section_files={str(draft["draft_path"])})
    target = section_target_summary([row["status"] for row in results], inputs.contract, expected=len(questions))
    results_path = run_root / "results.jsonl"
    _atomic_jsonl(results_path, results)
    summary = {
        "schema_version": SCHEMA_VERSION, "contract_version": CONTRACT_VERSION,
        "stage": "QUESTION_COVERAGE_AUDIT", "status": "COMPLETE", "audit_id": audit_id,
        "identity": identity, "updated_at": _now(), "section_id": section_id,
        "question_count": len(results), **target,
        "audit_decision": "PASS" if target["target_met"] else "COVERAGE_REMEDIATION_REQUIRED",
        "results_path": results_path.relative_to(root).as_posix(), "results_sha256": sha256_file(results_path),
    }
    _atomic_json(run_root / "manifest.json", summary)
    _atomic_json(root / "audit" / "book" / "coverage" / f"section_{section_id.replace('.', '_')}.json", summary)
    _write_report(root / "reports" / f"question_coverage_{section_id.replace('.', '_')}.md", summary, results)
    return summary


def inspect_coverage_audits(
    project_root: Path | str | None = None,
    *,
    evidence_reviews: Sequence[Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Return complete coverage audits bound to current evidence-review results."""

    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    reviews = list(evidence_reviews) if evidence_reviews is not None else inspect_evidence_reviews(root)
    by_section = {str(row["section_id"]): row for row in reviews}
    active_root = root / "audit" / "book" / "coverage"
    if not active_root.is_dir():
        return []
    output: list[dict[str, Any]] = []
    for path in sorted(active_root.glob("section_*.json")):
        try:
            summary = _read_json(path, "QUESTION_COVERAGE_AUDIT_INVALID")
            section_id = str(summary.get("section_id") or "")
            review = by_section.get(section_id)
            identity = summary.get("identity") or {}
            if (
                not review
                or summary.get("status") != "COMPLETE"
                or identity.get("evidence_review_id") != review.get("audit_id")
                or identity.get("evidence_review_sha256") != review.get("results_sha256")
            ):
                continue
            results_path = (root / str(summary["results_path"])).resolve()
            boundary = (root / "audit" / "book" / "coverage").resolve()
            if boundary not in results_path.parents or sha256_file(results_path) != summary.get("results_sha256"):
                continue
            if sum(1 for line in results_path.read_text(encoding="utf-8").splitlines() if line.strip()) != int(summary["question_count"]):
                continue
            output.append(summary)
        except (BookEngineError, OSError, KeyError, TypeError, ValueError):
            continue
    return output


__all__ = ["inspect_coverage_audits", "run_coverage_audit"]
