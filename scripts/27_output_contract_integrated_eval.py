"""Output-contract-integrated frozen benchmark v2 re-evaluation.

Executes the frozen 72-query benchmark under unchanged system prompt v5, then applies frozen
Output Contract v1 to every raw answer. Raw answers are immutable: the contract never sees a
transformed input and no artifact carries a rewritten answer field.

Retrieval is never re-run. Every item is answered from the packet frozen at authoring time,
matched by packet SHA, and each checkpoint row carries the full frozen identity so a run mixing
benchmark, prompt or contract versions cannot resume silently.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "data/evaluation/generation_eval_benchmark_v2.jsonl"
PACKETS = ROOT / "data/evaluation/generation_eval_benchmark_v2_packets.jsonl"
RAW = ROOT / "data/evaluation/generation_output_contract_eval_raw_v1.jsonl"
CONTRACT_RESULTS = ROOT / "data/evaluation/generation_output_contract_eval_results_v1.jsonl"
CRITERIA = ROOT / "data/metadata/generation_output_contract_eval_acceptance_v1.json"

BENCHMARK_SHA = "1e6347b557d583b56882c4c05fd1c5453874b7a05e61205c9430a24a677b0cff"
PACKET_ARTIFACT_SHA = "0538705147cf543b45fe8e73d57828cbc341a9a5a1dd574bd0969a9326e54d7a"
PROMPT_V5_SHA = "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085"
CONTRACT_SHA = "670031d116056485155fc9d5c3d12b472d91f6b1e7a34ed9b169166f3727ce7d"
TOKENIZER_SHA = "87a7830d63fcf43bf241c3c5242e96e62dd3fdc29224ca26fed8ea333db72de4"
TEMPLATE_SHA = "e84f32a23fdda27689f868aa4a1a5621f41133e51a48d7f3efcbea2839574259"
RETRIEVER_SCRIPT_SHA = "8ada31f64d8ef51c3b4d3b8b04f3fcc3e9fb7338b1554d1a5a9118a3a231b071"
QDRANT_POINTS = 5992

SYSTEM_PROMPT_VERSION = "v5"
MAX_TOKENS, SEED, TEMPERATURE = 3072, 11, 0.0


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gen = _load("generation_eval", "scripts/21_generation_model_eval.py")
oc = _load("output_contract", "scripts/26_generation_output_contract.py")


def now():
    return subprocess.run(["date", "-Iseconds"], capture_output=True, text=True).stdout.strip()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qdrant_points(collection="tunnelbook_dense_v1"):
    with urllib.request.urlopen(
            f"http://localhost:6333/collections/{collection}", timeout=10) as response:
        result = json.loads(response.read())["result"]
    return result["points_count"], result["status"]


def preflight() -> dict:
    """Hard preflight. Any frozen-identity difference is STOP / NO-GO before the first generation."""
    checks, failures = {}, []

    def check(name, actual, expected):
        ok = actual == expected
        checks[name] = {"expected": expected, "actual": actual, "ok": ok}
        if not ok:
            failures.append(name)
        return ok

    check("benchmark_v2_sha", file_sha(BENCHMARK), BENCHMARK_SHA)
    check("packet_artifact_sha", file_sha(PACKETS), PACKET_ARTIFACT_SHA)
    check("system_prompt_v5_sha", file_sha(ROOT / "data/metadata/generation_system_prompt_v5.txt"),
          PROMPT_V5_SHA)
    check("output_contract_sha", file_sha(ROOT / "scripts/26_generation_output_contract.py"),
          CONTRACT_SHA)

    meta = json.loads((ROOT / "data/metadata/generation_output_contract_v1.json")
                      .read_text(encoding="utf-8"))
    check("output_contract_metadata_status", meta["status"], "frozen")
    check("output_contract_version", meta["version"], oc.CONTRACT_VERSION)
    check("output_contract_recorded_sha", meta["implementation_sha"], CONTRACT_SHA)
    check("repair_policy", oc.REPAIR_POLICY, "none_fail_closed")
    check("validator_version", gen.VALIDATOR_VERSION, "citation-validator-v1.2")
    check("contract_validator_version", oc.VALIDATOR_VERSION, "citation-validator-v1.2")

    tokenizer = gen.GenerationTokenizer()
    renderer = gen.TemplateRenderer()
    check("tokenizer_sha", tokenizer.tokenizer_sha256, TOKENIZER_SHA)
    check("template_sha", renderer.template_sha256, TEMPLATE_SHA)
    check("endpoint", gen.COMPLETIONS_ENDPOINT, "/v1/completions")
    check("thinking_mode", gen.THINKING_MODE, "non_thinking_via_local_template")
    check("loaded_context_length", gen.LOADED_CONTEXT_LENGTH, 71936)
    check("model_id", gen.MODEL_ID, "qwen3.6-35b-a3b-mlx")
    check("stop_strings", list(gen.STOP_STRINGS), ["<|im_end|>", "<|im_start|>"])

    retriever = json.loads((ROOT / "data/metadata/retriever_v1_release.json").read_text(encoding="utf-8"))
    check("retriever_script_sha", retriever["retriever_script_sha256"], RETRIEVER_SCRIPT_SHA)
    check("retriever_status", retriever["status"], "frozen")
    context = json.loads((ROOT / "data/metadata/rag_context_contract_v1.json").read_text(encoding="utf-8"))
    check("context_version", context["context_version"], "tunnelbook-context-v1")
    check("context_retriever_script_sha", context["retriever_script_sha256"], RETRIEVER_SCRIPT_SHA)

    # Every benchmark item must resolve to a frozen packet by SHA; no retrieval is ever re-run.
    items = [json.loads(l) for l in BENCHMARK.read_text(encoding="utf-8").splitlines() if l.strip()]
    packets = {p["packet_sha"] for p in
               (json.loads(l) for l in PACKETS.read_text(encoding="utf-8").splitlines() if l.strip())}
    check("benchmark_items", len(items), 72)
    check("all_packets_resolve", all(i["context_packet_sha"] in packets for i in items), True)

    points, status = qdrant_points()
    check("qdrant_points_before", points, QDRANT_POINTS)
    check("qdrant_status", status, "green")

    model_ids = [m["id"] for m in json.loads(
        urllib.request.urlopen("http://localhost:1234/v1/models", timeout=10).read())["data"]]
    check("model_loaded", gen.MODEL_ID in model_ids, True)

    return {"checks": checks, "failures": failures, "qdrant_points_before": points,
            "go": not failures}

# ------------------------------------------------------------------ main execution

def execute(qdrant_before: int) -> int:
    """Generate all 72 answers under frozen v5 and enforce the contract on each raw answer."""
    items = sorted((json.loads(l) for l in BENCHMARK.read_text(encoding="utf-8").splitlines() if l.strip()),
                   key=lambda r: r["query_id"])
    packets = {p["packet_sha"]: p for p in
               (json.loads(l) for l in PACKETS.read_text(encoding="utf-8").splitlines() if l.strip())}
    prompt = gen.load_system_prompt_versioned(SYSTEM_PROMPT_VERSION)
    tokenizer = gen.GenerationTokenizer()
    renderer = gen.TemplateRenderer()
    config = gen.GenerationConfig(
        max_tokens=MAX_TOKENS, temperature=TEMPERATURE, seed=SEED,
        tokenizer_sha256=tokenizer.tokenizer_sha256, template_sha256=renderer.template_sha256,
        system_prompt_version=SYSTEM_PROMPT_VERSION, system_prompt_sha256=prompt["sha256"])

    done = {}
    if RAW.exists():
        for line in RAW.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                done[row["query_id"]] = row

    for item in items:
        query_id = item["query_id"]
        identity = {
            "query_id": query_id, "benchmark_sha": BENCHMARK_SHA,
            "packet_artifact_sha": PACKET_ARTIFACT_SHA,
            "context_packet_sha": item["context_packet_sha"],
            "system_prompt_version": prompt["name"], "system_prompt_sha": prompt["sha256"],
            "model_id": config.model_id, "tokenizer_sha": tokenizer.tokenizer_sha256,
            "template_sha": renderer.template_sha256,
            "generation_config_hash": config.config_hash(),
            "output_contract_version": oc.CONTRACT_VERSION,
            "output_contract_sha": CONTRACT_SHA}
        stored = done.get(query_id)
        if stored is not None:
            if stored.get("checkpoint_identity") == identity:
                print(f"{query_id} resume (identity matches)", flush=True)
                continue
            raise SystemExit(f"{query_id}: stored row is stale under this identity; delete the "
                             "artifact and re-run rather than mixing configurations")

        packet = packets[item["context_packet_sha"]]
        user = f"EVIDENCE PACKET:\n\n{packet['context_text']}\n\nQUESTION: {item['query']}"
        rendered = renderer.render(prompt["text"], user, enable_thinking=False)
        local = tokenizer.count(rendered)
        gen.validate_prompt_budget(local, MAX_TOKENS)

        started = now()
        response = gen.complete(rendered, config, max_tokens=MAX_TOKENS)
        completed = now()
        answer = response["text"]
        usage = response["usage"]
        answer_sha = hashlib.sha256(answer.encode("utf-8")).hexdigest()

        raw_row = {
            "query_id": query_id, "language": item["language"],
            "primary_query_type": item["primary_query_type"],
            "answerability": item["answerability"], "must_abstain": item["must_abstain"],
            "retrieval_limited": item["retrieval_limited"],
            "benchmark_sha": BENCHMARK_SHA, "packet_artifact_sha": PACKET_ARTIFACT_SHA,
            "context_packet_sha": item["context_packet_sha"],
            "context_token_count": item["context_token_count"],
            "model_id": config.model_id, "system_prompt_version": prompt["name"],
            "system_prompt_sha": prompt["sha256"],
            "generation_config_hash": config.config_hash(),
            "prompt_sha": hashlib.sha256(rendered.encode("utf-8")).hexdigest(),
            "prompt_tokens_local": local, "prompt_tokens_api": usage.get("prompt_tokens"),
            "prompt_token_delta": (usage.get("prompt_tokens") or 0) - local,
            "completion_tokens": usage.get("completion_tokens"),
            "answer_tokens": tokenizer.count(answer),
            "latency_seconds": round(response["latency_seconds"], 3),
            "finish_reason": response["finish_reason"],
            "raw_answer": answer, "raw_answer_sha": answer_sha,
            "evidence_ids": item["evidence_ids"],
            "max_tokens": MAX_TOKENS, "temperature": TEMPERATURE, "seed": SEED,
            "started_at": started, "completed_at": completed,
            "checkpoint_identity": identity}
        gen.atomic_append_jsonl(RAW, raw_row)

        # Enforcement runs on the untouched raw answer. No transformation of any kind precedes it.
        began = time.perf_counter()
        verdict = oc.enforce(answer, item["language"], set(item["evidence_ids"]),
                             answerability=item["answerability"])
        contract_ms = (time.perf_counter() - began) * 1000.0

        if verdict.raw_answer_sha != answer_sha:
            raise SystemExit(f"{query_id}: contract saw a different answer than was persisted; "
                             "no-repair assertion violated")

        contract_row = {"query_id": query_id, **verdict.to_dict(),
                        "contract_enforcement_ms": round(contract_ms, 4),
                        "raw_answer_sha_before_contract": answer_sha,
                        "language": item["language"], "must_abstain": item["must_abstain"],
                        "primary_query_type": item["primary_query_type"],
                        "context_token_count": item["context_token_count"]}
        gen.atomic_append_jsonl(CONTRACT_RESULTS, contract_row)

        flag = "ACCEPT" if verdict.contract_valid else "REJECT"
        print(f"{query_id} {flag} {verdict.failure_reasons} "
              f"cov={verdict.citation_coverage} gen={raw_row['latency_seconds']}s "
              f"contract={contract_ms:.2f}ms", flush=True)

    raw_n = sum(1 for l in RAW.read_text(encoding="utf-8").splitlines() if l.strip())
    con_n = sum(1 for l in CONTRACT_RESULTS.read_text(encoding="utf-8").splitlines() if l.strip())
    points_after, status_after = qdrant_points()
    print(f"EXECUTION COMPLETE raw={raw_n} contract={con_n} "
          f"qdrant {qdrant_before}->{points_after} ({status_after})")
    return 0 if raw_n == 72 and con_n == 72 else 1


if __name__ == "__main__":
    result = preflight()
    for name, c in result["checks"].items():
        mark = "OK  " if c["ok"] else "FAIL"
        print(f"  {mark} {name:<34} {str(c['actual'])[:64]}")
    print()
    if not result["go"]:
        print(f"HARD PREFLIGHT: STOP / NO-GO — {result['failures']}")
        raise SystemExit(1)
    print("HARD PREFLIGHT: GO — all frozen identities match\n")
    raise SystemExit(execute(result["qdrant_points_before"]))
