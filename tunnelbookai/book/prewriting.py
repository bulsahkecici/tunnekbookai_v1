"""Resumable Qwen-assisted pre-writing evidence audit over canonical retrieval."""

from __future__ import annotations

import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

from tunnelbookai.canonical.hashing import canonical_sha256, sha256_file
from tunnelbookai.ingest.classify.arbiter import LocalChatClient
from tunnelbookai.ingest.classify.embeddings import LocalEmbeddingClient
from tunnelbookai.ingest.vision.provider import assert_loopback

from .errors import BookEngineError
from .inputs import BookInputs, load_book_inputs
from .lexical import focused_window, token_jaccard
from .retrieval import DEFAULT_POLICY, HybridRetriever, RetrievalPolicy, inspect_index


SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "prewriting-evidence-audit-v1"
SOFTWARE_VERSION = "prewriting-evidence-audit-v5-hybrid"
PROMPT_VERSION = "qwen-prewriting-evidence-v4-hybrid-focused"
MAX_TOP_K = 20
SNIPPET_CHARS = 1000
DUPLICATE_SNIPPET_JACCARD = 0.8
ALLOWED_STATUSES = {"SUPPORTED", "PARTIAL", "UNSUPPORTED"}
REASON_CODES = {
    "DIRECT_ANSWER",
    "COMPOSITE_ANSWER",
    "PARTIAL_ONLY",
    "NO_DIRECT_SUPPORT",
    "NO_SECTION_EVIDENCE",
}


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


def _atomic_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
            handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _section_key(section_id: str) -> tuple[int, ...]:
    return tuple(int(part) for part in section_id.split("."))


def _locator(row: Mapping[str, Any]) -> str:
    where = f"canonical={row['canonical_retrieval_path']}#L{row['canonical_line_number']}"
    if row.get("page_start") is not None:
        end = row.get("page_end")
        pages = str(row["page_start"]) if end in (None, row["page_start"]) else f"{row['page_start']}-{end}"
        where = f"pages={pages};{where}"
    elif row.get("slide_number") is not None:
        where = f"slide={row['slide_number']};{where}"
    elif row.get("sheet_name"):
        where = f"sheet={row['sheet_name']};{where}"
    return f"{row['document_id']}:{row['chunk_id']}:{where}"


class AuditRetriever:
    """Section-aware evidence retrieval for the audit: hybrid ranking over the whole corpus.

    Evidence may legitimately be reused across book sections, so the target section is
    never a filter: it only enriches the query (``section title. question``) so the dense
    signal sees the topical frame and the lexical signal sees the heading terms.
    """

    def __init__(
        self,
        inputs: BookInputs,
        *,
        client: LocalEmbeddingClient | None = None,
        policy: RetrievalPolicy = DEFAULT_POLICY,
    ) -> None:
        self.inputs = inputs
        self.hybrid = HybridRetriever(inputs.contract.project_root, client=client, policy=policy, inputs=inputs)
        self.root = self.hybrid.root
        self.manifest = self.hybrid.manifest

    @property
    def identity(self) -> dict[str, Any]:
        return self.hybrid.identity

    def retrieve(self, questions: Sequence[Mapping[str, Any]], section_id: str, *, top_k: int = 8) -> list[list[dict[str, Any]]]:
        if not questions:
            return []
        title = str(self.inputs.scope_by_id.get(section_id, {}).get("title") or "")
        dense = [f"{title}. {row['question']}" if title else str(row["question"]) for row in questions]
        lexical = [f"{row['question']} {title}" for row in questions]
        # Over-fetch so that overlapping chunks (structure-aware chunking repeats the tail
        # of the previous chunk) can be dropped without starving the question of evidence.
        ranked = self.hybrid.search(dense, lexical, top_k=top_k * 2)
        results: list[list[dict[str, Any]]] = []
        for question, candidates, query in zip(questions, ranked, lexical):
            rows: list[dict[str, Any]] = []
            kept: list[str] = []
            for row in candidates:
                snippet = focused_window(self.hybrid.text(row), query, chars=SNIPPET_CHARS)
                if any(token_jaccard(snippet, previous) >= DUPLICATE_SNIPPET_JACCARD for previous in kept):
                    continue
                kept.append(snippet)
                rows.append({
                    **row,
                    "evidence_ref": f"{question['question_id']}:E{len(rows) + 1}",
                    "source_locator": _locator(row),
                    "snippet": snippet,
                })
                if len(rows) >= top_k:
                    break
            results.append(rows)
        return results


