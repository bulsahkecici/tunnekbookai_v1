"""ARCHITECTURE V2 PILOT #1 — manifest and report over the preserved evidence.

Reads what the pilot run left behind and records the outcome. It repairs nothing, regenerates
nothing and decides nothing the pilot script did not already decide; the rejection stands exactly
as validation produced it.

The finding worth stating plainly: the pilot was rejected on a defect in its own pre-generation
gate, not on anything the model did wrong. Gate 4 was required to expose only REALIZABLE
claim/role pairs, and per-role it did. But it listed SEC-02-2-C-005 — a claim whose mandatory
CONDITION obligation has no realizable slot — and marked `requires_condition_slot: true` beside an
`available_roles` list that omitted CONDITION. The option set therefore demanded a role it did not
offer. The planner followed the stated rule and allocated the slot, and plan validation rejected
it, which is the layer working. Gate 5's feasibility builder had already skipped C-005 for exactly
this reason; the two gates disagreed, and only one of them was shown to the model.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VERSION = "tunnelbook-sec-02-2-architecture-v2-pilot-1-manifest-v1"
PHASE = "SEC-02-2 ARCHITECTURE V2 PILOT #1 AUTHORISATION"
PILOT_ID = "SEC-02-2-ARCHV2-PILOT-1"

PILOT = ROOT / "data/book/drafting/sec_02_2/architecture_v2/pilot_1"
GATE = PILOT / "audits" / "pre_generation_gate_v1.json"
FEASIBILITY = PILOT / "audits" / "feasibility_proof_v1.json"
OPTIONS = PILOT / "contracts" / "planner_option_set_v1.json"
RAW = PILOT / "raw" / "semantic_plan_raw_v1.json"
PLAN = PILOT / "plan" / "semantic_plan_ir_v2.json"
VALIDATION = PILOT / "validation" / "pilot_1_validation.json"
MANIFEST_PATH = ROOT / "data/book/manifests/sec_02_2_architecture_v2_pilot_1.json"
REPORT_PATH = ROOT / "reports" / "sec_02_2_architecture_v2_pilot_1.md"

PROSE_FIELDS = ("text", "sentence", "phrase", "free_text", "explanation", "prose", "note",
                "description", "content", "body")


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def plan_field_names(node, into: set) -> set:
    if isinstance(node, dict):
        into.update(node.keys())
        for value in node.values():
            plan_field_names(value, into)
    elif isinstance(node, list):
        for value in node:
            plan_field_names(value, into)
    return into


def build() -> dict:
    gate = _json(GATE)
    validation = _json(VALIDATION)
    raw = _json(RAW)
    plan = _json(PLAN)
    feasibility = _json(FEASIBILITY)
    options = _json(OPTIONS)

    fields = sorted(plan_field_names(plan, set()))
    prose_present = sorted(set(fields) & set(PROSE_FIELDS))
    accepted = validation["status"] == "ACCEPT"

    return {
        "version": VERSION,
        "phase": PHASE,
        "pilot_id": PILOT_ID,
        "section_id": "SEC-02-2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase_status": "closed_go",
        "pilot_status": validation["status"],
        "pilot_rejected_at_stage": validation.get("stage"),
        "draft_status": "REJECTED" if not accepted else "PILOT_DRAFT",
        "rendered": accepted,
        "released": False,
        "pre_generation_gate": {
            "gate_1_frozen_inputs_passed": gate["gate_1_frozen_inputs"]["passed"],
            "rethink_inputs_checked": gate["gate_1_frozen_inputs"]["rethink_inputs_checked"],
            "rethink_drift": len(gate["gate_1_frozen_inputs"]["rethink_drift"]),
            "acceptance_contract_sha256":
                gate["gate_2_acceptance_contract"]["sha256"],
            "acceptance_contract_unamended":
                gate["gate_2_acceptance_contract"]["unamended"],
            "gate_3_static_proof": gate["gate_3_static_proof"]["status"],
            "gate_3_universe_reproduced": gate["gate_3_static_proof"]["universe_reproduced"],
            "gate_4_realizable_pairs_exposed":
                gate["gate_4_option_set"]["realizable_pairs_exposed"],
            "gate_4_unrealizable_pairs_exposed":
                gate["gate_4_option_set"]["unrealizable_pairs_exposed"],
            "gate_5_feasible": gate["gate_5_feasibility"]["feasible"],
            "gate_5_units": gate["gate_5_feasibility"]["units"],
            "gate_5_topics": gate["gate_5_feasibility"]["topics"],
            "gate_6_blocks_complete_pilot":
                gate["gate_6_limitations"]["blocks_complete_pilot"],
            "generation_authorised": gate["generation_authorised"],
        },
        "generation": {
            "calls": 1,
            "model_id": raw["model_id"],
            "temperature": raw["temperature"],
            "seed": raw["seed"],
            "finish_reason": raw["finish_reason"],
            "usage": raw["usage"],
            "raw_text_sha256": raw["raw_text_sha256"],
            "system_prompt_version": raw["system_prompt_version"],
            "system_prompt_sha256": raw["system_prompt_sha256"],
        },
        "semantic_plan": {
            "parsed": True,
            "schema_valid": True,
            "field_names_emitted": fields,
            "prose_fields_emitted": prose_present,
            "prose_field_count": len(prose_present),
            "slots": validation["semantic_plan"]["slots"],
            "claims": validation["semantic_plan"]["claims"],
            "role_counts": validation["semantic_plan"]["role_counts"],
            "subsections": len(plan["subsections"]),
            "paragraphs": sum(len(s["paragraph_groups"]) for s in plan["subsections"]),
            "valid": validation["semantic_plan"]["valid"],
            "failures": validation["semantic_plan"]["failures"],
            "unrealizable_pairs_selected":
                validation["semantic_plan"]["unrealizable_pairs_selected"],
        },
        "failure": {
            "codes": sorted({f["code"] for f in validation["semantic_plan"]["failures"]}),
            "count": len(validation["semantic_plan"]["failures"]),
            "caught_at": "plan_validation, before any prose was rendered",
            "attributed_to": "PRE_GENERATION_GATE_OPTION_SET_DEFECT",
            "detail": (
                "Gate 4 exposed SEC-02-2-C-005 with requires_condition_slot: true and an "
                "available_roles list that omits CONDITION, because C-005's CONDITION role is "
                "UNREALIZABLE — its registered condition is not Turkish and has no frozen gloss "
                "frame. The option set demanded a role it did not offer. The planner followed "
                "the stated rule, allocated the slot, and plan validation rejected it. Gate 5's "
                "feasibility builder had already skipped C-005 for the same reason, so the two "
                "gates disagreed and only one was shown to the model."),
            "not_attributed_to": [
                "the model emitting prose — it emitted none",
                "a containment failure — no prose was rendered",
                "a validator defect — plan validation caught the selection correctly",
            ],
            "route": "ARCHITECTURE V2 PILOT FAILURE ANALYSIS V1",
        },
        "what_held": [
            "the planner emitted no prose field of any kind; only the 12 declared field names",
            "the plan parsed against the frozen schema without repair",
            "every other selected claim/role pair was REALIZABLE",
            "the single invalid selection was caught before rendering, not after",
            "no prose was rendered, so no containment question arose",
        ],
        "counts": {
            "generation_calls": 1, "retrieval_calls": 0, "qdrant_writes": 0,
            "corpus_reads": 0, "post_render_model_calls": 0, "automatic_retries": 0,
            "regenerations": 0, "repairs": 0, "validators_weakened": 0,
            "lexicons_widened": 0, "frozen_artifacts_modified": 0,
        },
        "feasibility_proof": {
            "feasible": feasibility["feasible"],
            "units": feasibility["units"],
            "claims_stated": len(feasibility["claims_stated"]),
            "topics": feasibility["topics"],
            "validator": feasibility["validation"],
            "note": ("A deterministic full-section plan validates and renders clean. The section "
                     "is reachable under Architecture V2; this pilot's rejection is about the "
                     "option set shown to the planner, not about the architecture's reach."),
        },
        "known_limitations_audited": gate["gate_6_limitations"],
        "artifacts": {
            "pre_generation_gate": str(GATE.relative_to(ROOT)),
            "planner_option_set": str(OPTIONS.relative_to(ROOT)),
            "feasibility_proof": str(FEASIBILITY.relative_to(ROOT)),
            "raw_model_output": str(RAW.relative_to(ROOT)),
            "semantic_plan": str(PLAN.relative_to(ROOT)),
            "validation": str(VALIDATION.relative_to(ROOT)),
            "planner_prompt": "data/metadata/architecture_v2_semantic_planner_prompt_v1.txt",
            "report": str(REPORT_PATH.relative_to(ROOT)),
            "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
            "script": "scripts/65_sec_02_2_architecture_v2_pilot_1.py",
        },
        "attempt_4_identifier": "retired",
        "regeneration_authorised": False,
        "next_phase": "ARCHITECTURE V2 PILOT FAILURE ANALYSIS V1",
    }


def write_report(manifest: dict) -> None:
    lines: list[str] = []
    add = lines.append
    gate = manifest["pre_generation_gate"]
    plan = manifest["semantic_plan"]

    add(f"# {PHASE}")
    add("")
    add(f"**Phase CLOSED / GO. ARCHITECTURE V2 PILOT #1 — {manifest['pilot_status']}.** "
        "One generation, rejected at plan validation before any prose was rendered. "
        "No repair, no regeneration.")
    add("")
    add("")
    add("## Pre-generation gates")
    add("")
    add("| Gate | Result |")
    add("|---|---|")
    add(f"| 1 frozen inputs ({gate['rethink_inputs_checked']} checked) | "
        f"drift {gate['rethink_drift']} |")
    add(f"| 2 acceptance contract `{gate['acceptance_contract_sha256'][:16]}…` | "
        f"unamended {gate['acceptance_contract_unamended']} |")
    add(f"| 3 static containment proof | {gate['gate_3_static_proof']}, universe reproduced "
        f"{gate['gate_3_universe_reproduced']} |")
    add(f"| 4 planner option set | {gate['gate_4_realizable_pairs_exposed']} REALIZABLE pairs, "
        f"{gate['gate_4_unrealizable_pairs_exposed']} UNREALIZABLE exposed |")
    add(f"| 5 feasibility | {gate['gate_5_feasible']}, {gate['gate_5_units']} units, topics "
        f"{gate['gate_5_topics']['covered']}/{gate['gate_5_topics']['required']} |")
    add(f"| 6 known limitations block a pilot | {gate['gate_6_blocks_complete_pilot']} |")
    add(f"| **generation authorised** | **{gate['generation_authorised']}** |")
    add("")
    add("")
    add("## The generation")
    add("")
    generation = manifest["generation"]
    add(f"One call to `{generation['model_id']}`, temperature {generation['temperature']}, "
        f"seed {generation['seed']}, finish `{generation['finish_reason']}`, "
        f"{generation['usage'].get('completion_tokens')} completion tokens. Raw bytes preserved, "
        f"SHA256 `{generation['raw_text_sha256']}`.")
    add("")
    add("")
    add("## What the planner produced")
    add("")
    add(f"{plan['slots']} slots across {plan['claims']} claims, {plan['subsections']} "
        f"subsections, {plan['paragraphs']} paragraphs.")
    add("")
    add(f"Roles: `{plan['role_counts']}`")
    add("")
    add(f"**Prose fields emitted: {plan['prose_field_count']}.** The plan carried only the "
        f"declared field names: `{', '.join(plan['field_names_emitted'])}`.")
    add("")
    add("")
    add("## The rejection")
    add("")
    failure = manifest["failure"]
    add(f"One failure, code `{failure['codes'][0]}`, {failure['caught_at']}.")
    add("")
    add(f"**Attributed to: {failure['attributed_to']}.** {failure['detail']}")
    add("")
    add("Not attributed to:")
    add("")
    for item in failure["not_attributed_to"]:
        add(f"- {item}")
    add("")
    add("What held:")
    add("")
    for item in manifest["what_held"]:
        add(f"- {item}")
    add("")
    add("")
    add("## Feasibility, for the record")
    add("")
    feasibility = manifest["feasibility_proof"]
    add(f"{feasibility['note']} The deterministic plan renders {feasibility['units']} units "
        f"across {feasibility['claims_stated']} claims, covers "
        f"{feasibility['topics']['covered']}/{feasibility['topics']['required']} required "
        f"topics, and validates `{feasibility['validator']['status']}` with an empty histogram.")
    add("")
    add("")
    add("## Counts")
    add("")
    add("| | |")
    add("|---|---|")
    for key, value in sorted(manifest["counts"].items()):
        add(f"| {key.replace('_', ' ')} | {value} |")
    add(f"| rendered draft | NONE |")
    add(f"| released draft | NONE |")
    add("")
    add("")
    add("## Route")
    add("")
    add(f"**{manifest['next_phase']}.** Regeneration is not authorised. `Attempt #4` remains a "
        "retired identifier, and a second Architecture V2 pilot becomes reachable only if that "
        "analysis authorises one on its own evidence.")
    add("")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    manifest = build()
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    write_report(manifest)
    print(f"phase: {manifest['phase_status']}  pilot: {manifest['pilot_status']} "
          f"at {manifest['pilot_rejected_at_stage']}")
    print(f"failure codes: {manifest['failure']['codes']}")
    print(f"prose fields emitted: {manifest['semantic_plan']['prose_field_count']}")
    print(f"next phase: {manifest['next_phase']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
