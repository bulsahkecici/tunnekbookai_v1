#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_repository_evidence_admission_v1"
CONTRACT = OUT / "contracts/repository_evidence_admission_contract_v1.json"

INPUTS = {
    "coverage": "data/book/coverage/corpus_to_book_coverage_mapping_v1.json",
    "research": "data/book/research/research_question_gap_registry_v1.json",
    "packets": "data/book/evidence_packets/section_evidence_packets_v1.json",
    "structure": "data/book/master_structure/book_master_structure_v1.json",
    "sources": "data/book/source_registry_v1.jsonl",
    "failure_analysis": "data/book/prewriting_failure_analysis_v1/prewriting_failure_analysis_v1.json",
    "human_gate": "data/book/prewriting_explicit_human_decision_gate_v1/explicit_human_decision_gate_v1_manifest.json",
    "frozen_hashes": "data/book/prewriting_audit/prewriting_hash_list_v1.json",
}

COST_ARTIFACT_SECTIONS = {
    "CH-E-S08", "CH-E-S09", "CH-E-S10", "CH-E-S11", "CH-E-S12", "CH-E-S13",
    "CH-E-S14", "CH-E-S15", "CH-E-S16", "CH-F-S06", "CH-G-S01", "CH-G-S02",
}

def load(path):
    return json.loads((ROOT / path).read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

def verify_hash_list(spec):
    return all(sha(ROOT / item["path"]) == item["sha256"] for item in spec["files"])

coverage = load(INPUTS["coverage"])
research = load(INPUTS["research"])
packets = load(INPUTS["packets"])
structure = load(INPUTS["structure"])
failure = load(INPUTS["failure_analysis"])
human_gate = load(INPUTS["human_gate"])
frozen_hashes = load(INPUTS["frozen_hashes"])
assert len(coverage["sections"]) == len(research["sections"]) == len(packets["packets"]) == 60
assert len(structure["sections"]) == 60
assert human_gate["status"] == "GO"
assert failure["execution_order"][1] == "PRE-WRITING REPOSITORY EVIDENCE ADMISSION V1"
assert verify_hash_list(frozen_hashes)

sources = {}
for line in (ROOT / INPUTS["sources"]).read_text().splitlines():
    item = json.loads(line)
    sources.setdefault(item["document_id"], item)

research_by_id = {item["section_id"]: item for item in research["sections"]}
packet_by_id = {item["section_id"]: item for item in packets["packets"]}
rejected = []
ledger = []

for section in coverage["sections"]:
    sid = section["section_id"]
    candidate_ids = section["primary_source_ids"] + section["secondary_source_ids"]
    for document_id in candidate_ids:
        source = sources.get(document_id)
        reasons = []
        if source is None:
            reasons.append("SOURCE_ID_NOT_IN_AUTHORITATIVE_SOURCE_REGISTRY")
        else:
            if source.get("authority_level") is None:
                reasons.append("SOURCE_AUTHORITY_NOT_ESTABLISHED")
            reasons.append("CLAIM_LEVEL_CONTENT_SUPPORT_NOT_VALIDATED")
        rejected.append({
            "section_id": sid,
            "document_id": document_id,
            "candidate_basis": section["mapping_basis"],
            "candidate_role": "SECONDARY",
            "source_registry_identity": source is not None,
            "source_key": source.get("source_key") if source else None,
            "provenance_status": source.get("provenance_status") if source else None,
            "rejection_reasons": reasons,
        })
    disposition = ("HUMAN_ANALYSIS_ARTIFACT_REQUIRED" if sid in COST_ARTIFACT_SECTIONS
                   else "EXTERNAL_EVIDENCE_REQUIRED")
    dependency = None
    if sid in COST_ARTIFACT_SECTIONS:
        dependency = ("MAINTENANCE_COST_ANALYSIS_ARTIFACT_REQUIRED"
                      if sid.startswith("CH-E") or sid == "CH-G-S01"
                      else "CONSTRUCTION_COST_ANALYSIS_ARTIFACT_REQUIRED")
    ledger.append({
        "section_id": sid,
        "source_title": section["source_title"],
        "cp3_status_preserved": section["coverage_status"],
        "candidate_repository_evidence_count": len(candidate_ids),
        "admitted_evidence_ids": [],
        "rejected_candidate_count": len(candidate_ids),
        "research_question_ids": [q["question_id"] for q in research_by_id[sid]["research_questions"]],
        "scope_contract_ref": packet_by_id[sid]["scope_contract_ref"],
        "coverage_disposition": disposition,
        "unresolved_dependency": dependency,
        "freshness_status": "PENDING_DEDICATED_FRESHNESS_CONTROL",
        "visual_admission_status": "NOT_PUBLICATION_ADMITTED",
    })

disposition_counts = {}
for item in ledger:
    key = item["coverage_disposition"]
    disposition_counts[key] = disposition_counts.get(key, 0) + 1

admitted_registry = {
    "schema_version": "admitted-repository-evidence-registry-v1",
    "count": 0,
    "items": [],
    "reason": "No indexed candidate met source-authority and claim-level content-validation requirements.",
    "external_evidence_admitted": False,
}
rejected_registry = {
    "schema_version": "rejected-repository-evidence-registry-v1",
    "candidate_mapping_count": len(rejected),
    "unique_document_count": len({item["document_id"] for item in rejected}),
    "items": rejected,
}
coverage_ledger = {
    "schema_version": "section-evidence-coverage-ledger-v1",
    "section_count": len(ledger),
    "disposition_counts": disposition_counts,
    "sections": ledger,
    "cost_dependencies": [
        {"dependency_id": "MAINTENANCE_COST_ANALYSIS_ARTIFACT_REQUIRED", "state": "REGISTERED_NOT_SATISFIED"},
        {"dependency_id": "CONSTRUCTION_COST_ANALYSIS_ARTIFACT_REQUIRED", "state": "REGISTERED_NOT_SATISFIED"},
    ],
}
audit = {
    "phase": "PRE-WRITING REPOSITORY EVIDENCE ADMISSION V1",
    "status": "GO",
    "checks": {
        "sections_classified_60_of_60": len(ledger) == 60,
        "unsupported_admissions": 0,
        "provenance_complete_for_every_admitted_item": True,
        "rejected_items_preserved_with_reason": all(item["rejection_reasons"] for item in rejected),
        "claim_section_mapping_deterministic": True,
        "external_evidence_admitted": False,
        "corpus_mutated": False,
        "source_content_reads": 0,
        "broad_corpus_scans": 0,
        "visuals_publication_admitted": 0,
        "derived_monetary_analysis_admitted": 0,
        "frozen_integrity": "PASS",
        "drafting_authorized": False,
        "book_prose_generated": False,
    },
    "admitted_count": 0,
    "rejected_candidate_mapping_count": len(rejected),
    "coverage_disposition_counts": disposition_counts,
    "next_phase": "PRE-WRITING COST METHODOLOGY CLOSURE V1",
}

artifacts = {
    OUT / "admitted_evidence_registry_v1.json": admitted_registry,
    OUT / "rejected_evidence_registry_v1.json": rejected_registry,
    OUT / "section_evidence_coverage_ledger_v1.json": coverage_ledger,
    OUT / "repository_evidence_admission_v1_audit.json": audit,
}
for path, value in artifacts.items():
    write(path, value)

manifest_items = [CONTRACT] + list(artifacts)
manifest = {
    "schema_version": "repository-evidence-admission-manifest-v1",
    "phase": "PRE-WRITING REPOSITORY EVIDENCE ADMISSION V1",
    "status": "GO",
    "artifacts": [{"path": str(path.relative_to(ROOT)), "sha256": sha(path)} for path in manifest_items],
    "input_hashes": [{"path": path, "sha256": sha(ROOT / path)} for path in INPUTS.values()],
    "frozen_integrity": "PASS" if verify_hash_list(frozen_hashes) else "FAIL",
    "drafting_authorized": False,
    "book_prose_generated": False,
    "next_phase": "PRE-WRITING COST METHODOLOGY CLOSURE V1",
}
write(OUT / "repository_evidence_admission_v1_manifest.json", manifest)
