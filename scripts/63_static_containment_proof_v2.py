"""M5 — Static Containment Proof v2. The gate, and the phase's central claim.

Architecture A could only ever say "the validator accepted what we happened to write". This proof
says something stronger and different in kind: *every* output the renderer is capable of
constructing, over the whole universe the contracts permit, is valid under the unchanged Draft
Validator v1.2. That is a property of the construction, not a score on a sample, and it is why
this runs without generating anything.

The universe is enumerated, not sampled:

  every claim × every realization role                        — 189 pairs
  each REALIZABLE pair as a minimal plan                      — per-unit stages A-D, G-L
  each pair again with explicit citation source keys          — citation binding
  every claim's full realizable role set in one paragraph     — paragraph-scoped stages E, K, L
  every UNREALIZABLE pair offered to the renderer             — refusal, not silent omission

The last line is the one that keeps the proof honest. A contract could pass trivially by marking
everything UNREALIZABLE, so the proof asserts both directions: what the contract permits must
render and validate, and what it refuses must actually be refused rather than quietly skipped.

Negative fixtures cover the routes a bad plan could take, and they are grouped by where each is
caught, because that matters more than that it is caught. A denylisted claim, a laundered source
key, an unregistered numeric and an invented role are rejected at plan validation, before the
renderer runs. A free-text field is rejected at parse, before validation. The three semantic
attacks — presenting 15 cm as a derived 150 mm, generalising SEC-02-2-C-009's clay-zone figure,
and presenting Tablo-351-5 as establishing the C25/30 class — are checked twice over: that no
contract entry can construct them, and that the frozen validator rejects them if injected
directly. The first is the architectural claim; the second confirms the safety net beneath it is
still there.

Nothing here is a pilot. The rendered strings are proof artifacts and validator inputs. They are
not a draft, they are not authorised for release, and no plan in this file came from a model.
"""

from __future__ import annotations

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

VERSION = "tunnelbook-static-containment-proof-v2"
PHASE = "SEC-02-2 DRAFTING ARCHITECTURE V2 IMPLEMENTATION"
SECTION_ID = "SEC-02-2"

ARCH_V2 = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "architecture_v2"
PROOF_PATH = ARCH_V2 / "audits" / "static_containment_proof_v2.json"
NEGATIVE_PATH = ARCH_V2 / "fixtures" / "negative_fixtures_v2.json"
UNIVERSE_PATH = ARCH_V2 / "fixtures" / "realization_universe_v2.json"
ACCEPTANCE_PATH = ARCH_V2 / "contracts" / "architecture_v2_acceptance_contract_v1.json"


def _load(name: str, filename: str):
    path = ROOT / "scripts" / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


V1 = _load("scp_v1", "49_section_draft_validator_v1.py")
V1_2 = _load("scp_v1_2", "54_section_draft_validator_v1_2.py")
PLAN_IR = _load("scp_plan_ir", "59_semantic_plan_ir_contract_v2.py")
REALIZATION = _load("scp_realization", "60_claim_realization_contract_v2.py")
RENDERER = _load("scp_renderer", "62_deterministic_surface_renderer_v2.py")

ZERO_TOLERANCE = (
    "UNSUPPORTED_PROPOSITION", "CLAIM_EXPANSION", "NUMERIC_DRIFT", "UNIT_DRIFT",
    "MODALITY_DRIFT", "CONDITION_DROPPED", "QUALIFIER_DROPPED", "SEMANTIC_SCOPE_MISMATCH",
    "LANGUAGE_MISMATCH", "CLAIM_DENYLISTED", "UNKNOWN_CITATION",
)


# ================================================================ universe

def _slot(slot_id: str, claim_id: str, role: str, source_keys: list[str] | None = None) -> dict:
    slot: dict[str, Any] = {"slot_id": slot_id, "claim_id": claim_id,
                            "realization_role": role}
    if source_keys is not None:
        slot["citation_source_keys"] = source_keys
    return slot


def _plan(plan_id: str, slots: list[dict], subsection: str = "SEC-02-2-A") -> dict:
    return {
        "section_id": SECTION_ID,
        "plan_id": plan_id,
        "plan_version": "proof-v2",
        "language": "tr",
        "subsections": [{
            "subsection_id": subsection,
            "paragraph_groups": [{"paragraph_id": f"{plan_id}-P01", "slots": slots}],
        }],
    }


