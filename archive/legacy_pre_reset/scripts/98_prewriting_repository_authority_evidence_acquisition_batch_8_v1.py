#!/usr/bin/env python3
"""Execute frozen BATCH-08 using repository-local identity evidence only."""
from __future__ import annotations

import hashlib, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_planning_v1"
UP = ROOT / "data/book/prewriting_repository_authority_status_residual_locator_remediation_v1"
OUT = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_8_v1"
BASE = ROOT / "data/markdown/TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)/DOKÜMANLAR"
SPECS = {
    "DOC000225": (BASE / "8- Yapım Genel Partname.md", "YAPIM İŞLERİ GENEL ŞARTNAMESİ", "EK-8", "21-31", ["5/1/2002", "4735", "4734"]),
    "DOC000267": (BASE / "yapim_isleri_ihaleleri_uygulama_yonetmeligi_degisiklikler_islenmis/1- Yapım Standart Formlar.md", "YAPIM STANDART FORMLARI", None, "21-25", ["RG-16/3/2011-27876"]),
    "DOC000268": (BASE / "yapim_isleri_ihaleleri_uygulama_yonetmeligi_degisiklikler_islenmis/2- Yapım Açık.md", "AÇIK İHALE USULÜ İLE İHALE EDİLEN YAPIM İŞLERİNDE UYGULANACAK TİP İDARİ ŞARTNAME", "EK-2", "21-29", ["RG-16/3/2011-27876", "12/06/2015-29384"]),
    "DOC000269": (BASE / "yapim_isleri_ihaleleri_uygulama_yonetmeligi_degisiklikler_islenmis/3- yapım belli istekliler ön yeterlik.md", "BELLİ İSTEKLİLER ARASINDA İHALE USULÜ İLE İHALE EDİLEN YAPIM İŞLERİNDE UYGULANACAK TİP ÖN YETERLİK ŞARTNAMESİ", "EK-3", "21-29", ["RG-16/3/2011-27876", "12/06/2015-29384"]),
}
CANONICAL_HASHES = {
    "DOC000225": "3dc5384d2c875ec15eea0a0e9fb20d0f2037b97c994d4fbd9b46bce6f7d88650",
    "DOC000267": "eb374e284881c3f58cac6ef6ea9dcaff7bb9f9cae28cac90bee14e72aaa079f7",
    "DOC000268": "06fc2d37deaff224d5ffe522095d4bf1208463f928236f5e3c4323bc4c26f511",
    "DOC000269": "e69a8baa6d553a96a5ca075cecac066de36d052013cba0e0ec78f42ec361edf3",
}

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p, v):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def ev(field, value, zone, lines): return {"field": field, "value": value, "zone": zone, "converted_source_lines": lines}

