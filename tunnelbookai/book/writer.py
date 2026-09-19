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
SOFTWARE_VERSION = "section-writer-v3-outline-first"
PROMPT_VERSION = "qwen-section-writer-v2-themes"
MAX_CLAIM_EXCERPT = 900
MAX_PLAN_EXCERPT = 420
MIN_THEMES = 2
MAX_THEMES = 8
MAX_PARAGRAPHS_PER_THEME = 4


PLAN_SYSTEM_PROMPT = """Sen kaynak-temelli teknik tünel kitabının bölüm editörüsün.
Görevin, verilen bölüm için yalnızca KAYITLI CANONICAL PASAJLARA dayanan bir yazım planı
kurmaktır. Bölümü 2-8 tematik alt akışa böl; her tema için kısa bir başlık, o temada
kullanılacak pasaj numaraları (C) ve o temanın ele aldığı soru numaraları (Q) ver.
İlk tema bölümün tanım/giriş temasıdır. Bölüm başlığıyla ilgisi olmayan, içindekiler
tablosu, şekil listesi veya konu dışı pasajları hiçbir temaya koyma. Sırayı kitap
mantığına göre kur: tanım -> ilkeler -> uygulama -> Türkiye/örnek -> maliyet/işletme.
Sonucu yalnızca istenen JSON şemasında döndür."""

SYSTEM_PROMPT = """Sen kaynak-temelli teknik tünel kitabı yazarı olarak çalışıyorsun.
Bölümün yalnızca verilen TEMASINI yazıyorsun; sadece o temaya ayrılmış KAYITLI CANONICAL
PASAJLARI kullan. Genel bilgini kullanma; sayı, örnek, neden-sonuç veya proje bulgusu
uydurma. Akıcı, birbirine bağlı, tekrar etmeyen Türkçe paragraflar yaz; bölüm başlığını
her cümlede tekrar etme ve "X ile Y arasında bağ vardır" gibi yapay kalıplar kurma.
Her cümle en az bir C numarasına bağlanmalıdır; bir cümle bir soruyu doğrudan
yanıtlıyorsa Q numarasını da ver, yanıtlamıyorsa q listesini boş bırak. PARTIAL soruları
yalnızca açık sınırlama ve temkinli dille ele al. Başlık veya madde imi üretme; C/Q
numaralarını cümle metnine yazma. Sonucu yalnızca istenen JSON şemasında döndür."""


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


def _plan_schema(question_count: int, claim_count: int) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["themes"],
        "properties": {
            "themes": {
                "type": "array",
                "minItems": MIN_THEMES,
                "maxItems": MAX_THEMES,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["title", "c", "q"],
                    "properties": {
                        "title": {"type": "string", "minLength": 3, "maxLength": 120},
                        "c": {
                            "type": "array", "minItems": 1, "maxItems": claim_count,
                            "items": {"type": "integer", "minimum": 1, "maximum": claim_count},
                        },
                        "q": {
                            "type": "array", "maxItems": question_count,
                            "items": {"type": "integer", "minimum": 1, "maximum": question_count},
                        },
                    },
                },
            },
        },
    }


