from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/terminology_resolution_v1"


def load(relative: str) -> dict:
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def validate_candidate(candidate: dict, audit: dict | None = None) -> str:
    audit = audit or load("audits/terminology_evidence_audit_v1.json")
    if candidate["owner_claim_id"] != candidate["claim_id"]:
        return "TERM_CROSS_CLAIM_BORROWING"
    if candidate["source_case_id"] != candidate["case_id"]:
        return "TERM_WRONG_CASE_MAPPING"
    if candidate["language"] != "tr" or candidate["surface_term"] == audit["source_label"]:
        return "TERM_ENGLISH_LEAK"
    if candidate["surface_term"] == "kaya":
        return "TERM_GENERIC_ROCK_SUBSTITUTION"
    approved = audit["approved_mapping_check"]["approved_swelling_rock_terms"]
    if candidate["surface_term"] not in approved:
        return "TERM_UNSUPPORTED_SYNONYM"
    return "ACCEPT"


def evaluate() -> dict:
    audit = load("audits/terminology_evidence_audit_v1.json")
    fixtures = load("fixtures/negative_fixtures_v1.json")["fixtures"]
    results = [
        {"fixture_id": item["fixture_id"], "code": validate_candidate(item["candidate"], audit)}
        for item in fixtures
    ]
    return {
        "status": "NO_GO" if audit["decision_class"] != "CASE_1" else "GO",
        "decision_class": audit["decision_class"],
        "selected_term": audit["claim_owned_term_selected"],
        "fixture_results": results,
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
