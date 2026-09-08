"""Fail-closed pre-integration claim-role condition/dependency closure proof."""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/claim_role_condition_closure_v1"
CONTRACT_PATH = BASE / "contracts/claim_role_condition_closure_contract_v1.json"


@dataclass(frozen=True)
class Failure:
    code: str
    instance_id: str | None
    requirement_id: str | None
    detail: str


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _failure(code: str, instance_id: str | None, requirement_id: str | None, detail: str) -> Failure:
    return Failure(code, instance_id, requirement_id, detail)


def _close_requirement(kind: str, governed: dict, requirement_id: str, closures: list[dict],
                       instances: dict[str, dict]) -> list[Failure]:
    prefix = "CONDITION" if kind == "condition" else "DEPENDENCY"
    failures: list[Failure] = []
    selected = [row for row in closures if row.get("requirement_id") == requirement_id]
    if not selected:
        code = f"CRCC_{prefix}_OWNER_MISSING"
        if kind == "dependency" and requirement_id in governed.get("ambient_paragraph_semantics", []):
            code = "CRCC_DEPENDENCY_ACCIDENTAL_CONTEXT"
        return [_failure(code, governed["instance_id"], requirement_id, "no explicit owner")]
    if len(selected) != 1:
        return [_failure(f"CRCC_{prefix}_OWNER_DUPLICATED", governed["instance_id"],
                         requirement_id, "requirement must have exactly one closure record")]

    closure = selected[0]
    mechanism = closure.get("mechanism")
    owner = instances.get(closure.get("owner_instance_id"))
    if mechanism not in {"A", "B", "C"}:
        failures.append(_failure(f"CRCC_{prefix}_MECHANISM_INVALID", governed["instance_id"],
                                 requirement_id, "unknown ownership mechanism"))
        return failures
    if owner is None or owner.get("claim_id") != governed.get("claim_id") or not owner.get("role_realizable"):
        failures.append(_failure(f"CRCC_{prefix}_OWNER_UNREALIZABLE", governed["instance_id"],
                                 requirement_id, "owner is absent, cross-claim, or role-unrealizable"))
        return failures
    if not closure.get("owner_can_realize") or closure.get("renderer_input_field") not in owner.get("renderer_input_fields", []):
        failures.append(_failure(f"CRCC_ROLE_{prefix}_INFEASIBLE", governed["instance_id"],
                                 requirement_id, "owner cannot realize the declared renderer input"))

    scope = closure.get("validator_scope")
    same_unit = owner.get("unit_id") == governed.get("unit_id")
    same_paragraph = owner.get("paragraph_id") == governed.get("paragraph_id")
    if scope == "UNIT" and not same_unit:
        failures.append(_failure(f"CRCC_{prefix}_SCOPE_INVALID", governed["instance_id"],
                                 requirement_id, "UNIT scope cannot be closed by another unit"))
    elif scope == "PARAGRAPH" and not same_paragraph:
        failures.append(_failure(f"CRCC_{prefix}_SCOPE_INVALID", governed["instance_id"],
                                 requirement_id, "owner is outside the bound paragraph"))
    elif scope not in {"UNIT", "PARAGRAPH"}:
        failures.append(_failure(f"CRCC_{prefix}_SCOPE_INVALID", governed["instance_id"],
                                 requirement_id, "validator scope is unknown"))

    if mechanism == "A" and owner["instance_id"] != governed["instance_id"]:
        failures.append(_failure(f"CRCC_{prefix}_MECHANISM_INVALID", governed["instance_id"],
                                 requirement_id, "mechanism A requires self ownership"))
    if mechanism == "B" and owner["instance_id"] == governed["instance_id"]:
        failures.append(_failure(f"CRCC_{prefix}_MECHANISM_INVALID", governed["instance_id"],
                                 requirement_id, "mechanism B requires another explicit instance"))
    if mechanism == "C":
        proof = closure.get("validator_proof", {})
        if not owner.get("primary") or proof.get("status") != "PASS" or proof.get("scope") != scope:
            failures.append(_failure(f"CRCC_{prefix}_MECHANISM_INVALID", governed["instance_id"],
                                     requirement_id, "mechanism C lacks matching frozen-validator proof"))
    return failures


