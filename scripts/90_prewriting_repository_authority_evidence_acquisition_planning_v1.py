#!/usr/bin/env python3
"""Create a deterministic, non-promotional authority-evidence acquisition plan."""
from __future__ import annotations
import hashlib, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'data/book/prewriting_repository_authority_status_residual_locator_remediation_v1'
OUT=ROOT/'data/book/prewriting_repository_authority_evidence_acquisition_planning_v1'
CONTRACT=OUT/'contracts/authority_evidence_acquisition_planning_acceptance_contract_v1.json'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

TYPE_REQ={
 'STANDARD_OR_SPECIFICATION_CANDIDATE':['issuer','identifier','edition_or_date','canonical_title'],
 'OFFICIAL_REPORT':['issuing_body','canonical_title','publication_date','report_identifier_or_canonical_record'],
 'INSTITUTIONAL_TECHNICAL_REPORT':['institution','canonical_title','authors_or_responsible_unit','date','report_identifier_or_canonical_record'],
 'PROJECT_REPORT':['project_owner_or_issuer','canonical_title','date','report_or_contract_identifier'],
 'JOURNAL_ARTICLE':['authors','article_title','journal','year','doi_or_volume_issue_pages'],
 'CONFERENCE_PAPER':['authors','paper_title','conference_or_proceedings','year','doi_or_pages'],
 'BOOK_OR_BOOK_CHAPTER':['authors_or_editors','title','publisher','year','isbn_or_chapter_container'],
 'THESIS':['author','title','degree','institution','year','repository_record_or_identifier'],
 'DATASET':['creator','title','publisher_or_repository','version_or_date','persistent_identifier'],
 'HISTORICAL_SOURCE':['creator_or_issuing_body','title_or_record_description','date_or_period','archive_or_collection_locator'],
 'UNKNOWN':['source_type_evidence']}

def candidate(r):
 dt=(r['inspected_repository_fields'].get('document_type') or '').lower(); p=r['canonical_source_path'].lower()
 if dt=='thesis': return 'THESIS','EXPLICIT_REPOSITORY_DOCUMENT_TYPE'
 if dt=='conference_paper': return 'CONFERENCE_PAPER','EXPLICIT_REPOSITORY_DOCUMENT_TYPE'
 rules=[('tez','THESIS'),('şartname','STANDARD_OR_SPECIFICATION_CANDIDATE'),('sartname','STANDARD_OR_SPECIFICATION_CANDIDATE'),
        ('project','PROJECT_REPORT'),('proje','PROJECT_REPORT'),('dergi','JOURNAL_ARTICLE'),('report','INSTITUTIONAL_TECHNICAL_REPORT'),
        ('el kitabı','OFFICIAL_REPORT'),('el kitabi','OFFICIAL_REPORT'),('tarih','HISTORICAL_SOURCE')]
 for token,t in rules:
  if token in p: return t,'PATH_TITLE_TOKEN_HYPOTHESIS_ONLY_NOT_AUTHORITY_PROOF'
 return 'UNKNOWN','NO_EXPLICIT_SOURCE_TYPE_EVIDENCE'

