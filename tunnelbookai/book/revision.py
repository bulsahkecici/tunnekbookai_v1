"""Bounded, evidence-first revision of an audited section draft."""

from __future__ import annotations

import json
import os
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Mapping, Sequence

from tunnelbookai.canonical.hashing import canonical_sha256, sha256_file

from .errors import BookEngineError
from .evidence_review import inspect_evidence_reviews
from .inputs import load_book_inputs
from .preparation import inspect_preparation
from .writer import inspect_drafts


SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "section-revision-v1"
SOFTWARE_VERSION = "section-revision-v1"
EVIDENCE_ISSUE_STATES = {"PARTIAL", "UNSUPPORTED"}
DUPLICATE_SIMILARITY = 0.75


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


def _read_jsonl(path: Path, code: str) -> list[dict[str, Any]]:
    try:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BookEngineError(code, f"cannot read {path}: {exc}") from exc


def _normalized_text(value: str) -> str:
    return " ".join(re.findall(r"[a-zçğıöşü0-9]+", value.casefold()))


def _merge_unique(target: dict[str, Any], source: Mapping[str, Any], field: str) -> None:
    target[field] = list(dict.fromkeys([*(target.get(field) or []), *(source.get(field) or [])]))


def _plan_revision(
    sentence_map: Mapping[str, Any],
    review_rows: Sequence[Mapping[str, Any]],
    *,
    duplicate_similarity: float = DUPLICATE_SIMILARITY,
) -> tuple[list[list[dict[str, Any]]], list[dict[str, Any]]]:
    """Remove material evidence issues and merge only high-confidence repetitions.

    A repetition is mergeable only when its normalized wording is highly similar and it
    shares at least one mapped canonical claim with an earlier retained sentence. Merging
    preserves the union of the original claim/question provenance without creating prose.
    """

    reviews = {str(row.get("sentence_id")): row for row in review_rows}
    source_sentences = list(sentence_map.get("sentences") or [])
    source_ids = [str(row.get("sentence_id")) for row in source_sentences]
    if len(reviews) != len(source_sentences) or set(reviews) != set(source_ids):
        raise BookEngineError(
            "REVISION_INPUT_INVALID",
            "evidence-review rows do not exactly cover the active draft sentence map",
        )

    kept: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    for source in source_sentences:
        source_id = str(source["sentence_id"])
        review = reviews[source_id]
        status = str(review.get("status") or "")
        if str(review.get("sentence") or "") != str(source.get("text") or ""):
            raise BookEngineError("REVISION_INPUT_INVALID", f"review text mismatch for {source_id}")
        if status in EVIDENCE_ISSUE_STATES:
            actions.append({
                "source_sentence_id": source_id,
                "action": "REMOVED_EVIDENCE_ISSUE",
                "prior_evidence_status": status,
                "reason_code": str(review.get("reason_code") or ""),
                "target_source_sentence_id": None,
                "similarity": None,
            })
            continue

        candidate = dict(source)
        duplicate: dict[str, Any] | None = None
        similarity = 0.0
        for earlier in kept:
            if not set(candidate.get("claim_ids") or []) & set(earlier.get("claim_ids") or []):
                continue
            score = SequenceMatcher(
                None,
                _normalized_text(str(earlier["text"])),
                _normalized_text(str(candidate["text"])),
            ).ratio()
            if score >= duplicate_similarity and score > similarity:
                duplicate = earlier
                similarity = score
        if duplicate is not None:
            for field in ("claim_ids", "question_ids", "document_ids", "source_locators"):
                _merge_unique(duplicate, candidate, field)
            actions.append({
                "source_sentence_id": source_id,
                "action": "MERGED_REDUNDANT",
                "prior_evidence_status": status,
                "reason_code": "HIGH_TEXT_SIMILARITY_WITH_SHARED_CLAIM",
                "target_source_sentence_id": str(duplicate["sentence_id"]),
                "similarity": round(similarity, 4),
            })
            continue

        kept.append(candidate)
        actions.append({
            "source_sentence_id": source_id,
            "action": "KEPT",
            "prior_evidence_status": status,
            "reason_code": "NO_MATERIAL_EVIDENCE_ISSUE",
            "target_source_sentence_id": source_id,
            "similarity": None,
        })

    kept_by_old_id = {str(row["sentence_id"]): row for row in kept}
    paragraph_order = [str(row["paragraph_id"]) for row in sentence_map.get("paragraphs") or []]
    grouped: list[list[dict[str, Any]]] = []
    old_to_new: dict[str, str] = {}
    sentence_number = 0
    paragraph_number = 0
    section_id = str(sentence_map.get("section_id") or "")
    for old_paragraph_id in paragraph_order:
        rows = [row for row in kept if str(row.get("paragraph_id")) == old_paragraph_id]
        if not rows:
            continue
        paragraph_number += 1
        new_paragraph_id = f"{section_id}-P{paragraph_number:03d}"
        output_rows: list[dict[str, Any]] = []
        for row in rows:
            sentence_number += 1
            old_id = str(row["sentence_id"])
            new_id = f"{section_id}-S{sentence_number:03d}"
            old_to_new[old_id] = new_id
            output_rows.append({
                **row,
                "sentence_id": new_id,
                "paragraph_id": new_paragraph_id,
                "audit_status": "PENDING_POSTWRITING_EVIDENCE_AUDIT",
            })
        grouped.append(output_rows)

    for action in actions:
        target = action.pop("target_source_sentence_id")
        action["target_sentence_id"] = old_to_new.get(str(target)) if target else None
    if not grouped or not kept_by_old_id:
        raise BookEngineError("REVISION_EMPTY", "bounded revision would remove the entire section")
    return grouped, actions