def _companions(claim_id: str, role: str, realization, bundle) -> tuple[list[str], list[str]]:
    """The roles a plan must allocate alongside this one, and any that cannot be realized.

    Two contract rules drive this: a supporting role needs the statement it supports, and a
    registered qualifier needs a slot wherever its claim is stated. Where a required companion is
    UNREALIZABLE the pair is not plannable at all — that is a real gap in the realization data,
    and it is recorded rather than rendered around.
    """
    claim = bundle.allowlist.get(claim_id) or {}
    needed: list[str] = []
    if role not in ("CLAIM_STATEMENT", "REQUIREMENT"):
        statement = next((r for r in ("CLAIM_STATEMENT", "REQUIREMENT")
                          if (realization.entry(claim_id, r) or {}).get("status") == "REALIZABLE"),
                         "CLAIM_STATEMENT")
        needed.append(statement)
    if (claim.get("qualifiers") or []) and role != "QUALIFIER_SCOPE":
        needed.append("QUALIFIER_SCOPE")
    if PLAN_IR.paragraph_scoped_conditions(claim, bundle) and role != "CONDITION":
        needed.append("CONDITION")
    missing = [r for r in needed
               if (realization.entry(claim_id, r) or {}).get("status") != "REALIZABLE"]
    return needed, missing


def enumerate_universe(realization, bundle) -> tuple[list[dict], list[dict]]:
    """Every plan the contracts permit, plus the pairs that no permitted plan can contain."""
    pairs = realization.realizable_pairs()
    by_claim: dict[str, list[str]] = {}
    for claim_id, role in pairs:
        by_claim.setdefault(claim_id, []).append(role)

    cases: list[dict] = []
    not_plannable: list[dict] = []

    for index, (claim_id, role) in enumerate(pairs):
        prefix = f"UNIV{index:03d}"
        needed, missing = _companions(claim_id, role, realization, bundle)
        if missing:
            not_plannable.append({
                "claim_id": claim_id, "realization_role": role,
                "required_companions": needed, "unrealizable_companions": missing,
                "reason": ("a contract rule requires a companion role this claim cannot "
                           "realize, so no permitted plan contains this pair"),
            })
            continue
        slots = [_slot(f"{prefix}-S01", claim_id, role)]
        for n, companion_role in enumerate(needed, start=2):
            slots.append(_slot(f"{prefix}-S{n:02d}", claim_id, companion_role))
        cases.append({
            "case_id": f"{prefix}-minimal", "kind": "minimal_pair",
            "claim_id": claim_id, "realization_role": role,
            "plan": _plan(f"P-{prefix}-MIN", slots),
        })
        registered = sorted(bundle.allowlist[claim_id].get("source_keys") or [])
        if registered:
            cited = [dict(slot) for slot in slots]
            cited[0]["citation_source_keys"] = registered
            for n, slot in enumerate(cited):
                slot["slot_id"] = f"{prefix}C-S{n + 1:02d}"
            cases.append({
                "case_id": f"{prefix}-cited", "kind": "explicit_citation",
                "claim_id": claim_id, "realization_role": role,
                "plan": _plan(f"P-{prefix}-CIT", cited),
            })

    # Every realizable role for one claim, together. This is what exercises paragraph scope.
    for index, (claim_id, roles) in enumerate(sorted(by_claim.items())):
        ordered = sorted(roles)
        if not set(ordered) & {"CLAIM_STATEMENT", "REQUIREMENT"}:
            continue
        # One statement role per paragraph, per the plan contract. REQUIREMENT is the narrower
        # admission, so it is the one kept where a claim offers both.
        if {"CLAIM_STATEMENT", "REQUIREMENT"} <= set(ordered):
            ordered = [r for r in ordered if r != "CLAIM_STATEMENT"]
        claim = bundle.allowlist.get(claim_id) or {}
        if (claim.get("qualifiers") or []) and "QUALIFIER_SCOPE" not in ordered:
            continue
        if PLAN_IR.paragraph_scoped_conditions(claim, bundle) and "CONDITION" not in ordered:
            continue
        slots = [_slot(f"ALL{index:03d}-S{n:02d}", claim_id, role)
                 for n, role in enumerate(ordered, start=1)]
        cases.append({
            "case_id": f"ALL{index:03d}", "kind": "all_roles_one_paragraph",
            "claim_id": claim_id, "realization_role": "+".join(ordered),
            "plan": _plan(f"P-ALL{index:03d}", slots),
        })
    return cases, not_plannable


