import hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_9_v1"
SCRIPT = ROOT / "scripts/99_prewriting_repository_authority_evidence_acquisition_batch_9_v1.py"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def digests(): return {str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.rglob("*.json"))}

def test_batch_9_execution_determinism_and_gates():
    subprocess.run([sys.executable, str(SCRIPT)], check=True); first = digests()
    subprocess.run([sys.executable, str(SCRIPT)], check=True); assert first == digests()
    s = load(OUT / "checkpoint_summary_v1.json"); a = load(OUT / "audits/batch_9_audit_v1.json")
    assert s["status"] == "GO_LOCAL_FIRST_AUTHORITY_ACQUISITION_COMPLETE"
    assert a["passed"] and a["audit_count"] == 12 and a["false_accepts"] == a["false_rejects"] == 0
    assert a["deterministic_output"] == a["frozen_integrity"] == "PASS" and all(a["checks"].values())

def test_batch_9_fail_closed_identity_and_orthogonality():
    rs = load(OUT / "registries/batch_9_authority_evidence_registry_v1.json")["items"]
    impacts = load(OUT / "registries/batch_9_claim_relative_impact_registry_v1.json")["items"]
    assert {r["document_id"] for r in rs} == {"DOC000302", "DOC000306"}
    assert all(r["exact_title"] and r["source_type"] == "UNKNOWN_SOURCE_TYPE" for r in rs)
    assert all(r["result"] == "SOURCE_TYPE_UNRESOLVED" and not r["promotion"] for r in rs)
    assert all(not x["support_status_changed"] and not x["claim_proposition_changed"] for x in impacts)

def test_cumulative_rollup_and_external_queue():
    r = load(OUT / "registries/cumulative_34_source_authority_rollup_v1.json")
    q = load(OUT / "plans/external_identity_verification_queue_v1.json")
    assert r["coverage"] == "34/34" and r["authority_promotions"] == 5 and r["unknown_authority"] == 29
    assert r["source_type_unresolved"] == 17 and q["queue_count"] == 27
    assert sum(x["count"] for x in q["batches"]) == 27 and all(3 <= x["count"] <= 5 for x in q["batches"])
    required = {"source_id", "local_identity", "source_type", "missing_identity_fields", "preferred_authoritative_lookup_class", "fallback_lookup_class", "identity_matching_keys", "mismatch_behavior", "version_or_date_requirements", "claim_relative_authority_requirement", "provenance_requirements"}
    assert all(required <= set(x) for x in q["items"])

def test_positive_negative_controls():
    f = load(OUT / "fixtures/batch_9_fixtures_v1.json")
    assert len(f["positive"]) == 4 and len(f["negative"]) == 10
    assert "external_lookup_prohibited" in f["negative"] and "claim_mutation_rejected" in f["negative"]