def _markdown(section_id: str, title: str, paragraphs: Sequence[Sequence[Mapping[str, Any]]]) -> str:
    lines = [f"# {section_id} {title}", ""]
    for paragraph in paragraphs:
        lines.extend([" ".join(str(row["text"]).strip() for row in paragraph), ""])
    return "\n".join(lines).rstrip() + "\n"


def _report(summary: Mapping[str, Any]) -> str:
    return "\n".join([
        f"# Sınırlı editoryal revizyon — {summary['section_id']}",
        "",
        f"- Revizyon: **{summary['revision_number']} / {summary['max_editorial_revisions']}**",
        f"- Önceki taslak: `{summary['parent_draft_id']}`",
        f"- Yeni taslak: `{summary['draft_id']}`",
        f"- Önceki cümle: **{summary['source_sentence_count']}**",
        f"- Yeni cümle: **{summary['sentence_count']}**",
        f"- Kanıt sorunu nedeniyle çıkarılan: **{summary['removed_evidence_issue_count']}**",
        f"- Yüksek güvenli tekrar olarak birleştirilen: **{summary['merged_redundant_count']}**",
        "",
        "Bu revizyon yeni olgusal metin üretmez. PARTIAL/UNSUPPORTED cümleleri çıkarır;",
        "yalnız ortak canonical claim taşıyan yüksek benzerlikli cümleleri birleştirir ve",
        "kaynak soru/claim bağlantılarını korur. Yeni taslak yeniden kanıt ve kapsam auditine tabidir.",
        "",
    ])


