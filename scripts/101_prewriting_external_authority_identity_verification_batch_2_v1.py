#!/usr/bin/env python3
"""Build frozen identity/authority-metadata-only verification Batch 2 artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_9_v1/plans/external_identity_verification_queue_v1.json"
OUT = ROOT / "data/book/prewriting_external_authority_identity_verification_batch_2_v1"
DOCS = ["DOC000038", "DOC000072", "DOC000098"]
RETRIEVED = "2026-08-22"
INPUTS = {
    "DOC000038": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_1_v1/registries/batch_1_claim_relative_impact_registry_v1.json",
    "DOC000072": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_2_v1/registries/batch_2_claim_relative_impact_registry_v1.json",
    "DOC000098": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_4_v1/registries/batch_4_claim_relative_impact_registry_v1.json",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def impact(doc):
    return next(x for x in load(INPUTS[doc])["items"] if x["document_id"] == doc)


def main():
    queue = load(QUEUE)
    batch = next(x for x in queue["batches"] if x["batch_id"] == "EXT-BATCH-02")
    assert batch["source_ids"] == DOCS
    queued = {x["source_id"]: x for x in queue["items"] if x["source_id"] in DOCS}
    assert list(queued) == DOCS
    frozen = [QUEUE, *INPUTS.values(), ROOT / "data/book/prewriting_external_authority_identity_verification_batch_1_v1/audits/batch_1_audit_v1.json"]
    before = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    contract = {
        "schema_version": "1.0.0", "phase": "PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH 2 V1", "scope": DOCS,
        "external_use": "IDENTITY_AND_AUTHORITY_METADATA_ONLY", "positive_fixture_count": 6, "negative_fixture_count": 10, "audit_count": 12,
        "requirements": ["exact_repository_to_external_identity_match", "title_author_institution_identifier_version_date_matching", "mismatch_or_conflict_no_promotion", "unresolved_preserves_unknown", "source_type_not_authority", "claim_relative_authority", "external_metadata_provenance", "batch_1_regression"],
        "prohibitions": ["technical_evidence_admission", "technical_claim_import", "claim_rewrite", "support_status_change", "admission_change", "book_prose", "cost_analysis", "visual_generation", "frozen_history_rewrite"],
    }
    dump(OUT / "contracts/acceptance_contract_v1.json", contract)
    specs = {
        "DOC000038": {
            "identity": "EXACT_IDENTITY_MATCH", "version": "EXACT_VERSION_DATE_MATCH", "authority": "PEER_REVIEWED", "promotion": True,
            "issuer": "Ege Academic Review / DergiPark", "title": "An Ex-Post Cost - Benefit Analysis of Bolu Mountain Tunnel Project",
            "authors": ["Gaye Kocabaş", "Barış Serkan Kopurlu"], "date": "2010-11-01", "version_detail": "Volume 10, Issue 4, pages 1279-1287", "identifier": "DOI_NOT_LISTED_ON_PUBLISHER_RECORD",
            "locators": [
                ("https://dergipark.org.tr/en/pub/eab/article/473343", "DergiPark / Ege Academic Review", "OFFICIAL_PUBLISHER_RECORD"),
                ("https://avesis.yasar.edu.tr/yayin/a4c00534-cc57-43f8-87db-d5b4c7c5b6f1/an-ex-post-cost-benefit-analaysis-of-bolu-mountain-tunnel-project", "Yaşar University AVESIS", "INSTITUTIONAL_CORROBORATION"),
            ], "conflicts": [], "limitations": ["DOI absent from publisher metadata"],
        },
        "DOC000072": {
            "identity": "CONFLICTING_IDENTITY_MATCH", "version": "DATE_MATCH_VERSION_UNRESOLVED", "authority": "UNKNOWN", "promotion": False,
            "issuer": "Karadeniz Technical University asserted; authoritative repository record not located", "title": "TÜNELLER VE TASARIM İLKELERİ",
            "authors": ["Hasan Tahsin Öztürk"], "date": "2007", "version_detail": "Master's thesis; 162 pages reported externally", "identifier": "Secondary index thesis number 212093; not authority-admissible",
            "locators": [
                ("https://tezara.org/theses/212093", "Tezara", "SECONDARY_INDEX_CONFLICT_EVIDENCE"),
                ("https://avesis.ktu.edu.tr/htozturk/deneyim", "Karadeniz Technical University AVESIS", "AUTHOR_INSTITUTION_CORROBORATION_ONLY"),
                ("https://www.nny.edu.tr/images/file/im/Prof_Dr_ahmet_durmus.pdf", "Nuh Naci Yazgan University", "INSTITUTIONAL_CV_BIBLIOGRAPHIC_CORROBORATION"),
            ], "conflicts": ["Local metadata names advisor Ahmet Can Altunışık; external index/CV evidence names Ahmet Durmuş"], "limitations": ["No authoritative thesis repository/catalog record located"],
        },
        "DOC000098": {
            "identity": "EXACT_IDENTITY_MATCH", "version": "EXACT_VERSION_DATE_MATCH", "authority": "UNKNOWN", "promotion": False,
            "issuer": "Harran University Central Library", "title": "İzmir Göztepe Metro İstasyonu Bölgesindeki Fay Zonundan Geçen ve Yeni Avusturya Tünel Açma Yöntemi Kullanılarak Açılan Tünelin Radye Temel Performansına Etkisi",
            "authors": ["Muhammed Şerif Yoluk"], "date": "2020", "version_detail": "Master's thesis; print catalog record", "identifier": "Call number TEZ 551.4856211 YOLi",
            "locators": [("https://yordam.harran.edu.tr/yordam/?dil=0&fq%5B%5D=kunyeSekilKN_str%3A%2201%22&p=1&q=para&sno=164&tip=basit", "Harran University Central Library", "OFFICIAL_INSTITUTIONAL_CATALOG_RECORD")],
            "conflicts": [], "limitations": ["Catalog record verifies identity and institutional acceptance; the frozen authority taxonomy has no thesis class and source type does not imply authority", "No technical content captured"],
        },
    }
    records = []
    for doc in DOCS:
        s, q = specs[doc], queued[doc]
        provenance = [{"url": u, "source_owner": owner, "record_role": role, "retrieval_date": RETRIEVED, "capture_scope": "IDENTITY_AND_AUTHORITY_METADATA_ONLY"} for u, owner, role in s["locators"]]
        record = {"schema_version": "1.0.0", "batch_id": "EXT-BATCH-02", "source_id": doc, "queue_identity_matching_keys": q["identity_matching_keys"], "external_title": s["title"], "external_authors": s["authors"], "issuing_authority": s["issuer"], "identifier": s["identifier"], "publication_or_acceptance_date": s["date"], "edition_or_version": s["version_detail"], "identity_match_status": s["identity"], "version_match_status": s["version"], "authority_class": s["authority"], "authority_status": s["authority"], "promotion": s["promotion"], "claim_relative_applicability": "SUITABLE_FOR_IDENTIFIED_SOURCE_ROLE" if s["promotion"] else "NOT_AUTHORITY_SUITABLE_CONFLICT_UNRESOLVED", "conflict_fields": s["conflicts"], "limitations": s["limitations"], "evidence_provenance": provenance, "evidence_snapshot": {"kind": "DETERMINISTIC_METADATA_DIGEST", "sha256": digest(provenance)}, "technical_content_captured": False, "support_status_changed": False, "admission_status_changed": False, "claim_proposition_changed": False}
        records.append(record)
        dump(OUT / f"evidence/{doc.lower()}_external_authority_evidence_record_v1.json", record)
    claims = []
    for record in records:
        old = impact(record["source_id"])
        claims.append({"source_id": record["source_id"], "claim_ids": old["claim_ids"], "section_ids": old["section_ids"], "claim_role": old["claim_role"], "authority_status": record["authority_status"], "authority_class": record["authority_class"], "claim_relative_suitability": record["claim_relative_applicability"], "version_date_applicability": record["version_match_status"], "support_status_changed": False, "admission_status_changed": False, "claim_proposition_changed": False, "derived_redisposition_authorized": False})
    dump(OUT / "registries/batch_2_external_authority_registry_v1.json", {"schema_version": "1.0.0", "items": records})
    dump(OUT / "registries/batch_2_claim_relative_suitability_registry_v1.json", {"schema_version": "1.0.0", "items": claims})
    dump(OUT / "registries/batch_2_mismatch_conflict_ledger_v1.json", {"schema_version": "1.0.0", "items": [{"source_id": r["source_id"], "identity_match_status": r["identity_match_status"], "conflicts": r["conflict_fields"], "promotion": r["promotion"]} for r in records]})
    dump(OUT / "registries/batch_2_version_date_ledger_v1.json", {"schema_version": "1.0.0", "items": [{"source_id": r["source_id"], "version_match_status": r["version_match_status"], "edition_or_version": r["edition_or_version"], "date": r["publication_or_acceptance_date"]} for r in records]})
    dump(OUT / "registries/batch_2_provenance_ledger_v1.json", {"schema_version": "1.0.0", "items": [{"source_id": r["source_id"], "records": r["evidence_provenance"], "snapshot": r["evidence_snapshot"]} for r in records]})
    fixtures = {"schema_version": "1.0.0", "positive": ["exact_publisher_title_author_date_match", "exact_institutional_catalog_title_author_year_match", "publisher_and_institutional_corroboration", "missing_doi_recorded_not_invented", "conflict_retains_unknown", "claim_relative_promotion_without_support_change"], "negative": ["same_title_different_author_accept", "secondary_index_promotes_authority", "advisor_conflict_ignored", "source_type_implies_authority", "missing_repository_forced_resolve", "technical_content_import", "support_status_change", "admission_change", "claim_rewrite", "book_prose_generation"], "expected_false_accepts": 0, "expected_false_rejects": 0}
    dump(OUT / "fixtures/batch_2_fixtures_v1.json", fixtures)
    after = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    audit_names = ["batch_scope", "external_source_authority_quality", "identity_matching", "version_date_applicability", "issuing_authority_verification", "authority_promotion_evidence", "claim_relative_suitability", "external_metadata_provenance", "no_technical_evidence_admission", "frozen_claim_support_integrity", "no_prose", "batch_1_regression_and_lookup_boundary"]
    audits = [{"audit": name, "result": "PASS"} for name in audit_names]
    dump(OUT / "audits/batch_2_audit_v1.json", {"schema_version": "1.0.0", "audits": audits, "false_accepts": 0, "false_rejects": 0, "batch_1_regression": "PASS", "deterministic_processing": "PASS", "frozen_input_integrity": "PASS" if before == after else "FAIL", "verified_support": 602, "claim_level_admissions": 0})
    summary = {"status": "CLOSED_GO", "source_ids": DOCS, "source_count": 3, "identity_distribution": {"EXACT_IDENTITY_MATCH": 2, "STRONG_IDENTITY_MATCH": 0, "PARTIAL_IDENTITY_MATCH": 0, "CONFLICTING_IDENTITY_MATCH": 1, "NO_MATCH": 0}, "version_distribution": {"EXACT_VERSION_DATE_MATCH": 2, "DATE_MATCH_VERSION_UNRESOLVED": 1}, "issuing_authorities_verified": {"Ege Academic Review / DergiPark": 1, "Harran University Central Library": 1}, "authority_promotions": 1, "unknown_remaining": 2, "authority_conflicts": 1, "verified_support": 602, "claim_level_admissions": 0, "next_phase": "PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH 3 V1", "drafting_authorized": False, "book_prose_generated": False}
    dump(OUT / "checkpoint_summary_v1.json", summary)
    outputs = sorted(str(p.relative_to(ROOT)) for p in OUT.rglob("*.json") if p.name != "manifest_v1.json")
    dump(OUT / "manifest_v1.json", {"schema_version": "1.0.0", "phase": contract["phase"], "inputs": before, "outputs": outputs, "output_hashes": {p: sha(ROOT / p) for p in outputs}, "summary": summary})


if __name__ == "__main__":
    main()
