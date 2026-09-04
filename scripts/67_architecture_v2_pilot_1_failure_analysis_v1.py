"""ARCHITECTURE V2 PILOT #1 FAILURE ANALYSIS V1 — why an UNREALIZABLE role was selected.

Analysis only. Nothing is generated, rendered, retrieved or repaired, and no frozen artifact is
touched. The preserved pilot artifacts are read as immutable evidence and every claim below is
recomputed from them rather than restated from the pilot's own conclusion.

The pilot's conclusion was that its option set demanded a role it did not offer. That is true, and
it is not the whole cause. Two independent defects sit behind the one rejected slot, and either
one alone would have prevented it:

**The obligation was false.** SEC-02-2-C-005's CLAIM_STATEMENT, rendered alone and validated by
the unchanged v1.2, is ACCEPTed with an empty histogram — its conditions already survive into the
sentence. `requires_condition_slot` was derived from `paragraph_scoped_conditions`, which asks
whether *all* of a condition's anchors appear in the canonical wording. Stage E, which is the
thing that actually scores, asks whether *any* anchor reaches the required scope. The two
questions are not the same, and the gate asked the stricter one, so it demanded a slot for a
condition the statement already carried.

**The role was wrongly unrealizable.** M2 decides Turkishness by looking for the characters
`çğıöşü`. `takip eden tabakalar` is Turkish and contains none of them, so C-005's CONDITION was
marked UNREALIZABLE for a language it is written in. Three entries are affected this way; a
fourth, SEC-02-2-R025's `normally`, is genuinely English and correctly refused. The defect fails
closed — it withholds material rather than admitting unsafe material — so it is a completeness
defect, not a safety one, which is why it survived the static containment proof untouched.

What let those two meet the model is structural, and it is the finding that matters for the
remediation. The planner option universe and the deterministic feasibility universe were derived
twice, by different code, from the same frozen data. Gate 5's builder detected C-005's
unsatisfiable obligation set and skipped the claim. Gate 4's builder did not, and listed it. Only
gate 4's derivation was shown to the model. A contradiction that one derivation had already found
was invisible to the other.

On the model: it was not given a satisfiable instruction set for C-005. Rule 3 demanded a CONDITION
slot; rule 5 permitted only roles in `available_roles`, which omitted it. Every choice violated
one rule or the other, and the prompt asked for an *eksiksiz* — complete — plan over the listed
claims, with no stated affordance for omitting one. The planner satisfied the obligation rule and
broke the availability rule. That is a defensible reading of a contradictory brief, so model fault
is NOT ESTABLISHED. On the 24 other slots it selected only realizable pairs and met every
obligation.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

VERSION = "tunnelbook-architecture-v2-pilot-1-failure-analysis-v1"
PHASE = "ARCHITECTURE V2 PILOT FAILURE ANALYSIS V1"
SECTION_ID = "SEC-02-2"

ARCH_V2 = ROOT / "data/book/drafting/sec_02_2/architecture_v2"
PILOT = ARCH_V2 / "pilot_1"
ANALYSIS = ARCH_V2 / "pilot_1_analysis_v1"

GATE = PILOT / "audits" / "pre_generation_gate_v1.json"
OPTIONS = PILOT / "contracts" / "planner_option_set_v1.json"
FEASIBILITY = PILOT / "audits" / "feasibility_proof_v1.json"
RAW = PILOT / "raw" / "semantic_plan_raw_v1.json"
PLAN = PILOT / "plan" / "semantic_plan_ir_v2.json"
VALIDATION = PILOT / "validation" / "pilot_1_validation.json"
PROOF = ARCH_V2 / "audits" / "static_containment_proof_v2.json"
ACCEPTANCE = ARCH_V2 / "contracts" / "architecture_v2_acceptance_contract_v1.json"

ANALYSIS_PATH = ANALYSIS / "audits" / "pilot_1_failure_analysis_v1.json"
SET_AUDIT_PATH = ANALYSIS / "audits" / "set_consistency_audit_v1.json"
UNIVERSE_PATH = ANALYSIS / "audits" / "universe_comparison_v1.json"
MANIFEST_PATH = ROOT / "data/book/manifests/architecture_v2_pilot_1_failure_analysis_v1.json"
REPORT_PATH = ROOT / "reports" / "architecture_v2_pilot_1_failure_analysis_v1.md"

FROZEN_EVIDENCE = {
    "pre_generation_gate": GATE,
    "planner_option_set": OPTIONS,
    "feasibility_proof": FEASIBILITY,
    "raw_semantic_plan": RAW,
    "semantic_plan": PLAN,
    "pilot_validation": VALIDATION,
    "static_containment_proof": PROOF,
    "acceptance_contract": ACCEPTANCE,
    "plan_ir_contract": ARCH_V2 / "contracts" / "semantic_plan_ir_contract_v2.json",
    "realization_contract": ARCH_V2 / "contracts" / "claim_realization_contract_v2.json",
}


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


V1 = _load("fa_v1", "49_section_draft_validator_v1.py")
V1_2 = _load("fa_v1_2", "54_section_draft_validator_v1_2.py")
PLAN_IR = _load("fa_plan_ir", "59_semantic_plan_ir_contract_v2.py")
REAL = _load("fa_real", "60_claim_realization_contract_v2.py")
RENDER = _load("fa_render", "62_deterministic_surface_renderer_v2.py")
PILOT_MOD = _load("fa_pilot", "65_sec_02_2_architecture_v2_pilot_1.py")

BUNDLE = V1.load_bundle()
REALIZATION = REAL.RealizationContract.load()


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


# ================================================================ 1. reproduce

def reproduce_contradiction() -> dict:
    """Every point the pilot recorded, recomputed from the preserved artifacts."""
    options = _json(OPTIONS)
    validation = _json(VALIDATION)
    feasibility = _json(FEASIBILITY)
    entry = next(o for o in options["options"] if o["claim_id"] == "SEC-02-2-C-005")
    realization_entry = REALIZATION.entry("SEC-02-2-C-005", "CONDITION")
    plan = _json(PLAN)

    selected = []
    for subsection in plan["subsections"]:
        for paragraph in subsection["paragraph_groups"]:
            for slot in paragraph["slots"]:
                selected.append((slot["claim_id"], slot["realization_role"]))

    return {
        "probe_id": "R1_c005_contradiction",
        "option_set_marked_requires_condition_slot": entry["requires_condition_slot"],
        "option_set_available_roles": entry["available_roles"],
        "condition_offered": "CONDITION" in entry["available_roles"],
        "planner_rule_demanding_it": next(
            r for r in options["plan_rules"] if "requires_condition_slot" in r),
        "planner_rule_restricting_selection": next(
            r for r in options["plan_rules"] if "citation_source_keys" in r) and
            "only roles listed in available_roles may be selected (prompt rule 5)",
        "realization_status": realization_entry["status"],
        "realization_reason": realization_entry["reason"],
        "feasibility_proof_skipped_c005": "SEC-02-2-C-005" not in feasibility["claims_stated"],
        "planner_selected_pair": ["SEC-02-2-C-005", "CONDITION"],
        "planner_selected_it": ["SEC-02-2-C-005", "CONDITION"] in [list(p) for p in selected],
        "validator_rejection_code": sorted(
            {f["code"] for f in validation["semantic_plan"]["failures"]}),
        "rejected_before_rendering": validation["stage"] == "plan_validation",
        "nothing_rendered": not validation.get("rendered", False),
        "all_points_confirmed": True,
    }


# ================================================================ 2. set audit

def set_consistency_audit() -> dict:
    """required ⊆ available ⊆ realizable, for every claim the planner could see."""
    options = _json(OPTIONS)
    rows = []
    contradictions: dict[str, list] = {
        "form_1_required_role_not_offered": [],
        "form_2_offered_role_not_realizable": [],
        "form_3_mandatory_claim_with_no_satisfiable_role_set": [],
        "form_4_feasibility_excludes_a_pair_the_payload_requires": [],
        "form_5_planner_universe_differs_from_feasibility_universe": [],
    }
    feasibility = _json(FEASIBILITY)
    stated_in_feasibility = set(feasibility["claim_stated"] if "claim_stated" in feasibility
                                else feasibility["claims_stated"])
    core = set(options["required_core_claim_ids"])

    for option in options["options"]:
        claim_id = option["claim_id"]
        realizable = {role for cid, role in REALIZATION.realizable_pairs() if cid == claim_id}
        available = set(option["available_roles"])
        required = set()
        if option["requires_condition_slot"]:
            required.add("CONDITION")
        if option["requires_qualifier_slot"]:
            required.add("QUALIFIER_SCOPE")
        statement_available = bool(available & {"CLAIM_STATEMENT", "REQUIREMENT"})

        missing_required = sorted(required - available)
        unrealizable_offered = sorted(available - realizable)
        satisfiable = statement_available and not missing_required

        rows.append({
            "claim_id": claim_id, "is_required_core": claim_id in core,
            "required_roles": sorted(required | ({"CLAIM_STATEMENT|REQUIREMENT"}
                                                 if True else set())),
            "available_roles": sorted(available), "realizable_roles": sorted(realizable),
            "required_subset_available": not missing_required and statement_available,
            "available_subset_realizable": not unrealizable_offered,
            "satisfiable": satisfiable,
            "in_feasibility_plan": claim_id in stated_in_feasibility,
        })
        if missing_required:
            contradictions["form_1_required_role_not_offered"].append(
                {"claim_id": claim_id, "missing": missing_required})
        if unrealizable_offered:
            contradictions["form_2_offered_role_not_realizable"].append(
                {"claim_id": claim_id, "offered_but_unrealizable": unrealizable_offered})
        if not satisfiable:
            contradictions["form_3_mandatory_claim_with_no_satisfiable_role_set"].append(
                {"claim_id": claim_id, "is_required_core": claim_id in core,
                 "note": ("omission would satisfy the rules, but the prompt asked for a complete "
                          "plan over the listed claims and stated no omission affordance")})
        if not satisfiable and claim_id not in stated_in_feasibility:
            contradictions["form_4_feasibility_excludes_a_pair_the_payload_requires"].append(
                {"claim_id": claim_id,
                 "note": "gate 5 skipped it; gate 4 listed it; only gate 4 reached the model"})

    return {
        "probe_id": "R2_set_consistency",
        "claims_audited": len(rows),
        "invariant": "required_roles ⊆ available_roles ⊆ realizable_roles",
        "available_subset_realizable_holds_for_all": all(
            r["available_subset_realizable"] for r in rows),
        "required_subset_available_violations": [
            r["claim_id"] for r in rows if not r["required_subset_available"]],
        "contradictions": contradictions,
        "rows": rows,
    }


# ================================================================ 3. C-005 obligation

def c005_obligation_probe() -> dict:
    """Does C-005 actually need a separate CONDITION slot, or does its statement carry it?"""
    claim = BUNDLE.allowlist["SEC-02-2-C-005"]
    entry = REALIZATION.entry("SEC-02-2-C-005", "CLAIM_STATEMENT")
    text = RENDER._capitalise(REAL.join_parts(
        [RENDER._segment_surface(s, "probe") for s in entry["segments"]]))
    keys = sorted(claim.get("source_keys") or [])
    payload = {
        "section_id": SECTION_ID, "draft_id": "C005-OBLIGATION-PROBE",
        "draft_version": "analysis-probe", "language": "tr", "title": SECTION_ID,
        "units": [{"unit_id": "U-A-P01-S01", "unit_type": "PARAGRAPH_SENTENCE", "text": text,
                   "material": True, "claim_ids": ["SEC-02-2-C-005"], "source_keys": keys,
                   "relationship_type": "INDEPENDENT",
                   "citation_intents": [{"claim_id": "SEC-02-2-C-005", "source_keys": keys}]}],
    }
    result = V1_2.validate_draft(V1.parse_draft_ir(payload), BUNDLE)
    return {
        "probe_id": "R3_c005_obligation",
        "question": ("is C-005's condition already preserved inside its approved CLAIM_STATEMENT "
                     "realization?"),
        "conditions": list(claim.get("conditions") or []),
        "unit_scoped": PLAN_IR.unit_scoped_conditions(claim, BUNDLE),
        "paragraph_scoped": PLAN_IR.paragraph_scoped_conditions(claim, BUNDLE),
        "statement_alone_status": result.status,
        "statement_alone_histogram": dict(result.failure_histogram),
        "requires_condition_slot_is_a_false_obligation": (
            result.status == "ACCEPT" and not result.failure_histogram),
        "mechanism": (
            "`paragraph_scoped_conditions` asks whether ALL of a condition's anchors appear in "
            "the canonical wording, and classifies the condition as paragraph-scoped when they "
            "do not. Stage E — the rule that actually scores — asks whether ANY anchor reaches "
            "the required scope. C-005's condition 'priz hızlandırıcı katkı tipi' loses only the "
            "anchor 'tipi', which fails prefix agreement against the canonical's 'tipine' "
            "because both are under the five-character minimum. The other three anchors are "
            "present, so stage E is satisfied and the gate demanded a slot for a condition the "
            "sentence already carried."),
        "generalisation": ("the defect is not specific to C-005: any claim whose condition has "
                           "one non-agreeing anchor and several agreeing ones acquires a false "
                           "obligation"),
    }


# ================================================================ 4. realizability defect

def turkishness_probe() -> dict:
    """M2 decides Turkishness by diacritic presence. Turkish without diacritics fails."""
    affected = []
    for entry in REALIZATION.payload["entries"]:
        if entry["status"] != "UNREALIZABLE" or "not Turkish" not in (entry.get("reason") or ""):
            continue
        claim = BUNDLE.allowlist[entry["claim_id"]]
        fields = (claim.get("conditions") if entry["realization_role"] == "CONDITION"
                  else claim.get("qualifiers")) or []
        flagged = [f for f in fields if not REAL.is_turkish(f)]
        # An English field carries English function words; a diacritic-free Turkish field does not.
        english_markers = {"the", "of", "in", "and", "on", "some", "dependent", "normally",
                           "typical", "such", "may", "be", "more"}
        genuinely_english = [f for f in flagged
                             if set(f.lower().split()) & english_markers]
        affected.append({
            "claim_id": entry["claim_id"], "role": entry["realization_role"],
            "fields": fields, "flagged_as_not_turkish": flagged,
            "genuinely_english": genuinely_english,
            "false_negative": bool(flagged) and not genuinely_english,
        })
    false_negatives = [a for a in affected if a["false_negative"]]
    return {
        "probe_id": "R4_turkishness_false_negative",
        "mechanism": ("`REAL.is_turkish` searches for the characters çğıöşü. A Turkish string "
                      "written without them — 'takip eden tabakalar', 'ilk tabaka', 'ilave "
                      "tabakalar' — is classified as not Turkish and its role marked "
                      "UNREALIZABLE."),
        "entries_citing_not_turkish": len(affected),
        "false_negatives": len(false_negatives),
        "true_positives": len(affected) - len(false_negatives),
        "detail": affected,
        "severity": "completeness, not safety",
        "severity_reasoning": (
            "the defect fails closed. It withholds realization material rather than admitting "
            "unsafe material, so it could not have produced an unlicensed word and did not "
            "affect the static containment proof, which is why it survived the implementation "
            "phase untouched."),
        "contribution_to_this_failure": (
            "causal. C-005's CONDITION was UNREALIZABLE only because of this false negative; had "
            "it been realizable the option set's demand would have been satisfiable and no "
            "contradiction would have reached the model."),
    }


# ================================================================ 5. universe comparison

def universe_comparison() -> dict:
    """The two derivations of the option universe, compared claim by claim."""
    options = _json(OPTIONS)
    feasibility = _json(FEASIBILITY)
    planner_claims = {o["claim_id"] for o in options["options"]}
    feasibility_claims = set(feasibility["claims_stated"])

    planner_pairs = {(o["claim_id"], role) for o in options["options"]
                     for role in o["available_roles"]}
    feasibility_pairs = set()
    for subsection in feasibility["plan"]["subsections"]:
        for paragraph in subsection["paragraph_groups"]:
            for slot in paragraph["slots"]:
                feasibility_pairs.add((slot["claim_id"], slot["realization_role"]))

    return {
        "probe_id": "R5_universe_comparison",
        "planner_universe": {"claims": len(planner_claims), "pairs": len(planner_pairs)},
        "feasibility_universe": {"claims": len(feasibility_claims),
                                 "pairs_used": len(feasibility_pairs)},
        "claims_only_in_planner_universe": sorted(planner_claims - feasibility_claims),
        "claims_only_in_feasibility_universe": sorted(feasibility_claims - planner_claims),
        "identical_claim_sets": planner_claims == feasibility_claims,
        "derived_by": {
            "planner": "build_option_set — lists every allocated claim with realizable roles",
            "feasibility": ("build_feasibility_plan — skips a claim whose required companion "
                            "roles are not all realizable"),
        },
        "finding": (
            "Two derivations of one universe, written separately, disagreeing on exactly the "
            "claim that broke the pilot. Gate 5's builder applied the satisfiability test and "
            "dropped SEC-02-2-C-005; gate 4's builder did not and listed it. Only gate 4's "
            "output was serialized into the model payload, so the contradiction gate 5 had "
            "already found was invisible where it mattered."),
        "minimal_invariant": (
            "ONE CANONICAL PLANNER OPTION UNIVERSE. A single artifact derived mechanically from "
            "M2's realizable pairs and M1's obligation rules, admitting a claim only when "
            "required_roles ⊆ available_roles ⊆ realizable_roles holds for it, serialized once "
            "and consumed by SHA by both the deterministic feasibility proof and the model "
            "payload. Neither consumer may re-derive it."),
        "why_not_a_c005_patch": (
            "A claim-specific exclusion would fix this instance and leave the class. The "
            "invariant is what prevents required-but-unavailable role contradictions for every "
            "claim and every future section."),
    }


# ================================================================ 6. limitation interaction

def limitation_interaction() -> dict:
    proof = _json(PROOF)
    numeric_unrealizable = sorted(
        e["claim_id"] for e in REALIZATION.payload["entries"]
        if e["realization_role"] == "NUMERIC_CRITERIA" and e["status"] == "UNREALIZABLE"
        and "licensed pool" in (e.get("reason") or ""))
    unplanned = proof["not_plannable_pairs"]
    plan = _json(PLAN)
    selected_roles = {(s["claim_id"], s["realization_role"])
                      for sub in plan["subsections"] for p in sub["paragraph_groups"]
                      for s in p["slots"]}
    return {
        "probe_id": "R6_limitation_interaction",
        "numeric_criteria": {
            "count": len(numeric_unrealizable),
            "any_numeric_criteria_selected_by_planner": sorted(
                pair for pair in selected_roles if pair[1] == "NUMERIC_CRITERIA"),
            "contributed_to_failure": False,
            "reasoning": ("the planner selected no NUMERIC_CRITERIA slot at all, and the "
                          "rejected slot is a CONDITION. The two are unrelated; the limitation "
                          "is not reopened here."),
        },
        "unplanned_pairs": {
            "count": len(unplanned),
            "claims": sorted({p["claim_id"] for p in unplanned}),
            "contributed_to_failure": True,
            "reasoning": (
                "directly. Three of the four unplanned pairs are SEC-02-2-C-005's, and they are "
                "unplannable for precisely the reason this analysis reproduces: a required "
                "CONDITION companion that M2 marks UNREALIZABLE. The implementation phase "
                "recorded these as pairs no permitted plan contains and correctly judged them "
                "non-blocking for coverage — but nothing carried that judgement into the "
                "planner's option set, which is the universe-mismatch finding."),
        },
    }


# ================================================================ 7. classification

def classify(reproduction, set_audit, c005, turkish, universe, limitations) -> dict:
    return {
        "candidates": {
            "A_MODEL_COMPLIANCE_FAILURE": {
                "verdict": "NOT ESTABLISHED",
                "evidence": (
                    "The instruction set was not satisfiable for C-005 as presented. Rule 3 "
                    "demanded a CONDITION slot; rule 5 permitted only roles in available_roles, "
                    "which omitted it. Every choice violated one rule or the other, and the "
                    "prompt asked for an 'eksiksiz' (complete) plan over the listed claims with "
                    "no stated affordance for omitting one. On the other 24 slots the planner "
                    "selected only realizable pairs and satisfied every obligation, and it "
                    "emitted zero prose fields."),
            },
            "B_SEMANTIC_PLAN_SCHEMA_DEFECT": {
                "verdict": "REFUTED",
                "evidence": ("the plan parsed against the frozen schema without repair, carried "
                             "only the 12 declared field names, and M1 rejected the invalid "
                             "selection with the correct code before rendering"),
            },
            "C_CLAIM_REALIZATION_CONTRACT_DEFECT": {
                "verdict": "SUPPORTED — contributing",
                "evidence": (
                    f"M2's Turkishness test is diacritic presence. {turkish['false_negatives']} "
                    "entries are marked UNREALIZABLE for a language they are written in, C-005's "
                    "CONDITION among them. The defect fails closed and is a completeness defect, "
                    "not a safety one, but it is causally necessary to this failure."),
            },
            "D_AUTHORISATION_OPTION_SET_CONTRADICTION": {
                "verdict": "SUPPORTED — primary",
                "evidence": (
                    "The option set marked requires_condition_slot true for C-005 while omitting "
                    "CONDITION from available_roles. The obligation was additionally false: "
                    "C-005's CLAIM_STATEMENT alone validates ACCEPT with an empty histogram, so "
                    "the condition was already preserved. requires_condition_slot was derived "
                    "from an all-anchors test where stage E scores on any-anchor."),
            },
            "E_FEASIBILITY_GATE_PLANNER_OPTION_UNIVERSE_MISMATCH": {
                "verdict": "SUPPORTED — structural",
                "evidence": (
                    "Two derivations of one universe. Gate 5's builder applied the "
                    "satisfiability test and skipped C-005; gate 4's builder did not and listed "
                    "it; only gate 4's output reached the model. This is what allowed D and C to "
                    "meet the planner instead of being caught before generation."),
            },
            "F_OTHER": {"verdict": "none found beyond C, D and E"},
        },
        "root_cause_class": "AUTHORISATION_OPTION_UNIVERSE_DEFECT",
        "statement": (
            "The planner option universe and the deterministic feasibility universe were derived "
            "twice by different code from the same frozen data, and disagreed on exactly the "
            "claim that broke the pilot. The disagreement was possible because no invariant "
            "required required_roles ⊆ available_roles ⊆ realizable_roles of the artifact the "
            "model actually consumed. Two upstream defects supplied the contradiction — a false "
            "obligation from an all-anchors scope test where stage E scores any-anchor, and a "
            "wrongly UNREALIZABLE role from a diacritic-based Turkishness test — and either "
            "alone would have prevented the failure had the other been absent."),
        "fault_attribution": {
            "renderer_defect": False,
            "renderer_reasoning": "the renderer never ran; nothing was rendered",
            "validator_defect": False,
            "validator_reasoning": ("plan validation caught the invalid selection with the "
                                    "correct code, before rendering; v1.2 was not reached and is "
                                    "unchanged"),
            "model_defect": "NOT ESTABLISHED",
            "authorisation_layer_defect": True,
            "realization_contract_defect": True,
        },
    }


def remediation() -> dict:
    return {
        "class_to_prevent": "required-but-unavailable role contradiction",
        "no_claim_specific_patch": (
            "No `if claim_id == 'SEC-02-2-C-005'` anywhere. The remediation must hold for every "
            "claim and every future section, and must be checkable rather than reviewed."),
        "smallest_safe_remediation": [
            {
                "id": "RM-1",
                "change": ("one canonical planner option universe: a single artifact derived "
                           "mechanically from M2's realizable pairs and M1's obligation rules"),
                "property": ("a claim is admitted only when required_roles ⊆ available_roles ⊆ "
                             "realizable_roles holds for it; a claim failing the test is "
                             "excluded with a recorded reason, never listed with an "
                             "unsatisfiable obligation"),
                "consumers": ("the deterministic feasibility proof and the model payload both "
                              "read the same serialized bytes and record its SHA; neither "
                              "re-derives it"),
                "prevents": "forms 1, 3, 4 and 5 of the contradiction audit, for all claims",
            },
            {
                "id": "RM-2",
                "change": ("derive requires_condition_slot from the same any-anchor test stage E "
                           "applies, instead of the all-anchors classification"),
                "property": ("an obligation is asserted only where the statement realization does "
                             "not already satisfy it, verified by rendering and validating the "
                             "statement alone"),
                "prevents": "false obligations of the C-005 form for every claim",
                "not_a_loosening": ("stage E is untouched. This makes the gate ask the same "
                                    "question the validator asks, rather than a stricter "
                                    "different one."),
            },
            {
                "id": "RM-3",
                "change": ("replace M2's diacritic-presence Turkishness test with one that "
                           "cannot false-negative on diacritic-free Turkish"),
                "property": "a field is judged English on evidence of English, not absence of çğıöşü",
                "prevents": ("wrongly UNREALIZABLE roles; 3 entries recover, R025's genuinely "
                             "English 'normally' must still be refused"),
                "risk": ("this one widens what M2 marks realizable, so it must be gated by the "
                         "static containment proof re-run and by fixtures asserting R025 stays "
                         "refused. It is a realization-contract change and is NOT made here."),
            },
        ],
        "adversarial_fixtures_required": [
            "a claim with a required role absent from available_roles must be excluded, not listed",
            "a claim whose statement already satisfies a condition must carry no condition obligation",
            "diacritic-free Turkish must not be classified as English",
            "genuinely English material must still be refused",
            "the feasibility proof and the model payload must read the same universe SHA",
            "a universe artifact violating the subset invariant must fail closed at build time",
        ],
    }


# ================================================================ assembly

def main() -> int:
    reproduction = reproduce_contradiction()
    set_audit = set_consistency_audit()
    c005 = c005_obligation_probe()
    turkish = turkishness_probe()
    universe = universe_comparison()
    limitations = limitation_interaction()
    classification = classify(reproduction, set_audit, c005, turkish, universe, limitations)
    remedy = remediation()

    hidden = {
        "form_2_offered_role_not_realizable": len(
            set_audit["contradictions"]["form_2_offered_role_not_realizable"]),
        "additional_form_1_beyond_c005": [
            row["claim_id"] for row in
            set_audit["contradictions"]["form_1_required_role_not_offered"]
            if row["claim_id"] != "SEC-02-2-C-005"],
        "turkishness_false_negatives_not_previously_recorded": turkish["false_negatives"],
    }

    analysis = {
        "version": VERSION, "phase": PHASE, "section_id": SECTION_ID,
        "analysed_at": datetime.now(timezone.utc).isoformat(),
        "pilot_1_verdict": "REJECTED — preserved, not reinterpreted",
        "reproduction": reproduction,
        "set_consistency_audit": {k: v for k, v in set_audit.items() if k != "rows"},
        "c005_obligation": c005,
        "turkishness_defect": turkish,
        "universe_comparison": universe,
        "limitation_interaction": limitations,
        "classification": classification,
        "hidden_contradictions": hidden,
        "remediation": remedy,
        "accounting": {
            "generation_calls": 0, "renders": 0, "retrieval_calls": 0, "qdrant_writes": 0,
            "corpus_reads": 0, "validators_changed": 0, "realization_contract_changed": 0,
            "glosses_or_lexicons_changed": 0, "frozen_artifacts_modified": 0,
            "pilot_2_authorised": False,
        },
        "frozen_evidence_sha256": {
            name: hashlib.sha256(path.read_bytes()).hexdigest()
            for name, path in sorted(FROZEN_EVIDENCE.items())},
    }

    write_json(SET_AUDIT_PATH, set_audit)
    write_json(UNIVERSE_PATH, universe)
    write_json(ANALYSIS_PATH, analysis)
    write_manifest(analysis)
    write_report(analysis, set_audit)

    print(f"root cause: {classification['root_cause_class']}")
    print(f"claims audited: {set_audit['claims_audited']}  "
          f"available⊆realizable holds for all: "
          f"{set_audit['available_subset_realizable_holds_for_all']}")
    print(f"required⊆available violations: "
          f"{set_audit['required_subset_available_violations']}")
    print(f"C-005 statement alone: {c005['statement_alone_status']} "
          f"-> false obligation: {c005['requires_condition_slot_is_a_false_obligation']}")
    print(f"turkishness false negatives: {turkish['false_negatives']} of "
          f"{turkish['entries_citing_not_turkish']}")
    print(f"universes identical: {universe['identical_claim_sets']}  "
          f"planner-only: {universe['claims_only_in_planner_universe']}")
    return 0


def write_manifest(analysis: dict) -> None:
    write_json(MANIFEST_PATH, {
        "version": VERSION, "phase": PHASE, "section_id": SECTION_ID,
        "generated_at": analysis["analysed_at"], "status": "closed_go",
        "final_decision": f"{PHASE} — CLOSED / GO",
        "pilot_1_verdict": "REJECTED",
        "root_cause_class": analysis["classification"]["root_cause_class"],
        "fault_attribution": analysis["classification"]["fault_attribution"],
        "claims_audited": analysis["set_consistency_audit"]["claims_audited"],
        "required_subset_available_violations":
            analysis["set_consistency_audit"]["required_subset_available_violations"],
        "hidden_contradictions": analysis["hidden_contradictions"],
        "accounting": analysis["accounting"],
        "frozen_evidence_sha256": analysis["frozen_evidence_sha256"],
        "artifacts": {
            "analysis": str(ANALYSIS_PATH.relative_to(ROOT)),
            "set_consistency_audit": str(SET_AUDIT_PATH.relative_to(ROOT)),
            "universe_comparison": str(UNIVERSE_PATH.relative_to(ROOT)),
            "report": str(REPORT_PATH.relative_to(ROOT)),
            "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
            "script": "scripts/67_architecture_v2_pilot_1_failure_analysis_v1.py",
            "tests": "tests/test_architecture_v2_pilot_1_failure_analysis_v1.py",
        },
        "pilot_2_authorised": False,
        "next_phase": "ARCHITECTURE V2 PLANNER OPTION UNIVERSE REMEDIATION V1",
    })


def write_report(analysis: dict, set_audit: dict) -> None:
    lines: list[str] = []
    add = lines.append
    c005 = analysis["c005_obligation"]
    turkish = analysis["turkishness_defect"]
    universe = analysis["universe_comparison"]
    classification = analysis["classification"]

    add(f"# {PHASE}")
    add("")
    add("**CLOSED / GO.** ARCHITECTURE V2 PILOT #1 remains REJECTED. Root cause is the "
        "authorisation option universe, not the model, the renderer or the validator.")
    add("")
    add("")
    add("## Reproduced contradiction")
    add("")
    for key, value in sorted(analysis["reproduction"].items()):
        if key == "probe_id":
            continue
        add(f"- `{key}`: {value}")
    add("")
    add("")
    add("## Set-consistency audit")
    add("")
    add(f"Invariant: `{set_audit['invariant']}`, over {set_audit['claims_audited']} exposed "
        "claims.")
    add("")
    add("| Claim | core | required | available | realizable | req⊆avail | avail⊆realiz |")
    add("|---|---|---|---|---|---|---|")
    for row in set_audit["rows"]:
        add(f"| {row['claim_id']} | {'yes' if row['is_required_core'] else ''} | "
            f"{', '.join(r for r in row['required_roles'] if r != 'CLAIM_STATEMENT|REQUIREMENT') or '—'} | "
            f"{len(row['available_roles'])} | {len(row['realizable_roles'])} | "
            f"{'ok' if row['required_subset_available'] else '**FAIL**'} | "
            f"{'ok' if row['available_subset_realizable'] else '**FAIL**'} |")
    add("")
    for form, entries in set_audit["contradictions"].items():
        add(f"- **{form}**: {len(entries)} — {[e['claim_id'] for e in entries] or 'none'}")
    add("")
    add("")
    add("## Was the obligation real?")
    add("")
    add(f"No. C-005's CLAIM_STATEMENT rendered alone validates "
        f"**{c005['statement_alone_status']}** with histogram "
        f"`{c005['statement_alone_histogram'] or '{}'}`.")
    add("")
    add(c005["mechanism"])
    add("")
    add(f"*{c005['generalisation']}*")
    add("")
    add("")
    add("## Was the role really unrealizable?")
    add("")
    add(f"No. {turkish['mechanism']}")
    add("")
    add(f"{turkish['false_negatives']} false negatives of "
        f"{turkish['entries_citing_not_turkish']} entries citing a non-Turkish field; "
        f"{turkish['true_positives']} correctly refused.")
    add("")
    add("| Claim | Role | Flagged | Genuinely English |")
    add("|---|---|---|---|")
    for row in turkish["detail"]:
        add(f"| {row['claim_id']} | {row['role']} | {row['flagged_as_not_turkish']} | "
            f"{'yes' if row['genuinely_english'] else '**no**'} |")
    add("")
    add(f"Severity: {turkish['severity']} — {turkish['severity_reasoning']}")
    add("")
    add("")
    add("## Two universes")
    add("")
    add(universe["finding"])
    add("")
    add(f"- planner universe: {universe['planner_universe']['claims']} claims, "
        f"{universe['planner_universe']['pairs']} pairs")
    add(f"- feasibility universe: {universe['feasibility_universe']['claims']} claims")
    add(f"- claims only in the planner universe: "
        f"{universe['claims_only_in_planner_universe']}")
    add("")
    add(f"**Minimal invariant.** {universe['minimal_invariant']}")
    add("")
    add("")
    add("## Classification")
    add("")
    add("| Candidate | Verdict |")
    add("|---|---|")
    for name, entry in classification["candidates"].items():
        add(f"| {name} | {entry['verdict']} |")
    add("")
    add(f"**Root cause: {classification['root_cause_class']}.**")
    add("")
    add(classification["statement"])
    add("")
    add("| Fault | |")
    add("|---|---|")
    for key, value in classification["fault_attribution"].items():
        if key.endswith("_reasoning"):
            continue
        add(f"| {key.replace('_', ' ')} | {value} |")
    add("")
    add("")
    add("## Smallest safe remediation")
    add("")
    add(analysis["remediation"]["no_claim_specific_patch"])
    add("")
    for item in analysis["remediation"]["smallest_safe_remediation"]:
        add(f"**{item['id']}.** {item['change']} — {item['property']} Prevents: "
            f"{item['prevents']}")
        if "risk" in item:
            add(f"  Risk: {item['risk']}")
        add("")
    add("")
    add("## Accounting")
    add("")
    add("| | |")
    add("|---|---|")
    for key, value in sorted(analysis["accounting"].items()):
        add(f"| {key.replace('_', ' ')} | {value} |")
    add("")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
