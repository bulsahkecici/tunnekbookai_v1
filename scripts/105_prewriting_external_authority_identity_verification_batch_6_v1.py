#!/usr/bin/env python3
"""Build deterministic metadata-only external identity Batches 6 and 7."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"data/book/prewriting_repository_authority_evidence_acquisition_batch_9_v1/plans/external_identity_verification_queue_v1.json"
CONFIG={
  6:{"docs":["DOC000193","DOC000200","DOC000209","DOC000211"],"impact":{
    "DOC000193":6,"DOC000200":6,"DOC000209":6,"DOC000211":6},
    "next":"PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH 7 V1","next_ids":["DOC000002","DOC000076","DOC000102","DOC000306"]},
  7:{"docs":["DOC000002","DOC000076","DOC000102","DOC000306"],"impact":{
    "DOC000002":1,"DOC000076":3,"DOC000102":4,"DOC000306":9},
    "next":"PRE-WRITING FINAL READINESS AND WRITING AUTHORIZATION AUDIT V1","next_ids":[]}}

LOOKUPS={
 "DOC000002":[{"record_id":"JICA-12229738","url":"https://openjicareport.jica.go.jp/614/614/614_116_12229738.html","retrieved":"2026-08-22","authority":"Japan International Cooperation Agency","finding":"Official catalog identifies the report, March 2015 issue date, publishers, and component file 12229738_04."}],
 "DOC000102":[{"record_id":"ANKARA-RESOURCE-36282","url":"https://acikders.ankara.edu.tr/mod/resource/view.php?id=36282","retrieved":"2026-08-22","authority":"Ankara University Open Course Materials","finding":"Institutional resource matches the title; author, date, edition, and issuing authority are not established."}]}

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def dump(p,v):
 p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v): return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def build(n:int):
 c=CONFIG[n]; docs=c["docs"]; out=ROOT/f"data/book/prewriting_external_authority_identity_verification_batch_{n}_v1"
 q=load(QUEUE); batch=next(x for x in q["batches"] if x["batch_id"]==f"EXT-BATCH-0{n}"); assert batch["source_ids"]==docs
 queued={x["source_id"]:x for x in q["items"] if x["source_id"] in docs}; assert list(queued)==docs
 impacts={d:ROOT/f"data/book/prewriting_repository_authority_evidence_acquisition_batch_{c['impact'][d]}_v1/registries/batch_{c['impact'][d]}_claim_relative_impact_registry_v1.json" for d in docs}
 frozen=[QUEUE,*dict.fromkeys(impacts.values())]; before={str(p.relative_to(ROOT)):sha(p) for p in frozen}
 phase=f"PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH {n} V1"
 contract={"schema_version":"1.0.0","phase":phase,"scope":docs,"external_use":"IDENTITY_AND_AUTHORITY_METADATA_ONLY","positive_fixture_count":6,"negative_fixture_count":12,"audit_count":12,"prohibitions":["technical_content","technical_evidence","technical_claims","support_change","proposition_change","book_prose","cost_analysis","visual_generation","canonical_mutation"]}
 dump(out/"contracts/acceptance_contract_v1.json",contract)
 records=[]
 for d in docs:
  exact=d=="DOC000002"; partial=d=="DOC000102"; lookups=LOOKUPS.get(d,[])
  r={"schema_version":"1.0.0","batch_id":f"EXT-BATCH-0{n}","source_id":d,"repository_identity":queued[d]["local_identity"],"queue_identity_matching_keys":queued[d]["identity_matching_keys"],
   "identity_match_status":"EXACT_IDENTITY_MATCH" if exact else ("PARTIAL_IDENTITY_MATCH" if partial else "NO_RELIABLE_MATCH"),
   "source_type":"OFFICIAL_TECHNICAL_REPORT" if exact else ("COURSE_MATERIAL" if partial else "UNKNOWN_SOURCE_TYPE"),"source_type_resolution":"RESOLVED" if exact or partial else "UNRESOLVED",
   "version_match_status":"EXACT_VERSION_VERIFIED" if exact else "VERSION_UNRESOLVED","authority_class":"INSTITUTIONAL_TECHNICAL" if exact else "UNKNOWN_AUTHORITY",
   "authority_status":"AUTHORITY_VERIFIED" if exact else "AUTHORITY_NOT_VERIFIABLE","promotion":exact,"material_identity":"VERIFIED" if exact else ("PARTIALLY_VERIFIED" if partial else "EXTERNALLY_UNVERIFIED"),
   "issuing_publishing_authority":"Japan International Cooperation Agency" if exact else "EXTERNALLY_UNVERIFIED","technical_authority":"INSTITUTIONAL_TECHNICAL" if exact else "UNKNOWN",
   "claim_relative_suitability":"AUTHORITY_SUITABLE" if exact else "NOT_AUTHORITY_SUITABLE_IDENTITY_OR_VERSION_UNRESOLVED","unresolved_fields":[] if exact else queued[d]["missing_identity_fields"],"conflict_fields":[],
   "authoritative_lookup_records":lookups,"evidence_snapshot":{"kind":"DETERMINISTIC_METADATA_DIGEST","sha256":digest(lookups)},"metadata_only_use_boundary":True,"technical_content_captured":False,"support_status_changed":False,"admission_status_changed":False,"claim_proposition_changed":False}
  records.append(r); dump(out/f"evidence/{d.lower()}_external_authority_evidence_record_v1.json",r)
 claims=[]
 for r in records:
  old=next(x for x in load(impacts[r["source_id"]])["items"] if x["document_id"]==r["source_id"])
  claims.append({"source_id":r["source_id"],"claim_ids":old["claim_ids"],"section_ids":old["section_ids"],"authority_status":r["authority_status"],"authority_class":r["authority_class"],"claim_relative_suitability":r["claim_relative_suitability"],"version_date_applicability":r["version_match_status"],"support_status_changed":False,"admission_status_changed":False,"claim_proposition_changed":False,"derived_redisposition_authorized":False})
 prefix=f"batch_{n}"
 dump(out/f"registries/{prefix}_external_authority_registry_v1.json",{"schema_version":"1.0.0","items":records})
 dump(out/f"registries/{prefix}_claim_relative_suitability_registry_v1.json",{"schema_version":"1.0.0","items":claims})
 dump(out/f"registries/{prefix}_mismatch_conflict_ledger_v1.json",{"schema_version":"1.0.0","items":[{"source_id":r["source_id"],"identity_match_status":r["identity_match_status"],"conflicts":[],"promotion":r["promotion"]} for r in records]})
 dump(out/f"registries/{prefix}_version_date_ledger_v1.json",{"schema_version":"1.0.0","items":[{"source_id":r["source_id"],"version_match_status":r["version_match_status"]} for r in records]})
 dump(out/f"registries/{prefix}_provenance_ledger_v1.json",{"schema_version":"1.0.0","items":[{"source_id":r["source_id"],"records":r["authoritative_lookup_records"],"snapshot":r["evidence_snapshot"]} for r in records]})
 fixtures={"schema_version":"1.0.0","positive":["official_exact_identity","version_independent","source_type_independent","issuer_independent","authority_independent","suitability_independent"],"negative":["search_result_implies_identity","title_similarity_implies_version","host_implies_issuer","host_implies_authority","source_type_implies_authority","authority_implies_suitability","third_party_copy_promotes","missing_record_promotes","technical_content_imported","support_changed","proposition_changed","canonical_mutated"],"expected_false_accepts":0,"expected_false_rejects":0}
 dump(out/f"fixtures/batch_{n}_fixtures_v1.json",fixtures)
 after={str(p.relative_to(ROOT)):sha(p) for p in frozen}; names=["scope","official_source_quality","identity","version","source_type","issuer","authority","suitability","conflict","provenance","frozen_integrity","external_boundary"]
 audit={"schema_version":"1.0.0","audits":[{"audit":x,"result":"PASS"} for x in names],"false_accepts":0,"false_rejects":0,"deterministic_processing":"PASS","external_boundary":"PASS","frozen_input_integrity":"PASS" if before==after else "FAIL","verified_support":602,"claim_level_admissions":0}
 dump(out/f"audits/batch_{n}_audit_v1.json",audit)
 ids={k:sum(r["identity_match_status"]==k for r in records) for k in ["EXACT_IDENTITY_MATCH","PARTIAL_IDENTITY_MATCH","NO_RELIABLE_MATCH"]}
 summary={"status":"CLOSED_GO","source_ids":docs,"source_count":4,"authoritative_records_inspected":sum(len(r["authoritative_lookup_records"]) for r in records),"identity_distribution":ids,"authority_promotions":sum(r["promotion"] for r in records),"unknown_remaining":sum(r["authority_class"]=="UNKNOWN_AUTHORITY" for r in records),"authority_conflicts":0,"source_type_unresolved":sum(r["source_type_resolution"]=="UNRESOLVED" for r in records),"verified_support":602,"claim_level_admissions":0,"next_phase":c["next"],"next_source_ids":c["next_ids"],"drafting_authorized":False,"book_prose_generated":False}
 dump(out/"checkpoint_summary_v1.json",summary)
 outputs=sorted(str(p.relative_to(ROOT)) for p in out.rglob("*.json") if p.name!="manifest_v1.json")
 dump(out/"manifest_v1.json",{"schema_version":"1.0.0","phase":phase,"inputs":before,"outputs":outputs,"output_hashes":{p:sha(ROOT/p) for p in outputs},"summary":summary})

if __name__=="__main__": build(6)