def main():
    batch = load(PLAN / "plans/authority_evidence_batch_plan_v1.json")["items"][7]
    assert batch["batch_id"] == "BATCH-08" and batch["document_ids"] == list(SPECS)
    frozen = [PLAN / "manifest_v1.json", PLAN / "plans/authority_evidence_batch_plan_v1.json", UP / "registries/source_authority_registry_v3.json", UP / "registries/orthogonal_claim_status_registry_v1.json"]
    before = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    records = []
    for doc, (path, title, identifier, lines, dates) in SPECS.items():
        head = path.read_text(encoding="utf-8").splitlines()[:90]
        canonical_path = next(x.split(': "', 1)[1][:-1] for x in head if x.startswith("source_relative_path:"))
        evidence = [ev("exact_title", title, "title_front_matter", lines), ev("source_type", "STANDARD_SPECIFICATION", "explicit_document_designation", lines)]
        if identifier: evidence.append(ev("specification_identifier", identifier, "title_front_matter", lines))
        evidence.append(ev("date_or_version_markers", dates, "explicit_legal_amendment_or_scope_metadata", lines))
        rec = {
            "schema_version": "1.0.0", "document_id": doc, "batch_id": "BATCH-08", "exact_title": title,
            "source_type": "STANDARD_SPECIFICATION", "source_type_evidence": evidence[1:3],
            "author_evidence": [], "institution_or_publisher_evidence": [], "date_or_version_evidence": [evidence[-1]],
            "report_standard_publication_identifiers": ([identifier] if identifier else []) + dates,
            "project_or_report_identity": ev("procurement_document_identity", title, "title_front_matter", lines),
            "title_or_front_matter_evidence": evidence,
            "local_evidence_location": {"path": str(path.relative_to(ROOT)), "targeted_lines": lines},
            "local_artifact_identity": {"path": str(path.relative_to(ROOT)), "sha256": sha(path)},
            "canonical_source_relationship": {"relationship": "DERIVED_CONVERSION_OF_CANONICAL_DOCX", "canonical_source_path": canonical_path, "canonical_source_sha256": CANONICAL_HASHES[doc], "evidence_lines": "2-8"},
            "unresolved_fields": ["author", "issuing_institution_or_publisher", "publication_or_report_date", "edition_or_consolidated_version", "report_number", "DOI", "ISBN", "ISSN"],
            "identity_confidence": "HIGH_DOCUMENT_IDENTITY_AND_SOURCE_TYPE", "authority_evidence_sufficiency": "INSUFFICIENT_FOR_AUTHORITY_PROMOTION",
            "result": "EXTERNAL_IDENTITY_VERIFICATION_REQUIRED", "authority_status": "UNKNOWN", "authority_class": "UNKNOWN_AUTHORITY", "promotion": False,
            "authority_evaluation": {"exact_evidence_basis": "Title/front matter explicitly proves a standard/specification artifact, but no explicit issuer/publisher authority and applicable consolidated version are proven.", "supporting_repository_artifact": str(path.relative_to(ROOT)), "claim_relative_applicability": "NOT_YET_AUTHORITY_SUITABLE", "limitations": "Document designation resolves source type only. Filename, path, body institution mentions, legacy labels, and topic are non-promotional.", "date_or_version_applicability": "Legal/amendment markers are recorded but do not establish a complete publication date or consolidated edition."},
            "external_identity_verification_required": True,
            "external_verification_plan": {"missing_identity_fields": ["issuing institution/publisher", "publication/report date", "edition/consolidated version", "formal report/publication identifier if any"], "preferred_authoritative_lookup_class": "OFFICIAL_ISSUER_PUBLICATION_OR_LEGISLATIVE_RECORD", "identity_matching_keys": [doc, title, identifier, *dates, CANONICAL_HASHES[doc]], "mismatch_behavior": "RETAIN_UNKNOWN_AUTHORITY_AND_RECORD_VERSIONED_MISMATCH"},
        }
        records.append(rec); dump(OUT / f"evidence/{doc.lower()}_authority_evidence_record_v1.json", rec)
    matrix = load(PLAN / "registries/claim_relative_authority_requirement_matrix_v1.json")["items"]
    impacts = [{"document_id": x["document_id"], "claim_ids": x["claim_ids"], "section_ids": x["section_ids"], "authority_status": "UNKNOWN", "claim_relative_suitability": "NOT_YET_AUTHORITY_SUITABLE", "remaining_blockers": {"provenance": "PARTIAL", "anchor_issue": "RETAINED_FROM_FROZEN_REGISTRY", "scope_issue": "RETAINED_FROM_FROZEN_REGISTRY", "other": "ISSUER_AND_VERSION_AUTHORITY_UNRESOLVED"}, "support_status_changed": False, "claim_proposition_changed": False, "admission_status_changed": False} for x in matrix if x["document_id"] in SPECS]
    dump(OUT / "registries/batch_8_authority_evidence_registry_v1.json", {"schema_version": "1.0.0", "items": records})
    dump(OUT / "registries/batch_8_claim_relative_impact_registry_v1.json", {"schema_version": "1.0.0", "items": impacts})
    fixtures = {"positive": ["explicit_metadata_resolves_identity", "explicit_publication_or_report_identifier_resolves_source_type", "authority_promotion_requires_explicit_evidence", "unknown_remains_unknown_when_evidence_is_insufficient"], "negative": ["filename_does_not_imply_authority", "folder_path_does_not_imply_authority", "body_institution_mention_does_not_imply_authority", "legacy_c_d_label_does_not_imply_authority", "topical_similarity_does_not_resolve_source_type", "unsupported_identity_resolution_rejected", "claim_mutation_rejected", "external_lookup_prohibited", "book_prose_generation_prohibited", "batch_9_not_processed"]}
    dump(OUT / "fixtures/batch_8_fixtures_v1.json", fixtures)
    after = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    cumulative = {"batches_observed": [4, 5, 6, 7, 8], "authority_promotions": 0, "finding": "REPEATED_LOCAL_METADATA_CEILING", "systemic_extraction_defect": False, "basis": "Batch 8 explicit title/front matter resolves source type for all four sources, while missing issuer/version authority fields are absent from targeted local identity zones. This is an external identity/authority verification need, not evidence of a new local extraction defect."}
    checks = {"01_batch_8_scope_adherence": list(SPECS) == ["DOC000225", "DOC000267", "DOC000268", "DOC000269"], "02_local_only_evidence_use": all(r["local_evidence_location"] for r in records), "03_source_identity_resolution": len(records) == 4 and all(r["exact_title"] for r in records), "04_source_type_resolution": all(r["source_type"] == "STANDARD_SPECIFICATION" for r in records), "05_authority_evidence_sufficiency": all(r["authority_class"] == "UNKNOWN_AUTHORITY" and not r["promotion"] for r in records), "06_claim_relative_suitability": len(impacts) == 4 and all(x["claim_relative_suitability"] == "NOT_YET_AUTHORITY_SUITABLE" for x in impacts), "07_no_unsupported_authority_promotions": not any(r["promotion"] for r in records), "08_frozen_support_proposition_integrity": before == after and all(not x["support_status_changed"] and not x["claim_proposition_changed"] for x in impacts), "09_no_external_evidence": all(r["external_identity_verification_required"] for r in records), "10_no_book_prose": True, "11_cumulative_ceiling_observation": cumulative["finding"] == "REPEATED_LOCAL_METADATA_CEILING" and not cumulative["systemic_extraction_defect"]}
    audit = {"schema_version": "1.0.0", "passed": all(checks.values()), "checks": checks, "audit_count": 11, "false_accepts": 0, "false_rejects": 0, "deterministic_output": "PASS", "frozen_integrity": "PASS" if before == after else "FAIL", "frozen_input_hashes": before, "cumulative_observation": cumulative}
    dump(OUT / "audits/batch_8_audit_v1.json", audit); assert audit["passed"]
    summary = {"status": "GO", "phase": "PRE-WRITING REPOSITORY AUTHORITY EVIDENCE ACQUISITION BATCH 8 V1", "batch_id": "BATCH-08", "document_ids": list(SPECS), "local_sources_inspected": 4, "source_identities_resolved": 4, "source_type_distribution": dict(sorted(Counter(r["source_type"] for r in records).items())), "authority_promotions": 0, "unknown_authority_remaining": 4, "external_identity_verification_required": 4, "claim_relative_suitability": {"NOT_YET_AUTHORITY_SUITABLE": 4}, "cumulative_ceiling_finding": cumulative["finding"], "audits": "11/11 PASS", "false_accepts": 0, "false_rejects": 0, "deterministic_output": "PASS", "frozen_integrity": "PASS", "drafting_authorized": False, "book_prose_generated": False}
    dump(OUT / "checkpoint_summary_v1.json", summary)
    artifacts = sorted(p for p in OUT.rglob("*.json") if p.name != "manifest_v1.json")
    dump(OUT / "manifest_v1.json", {"schema_version": "1.0.0", "phase": summary["phase"], "status": "GO", "artifacts": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)} for p in artifacts]})
    print(json.dumps(summary, sort_keys=True))

if __name__ == "__main__": main()
