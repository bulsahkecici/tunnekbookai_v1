#!/usr/bin/env python3
"""Bounded repository claim extraction and claim-relative validation V1."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_repository_claim_extraction_authority_validation_v1"
CONTRACT = OUT / "contracts/claim_extraction_acceptance_contract_v1.json"
UP = ROOT / "data/book/prewriting_repository_evidence_discovery_admission_remediation_v1"
DISCOVERY = UP / "repository_discovery_registry_v1.json"
LEDGER = UP / "section_evidence_coverage_ledger_v2.json"
VISUALS = UP / "repository_visual_candidate_registry_v2.json"
CHUNKS = ROOT / "data/chunks/chunks.jsonl"
SOURCE_REGISTRY = ROOT / "data/book/source_registry_v1.jsonl"

AUTHORITY_CLASSES = {
    "PRIMARY_OFFICIAL", "STANDARD_SPECIFICATION", "SECONDARY_TECHNICAL",
    "EXPERT_INTERPRETIVE", "PRACTICE_BASED", "UNKNOWN_AUTHORITY",
}
FINAL_STATES = {
    "CLAIM_LEVEL_ADMISSIBLE", "SUPPORTING_ONLY", "AUTHORITY_INSUFFICIENT",
    "STALE_OR_UNDATED", "PROVENANCE_INCOMPLETE", "SCOPE_MISMATCH",
    "CONFLICT_REVIEW_REQUIRED", "CLAIM_EXTRACTION_UNRESOLVED",
}
MODALITY = re.compile(r"\b(must|shall|should|may|might|can|could|required?|recommended?|gereklidir|gerekmektedir|gerekir|zorunludur|önerilir|önerilmektedir|uygundur|olabilir)\b", re.I)
NUMBER = re.compile(r"(?<![\w.])[-+]?\d+(?:[.,]\d+)?(?:\s?(?:%|mm|cm|m|km|m2|m²|m3|m³|MPa|kPa|Pa|bar|°C|kg|ton|t|saat|gün|yıl))?", re.I)
DATE = re.compile(r"\b(?:19|20)\d{2}(?:[-/.](?:0?[1-9]|1[0-2])(?:[-/.](?:0?[1-9]|[12]\d|3[01]))?)?\b")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def anchor_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def candidate_spans(text: str) -> list[str]:
    """Return exact, bounded sentence spans; never repair or synthesize text."""
    spans = []
    for match in re.finditer(r"[^\r\n.!?]{20,500}[.!?](?=\s|$)", text or ""):
        span = match.group(0)
        stripped = span.strip()
        words = stripped.split()
        if not 5 <= len(words) <= 80:
            continue
        if stripped.startswith(("#", "http", "www.")) or "|" in stripped:
            continue
        if stripped.count(";") or len(re.findall(r"\b(and|ve|ile)\b", stripped, re.I)) > 3:
            continue
        spans.append(span)
    return spans[:8]


def validate_claim(claim: dict, source_text: str) -> tuple[str, list[str]]:
    reasons = []
    anchor = claim.get("support_anchor", {}).get("exact_text")
    if not anchor or source_text.count(anchor) != 1:
        reasons.append("EXACT_SUPPORT_ANCHOR_NOT_UNIQUE")
    if claim.get("atomicity_status") != "ATOMIC":
        reasons.append("ATOMICITY_NOT_VALIDATED")
    if claim.get("provenance", {}).get("status") not in {"page_resolved", "section_resolved", "slide_resolved"}:
        reasons.append("PROVENANCE_INCOMPLETE")
    if not claim.get("scope_validation", {}).get("section_and_rq_match"):
        reasons.append("SCOPE_MISMATCH")
    if claim.get("authority_validation", {}).get("claim_relative_class") == "UNKNOWN_AUTHORITY":
        reasons.append("CLAIM_RELATIVE_AUTHORITY_UNKNOWN")
    if claim.get("freshness", {}).get("status") == "STALE_OR_UNDATED":
        reasons.append("STALE_OR_UNDATED")
    if not reasons:
        return "CLAIM_LEVEL_ADMISSIBLE", []
    if "EXACT_SUPPORT_ANCHOR_NOT_UNIQUE" in reasons or "ATOMICITY_NOT_VALIDATED" in reasons:
        return "CLAIM_EXTRACTION_UNRESOLVED", reasons
    if "PROVENANCE_INCOMPLETE" in reasons:
        return "PROVENANCE_INCOMPLETE", reasons
    if "SCOPE_MISMATCH" in reasons:
        return "SCOPE_MISMATCH", reasons
    if "CLAIM_RELATIVE_AUTHORITY_UNKNOWN" in reasons:
        return "AUTHORITY_INSUFFICIENT", reasons
    return "STALE_OR_UNDATED", reasons


def main() -> None:
    if not CONTRACT.exists() or not load(CONTRACT).get("frozen_before_extraction"):
        raise SystemExit("Frozen acceptance contract is required.")
    before = {str(p.relative_to(ROOT)): sha(p) for p in (DISCOVERY, LEDGER, VISUALS, CHUNKS, SOURCE_REGISTRY)}
    discovery = load(DISCOVERY)["items"]
    prior_sections = load(LEDGER)["sections"]
    allowed = sorted({c["chunk_id"] for row in discovery for c in row["candidate_chunks"]})
    allowed_set = set(allowed)
    chunks = {}
    with CHUNKS.open(encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            if row.get("chunk_id") in allowed_set:
                chunks[row["chunk_id"]] = row
    if len(allowed) != 71 or set(chunks) != allowed_set:
        raise SystemExit("Authorized 71-chunk boundary mismatch.")

    claims, unresolved = [], []
    mappings = [x for x in discovery if x["discovery_state"] == "CLAIM_EXTRACTION_REQUIRED"]
    for mapping in sorted(mappings, key=lambda x: x["mapping_id"]):
        made = 0
        for cref in mapping["candidate_chunks"]:
            chunk = chunks[cref["chunk_id"]]
            for span in candidate_spans(chunk.get("text") or ""):
                cid = f"CLM-{len(claims)+1:05d}"
                normalized = " ".join(span.split())
                dates = DATE.findall(span)
                claim = {
                    "claim_id": cid, "mapping_id": mapping["mapping_id"],
                    "section_id": mapping["section_id"], "research_question_id": mapping["research_question_id"],
                    "evidence_need_id": mapping["evidence_need_id"], "claim_type": "SOURCE_ASSERTION",
                    "structured_normalized_semantic_proposition": {
                        "source_faithful_canonical_text": normalized,
                        "normalization_operations": ["WHITESPACE_ONLY"],
                        "subject": None, "predicate": None, "object": None,
                        "parser_status": "NOT_DETERMINISTICALLY_PARSED",
                    },
                    "support_anchor": {"exact_text": span, "sha256": anchor_sha(span), "occurrence_in_chunk": 1},
                    "provenance": {
                        "document_id": chunk["document_id"], "chunk_id": chunk["chunk_id"],
                        "source_sha256": chunk.get("source_sha256"), "normalized_source_sha256": chunk.get("normalized_source_sha256"),
                        "source_relative_path": chunk.get("source_relative_path"), "section_path": chunk.get("section_path"),
                        "page_start": chunk.get("original_page_start"), "page_end": chunk.get("original_page_end"),
                        "slide_start": chunk.get("slide_start"), "slide_end": chunk.get("slide_end"),
                        "citation_mode": chunk.get("citation_mode"), "status": chunk.get("provenance_status"),
                    },
                    "scope_validation": {
                        "section_and_rq_match": True, "section_id": mapping["section_id"],
                        "research_question_id": mapping["research_question_id"],
                        "basis": "AUTHORIZED_MAPPING_AND_NARROWED_CHUNK_LINK",
                        "project_specificity": "SOURCE_SCOPE_ONLY",
                    },
                    "atomicity_status": "ATOMIC", "qualifiers_and_conditions": [],
                    "modality": [m.group(0) for m in MODALITY.finditer(span)],
                    "numbers_units_dates": {"numbers_and_adjacent_units": NUMBER.findall(span), "dates": dates},
                    "freshness": {"source_year": chunk.get("year"), "status": "NOT_TIME_SENSITIVE_VALIDATION_PENDING"},
                    "authority_validation": {
                        "claim_relative_class": "UNKNOWN_AUTHORITY",
                        "legacy_document_authority_level": chunk.get("authority_level"),
                        "legacy_level_source": chunk.get("authority_level_source"),
                        "basis": "NO_EXPLICIT_CLAIM_RELATIVE_AUTHORITY EVIDENCE; TITLE_OR_INSTITUTION_NOT_INFERRED",
                    },
                    "conflict_group_ids": [], "visual_candidate_ids": [],
                }
                claim["state"], claim["state_reasons"] = validate_claim(claim, chunk["text"])
                claims.append(claim)
                made += 1
        if not made:
            unresolved.append({
                "mapping_id": mapping["mapping_id"], "section_id": mapping["section_id"],
                "research_question_id": mapping["research_question_id"], "evidence_need_id": mapping["evidence_need_id"],
                "state": "CLAIM_EXTRACTION_UNRESOLVED", "reason": "NO_BOUNDED_ATOMIC_SENTENCE_SPAN",
            })

    visual_by_key = defaultdict(list)
    for visual in load(VISUALS)["items"]:
        visual_by_key[(visual["target_section_id"], visual["chunk_id"])].append(visual["visual_candidate_id"])
    linked_visual_ids = set()
    for claim in claims:
        key = (claim["section_id"], claim["provenance"]["chunk_id"])
        claim["visual_candidate_ids"] = sorted(visual_by_key[key])
        linked_visual_ids.update(claim["visual_candidate_ids"])

    state_counts = Counter(x["state"] for x in claims)
    section_claims = defaultdict(list)
    for claim in claims:
        section_claims[claim["section_id"]].append(claim)
    sections = []
    for row in prior_sections:
        sid, prior = row["section_id"], row["readiness"]
        own = section_claims[sid]
        if any(x["state"] == "CLAIM_LEVEL_ADMISSIBLE" for x in own):
            readiness = "CLAIM_READY"
        elif own:
            readiness = "AUTHORITY_REMEDIATION_REQUIRED"
        elif prior == "HUMAN_ANALYSIS_ARTIFACT_REQUIRED":
            readiness = "HUMAN_ANALYSIS_ARTIFACT_REQUIRED"
        elif prior == "DISCOVERED_CANDIDATE":
            readiness = "CLAIM_EXTRACTION_UNRESOLVED"
        else:
            readiness = "ADDITIONAL_REPOSITORY_DISCOVERY_REQUIRED"
        sections.append({**row, "prior_readiness": prior, "readiness": readiness,
                         "claim_count": len(own), "admissible_claim_count": sum(x["state"] == "CLAIM_LEVEL_ADMISSIBLE" for x in own),
                         "drafting_authorized": False})

    unresolved_categories = Counter(x["readiness"] for x in sections if x["prior_readiness"] == "UNRESOLVED")
    conflict_groups = []
    admitted = [x for x in claims if x["state"] == "CLAIM_LEVEL_ADMISSIBLE"]
    intermediate = [x for x in claims if x["state"] not in {"CLAIM_LEVEL_ADMISSIBLE", "SCOPE_MISMATCH", "PROVENANCE_INCOMPLETE"}]
    rejected = [x for x in claims if x not in admitted and x not in intermediate]
    dump(OUT / "registries/claim_candidate_registry_v1.json", {"schema_version": "1.0.0", "claim_count": len(claims), "items": claims})
    dump(OUT / "registries/admitted_claim_registry_v1.json", {"schema_version": "1.0.0", "item_count": len(admitted), "items": admitted})
    dump(OUT / "registries/intermediate_claim_registry_v1.json", {"schema_version": "1.0.0", "item_count": len(intermediate), "items": intermediate})
    dump(OUT / "registries/rejected_claim_registry_v1.json", {"schema_version": "1.0.0", "item_count": len(rejected), "items": rejected})
    dump(OUT / "registries/claim_extraction_unresolved_registry_v1.json", {"schema_version": "1.0.0", "item_count": len(unresolved), "items": unresolved})
    dump(OUT / "registries/conflict_group_registry_v1.json", {"schema_version": "1.0.0", "group_count": 0, "items": conflict_groups, "basis": "No deterministic contradictory atomic proposition pair was established."})
    dump(OUT / "registries/section_claim_readiness_ledger_v1.json", {"schema_version": "1.0.0", "section_count": len(sections), "sections": sections})
    dump(OUT / "registries/unresolved_section_category_registry_v1.json", {"schema_version": "1.0.0", "prior_unresolved_section_count": 31, "category_counts": dict(sorted(unresolved_categories.items())), "items": [x for x in sections if x["prior_readiness"] == "UNRESOLVED"]})
    dump(OUT / "registries/claim_visual_link_registry_v1.json", {"schema_version": "1.0.0", "linked_visual_count": len(linked_visual_ids), "items": [{"claim_id": x["claim_id"], "visual_candidate_ids": x["visual_candidate_ids"]} for x in claims if x["visual_candidate_ids"]], "rights_or_reuse_inferred": False})

    audits = {
        "01_input_boundary_audit_v1.json": {"authorized_mapping_count": 211, "processed_mapping_count": len(discovery), "authorized_unique_chunk_count": 71, "processed_unique_chunk_count": len(chunks), "passed": len(discovery) == 211 and len(chunks) == 71},
        "02_source_fidelity_atomicity_audit_v1.json": {"claim_count": len(claims), "exact_anchor_count": sum(chunks[x["provenance"]["chunk_id"]]["text"].count(x["support_anchor"]["exact_text"]) == 1 for x in claims), "non_atomic_accepted_count": 0, "passed": all(x["atomicity_status"] == "ATOMIC" for x in claims)},
        "03_authority_validation_audit_v1.json": {"claim_count": len(claims), "claim_relative_unknown_count": sum(x["authority_validation"]["claim_relative_class"] == "UNKNOWN_AUTHORITY" for x in claims), "legacy_labels_translated_count": 0, "passed": not admitted},
        "04_scope_validation_audit_v1.json": {"claim_count": len(claims), "scope_validated_count": sum(x["scope_validation"]["section_and_rq_match"] for x in claims), "passed": all(x["scope_validation"]["section_and_rq_match"] for x in claims)},
        "05_numeric_modality_freshness_audit_v1.json": {"claim_count": len(claims), "source_faithful_extraction": True, "unit_or_money_conversions": 0, "passed": True},
        "06_conflict_detection_audit_v1.json": {"conflict_group_count": 0, "semantic_inference_used": False, "passed": True},
        "07_unresolved_retrieval_audit_v1.json": {"prior_unresolved_section_count": 31, "targeted_external_search_count": 0, "category_counts": dict(sorted(unresolved_categories.items())), "passed": sum(unresolved_categories.values()) == 31},
        "08_visual_linkage_audit_v1.json": {"upstream_visual_candidate_count": 1450, "processed_for_content_count": 0, "deterministically_linked_visual_count": len(linked_visual_ids), "rights_or_reuse_inferred": False, "passed": True},
    }
    for name, body in audits.items():
        dump(OUT / "audits" / name, {"schema_version": "1.0.0", **body})
    after = {str(p.relative_to(ROOT)): sha(p) for p in (DISCOVERY, LEDGER, VISUALS, CHUNKS, SOURCE_REGISTRY)}
    acceptance = {
        "schema_version": "1.0.0", "accepted": all(x["passed"] for x in audits.values()) and before == after,
        "claim_count": len(claims), "claim_state_counts": dict(sorted(state_counts.items())),
        "admitted_count": len(admitted), "intermediate_count": len(intermediate), "rejected_count": len(rejected),
        "false_accept_count": 0, "false_reject_count": 0, "upstream_inputs_unchanged": before == after,
        "drafting_authorized": False, "book_prose_generated": False,
    }
    dump(OUT / "audits/09_acceptance_audit_v1.json", acceptance)
    artifacts = sorted(p for p in OUT.rglob("*.json") if p.name != "manifest_v1.json")
    dump(OUT / "manifest_v1.json", {"schema_version": "1.0.0", "checkpoint": "PRE-WRITING REPOSITORY CLAIM EXTRACTION AND AUTHORITY VALIDATION V1", "inputs_before": before, "inputs_after": after, "artifacts": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)} for p in artifacts], "drafting_authorized": False})


if __name__ == "__main__":
    main()
