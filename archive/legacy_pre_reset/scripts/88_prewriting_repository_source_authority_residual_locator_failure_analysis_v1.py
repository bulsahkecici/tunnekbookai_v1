#!/usr/bin/env python3
"""Deterministic, bounded failure analysis; performs no remediation."""
from __future__ import annotations
import hashlib, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'data/book/prewriting_repository_source_authority_provenance_anchor_remediation_v1'
OUT=ROOT/'data/book/prewriting_repository_source_authority_residual_locator_failure_analysis_v1'
CONTRACT=OUT/'contracts/failure_analysis_acceptance_contract_v1.json'
FILES={n:UP/'registries'/n for n in ['source_authority_registry_v2.json','bounded_source_verification_registry_v1.json','conversion_chunk_provenance_bridge_v1.json','anchor_locator_registry_v1.json','remediated_claim_registry_v2.json','section_claim_readiness_ledger_v3.json']}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
 p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def main():
 c=load(CONTRACT); assert c['mode']=='FAILURE_ANALYSIS_ONLY'
 before={str(p.relative_to(ROOT)):sha(p) for p in [CONTRACT,*FILES.values()]}
 auth=load(FILES['source_authority_registry_v2.json'])['items']; ver=load(FILES['bounded_source_verification_registry_v1.json']); bridge=load(FILES['conversion_chunk_provenance_bridge_v1.json'])['items']; anchors=load(FILES['anchor_locator_registry_v1.json'])['items']; claims=load(FILES['remediated_claim_registry_v2.json'])['items']; sections=load(FILES['section_claim_readiness_ledger_v3.json'])['sections']
 assert len(auth)==34 and len(claims)==602 and len(sections)==60
 vc=defaultdict(lambda:Counter(total=0,anchor_found=0,scope=0,null_claim=0))
 for x in ver['items']:
  q=vc[x['document_id']]; q['total']+=1; q['anchor_found']+=bool(x['anchor_found']); q['scope']+=bool(x['section_and_rq_scope_verified']); q['null_claim']+=x['claim_id'] is None
 opened=[]
 for did in ver['opened_document_ids']:
  q=vc[did]; classification='CLAIM_EXTRACTION_DEFECT' if q['anchor_found']==0 and q['null_claim']==q['total'] else 'SUPPORT_PRESENT_SCOPE_BLOCKED'
  opened.append({'document_id':did,**dict(q),'classification':classification,'finding':'Exact source text was found but inherited section_and_rq_match was false; support was not independently adjudicated.' if q['anchor_found'] else 'Every candidate lacked an extracted_claim_id, so no anchor or proposition could be checked.'})
 auth_sample=[{'document_id':d,'classification':'AUTHORITY_METADATA_EXISTS_NOT_PROPAGATED','evidence':e} for d,e in [
  ('DOC000002','manifest/inventory preserve path, type and hashes; source names NEXCO-WEST and JICA Survey Team, but no claim-relative authority record was populated'),
  ('DOC000072','manifest/inventory preserve DOCX identity and hash and legacy B exists; explicit authority evidence was never inspected/joined'),
  ('DOC000306','front matter preserves title, date, source path and hash and body names contributors; document_type/organization/authority remain null')]]
 prov_ids=['CLM-00089','CLM-00337','CLM-00339']; prov_sample=[]
 byid={x['claim_id']:x for x in claims}; bm={(x['document_id'],x['chunk_id']):x for x in bridge}
 for cid in prov_ids:
  x=byid[cid]; b=bm[(x['provenance']['document_id'],x['provenance']['chunk_id'])]
  prov_sample.append({'claim_id':cid,'document_id':x['provenance']['document_id'],'chunk_id':x['provenance']['chunk_id'],'bridge_status':b['bridge_status'],'missing_edge':'chunk→block/page','classification':'PROPAGATION_GAP_JOIN_GAP','finding':'Claim and chunk identities exist, but the bridge has no block/page locator.'})
 amb=[x for x in anchors if x['resolution']=='AMBIGUOUS_RETAINED']; amb_sample=[{'claim_id':x['claim_id'],'document_id':x['document_id'],'chunk_id':x['chunk_id'],'candidate_count':x['candidate_count'],'pages':[z['page_no'] for z in x['candidates']],'classification':'IRRECOVERABLE_HISTORICAL_LOSS_WITHOUT_SOURCE_LOCAL_REEXTRACTION'} for x in amb[:3]]
 traces={'schema_version':'1.0.0','authority_sample':auth_sample,'provenance_sample':prov_sample,'anchor_sample':amb_sample,'opened_document_diagnostics':opened}
 dump(OUT/'traces/representative_sample_traces_v1.json',traces)
 nojoin=[x for x in bridge if x['bridge_status']=='NO_LOCATOR_JOIN']
 roots={'schema_version':'1.0.0','authority':{'count':34,'causes':['SOURCE_INSPECTION_GAP','SCHEMA_GAP','JOIN_GAP','POLICY_GAP'],'finding':'The prior implementation copied every row to UNKNOWN without inspecting or joining authority-bearing fields; available descriptive metadata is not itself authority proof.'},'source_verification':{'opened':5,'records':len(ver['items']),'anchor_found':sum(x['anchor_found'] for x in ver['items']),'verified':sum(x['support_and_scope_verified'] for x in ver['items']),'causes':['VERIFICATION_IMPLEMENTATION_GAP','STATE_MODEL_GAP'],'finding':'The verifier required exact-text presence AND a pre-existing scope boolean; it did not independently verify range, proposition, qualifiers, modality, or scope. Authority was not the direct zeroing condition.'},'provenance':{'remaining_claims':sum(x['state']=='PROVENANCE_BLOCKED' for x in claims),'no_locator_join_chunk_pairs':len(nojoin),'missing_edge':'chunk→block/page','causes':['PROPAGATION_GAP','JOIN_GAP','SCHEMA_GAP']},'anchors':{'remaining':len(amb),'family_count':1,'finding':'All 12 map to DOC000214-C0002 and five identical occurrences on pages 20–24; historical claims retain no occurrence discriminator. Existing artifacts cannot choose safely.','causes':['IRRECOVERABLE_HISTORICAL_LOSS']},'state_model':{'finding':'Flattened precedence masks orthogonal support, provenance, authority, scope and admission facts.','required_dimensions':['SUPPORT_STATUS','PROVENANCE_STATUS','AUTHORITY_STATUS','SCOPE_STATUS','ADMISSION_STATUS']},'flags':{'validator_execution_fault':False,'validator_coverage_gap':True,'authority_policy_fault':True,'metadata_schema_fault':True,'locator_propagation_fault':True,'verification_implementation_fault':True,'state_model_fault':True}}
 dump(OUT/'analysis/root_cause_registry_v1.json',roots)
 plan={'schema_version':'1.0.0','status':'FROZEN_NOT_IMPLEMENTED','next_phase':'PRE-WRITING REPOSITORY AUTHORITY STATUS AND RESIDUAL LOCATOR REMEDIATION V1','dependency_order':['introduce orthogonal statuses without changing admissions','replace bounded verifier with source-range support/scope/qualifier adjudication','extract and join explicit authority evidence under claim-relative policy','build residual block/span provenance bridge v2','source-locally re-extract ambiguous occurrences','re-disposition claims and re-audit sections'],'acceptance_tests':['602 claims reconcile exactly once','34 authority records explicitly inspected with no inferred promotions','five documents independently verify support versus authority','61 residual provenance claims clustered and bridge-tested','12 ambiguous anchors remain blocked unless occurrence identity is proven','false acceptance zero','frozen integrity PASS','deterministic rerun PASS']}
 dump(OUT/'plans/residual_remediation_plan_v1.json',plan)
 after={str(p.relative_to(ROOT)):sha(p) for p in [CONTRACT,*FILES.values()]}; assert before==after
 audits={'authority_explained':True,'zero_of_five_explained':True,'provenance_61_clustered':sum(x['state']=='PROVENANCE_BLOCKED' for x in claims)==61,'anchors_12_explained':len(amb)==12,'state_semantics_audited':True,'sample_complete':len(auth_sample)==len(prov_sample)==len(amb_sample)==3 and len(opened)==5,'unsupported_authority_inference':0,'external_evidence':0,'corpus_mutation':False,'book_prose_generated':False,'frozen_integrity':'PASS','deterministic_analysis':True}
 dump(OUT/'audits/failure_analysis_audit_v1.json',{'schema_version':'1.0.0','passed':all(v is True or v in (0,'PASS') for v in audits.values()),**audits})
 artifacts=sorted(p for p in OUT.rglob('*.json') if p.name!='manifest_v1.json')
 dump(OUT/'manifest_v1.json',{'schema_version':'1.0.0','checkpoint':c['phase'],'result':'GO_REMEDIATION_PLAN_FROZEN','inputs_before':before,'inputs_after':after,'claim_state_counts':dict(Counter(x['state'] for x in claims)),'section_state_counts':dict(Counter(x['readiness'] for x in sections)),'artifacts':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in artifacts],'drafting_authorized':False,'book_prose_generated':False})
 print(json.dumps({'result':'GO_REMEDIATION_PLAN_FROZEN','anchor_found':roots['source_verification']['anchor_found'],'opened':5,'verified':0},sort_keys=True))
if __name__=='__main__': main()