def validate(plan: dict, contract: dict | None = None) -> dict:
    contract = contract or load(CONTRACT_PATH)
    failures: list[Failure] = []
    if plan.get("claim_specific_branches"):
        failures.append(_failure("CRCC_CLAIM_SPECIFIC_BRANCH", None, None,
                                 "claim-specific allocation branches are forbidden"))
    rows = plan.get("instances")
    if not isinstance(rows, list) or not rows:
        failures.append(_failure("CRCC_SCHEMA_INVALID", None, None, "instances must be non-empty"))
        rows = []
    instances = {row.get("instance_id"): row for row in rows if row.get("instance_id")}
    if len(instances) != len(rows):
        failures.append(_failure("CRCC_SCHEMA_INVALID", None, None, "instance ids must be present and unique"))

    feasibility: list[dict] = []
    requirement_registry = plan.get("role_requirement_registry", {})
    strict_registry = bool(plan.get("strict_requirement_registry"))
    for row in rows:
        start = len(failures)
        if not row.get("semantic_content", False):
            continue
        if not row.get("role_realizable", False):
            failures.append(_failure("CRCC_ROLE_UNREALIZABLE", row.get("instance_id"), None,
                                     "semantic role is not lexically realizable"))
        if not row.get("condition_set_known", False):
            failures.append(_failure("CRCC_CONDITION_SET_UNKNOWN", row.get("instance_id"), None,
                                     "role-level required condition set is unknown"))
        condition_ids = row.get("semantic_condition_ids", [])
        dependency_ids = row.get("semantic_dependency_ids", [])
        if strict_registry:
            registered = requirement_registry.get(row.get("instance_id"))
            if registered is None:
                failures.append(_failure("CRCC_CONDITION_SET_UNKNOWN", row.get("instance_id"), None,
                                         "role has no requirement-registry entry"))
            elif (set(condition_ids) != set(registered.get("condition_ids", [])) or
                  set(dependency_ids) != set(registered.get("dependency_ids", []))):
                failures.append(_failure("CRCC_CONDITION_SET_MISMATCH", row.get("instance_id"), None,
                                         "allocated requirements differ from the role-requirement registry"))
        condition_closures = row.get("condition_closures", [])
        dependency_closures = row.get("dependency_closures", [])
        for requirement_id in condition_ids:
            failures += _close_requirement("condition", row, requirement_id, condition_closures, instances)
        for requirement_id in dependency_ids:
            failures += _close_requirement("dependency", row, requirement_id, dependency_closures, instances)
        if {c.get("requirement_id") for c in condition_closures} - set(condition_ids):
            failures.append(_failure("CRCC_SCHEMA_INVALID", row.get("instance_id"), None,
                                     "condition closure exists for a non-required condition"))
        if {c.get("requirement_id") for c in dependency_closures} - set(dependency_ids):
            failures.append(_failure("CRCC_SCHEMA_INVALID", row.get("instance_id"), None,
                                     "dependency closure exists for a non-required dependency"))
        row_failures = failures[start:]
        feasibility.append({
            "instance_id": row.get("instance_id"),
            "role_feasible": not row_failures,
            "lexical_feasible": bool(row.get("role_realizable")),
            "condition_feasible": not any("CONDITION" in failure.code for failure in row_failures),
            "dependency_feasible": not any("DEPENDENCY" in failure.code for failure in row_failures),
        })
    return {
        "status": "ACCEPT" if not failures else "REJECT",
        "contract_version": contract["version"],
        "failure_codes": sorted({failure.code for failure in failures}),
        "failures": [asdict(failure) for failure in failures],
        "role_feasibility": feasibility,
        "checked_instances": len(feasibility),
        "pre_integration_authorised": not failures,
    }


def evaluate_fixtures(path: Path | None = None) -> dict:
    payload = load(path or BASE / "fixtures/closure_fixtures_v1.json")
    results = []
    false_accepts = false_rejects = code_mismatches = 0
    for fixture in payload["fixtures"]:
        result = validate(fixture["plan"])
        expected = fixture["expected_status"]
        if result["status"] == "ACCEPT" and expected == "REJECT":
            false_accepts += 1
        if result["status"] == "REJECT" and expected == "ACCEPT":
            false_rejects += 1
        expected_codes = set(fixture.get("expected_codes", []))
        if expected_codes - set(result["failure_codes"]):
            code_mismatches += 1
        results.append({"fixture_id": fixture["fixture_id"], "expected_status": expected,
                        "actual_status": result["status"], "failure_codes": result["failure_codes"]})
    return {"results": results, "false_accepts": false_accepts, "false_rejects": false_rejects,
            "code_mismatches": code_mismatches,
            "positive_count": sum(row["expected_status"] == "ACCEPT" for row in payload["fixtures"]),
            "negative_count": sum(row["expected_status"] == "REJECT" for row in payload["fixtures"])}


if __name__ == "__main__":
    print(json.dumps(evaluate_fixtures(), ensure_ascii=False, sort_keys=True, indent=2))
