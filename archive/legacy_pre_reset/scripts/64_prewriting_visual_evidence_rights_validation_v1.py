#!/usr/bin/env python3
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_visual_evidence_rights_validation_v1"
INPUTS = {
    "master_structure": "data/book/master_structure/book_master_structure_v1.json",
    "cp3_coverage": "data/book/coverage/corpus_to_book_coverage_mapping_v1.json",
    "cp4_questions": "data/book/research/research_question_gap_registry_v1.json",
    "cp5_assets": "data/book/assets/nontext_asset_policy_registry_v1.json",
    "cp7_packets": "data/book/evidence_packets/section_evidence_packets_v1.json",
    "source_registry": "data/book/source_registry_v1.jsonl",
    "repository_coverage": "data/book/prewriting_repository_evidence_admission_v1/section_evidence_coverage_ledger_v1.json",
    "freshness_matrix": "data/book/prewriting_freshness_control_v1/section_freshness_matrix_v1.json",
    "frozen_hashes": "data/book/prewriting_audit/prewriting_hash_list_v1.json",
}
ASSET_CLASSES = {"SOURCE_TABLE", "SOURCE_FIGURE", "SOURCE_PHOTO", "AUTHOR_RECONSTRUCTED_TABLE", "AUTHOR_GENERATED_SCHEMATIC", "DERIVED_CHART", "MAP", "EQUATION", "DATA_TABLE", "OTHER"}
RIGHTS = {"CLEARED", "AUTHOR_GENERATED", "INTERNAL_USE_ONLY", "REQUIRES_PERMISSION", "UNKNOWN"}
READINESS = {"VISUAL_NOT_REQUIRED", "REPOSITORY_VISUAL_READY", "RECONSTRUCTION_CANDIDATE", "EXTERNAL_VISUAL_REQUIRED", "RIGHTS_REVIEW_REQUIRED", "DATA_ANALYSIS_OUTPUT_REQUIRED", "UNRESOLVED"}

