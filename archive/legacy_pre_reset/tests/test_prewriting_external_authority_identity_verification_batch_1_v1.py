import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_external_authority_identity_verification_batch_1_v1"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_batch_1_external_authority_verification():
    subprocess.run(["python3", str(ROOT / "scripts/100_prewriting_external_authority_identity_verification_batch_1_v1.py")], check=True)
    records = load(OUT / "registries/batch_1_external_authority_registry_v1.json")["items"]
    assert [x["source_id"] for x in records] == ["DOC000225", "DOC000267", "DOC000268", "DOC000269"]
    assert all(x["issuing_authority"] == "Kamu İhale Kurumu" for x in records)
    assert all(x["authority_status"] == "UNKNOWN" and not x["promotion"] for x in records)
    assert all(x["authority_disposition"] == "AUTHORITY_PARTIALLY_VERIFIED" for x in records)
    assert all(x["version_match_status"] in {"VERSION_PARTIAL", "VERSION_UNRESOLVED"} for x in records)
    assert all("technical" not in json.dumps(x["external_record_identity"]).lower() for x in records)


def test_contract_fixtures_audits_and_integrity():
    contract = load(OUT / "contracts/acceptance_contract_v1.json")
    fixtures = load(OUT / "fixtures/batch_1_fixtures_v1.json")
    audit = load(OUT / "audits/batch_1_audit_v1.json")
    assert contract["scope"] == ["DOC000225", "DOC000267", "DOC000268", "DOC000269"]
    assert len(fixtures["positive"]) == 5 and len(fixtures["negative"]) == 10
    assert len(audit["audits"]) == 12 and all(x["result"] == "PASS" for x in audit["audits"])
    assert audit["false_accepts"] == audit["false_rejects"] == 0
    assert audit["verified_support"] == 602 and audit["claim_level_admissions"] == 0
    assert audit["frozen_input_integrity"] == audit["deterministic_processing"] == "PASS"
