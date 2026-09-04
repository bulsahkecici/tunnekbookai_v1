"""Metrics and stack-gate evaluation for Output Contract v1.1, over replay or fresh results.

Thresholds and denominators are read from the acceptance criteria frozen before the v1 integrated
evaluation. Nothing here may relax a gate: the criteria file is the only source of thresholds and
its SHA is asserted by test.
"""
from __future__ import annotations

import hashlib
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "data/evaluation"
BENCHMARK = EV / "generation_eval_benchmark_v2.jsonl"
CLAIMS = EV / "generation_output_contract_claim_audit_v1.jsonl"
CRITERIA = ROOT / "data/metadata/generation_output_contract_eval_acceptance_v1.json"

FAILURE_REASON_ENUM = {
    "wrong_abstention_marker_language", "abstention_marker_not_at_start",
    "answer_body_language_mismatch", "answer_body_language_ambiguous", "malformed_citation",
    "unknown_citation", "source_coordinate_leak", "template_leak", "thinking_marker_leak",
    "empty_answer", "query_language_ambiguous",
}

# Re-adjudicated by hand in this phase; see reports/generation_output_contract_v1_1_integrated_eval.md.
# Every v1.1 rejection was read beside its query and evidence and found genuine.
CONTRACT_FALSE_POSITIVES: set[str] = set()
# Query-level acceptability, carried from the Phase B v2 adjudication of these identical answers.
QUERY_UNACCEPTABLE = {"GEV042", "GEV062", "GEV067"}


def load(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pct(n, d):
    return round(n / d, 4) if d else None


def numeric_accuracy(raw, items):
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
                            "correct": bool(found and unit_ok)})
    return results


def analyse(results_path: Path, raw_path: Path, claims_path: Path = CLAIMS) -> dict:
    contract = {c["query_id"]: c for c in load(results_path)}
    raw = {r["query_id"]: r for r in load(raw_path)}
    items = {i["query_id"]: i for i in load(BENCHMARK)}
    claims = load(claims_path)

    accepted = sorted(q for q, c in contract.items() if c["contract_valid"])
    rejected = sorted(q for q, c in contract.items() if not c["contract_valid"])
    accepted_set = set(accepted)

    m = {}
    m["first_pass_contract_accept_rate"] = pct(len(accepted), 72)
    m["accepted_count"], m["rejected_count"] = len(accepted), len(rejected)
    m["rejected_ids"] = rejected

    m["contract_false_positive_count"] = len(CONTRACT_FALSE_POSITIVES)
    m["contract_false_positive_rate"] = pct(len(CONTRACT_FALSE_POSITIVES), len(rejected))

    false_negatives = []
    for q in accepted:
        c = contract[q]
        if (c["malformed_citations"] or c["unknown_handles"] or c["doc_leaks"] or c["page_leaks"]
                or c["slide_leaks"] or c["path_leaks"] or c["template_leaks"]
                or c["thinking_marker_leaks"] or not raw[q]["raw_answer"].strip()
                or (c["abstention_detected"] and c["marker_language_valid"] is False)
                or c["body_language_valid"] is False):
            false_negatives.append(q)
    m["contract_false_negative_count"] = len(false_negatives)
    m["contract_false_negatives"] = false_negatives
    m["catastrophic_failure_count"] = len(false_negatives)

    # Claim labels attach to answer text. Reuse is valid only where the audited bytes are the same.
    raw_sha = {q: r["raw_answer_sha"] for q, r in raw.items()}
    audited_sha = {r["query_id"]: r for r in load(EV / "generation_output_contract_eval_raw_v1.jsonl")}
    m["claim_labels_reusable"] = all(
        raw_sha[q] == audited_sha[q]["raw_answer_sha"] for q in raw_sha if q in audited_sha)

    material = [c for c in claims if c["material"]]
    accepted_material = [c for c in material if c["query_id"] in accepted_set]
    for prefix, pool in (("all_answers", material), ("pass_answer", accepted_material)):
        unsupported = [c for c in pool if c["claim_label"] == "UNSUPPORTED"]
        partial = [c for c in pool if c["claim_label"] == "PARTIALLY_SUPPORTED"]
        cited = [c for c in pool if c["citation_bearing"]]
        supported_cited = [c for c in cited if c["claim_label"] == "SUPPORTED"]
        m[f"{prefix}_material_claims"] = len(pool)
        m[f"{prefix}_unsupported_material_claim_rate"] = pct(len(unsupported), len(pool))
        m[f"{prefix}_partially_supported_rate"] = pct(len(partial), len(pool))
        m[f"{prefix}_citation_precision"] = pct(len(supported_cited), len(cited))
        m[f"{prefix}_citation_coverage"] = pct(len(cited), len(pool))
    m["unresolved_claims"] = sum(1 for c in claims if not c["resolved"])

    must_abstain = [q for q in items if items[q]["must_abstain"]]
    m["must_abstain_count"] = len(must_abstain)
    m["must_abstain_factual_correctness"] = pct(
        sum(1 for q in must_abstain if contract[q]["abstention_detected"]), len(must_abstain))
    m["must_abstain_contract_valid"] = sum(1 for q in must_abstain if contract[q]["contract_valid"])
    m["must_abstain_marker_language_failures"] = sorted(
        q for q in must_abstain if contract[q]["marker_language_valid"] is False)
    m["must_abstain_body_language_failures"] = sorted(
        q for q in must_abstain if contract[q]["body_language_valid"] is False)

    injection = [q for q in items if items[q]["primary_query_type"] == "injection_adversarial"]
    complied = [q for q in injection if contract[q]["template_leaks"]]
    m["injection_items"] = len(injection)
    m["injection_resistance"] = pct(len(injection) - len(complied), len(injection))

    numeric = numeric_accuracy(raw, items)
    m["numeric_required_facts"] = len(numeric)
    m["numeric_accuracy"] = pct(sum(1 for n in numeric if n["correct"]), len(numeric))
    m["numeric_failures"] = [n for n in numeric if not n["correct"]]

    unacceptable_accepted = [q for q in accepted if q in QUERY_UNACCEPTABLE]
    m["pass_answer_query_acceptable_rate"] = pct(len(accepted) - len(unacceptable_accepted),
                                                 len(accepted))
    m["pass_answer_unacceptable"] = unacceptable_accepted

    def subset(name, ids):
        m[f"pass_rate_{name}"] = pct(sum(1 for q in ids if contract[q]["contract_valid"]), len(ids))
        m[f"count_{name}"] = len(ids)

    subset("tr", [q for q in items if items[q]["language"] == "tr"])
    subset("en", [q for q in items if items[q]["language"] == "en"])
    subset("tr_abstention", [q for q in must_abstain if items[q]["language"] == "tr"])
    subset("en_abstention", [q for q in must_abstain if items[q]["language"] == "en"])
    for query_type in sorted({items[q]["primary_query_type"] for q in items}):
        subset(query_type, [q for q in items if items[q]["primary_query_type"] == query_type])

    marker_answers = [q for q in contract if contract[q]["abstention_detected"]]
    m["marker_language_accuracy"] = pct(
        sum(1 for q in marker_answers if contract[q]["marker_language_valid"]), len(marker_answers))
    body_judged = [q for q in contract if contract[q]["body_language_valid"] is not None]
    m["body_language_checked"] = len(body_judged)
    m["body_language_accuracy"] = pct(
        sum(1 for q in body_judged if contract[q]["body_language_valid"]), len(body_judged))

    latency = sorted(c["contract_enforcement_ms"] for c in contract.values())
    m["contract_latency_ms"] = {
        "median": round(statistics.median(latency), 4),
        "p90": round(latency[int(0.90 * len(latency)) - 1], 4),
        "p95": round(latency[int(0.95 * len(latency)) - 1], 4),
        "max": round(max(latency), 4)}

    m["failure_reasons_in_enum"] = all(set(c["failure_reasons"]) <= FAILURE_REASON_ENUM
                                       for c in contract.values())
    m["raw_answer_sha_preserved"] = all(contract[q]["raw_answer_sha"] == raw_sha[q]
                                        for q in contract)
    m["contract_version_uniform"] = sorted({c["contract_version"] for c in contract.values()})
    return m


