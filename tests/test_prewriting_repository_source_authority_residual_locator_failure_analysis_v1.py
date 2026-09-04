import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'data/book/prewriting_repository_source_authority_residual_locator_failure_analysis_v1'
def test_failure_analysis_is_deterministic_and_complete():
 subprocess.run([sys.executable,str(ROOT/'scripts/88_prewriting_repository_source_authority_residual_locator_failure_analysis_v1.py')],check=True)
 first=(OUT/'manifest_v1.json').read_bytes()
 subprocess.run([sys.executable,str(ROOT/'scripts/88_prewriting_repository_source_authority_residual_locator_failure_analysis_v1.py')],check=True)
 assert first==(OUT/'manifest_v1.json').read_bytes()
 m=json.loads(first); assert m['result']=='GO_REMEDIATION_PLAN_FROZEN' and sum(m['claim_state_counts'].values())==602
 a=json.loads((OUT/'audits/failure_analysis_audit_v1.json').read_text()); assert a['passed'] and a['frozen_integrity']=='PASS'
 r=json.loads((OUT/'analysis/root_cause_registry_v1.json').read_text()); assert r['source_verification']['anchor_found']==24 and r['source_verification']['verified']==0 and r['anchors']['remaining']==12