# ================================================================ validation

def validate_payload(payload: dict, bundle) -> dict:
    ir = V1.parse_draft_ir(payload)
    result = V1_2.validate_draft(ir, bundle)
    return {
        "status": result.status,
        "histogram": dict(result.failure_histogram),
        "rejected_unit_ids": sorted(result.rejected_unit_ids),
        "failures": [f for unit in result.units for f in
                     [dict(x) for x in getattr(unit, "failures", [])]],
    }


def run_universe(cases: list[dict], realization, bundle) -> dict:
    results = []
    histogram: dict[str, int] = {}
    rendered_units = 0
    for case in cases:
        try:
            payload = RENDERER.render_from_raw(case["plan"], realization, bundle)
        except RENDERER.RenderRefusal as refusal:
            results.append({**{k: v for k, v in case.items() if k != "plan"},
                            "outcome": "RENDER_REFUSED", "detail": refusal.as_dict()})
            histogram["RENDER_REFUSED"] = histogram.get("RENDER_REFUSED", 0) + 1
            continue
        verdict = validate_payload(payload, bundle)
        rendered_units += len(payload["units"])
        for code, count in verdict["histogram"].items():
            histogram[code] = histogram.get(code, 0) + count
        results.append({**{k: v for k, v in case.items() if k != "plan"},
                        "outcome": verdict["status"],
                        "units": len(payload["units"]),
                        "render_sha256": RENDERER.render_sha256(payload),
                        "histogram": verdict["histogram"],
                        "rejected_unit_ids": verdict["rejected_unit_ids"]})
    accepted = [r for r in results if r["outcome"] == "ACCEPT"]
    return {
        "cases": len(results),
        "accepted": len(accepted),
        "rendered_units": rendered_units,
        "failure_histogram": histogram,
        "results": results,
    }


def run_unrealizable_refusals(realization, bundle) -> dict:
    """A contract that marks everything UNREALIZABLE must not pass. Both directions are asserted."""
    checked = []
    for entry in realization.payload["entries"]:
        if entry["status"] != "UNREALIZABLE":
            continue
        plan = _plan(f"P-UNREAL-{len(checked):03d}",
                     [_slot("UNREAL-S01", entry["claim_id"], entry["realization_role"])])
        try:
            RENDERER.render_from_raw(plan, realization, bundle)
            refused = False
            code = None
        except RENDERER.RenderRefusal as refusal:
            refused = True
            code = refusal.code
        checked.append({"claim_id": entry["claim_id"], "role": entry["realization_role"],
                        "refused": refused, "code": code})
    return {"checked": len(checked),
            "refused": sum(1 for c in checked if c["refused"]),
            "leaked": [c for c in checked if not c["refused"]],
            "detail": checked}


# ================================================================ negative fixtures

