#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COVERAGE = ROOT / "data/book/coverage/corpus_to_book_coverage_mapping_v1.json"
SCOPE = ROOT / "data/book/scope_contracts/section_scope_boundary_contracts_v1.json"
OUTPUT = ROOT / "data/book/research/research_question_gap_registry_v1.json"

coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
scope = json.loads(SCOPE.read_text(encoding="utf-8"))
author_decision_ids = {section_id for item in scope["responsibility_exceptions"] for section_id in item["section_ids"]}
terminology_ids = {"CH-B-S01", "CH-B-S03"}
records = []
for index, section in enumerate(coverage["sections"], 1):
    gap = "NO_SOURCE" if section["coverage_status"] == "UNOBSERVED" else "INSUFFICIENT_SCOPE"
    gaps = [{"gap_type": gap, "basis": section["confidence_evidence_basis"]}]
    if section["section_id"] in author_decision_ids:
        gaps.append({"gap_type": "AUTHOR_DECISION_REQUIRED", "basis": "CP2 responsibility exception"})
    if section["section_id"] in terminology_ids:
        gaps.append({"gap_type": "TERMINOLOGY_UNRESOLVED", "basis": "CP2 boundary rule BR-007"})
    records.append({
        "section_id": section["section_id"],
        "research_questions": [{
            "question_id": f"RQ-{index:03d}-01",
            "question_text": f"Which authoritative evidence establishes the subject and approved boundaries of ‘{section['source_title']}’ without importing sibling-section scope?",
            "purpose": "Test the section scope and identify supportable claims before drafting.",
            "evidence_type_required": ["authoritative_source", "claim_level_citation_support"],
            "source_type_priority": ["canonical_primary_source", "authoritative_technical_source", "reviewed_secondary_source"],
            "freshness_requirement": "ASSESS_DURING_SOURCE_VALIDATION",
            "acceptable_unresolved_outcome": "Record the gap and prohibit unsupported drafting.",
            "expected_claim_class": "SECTION_SCOPE_FACTS",
            "visualization_data_possibility": "ASSESS_AFTER_EVIDENCE_VALIDATION",
            "dependency_on_other_sections": "USE_CP2_BOUNDARY_RULES",
            "current_evidence_status": section["coverage_status"]
        }],
        "gaps": gaps,
        "drafting_status": "NOT_AUTHORIZED"
    })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps({
    "schema_version": "research-question-gap-registry-v1",
    "section_count": len(records),
    "question_count": len(records),
    "sections": records,
    "model_knowledge_used_to_fill_gaps": False,
    "book_prose_generated": False,
    "drafting_authorized": False
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
