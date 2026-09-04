import hashlib, json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/book/prewriting_final_readiness_writing_authorization_audit_v1'

def load(name): return json.loads((OUT/name).read_text())

def test_final_gate_invariants_and_determinism():
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.json')}
    subprocess.run([sys.executable,str(ROOT/'scripts/107_prewriting_final_readiness_writing_authorization_audit_v1.py')],check=True,capture_output=True)
    after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.json')}
    assert before==after
    audit=load('final_readiness_audit_v1.json'); tiers=load('evidence_use_tier_registry_v1.json'); sections=load('section_readiness_registry_v1.json')
    assert audit['decision']=='PRE-WRITING_READY / DRAFTING_NOT_AUTHORIZED'
    assert audit['state_reconciliation']['verified_support_claims']==602
    assert audit['drafting_authorized'] is False and audit['book_prose_generated'] is False
    assert sum(tiers['distribution'].values())==602 and all(x['support_status']=='VERIFIED_SUPPORT' for x in tiers['items'])
    assert all(x['tier']=='RESTRICTED_OR_EXCLUDED' for x in tiers['items'] if x['document_id'] in {'DOC000072','DOC000165'})
    assert sum(sections['distribution'].values())==60
    assert audit['cost_dependencies']['global_blocker'] is False
    assert all(v=='REGISTERED_NOT_SATISFIED' for k,v in audit['cost_dependencies'].items() if k.endswith('_REQUIRED'))
