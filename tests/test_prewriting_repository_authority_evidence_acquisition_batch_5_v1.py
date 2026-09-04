import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'data/book/prewriting_repository_authority_evidence_acquisition_batch_5_v1'
def load(p): return json.loads(p.read_text())
def test_batch_5_execution():
 subprocess.run([sys.executable,str(ROOT/'scripts/95_prewriting_repository_authority_evidence_acquisition_batch_5_v1.py')],check=True)
 s=load(OUT/'checkpoint_summary_v1.json'); a=load(OUT/'audits/batch_5_audit_v1.json')
 assert s['status']=='GO' and s['authority_promotions']==0 and s['unknown_authority_remaining']==4
 assert a['passed'] and a['audit_count']==10 and a['false_accepts']==a['false_rejects']==0 and all(a['checks'].values())
def test_identity_type_and_fail_closed_rules():
 rs=load(OUT/'registries/batch_5_authority_evidence_registry_v1.json')['items']
 assert {r['document_id'] for r in rs}=={'DOC000105','DOC000163','DOC000164','DOC000165'}
 assert {r['source_type'] for r in rs}=={'JOURNAL_ARTICLE','CONFERENCE_PAPER','PROJECT_TECHNICAL_REPORT'}
 assert all(r['authority_class']=='UNKNOWN_AUTHORITY' and not r['promotion'] for r in rs)
 assert next(r for r in rs if r['document_id']=='DOC000105')['result']=='LOCAL_EVIDENCE_SUFFICIENT'
def test_orthogonality_and_prohibitions():
 impacts=load(OUT/'registries/batch_5_claim_relative_impact_registry_v1.json')['items']; fx=load(OUT/'fixtures/batch_5_fixtures_v1.json')
 assert all(not x['support_status_changed'] and not x['claim_proposition_changed'] and not x['admission_status_changed'] for x in impacts)
 assert {'filename_does_not_imply_authority','folder_path_does_not_imply_authority','body_institution_mention_does_not_imply_authority','legacy_c_d_label_does_not_imply_authority','external_lookup_prohibited','book_prose_generation_prohibited','batch_6_not_processed'} <= set(fx['negative'])
