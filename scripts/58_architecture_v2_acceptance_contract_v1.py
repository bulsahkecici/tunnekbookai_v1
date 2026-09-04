"""Architecture V2 Acceptance Contract v1 — the thresholds, authored before the implementation.

This script exists to be run first, before M1 through M5 are written, so that the conditions the
phase is judged against cannot be adjusted once the results are known. It records nothing about
the implementation because at authoring time there is no implementation to record.

The contract is frozen by SHA. Any later phase that wants different thresholds must supersede it
with a new versioned contract and say why; editing this one in place is the failure mode it is
built to prevent.

Two acceptance conditions deserve their rationale stated here rather than in a field.

**Zero, not low.** Every rejection-code budget is exactly zero over the declared universe. A
budget of "few" would make architecture V2 a better version of architecture A — the thing whose
measured composed-mode rate of 0.0759 the rethink phase rejected as an architecture. The claim
being tested is a construction property, and a construction property admits no counterexamples.

**Capability, not behaviour.** The universe is every plan the contract permits, not a sample of
plans someone chose to write. `every_constructible_output_is_valid` is the condition that
separates this from "the validator usually accepts what we rendered", and it is the reason M5
enumerates rather than tests.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

VERSION = "tunnelbook-architecture-v2-acceptance-contract-v1"
PHASE = "SEC-02-2 DRAFTING ARCHITECTURE V2 IMPLEMENTATION"
SECTION_ID = "SEC-02-2"

CONTRACT_PATH = (ROOT / "data" / "book" / "drafting" / "sec_02_2" / "architecture_v2"
                 / "contracts" / "architecture_v2_acceptance_contract_v1.json")
MANIFEST_PATH = (ROOT / "data" / "book" / "manifests"
                 / "architecture_v2_acceptance_contract_v1.json")

ZERO_TOLERANCE_CODES = (
    "UNSUPPORTED_PROPOSITION",
    "CLAIM_EXPANSION",
    "NUMERIC_DRIFT",
    "UNIT_DRIFT",
    "MODALITY_DRIFT",
    "CONDITION_DROPPED",
    "QUALIFIER_DROPPED",
    "SEMANTIC_SCOPE_MISMATCH",
    "LANGUAGE_MISMATCH",
    "CLAIM_DENYLISTED",
    "UNKNOWN_CITATION",
)


def build_contract() -> dict:
    return {
        "version": VERSION,
        "phase": PHASE,
        "section_id": SECTION_ID,
        "authored_at": datetime.now(timezone.utc).isoformat(),
        "authored_before_implementation": True,
        "amendment_policy": (
            "Frozen on authoring. Thresholds may not be changed after observing implementation "
            "results. A later phase may supersede this contract with a new version and a stated "
            "reason; it may not edit this one."),
        "acceptance_conditions": {
            "AC-01_preflight_frozen_drift": {
                "requirement": "all 15 rethink-v1 frozen inputs re-hash identically",
                "threshold": 0,
                "unit": "drifted inputs",
            },
            "AC-02_plan_ir_has_no_prose_field": {
                "requirement": ("SemanticPlanIRV2 declares no field whose name or role admits "
                                "free text; a plan carrying one is rejected at parse"),
                "forbidden_field_names": ["free_text", "text", "prose", "sentence", "phrase",
                                          "wording", "draft", "content", "body", "narrative"],
                "threshold": 0,
                "unit": "prose-bearing fields",
            },
            "AC-03_plan_validation_fails_closed": {
                "requirement": ("an unknown realization role, claim, source key, numeric, "
                                "condition, qualifier or relation is rejected before rendering"),
                "threshold": 0,
                "unit": "invalid plans reaching the renderer",
            },
            "AC-04_realization_data_is_frozen": {
                "requirement": ("every factual lexical element the renderer can emit traces to "
                                "frozen approved claim data, the frozen V2 grammatical scaffold, "
                                "or deterministic morphology over a frozen stem"),
                "threshold": 0,
                "unit": "renderer lexical outputs not owned by a contract",
            },
            "AC-05_morphology_is_deterministic": {
                "requirement": "every morphological transformation is a pure function",
                "threshold": 0,
                "unit": "non-deterministic transformations",
            },
            "AC-06_renderer_is_pure": {
                "requirement": ("same input bytes produce same output bytes across repeated "
                                "runs and across process boundaries; no model call, retrieval, "
                                "network, clock or randomness"),
                "threshold": 0,
                "unit": "byte differences across repeated renders",
            },
            "AC-07_static_containment_proof": {
                "requirement": ("every (claim × role × condition form × qualifier form × numeric "
                                "form) the contract permits is rendered and validated by the "
                                "unchanged Draft Validator v1.2"),
                "zero_tolerance_codes": list(ZERO_TOLERANCE_CODES),
                "threshold": 0,
                "unit": "failures of any listed code over the declared universe",
            },
            "AC-08_no_false_accepts_or_rejects": {
                "requirement": ("negative fixtures reject before prose is released; positive "
                                "fixtures are not rejected"),
                "false_accepts_threshold": 0,
                "false_rejects_threshold": 0,
            },
            "AC-09_construction_invariant": {
                "requirement": ("the property tested is capability, not behaviour: every output "
                                "the renderer is capable of constructing within the declared "
                                "contract universe is valid. A plan the contract permits and the "
                                "renderer refuses is a contract defect, not a pass."),
                "threshold": 0,
                "unit": "constructible outputs that fail validation",
            },
            "AC-10_unrealizable_is_explicit": {
                "requirement": ("a claim/role pair that cannot be built from approved semantics "
                                "is marked UNREALIZABLE and refused by the renderer; it is never "
                                "filled from model knowledge or silently skipped"),
                "threshold": 0,
                "unit": "UNREALIZABLE pairs the renderer nonetheless renders",
            },
            "AC-11_frozen_integrity": {
                "requirement": ("Draft Validator v1, v1.1, v1.2, the language validator, the "
                                "Section Drafting Contract v1, the Book Citation Rendering "
                                "Contract v1, the function lexicon, the paraphrase lexicon, the "
                                "translation glosses, all draft plans and all preserved attempts "
                                "are byte-identical"),
                "threshold": 0,
                "unit": "modified frozen artifacts",
            },
            "AC-12_no_generation_in_this_phase": {
                "requirement": "no model call, no retrieval, no Qdrant write, no corpus read",
                "generation_calls": 0,
                "retrieval_calls": 0,
                "qdrant_writes": 0,
                "corpus_reads": 0,
                "rendered_pilot": "NONE",
            },
            "AC-13_no_style_layer": {
                "requirement": ("no LLM rewrite, paraphrase or style pass runs after deterministic "
                                "rendering. Such a layer would reinstate architecture A behind "
                                "the safety boundary."),
                "threshold": 0,
                "unit": "post-render model passes",
            },
            "AC-14_historical_regression": {
                "requirement": ("targeted suites for the drafting contract, citation renderer, "
                                "validators v1/v1.1/v1.2, language validator, composition "
                                "validator, qualifier semantics, remediation, analysis v2, "
                                "attempt #3 plan and rethink v1 all pass"),
                "threshold": 0,
                "unit": "test failures",
            },
        },
        "numeric_safety_invariants": [
            "15 cm remains 15 cm; no derived 150 mm is presented as source-stated for that claim",
            "a source-stated 100-150 mm elsewhere remains permitted",
            "C25/30 remains C25/30 and is never converted to an inferred MPa figure",
            "360 / 350 / 400 scope rules are unchanged",
            "a numeric the declaring claim does not register is rejected",
        ],
        "relationship_invariants": [
            ("the renderer never introduces a relation between adjacent slots. Connectives such "
             "as bu nedenle, dolayısıyla, bunun sonucunda, sayesinde, böylece, ancak and buna "
             "karşın are emitted only under an explicit frozen relation constraint."),
            "adjacent independent claims remain independent",
        ],
        "citation_invariants": [
            "stable source_keys only",
            "packet-local [E###] handles are never rendered",
            "Book Citation Rendering Contract v1 is unchanged",
        ],
        "closed_role_enumeration": [
            "CLAIM_STATEMENT", "REQUIREMENT", "IDENTITY_SCOPE", "QUALIFIER_SCOPE",
            "CONDITION", "EXEMPLIFICATION", "NUMERIC_CRITERIA",
        ],
        "forbidden_role_names": ["FREEFORM", "OTHER", "GENERIC", "CUSTOM"],
        "go_condition": ("CLOSED / GO requires every acceptance condition above to hold. A single "
                         "failure is NO-GO, and is remediated in a later versioned phase rather "
                         "than by amending this contract."),
        "does_not_authorise": [
            "ARCHITECTURE V2 PILOT #1",
            "any semantic plan generated by a model",
            "any prose generated by a model",
            "rendering or release of a pilot section",
            "human technical review",
        ],
    }


def main() -> int:
    if CONTRACT_PATH.exists():
        print(f"REFUSED: {CONTRACT_PATH.relative_to(ROOT)} already exists and is frozen.")
        print("Amending a frozen acceptance contract is the failure mode this script prevents.")
        return 1
    contract = build_contract()
    CONTRACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT_PATH.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    sha = hashlib.sha256(CONTRACT_PATH.read_bytes()).hexdigest()
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps({
        "version": VERSION,
        "phase": PHASE,
        "section_id": SECTION_ID,
        "frozen_at": contract["authored_at"],
        "authored_before_implementation": True,
        "contract_path": str(CONTRACT_PATH.relative_to(ROOT)),
        "contract_sha256": sha,
        "acceptance_conditions": sorted(contract["acceptance_conditions"]),
        "zero_tolerance_codes": list(ZERO_TOLERANCE_CODES),
        "amendment_policy": contract["amendment_policy"],
    }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"acceptance contract frozen: {CONTRACT_PATH.relative_to(ROOT)}")
    print(f"sha256: {sha}")
    print(f"conditions: {len(contract['acceptance_conditions'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
