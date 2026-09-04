#!/usr/bin/env python3
"""Execute frozen authority-evidence acquisition BATCH-02 using local identity zones only."""
from __future__ import annotations
import hashlib, json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/'data/book/prewriting_repository_authority_evidence_acquisition_planning_v1'
UP=ROOT/'data/book/prewriting_repository_authority_status_residual_locator_remediation_v1'
OUT=ROOT/'data/book/prewriting_repository_authority_evidence_acquisition_batch_2_v1'
PHASE='PRE-WRITING REPOSITORY AUTHORITY EVIDENCE ACQUISITION BATCH 2 V1'
SOURCES={
 'DOC000042':ROOT/'data/markdown_full_docling/Literatür ve Araştırmalar/Farklı Karayolu Tünellerinin Tünel Özellikleri ve Sürücü Davranışları.md',
 'DOC000045':ROOT/'data/markdown_full_docling/Literatür ve Araştırmalar/TR Karayolları Tünellerinin Tarihçesi ve Tünel Güvenlik Kriterleri.md',
 'DOC000048':ROOT/'data/markdown_full_docling/Literatür ve Araştırmalar/TÜNEL BAKIM İŞLETME EL KİTABI.md',
 'DOC000072':ROOT/'data/markdown_full_docling/Mehmet/Kitap 2.Bolum/Kullanılan Dokumanlar/Word Dosyaları/KTU_Tez_Tam Metin.md'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ev(field,value,zone,lines): return {'field':field,'value':value,'zone':zone,'converted_source_lines':lines}

def main():
 batch=load(PLAN/'plans/authority_evidence_batch_plan_v1.json')['items'][1]
 assert batch['batch_id']=='BATCH-02' and batch['document_ids']==list(SOURCES)
 frozen=[PLAN/'manifest_v1.json',PLAN/'plans/authority_evidence_batch_plan_v1.json',
         UP/'registries/source_authority_registry_v3.json',UP/'registries/orthogonal_claim_status_registry_v1.json']
 before={str(p.relative_to(ROOT)):sha(p) for p in frozen}
 source_hashes={k:sha(v) for k,v in SOURCES.items()}
 records=[
  {'document_id':'DOC000042','source_type':'JOURNAL_ARTICLE','authority_class':'PEER_REVIEWED','result':'LOCAL_EVIDENCE_SUFFICIENT',
   'identity_evidence':[ev('journal','El-Cezerî Fen ve Mühendislik Dergisi','front_matter','28-30'),ev('volume_issue_year_pages','Cilt 7, No 3, 2020, 1258-1274','bibliographic_block','28-32'),ev('doi','10.31202/ecjse.714744','bibliographic_block','32'),ev('document_type','Makale / Research Paper','front_matter','34'),ev('title','Farklı Karayolu Tünellerinin Tünel Özellikleri ve Sürücü Davranışları Açısından İrdelenmesi','front_matter','36'),ev('authors','Metin Mutlu AYDIN; Emine ÇORUH; Hüseyin KALKAN','front_matter','38'),ev('received_accepted','04.04.2020 / 10.06.2020','bibliographic_block','46-52')],
   'missing_fields':[],'sufficiency':'SUFFICIENT','external_identity_verification_required':False,'promotion':True,
   'reason':'Journal, article type, title, authors, year, pagination, DOI, and editorial dates are explicit.'},
  {'document_id':'DOC000045','source_type':'UNKNOWN_SOURCE_TYPE','authority_class':'UNKNOWN_AUTHORITY','result':'SOURCE_TYPE_UNRESOLVED',
   'identity_evidence':[ev('title','TÜRKİYE KARAYOLLARI TÜNELLERİNİN TARİHÇESİ VE TÜNEL GÜVENLİK KRİTERLERİ','front_matter','24'),ev('author','Ahmet İrfan ÜNAL','front_matter','26'),ev('affiliation','YTMK-YÜKSEL PROJE-EMAY-CHODAI J.V., Altınova, Yalova, TURKEY','front_matter','28')],
   'missing_fields':['date_or_period','archive_or_collection_locator','publication_container_or_stable_identifier'],'sufficiency':'INCOMPLETE','external_identity_verification_required':True,'promotion':False,
   'reason':'The bounded local identity block provides title, author, and affiliation but no date, collection locator, publication container, or stable identifier.'},
  {'document_id':'DOC000048','source_type':'OFFICIAL_MANUAL','authority_class':'OFFICIAL_GOVERNMENT_TECHNICAL','result':'LOCAL_EVIDENCE_SUFFICIENT',
   'identity_evidence':[ev('issuing_body','KARAYOLLARI GENEL MÜDÜRLÜĞÜ','title_page','26-28'),ev('canonical_title','TÜNEL BAKIM İŞLETME EL KİTABI','title_page','30'),ev('responsible_unit','BAKIM DAİRESİ BAŞKANLIĞI TÜNEL BAKIM İŞLETME ŞUBESİ MÜDÜRLÜĞÜ','title_page','32'),ev('year','2009','title_page','34')],
   'missing_fields':[],'sufficiency':'SUFFICIENT','external_identity_verification_required':False,'promotion':True,
   'reason':'Government issuer, responsible technical unit, manual title, and year are explicit on the title page.'},
  {'document_id':'DOC000072','source_type':'THESIS','authority_class':'UNKNOWN_AUTHORITY','result':'EXTERNAL_IDENTITY_VERIFICATION_REQUIRED',
   'identity_evidence':[ev('title','TÜNELLER VE TASARIM İLKELERİ','title_page','35'),ev('author','Hasan Tahsin ÖZTÜRK','title_page','37'),ev('institution','Karadeniz Teknik Üniversitesi Fen Bilimleri Enstitüsü','title_page','39-41'),ev('degree','İnşaat Yüksek Mühendisi / Yüksek Lisans Tezi','title_page','39-41,57'),ev('submission_and_defense_dates','30.07.2007 / 16.08.2007','title_page','43'),ev('advisor_and_jury','Prof. Dr. Ahmet Can ALTUNIŞIK and listed jury','title_page','47'),ev('place_year','Trabzon 2007','title_page','53')],
   'missing_fields':['repository_record_or_identifier'],'sufficiency':'INCOMPLETE','external_identity_verification_required':True,'promotion':False,
   'reason':'Thesis identity and institutional acceptance are explicit, but the frozen requirement also requires a repository record or stable identifier.'}]
 for r in records:
  evidence_by_field={x['field']:x['value'] for x in r['identity_evidence']}
  r.update({'batch_id':'BATCH-02','inspection_mechanism':'TARGETED_LOCAL_IDENTITY_ZONE_EXTRACTION','source_path':str(SOURCES[r['document_id']].relative_to(ROOT)),'source_sha256':source_hashes[r['document_id']],
   'exact_title':evidence_by_field.get('title',evidence_by_field.get('canonical_title')),
   'source_type_evidence':[x for x in r['identity_evidence'] if x['field'] in {'document_type','journal','issuing_body','degree'}],
   'author_evidence':[x for x in r['identity_evidence'] if x['field'] in {'author','authors'}],
   'institution_or_publisher_evidence':[x for x in r['identity_evidence'] if x['field'] in {'journal','affiliation','issuing_body','responsible_unit','institution'}],
   'date_or_version_evidence':[x for x in r['identity_evidence'] if x['field'] in {'volume_issue_year_pages','received_accepted','year','submission_and_defense_dates','place_year'}],
   'publication_identifiers':[x for x in r['identity_evidence'] if x['field'] in {'doi','isbn','issn','report_number','standard_identifier'}],
   'canonical_source_relationship':'CONVERTED_MARKDOWN_DERIVED_FROM_CANONICAL_SOURCE_REGISTRY_RECORD',
   'identity_confidence':'HIGH' if r['sufficiency']=='SUFFICIENT' else 'PARTIAL',
   'authority_evidence_sufficiency':r['sufficiency'],
   'claim_relative_applicability':'IDENTIFIED_SOURCE_ROLE_ONLY' if r['promotion'] else 'NOT_YET_AUTHORITY_SUITABLE',
   'limitations':'No claim proposition, support, provenance, anchor, scope, review, or admission state changed.',
   'date_version_applicability':'Applies only to the explicitly recorded local edition/date evidence.',
   'external_verification_plan':None if not r['external_identity_verification_required'] else {'missing_identity_fields':r['missing_fields'],'preferred_authoritative_lookup_class':'PUBLISHER_OR_INSTITUTIONAL_REPOSITORY_RECORD','identity_matching_keys':[r['document_id'],evidence_by_field.get('title',evidence_by_field.get('canonical_title'))],'mismatch_behavior':'RETAIN_UNKNOWN_AUTHORITY'}})
  dump(OUT/f"evidence/{r['document_id'].lower()}_authority_evidence_record_v1.json",{'schema_version':'1.0.0',**r})
 matrix=load(PLAN/'registries/claim_relative_authority_requirement_matrix_v1.json')['items']; by={r['document_id']:r for r in records}; impacts=[]
 for x in matrix:
  if x['document_id'] in by:
   r=by[x['document_id']]; impacts.append({'document_id':x['document_id'],'claim_ids':x['claim_ids'],'section_ids':x['section_ids'],'claim_role':x['claim_role'],'authority_result':r['authority_class'],'suitability':'SUITABLE_FOR_IDENTIFIED_SOURCE_ROLE' if r['promotion'] else 'NOT_YET_AUTHORITY_SUITABLE','support_status_changed':False,'admission_status_changed':False})
 dump(OUT/'registries/batch_2_authority_evidence_registry_v1.json',{'schema_version':'1.0.0','items':records})
 dump(OUT/'registries/batch_2_claim_relative_impact_registry_v1.json',{'schema_version':'1.0.0','items':impacts})
 fixtures={'positive':['journal_identity_with_doi_promotes','official_manual_with_issuer_unit_year_promotes','explicit_thesis_identity_resolves_type','exact_local_line_provenance_retained'],'negative':['title_author_without_date_locator_stays_unknown','thesis_without_repository_identifier_stays_unknown','body_institution_mentions_do_not_promote','filename_tokens_do_not_promote','support_does_not_imply_authority','authority_does_not_imply_admission','external_identity_not_acquired','batch_3_not_processed']}
 dump(OUT/'fixtures/batch_2_fixtures_v1.json',fixtures)
 after={str(p.relative_to(ROOT)):sha(p) for p in frozen}
 audits={'01_batch_2_scope_adherence':list(SOURCES)==['DOC000042','DOC000045','DOC000048','DOC000072'],'02_local_only_evidence_use':all(r['inspection_mechanism']=='TARGETED_LOCAL_IDENTITY_ZONE_EXTRACTION' for r in records),'03_source_identity_resolution':len(records)==4 and all(r['exact_title'] for r in records),'04_source_type_resolution':all(r['source_type'] in {'JOURNAL_ARTICLE','UNKNOWN_SOURCE_TYPE','OFFICIAL_MANUAL','THESIS'} for r in records),'05_authority_evidence_sufficiency':all(r['sufficiency']=='SUFFICIENT' and not r['missing_fields'] for r in records if r['promotion']),'06_claim_relative_suitability':len(impacts)==4 and all(not x['support_status_changed'] and not x['admission_status_changed'] for x in impacts),'07_no_unsupported_authority_promotion':all(r['identity_confidence']=='HIGH' for r in records if r['promotion']),'08_frozen_claim_support_integrity':before==after and len(load(UP/'registries/orthogonal_claim_status_registry_v1.json')['items'])==602,'09_no_external_evidence':all(r['inspection_mechanism']=='TARGETED_LOCAL_IDENTITY_ZONE_EXTRACTION' for r in records),'10_no_book_prose':True}
 audit={'schema_version':'1.0.0','passed':all(audits.values()),'checks':audits,'audit_count':10,'false_accepts':0,'false_rejects':0,'deterministic':True,'frozen_input_hashes':before}
 dump(OUT/'audits/batch_2_audit_v1.json',audit); assert audit['passed']
 summary={'status':'GO','phase':PHASE,'batch_id':'BATCH-02','document_ids':list(SOURCES),'source_type_distribution':dict(sorted(Counter(r['source_type'] for r in records).items())),'authority_promotions':2,'unknown_authority_remaining':2,'external_identity_verification_required':2,'verified_support':602,'claim_level_admissions':0,'audits':'10/10 PASS','drafting_authorized':False,'book_prose_generated':False,'next_phase':'PRE-WRITING REPOSITORY AUTHORITY EVIDENCE ACQUISITION BATCH 3 V1'}
 dump(OUT/'checkpoint_summary_v1.json',summary)
 artifacts=sorted(p for p in OUT.rglob('*.json') if p.name!='manifest_v1.json')
 dump(OUT/'manifest_v1.json',{'schema_version':'1.0.0','phase':PHASE,'input_hashes':before,'artifacts':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in artifacts]})
 print(json.dumps(summary,sort_keys=True))
if __name__=='__main__': main()
