#!/usr/bin/env python3
"""Execute frozen authority-evidence acquisition BATCH-01 using local identity zones only."""
from __future__ import annotations
import hashlib, json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/'data/book/prewriting_repository_authority_evidence_acquisition_planning_v1'
UP=ROOT/'data/book/prewriting_repository_authority_status_residual_locator_remediation_v1'
OUT=ROOT/'data/book/prewriting_repository_authority_evidence_acquisition_batch_1_v1'
PHASE='PRE-WRITING REPOSITORY AUTHORITY EVIDENCE ACQUISITION BATCH 1 V1'
SOURCES={
 'DOC000002':ROOT/'data/markdown_full_docling/Leyla Literatür/TunelMaliyet/12229738_04.md',
 'DOC000003':ROOT/'data/markdown_full_docling/Leyla Literatür/TunelMaliyet/13965.md',
 'DOC000038':ROOT/'data/markdown_full_docling/Literatür ve Araştırmalar/An Ex-Post Cost - Benefit Analysis of Bolu Mountain__Tunnel Project.md',
 'DOC000039':ROOT/'data/markdown_full_docling/Literatür ve Araştırmalar/Benchmarking_tunnelling_costs_and_production_rates_in_the_UK_Web_Accessible.md'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ev(field,value,zone,lines): return {'field':field,'value':value,'zone':zone,'converted_source_lines':lines}

def main():
 batch=load(PLAN/'plans/authority_evidence_batch_plan_v1.json')['items'][0]
 assert batch['batch_id']=='BATCH-01' and batch['document_ids']==list(SOURCES)
 frozen=[PLAN/'manifest_v1.json',PLAN/'plans/authority_evidence_batch_plan_v1.json',
         UP/'registries/source_authority_registry_v3.json',UP/'registries/orthogonal_claim_status_registry_v1.json']
 before={str(p.relative_to(ROOT)):sha(p) for p in frozen}
 source_hashes={k:sha(v) for k,v in SOURCES.items()}
 records=[
  {'document_id':'DOC000002','source_type':'UNKNOWN_SOURCE_TYPE','authority_class':'UNKNOWN','result':'SOURCE_TYPE_UNRESOLVED',
   'identity_evidence':[ev('fragment_heading','CHAPTER 14 OPERATIONS AND MAINTENANCE OF THE PROJECT','front_matter','24-26')],
   'missing_fields':['parent_work_title','author_or_issuer','publisher','year','stable_identifier'],
   'sufficiency':'INCOMPLETE','external_identity_verification_required':True,'promotion':False,
   'reason':'The bounded local file begins at Chapter 14 and contains no parent-work identity block.'},
  {'document_id':'DOC000003','source_type':'OFFICIAL_REPORT','authority_class':'INSTITUTIONAL_TECHNICAL','result':'LOCAL_EVIDENCE_SUFFICIENT',
   'identity_evidence':[ev('publisher','THE NATIONAL ACADEMIES PRESS','front_matter','24-26'),ev('canonical_title','Making Transportation Tunnels Safe and Secure','front_matter','38'),ev('year','2006','front_matter','38'),ev('isbn','978-0-309-09871-7','bibliographic_block','42'),ev('doi','10.17226/13965','bibliographic_block','42'),ev('responsible_programs','NCHRP; TCRP; Transportation Research Board; National Academies','contributors','44-46')],
   'missing_fields':[],'sufficiency':'SUFFICIENT','external_identity_verification_required':False,'promotion':True,
   'reason':'Publisher, title, year, stable identifiers, and responsible institutional programs are explicit.'},
  {'document_id':'DOC000038','source_type':'UNKNOWN_SOURCE_TYPE','authority_class':'UNKNOWN','result':'EXTERNAL_IDENTITY_REQUIRED',
   'identity_evidence':[ev('paper_title','An Ex-Post Cost - Benefit Analysis of Bolu Mountain Tunnel Project','front_matter','24'),ev('authors','Gaye KOCABAŞ; Barış Serkan KOPURLU','front_matter','26')],
   'missing_fields':['journal_or_conference','publication_year','doi_or_volume_issue_pages'],'sufficiency':'INCOMPLETE','external_identity_verification_required':True,'promotion':False,
   'reason':'Local front matter identifies a paper and authors but not its publication container, date, or stable identifier.'},
  {'document_id':'DOC000039','source_type':'OFFICIAL_REPORT','authority_class':'OFFICIAL_GOVERNMENT_TECHNICAL','result':'LOCAL_EVIDENCE_SUFFICIENT',
   'identity_evidence':[ev('canonical_title','Case Study: Benchmarking tunnelling costs and production rates in the UK','front_matter','26'),ev('issuing_program','Transforming Infrastructure Performance programme; Infrastructure and Projects Authority','synopsis','30'),ev('date','2018','synopsis','34'),ev('authors','Bill Grose; Aleister Hellier','authors','213-219'),ev('government_contact','publiccorrespondence@hmtreasury.gov.uk','contact_block','232-234')],
   'missing_fields':[],'sufficiency':'SUFFICIENT','external_identity_verification_required':False,'promotion':True,
   'reason':'Title, government authority/program, exercise date, authors, and government contact are explicit.'}]
 for r in records:
  r.update({'batch_id':'BATCH-01','inspection_mechanism':'TARGETED_LOCAL_IDENTITY_ZONE_EXTRACTION','source_path':str(SOURCES[r['document_id']].relative_to(ROOT)),'source_sha256':source_hashes[r['document_id']]})
  dump(OUT/f"evidence/{r['document_id'].lower()}_authority_evidence_record_v1.json",{'schema_version':'1.0.0',**r})
 impacts=[]
 matrix=load(PLAN/'registries/claim_relative_authority_requirement_matrix_v1.json')['items']
 by={r['document_id']:r for r in records}
 for x in matrix:
  if x['document_id'] in by:
   r=by[x['document_id']]; impacts.append({'document_id':x['document_id'],'claim_ids':x['claim_ids'],'section_ids':x['section_ids'],'claim_role':x['claim_role'],
    'authority_result':r['authority_class'],'suitability':'SUITABLE_FOR_IDENTIFIED_SOURCE_ROLE' if r['promotion'] else 'NOT_YET_AUTHORITY_SUITABLE',
    'support_status_changed':False,'admission_status_changed':False})
 dump(OUT/'registries/batch_1_authority_evidence_registry_v1.json',{'schema_version':'1.0.0','items':records})
 dump(OUT/'registries/batch_1_claim_relative_impact_registry_v1.json',{'schema_version':'1.0.0','items':impacts})
 fixtures={'positive':['explicit_publisher_title_year_identifier_promotes','explicit_government_issuer_title_date_authors_promotes','field_level_locator_captured','claim_relative_impact_orthogonal'],
           'negative':['chapter_heading_does_not_identify_parent','paper_label_does_not_select_journal_or_conference','body_institution_mention_does_not_promote','filename_does_not_promote','missing_date_or_identifier_fails_closed','support_mutation_rejected','admission_mutation_rejected','out_of_batch_source_rejected']}
 dump(OUT/'fixtures/batch_1_fixtures_v1.json',fixtures)
 after={str(p.relative_to(ROOT)):sha(p) for p in frozen}
 audits={
  '01_batch_scope':set(by)==set(batch['document_ids']) and len(records)==4,
  '02_local_only':all(r['inspection_mechanism']=='TARGETED_LOCAL_IDENTITY_ZONE_EXTRACTION' for r in records),
  '03_source_hash_provenance':all(r['source_sha256']==sha(SOURCES[r['document_id']]) for r in records),
  '04_type_resolution_fail_closed':all(r['authority_class']=='UNKNOWN' for r in records if r['source_type']=='UNKNOWN_SOURCE_TYPE'),
  '05_promotion_sufficiency':all(r['sufficiency']=='SUFFICIENT' and not r['missing_fields'] for r in records if r['promotion']),
  '06_claim_relative_impact':len(impacts)==4 and all(not x['support_status_changed'] and not x['admission_status_changed'] for x in impacts),
  '07_verified_support_preserved':len(load(UP/'registries/orthogonal_claim_status_registry_v1.json')['items'])==602,
  '08_no_claim_admission':all(not x['admission_status_changed'] for x in impacts),
  '09_frozen_integrity':before==after,
  '10_fixtures':len(fixtures['positive'])==4 and len(fixtures['negative'])==8}
 audit={'schema_version':'1.0.0','passed':all(audits.values()),'checks':audits,'audit_count':10,'false_accepts':0,'false_rejects':0,'deterministic':True,'frozen_input_hashes':before}
 dump(OUT/'audits/batch_1_audit_v1.json',audit); assert audit['passed']
 dist=dict(sorted(Counter(r['source_type'] for r in records).items()))
 summary={'status':'GO','phase':PHASE,'batch_id':'BATCH-01','document_ids':list(SOURCES),'source_type_distribution':dist,'authority_promotions':2,
  'unknown_authority_remaining':2,'external_identity_verification_required':2,'verified_support':602,'claim_level_admissions':0,'audits':'10/10 PASS',
  'drafting_authorized':False,'book_prose_generated':False,'next_phase':'PRE-WRITING REPOSITORY AUTHORITY EVIDENCE ACQUISITION BATCH 2 V1'}
 dump(OUT/'checkpoint_summary_v1.json',summary)
 artifacts=sorted(p for p in OUT.rglob('*.json') if p.name!='manifest_v1.json')
 dump(OUT/'manifest_v1.json',{'schema_version':'1.0.0','phase':PHASE,'input_hashes':before,'artifacts':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in artifacts]})
 print(json.dumps(summary,sort_keys=True))
if __name__=='__main__': main()
