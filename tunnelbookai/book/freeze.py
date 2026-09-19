"""Hash-verified, write-once section freeze snapshots."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from tunnelbookai.canonical.hashing import canonical_sha256, sha256_file

from .coverage_audit import inspect_coverage_audits
from .editorial import inspect_editorial_audits
from .errors import BookEngineError
from .evidence_review import inspect_evidence_reviews
from .inputs import load_book_inputs
from .preparation import inspect_preparation
from .writer import inspect_drafts


SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "section-freeze-v1"
SOFTWARE_VERSION = "section-freeze-v1"


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


def _atomic_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as handle:
        handle.write(value)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _atomic_text(path: Path, value: str) -> None:
    _atomic_bytes(path, value.encode("utf-8"))


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


def _citation_integrity(
    sentence_map: Mapping[str, Any],
    evidence_rows: Sequence[Mapping[str, Any]],
    registry: Mapping[str, Any],
) -> dict[str, Any]:
    sentences = {str(row["sentence_id"]): row for row in sentence_map.get("sentences") or []}
    reviews = {str(row["sentence_id"]): row for row in evidence_rows}
    claims = {str(row["claim_id"]): row for row in registry.get("claims") or []}
    errors: list[str] = []
    if set(sentences) != set(reviews):
        errors.append("SENTENCE_REVIEW_COVERAGE_MISMATCH")
    for sentence_id, sentence in sentences.items():
        review = reviews.get(sentence_id)
        if not review:
            continue
        status = str(review.get("status") or "")
        mapped = set(str(value) for value in sentence.get("claim_ids") or [])
        supporting = [str(value) for value in review.get("supporting_claim_ids") or []]
        if not mapped or not mapped <= set(claims):
            errors.append(f"UNKNOWN_MAPPED_CLAIM:{sentence_id}")
            continue
        if status == "SUPPORTED" and not supporting:
            errors.append(f"SUPPORTED_WITHOUT_CLAIM:{sentence_id}")
        if status not in {"SUPPORTED", "NON_FACTUAL_OR_EDITORIAL"}:
            errors.append(f"MATERIAL_EVIDENCE_STATE:{sentence_id}:{status}")
        if not set(supporting) <= mapped:
            errors.append(f"SUPPORT_NOT_MAPPED:{sentence_id}")
        selected = [claims[value] for value in supporting if value in claims]
        expected_documents = list(dict.fromkeys(str(row["document_id"]) for row in selected))
        expected_locators = list(dict.fromkeys(str(row["locator"]) for row in selected))
        if list(review.get("supporting_document_ids") or []) != expected_documents:
            errors.append(f"DOCUMENT_PROVENANCE_MISMATCH:{sentence_id}")
        if list(review.get("source_locators") or []) != expected_locators:
            errors.append(f"LOCATOR_PROVENANCE_MISMATCH:{sentence_id}")
    return {
        "decision": "PASS" if not errors else "HOLD",
        "sentence_count": len(sentences), "claim_count": len(claims), "errors": errors,
    }


def _freeze_checks(
    *,
    section_id: str,
    evidence: Mapping[str, Any],
    coverage: Mapping[str, Any],
    editorial: Mapping[str, Any],
    citation: Mapping[str, Any],
    required_analysis_artifacts: Sequence[Mapping[str, Any]],
) -> dict[str, str]:
    analysis_ok = all(str(row.get("status") or "") == "VERIFIED" for row in required_analysis_artifacts)
    checks = {
        "SCOPE_VALIDATION_PASS": "PASS" if section_id else "HOLD",
        "EVIDENCE_AUDIT_PASS": "PASS" if evidence.get("audit_decision") == "PASS" else "HOLD",
        "NO_MATERIAL_UNSUPPORTED_TECHNICAL_CLAIMS": "PASS" if int(evidence.get("material_issue_count") or 0) == 0 else "HOLD",
        "QUESTION_COVERAGE_AUDIT_COMPLETE": "PASS" if coverage.get("status") == "COMPLETE" and int(coverage.get("question_count") or 0) == 50 else "HOLD",
        "EDITORIAL_AUDIT_PASS": "PASS" if editorial.get("audit_decision") == "PASS" else "HOLD",
        "CITATION_PROVENANCE_INTEGRITY_PASS": "PASS" if citation.get("decision") == "PASS" else "HOLD",
        "REQUIRED_ANALYSIS_ARTIFACTS_SATISFIED": "PASS" if analysis_ok else "HOLD",
    }
    return checks


def is_section_frozen(project_root: Path | str, section_id: str) -> bool:
    root = Path(project_root).resolve()
    pointer = root / "book" / "production" / "frozen" / "active" / f"section_{section_id.replace('.', '_')}.json"
    if not pointer.is_file():
        return False
    try:
        manifest = _read_json(pointer, "SECTION_FREEZE_INVALID")
        manifest_path = root / str(manifest["manifest_path"])
        return (
            manifest.get("status") == "FROZEN"
            and manifest.get("section_id") == section_id
            and manifest_path.is_file()
            and sha256_file(manifest_path) == manifest.get("manifest_sha256")
        )
    except (BookEngineError, OSError, KeyError, TypeError, ValueError):
        return False


def _copy_artifact(root: Path, freeze_root: Path, name: str, source_rel: str) -> dict[str, Any]:
    source = (root / source_rel).resolve()
    if root not in source.parents or not source.is_file() or source.is_symlink():
        raise BookEngineError("SECTION_FREEZE_INPUT_INVALID", f"invalid freeze source: {source_rel}")
    target = freeze_root / "artifacts" / name
    content = source.read_bytes()
    if target.exists() and target.read_bytes() != content:
        raise BookEngineError("SECTION_FREEZE_IMMUTABILITY_FAILED", f"frozen artifact differs: {target}")
    if not target.exists():
        _atomic_bytes(target, content)
        target.chmod(0o444)
    return {
        "name": name, "source_path": source.relative_to(root).as_posix(),
        "frozen_path": target.relative_to(root).as_posix(), "size": len(content),
        "sha256": sha256_file(target),
    }


def run_freeze(section_id: str, project_root: Path | str | None = None) -> dict[str, Any]:
    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    inputs = load_book_inputs(root)
    preparation = inspect_preparation(root, inputs=inputs)
    drafts = inspect_drafts(root, preparation=preparation)
    evidence_reviews = inspect_evidence_reviews(root, drafts=drafts)
    coverage_audits = inspect_coverage_audits(root, evidence_reviews=evidence_reviews)
    editorial_audits = inspect_editorial_audits(root, coverage_audits=coverage_audits)
    draft = next((row for row in drafts if row["section_id"] == section_id), None)
    evidence = next((row for row in evidence_reviews if row["section_id"] == section_id), None)
    coverage = next((row for row in coverage_audits if row["section_id"] == section_id), None)
    editorial = next((row for row in editorial_audits if row["section_id"] == section_id), None)
    if not all((draft, evidence, coverage, editorial)):
        raise BookEngineError("SECTION_FREEZE_PREREQUISITE_MISSING", f"complete active artifacts required for {section_id}")
    prep_entry = next((row for row in preparation["sections"] if row["section_id"] == section_id), None)
    if not prep_entry:
        raise BookEngineError("SECTION_FREEZE_PREREQUISITE_MISSING", f"prepared packet missing for {section_id}")
    sentence_map = _read_json(root / str(draft["sentence_map_path"]), "SECTION_FREEZE_INPUT_INVALID")
    evidence_rows = _read_jsonl(root / str(evidence["results_path"]), "SECTION_FREEZE_INPUT_INVALID")
    registry = _read_json(root / str(prep_entry["claim_registry_path"]), "SECTION_FREEZE_INPUT_INVALID")
    packet = _read_json(root / str(prep_entry["packet_path"]), "SECTION_FREEZE_INPUT_INVALID")
    citation = _citation_integrity(sentence_map, evidence_rows, registry)
    required_analysis = list(packet.get("required_analysis_artifacts") or [])
    checks = _freeze_checks(
        section_id=section_id, evidence=evidence, coverage=coverage, editorial=editorial,
        citation=citation, required_analysis_artifacts=required_analysis,
    )
    contract_requirements = list(inputs.contract.payload["section_policy"]["freeze_requirements"])
    if set(checks) != set(contract_requirements) or any(value != "PASS" for value in checks.values()):
        raise BookEngineError("SECTION_FREEZE_BLOCKED", f"freeze gates did not pass for {section_id}", details=checks)
    identity = {
        "section_id": section_id, "draft_id": draft["draft_id"], "draft_sha256": draft["draft_sha256"],
        "sentence_map_sha256": draft["sentence_map_sha256"],
        "evidence_review_id": evidence["audit_id"], "evidence_review_sha256": evidence["results_sha256"],
        "coverage_audit_id": coverage["audit_id"], "coverage_results_sha256": coverage["results_sha256"],
        "editorial_audit_id": editorial["audit_id"], "editorial_result_sha256": editorial["result_sha256"],
        "claim_registry_id": prep_entry["claim_registry_id"], "claim_registry_sha256": prep_entry["claim_registry_sha256"],
        "book_contract_sha256": inputs.identities["book_contract_sha256"],
        "software_version": SOFTWARE_VERSION,
    }
    freeze_id = "FRZ_" + canonical_sha256(identity)
    freeze_root = root / "book" / "production" / "frozen" / freeze_id
    manifest_path = freeze_root / "manifest.json"
    pointer_path = root / "book" / "production" / "frozen" / "active" / f"section_{section_id.replace('.', '_')}.json"
    if manifest_path.is_file():
        manifest = _read_json(manifest_path, "SECTION_FREEZE_INVALID")
        if manifest.get("freeze_id") != freeze_id:
            raise BookEngineError("SECTION_FREEZE_IMMUTABILITY_FAILED", "existing freeze identity differs")
    else:
        artifacts = [
            _copy_artifact(root, freeze_root, "section.md", str(draft["draft_path"])),
            _copy_artifact(root, freeze_root, "sentence_map.json", str(draft["sentence_map_path"])),
            _copy_artifact(root, freeze_root, "evidence_results.jsonl", str(evidence["results_path"])),
            _copy_artifact(root, freeze_root, "coverage_results.jsonl", str(coverage["results_path"])),
            _copy_artifact(root, freeze_root, "editorial_result.json", str(editorial["result_path"])),
            _copy_artifact(root, freeze_root, "claim_registry.json", str(prep_entry["claim_registry_path"])),
            _copy_artifact(root, freeze_root, "evidence_packet.json", str(prep_entry["packet_path"])),
        ]
        manifest = {
            "schema_version": SCHEMA_VERSION, "contract_version": CONTRACT_VERSION,
            "stage": "SECTION_FREEZE", "status": "FROZEN", "freeze_id": freeze_id,
            "identity": identity, "frozen_at": _now(), "section_id": section_id,
            "section_title": draft["section_title"], "freeze_checks": checks,
            "analysis_artifact_state": "NOT_REQUIRED" if not required_analysis else "VERIFIED",
            "analysis_artifact_reason": "NO_REQUIRED_ANALYSIS_ARTIFACT_DECLARED_IN_SECTION_PACKET" if not required_analysis else "ALL_DECLARED_ARTIFACTS_VERIFIED",
            "citation_integrity": citation, "artifacts": artifacts,
            "sentence_count": draft["sentence_count"], "answered": coverage["answered"],
            "coverage": coverage["coverage"], "editorial_model_decision": editorial["model_decision"],
        }
        _atomic_json(manifest_path, manifest)
        manifest_path.chmod(0o444)
    pointer = {
        **manifest,
        "manifest_path": manifest_path.relative_to(root).as_posix(),
        "manifest_sha256": sha256_file(manifest_path),
    }
    _atomic_json(pointer_path, pointer)
    report = "\n".join([
        f"# Bölüm dondurma — {section_id}", "", f"- Durum: **FROZEN**",
        f"- Freeze kimliği: `{freeze_id}`", f"- Draft: `{draft['draft_id']}`",
        f"- Cümle: **{draft['sentence_count']}**", f"- ANSWERED: **{coverage['answered']} / 50**",
        f"- Kapsam: **{float(coverage['coverage']):.0%}**",
        f"- Editoryal model görüşü: **{editorial['model_decision']} (advisory)**", "",
        "Yedi sözleşmeli freeze koşulunun tamamı ve bütün snapshot hashleri doğrulanmıştır.", "",
    ])
    _atomic_text(root / "reports" / f"section_freeze_{section_id.replace('.', '_')}.md", report)
    return pointer


def inspect_freezes(
    project_root: Path | str | None = None,
    *,
    editorial_audits: Sequence[Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    editorials = list(editorial_audits) if editorial_audits is not None else inspect_editorial_audits(root)
    by_section = {str(row["section_id"]): row for row in editorials}
    active = root / "book" / "production" / "frozen" / "active"
    output: list[dict[str, Any]] = []
    if not active.is_dir():
        return output
    for path in sorted(active.glob("section_*.json")):
        try:
            pointer = _read_json(path, "SECTION_FREEZE_INVALID")
            section_id = str(pointer.get("section_id") or "")
            editorial = by_section.get(section_id)
            identity = pointer.get("identity") or {}
            manifest_path = (root / str(pointer["manifest_path"])).resolve()
            boundary = (root / "book" / "production" / "frozen").resolve()
            if (
                not editorial or pointer.get("status") != "FROZEN"
                or identity.get("editorial_audit_id") != editorial.get("audit_id")
                or identity.get("editorial_result_sha256") != editorial.get("result_sha256")
                or boundary not in manifest_path.parents
                or sha256_file(manifest_path) != pointer.get("manifest_sha256")
                or any(sha256_file(root / row["frozen_path"]) != row["sha256"] for row in pointer.get("artifacts") or [])
            ):
                continue
            output.append(pointer)
        except (BookEngineError, OSError, KeyError, TypeError, ValueError):
            continue
    return output


__all__ = ["inspect_freezes", "is_section_frozen", "run_freeze"]
