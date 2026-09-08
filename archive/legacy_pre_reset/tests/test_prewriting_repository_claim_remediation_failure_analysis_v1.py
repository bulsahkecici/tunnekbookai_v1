import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_repository_claim_remediation_failure_analysis_v1"


def load(relative):
    return json.loads((OUT / relative).read_text(encoding="utf-8"))


def tree_hashes():
    return {
        str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(OUT.rglob("*.json"))
    }


class FailureAnalysisTests(unittest.TestCase):
 def test_all_claims_have_one_primary_family_and_counts_reconcile(self):
    affected = load("registries/affected_record_registry_v1.json")["items"]
    assert len(affected) == len({x["claim_id"] for x in affected}) == 602
    assert Counter(x["state"] for x in affected) == {
        "AUTHORITY_INSUFFICIENT": 452,
        "PROVENANCE_BLOCKED": 113,
        "ANCHOR_AMBIGUOUS": 12,
        "SCOPE_INSUFFICIENT": 25,
    }
    assert all(x["primary_defect_family"] for x in affected)


 def test_each_family_has_two_representative_traces(self):
    samples = load("registries/representative_sample_trace_registry_v1.json")["items"]
    counts = Counter(x["family"] for x in samples)
    assert len(samples) == 8
    assert set(counts.values()) == {2}


 def test_anchor_trace_preserves_block_level_disambiguators(self):
    samples = load("registries/representative_sample_trace_registry_v1.json")["items"]
    anchor = next(x for x in samples if x["claim_id"] == "CLM-00137")
    matches = anchor["conversion_block_matches"]
    assert len(matches) == 5
    assert [p["page_no"] for x in matches for p in x["provenance"]] == [20, 21, 22, 23, 24]


 def test_fail_closed_boundaries_and_validator_diagnosis(self):
    ledger = load("registries/remediation_decision_ledger_v1.json")
    assert ledger["validator_execution_fault"] is False
    assert ledger["validator_coverage_gap"] is True
    assert ledger["false_authority_or_provenance_acceptance"] == 0
    assert ledger["drafting_authorized"] is False
    assert ledger["book_prose_generated"] is False


 def test_all_audits_pass_and_state_sync_scope_is_five_files(self):
    audits = [json.loads(p.read_text()) for p in sorted((OUT / "audits").glob("*.json"))]
    assert len(audits) == 9 and all(x["passed"] for x in audits)
    assert audits[-1]["file_count"] == 5


 def test_deterministic_rerun_and_frozen_inputs(self):
    before = tree_hashes()
    subprocess.run(
        ["python3", str(ROOT / "scripts/86_prewriting_repository_claim_remediation_failure_analysis_v1.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert tree_hashes() == before
    manifest = load("manifest_v1.json")
    assert manifest["input_hashes_before"] == manifest["input_hashes_after"]


if __name__ == "__main__":
    unittest.main()
