"""Resumable Qwen post-writing sentence-to-claim evidence review."""

from __future__ import annotations

import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from tunnelbookai.canonical.hashing import canonical_sha256, sha256_file
from tunnelbookai.ingest.classify.arbiter import LocalChatClient

from .errors import BookEngineError
from .inputs import load_book_inputs
from .preparation import inspect_preparation
from .prewriting import _llm_settings
from .writer import inspect_drafts


SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "postwriting-sentence-evidence-v1"
SOFTWARE_VERSION = "postwriting-sentence-evidence-v2"
PROMPT_VERSION = "qwen-sentence-entailment-v1"
ALLOWED_STATUSES = {"SUPPORTED", "PARTIAL", "UNSUPPORTED", "NON_FACTUAL_OR_EDITORIAL"}


SYSTEM_PROMPT = """Sen teknik kitap için katı bir cümle-kanit hakemisin.
Yalnızca her cümlenin altında verilen KAYITLI CANONICAL PASAJLARI kullan.
SUPPORTED: cümlenin bütün maddi olguları pasajlarca doğrudan destekleniyor.
PARTIAL: yalnızca bir bölümü destekleniyor veya cümle pasajı aşan genelleme/neden-sonuç içeriyor.
UNSUPPORTED: doğrudan destek yok, çelişki var ya da temel olgu pasajlarda bulunmuyor.
NON_FACTUAL_OR_EDITORIAL: doğrulanabilir teknik olgu ileri sürmeyen salt geçiş/yorum cümlesi.
Benzerlik veya claim etiketi tek başına kanıt değildir. Genel bilgini kullanma.
Kısa kodlar: s=S/P/U/E; r=D(direct), C(composite), O(overreach), N(no support),
E(editorial); c 0-100 güven. e yalnızca gerçekten destek veren C sıra numaralarıdır.
Sonucu yalnızca istenen JSON şemasında ve cümle sırasını koruyarak döndür."""


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


def _write_report(path: Path, summary: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> None:
    counts = summary["counts"]
    lines = [
        f"# Yazım sonrası cümle-kanıt auditi — {summary['section_id']}",
        "",
        f"- Karar: **{summary['audit_decision']}**",
        f"- Denetlenen cümle: **{summary['sentences_audited']} / {summary['sentence_count']}**",
        f"- SUPPORTED: **{counts['SUPPORTED']}**",
        f"- PARTIAL: **{counts['PARTIAL']}**",
        f"- UNSUPPORTED: **{counts['UNSUPPORTED']}**",
        f"- NON_FACTUAL_OR_EDITORIAL: **{counts['NON_FACTUAL_OR_EDITORIAL']}**",
        f"- Maddi düzeltme adayı: **{summary['material_issue_count']}**",
        "",
        "| Cümle | Durum | Neden | Güven | Metin |",
        "|---|---|---|---:|---|",
    ]
    for row in rows:
        if row["status"] not in {"PARTIAL", "UNSUPPORTED"}:
            continue
        text = str(row["sentence"]).replace("|", "\\|")
        lines.append(
            f"| {row['sentence_id']} | {row['status']} | {row['reason_code']} | "
            f"{float(row['confidence']):.0%} | {text} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _schema(sentence_count: int, claim_count: int) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["results"],
        "properties": {
            "results": {
                "type": "array", "minItems": sentence_count, "maxItems": sentence_count,
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["i", "s", "e", "r", "c"],
                    "properties": {
                        "i": {"type": "integer", "minimum": 1, "maximum": sentence_count},
                        "s": {"type": "string", "enum": ["S", "P", "U", "E"]},
                        "e": {
                            "type": "array", "maxItems": 4,
                            "items": {"type": "integer", "minimum": 1, "maximum": claim_count},
                        },
                        "r": {"type": "string", "enum": ["D", "C", "O", "N", "E"]},
                        "c": {"type": "integer", "minimum": 0, "maximum": 100},
                    },
                },
            },
        },
    }


def _prompt(sentences: Sequence[Mapping[str, Any]], claim_by_id: Mapping[str, Mapping[str, Any]]) -> tuple[str, list[Mapping[str, Any]]]:
    claim_ids = list(dict.fromkeys(
        str(claim_id) for sentence in sentences for claim_id in sentence["claim_ids"]
    ))
    claims = [claim_by_id[value] for value in claim_ids]
    claim_numbers = {str(row["claim_id"]): number for number, row in enumerate(claims, 1)}
    lines: list[str] = []
    for index, sentence in enumerate(sentences, 1):
        lines.append(f"CÜMLE {index} [{sentence['sentence_id']}]: {sentence['text']}")
        for claim_id in sentence["claim_ids"]:
            claim = claim_by_id[str(claim_id)]
            passage = " ".join(str(claim["claim_text"]).split())[:900]
            lines.append(
                f"C{claim_numbers[str(claim_id)]} | {claim['document_id']} | {claim['locator']}\n{passage}"
            )
        lines.append("")
    return "\n".join(lines), claims


