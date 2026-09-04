"""Same-config retry diagnostic: exactly one extra attempt per contract-rejected item.

Nothing changes between attempt 1 and attempt 2 - same prompt, packet, model, temperature and
seed. The purpose is only to establish whether a contract failure is transient or fully
deterministic, so that production is not told to spend latency on a retry that cannot help.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "data/evaluation"
FIRST_PASS = EV / "generation_output_contract_first_pass_v1.jsonl"
RAW = EV / "generation_output_contract_eval_raw_v1.jsonl"
OUT = EV / "generation_output_contract_retry_same_config_v1.jsonl"
BENCHMARK = EV / "generation_eval_benchmark_v2.jsonl"
PACKETS = EV / "generation_eval_benchmark_v2_packets.jsonl"
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


def main() -> int:
    if not FIRST_PASS.exists():
        raise SystemExit("first-pass artifact missing: freeze the 72-item first pass before retrying")
    first = [json.loads(l) for l in FIRST_PASS.read_text(encoding="utf-8").splitlines() if l.strip()]
    if len(first) != 72:
        raise SystemExit(f"first pass is not complete ({len(first)} rows); refusing to retry")
    rejected = [r["query_id"] for r in first if r["production_action"] == "reject"]

    raw = {r["query_id"]: r for r in
           (json.loads(l) for l in RAW.read_text(encoding="utf-8").splitlines() if l.strip())}
    items = {i["query_id"]: i for i in
             (json.loads(l) for l in BENCHMARK.read_text(encoding="utf-8").splitlines() if l.strip())}
    packets = {p["packet_sha"]: p for p in
               (json.loads(l) for l in PACKETS.read_text(encoding="utf-8").splitlines() if l.strip())}

    prompt = gen.load_system_prompt_versioned(SYSTEM_PROMPT_VERSION)
    tokenizer = gen.GenerationTokenizer()
    renderer = gen.TemplateRenderer()
    config = gen.GenerationConfig(
        max_tokens=MAX_TOKENS, temperature=TEMPERATURE, seed=SEED,
        tokenizer_sha256=tokenizer.tokenizer_sha256, template_sha256=renderer.template_sha256,
        system_prompt_version=SYSTEM_PROMPT_VERSION, system_prompt_sha256=prompt["sha256"])

    rows = []
    for query_id in rejected:
        item = items[query_id]
        packet = packets[item["context_packet_sha"]]
        user = f"EVIDENCE PACKET:\n\n{packet['context_text']}\n\nQUESTION: {item['query']}"
        rendered = renderer.render(prompt["text"], user, enable_thinking=False)
        assert hashlib.sha256(rendered.encode("utf-8")).hexdigest() == raw[query_id]["prompt_sha"], \
            f"{query_id}: retry prompt differs from attempt 1; config is not identical"

        response = gen.complete(rendered, config, max_tokens=MAX_TOKENS)
        answer = response["text"]
        retry_sha = hashlib.sha256(answer.encode("utf-8")).hexdigest()
        began = time.perf_counter()
        verdict = oc.enforce(answer, item["language"], set(item["evidence_ids"]),
                             answerability=item["answerability"])
        contract_ms = (time.perf_counter() - began) * 1000.0

        original_sha = raw[query_id]["raw_answer_sha"]
        row = {"query_id": query_id, "attempt": 2,
               "raw_answer_sha_original": original_sha,
               "raw_answer_sha_retry": retry_sha,
               "byte_identical": retry_sha == original_sha,
               "contract_valid_original": False,
               "contract_valid_retry": verdict.contract_valid,
               "failure_reasons_original": [r["failure_reasons"] for r in first
                                            if r["query_id"] == query_id][0],
               "failure_reasons_retry": verdict.failure_reasons,
               "recovered": verdict.contract_valid,
               "generation_config_hash": config.config_hash(),
               "contract_enforcement_ms": round(contract_ms, 4),
               "latency_seconds": round(response["latency_seconds"], 3),
               "raw_answer_retry": answer}
        rows.append(row)
        print(f"{query_id} identical={row['byte_identical']} valid_retry={verdict.contract_valid} "
              f"{verdict.failure_reasons}", flush=True)

    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    recovered = sum(1 for r in rows if r["recovered"])
    identical = sum(1 for r in rows if r["byte_identical"])
    print(f"RETRY COMPLETE rejected={len(rows)} byte_identical={identical} recovered={recovered} "
          f"recovery_rate={recovered / len(rows) if rows else 0:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