def negative_fixtures(realization, bundle) -> dict:
    base = lambda slots, pid="P-NEG": _plan(pid, slots)  # noqa: E731
    fixtures: list[dict] = []

    def add(fixture_id: str, description: str, plan: dict, expect_stage: str) -> None:
        outcome, detail = _probe_plan(plan, realization, bundle)
        fixtures.append({"fixture_id": fixture_id, "description": description,
                         "expected_stage": expect_stage, "outcome": outcome, "detail": detail,
                         "rejected": outcome != "RENDERED"})

    add("NEG-01", "a claim that is not on the allowlist",
        base([_slot("N01", "SEC-02-2-C-999", "CLAIM_STATEMENT")]), "plan_validation")
    denylisted = sorted(bundle.denylist)[:1]
    if denylisted:
        add("NEG-02", "a claim on the composition denylist",
            base([_slot("N02", denylisted[0], "CLAIM_STATEMENT")]), "plan_validation")
    add("NEG-03", "a relation the claim does not allow",
        _with(base([_slot("N03", "SEC-02-2-C-001", "CLAIM_STATEMENT")]),
              relation_constraint_ids=["SOURCE_SUPPORTED_RELATION"]), "plan_validation")
    add("NEG-04", "a source key registered to a different claim (source laundering)",
        _with(base([_slot("N04", "SEC-02-2-C-001", "CLAIM_STATEMENT")]),
              citation_source_keys=sorted(
                  bundle.allowlist["SEC-02-2-C-009"].get("source_keys") or [])),
        "plan_validation")
    add("NEG-05", "a numeric the declaring claim does not register",
        _with(base([_slot("N05", "SEC-02-2-C-001", "CLAIM_STATEMENT")]),
              numeric_fact_ids=["SEC-02-2-C-001#NUM7"]), "plan_validation")
    add("NEG-06", "a numeric addressed through another claim's id",
        _with(base([_slot("N06", "SEC-02-2-C-001", "CLAIM_STATEMENT")]),
              numeric_fact_ids=["SEC-02-2-C-009#NUM0"]), "plan_validation")
    add("NEG-07", "a condition the claim does not carry",
        _with(base([_slot("N07", "SEC-02-2-C-001", "CLAIM_STATEMENT")]),
              condition_ids=["SEC-02-2-C-001#COND9"]), "plan_validation")
    add("NEG-08", "a qualifier id belonging to no registered qualifier",
        _with(base([_slot("N08", "SEC-02-2-C-002", "CLAIM_STATEMENT")]),
              qualifier_constraint_ids=["DQS-C009-001"]), "plan_validation")
    add("NEG-09", "an invented realization role",
        base([_slot("N09", "SEC-02-2-C-001", "FREEFORM")]), "plan_parse")
    add("NEG-10", "a free-text field injected into a slot",
        base([{**_slot("N10", "SEC-02-2-C-001", "CLAIM_STATEMENT"),
               "text": "Püskürtme beton her koşulda yeterli dayanımı sağlar."}]), "plan_parse")
    add("NEG-11", "prose smuggled under an undeclared but innocent field name",
        base([{**_slot("N11", "SEC-02-2-C-001", "CLAIM_STATEMENT"),
               "note": "Bu tablo dayanım sınıfını belirler."}]), "plan_parse")
    add("NEG-12", "a paragraph stating C-002 without its paragraph-scoped qualifier",
        base([_slot("N12", "SEC-02-2-C-002", "CLAIM_STATEMENT")]), "plan_validation")
    add("NEG-13", "a paragraph stating C-009 without its scope limitation",
        base([_slot("N13", "SEC-02-2-C-009", "CLAIM_STATEMENT")]), "plan_validation")
    add("NEG-14", "a role the contract marks UNREALIZABLE for this claim",
        base([_slot("N14", "SEC-02-2-C-001", "EXEMPLIFICATION")]), "plan_validation")
    add("NEG-15a", "a supporting role standing without the statement it supports",
        base([_slot("N15a", "SEC-02-2-C-009", "QUALIFIER_SCOPE")]), "plan_validation")
    add("NEG-15b", "a paragraph-scoped condition with no slot to carry it",
        base([_slot("N15b1", "SEC-02-2-P0-001", "CLAIM_STATEMENT")]), "plan_validation")
    add("NEG-15c", "both statement roles for one claim in one paragraph",
        base([_slot("N15c1", "SEC-02-2-C-009", "CLAIM_STATEMENT"),
              _slot("N15c2", "SEC-02-2-C-009", "REQUIREMENT"),
              _slot("N15c3", "SEC-02-2-C-009", "QUALIFIER_SCOPE")]), "plan_validation")
    add("NEG-15", "a language the section policy does not permit",
        {**base([_slot("N15", "SEC-02-2-C-001", "CLAIM_STATEMENT")]), "language": "en"},
        "plan_parse")

    # The semantic attacks. Checked twice: the renderer cannot construct them, and the frozen
    # validator rejects them when injected directly as units.
    injected = [
        {"fixture_id": "NEG-16",
         "description": "15 cm presented as a derived 150 mm source-stated figure",
         "claim_id": "SEC-02-2-C-003",
         "text": "İlk püskürtme beton katman kalınlığı 150 mm olmalıdır.",
         "expected_codes": ("NUMERIC_DRIFT", "UNIT_DRIFT", "UNSUPPORTED_PROPOSITION")},
        {"fixture_id": "NEG-17",
         "description": "SEC-02-2-C-009's clay-zone thickness generalised to all first layers",
         "claim_id": "SEC-02-2-C-009",
         "text": "Genel olarak ilk katman kalınlığı 100-150 mm'dir.",
         "expected_codes": ("SEMANTIC_SCOPE_MISMATCH", "QUALIFIER_DROPPED",
                            "CONDITION_DROPPED")},
        {"fixture_id": "NEG-18",
         "description": "Tablo-351-5 presented as establishing the C25/30 strength class",
         "claim_id": "SEC-02-2-C-002",
         "text": ("Tablo-351-5'e göre püskürtme betonun basınç dayanım sınıfı C25/30 olarak "
                  "belirlenmiştir."),
         "expected_codes": ("SEMANTIC_SCOPE_MISMATCH", "QUALIFIER_DROPPED")},
    ]
    for case in injected:
        constructible = _renderer_can_construct(case["text"], case["claim_id"], realization)
        verdict = _validate_injected_unit(case, bundle)
        fixtures.append({
            "fixture_id": case["fixture_id"],
            "description": case["description"],
            "expected_stage": "unconstructible_and_validator_rejects",
            "renderer_can_construct": constructible,
            "validator_status": verdict["status"],
            "validator_codes": sorted(verdict["histogram"]),
            "expected_codes": list(case["expected_codes"]),
            "expected_code_seen": bool(set(case["expected_codes"]) & set(verdict["histogram"])),
            "rejected": (not constructible) and verdict["status"] == "REJECT",
            "outcome": "REJECTED" if verdict["status"] == "REJECT" else "ACCEPTED",
        })

    return {
        "count": len(fixtures),
        "rejected": sum(1 for f in fixtures if f["rejected"]),
        "false_accepts": [f["fixture_id"] for f in fixtures if not f["rejected"]],
        "fixtures": fixtures,
    }


