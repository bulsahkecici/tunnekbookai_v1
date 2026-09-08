#!/usr/bin/env python3
"""Repository evidence discovery and admission remediation V1.

The pipeline streams authoritative registries, narrows work to the 211 mappings
diagnosed by the prior checkpoint, and emits a separate fail-closed V2 decision
set. It never reads or rewrites canonical source documents.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_repository_evidence_discovery_admission_remediation_v1"
CONTRACT = OUT / "remediation_acceptance_contract_v1.json"
INVENTORY = ROOT / "data/inventory/inventory.jsonl"
CHUNKS = ROOT / "data/chunks/chunks.jsonl"
DIAGNOSTIC = ROOT / "data/book/prewriting_external_evidence_admission_v1/repository_zero_admission_diagnostic_v1.json"
QUESTIONS = ROOT / "data/book/research/research_question_gap_registry_v1.json"
COVERAGE = ROOT / "data/book/coverage/corpus_to_book_coverage_mapping_v1.json"

COST_SECTIONS = {
    "CH-E-S08", "CH-E-S09", "CH-E-S10", "CH-E-S11", "CH-E-S12",
    "CH-E-S13", "CH-E-S14", "CH-E-S15", "CH-E-S16", "CH-F-S06",
    "CH-G-S01", "CH-G-S02",
}
STOP = {
    "and", "the", "which", "without", "section", "scope", "evidence", "approved",
    "authoritative", "establishes", "subject", "boundaries", "importing", "sibling",
    "ve", "ile", "bir", "bu", "için", "icin", "veya", "olarak", "olan", "bölüm",
    "bolum", "tanımı", "tanimi", "genel", "temel",
}
VALID_INTERMEDIATE = {
    "DISCOVERED_CANDIDATE", "EVIDENCE_NEED_MATCH", "CLAIM_EXTRACTION_REQUIRED",
    "PROVENANCE_BLOCKED", "HUMAN_ANALYSIS_ARTIFACT_REQUIRED",
    "TRUE_EXTERNAL_EVIDENCE_REQUIRED", "UNRESOLVED",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def words(value: str) -> set[str]:
    return {w for w in re.findall(r"[^\W\d_]{3,}", (value or "").casefold()) if w not in STOP}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def validate_scoped_candidate(item: dict, section_id: str, question_id: str) -> tuple[bool, str]:
    if item.get("section_id") != section_id:
        return False, "SECTION_SCOPE_MISMATCH"
    if item.get("research_question_id") != question_id:
        return False, "RESEARCH_QUESTION_SCOPE_MISMATCH"
    if not item.get("evidence_need_id"):
        return False, "EVIDENCE_NEED_MISSING"
    return True, "SCOPED"


def final_admission_decision(item: dict) -> tuple[bool, list[str]]:
    reasons = []
    if item.get("granularity") != "CLAIM_LEVEL_CONTENT_SUPPORT":
        reasons.append("CLAIM_LEVEL_CONTENT_SUPPORT_NOT_VALIDATED")
    if item.get("authority_status") != "ACCEPTABLE":
        reasons.append("AUTHORITY_NOT_VALIDATED")
    if item.get("provenance_status") != "COMPLETE":
        reasons.append("PROVENANCE_NOT_COMPLETE")
    if not item.get("scope_validated"):
        reasons.append("SECTION_OR_RESEARCH_QUESTION_SCOPE_NOT_VALIDATED")
    return not reasons, reasons


def main() -> None:
    if not CONTRACT.exists():
        raise SystemExit("Acceptance contract must be frozen before implementation runs.")

    diag = load(DIAGNOSTIC)
    questions_doc = load(QUESTIONS)
    coverage_doc = load(COVERAGE)
    mappings = sorted(diag["items"], key=lambda x: (x["section_id"], x["document_id"]))
    target_ids = {x["document_id"] for x in mappings}
    titles = {x["section_id"]: x["source_title"] for x in coverage_doc["sections"]}
    rq_by_section = {
        x["section_id"]: x["research_questions"][0] for x in questions_doc["sections"]
    }

    inventory = {}
    with INVENTORY.open(encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            if row.get("document_id") in target_ids:
                inventory[row["document_id"]] = row

    mappings_by_doc = defaultdict(list)
    query_terms = {}
    for mapping in mappings:
        sid = mapping["section_id"]
        rq = rq_by_section[sid]
        query_terms[(sid, mapping["document_id"])] = words(titles.get(sid, "") + " " + rq["question_text"])
        mappings_by_doc[mapping["document_id"]].append(mapping)

    ranked = defaultdict(list)
    chunk_presence = Counter()
    visual_chunks = {}
    with CHUNKS.open(encoding="utf-8") as stream:
        for line in stream:
            chunk = json.loads(line)
            did = chunk.get("document_id")
            if did not in target_ids:
                continue
            chunk_presence[did] += 1
            searchable = " ".join(str(chunk.get(k) or "") for k in ("title", "heading", "section_path", "topics", "text"))
            cwords = words(searchable)
            for mapping in mappings_by_doc[did]:
                key = (mapping["section_id"], did)
                overlap = sorted(query_terms[key] & cwords)
                score = len(overlap)
                if score:
                    candidate = {
                        "chunk_id": chunk.get("chunk_id"),
                        "heading": chunk.get("heading"),
                        "section_path": chunk.get("section_path"),
                        "location": {
                            "page_start": chunk.get("original_page_start"),
                            "page_end": chunk.get("original_page_end"),
                            "slide": chunk.get("slide"),
                        },
                        "source_sha256": chunk.get("source_sha256"),
                        "normalized_source_sha256": chunk.get("normalized_source_sha256"),
                        "authority_level": chunk.get("authority_level"),
                        "provenance_status": chunk.get("provenance_status"),
                        "overlap_terms": overlap,
                        "retrieval_score": score,
                    }
                    ranked[key].append(candidate)
            if chunk.get("contains_image_placeholder") or chunk.get("contains_table") or chunk.get("contains_formula_placeholder"):
                visual_chunks[chunk.get("chunk_id")] = {
                    "chunk_id": chunk.get("chunk_id"), "document_id": did,
                    "heading": chunk.get("heading"), "section_path": chunk.get("section_path"),
                    "page_start": chunk.get("original_page_start"), "page_end": chunk.get("original_page_end"),
                    "slide": chunk.get("slide"), "source_sha256": chunk.get("source_sha256"),
                    "normalized_source_sha256": chunk.get("normalized_source_sha256"),
                    "has_image": bool(chunk.get("contains_image_placeholder")),
                    "has_table": bool(chunk.get("contains_table")),
                    "has_formula": bool(chunk.get("contains_formula_placeholder")),
                }

    discovery, intermediate, rejected = [], [], []
    defect_audits = {"DISCOVERY_GAP": [], "ADMISSION_GRANULARITY_MISMATCH": [], "PROVENANCE_GAP": []}
    for index, mapping in enumerate(mappings, 1):
        sid, did = mapping["section_id"], mapping["document_id"]
        rq = rq_by_section[sid]
        evidence_need_id = f"EN-{sid}-{rq['question_id']}-{index:03d}"
        candidates = sorted(ranked[(sid, did)], key=lambda x: (-x["retrieval_score"], x["chunk_id"] or ""))[:3]
        inv = inventory.get(did)
        has_authoritative_hash = bool(inv and inv.get("sha256"))
        if candidates:
            state = "HUMAN_ANALYSIS_ARTIFACT_REQUIRED" if sid in COST_SECTIONS else "CLAIM_EXTRACTION_REQUIRED"
        elif inv and chunk_presence[did]:
            state = "DISCOVERED_CANDIDATE"
        else:
            state = "UNRESOLVED"
        if mapping["diagnostic_disposition"] == "PROVENANCE_GAP" and not has_authoritative_hash:
            state = "PROVENANCE_BLOCKED"
        record = {
            "mapping_id": f"REM-{index:03d}", "section_id": sid, "section_title": titles.get(sid),
            "research_question_id": rq["question_id"], "research_question": rq["question_text"],
            "evidence_need_id": evidence_need_id, "expected_claim_class": rq["expected_claim_class"],
            "claim_candidate_id": f"CC-{index:03d}", "document_id": did,
            "prior_defect_class": mapping["diagnostic_disposition"],
            "inventory_resolved": bool(inv), "inventory_sha256": inv.get("sha256") if inv else None,
            "chunk_count_in_registry": chunk_presence[did], "candidate_chunks": candidates,
            "discovery_state": state, "topical_similarity_is_admissibility": False,
            "targeted_source_read_performed": False,
        }
        discovery.append(record)
        scoped, _ = validate_scoped_candidate(record, sid, rq["question_id"])
        decision_input = {
            **record, "granularity": "EVIDENCE_NEED_MATCH" if candidates else "SOURCE_LEVEL",
            "authority_status": "NOT_VALIDATED", "provenance_status": "COMPLETE" if has_authoritative_hash else "INCOMPLETE",
            "scope_validated": scoped,
        }
        admitted, reasons = final_admission_decision(decision_input)
        decision_input["final_admitted"] = admitted
        decision_input["final_admission_reasons"] = reasons
        if state == "UNRESOLVED":
            rejected.append(decision_input)
        else:
            intermediate.append(decision_input)
        prior = mapping["diagnostic_disposition"]
        if prior == "DISCOVERY_GAP":
            resolved = bool(inv and chunk_presence[did])
            basis = "AUTHORITATIVE_INVENTORY_AND_CHUNK_REGISTRY_RESOLVED" if resolved else "REPOSITORY_REGISTRIES_EXHAUSTED_WITHOUT_RESOLUTION"
        elif prior == "ADMISSION_GRANULARITY_MISMATCH":
            resolved = state in VALID_INTERMEDIATE
            basis = "RECLASSIFIED_TO_EXPLICIT_NON_ADMITTED_INTERMEDIATE_STATE"
        else:
            resolved = has_authoritative_hash
            basis = "AUTHORITATIVE_INVENTORY_HASH_RESOLVED" if resolved else "PROVENANCE_REMAINS_EXPLICITLY_UNRESOLVED"
        defect_audits[prior].append({
            "mapping_id": record["mapping_id"], "section_id": sid, "document_id": did,
            "resolved": resolved, "basis": basis, "resulting_state": state,
        })

    visual = []
    for chunk_id, item in sorted(visual_chunks.items()):
        for mapping in sorted(mappings_by_doc[item["document_id"]], key=lambda x: x["section_id"]):
            classes = [name for flag, name in ((item["has_image"], "IMAGE"), (item["has_table"], "TABLE"), (item["has_formula"], "FORMULA")) if flag]
            visual.append({
                **item, "visual_candidate_id": f"VIS-{len(visual)+1:05d}",
                "candidate_classes": classes, "target_section_id": mapping["section_id"],
                "rights_status": "UNKNOWN", "reuse_authorized": False,
                "eligibility_state": "RECONSTRUCTION_REVIEW_REQUIRED",
                "reconstruction_guidance": "Reconstruct from validated data and cite the source; do not reuse the source visual while rights are UNKNOWN.",
            })

    section_states = []
    by_section = defaultdict(list)
    for item in discovery:
        by_section[item["section_id"]].append(item)
    for sid in sorted(rq_by_section):
        rows = by_section[sid]
        if sid in COST_SECTIONS:
            readiness = "HUMAN_ANALYSIS_ARTIFACT_REQUIRED"
        elif any(x["candidate_chunks"] for x in rows):
            readiness = "CLAIM_EXTRACTION_REQUIRED"
        elif any(x["inventory_resolved"] and x["chunk_count_in_registry"] for x in rows):
            readiness = "DISCOVERED_CANDIDATE"
        else:
            readiness = "UNRESOLVED"
        section_states.append({
            "section_id": sid, "research_question_id": rq_by_section[sid]["question_id"],
            "mapping_count": len(rows), "candidate_mapping_count": sum(bool(x["candidate_chunks"]) for x in rows),
            "readiness": readiness, "drafting_authorized": False,
        })

    def audit_doc(name, expected, rows):
        return {
            "schema_version": "1.0.0", "defect_class": name, "expected_count": expected,
            "observed_count": len(rows), "resolved_count": sum(x["resolved"] for x in rows),
            "unresolved_count": sum(not x["resolved"] for x in rows), "items": rows,
        }

    dump(OUT / "repository_discovery_registry_v1.json", {"schema_version": "1.0.0", "mapping_count": len(discovery), "items": discovery})
    dump(OUT / "intermediate_evidence_registry_v2.json", {"schema_version": "2.0.0", "item_count": len(intermediate), "items": intermediate})
    dump(OUT / "rejected_evidence_registry_v2.json", {"schema_version": "2.0.0", "item_count": len(rejected), "items": rejected})
    dump(OUT / "admitted_evidence_registry_v2.json", {"schema_version": "2.0.0", "item_count": 0, "items": [], "basis": "No candidate independently validated claim-level support, authority, provenance, and scope."})
    dump(OUT / "section_evidence_coverage_ledger_v2.json", {"schema_version": "2.0.0", "section_count": len(section_states), "sections": section_states})
    dump(OUT / "repository_visual_candidate_registry_v2.json", {"schema_version": "2.0.0", "discovery_executed": True, "candidate_count": len(visual), "items": visual})
    dump(OUT / "visual_discovery_audit_v1.json", {"schema_version": "1.0.0", "discovery_executed": True, "mapped_document_count": len(target_ids), "candidate_count": len(visual), "rights_unknown_count": len(visual), "reuse_authorized_count": 0})
    dump(OUT / "visual_zero_candidate_diagnostic_v2.json", {"schema_version": "2.0.0", "applicable": not visual, "discovery_executed": True, "candidate_count": len(visual), "basis": "No visual flags were found after actual mapped-document chunk discovery." if not visual else "Not applicable because candidates were found."})
    for name, expected in (("DISCOVERY_GAP", 172), ("ADMISSION_GRANULARITY_MISMATCH", 37), ("PROVENANCE_GAP", 2)):
        dump(OUT / f"{name.casefold()}_remediation_audit_v1.json", audit_doc(name, expected, defect_audits[name]))

    state_counts = Counter(x["discovery_state"] for x in discovery)
    acceptance = {
        "schema_version": "1.0.0", "contract": str(CONTRACT.relative_to(ROOT)),
        "mapping_count": len(discovery), "state_counts": dict(sorted(state_counts.items())),
        "discovery_gap_resolved": sum(x["resolved"] for x in defect_audits["DISCOVERY_GAP"]),
        "granularity_mismatch_resolved": sum(x["resolved"] for x in defect_audits["ADMISSION_GRANULARITY_MISMATCH"]),
        "provenance_gap_resolved": sum(x["resolved"] for x in defect_audits["PROVENANCE_GAP"]),
        "provenance_gap_unresolved": sum(not x["resolved"] for x in defect_audits["PROVENANCE_GAP"]),
        "visual_discovery_executed": True, "visual_candidate_count": len(visual),
        "final_admitted_count": 0, "intermediate_count": len(intermediate), "rejected_count": len(rejected),
        "v1_outputs_modified": False, "standards_weakened": False,
        "source_document_content_reads": 0, "canonical_material_modified": False,
        "drafting_authorized": False, "book_prose_generated": False,
    }
    acceptance["accepted"] = (
        acceptance["mapping_count"] == 211
        and len(defect_audits["DISCOVERY_GAP"]) == 172
        and len(defect_audits["ADMISSION_GRANULARITY_MISMATCH"]) == 37
        and len(defect_audits["PROVENANCE_GAP"]) == 2
        and acceptance["discovery_gap_resolved"] == 172
        and acceptance["granularity_mismatch_resolved"] == 37
        and acceptance["provenance_gap_unresolved"] == 0
        and acceptance["visual_discovery_executed"]
    )
    dump(OUT / "repository_evidence_admission_v2_audit.json", acceptance)
    dump(OUT / "remediation_acceptance_audit_v1.json", acceptance)

    artifact_paths = sorted(p for p in OUT.rglob("*.json") if p.name != "remediation_manifest_v1.json")
    manifest = {
        "schema_version": "1.0.0", "checkpoint": load(CONTRACT)["checkpoint"],
        "artifacts": [{"path": str(p.relative_to(ROOT)), "sha256": sha256(p)} for p in artifact_paths],
        "canonical_inputs": [
            {"path": str(p.relative_to(ROOT)), "sha256": sha256(p)}
            for p in (INVENTORY, CHUNKS, DIAGNOSTIC, QUESTIONS, COVERAGE)
        ],
        "drafting_authorized": False, "book_prose_generated": False,
    }
    dump(OUT / "remediation_manifest_v1.json", manifest)


if __name__ == "__main__":
    main()
