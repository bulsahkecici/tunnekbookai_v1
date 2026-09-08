"""Development regression runner for citation-adherence remediation.

Runs the development set under one system prompt version and scores the two Phase B failure modes:
malformed citations, and material-claim citation coverage measured PER CLAIM (a handle on a parent
bullet never counts for a child bullet). This is a development set: it can show a failure
reproducing, closing, or regressing. It is not an evaluation benchmark and yields no quality claim.
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
DEVSET = ROOT / "data/evaluation/generation_dev_regression_v1.jsonl"
MAX_TOKENS = 3072
SEED = 11
TEMPERATURE = 0.0

HANDLE = re.compile(r"\[E\d{3}\]")
ABSTAIN = re.compile(r"^\s*(YETERSİZ KANIT|INSUFFICIENT EVIDENCE)\b", re.I)
STOPWORDS = set("""the a an and or of to in for on with is are be as by from that this these those it
its at which such using used use can may shall must should not no than then when where while their
they them ve ile bir bu şu da de ki için gibi olarak olan olup ise ancak ayrıca daha en çok az var
yok göre kadar sonra önce her tüm""".split())


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gen = _load("generation_eval", "scripts/21_generation_model_eval.py")


def now():
    return subprocess.run(["date", "-Iseconds"], capture_output=True, text=True).stdout.strip()


def blocks(answer: str) -> list[str]:
    """Split into candidate claims at bullet / list-item / paragraph granularity."""
    text = re.sub(r"\r", "", answer)
    parts = [b.strip() for b in re.split(r"\n(?=\s*(?:[-*•]|\d{1,2}[.)]))|\n{2,}", text) if b.strip()]
    return [re.sub(r"\s+", " ", b).strip() for b in parts if len(b.strip()) >= 12]


def content_words(text: str) -> list[str]:
    body = re.sub(r"\[E\d{3}\]", " ", text)
    body = re.sub(r"^\s*(?:[-*•]|\d{1,2}[.)])\s*", "", body)
    body = re.sub(r"[^\w\sçğıöşüâîû]", " ", body.lower())
    return [w for w in body.split() if len(w) > 3 and w not in STOPWORDS]


def is_material(block: str) -> bool:
    """A material factual claim asserts something; headings, lead-ins and the marker do not."""
    stripped = block.strip()
    if ABSTAIN.match(stripped) and len(content_words(stripped)) < 8:
        return False
    if re.search(r":\s*$", stripped) and not HANDLE.search(stripped):
        return False                      # lead-in announcing a list
    if re.fullmatch(r"[#*\s\-]*\*{0,2}[^.]{0,60}\*{0,2}:?", stripped) and not HANDLE.search(stripped):
        return False                      # bare heading
    body = re.sub(r"^\s*(?:[-*•]|\d{1,2}[.)])\s*", "", stripped)
    return len(content_words(body)) >= 4 or bool(re.search(r"\d", re.sub(r"\[E\d{3}\]", "", body)))


def coverage(answer: str) -> dict:
    material, covered, uncovered = 0, 0, []
    for block in blocks(answer):
        if not is_material(block):
            continue
        material += 1
        if HANDLE.search(block):
            covered += 1
        else:
            uncovered.append(block[:160])
    return {"material_claims": material, "claims_with_citation": covered,
            "claims_without_citation": material - covered,
            "citation_coverage": round(covered / material, 4) if material else None,
            "uncovered_examples": uncovered[:6]}


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
        done = {json.loads(l)["dev_id"] for l in out_path.read_text(encoding="utf-8").splitlines() if l.strip()}
    for item in items:
        if item["dev_id"] in done:
            continue
        user = f"EVIDENCE PACKET:\n\n{item['context_text']}\n\nQUESTION: {item['query']}"
        rendered = renderer.render(prompt["text"], user, enable_thinking=False)
        local = tokenizer.count(rendered)
        gen.validate_prompt_budget(local, MAX_TOKENS)
        started = now()
        response = gen.complete(rendered, config, max_tokens=MAX_TOKENS)
        completed = now()
        answer = response["text"]
        exposed = set(item["evidence_ids"])
        citations = gen.validate_citations(answer, exposed)
        abstention = gen.validate_abstention(answer)
        cov = coverage(answer)
        row = {"dev_id": item["dev_id"], "dataset_role": "development_regression",
               "failure_shape": item["failure_shape"], "origin": item["origin"],
               "origin_query_id": item["origin_query_id"], "language": item["language"],
               "query": item["query"], "system_prompt_version": prompt["name"],
               "system_prompt_sha": prompt["sha256"], "model_id": config.model_id,
               "generation_config_hash": config.config_hash(),
               "context_packet_sha": item["context_packet_sha"],
               "prompt_tokens_local": local,
               "prompt_tokens_api": response["usage"].get("prompt_tokens"),
               "prompt_token_delta": (response["usage"].get("prompt_tokens") or 0) - local,
               "completion_tokens": response["usage"].get("completion_tokens"),
               "answer_tokens": tokenizer.count(answer),
               "latency_seconds": round(response["latency_seconds"], 3),
               "finish_reason": response["finish_reason"], "answer": answer,
               "answer_sha": hashlib.sha256(answer.encode("utf-8")).hexdigest(),
               "abstention_at_start": bool(ABSTAIN.match(answer.lstrip())),
               **citations, **abstention, **cov,
               "started_at": started, "completed_at": completed}
        gen.atomic_append_jsonl(out_path, row)
        print(f"{item['dev_id']} {version} mal={len(citations['malformed_citations'])} "
              f"{citations['malformed_citations']} unk={len(citations['unknown_handles'])} "
              f"cov={cov['citation_coverage']} ({cov['claims_with_citation']}/{cov['material_claims']}) "
              f"abst={abstention.get('abstention_marker')} {row['latency_seconds']}s", flush=True)
    return 0


if __name__ == "__main__":
    version = sys.argv[1]
    out = ROOT / f"data/evaluation/generation_dev_regression_{version}_results.jsonl"
    raise SystemExit(run(version, out))