def _llm_settings(inputs: BookInputs) -> tuple[str, str, str]:
    path = inputs.contract.project_root / "config" / "models.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    settings = payload.get("llm") or {}
    model = str(settings.get("model") or "").strip()
    endpoint = os.getenv(
        str(settings.get("endpoint_env") or "LLM_SERVER"),
        str(settings.get("default_endpoint") or ""),
    ).strip()
    if not model or not endpoint:
        raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", "LLM configuration is incomplete")
    return model, assert_loopback(endpoint), sha256_file(path)


SYSTEM_PROMPT = """Sen tünel mühendisliği kitabının kanıt denetçisisin.
Yalnızca verilen CANONICAL KANIT parçalarını kullan; genel bilgini kullanma ve çıkarım uydurma.
SUPPORTED: kanıtlar sorunun bütün maddi kapsamını doğrudan yanıtlıyor.
PARTIAL: kanıtlar sorunun yalnızca bir bölümünü yanıtlıyor veya ayrıntı eksik.
UNSUPPORTED: doğrudan yanıt veren kanıt yok.
Benzerlik skoru yalnızca retrieval sırasıdır; tek başına yeterlilik kanıtı değildir.
Her soru için yalnızca o soruya ait E sıra numaralarını seç.
Kısa kodlar: s=S(SUPPORTED), P(PARTIAL), U(UNSUPPORTED); r=D(DIRECT_ANSWER),
C(COMPOSITE_ANSWER), P(PARTIAL_ONLY), N(NO_DIRECT_SUPPORT). c 0-100 güven puanıdır.
Sonuçları soru sırasını koruyarak verilen kompakt JSON şemasında döndür."""


def _response_schema(question_count: int, maximum_evidence: int) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["results"],
        "properties": {
            "results": {
                "type": "array",
                "minItems": question_count,
                "maxItems": question_count,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["i", "s", "e", "r", "c"],
                    "properties": {
                        "i": {"type": "integer", "minimum": 1, "maximum": question_count},
                        "s": {"type": "string", "enum": ["S", "P", "U"]},
                        "e": {
                            "type": "array", "maxItems": maximum_evidence,
                            "items": {"type": "integer", "minimum": 1, "maximum": maximum_evidence},
                        },
                        "r": {"type": "string", "enum": ["D", "C", "P", "N"]},
                        "c": {"type": "integer", "minimum": 0, "maximum": 100},
                    },
                },
            },
        },
    }


def _prompt(section_id: str, section_title: str, questions: Sequence[Mapping[str, Any]], evidence: Sequence[Sequence[Mapping[str, Any]]]) -> str:
    blocks = [f"BÖLÜM {section_id}: {section_title}"]
    for order, (question, candidates) in enumerate(zip(questions, evidence), 1):
        blocks.append(f"\nSORU {order} [{question['question_id']}]: {question['question']}")
        if not candidates:
            blocks.append("CANONICAL KANIT: YOK")
            continue
        for rank, row in enumerate(candidates, 1):
            blocks.append(
                f"E{rank} | skor={row['score']:.6f} | belge={row['document_id']} | "
                f"chunk={row['chunk_id']} | {row['source_locator']}\n{row['snippet'][:SNIPPET_CHARS]}"
            )
    return "\n".join(blocks)


