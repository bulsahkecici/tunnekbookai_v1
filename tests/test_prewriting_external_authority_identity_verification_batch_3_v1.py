import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_external_authority_identity_verification_batch_3_v1"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_batch_3_identity_authority_and_fail_closed_outcomes():
    subprocess.run(["python3", str(ROOT / "scripts/102_prewriting_external_authority_identity_verification_batch_3_v1.py")], check=True)
    records = load(OUT / "registries/batch_3_external_authority_registry_v1.json")["items"]
    assert [x["source_id"] for x in records] == ["DOC000045", "DOC000100", "DOC000163", "DOC000164", "DOC000165"]
    assert [x["identity_match_status"] for x in records] == ["NO_RELIABLE_MATCH", "EXACT_IDENTITY_MATCH", "EXACT_IDENTITY_MATCH", "PARTIAL_IDENTITY_MATCH", "IDENTITY_CONFLICT"]
    assert [x["promotion"] for x in records] == [False, True, True, False, False]
    assert all(not x["peer_review_verified"] for x in records)
    assert all(not x["technical_content_captured"] for x in records)
    assert all(not x["support_status_changed"] and not x["admission_status_changed"] and not x["claim_proposition_changed"] for x in records)


def test_batch_3_contract_fixtures_audits_ledgers_and_integrity():
    contract = load(OUT / "contracts/acceptance_contract_v1.json")
    fixtures = load(OUT / "fixtures/batch_3_fixtures_v1.json")
    audit = load(OUT / "audits/batch_3_audit_v1.json")
    manifest = load(OUT / "manifest_v1.json")
    assert contract["scope"] == ["DOC000045", "DOC000100", "DOC000163", "DOC000164", "DOC000165"]
    assert len(fixtures["positive"]) == 6 and len(fixtures["negative"]) == 11
    assert len(audit["audits"]) == 12 and all(x["result"] == "PASS" for x in audit["audits"])
    assert audit["false_accepts"] == audit["false_rejects"] == 0
    assert audit["batch_1_regression"] == audit["batch_2_doc000072_regression"] == "PASS"
    assert audit["frozen_input_integrity"] == audit["deterministic_processing"] == audit["external_boundary"] == "PASS"
    assert audit["verified_support"] == 602 and audit["claim_level_admissions"] == 0
    assert len(load(OUT / "registries/batch_3_provenance_ledger_v1.json")["items"]) == 5
    assert len(manifest["outputs"]) == len(manifest["output_hashes"])
