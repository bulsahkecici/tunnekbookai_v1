import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_7_v1"
SCRIPT = ROOT / "scripts/97_prewriting_repository_authority_evidence_acquisition_batch_7_v1.py"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest_outputs():
    return {str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.rglob("*.json"))}


def test_batch_7_execution_and_determinism():
    subprocess.run([sys.executable, str(SCRIPT)], check=True)
    first = digest_outputs()
    subprocess.run([sys.executable, str(SCRIPT)], check=True)
    assert first == digest_outputs()
    summary = load(OUT / "checkpoint_summary_v1.json")
    audit = load(OUT / "audits/batch_7_audit_v1.json")
    assert summary["status"] == "GO" and summary["authority_promotions"] == 0 and summary["unknown_authority_remaining"] == 4
    assert audit["passed"] and audit["audit_count"] == 10 and audit["false_accepts"] == audit["false_rejects"] == 0
    assert audit["deterministic_output"] == audit["frozen_integrity"] == "PASS" and all(audit["checks"].values())


def test_explicit_identity_source_type_and_authority_rules():
    records = load(OUT / "registries/batch_7_authority_evidence_registry_v1.json")["items"]
    assert {r["document_id"] for r in records} == {"DOC000214", "DOC000215", "DOC000216", "DOC000217"}
    assert all(r["exact_title"] and r["author_evidence"] and r["date_or_version_evidence"] for r in records)
    assert all(r["canonical_source_relationship"]["canonical_source_sha256"] for r in records)
    assert {r["source_type"] for r in records} == {"UNKNOWN_SOURCE_TYPE"}
    assert all(r["result"] == "SOURCE_TYPE_UNRESOLVED" and r["authority_class"] == "UNKNOWN_AUTHORITY" and not r["promotion"] for r in records)


def test_negative_controls_and_orthogonality():
    fixtures = load(OUT / "fixtures/batch_7_fixtures_v1.json")
    impacts = load(OUT / "registries/batch_7_claim_relative_impact_registry_v1.json")["items"]
    required = {"filename_does_not_imply_authority", "folder_path_does_not_imply_authority", "body_institution_mention_does_not_imply_authority", "legacy_c_d_label_does_not_imply_authority", "topical_similarity_does_not_resolve_source_type", "unsupported_identity_resolution_rejected", "claim_mutation_rejected", "external_lookup_prohibited", "book_prose_generation_prohibited", "batch_8_not_processed"}
    assert required <= set(fixtures["negative"])
    assert all(not x["support_status_changed"] and not x["claim_proposition_changed"] and not x["admission_status_changed"] for x in impacts)
