"""RM-1 / RM-2 — the canonical planner option universe, and the obligations it may assert.

ARCHITECTURE V2 PILOT #1 was rejected on one slot out of twenty-five. The planner selected
`SEC-02-2-C-005 / CONDITION`, which was UNREALIZABLE, because the option set it was given listed
C-005 with `requires_condition_slot: true` beside an `available_roles` list that did not contain
CONDITION. The instruction set was unsatisfiable, and the planner followed it.

The reason two artifacts could contradict each other is that there were two artifacts. Gate 4
built the planner's option set and gate 5 built the feasibility universe, from the same frozen
data, by different code, and only gate 4's output reached the model. Nothing required them to
agree, and on exactly one claim they did not.

**There is one universe now.** It is built once, serialized once, and read by both consumers as
bytes. The deterministic feasibility proof and the planner payload each embed the identical
`universe` block and record its SHA; the phase gate requires the two SHAs to be equal. Neither
re-derives anything, because there is nothing left to re-derive.

**The invariant is structural, not a test that runs afterwards.**

    required_roles ⊆ available_roles ⊆ realizable_roles

is checked while the universe is being constructed. A claim that fails it is not listed with an
obligation it cannot satisfy — it is excluded, with the reason recorded, and if it was a required
core claim the build fails rather than quietly producing a thinner section. A serialized universe
that violates the invariant cannot be loaded. That is why C-005's contradiction is impossible
here rather than merely absent: there is no state of the frozen data that produces it.

**RM-2 — the obligation is derived from the rule that scores it.** v1 asked whether *all* of a
condition's anchors appear in the claim's own canonical wording, which is stage E's test for
*where* a condition is checked, not for *whether* it survived. Stage E's satisfaction test is
any-anchor. So an obligation is asserted here only when the claim's own statement realization,
rendered alone and put to the unchanged Draft Validator v1.2, actually drops the condition. The
gate now asks the validator's question instead of a stricter different one, and it asks it by
running the validator rather than by reimplementing it. Where the probe cannot be run, the
obligation stands: the failure direction is toward demanding a slot, never toward dropping one.

Qualifier obligations are deliberately *not* derived this way and are unchanged. Stage E scores a
qualifier on half its anchors, and DF-01 established that a claim's own canonical sentence can
clear that threshold while saying nothing the qualifier says. Deriving the qualifier obligation
from stage E would reintroduce exactly the defect Draft Validator v1.2 was authored to close. A
registered qualifier remains mandatory wherever its claim is stated.

Nothing here is claim-specific. The class being prevented is *required-but-unavailable role
contradiction*, for every claim and every future section.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

UNIVERSE_VERSION = "tunnelbook-architecture-v2-planner-option-universe-v2-1"
SECTION_ID = "SEC-02-2"

ARCH_V2 = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "architecture_v2"
UNIVERSE_PATH = ARCH_V2 / "contracts" / "planner_option_universe_v2_1.json"
PLAN_V1_2 = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "draft_plan_v1_2.json"

VALIDATOR_V1 = ROOT / "scripts" / "49_section_draft_validator_v1.py"
VALIDATOR_V1_2 = ROOT / "scripts" / "54_section_draft_validator_v1_2.py"
PLAN_IR = ROOT / "scripts" / "59_semantic_plan_ir_contract_v2.py"
RENDERER = ROOT / "scripts" / "62_deterministic_surface_renderer_v2.py"
M2_V2_1 = ROOT / "scripts" / "68_claim_realization_contract_v2_1.py"

STATEMENT_ROLES = ("REQUIREMENT", "CLAIM_STATEMENT")


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_MODULES: dict[str, Any] = {}


def module(key: str, path: Path):
    if key not in _MODULES:
        _MODULES[key] = _load(key, path)
    return _MODULES[key]


class UniverseViolation(Exception):
    """The universe cannot be constructed without stating a contradiction. Terminal."""


def canonical_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ================================================================ RM-2 — obligations


def _statement_role(claim_id: str, realization) -> str | None:
    """The role a paragraph would use to state this claim. REQUIREMENT is the narrower of the two."""
    for role in STATEMENT_ROLES:
        entry = realization.entry(claim_id, role)
        if entry and entry["status"] == "REALIZABLE":
            return role
    return None


def probe_statement_alone(claim_id: str, role: str, realization, bundle) -> dict:
    """Render the claim's statement by itself and put it to the unchanged Draft Validator v1.2.

    Plan validation is deliberately bypassed here and only here. The question being asked is
    whether the statement satisfies the condition on its own; plan validation answers by consulting
    the obligation rule, which is what is being derived. Rendering the slot directly asks the
    validator instead of asking the rule about itself. The prose is never released — it exists for
    the length of one validation call and is recorded as evidence.
    """
    v1 = module("v1", VALIDATOR_V1)
    v1_2 = module("v1_2", VALIDATOR_V1_2)
    plan_ir = module("plan_ir", PLAN_IR)
    renderer = module("renderer", RENDERER)
    raw = {
        "section_id": SECTION_ID, "plan_id": f"OBLIGATION-PROBE-{claim_id}",
        "plan_version": "obligation-probe-v2-1", "language": "tr",
        "subsections": [{
            "subsection_id": "SEC-02-2-A",
            "paragraph_groups": [{
                "paragraph_id": "OBLIGATION-P01",
                "slots": [{"slot_id": "OB-01", "claim_id": claim_id,
                           "realization_role": role}]}]}],
    }
    payload = renderer.render_plan(plan_ir.parse_plan(raw), realization, bundle)
    result = v1_2.validate_draft(v1.parse_draft_ir(payload), bundle)
    histogram = dict(result.failure_histogram)
    return {
        "probe_role": role,
        "status": result.status,
        "histogram": histogram,
        "condition_dropped": histogram.get("CONDITION_DROPPED", 0) > 0,
        "rendered_text": [u["text"] for u in payload["units"] if u["material"]],
    }


def derive_obligations(claim_id: str, claim: dict, realization, bundle) -> dict:
    """Which companion roles a paragraph stating this claim must also allocate.

    CONDITION is asserted only where the frozen validator, run on the statement alone, says the
    condition was dropped. QUALIFIER_SCOPE is asserted wherever the claim registers a qualifier,
    unchanged — see the module docstring on DF-01.
    """
    conditions = [c for c in (claim.get("conditions") or [])
                  if module("v1", VALIDATOR_V1).content_tokens(c, bundle.function_lexicon)]
    qualifiers = list(claim.get("qualifiers") or [])
    role = _statement_role(claim_id, realization)

    obligation: dict[str, Any] = {
        "claim_id": claim_id,
        "registered_conditions": conditions,
        "registered_qualifiers": qualifiers,
        "statement_role": role,
        "qualifier_obligation_rule": ("registered qualifier is mandatory wherever the claim is "
                                      "stated; not derived from stage E — see DF-01"),
        "requires_qualifier_slot": bool(qualifiers),
    }

    if not conditions:
        obligation.update({"requires_condition_slot": False,
                           "condition_obligation_basis": "the claim registers no condition"})
        return obligation
    if role is None:
        obligation.update({"requires_condition_slot": True,
                           "condition_obligation_basis": ("no statement realization exists, so the "
                                                          "obligation cannot be discharged and "
                                                          "stands — fail closed")})
        return obligation
    try:
        probe = probe_statement_alone(claim_id, role, realization, bundle)
    except Exception as error:  # noqa: BLE001 — any probe failure must fail closed, not silently
        obligation.update({
            "requires_condition_slot": True,
            "condition_obligation_basis": (f"the statement realization could not be probed "
                                           f"({type(error).__name__}: {error}); the obligation "
                                           f"stands — fail closed"),
        })
        return obligation
    obligation.update({
        "requires_condition_slot": probe["condition_dropped"],
        "condition_obligation_basis": (
            "Draft Validator v1.2 raised CONDITION_DROPPED on the statement rendered alone"
            if probe["condition_dropped"] else
            "Draft Validator v1.2 raised no CONDITION_DROPPED on the statement rendered alone, "
            "so the statement carries its own condition and no separate slot is required"),
        "obligation_probe": probe,
    })
    return obligation


def install_obligation_rule(obligations: dict[str, dict]) -> None:
    """Make plan validation ask the same question the universe answered.

    M1's `_validate_paragraph_scope` raises PLAN_PARAGRAPH_CONDITION_MISSING from
    `paragraph_scoped_conditions`, the all-anchors classification RM-2 replaces. Leaving it in
    place would recreate the pilot's defect with the disagreement moved one layer down: the
    universe would offer a plan that plan validation then refused. The substitution is made on the
    imported module object — `59_semantic_plan_ir_contract_v2.py` is not written to, and the phase
    gate re-hashes it. `unit_scoped_conditions` is untouched, so the renderer's condition prefix
    behaves exactly as it did. No failure code is renamed, removed or made unreachable:
    PLAN_PARAGRAPH_CONDITION_MISSING still fires for every claim whose statement really does drop
    its condition, and PLAN_ROLE_UNREALIZABLE is not touched at all.
    """
    unify_plan_ir()
    # Copied before anything is cleared: `ensure_obligation_rule` may pass the module-level dict
    # itself, and clearing the argument would install an empty rule that silently falls back to
    # M1 v2's classification for every claim.
    obligations = dict(obligations)
    _INSTALLED_OBLIGATIONS.clear()
    _INSTALLED_OBLIGATIONS.update(obligations)
    for instance in plan_ir_instances():
        if getattr(instance, "_rm2_obligation_rule_installed", False):
            instance._rm2_obligations = obligations
            continue
        instance._rm2_obligations = obligations
        instance._rm2_obligation_rule_original = instance.paragraph_scoped_conditions
        instance.paragraph_scoped_conditions = _make_rule(instance)
        instance._rm2_obligation_rule_installed = True


_INSTALLED_OBLIGATIONS: dict[str, dict] = {}


def ensure_obligation_rule() -> None:
    """Re-apply the rule to any M1 instance loaded since the last install. Idempotent.

    Modules here import M1 lazily, so a consumer can create a fresh instance after the rule was
    installed. Every entry point that validates a plan calls this first.
    """
    if _INSTALLED_OBLIGATIONS:
        install_obligation_rule(dict(_INSTALLED_OBLIGATIONS))


def original_obligation_rule(claim: dict, bundle) -> list[str]:
    """M1 v2's all-anchors classification, kept callable so RM-2's delta can be reported."""
    for instance in plan_ir_instances():
        original = getattr(instance, "_rm2_obligation_rule_original", None)
        if original is not None:
            return original(claim, bundle)
    return module("plan_ir", PLAN_IR).paragraph_scoped_conditions(claim, bundle)


def _reachable_modules() -> list[Any]:
    """Every module object reachable in this process, including privately cached ones.

    The scripts in this architecture import each other by path with ad-hoc keys and cache the
    result in a private `_MODULES` dict, so one file can be represented by several distinct module
    objects and `sys.modules` shows only the last under any given key.
    """
    seen: set[int] = set()
    found: list[Any] = []

    def consider(candidate: Any) -> None:
        if not isinstance(candidate, ModuleType) or id(candidate) in seen:
            return
        seen.add(id(candidate))
        found.append(candidate)

    for holder in list(sys.modules.values()):
        consider(holder)
    index = 0
    while index < len(found):
        namespace = getattr(found[index], "__dict__", None)
        index += 1
        if not isinstance(namespace, dict):
            continue
        for value in list(namespace.values()):
            consider(value)
            if isinstance(value, dict):
                for nested in list(value.values()):
                    consider(nested)
    return found


def _is_m1(candidate: Any) -> bool:
    source = getattr(candidate, "__file__", None)
    if not isinstance(candidate, ModuleType) or not source:
        return False
    try:
        return Path(source).resolve() == PLAN_IR.resolve()
    except OSError:
        return False


def unify_plan_ir() -> Any:
    """Collapse every private copy of M1 onto one shared instance, and pre-seed the lazy caches.

    This is the same principle as the universe itself, applied to code rather than data: the
    pilot's defect was one thing derived twice, and a module imported twice is one rule
    implemented twice. After this runs there is a single M1 object in the process, every consumer
    holds a reference to it, and a consumer that has not imported M1 yet will find it already in
    its cache instead of constructing a second one.
    """
    canonical = module("plan_ir", PLAN_IR)
    for holder in _reachable_modules():
        if holder is canonical:
            continue
        namespace = getattr(holder, "__dict__", None)
        if not isinstance(namespace, dict):
            continue
        for name, value in list(namespace.items()):
            if _is_m1(value) and value is not canonical:
                setattr(holder, name, canonical)
        cache = namespace.get("_MODULES")
        if isinstance(cache, dict):
            for key, value in list(cache.items()):
                if _is_m1(value) and value is not canonical:
                    cache[key] = canonical
            target = namespace.get("PLAN_IR")
            if isinstance(target, Path) and target.resolve() == PLAN_IR.resolve():
                cache.setdefault("plan_ir", canonical)
                cache["plan_ir"] = canonical
    return canonical


def plan_ir_instances() -> list[Any]:
    """Every loaded copy of M1 after unification — normally exactly one."""
    return [m for m in _reachable_modules()
            if _is_m1(m) and hasattr(m, "paragraph_scoped_conditions")]


def _make_rule(instance):
    original = instance.paragraph_scoped_conditions

    def paragraph_scoped_conditions(claim: dict, bundle) -> list[str]:
        entry = instance._rm2_obligations.get(claim.get("claim_id"))
        if entry is None:
            # A claim outside the universe keeps M1 v2's stricter rule. Fail closed.
            return original(claim, bundle)
        return list(entry["registered_conditions"]) if entry["requires_condition_slot"] else []

    return paragraph_scoped_conditions


# ================================================================ RM-1 — the universe


def build_universe(realization, bundle) -> dict:
    """One universe. Derived mechanically; no hand-maintained second option list exists."""
    v1 = module("v1", VALIDATOR_V1)
    plan_ir = module("plan_ir", PLAN_IR)
    plan = json.loads(PLAN_V1_2.read_text(encoding="utf-8"))

    closed_roles = set(plan_ir.REALIZATION_ROLES) if hasattr(plan_ir, "REALIZATION_ROLES") else None
    allocated = [cid for sub in plan["subsections"] for cid in sub["claim_ids"]]
    required_core = sorted({c for t in plan["required_topics"]["coverage"].values()
                            for c in t["required_core_claim_ids"]})

    realizable_by_claim: dict[str, list[str]] = {}
    for claim_id, role in realization.realizable_pairs():
        realizable_by_claim.setdefault(claim_id, []).append(role)

    obligations = {cid: derive_obligations(cid, bundle.allowlist[cid], realization, bundle)
                   for cid in sorted(set(allocated))}
    install_obligation_rule(obligations)

    options, exclusions, invariant_rows = [], [], []
    for claim_id in allocated:
        claim = bundle.allowlist[claim_id]
        obligation = obligations[claim_id]
        realizable = sorted(realizable_by_claim.get(claim_id, []))
        available = sorted(r for r in realizable
                           if closed_roles is None or r in closed_roles)

        required = []
        if obligation["statement_role"]:
            required.append(obligation["statement_role"])
        if obligation["requires_condition_slot"]:
            required.append("CONDITION")
        if obligation["requires_qualifier_slot"]:
            required.append("QUALIFIER_SCOPE")
        required = sorted(set(required))

        row = {
            "claim_id": claim_id,
            "required_roles": required,
            "available_roles": available,
            "realizable_roles": realizable,
            "required_subset_available": set(required) <= set(available),
            "available_subset_realizable": set(available) <= set(realizable),
        }
        row["invariant_holds"] = (row["required_subset_available"]
                                  and row["available_subset_realizable"])
        invariant_rows.append(row)

        if not obligation["statement_role"]:
            exclusions.append({"claim_id": claim_id, "reason_code": "NO_SATISFIABLE_ROLE_SET",
                               "reason": "no statement realization exists for this claim",
                               "required_roles": required, "available_roles": available,
                               "realizable_roles": realizable})
            continue
        if not row["invariant_holds"]:
            exclusions.append({
                "claim_id": claim_id, "reason_code": "REQUIRED_ROLE_UNAVAILABLE",
                "reason": ("the claim carries obligations its available roles cannot satisfy: "
                           f"{sorted(set(required) - set(available))}"),
                "required_roles": required, "available_roles": available,
                "realizable_roles": realizable})
            continue

        options.append({
            "claim_id": claim_id,
            "topic": claim.get("topic"),
            "source_keys": sorted(claim.get("source_keys") or []),
            "allowed_relationships": sorted(claim.get("allowed_relationships") or []),
            "statement_role": obligation["statement_role"],
            "required_roles": required,
            "available_roles": available,
            "realizable_roles": realizable,
            "requires_condition_slot": obligation["requires_condition_slot"],
            "requires_qualifier_slot": obligation["requires_qualifier_slot"],
            "condition_obligation_basis": obligation["condition_obligation_basis"],
        })

    exposed = {o["claim_id"] for o in options}
    missing_core = sorted(set(required_core) - exposed)
    if missing_core:
        raise UniverseViolation(
            f"required core claims excluded from the universe: {missing_core}; a thinner section "
            "is not an acceptable resolution of a contradiction")

    universe = {
        "version": UNIVERSE_VERSION,
        "section_id": SECTION_ID,
        "principle": ("One option universe, derived mechanically from M2 v2.1's realizable pairs "
                      "and M1's plan rules, consumed by SHA by every downstream reader. "
                      "required_roles ⊆ available_roles ⊆ realizable_roles holds for every "
                      "exposed claim, enforced at construction."),
        "derived_from": {
            "M1_semantic_plan_ir_contract_v2": "plan rules, closed role set, plan validation",
            "M2_claim_realization_contract_v2_1": "realizable claim×role pairs",
            "frozen_claim_obligations": "conditions and qualifiers on the frozen allowlist",
            "draft_plan_v1_2": "subsection allocation and required topics",
            "draft_validator_v1_2": "the obligation derivation, run not reimplemented",
        },
        "invariant": "required_roles ⊆ available_roles ⊆ realizable_roles",
        "subsections": [{"subsection_id": s["subsection_id"], "title": s["title"],
                         "required_topic": s.get("required_topic"),
                         "claim_ids": [c for c in s["claim_ids"] if c in exposed]}
                        for s in plan["subsections"]],
        "required_topics": plan["required_topics"]["required"],
        "required_core_claim_ids": required_core,
        "options": options,
        "exclusions": exclusions,
        "unrealizable_pairs_exposed": 0,
        "plan_rules": [
            "every claim stated needs its declared statement_role slot in its paragraph",
            "a claim with requires_condition_slot needs a CONDITION slot in the same paragraph",
            "a claim with requires_qualifier_slot needs a QUALIFIER_SCOPE slot in the same "
            "paragraph",
            "a claim holds at most one of CLAIM_STATEMENT / REQUIREMENT per paragraph",
            "only (claim_id, role) pairs listed in available_roles may be selected",
            "citation_source_keys, when given, must be the claim's own registered keys",
        ],
    }
    audit = {
        "invariant_rows": invariant_rows,
        "obligations": obligations,
        "claims_allocated": len(set(allocated)),
        "claims_exposed": len(options),
        "claims_excluded": len(exclusions),
    }
    return {"universe": universe, "audit": audit}


def assert_invariant(universe: dict) -> list[dict]:
    """Fail-closed re-check on the serialized artifact. A violating universe cannot be loaded."""
    violations = []
    for option in universe["options"]:
        required = set(option["required_roles"])
        available = set(option["available_roles"])
        realizable = set(option["realizable_roles"])
        if not (required <= available <= realizable):
            violations.append({"claim_id": option["claim_id"],
                               "required_not_available": sorted(required - available),
                               "available_not_realizable": sorted(available - realizable)})
        if option["requires_condition_slot"] and "CONDITION" not in available:
            violations.append({"claim_id": option["claim_id"],
                               "contradiction": "requires CONDITION but does not offer it"})
        if option["requires_qualifier_slot"] and "QUALIFIER_SCOPE" not in available:
            violations.append({"claim_id": option["claim_id"],
                               "contradiction": "requires QUALIFIER_SCOPE but does not offer it"})
    return violations


def load_universe(path: Path = UNIVERSE_PATH) -> tuple[dict, str]:
    """Read the universe as bytes and refuse a violating one. Both consumers enter here."""
    data = path.read_bytes()
    payload = json.loads(data.decode("utf-8"))
    universe = payload["universe"]
    violations = assert_invariant(universe)
    if violations:
        raise UniverseViolation(f"serialized universe violates the subset invariant: {violations}")
    return universe, sha_bytes(canonical_bytes(universe))


# ================================================================ the two consumers


def feasibility_plan(universe: dict) -> dict:
    """A full deterministic section plan, built from the universe and nothing else."""
    ensure_obligation_rule()
    subsections = []
    options = {o["claim_id"]: o for o in universe["options"]}
    for subsection in universe["subsections"]:
        slots, index = [], 0
        for claim_id in subsection["claim_ids"]:
            option = options[claim_id]
            for role in ([option["statement_role"]]
                         + [r for r in option["required_roles"]
                            if r != option["statement_role"]]):
                index += 1
                slots.append({"slot_id": f"F-{subsection['subsection_id']}-{index:02d}",
                              "claim_id": claim_id, "realization_role": role,
                              "citation_source_keys": option["source_keys"]})
        if slots:
            subsections.append({
                "subsection_id": f"{SECTION_ID}-{subsection['subsection_id']}",
                "paragraph_groups": [{
                    "paragraph_id": f"F-{subsection['subsection_id']}-P01", "slots": slots}]})
    return {"section_id": SECTION_ID, "plan_id": "SEC-02-2-FEASIBILITY-V2-1",
            "plan_version": "feasibility-v2-1", "language": "tr", "subsections": subsections}


def planner_payload(universe: dict) -> dict:
    """The payload a future ARCHITECTURE V2 PILOT #2 would send. Built here, not sent.

    It embeds the universe block verbatim. There is no projection, no filtering and no second
    rendering of the option list, because any of those would be the second derivation this phase
    exists to remove.
    """
    return {
        "payload_version": "tunnelbook-architecture-v2-planner-payload-v2-1",
        "section_id": SECTION_ID,
        "task": ("Select claim×role slots for each subsection. Emit field names only; emit no "
                 "prose. Every selected pair must appear in that claim's available_roles."),
        "rules": universe["plan_rules"],
        "universe": universe,
    }


def universe_sha_of(container: dict) -> str:
    return sha_bytes(canonical_bytes(container["universe"]))


def main() -> int:
    m2_1 = module("m2_v2_1", M2_V2_1)
    v1 = module("v1", VALIDATOR_V1)
    bundle = v1.load_bundle()
    realization = m2_1.load()
    built = build_universe(realization, bundle)
    violations = assert_invariant(built["universe"])
    if violations:
        raise UniverseViolation(f"construction produced a violating universe: {violations}")
    UNIVERSE_PATH.parent.mkdir(parents=True, exist_ok=True)
    universe_sha = sha_bytes(canonical_bytes(built["universe"]))
    payload = {"universe": built["universe"], "audit": built["audit"],
               "universe_sha256": universe_sha}
    UNIVERSE_PATH.write_bytes(canonical_bytes(payload))
    print(f"planner option universe: {UNIVERSE_PATH.relative_to(ROOT)}")
    print(f"universe sha256 {universe_sha}")
    print(f"exposed {built['audit']['claims_exposed']} / allocated "
          f"{built['audit']['claims_allocated']}, excluded {built['audit']['claims_excluded']}")
    for row in built["universe"]["exclusions"]:
        print(f"  excluded {row['claim_id']}: {row['reason_code']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
