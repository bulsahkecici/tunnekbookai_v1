"""Metrics, first-pass deployment simulation and integrity manifest for the integrated evaluation.

Every rate here is computed against a denominator frozen in
data/metadata/generation_output_contract_eval_acceptance_v1.json before the first model call.
Nothing in this file may change a threshold.
"""
from __future__ import annotations

import hashlib
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "data/evaluation"
RAW = EV / "generation_output_contract_eval_raw_v1.jsonl"
CONTRACT = EV / "generation_output_contract_eval_results_v1.jsonl"
CLAIMS = EV / "generation_output_contract_claim_audit_v1.jsonl"
FIRST_PASS = EV / "generation_output_contract_first_pass_v1.jsonl"
RETRY = EV / "generation_output_contract_retry_same_config_v1.jsonl"
BENCHMARK = EV / "generation_eval_benchmark_v2.jsonl"
CRITERIA = ROOT / "data/metadata/generation_output_contract_eval_acceptance_v1.json"
MANIFEST = EV / "generation_output_contract_eval_manifest_v1.json"

FAILURE_REASON_ENUM = {
    "wrong_abstention_marker_language", "abstention_marker_not_at_start",
    "answer_body_language_mismatch", "answer_body_language_ambiguous", "malformed_citation",
    "unknown_citation", "source_coordinate_leak", "template_leak", "thinking_marker_leak",
    "empty_answer", "query_language_ambiguous",
}

# Adjudicated by hand in this phase; see reports/generation_output_contract_integrated_eval_v1.md.
CONTRACT_FALSE_POSITIVES = {"GEV018"}
QUERY_UNACCEPTABLE = {"GEV042", "GEV062", "GEV067"}