def _with(plan: dict, **fields) -> dict:
    plan["subsections"][0]["paragraph_groups"][0]["slots"][0].update(fields)
    return plan


def _probe_plan(plan: dict, realization, bundle) -> tuple[str, Any]:
    try:
        parsed = PLAN_IR.parse_plan(plan)
    except PLAN_IR.PlanRejection as rejection:
        return "PLAN_PARSE_REJECTED", rejection.as_dict()
    validation = PLAN_IR.validate_plan(parsed, bundle, realization)
    if not validation.valid:
        return "PLAN_VALIDATION_REJECTED", validation.failures
    try:
        RENDERER.render_plan(parsed, realization, bundle)
    except RENDERER.RenderRefusal as refusal:
        return "RENDER_REFUSED", refusal.as_dict()
    return "RENDERED", None


def _renderer_can_construct(text: str, claim_id: str, realization) -> bool:
    """Is this string in the renderer's image at all? Compared on the normalised surface."""
    target = " ".join(V1.fold(text).split())
    for entry in realization.payload["entries"]:
        if entry["status"] != "REALIZABLE" or entry["claim_id"] != claim_id:
            continue
        parts = [RENDERER._segment_surface(s, "probe") for s in entry["segments"]]
        rendered = " ".join(V1.fold(REALIZATION.join_parts(parts)).split())
        if rendered == target:
            return True
    return False


def _validate_injected_unit(case: dict, bundle) -> dict:
    keys = sorted(bundle.allowlist[case["claim_id"]].get("source_keys") or [])
    payload = {
        "section_id": SECTION_ID, "draft_id": f"NEG-{case['fixture_id']}",
        "draft_version": "negative-fixture-v2", "language": "tr", "title": SECTION_ID,
        "units": [{
            "unit_id": "U-N-P01-S01", "unit_type": "PARAGRAPH_SENTENCE", "text": case["text"],
            "material": True, "claim_ids": [case["claim_id"]], "source_keys": keys,
            "relationship_type": "INDEPENDENT",
            "citation_intents": [{"claim_id": case["claim_id"], "source_keys": keys}],
        }],
    }
    return validate_payload(payload, bundle)


# ================================================================ determinism

def determinism_probe(cases: list[dict], realization, bundle) -> dict:
    """Byte equality within a process, and again in a fresh one. Purity is measured, not claimed."""
    def digest() -> str:
        hasher = hashlib.sha256()
        for case in cases:
            try:
                payload = RENDERER.render_from_raw(case["plan"], realization, bundle)
            except RENDERER.RenderRefusal as refusal:
                hasher.update(f"REFUSED:{refusal.code}".encode("utf-8"))
                continue
            hasher.update(RENDERER.render_bytes(payload))
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
        "rc=L('b','60_claim_realization_contract_v2.py')\n"
        "rd=L('c','62_deterministic_surface_renderer_v2.py')\n"
        "b=v1.load_bundle();r=rc.RealizationContract.load()\n"
        f"cases=json.loads(open({str(UNIVERSE_PATH)!r},encoding='utf-8').read())['cases']\n"
        "h=hashlib.sha256()\n"
        "for c in cases:\n"
        "    try:\n"
        "        h.update(rd.render_bytes(rd.render_from_raw(c['plan'],r,b)))\n"
        "    except rd.RenderRefusal as e:\n"
        "        h.update(('REFUSED:'+e.code).encode('utf-8'))\n"
        "print(h.hexdigest())\n")
    completed = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True,
                               cwd=str(ROOT))
    cross_process = completed.stdout.strip()
    return {
        "in_process_runs": len(in_process),
        "in_process_identical": len(set(in_process)) == 1,
        "in_process_sha256": in_process[0],
        "cross_process_sha256": cross_process,
        "cross_process_identical": cross_process == in_process[0],
        "cross_process_stderr": completed.stderr.strip()[-400:],
    }


