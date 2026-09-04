"""Architecture V2.2 technical/style integration gate.

This module emits no prose and writes no files. It evaluates versioned declarative contracts and
returns either a loadable integration status or a deterministic refusal. There are no model,
retrieval, corpus, Qdrant, clock, randomness or post-render rewrite branches.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/architecture_v2_2/contracts"
REALIZATION = BASE / "claim_realization_contract_v2_2.json"
UNIVERSE = BASE / "planner_option_universe_v2_2.json"
STYLE = BASE / "deterministic_book_style_integration_v2_2.json"
RENDERER = BASE / "deterministic_renderer_contract_v2_2.json"
CITATIONS = (ROOT / "data/book/drafting/sec_02_2/technical_remediation_v1/contracts/"
             "citation_allocation_contract_v2.json")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(payload: dict) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def evaluate() -> dict:
    realization = load(REALIZATION)
    universe = load(UNIVERSE)
    style = load(STYLE)
    renderer = load(RENDERER)
    citations = load(CITATIONS)

    entries = {(entry.get("claim_id"), entry["role"]): entry
               for entry in realization["entries"]}
    failures: list[dict] = []
    for violation in universe["violations"]:
        for role in violation["required_not_available"]:
            entry = entries.get((violation["claim_id"], role))
            failures.append({
                "claim_id": violation["claim_id"],
                "role": role,
                "code": universe["refusal_code"],
                "entry_status": None if entry is None else entry["status"],
                "reason": violation["reason"],
            })

    if not style["deterministic"] or style["model_style_pass"] != "FORBIDDEN":
        failures.append({"code": "V22_STYLE_NOT_DETERMINISTIC"})
    if renderer["model_call_branch"] or renderer["post_render_style_branch"]:
        failures.append({"code": "V22_FORBIDDEN_RENDERER_BRANCH"})
    if citations["result"]["misleading_allocations_remaining"]:
        failures.append({"code": "V22_CITATION_ALLOCATION_INVALID"})

    status = "NO_GO" if failures else "GO"
    result = {
        "version": "tunnelbook-architecture-v2.2-integration-evaluation-v1",
        "status": status,
        "build_status": universe["build_status"],
        "failures": failures,
        "planner_payload_authorised": status == "GO",
        "section_draft_render_authorised": False,
        "model_calls": 0,
        "draft_renders": 0,
    }
    result["content_sha256"] = hashlib.sha256(canonical_bytes(result)).hexdigest()
    return result


if __name__ == "__main__":
    print(canonical_bytes(evaluate()).decode("utf-8"), end="")
