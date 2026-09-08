import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_external_authority_identity_verification_batch_4_v1"
def load(path): return json.loads(path.read_text(encoding="utf-8"))


def test_batch_4_fail_closed_course_deck_separation_and_anchors():
    subprocess.run(["python3", str(ROOT / "scripts/103_prewriting_external_authority_identity_verification_batch_4_v1.py")], check=True)
    records = load(OUT / "registries/batch_4_external_authority_registry_v1.json")["items"]
    assert [x["source_id"] for x in records] == ["DOC000073", "DOC000074", "DOC000214", "DOC000215"]
    assert all(x["identity_match_status"] == "NO_RELIABLE_MATCH" and x["authority_class"] == "UNKNOWN_AUTHORITY" and not x["promotion"] for x in records)
    assert all(not x["technical_content_captured"] and not x["support_status_changed"] and not x["admission_status_changed"] and not x["claim_proposition_changed"] for x in records)
    assert all(x["course_deck_separation_applied"] and x["anchor_history_preserved"] for x in records[2:])
    assert all(x[k] in {"EXTERNALLY_UNVERIFIED", "UNKNOWN", "NOT_AUTHORITY_SUITABLE_IDENTITY_OR_VERSION_UNRESOLVED"} for x in records[2:] for k in ["material_identity", "presenter_author_identity", "host_institution", "issuing_publishing_authority", "technical_authority", "claim_relative_suitability"])


def test_batch_4_contract_fixtures_audits_regressions_and_integrity():
    contract = load(OUT / "contracts/acceptance_contract_v1.json")
    fixtures = load(OUT / "fixtures/batch_4_fixtures_v1.json")
    audit = load(OUT / "audits/batch_4_audit_v1.json")
    manifest = load(OUT / "manifest_v1.json")
    assert contract["scope"] == ["DOC000073", "DOC000074", "DOC000214", "DOC000215"]
    assert len(fixtures["positive"]) == 6 and len(fixtures["negative"]) == 11
    assert len(audit["audits"]) == 12 and all(x["result"] == "PASS" for x in audit["audits"])
    assert audit["false_accepts"] == audit["false_rejects"] == 0
    assert all(audit[k] == "PASS" for k in ["batch_1_regression", "batch_2_doc000072_regression", "batch_3_doc000165_conflict_regression", "doc000214_anchor_history", "doc000215_anchor_history", "frozen_input_integrity", "deterministic_processing", "external_boundary"])
    assert audit["verified_support"] == 602 and audit["claim_level_admissions"] == 0
    assert len(manifest["outputs"]) == len(manifest["output_hashes"])
