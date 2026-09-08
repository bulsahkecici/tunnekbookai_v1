import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_external_authority_identity_verification_batch_2_v1"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_batch_2_identity_authority_and_fail_closed_conflict():
    subprocess.run(["python3", str(ROOT / "scripts/101_prewriting_external_authority_identity_verification_batch_2_v1.py")], check=True)
    records = load(OUT / "registries/batch_2_external_authority_registry_v1.json")["items"]
    assert [x["source_id"] for x in records] == ["DOC000038", "DOC000072", "DOC000098"]
    assert [x["identity_match_status"] for x in records] == ["EXACT_IDENTITY_MATCH", "CONFLICTING_IDENTITY_MATCH", "EXACT_IDENTITY_MATCH"]
    assert [x["promotion"] for x in records] == [True, False, False]
    assert records[1]["authority_status"] == "UNKNOWN" and records[1]["conflict_fields"]
    assert records[2]["authority_status"] == "UNKNOWN" and "source type does not imply authority" in " ".join(records[2]["limitations"])
    assert all(not x["technical_content_captured"] for x in records)
    assert all(not x["support_status_changed"] and not x["admission_status_changed"] and not x["claim_proposition_changed"] for x in records)


def test_contract_fixtures_audits_ledgers_and_integrity():
    contract = load(OUT / "contracts/acceptance_contract_v1.json")
    fixtures = load(OUT / "fixtures/batch_2_fixtures_v1.json")
    audit = load(OUT / "audits/batch_2_audit_v1.json")
    manifest = load(OUT / "manifest_v1.json")
    assert contract["scope"] == ["DOC000038", "DOC000072", "DOC000098"]
    assert len(fixtures["positive"]) == 6 and len(fixtures["negative"]) == 10
    assert len(audit["audits"]) == 12 and all(x["result"] == "PASS" for x in audit["audits"])
    assert audit["false_accepts"] == audit["false_rejects"] == 0
    assert audit["batch_1_regression"] == audit["frozen_input_integrity"] == audit["deterministic_processing"] == "PASS"
    assert audit["verified_support"] == 602 and audit["claim_level_admissions"] == 0
    assert len(load(OUT / "registries/batch_2_provenance_ledger_v1.json")["items"]) == 3
    assert len(manifest["outputs"]) == len(manifest["output_hashes"])
