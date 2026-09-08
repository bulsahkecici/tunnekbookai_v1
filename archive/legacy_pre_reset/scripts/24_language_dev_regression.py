"""Abstention marker language-selection development regression.

Scores one rule: when the model abstains, the opening marker must be chosen by the QUESTION's
language, never the evidence language. Expected markers are derived from the query language alone
and are computed independently of anything the model produced. No post-processing ever rewrites a
marker - the prompt has to emit the right one.
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
DEVSET = ROOT / "data/evaluation/generation_language_dev_regression_v1.jsonl"
MAX_TOKENS = 3072
SEED = 11
TEMPERATURE = 0.0

MARKER_FOR_LANGUAGE = {"tr": "YETERSİZ KANIT", "en": "INSUFFICIENT EVIDENCE"}
ANY_MARKER = re.compile(r"^\s*(YETERSİZ KANIT|INSUFFICIENT EVIDENCE)", re.I)


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gen = _load("generation_eval", "scripts/21_generation_model_eval.py")
devreg = _load("dev_regression", "scripts/23_dev_regression.py")


def now():
    return subprocess.run(["date", "-Iseconds"], capture_output=True, text=True).stdout.strip()


def expected_marker(query_language: str) -> str:
    """Derived from the question only. Never consults the answer or the evidence."""
    return MARKER_FOR_LANGUAGE[query_language]


def marker_report(answer: str, query_language: str) -> dict:
    expected = expected_marker(query_language)
    found = gen.validate_abstention(answer).get("abstention_marker")
    at_start = bool(ANY_MARKER.match(answer.lstrip()))
    abstained = found is not None
    return {
        "expected_abstention_marker": expected,
        "actual_abstention_marker": found,
        "abstained": abstained,
        "marker_at_start": at_start if abstained else None,
        "marker_language_correct": (found == expected) if abstained else None,
        "wrong_language_marker": bool(abstained and found != expected),
    }


def run(version: str, out_path: Path) -> int:
    items = [json.loads(l) for l in DEVSET.read_text(encoding="utf-8").splitlines() if l.strip()]
    prompt = gen.load_system_prompt_versioned(version)
    tokenizer = gen.GenerationTokenizer()
    renderer = gen.TemplateRenderer()
    config = gen.GenerationConfig(
        max_tokens=MAX_TOKENS, temperature=TEMPERATURE, seed=SEED,
        tokenizer_sha256=tokenizer.tokenizer_sha256, template_sha256=renderer.template_sha256,
        system_prompt_version=version, system_prompt_sha256=prompt["sha256"])
    done = set()
    if out_path.exists():
        done = {json.loads(l)["lang_id"] for l in out_path.read_text(encoding="utf-8").splitlines() if l.strip()}
    for item in items:
        if item["lang_id"] in done:
            continue
        user = f"EVIDENCE PACKET:\n\n{item['context_text']}\n\nQUESTION: {item['query']}"
        rendered = renderer.render(prompt["text"], user, enable_thinking=False)
        local = tokenizer.count(rendered)
        gen.validate_prompt_budget(local, MAX_TOKENS)
        started = now()
        response = gen.complete(rendered, config, max_tokens=MAX_TOKENS)
        completed = now()
        answer = response["text"]
        citations = gen.validate_citations(answer, set(item["evidence_ids"]))
        markers = marker_report(answer, item["language"])
        cov = devreg.coverage(answer)
        behaved = ("abstain" if markers["abstained"] else "answer") == item["expected_behavior"]
        row = {"lang_id": item["lang_id"], "dataset_role": "development_regression",
               "origin": item["origin"], "origin_dev_id": item["origin_dev_id"],
               "language": item["language"], "query": item["query"],
               "expected_behavior": item["expected_behavior"], "evidence_mix": item["evidence_mix"],
               "behaviour_matches_expectation": behaved,
               "system_prompt_version": prompt["name"], "system_prompt_sha": prompt["sha256"],
               "model_id": config.model_id, "generation_config_hash": config.config_hash(),
               "context_packet_sha": item["context_packet_sha"],
               "prompt_tokens_local": local,
               "prompt_tokens_api": response["usage"].get("prompt_tokens"),
               "prompt_token_delta": (response["usage"].get("prompt_tokens") or 0) - local,
               "completion_tokens": response["usage"].get("completion_tokens"),
               "latency_seconds": round(response["latency_seconds"], 3),
               "finish_reason": response["finish_reason"], "answer": answer,
               "answer_sha": hashlib.sha256(answer.encode("utf-8")).hexdigest(),
               **markers, **citations, **cov,
               "started_at": started, "completed_at": completed}
        gen.atomic_append_jsonl(out_path, row)
        print(f"{item['lang_id']} [{item['language']}] {version} "
              f"expect={item['expected_behavior']:<7} marker={markers['actual_abstention_marker']!r} "
              f"lang_ok={markers['marker_language_correct']} at_start={markers['marker_at_start']} "
              f"mal={len(citations['malformed_citations'])} cov={cov['citation_coverage']}", flush=True)
    return 0


if __name__ == "__main__":
    version = sys.argv[1]
    out = ROOT / f"data/evaluation/generation_language_dev_{version}_results.jsonl"
    raise SystemExit(run(version, out))
