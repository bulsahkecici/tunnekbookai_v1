import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/book/prewriting_repository_authority_evidence_acquisition_planning_v1'
def test_plan():
    subprocess.run([sys.executable,str(ROOT/'scripts/90_prewriting_repository_authority_evidence_acquisition_planning_v1.py')],check=True)
    gaps=json.loads((OUT/'registries/authority_evidence_gap_registry_v1.json').read_text())['items']
    audit=json.loads((OUT/'audits/authority_evidence_planning_audit_v1.json').read_text())
    assert len(gaps)==34 and audit['passed'] and audit['verified_support']==602
    assert audit['authority_promotions']==audit['claim_level_admissions']==audit['external_browsing']==0
def test_boundaries_and_batches():
    types=json.loads((OUT/'registries/source_type_candidate_registry_v1.json').read_text())['items']
    ext=json.loads((OUT/'plans/external_identity_verification_plan_v1.json').read_text())
    batches=json.loads((OUT/'plans/authority_evidence_batch_plan_v1.json').read_text())['items']
    assert all(x['candidate_only'] and x['authority_effect']=='NONE' for x in types)
    assert not ext['external_technical_evidence_permitted']
    assert sum(x['size'] for x in batches)==34 and all(2<=x['size']<=5 for x in batches)
