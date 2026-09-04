import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def test_batches_6_7_sequential_fail_closed():
 for n in (6,7): subprocess.run(["python3",str(ROOT/f"scripts/{99+n}_prewriting_external_authority_identity_verification_batch_{n}_v1.py")],check=True)
 b6=load(ROOT/"data/book/prewriting_external_authority_identity_verification_batch_6_v1/checkpoint_summary_v1.json")
 b7=load(ROOT/"data/book/prewriting_external_authority_identity_verification_batch_7_v1/checkpoint_summary_v1.json")
 assert b6["status"]==b7["status"]=="CLOSED_GO" and b6["authority_promotions"]==0 and b6["unknown_remaining"]==4
 assert b7["authority_promotions"]==1 and b7["unknown_remaining"]==3 and b7["next_source_ids"]==[]
 assert b7["next_phase"]=="PRE-WRITING FINAL READINESS AND WRITING AUTHORIZATION AUDIT V1"
def test_boundaries_fixtures_audits_and_exact_jica_match():
 for n in (6,7):
  out=ROOT/f"data/book/prewriting_external_authority_identity_verification_batch_{n}_v1"
  a=load(out/f"audits/batch_{n}_audit_v1.json"); f=load(out/f"fixtures/batch_{n}_fixtures_v1.json")
  assert len(a["audits"])==12 and all(x["result"]=="PASS" for x in a["audits"])
  assert a["false_accepts"]==a["false_rejects"]==0 and a["external_boundary"]==a["frozen_input_integrity"]=="PASS"
  assert len(f["positive"])==6 and len(f["negative"])==12
 r=load(ROOT/"data/book/prewriting_external_authority_identity_verification_batch_7_v1/registries/batch_7_external_authority_registry_v1.json")["items"]
 assert r[0]["source_id"]=="DOC000002" and r[0]["promotion"] and r[0]["authority_class"]=="INSTITUTIONAL_TECHNICAL"
 assert all(not x["technical_content_captured"] and not x["support_status_changed"] and not x["admission_status_changed"] and not x["claim_proposition_changed"] for x in r)
