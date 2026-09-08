"""Production orchestration smoke run.

This validates the ORCHESTRATION, not the model. It checks that the canonical entrypoint wires
Retriever v1, Context v1, Prompt v5, the generator and Output Contract v1.1 together correctly,
that decisions are recorded immutably, and above all that a contract-invalid answer is never
released. No generalisation metric may be claimed from 16 cases.

The two contract-failure cases inject a frozen fixture answer at the generation boundary so the
reject path runs deterministically. The injection is test-time only: the orchestrator itself has no
answer-injection parameter, so no production backdoor is created.
"""
from __future__ import annotations

import contextlib
import importlib.util
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "data/evaluation"
SMOKE = EV / "production_orchestration_smoke_v1.jsonl"
REPORT = ROOT / "data/production/orchestration_smoke_report_v1.json"


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


orch = _load("production_generator", "scripts/36_production_grounded_generator.py")


@contextlib.contextmanager
def fixture_answer(text: str):
    """Substitute the generation call for one request. Test-time only."""
    original = orch.gen.complete
    orch.gen.complete = lambda prompt, config, max_tokens, **kw: {
        "text": text, "finish_reason": "stop",
        "usage": {"prompt_tokens": orch.gen.GenerationTokenizer().count(prompt),
                  "completion_tokens": 0},
        "latency_seconds": 0.0}
    try:
        yield
    finally:
        orch.gen.complete = original


def main() -> int:
    cases = [json.loads(l) for l in SMOKE.read_text(encoding="utf-8").splitlines() if l.strip()]
    runtime = orch.ProductionGroundedGenerator()

    audit_before = sum(1 for _ in orch.AUDIT_LOG.open(encoding="utf-8")) if orch.AUDIT_LOG.exists() else 0
    qdrant_before = orch.qdrant_collection_state()

    rows, failures = [], []
    for case in cases:
        request = orch.ProductionGenerationRequest(
            query=case["query"], query_language=case["query_language"])
        began = time.perf_counter()
        if case["mode"] == "fixture":
            with fixture_answer(case["fixture_raw_answer"]):
                result = runtime.generate(request)
        else:
            result = runtime.generate(request)
        elapsed = time.perf_counter() - began

        checks = {}
        checks["completed"] = result.status in ("accepted", "rejected")
        checks["audit_id_present"] = bool(result.audit_id)
        checks["request_id_present"] = bool(result.request_id)
        checks["context_packet_sha_present"] = bool(result.context_packet_sha)
        public = result.to_public_dict()
        if result.status == "accepted":
            checks["answer_released"] = bool(result.answer)
            checks["visible_handles_present"] = bool(result.evidence_handles)
            checks["handles_canonical"] = all(
                h.startswith("E") and h[1:].isdigit() and len(h) == 4
                for h in result.evidence_handles)
            checks["no_safe_message"] = public.get("safe_message") is None
        else:
            checks["raw_answer_not_released"] = result.answer is None and "answer" not in public
            checks["safe_message_present"] = bool(result.safe_message)
            checks["safe_message_is_canonical"] = (
                result.safe_message == orch.SAFE_REJECT_MESSAGE[case["query_language"]])
            checks["failure_reasons_present"] = bool(result.failure_reasons)
            checks["no_fabricated_replacement"] = public.get("answer") is None

        if case["mode"] == "fixture":
            checks["expected_status"] = result.status == case["expected_status"]
            checks["expected_reasons"] = (sorted(result.failure_reasons)
                                          == sorted(case["expected_failure_reasons"]))

        passed = all(checks.values())
        if not passed:
            failures.append({"case_id": case["case_id"],
                             "failed": [k for k, v in checks.items() if not v]})
        rows.append({"case_id": case["case_id"], "group": case["group"], "mode": case["mode"],
                     "status": result.status, "failure_reasons": result.failure_reasons,
                     "evidence_handles": result.evidence_handles,
                     "latency": result.latency, "wall_seconds": round(elapsed, 3),
                     "checks": checks, "passed": passed})
        print(f"  {'PASS' if passed else 'FAIL'} {case['case_id']:<8} {case['group']:<28} "
              f"{result.status:<9} {result.failure_reasons}", flush=True)

    qdrant_after = orch.qdrant_collection_state()
    audit_after = sum(1 for _ in orch.AUDIT_LOG.open(encoding="utf-8"))

    def stat(key, source="latency"):
        values = [r[source][key] for r in rows if key in r[source]]
        if not values:
            return None
        ordered = sorted(values)
        return {"median": round(statistics.median(ordered), 4),
                "p90": round(ordered[max(0, int(0.9 * len(ordered)) - 1)], 4),
                "max": round(max(ordered), 4)}

    summary = {
        "cases": len(rows), "passed": sum(1 for r in rows if r["passed"]),
        "failed": len(failures), "failures": failures,
        "accepted": sum(1 for r in rows if r["status"] == "accepted"),
        "rejected": sum(1 for r in rows if r["status"] == "rejected"),
        "contract_failures_released": sum(
            1 for r in rows if r["status"] == "rejected" and not r["checks"].get(
                "raw_answer_not_released", False)),
        "audit_rows_appended": audit_after - audit_before,
        "qdrant_before": {"points": qdrant_before[0], "status": qdrant_before[1]},
        "qdrant_after": {"points": qdrant_after[0], "status": qdrant_after[1]},
        "qdrant_writes": qdrant_after[0] - qdrant_before[0],
        "performance": {"retrieval_and_context": stat("retrieval_and_context_seconds"),
                        "prompt_render": stat("prompt_render_seconds"),
                        "generation": stat("generation_seconds"),
                        "contract": stat("contract_seconds"),
                        "total": stat("total_seconds")},
        "rows": rows,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nSMOKE {summary['passed']}/{summary['cases']} PASS  "
          f"accepted={summary['accepted']} rejected={summary['rejected']}  "
          f"contract_failures_released={summary['contract_failures_released']}  "
          f"audit_rows=+{summary['audit_rows_appended']}  "
          f"qdrant {qdrant_before[0]}->{qdrant_after[0]} writes={summary['qdrant_writes']}")
    return 0 if summary["failed"] == 0 and summary["qdrant_writes"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
