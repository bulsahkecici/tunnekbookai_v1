import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/book/prewriting_external_authority_identity_verification_batch_5_v1"
def load(p): return json.loads(p.read_text(encoding="utf-8"))

def test_batch_5_fail_closed_guards_and_boundary():
    subprocess.run(["python3",str(ROOT/"scripts/104_prewriting_external_authority_identity_verification_batch_5_v1.py")],check=True)
    records=load(OUT/"registries/batch_5_external_authority_registry_v1.json")["items"]
    assert [r["source_id"] for r in records]==["DOC000216","DOC000217","DOC000302"]
    assert all(r["identity_match_status"]=="NO_RELIABLE_MATCH" and r["source_type"]=="UNKNOWN_SOURCE_TYPE" and r["authority_class"]=="UNKNOWN_AUTHORITY" and not r["promotion"] for r in records)
    assert all(r["course_material_guard_applied"] for r in records[:2]) and records[2]["unknown_source_type_guard_applied"]
    assert all(not r["technical_content_captured"] and not r["support_status_changed"] and not r["admission_status_changed"] and not r["claim_proposition_changed"] for r in records)

def test_batch_5_fixtures_audits_integrity_and_next_scope():
    fixtures=load(OUT/"fixtures/batch_5_fixtures_v1.json"); audit=load(OUT/"audits/batch_5_audit_v1.json"); summary=load(OUT/"checkpoint_summary_v1.json"); manifest=load(OUT/"manifest_v1.json")
    assert len(fixtures["positive"])==6 and len(fixtures["negative"])==12
    assert len(audit["audits"])==12 and all(x["result"]=="PASS" for x in audit["audits"])
    assert audit["false_accepts"]==audit["false_rejects"]==0 and audit["verified_support"]==602 and audit["claim_level_admissions"]==0
    assert all(audit[k]=="PASS" for k in ["batch_1_regression","batch_2_doc000072_regression","batch_3_doc000165_conflict_regression","batch_4_regression","doc000216_course_guard","doc000217_course_guard","doc000302_unknown_type_guard","frozen_input_integrity","deterministic_processing","external_boundary"])
    assert summary["next_source_ids"]==["DOC000193","DOC000200","DOC000209","DOC000211"]
    assert len(manifest["outputs"])==len(manifest["output_hashes"])
