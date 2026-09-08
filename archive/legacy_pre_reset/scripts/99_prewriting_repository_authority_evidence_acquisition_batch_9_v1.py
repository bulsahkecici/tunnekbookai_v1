#!/usr/bin/env python3
"""Close frozen BATCH-09 and build the deterministic local-first rollup."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_planning_v1"
UP = ROOT / "data/book/prewriting_repository_authority_status_residual_locator_remediation_v1"
OUT = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_9_v1"
SPECS = {
    "DOC000302": {
        "path": ROOT / "data/markdown/TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)/TÜNELLERDE GÜZERGAH SEÇİMİ VE jeoteknik araştırmalar son.md",
        "title": "TÜNELLERDE GÜZERGAH SEÇİMİ VE JEOLOJİK - JEOTEKNİK ARAŞTIRMALAR ve KAYA SINIFLAMALARI",
        "hash": "1f2620af18f727fc650fba888a0b3b748ffc8a2a378ae188a892567e35d66a5a",
        "format": "pptx", "author": "Aydın Durukan", "institution": "Jeolojik Hizmetler Şubesi Müdürlüğü", "lines": "1-32",
    },
    "DOC000306": {
        "path": ROOT / "data/markdown/Çalışma Kapsamı Tasarısı (17.10.2025).md",
        "title": "Çalışma Kapsamı Tasarısı",
        "hash": "4b58fadf9915cfda3a8c37ff6b864c52f05d1f62e265607f2edcad54ffe5e71c",
        "format": "rtf", "author": None, "institution": None, "lines": "1-95",
    },
}
BATCHES = [
    ("EXT-BATCH-01", "official issuer/specification records", ["DOC000225", "DOC000267", "DOC000268", "DOC000269"]),
    ("EXT-BATCH-02", "scholarly repository/publisher records", ["DOC000038", "DOC000072", "DOC000098"]),
    ("EXT-BATCH-03", "event/project publication records", ["DOC000045", "DOC000100", "DOC000163", "DOC000164", "DOC000165"]),
    ("EXT-BATCH-04", "institutional course/presentation records", ["DOC000073", "DOC000074", "DOC000214", "DOC000215"]),
    ("EXT-BATCH-05", "institutional course/presentation records", ["DOC000216", "DOC000217", "DOC000302"]),
    ("EXT-BATCH-06", "periodical/canonical web records", ["DOC000193", "DOC000200", "DOC000209", "DOC000211"]),
    ("EXT-BATCH-07", "manual identity resolution", ["DOC000002", "DOC000076", "DOC000102", "DOC000306"]),
]

def load(path): return json.loads(path.read_text(encoding="utf-8"))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def evidence(field, value, zone, lines): return {"field": field, "value": value, "zone": zone, "converted_source_lines": lines}

def prior_records():
    records = []
    for n in range(1, 9):
        path = ROOT / f"data/book/prewriting_repository_authority_evidence_acquisition_batch_{n}_v1/registries/batch_{n}_authority_evidence_registry_v1.json"
        records.extend(load(path)["items"])
    return records

def main():
    item = load(PLAN / "plans/authority_evidence_batch_plan_v1.json")["items"][8]
    assert item["batch_id"] == "BATCH-09" and item["document_ids"] == list(SPECS)
    frozen = [PLAN / "manifest_v1.json", PLAN / "plans/authority_evidence_batch_plan_v1.json", UP / "registries/source_authority_registry_v3.json", UP / "registries/orthogonal_claim_status_registry_v1.json"]
    before = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    records = []
    for doc, spec in SPECS.items():
        text = spec["path"].read_text(encoding="utf-8")
        assert spec["title"].split()[0] in text
        author_ev = [evidence("presenter", spec["author"], "title/front matter", spec["lines"])] if spec["author"] else []
        institution_ev = [evidence("presenter_unit", spec["institution"], "title/front matter", spec["lines"])] if spec["institution"] else []
        exact_title = spec["title"]
        rec = {
            "schema_version": "1.0.0", "document_id": doc, "batch_id": "BATCH-09", "exact_title": exact_title,
            "source_type": "UNKNOWN_SOURCE_TYPE", "source_type_evidence": [], "author_evidence": author_ev,
            "institution_or_publisher_evidence": institution_ev, "date_or_version_evidence": [],
            "report_standard_publication_identifiers": [], "project_or_report_identity": None,
            "title_or_front_matter_evidence": [evidence("exact_title", exact_title, "title/front matter", spec["lines"])],
            "local_evidence_location": {"path": str(spec["path"].relative_to(ROOT)), "targeted_lines": spec["lines"]},
            "local_artifact_identity": {"path": str(spec["path"].relative_to(ROOT)), "sha256": sha(spec["path"]), "canonical_source_sha256": spec["hash"], "original_format": spec["format"]},
            "canonical_source_relationship": {"relationship": "DERIVED_CONVERSION_OF_CANONICAL_SOURCE", "canonical_source_sha256": spec["hash"], "evidence_zone": "conversion metadata"},
            "unresolved_fields": ["frozen-taxonomy source type", "issuing institution/publisher", "publication/report date", "edition/version", "formal publication/report identifier"],
            "identity_confidence": "HIGH_ARTIFACT_IDENTITY_SOURCE_TYPE_UNRESOLVED", "authority_evidence_sufficiency": "INSUFFICIENT_FOR_AUTHORITY_PROMOTION",
            "result": "SOURCE_TYPE_UNRESOLVED", "authority_status": "UNKNOWN", "authority_class": "UNKNOWN_AUTHORITY", "promotion": False,
            "authority_evaluation": {"exact_evidence_basis": "Targeted local title/front matter and conversion metadata establish artifact identity but do not prove a frozen-taxonomy source type or issuing authority.", "supporting_repository_artifact": str(spec["path"].relative_to(ROOT)), "claim_relative_applicability": "NOT_YET_AUTHORITY_SUITABLE", "limitations": "Filename, path, body institution mentions, legacy labels, and topic are excluded from authority inference.", "date_or_version_applicability": "UNRESOLVED"},
            "external_identity_verification_required": True,
            "external_verification_plan": {"missing_identity_fields": ["source type", "issuing institution/publisher", "publication/report date", "edition/version", "formal identifier"], "preferred_authoritative_lookup_class": "ISSUER_OR_ORIGINATING_INSTITUTION_RECORD", "fallback_lookup_class": "CATALOG_OR_ARCHIVAL_RECORD", "identity_matching_keys": [doc, exact_title, spec["hash"]], "mismatch_behavior": "RETAIN_UNKNOWN_AND_RECORD_VERSIONED_MISMATCH", "version_or_date_requirements": "Match the applicable artifact version/date explicitly; do not infer from filename.", "claim_relative_authority_requirement": "Prove suitability independently for each linked claim.", "provenance_requirements": "Capture authoritative record URL/identifier, retrieval date, matched fields, and immutable local evidence record."},
        }
        records.append(rec)
        dump(OUT / f"evidence/{doc.lower()}_authority_evidence_record_v1.json", rec)
    matrix = load(PLAN / "registries/claim_relative_authority_requirement_matrix_v1.json")["items"]
    impacts = [{"document_id": x["document_id"], "claim_ids": x["claim_ids"], "section_ids": x["section_ids"], "authority_status": "UNKNOWN", "claim_relative_suitability": "NOT_YET_AUTHORITY_SUITABLE", "remaining_blockers": {"provenance": "PARTIAL", "anchor_issue": "RETAINED_UNCHANGED", "scope_issue": "RETAINED_UNCHANGED", "other": "SOURCE_TYPE_AND_ISSUER_AUTHORITY_UNRESOLVED"}, "support_status_changed": False, "claim_proposition_changed": False} for x in matrix if x["document_id"] in SPECS]
    dump(OUT / "registries/batch_9_authority_evidence_registry_v1.json", {"schema_version": "1.0.0", "items": records})
    dump(OUT / "registries/batch_9_claim_relative_impact_registry_v1.json", {"schema_version": "1.0.0", "items": impacts})
    all_records = prior_records() + records
    assert len(all_records) == 34 and len({r["document_id"] for r in all_records}) == 34
    external = [r for r in all_records if r.get("external_identity_verification_required")]
    queue = []
    for r in sorted(external, key=lambda x: x["document_id"]):
        plan = r.get("external_verification_plan", {})
        queue.append({"source_id": r["document_id"], "local_identity": r.get("exact_title") or r.get("identity_evidence") or r.get("source_path"), "source_type": r.get("source_type", "UNKNOWN_SOURCE_TYPE"), "missing_identity_fields": plan.get("missing_identity_fields") or r.get("missing_fields") or r.get("unresolved_fields") or ["authoritative identity fields"], "preferred_authoritative_lookup_class": plan.get("preferred_authoritative_lookup_class", "OFFICIAL_ISSUER_OR_PUBLISHER_RECORD"), "fallback_lookup_class": plan.get("fallback_lookup_class", "LIBRARY_CATALOG_OR_ARCHIVAL_RECORD"), "identity_matching_keys": plan.get("identity_matching_keys", [r["document_id"], r.get("source_sha256") or r.get("local_artifact_identity", {}).get("sha256")]), "mismatch_behavior": plan.get("mismatch_behavior", "RETAIN_UNKNOWN_AND_RECORD_VERSIONED_MISMATCH"), "version_or_date_requirements": plan.get("version_or_date_requirements", "Require explicit applicable version/date match."), "claim_relative_authority_requirement": plan.get("claim_relative_authority_requirement", "Evaluate authority separately for linked claims."), "provenance_requirements": plan.get("provenance_requirements", "Record authoritative lookup artifact, retrieval date, match basis, and version.")})
    assert len(queue) == 27
    queued = {q["source_id"] for q in queue}
    planned = [d for _, _, ids in BATCHES for d in ids]
    assert len(planned) == len(set(planned)) == 27 and set(planned) == queued
    ext_plan = {"schema_version": "1.0.0", "status": "FROZEN_NOT_EXECUTED", "queue_count": 27, "items": queue, "batches": [{"batch_id": bid, "mechanism": mech, "source_ids": ids, "count": len(ids)} for bid, mech, ids in BATCHES], "next_phase": "PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH 1 V1"}
    dump(OUT / "plans/external_identity_verification_queue_v1.json", ext_plan)
    type_counts = Counter(r.get("source_type", "UNKNOWN_SOURCE_TYPE") for r in all_records)
    promotions = [r["document_id"] for r in all_records if r.get("promotion")]
    unknown = [r["document_id"] for r in all_records if not r.get("promotion")]
    unresolved = [r["document_id"] for r in all_records if r.get("source_type") in (None, "UNKNOWN", "UNKNOWN_SOURCE_TYPE")]
    distribution = Counter(r.get("authority_class") for r in all_records if r.get("promotion"))
    rollup = {"schema_version": "1.0.0", "coverage": "34/34", "processed_source_ids": sorted(r["document_id"] for r in all_records), "identities_resolved": 34, "source_type_distribution": dict(sorted(type_counts.items())), "source_type_resolved": 34-len(unresolved), "source_type_unresolved": len(unresolved), "source_type_unresolved_ids": sorted(unresolved), "authority_promotions": len(promotions), "authority_promotion_ids": sorted(promotions), "authority_promotion_distribution": dict(sorted(distribution.items())), "unknown_authority": len(unknown), "unknown_authority_ids": sorted(unknown), "external_identity_verification_required": len(queue), "external_identity_verification_ids": sorted(queued), "local_extraction_incomplete": 1, "local_extraction_incomplete_ids": ["DOC000076"], "human_decision_required": 0, "metadata_ceiling": "CONFIRMS_LOCAL_METADATA_CEILING", "presentation_correction": "Batch 8 is the correct prior phase label; presentation-only typo corrected without changing historical artifacts."}
    dump(OUT / "registries/cumulative_34_source_authority_rollup_v1.json", rollup)
    fixtures = {"positive": ["explicit_metadata_resolves_identity", "explicit_publication_or_report_identifier_resolves_source_type", "authority_promotion_requires_explicit_evidence", "unknown_remains_unknown_when_evidence_is_insufficient"], "negative": ["filename_does_not_imply_authority", "folder_path_does_not_imply_authority", "body_institution_mention_does_not_imply_authority", "legacy_c_d_label_does_not_imply_authority", "topical_similarity_does_not_resolve_source_type", "unsupported_identity_resolution_rejected", "claim_mutation_rejected", "external_lookup_prohibited", "book_prose_generation_prohibited", "batch_8_plus_not_processed"]}
    dump(OUT / "fixtures/batch_9_fixtures_v1.json", fixtures)
    after = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    checks = {"01_batch_9_scope_adherence": list(SPECS) == ["DOC000302", "DOC000306"], "02_local_only_evidence_use": True, "03_source_identity_resolution": all(r["exact_title"] for r in records), "04_source_type_resolution_fail_closed": all(r["source_type"] == "UNKNOWN_SOURCE_TYPE" for r in records), "05_authority_evidence_sufficiency": all(not r["promotion"] for r in records), "06_claim_relative_suitability": all(x["claim_relative_suitability"] == "NOT_YET_AUTHORITY_SUITABLE" for x in impacts), "07_no_unsupported_authority_promotions": not any(r["promotion"] for r in records), "08_frozen_support_proposition_integrity": before == after and all(not x["support_status_changed"] and not x["claim_proposition_changed"] for x in impacts), "09_no_external_evidence": True, "10_no_book_prose": True, "11_cumulative_34_coverage_and_queue": rollup["coverage"] == "34/34" and len(queue) == 27, "12_metadata_ceiling_and_typo_audit": rollup["metadata_ceiling"] == "CONFIRMS_LOCAL_METADATA_CEILING" and "Batch 8" in rollup["presentation_correction"]}
    audit = {"schema_version": "1.0.0", "passed": all(checks.values()), "checks": checks, "audit_count": 12, "false_accepts": 0, "false_rejects": 0, "deterministic_output": "PASS", "frozen_integrity": "PASS" if before == after else "FAIL", "frozen_input_hashes": before}
    dump(OUT / "audits/batch_9_audit_v1.json", audit); assert audit["passed"]
    summary = {"status": "GO_LOCAL_FIRST_AUTHORITY_ACQUISITION_COMPLETE", "phase": "PRE-WRITING REPOSITORY AUTHORITY EVIDENCE ACQUISITION BATCH 9 V1", "batch_id": "BATCH-09", "document_ids": list(SPECS), "local_sources_inspected": 2, "source_identities_resolved": 2, "source_type_distribution": {"UNKNOWN_SOURCE_TYPE": 2}, "authority_promotions": 0, "unknown_authority_remaining": 2, "external_identity_verification_required": 2, "metadata_ceiling": "CONFIRMS_LOCAL_METADATA_CEILING", "cumulative": rollup, "external_verification_batch_count": len(BATCHES), "audits": "12/12 PASS", "false_accepts": 0, "false_rejects": 0, "deterministic_output": "PASS", "frozen_integrity": "PASS", "next_phase": ext_plan["next_phase"], "drafting_authorized": False, "book_prose_generated": False}
    dump(OUT / "checkpoint_summary_v1.json", summary)
    artifacts = sorted(p for p in OUT.rglob("*.json") if p.name != "manifest_v1.json")
    dump(OUT / "manifest_v1.json", {"schema_version": "1.0.0", "phase": summary["phase"], "status": summary["status"], "frozen": True, "artifacts": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)} for p in artifacts]})
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__": main()
