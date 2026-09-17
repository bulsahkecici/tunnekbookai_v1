"""Deterministic, canonical-only section evidence packets and claim registries."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from tunnelbookai.canonical.hashing import canonical_sha256, sha256_file

from .errors import BookEngineError
from .inputs import BookInputs, load_book_inputs
from .models import EvidenceClaim
from .retrieval import inspect_index


SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "section-preparation-v1"
SOFTWARE_VERSION = "section-preparation-v1"
ALLOWED_EVIDENCE_STATES = {"SUPPORTED", "PARTIAL", "UNSUPPORTED"}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _section_key(section_id: str) -> tuple[int, ...]:
    return tuple(int(part) for part in section_id.split("."))


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _read_json(path: Path, *, code: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BookEngineError(code, f"cannot read {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise BookEngineError(code, f"{path} root must be an object")
    return payload


def _read_jsonl(path: Path, *, code: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise BookEngineError(code, f"cannot read {path}: {exc}") from exc
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise BookEngineError(code, f"invalid JSON at {path}:{number}: {exc}") from exc
        if not isinstance(row, dict):
            raise BookEngineError(code, f"{path}:{number} must be an object")
        rows.append(row)
    return rows


def _safe_path(root: Path, value: object, *, boundary: Path, code: str) -> Path:
    relative = Path(str(value or ""))
    if not str(value or "").strip() or relative.is_absolute() or ".." in relative.parts:
        raise BookEngineError(code, f"unsafe project-relative path: {value!r}")
    candidate = (root / relative).resolve()
    allowed = boundary.resolve()
    if candidate != allowed and allowed not in candidate.parents:
        raise BookEngineError(code, f"path escapes allowed boundary: {value}")
    return candidate


def _locator_map(row: Mapping[str, Any]) -> dict[tuple[str, str], str]:
    locators: dict[tuple[str, str], str] = {}
    for raw in row.get("source_locators") or []:
        value = str(raw)
        parts = value.split(":", 2)
        if len(parts) != 3 or not all(parts[:2]):
            raise BookEngineError(
                "PREWRITING_AUDIT_INVALID",
                f"invalid source locator for {row.get('question_id')}: {value}",
            )
        key = (parts[0], parts[1])
        if key in locators:
            raise BookEngineError(
                "PREWRITING_AUDIT_INVALID",
                f"duplicate source locator for {row.get('question_id')}: {key}",
            )
        locators[key] = value
    return locators


def _canonical_source(
    root: Path,
    provenance: Mapping[str, Any],
    locator: str,
) -> dict[str, Any]:
    path = _safe_path(
        root,
        provenance.get("canonical_retrieval_path"),
        boundary=root / "corpus" / "canonical",
        code="NON_CANONICAL_EVIDENCE_REJECTED",
    )
    try:
        line_number = int(provenance.get("canonical_line_number"))
    except (TypeError, ValueError) as exc:
        raise BookEngineError("PREWRITING_AUDIT_INVALID", "canonical line number is invalid") from exc
    if line_number < 1 or not path.is_file() or path.is_symlink():
        raise BookEngineError("CANONICAL_EVIDENCE_INVALID", f"canonical source is unavailable: {path}")
    payload: dict[str, Any] | None = None
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if number == line_number:
                try:
                    candidate = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise BookEngineError("CANONICAL_EVIDENCE_INVALID", str(exc)) from exc
                if isinstance(candidate, dict):
                    payload = candidate
                break
    if payload is None:
        raise BookEngineError("CANONICAL_EVIDENCE_INVALID", f"canonical locator is missing: {path}#{line_number}")
    document_id = str(provenance.get("document_id") or "")
    chunk_id = str(provenance.get("chunk_id") or "")
    text = str(payload.get("embedding_text") or "").strip()
    if (
        payload.get("eligible") is not True
        or payload.get("document_id") != document_id
        or payload.get("chunk_id") != chunk_id
        or not text
    ):
        raise BookEngineError(
            "CANONICAL_EVIDENCE_INVALID",
            f"canonical evidence identity changed: {document_id}/{chunk_id}",
        )
    return {
        "document_id": document_id,
        "chunk_id": chunk_id,
        "claim_text": text,
        "locator": locator,
        "canonical_retrieval_path": str(provenance["canonical_retrieval_path"]),
        "canonical_line_number": line_number,
        "canonical_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "chunk_type": str(payload.get("chunk_type") or "UNKNOWN"),
        "source_section_id": payload.get("section_id"),
        "secondary_section_ids": list(payload.get("secondary_section_ids") or []),
        "page_start": payload.get("page_start"),
        "page_end": payload.get("page_end"),
        "slide_number": payload.get("slide_number"),
        "sheet_name": payload.get("sheet_name"),
        "source_kind": str((payload.get("provenance") or {}).get("source_kind") or "UNKNOWN"),
        "evidence_level": str((payload.get("provenance") or {}).get("evidence_level") or "UNKNOWN"),
    }


def _load_active_audit(
    root: Path,
    inputs: BookInputs,
    retrieval_manifest: Mapping[str, Any],
) -> tuple[dict[str, Any], Path, list[dict[str, Any]]]:
    active_path = root / "audit" / "book" / "prewriting_evidence_audit.json"
    audit = _read_json(active_path, code="PREWRITING_AUDIT_INVALID")
    expected = {
        "status": "COMPLETE",
        "question_bank_sha256": inputs.identities["question_bank_sha256"],
        "scope_sha256": inputs.identities["scope_sha256"],
        "canonical_corpus_digest": retrieval_manifest.get("canonical_corpus_digest"),
        "retrieval_index_id": retrieval_manifest.get("index_id"),
        "embedding_model_id": retrieval_manifest.get("model_id"),
    }
    mismatches = {
        key: {"expected": value, "actual": audit.get(key)}
        for key, value in expected.items()
        if audit.get(key) != value
    }
    if mismatches:
        raise BookEngineError(
            "PREWRITING_AUDIT_STALE",
            "completed pre-writing audit does not match the active book inputs/index",
            details=mismatches,
        )
    results_path = _safe_path(
        root,
        audit.get("results_path"),
        boundary=root / "audit" / "book" / "prewriting",
        code="PREWRITING_AUDIT_INVALID",
    )
    rows = _read_jsonl(results_path, code="PREWRITING_AUDIT_INVALID")
    expected_ids = [str(row["question_id"]) for row in inputs.questions]
    actual_ids = [str(row.get("question_id") or "") for row in rows]
    if actual_ids != expected_ids or len(actual_ids) != len(set(actual_ids)):
        raise BookEngineError(
            "PREWRITING_AUDIT_INVALID",
            "question-level audit rows do not exactly match the frozen question bank",
        )
    if any(str(row.get("status") or "") not in ALLOWED_EVIDENCE_STATES for row in rows):
        raise BookEngineError("PREWRITING_AUDIT_INVALID", "audit contains an invalid evidence state")
    return audit, results_path, rows


def _build_section_artifacts(
    *,
    section_id: str,
    section_title: str,
    readiness: str,
    section_rows: Sequence[Mapping[str, Any]],
    identity: Mapping[str, Any],
    source_loader: Callable[[Mapping[str, Any], str], Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    claims: dict[tuple[str, str], dict[str, Any]] = {}
    questions: list[dict[str, Any]] = []
    for row in section_rows:
        question_id = str(row.get("question_id") or "")
        status = str(row.get("status") or "")
        if str(row.get("section_id") or "") != section_id or status not in ALLOWED_EVIDENCE_STATES:
            raise BookEngineError("PREWRITING_AUDIT_INVALID", f"invalid audit row: {question_id}")
        locators = _locator_map(row)
        allowed_claim_ids: list[str] = []
        for provenance in row.get("authority_and_provenance") or []:
            if not isinstance(provenance, Mapping) or provenance.get("selected_by_qwen") is not True:
                continue
            key = (str(provenance.get("document_id") or ""), str(provenance.get("chunk_id") or ""))
            locator = locators.get(key)
            if not locator:
                raise BookEngineError(
                    "PREWRITING_AUDIT_INVALID",
                    f"selected evidence has no locator: {question_id}/{key}",
                )
            source = dict(source_loader(provenance, locator))
            claim_id = "CLM_" + canonical_sha256({
                "section_id": section_id,
                "document_id": key[0],
                "chunk_id": key[1],
                "canonical_text_sha256": source["canonical_text_sha256"],
            })
            allowed_claim_ids.append(claim_id)
            if key not in claims:
                limitations = ["VERBATIM_CANONICAL_PASSAGE_NOT_A_LICENSE_TO_GENERALIZE"]
                if source["chunk_type"] != "TEXT_CHUNK":
                    limitations.append(f"SOURCE_CHUNK_TYPE_{source['chunk_type']}")
                claims[key] = {
                    "claim_id": claim_id,
                    "claim_text": source.pop("claim_text"),
                    "document_id": key[0],
                    "chunk_id": key[1],
                    "locator": locator,
                    "section_id": section_id,
                    "evidence_strength": status,
                    "authority_class": f"{source['source_kind']}:{source['evidence_level']}",
                    "provenance_status": "VERIFIED_CANONICAL",
                    "qualifiers": [],
                    "conditions": [],
                    "limitations": limitations,
                    "supporting_question_ids": [question_id],
                    "question_evidence_states": {question_id: status},
                    **source,
                }
            else:
                claim = claims[key]
                claim["supporting_question_ids"].append(question_id)
                claim["question_evidence_states"][question_id] = status
                if status == "SUPPORTED":
                    claim["evidence_strength"] = "SUPPORTED"
        allowed_claim_ids = list(dict.fromkeys(allowed_claim_ids))
        if status == "UNSUPPORTED" and allowed_claim_ids:
            raise BookEngineError(
                "PREWRITING_AUDIT_INVALID",
                f"unsupported question unexpectedly selects evidence: {question_id}",
            )
        if status != "UNSUPPORTED" and not allowed_claim_ids:
            raise BookEngineError(
                "PREWRITING_AUDIT_INVALID",
                f"{status} question has no selected evidence: {question_id}",
            )
        questions.append({
            "question_id": question_id,
            "question": str(row.get("question") or ""),
            "evidence_status": status,
            "reason_code": str(row.get("reason_code") or ""),
            "confidence": row.get("confidence"),
            "allowed_claim_ids": allowed_claim_ids,
            "drafting_permission": (
                "DIRECT_WITH_CITATION" if status == "SUPPORTED"
                else "LIMITED_WITH_QUALIFIER" if status == "PARTIAL"
                else "NO_FACTUAL_ANSWER"
            ),
        })
    ordered_claims = sorted(claims.values(), key=lambda row: row["claim_id"])
    for claim in ordered_claims:
        claim["supporting_question_ids"] = sorted(set(claim["supporting_question_ids"]))
        if "PARTIAL" in claim["question_evidence_states"].values():
            claim["limitations"].append("PARTIAL_FOR_ONE_OR_MORE_LINKED_QUESTIONS")
        EvidenceClaim.from_mapping(claim)
    registry_core = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "section_id": section_id,
        "section_title": section_title,
        "identity": dict(identity),
        "claim_count": len(ordered_claims),
        "claims": ordered_claims,
    }
    registry_id = "SCR_" + canonical_sha256(registry_core)
    registry = {**registry_core, "registry_id": registry_id}
    counts = Counter(str(row["evidence_status"]) for row in questions)
    packet_core = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "section_id": section_id,
        "section_title": section_title,
        "readiness": readiness,
        "identity": dict(identity),
        "claim_registry_id": registry_id,
        "claim_registry_file": "claim_registry.json",
        "question_count": len(questions),
        "evidence_counts": {state: counts[state] for state in sorted(ALLOWED_EVIDENCE_STATES)},
        "questions": questions,
        "writer_constraints": {
            "allowed_claim_ids": [row["claim_id"] for row in ordered_claims],
            "unsupported_question_ids": [
                row["question_id"] for row in questions if row["evidence_status"] == "UNSUPPORTED"
            ],
            "partial_question_ids": [
                row["question_id"] for row in questions if row["evidence_status"] == "PARTIAL"
            ],
            "unregistered_factual_claims_allowed": False,
            "noncanonical_sources_allowed": False,
            "project_findings_may_be_invented": False,
            "sentence_evidence_map_required": True,
        },
    }
    packet_id = "SEP_" + canonical_sha256(packet_core)
    packet = {**packet_core, "packet_id": packet_id}
    return packet, registry


def _write_report(path: Path, manifest: Mapping[str, Any]) -> None:
    totals = manifest.get("evidence_counts") or {}
    lines = [
        "# Bölüm kanıt paketleri ve iddia kayıtları",
        "",
        f"- Durum: **{manifest['status']}**",
        f"- Hazırlanan bölüm: **{manifest['sections_prepared']} / {manifest['section_count']}**",
        f"- Kayıtlı canonical pasaj/iddia: **{manifest['claim_count']}**",
        f"- SUPPORTED soru: **{totals.get('SUPPORTED', 0)}**",
        f"- PARTIAL soru: **{totals.get('PARTIAL', 0)}**",
        f"- UNSUPPORTED soru: **{totals.get('UNSUPPORTED', 0)}**",
        "",
        "| Bölüm | Hazırlık | İddia/pasaj | Destekli | Kısmi | Desteksiz |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in manifest.get("sections") or []:
        counts = row["evidence_counts"]
        lines.append(
            f"| {row['section_id']} | {row['readiness']} | {row['claim_count']} | "
            f"{counts['SUPPORTED']} | {counts['PARTIAL']} | {counts['UNSUPPORTED']} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def prepare_sections(
    project_root: Path | str | None = None,
    *,
    section_ids: Sequence[str] | None = None,
    progress: Any = None,
) -> dict[str, Any]:
    """Build immutable, content-addressed preparation artifacts for requested sections."""

    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    inputs = load_book_inputs(root)
    retrieval = inspect_index(root)
    if not retrieval.ready or not retrieval.manifest:
        raise BookEngineError("RETRIEVAL_INDEX_NOT_READY", retrieval.reason)
    audit, results_path, rows = _load_active_audit(root, inputs, retrieval.manifest)
    all_sections = sorted(inputs.question_section_ids, key=_section_key)
    requested = list(section_ids or all_sections)
    if len(requested) != len(set(requested)) or any(value not in inputs.questions_by_section for value in requested):
        raise BookEngineError("UNKNOWN_SECTION", "section preparation selection is invalid")
    rows_by_section = {
        section_id: [row for row in rows if row.get("section_id") == section_id]
        for section_id in all_sections
    }
    for section_id in all_sections:
        expected_ids = [str(row["question_id"]) for row in inputs.questions_by_section[section_id]]
        actual_ids = [str(row.get("question_id") or "") for row in rows_by_section[section_id]]
        if actual_ids != expected_ids:
            raise BookEngineError(
                "PREWRITING_AUDIT_INVALID",
                f"audit question order/count differs for section {section_id}",
            )
    summary_by_section = {str(row["section_id"]): row for row in audit.get("sections") or []}
    identity = {
        "scope_sha256": inputs.identities["scope_sha256"],
        "question_bank_sha256": inputs.identities["question_bank_sha256"],
        "canonical_corpus_digest": retrieval.manifest["canonical_corpus_digest"],
        "retrieval_index_id": retrieval.manifest["index_id"],
        "prewriting_audit_id": audit["audit_id"],
        "prewriting_results_sha256": sha256_file(results_path),
        "embedding_model_id": audit["embedding_model_id"],
        "llm_model_id": audit["llm_model_id"],
        "model_configuration": audit["model_configuration"],
        "software_version": SOFTWARE_VERSION,
    }
    manifest_id = "SPM_" + canonical_sha256(identity)
    output_root = root / "book" / "production" / "preparation"
    packets_root = output_root / "packets"
    active_path = output_root / "manifest.json"
    existing_sections: dict[str, dict[str, Any]] = {}
    if active_path.is_file():
        existing = _read_json(active_path, code="SECTION_PREPARATION_INVALID")
        if existing.get("manifest_id") == manifest_id and existing.get("identity") == identity:
            existing_sections = {
                str(row.get("section_id")): row
                for row in existing.get("sections") or []
                if isinstance(row, dict)
            }
    for section_id in requested:
        section_summary = summary_by_section.get(section_id)
        if not isinstance(section_summary, Mapping):
            raise BookEngineError("PREWRITING_AUDIT_INVALID", f"missing section summary: {section_id}")
        packet, registry = _build_section_artifacts(
            section_id=section_id,
            section_title=str(inputs.scope_by_id[section_id]["title"]),
            readiness=str(section_summary.get("readiness") or "EVIDENCE_GAP"),
            section_rows=rows_by_section[section_id],
            identity=identity,
            source_loader=lambda provenance, locator: _canonical_source(root, provenance, locator),
        )
        packet_dir = packets_root / packet["packet_id"]
        packet_path = packet_dir / "evidence_packet.json"
        registry_path = packet_dir / "claim_registry.json"
        _atomic_json(registry_path, registry)
        _atomic_json(packet_path, packet)
        existing_sections[section_id] = {
            "section_id": section_id,
            "section_title": packet["section_title"],
            "readiness": packet["readiness"],
            "packet_id": packet["packet_id"],
            "packet_path": packet_path.relative_to(root).as_posix(),
            "packet_sha256": sha256_file(packet_path),
            "claim_registry_id": registry["registry_id"],
            "claim_registry_path": registry_path.relative_to(root).as_posix(),
            "claim_registry_sha256": sha256_file(registry_path),
            "claim_count": registry["claim_count"],
            "question_count": packet["question_count"],
            "evidence_counts": packet["evidence_counts"],
        }
        if progress:
            progress({
                "manifest_id": manifest_id,
                "section_id": section_id,
                "sections_prepared": len(existing_sections),
                "section_count": len(all_sections),
                "claim_count": registry["claim_count"],
            })
    ordered = [existing_sections[key] for key in all_sections if key in existing_sections]
    evidence_counts = Counter()
    for row in ordered:
        evidence_counts.update(row["evidence_counts"])
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "manifest_id": manifest_id,
        "identity": identity,
        "status": "COMPLETE" if len(ordered) == len(all_sections) else "IN_PROGRESS",
        "updated_at": _now(),
        "section_count": len(all_sections),
        "sections_prepared": len(ordered),
        "question_count": sum(int(row["question_count"]) for row in ordered),
        "claim_count": sum(int(row["claim_count"]) for row in ordered),
        "evidence_counts": {state: evidence_counts[state] for state in sorted(ALLOWED_EVIDENCE_STATES)},
        "sections": ordered,
    }
    _atomic_json(active_path, manifest)
    _write_report(root / "reports" / "section_preparation.md", manifest)
    return manifest


def inspect_preparation(
    project_root: Path | str | None = None,
    *,
    inputs: BookInputs | None = None,
) -> dict[str, Any] | None:
    """Return a valid active preparation manifest, otherwise no prepared state."""

    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    active_path = root / "book" / "production" / "preparation" / "manifest.json"
    if not active_path.is_file():
        return None
    try:
        loaded_inputs = inputs or load_book_inputs(root)
        retrieval = inspect_index(root)
        if not retrieval.ready or not retrieval.manifest:
            return None
        audit, results_path, _ = _load_active_audit(root, loaded_inputs, retrieval.manifest)
        manifest = _read_json(active_path, code="SECTION_PREPARATION_INVALID")
        identity = manifest.get("identity") or {}
        if (
            identity.get("scope_sha256") != loaded_inputs.identities["scope_sha256"]
            or identity.get("question_bank_sha256") != loaded_inputs.identities["question_bank_sha256"]
            or identity.get("canonical_corpus_digest") != retrieval.manifest["canonical_corpus_digest"]
            or identity.get("retrieval_index_id") != retrieval.manifest["index_id"]
            or identity.get("prewriting_audit_id") != audit["audit_id"]
            or identity.get("prewriting_results_sha256") != sha256_file(results_path)
        ):
            return None
        for row in manifest.get("sections") or []:
            packet = _safe_path(root, row.get("packet_path"), boundary=root / "book" / "production", code="SECTION_PREPARATION_INVALID")
            registry = _safe_path(root, row.get("claim_registry_path"), boundary=root / "book" / "production", code="SECTION_PREPARATION_INVALID")
            if sha256_file(packet) != row.get("packet_sha256") or sha256_file(registry) != row.get("claim_registry_sha256"):
                return None
        return manifest
    except (BookEngineError, OSError, KeyError, TypeError, ValueError):
        return None


__all__ = ["inspect_preparation", "prepare_sections"]
