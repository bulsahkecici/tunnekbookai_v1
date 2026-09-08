"""Phase C - fresh 72-query confirmation run under frozen v5 with Output Contract v1.1.

The replay proved the contract delta in isolation. This run proves the whole stack end to end:
the generator is invoked again from the frozen packets, and v1.1 enforces each raw answer. Nothing
about the generator, prompt, benchmark, packets or generation config differs from the v1 run - only
the contract. Retrieval is never re-run; packets are matched by SHA.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "data/evaluation"
BENCHMARK = EV / "generation_eval_benchmark_v2.jsonl"
PACKETS = EV / "generation_eval_benchmark_v2_packets.jsonl"
FRESH_RAW = EV / "generation_output_contract_v1_1_fresh_raw.jsonl"
FRESH_RESULTS = EV / "generation_output_contract_v1_1_fresh_results.jsonl"

BENCHMARK_SHA = "1e6347b557d583b56882c4c05fd1c5453874b7a05e61205c9430a24a677b0cff"
PACKET_ARTIFACT_SHA = "0538705147cf543b45fe8e73d57828cbc341a9a5a1dd574bd0969a9326e54d7a"
CONTRACT_V1_1_SHA = "5ebf8fe90e3e5491ce07a9143f8fd377841defa2e0e7a09188f3a835b07bdef5"
SYSTEM_PROMPT_VERSION = "v5"
MAX_TOKENS, SEED, TEMPERATURE = 3072, 11, 0.0


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


v11 = _load("output_contract_v1_1", "scripts/31_generation_output_contract_v1_1.py")
gen = v11.gen


def now():
    return subprocess.run(["date", "-Iseconds"], capture_output=True, text=True).stdout.strip()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if file_sha(BENCHMARK) != BENCHMARK_SHA:
        raise SystemExit("benchmark v2 SHA mismatch; refusing to execute")
    if file_sha(PACKETS) != PACKET_ARTIFACT_SHA:
        raise SystemExit("packet artifact SHA mismatch; refusing to execute")
    if file_sha(ROOT / "scripts/31_generation_output_contract_v1_1.py") != CONTRACT_V1_1_SHA:
        raise SystemExit("contract v1.1 SHA mismatch; refusing to execute")

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
    if FRESH_RAW.exists():
        for line in FRESH_RAW.read_text(encoding="utf-8").splitlines():
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
            "output_contract_version": v11.CONTRACT_VERSION,
            "output_contract_sha": CONTRACT_V1_1_SHA}
        stored = done.get(query_id)
        if stored is not None:
            if stored.get("checkpoint_identity") == identity:
                print(f"{query_id} resume (identity matches)", flush=True)
                continue
            raise SystemExit(f"{query_id}: stored row is stale under this identity")

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

        gen.atomic_append_jsonl(FRESH_RAW, {
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
            "checkpoint_identity": identity})

        began = time.perf_counter()
        verdict = v11.enforce(answer, item["language"], set(item["evidence_ids"]),
                              answerability=item["answerability"])
        contract_ms = (time.perf_counter() - began) * 1000.0
        if verdict.raw_answer_sha != answer_sha:
            raise SystemExit(f"{query_id}: contract saw a different answer than was persisted")

        gen.atomic_append_jsonl(FRESH_RESULTS, {
            "query_id": query_id, **verdict.to_dict(),
            "contract_enforcement_ms": round(contract_ms, 4),
            "raw_answer_sha_before_contract": answer_sha,
            "language": item["language"], "must_abstain": item["must_abstain"],
            "primary_query_type": item["primary_query_type"],
            "context_token_count": item["context_token_count"]})

        print(f"{query_id} {'ACCEPT' if verdict.contract_valid else 'REJECT'} "
              f"{verdict.failure_reasons} gen={response['latency_seconds']:.1f}s "
              f"contract={contract_ms:.2f}ms", flush=True)

    raw_n = sum(1 for l in FRESH_RAW.read_text(encoding="utf-8").splitlines() if l.strip())
    res_n = sum(1 for l in FRESH_RESULTS.read_text(encoding="utf-8").splitlines() if l.strip())
    print(f"FRESH RUN COMPLETE raw={raw_n} results={res_n}")
    return 0 if raw_n == 72 and res_n == 72 else 1


if __name__ == "__main__":
    raise SystemExit(main())
