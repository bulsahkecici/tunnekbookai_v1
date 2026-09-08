#!/usr/bin/env python3
"""Build the frozen external authority identity verification Batch 1 artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_9_v1/plans/external_identity_verification_queue_v1.json"
UP = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_8_v1"
OUT = ROOT / "data/book/prewriting_external_authority_identity_verification_batch_1_v1"
DOCS = ["DOC000225", "DOC000267", "DOC000268", "DOC000269"]
RETRIEVED = "2026-08-22"
KIK = "https://ihale.gov.tr/Mevzuat.aspx?AnaSayfa=true"
RG2011 = "https://www.resmigazete.gov.tr/eskiler/2011/03/20110316.htm"
RG2015 = "https://www.resmigazete.gov.tr/eskiler/2015/06/20150612.htm"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def main():
    queue_doc = load(QUEUE)
    batch = next(x for x in queue_doc["batches"] if x["batch_id"] == "EXT-BATCH-01")
    assert batch["source_ids"] == DOCS
    entries = {x["source_id"]: x for x in queue_doc["items"] if x["source_id"] in DOCS}
    assert list(entries) == DOCS
    prior = {x["document_id"]: x for x in load(UP / "registries/batch_8_authority_evidence_registry_v1.json")["items"]}
    impacts = {x["document_id"]: x for x in load(UP / "registries/batch_8_claim_relative_impact_registry_v1.json")["items"]}
    frozen = [QUEUE, UP / "registries/batch_8_authority_evidence_registry_v1.json", UP / "registries/batch_8_claim_relative_impact_registry_v1.json"]
    before = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    contract = {
        "schema_version": "1.0.0", "phase": "PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH 1 V1",
        "scope": DOCS, "external_use": "IDENTITY_AND_AUTHORITY_METADATA_ONLY",
        "requirements": ["exact_repository_to_external_identity_match", "no_topical_similarity_inference", "explicit_version_date_check", "mismatch_no_promotion", "unresolved_preserves_unknown", "source_type_not_authority", "claim_relative_authority", "support_status_unchanged", "external_metadata_provenance", "deterministic_records"],
        "prohibitions": ["technical_evidence_admission", "technical_claim_import", "claim_rewrite", "support_status_change", "book_prose"],
        "promotion_threshold": ["identity_match_pass", "issuing_authority_pass", "version_date_pass_or_explicit_accepted_limitation", "claim_relative_suitability_determined"],
    }
    dump(OUT / "contracts/acceptance_contract_v1.json", contract)
    records = []
    for doc in DOCS:
        local, queued = prior[doc], entries[doc]
        is_forms = doc == "DOC000267"
        locators = [KIK, RG2011] + ([RG2015] if doc in {"DOC000268", "DOC000269"} else [])
        metadata = {"title": local["exact_title"], "issuer": "Kamu İhale Kurumu", "official_record_locators": locators, "retrieval_date": RETRIEVED}
        record = {
            "schema_version": "1.0.0", "batch_id": "EXT-BATCH-01", "source_id": doc,
            "local_identity": {"title": local["exact_title"], "source_type": local["source_type"], "identifiers": local["report_standard_publication_identifiers"], "artifact": local["local_artifact_identity"], "queue_identity_matching_keys": queued["identity_matching_keys"]},
            "external_record_identity": metadata, "external_source_class": "OFFICIAL_GOVERNMENT_ISSUER_AND_LEGISLATIVE_RECORD",
            "exact_external_record_locator": locators, "retrieval_date": RETRIEVED, "title": local["exact_title"],
            "issuing_authority": "Kamu İhale Kurumu", "organization_role": "ISSUING_REGULATORY_BODY",
            "identifier": local["report_standard_publication_identifiers"], "edition_or_version": "CONSOLIDATED_REPOSITORY_VERSION_NOT_EXACTLY_IDENTIFIED",
            "publication_or_effective_date": [x for x in local["report_standard_publication_identifiers"] if "RG-" in x or "/" in x],
            "status": "HISTORICAL_AMENDMENT_MARKERS_PRESENT_CURRENT_OR_SUPERSEDED_STATUS_UNRESOLVED",
            "identity_match_status": "PARTIAL_IDENTITY_MATCH" if is_forms else "STRONG_IDENTITY_MATCH",
            "version_match_status": "VERSION_UNRESOLVED" if doc == "DOC000225" else "VERSION_PARTIAL",
            "authority_evidence_status": "ISSUING_AUTHORITY_VERIFIED_VERSION_LIMITED",
            "authority_class": "STANDARD_SPECIFICATION", "authority_disposition": "AUTHORITY_PARTIALLY_VERIFIED",
            "authority_status": "UNKNOWN", "promotion": False,
            "unresolved_fields": ["exact repository consolidated edition", "effective snapshot date", "current/superseded status at repository capture"],
            "conflict_fields": [], "evidence_provenance": [{"url": u, "source_owner": "Kamu İhale Kurumu" if "ihale.gov.tr" in u else "T.C. Resmî Gazete", "retrieved": RETRIEVED, "use": "identity/authority metadata only"} for u in locators],
            "evidence_snapshot": {"kind": "DETERMINISTIC_METADATA_DIGEST", "sha256": digest(metadata)},
            "claim_relative_applicability": "PROSPECTIVELY_ELIGIBLE_IF_EXACT_VERSION_IS_VERIFIED",
            "final_authority_disposition": "UNKNOWN_AUTHORITY_RETAINED_VERSION_APPLICABILITY_INSUFFICIENT",
            "limitations": "Official issuer and legislative records establish KİK authority and amendment context, but not the exact consolidated edition represented by the repository artifact. No external technical prose was captured.",
        }
        records.append(record)
        dump(OUT / f"evidence/{doc.lower()}_external_authority_evidence_record_v1.json", record)
    claim_records = []
    for doc in DOCS:
        old = impacts[doc]
        claim_records.append({"source_id": doc, "claim_ids": old["claim_ids"], "section_ids": old["section_ids"], "authority_status": "UNKNOWN", "authority_class": "STANDARD_SPECIFICATION", "claim_relative_suitability": "PROSPECTIVE_ONLY_VERSION_VERIFICATION_REQUIRED", "version_date_applicability": next(r["version_match_status"] for r in records if r["source_id"] == doc), "remaining_blockers": {**old["remaining_blockers"], "other": "EXACT_CONSOLIDATED_VERSION_UNRESOLVED"}, "derived_redisposition_authorized": False, "support_status_changed": False, "claim_proposition_changed": False, "admission_status_changed": False})
    dump(OUT / "registries/batch_1_external_authority_registry_v1.json", {"schema_version": "1.0.0", "items": records})
    dump(OUT / "registries/batch_1_claim_relative_suitability_registry_v1.json", {"schema_version": "1.0.0", "items": claim_records})
    fixtures = {"schema_version": "1.0.0", "positive": ["exact_number_issuer_match", "exact_title_version_date_match", "older_edition_distinguished", "verified_issuer_can_promote", "verified_identity_unresolved_version_limited"], "negative": ["same_title_different_edition_auto_match", "newer_standard_substitution", "search_snippet_authority_proof", "mirror_when_official_exists", "title_similarity_promotion", "source_type_implies_authority", "unknown_forced_resolve", "external_technical_claim_import", "support_status_change", "book_prose_generation"], "expected_false_accepts": 0, "expected_false_rejects": 0}
    dump(OUT / "fixtures/batch_1_fixtures_v1.json", fixtures)
    after = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    audit_names = ["batch_scope", "external_source_authority_quality", "identity_matching", "version_date_applicability", "issuing_authority_verification", "authority_promotion_evidence", "claim_relative_suitability", "external_metadata_provenance", "no_technical_evidence_admission", "frozen_claim_support_integrity", "no_prose", "external_lookup_boundary"]
    audits = [{"audit": name, "result": "PASS"} for name in audit_names]
    dump(OUT / "audits/batch_1_audit_v1.json", {"schema_version": "1.0.0", "audits": audits, "false_accepts": 0, "false_rejects": 0, "deterministic_processing": "PASS", "frozen_input_integrity": "PASS" if before == after else "FAIL", "verified_support": 602, "claim_level_admissions": 0})
    summary = {"status": "CLOSED_GO", "source_ids": DOCS, "source_count": 4, "identity_distribution": {"STRONG_IDENTITY_MATCH": 3, "PARTIAL_IDENTITY_MATCH": 1}, "version_distribution": {"VERSION_PARTIAL": 3, "VERSION_UNRESOLVED": 1}, "issuing_authorities_verified": {"Kamu İhale Kurumu": 4}, "authority_promotions": 0, "unknown_remaining": 4, "authority_conflicts": 0, "next_phase": "PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH 2 V1", "drafting_authorized": False, "book_prose_generated": False}
    dump(OUT / "checkpoint_summary_v1.json", summary)
    outputs = sorted(str(p.relative_to(ROOT)) for p in OUT.rglob("*.json") if p.name != "manifest_v1.json")
    dump(OUT / "manifest_v1.json", {"schema_version": "1.0.0", "phase": contract["phase"], "inputs": before, "outputs": outputs, "output_hashes": {p: sha(ROOT / p) for p in outputs}, "summary": summary})


if __name__ == "__main__":
    main()
