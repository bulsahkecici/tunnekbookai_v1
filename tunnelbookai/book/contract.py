"""Single parser and validator for the canonical Book Contract."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse

import yaml

from .errors import ContractValidationError
from .models import (
    AnalysisArtifactStatus,
    EvidenceType,
    FreezeStatus,
    QuestionCoverageStatus,
    QuestionEvidenceStatus,
    SectionReadinessStatus,
    StatementEvidenceStatus,
)


DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONTRACT_PATH = Path("book/config/book_contract.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_project_path(project_root: Path, value: Any, *, field: str) -> Path:
    relative = Path(str(value or ""))
    if not str(value or "").strip() or relative.is_absolute():
        raise ContractValidationError(f"{field} must be a project-relative path")
    root = project_root.resolve()
    resolved = (root / relative).resolve()
    if resolved != root and root not in resolved.parents:
        raise ContractValidationError(f"{field} escapes the project root")
    return resolved


def _mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ContractValidationError(f"{key} must be an object")
    return value


def _positive_int(mapping: Mapping[str, Any], key: str) -> int:
    value = mapping.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ContractValidationError(f"{key} must be a positive integer")
    return value


def _ratio(mapping: Mapping[str, Any], key: str) -> float:
    value = mapping.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 < float(value) <= 1:
        raise ContractValidationError(f"{key} must be a ratio in (0, 1]")
    return float(value)


def _enum_values(enum_type: type, values: Any, *, field: str) -> set[str]:
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise ContractValidationError(f"{field} must be a string array")
    expected = {item.value for item in enum_type}
    actual = set(values)
    if actual != expected or len(values) != len(actual):
        raise ContractValidationError(
            f"{field} must contain each allowed state exactly once",
            details={"expected": sorted(expected), "actual": values},
        )
    return actual


def _require_true(mapping: Mapping[str, Any], keys: tuple[str, ...], *, prefix: str) -> None:
    for key in keys:
        if mapping.get(key) is not True:
            raise ContractValidationError(f"{prefix}.{key} must be true")


@dataclass(frozen=True)
class BookContract:
    project_root: Path
    path: Path
    payload: Mapping[str, Any]
    contract_sha256: str

    @property
    def expected_structure(self) -> Mapping[str, Any]:
        return _mapping(self.payload, "expected_structure")

    @property
    def coverage_policy(self) -> Mapping[str, Any]:
        return _mapping(self.payload, "coverage_policy")

    @property
    def authorities(self) -> Mapping[str, Any]:
        return _mapping(self.payload, "authorities")

    def authority_path(self, name: str) -> Path:
        entry = _mapping(self.authorities, name)
        return resolve_project_path(self.project_root, entry.get("path"), field=f"authorities.{name}.path")


def validate_contract_payload(
    payload: Mapping[str, Any], *, project_root: Path, contract_path: Path
) -> None:
    if payload.get("schema_version") != "1.0":
        raise ContractValidationError("unsupported Book Contract schema_version")
    if not str(payload.get("contract_version") or "").strip():
        raise ContractValidationError("contract_version is required")

    authorities = _mapping(payload, "authorities")
    required_authorities = {
        "scope", "question_bank", "question_bank_index", "question_bank_integrity",
        "source_manifest",
    }
    if set(authorities) != required_authorities:
        raise ContractValidationError(
            "authorities must contain the exact frozen book inputs",
            details={"expected": sorted(required_authorities), "actual": sorted(authorities)},
        )
    for name in sorted(required_authorities):
        entry = _mapping(authorities, name)
        path = resolve_project_path(project_root, entry.get("path"), field=f"authorities.{name}.path")
        digest = str(entry.get("sha256") or "")
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise ContractValidationError(f"authorities.{name}.sha256 is invalid")
        if path == contract_path.resolve():
            raise ContractValidationError("the Book Contract cannot identify itself as an authority")

    structure = _mapping(payload, "expected_structure")
    chapters = _positive_int(structure, "top_level_chapters")
    headings = _positive_int(structure, "structural_headings")
    sections = _positive_int(structure, "question_bank_sections")
    per_section = _positive_int(structure, "questions_per_section")
    total = _positive_int(structure, "total_questions")
    if chapters != 7 or headings != 66 or sections != 59 or per_section != 50 or total != 2950:
        raise ContractValidationError("frozen structural counts may not be changed")
    if sections * per_section != total:
        raise ContractValidationError("question count is inconsistent with per-section policy")

    coverage = _mapping(payload, "coverage_policy")
    _enum_values(QuestionCoverageStatus, coverage.get("allowed_states"), field="coverage_policy.allowed_states")
    if coverage.get("counted_as_answered") != [QuestionCoverageStatus.ANSWERED.value]:
        raise ContractValidationError("only ANSWERED may count toward coverage")
    global_policy = _mapping(coverage, "global")
    minimum_count = _positive_int(global_policy, "minimum_answered_count")
    minimum_coverage = _ratio(global_policy, "minimum_coverage")
    if global_policy.get("hard_gate") is not True or global_policy.get("requires_complete_audit") is not True:
        raise ContractValidationError("global coverage and complete-audit rules must be hard gates")
    if minimum_count != 1770 or minimum_coverage != 0.6:
        raise ContractValidationError("global publication threshold must remain 1770 / 60%")
    if minimum_count != math.ceil(total * minimum_coverage):
        raise ContractValidationError("minimum answered count and coverage ratio disagree")
    section_policy = _mapping(coverage, "section")
    if section_policy.get("hard_gate") is not False:
        raise ContractValidationError("section coverage is a preferred target in V1 foundation")
    if _positive_int(section_policy, "preferred_minimum_answered_count") != 30:
        raise ContractValidationError("preferred section target must remain 30 questions")
    if _ratio(section_policy, "preferred_minimum_coverage") != 0.6:
        raise ContractValidationError("preferred section coverage must remain 60%")

    evidence = _mapping(payload, "evidence_policy")
    _enum_values(QuestionEvidenceStatus, evidence.get("prewriting_states"), field="evidence_policy.prewriting_states")
    _enum_values(
        StatementEvidenceStatus,
        evidence.get("postwriting_statement_states"),
        field="evidence_policy.postwriting_statement_states",
    )
    if evidence.get("allowed_source_roots") != ["corpus/canonical"]:
        raise ContractValidationError("canonical corpus must be the only book evidence root")
    _require_true(
        evidence,
        (
            "require_claim_registry", "require_document_identity", "require_source_locator",
            "require_provenance", "no_hallucinated_facts", "no_hallucinated_headings",
        ),
        prefix="evidence_policy",
    )
    disallowed = set(evidence.get("disallowed_source_roots") or [])
    if not {"incoming", "processing", "corpus/staging", "archive", "internet"}.issubset(disallowed):
        raise ContractValidationError("evidence policy must explicitly reject every non-canonical source")
    if evidence.get("external_evidence_admission") != "UNIFIED_INGEST_THEN_CONTROLLED_CANONICAL_PROMOTION":
        raise ContractValidationError("external evidence must pass ingest and controlled promotion")
    resolve_project_path(project_root, evidence.get("canonical_root"), field="evidence_policy.canonical_root")
    resolve_project_path(project_root, evidence.get("canonical_manifest"), field="evidence_policy.canonical_manifest")

    citation = _mapping(payload, "citation_policy")
    _require_true(
        citation,
        (
            "answer_requires_span", "answered_requires_claim_ids",
            "answered_requires_document_ids", "answered_requires_source_locators",
            "technical_sentences_require_evidence_audit",
        ),
        prefix="citation_policy",
    )

    model = _mapping(payload, "model_policy")
    model_path = resolve_project_path(project_root, model.get("authority_path"), field="model_policy.authority_path")
    expected_model_hash = str(model.get("authority_sha256") or "")
    if not model_path.is_file() or sha256_file(model_path) != expected_model_hash:
        raise ContractValidationError("model authority is missing or its hash changed")
    if model.get("provider") != "local" or model.get("loopback_only") is not True:
        raise ContractValidationError("book models must be local and loopback-only")
    if model.get("allow_cloud_fallback") is not False or model.get("allow_model_substitution") is not False:
        raise ContractValidationError("model fallback and substitution must remain disabled")
    models = yaml.safe_load(model_path.read_text(encoding="utf-8")) or {}
    for capability in ("embedding", "llm"):
        settings = models.get(capability) or {}
        endpoint = urlparse(str(settings.get("default_endpoint") or ""))
        if settings.get("provider") != "local" or not str(settings.get("model") or "").strip():
            raise ContractValidationError(f"models.yaml {capability} requires an exact local model")
        if endpoint.scheme not in {"http", "https"} or endpoint.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise ContractValidationError(f"models.yaml {capability} endpoint must be loopback")

    analysis = _mapping(payload, "analysis_artifact_policy")
    _enum_values(EvidenceType, analysis.get("evidence_types"), field="analysis_artifact_policy.evidence_types")
    _enum_values(AnalysisArtifactStatus, analysis.get("states"), field="analysis_artifact_policy.states")
    if analysis.get("missing_required_state") != "HUMAN_ANALYSIS_ARTIFACT_REQUIRED":
        raise ContractValidationError("missing analysis artifacts must block section readiness")
    if analysis.get("allow_model_to_invent_project_findings") is not False:
        raise ContractValidationError("models may not invent project-analysis findings")

    section = _mapping(payload, "section_policy")
    _enum_values(SectionReadinessStatus, section.get("readiness_states"), field="section_policy.readiness_states")
    _enum_values(FreezeStatus, section.get("freeze_states"), field="section_policy.freeze_states")
    if section.get("max_editorial_revisions") != 2:
        raise ContractValidationError("max editorial revisions must be 2 in this contract")
    if not isinstance(section.get("freeze_requirements"), list) or not section.get("freeze_requirements"):
        raise ContractValidationError("freeze requirements may not be empty")
    if section.get("revision_requires_reaudit") is not True or section.get("rollback_requires_hash_verification") is not True:
        raise ContractValidationError("revision re-audit and hash-verified rollback are required")

    artifact = _mapping(payload, "artifact_policy")
    _require_true(
        artifact,
        ("retrieval_index_is_derivative", "manifest_driven", "atomic_writes_required"),
        prefix="artifact_policy",
    )
    required_identity_fields = {
        "scope_sha256", "question_bank_sha256", "canonical_corpus_digest", "model_id",
        "model_configuration", "prompt_version", "software_version",
    }
    if set(artifact.get("identity_fields") or []) != required_identity_fields:
        raise ContractValidationError("artifact identity requirements are incomplete")

    publication = _mapping(payload, "publication_policy")
    if publication.get("required_structural_headings") != headings:
        raise ContractValidationError("publication structural count disagrees with scope")
    if publication.get("required_question_sections") != sections:
        raise ContractValidationError("publication question-section count disagrees with scope")
    if publication.get("required_question_audits") != total:
        raise ContractValidationError("publication question audit count disagrees with scope")
    _require_true(
        publication,
        (
            "requires_all_sections_frozen", "requires_global_coverage_gate",
            "requires_cross_chapter_consistency_pass", "requires_valid_book_manifest",
            "requires_reproducible_assembly",
        ),
        prefix="publication_policy",
    )
    if publication.get("failure_status") != "COVERAGE_REMEDIATION_REQUIRED":
        raise ContractValidationError("failed publication coverage must require remediation")


def load_book_contract(
    project_root: Path = DEFAULT_PROJECT_ROOT,
    contract_path: Path | str = DEFAULT_CONTRACT_PATH,
) -> BookContract:
    root = Path(project_root).resolve()
    path = Path(contract_path)
    if not path.is_absolute():
        path = resolve_project_path(root, path, field="contract_path")
    if not path.is_file():
        raise ContractValidationError(f"Book Contract does not exist: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractValidationError(f"cannot read Book Contract: {exc}") from exc
    if not isinstance(payload, Mapping):
        raise ContractValidationError("Book Contract root must be an object")
    validate_contract_payload(payload, project_root=root, contract_path=path)
    return BookContract(root, path, payload, sha256_file(path))