def load(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pct(n, d):
    return round(n / d, 4) if d else None


def numeric_accuracy(raw, items):
    """A required numeric fact counts as correct when its gold value appears with its unit."""
    results = []
    for query_id, item in sorted(items.items()):
        for gold in item.get("numeric_gold") or []:
            answer = raw[query_id]["raw_answer"]
            value = str(gold["value"])
            variants = {value, value.replace(".", ","), value.replace(",", ".")}
            found = any(re.search(rf"(?<![\d.,]){re.escape(v)}(?![\d])", answer) for v in variants)
            unit = (gold.get("unit") or "").strip()
            unit_ok = (not unit) or re.search(re.escape(unit), answer, re.I) is not None
            results.append({"query_id": query_id, "value": value, "unit": unit,
                            "value_found": found, "unit_found": bool(unit_ok),
                            "correct": bool(found and unit_ok)})
    return results


def main():
    raw = {r["query_id"]: r for r in load(RAW)}
    contract = {c["query_id"]: c for c in load(CONTRACT)}
    claims = load(CLAIMS)
    items = {i["query_id"]: i for i in load(BENCHMARK)}
    criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))

    accepted = sorted(q for q, c in contract.items() if c["contract_valid"])
    rejected = sorted(q for q, c in contract.items() if not c["contract_valid"])

    # ---- first-pass deployment simulation (no auto-fix of any kind)
    FIRST_PASS.write_text("".join(json.dumps({
        "query_id": q, "contract_valid": contract[q]["contract_valid"],
        "production_action": "accept" if contract[q]["contract_valid"] else "reject",
        "failure_reasons": contract[q]["failure_reasons"]}, ensure_ascii=False) + "\n"
        for q in sorted(contract)), encoding="utf-8")

    metrics = {}
    metrics["first_pass_contract_accept_rate"] = pct(len(accepted), 72)
    metrics["accepted_count"], metrics["rejected_count"] = len(accepted), len(rejected)

    # ---- false positives / negatives
    metrics["contract_false_positive_count"] = len(CONTRACT_FALSE_POSITIVES)
    metrics["contract_false_positive_rate"] = pct(len(CONTRACT_FALSE_POSITIVES), len(rejected))
    false_negatives = []
    for q in accepted:
        c = contract[q]
        if (c["malformed_citations"] or c["unknown_handles"] or c["doc_leaks"] or c["page_leaks"]
                or c["slide_leaks"] or c["path_leaks"] or c["template_leaks"]
                or c["thinking_marker_leaks"] or not raw[q]["raw_answer"].strip()
                or (c["abstention_detected"] and c["marker_language_valid"] is False)
                or c["body_language_valid"] is False):
            false_negatives.append(q)
    metrics["contract_false_negative_count"] = len(false_negatives)
    metrics["contract_false_negatives"] = false_negatives

    # ---- claim-level grounding
    material = [c for c in claims if c["material"]]
    accepted_material = [c for c in material if c["contract_valid_for_answer"]]
    for label, prefix, pool in (("all", "all_answers", material),
                                ("pass", "pass_answer", accepted_material)):
        unsupported = [c for c in pool if c["claim_label"] == "UNSUPPORTED"]
        partial = [c for c in pool if c["claim_label"] == "PARTIALLY_SUPPORTED"]
        cited = [c for c in pool if c["citation_bearing"]]
        supported_cited = [c for c in cited if c["claim_label"] == "SUPPORTED"]
        metrics[f"{prefix}_material_claims"] = len(pool)
        metrics[f"{prefix}_unsupported_material_claim_rate"] = pct(len(unsupported), len(pool))
        metrics[f"{prefix}_partially_supported_rate"] = pct(len(partial), len(pool))
        metrics[f"{prefix}_citation_precision"] = pct(len(supported_cited), len(cited))
        metrics[f"{prefix}_citation_coverage"] = pct(len(cited), len(pool))
    metrics["unresolved_claims"] = sum(1 for c in claims if not c["resolved"])

    # ---- must-abstain, injection, numeric, acceptability
    must_abstain = [q for q in items if items[q]["must_abstain"]]
    correct_abstentions = [q for q in must_abstain if contract[q]["abstention_detected"]]
    metrics["must_abstain_count"] = len(must_abstain)
    metrics["must_abstain_factual_correctness"] = pct(len(correct_abstentions), len(must_abstain))
    metrics["must_abstain_contract_valid"] = sum(1 for q in must_abstain if contract[q]["contract_valid"])
    metrics["must_abstain_marker_language_failures"] = sorted(
        q for q in must_abstain if contract[q]["marker_language_valid"] is False)
    metrics["must_abstain_body_language_failures"] = sorted(
        q for q in must_abstain if contract[q]["body_language_valid"] is False)

    injection = [q for q in items if (items[q].get("injection_metadata") or {}).get("injection_present")]
    injection_all = [q for q in items if items[q]["primary_query_type"] == "injection_adversarial"]
    complied = [q for q in injection_all if contract[q]["template_leaks"]]
    metrics["injection_items"] = len(injection_all)
    metrics["injection_with_payload"] = len(injection)
    metrics["injection_compliance_count"] = len(complied)
    metrics["injection_resistance"] = pct(len(injection_all) - len(complied), len(injection_all))

    numeric = numeric_accuracy(raw, items)
    metrics["numeric_required_facts"] = len(numeric)
    metrics["numeric_accuracy"] = pct(sum(1 for n in numeric if n["correct"]), len(numeric))
    metrics["numeric_failures"] = [n for n in numeric if not n["correct"]]

    unacceptable_accepted = [q for q in accepted if q in QUERY_UNACCEPTABLE]
    metrics["pass_answer_query_acceptable_rate"] = pct(
        len(accepted) - len(unacceptable_accepted), len(accepted))
    metrics["pass_answer_unacceptable"] = unacceptable_accepted

    # ---- subsets
    def subset(name, ids):
        ok = sum(1 for q in ids if contract[q]["contract_valid"])
        metrics[f"pass_rate_{name}"] = pct(ok, len(ids))
        metrics[f"count_{name}"] = len(ids)

    subset("tr", [q for q in items if items[q]["language"] == "tr"])
    subset("en", [q for q in items if items[q]["language"] == "en"])
    subset("tr_abstention", [q for q in must_abstain if items[q]["language"] == "tr"])
    subset("en_abstention", [q for q in must_abstain if items[q]["language"] == "en"])
    for query_type in sorted({items[q]["primary_query_type"] for q in items}):
        subset(query_type, [q for q in items if items[q]["primary_query_type"] == query_type])

    marker_answers = [q for q in contract if contract[q]["abstention_detected"]]
    metrics["marker_language_accuracy"] = pct(
        sum(1 for q in marker_answers if contract[q]["marker_language_valid"]), len(marker_answers))
    body_judged = [q for q in contract if contract[q]["body_language_valid"] is not None]
    metrics["body_language_accuracy_as_measured"] = pct(
        sum(1 for q in body_judged if contract[q]["body_language_valid"]), len(body_judged))

    # ---- context quartiles (descriptive only; no causal claim)
    by_context = sorted(contract, key=lambda q: contract[q]["context_token_count"])
    quartiles = [by_context[i::4] for i in range(4)]
    quartiles = [by_context[i * 18:(i + 1) * 18] for i in range(4)]
    metrics["context_quartiles"] = [
        {"quartile": i + 1,
         "min_tokens": min(contract[q]["context_token_count"] for q in group),
         "max_tokens": max(contract[q]["context_token_count"] for q in group),
         "accept_rate": pct(sum(1 for q in group if contract[q]["contract_valid"]), len(group)),
         "rejected": sorted(q for q in group if not contract[q]["contract_valid"])}
        for i, group in enumerate(quartiles)]

    # ---- latency
    enforcement = sorted(c["contract_enforcement_ms"] for c in contract.values())
    metrics["contract_latency_ms"] = {
        "median": round(statistics.median(enforcement), 4),
        "p90": round(enforcement[int(0.90 * len(enforcement)) - 1], 4),
        "p95": round(enforcement[int(0.95 * len(enforcement)) - 1], 4),
        "max": round(max(enforcement), 4)}
    generation = sorted(r["latency_seconds"] for r in raw.values())
    metrics["generation_latency_seconds"] = {
        "median": round(statistics.median(generation), 3), "max": round(max(generation), 3),
        "total": round(sum(generation), 1)}

    # ---- integrity
    metrics["prompt_token_delta_max"] = max(abs(r["prompt_token_delta"]) for r in raw.values())
    metrics["raw_answer_sha_preserved"] = all(
        c["raw_answer_sha"] == c["raw_answer_sha_before_contract"] for c in contract.values())
    metrics["failure_reasons_in_enum"] = all(
        set(c["failure_reasons"]) <= FAILURE_REASON_ENUM for c in contract.values())
    metrics["finish_reasons"] = sorted({r["finish_reason"] for r in raw.values()})

    return metrics, accepted, rejected


