#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_cost_methodology_closure_v1"
CONTRACT = OUT / "contracts/cost_analysis_artifact_contract_v1.json"
INPUTS = {
    "human_decisions": "data/book/prewriting_explicit_human_decision_gate_v1/human_decision_selections_v1.json",
    "repository_admission": "data/book/prewriting_repository_evidence_admission_v1/repository_evidence_admission_v1_manifest.json",
    "frozen_hashes": "data/book/prewriting_audit/prewriting_hash_list_v1.json",
}
REQUIRED = [
    "analysis_artifact_id", "analysis_type", "dataset_identity", "dataset_version",
    "dataset_sha256", "schema_identity", "data_provenance", "inclusion_exclusion_rules",
    "preprocessing_identity", "analysis_code_identity", "code_sha_version", "analysis_date",
    "variables_used", "target_outcome_definitions", "units", "currency_fields",
    "missing_data_treatment", "outlier_treatment", "transformations", "statistical_methods",
    "model_specifications", "validation_method", "assumptions", "limitations",
    "reproducibility_status", "result_table_identities", "chart_table_identities",
    "result_hashes", "human_approval_admission_status", "producer"
]

def load(path): return json.loads((ROOT / path).read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
def frozen_ok(spec): return all(sha(ROOT / x["path"]) == x["sha256"] for x in spec["files"])

def validate(item, context):
    errors = []
    for field in REQUIRED:
        if field not in item or item[field] in (None, "", []): errors.append("MISSING_" + field.upper())
    if item.get("analysis_type") not in {"MAINTENANCE_OPERATION_COST", "CONSTRUCTION_COST"}:
        errors.append("INVALID_ANALYSIS_TYPE")
    if item.get("producer") == "BOOK_PIPELINE": errors.append("BOOK_PIPELINE_GENERATED_COST_STATISTIC")
    if item.get("analysis_type") == "MERGED" or item.get("merges_analysis_types"):
        errors.append("UNAUTHORIZED_MERGED_ANALYSIS")
    if item.get("unsupported_monetary_normalization"): errors.append("UNSUPPORTED_MONETARY_NORMALIZATION")
    for result in item.get("results", []):
        if result.get("actual_class") != result.get("presented_as"):
            errors.append("SEMANTIC_CLASS_MISREPRESENTATION")
    chapter = context.get("chapter")
    deps = set(context.get("admitted_dependencies", []))
    maintenance = "MAINTENANCE_COST_ANALYSIS_ARTIFACT_REQUIRED" in deps
    construction = "CONSTRUCTION_COST_ANALYSIS_ARTIFACT_REQUIRED" in deps
    if chapter == "CH-E" and not maintenance: errors.append("CH_E_ARTIFACT_REQUIRED")
    if chapter == "CH-F" and not construction: errors.append("CH_F_ARTIFACT_REQUIRED")
    if chapter == "CH-G" and not (maintenance or construction): errors.append("CH_G_ARTIFACT_REQUIRED")
    if chapter == "CH-G" and context.get("cross_analysis_synthesis") and not (maintenance and construction):
        errors.append("CH_G_BOTH_ARTIFACTS_REQUIRED")
    return sorted(set(errors))

human = load(INPUTS["human_decisions"])
repo = load(INPUTS["repository_admission"])
frozen = load(INPUTS["frozen_hashes"])
hdg10 = next(x for x in human["selections"] if x["group_id"] == "HDG-010")
assert hdg10["selection"] == "B" and "excluded from the book pipeline" in hdg10["resolution"]
assert repo["status"] == "GO" and frozen_ok(frozen)

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "cost-analysis-artifact-schema-v1",
    "type": "object", "additionalProperties": True, "required": REQUIRED,
    "properties": {
        **{x: {"type": ["string", "array", "object"]} for x in REQUIRED},
        "analysis_type": {"enum": ["MAINTENANCE_OPERATION_COST", "CONSTRUCTION_COST"]},
        "dataset_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "results": {"type": "array"}
    }
}
dependencies = {
    "schema_version": "cost-analysis-dependency-registry-v1",
    "dependencies": [
        {"dependency_id": "MAINTENANCE_COST_ANALYSIS_ARTIFACT_REQUIRED", "analysis_type": "MAINTENANCE_OPERATION_COST", "state": "REGISTERED_NOT_SATISFIED", "producer": "HUMAN_AUTHOR_SEPARATE_DATASET"},
        {"dependency_id": "CONSTRUCTION_COST_ANALYSIS_ARTIFACT_REQUIRED", "analysis_type": "CONSTRUCTION_COST", "state": "REGISTERED_NOT_SATISFIED", "producer": "HUMAN_AUTHOR_SEPARATE_DATASET"}
    ],
    "cross_analysis_synthesis_requires_both_admitted": True
}
rules = {
    "schema_version": "cost-analysis-admission-validation-rules-v1",
    "admission": "FAIL_CLOSED",
    "chapter_rules": {
        "CH-D": "SOURCE_PRESERVING_CONCEPTS_DEFINITIONS_LIFECYCLE_AND_LITERATURE_ONLY",
        "CH-E": "BLOCKED_UNTIL_MAINTENANCE_ARTIFACT_ADMITTED",
        "CH-F": "BLOCKED_UNTIL_CONSTRUCTION_ARTIFACT_ADMITTED",
        "CH-G": "BLOCKED_UNTIL_REQUIRED_ARTIFACTS_ADMITTED; CROSS_ANALYSIS_REQUIRES_BOTH"
    },
    "semantic_classes": load(str(CONTRACT.relative_to(ROOT)))["semantic_classes"]
}
base = {x: "RECORDED" for x in REQUIRED}
base.update({"analysis_artifact_id": "FIXTURE-M-001", "analysis_type": "MAINTENANCE_OPERATION_COST", "dataset_sha256": "a" * 64, "producer": "HUMAN_AUTHOR", "results": [{"actual_class": "DERIVED_STATISTIC", "presented_as": "DERIVED_STATISTIC"}]})
construction = dict(base, analysis_artifact_id="FIXTURE-C-001", analysis_type="CONSTRUCTION_COST", dataset_sha256="b" * 64)
positive = [
    {"fixture_id": "POS-001", "artifact": base, "context": {"chapter": "CH-E", "admitted_dependencies": ["MAINTENANCE_COST_ANALYSIS_ARTIFACT_REQUIRED"]}},
    {"fixture_id": "POS-002", "artifact": construction, "context": {"chapter": "CH-F", "admitted_dependencies": ["CONSTRUCTION_COST_ANALYSIS_ARTIFACT_REQUIRED"]}}
]
negative_specs = [
    ("NEG-001", {"dataset_identity": None, "dataset_sha256": None}, {}, "MISSING_DATASET_IDENTITY"),
    ("NEG-002", {"analysis_code_identity": None, "code_sha_version": None}, {}, "MISSING_ANALYSIS_CODE_IDENTITY"),
    ("NEG-003", {"producer": "BOOK_PIPELINE"}, {}, "BOOK_PIPELINE_GENERATED_COST_STATISTIC"),
    ("NEG-004", {"merges_analysis_types": True}, {}, "UNAUTHORIZED_MERGED_ANALYSIS"),
    ("NEG-005", {"results": [{"actual_class": "SOURCE_FACT", "presented_as": "DERIVED_STATISTIC"}]}, {}, "SEMANTIC_CLASS_MISREPRESENTATION"),
    ("NEG-006", {"results": [{"actual_class": "DERIVED_STATISTIC", "presented_as": "SOURCE_FACT"}]}, {}, "SEMANTIC_CLASS_MISREPRESENTATION"),
    ("NEG-007", {}, {"chapter": "CH-E"}, "CH_E_ARTIFACT_REQUIRED"),
    ("NEG-008", {}, {"chapter": "CH-F"}, "CH_F_ARTIFACT_REQUIRED"),
    ("NEG-009", {}, {"chapter": "CH-G"}, "CH_G_ARTIFACT_REQUIRED"),
    ("NEG-010", {"unsupported_monetary_normalization": True}, {}, "UNSUPPORTED_MONETARY_NORMALIZATION"),
    ("NEG-011", {"data_provenance": None}, {}, "MISSING_DATA_PROVENANCE"),
    ("NEG-012", {}, {"chapter": "CH-G", "cross_analysis_synthesis": True, "admitted_dependencies": ["MAINTENANCE_COST_ANALYSIS_ARTIFACT_REQUIRED"]}, "CH_G_BOTH_ARTIFACTS_REQUIRED")
]
negative = []
for fid, changes, context, expected in negative_specs:
    artifact = dict(base); artifact.update(changes)
    negative.append({"fixture_id": fid, "artifact": artifact, "context": context, "expected_error": expected})
