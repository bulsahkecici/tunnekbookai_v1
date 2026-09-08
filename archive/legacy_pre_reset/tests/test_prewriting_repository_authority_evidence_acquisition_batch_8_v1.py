import hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_8_v1"
SCRIPT = ROOT / "scripts/98_prewriting_repository_authority_evidence_acquisition_batch_8_v1.py"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def digests(): return {str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.rglob("*.json"))}

def test_batch_8_execution_and_determinism():
    subprocess.run([sys.executable, str(SCRIPT)], check=True); first = digests()
    subprocess.run([sys.executable, str(SCRIPT)], check=True); assert first == digests()
    s = load(OUT / "checkpoint_summary_v1.json"); a = load(OUT / "audits/batch_8_audit_v1.json")
    assert s["status"] == "GO" and s["authority_promotions"] == 0 and s["unknown_authority_remaining"] == 4
    assert a["passed"] and a["audit_count"] == 11 and a["false_accepts"] == a["false_rejects"] == 0
    assert a["deterministic_output"] == a["frozen_integrity"] == "PASS" and all(a["checks"].values())

def test_explicit_identity_and_fail_closed_authority():
    rs = load(OUT / "registries/batch_8_authority_evidence_registry_v1.json")["items"]
    assert {r["document_id"] for r in rs} == {"DOC000225", "DOC000267", "DOC000268", "DOC000269"}
    assert all(r["exact_title"] and r["source_type"] == "STANDARD_SPECIFICATION" for r in rs)
    assert all(r["result"] == "EXTERNAL_IDENTITY_VERIFICATION_REQUIRED" and r["authority_class"] == "UNKNOWN_AUTHORITY" and not r["promotion"] for r in rs)

def test_negative_controls_orthogonality_and_ceiling():
    f = load(OUT / "fixtures/batch_8_fixtures_v1.json"); a = load(OUT / "audits/batch_8_audit_v1.json")
    required = {"filename_does_not_imply_authority", "folder_path_does_not_imply_authority", "body_institution_mention_does_not_imply_authority", "legacy_c_d_label_does_not_imply_authority", "topical_similarity_does_not_resolve_source_type", "unsupported_identity_resolution_rejected", "claim_mutation_rejected", "external_lookup_prohibited", "book_prose_generation_prohibited", "batch_9_not_processed"}
    assert required <= set(f["negative"])
    assert a["cumulative_observation"]["finding"] == "REPEATED_LOCAL_METADATA_CEILING" and not a["cumulative_observation"]["systemic_extraction_defect"]
    impacts = load(OUT / "registries/batch_8_claim_relative_impact_registry_v1.json")["items"]
    assert all(not x["support_status_changed"] and not x["claim_proposition_changed"] and not x["admission_status_changed"] for x in impacts)
