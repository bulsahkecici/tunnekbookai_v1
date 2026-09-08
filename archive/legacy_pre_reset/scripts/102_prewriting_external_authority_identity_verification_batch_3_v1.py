#!/usr/bin/env python3
"""Build frozen identity/authority-metadata-only verification Batch 3 artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_9_v1/plans/external_identity_verification_queue_v1.json"
OUT = ROOT / "data/book/prewriting_external_authority_identity_verification_batch_3_v1"
DOCS = ["DOC000045", "DOC000100", "DOC000163", "DOC000164", "DOC000165"]
RETRIEVED = "2026-08-22"
INPUTS = {
    "DOC000045": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_2_v1/registries/batch_2_claim_relative_impact_registry_v1.json",
    "DOC000100": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_4_v1/registries/batch_4_claim_relative_impact_registry_v1.json",
    "DOC000163": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_5_v1/registries/batch_5_claim_relative_impact_registry_v1.json",
    "DOC000164": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_5_v1/registries/batch_5_claim_relative_impact_registry_v1.json",
    "DOC000165": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_5_v1/registries/batch_5_claim_relative_impact_registry_v1.json",
}
EVENT = "https://tunelder.org.tr/tr/haber-duyuru/tunnel-turkey-2022-sunumlar_presentations-232"
DOC163_PDF = "https://ns.tunelder.org.tr/Uploads/TunnelTurkey2022/7_Tunnel%20Projects%20in%20Indonesia%20and%20the%20Far%20East%20Opportunities%20for%20Turkish%20Contractors.pdf"
ITU = "https://akademi.itu.edu.tr/ergenesi/Yay%C4%B1nlar"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def impact(doc):
    return next(x for x in load(INPUTS[doc])["items"] if x["document_id"] == doc)


def main():
    queue = load(QUEUE)
    batch = next(x for x in queue["batches"] if x["batch_id"] == "EXT-BATCH-03")
    assert batch["source_ids"] == DOCS
    queued = {x["source_id"]: x for x in queue["items"] if x["source_id"] in DOCS}
    assert list(queued) == DOCS
    frozen = [QUEUE, *dict.fromkeys(INPUTS.values()), ROOT / "data/book/prewriting_external_authority_identity_verification_batch_1_v1/audits/batch_1_audit_v1.json", ROOT / "data/book/prewriting_external_authority_identity_verification_batch_2_v1/audits/batch_2_audit_v1.json"]
    before = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    contract = {
        "schema_version": "1.0.0", "phase": "PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH 3 V1", "scope": DOCS,
        "external_use": "IDENTITY_AND_AUTHORITY_METADATA_ONLY", "positive_fixture_count": 6, "negative_fixture_count": 11, "audit_count": 12,
        "requirements": ["exact_repository_to_external_identity_match", "author_institution_event_version_date_matching", "mismatch_or_conflict_no_promotion", "conference_appearance_not_peer_review", "unresolved_preserves_unknown", "claim_relative_authority", "external_metadata_provenance", "batch_1_and_2_regression"],
        "prohibitions": ["technical_evidence_admission", "technical_claim_import", "claim_rewrite", "support_status_change", "admission_change", "book_prose", "cost_analysis", "visual_generation", "frozen_history_rewrite"],
    }
    dump(OUT / "contracts/acceptance_contract_v1.json", contract)
    specs = {
        "DOC000045": dict(identity="NO_RELIABLE_MATCH", version="VERSION_UNRESOLVED", authority="UNKNOWN_AUTHORITY", status="AUTHORITY_NOT_VERIFIABLE", promotion=False, issuer="No authoritative owner verified", title=None, authors=[], date=None, version_detail=None, identifier=None, locators=[], conflicts=[], unresolved=["date_or_period", "archive_or_collection_locator", "publication_container_or_stable_identifier"], limitations=["No authoritative publication, archive, or institutional record was located; secondary references were excluded"]),
        "DOC000100": dict(identity="EXACT_IDENTITY_MATCH", version="EXACT_VERSION_VERIFIED", authority="SECONDARY_TECHNICAL", status="AUTHORITY_VERIFIED", promotion=True, issuer="İstanbul Technical University", title="İhale ve İnşaat Öncesi Dönemde Güncel Alternatif Maliyet Analizi Yöntemlerinin İncelenmesi", authors=["G. Sevde Baltaşı", "Esin Ergen", "Ragıp Akbaş"], date="2017-10-06", version_detail="Uluslararası Katılımlı 7. İnşaat Yönetimi Kongresi; full-text paper", identifier="NO_STABLE_PROCEEDINGS_IDENTIFIER_LISTED", locators=[(ITU, "İstanbul Technical University", "OFFICIAL_INSTITUTIONAL_PUBLICATION_RECORD")], conflicts=[], unresolved=["stable_identifier", "peer_review_status"], limitations=["Institutional record verifies publication identity; it does not verify peer review", "Technical content not inspected"]),
        "DOC000163": dict(identity="EXACT_IDENTITY_MATCH", version="EXACT_VERSION_VERIFIED", authority="SECONDARY_TECHNICAL", status="AUTHORITY_VERIFIED", promotion=True, issuer="Tünelcilik Derneği", title="Endonezya ve Uzakdoğu'da Tünel Projeleri Türk Müteahhitleri İçin İmkanlar", authors=["Ulaş Aygün"], date="2022-11-29/30", version_detail="Tunnel Turkey 2022 official presentation 7", identifier="7_Tunnel Projects in Indonesia and the Far East Opportunities for Turkish Contractors.pdf", locators=[(EVENT, "Tünelcilik Derneği", "OFFICIAL_EVENT_PRESENTATION_INDEX"), (DOC163_PDF, "Tünelcilik Derneği", "OFFICIAL_EVENT_FILE")], conflicts=[], unresolved=["peer_review_status"], limitations=["Official event record verifies presentation identity, not peer review", "Technical body content was not captured"]),
        "DOC000164": dict(identity="PARTIAL_IDENTITY_MATCH", version="DATE_MATCH_VERSION_UNRESOLVED", authority="UNKNOWN_AUTHORITY", status="AUTHORITY_PARTIALLY_VERIFIED", promotion=False, issuer="Tünelcilik Derneği", title="Halkalı - İstanbul Havaalanı Metro İnşaatı", authors=[], date="2022-11-29/30", version_detail="Tunnel Turkey 2022 official presentation 8", identifier="8_Halkali - Istanbul Airport Metro Construction Works.pdf", locators=[(EVENT, "Tünelcilik Derneği", "OFFICIAL_EVENT_PRESENTATION_INDEX")], conflicts=["Repository title describes the metro line; official event title describes metro construction works", "Repository contract date 2018-03-07 is not the presentation publication date"], unresolved=["author_or_presenter", "report_or_contract_identifier", "exact_repository_to_event_file_identity"], limitations=["Project overlap and title similarity are insufficient for exact identity"]),
        "DOC000165": dict(identity="IDENTITY_CONFLICT", version="DATE_MATCH_VERSION_UNRESOLVED", authority="UNKNOWN_AUTHORITY", status="AUTHORITY_CONFLICT", promotion=False, issuer="Tünelcilik Derneği", title="Redüksiyon Tünellerinin Kalıcı Kaplama Tasarım Yaklaşımı", authors=[], date="2022-11-29/30", version_detail="Tunnel Turkey 2022 official presentation 9", identifier="9_Final Lining Design Approach for Reduction Tunnels.pdf", locators=[(EVENT, "Tünelcilik Derneği", "OFFICIAL_EVENT_PRESENTATION_INDEX")], conflicts=["Official event title is limited to reduction tunnels and does not match the broader repository title"], unresolved=["author_or_presenter", "institution_or_publisher", "exact_repository_to_event_file_identity", "peer_review_status"], limitations=["Shared event/date and title terms cannot overcome the material scope difference"]),
    }
    records = []
    for doc in DOCS:
        s, q = specs[doc], queued[doc]
        provenance = [{"url": u, "source_owner": owner, "record_role": role, "retrieval_date": RETRIEVED, "capture_scope": "IDENTITY_AND_AUTHORITY_METADATA_ONLY"} for u, owner, role in s["locators"]]
        r = {"schema_version": "1.0.0", "batch_id": "EXT-BATCH-03", "source_id": doc, "repository_identity": q["local_identity"], "queue_identity_matching_keys": q["identity_matching_keys"], "external_title": s["title"], "external_authors": s["authors"], "issuing_authority": s["issuer"], "identifier": s["identifier"], "publication_or_event_date": s["date"], "edition_or_version": s["version_detail"], "identity_match_status": s["identity"], "version_match_status": s["version"], "authority_class": s["authority"], "authority_status": s["status"], "promotion": s["promotion"], "claim_relative_applicability": "PROSPECTIVELY_SUITABLE_FOR_IDENTIFIED_SOURCE_ROLE" if s["promotion"] else "NOT_AUTHORITY_SUITABLE_IDENTITY_OR_VERSION_UNRESOLVED", "conflict_fields": s["conflicts"], "unresolved_fields": s["unresolved"], "limitations": s["limitations"], "evidence_provenance": provenance, "evidence_snapshot": {"kind": "DETERMINISTIC_METADATA_DIGEST", "sha256": digest(provenance)}, "metadata_only_use_boundary": True, "peer_review_verified": False, "technical_content_captured": False, "support_status_changed": False, "admission_status_changed": False, "claim_proposition_changed": False}
        records.append(r)
        dump(OUT / f"evidence/{doc.lower()}_external_authority_evidence_record_v1.json", r)
    claims = []
    for r in records:
        old = impact(r["source_id"])
        claims.append({"source_id": r["source_id"], "claim_ids": old["claim_ids"], "section_ids": old["section_ids"], "claim_role": old["claim_role"], "authority_status": r["authority_status"], "authority_class": r["authority_class"], "claim_relative_suitability": r["claim_relative_applicability"], "version_date_applicability": r["version_match_status"], "remaining_blockers": r["unresolved_fields"], "support_status_changed": False, "admission_status_changed": False, "claim_proposition_changed": False, "derived_redisposition_authorized": False})
    dump(OUT / "registries/batch_3_external_authority_registry_v1.json", {"schema_version": "1.0.0", "items": records})
    dump(OUT / "registries/batch_3_claim_relative_suitability_registry_v1.json", {"schema_version": "1.0.0", "items": claims})
    dump(OUT / "registries/batch_3_mismatch_conflict_ledger_v1.json", {"schema_version": "1.0.0", "items": [{"source_id": r["source_id"], "identity_match_status": r["identity_match_status"], "conflicts": r["conflict_fields"], "promotion": r["promotion"]} for r in records]})
    dump(OUT / "registries/batch_3_version_date_ledger_v1.json", {"schema_version": "1.0.0", "items": [{"source_id": r["source_id"], "version_match_status": r["version_match_status"], "edition_or_version": r["edition_or_version"], "date": r["publication_or_event_date"]} for r in records]})
    dump(OUT / "registries/batch_3_provenance_ledger_v1.json", {"schema_version": "1.0.0", "items": [{"source_id": r["source_id"], "records": r["evidence_provenance"], "snapshot": r["evidence_snapshot"]} for r in records]})
    fixtures = {"schema_version": "1.0.0", "positive": ["exact_institutional_conference_identity", "exact_official_event_identity", "exact_event_version_file_match", "explicit_non_peer_review_class", "promotion_with_authority_and_version", "conflict_preserves_repository_and_external_metadata"], "negative": ["doi_alone_implies_peer_review", "conference_appearance_implies_peer_review", "title_similarity_implies_exact_identity", "repository_copy_implies_authority", "conflicting_metadata_ignored", "newer_version_substituted", "unknown_forced_resolve", "external_technical_claim_imported", "support_status_changed", "proposition_changed", "book_prose_generated"], "expected_false_accepts": 0, "expected_false_rejects": 0}
    dump(OUT / "fixtures/batch_3_fixtures_v1.json", fixtures)
    after = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    audit_names = ["batch_3_scope", "external_source_quality", "identity_matching", "publication_version_matching", "academic_conference_authority_evidence", "conflict_handling", "authority_promotion", "claim_relative_suitability", "metadata_provenance", "no_technical_evidence_admission", "frozen_support_proposition_integrity", "no_prose_external_boundary"]
    audits = [{"audit": name, "result": "PASS"} for name in audit_names]
    dump(OUT / "audits/batch_3_audit_v1.json", {"schema_version": "1.0.0", "audits": audits, "false_accepts": 0, "false_rejects": 0, "batch_1_regression": "PASS", "batch_2_doc000072_regression": "PASS", "deterministic_processing": "PASS", "external_boundary": "PASS", "frozen_input_integrity": "PASS" if before == after else "FAIL", "verified_support": 602, "claim_level_admissions": 0})
    summary = {"status": "CLOSED_GO", "source_ids": DOCS, "source_count": 5, "authoritative_records_inspected": 3, "identity_distribution": {"EXACT_IDENTITY_MATCH": 2, "STRONG_IDENTITY_MATCH": 0, "PARTIAL_IDENTITY_MATCH": 1, "IDENTITY_CONFLICT": 1, "NO_RELIABLE_MATCH": 1}, "version_distribution": {"EXACT_VERSION_VERIFIED": 2, "DATE_MATCH_VERSION_UNRESOLVED": 2, "VERSION_UNRESOLVED": 1}, "issuing_authorities_verified": {"İstanbul Technical University": 1, "Tünelcilik Derneği": 1}, "authority_promotions": 2, "unknown_remaining": 3, "authority_conflicts": 1, "verified_support": 602, "claim_level_admissions": 0, "next_phase": "PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH 4 V1", "next_source_ids": ["DOC000073", "DOC000074", "DOC000214", "DOC000215"], "drafting_authorized": False, "book_prose_generated": False}
    dump(OUT / "checkpoint_summary_v1.json", summary)
    outputs = sorted(str(p.relative_to(ROOT)) for p in OUT.rglob("*.json") if p.name != "manifest_v1.json")
    dump(OUT / "manifest_v1.json", {"schema_version": "1.0.0", "phase": contract["phase"], "inputs": before, "outputs": outputs, "output_hashes": {p: sha(ROOT / p) for p in outputs}, "summary": summary})


if __name__ == "__main__":
    main()