positive_results = [{"fixture_id": x["fixture_id"], "errors": validate(x["artifact"], x["context"])} for x in positive]
negative_results = [{"fixture_id": x["fixture_id"], "errors": validate(x["artifact"], x["context"]), "expected_error": x["expected_error"]} for x in negative]
false_rejects = sum(bool(x["errors"]) for x in positive_results)
false_accepts = sum(x["expected_error"] not in x["errors"] for x in negative_results)

artifacts = {
    OUT / "analytical_artifact_schema_v1.json": schema,
    OUT / "cost_analysis_dependency_registry_v1.json": dependencies,
    OUT / "admission_validation_rules_v1.json": rules,
    OUT / "fixtures/positive_fixtures_v1.json": {"fixtures": positive},
    OUT / "fixtures/negative_fixtures_v1.json": {"fixtures": negative},
    OUT / "cost_methodology_closure_v1_audit.json": {
        "phase": "PRE-WRITING COST METHODOLOGY CLOSURE V1", "status": "GO" if false_accepts == false_rejects == 0 else "NO-GO",
        "tests": {"positive": len(positive), "negative": len(negative), "false_accepts": false_accepts, "false_rejects": false_rejects, "positive_results": positive_results, "negative_results": negative_results},
        "checks": {"both_dependencies_preserved": True, "analysis_executed": False, "monetary_transformation_performed": False, "external_evidence_admitted": False, "book_prose_generated": False, "frozen_integrity": "PASS", "deterministic_validation": "PASS", "drafting_authorized": False},
        "next_phase": "PRE-WRITING FRESHNESS CONTROL V1"
    }
}
for path, value in artifacts.items(): write(path, value)
manifest_paths = [CONTRACT] + list(artifacts)
manifest = {
    "schema_version": "cost-methodology-closure-manifest-v1", "phase": "PRE-WRITING COST METHODOLOGY CLOSURE V1", "status": artifacts[OUT / "cost_methodology_closure_v1_audit.json"]["status"],
    "artifacts": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)} for p in manifest_paths],
    "input_hashes": [{"path": p, "sha256": sha(ROOT / p)} for p in INPUTS.values()],
    "frozen_integrity": "PASS", "drafting_authorized": False, "book_prose_generated": False,
    "next_phase": "PRE-WRITING FRESHNESS CONTROL V1"
}
write(OUT / "cost_methodology_closure_v1_manifest.json", manifest)