def _validate_llm_results(
    payload: Mapping[str, Any],
    questions: Sequence[Mapping[str, Any]],
    evidence: Sequence[Sequence[Mapping[str, Any]]],
) -> list[dict[str, Any]]:
    raw = payload.get("results")
    if not isinstance(raw, list) or len(raw) != len(questions):
        raise ValueError("Qwen result count does not match question batch")
    by_order: dict[int, Mapping[str, Any]] = {}
    for row in raw:
        if not isinstance(row, Mapping):
            raise ValueError("Qwen result is not an object")
        try:
            order = int(row.get("i"))
        except (TypeError, ValueError) as exc:
            raise ValueError("Qwen returned an invalid question order") from exc
        if order in by_order:
            raise ValueError("Qwen returned a duplicate question order")
        by_order[order] = row
    output: list[dict[str, Any]] = []
    status_map = {"S": "SUPPORTED", "P": "PARTIAL", "U": "UNSUPPORTED"}
    reason_map = {"D": "DIRECT_ANSWER", "C": "COMPOSITE_ANSWER", "P": "PARTIAL_ONLY", "N": "NO_DIRECT_SUPPORT"}
    for order, (question, candidates) in enumerate(zip(questions, evidence), 1):
        question_id = str(question["question_id"])
        row = by_order.get(order)
        if row is None:
            raise ValueError(f"Qwen omitted {question_id}")
        status = status_map.get(str(row.get("s") or ""), "")
        reason_code = reason_map.get(str(row.get("r") or ""), "")
        if status not in ALLOWED_STATUSES or reason_code not in REASON_CODES:
            raise ValueError(f"Qwen returned an invalid state for {question_id}")
        candidate_by_ref = {str(item["evidence_ref"]): item for item in candidates}
        refs = [f"{question_id}:E{int(value)}" for value in (row.get("e") or [])]
        if len(refs) != len(set(refs)) or any(ref not in candidate_by_ref for ref in refs):
            raise ValueError(f"Qwen returned an invalid evidence reference for {question_id}")
        if status == "UNSUPPORTED":
            refs = []
        elif not refs:
            raise ValueError(f"Qwen marked {question_id} {status} without evidence")
        try:
            confidence = float(row.get("c")) / 100.0
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Qwen returned invalid confidence for {question_id}") from exc
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(f"Qwen confidence is out of range for {question_id}")
        selected_refs = set(refs)
        output.append({
            "question_id": question_id,
            "section_id": str(question["section_id"]),
            "question": str(question["question"]),
            "status": status,
            "retrieved_chunk_ids": list(dict.fromkeys(str(item["chunk_id"]) for item in candidates)),
            "document_ids": list(dict.fromkeys(str(item["document_id"]) for item in candidates)),
            "source_locators": list(dict.fromkeys(str(item["source_locator"]) for item in candidates)),
            "authority_and_provenance": [{
                "document_id": item["document_id"],
                "chunk_id": item["chunk_id"],
                "canonical_retrieval_path": item["canonical_retrieval_path"],
                "canonical_line_number": item["canonical_line_number"],
                "score": item["score"],
                "dense_rank": item.get("dense_rank"),
                "lexical_rank": item.get("lexical_rank"),
                "selected_by_qwen": item["evidence_ref"] in selected_refs,
            } for item in candidates],
            "reason_code": reason_code,
            "confidence": round(confidence, 4),
        })
    return output


def _audit_batch(
    client: LocalChatClient,
    model: str,
    section_id: str,
    section_title: str,
    questions: Sequence[Mapping[str, Any]],
    evidence: Sequence[Sequence[Mapping[str, Any]]],
) -> list[dict[str, Any]]:
    payload = client.chat_json(
        model,
        SYSTEM_PROMPT,
        _prompt(section_id, section_title, questions, evidence),
        response_schema=_response_schema(len(questions), max(len(candidates) for candidates in evidence)),
        max_tokens=min(4096, max(1024, len(questions) * 60)),
        reasoning_effort="none",
    )
    return _validate_llm_results(payload, questions, evidence)


def _audit_with_split(
    client: LocalChatClient,
    model: str,
    section_id: str,
    section_title: str,
    questions: Sequence[Mapping[str, Any]],
    evidence: Sequence[Sequence[Mapping[str, Any]]],
) -> list[dict[str, Any]]:
    if any(not candidates for candidates in evidence):
        nonempty = [(question, candidates) for question, candidates in zip(questions, evidence) if candidates]
        audited = _audit_with_split(
            client, model, section_id, section_title,
            [item[0] for item in nonempty], [item[1] for item in nonempty],
        ) if nonempty else []
        by_id = {row["question_id"]: row for row in audited}
        output: list[dict[str, Any]] = []
        for question, candidates in zip(questions, evidence):
            if candidates:
                output.append(by_id[str(question["question_id"])])
            else:
                output.append({
                    "question_id": str(question["question_id"]),
                    "section_id": str(question["section_id"]),
                    "question": str(question["question"]),
                    "status": "UNSUPPORTED",
                    "retrieved_chunk_ids": [],
                    "document_ids": [],
                    "source_locators": [],
                    "authority_and_provenance": [],
                    "reason_code": "NO_SECTION_EVIDENCE",
                    "confidence": 1.0,
                })
        return output
    try:
        return _audit_batch(client, model, section_id, section_title, questions, evidence)
    except Exception as exc:
        if len(questions) == 1:
            raise BookEngineError(
                "LLM_EVIDENCE_AUDIT_FAILED",
                f"Qwen could not audit {questions[0]['question_id']}: {type(exc).__name__}: {exc}",
            ) from exc
        middle = len(questions) // 2
        return [
            *_audit_with_split(client, model, section_id, section_title, questions[:middle], evidence[:middle]),
            *_audit_with_split(client, model, section_id, section_title, questions[middle:], evidence[middle:]),
        ]


