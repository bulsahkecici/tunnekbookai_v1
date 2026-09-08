#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text())

structure = load("data/book/master_structure/book_master_structure_v1.json")
scope = load("data/book/scope_contracts/section_scope_boundary_contracts_v1.json")
coverage = load("data/book/coverage/corpus_to_book_coverage_mapping_v1.json")
research = load("data/book/research/research_question_gap_registry_v1.json")
assets = load("data/book/assets/nontext_asset_policy_registry_v1.json")
editorial = load("data/book/editorial/editorial_mechanics_v1.json")

chapters = {c["chapter_id"]: c for c in structure["chapters"]}
sections_by_id = {s["section_id"]: s for s in structure["sections"]}
coverage_by_id = {s["section_id"]: s for s in coverage["sections"]}
research_by_id = {s["section_id"]: s for s in research["sections"]}
assets_by_id = {s["section_id"]: s for s in assets["section_plans"]}
responsibility_exceptions = scope["responsibility_exceptions"]
boundary_rules = scope["boundary_rules"]

packets = []
for ordinal, section in enumerate(structure["sections"], 1):
    sid = section["section_id"]
    parent = section["parent_id"]
    chapter_id = parent
    while chapter_id not in chapters:
        chapter_id = sections_by_id[chapter_id]["parent_id"]
    chapter = chapters[chapter_id]
    cov = coverage_by_id[sid]
    rq = research_by_id[sid]
    asset = assets_by_id[sid]
    relevant_boundaries = [r for r in boundary_rules if sid in r["section_ids"] or parent in r["section_ids"] or chapter_id in r["section_ids"]]
    relevant_exceptions = [e for e in responsibility_exceptions if sid in e["section_ids"] or parent in e["section_ids"] or chapter_id in e["section_ids"]]
    chapter_decisions = [d for d in scope["chapter_level_unresolved_decisions"] if d.startswith(chapter_id)]
    human_needed = bool(relevant_boundaries or relevant_exceptions or chapter_decisions)
    if human_needed:
        readiness = "HUMAN_DECISION_REQUIRED"
        readiness_basis = "CP2 boundary/responsibility decision remains unresolved."
    elif cov["coverage_status"] == "UNOBSERVED":
        readiness = "BLOCKED"
        readiness_basis = "No source content has been validated for this section."
    else:
        readiness = "EVIDENCE_PARTIAL"
        readiness_basis = "Metadata candidates exist but claim-level source validation is pending."
    packets.append({
        "packet_id": f"EP-{ordinal:03d}",
        "section_id": sid,
        "source_title": section["source_title"],
        "scope_contract_ref": {
            "artifact": "section_scope_boundary_contracts_v1",
            "default_contract": True,
            "boundary_rule_ids": [r["rule_id"] for r in relevant_boundaries]
        },
        "responsibility": {
            "state": "HUMAN_DECISION_REQUIRED" if relevant_exceptions or chapter_decisions else "INHERITED_FROM_CHAPTER",
            "responsible_authors": chapter["responsible_authors"],
            "exception_states": [e["state"] for e in relevant_exceptions],
            "chapter_decisions": chapter_decisions
        },
        "research_question_ids": [q["question_id"] for q in rq["research_questions"]],
        "evidence": {
            "coverage_status": cov["coverage_status"],
            "primary_source_ids": cov["primary_source_ids"],
            "secondary_source_ids": cov["secondary_source_ids"],
            "evidence_note_refs": [f"corpus_to_book_coverage_mapping_v1#{sid}"]
        },
        "claim_candidates": [],
        "conflicts": cov["unresolved_source_conflicts"],
        "qualifiers_conditions_dependencies": {
            "boundary_rule_ids": [r["rule_id"] for r in relevant_boundaries],
            "prerequisites": scope["default_contract"]["prerequisite_concepts"],
            "claim_level_items": []
        },
        "terminology": {
            "contract_ref": "editorial_mechanics_v1#terminology",
            "unresolved_term_ids": [e["term_id"] for e in editorial["terminology"]["entries"] if e["translation_state"] == "ORIGINAL_TERM_UNRESOLVED"]
        },
        "citation_candidates": cov["primary_source_ids"] + cov["secondary_source_ids"],
        "asset_candidates": asset["candidate_asset_ids"],
        "gaps": rq["gaps"],
        "readiness": {"state": readiness, "basis": readiness_basis},
        "drafting_authorized": False
    })

out = {
    "schema_version": "section-evidence-packets-v1",
    "status": "PREWRITING_ONLY",
    "section_count": len(packets),
    "packets": packets,
    "unsupported_facts_inserted": 0,
    "book_prose_generated": False,
    "drafting_authorized": False
}
target = ROOT / "data/book/evidence_packets/section_evidence_packets_v1.json"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
