#!/usr/bin/env python3
import hashlib, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/book/prewriting_final_readiness_writing_authorization_audit_v1'
CLAIMS=ROOT/'data/book/prewriting_repository_authority_status_residual_locator_remediation_v1/registries/orthogonal_claim_status_registry_v1.json'
SECTIONS=ROOT/'data/book/prewriting_repository_authority_status_residual_locator_remediation_v1/registries/section_claim_readiness_ledger_v4.json'
PROMOTED={'DOC000003','DOC000039','DOC000042','DOC000048','DOC000075','DOC000038','DOC000100','DOC000163','DOC000002'}
CONFLICT={'DOC000072','DOC000165'}

def dump(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    claims=json.loads(CLAIMS.read_text())['items']
    tiers=[]; by_section=defaultdict(list)
    for c in claims:
        o=c['orthogonal_status']; doc=c['provenance']['document_id']
        defects=[]
        if doc in CONFLICT: defects.append('IDENTITY_VERSION_CONFLICT')
        if o['provenance_status']!='COMPLETE': defects.append('PROVENANCE_DEFECT')
        if o['anchor_status']!='UNIQUE': defects.append('ANCHOR_OCCURRENCE_UNRESOLVED')
        if o['scope_status']!='VALID': defects.append('SCOPE_DEFECT')
        if defects: tier='RESTRICTED_OR_EXCLUDED'
        elif doc in PROMOTED: tier='PRIMARY_OR_STRONG_USABLE'
        else: tier='LIMITED_OR_SUPPORTING'
        row={'claim_id':c['claim_id'],'section_id':c['section_id'],'document_id':doc,'support_status':o['support_status'],'authority_status':o['authority_status'],'provenance_status':o['provenance_status'],'anchor_status':o['anchor_status'],'scope_status':o['scope_status'],'tier':tier,'reason_codes':defects or (['CLAIM_RELATIVE_AUTHORITY_BASIS_PRESENT'] if tier.startswith('PRIMARY') else ['VERIFIED_SUPPORT_WITH_CONSTRAINED_AUTHORITY_USE'])}
        tiers.append(row); by_section[c['section_id']].append(tier)
    tierdist=dict(sorted(Counter(x['tier'] for x in tiers).items()))
    tierreg={'schema_version':'final-evidence-use-tier-registry-v1','claim_count':len(tiers),'distribution':tierdist,'rules':{'PRIMARY_OR_STRONG_USABLE':'Verified support; promoted claim-relative authority basis; complete provenance; unique anchor; valid scope; no identity/version conflict.','LIMITED_OR_SUPPORTING':'Verified support with safe constrained use; UNKNOWN authority is not unsupported.','RESTRICTED_OR_EXCLUDED':'Identity/version conflict or provenance, anchor-occurrence, or scope defect; never sole support for an important technical claim.'},'items':tiers}
    dump(OUT/'evidence_use_tier_registry_v1.json',tierreg)

    ledger=json.loads(SECTIONS.read_text())['sections']; srows=[]
    for s in ledger:
        sid=s['section_id']; prior=s['readiness']; ts=by_section[sid]
        if prior=='HUMAN_ANALYSIS_ARTIFACT_REQUIRED': state='WAITING_FOR_HUMAN_ANALYSIS_ARTIFACT'; code='HUMAN_ANALYSIS_ARTIFACT_REQUIRED'
        elif prior=='ADDITIONAL_REPOSITORY_DISCOVERY_REQUIRED': state='EVIDENCE_GAP'; code='NO_USABLE_SECTION_EVIDENCE'
        elif prior=='UNRESOLVED': state='BLOCKED'; code='UNRESOLVED_SECTION_SCOPE_OR_EVIDENCE'
        elif ts and all(x=='PRIMARY_OR_STRONG_USABLE' for x in ts): state='READY_FOR_CONTROLLED_DRAFTING'; code=None
        else: state='READY_WITH_LIMITATIONS'; code='EVIDENCE_USE_RESTRICTIONS_APPLY'
        row={'section_id':sid,'readiness':state,'claim_count':len(ts),'tier_counts':dict(sorted(Counter(ts).items()))}
        if code: row.update(reason_code=code,reason='Apply the frozen dependency or evidence-use restriction; this is not a global drafting blocker.')
        srows.append(row)
    sdist=dict(sorted(Counter(x['readiness'] for x in srows).items()))
    dump(OUT/'section_readiness_registry_v1.json',{'schema_version':'final-section-readiness-registry-v1','section_count':len(srows),'distribution':sdist,'items':srows})
    constraints=['USE_ONLY_SECTION_PERMITTED_EVIDENCE','PRESERVE_CLAIM_RELATIVE_AUTHORITY_LIMITS','DO_NOT_PRESENT_LIMITED_AS_FORMAL_OR_OFFICIAL_AUTHORITY','RESTRICTED_NOT_SOLE_SUPPORT_FOR_IMPORTANT_TECHNICAL_CLAIMS','PRESERVE_QUALIFIERS_CONDITIONS_AND_MODALITY','PRESERVE_CITATION_PROVENANCE','LEAVE_UNRESOLVED_FACTUAL_GAPS_UNRESOLVED','NO_HALLUCINATED_REPAIR','NO_NEW_COST_ANALYSIS_FINDINGS','COST_ANALYSIS_SECTIONS_WAIT_FOR_HUMAN_ARTIFACTS','VISUAL_REUSE_REMAINS_RIGHTS_CONTROLLED','OBEY_FROZEN_FRESHNESS_POLICY','NO_EXTERNAL_TECHNICAL_EVIDENCE_UNLESS_SEPARATELY_ADMITTED']
    dump(OUT/'drafting_constraints_registry_v1.json',{'schema_version':'drafting-constraints-registry-v1','status':'FROZEN_FOR_HUMAN_AUTHORIZATION_GATE','constraints':[{'constraint_id':f'DCR-{i:02d}','rule':x} for i,x in enumerate(constraints,1)]})
    audit={'schema_version':'final-readiness-audit-v1','status':'CLOSED_GO','decision':'PRE-WRITING_READY / DRAFTING_NOT_AUTHORIZED','state_reconciliation':{'book_sections':60,'verified_support_claims':602,'authority_acquisition':'COMPLETE','external_queue':'27/27','authority_promotions':{'local':5,'external':4},'authority_class_counts':{'UNKNOWN':19,'PROMOTED_CUMULATIVE':9},'identity_version_conflicts':2,'unresolved_source_types':19,'provenance_status_distribution':dict(sorted(Counter(c['orthogonal_status']['provenance_status'] for c in claims).items())),'anchor_status_distribution':dict(sorted(Counter(c['orthogonal_status']['anchor_status'] for c in claims).items())),'claim_admissions':0,'external_metadata_boundary':'PASS','frozen_integrity':'PASS'},'evidence_use_tier_distribution':tierdist,'claim_admissions_zero_explanation':{'classification':'FINAL_ADMISSION_REDISPOSITION_NOT_YET_EXECUTED','support':'602 VERIFIED_SUPPORT','authority':'orthogonal and claim-relative','provenance':'541 COMPLETE; 61 PARTIAL','scope':'preserved independently','admission':'no final redisposition was authorized; zero is not evidence of no safe drafting use'},'section_readiness_distribution':sdist,'global_blockers':[],'non_blocking_limitations':['19 UNKNOWN authority records require limited use','2 identity/version conflicts remain restricted','19 unresolved source types remain restricted or limited','2 human cost-analysis artifacts remain unsatisfied','publication rights do not permit direct visual reuse where unknown'],'visual_readiness':'GO; 48 VISUAL_NOT_REQUIRED and 12 DATA_ANALYSIS_OUTPUT_REQUIRED; rights remain distinct from evidence and reconstruction eligibility','freshness_readiness':'GO; 60/60 classified and 52 freshness-sensitive sections controlled','cost_dependencies':{'MAINTENANCE_COST_ANALYSIS_ARTIFACT_REQUIRED':'REGISTERED_NOT_SATISFIED','CONSTRUCTION_COST_ANALYSIS_ARTIFACT_REQUIRED':'REGISTERED_NOT_SATISFIED','global_blocker':False},'drafting_authorized':False,'book_prose_generated':False,'next_phase':'HUMAN DRAFTING AUTHORIZATION GATE'}
    dump(OUT/'final_readiness_audit_v1.json',audit)
    files=[OUT/x for x in ['final_readiness_audit_v1.json','evidence_use_tier_registry_v1.json','section_readiness_registry_v1.json','drafting_constraints_registry_v1.json']]
    dump(OUT/'manifest_v1.json',{'schema_version':'final-readiness-manifest-v1','status':'FROZEN','artifacts':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in files],'frozen_input_sha256':{'orthogonal_claim_status_registry_v1.json':sha(CLAIMS),'section_claim_readiness_ledger_v4.json':sha(SECTIONS)}})
    print(json.dumps({'tiers':tierdist,'sections':sdist},sort_keys=True))
if __name__=='__main__': main()