def _section_summary(
    section_id: str,
    section_title: str,
    rows: Sequence[Mapping[str, Any]],
    *,
    target: int,
    human_analysis: bool = False,
) -> dict[str, Any]:
    counts = Counter(str(row["status"]) for row in rows)
    supported = counts["SUPPORTED"]
    if human_analysis:
        # Chapter 7 style findings: literature can support context but the section is
        # written from project analysis artifacts, never from retrieval alone.
        readiness = "HUMAN_ANALYSIS_ARTIFACT_REQUIRED"
    elif supported >= target:
        readiness = "READY" if supported == len(rows) else "READY_WITH_LIMITATIONS"
    elif supported + counts["PARTIAL"] >= target:
        readiness = "READY_WITH_LIMITATIONS"
    else:
        readiness = "EVIDENCE_GAP"
    return {
        "section_id": section_id,
        "section_title": section_title,
        "total": len(rows),
        "supported": supported,
        "partial": counts["PARTIAL"],
        "unsupported": counts["UNSUPPORTED"],
        "supported_ratio": round(supported / len(rows), 6) if rows else 0.0,
        "preferred_target": target,
        "preferred_target_met": supported >= target,
        "readiness": readiness,
    }


def _valid_section_checkpoint(path: Path, questions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]] | None:
    if not path.is_file():
        return None
    try:
        rows = _read_jsonl(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    expected = [str(row["question_id"]) for row in questions]
    if [str(row.get("question_id")) for row in rows] != expected:
        return None
    if any(str(row.get("status")) not in ALLOWED_STATUSES for row in rows):
        return None
    return rows


def _write_report(path: Path, summary: Mapping[str, Any]) -> None:
    counts = summary["counts"]
    lines = [
        "# Yazım öncesi kanıt auditi",
        "",
        f"- Durum: **{summary['status']}**",
        f"- Qwen modeli: `{summary['llm_model_id']}`",
        f"- Embedding modeli: `{summary['embedding_model_id']}`",
        f"- İncelenen soru: **{summary['questions_audited']} / {summary['question_count']}**",
        f"- SUPPORTED: **{counts['SUPPORTED']}**",
        f"- PARTIAL: **{counts['PARTIAL']}**",
        f"- UNSUPPORTED: **{counts['UNSUPPORTED']}**",
        "",
        "| Bölüm | Başlık | Destekli | Kısmi | Desteksiz | Hazırlık |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in summary["sections"]:
        lines.append(
            f"| {row['section_id']} | {row['section_title']} | {row['supported']} | "
            f"{row['partial']} | {row['unsupported']} | {row['readiness']} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def run_prewriting_audit(
    project_root: Path | str | None = None,
    *,
    section_ids: Sequence[str] | None = None,
    batch_size: int = 8,
    top_k: int = 8,
    progress: Any = None,
    embedding_client: LocalEmbeddingClient | None = None,
    llm_client: LocalChatClient | None = None,
    policy: RetrievalPolicy = DEFAULT_POLICY,
) -> dict[str, Any]:
    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    if batch_size < 1 or batch_size > 50:
        raise BookEngineError("INVALID_BATCH_SIZE", "audit batch size must be between 1 and 50")
    if top_k < 1 or top_k > MAX_TOP_K:
        raise BookEngineError("INVALID_TOP_K", f"audit top_k must be between 1 and {MAX_TOP_K}")
    inputs = load_book_inputs(root)
    status = inspect_index(root)
    if not status.ready or not status.manifest:
        raise BookEngineError("RETRIEVAL_INDEX_NOT_READY", status.reason)
    all_sections = sorted(inputs.question_section_ids, key=_section_key)
    requested = list(section_ids or all_sections)
    if len(requested) != len(set(requested)) or any(section not in inputs.questions_by_section for section in requested):
        raise BookEngineError("UNKNOWN_SECTION", "audit section selection is invalid")
    llm_model, llm_endpoint, model_config_sha = _llm_settings(inputs)
    identity = {
        "scope_sha256": inputs.identities["scope_sha256"],
        "question_bank_sha256": inputs.identities["question_bank_sha256"],
        "canonical_corpus_digest": status.manifest["canonical_corpus_digest"],
        "retrieval_index_id": status.manifest["index_id"],
        "lexical_index_id": (status.lexical or {}).get("lexical_index_id"),
        "retrieval_policy": policy.to_dict(),
        "embedding_model_id": status.manifest["model_id"],
        "llm_model_id": llm_model,
        "model_configuration": model_config_sha,
        "prompt_version": PROMPT_VERSION,
        "software_version": SOFTWARE_VERSION,
        "top_k": top_k,
    }
    audit_id = "PEA_" + canonical_sha256(identity)
    run_root = root / "audit" / "book" / "prewriting" / audit_id
    section_root = run_root / "sections"
    run_manifest_path = run_root / "manifest.json"
    active_path = root / "audit" / "book" / "prewriting_evidence_audit.json"
    report_path = root / "reports" / "prewriting_evidence_audit.md"
    completed: dict[str, list[dict[str, Any]]] = {}
    for section_id in all_sections:
        checkpoint = _valid_section_checkpoint(
            section_root / f"section_{section_id.replace('.', '_')}.jsonl",
            inputs.questions_by_section[section_id],
        )
        if checkpoint is not None:
            completed[section_id] = checkpoint
    remaining = [section for section in requested if section not in completed]
    retriever: AuditRetriever | None = None
    chat = llm_client or LocalChatClient(llm_endpoint, timeout=600.0)
    if remaining and not chat.has_model(llm_model):
        raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", f"exact Qwen model is unavailable: {llm_model}")
    if remaining and status.lexical is None:
        raise BookEngineError("LEXICAL_INDEX_MISSING", "lexical index is missing; run book build-index first")

    def write_state() -> dict[str, Any]:
        summaries = [
            _section_summary(
                section, str(inputs.scope_by_id[section]["title"]), completed[section],
                target=inputs.contract.section_target(len(inputs.questions_by_section[section])),
                human_analysis=inputs.requires_human_analysis(section),
            )
            for section in all_sections if section in completed
        ]
        counts = Counter(str(row["status"]) for rows in completed.values() for row in rows)
        payload = {
            "schema_version": SCHEMA_VERSION,
            "contract_version": CONTRACT_VERSION,
            "audit_id": audit_id,
            **identity,
            "status": "COMPLETE" if len(completed) == len(all_sections) else "IN_PROGRESS",
            "updated_at": _now(),
            "question_count": len(inputs.questions),
            "questions_audited": sum(len(rows) for rows in completed.values()),
            "section_count": len(all_sections),
            "sections_audited": len(completed),
            "counts": {status_name: counts[status_name] for status_name in sorted(ALLOWED_STATUSES)},
            "sections": summaries,
            "results_path": (run_root / "results.jsonl").relative_to(root).as_posix() if len(completed) == len(all_sections) else None,
        }
        _atomic_json(run_manifest_path, payload)
        _atomic_json(active_path, payload)
        _write_report(report_path, payload)
        return payload

    write_state()
    for section_id in remaining:
        if retriever is None:
            retriever = AuditRetriever(inputs, client=embedding_client, policy=policy)
        questions = list(inputs.questions_by_section[section_id])
        evidence = retriever.retrieve(questions, section_id, top_k=top_k)
        rows: list[dict[str, Any]] = []
        title = str(inputs.scope_by_id[section_id]["title"])
        for start in range(0, len(questions), batch_size):
            rows.extend(_audit_with_split(
                chat, llm_model, section_id, title,
                questions[start:start + batch_size], evidence[start:start + batch_size],
            ))
        checkpoint_path = section_root / f"section_{section_id.replace('.', '_')}.jsonl"
        _atomic_jsonl(checkpoint_path, rows)
        completed[section_id] = rows
        state = write_state()
        if progress:
            progress({
                "audit_id": audit_id,
                "section_id": section_id,
                "sections_audited": state["sections_audited"],
                "section_count": state["section_count"],
                "questions_audited": state["questions_audited"],
            })
    if len(completed) == len(all_sections):
        ordered = [row for section in all_sections for row in completed[section]]
        _atomic_jsonl(run_root / "results.jsonl", ordered)
    return write_state()


__all__ = ["AuditRetriever", "run_prewriting_audit"]