def _response_schema(question_count: int, claim_count: int) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["paragraphs"],
        "properties": {
            "paragraphs": {
                "type": "array",
                "minItems": 1,
                "maxItems": MAX_PARAGRAPHS_PER_THEME,
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
                                        "type": "array", "maxItems": max(1, question_count),
                                        "items": {"type": "integer", "minimum": 1, "maximum": max(1, question_count)},
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }


def _plan_prompt(
    section_id: str,
    section_title: str,
    questions: Sequence[Mapping[str, Any]],
    claims: Sequence[Mapping[str, Any]],
) -> str:
    lines = [f"BÖLÜM {section_id}: {section_title}", "", "BÖLÜMÜN YANITLAMASI BEKLENEN SORULAR:"]
    for number, question in enumerate(questions, 1):
        lines.append(f"Q{number} [{question['evidence_status']}]: {question['question']}")
    lines.extend(["", "KAYITLI CANONICAL PASAJLAR (özet):"])
    for number, claim in enumerate(claims, 1):
        passage = " ".join(str(claim["claim_text"]).split())[:MAX_PLAN_EXCERPT]
        lines.append(f"C{number} | {claim['document_id']} | {claim.get('chunk_type') or ''}\n{passage}")
    return "\n".join(lines)


def _prompt(
    section_id: str,
    section_title: str,
    theme: Mapping[str, Any],
    questions: Sequence[Mapping[str, Any]],
    claims: Sequence[Mapping[str, Any]],
    *,
    previous_titles: Sequence[str] = (),
) -> str:
    lines = [f"BÖLÜM {section_id}: {section_title}", f"TEMA {theme['number']}/{theme['count']}: {theme['title']}"]
    if previous_titles:
        lines.append("ÖNCEKİ TEMALARDA ELE ALINANLAR (tekrar etme): " + "; ".join(previous_titles))
    lines.extend(["", "BU TEMANIN ELE ALDIĞI SORULAR:"])
    if questions:
        for number, question in enumerate(questions, 1):
            lines.append(
                f"Q{number} [{question['evidence_status']} / {question['drafting_permission']}]: "
                f"{question['question']}"
            )
    else:
        lines.append("(bu tema için doğrudan soru atanmadı; q listelerini boş bırak)")
    lines.extend(["", "BU TEMAYA AYRILAN KAYITLI CANONICAL PASAJLAR:"])
    for number, claim in enumerate(claims, 1):
        passage = " ".join(str(claim["claim_text"]).split())[:MAX_CLAIM_EXCERPT]
        lines.append(
            f"C{number} [{claim['claim_id']}] | {claim['document_id']} | {claim['locator']}\n{passage}"
        )
    return "\n".join(lines)


def _validate_plan(
    payload: Mapping[str, Any],
    questions: Sequence[Mapping[str, Any]],
    claims: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    raw = payload.get("themes")
    if not isinstance(raw, list) or not MIN_THEMES <= len(raw) <= MAX_THEMES:
        raise ValueError("Qwen returned an invalid theme count")
    themes: list[dict[str, Any]] = []
    for raw_theme in raw:
        if not isinstance(raw_theme, Mapping):
            raise ValueError("Qwen theme is not an object")
        title = " ".join(str(raw_theme.get("title") or "").split())
        if len(title) < 3:
            raise ValueError("Qwen theme title is empty")
        try:
            claim_numbers = [int(value) for value in raw_theme.get("c") or []]
            question_numbers = [int(value) for value in raw_theme.get("q") or []]
        except (TypeError, ValueError) as exc:
            raise ValueError("Qwen returned non-numeric theme references") from exc
        if not claim_numbers or len(claim_numbers) != len(set(claim_numbers)) or any(v < 1 or v > len(claims) for v in claim_numbers):
            raise ValueError("Qwen returned an invalid theme claim reference")
        if len(question_numbers) != len(set(question_numbers)) or any(v < 1 or v > len(questions) for v in question_numbers):
            raise ValueError("Qwen returned an invalid theme question reference")
        themes.append({
            "title": title,
            "claim_ids": [str(claims[v - 1]["claim_id"]) for v in claim_numbers],
            "question_ids": [str(questions[v - 1]["question_id"]) for v in question_numbers],
        })
    if len({theme["title"].casefold() for theme in themes}) != len(themes):
        raise ValueError("Qwen returned duplicate theme titles")
    return themes


def _validate_batch(
    payload: Mapping[str, Any],
    questions: Sequence[Mapping[str, Any]],
    claims: Sequence[Mapping[str, Any]],
    *,
    require_question_coverage: bool = False,
) -> list[list[dict[str, Any]]]:
    """Project one theme's Qwen output onto registered claim and question identities.

    Sentence question tags are optional: a sentence must cite at least one claim, and the
    caller derives implicit question links from the claims' ``supporting_question_ids``.
    ``require_question_coverage`` keeps the legacy strict behaviour for callers that want it.
    """

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
                len(question_numbers) != len(set(question_numbers))
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
    if require_question_coverage:
        expected = set(range(1, len(questions) + 1))
        if covered != expected:
            missing = sorted(expected - covered)
            raise ValueError(f"Qwen did not cover every eligible question: {missing}")
    return paragraphs


def _link_questions(
    sentence: Mapping[str, Any],
    claim_by_id: Mapping[str, Mapping[str, Any]],
    eligible_question_ids: Sequence[str],
) -> list[str]:
    """Explicit Qwen tags plus every eligible question the cited claims were retrieved for."""

    allowed = set(eligible_question_ids)
    linked = [qid for qid in sentence.get("question_ids") or [] if qid in allowed]
    for claim_id in sentence.get("claim_ids") or []:
        for qid in claim_by_id[claim_id].get("supporting_question_ids") or []:
            if qid in allowed and qid not in linked:
                linked.append(qid)
    if not linked:
        raise ValueError("sentence cites claims that support no eligible question")
    return linked


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


def _valid_plan_checkpoint(
    path: Path,
    *,
    question_ids: Sequence[str],
    claim_ids: Sequence[str],
) -> list[dict[str, Any]] | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("question_ids") != list(question_ids) or payload.get("claim_ids") != list(claim_ids):
            return None
        themes = payload.get("themes")
        if not isinstance(themes, list) or not MIN_THEMES <= len(themes) <= MAX_THEMES:
            return None
        known_questions, known_claims = set(question_ids), set(claim_ids)
        for theme in themes:
            if (
                not isinstance(theme, dict)
                or not str(theme.get("title") or "").strip()
                or not theme.get("claim_ids")
                or not set(theme.get("claim_ids") or []) <= known_claims
                or not set(theme.get("question_ids") or []) <= known_questions
            ):
                return None
        return themes
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return None


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
                    or not sentence.get("claim_ids")
                    or not set(sentence.get("claim_ids") or []) <= known_claims
                    or not set(sentence.get("question_ids") or []) <= known_questions
                ):
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
    client = llm_client or LocalChatClient(endpoint, timeout=900.0)
    claim_by_id = {str(row["claim_id"]): row for row in registry["claims"]}
    all_claims = _claims_for_questions(eligible_questions, claim_by_id)
    eligible_question_ids = [str(row["question_id"]) for row in eligible_questions]
    all_claim_ids = [str(row["claim_id"]) for row in all_claims]
    question_by_id = {str(row["question_id"]): row for row in eligible_questions}

    def call(system: str, prompt: str, schema: dict[str, Any], max_tokens: int) -> Mapping[str, Any]:
        if not client.has_model(model):
            raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", f"exact Qwen model is unavailable: {model}")
        return client.chat_json(model, system, prompt, response_schema=schema, max_tokens=max_tokens, reasoning_effort="none")

    # Pass 1: outline.  The section is planned as ordered themes before any prose is
    # written, so the draft reads as a chapter rather than a sequence of question answers.
    plan_path = checkpoint_root / "plan.json"
    themes = _valid_plan_checkpoint(plan_path, question_ids=eligible_question_ids, claim_ids=all_claim_ids)
    if themes is None:
        try:
            response = call(
                PLAN_SYSTEM_PROMPT,
                _plan_prompt(section_id, str(packet["section_title"]), eligible_questions, all_claims),
                _plan_schema(len(eligible_questions), len(all_claims)),
                min(4096, max(1024, len(all_claims) * 24)),
            )
            themes = _validate_plan(response, eligible_questions, all_claims)
        except Exception as exc:
            raise BookEngineError(
                "SECTION_WRITER_FAILED",
                f"Qwen section plan failed at {section_id}: {type(exc).__name__}: {exc}",
            ) from exc
        _atomic_json(plan_path, {"question_ids": eligible_question_ids, "claim_ids": all_claim_ids, "themes": themes})

    # Pass 2: one prose call per theme, restricted to that theme's claims.
    completed: list[tuple[dict[str, Any], list[list[dict[str, Any]]]]] = []
    for theme_number, theme in enumerate(themes, 1):
        claims = [claim_by_id[cid] for cid in theme["claim_ids"]]
        questions = [question_by_id[qid] for qid in theme["question_ids"]]
        question_ids = [str(row["question_id"]) for row in questions]
        claim_ids = [str(row["claim_id"]) for row in claims]
        checkpoint_path = checkpoint_root / f"theme_{theme_number:03d}.json"
        paragraphs = _valid_checkpoint(checkpoint_path, question_ids=question_ids, claim_ids=claim_ids)
        if paragraphs is None:
            try:
                response = call(
                    SYSTEM_PROMPT,
                    _prompt(
                        section_id, str(packet["section_title"]),
                        {"number": theme_number, "count": len(themes), "title": theme["title"]},
                        questions, claims, previous_titles=[row["title"] for row in themes[:theme_number - 1]],
                    ),
                    _response_schema(len(questions), len(claims)),
                    min(8192, max(2048, len(claims) * 400)),
                )
                paragraphs = _validate_batch(response, questions, claims)
                for paragraph in paragraphs:
                    for sentence in paragraph:
                        sentence["question_ids"] = _link_questions(sentence, claim_by_id, eligible_question_ids)
            except Exception as exc:
                raise BookEngineError(
                    "SECTION_WRITER_FAILED",
                    f"Qwen writer failed at {section_id} theme {theme_number}: {type(exc).__name__}: {exc}",
                ) from exc
            _atomic_json(checkpoint_path, {
                "theme_number": theme_number,
                "theme_title": theme["title"],
                "question_ids": question_ids,
                "claim_ids": claim_ids,
                "paragraphs": paragraphs,
            })
        completed.append((theme, paragraphs))
        if progress:
            progress({
                "draft_id": draft_id,
                "section_id": section_id,
                "theme": theme_number,
                "theme_count": len(themes),
                "eligible_question_count": len(eligible_questions),
            })
    flat_paragraphs: list[list[dict[str, Any]]] = []
    paragraph_themes: list[dict[str, Any]] = []
    for theme_number, (theme, paragraphs) in enumerate(completed, 1):
        for paragraph in paragraphs:
            flat_paragraphs.append(paragraph)
            paragraph_themes.append({"theme_number": theme_number, "theme_title": theme["title"]})
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
        paragraph_rows.append({"paragraph_id": paragraph_id, "sentence_ids": sentence_ids, **paragraph_themes[paragraph_number - 1]})
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
        "theme_count": len(themes),
        "themes": [{"number": number, "title": theme["title"], "claim_count": len(theme["claim_ids"]), "question_count": len(theme["question_ids"])} for number, theme in enumerate(themes, 1)],
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
