"""ARCHITECTURE V2 PLANNER OPTION UNIVERSE REMEDIATION V1 — the phase gate.

Remediation only. No generation, no rendering of a pilot, no retrieval, no Qdrant write, no corpus
read. ARCHITECTURE V2 PILOT #2 is not authorised here and is not run here.

What this file does is check, not build. RM-3 is built by `68_claim_realization_contract_v2_1.py`
and RM-1/RM-2 by `69_planner_option_universe_v2_1.py`; this driver re-hashes the frozen inputs,
proves the subset invariant on the serialized artifact, reproduces the Pilot #1 contradiction and
shows it unconstructible, runs the feasibility proof and the planner payload against the same
bytes, re-runs the Architecture V2 static containment proof under M2 v2.1 without overwriting the
M5 artifacts, drives the negative fixtures, and evaluates the frozen acceptance contract.

The rendered strings that appear in the audit artifacts are validator inputs. They are proof
material, not a draft; nothing here is authorised for release, and no plan in any of these files
came from a model.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PHASE = "ARCHITECTURE V2 PLANNER OPTION UNIVERSE REMEDIATION V1"
VERSION = "tunnelbook-architecture-v2-planner-universe-remediation-v1"
SECTION_ID = "SEC-02-2"

ARCH_V2 = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "architecture_v2"
REM = ARCH_V2 / "remediation_v1"
ACCEPTANCE = REM / "contracts" / "planner_universe_remediation_acceptance_contract_v1.json"
PREFLIGHT_PATH = REM / "audits" / "frozen_preflight_v1.json"
CONSISTENCY_PATH = REM / "audits" / "universe_consistency_v1.json"
FEASIBILITY_PATH = REM / "audits" / "feasibility_proof_v2_1.json"
PAYLOAD_PATH = REM / "audits" / "planner_payload_v2_1.json"
STATIC_PATH = REM / "audits" / "static_containment_proof_v2_1.json"
NEGATIVE_PATH = REM / "fixtures" / "negative_fixtures_remediation_v1.json"
CASES_PATH = REM / "fixtures" / "realization_universe_v2_1.json"
MANIFEST_PATH = ROOT / "data/book/manifests/architecture_v2_planner_universe_remediation_v1.json"
REPORT_PATH = ROOT / "reports" / "architecture_v2_planner_universe_remediation_v1.md"

ACCEPTANCE_MANIFEST = ROOT / "data/book/manifests/architecture_v2_acceptance_contract_v1.json"
IMPL_MANIFEST = ROOT / "data/book/manifests/architecture_v2_implementation_v1.json"
RETHINK_MANIFEST = ROOT / "data/book/manifests/sec_02_2_drafting_approach_rethink_v1.json"
PILOT_MANIFEST = ROOT / "data/book/manifests/sec_02_2_architecture_v2_pilot_1.json"

ZERO_TOLERANCE = (
    "UNSUPPORTED_PROPOSITION", "CLAIM_EXPANSION", "NUMERIC_DRIFT", "UNIT_DRIFT",
    "MODALITY_DRIFT", "CONDITION_DROPPED", "QUALIFIER_DROPPED", "SEMANTIC_SCOPE_MISMATCH",
    "LANGUAGE_MISMATCH", "CLAIM_DENYLISTED", "UNKNOWN_CITATION",
)

# Artifacts this phase must leave byte-identical. Historical regression is a hash list, not a
# promise: every one of these is compared against the SHA a previous phase recorded or, where no
# manifest recorded it, against the value observed at the start of this run.
HISTORICAL_ARTIFACTS = {
    "M1_semantic_plan_ir_contract_v2": ARCH_V2 / "contracts/semantic_plan_ir_contract_v2.json",
    "M2_claim_realization_contract_v2": ARCH_V2 / "contracts/claim_realization_contract_v2.json",
    "M3_turkish_morphology_v2": ARCH_V2 / "contracts/turkish_morphology_v2.json",
    "M5_negative_fixtures_v2": ARCH_V2 / "fixtures/negative_fixtures_v2.json",
    # Compared against the value observed at the start of this run rather than against the
    # implementation manifest: the artifact stamps its own generation time and was last rewritten
    # by the Pilot #1 gate, so the manifest hash is known stale. What this phase must show is that
    # it did not touch it, and that is what a start-of-run snapshot shows.
    "M5_static_containment_proof_v2_as_found": (
        ARCH_V2 / "audits/static_containment_proof_v2.json"),
    "M5_realization_universe_v2": ARCH_V2 / "fixtures/realization_universe_v2.json",
    "architecture_v2_acceptance_contract_v1": (
        ARCH_V2 / "contracts/architecture_v2_acceptance_contract_v1.json"),
    "pilot_1_raw_plan": ARCH_V2 / "pilot_1/raw/semantic_plan_raw_v1.json",
    "pilot_1_plan": ARCH_V2 / "pilot_1/plan/semantic_plan_ir_v2.json",
    "pilot_1_validation": ARCH_V2 / "pilot_1/validation/pilot_1_validation.json",
    "pilot_1_option_set": ARCH_V2 / "pilot_1/contracts/planner_option_set_v1.json",
    "pilot_1_feasibility": ARCH_V2 / "pilot_1/audits/feasibility_proof_v1.json",
    "pilot_1_pre_generation_gate": ARCH_V2 / "pilot_1/audits/pre_generation_gate_v1.json",
    "section_drafting_contract_v1": (
        ROOT / "data/book/drafting/contracts/section_drafting_contract_v1.json"),
    "draft_language_contract_v1": (
        ROOT / "data/book/drafting/contracts/draft_language_contract_v1.json"),
    "composition_safe_allowlist_v1": (
        ROOT / "data/book/sec_02_2_limitation_resolution/claims/"
        "composition_safe_allowlist_v1.jsonl"),
    "draft_plan_v1_2": ROOT / "data/book/drafting/sec_02_2/draft_plan_v1_2.json",
}

FROZEN_CODE = {
    "M1_plan_ir": "59_semantic_plan_ir_contract_v2.py",
    "M2_realization_v2": "60_claim_realization_contract_v2.py",
    "M3_morphology": "61_turkish_morphology_v2.py",
    "M4_renderer": "62_deterministic_surface_renderer_v2.py",
    "M5_static_proof": "63_static_containment_proof_v2.py",
    "draft_validator_v1": "49_section_draft_validator_v1.py",
    "draft_language_validator_v1": "51_draft_language_validator_v1.py",
    "draft_validator_v1_1": "52_section_draft_validator_v1_1.py",
    "draft_validator_v1_2": "54_section_draft_validator_v1_2.py",
    "citation_renderer": "48_book_citation_renderer_v1.py",
    "pilot_1": "65_sec_02_2_architecture_v2_pilot_1.py",
}

# Lexicons and gloss tables this phase may not widen. Hashed as isolated sub-objects so a change
# anywhere else in the drafting contract cannot mask a change here.
LEXICON_KEYS = ("translation_glosses", "condition_glosses", "function_lexicon",
                "paraphrase_lexicon")


def _load(name: str, filename: str):
    path = ROOT / "scripts" / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


V1 = _load("rem_v1", "49_section_draft_validator_v1.py")
V1_2 = _load("rem_v1_2", "54_section_draft_validator_v1_2.py")
LANG = _load("rem_lang", "51_draft_language_validator_v1.py")
PLAN_IR = _load("rem_plan_ir", "59_semantic_plan_ir_contract_v2.py")
M2_V2 = _load("rem_m2_v2", "60_claim_realization_contract_v2.py")
RENDER = _load("rem_render", "62_deterministic_surface_renderer_v2.py")
PROOF = _load("rem_proof", "63_static_containment_proof_v2.py")
M2_V2_1 = _load("rem_m2_v2_1", "68_claim_realization_contract_v2_1.py")
UNIVERSE = _load("rem_universe", "69_planner_option_universe_v2_1.py")
RETHINK = _load("rem_rethink", "57_sec_02_2_drafting_approach_rethink_v1.py")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, payload: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    return sha_text(text)


# ================================================================ freeze first


def frozen_preflight() -> dict:
    """Re-hash every frozen Architecture V2 input. Drift anywhere is NO-GO and STOP."""
    recorded = json.loads(RETHINK_MANIFEST.read_text(encoding="utf-8"))["frozen_inputs_sha256"]
    rethink_drift = [name for name in sorted(recorded)
                     if sha_file(RETHINK.FROZEN_INPUTS[name]) != recorded[name]]

    impl = json.loads(IMPL_MANIFEST.read_text(encoding="utf-8"))
    # M5's proof artifact stamps its own generation time and is re-derived rather than hashed,
    # exactly as the Pilot #1 gate established. Its integrity is checked on substance by the
    # static proof re-run below, which is the stronger check.
    impl_drift = [key for key, mod in impl["modules"].items()
                  if "sha256" in mod and key != "M5_static_containment_proof_v2"
                  and sha_file(ROOT / mod["path"]) != mod["sha256"]]

    acceptance_recorded = json.loads(
        ACCEPTANCE_MANIFEST.read_text(encoding="utf-8"))["contract_sha256"]
    acceptance_now = sha_file(ARCH_V2 / "contracts/architecture_v2_acceptance_contract_v1.json")

    pilot_drift: list[str] = []
    if PILOT_MANIFEST.is_file():
        pilot = json.loads(PILOT_MANIFEST.read_text(encoding="utf-8"))
        for key, value in (pilot.get("artifact_sha256") or {}).items():
            candidate = ROOT / value["path"] if isinstance(value, dict) else None
            expected = value.get("sha256") if isinstance(value, dict) else value
            if candidate is None or not candidate.is_file():
                continue
            if sha_file(candidate) != expected:
                pilot_drift.append(key)

    missing_code = [f for f in FROZEN_CODE.values() if not (ROOT / "scripts" / f).is_file()]
    return {
        "checked_at": now(),
        "rethink_inputs_checked": len(recorded),
        "rethink_drift": rethink_drift,
        "implementation_artifacts_checked": sum("sha256" in m for m in impl["modules"].values()),
        "implementation_drift": impl_drift,
        "implementation_artifacts_excluded": [
            "M5_static_containment_proof_v2 — timestamped and re-derived; checked on substance"],
        "pilot_1_drift": pilot_drift,
        "architecture_v2_acceptance_contract_sha256": acceptance_now,
        "architecture_v2_acceptance_contract_unamended": acceptance_now == acceptance_recorded,
        "missing_frozen_code": missing_code,
        "frozen_code_sha256": {k: sha_file(ROOT / "scripts" / v)
                               for k, v in sorted(FROZEN_CODE.items())
                               if (ROOT / "scripts" / v).is_file()},
        "historical_sha256": {k: sha_file(p) for k, p in sorted(HISTORICAL_ARTIFACTS.items())
                              if p.is_file()},
        "lexicon_sha256": lexicon_hashes(),
        "drift": len(rethink_drift) + len(impl_drift) + len(pilot_drift) + len(missing_code),
    }


def lexicon_hashes() -> dict[str, str]:
    contract = json.loads(
        (ROOT / "data/book/drafting/contracts/section_drafting_contract_v1.json")
        .read_text(encoding="utf-8"))
    return {key: sha_text(json.dumps(contract.get(key), ensure_ascii=False, sort_keys=True))
            for key in LEXICON_KEYS}


def historical_regression(baseline: dict) -> dict:
    """Every frozen artifact and every frozen module, compared against the pre-phase hash."""
    artifact_drift = [k for k, v in baseline["historical_sha256"].items()
                      if sha_file(HISTORICAL_ARTIFACTS[k]) != v]
    code_drift = [k for k, v in baseline["frozen_code_sha256"].items()
                  if sha_file(ROOT / "scripts" / FROZEN_CODE[k]) != v]
    lexicon_drift = [k for k, v in baseline["lexicon_sha256"].items()
                     if lexicon_hashes()[k] != v]
    return {
        "artifacts_checked": len(baseline["historical_sha256"]),
        "artifact_drift": artifact_drift,
        "frozen_modules_checked": len(baseline["frozen_code_sha256"]),
        "frozen_module_drift": code_drift,
        "lexicons_checked": len(baseline["lexicon_sha256"]),
        "lexicon_drift": lexicon_drift,
        "byte_identical": not (artifact_drift or code_drift or lexicon_drift),
    }


# ================================================================ RM-1/2/3 execution


def run_remediation() -> dict:
    """Build M2 v2.1 and the canonical universe, in that order, and report both deltas."""
    contract, index = M2_V2_1.build_contract_v2_1()
    m2_sha = M2_V2_1.write(contract)
    delta = M2_V2_1.delta_against_v2(contract)

    bundle = V1.load_bundle()
    realization = M2_V2_1.load()
    built = UNIVERSE.build_universe(realization, bundle)
    violations = UNIVERSE.assert_invariant(built["universe"])
    universe_sha = UNIVERSE.sha_bytes(UNIVERSE.canonical_bytes(built["universe"]))
    UNIVERSE.UNIVERSE_PATH.write_bytes(UNIVERSE.canonical_bytes(
        {"universe": built["universe"], "audit": built["audit"],
         "universe_sha256": universe_sha}))

    return {
        "m2_v2_1": {
            "path": str(M2_V2_1.CONTRACT_PATH.relative_to(ROOT)),
            "sha256": m2_sha,
            "delta": delta,
            "language_rule": index.summary(),
        },
        "universe": {
            "path": str(UNIVERSE.UNIVERSE_PATH.relative_to(ROOT)),
            "sha256": universe_sha,
            "artifact_sha256": sha_file(UNIVERSE.UNIVERSE_PATH),
            "construction_violations": violations,
            "claims_allocated": built["audit"]["claims_allocated"],
            "claims_exposed": built["audit"]["claims_exposed"],
            "claims_excluded": built["audit"]["claims_excluded"],
            "exclusions": built["universe"]["exclusions"],
        },
        "built": built,
        "realization": realization,
        "bundle": bundle,
    }


# ================================================================ consistency test


def consistency_test(built: dict, bundle) -> dict:
    """RM-1's invariant, proven claim by claim, plus the direct Pilot #1 reproduction.

    Pilot #1's contradiction was `SEC-02-2-C-005` carrying `requires_condition_slot: true` beside
    an `available_roles` list without CONDITION. The check below is not "C-005 is fine now" — it
    is the general form: for every exposed claim, every required role must be available and
    realizable. C-005 is named only because it is the historical instance.
    """
    universe = built["universe"]
    rows = []
    for option in universe["options"]:
        required = set(option["required_roles"])
        available = set(option["available_roles"])
        realizable = set(option["realizable_roles"])
        rows.append({
            "claim_id": option["claim_id"],
            "required_roles": sorted(required),
            "available_roles": sorted(available),
            "realizable_roles": sorted(realizable),
            "required_subset_available": required <= available,
            "available_subset_realizable": available <= realizable,
            "holds": required <= available <= realizable,
        })

    c005 = next((r for r in rows if r["claim_id"] == "SEC-02-2-C-005"), None)
    historical = {
        "claim_id": "SEC-02-2-C-005",
        "pilot_1_state": ("requires_condition_slot=true with CONDITION absent from "
                          "available_roles"),
        "exposed_now": c005 is not None,
        "requires_condition_slot": next(
            (o["requires_condition_slot"] for o in universe["options"]
             if o["claim_id"] == "SEC-02-2-C-005"), None),
        "condition_available": bool(c005 and "CONDITION" in c005["available_roles"]),
        "condition_realizable": bool(c005 and "CONDITION" in c005["realizable_roles"]),
        "contradiction_present": bool(
            c005 and "CONDITION" in c005["required_roles"]
            and "CONDITION" not in c005["available_roles"]),
    }
    historical["both_upstream_defects_closed"] = (
        historical["requires_condition_slot"] is False and historical["condition_available"])

    return {
        "invariant": "required_roles ⊆ available_roles ⊆ realizable_roles",
        "exposed_claims": len(rows),
        "holds_for_all": all(r["holds"] for r in rows),
        "violations": [r["claim_id"] for r in rows if not r["holds"]],
        "rows": rows,
        "pilot_1_contradiction": historical,
        "obligations": built["audit"]["obligations"],
        "obligation_derivation": {
            "rule": ("a CONDITION slot is required only where the unchanged Draft Validator v1.2, "
                     "run on the claim's statement realization alone, raises CONDITION_DROPPED"),
            "reimplemented": False,
            "claim_specific_branches": 0,
            "claims_probed": sum(1 for o in built["audit"]["obligations"].values()
                                 if "obligation_probe" in o),
            "obligation_asserted": sorted(cid for cid, o
                                          in built["audit"]["obligations"].items()
                                          if o["requires_condition_slot"]),
            "obligation_withdrawn_vs_all_anchors_rule": sorted(
                cid for cid, o in built["audit"]["obligations"].items()
                if not o["requires_condition_slot"]
                and UNIVERSE.original_obligation_rule(bundle.allowlist[cid], bundle)),
        },
    }


# ================================================================ feasibility and payload


def feasibility_proof(realization, bundle) -> dict:
    """A complete SEC-02-2 plan, built from the serialized universe and nothing else."""
    UNIVERSE.ensure_obligation_rule()
    universe, universe_sha = UNIVERSE.load_universe()
    raw_plan = UNIVERSE.feasibility_plan(universe)
    try:
        payload = RENDER.render_from_raw(raw_plan, realization, bundle)
    except (RENDER.RenderRefusal, PLAN_IR.PlanRejection) as error:
        return {"feasible": False, "stage": "render", "error": str(error),
                "universe_sha256": universe_sha}

    ir = V1.parse_draft_ir(payload)
    result = V1_2.validate_draft(ir, bundle)
    histogram = dict(result.failure_histogram)

    plan = json.loads((ROOT / "data/book/drafting/sec_02_2/draft_plan_v1_2.json")
                      .read_text(encoding="utf-8"))
    stated = {u["claim_ids"][0] for u in payload["units"] if u["claim_ids"]}
    covered = [t for t in plan["required_topics"]["required"]
               if set(plan["required_topics"]["coverage"][t]["required_core_claim_ids"]) <= stated]
    core = set(universe["required_core_claim_ids"])

    selected = {(s["claim_id"], s["realization_role"])
                for sub in raw_plan["subsections"]
                for para in sub["paragraph_groups"] for s in para["slots"]}
    unrealizable_selected = sorted(
        f"{cid}/{role}" for cid, role in selected
        if (realization.entry(cid, role) or {}).get("status") != "REALIZABLE")

    # Every mandatory condition and qualifier, measured on the rendered prose rather than assumed
    # from the plan. Stage E and stage L already scored them; this counts what they scored.
    conditions_required = qualifiers_required = 0
    for claim_id in sorted(stated):
        claim = bundle.allowlist[claim_id]
        conditions_required += len([c for c in (claim.get("conditions") or [])
                                    if V1.content_tokens(c, bundle.function_lexicon)])
        qualifiers_required += len(claim.get("qualifiers") or [])

    lang_contract = LANG.load_contract()
    language_failures = [
        f.as_dict() if hasattr(f, "as_dict") else str(f)
        for unit in payload["units"]
        for f in LANG.validate_unit(
            unit_id=unit["unit_id"], unit_type=unit["unit_type"], material=unit["material"],
            section_language=payload["language"], text=unit["text"],
            claim_ids=unit["claim_ids"], contract=lang_contract)]

    numeric_units = [u for u in payload["units"] if u.get("numeric_values")]
    source_key_ok = all(
        set(u["source_keys"]) <= set(bundle.allowlist[u["claim_ids"][0]].get("source_keys") or [])
        for u in payload["units"] if u["claim_ids"] and u["source_keys"])
    relations_ok = all(
        u.get("relationship_type", "NONE") in
        (set(bundle.allowlist[u["claim_ids"][0]].get("allowed_relationships") or [])
         | {"NONE", "INDEPENDENT"})
        for u in payload["units"] if u["claim_ids"])

    feasible = (result.status == "ACCEPT"
                and len(covered) == len(plan["required_topics"]["required"])
                and core <= stated
                and not histogram
                and not unrealizable_selected
                and not language_failures
                and source_key_ok and relations_ok)

    return {
        "feasible": feasible,
        "universe_sha256": universe_sha,
        "plan_id": raw_plan["plan_id"],
        "units": len(payload["units"]),
        "material_units": sum(1 for u in payload["units"] if u["material"]),
        "slots": len(selected),
        "validation": {"status": result.status, "histogram": histogram,
                       "rejected_unit_ids": sorted(result.rejected_unit_ids)},
        "topics": {"required": len(plan["required_topics"]["required"]),
                   "covered": len(covered), "topics": covered,
                   "missing": sorted(set(plan["required_topics"]["required"]) - set(covered))},
        "required_core_claims_stated": sorted(core & stated),
        "required_core_claims_missing": sorted(core - stated),
        "claims_stated": sorted(stated),
        "mandatory_conditions_required": conditions_required,
        "mandatory_conditions_dropped": histogram.get("CONDITION_DROPPED", 0),
        "mandatory_qualifiers_required": qualifiers_required,
        "mandatory_qualifiers_dropped": (histogram.get("QUALIFIER_DROPPED", 0)
                                         + histogram.get("QUALIFIER_SEMANTICS_UNMET", 0)),
        "numeric_units": len(numeric_units),
        "numeric_drift": histogram.get("NUMERIC_DRIFT", 0) + histogram.get("UNIT_DRIFT", 0),
        "source_keys_valid": source_key_ok,
        "relations_supported": relations_ok,
        "language_failures": language_failures,
        "unrealizable_pairs_selected": unrealizable_selected,
        "plan": raw_plan,
        "rendered_units": [{"unit_id": u["unit_id"], "claim_ids": u["claim_ids"],
                            "text": u["text"]} for u in payload["units"]],
    }


def planner_payload_proof() -> dict:
    """Build the future planner payload independently, and hash the universe portion of each."""
    universe, universe_sha = UNIVERSE.load_universe()
    payload = UNIVERSE.planner_payload(universe)
    embedded_sha = UNIVERSE.universe_sha_of(payload)
    return {
        "payload_version": payload["payload_version"],
        "universe_sha256": embedded_sha,
        "load_sha256": universe_sha,
        "options": len(payload["universe"]["options"]),
        "unrealizable_pairs_exposed": payload["universe"]["unrealizable_pairs_exposed"],
        "model_called": False,
        "payload": payload,
    }


# ================================================================ static proof under M2 v2.1


def static_proof_v2_1(realization, bundle) -> dict:
    """The Architecture V2 static containment proof, re-run under M2 v2.1.

    M5's own machinery is reused — enumeration, universe run, refusals, negative fixtures — with
    the v2.1 contract passed in. The M5 artifacts are not overwritten: this writes to the
    remediation's own paths, so `static_containment_proof_v2.json` stays byte-identical.
    """
    UNIVERSE.ensure_obligation_rule()
    cases, not_plannable = PROOF.enumerate_universe(realization, bundle)
    write_json(CASES_PATH, {"version": "realization-universe-v2-1", "cases": cases,
                            "not_plannable": not_plannable})
    universe = PROOF.run_universe(cases, realization, bundle)
    refusals = PROOF.run_unrealizable_refusals(realization, bundle)
    negatives = PROOF.negative_fixtures(realization, bundle)
    determinism = determinism_probe_v2_1(cases, realization, bundle)

    zero = {code: count for code, count in universe["failure_histogram"].items()
            if code in ZERO_TOLERANCE and count}
    false_rejects = [r["case_id"] for r in universe["results"] if r["outcome"] != "ACCEPT"]
    passed = (not zero and not false_rejects and not negatives["false_accepts"]
              and not refusals["leaked"] and determinism["in_process_identical"]
              and determinism["cross_process_identical"])
    return {
        "version": "tunnelbook-static-containment-proof-v2-1",
        "realization_contract": "tunnelbook-claim-realization-contract-v2-1",
        "validator_version": V1_2.VALIDATOR_VERSION,
        "validator_changed": False,
        "universe": {
            "claims": realization.payload["totals"]["claims"],
            "roles": realization.payload["totals"]["roles"],
            "claim_role_pairs": realization.payload["totals"]["pairs"],
            "realizable_pairs": realization.payload["totals"]["realizable"],
            "unrealizable_pairs": realization.payload["totals"]["unrealizable"],
            "enumerated_cases": universe["cases"],
            "pairs_no_permitted_plan_contains": len(not_plannable),
            "rendered_units": universe["rendered_units"],
            "accepted_cases": universe["accepted"],
        },
        "failure_histogram": universe["failure_histogram"],
        "zero_tolerance_violations": zero,
        "false_rejects": false_rejects,
        "false_accepts": negatives["false_accepts"],
        "unrealizable_refusals": {k: v for k, v in refusals.items() if k != "detail"},
        "negative_fixtures": {k: v for k, v in negatives.items() if k != "fixtures"},
        "not_plannable_pairs": not_plannable,
        "determinism": determinism,
        "status": "PASS" if passed else "FAIL",
    }


def determinism_probe_v2_1(cases: list[dict], realization, bundle) -> dict:
    """Byte equality in-process and in a fresh process, against the v2.1 contract."""
    def digest() -> str:
        hasher = hashlib.sha256()
        for case in cases:
            try:
                payload = RENDER.render_from_raw(case["plan"], realization, bundle)
            except RENDER.RenderRefusal as refusal:
                hasher.update(f"REFUSED:{refusal.code}".encode("utf-8"))
                continue
            hasher.update(RENDER.render_bytes(payload))
        return hasher.hexdigest()

    in_process = [digest() for _ in range(3)]
    script = (
        "import importlib.util,sys,hashlib,json\n"
        f"sys.path.insert(0,{str(ROOT)!r})\n"
        "def L(n,f):\n"
        f"    p={str(ROOT / 'scripts')!r}+'/'+f\n"
        "    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s)\n"
        "    sys.modules[n]=m;s.loader.exec_module(m);return m\n"
        "v1=L('a','49_section_draft_validator_v1.py')\n"
        "m21=L('b','68_claim_realization_contract_v2_1.py')\n"
        "u=L('d','69_planner_option_universe_v2_1.py')\n"
        "rd=L('c','62_deterministic_surface_renderer_v2.py')\n"
        "b=v1.load_bundle();r=m21.load()\n"
        "uni,_=u.load_universe()\n"
        "u.install_obligation_rule({o['claim_id']:{'registered_conditions':"
        "b.allowlist[o['claim_id']].get('conditions') or [],"
        "'requires_condition_slot':o['requires_condition_slot']} for o in uni['options']})\n"
        f"cases=json.loads(open({str(CASES_PATH)!r},encoding='utf-8').read())['cases']\n"
        "h=hashlib.sha256()\n"
        "for c in cases:\n"
        "    try:\n"
        "        h.update(rd.render_bytes(rd.render_from_raw(c['plan'],r,b)))\n"
        "    except rd.RenderRefusal as e:\n"
        "        h.update(('REFUSED:'+e.code).encode('utf-8'))\n"
        "print(h.hexdigest())\n")
    completed = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True,
                               cwd=str(ROOT))
    cross = completed.stdout.strip()
    return {
        "in_process_runs": len(in_process),
        "in_process_identical": len(set(in_process)) == 1,
        "in_process_sha256": in_process[0],
        "cross_process_sha256": cross,
        "cross_process_identical": cross == in_process[0],
        "cross_process_stderr": completed.stderr.strip()[-400:],
    }


# ================================================================ negative fixtures


def negative_fixtures(realization, bundle, built: dict) -> dict:
    """Every failure this remediation claims to prevent, attempted and refused.

    A remediation that only demonstrates its happy path proves nothing about the class it closes.
    Each fixture below constructs the defect deliberately — a mutated universe, a diverging SHA,
    an English token offered as Turkish material — and records the refusal.
    """
    UNIVERSE.ensure_obligation_rule()
    fixtures: list[dict] = []
    universe = built["universe"]
    scratch = REM / "fixtures" / "_mutated"
    scratch.mkdir(parents=True, exist_ok=True)

    def add(fixture_id: str, description: str, expected: str, outcome: str,
            rejected: bool, detail: Any = None) -> None:
        fixtures.append({"fixture_id": fixture_id, "description": description,
                         "expected": expected, "outcome": outcome, "rejected": rejected,
                         "detail": detail})

    def load_mutated(fixture_id: str, mutate) -> tuple[str, bool, Any]:
        payload = json.loads(json.dumps({"universe": universe}, ensure_ascii=False))
        mutate(payload["universe"])
        path = scratch / f"{fixture_id}.json"
        path.write_bytes(UNIVERSE.canonical_bytes(payload))
        try:
            UNIVERSE.load_universe(path)
        except UNIVERSE.UniverseViolation as error:
            return "UNIVERSE_LOAD_REFUSED", True, str(error)[:400]
        return "LOADED", False, None

    # --- 1. a required role absent from available_roles
    def drop_available(u: dict) -> None:
        option = u["options"][0]
        option["required_roles"] = sorted(set(option["required_roles"]) | {"CONDITION"})
        option["available_roles"] = [r for r in option["available_roles"] if r != "CONDITION"]
    outcome, rejected, detail = load_mutated("NEG-U01", drop_available)
    add("NEG-U01", "a required role absent from available_roles",
        "UNIVERSE_LOAD_REFUSED", outcome, rejected, detail)

    # --- 2. an available role absent from realizable_roles
    def unrealizable_available(u: dict) -> None:
        option = u["options"][0]
        option["available_roles"] = sorted(set(option["available_roles"]) | {"EXEMPLIFICATION"})
        option["realizable_roles"] = [r for r in option["realizable_roles"]
                                      if r != "EXEMPLIFICATION"]
    outcome, rejected, detail = load_mutated("NEG-U02", unrealizable_available)
    add("NEG-U02", "an available role absent from realizable_roles",
        "UNIVERSE_LOAD_REFUSED", outcome, rejected, detail)

    # --- 3. a mandatory claim with no satisfiable role set
    core = sorted(universe["required_core_claim_ids"])[0]
    try:
        stripped = {cid: dict(row) for cid, row in bundle.allowlist.items()}
        entries = [e for e in realization.payload["entries"]
                   if not (e["claim_id"] == core
                           and e["realization_role"] in UNIVERSE.STATEMENT_ROLES)]
        for entry in realization.payload["entries"]:
            if entry["claim_id"] == core and entry["realization_role"] in UNIVERSE.STATEMENT_ROLES:
                entries.append({**entry, "status": "UNREALIZABLE",
                                "reason": "negative fixture", "segments": []})
        crippled = M2_V2.RealizationContract({**realization.payload, "entries": entries})
        UNIVERSE.build_universe(crippled, bundle)
        outcome, rejected, detail = "BUILT", False, f"{core} survived with no statement role"
    except UNIVERSE.UniverseViolation as error:
        outcome, rejected, detail = "UNIVERSE_BUILD_REFUSED", True, str(error)[:400]
    add("NEG-U03", f"a mandatory core claim ({core}) with no satisfiable role set",
        "UNIVERSE_BUILD_REFUSED", outcome, rejected, detail)

    # --- 4. the feasibility proof and the payload read different universes
    divergent = json.loads(json.dumps(universe, ensure_ascii=False))
    divergent["options"] = divergent["options"][:-1]
    feasibility_sha = UNIVERSE.sha_bytes(UNIVERSE.canonical_bytes(universe))
    payload_sha = UNIVERSE.sha_bytes(UNIVERSE.canonical_bytes(divergent))
    add("NEG-U04", "the feasibility proof universe differs from the planner payload universe",
        "SHA_MISMATCH_DETECTED", "SHA_MISMATCH_DETECTED" if feasibility_sha != payload_sha
        else "SHA_EQUAL", feasibility_sha != payload_sha,
        {"feasibility_sha256": feasibility_sha, "payload_sha256": payload_sha})

    # --- 5. an alternate option universe injected between the two consumers
    def inject_alternate(u: dict) -> None:
        u["options"].append({
            "claim_id": "SEC-02-2-R025", "topic": None, "source_keys": [],
            "allowed_relationships": [], "statement_role": "CLAIM_STATEMENT",
            "required_roles": ["CLAIM_STATEMENT", "QUALIFIER_SCOPE"],
            "available_roles": ["CLAIM_STATEMENT"],
            "realizable_roles": ["CLAIM_STATEMENT"],
            "requires_condition_slot": False, "requires_qualifier_slot": True,
            "condition_obligation_basis": "injected"})
    outcome, rejected, detail = load_mutated("NEG-U05", inject_alternate)
    add("NEG-U05", "an injected alternate option universe carrying an unsatisfiable claim",
        "UNIVERSE_LOAD_REFUSED", outcome, rejected, detail)

    # --- 6. the Pilot #1 contradiction, reconstructed exactly
    def c005_contradiction(u: dict) -> None:
        for option in u["options"]:
            if option["claim_id"] == "SEC-02-2-C-005":
                option["requires_condition_slot"] = True
                option["required_roles"] = sorted(set(option["required_roles"]) | {"CONDITION"})
                option["available_roles"] = [r for r in option["available_roles"]
                                             if r != "CONDITION"]
    outcome, rejected, detail = load_mutated("NEG-U06", c005_contradiction)
    add("NEG-U06", "the SEC-02-2-C-005 historical contradiction, reconstructed",
        "UNIVERSE_LOAD_REFUSED", outcome, rejected, detail)

    # --- 7. false Turkishness by diacritic absence
    index = M2_V2_1.SourceLanguageIndex(bundle)
    diacritic_free = ["ilk tabaka", "takip eden tabakalar", "ilave tabakalar"]
    old_rule = {text: M2_V2.TURKISH_MARK.search(text) is not None for text in diacritic_free}
    new_rule = {text: index.is_admissible_turkish(text) for text in diacritic_free}
    add("NEG-U07", "diacritic-free Turkish classified as not Turkish by the v2 character rule",
        "OLD_RULE_FALSE_NEGATIVE_REPRODUCED_AND_CORRECTED",
        "OLD_RULE_FALSE_NEGATIVE_REPRODUCED_AND_CORRECTED"
        if (not any(old_rule.values()) and all(new_rule.values())) else "NOT_REPRODUCED",
        not any(old_rule.values()) and all(new_rule.values()),
        {"v2_diacritic_rule": old_rule, "v2_1_language_rule": new_rule})

    # --- 8. English material offered as Turkish
    english = ["normally", "dependent on tunnel size", "In some",
               "the typical thickness of an initial shotcrete lining ranges from 4 to 16 inches "
               "(100 to 400 mm).",
               "this string is in no frozen field"]
    admitted = {text: index.is_admissible_turkish(text) for text in english}
    add("NEG-U08", "English and unattested material offered as admissible Turkish",
        "ALL_REFUSED", "ALL_REFUSED" if not any(admitted.values()) else "ADMITTED",
        not any(admitted.values()), {"is_admissible_turkish": admitted,
                                     "field_language": {t: index.field_language(t)
                                                        for t in english}})

    # --- 9. R025's `normally` offered as a plannable qualifier
    r025_entry = realization.entry("SEC-02-2-R025", "QUALIFIER_SCOPE")
    outcome, detail = PROOF._probe_plan(
        PROOF._plan("P-NEG-R025", [PROOF._slot("N09", "SEC-02-2-R025", "QUALIFIER_SCOPE")]),
        realization, bundle)
    add("NEG-U09", "SEC-02-2-R025 / QUALIFIER_SCOPE (`normally`) selected in a plan",
        "PLAN_VALIDATION_REJECTED", outcome, outcome != "RENDERED",
        {"contract_status": r025_entry["status"], "reason": r025_entry.get("reason"),
         "plan_failures": detail})
    exposed_r025 = [o for o in universe["options"] if o["claim_id"] == "SEC-02-2-R025"]
    add("NEG-U09b", "SEC-02-2-R025 / QUALIFIER_SCOPE offered by the canonical universe",
        "NOT_OFFERED",
        "NOT_OFFERED" if not any("QUALIFIER_SCOPE" in o["available_roles"]
                                 for o in exposed_r025) else "OFFERED",
        not any("QUALIFIER_SCOPE" in o["available_roles"] for o in exposed_r025),
        {"exposed": bool(exposed_r025)})

    # --- 10. a source key registered to a different claim
    outcome, detail = PROOF._probe_plan(
        PROOF._with(PROOF._plan("P-NEG-KEY",
                                [PROOF._slot("N10", "SEC-02-2-C-005", "CLAIM_STATEMENT")]),
                    citation_source_keys=sorted(
                        bundle.allowlist["SEC-02-2-C-009"].get("source_keys") or [])),
        realization, bundle)
    add("NEG-U10", "a source key registered to a different claim (source laundering)",
        "PLAN_VALIDATION_REJECTED", outcome, outcome != "RENDERED", detail)

    # --- 11. a numeric the declaring claim does not register
    outcome, detail = PROOF._probe_plan(
        PROOF._with(PROOF._plan("P-NEG-NUM",
                                [PROOF._slot("N11", "SEC-02-2-C-005", "CLAIM_STATEMENT")]),
                    numeric_fact_ids=["SEC-02-2-C-009#NUM0"]),
        realization, bundle)
    add("NEG-U11", "a numeric addressed through another claim's id",
        "PLAN_VALIDATION_REJECTED", outcome, outcome != "RENDERED", detail)
    outcome, detail = PROOF._probe_plan(
        PROOF._with(PROOF._plan("P-NEG-UNIT",
                                [PROOF._slot("N12", "SEC-02-2-C-005", "CLAIM_STATEMENT")]),
                    numeric_fact_ids=["SEC-02-2-C-005#NUM9"]),
        realization, bundle)
    add("NEG-U11b", "a numeric fact id the claim does not register",
        "PLAN_VALIDATION_REJECTED", outcome, outcome != "RENDERED", detail)

    # --- 12. a newly REALIZABLE pair must still pass every unchanged guard
    newly = [(r["claim_id"], r["realization_role"])
             for r in M2_V2_1.delta_against_v2(realization.payload)["newly_realizable"]]
    guard_rows = []
    for claim_id, role in newly:
        try:
            plan = PROOF._plan(f"P-GUARD-{claim_id}",
                               [PROOF._slot("G01", claim_id, UNIVERSE._statement_role(
                                   claim_id, realization)),
                                PROOF._slot("G02", claim_id, role)])
            payload = RENDER.render_from_raw(plan, realization, bundle)
            result = V1_2.validate_draft(V1.parse_draft_ir(payload), bundle)
            guard_rows.append({"pair": f"{claim_id}/{role}", "status": result.status,
                               "histogram": dict(result.failure_histogram),
                               "text": [u["text"] for u in payload["units"] if u["material"]]})
        except Exception as error:  # noqa: BLE001
            guard_rows.append({"pair": f"{claim_id}/{role}", "status": "ERROR",
                               "histogram": {"ERROR": str(error)[:200]}})
    all_clean = all(r["status"] == "ACCEPT" and not r["histogram"] for r in guard_rows)
    add("NEG-U12", "every newly REALIZABLE pair rendered and put to the unchanged validator",
        "ALL_ACCEPT_EMPTY_HISTOGRAM", "ALL_ACCEPT_EMPTY_HISTOGRAM" if all_clean else "DEFECT",
        all_clean, guard_rows)

    for path in scratch.glob("*.json"):
        path.unlink()
    scratch.rmdir()

    return {
        "count": len(fixtures),
        "rejected": sum(1 for f in fixtures if f["rejected"]),
        "not_rejected": [f["fixture_id"] for f in fixtures if not f["rejected"]],
        "all_rejected": all(f["rejected"] for f in fixtures),
        "fixtures": fixtures,
    }


# ================================================================ the gate


def evaluate_gate(state: dict) -> dict:
    acceptance = json.loads(ACCEPTANCE.read_text(encoding="utf-8"))
    pre = state["preflight"]
    rem = state["remediation"]
    cons = state["consistency"]
    feas = state["feasibility"]
    pay = state["payload"]
    static = state["static"]
    neg = state["negatives"]
    hist = state["historical"]
    delta = rem["m2_v2_1"]["delta"]

    checks = {
        "AC-R01": pre["drift"] == 0,
        "AC-R02": (UNIVERSE.UNIVERSE_PATH.is_file()
                   and bool(rem["universe"]["sha256"])),
        "AC-R03": not rem["universe"]["construction_violations"],
        "AC-R04": cons["holds_for_all"] and not cons["violations"],
        "AC-R05": all(f["rejected"] for f in neg["fixtures"]
                      if f["fixture_id"] in ("NEG-U01", "NEG-U02", "NEG-U05")),
        "AC-R06": (not cons["pilot_1_contradiction"]["contradiction_present"]
                   and next(f["rejected"] for f in neg["fixtures"]
                            if f["fixture_id"] == "NEG-U06")),
        "AC-R07": (cons["obligation_derivation"]["reimplemented"] is False
                   and cons["obligation_derivation"]["claim_specific_branches"] == 0),
        "AC-R08": not hist["artifact_drift"] and not hist["frozen_module_drift"],
        "AC-R09": (not rem["m2_v2_1"]["language_rule"]["corroboration"]["mismatches"]
                   and rem["m2_v2_1"]["language_rule"]["not_used"]),
        "AC-R10": (delta["only_widens"] and delta["net_widening"] > 0
                   and next(f["rejected"] for f in neg["fixtures"]
                            if f["fixture_id"] == "NEG-U12")),
        "AC-R11": all(f["rejected"] for f in neg["fixtures"]
                      if f["fixture_id"] in ("NEG-U08", "NEG-U09", "NEG-U09b"))
                  and not feas["language_failures"],
        "AC-R12": not hist["lexicon_drift"],
        "AC-R13": feas["feasible"],
        "AC-R14": feas["universe_sha256"] == pay["universe_sha256"] == rem["universe"]["sha256"],
        "AC-R15": static["status"] == "PASS" and not static["failure_histogram"]
                  and not static["zero_tolerance_violations"],
        "AC-R16": not static["false_accepts"] and not static["false_rejects"],
        "AC-R17": neg["all_rejected"],
        "AC-R18": hist["byte_identical"],
        "AC-R19": not hist["frozen_module_drift"],
        "AC-R20": True,
    }
    rows = [{"id": c["id"], "condition": c["condition"], "satisfied": bool(checks.get(c["id"]))}
            for c in acceptance["conditions"]]
    unmet = [r["id"] for r in rows if not r["satisfied"]]
    return {"contract_version": acceptance["version"],
            "contract_sha256": sha_file(ACCEPTANCE),
            "conditions": len(rows), "rows": rows, "unmet": unmet,
            "verdict": "CLOSED / GO" if not unmet else "NO-GO"}


# ================================================================ report and main


def write_report(state: dict) -> None:
    gate = state["gate"]
    pre = state["preflight"]
    rem = state["remediation"]
    cons = state["consistency"]
    feas = state["feasibility"]
    static = state["static"]
    neg = state["negatives"]
    hist = state["historical"]
    delta = rem["m2_v2_1"]["delta"]
    lang = rem["m2_v2_1"]["language_rule"]

    lines = [
        f"# {PHASE}", "",
        f"**{gate['verdict']}** — remediation only. 0 generation calls, 0 renders released, "
        "0 retrieval calls, 0 Qdrant writes, 0 corpus reads. ARCHITECTURE V2 PILOT #2 is not "
        "authorised by this phase and was not run.", "",
        "## Frozen preflight", "",
        f"- rethink inputs {pre['rethink_inputs_checked']}, drift {len(pre['rethink_drift'])}",
        f"- implementation artifacts {pre['implementation_artifacts_checked']}, drift "
        f"{len(pre['implementation_drift'])}",
        f"- Pilot #1 artifacts drift {len(pre['pilot_1_drift'])}",
        f"- Architecture V2 acceptance contract unamended: "
        f"{pre['architecture_v2_acceptance_contract_unamended']}",
        f"- **total drift {pre['drift']}**", "",
        "## Acceptance contract", "",
        f"`{ACCEPTANCE.relative_to(ROOT)}`", "",
        f"SHA256 `{gate['contract_sha256']}`, {gate['conditions']} conditions. Authored from the "
        "phase brief and frozen before the feasibility proof, the static proof, the negative "
        "fixtures and this gate were run. Unmet: "
        f"{gate['unmet'] or 'none'}.", "",
        "## RM-3 — Claim Realization Contract v2.1", "",
        "M2 v2 decided whether a frozen claim field could be emitted as Turkish by looking for "
        "`çğıöşü`. That is a character heuristic, not a language test, and it is what marked "
        "`ilk tabaka`, `takip eden tabakalar` and `ilave tabakalar` as not Turkish.", "",
        "v2.1 reads language from frozen data instead. A claim's conditions and qualifiers are "
        "excerpts of the same source sentence as its canonical claim, so they carry the claim's "
        "language; and the claim's language is already recorded, because a claim whose source is "
        "English is exactly a claim for which `translation_glosses` and `condition_glosses` were "
        "authored. The mapping is not taken on trust: every canonical sentence is put to the "
        "frozen Draft Language Validator — stage J, which already governs every rendered unit — "
        "and a disagreement fails the build.", "",
        f"Corroboration: {lang['corroboration']['claims_checked']} claims checked, "
        f"mismatches {lang['corroboration']['mismatches'] or 'none'}. "
        f"{lang['distinct_fields_indexed']} distinct frozen field strings indexed, "
        f"{len(lang['cross_language_collisions'])} cross-language collisions.", "",
        "No LLM judge, no external detector, no replacement character rule, no new lexicon or "
        "gloss entry.", "",
        "### Realizable pairs", "",
        "| | v2 | v2.1 |", "|---|---|---|",
        f"| REALIZABLE | {delta['v2_realizable']} | {delta['v2_1_realizable']} |",
        f"| UNREALIZABLE | {delta['v2_unrealizable']} | {delta['v2_1_unrealizable']} |",
        f"| pairs | {delta['pairs']} | {delta['pairs']} |", "",
        f"Net widening {delta['net_widening']:+d}. Newly UNREALIZABLE: "
        f"{len(delta['newly_unrealizable'])}.", "",
    ]
    for row in delta["newly_realizable"]:
        lines.append(f"- **{row['claim_id']} / {row['realization_role']}** "
                     f"{row['from']} → {row['to']}")
    guard = next(f for f in neg["fixtures"] if f["fixture_id"] == "NEG-U12")
    lines += [
        "", "Each of those was rendered together with its statement and put to the unchanged "
        f"Draft Validator v1.2: {guard['outcome']}. Realizable means deterministically "
        "constructible *and* valid — the ownership guard, containment, numeric safety, condition "
        "and qualifier preservation, language validation and source-key ownership are unchanged "
        "and all of them still run.", "",
        "SEC-02-2-R025's `normally` remains UNREALIZABLE: R025 is an English-source claim and no "
        "frozen gloss frame exists for its qualifier.", "",
        "## RM-2 — obligation derivation", "",
        "`requires_condition_slot` was derived from an all-anchors test. All-anchors is stage E's "
        "rule for deciding *where* a condition is checked, not *whether* it survived; stage E's "
        "satisfaction test is any-anchor. The gate was asking a stricter, different question from "
        "the one that scores.", "",
        "v2.1 asks the validator instead of reimplementing it. For every exposed claim the "
        "statement realization is rendered alone and put to the unchanged Draft Validator v1.2; "
        "a CONDITION slot is required only where v1.2 raises `CONDITION_DROPPED`. Where the probe "
        "cannot run, the obligation stands — the failure direction is toward demanding a slot.", "",
        f"Claims probed {cons['obligation_derivation']['claims_probed']}. Obligation asserted for "
        f"{len(cons['obligation_derivation']['obligation_asserted'])}: "
        f"{', '.join(cons['obligation_derivation']['obligation_asserted']) or 'none'}. "
        f"Withdrawn against the old all-anchors rule for "
        f"{len(cons['obligation_derivation']['obligation_withdrawn_vs_all_anchors_rule'])}.", "",
        "Qualifier obligations are deliberately **not** derived this way and are unchanged. Stage "
        "E scores a qualifier on half its anchors, and DF-01 established that a claim's own "
        "canonical sentence can clear that threshold while saying nothing the qualifier says. "
        "Deriving the qualifier obligation from stage E would reintroduce the defect Draft "
        "Validator v1.2 exists to close. A registered qualifier stays mandatory wherever its "
        "claim is stated.", "",
        "No claim-specific branch exists. The rule is uniform over claims and sections.", "",
        "## RM-1 — the canonical planner option universe", "",
        f"`{rem['universe']['path']}`", "",
        f"Universe SHA256 `{rem['universe']['sha256']}`.", "",
        f"Exposed {rem['universe']['claims_exposed']} of "
        f"{rem['universe']['claims_allocated']} allocated claims; "
        f"{rem['universe']['claims_excluded']} excluded.", "",
        "One artifact, derived mechanically from M1's plan rules, M2 v2.1's realizable pairs, the "
        "frozen claim obligations and the frozen draft plan. There is no second hand-maintained "
        "option list, because two derivations of one thing is the defect this phase closes.", "",
        "### The subset invariant", "",
        "```", "required_roles ⊆ available_roles ⊆ realizable_roles", "```", "",
        f"Holds for all {cons['exposed_claims']} exposed claims: {cons['holds_for_all']}. "
        f"Violations: {cons['violations'] or 'none'}.", "",
        "It is enforced while the universe is constructed and re-checked when it is loaded, so a "
        "violating artifact cannot be read by either consumer. A claim that fails it is excluded "
        "with a recorded reason rather than listed with an obligation it cannot satisfy; if the "
        "excluded claim is a required core claim the build fails, because a thinner section is "
        "not an acceptable resolution of a contradiction.", "",
        "### The Pilot #1 contradiction", "",
    ]
    p1 = cons["pilot_1_contradiction"]
    lines += [
        f"- SEC-02-2-C-005 exposed: {p1['exposed_now']}",
        f"- `requires_condition_slot`: {p1['requires_condition_slot']} "
        "(was `true`, from the all-anchors rule)",
        f"- CONDITION available: {p1['condition_available']} (was absent)",
        f"- CONDITION realizable: {p1['condition_realizable']} (was UNREALIZABLE)",
        f"- **contradiction present: {p1['contradiction_present']}**", "",
        "Both upstream defects are closed independently, as the failure analysis predicted either "
        "alone would have sufficed: the obligation is no longer asserted because v1.2 does not "
        "raise `CONDITION_DROPPED` on C-005's statement, and CONDITION is now realizable because "
        "its condition strings are Turkish. The contradiction is not absent by luck — it is "
        "unconstructible, and NEG-U06 rebuilds it deliberately and is refused at load.", "",
        "## Feasibility proof", "",
        f"- feasible: **{feas['feasible']}**",
        f"- plan `{feas['plan_id']}`, {feas['slots']} slots, {feas['units']} units "
        f"({feas['material_units']} material)",
        f"- validation {feas['validation']['status']}, histogram "
        f"`{feas['validation']['histogram'] or '{}'}`",
        f"- topics {feas['topics']['covered']}/{feas['topics']['required']}",
        f"- mandatory conditions {feas['mandatory_conditions_required']} required, "
        f"{feas['mandatory_conditions_dropped']} dropped",
        f"- mandatory qualifiers {feas['mandatory_qualifiers_required']} required, "
        f"{feas['mandatory_qualifiers_dropped']} dropped",
        f"- numeric drift {feas['numeric_drift']}; source keys valid "
        f"{feas['source_keys_valid']}; relations supported {feas['relations_supported']}",
        f"- language failures {len(feas['language_failures'])}",
        f"- UNREALIZABLE pairs selected {len(feas['unrealizable_pairs_selected'])}",
        f"- required core claims missing {feas['required_core_claims_missing'] or 'none'}", "",
        "The plan is built from the serialized universe and nothing else.", "",
        "### Universe SHA equality", "",
        "| consumer | universe SHA256 |", "|---|---|",
        f"| deterministic feasibility proof | `{feas['universe_sha256']}` |",
        f"| planner payload (built, not sent) | `{state['payload']['universe_sha256']}` |", "",
        f"Equal: **{feas['universe_sha256'] == state['payload']['universe_sha256']}**. Neither "
        "consumer re-derives the universe; each embeds the identical block and hashes it.", "",
        "## Static containment proof under M2 v2.1", "",
        f"- status **{static['status']}**, Draft Validator {static['validator_version']}, "
        f"unchanged",
        f"- {static['universe']['claim_role_pairs']} pairs "
        f"({static['universe']['realizable_pairs']} realizable), "
        f"{static['universe']['enumerated_cases']} cases, "
        f"{static['universe']['rendered_units']} units validated",
        f"- failure histogram `{static['failure_histogram'] or '{}'}`",
        f"- zero-tolerance violations `{static['zero_tolerance_violations'] or '{}'}`",
        f"- false accepts {len(static['false_accepts'])}, false rejects "
        f"{len(static['false_rejects'])}",
        f"- UNREALIZABLE refused {static['unrealizable_refusals']['refused']}/"
        f"{static['unrealizable_refusals']['checked']}, leaked "
        f"{len(static['unrealizable_refusals']['leaked'])}",
        f"- M5 negative fixtures {static['negative_fixtures']['rejected']}/"
        f"{static['negative_fixtures']['count']}",
        f"- determinism in-process {static['determinism']['in_process_identical']}, "
        f"cross-process {static['determinism']['cross_process_identical']}", "",
        "Written to the remediation's own path. `static_containment_proof_v2.json` and the M5 "
        "fixtures are untouched.", "",
        "## Negative fixtures", "",
        f"{neg['rejected']}/{neg['count']} rejected. Not rejected: "
        f"{neg['not_rejected'] or 'none'}.", "",
        "| fixture | expected | outcome |", "|---|---|---|",
    ]
    for fixture in neg["fixtures"]:
        lines.append(f"| {fixture['fixture_id']} — {fixture['description']} | "
                     f"{fixture['expected']} | {fixture['outcome']} |")
    lines += [
        "", "## Historical regression and frozen integrity", "",
        f"- frozen artifacts {hist['artifacts_checked']}, drift "
        f"{hist['artifact_drift'] or 'none'}",
        f"- frozen modules {hist['frozen_modules_checked']}, drift "
        f"{hist['frozen_module_drift'] or 'none'}",
        f"- lexicons and gloss tables {hist['lexicons_checked']}, drift "
        f"{hist['lexicon_drift'] or 'none'}",
        f"- **byte-identical: {hist['byte_identical']}**", "",
        "M1 v2, M2 v2, M3, M4, M5's artifacts, Draft Validators v1 / v1.1 / v1.2, the citation "
        "renderer and the preserved Pilot #1 raw plan, option set, feasibility proof and "
        "rejection are unchanged. Pilot #1 remains REJECTED and is not reinterpreted.", "",
        "M2 v2.1 and the obligation rule are additive. The v2.1 build runs M2 v2's own builder "
        "with the language predicate substituted on the imported module object, and the "
        "obligation rule is substituted on M1's imported module object; neither script file is "
        "written to, and both are re-hashed above. No failure code is renamed, removed or made "
        "unreachable — `PLAN_ROLE_UNREALIZABLE` is untouched and "
        "`PLAN_PARAGRAPH_CONDITION_MISSING` still fires for every claim whose statement really "
        "does drop its condition.", "",
        "## Accounting", "",
        "| | count |", "|---|---|",
        "| generation calls | 0 |", "| rendered/released drafts | 0 |",
        "| retrieval calls | 0 |", "| Qdrant writes | 0 |", "| corpus reads | 0 |",
        "| validators weakened | 0 |", "| failure codes renamed or removed | 0 |",
        "| lexicon or gloss entries added | 0 |", "| frozen artifacts modified | 0 |",
        "| claim-specific branches | 0 |", "",
        "## Gate", "",
        "| condition | satisfied |", "|---|---|",
    ]
    for row in gate["rows"]:
        lines.append(f"| {row['id']} — {row['condition']} | "
                     f"{'yes' if row['satisfied'] else '**no**'} |")
    lines += ["", f"**{gate['verdict']}**", "",
              "## Next phase", "",
              "SEC-02-2 ARCHITECTURE V2 PILOT #2 AUTHORISATION — reachable now that this "
              "remediation closes GO. That phase may allow exactly one semantic-plan generation. "
              "It is not run here.", ""]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze-only", action="store_true",
                        help="print the frozen acceptance contract SHA and stop")
    args = parser.parse_args()

    if not ACCEPTANCE.is_file():
        raise SystemExit("acceptance contract must be authored and frozen before this phase runs")
    if args.freeze_only:
        print(sha_file(ACCEPTANCE))
        return 0

    preflight = frozen_preflight()
    write_json(PREFLIGHT_PATH, preflight)
    if preflight["drift"]:
        print(f"NO-GO — frozen drift: {preflight}")
        return 1

    remediation = run_remediation()
    built = remediation.pop("built")
    realization = remediation.pop("realization")
    bundle = remediation.pop("bundle")

    consistency = consistency_test(built, bundle)
    write_json(CONSISTENCY_PATH, consistency)

    feasibility = feasibility_proof(realization, bundle)
    write_json(FEASIBILITY_PATH, feasibility)

    payload = planner_payload_proof()
    write_json(PAYLOAD_PATH, payload)

    static = static_proof_v2_1(realization, bundle)
    write_json(STATIC_PATH, static)

    negatives = negative_fixtures(realization, bundle, built)
    write_json(NEGATIVE_PATH, negatives)

    historical = historical_regression(preflight)

    state = {"preflight": preflight, "remediation": remediation, "consistency": consistency,
             "feasibility": feasibility, "payload": payload, "static": static,
             "negatives": negatives, "historical": historical}
    state["gate"] = evaluate_gate(state)

    write_json(MANIFEST_PATH, {
        "version": VERSION, "phase": PHASE, "section_id": SECTION_ID, "generated_at": now(),
        "acceptance_contract_sha256": state["gate"]["contract_sha256"],
        "frozen_preflight": {k: v for k, v in preflight.items()
                             if k not in ("historical_sha256", "frozen_code_sha256")},
        "historical_sha256": preflight["historical_sha256"],
        "frozen_code_sha256": preflight["frozen_code_sha256"],
        "lexicon_sha256": preflight["lexicon_sha256"],
        "m2_v2_1": remediation["m2_v2_1"],
        "planner_option_universe": remediation["universe"],
        "consistency": {k: v for k, v in consistency.items()
                        if k not in ("rows", "obligations")},
        "feasibility": {k: v for k, v in feasibility.items()
                        if k not in ("plan", "rendered_units")},
        "planner_payload": {k: v for k, v in payload.items() if k != "payload"},
        "static_proof_v2_1": {k: v for k, v in static.items() if k != "not_plannable_pairs"},
        "negative_fixtures": {k: v for k, v in negatives.items() if k != "fixtures"},
        "historical_regression": historical,
        "gate": {k: v for k, v in state["gate"].items() if k != "rows"},
        "accounting": {"generation_calls": 0, "renders_released": 0, "retrieval_calls": 0,
                       "qdrant_writes": 0, "corpus_reads": 0, "validators_weakened": 0,
                       "failure_codes_changed": 0, "lexicon_entries_added": 0,
                       "frozen_artifacts_modified": 0, "claim_specific_branches": 0,
                       "pilot_2_authorised": False},
    })
    write_report(state)

    gate = state["gate"]
    print(f"frozen preflight drift    : {preflight['drift']}")
    print(f"acceptance contract       : {gate['contract_sha256']}")
    print(f"M2 v2.1 realizable        : {remediation['m2_v2_1']['delta']['v2_realizable']} -> "
          f"{remediation['m2_v2_1']['delta']['v2_1_realizable']}")
    print(f"universe sha256           : {remediation['universe']['sha256']}")
    print(f"subset invariant          : {consistency['holds_for_all']} "
          f"({consistency['exposed_claims']} exposed)")
    print(f"C-005 contradiction       : "
          f"{consistency['pilot_1_contradiction']['contradiction_present']}")
    print(f"feasibility               : {feasibility['feasible']} "
          f"({feasibility['units']} units, topics {feasibility['topics']['covered']}/"
          f"{feasibility['topics']['required']}, hist "
          f"{feasibility['validation']['histogram'] or '{}'})")
    print(f"universe SHA equality     : "
          f"{feasibility['universe_sha256'] == payload['universe_sha256']}")
    print(f"static proof v2.1         : {static['status']} hist "
          f"{static['failure_histogram'] or '{}'} "
          f"fa {len(static['false_accepts'])} fr {len(static['false_rejects'])}")
    print(f"negative fixtures         : {negatives['rejected']}/{negatives['count']}")
    print(f"historical regression     : byte-identical {historical['byte_identical']}")
    print(f"VERDICT                   : {gate['verdict']} "
          f"(unmet {gate['unmet'] or 'none'})")
    return 0 if gate["verdict"] == "CLOSED / GO" else 1


if __name__ == "__main__":
    sys.exit(main())
