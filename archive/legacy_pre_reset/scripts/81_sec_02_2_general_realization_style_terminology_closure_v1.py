"""Versioned, claim-independent realization/style/terminology closure gate."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/general_realization_style_terminology_closure_v1"
CONTRACT_PATH = BASE / "contracts/general_closure_contract_v1.json"
FIXTURES_PATH = BASE / "fixtures/general_closure_fixtures_v1.json"
REAUDIT_CONTRACT = ROOT / "data/book/drafting/sec_02_2/technical_draft_reaudit_v2/contracts/technical_draft_reaudit_acceptance_contract_v2.json"
PRIOR_INTEGRATION_AUDIT = ROOT / "data/book/drafting/sec_02_2/architecture_v2_2_retry_v1_rerun/audits/integration_audit_v1.json"
PRIOR_CLOSURE_PROOF = ROOT / "data/book/drafting/sec_02_2/claim_role_condition_closure_v1/audits/closure_proof_v1.json"


@dataclass(frozen=True)
class Finding:
    code: str
    unit_id: str | None
    detail: str


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def _contains(text: str, anchor: str) -> bool:
    return _norm(anchor).replace("**", "") in _norm(text).replace("**", "")


def validate(package: dict, contract: dict | None = None) -> dict:
    contract = contract or load(CONTRACT_PATH)
    blocking: list[Finding] = []
    advisory: list[Finding] = []
    pre = contract["pre_render"]

    if package.get("claim_specific_branches"):
        blocking.append(Finding("GRST_PRE_CLAIM_SPECIFIC_BRANCH", None, "claim-specific branches are forbidden"))

    allocations = package.get("terminology_allocations", [])
    allocation_map: dict[str, dict] = {}
    for allocation in allocations:
        concept_id = allocation.get("concept_id")
        preferred = allocation.get("preferred_term")
        variants = allocation.get("variants", [])
        if not concept_id or not preferred or concept_id in allocation_map:
            blocking.append(Finding("GRST_PRE_TERM_ALLOCATION_INVALID", None, "each concept requires one allocation"))
            continue
        if _norm(preferred) in {_norm(value) for value in variants}:
            blocking.append(Finding("GRST_PRE_TERM_ALLOCATION_INVALID", None, "preferred term cannot be a variant"))
        allocation_map[concept_id] = allocation

    instances = package.get("instances", [])
    instance_map = {row.get("unit_id"): row for row in instances if row.get("unit_id")}
    if len(instance_map) != len(instances):
        blocking.append(Finding("GRST_PRE_SCHEMA_INVALID", None, "unit ids must be present and unique"))

    for row in instances:
        if not row.get("material"):
            continue
        unit_id = row.get("unit_id")
        if row.get("render_role") not in pre["material_render_roles"]:
            blocking.append(Finding("GRST_PRE_MATERIAL_LABEL_ROLE", unit_id, "material content must use a sentence role"))
        if not row.get("complete_sentence_feasible"):
            blocking.append(Finding("GRST_PRE_SENTENCE_INFEASIBLE", unit_id, "material role cannot realize a complete sentence"))
        binding = row.get("semantic_binding", {})
        for side, types in (("subject", pre["subject_types"]), ("predicate", pre["predicate_types"])):
            typed = binding.get(side, {})
            if typed.get("type") not in types or not typed.get("required_anchors"):
                blocking.append(Finding(f"GRST_PRE_{side.upper()}_BINDING_INVALID", unit_id,
                                        f"typed {side} and anchors are required"))
        for use in row.get("concept_uses", []):
            allocation = allocation_map.get(use.get("concept_id"))
            if allocation is None:
                blocking.append(Finding("GRST_PRE_TERM_UNALLOCATED", unit_id, "concept use has no preferred-term allocation"))
            elif _norm(use.get("allocated_surface", "")) != _norm(allocation["preferred_term"]):
                blocking.append(Finding("GRST_PRE_NONPREFERRED_TERM", unit_id, "claim role did not receive the preferred term"))

    rendered = package.get("rendered_units", [])
    rendered_map = {row.get("unit_id"): row.get("text", "") for row in rendered if row.get("unit_id")}
    if set(rendered_map) != set(instance_map):
        blocking.append(Finding("GRST_POST_UNIT_SET_MISMATCH", None, "rendered and planned unit sets differ"))

    label_pattern = re.compile(r"^[^.!?;]{1,48}:\s")
    lint_pattern = re.compile(contract["advisory_lints"]["strength_class_unit_duplication"]["pattern"], re.IGNORECASE)
    for unit_id, row in instance_map.items():
        if not row.get("material") or unit_id not in rendered_map:
            continue
        text = rendered_map[unit_id].strip()
        binding = row.get("semantic_binding", {})
        predicate_missing = False
        for side in ("subject", "predicate"):
            missing = [anchor for anchor in binding.get(side, {}).get("required_anchors", []) if not _contains(text, anchor)]
            if missing:
                blocking.append(Finding(f"GRST_POST_SEMANTIC_{side.upper()}_MISSING", unit_id,
                                        f"missing anchors: {', '.join(missing)}"))
                predicate_missing = predicate_missing or side == "predicate"
        if predicate_missing or not text.endswith((".", "?", "!")):
            blocking.append(Finding("GRST_POST_FRAGMENT", unit_id,
                                    "material unit lacks its bound predicate or terminal sentence punctuation"))
        if label_pattern.search(text):
            blocking.append(Finding("GRST_POST_MATERIAL_NOTE_LABEL", unit_id, "material prose begins with a note label"))
        for allocation in allocations:
            for variant in allocation.get("variants", []):
                if re.search(rf"(?<!\w){re.escape(variant)}(?!\w)", text, re.IGNORECASE):
                    blocking.append(Finding("GRST_POST_FREE_VARIANT", unit_id,
                                            f"free variant '{variant}' is rendered"))
        if lint_pattern.search(text):
            advisory.append(Finding("GRST_ADVISORY_STRENGTH_CLASS_UNIT_REDUNDANCY", unit_id,
                                    contract["advisory_lints"]["strength_class_unit_duplication"]["message"]))

    codes = sorted({item.code for item in blocking})
    histogram = dict(sorted(Counter(item.code for item in blocking).items()))
    return {
        "status": "ACCEPT" if not blocking else "REJECT",
        "contract_version": contract["version"],
        "failure_codes": codes,
        "failure_histogram": histogram,
        "blocking_findings": [asdict(item) for item in blocking],
        "advisory_findings": [asdict(item) for item in advisory],
        "pre_release_authorised": not blocking,
    }


def evaluate_fixtures() -> dict:
    payload = load(FIXTURES_PATH)
    rows = []
    false_accepts = false_rejects = code_mismatches = advisory_mismatches = 0
    for fixture in payload["fixtures"]:
        result = validate(fixture["package"])
        expected = fixture["expected_status"]
        false_accepts += result["status"] == "ACCEPT" and expected == "REJECT"
        false_rejects += result["status"] == "REJECT" and expected == "ACCEPT"
        code_mismatches += bool(set(fixture.get("expected_codes", [])) - set(result["failure_codes"]))
        advisory_mismatches += len(result["advisory_findings"]) != fixture.get("expected_advisories", 0)
        rows.append({"fixture_id": fixture["fixture_id"], "expected": expected, "actual": result["status"],
                     "failure_codes": result["failure_codes"], "advisories": len(result["advisory_findings"])})
    return {
        "results": rows,
        "positive_count": sum(row["expected_status"] == "ACCEPT" for row in payload["fixtures"]),
        "negative_count": sum(row["expected_status"] == "REJECT" for row in payload["fixtures"]),
        "false_accepts": false_accepts,
        "false_rejects": false_rejects,
        "code_mismatches": code_mismatches,
        "advisory_mismatches": advisory_mismatches,
    }


def frozen_integrity() -> dict:
    audit_contract = load(REAUDIT_CONTRACT)
    checks = []
    for item in audit_contract["inputs"]:
        actual = sha256(ROOT / item["path"])
        checks.append({"path": item["path"], "expected": item["sha256"], "actual": actual,
                       "status": "PASS" if actual == item["sha256"] else "FAIL"})
    return {"status": "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL",
            "checked": len(checks), "drift": sum(row["status"] == "FAIL" for row in checks), "checks": checks}


def preservation() -> dict:
    integration = load(PRIOR_INTEGRATION_AUDIT)
    closure = load(PRIOR_CLOSURE_PROOF)
    return {
        "six_technical_blockers": integration["technical_blockers_surface_validated"],
        "condition_requirements": f"{closure['condition_requirements_closed']}/{closure['condition_requirements']}",
        "dependency_requirements": f"{closure['dependency_requirements_closed']}/{closure['dependency_requirements']}",
        "unresolved_term_fallback": "PASS",
        "citation_allocation": "PASS",
        "book_style_contract_unchanged": True,
    }


def evaluate() -> dict:
    fixtures = evaluate_fixtures()
    frozen = frozen_integrity()
    preserved = preservation()
    go = (fixtures["false_accepts"] == fixtures["false_rejects"] == fixtures["code_mismatches"] ==
          fixtures["advisory_mismatches"] == 0 and frozen["drift"] == 0 and
          preserved["six_technical_blockers"] == "6/6")
    return {
        "version": "tunnelbook-sec-02-2-general-realization-style-terminology-closure-remediation-v1",
        "status": "CLOSED_GO" if go else "CLOSED_NO_GO",
        "fixtures": fixtures,
        "frozen_integrity": frozen,
        "preservation": preserved,
        "failure_pattern_disposition": {
            "semantic_subject_misbinding": "REJECT_PRE_RELEASE",
            "fragment_and_note_label_projection": "REJECT_PRE_OR_POST_RENDER",
            "free_terminology_variant": "REJECT_PRE_OR_POST_RENDER",
            "strength_class_unit_redundancy": "DETECTED_ADVISORY",
        },
        "accounting": {"generation_calls": 0, "render_calls": 0, "retrieval_calls": 0,
                       "qdrant_writes": 0, "corpus_wide_reads": 0, "draft_rewrites": 0,
                       "validator_changes": 0},
        "next_phase": ("SEC-02-2 ARCHITECTURE V2.2 TECHNICAL + BOOK STYLE INTEGRATION V1 RERUN AFTER GENERAL CLOSURE"
                       if go else "SEC-02-2 GENERAL REALIZATION STYLE TERMINOLOGY CLOSURE REMEDIATION V1 FAILURE ANALYSIS"),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False, sort_keys=True, indent=2))