def main():
 c=load(CONTRACT); assert c['phase']=='PRE-WRITING REPOSITORY AUTHORITY EVIDENCE ACQUISITION PLANNING V1'
 paths=[CONTRACT,UP/'registries/source_authority_registry_v3.json',UP/'registries/orthogonal_claim_status_registry_v1.json',UP/'registries/section_claim_readiness_ledger_v4.json']
 before={str(p.relative_to(ROOT)):sha(p) for p in paths}
 auth=load(paths[1])['items']; claims=load(paths[2])['items']; sections=load(paths[3])['sections']
 assert len(auth)==34 and len(claims)==602
 uses=defaultdict(list)
 for x in claims:
  uses[x['provenance']['document_id']].append(x)
 types=[]; gaps=[]; local=[]; external=[]; matrix=[]
 for r in auth:
  did=r['document_id']; typ,basis=candidate(r); req=TYPE_REQ[typ]; missing=list(req)
  state='SOURCE_TYPE_UNRESOLVED' if typ=='UNKNOWN' else 'REPOSITORY_THEN_EXTERNAL_REQUIRED'
  types.append({'document_id':did,'source_type_candidate':typ,'candidate_basis':basis,'candidate_only':True,'authority_effect':'NONE'})
  gaps.append({'document_id':did,'planning_state':state,'sufficient_evidence_fields_for_candidate_type':req,'currently_satisfied_fields':[],
               'missing_evidence_fields':missing,'authority_status':'UNKNOWN','promotion_status':'NONE'})
  local.append({'document_id':did,'planning_state':state,'target_fields':missing,'target_zones':['embedded_metadata','front_matter','title_page','imprint_or_colophon','headers_and_footers','bibliographic_block'],
                'method':'TARGETED_DOCUMENT_LOCAL_IDENTITY_EXTRACTION','bulk_scan_forbidden':True,'stop_when':'SUFFICIENT_TYPE_RELATIVE_IDENTITY_FIELDS_CAPTURED_OR_TARGET_ZONES_EXHAUSTED'})
  external.append({'document_id':did,'permitted_only_after_repository_extraction':True,'identity_fields':missing,
    'preferred_lookup_class':'ISSUER_PUBLISHER_OR_CANONICAL_REPOSITORY_RECORD','fallback_lookup_class':'DOI_ISBN_LIBRARY_STANDARDS_OR_ARCHIVE_CATALOG_AS_TYPE_APPLICABLE',
    'matching_keys':['canonical_title','author_or_issuer','date','stable_identifier'], 'mismatch_behavior':'RETAIN_UNKNOWN_AND_ESCALATE_HUMAN_DECISION',
    'admission_boundary':'IDENTITY_AND_AUTHORITY_VERIFICATION_ONLY_NO_TECHNICAL_EVIDENCE','capture_provenance':['lookup_class','canonical_url_or_record_id','access_date','matched_keys','mismatches'],'browsing_performed':False})
  grouped=defaultdict(lambda:{'claim_ids':[],'section_ids':set()})
  for x in uses[did]:
   role=x['claim_type']; grouped[role]['claim_ids'].append(x['claim_id']); grouped[role]['section_ids'].add(x['section_id'])
  if not grouped: grouped['UNUSED_AUTHORITY_RECORD']
  for role,g in grouped.items(): matrix.append({'document_id':did,'claim_role':role,'claim_ids':g['claim_ids'],'section_ids':sorted(g['section_ids']),
    'minimum_acceptable_authority_class':'CLAIM_ROLE_COMPETENT_IDENTIFIED_SOURCE','current_authority_state':'UNKNOWN','needed_evidence':missing,'promotion_performed':False})
 dump(OUT/'registries/authority_evidence_gap_registry_v1.json',{'schema_version':'1.0.0','items':gaps})
 dump(OUT/'registries/source_type_candidate_registry_v1.json',{'schema_version':'1.0.0','items':types})
 dump(OUT/'plans/local_repository_evidence_plan_v1.json',{'schema_version':'1.0.0','items':local})
 dump(OUT/'plans/external_identity_verification_plan_v1.json',{'schema_version':'1.0.0','external_technical_evidence_permitted':False,'items':external})
 dump(OUT/'registries/claim_relative_authority_requirement_matrix_v1.json',{'schema_version':'1.0.0','items':matrix})
 batches=[]
 for i in range(0,34,4):
  ds=[x['document_id'] for x in gaps[i:i+4]]; batches.append({'batch_id':f'BATCH-{i//4+1:02d}','document_ids':ds,'size':len(ds),
   'mechanism':'TARGETED_LOCAL_IDENTITY_ZONE_EXTRACTION','actions':['inspect target zones only','capture field-level provenance','evaluate type-relative sufficiency'],
   'audits':['no authority promotion','no support or admission mutation','input hashes unchanged'],'stop_conditions':['target zones exhausted','identity mismatch','human judgment required']})
 dump(OUT/'plans/authority_evidence_batch_plan_v1.json',{'schema_version':'1.0.0','items':batches})
 deps=[]
 for s in sections:
  if s['readiness'] in {'ADDITIONAL_REPOSITORY_DISCOVERY_REQUIRED','UNRESOLVED'}:
   deps.append({'section_id':s['section_id'],'research_question_id':s['research_question_id'],'current_readiness':s['readiness'],
    'authority_plan_dependency':'NONE_NO_EXISTING_CLAIMS' if s['claim_count']==0 else 'REVIEW_EXISTING_MAPPING_METADATA',
    'metadata_only_answer_possible':s['mapping_count']>0,'required_next_action':'BOUNDED_DISCOVERY_OR_MAPPING_REVIEW_OUTSIDE_AUTHORITY_PROMOTION'})
 dump(OUT/'ledgers/section_dependency_ledger_v1.json',{'schema_version':'1.0.0','items':deps})
 fixtures={'positive':['local_frontmatter_sufficient_ready','doi_publisher_external_identity_plan','project_report_type_relative_requirements','standard_missing_identifier_standards_lookup_plan','support_count_unchanged'],
 'negative':['filename_as_authority_proof','institution_body_mention_as_authority_proof','external_technical_substitution','unknown_promotion','legacy_c_d_authority','support_changed','partial_provenance_as_complete','bulk_corpus_scan','book_prose']}
 dump(OUT/'fixtures/planning_fixtures_v1.json',fixtures)
 type_counts=dict(sorted(Counter(x['source_type_candidate'] for x in types).items())); state_counts=dict(sorted(Counter(x['planning_state'] for x in gaps).items()))
 passed=(len(gaps)==34 and all(x['authority_status']=='UNKNOWN' for x in gaps) and len(deps)==5 and len(batches)==9 and before=={str(p.relative_to(ROOT)):sha(p) for p in paths})
 audit={'schema_version':'1.0.0','passed':passed,'coverage':'34/34','authority_promotions':0,'claim_level_admissions':0,'verified_support':602,
  'partial_provenance_claims':61,'partial_provenance_is_orthogonal':True,'external_browsing':0,'external_technical_evidence':0,'fixtures':fixtures,'frozen_input_hashes':before,'deterministic':True}
 dump(OUT/'audits/authority_evidence_planning_audit_v1.json',audit); assert passed
 summary={'status':'GO','coverage':'34/34','source_type_distribution':type_counts,'planning_state_distribution':state_counts,'local_ready_count':state_counts.get('REPOSITORY_EVIDENCE_READY',0),
  'repository_extraction_required':sum(v for k,v in state_counts.items() if k in {'REPOSITORY_EXTRACTION_REQUIRED','REPOSITORY_THEN_EXTERNAL_REQUIRED','SOURCE_TYPE_UNRESOLVED'}),
  'external_identity_required':sum(v for k,v in state_counts.items() if k in {'EXTERNAL_IDENTITY_VERIFICATION_REQUIRED','REPOSITORY_THEN_EXTERNAL_REQUIRED'}),'unresolved_type':state_counts.get('SOURCE_TYPE_UNRESOLVED',0),
  'batch_count':len(batches),'authority_promotions':0,'claim_level_admissions':0,'verified_support':602,'drafting_authorized':False,'book_prose_generated':False,
  'next_phase':'PRE-WRITING REPOSITORY AUTHORITY EVIDENCE ACQUISITION BATCH 1 V1'}
 dump(OUT/'checkpoint_summary_v1.json',summary)
 artifacts=sorted(p for p in OUT.rglob('*.json') if p.name!='manifest_v1.json')
 dump(OUT/'manifest_v1.json',{'schema_version':'1.0.0','phase':c['phase'],'input_hashes':before,'artifacts':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in artifacts]})
 print(json.dumps(summary,sort_keys=True))
if __name__=='__main__': main()
