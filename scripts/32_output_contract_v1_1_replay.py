"""Phase A - contract-only replay of the frozen 72 raw answers under Output Contract v1.1.

The generator, prompt, benchmark, packets and generation config are all unchanged since the v1
integrated evaluation; the only component that moved is the contract. Replaying the identical raw
answers therefore isolates the contract delta exactly, with no generation variance mixed in.

Raw answers are read-only here. Nothing is regenerated, retrieved, translated or repaired.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "data/evaluation"
RAW = EV / "generation_output_contract_eval_raw_v1.jsonl"
V1_RESULTS = EV / "generation_output_contract_eval_results_v1.jsonl"
BENCHMARK = EV / "generation_eval_benchmark_v2.jsonl"
REPLAY = EV / "generation_output_contract_v1_1_replay_results.jsonl"

BENCHMARK_SHA = "1e6347b557d583b56882c4c05fd1c5453874b7a05e61205c9430a24a677b0cff"
PACKET_SHA = "0538705147cf543b45fe8e73d57828cbc341a9a5a1dd574bd0969a9326e54d7a"
PROMPT_V5_SHA = "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085"
CONTRACT_V1_SHA = "670031d116056485155fc9d5c3d12b472d91f6b1e7a34ed9b169166f3727ce7d"
CONTRACT_V1_1_SHA = "5ebf8fe90e3e5491ce07a9143f8fd377841defa2e0e7a09188f3a835b07bdef5"
CRITERIA_SHA = "2a46ed2147ec24dd4a1944e23a1b1a458cfe1997edd13773eaf66692f417b6f8"
TOKENIZER_SHA = "87a7830d63fcf43bf241c3c5242e96e62dd3fdc29224ca26fed8ea333db72de4"
TEMPLATE_SHA = "e84f32a23fdda27689f868aa4a1a5621f41133e51a48d7f3efcbea2839574259"
GENERATION_CONFIG_HASH = "35d7ebb6ce531f8bb385b402759d789fd106f66d48ec9bba82d23753d4f883e0"

NON_LANGUAGE_FIELDS = [
    "malformed_citations", "unknown_handles", "citation_syntax_valid", "doc_leaks", "page_leaks",
    "slide_leaks", "path_leaks", "template_leaks", "thinking_marker_leaks", "material_claim_count",
    "claims_with_citation", "citation_coverage", "citation_coverage_status", "abstention_detected",
    "actual_abstention_marker", "marker_at_start", "expected_abstention_marker",
    "marker_language_valid", "validator_version", "repair_policy", "raw_answer_sha",
]


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


v11 = _load("output_contract_v1_1", "scripts/31_generation_output_contract_v1_1.py")
v1 = v11.v1


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qdrant_points(collection="tunnelbook_dense_v1"):
    with urllib.request.urlopen(
            f"http://localhost:6333/collections/{collection}", timeout=10) as response:
        result = json.loads(response.read())["result"]
    return result["points_count"], result["status"]


def preflight() -> dict:
    checks, failures = {}, []

    def check(name, actual, expected):
        ok = actual == expected
        checks[name] = {"expected": expected, "actual": actual, "ok": ok}
        if not ok:
            failures.append(name)

    check("benchmark_v2_sha", sha(BENCHMARK), BENCHMARK_SHA)
    check("packet_artifact_sha", sha(EV / "generation_eval_benchmark_v2_packets.jsonl"), PACKET_SHA)
    check("system_prompt_v5_sha", sha(ROOT / "data/metadata/generation_system_prompt_v5.txt"),
          PROMPT_V5_SHA)
    check("contract_v1_sha", sha(ROOT / "scripts/26_generation_output_contract.py"),
          CONTRACT_V1_SHA)
    check("contract_v1_1_sha", sha(ROOT / "scripts/31_generation_output_contract_v1_1.py"),
          CONTRACT_V1_1_SHA)
    check("acceptance_criteria_sha",
          sha(ROOT / "data/metadata/generation_output_contract_eval_acceptance_v1.json"),
          CRITERIA_SHA)

    meta = json.loads((ROOT / "data/metadata/generation_output_contract_v1_1.json")
                      .read_text(encoding="utf-8"))
    check("v1_1_metadata_status", meta["status"], "frozen")
    check("v1_1_metadata_sha", meta["implementation_sha"], CONTRACT_V1_1_SHA)
    check("v1_1_parent_sha", meta["parent_contract_sha"], CONTRACT_V1_SHA)
    check("validator_version", v11.VALIDATOR_VERSION, "citation-validator-v1.2")
    check("repair_policy", v11.REPAIR_POLICY, "none_fail_closed")
    check("marker_mapping", v11.MARKER_FOR_LANGUAGE,
          {"tr": "YETERSİZ KANIT", "en": "INSUFFICIENT EVIDENCE"})
    check("no_prompt_v6", (ROOT / "data/metadata/generation_system_prompt_v6.txt").exists(), False)

    raw = [json.loads(l) for l in RAW.read_text(encoding="utf-8").splitlines() if l.strip()]
    check("raw_rows", len(raw), 72)
    check("raw_answer_sha_intact",
          all(hashlib.sha256(r["raw_answer"].encode("utf-8")).hexdigest() == r["raw_answer_sha"]
              for r in raw), True)
    check("raw_benchmark_sha", {r["benchmark_sha"] for r in raw}, {BENCHMARK_SHA})
    check("raw_packet_sha", {r["packet_artifact_sha"] for r in raw}, {PACKET_SHA})
    check("raw_prompt_sha", {r["system_prompt_sha"] for r in raw}, {PROMPT_V5_SHA})
    check("raw_generation_config_hash", {r["generation_config_hash"] for r in raw},
          {GENERATION_CONFIG_HASH})
    check("raw_tokenizer_sha", {r["checkpoint_identity"]["tokenizer_sha"] for r in raw},
          {TOKENIZER_SHA})
    check("raw_template_sha", {r["checkpoint_identity"]["template_sha"] for r in raw},
          {TEMPLATE_SHA})

    points, status = qdrant_points()
    check("qdrant_points", points, 5992)
    check("qdrant_status", status, "green")
    return {"checks": checks, "failures": failures, "go": not failures,
            "qdrant_points_before": points}


def replay() -> dict:
    raw = {r["query_id"]: r for r in
           (json.loads(l) for l in RAW.read_text(encoding="utf-8").splitlines() if l.strip())}
    items = {i["query_id"]: i for i in
             (json.loads(l) for l in BENCHMARK.read_text(encoding="utf-8").splitlines() if l.strip())}
    historical = {c["query_id"]: c for c in
                  (json.loads(l) for l in V1_RESULTS.read_text(encoding="utf-8").splitlines()
                   if l.strip())}

    rows, deltas, drift = [], [], []
    for query_id in sorted(raw):
        row = raw[query_id]
        item = items[query_id]
        answer = row["raw_answer"]

        began = time.perf_counter()
        verdict = v11.enforce(answer, item["language"], set(item["evidence_ids"]),
                              answerability=item["answerability"])
        elapsed_ms = (time.perf_counter() - began) * 1000.0

        if verdict.raw_answer_sha != row["raw_answer_sha"]:
            raise SystemExit(f"{query_id}: contract saw a different answer than was frozen")

        old = historical[query_id]
        new = verdict.to_dict()
        changed = [f for f in NON_LANGUAGE_FIELDS if old[f] != new[f]]
        if changed:
            drift.append({"query_id": query_id, "fields": changed,
                          "v1": {f: old[f] for f in changed}, "v1_1": {f: new[f] for f in changed}})
        if old["contract_valid"] != verdict.contract_valid or \
                sorted(old["failure_reasons"]) != sorted(verdict.failure_reasons):
            deltas.append({"query_id": query_id,
                           "v1_contract_valid": old["contract_valid"],
                           "v1_1_contract_valid": verdict.contract_valid,
                           "v1_failure_reasons": old["failure_reasons"],
                           "v1_1_failure_reasons": verdict.failure_reasons,
                           "v1_body_language": old["answer_body_language"],
                           "v1_1_body_language": verdict.answer_body_language,
                           "decision_change": ("reject_to_accept"
                                               if verdict.contract_valid and not old["contract_valid"]
                                               else "accept_to_reject"
                                               if old["contract_valid"] and not verdict.contract_valid
                                               else "reasons_only")})

        rows.append({"query_id": query_id, **new,
                     "contract_enforcement_ms": round(elapsed_ms, 4),
                     "language": item["language"], "must_abstain": item["must_abstain"],
                     "primary_query_type": item["primary_query_type"],
                     "context_token_count": row["context_token_count"],
                     "v1_contract_valid": old["contract_valid"],
                     "v1_failure_reasons": old["failure_reasons"],
                     "v1_answer_body_language": old["answer_body_language"]})

    REPLAY.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                      encoding="utf-8")
    return {"rows": rows, "deltas": deltas, "drift": drift}


if __name__ == "__main__":
    pre = preflight()
    for name, c in pre["checks"].items():
        print(f"  {'OK  ' if c['ok'] else 'FAIL'} {name:<32} {str(c['actual'])[:56]}")
    if not pre["go"]:
        print(f"\nHARD PREFLIGHT: STOP — {pre['failures']}")
        raise SystemExit(1)
    print("\nHARD PREFLIGHT: GO\n")

    result = replay()
    rows, deltas, drift = result["rows"], result["deltas"], result["drift"]
    accepted = [r for r in rows if r["contract_valid"]]
    print(f"REPLAY COMPLETE rows={len(rows)} accepted={len(accepted)} "
          f"rate={len(accepted)/72:.4f}")
    print(f"\nDECISION DELTAS ({len(deltas)}):")
    for d in deltas:
        print(f"  {d['query_id']} {d['decision_change']:<18} "
              f"v1={d['v1_failure_reasons']} -> v1.1={d['v1_1_failure_reasons']}")
    print(f"\nNON-LANGUAGE SEMANTIC DRIFT: {len(drift)}")
    for d in drift:
        print(f"  {d['query_id']} {d['fields']}")
    print(f"\nREJECTED under v1.1: {sorted(r['query_id'] for r in rows if not r['contract_valid'])}")
    raise SystemExit(0 if len(rows) == 72 else 1)