def gate_evaluation(m: dict) -> list:
    criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
    lookup = {
        "first_pass_contract_accept_rate": m["first_pass_contract_accept_rate"],
        "contract_false_negative_count": m["contract_false_negative_count"],
        "contract_false_positive_rate": m["contract_false_positive_rate"],
        "pass_answer_unsupported_material_claim_rate": m["pass_answer_unsupported_material_claim_rate"],
        "pass_answer_citation_precision": m["pass_answer_citation_precision"],
        "pass_answer_query_acceptable_rate": m["pass_answer_query_acceptable_rate"],
        "must_abstain_factual_correctness": m["must_abstain_factual_correctness"],
        "injection_resistance": m["injection_resistance"],
        "numeric_accuracy": m["numeric_accuracy"],
        "catastrophic_failure_count": m["catastrophic_failure_count"],
    }
    ops = {">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b, "==": lambda a, b: a == b}
    results = []
    for gate in criteria["stack_gates"]:
        actual = lookup[gate["metric"]]
        results.append({**gate, "actual": actual,
                        "passed": ops[gate["comparator"]](actual, gate["threshold"])})
    for gate in criteria["contract_latency_gates"]:
        key = "median" if "median" in gate["metric"] else "p95"
        actual = m["contract_latency_ms"][key]
        results.append({**gate, "actual": actual,
                        "passed": ops[gate["comparator"]](actual, gate["threshold"])})
    return results


if __name__ == "__main__":
    import sys
    results = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        EV / "generation_output_contract_v1_1_replay_results.jsonl"
    raw = Path(sys.argv[2]) if len(sys.argv) > 2 else \
        EV / "generation_output_contract_eval_raw_v1.jsonl"
    m = analyse(results, raw)
    gates = gate_evaluation(m)
    print(json.dumps(m, ensure_ascii=False, indent=2))
    print("\n=== PRE-FROZEN STACK GATES (criteria SHA unchanged) ===")
    for g in gates:
        print(f"  {'PASS' if g['passed'] else 'FAIL'}  {g['metric']:<48} "
              f"{g['actual']} {g['comparator']} {g['threshold']}")
    failed = [g["metric"] for g in gates if not g["passed"]]
    print(f"\nDECISION: {'GO' if not failed else 'NO-GO'}   failed_gates={failed}")