def _validate_results(
    payload: Mapping[str, Any],
    sentences: Sequence[Mapping[str, Any]],
    claims: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    raw = payload.get("results")
    if not isinstance(raw, list) or len(raw) != len(sentences):
        raise ValueError("Qwen result count differs from the sentence batch")
    by_index: dict[int, Mapping[str, Any]] = {}
    for row in raw:
        if not isinstance(row, Mapping):
            raise ValueError("Qwen result is not an object")
        index = int(row.get("i"))
        if index in by_index:
            raise ValueError("Qwen returned a duplicate sentence index")
        by_index[index] = row
    status_map = {"S": "SUPPORTED", "P": "PARTIAL", "U": "UNSUPPORTED", "E": "NON_FACTUAL_OR_EDITORIAL"}
    reason_map = {"D": "DIRECT_SUPPORT", "C": "COMPOSITE_SUPPORT", "O": "CLAIM_OVERREACH", "N": "NO_DIRECT_SUPPORT", "E": "EDITORIAL_SENTENCE"}
    output: list[dict[str, Any]] = []
    for index, sentence in enumerate(sentences, 1):
        row = by_index.get(index)
        if row is None:
            raise ValueError(f"Qwen omitted sentence {index}")
        status = status_map.get(str(row.get("s") or ""), "")
        reason_code = reason_map.get(str(row.get("r") or ""), "")
        if status not in ALLOWED_STATUSES or not reason_code:
            raise ValueError("Qwen returned an invalid audit state")
        refs = [int(value) for value in row.get("e") or []]
        if len(refs) != len(set(refs)) or any(value < 1 or value > len(claims) for value in refs):
            raise ValueError("Qwen returned an invalid evidence reference")
        selected = [claims[value - 1] for value in refs]
        mapped = set(str(value) for value in sentence["claim_ids"])
        if any(str(value["claim_id"]) not in mapped for value in selected):
            raise ValueError("Qwen selected evidence not mapped to the sentence")
        if status in {"SUPPORTED", "PARTIAL"} and not selected:
            raise ValueError(f"Qwen marked sentence {index} {status} without evidence")
        if status in {"UNSUPPORTED", "NON_FACTUAL_OR_EDITORIAL"}:
            selected = []
        confidence = float(row.get("c")) / 100.0
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("Qwen confidence is outside 0-1")
        output.append({
            "sentence_id": sentence["sentence_id"],
            "paragraph_id": sentence["paragraph_id"],
            "section_id": sentence["sentence_id"].rsplit("-S", 1)[0],
            "sentence": sentence["text"],
            "status": status,
            "mapped_claim_ids": list(sentence["claim_ids"]),
            "supporting_claim_ids": [str(value["claim_id"]) for value in selected],
            "supporting_document_ids": list(dict.fromkeys(str(value["document_id"]) for value in selected)),
            "source_locators": list(dict.fromkeys(str(value["locator"]) for value in selected)),
            "question_ids": list(sentence["question_ids"]),
            "reason_code": reason_code,
            "confidence": round(confidence, 4),
        })
    return output


def _audit_with_split(
    client: LocalChatClient,
    model: str,
    sentences: Sequence[Mapping[str, Any]],
    claim_by_id: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    prompt, claims = _prompt(sentences, claim_by_id)
    try:
        response = client.chat_json(
            model, SYSTEM_PROMPT, prompt,
            response_schema=_schema(len(sentences), len(claims)),
            max_tokens=min(8192, max(2048, len(sentences) * 320)),
            reasoning_effort="none",
        )
        return _validate_results(response, sentences, claims)
    except Exception:
        if len(sentences) == 1:
            raise
        middle = len(sentences) // 2
        return [
            *_audit_with_split(client, model, sentences[:middle], claim_by_id),
            *_audit_with_split(client, model, sentences[middle:], claim_by_id),
        ]


def run_evidence_review(
    section_id: str,
    project_root: Path | str | None = None,
    *,
    batch_size: int = 12,
    progress: Any = None,
    llm_client: LocalChatClient | None = None,
) -> dict[str, Any]:
    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    if batch_size < 1 or batch_size > 20:
        raise BookEngineError("INVALID_BATCH_SIZE", "evidence-review batch size must be between 1 and 20")
    inputs = load_book_inputs(root)
    preparation = inspect_preparation(root, inputs=inputs)
    drafts = inspect_drafts(root, preparation=preparation)
    draft = next((row for row in drafts if row["section_id"] == section_id), None)
    if not draft:
        raise BookEngineError("SECTION_DRAFT_NOT_READY", f"no valid active draft for section {section_id}")
    prep_entry = next(row for row in preparation["sections"] if row["section_id"] == section_id)
    registry = _read_json(root / prep_entry["claim_registry_path"], "SECTION_PREPARATION_INVALID")
    sentence_map = _read_json(root / draft["sentence_map_path"], "SECTION_DRAFT_INVALID")
    claim_by_id = {str(row["claim_id"]): row for row in registry["claims"]}
    sentences = list(sentence_map["sentences"])
    if any(claim_id not in claim_by_id for row in sentences for claim_id in row["claim_ids"]):
        raise BookEngineError("SECTION_DRAFT_INVALID", "sentence map references unknown claims")
    model, endpoint, model_configuration = _llm_settings(inputs)
    identity = {
        "section_id": section_id,
        "draft_id": draft["draft_id"],
        "draft_sha256": draft["draft_sha256"],
        "sentence_map_sha256": draft["sentence_map_sha256"],
        "claim_registry_id": registry["registry_id"],
        "claim_registry_sha256": prep_entry["claim_registry_sha256"],
        "model_id": model,
        "model_configuration": model_configuration,
        "prompt_version": PROMPT_VERSION,
        "software_version": SOFTWARE_VERSION,
        "batch_size": batch_size,
    }
    audit_id = "PSE_" + canonical_sha256(identity)
    run_root = root / "audit" / "book" / "postwriting" / audit_id
    checkpoint_root = run_root / "batches"
    client = llm_client or LocalChatClient(endpoint, timeout=600.0)
    results: list[dict[str, Any]] = []
    batches = [sentences[start:start + batch_size] for start in range(0, len(sentences), batch_size)]
    for batch_number, batch in enumerate(batches, 1):
        checkpoint = checkpoint_root / f"batch_{batch_number:03d}.json"
        batch_ids = [str(row["sentence_id"]) for row in batch]
        rows: list[dict[str, Any]] | None = None
        if checkpoint.is_file():
            try:
                candidate = _read_json(checkpoint, "POSTWRITING_AUDIT_INVALID")
                if candidate.get("sentence_ids") == batch_ids and isinstance(candidate.get("results"), list):
                    rows = candidate["results"]
            except BookEngineError:
                rows = None
        if rows is None:
            if not client.has_model(model):
                raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", f"exact Qwen model is unavailable: {model}")
            try:
                rows = _audit_with_split(client, model, batch, claim_by_id)
            except Exception as exc:
                raise BookEngineError(
                    "POSTWRITING_EVIDENCE_REVIEW_FAILED",
                    f"Qwen audit failed at {section_id} batch {batch_number}: {type(exc).__name__}: {exc}",
                ) from exc
            _atomic_json(checkpoint, {"batch_number": batch_number, "sentence_ids": batch_ids, "results": rows})
        results.extend(rows)
        if progress:
            progress({
                "audit_id": audit_id, "section_id": section_id,
                "batch": batch_number, "batch_count": len(batches),
                "sentences_audited": len(results), "sentence_count": len(sentences),
            })
    counts = Counter(str(row["status"]) for row in results)
    results_path = run_root / "results.jsonl"
    _atomic_jsonl(results_path, results)
    summary = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "stage": "POSTWRITING_EVIDENCE_AUDIT",
        "status": "COMPLETE",
        "audit_id": audit_id,
        "identity": identity,
        "updated_at": _now(),
        "section_id": section_id,
        "sentence_count": len(sentences),
        "sentences_audited": len(results),
        "counts": {value: counts[value] for value in sorted(ALLOWED_STATUSES)},
        "material_issue_count": counts["PARTIAL"] + counts["UNSUPPORTED"],
        "audit_decision": "PASS" if counts["PARTIAL"] + counts["UNSUPPORTED"] == 0 else "REVISION_REQUIRED",
        "results_path": results_path.relative_to(root).as_posix(),
        "results_sha256": sha256_file(results_path),
    }
    _atomic_json(run_root / "manifest.json", summary)
    _atomic_json(root / "audit" / "book" / "postwriting" / f"section_{section_id.replace('.', '_')}.json", summary)
    _write_report(root / "reports" / f"postwriting_evidence_review_{section_id.replace('.', '_')}.md", summary, results)
    return summary


def inspect_evidence_reviews(
    project_root: Path | str | None = None,
    *,
    drafts: Sequence[Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Return complete post-writing reviews still bound to active draft hashes."""

    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    active_drafts = list(drafts) if drafts is not None else inspect_drafts(root)
    by_section = {str(row["section_id"]): row for row in active_drafts}
    active_root = root / "audit" / "book" / "postwriting"
    if not active_root.is_dir():
        return []
    output: list[dict[str, Any]] = []
    for path in sorted(active_root.glob("section_*.json")):
        try:
            summary = _read_json(path, "POSTWRITING_AUDIT_INVALID")
            section_id = str(summary.get("section_id") or "")
            draft = by_section.get(section_id)
            identity = summary.get("identity") or {}
            if (
                not draft
                or summary.get("status") != "COMPLETE"
                or identity.get("draft_id") != draft.get("draft_id")
                or identity.get("draft_sha256") != draft.get("draft_sha256")
                or identity.get("sentence_map_sha256") != draft.get("sentence_map_sha256")
            ):
                continue
            results_path = (root / str(summary["results_path"])).resolve()
            boundary = (root / "audit" / "book" / "postwriting").resolve()
            if boundary not in results_path.parents or sha256_file(results_path) != summary.get("results_sha256"):
                continue
            if sum(1 for line in results_path.read_text(encoding="utf-8").splitlines() if line.strip()) != int(summary["sentence_count"]):
                continue
            output.append(summary)
        except (BookEngineError, OSError, KeyError, TypeError, ValueError):
            continue
    return output


__all__ = ["inspect_evidence_reviews", "run_evidence_review"]