def gate_evaluation(metrics):
    """Evaluate the pre-frozen hard gates. Thresholds come from the frozen criteria file only."""
    criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
    lookup = {
        "first_pass_contract_accept_rate": metrics["first_pass_contract_accept_rate"],
        "contract_false_negative_count": metrics["contract_false_negative_count"],
        "contract_false_positive_rate": metrics["contract_false_positive_rate"],
        "pass_answer_unsupported_material_claim_rate": metrics["pass_answer_unsupported_material_claim_rate"],
        "pass_answer_citation_precision": metrics["pass_answer_citation_precision"],
        "pass_answer_query_acceptable_rate": metrics["pass_answer_query_acceptable_rate"],
        "must_abstain_factual_correctness": metrics["must_abstain_factual_correctness"],
        "injection_resistance": metrics["injection_resistance"],
        "numeric_accuracy": metrics["numeric_accuracy"],
        "catastrophic_failure_count": metrics["contract_false_negative_count"],
    }
    ops = {">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b, "==": lambda a, b: a == b}
    results = []
    for gate in criteria["stack_gates"]:
        actual = lookup[gate["metric"]]
        passed = ops[gate["comparator"]](actual, gate["threshold"])
        results.append({**gate, "actual": actual, "passed": passed})
    for gate in criteria["contract_latency_gates"]:
        key = "median" if "median" in gate["metric"] else "p95"
        actual = metrics["contract_latency_ms"][key]
        results.append({**gate, "actual": actual,
                        "passed": ops[gate["comparator"]](actual, gate["threshold"])})
    return results


def write_manifest(metrics):
    retry = load(RETRY) if RETRY.exists() else []
    manifest = {
        "phase": "output-contract-integrated frozen benchmark v2 re-evaluation",
        "benchmark_v2_sha": sha(BENCHMARK),
        "packet_artifact_sha": sha(EV / "generation_eval_benchmark_v2_packets.jsonl"),
        "system_prompt_v5_sha": sha(ROOT / "data/metadata/generation_system_prompt_v5.txt"),
        "output_contract_sha": sha(ROOT / "scripts/26_generation_output_contract.py"),
        "output_contract_version": "tunnelbook-generation-output-contract-v1",
        "validator_version": "citation-validator-v1.2",
        "repair_policy": "none_fail_closed",
        "model_id": "qwen3.6-35b-a3b-mlx",
        "tokenizer_sha": "87a7830d63fcf43bf241c3c5242e96e62dd3fdc29224ca26fed8ea333db72de4",
        "template_sha": "e84f32a23fdda27689f868aa4a1a5621f41133e51a48d7f3efcbea2839574259",
        "generation_config_hash": load(RAW)[0]["generation_config_hash"],
        "acceptance_criteria_sha": sha(CRITERIA),
        "raw_result_sha": sha(RAW),
        "contract_result_sha": sha(CONTRACT),
        "claim_audit_sha": sha(CLAIMS),
        "claim_manual_adjudication_sha": sha(EV / "generation_output_contract_claim_manual_v1.json"),
        "first_pass_sha": sha(FIRST_PASS),
        "retry_sha": sha(RETRY) if RETRY.exists() else None,
        "analysis_script_sha": sha(ROOT / "scripts/29_output_contract_eval_analysis.py"),
        "execution_script_sha": sha(ROOT / "scripts/27_output_contract_integrated_eval.py"),
        "claim_audit_script_sha": sha(ROOT / "scripts/28_output_contract_claim_audit.py"),
        "retry_script_sha": sha(ROOT / "scripts/30_output_contract_retry_same_config.py"),
        "result_counts": {
            "raw_rows": len(load(RAW)), "contract_rows": len(load(CONTRACT)),
            "first_pass_rows": len(load(FIRST_PASS)), "claim_rows": len(load(CLAIMS)),
            "retry_rows": len(retry), "accepted": metrics["accepted_count"],
            "rejected": metrics["rejected_count"]},
        "execution_start": min(r["started_at"] for r in load(RAW)),
        "execution_end": max(r["completed_at"] for r in load(RAW)),
        "qdrant_points_before": 5992, "qdrant_points_after": 5992, "qdrant_writes": 0,
        "no_repair_assertion": metrics["raw_answer_sha_preserved"],
        "prompt_token_delta_max": metrics["prompt_token_delta_max"],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    metrics, accepted, rejected = main()
    gates = gate_evaluation(metrics)
    manifest = write_manifest(metrics)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    print(f"\nREJECTED: {rejected}")
    print("\n=== PRE-FROZEN GATES ===")
    for g in gates:
        mark = "PASS" if g["passed"] else "FAIL"
        print(f"  {mark}  {g['metric']:<48} {g['actual']} {g['comparator']} {g['threshold']}")
    failed = [g["metric"] for g in gates if not g["passed"]]
    print(f"\nSTACK DECISION: {'GO' if not failed else 'NO-GO'}  failed_gates={failed}")
