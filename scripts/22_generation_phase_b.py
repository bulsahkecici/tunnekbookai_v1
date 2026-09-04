"""TunnelBookAI Generation Phase B - frozen 72-query execution.

Executes the frozen benchmark against the frozen generation runtime. Retrieval is NOT re-run:
every item is answered from the ContextPacket that was frozen at authoring time, addressed by its
packet SHA. Results are checkpointed after every single query with full identity, so an interrupted
run resumes only rows whose identity still matches.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BENCHMARK = ROOT / "data/evaluation/generation_eval_benchmark_v1.jsonl"
PACKETS = ROOT / "data/evaluation/generation_eval_benchmark_v1_packets.jsonl"
BENCHMARK_SHA = "de3c1684ad26b459e6a209a9ef770c1a0f0fae39b44d0d251bc492ca3f75bd6b"
RESULTS = ROOT / "data/evaluation/generation_eval_results_v1.jsonl"

SYSTEM_PROMPT_VERSION = "v3"
MAX_TOKENS = 3072          # frozen candidate reserve; never swept in the main execution
SEED = 11
TEMPERATURE = 0.0

THINKING_MARKERS = ("<think>", "</think>", "<|im_start|>", "<|im_end|>")


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gen = _load("generation_eval", "scripts/21_generation_model_eval.py")


def now() -> str:
    return subprocess.run(["date", "-Iseconds"], capture_output=True, text=True).stdout.strip()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_benchmark() -> list[dict]:
    actual = sha256_file(BENCHMARK)
    if actual != BENCHMARK_SHA:
        raise SystemExit(f"benchmark SHA mismatch: {actual} != {BENCHMARK_SHA}; refusing to execute "
                         "a modified benchmark under v1 identity")
    rows = [json.loads(line) for line in BENCHMARK.read_text(encoding="utf-8").splitlines() if line.strip()]
    return sorted(rows, key=lambda r: r["query_id"])


def load_packets() -> dict[str, dict]:
    packets = {}
    for line in PACKETS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            packet = json.loads(line)
            packets[packet["packet_sha"]] = packet
    return packets


def build_prompt(renderer, system_prompt: str, context_text: str, query: str) -> str:
    user = f"EVIDENCE PACKET:\n\n{context_text}\n\nQUESTION: {query}"
    return renderer.render(system_prompt, user, enable_thinking=False), user


def thinking_leakage(answer: str) -> list[str]:
    return [marker for marker in THINKING_MARKERS if marker in answer]


def abstention_at_start(answer: str, marker: str | None) -> bool:
    if not marker:
        return False
    return answer.lstrip().upper().startswith(marker.upper())


def reasoning_token_field(usage: dict) -> tuple[int | None, str]:
    """Never fabricate a zero: if the API does not expose reasoning tokens, say so."""
    for key in ("reasoning_tokens", "completion_tokens_details", "reasoning"):
        if key in usage:
            value = usage[key]
            if isinstance(value, dict):
                inner = value.get("reasoning_tokens")
                if inner is not None:
                    return int(inner), "exposed"
            elif value is not None:
                return int(value), "exposed"
    return None, "not_exposed"


def main() -> int:
    benchmark = load_benchmark()
    packets = load_packets()
    prompt = gen.load_system_prompt_versioned(SYSTEM_PROMPT_VERSION)
    tokenizer = gen.GenerationTokenizer()
    renderer = gen.TemplateRenderer()
    config = gen.GenerationConfig(
        max_tokens=MAX_TOKENS, temperature=TEMPERATURE, seed=SEED,
        tokenizer_sha256=tokenizer.tokenizer_sha256, template_sha256=renderer.template_sha256,
        system_prompt_version=SYSTEM_PROMPT_VERSION, system_prompt_sha256=prompt["sha256"])
    config_hash = config.config_hash()

    done: dict[str, dict] = {}
    if RESULTS.exists():
        for line in RESULTS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                done[row["query_id"]] = row

    for item in benchmark:
        query_id = item["query_id"]
        packet = packets[item["context_packet_sha"]]
        expected_identity = {
            "query_id": query_id, "benchmark_sha": BENCHMARK_SHA,
            "system_prompt_sha": prompt["sha256"], "model_id": config.model_id,
            "tokenizer_sha": tokenizer.tokenizer_sha256, "template_sha": renderer.template_sha256,
            "generation_config_hash": config_hash,
            "context_packet_sha": item["context_packet_sha"]}
        stored = done.get(query_id)
        if stored is not None:
            stale = not gen.is_resumable(stored.get("checkpoint_identity", {}), expected_identity)
            if not stale:
                print(f"{query_id} resume (identity matches)", flush=True)
                continue
            raise SystemExit(f"{query_id}: stored result is stale under the current identity; "
                             "delete the results artifact and re-run rather than mixing configs")

        rendered, _user = build_prompt(renderer, prompt["text"], packet["context_text"], item["query"])
        local_tokens = tokenizer.count(rendered)
        gen.validate_prompt_budget(local_tokens, MAX_TOKENS)

        started = now()
        response = gen.complete(rendered, config, max_tokens=MAX_TOKENS)
        completed = now()
        answer = response["text"]
        usage = response["usage"]
        exposed_ids = set(item["evidence_ids"])
        citations = gen.validate_citations(answer, exposed_ids)
        abstention = gen.validate_abstention(answer)
        state = gen.classify_completion(answer, response["finish_reason"],
                                        {**citations, **abstention}, item["must_abstain"])
        reasoning_tokens, reasoning_status = reasoning_token_field(usage)

        row = {
            "query_id": query_id, "primary_query_type": item["primary_query_type"],
            "language": item["language"], "answerability": item["answerability"],
            "must_abstain": item["must_abstain"], "retrieval_limited": item["retrieval_limited"],
            "model_id": config.model_id, "system_prompt_version": prompt["name"],
            "system_prompt_sha": prompt["sha256"], "benchmark_sha": BENCHMARK_SHA,
            "context_packet_sha": item["context_packet_sha"],
            "context_token_count": item["context_token_count"],
            "generation_config_hash": config_hash,
            "prompt_sha": hashlib.sha256(rendered.encode("utf-8")).hexdigest(),
            "prompt_tokens_local": local_tokens,
            "prompt_tokens_api": usage.get("prompt_tokens"),
            "prompt_token_delta": (usage.get("prompt_tokens") or 0) - local_tokens,
            "completion_tokens": usage.get("completion_tokens"),
            "answer_tokens": tokenizer.count(answer),
            "latency_seconds": round(response["latency_seconds"], 3),
            "finish_reason": response["finish_reason"],
            "raw_answer": answer,
            "reasoning_tokens": reasoning_tokens,
            "reasoning_tokens_status": reasoning_status,
            "thinking_marker_leaks": thinking_leakage(answer),
            "abstention_at_start": abstention_at_start(answer, abstention.get("abstention_marker")),
            "completion_state": state,
            "max_tokens": MAX_TOKENS, "temperature": TEMPERATURE, "seed": SEED,
            "validator_version": gen.VALIDATOR_VERSION,
            "started_at": started, "completed_at": completed,
            "checkpoint_identity": expected_identity,
        }
        row.update(citations)
        row.update(abstention)
        gen.atomic_append_jsonl(RESULTS, row)
        print(f"{query_id} {state:<22} mal={len(citations['malformed_citations'])} "
              f"unk={len(citations['unknown_handles'])} cites={len(citations['valid_handles'])} "
              f"abst={abstention.get('abstention_marker')} {row['latency_seconds']}s", flush=True)

    total = sum(1 for line in RESULTS.read_text(encoding="utf-8").splitlines() if line.strip())
    print(f"EXECUTION COMPLETE rows={total}")
    return 0 if total == 72 else 1


if __name__ == "__main__":
    raise SystemExit(main())
