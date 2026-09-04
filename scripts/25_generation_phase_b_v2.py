"""Generation Phase B v2 - clean holdout execution against frozen benchmark v2 under prompt v5.

Retrieval is never re-run: each item is answered from the packet frozen at authoring time, matched
by packet SHA. Every row is checkpointed with a full identity that includes the packet-artifact SHA,
so a run mixing benchmark or prompt versions cannot be resumed silently.
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
BENCHMARK = ROOT / "data/evaluation/generation_eval_benchmark_v2.jsonl"
PACKETS = ROOT / "data/evaluation/generation_eval_benchmark_v2_packets.jsonl"
RESULTS = ROOT / "data/evaluation/generation_eval_results_v2.jsonl"
BENCHMARK_SHA = "1e6347b557d583b56882c4c05fd1c5453874b7a05e61205c9430a24a677b0cff"
PACKET_ARTIFACT_SHA = "0538705147cf543b45fe8e73d57828cbc341a9a5a1dd574bd0969a9326e54d7a"
SYSTEM_PROMPT_VERSION = "v5"
MAX_TOKENS, SEED, TEMPERATURE = 3072, 11, 0.0

MARKER_FOR_LANGUAGE = {"tr": "YETERSİZ KANIT", "en": "INSUFFICIENT EVIDENCE"}
ANY_MARKER = re.compile(r"^\s*(YETERSİZ KANIT|INSUFFICIENT EVIDENCE)", re.I)
THINKING_MARKERS = ("<think>", "</think>", "<|im_start|>", "<|im_end|>")


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gen = _load("generation_eval", "scripts/21_generation_model_eval.py")


def now():
    return subprocess.run(["date", "-Iseconds"], capture_output=True, text=True).stdout.strip()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reasoning_tokens(usage: dict):
    for key in ("reasoning_tokens", "completion_tokens_details"):
        if key in usage:
            value = usage[key]
            if isinstance(value, dict) and value.get("reasoning_tokens") is not None:
                return int(value["reasoning_tokens"]), "exposed"
            if not isinstance(value, dict) and value is not None:
                return int(value), "exposed"
    return None, "not_exposed"


def main() -> int:
    if file_sha(BENCHMARK) != BENCHMARK_SHA:
        raise SystemExit("benchmark v2 SHA mismatch; refusing to execute")
    if file_sha(PACKETS) != PACKET_ARTIFACT_SHA:
        raise SystemExit("packet artifact SHA mismatch; refusing to execute")
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
    if RESULTS.exists():
        for line in RESULTS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                done[row["query_id"]] = row

    for item in items:
        query_id = item["query_id"]
        identity = {
            "query_id": query_id, "benchmark_v2_sha": BENCHMARK_SHA,
            "packet_artifact_sha": PACKET_ARTIFACT_SHA,
            "context_packet_sha": item["context_packet_sha"],
            "system_prompt_version": prompt["name"], "system_prompt_sha": prompt["sha256"],
            "model_id": config.model_id, "tokenizer_sha": tokenizer.tokenizer_sha256,
            "template_sha": renderer.template_sha256,
            "generation_config_hash": config.config_hash()}
        stored = done.get(query_id)
        if stored is not None:
            if stored.get("checkpoint_identity") == identity:
                print(f"{query_id} resume (identity matches)", flush=True)
                continue
            raise SystemExit(f"{query_id}: stored result is stale under this identity; delete the "
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
        citations = gen.validate_citations(answer, set(item["evidence_ids"]))
        abstention = gen.validate_abstention(answer)
        state = gen.classify_completion(answer, response["finish_reason"],
                                        {**citations, **abstention}, item["must_abstain"])
        expected_marker = MARKER_FOR_LANGUAGE[item["language"]]
        found_marker = abstention.get("abstention_marker")
        tokens, status = reasoning_tokens(usage)

        row = {
            "query_id": query_id, "primary_query_type": item["primary_query_type"],
            "language": item["language"], "answerability": item["answerability"],
            "must_abstain": item["must_abstain"], "retrieval_limited": item["retrieval_limited"],
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
            "finish_reason": response["finish_reason"], "raw_answer": answer,
            "reasoning_tokens": tokens, "reasoning_tokens_status": status,
            "thinking_marker_leaks": [m for m in THINKING_MARKERS if m in answer],
            "expected_abstention_marker": expected_marker,
            "abstention_marker_language_correct": (found_marker == expected_marker)
                                                   if found_marker else None,
            "abstention_at_start": bool(ANY_MARKER.match(answer.lstrip())) if found_marker else False,
            "completion_state": state,
            "max_tokens": MAX_TOKENS, "temperature": TEMPERATURE, "seed": SEED,
            "validator_version": gen.VALIDATOR_VERSION,
            "started_at": started, "completed_at": completed,
            "checkpoint_identity": identity}
        row.update(citations)
        row.update(abstention)
        gen.atomic_append_jsonl(RESULTS, row)
        print(f"{query_id} {state:<22} mal={len(citations['malformed_citations'])} "
              f"unk={len(citations['unknown_handles'])} cites={len(citations['valid_handles'])} "
              f"marker={found_marker!r} lang_ok={row['abstention_marker_language_correct']} "
              f"{row['latency_seconds']}s", flush=True)

    total = sum(1 for l in RESULTS.read_text(encoding="utf-8").splitlines() if l.strip())
    print(f"EXECUTION COMPLETE rows={total}")
    return 0 if total == 72 else 1


if __name__ == "__main__":
    raise SystemExit(main())
