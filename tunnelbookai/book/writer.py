"""Resumable local-Qwen section writer constrained by prepared claim registries."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from tunnelbookai.canonical.hashing import canonical_sha256, sha256_file
from tunnelbookai.ingest.classify.arbiter import LocalChatClient

from .errors import BookEngineError
from .inputs import load_book_inputs
from .preparation import inspect_preparation
from .prewriting import _llm_settings


SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "section-writer-v1"
SOFTWARE_VERSION = "section-writer-v2"
PROMPT_VERSION = "qwen-section-writer-v1"
MAX_CLAIM_EXCERPT = 900


SYSTEM_PROMPT = """Sen kaynak-temelli teknik tünel kitabı yazarı olarak çalışıyorsun.
Yalnızca verilen KAYITLI CANONICAL İDDİA/PASAJLARI kullan. Genel bilgini kullanma, sayı,
örnek, neden-sonuç veya proje bulgusu uydurma. Her cümle en az bir C numarasına ve en az
bir Q numarasına bağlanmalıdır. PARTIAL soruları yalnızca açık sınırlama ve temkinli dille
yanıtla. UNSUPPORTED sorular bu girdide yoktur ve onlar hakkında olgusal cümle yazma.
Başlık üretme; kısa, teknik, tekrar etmeyen Türkçe paragraflar üret. C/Q numaralarını cümle
metnine yazma. Sonucu yalnızca istenen JSON şemasında döndür."""


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(text)
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


def _response_schema(question_count: int, claim_count: int) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["paragraphs"],
        "properties": {
            "paragraphs": {
                "type": "array",
                "minItems": 1,
                "maxItems": max(2, question_count * 2),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["sentences"],
                    "properties": {
                        "sentences": {
                            "type": "array",
                            "minItems": 1,
                            "maxItems": 8,
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": ["t", "c", "q"],
                                "properties": {
                                    "t": {"type": "string", "minLength": 10, "maxLength": 900},
                                    "c": {
                                        "type": "array", "minItems": 1, "maxItems": 4,
                                        "items": {"type": "integer", "minimum": 1, "maximum": claim_count},
                                    },
                                    "q": {
                                        "type": "array", "minItems": 1, "maxItems": question_count,
                                        "items": {"type": "integer", "minimum": 1, "maximum": question_count},
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }


def _prompt(
    section_id: str,
    section_title: str,
    questions: Sequence[Mapping[str, Any]],
    claims: Sequence[Mapping[str, Any]],
) -> str:
    lines = [f"BÖLÜM {section_id}: {section_title}", "", "SORULAR:"]
    for number, question in enumerate(questions, 1):
        lines.append(
            f"Q{number} [{question['evidence_status']} / {question['drafting_permission']}]: "
            f"{question['question']}"
        )
    lines.extend(["", "KAYITLI CANONICAL İDDİA/PASAJLAR:"])
    for number, claim in enumerate(claims, 1):
        passage = " ".join(str(claim["claim_text"]).split())[:MAX_CLAIM_EXCERPT]
        lines.append(
            f"C{number} [{claim['claim_id']}] | {claim['document_id']} | {claim['locator']}\n{passage}"
        )
    return "\n".join(lines)


def _validate_batch(
    payload: Mapping[str, Any],
    questions: Sequence[Mapping[str, Any]],
    claims: Sequence[Mapping[str, Any]],
) -> list[list[dict[str, Any]]]:
    raw_paragraphs = payload.get("paragraphs")
    if not isinstance(raw_paragraphs, list) or not raw_paragraphs:
        raise ValueError("Qwen returned no paragraphs")
    paragraphs: list[list[dict[str, Any]]] = []
    covered: set[int] = set()
    for raw_paragraph in raw_paragraphs:
        if not isinstance(raw_paragraph, Mapping):
            raise ValueError("Qwen paragraph is not an object")
        raw_sentences = raw_paragraph.get("sentences")
        if not isinstance(raw_sentences, list) or not raw_sentences:
            raise ValueError("Qwen paragraph has no sentences")
        sentences: list[dict[str, Any]] = []
        for raw in raw_sentences:
            if not isinstance(raw, Mapping):
                raise ValueError("Qwen sentence is not an object")
            text = " ".join(str(raw.get("t") or "").split())
            if len(text) < 10:
                raise ValueError("Qwen sentence text is empty or too short")
            try:
                claim_numbers = [int(value) for value in raw.get("c") or []]
                question_numbers = [int(value) for value in raw.get("q") or []]
            except (TypeError, ValueError) as exc:
                raise ValueError("Qwen returned non-numeric references") from exc
            if (
                not claim_numbers
                or len(claim_numbers) != len(set(claim_numbers))
                or any(value < 1 or value > len(claims) for value in claim_numbers)
            ):
                raise ValueError("Qwen returned an invalid claim reference")
            if (
                not question_numbers
                or len(question_numbers) != len(set(question_numbers))
                or any(value < 1 or value > len(questions) for value in question_numbers)
            ):
                raise ValueError("Qwen returned an invalid question reference")
            covered.update(question_numbers)
            sentences.append({
                "text": text,
                "claim_ids": [str(claims[value - 1]["claim_id"]) for value in claim_numbers],
                "question_ids": [str(questions[value - 1]["question_id"]) for value in question_numbers],
            })
        paragraphs.append(sentences)
    expected = set(range(1, len(questions) + 1))
    if covered != expected:
        missing = sorted(expected - covered)
        raise ValueError(f"Qwen did not cover every eligible question: {missing}")
    return paragraphs


def _batch_questions(
    questions: Sequence[Mapping[str, Any]],
    *,
    batch_size: int,
) -> list[list[Mapping[str, Any]]]:
    return [list(questions[start:start + batch_size]) for start in range(0, len(questions), batch_size)]


def _claims_for_questions(
    questions: Sequence[Mapping[str, Any]],
    claim_by_id: Mapping[str, Mapping[str, Any]],
) -> list[Mapping[str, Any]]:
    ids = list(dict.fromkeys(
        str(claim_id)
        for question in questions
        for claim_id in question.get("allowed_claim_ids") or []
    ))
    missing = [claim_id for claim_id in ids if claim_id not in claim_by_id]
    if missing:
        raise BookEngineError("SECTION_PREPARATION_INVALID", "packet references unknown claims", details=missing)
    return [claim_by_id[claim_id] for claim_id in ids]


def _valid_checkpoint(
    path: Path,
    *,
    question_ids: Sequence[str],
    claim_ids: Sequence[str],
) -> list[list[dict[str, Any]]] | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("question_ids") != list(question_ids) or payload.get("claim_ids") != list(claim_ids):
            return None
        paragraphs = payload.get("paragraphs")
        if not isinstance(paragraphs, list) or not paragraphs:
            return None
        known_questions = set(question_ids)
        known_claims = set(claim_ids)
        for paragraph in paragraphs:
            if not isinstance(paragraph, list) or not paragraph:
                return None
            for sentence in paragraph:
                if (
                    not isinstance(sentence, dict)
                    or not str(sentence.get("text") or "").strip()
                    or not set(sentence.get("claim_ids") or []) <= known_claims
                    or not set(sentence.get("question_ids") or []) <= known_questions
                ):
                    return None
        if {qid for paragraph in paragraphs for sentence in paragraph for qid in sentence["question_ids"]} != known_questions:
            return None
        return paragraphs
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return None


def _write_markdown(section_id: str, section_title: str, paragraphs: Iterable[Sequence[Mapping[str, Any]]]) -> str:
    lines = [f"# {section_id} {section_title}", ""]
    for paragraph in paragraphs:
        lines.append(" ".join(str(sentence["text"]).strip() for sentence in paragraph))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run_section_writer(
    section_id: str,
    project_root: Path | str | None = None,
    *,
    batch_size: int = 8,
    progress: Any = None,
    llm_client: LocalChatClient | None = None,
) -> dict[str, Any]:
    """Write one evidence-constrained draft, with resumable Qwen batch checkpoints."""

    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    from .freeze import is_section_frozen
    if is_section_frozen(root, section_id):
        raise BookEngineError("SECTION_FROZEN", f"section {section_id} is immutable while frozen")
    if batch_size < 1 or batch_size > 12:
        raise BookEngineError("INVALID_BATCH_SIZE", "writer batch size must be between 1 and 12")
    inputs = load_book_inputs(root)
    if section_id not in inputs.questions_by_section:
        raise BookEngineError("UNKNOWN_SECTION", f"section is not a question-bank section: {section_id}")
    preparation = inspect_preparation(root, inputs=inputs)
    if not preparation or preparation.get("status") != "COMPLETE":
        raise BookEngineError("SECTION_PREPARATION_INCOMPLETE", "all section evidence packets must be valid")
    entry = next((row for row in preparation["sections"] if row["section_id"] == section_id), None)
    if not entry:
        raise BookEngineError("SECTION_PREPARATION_INVALID", f"prepared section is missing: {section_id}")
    packet_path = root / entry["packet_path"]
    registry_path = root / entry["claim_registry_path"]
    if sha256_file(packet_path) != entry["packet_sha256"] or sha256_file(registry_path) != entry["claim_registry_sha256"]:
        raise BookEngineError("SECTION_PREPARATION_INVALID", "prepared artifact hash mismatch")
    packet = _read_json(packet_path, "SECTION_PREPARATION_INVALID")
    registry = _read_json(registry_path, "SECTION_PREPARATION_INVALID")
    if packet.get("claim_registry_id") != registry.get("registry_id"):
        raise BookEngineError("SECTION_PREPARATION_INVALID", "packet/claim registry identity mismatch")
    eligible_questions = [
        row for row in packet["questions"] if row["evidence_status"] in {"SUPPORTED", "PARTIAL"}
    ]
    if not eligible_questions or not registry.get("claims"):
        return {
            "stage": "SECTION_WRITER",
            "status": "BLOCKED",
            "reason_code": "EVIDENCE_GAP",
            "section_id": section_id,
            "detail": "No supported or partial canonical claims are available for this section.",
        }
    model, endpoint, model_configuration = _llm_settings(inputs)
    identity = {
        "section_id": section_id,
        "packet_id": packet["packet_id"],
        "packet_sha256": entry["packet_sha256"],
        "claim_registry_id": registry["registry_id"],
        "claim_registry_sha256": entry["claim_registry_sha256"],
        "model_id": model,
        "model_configuration": model_configuration,
        "prompt_version": PROMPT_VERSION,
        "software_version": SOFTWARE_VERSION,
        "batch_size": batch_size,
        "max_claim_excerpt": MAX_CLAIM_EXCERPT,
    }
    draft_id = "DRF_" + canonical_sha256(identity)
    draft_root = root / "book" / "production" / "drafts" / draft_id
    checkpoint_root = draft_root / "batches"
    client = llm_client or LocalChatClient(endpoint, timeout=600.0)
    batches = _batch_questions(eligible_questions, batch_size=batch_size)
    claim_by_id = {str(row["claim_id"]): row for row in registry["claims"]}
    completed: list[list[list[dict[str, Any]]]] = []
    for batch_number, questions in enumerate(batches, 1):
        claims = _claims_for_questions(questions, claim_by_id)
        question_ids = [str(row["question_id"]) for row in questions]
        claim_ids = [str(row["claim_id"]) for row in claims]
        checkpoint_path = checkpoint_root / f"batch_{batch_number:03d}.json"
        paragraphs = _valid_checkpoint(
            checkpoint_path, question_ids=question_ids, claim_ids=claim_ids
        )
        if paragraphs is None:
            if not client.has_model(model):
                raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", f"exact Qwen model is unavailable: {model}")
            try:
                response = client.chat_json(
                    model,
                    SYSTEM_PROMPT,
                    _prompt(section_id, str(packet["section_title"]), questions, claims),
                    response_schema=_response_schema(len(questions), len(claims)),
                    max_tokens=min(8192, max(2048, len(questions) * 650)),
                    reasoning_effort="none",
                )
                paragraphs = _validate_batch(response, questions, claims)
            except Exception as exc:
                raise BookEngineError(
                    "SECTION_WRITER_FAILED",
                    f"Qwen writer failed at {section_id} batch {batch_number}: {type(exc).__name__}: {exc}",
                ) from exc
            _atomic_json(checkpoint_path, {
                "batch_number": batch_number,
                "question_ids": question_ids,
                "claim_ids": claim_ids,
                "paragraphs": paragraphs,
            })
        completed.append(paragraphs)
        if progress:
            progress({
                "draft_id": draft_id,
                "section_id": section_id,
                "batch": batch_number,
                "batch_count": len(batches),
                "questions_processed": sum(len(value) for value in batches[:batch_number]),
                "eligible_question_count": len(eligible_questions),
            })
    flat_paragraphs = [paragraph for batch in completed for paragraph in batch]
    sentence_rows: list[dict[str, Any]] = []
    paragraph_rows: list[dict[str, Any]] = []
    sentence_number = 0
    for paragraph_number, paragraph in enumerate(flat_paragraphs, 1):
        paragraph_id = f"{section_id}-P{paragraph_number:03d}"
        sentence_ids: list[str] = []
        for sentence in paragraph:
            sentence_number += 1
            sentence_id = f"{section_id}-S{sentence_number:03d}"
            sentence_ids.append(sentence_id)
            claims = [claim_by_id[value] for value in sentence["claim_ids"]]
            sentence_rows.append({
                "sentence_id": sentence_id,
                "paragraph_id": paragraph_id,
                "text": sentence["text"],
                "claim_ids": sentence["claim_ids"],
                "question_ids": sentence["question_ids"],
                "document_ids": list(dict.fromkeys(str(row["document_id"]) for row in claims)),
                "source_locators": list(dict.fromkeys(str(row["locator"]) for row in claims)),
                "audit_status": "PENDING_POSTWRITING_EVIDENCE_AUDIT",
            })
        paragraph_rows.append({"paragraph_id": paragraph_id, "sentence_ids": sentence_ids})
    markdown = _write_markdown(section_id, str(packet["section_title"]), flat_paragraphs)
    draft_path = draft_root / "section.md"
    sentence_map_path = draft_root / "sentence_map.json"
    _atomic_text(draft_path, markdown)
    sentence_map = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "draft_id": draft_id,
        "section_id": section_id,
        "paragraphs": paragraph_rows,
        "sentences": sentence_rows,
    }
    _atomic_json(sentence_map_path, sentence_map)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "stage": "SECTION_WRITER",
        "status": "DRAFTED_UNAUDITED",
        "reason_code": "POSTWRITING_AUDITS_REQUIRED",
        "draft_id": draft_id,
        "identity": identity,
        "section_id": section_id,
        "section_title": packet["section_title"],
        "readiness": packet["readiness"],
        "eligible_question_count": len(eligible_questions),
        "unsupported_question_count": packet["evidence_counts"]["UNSUPPORTED"],
        "covered_question_count": len({qid for row in sentence_rows for qid in row["question_ids"]}),
        "paragraph_count": len(paragraph_rows),
        "sentence_count": len(sentence_rows),
        "claim_count_used": len({cid for row in sentence_rows for cid in row["claim_ids"]}),
        "draft_path": draft_path.relative_to(root).as_posix(),
        "draft_sha256": sha256_file(draft_path),
        "sentence_map_path": sentence_map_path.relative_to(root).as_posix(),
        "sentence_map_sha256": sha256_file(sentence_map_path),
    }
    _atomic_json(draft_root / "manifest.json", manifest)
    active = root / "book" / "production" / "drafts" / "active" / f"section_{section_id.replace('.', '_')}.json"
    _atomic_json(active, manifest)
    return manifest


def inspect_drafts(
    project_root: Path | str | None = None,
    *,
    preparation: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return only active drafts still bound to the current prepared artifacts."""

    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    prepared = preparation or inspect_preparation(root)
    if not prepared:
        return []
    entries = {str(row["section_id"]): row for row in prepared.get("sections") or []}
    active_root = root / "book" / "production" / "drafts" / "active"
    if not active_root.is_dir():
        return []
    valid: list[dict[str, Any]] = []
    for path in sorted(active_root.glob("section_*.json")):
        try:
            manifest = _read_json(path, "SECTION_DRAFT_INVALID")
            section_id = str(manifest.get("section_id") or "")
            entry = entries.get(section_id)
            identity = manifest.get("identity") or {}
            if (
                not entry
                or manifest.get("status") != "DRAFTED_UNAUDITED"
                or identity.get("packet_id") != entry.get("packet_id")
                or identity.get("claim_registry_id") != entry.get("claim_registry_id")
            ):
                continue
            draft_path = (root / str(manifest["draft_path"])).resolve()
            map_path = (root / str(manifest["sentence_map_path"])).resolve()
            boundary = (root / "book" / "production" / "drafts").resolve()
            if boundary not in draft_path.parents or boundary not in map_path.parents:
                continue
            if (
                sha256_file(draft_path) != manifest.get("draft_sha256")
                or sha256_file(map_path) != manifest.get("sentence_map_sha256")
            ):
                continue
            valid.append(manifest)
        except (BookEngineError, OSError, KeyError, TypeError, ValueError):
            continue
    return valid


__all__ = ["inspect_drafts", "run_section_writer"]
