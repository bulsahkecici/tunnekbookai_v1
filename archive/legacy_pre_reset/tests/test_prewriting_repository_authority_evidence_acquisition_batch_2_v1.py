import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/book/prewriting_repository_authority_evidence_acquisition_batch_2_v1'
def load(p): return json.loads(p.read_text())
def test_batch_2_execution():
 subprocess.run([sys.executable,str(ROOT/'scripts/92_prewriting_repository_authority_evidence_acquisition_batch_2_v1.py')],check=True)
 s=load(OUT/'checkpoint_summary_v1.json'); a=load(OUT/'audits/batch_2_audit_v1.json')
 assert s['status']=='GO' and s['authority_promotions']==2 and s['unknown_authority_remaining']==2
 assert a['passed'] and a['audit_count']==10 and all(a['checks'].values())
def test_fail_closed_and_orthogonal():
 rs=load(OUT/'registries/batch_2_authority_evidence_registry_v1.json')['items']
 impacts=load(OUT/'registries/batch_2_claim_relative_impact_registry_v1.json')['items']
 assert {r['document_id'] for r in rs if r['authority_class']=='UNKNOWN_AUTHORITY'}=={'DOC000045','DOC000072'}
 assert all(not x['support_status_changed'] and not x['admission_status_changed'] for x in impacts)
