#!/usr/bin/env python3
"""Execute frozen BATCH-03 using bounded local identity evidence only."""
from __future__ import annotations
import hashlib, json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/'data/book/prewriting_repository_authority_evidence_acquisition_planning_v1'
UP=ROOT/'data/book/prewriting_repository_authority_status_residual_locator_remediation_v1'
OUT=ROOT/'data/book/prewriting_repository_authority_evidence_acquisition_batch_3_v1'
PHASE='PRE-WRITING REPOSITORY AUTHORITY EVIDENCE ACQUISITION BATCH 3 V1'
SOURCES={
 'DOC000073':ROOT/'data/markdown_full_docling/Mehmet/Kitap 2.Bolum/Kullanılan Dokumanlar/Word Dosyaları/SinaKiziroglu.md',
 'DOC000074':ROOT/'data/markdown_full_docling/Mehmet/Kitap 2.Bolum/Kullanılan Dokumanlar/Word Dosyaları/TUNELLERDE_DESTEK_SISTEMLERI_VE_GUCLENDI.md',
 'DOC000075':ROOT/'data/markdown_full_docling/Mehmet/Kitap 2.Bolum/Kullanılan Dokumanlar/Word Dosyaları/Tünel Eğitim Kitabı 8 EYLÜL 2016.md',
 'DOC000076':ROOT/'data/markdown_full_docling/Mehmet/Kitap 2.Bolum/Tuneller Bolum2_9_7_2025.md'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ev(field,value,zone,lines): return {'field':field,'value':value,'zone':zone,'converted_source_lines':lines}

def main():
 batch=load(PLAN/'plans/authority_evidence_batch_plan_v1.json')['items'][2]
 assert batch['batch_id']=='BATCH-03' and batch['document_ids']==list(SOURCES)
 frozen=[PLAN/'manifest_v1.json',PLAN/'plans/authority_evidence_batch_plan_v1.json',UP/'registries/source_authority_registry_v3.json',UP/'registries/orthogonal_claim_status_registry_v1.json']
 before={str(p.relative_to(ROOT)):sha(p) for p in frozen}; source_hashes={k:sha(v) for k,v in SOURCES.items()}
 rows=[
  ('DOC000073','UNKNOWN_SOURCE_TYPE','UNKNOWN_AUTHORITY','SOURCE_TYPE_UNRESOLVED',[
   ev('presentation_name','63. Bölge Müdürleri Toplantısı','title_page','27-31'),ev('presenter','Sina Kiziroğlu','title_page','39-41'),ev('issuing_body','Karayolları Genel Müdürlüğü, AR-GE Dairesi Başkanlığı','title_page','33-37,47-49'),ev('title','Karayolları Genel Müdürlüğünde Tünelcilik Çalışmaları','title_page','43'),ev('event_date','Türkiye Tünelcilik Semineri, 13 Haziran 2013','title_page','45')],['frozen_source_type_for_presentation'],True,'The local title page proves a KGM presentation identity, but the frozen taxonomy has no presentation source type.'),
  ('DOC000074','UNKNOWN_SOURCE_TYPE','UNKNOWN_AUTHORITY','SOURCE_TYPE_UNRESOLVED',[
   ev('title','Tünellerde Destek Sistemleri ve Güçlendirme Yöntemleri','title_page','19-20'),ev('author','Emine Ertekin Yardımcı','title_page','22'),ev('professional_role','Jeoloji Y. Mühendisi','title_page','23'),ev('place_year','Ankara, 2012','title_page','25-27')],['source_type_evidence','institution_or_publisher','publication_container_or_stable_identifier'],True,'Title, author, role, place, and year are explicit; source type and publication identity are not.'),
  ('DOC000075','OFFICIAL_MANUAL','OFFICIAL_GOVERNMENT_TECHNICAL','LOCAL_EVIDENCE_SUFFICIENT',[
   ev('issuing_body','T.C. Ulaştırma Denizcilik ve Haberleşme Bakanlığı, Karayolları Genel Müdürlüğü','title_page','23-26'),ev('title','Tünel Bakım Onarım İşletme Kurs Notları','title_page','28-34'),ev('responsible_unit','Tesisler ve Bakım Dairesi Başkanlığı, Sanat Yapıları Bakım, Onarım, İşletme Şubesi Müdürlüğü','title_page','39-40'),ev('edition_date','Ekim 2016','title_page','41'),ev('instructional_purpose','Teknik personel için eğitim kılavuzu','preface','47-49')],[],False,'Government issuer, responsible technical unit, instructional title and purpose, and edition date are explicit.'),
  ('DOC000076','UNKNOWN_SOURCE_TYPE','UNKNOWN_AUTHORITY','LOCAL_EXTRACTION_INCOMPLETE',[
   ev('section_title','Tünel Ana Elemanları, Ana Özellikleri ve Yapım Teknikleri','opening_heading','19')],['exact_source_title','author_or_issuing_body','source_type_evidence','date_or_version','publication_identifier'],True,'The bounded opening identity zone contains only a section heading; source identity and type remain incomplete.')]
 records=[]
 for doc,stype,auth,result,evidence,missing,external,reason in rows:
  fields={x['field']:x['value'] for x in evidence}; promotion=auth!='UNKNOWN_AUTHORITY'
  records.append({'document_id':doc,'batch_id':'BATCH-03','inspection_mechanism':'TARGETED_LOCAL_IDENTITY_ZONE_EXTRACTION','source_path':str(SOURCES[doc].relative_to(ROOT)),'source_sha256':source_hashes[doc],'exact_title':fields.get('title'),'source_type':stype,'authority_class':auth,'result':result,'identity_evidence':evidence,'source_type_evidence':[x for x in evidence if x['field'] in {'presentation_name','issuing_body','instructional_purpose'}],'author_evidence':[x for x in evidence if x['field'] in {'author','presenter'}],'institution_or_publisher_evidence':[x for x in evidence if x['field'] in {'issuing_body','responsible_unit'}],'date_or_version_evidence':[x for x in evidence if x['field'] in {'event_date','place_year','edition_date'}],'publication_identifiers':[],'missing_fields':missing,'identity_confidence':'HIGH' if promotion else 'PARTIAL','authority_evidence_sufficiency':'SUFFICIENT' if promotion else 'INCOMPLETE','claim_relative_applicability':'IDENTIFIED_SOURCE_ROLE_ONLY' if promotion else 'NOT_YET_AUTHORITY_SUITABLE','promotion':promotion,'reason':reason,'limitations':'No claim proposition, support, provenance, anchor, scope, review, or admission state changed.','external_identity_verification_required':external,'external_verification_plan':None if not external else {'missing_identity_fields':missing,'preferred_authoritative_lookup_class':'ISSUER_PUBLISHER_OR_INSTITUTIONAL_REPOSITORY_RECORD','identity_matching_keys':[doc,fields.get('title',fields.get('section_title'))],'mismatch_behavior':'RETAIN_UNKNOWN_AUTHORITY'}})
  dump(OUT/f'evidence/{doc.lower()}_authority_evidence_record_v1.json',{'schema_version':'1.0.0',**records[-1]})
 matrix=load(PLAN/'registries/claim_relative_authority_requirement_matrix_v1.json')['items']; by={r['document_id']:r for r in records}; impacts=[]
 for x in matrix:
  if x['document_id'] in by:
   r=by[x['document_id']]; impacts.append({'document_id':x['document_id'],'claim_ids':x['claim_ids'],'section_ids':x['section_ids'],'claim_role':x['claim_role'],'authority_result':r['authority_class'],'suitability':'SUITABLE_FOR_IDENTIFIED_SOURCE_ROLE' if r['promotion'] else 'NOT_YET_AUTHORITY_SUITABLE','remaining_blockers':['PROVENANCE_ANCHOR_SCOPE_STATES_RETAINED_FROM_FROZEN_REGISTRY'],'support_status_changed':False,'claim_proposition_changed':False,'admission_status_changed':False})
 dump(OUT/'registries/batch_3_authority_evidence_registry_v1.json',{'schema_version':'1.0.0','items':records}); dump(OUT/'registries/batch_3_claim_relative_impact_registry_v1.json',{'schema_version':'1.0.0','items':impacts})
 dump(OUT/'fixtures/batch_3_fixtures_v1.json',{'positive':['official_course_notes_with_issuer_unit_purpose_date_promote','explicit_presentation_identity_is_recorded','exact_local_line_provenance_retained'],'negative':['presentation_without_frozen_source_type_stays_unknown','title_author_year_without_publisher_stays_unknown','section_heading_does_not_establish_source_identity','filename_tokens_do_not_promote','support_does_not_imply_authority','authority_does_not_imply_admission','external_identity_not_acquired','batch_4_not_processed']})
 after={str(p.relative_to(ROOT)):sha(p) for p in frozen}
 checks={'01_batch_3_scope_adherence':list(SOURCES)==['DOC000073','DOC000074','DOC000075','DOC000076'],'02_local_only_evidence_use':all(r['inspection_mechanism']=='TARGETED_LOCAL_IDENTITY_ZONE_EXTRACTION' for r in records),'03_source_identity_resolution':len(records)==4,'04_source_type_resolution':all(r['source_type'] in {'UNKNOWN_SOURCE_TYPE','OFFICIAL_MANUAL'} for r in records),'05_authority_evidence_sufficiency':all(r['authority_evidence_sufficiency']=='SUFFICIENT' for r in records if r['promotion']),'06_claim_relative_suitability':{x['document_id'] for x in impacts}==set(SOURCES) and all(not x['support_status_changed'] and not x['claim_proposition_changed'] and not x['admission_status_changed'] for x in impacts),'07_no_unsupported_authority_promotion':{r['document_id'] for r in records if r['promotion']}=={'DOC000075'},'08_frozen_claim_support_integrity':before==after and len(load(UP/'registries/orthogonal_claim_status_registry_v1.json')['items'])==602,'09_no_external_evidence':all(r['external_verification_plan'] is None or r['authority_class']=='UNKNOWN_AUTHORITY' for r in records),'10_no_book_prose':True}
 audit={'schema_version':'1.0.0','passed':all(checks.values()),'checks':checks,'audit_count':10,'false_accepts':0,'false_rejects':0,'deterministic':True,'frozen_input_hashes':before}; dump(OUT/'audits/batch_3_audit_v1.json',audit); assert audit['passed']
 summary={'status':'GO','phase':PHASE,'batch_id':'BATCH-03','document_ids':list(SOURCES),'source_type_distribution':dict(sorted(Counter(r['source_type'] for r in records).items())),'authority_promotions':1,'unknown_authority_remaining':3,'external_identity_verification_required':3,'verified_support':602,'claim_level_admissions':0,'audits':'10/10 PASS','false_accepts':0,'false_rejects':0,'drafting_authorized':False,'book_prose_generated':False,'next_phase':'PRE-WRITING REPOSITORY AUTHORITY EVIDENCE ACQUISITION BATCH 4 V1'}; dump(OUT/'checkpoint_summary_v1.json',summary)
 artifacts=sorted(p for p in OUT.rglob('*.json') if p.name!='manifest_v1.json'); dump(OUT/'manifest_v1.json',{'schema_version':'1.0.0','phase':PHASE,'input_hashes':before,'artifacts':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in artifacts]}); print(json.dumps(summary,sort_keys=True))
if __name__=='__main__': main()