def run_revision(section_id: str, project_root: Path | str | None = None) -> dict[str, Any]:
    """Create and activate one immutable bounded revision for an audited draft."""

    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    from .freeze import is_section_frozen
    if is_section_frozen(root, section_id):
        raise BookEngineError("SECTION_FROZEN", f"section {section_id} is immutable while frozen")
    inputs = load_book_inputs(root)
    preparation = inspect_preparation(root, inputs=inputs)
    drafts = inspect_drafts(root, preparation=preparation)
    reviews = inspect_evidence_reviews(root, drafts=drafts)
    draft = next((row for row in drafts if row["section_id"] == section_id), None)
    review = next((row for row in reviews if row["section_id"] == section_id), None)
    if not draft or not review:
        raise BookEngineError(
            "POSTWRITING_EVIDENCE_REVIEW_REQUIRED",
            f"a complete evidence review of the active draft is required for {section_id}",
        )
    if review.get("audit_decision") != "REVISION_REQUIRED":
        raise BookEngineError("REVISION_NOT_REQUIRED", f"active draft for {section_id} has no material evidence issue")

    max_revisions = int(inputs.contract.payload["section_policy"]["max_editorial_revisions"])
    parent_revision = int((draft.get("identity") or {}).get("revision_number") or 0)
    revision_number = parent_revision + 1
    if revision_number > max_revisions:
        raise BookEngineError(
            "REVISION_LIMIT_REACHED",
            f"section {section_id} already used {parent_revision} editorial revisions",
        )

    sentence_map = _read_json(root / str(draft["sentence_map_path"]), "SECTION_DRAFT_INVALID")
    review_rows = _read_jsonl(root / str(review["results_path"]), "POSTWRITING_AUDIT_INVALID")
    paragraphs, actions = _plan_revision(sentence_map, review_rows)
    prep_entry = next(row for row in preparation["sections"] if row["section_id"] == section_id)
    identity = {
        "section_id": section_id,
        "packet_id": prep_entry["packet_id"],
        "packet_sha256": prep_entry["packet_sha256"],
        "claim_registry_id": prep_entry["claim_registry_id"],
        "claim_registry_sha256": prep_entry["claim_registry_sha256"],
        "parent_draft_id": draft["draft_id"],
        "parent_draft_sha256": draft["draft_sha256"],
        "parent_sentence_map_sha256": draft["sentence_map_sha256"],
        "parent_evidence_review_id": review["audit_id"],
        "parent_evidence_review_sha256": review["results_sha256"],
        "revision_number": revision_number,
        "duplicate_similarity": DUPLICATE_SIMILARITY,
        "prompt_version": "deterministic-evidence-first-revision-v1",
        "software_version": SOFTWARE_VERSION,
    }
    draft_id = "DRF_" + canonical_sha256(identity)
    draft_root = root / "book" / "production" / "drafts" / draft_id
    flat = [row for paragraph in paragraphs for row in paragraph]
    paragraph_rows = [{
        "paragraph_id": paragraph[0]["paragraph_id"],
        "sentence_ids": [row["sentence_id"] for row in paragraph],
    } for paragraph in paragraphs]
    sentence_map_out = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": "section-writer-v1",
        "draft_id": draft_id,
        "section_id": section_id,
        "paragraphs": paragraph_rows,
        "sentences": flat,
    }
    title = str(draft["section_title"])
    draft_path = draft_root / "section.md"
    map_path = draft_root / "sentence_map.json"
    actions_path = draft_root / "revision_actions.jsonl"
    _atomic_text(draft_path, _markdown(section_id, title, paragraphs))
    _atomic_json(map_path, sentence_map_out)
    _atomic_jsonl(actions_path, actions)
    removed = sum(row["action"] == "REMOVED_EVIDENCE_ISSUE" for row in actions)
    merged = sum(row["action"] == "MERGED_REDUNDANT" for row in actions)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": "section-writer-v1",
        "revision_contract_version": CONTRACT_VERSION,
        "stage": "SECTION_WRITER",
        "status": "DRAFTED_UNAUDITED",
        "reason_code": "POSTWRITING_AUDITS_REQUIRED",
        "draft_id": draft_id,
        "identity": identity,
        "section_id": section_id,
        "section_title": title,
        "readiness": draft.get("readiness"),
        "eligible_question_count": draft["eligible_question_count"],
        "unsupported_question_count": draft["unsupported_question_count"],
        "covered_question_count": len({qid for row in flat for qid in row["question_ids"]}),
        "paragraph_count": len(paragraphs),
        "sentence_count": len(flat),
        "claim_count_used": len({cid for row in flat for cid in row["claim_ids"]}),
        "draft_path": draft_path.relative_to(root).as_posix(),
        "draft_sha256": sha256_file(draft_path),
        "sentence_map_path": map_path.relative_to(root).as_posix(),
        "sentence_map_sha256": sha256_file(map_path),
        "revision_actions_path": actions_path.relative_to(root).as_posix(),
        "revision_actions_sha256": sha256_file(actions_path),
        "parent_draft_id": draft["draft_id"],
        "revision_number": revision_number,
        "source_sentence_count": len(sentence_map["sentences"]),
        "removed_evidence_issue_count": removed,
        "merged_redundant_count": merged,
        "max_editorial_revisions": max_revisions,
    }
    _atomic_json(draft_root / "manifest.json", manifest)
    active_path = root / "book" / "production" / "drafts" / "active" / f"section_{section_id.replace('.', '_')}.json"
    _atomic_json(active_path, manifest)
    report_text = _report(manifest)
    report_stem = f"section_revision_{section_id.replace('.', '_')}"
    _atomic_text(root / "reports" / f"{report_stem}_r{revision_number}.md", report_text)
    _atomic_text(root / "reports" / f"{report_stem}.md", report_text)
    return manifest


__all__ = ["run_revision"]