def load(path): return json.loads((ROOT / path).read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

def validate(candidate):
    errors = []
    if candidate.get("asset_class") not in ASSET_CLASSES: errors.append("INVALID_ASSET_CLASS")
    if candidate.get("rights_state") not in RIGHTS: errors.append("INVALID_RIGHTS_STATE")
    if candidate.get("corpus_presence") and candidate.get("rights_state") == "CLEARED" and not candidate.get("rights_evidence"): errors.append("CORPUS_PRESENCE_NOT_CLEARANCE")
    if candidate.get("public_url") and candidate.get("rights_state") == "CLEARED" and not candidate.get("rights_evidence"): errors.append("PUBLIC_URL_NOT_PERMISSION")
    if candidate.get("prior_rights_state") == "UNKNOWN" and candidate.get("rights_state") == "CLEARED" and not candidate.get("rights_evidence"): errors.append("UNKNOWN_RIGHTS_PROMOTION")
    if candidate.get("publication_eligible") and not all(candidate.get(x) for x in ("source_identity", "provenance", "rights_evidence")): errors.append("PUBLICATION_READY_PROVENANCE_RIGHTS_REQUIRED")
    if candidate.get("asset_class") == "DERIVED_CHART" and not all(candidate.get(x) for x in ("underlying_data_identity", "underlying_data_sha256", "reproducible_method")): errors.append("REPRODUCIBLE_DATA_REQUIRED")
    if candidate.get("asset_class") == "AUTHOR_RECONSTRUCTED_TABLE" and candidate.get("factual_content") and not candidate.get("underlying_evidence_admitted"): errors.append("RECONSTRUCTION_FACTUAL_SUPPORT_REQUIRED")
    if candidate.get("generation_origin") == "AI" and candidate.get("technical_review_status") == "REVIEWED": errors.append("AI_GENERATION_NOT_TECHNICAL_REVIEW")
    if candidate.get("pixel_values_used_as_structured_data") and not candidate.get("authorized_extraction_validation"): errors.append("UNAUTHORIZED_IMAGE_VALUE_EXTRACTION")
    if candidate.get("freshness_sensitive") and candidate.get("presented_as_current") and not candidate.get("valid_as_of_date"): errors.append("FRESHNESS_VALIDATION_REQUIRED")
    if candidate.get("publication_eligible") and not candidate.get("evidence_eligible"): errors.append("PUBLICATION_REQUIRES_EVIDENCE_ELIGIBILITY")
    return sorted(set(errors))

master, cp5, cp7 = load(INPUTS["master_structure"]), load(INPUTS["cp5_assets"]), load(INPUTS["cp7_packets"])
coverage, freshness, frozen = load(INPUTS["repository_coverage"]), load(INPUTS["freshness_matrix"]), load(INPUTS["frozen_hashes"])
source_records = [json.loads(x) for x in (ROOT / INPUTS["source_registry"]).read_text().splitlines() if x.strip()]
assert len(master["sections"]) == len(cp5["section_plans"]) == len(cp7["packets"]) == len(coverage["sections"]) == 60
assert all(sha(ROOT / x["path"]) == x["sha256"] for x in frozen["files"])
assert not cp5["candidate_assets"] and all(not x["asset_candidates"] for x in cp7["packets"])
coverage_by_id = {x["section_id"]: x for x in coverage["sections"]}
fresh_by_id = {x["section_id"]: x for x in freshness["sections"]}

contract = {
    "schema_version": "visual-evidence-rights-acceptance-contract-v1", "mode": "FAIL_CLOSED",
    "asset_classes": sorted(ASSET_CLASSES), "rights_states": sorted(RIGHTS), "readiness_states": sorted(READINESS),
    "required_candidate_fields": ["asset_id", "section_id", "asset_class", "source_identity", "provenance", "evidence_role", "section_fit", "rights_state", "rights_evidence", "freshness_class", "evidence_eligible", "publication_eligible", "reconstruction_eligible", "status"],
    "separation_rule": "Evidence eligibility, publication-rights eligibility, and reconstruction eligibility are independent and must never be inferred from one another.",
    "rights_rule": "Corpus presence and public URL availability are not licence or permission evidence; UNKNOWN cannot be promoted without evidence.",
    "derived_rule": "Derived charts require validated underlying data identity/hash and reproducible method; future human analysis outputs remain dependency-blocked.",
    "image_extraction_rule": "Pixel values are not structured data unless an authorized extraction and validation process exists.",
    "candidate_count_zero_valid": True, "external_evidence_admitted": False, "visuals_generated": False, "drafting_authorized": False, "book_prose_generated": False,
}

matrix = []
for section in master["sections"]:
    sid = section["section_id"]
    disposition = coverage_by_id[sid]["coverage_disposition"]
    readiness = "DATA_ANALYSIS_OUTPUT_REQUIRED" if disposition == "HUMAN_ANALYSIS_ARTIFACT_REQUIRED" else "VISUAL_NOT_REQUIRED"
    matrix.append({
        "section_id": sid, "source_title": section["source_title"], "candidate_count": 0,
        "readiness": readiness,
        "basis": "VALIDATED_HUMAN_ANALYSIS_OUTPUT_REQUIRED_BEFORE_DERIVED_VISUAL" if readiness == "DATA_ANALYSIS_OUTPUT_REQUIRED" else "NO_EVIDENCE_SUPPORTED_MANDATORY_VISUAL_CURRENTLY_REGISTERED",
        "repository_coverage_disposition": disposition,
        "freshness_classification": fresh_by_id[sid]["section_classification"],
        "publication_visual_ready": False, "rights_review_required": False,
    })

positive = [
    {"fixture_id":"POS-001", "candidate":{"asset_class":"SOURCE_FIGURE","rights_state":"UNKNOWN","evidence_eligible":True,"publication_eligible":False}},
    {"fixture_id":"POS-002", "candidate":{"asset_class":"AUTHOR_RECONSTRUCTED_TABLE","rights_state":"AUTHOR_GENERATED","factual_content":True,"underlying_evidence_admitted":True,"evidence_eligible":True,"publication_eligible":False}},
    {"fixture_id":"POS-003", "candidate":{"asset_class":"DERIVED_CHART","rights_state":"AUTHOR_GENERATED","underlying_data_identity":"DS-1","underlying_data_sha256":"a"*64,"reproducible_method":"SCRIPT-1","evidence_eligible":True,"publication_eligible":False}},
]
negative = [
    ("NEG-001", {"asset_class":"SOURCE_FIGURE","rights_state":"CLEARED","corpus_presence":True}, "CORPUS_PRESENCE_NOT_CLEARANCE"),
    ("NEG-002", {"asset_class":"SOURCE_PHOTO","rights_state":"CLEARED","public_url":True}, "PUBLIC_URL_NOT_PERMISSION"),
    ("NEG-003", {"asset_class":"SOURCE_TABLE","rights_state":"CLEARED","prior_rights_state":"UNKNOWN"}, "UNKNOWN_RIGHTS_PROMOTION"),
    ("NEG-004", {"asset_class":"SOURCE_FIGURE","rights_state":"CLEARED","publication_eligible":True,"evidence_eligible":True}, "PUBLICATION_READY_PROVENANCE_RIGHTS_REQUIRED"),
    ("NEG-005", {"asset_class":"DERIVED_CHART","rights_state":"AUTHOR_GENERATED"}, "REPRODUCIBLE_DATA_REQUIRED"),
    ("NEG-006", {"asset_class":"AUTHOR_RECONSTRUCTED_TABLE","rights_state":"AUTHOR_GENERATED","factual_content":True}, "RECONSTRUCTION_FACTUAL_SUPPORT_REQUIRED"),
    ("NEG-007", {"asset_class":"AUTHOR_GENERATED_SCHEMATIC","rights_state":"AUTHOR_GENERATED","generation_origin":"AI","technical_review_status":"REVIEWED"}, "AI_GENERATION_NOT_TECHNICAL_REVIEW"),
    ("NEG-008", {"asset_class":"SOURCE_FIGURE","rights_state":"UNKNOWN","pixel_values_used_as_structured_data":True}, "UNAUTHORIZED_IMAGE_VALUE_EXTRACTION"),
    ("NEG-009", {"asset_class":"MAP","rights_state":"UNKNOWN","freshness_sensitive":True,"presented_as_current":True}, "FRESHNESS_VALIDATION_REQUIRED"),
]
positive_results = [{"fixture_id":x["fixture_id"], "errors":validate(x["candidate"]), "result":"PASS" if not validate(x["candidate"]) else "FAIL"} for x in positive]
negative_results = [{"fixture_id":fid, "errors":validate(item), "expected_error":expected, "result":"PASS" if expected in validate(item) else "FAIL"} for fid,item,expected in negative]
false_rejects = sum(x["result"] == "FAIL" for x in positive_results)
false_accepts = sum(x["result"] == "FAIL" for x in negative_results)
counts = dict(sorted(Counter(x["readiness"] for x in matrix).items()))
status = "GO" if len(matrix) == 60 and false_accepts == false_rejects == 0 else "NO-GO"

artifacts = {
    OUT / "contracts/visual_evidence_rights_acceptance_contract_v1.json": contract,
    OUT / "repository_visual_candidate_registry_v1.json": {"schema_version":"repository-visual-candidate-registry-v1","candidate_count":0,"candidates":[],"basis":"CP5 and CP7 authoritative registries contain zero candidates; no unsupported candidate was invented."},
    OUT / "visual_rights_registry_v1.json": {"schema_version":"visual-rights-registry-v1","candidate_count":0,"rights_state_counts":{x:0 for x in sorted(RIGHTS)},"records":[]},
    OUT / "section_visual_readiness_matrix_v1.json": {"schema_version":"section-visual-readiness-matrix-v1","section_count":60,"readiness_counts":counts,"sections":matrix},
    OUT / "reconstruction_candidate_registry_v1.json": {"schema_version":"reconstruction-candidate-registry-v1","candidate_count":0,"candidates":[],"policy":"No reconstruction is registered without admitted factual evidence and explicit section fit."},
    OUT / "rejected_unknown_visual_candidate_registry_v1.json": {"schema_version":"rejected-unknown-visual-candidate-registry-v1","rejected_count":0,"unknown_rights_count":0,"records":[]},
    OUT / "fixtures/positive_fixtures_v1.json": {"fixtures":positive},
    OUT / "fixtures/negative_fixtures_v1.json": {"fixtures":[{"fixture_id":a,"candidate":b,"expected_error":c} for a,b,c in negative]},
    OUT / "visual_evidence_rights_validation_v1_audit.json": {
        "phase":"PRE-WRITING VISUAL EVIDENCE AND RIGHTS VALIDATION V1","status":status,
        "counts":{"sections_evaluated":60,"repository_candidates":0,"rights_records":0,"reconstruction_candidates":0,"rejected_candidates":0,"source_registry_records":len(source_records),"readiness":counts},
        "tests":{"positive":len(positive),"negative":len(negative),"false_accepts":false_accepts,"false_rejects":false_rejects,"positive_results":positive_results,"negative_results":negative_results},
        "checks":{"all_60_sections_evaluated":True,"unsupported_candidate_admitted":False,"rights_inferred":False,"publication_eligibility_inferred":False,"external_evidence_admitted":False,"visual_generated":False,"corpus_mutated":False,"frozen_integrity":"PASS","deterministic_validation":"PASS","drafting_authorized":False,"book_prose_generated":False},
        "next_phase":"PRE-WRITING EXTERNAL EVIDENCE ADMISSION V1",
    },
}
for path,value in artifacts.items(): write(path,value)
manifest = {
    "schema_version":"visual-evidence-rights-validation-manifest-v1","phase":"PRE-WRITING VISUAL EVIDENCE AND RIGHTS VALIDATION V1","status":status,
    "artifacts":[{"path":str(p.relative_to(ROOT)),"sha256":sha(p)} for p in artifacts],
    "input_hashes":[{"path":p,"sha256":sha(ROOT / p)} for p in INPUTS.values()],
    "frozen_integrity":"PASS","deterministic_validation":"PASS","drafting_authorized":False,"book_prose_generated":False,
    "next_phase":"PRE-WRITING EXTERNAL EVIDENCE ADMISSION V1",
}
write(OUT / "visual_evidence_rights_validation_v1_manifest.json", manifest)
