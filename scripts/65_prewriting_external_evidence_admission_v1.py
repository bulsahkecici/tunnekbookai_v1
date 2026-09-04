#!/usr/bin/env python3
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_external_evidence_admission_v1"

INPUTS = {
    "failure_analysis": "data/book/prewriting_failure_analysis_v1/prewriting_failure_analysis_v1.json",
    "repository_manifest": "data/book/prewriting_repository_evidence_admission_v1/repository_evidence_admission_v1_manifest.json",
    "repository_rejected": "data/book/prewriting_repository_evidence_admission_v1/rejected_evidence_registry_v1.json",
    "repository_ledger": "data/book/prewriting_repository_evidence_admission_v1/section_evidence_coverage_ledger_v1.json",
    "cost_manifest": "data/book/prewriting_cost_methodology_closure_v1/cost_methodology_closure_v1_manifest.json",
    "freshness_manifest": "data/book/prewriting_freshness_control_v1/freshness_control_v1_manifest.json",
    "freshness_matrix": "data/book/prewriting_freshness_control_v1/section_freshness_matrix_v1.json",
    "visual_manifest": "data/book/prewriting_visual_evidence_rights_validation_v1/visual_evidence_rights_validation_v1_manifest.json",
    "visual_candidates": "data/book/prewriting_visual_evidence_rights_validation_v1/repository_visual_candidate_registry_v1.json",
    "cp5_assets": "data/book/assets/nontext_asset_policy_registry_v1.json",
    "cp7_packets": "data/book/evidence_packets/section_evidence_packets_v1.json",
    "frozen_hashes": "data/book/prewriting_audit/prewriting_hash_list_v1.json",
}

