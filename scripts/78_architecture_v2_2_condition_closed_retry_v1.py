from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/architecture_v2_2_retry_v1_rerun"
CLOSURE_BASE = ROOT / "data/book/drafting/sec_02_2/claim_role_condition_closure_v1"


def _module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


integration = _module(
    "condition_closed_retry_parent",
    ROOT / "scripts/75_architecture_v2_2_retry_integration_v1.py",
)
closure = _module(
    "condition_closed_retry_gate",
    ROOT / "scripts/77_claim_role_condition_closure_v1.py",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def closure_gate() -> dict:
    plan = load(CLOSURE_BASE / "proof/allocated_role_condition_plan_v1.json")
    result = closure.validate(plan)
    proof = load(CLOSURE_BASE / "audits/closure_proof_v1.json")
    if result["status"] != "ACCEPT" or proof["status"] != "PASS":
        raise RuntimeError("claim-role condition closure failed before renderer call")
    return proof


def _apply_safe_allocation(draft: dict) -> None:
    allocation = load(CLOSURE_BASE / "audits/p0_008_safe_allocation_v1.json")
    for instance in allocation["safe_instances"]:
        unit = next(row for row in draft["units"] if row["unit_id"] == instance["unit_id"])
        owned = [row["surface"] for row in instance["owns"] if row["scope"] == "UNIT"]
        for surface in owned:
            if surface.casefold() not in unit["text"].casefold():
                unit["text"] = f"{surface} {unit['text'][0].lower()}{unit['text'][1:]}"


def build(projected: bool = False) -> tuple[dict, list[dict]]:
    draft, layout = integration.build(projected)
    _apply_safe_allocation(draft)
    draft["draft_id"] = "SEC-02-2-V2-2-TECHNICAL-STYLE-RETRY-V1-RERUN"
    draft["draft_version"] = "tunnelbook-rendered-draft-ir-v2.2-condition-closed-retry-v1"
    return draft, layout


def evaluate() -> dict:
    proof = closure_gate()
    visible, layout = build(False)
    projected, _ = build(True)
    validation = integration.validate_draft(visible, projected)
    markdown = integration.render_markdown(visible, layout)
    return {
        "status": "GO" if validation["status"] == "ACCEPT" else "NO_GO",
        "closure_proof": {
            "status": proof["status"],
            "roles": f"{proof['fully_feasible_instances']}/{proof['allocated_claim_role_instances']}",
            "conditions": f"{proof['condition_requirements_closed']}/{proof['condition_requirements']}",
            "dependencies": f"{proof['dependency_requirements_closed']}/{proof['dependency_requirements']}",
        },
        "draft_ir": visible,
        "markdown": markdown,
        "validation": validation,
        "accounting": {
            "model_generation_calls": 0,
            "retrieval_calls": 0,
            "qdrant_writes": 0,
            "corpus_wide_reads": 0,
            "post_render_model_passes": 0,
        },
    }


if __name__ == "__main__":
    sys.stdout.buffer.write(integration.canonical_bytes(evaluate()))
