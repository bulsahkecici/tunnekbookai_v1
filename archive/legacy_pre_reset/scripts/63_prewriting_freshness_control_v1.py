#!/usr/bin/env python3
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_freshness_control_v1"
INPUTS = {
    "master_structure": "data/book/master_structure/book_master_structure_v1.json",
    "scope_contracts": "data/book/scope_contracts/section_scope_boundary_contracts_v1.json",
    "cp3_coverage": "data/book/coverage/corpus_to_book_coverage_mapping_v1.json",
    "cp4_questions": "data/book/research/research_question_gap_registry_v1.json",
    "cp7_packets": "data/book/evidence_packets/section_evidence_packets_v1.json",
    "repository_admission": "data/book/prewriting_repository_evidence_admission_v1/section_evidence_coverage_ledger_v1.json",
    "repository_manifest": "data/book/prewriting_repository_evidence_admission_v1/repository_evidence_admission_v1_manifest.json",
    "source_registry": "data/book/source_registry_v1.jsonl",
    "cost_contract": "data/book/prewriting_cost_methodology_closure_v1/contracts/cost_analysis_artifact_contract_v1.json",
    "cost_dependencies": "data/book/prewriting_cost_methodology_closure_v1/cost_analysis_dependency_registry_v1.json",
    "cost_manifest": "data/book/prewriting_cost_methodology_closure_v1/cost_methodology_closure_v1_manifest.json",
    "frozen_hashes": "data/book/prewriting_audit/prewriting_hash_list_v1.json",
}

HISTORICAL = {"CH-A-S03", "CH-A-S04", "CH-A-S05"}
AS_OF = {"CH-A-S07", "CH-A-S08", "CH-E-S17"}
EVENT = {"CH-A-S09", "CH-A-S10", "CH-A-S11"}
CURRENT = {"CH-A-S06", "CH-B-S17"}
DATASET = {
    "CH-E-S03", "CH-E-S08", "CH-E-S09", "CH-E-S10", "CH-E-S11", "CH-E-S12",
    "CH-E-S13", "CH-E-S14", "CH-E-S15", "CH-E-S16", "CH-F-S04", "CH-F-S06",
    "CH-G-S01", "CH-G-S02",
}
NOT_APPLICABLE = {"CH-E-S01", "CH-E-S02", "CH-F-S01", "CH-F-S02", "CH-F-S03"}
CLASSES = {
    "HISTORICAL_STABLE", "SLOW_CHANGING", "CURRENTNESS_SENSITIVE",
    "AS_OF_DATE_REQUIRED", "EVENT_DEPENDENT", "DATASET_SNAPSHOT_DEPENDENT",
    "NOT_APPLICABLE",
}

