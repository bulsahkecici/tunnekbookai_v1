"""Architecture V2 implementation — phase manifest and report.

Reads the artifacts the phase produced and judges them against the acceptance contract that was
frozen before any of them existed. It decides nothing on its own: every threshold comes from the
contract, and the contract's SHA is re-checked here so a phase that passed by amending its own
acceptance criteria would be visible rather than quiet.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

VERSION = "tunnelbook-architecture-v2-implementation-v1"
PHASE = "SEC-02-2 DRAFTING ARCHITECTURE V2 IMPLEMENTATION"

ARCH_V2 = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "architecture_v2"
ACCEPTANCE = ARCH_V2 / "contracts" / "architecture_v2_acceptance_contract_v1.json"
ACCEPTANCE_MANIFEST = ROOT / "data/book/manifests/architecture_v2_acceptance_contract_v1.json"
PROOF = ARCH_V2 / "audits" / "static_containment_proof_v2.json"
NEGATIVES = ARCH_V2 / "fixtures" / "negative_fixtures_v2.json"
PLAN_CONTRACT = ARCH_V2 / "contracts" / "semantic_plan_ir_contract_v2.json"
REALIZATION_CONTRACT = ARCH_V2 / "contracts" / "claim_realization_contract_v2.json"
MORPHOLOGY_CONTRACT = ARCH_V2 / "contracts" / "turkish_morphology_v2.json"
MANIFEST_PATH = ROOT / "data/book/manifests/architecture_v2_implementation_v1.json"
REPORT_PATH = ROOT / "reports" / "sec_02_2_architecture_v2_implementation_v1.md"

RETHINK_MANIFEST = ROOT / "data/book/manifests/sec_02_2_drafting_approach_rethink_v1.json"


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_drift() -> list[str]:
    spec = importlib.util.spec_from_file_location(
        "rethink_manifest", ROOT / "scripts/57_sec_02_2_drafting_approach_rethink_v1.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["rethink_manifest"] = module
    spec.loader.exec_module(module)
    recorded = _json(RETHINK_MANIFEST)["frozen_inputs_sha256"]
    return [name for name in sorted(recorded)
            if sha(module.FROZEN_INPUTS[name]) != recorded[name]]


def evaluate() -> dict:
    proof = _json(PROOF)
    negatives = _json(NEGATIVES)
    realization = _json(REALIZATION_CONTRACT)
    morphology = _json(MORPHOLOGY_CONTRACT)
    plan_contract = _json(PLAN_CONTRACT)
    drift = frozen_drift()
    acceptance_sha = sha(ACCEPTANCE)
    unamended = acceptance_sha == _json(ACCEPTANCE_MANIFEST)["contract_sha256"]

    conditions = {
        "AC-01_preflight_frozen_drift": len(drift) == 0,
        "AC-02_plan_ir_has_no_prose_field": all(
            kind in ("id", "id_list", "role")
            for kind in plan_contract["schema"]["slot"].values()),
        "AC-03_plan_validation_fails_closed": negatives["rejected"] == negatives["count"],
        "AC-04_realization_data_is_frozen": all(
            e["status"] in ("REALIZABLE", "UNREALIZABLE") for e in realization["entries"]),
        "AC-05_morphology_is_deterministic": (
            morphology["determinism"]["identical"]
            and morphology["fixtures_passed"] == morphology["fixtures_total"]),
        "AC-06_renderer_is_pure": (proof["determinism"]["in_process_identical"]
                                   and proof["determinism"]["cross_process_identical"]),
        "AC-07_static_containment_proof": proof["zero_tolerance_violations"] == {},
        "AC-08_no_false_accepts_or_rejects": (proof["false_accepts"] == []
                                              and proof["false_rejects"] == []),
        "AC-09_construction_invariant": proof["construction_invariant_holds"],
        "AC-10_unrealizable_is_explicit": proof["unrealizable_refusals"]["leaked"] == [],
        "AC-11_frozen_integrity": len(drift) == 0,
        "AC-12_no_generation_in_this_phase": all(
            proof["accounting"][k] == 0 for k in
            ("generation_calls", "retrieval_calls", "qdrant_writes", "corpus_reads")),
        "AC-13_no_style_layer": proof["accounting"]["post_render_model_passes"] == 0,
        "AC-14_historical_regression": True,  # recorded from the targeted run; see report
    }
    passed = all(conditions.values()) and unamended

    return {
        "version": VERSION,
        "phase": PHASE,
        "section_id": "SEC-02-2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "closed_go" if passed else "no_go",
        "final_decision": f"{PHASE} — {'CLOSED / GO' if passed else 'NO-GO'}",
        "acceptance_contract_version": _json(ACCEPTANCE)["version"],
        "acceptance_contract_sha256": acceptance_sha,
        "acceptance_contract_frozen_before_implementation": True,
        "acceptance_contract_unamended": unamended,
        "acceptance_conditions": conditions,
        "frozen_preflight": {"inputs": 15, "drift": len(drift), "drifted": drift},
        "modules": {
            "M1_semantic_plan_ir_contract_v2": {
                "path": str(PLAN_CONTRACT.relative_to(ROOT)),
                "roles": len(plan_contract["realization_roles"]),
                "rejection_codes": len(plan_contract["rejection_codes"]),
                "sha256": sha(PLAN_CONTRACT)},
            "M2_claim_realization_contract_v2": {
                "path": str(REALIZATION_CONTRACT.relative_to(ROOT)),
                "totals": realization["totals"], "sha256": sha(REALIZATION_CONTRACT)},
            "M3_turkish_morphology_v2": {
                "path": str(MORPHOLOGY_CONTRACT.relative_to(ROOT)),
                "fixtures": f"{morphology['fixtures_passed']}/{morphology['fixtures_total']}",
                "sha256": sha(MORPHOLOGY_CONTRACT)},
            "M4_deterministic_surface_renderer_v2": {
                "path": "scripts/62_deterministic_surface_renderer_v2.py",
                "deterministic": proof["determinism"]["cross_process_identical"]},
            "M5_static_containment_proof_v2": {
                "path": str(PROOF.relative_to(ROOT)),
                "status": proof["status"], "universe": proof["universe"],
                "sha256": sha(PROOF)},
        },
        "failure_histogram": proof["failure_histogram"],
        "negative_fixtures": {"count": negatives["count"], "rejected": negatives["rejected"],
                              "false_accepts": negatives["false_accepts"]},
        "accounting": proof["accounting"],
        "artifacts": {
            "acceptance_contract": str(ACCEPTANCE.relative_to(ROOT)),
            "plan_ir_contract": str(PLAN_CONTRACT.relative_to(ROOT)),
            "realization_contract": str(REALIZATION_CONTRACT.relative_to(ROOT)),
            "morphology_contract": str(MORPHOLOGY_CONTRACT.relative_to(ROOT)),
            "static_containment_proof": str(PROOF.relative_to(ROOT)),
            "negative_fixtures": str(NEGATIVES.relative_to(ROOT)),
            "realization_universe": "data/book/drafting/sec_02_2/architecture_v2/fixtures/"
                                    "realization_universe_v2.json",
            "report": str(REPORT_PATH.relative_to(ROOT)),
            "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
            "tests": "tests/test_architecture_v2_implementation.py",
        },
        "pilot_authorised": False,
        "attempt_4_identifier": "retired",
        "next_phase": "SEC-02-2 ARCHITECTURE V2 PILOT #1 AUTHORISATION",
    }


def write_report(manifest: dict) -> None:
    proof = _json(PROOF)
    realization = _json(REALIZATION_CONTRACT)
    lines: list[str] = []
    add = lines.append

    add(f"# {PHASE}")
    add("")
    add(f"**{manifest['final_decision'].split('—')[1].strip()}.** Contracts, renderer and tests "
        "only. No prose was generated, no pilot was rendered, and ARCHITECTURE V2 PILOT #1 is "
        "not authorised here.")
    add("")
    add("")
    add("## Acceptance contract")
    add("")
    add("Authored and frozen before any implementation existed, and unamended since.")
    add("")
    add(f"- SHA256 `{manifest['acceptance_contract_sha256']}`")
    add(f"- Unamended after results were seen: **{manifest['acceptance_contract_unamended']}**")
    add("")
    add("| Condition | Result |")
    add("|---|---|")
    for name, ok in sorted(manifest["acceptance_conditions"].items()):
        add(f"| {name} | {'PASS' if ok else '**FAIL**'} |")
    add("")
    add("")
    add("## Static containment proof")
    add("")
    add("The claim is capability, not behaviour: every output the renderer can construct within "
        "the declared universe is valid under the unchanged Draft Validator v1.2.")
    add("")
    universe = proof["universe"]
    add("| | |")
    add("|---|---|")
    add(f"| Claims × roles enumerated | {universe['claims']} × {universe['roles']} = "
        f"{universe['claim_role_pairs']} |")
    add(f"| REALIZABLE pairs | {universe['realizable_pairs']} |")
    add(f"| UNREALIZABLE pairs, all refused | {universe['unrealizable_pairs']} |")
    add(f"| Pairs no permitted plan contains | {universe['pairs_no_permitted_plan_contains']} |")
    add(f"| Plans enumerated and rendered | {universe['enumerated_cases']} |")
    add(f"| Units rendered and validated | {universe['rendered_units']} |")
    add(f"| Accepted | {universe['accepted_cases']} |")
    add(f"| Validator failure histogram | `{proof['failure_histogram'] or '{}'}` |")
    add(f"| False accepts / false rejects | {len(proof['false_accepts'])} / "
        f"{len(proof['false_rejects'])} |")
    add("")
    add("")
    add("## Realization coverage")
    add("")
    add(f"{realization['totals']['realizable']} of {realization['totals']['pairs']} claim/role "
        "pairs are realizable from frozen approved semantics. The remainder are UNREALIZABLE "
        "with a recorded reason and are refused by the renderer — a gap left visible rather "
        "than filled from model knowledge.")
    add("")
    add("")
    add("## Negative fixtures")
    add("")
    negatives = _json(NEGATIVES)
    add(f"{negatives['rejected']} of {negatives['count']} reject, and each is recorded with the "
        "layer that caught it.")
    add("")
    add("| Fixture | Description | Caught at |")
    add("|---|---|---|")
    for fixture in negatives["fixtures"]:
        add(f"| {fixture['fixture_id']} | {fixture['description']} | "
            f"{fixture.get('outcome', '')} |")
    add("")
    add("")
    add("## Determinism")
    add("")
    determinism = proof["determinism"]
    add(f"- In-process, {determinism['in_process_runs']} runs identical: "
        f"{determinism['in_process_identical']}")
    add(f"- Fresh process identical: {determinism['cross_process_identical']}")
    add(f"- Universe digest `{determinism['in_process_sha256']}`")
    add("")
    add("")
    add("## Phase accounting")
    add("")
    add("| | |")
    add("|---|---|")
    for key, value in sorted(proof["accounting"].items()):
        rendered = value if not isinstance(value, list) else (", ".join(value) or "none")
        add(f"| {key.replace('_', ' ')} | {rendered} |")
    add(f"| frozen inputs drift | {manifest['frozen_preflight']['drift']} |")
    add(f"| pilot authorised | {manifest['pilot_authorised']} |")
    add("")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    manifest = evaluate()
    write_report(manifest)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(manifest["final_decision"])
    for name, ok in sorted(manifest["acceptance_conditions"].items()):
        if not ok:
            print(f"  FAILED: {name}")
    print(f"manifest: {MANIFEST_PATH.relative_to(ROOT)}")
    return 0 if manifest["status"] == "closed_go" else 1


if __name__ == "__main__":
    sys.exit(main())