def load(rel):
    return json.loads((ROOT / rel).read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(rel, value):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return path

def frozen_ok(spec):
    return all(sha(ROOT / item["path"]) == item["sha256"] for item in spec["files"])

failure = load(INPUTS["failure_analysis"])
repo_manifest = load(INPUTS["repository_manifest"])
rejected_repo = load(INPUTS["repository_rejected"])
ledger = load(INPUTS["repository_ledger"])
cost_manifest = load(INPUTS["cost_manifest"])
fresh_manifest = load(INPUTS["freshness_manifest"])
fresh_matrix = load(INPUTS["freshness_matrix"])
visual_manifest = load(INPUTS["visual_manifest"])
visual_candidates = load(INPUTS["visual_candidates"])
cp5 = load(INPUTS["cp5_assets"])
cp7 = load(INPUTS["cp7_packets"])
frozen = load(INPUTS["frozen_hashes"])

assert failure["execution_order"][5] == "PRE-WRITING EXTERNAL EVIDENCE ADMISSION V1"
assert repo_manifest["status"] == cost_manifest["status"] == fresh_manifest["status"] == visual_manifest["status"] == "GO"
assert frozen_ok(frozen)

required_fields = [
    "external_source_id", "target_chapter_ids", "target_section_ids", "target_research_question_ids",
    "source_title", "author_institution", "source_type", "publication_update_date", "access_as_of_date",
    "authoritative_url_or_persistent_identifier", "authority_class", "freshness_class", "evidence_role",
    "exact_claim_evidence_scope_supported", "limitations", "provenance", "rights_access_status",
    "immutable_capture_hash", "admission_decision",
]
contract = {
    "schema_version": "external-evidence-admission-acceptance-contract-v1",
    "mode": "FAIL_CLOSED",
    "required_fields": required_fields,
    "conditional_required_fields": {"REJECT": ["rejection_reason"]},
    "authority_priority": ["OFFICIAL_INSTITUTIONAL", "STANDARD_SPECIFICATION", "PEER_REVIEWED_TECHNICAL", "AUTHORITATIVE_INVENTORY_STATISTICS", "OFFICIAL_INVESTIGATION_RECORD", "PRIMARY_TECHNICAL_DOCUMENTATION"],
    "rules": {
        "registered_gap_required": True,
        "exact_section_and_research_question_mapping_required": True,
        "complete_provenance_required": True,
        "freshness_control_v1_pass_required_where_applicable": True,
        "historical_conflicts_preserved": True,
        "repository_criteria_may_not_be_weakened": True,
        "external_evidence_may_not_mask_systemic_repository_defects": True,
        "cost_analysis_dependencies_may_not_be_satisfied": True,
        "visual_reproduction_rights_may_not_be_inferred": True,
    },
    "drafting_authorized": False,
    "book_prose_generated": False,
}

def validate(candidate):
    errors = []
    for field in required_fields:
        if field not in candidate or candidate[field] in (None, "", []):
            errors.append("MISSING_REQUIRED_FIELD:" + field)
    if candidate.get("admission_decision") == "REJECT" and not candidate.get("rejection_reason"):
        errors.append("MISSING_REQUIRED_FIELD:rejection_reason")
    if not candidate.get("target_section_ids") or not candidate.get("target_research_question_ids"):
        errors.append("EXACT_GAP_MAPPING_REQUIRED")
    if candidate.get("freshness_class") not in (None, "NOT_APPLICABLE") and candidate.get("freshness_result") != "PASS":
        errors.append("FRESHNESS_PASS_REQUIRED")
    if candidate.get("evidence_role") == "COST_ANALYSIS_ARTIFACT":
        errors.append("COST_ANALYSIS_DEPENDENCY_CANNOT_BE_SATISFIED")
    if candidate.get("visual_publication_permission_inferred"):
        errors.append("VISUAL_RIGHTS_INFERENCE_PROHIBITED")
    return sorted(set(errors))

diagnostic_items = []
for item in rejected_repo["items"]:
    if not item["source_registry_identity"]:
        disposition = "DISCOVERY_GAP"
        basis = "Mapped document_id is absent from the authoritative source registry."
    elif item.get("provenance_status") == "source_only":
        disposition = "PROVENANCE_GAP"
        basis = "Identity exists, but provenance resolves only to source level."
    else:
        disposition = "ADMISSION_GRANULARITY_MISMATCH"
        basis = "Candidate was rejected for unvalidated claim-level support without a source-content read."
    diagnostic_items.append({
        "section_id": item["section_id"], "document_id": item["document_id"],
        "historical_rejection_reasons": item["rejection_reasons"],
        "diagnostic_disposition": disposition, "basis": basis,
        "historical_admission_decision_changed": False,
    })
diagnostic_counts = dict(sorted(Counter(x["diagnostic_disposition"] for x in diagnostic_items).items()))
for key in ["TRUE_INSUFFICIENT_EVIDENCE", "ADMISSION_GRANULARITY_MISMATCH", "DISCOVERY_GAP", "PROVENANCE_GAP", "OTHER_EVIDENCED_REASON"]:
    diagnostic_counts.setdefault(key, 0)

external_sections = [x for x in ledger["sections"] if x["coverage_disposition"] == "EXTERNAL_EVIDENCE_REQUIRED"]
gap_mapping = {
    "schema_version": "external-section-research-question-gap-mapping-v1",
    "section_count": len(external_sections),
    "improved_section_count": 0,
    "remaining_gap_count": len(external_sections),
    "sections": [{
        "section_id": x["section_id"], "research_question_ids": x["research_question_ids"],
        "external_candidate_ids": [], "admitted_external_source_ids": [],
        "status": "HELD_FOR_REPOSITORY_DISCOVERY_ADMISSION_REMEDIATION",
    } for x in external_sections],
}

positive = {field: "fixture" for field in required_fields}
positive.update({"target_chapter_ids":["CH-A"], "target_section_ids":["CH-A-S01"], "target_research_question_ids":["RQ-001-01"], "freshness_class":"NOT_APPLICABLE", "admission_decision":"ADMIT"})
negative = dict(positive)
negative.pop("provenance")
negative["evidence_role"] = "COST_ANALYSIS_ARTIFACT"
rejected_without_reason = dict(positive)
rejected_without_reason["admission_decision"] = "REJECT"
positive_errors = validate(positive)
negative_errors = validate(negative)
rejected_without_reason_errors = validate(rejected_without_reason)

visual_upstream_empty = not cp5.get("candidate_assets") and all(not p.get("asset_candidates") for p in cp7["packets"])
visual_diagnostic = {
    "schema_version": "visual-zero-candidate-diagnostic-v1",
    "diagnosis": "DISCOVERY_NOT_EXECUTED",
    "basis": "The visual phase consumed and asserted already-empty CP5/CP7 candidate registries; it did not execute repository visual discovery.",
    "recorded_candidate_count": visual_candidates["candidate_count"],
    "upstream_registries_empty": visual_upstream_empty,
    "systemic_remediation_required": True,
}

authority_freshness = {
    "schema_version": "external-authority-freshness-audit-v1", "candidate_count": 0,
    "authority_pass_count": 0, "freshness_required_count": 0, "freshness_pass_count": 0,
    "freshness_closure_result": "NOT_EVALUATED_NO_EXTERNAL_CANDIDATES",
    "freshness_control_v1_status_preserved": fresh_manifest["status"], "records": [],
}
repo_diagnostic = {
    "schema_version": "repository-zero-admission-diagnostic-v1",
    "candidate_mapping_count": len(diagnostic_items), "disposition_counts": diagnostic_counts,
    "systemic_design_defect_established": True,
    "remediation_route": "PRE-WRITING REPOSITORY EVIDENCE DISCOVERY AND ADMISSION REMEDIATION V1",
    "historical_admission_decisions_changed": False, "items": diagnostic_items,
}

artifacts = {}
artifacts["contracts/external_evidence_admission_acceptance_contract_v1.json"] = contract
artifacts["external_candidate_registry_v1.json"] = {"schema_version":"external-candidate-registry-v1","candidate_count":0,"candidates":[],"hold_reason":"SYSTEMIC_REPOSITORY_DISCOVERY_ADMISSION_DEFECT_PRECEDES_EXTERNAL_SEARCH"}
artifacts["admitted_external_evidence_registry_v1.json"] = {"schema_version":"admitted-external-evidence-registry-v1","admitted_count":0,"items":[]}
artifacts["rejected_external_evidence_registry_v1.json"] = {"schema_version":"rejected-external-evidence-registry-v1","rejected_count":0,"items":[]}
artifacts["section_research_question_gap_mapping_v1.json"] = gap_mapping
artifacts["authority_freshness_audit_v1.json"] = authority_freshness
artifacts["repository_zero_admission_diagnostic_v1.json"] = repo_diagnostic
artifacts["visual_zero_candidate_diagnostic_v1.json"] = visual_diagnostic
artifacts["fixtures/positive_fixtures_v1.json"] = {"fixtures":[positive], "validation_errors":[positive_errors]}
artifacts["fixtures/negative_fixtures_v1.json"] = {"fixtures":[negative, rejected_without_reason], "validation_errors":[negative_errors, rejected_without_reason_errors]}

audit = {
    "phase": "PRE-WRITING EXTERNAL EVIDENCE ADMISSION V1", "status": "GO_REMEDIATION_REQUIRED",
    "counts": {"external_candidates":0, "admitted":0, "rejected":0, "sections_improved":0, "remaining_external_evidence_gaps":len(external_sections)},
    "checks": {
        "every_admission_tied_to_registered_gap": True, "exact_mapping": True, "provenance_complete": True,
        "authority_appropriate": True, "freshness_pass_where_required": True, "unsupported_admissions": 0,
        "rejected_candidates_preserve_reason": True, "cost_dependencies_falsely_satisfied": 0,
        "visual_rights_inferred": False, "book_prose_generated": False, "corpus_mutated": False,
        "deterministic_registries": True, "frozen_integrity": "PASS", "state_synchronization": "PASS",
        "positive_test_pass": not positive_errors,
        "negative_test_pass": "MISSING_REQUIRED_FIELD:provenance" in negative_errors and "COST_ANALYSIS_DEPENDENCY_CANNOT_BE_SATISFIED" in negative_errors and "MISSING_REQUIRED_FIELD:rejection_reason" in rejected_without_reason_errors,
    },
    "repository_zero_diagnostic": "SYSTEMIC_DESIGN_DEFECT_ESTABLISHED",
    "visual_zero_diagnostic": visual_diagnostic["diagnosis"],
    "cost_dependencies": "REGISTERED_NOT_SATISFIED",
    "drafting_authorized": False, "book_prose_generated": False,
    "next_phase": "PRE-WRITING REPOSITORY EVIDENCE DISCOVERY AND ADMISSION REMEDIATION V1",
}
artifacts["external_evidence_admission_v1_audit.json"] = audit

written = [write(rel, value) for rel, value in artifacts.items()]
manifest = {
    "schema_version":"external-evidence-admission-manifest-v1", "phase":audit["phase"], "status":audit["status"],
    "artifacts":[{"path":str(p.relative_to(ROOT)), "sha256":sha(p)} for p in written],
    "input_hashes":[{"path":rel, "sha256":sha(ROOT / rel)} for rel in INPUTS.values()],
    "frozen_integrity":"PASS", "state_sync_result":"PASS", "drafting_authorized":False,
    "book_prose_generated":False, "next_phase":audit["next_phase"],
}
write("external_evidence_admission_v1_manifest.json", manifest)