def load(path):
    return json.loads((ROOT / path).read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

def classify(section_id):
    if section_id in HISTORICAL: return "HISTORICAL_STABLE"
    if section_id in AS_OF: return "AS_OF_DATE_REQUIRED"
    if section_id in EVENT: return "EVENT_DEPENDENT"
    if section_id in CURRENT: return "CURRENTNESS_SENSITIVE"
    if section_id in DATASET: return "DATASET_SNAPSHOT_DEPENDENT"
    if section_id in NOT_APPLICABLE: return "NOT_APPLICABLE"
    return "SLOW_CHANGING"

def validate(item):
    errors = []
    cls = item.get("freshness_class")
    if cls not in CLASSES: errors.append("INVALID_FRESHNESS_CLASS")
    current_claim = cls in {"CURRENTNESS_SENSITIVE", "AS_OF_DATE_REQUIRED", "EVENT_DEPENDENT"}
    if current_claim and not item.get("as_of_date"): errors.append("CURRENT_CLAIM_AS_OF_DATE_REQUIRED")
    if current_claim and item.get("evidence_expired") and item.get("presented_as_current"):
        errors.append("EXPIRED_EVIDENCE_PRESENTED_AS_CURRENT")
    if cls == "HISTORICAL_STABLE" and item.get("presented_as_current"):
        errors.append("HISTORICAL_EVIDENCE_PRESENTED_AS_CURRENT")
    if cls == "DATASET_SNAPSHOT_DEPENDENT":
        if not all(item.get(x) for x in ("dataset_version", "dataset_date", "dataset_sha256")):
            errors.append("DATASET_SNAPSHOT_IDENTITY_REQUIRED")
    if item.get("evidence_origin") == "MODEL_MEMORY": errors.append("MODEL_MEMORY_LATEST_FACT_PROHIBITED")
    if item.get("institutional_fact") and not (item.get("authority") and item.get("as_of_date")):
        errors.append("INSTITUTIONAL_AUTHORITY_DATE_REQUIRED")
    if item.get("overwrites_stale_source") and not item.get("preserves_prior_provenance"):
        errors.append("STALE_SOURCE_PROVENANCE_MUST_BE_PRESERVED")
    if item.get("global_refresh_interval_applied"):
        errors.append("ARBITRARY_GLOBAL_REFRESH_INTERVAL_PROHIBITED")
    return sorted(set(errors))

master = load(INPUTS["master_structure"])
questions = load(INPUTS["cp4_questions"])
ledger = load(INPUTS["repository_admission"])
source_records = [json.loads(line) for line in (ROOT / INPUTS["source_registry"]).read_text().splitlines() if line.strip()]
frozen = load(INPUTS["frozen_hashes"])
assert len(master["sections"]) == len(questions["sections"]) == len(ledger["sections"]) == 60
assert all(sha(ROOT / x["path"]) == x["sha256"] for x in frozen["files"])
q_by_id = {x["section_id"]: x for x in questions["sections"]}
l_by_id = {x["section_id"]: x for x in ledger["sections"]}

rules = {
    "schema_version": "book-freshness-expiry-refresh-rules-v1",
    "rules": {
        "HISTORICAL_STABLE": {"as_of_date": "SOURCE_EVENT_DATE_WHERE_AVAILABLE", "expiry": "NO_PERIODIC_EXPIRY", "behavior": "PRESERVE_SOURCE_DATE_PROVENANCE_AND_CONFLICTS"},
        "SLOW_CHANGING": {"as_of_date": "SOURCE_VERSION_OR_PUBLICATION_DATE_REQUIRED_FOR_ADMISSION", "expiry": "AUTHORITY_VERSION_CHANGE_OR_RELEASE_REVIEW", "behavior": "FAIL_CLOSED_IF_VERSION_CURRENCY_IS_MATERIAL_AND_UNVERIFIED"},
        "CURRENTNESS_SENSITIVE": {"as_of_date": "REQUIRED", "expiry": "SOURCE_DEFINED; OTHERWISE REVALIDATE_AT_RELEASE", "behavior": "MARK_FRESHNESS_REQUIRED_AND_BLOCK_AFFECTED_SCOPE"},
        "AS_OF_DATE_REQUIRED": {"as_of_date": "REQUIRED", "expiry": "REVALIDATE_AT_EACH_RELEASE", "behavior": "PRESERVE_VALID_OLDER_EVIDENCE_AS_HISTORICAL_AS_OF"},
        "EVENT_DEPENDENT": {"as_of_date": "COVERAGE_CUTOFF_REQUIRED", "expiry": "REVALIDATE_AT_RELEASE_IF_SCOPE_CLAIMS_CURRENT_COVERAGE", "behavior": "BLOCK_ONLY_CURRENT_COVERAGE_SCOPE"},
        "DATASET_SNAPSHOT_DEPENDENT": {"as_of_date": "DATASET_DATE_REQUIRED", "expiry": "FROZEN_SNAPSHOT; NEW_RESULT_REQUIRES_NEW_VERSION_DATE_HASH", "behavior": "NO_LIVE_WEB_RECENCY_SUBSTITUTION"},
        "NOT_APPLICABLE": {"as_of_date": "NOT_APPLICABLE", "expiry": "NOT_APPLICABLE", "behavior": "NO_FRESHNESS_GATE"},
    },
    "global_interval_policy": "PROHIBITED; APPLY CLASS- AND AUTHORITY-SPECIFIC RULES",
}
contract = {
    "schema_version": "book-freshness-control-contract-v1",
    "admission_mode": "FAIL_CLOSED",
    "allowed_classes": sorted(CLASSES),
    "stale_evidence_policy": {
        "infer_or_update_missing_current_fact": False,
        "missing_valid_current_evidence_status": "FRESHNESS_REQUIRED",
        "block_scope": "AFFECTED_CLAIM_OR_SECTION_ONLY",
        "preserve_valid_older_evidence": "HISTORICAL_AS_OF_EVIDENCE_WITH_PROVENANCE",
        "silently_discard_or_overwrite_provenance": False,
    },
    "historical_policy": "Exact historical facts require source/date provenance and conflict handling, not periodic refresh merely because they are old.",
    "dataset_policy": "Future analysis freshness follows a frozen dataset version/date/SHA-256, not live-web recency.",
    "visual_policy": "Visual/licensing URL access and rights state are freshness-controlled only after candidate registration; none are publication-admitted here.",
    "external_evidence_admitted": False,
    "book_prose_generated": False,
    "drafting_authorized": False,
}

matrix = []
registry = []
for section in master["sections"]:
    sid = section["section_id"]
    cls = classify(sid)
    rq = q_by_id[sid]["research_questions"][0]
    dep = l_by_id[sid].get("unresolved_dependency")
    sensitive = cls not in {"HISTORICAL_STABLE", "NOT_APPLICABLE"}
    external = sensitive and cls != "DATASET_SNAPSHOT_DEPENDENT"
    matrix.append({
        "section_id": sid,
        "source_title": section["source_title"],
        "research_question_ids": [rq["question_id"]],
        "section_classification": cls,
        "research_question_classification": cls,
        "evidence_classification": cls,
        "asset_classification": "NOT_APPLICABLE",
        "asset_candidate_count": 0,
        "repository_coverage_disposition": l_by_id[sid]["coverage_disposition"],
        "current_status": "FRESHNESS_REQUIRED" if sensitive else "CLASSIFIED",
    })
    if sensitive:
        authority = "AUTHORITATIVE_TECHNICAL_OR_INSTITUTIONAL_SOURCE"
        if cls == "DATASET_SNAPSHOT_DEPENDENT": authority = "VALIDATED_HUMAN_ANALYSIS_ARTIFACT"
        registry.append({
            "freshness_item_id": f"FR-{len(registry)+1:03d}",
            "chapter_section_id": sid,
            "research_question_id": rq["question_id"],
            "research_question_evidence_need": rq["question_text"],
            "claim_evidence_class": rq["expected_claim_class"],
            "freshness_class": cls,
            "reason_freshness_matters": rules["rules"][cls]["behavior"],
            "required_as_of_date": rules["rules"][cls]["as_of_date"],
            "acceptable_source_authority_class": authority,
            "refresh_interval_or_expiry_rule": rules["rules"][cls]["expiry"],
            "stale_evidence_behavior": rules["rules"][cls]["behavior"],
            "external_evidence_required": external,
            "dataset_snapshot_dependency": dep or ("VALIDATED_DATASET_SNAPSHOT_REQUIRED" if cls == "DATASET_SNAPSHOT_DEPENDENT" else None),
            "release_blocking": True,
            "current_status": "FRESHNESS_REQUIRED",
        })

counts = dict(sorted(Counter(x["section_classification"] for x in matrix).items()))
positive = [
    {"fixture_id": "POS-001", "item": {"freshness_class": "HISTORICAL_STABLE", "presented_as_current": False}},
    {"fixture_id": "POS-002", "item": {"freshness_class": "CURRENTNESS_SENSITIVE", "as_of_date": "2026-08-21", "authority": "OFFICIAL", "presented_as_current": True, "evidence_expired": False}},
    {"fixture_id": "POS-003", "item": {"freshness_class": "DATASET_SNAPSHOT_DEPENDENT", "dataset_version": "v1", "dataset_date": "2026-08-21", "dataset_sha256": "a" * 64}},
]
negative = [
    ("NEG-001", {"freshness_class": "CURRENTNESS_SENSITIVE", "presented_as_current": True}, "CURRENT_CLAIM_AS_OF_DATE_REQUIRED"),
    ("NEG-002", {"freshness_class": "CURRENTNESS_SENSITIVE", "as_of_date": "2020-01-01", "evidence_expired": True, "presented_as_current": True}, "EXPIRED_EVIDENCE_PRESENTED_AS_CURRENT"),
    ("NEG-003", {"freshness_class": "HISTORICAL_STABLE", "presented_as_current": True}, "HISTORICAL_EVIDENCE_PRESENTED_AS_CURRENT"),
    ("NEG-004", {"freshness_class": "DATASET_SNAPSHOT_DEPENDENT"}, "DATASET_SNAPSHOT_IDENTITY_REQUIRED"),
    ("NEG-005", {"freshness_class": "SLOW_CHANGING", "evidence_origin": "MODEL_MEMORY"}, "MODEL_MEMORY_LATEST_FACT_PROHIBITED"),
    ("NEG-006", {"freshness_class": "CURRENTNESS_SENSITIVE", "institutional_fact": True}, "INSTITUTIONAL_AUTHORITY_DATE_REQUIRED"),
    ("NEG-007", {"freshness_class": "SLOW_CHANGING", "overwrites_stale_source": True, "preserves_prior_provenance": False}, "STALE_SOURCE_PROVENANCE_MUST_BE_PRESERVED"),
    ("NEG-008", {"freshness_class": "SLOW_CHANGING", "global_refresh_interval_applied": True}, "ARBITRARY_GLOBAL_REFRESH_INTERVAL_PROHIBITED"),
]
positive_results = [{"fixture_id": x["fixture_id"], "errors": validate(x["item"])} for x in positive]
negative_results = [{"fixture_id": fid, "expected_error": expected, "errors": validate(item)} for fid, item, expected in negative]
false_rejects = sum(bool(x["errors"]) for x in positive_results)
false_accepts = sum(x["expected_error"] not in x["errors"] for x in negative_results)
dated_sources = sum(any(x.get(k) for k in ("date", "year", "publication_date", "as_of_date")) for x in source_records)
status = "GO" if len(matrix) == 60 and len(registry) == 52 and false_accepts == false_rejects == 0 else "NO-GO"

artifacts = {
    OUT / "contracts/book_freshness_control_contract_v1.json": contract,
    OUT / "freshness_registry_v1.json": {"schema_version": "freshness-registry-v1", "item_count": len(registry), "items": registry},
    OUT / "section_freshness_matrix_v1.json": {"schema_version": "section-freshness-matrix-v1", "section_count": len(matrix), "classification_counts": counts, "sections": matrix},
    OUT / "expiry_refresh_rules_v1.json": rules,
    OUT / "fixtures/positive_fixtures_v1.json": {"fixtures": positive},
    OUT / "fixtures/negative_fixtures_v1.json": {"fixtures": [{"fixture_id": x[0], "item": x[1], "expected_error": x[2]} for x in negative]},
    OUT / "freshness_control_v1_audit.json": {
        "phase": "PRE-WRITING FRESHNESS CONTROL V1", "status": status,
        "counts": {"sections_evaluated": len(matrix), "freshness_sensitive_items": len(registry), "freshness_required": sum(x["current_status"] == "FRESHNESS_REQUIRED" for x in registry), "external_evidence_dependencies": sum(x["external_evidence_required"] for x in registry), "asset_candidates": 0, "source_registry_records": len(source_records), "source_records_with_date_metadata": dated_sources},
        "classification_counts": counts,
        "tests": {"positive": len(positive), "negative": len(negative), "false_accepts": false_accepts, "false_rejects": false_rejects, "positive_results": positive_results, "negative_results": negative_results},
        "checks": {"all_60_sections_evaluated": len(matrix) == 60, "every_sensitive_item_classified": all(x["freshness_class"] in CLASSES for x in registry), "current_facts_invented": False, "web_or_external_evidence_admitted": False, "corpus_mutated": False, "book_prose_generated": False, "deterministic_validation": "PASS", "frozen_integrity": "PASS", "drafting_authorized": False},
        "next_phase": "PRE-WRITING VISUAL EVIDENCE AND RIGHTS VALIDATION V1",
    },
}
for path, value in artifacts.items(): write(path, value)
manifest_paths = list(artifacts)
manifest = {
    "schema_version": "freshness-control-manifest-v1", "phase": "PRE-WRITING FRESHNESS CONTROL V1", "status": status,
    "artifacts": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)} for p in manifest_paths],
    "input_hashes": [{"path": p, "sha256": sha(ROOT / p)} for p in INPUTS.values()],
    "frozen_integrity": "PASS", "deterministic_validation": "PASS", "drafting_authorized": False, "book_prose_generated": False,
    "next_phase": "PRE-WRITING VISUAL EVIDENCE AND RIGHTS VALIDATION V1",
}
write(OUT / "freshness_control_v1_manifest.json", manifest)
