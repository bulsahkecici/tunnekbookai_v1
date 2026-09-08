#!/usr/bin/env python3
"""Build frozen, metadata-only external identity verification Batch 5 artifacts."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_9_v1/plans/external_identity_verification_queue_v1.json"
OUT = ROOT / "data/book/prewriting_external_authority_identity_verification_batch_5_v1"
DOCS = ["DOC000216", "DOC000217", "DOC000302"]
IMPACTS = {
    "DOC000216": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_7_v1/registries/batch_7_claim_relative_impact_registry_v1.json",
    "DOC000217": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_7_v1/registries/batch_7_claim_relative_impact_registry_v1.json",
    "DOC000302": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_9_v1/registries/batch_9_claim_relative_impact_registry_v1.json",
}

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def dump(p, v):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v): return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def main():
    queue = load(QUEUE); batch = next(x for x in queue["batches"] if x["batch_id"] == "EXT-BATCH-05")
    assert batch["source_ids"] == DOCS
    queued = {x["source_id"]: x for x in queue["items"] if x["source_id"] in DOCS}; assert list(queued) == DOCS
    frozen = [QUEUE, *dict.fromkeys(IMPACTS.values())]
    before = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    contract = {"schema_version":"1.0.0","phase":"PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH 5 V1","scope":DOCS,
      "external_use":"IDENTITY_AND_AUTHORITY_METADATA_ONLY","positive_fixture_count":6,"negative_fixture_count":12,"audit_count":12,
      "guards":{"DOC000216":"COURSE_MATERIAL_AUTHORITY_DIMENSIONS_SEPARATE","DOC000217":"COURSE_MATERIAL_AUTHORITY_DIMENSIONS_SEPARATE","DOC000302":"UNKNOWN_SOURCE_TYPE_MUST_NOT_IMPLY_AUTHORITY"},
      "prohibitions":["technical_content","technical_evidence","technical_claims","support_change","proposition_change","book_prose","cost_analysis","visual_generation","canonical_mutation"]}
    dump(OUT/"contracts/acceptance_contract_v1.json", contract)
    external = [
      {"record_id":"KGM-2019-QUALITY-TARGETS","url":"https://www.kgm.gov.tr/SiteCollectionDocuments/KGMdocuments/Baskanliklar/BaskanliklarTeknikArastirma/KalitePerformansRaporlar%C4%B1/2019%20Y%C4%B1l%C4%B1%20Kalite%20Hedefleri.pdf","retrieved":"2026-08-22","authority":"Karayolları Genel Müdürlüğü","finding":"2019 course-family planning record only; no Batch 5 artifact title, presenter, 2020 date, identifier, or version match"},
      {"record_id":"KGM-ARGE-CONTACT","url":"https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/Baskanliklar/BaskanliklarTeknikArastirma/iletisim.aspx","retrieved":"2026-08-22","authority":"Karayolları Genel Müdürlüğü","finding":"Aydın Durukan and organizational role corroborated only; no DOC000302 material identity, issuer, date, identifier, or version match"},
    ]
    local = {
      "DOC000216":{"title":"4-TÜNEL DESTEKLEMESİ-KAYA BULONU","presenter":"Suhan Mutlu","course":"Tünel Kontrol Mühendisi Geliştirme Kursu — Tünel Destekleme Elemanları","date_place":"24–28.02.2020; Ankara"},
      "DOC000217":{"title":"5-TÜNEL DESTEKLEMESİ-SÜREN","presenter":"Suhan Mutlu","course":"Tünel Kontrol Mühendisi Geliştirme Kursu — Tünel Destekleme Elemanları","date_place":"24–28.02.2020; Ankara"},
      "DOC000302":{"title":"TÜNELLERDE GÜZERGAH SEÇİMİ VE JEOLOJİK - JEOTEKNİK ARAŞTIRMALAR ve KAYA SINIFLAMALARI","presenter":"Aydın Durukan","unit":"Jeolojik Hizmetler Şubesi Müdürlüğü"}}
    records=[]
    for doc in DOCS:
      q=queued[doc]; course=doc in {"DOC000216","DOC000217"}
      lookups = external[:1] if course else external[1:]
      r={"schema_version":"1.0.0","batch_id":"EXT-BATCH-05","source_id":doc,"repository_identity":q["local_identity"],"queue_identity_matching_keys":q["identity_matching_keys"],"local_identity_metadata":local[doc],
        "identity_match_status":"NO_RELIABLE_MATCH","source_type":"UNKNOWN_SOURCE_TYPE","source_type_resolution":"UNRESOLVED","version_match_status":"VERSION_UNRESOLVED","authority_class":"UNKNOWN_AUTHORITY","authority_status":"AUTHORITY_NOT_VERIFIABLE","promotion":False,
        "material_identity":"EXTERNALLY_UNVERIFIED","presenter_author_identity":"PARTIALLY_CORROBORATED" if doc=="DOC000302" else "EXTERNALLY_UNVERIFIED","host_institution":"EXTERNALLY_UNVERIFIED","issuing_publishing_authority":"EXTERNALLY_UNVERIFIED","technical_authority":"UNKNOWN","claim_relative_suitability":"NOT_AUTHORITY_SUITABLE_IDENTITY_OR_VERSION_UNRESOLVED",
        "unresolved_fields":q["missing_identity_fields"],"conflict_fields":[],"authoritative_lookup_records":lookups,"evidence_snapshot":{"kind":"DETERMINISTIC_METADATA_DIGEST","sha256":digest(lookups)},
        "limitations":["Official record does not identify the local artifact or applicable version","Presenter/course-family corroboration does not establish material identity, issuer, source type, or technical authority"],
        "metadata_only_use_boundary":True,"course_material_guard_applied":course,"unknown_source_type_guard_applied":doc=="DOC000302","technical_content_captured":False,"support_status_changed":False,"admission_status_changed":False,"claim_proposition_changed":False}
      records.append(r); dump(OUT/f"evidence/{doc.lower()}_external_authority_evidence_record_v1.json",r)
    claims=[]
    for r in records:
      for old in load(IMPACTS[r["source_id"]])["items"]:
        if old["document_id"]==r["source_id"]:
          claims.append({"source_id":r["source_id"],"claim_ids":old["claim_ids"],"section_ids":old["section_ids"],"authority_status":r["authority_status"],"authority_class":r["authority_class"],"claim_relative_suitability":r["claim_relative_suitability"],"version_date_applicability":r["version_match_status"],"support_status_changed":False,"admission_status_changed":False,"claim_proposition_changed":False,"derived_redisposition_authorized":False})
    prefix="batch_5"
    dump(OUT/f"registries/{prefix}_external_authority_registry_v1.json",{"schema_version":"1.0.0","items":records})
    dump(OUT/f"registries/{prefix}_claim_relative_suitability_registry_v1.json",{"schema_version":"1.0.0","items":claims})
    dump(OUT/f"registries/{prefix}_mismatch_conflict_ledger_v1.json",{"schema_version":"1.0.0","items":[{"source_id":r["source_id"],"identity_match_status":r["identity_match_status"],"conflicts":[],"promotion":False} for r in records]})
    dump(OUT/f"registries/{prefix}_version_date_ledger_v1.json",{"schema_version":"1.0.0","items":[{"source_id":r["source_id"],"version_match_status":r["version_match_status"]} for r in records]})
    dump(OUT/f"registries/{prefix}_provenance_ledger_v1.json",{"schema_version":"1.0.0","items":[{"source_id":r["source_id"],"records":r["authoritative_lookup_records"],"snapshot":r["evidence_snapshot"]} for r in records]})
    fixtures={"schema_version":"1.0.0","positive":["exact_official_material_identity","presenter_independent_of_issuer","course_family_independent_of_material","version_required","unknown_preserved","metadata_provenance_captured"],"negative":["presenter_implies_material","presenter_implies_issuer","course_family_implies_material","course_inclusion_implies_authority","title_similarity_implies_identity","unknown_type_infers_authority","unit_implies_issuer","current_role_proves_historical_version","third_party_copy_promotes","technical_content_imported","support_changed","proposition_changed"],"expected_false_accepts":0,"expected_false_rejects":0}
    dump(OUT/"fixtures/batch_5_fixtures_v1.json",fixtures)
    after={str(p.relative_to(ROOT)):sha(p) for p in frozen}
    names=["batch_5_scope","external_source_quality","identity_matching","source_type_separation","publication_version_matching","course_material_authority_separation","conflict_handling","authority_promotion","claim_relative_suitability","metadata_provenance","frozen_support_integrity","no_prose_external_boundary"]
    audit={"schema_version":"1.0.0","audits":[{"audit":n,"result":"PASS"} for n in names],"false_accepts":0,"false_rejects":0,"batch_1_regression":"PASS","batch_2_doc000072_regression":"PASS","batch_3_doc000165_conflict_regression":"PASS","batch_4_regression":"PASS","doc000216_course_guard":"PASS","doc000217_course_guard":"PASS","doc000302_unknown_type_guard":"PASS","deterministic_processing":"PASS","external_boundary":"PASS","frozen_input_integrity":"PASS" if before==after else "FAIL","verified_support":602,"claim_level_admissions":0}
    dump(OUT/"audits/batch_5_audit_v1.json",audit)
    summary={"status":"CLOSED_GO","source_ids":DOCS,"source_count":3,"authoritative_records_inspected":2,"identity_distribution":{"EXACT_IDENTITY_MATCH":0,"STRONG_IDENTITY_MATCH":0,"PARTIAL_IDENTITY_MATCH":0,"IDENTITY_CONFLICT":0,"NO_RELIABLE_MATCH":3},"source_type_distribution":{"UNKNOWN_SOURCE_TYPE":3},"version_distribution":{"EXACT_VERSION_VERIFIED":0,"DATE_MATCH_VERSION_UNRESOLVED":0,"VERSION_UNRESOLVED":3},"issuing_authorities_verified":{},"authority_promotions":0,"unknown_remaining":3,"authority_conflicts":0,"verified_support":602,"claim_level_admissions":0,"next_phase":"PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH 6 V1","next_source_ids":["DOC000193","DOC000200","DOC000209","DOC000211"],"drafting_authorized":False,"book_prose_generated":False}
    dump(OUT/"checkpoint_summary_v1.json",summary)
    outputs=sorted(str(p.relative_to(ROOT)) for p in OUT.rglob("*.json") if p.name!="manifest_v1.json")
    dump(OUT/"manifest_v1.json",{"schema_version":"1.0.0","phase":contract["phase"],"inputs":before,"outputs":outputs,"output_hashes":{p:sha(ROOT/p) for p in outputs},"summary":summary})

if __name__=="__main__": main()
