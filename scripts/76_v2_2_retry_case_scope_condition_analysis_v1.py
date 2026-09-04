"""Targeted, analysis-only probes for the preserved V2.2 retry condition failure.

No planner, renderer, retrieval, corpus, or Qdrant path is imported or executed.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/54_section_draft_validator_v1_2.py"
CLAIM_ID = "SEC-02-2-P0-008"
STATEMENT = "Belirli kaya koşullarında, tünel boyutuna bağlı olarak, kalınlık 300 mm ve daha fazla olabilir."
CASE_SCOPE = "ezilmiş kaya, sıkışan kaya."


def _load_validator():
    spec = importlib.util.spec_from_file_location("case_scope_analysis_validator_v1_2", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = _load_validator()
base = validator.base


def _unit(text: str, unit_id: str = "U-C-P02-S02"):
    return validator.DraftUnit(
        unit_id=unit_id,
        unit_type="PARAGRAPH_SENTENCE",
        text=text,
        material=True,
        claim_ids=[CLAIM_ID],
        source_keys=["SRC-DOC000047-d5c60204e247"],
        relationship_type="INDEPENDENT",
    )


def _probe(text: str, paragraph: str, bundle=None) -> dict:
    failures = base.stage_e_conditions(_unit(text), paragraph, bundle or validator.load_bundle())
    return {
        "failure_codes": [row.code for row in failures],
        "conditions": [row.evidence for row in failures],
        "status": "REJECT" if failures else "ACCEPT",
    }


def analyse() -> dict:
    bundle = validator.load_bundle()
    paragraph = f"{STATEMENT} {CASE_SCOPE}"
    paragraph_scoped = deepcopy(bundle)
    paragraph_scoped.allowlist[CLAIM_ID]["canonical_claim"] = (
        "Specific rock conditions, such as crushed or squeezing rock, may require 12 inches (300 mm) and more."
    )
    return {
        "version": "tunnelbook-v2.2-retry-case-scope-condition-probes-v1",
        "validator_version": validator.VALIDATOR_VERSION,
        "preserved_allocation": _probe(CASE_SCOPE, paragraph),
        "statement_control": _probe(STATEMENT, STATEMENT, bundle),
        "different_paragraph_control": _probe(CASE_SCOPE, CASE_SCOPE, bundle),
        "unit_condition_realized_control": _probe(f"Belirli {CASE_SCOPE}", f"{STATEMENT} Belirli {CASE_SCOPE}", bundle),
        "paragraph_scope_counterfactual": _probe(CASE_SCOPE, paragraph, paragraph_scoped),
        "counts": {
            "generation": 0,
            "rendering": 0,
            "retrieval": 0,
            "qdrant_writes": 0,
            "corpus_wide_reads": 0,
        },
    }


if __name__ == "__main__":
    print(json.dumps(analyse(), ensure_ascii=False, sort_keys=True, indent=2))