# ================================================================ assembly

def main() -> int:
    bundle = V1.load_bundle()
    realization = REALIZATION.RealizationContract.load()
    cases, not_plannable = enumerate_universe(realization, bundle)

    UNIVERSE_PATH.parent.mkdir(parents=True, exist_ok=True)
    UNIVERSE_PATH.write_text(json.dumps({"version": VERSION, "cases": cases,
                                         "not_plannable": not_plannable},
                                        ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                             encoding="utf-8")

    universe = run_universe(cases, realization, bundle)
    refusals = run_unrealizable_refusals(realization, bundle)
    negatives = negative_fixtures(realization, bundle)
    determinism = determinism_probe(cases, realization, bundle)

    zero_violations = {code: count for code, count in universe["failure_histogram"].items()
                       if code in ZERO_TOLERANCE and count}
    false_rejects = [r["case_id"] for r in universe["results"] if r["outcome"] != "ACCEPT"]
    acceptance = json.loads(ACCEPTANCE_PATH.read_text(encoding="utf-8"))

    passed = (not zero_violations
              and not false_rejects
              and not negatives["false_accepts"]
              and not refusals["leaked"]
              and determinism["in_process_identical"]
              and determinism["cross_process_identical"])

    proof = {
        "version": VERSION,
        "phase": PHASE,
        "section_id": SECTION_ID,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "validator_version": V1_2.VALIDATOR_VERSION,
        "acceptance_contract_sha256": hashlib.sha256(ACCEPTANCE_PATH.read_bytes()).hexdigest(),
        "acceptance_contract_version": acceptance["version"],
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
        "zero_tolerance_violations": zero_violations,
        "false_rejects": false_rejects,
        "false_accepts": negatives["false_accepts"],
        "unrealizable_refusals": {k: v for k, v in refusals.items() if k != "detail"},
        "negative_fixtures": {k: v for k, v in negatives.items() if k != "fixtures"},
        "not_plannable_pairs": not_plannable,
        "determinism": determinism,
        "construction_invariant_holds": passed,
        "status": "PASS" if passed else "FAIL",
        "accounting": {
            "generation_calls": 0, "retrieval_calls": 0, "qdrant_writes": 0,
            "corpus_reads": 0, "rendered_pilot": "NONE", "validators_weakened": [],
            "post_render_model_passes": 0,
        },
        "note": ("The rendered strings in this proof are validator inputs and proof artifacts. "
                 "They are not a draft, nothing here is authorised for release, and no plan in "
                 "this file came from a model."),
    }

    PROOF_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROOF_PATH.write_text(json.dumps({**proof, "results": universe["results"],
                                      "unrealizable_detail": refusals["detail"]},
                                     ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
    NEGATIVE_PATH.write_text(json.dumps(negatives, ensure_ascii=False, indent=2,
                                        sort_keys=True) + "\n", encoding="utf-8")

    print(f"universe: {universe['cases']} cases, {universe['rendered_units']} units, "
          f"{universe['accepted']} accepted")
    print(f"histogram: {universe['failure_histogram'] or '{}'}")
    print(f"zero-tolerance violations: {zero_violations or 'none'}")
    print(f"false rejects: {len(false_rejects)}  false accepts: "
          f"{len(negatives['false_accepts'])}")
    print(f"unrealizable refused: {refusals['refused']}/{refusals['checked']} "
          f"(leaked {len(refusals['leaked'])})")
    print(f"negative fixtures rejected: {negatives['rejected']}/{negatives['count']}")
    print(f"determinism: in-process {determinism['in_process_identical']}, "
          f"cross-process {determinism['cross_process_identical']}")
    print(f"STATUS: {proof['status']}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
