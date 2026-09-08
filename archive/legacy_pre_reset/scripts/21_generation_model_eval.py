"""TunnelBookAI generation evaluation harness (Phase A1, Run 1).

Runtime foundation only: template rendering, tokenisation, raw-completions client, deterministic
citation/abstention validation, result schema, checkpoint identity. No benchmark, no grading.

Two measured facts shape this file:
  * LM Studio's /v1/chat/completions silently ignores `chat_template_kwargs`, so `enable_thinking`
    never reaches the template. Benchmark generation therefore renders the real local template
    in-process and posts the raw prompt to /v1/completions. The chat endpoint is rejected outright.
  * With the template's pre-closed <think></think> block the model emits zero reasoning tokens.
    Hidden reasoning is never requested, never parsed and never persisted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import time
import urllib.request
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = Path(os.environ.get(
    "TUNNELBOOK_GEN_MODEL_DIR",
    Path.home() / ".lmstudio/models/lmstudio-community/Qwen3.6-35B-A3B-MLX-4bit"))
MODEL_ID = "qwen3.6-35b-a3b-mlx"
UPSTREAM_MODEL = "Qwen/Qwen3.6-35B-A3B"
LMSTUDIO_BASE = os.environ.get("TUNNELBOOK_LMSTUDIO", "http://127.0.0.1:1234")
COMPLETIONS_ENDPOINT = "/v1/completions"
FORBIDDEN_ENDPOINT = "/v1/chat/completions"
LOADED_CONTEXT_LENGTH = 71936
THINKING_MODE = "non_thinking_via_local_template"
STOP_STRINGS = ("<|im_end|>", "<|im_start|>")
# Frozen, versioned system prompts. Each entry is immutable; a change means a new version, never an
# edit. The loader verifies SHA and fails closed - it never falls back to another version.
SYSTEM_PROMPTS = {
    "v1": {"path": ROOT / "data/metadata/generation_system_prompt_v1.txt",
           "sha256": "303691ec02501fa4637a2618ceb90f21bba4c558e41124325ed8915ef7a64817",
           "name": "generation-system-prompt-v1"},
    "v2": {"path": ROOT / "data/metadata/generation_system_prompt_v2.txt",
           "sha256": "0063b9bcbe2d93325b03ae18c6005feb0b9a9571d93132607b740ad794f005cc",
           "name": "generation-system-prompt-v2"},
    "v3": {"path": ROOT / "data/metadata/generation_system_prompt_v3.txt",
           "sha256": "d3cadd465e2733d0cdd451d146407f28f80cefc784b432088fc20ecf7526dc74",
           "name": "generation-system-prompt-v3"},
    "v4": {"path": ROOT / "data/metadata/generation_system_prompt_v4.txt",
           "sha256": "5950bafff10d82c2db3e0fe1999f25bd6b705924946737187a7fdde017dba072",
           "name": "generation-system-prompt-v4"},
    "v5": {"path": ROOT / "data/metadata/generation_system_prompt_v5.txt",
           "sha256": "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085",
           "name": "generation-system-prompt-v5"},
}
CANDIDATE_SYSTEM_PROMPT_VERSION = "v3"
SYSTEM_PROMPT_PATH = SYSTEM_PROMPTS["v1"]["path"]
SYSTEM_PROMPT_SHA256 = SYSTEM_PROMPTS["v1"]["sha256"]
VALIDATOR_VERSION = "citation-validator-v1.2"
HARNESS_VERSION = "generation-harness-v1"

ABSTAIN_TR = "YETERSİZ KANIT"
ABSTAIN_EN = "INSUFFICIENT EVIDENCE"

# --- citation syntax -------------------------------------------------------------------------
# Valid-first parsing. A single alternation cannot separate "valid", "malformed" and "bare"
# without matching valid handles as malformed, which is exactly the bug this version fixes.
VALID_HANDLE = re.compile(r"\[E\d{3}\]")
BRACKET_CANDIDATE = re.compile(r"\[\s*[Ee][^\]\n]{0,12}\]")   # bracketed, evidence-looking
BARE_CANDIDATE = re.compile(r"(?<![\[\w])[Ee]\d{2,4}(?![\]\w])")
OPEN_UNCLOSED = re.compile(r"\[[Ee]\d{1,4}(?![\]\d])")

DOC_LEAK = re.compile(r"\bDOC\d{4,}\b")
PAGE_LEAK = re.compile(r"\bpage\s+\d+|\bpp\.\s?\d+|\bss?\.\s?\d+(?:\s*[-–]\s*\d+)?", re.IGNORECASE)
SLIDE_LEAK = re.compile(r"\b(?:slayt|slide)\s+\d+", re.IGNORECASE)
# A bare "/" is not a path: C30/37 and 10/20 are ordinary engineering notation. Require either a
# real document extension, or an absolute path of at least two segments preceded by whitespace.
PATH_LEAK = re.compile(r"[\w/\-.]+\.(?:pdf|docx|pptx|xlsx|md)\b"
                      r"|(?:(?<=\s)|^)/[\w\-.]+(?:/[\w\-.]+)+", re.IGNORECASE)
TEMPLATE_LEAK = re.compile(r"<\|im_(?:start|end)\|>|</?think>")
TRAILING_PUNCT = ".,;:!?"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def atomic_append_jsonl(path: Path, row: dict[str, Any]) -> None:
    """Durable per-result write: a long run must not lose completed work."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


class HarnessConfigError(RuntimeError):
    """Configuration is unsafe to evaluate under. Always fail closed."""


class PromptBudgetExceeded(RuntimeError):
    """The rendered prompt plus reserve plus margin would overflow the loaded context.

    Raised before any API call: LM Studio must never be the first component to discover overflow.
    """

    def __init__(self, rendered_prompt_tokens, max_tokens, safety_margin, loaded_context_length):
        self.rendered_prompt_tokens = rendered_prompt_tokens
        self.max_tokens = max_tokens
        self.safety_margin = safety_margin
        self.loaded_context_length = loaded_context_length
        self.total = rendered_prompt_tokens + max_tokens + safety_margin
        super().__init__(
            f"prompt {rendered_prompt_tokens} + reserve {max_tokens} + margin {safety_margin} "
            f"= {self.total} exceeds loaded context {loaded_context_length} "
            f"by {self.total - loaded_context_length}")


class TemplateUnsupported(RuntimeError):
    """The local chat template needs a Jinja helper this renderer does not provide."""


# ---------------------------------------------------------------- runtime artefacts

def load_system_prompt(version: str = "v1") -> str:
    """Backwards-compatible text-only loader."""
    return load_system_prompt_versioned(version)["text"]


def load_system_prompt_versioned(version: str) -> dict[str, Any]:
    """Resolve a known frozen prompt version, verify its SHA, and fail closed on any mismatch."""
    if version not in SYSTEM_PROMPTS:
        raise HarnessConfigError(
            f"unknown system prompt version {version!r}; known: {sorted(SYSTEM_PROMPTS)}")
    entry = SYSTEM_PROMPTS[version]
    path = entry["path"]
    if not path.is_file():
        raise HarnessConfigError(f"frozen system prompt missing: {path}")
    text = path.read_text(encoding="utf-8")
    actual = sha256_text(text)
    if actual != entry["sha256"]:
        raise HarnessConfigError(
            f"system prompt {version} SHA mismatch: expected {entry['sha256']}, got {actual}. "
            "Refusing to evaluate under a modified prompt; create a new version instead of editing.")
    return {"version": version, "name": entry["name"], "path": str(path),
            "text": text, "sha256": actual}


class TemplateRenderer:
    """Renders the ACTUAL local chat_template.jinja. No embedded copy, no approximation."""

    REQUIRED_GLOBALS = ("raise_exception",)

    def __init__(self, model_dir: Path = MODEL_DIR):
        from jinja2 import Environment
        self.model_dir = model_dir
        self.template_path = model_dir / "chat_template.jinja"
        if not self.template_path.is_file():
            raise HarnessConfigError(f"chat template not found: {self.template_path}")
        self.source = self.template_path.read_text(encoding="utf-8")
        self.template_sha256 = sha256_text(self.source)
        self.environment = Environment()
        self.environment.globals["raise_exception"] = self._raise
        self.environment.policies["json.dumps_kwargs"] = {"ensure_ascii": False}
        self._template = self.environment.from_string(self.source)
        self.audit = self.audit_helpers()

    @staticmethod
    def _raise(message: str):
        raise TemplateUnsupported(message)

    def audit_helpers(self) -> dict[str, Any]:
        """Report which helpers the template references, so an unsupported one fails loudly."""
        referenced = sorted(set(re.findall(r"\b(raise_exception|tojson|strftime_now|namespace)\b",
                                           self.source)))
        provided = set(self.environment.globals) | {"namespace", "tojson"}
        missing = [name for name in referenced if name not in provided]
        return {"referenced": referenced, "missing": missing,
                "uses_tools": "tools" in self.source, "supported": not missing}

    def render(self, system: str, user: str, enable_thinking: bool = False,
               add_generation_prompt: bool = True) -> str:
        if self.audit["missing"]:
            raise TemplateUnsupported(f"template needs helpers: {self.audit['missing']}")
        return self._template.render(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            add_generation_prompt=add_generation_prompt, enable_thinking=enable_thinking, tools=None)


class GenerationTokenizer:
    """The generation model's own tokenizer. Never BGE-M3, which is the retrieval tokenizer."""

    def __init__(self, model_dir: Path = MODEL_DIR):
        from tokenizers import Tokenizer
        self.path = model_dir / "tokenizer.json"
        if not self.path.is_file():
            raise HarnessConfigError(f"tokenizer not found: {self.path}")
        self.tokenizer = Tokenizer.from_file(str(self.path))
        self.tokenizer_sha256 = sha256_file(self.path)

    def count(self, text: str) -> int:
        """Authoritative count is over the exact rendered prompt, without extra special tokens."""
        return len(self.tokenizer.encode(text, add_special_tokens=False).ids)


@dataclass(frozen=True)
class GenerationConfig:
    model_id: str = MODEL_ID
    endpoint: str = COMPLETIONS_ENDPOINT
    temperature: float = 0.0
    max_tokens: int | None = None            # pilot_pending until Run 2 measures it
    stop: tuple[str, ...] = STOP_STRINGS
    thinking_mode: str = THINKING_MODE
    tokenizer_sha256: str = ""
    template_sha256: str = ""
    system_prompt_version: str = "v1"
    system_prompt_sha256: str = SYSTEM_PROMPT_SHA256
    loaded_context_length: int = LOADED_CONTEXT_LENGTH
    seed: int | None = 11

    def __post_init__(self):
        if FORBIDDEN_ENDPOINT in self.endpoint or self.endpoint.rstrip("/").endswith("chat/completions"):
            raise HarnessConfigError(
                f"endpoint {self.endpoint} is forbidden: LM Studio's chat endpoint ignores "
                "chat_template_kwargs, so enable_thinking never reaches the template. "
                f"Use {COMPLETIONS_ENDPOINT} with an in-process rendered prompt.")
        if self.endpoint != COMPLETIONS_ENDPOINT:
            raise HarnessConfigError(f"endpoint must be {COMPLETIONS_ENDPOINT}, got {self.endpoint}")

    def config_hash(self) -> str:
        payload = json.dumps({k: (list(v) if isinstance(v, tuple) else v)
                              for k, v in asdict(self).items()}, sort_keys=True)
        return sha256_text(payload)


# ---------------------------------------------------------------- validators

def _strip_trailing(text: str) -> str:
    return text.rstrip(TRAILING_PUNCT)


def validate_citations(answer: str, packet_evidence_ids,
                       excluded_evidence_ids=None) -> dict[str, Any]:
    """Deterministic citation validation. No LLM.

    Two orthogonal axes, deliberately not conflated:

      SYNTAX     - is the handle written in canonical `[E###]` form?
      REFERENCE  - does that handle actually exist in the rendered ContextPacket?

    `[E009]` with correct syntax but no such evidence is *unknown*, never *malformed*: the model
    formatted the citation correctly and referenced something that does not exist, which is a
    different failure from writing `[E01]`.

    Canonical handles are sorted into exactly one semantic bucket, in this precedence:
      1. present in packet_evidence_ids        -> valid_handles
      2. present in excluded_evidence_ids      -> excluded_handle_citations
      3. otherwise                             -> unknown_handles

    NOTE ON EXCLUDED EVIDENCE UNDER CONTEXT v1:
    `ContextPacket.excluded_items` records {chunk_id, rank, reason} and carries **no evidence_id** --
    Evidence IDs are assigned only to selected items, by position, as `E{len(selected)+1:03d}`. An
    excluded chunk therefore never receives an E-handle and never appears in context_text. Under
    Context v1 semantics an excluded-evidence citation is consequently *not representable*: a model
    citing an unrendered handle is indistinguishable from one inventing `[E999]`, and both land in
    `unknown_handles`. IDs are NOT fabricated to close that gap. The `excluded_evidence_ids`
    parameter is a forward-compatible hook for a future context version that assigns stable IDs
    before selection; callers passing real Context v1 packets should leave it empty.
    """
    known = set(packet_evidence_ids or ())
    excluded = set(excluded_evidence_ids or ())
    overlap = known & excluded
    if overlap:
        raise ValueError(f"evidence ids cannot be both present and excluded: {sorted(overlap)}")

    valid_spans = [(m.start(), m.end(), m.group(0)) for m in VALID_HANDLE.finditer(answer)]
    syntactic = [span[2][1:-1] for span in valid_spans]

    in_packet, in_excluded, unknown = [], [], []
    for handle in syntactic:
        if handle in known:
            in_packet.append(handle)
        elif handle in excluded:
            in_excluded.append(handle)
        else:
            unknown.append(handle)

    malformed: list[str] = []
    for match in BRACKET_CANDIDATE.finditer(answer):
        token = match.group(0)
        if not VALID_HANDLE.fullmatch(token):
            malformed.append(token)
    for match in OPEN_UNCLOSED.finditer(answer):
        malformed.append(match.group(0))
    covered = [(s, e) for s, e, _ in valid_spans]
    for match in BARE_CANDIDATE.finditer(answer):
        if any(s <= match.start() and match.end() <= e for s, e in covered):
            continue
        malformed.append(match.group(0))

    return {
        # syntax axis
        "syntactically_valid_handles": sorted(set(syntactic)),
        "syntactically_valid_handle_occurrences": len(syntactic),
        "malformed_citations": sorted(set(malformed)),
        # reference axis - pairwise disjoint by construction
        "valid_handles": sorted(set(in_packet)),
        "excluded_handle_citations": sorted(set(in_excluded)),
        "unknown_handles": sorted(set(unknown)),
        # leaks
        "doc_leaks": sorted(set(DOC_LEAK.findall(answer))),
        "page_leaks": sorted({_strip_trailing(m.strip()) for m in PAGE_LEAK.findall(answer)}),
        "slide_leaks": sorted({_strip_trailing(m.strip()) for m in SLIDE_LEAK.findall(answer)}),
        "path_leaks": sorted({_strip_trailing(m.strip()) for m in PATH_LEAK.findall(answer)}),
        "template_leaks": sorted(set(TEMPLATE_LEAK.findall(answer))),
        "validator_version": VALIDATOR_VERSION,
    }


def validate_abstention(answer: str) -> dict[str, Any]:
    """A marker buried mid-prose is not an abstention; it must open the response."""
    stripped = answer.lstrip()
    marker = None
    if stripped.startswith(ABSTAIN_TR):
        marker = ABSTAIN_TR
    elif stripped.startswith(ABSTAIN_EN):
        marker = ABSTAIN_EN
    present = ABSTAIN_TR in answer or ABSTAIN_EN in answer
    return {"abstention_marker": marker, "abstention_at_start": marker is not None,
            "abstention_marker_present_anywhere": present}


# ---------------------------------------------------------------- result + checkpoint

RESULT_FIELDS = ("query_id", "model_id", "generation_config_hash", "benchmark_sha",
                 "system_prompt_sha", "tokenizer_sha", "template_sha", "context_packet_sha",
                 "prompt_sha", "prompt_tokens_local", "prompt_tokens_api", "prompt_token_delta",
                 "completion_tokens", "answer_tokens", "latency_seconds", "finish_reason",
                 "raw_answer", "syntactically_valid_handles", "syntactically_valid_handle_occurrences",
                 "valid_handles", "excluded_handle_citations", "unknown_handles",
                 "malformed_citations",
                 "doc_leaks", "page_leaks", "slide_leaks", "path_leaks", "template_leaks",
                 "abstention_marker", "abstention_at_start", "language", "started_at",
                 "completed_at")
FORBIDDEN_RESULT_KEYS = ("reasoning_content", "chain_of_thought", "cot", "hidden_reasoning",
                         "reasoning", "thoughts")


def checkpoint_identity(query_id: str, benchmark_sha: str, system_prompt_sha: str, model_id: str,
                        tokenizer_sha: str, template_sha: str, generation_config_hash: str,
                        context_packet_sha: str) -> str:
    """All eight fields participate: a stale result must never survive config drift."""
    return sha256_text("\0".join([query_id, benchmark_sha, system_prompt_sha, model_id,
                                  tokenizer_sha, template_sha, generation_config_hash,
                                  context_packet_sha]))


def is_resumable(stored: dict[str, Any], expected: dict[str, Any]) -> bool:
    keys = ("query_id", "benchmark_sha", "system_prompt_sha", "model_id", "tokenizer_sha",
            "template_sha", "generation_config_hash", "context_packet_sha")
    return all(stored.get(k) == expected.get(k) for k in keys)


def load_checkpoints(path: Path) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue                     # tolerate a torn final line from an interrupted run
        out[row.get("query_id", "")] = row
    return out


# ---------------------------------------------------------------- client

def complete(prompt: str, config: GenerationConfig, max_tokens: int,
             base_url: str = LMSTUDIO_BASE, timeout: int = 1200) -> dict[str, Any]:
    if config.endpoint != COMPLETIONS_ENDPOINT:
        raise HarnessConfigError("refusing to generate on a non-raw-completions endpoint")
    body = {"model": config.model_id, "prompt": prompt, "temperature": config.temperature,
            "max_tokens": max_tokens, "stop": list(config.stop)}
    if config.seed is not None:
        body["seed"] = config.seed
    request = urllib.request.Request(f"{base_url}{config.endpoint}",
                                     data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json"})
    began = time.perf_counter()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read())
    elapsed = time.perf_counter() - began
    choice = payload["choices"][0]
    return {"text": choice.get("text", ""), "finish_reason": choice.get("finish_reason"),
            "usage": payload.get("usage", {}), "latency_seconds": elapsed}


SAFETY_MARGIN = 3596


def validate_prompt_budget(rendered_prompt_tokens: int, max_tokens: int,
                           safety_margin: int = SAFETY_MARGIN,
                           loaded_context_length: int = LOADED_CONTEXT_LENGTH) -> int:
    """Fail closed before generation. Returns headroom on success."""
    if rendered_prompt_tokens < 0:
        raise ValueError("rendered_prompt_tokens must be non-negative")
    if max_tokens <= 0:
        raise ValueError(f"output reserve must be positive, got {max_tokens}")
    if safety_margin < 0:
        raise ValueError(f"safety_margin must be non-negative, got {safety_margin}")
    if loaded_context_length <= 0:
        raise ValueError("loaded_context_length must be positive")
    total = rendered_prompt_tokens + max_tokens + safety_margin
    if total > loaded_context_length:
        raise PromptBudgetExceeded(rendered_prompt_tokens, max_tokens, safety_margin,
                                   loaded_context_length)
    return loaded_context_length - total


def classify_completion(answer: str, finish_reason: str, checks: dict, must_abstain: bool) -> str:
    """A response can stop naturally and still fail the contract; finish_reason alone is not enough."""
    if not answer.strip():
        return "empty"
    if checks.get("template_leaks"):
        return "other_failure"
    if finish_reason == "length":
        return "truncated"
    if must_abstain:
        return "complete" if checks.get("abstention_at_start") else "wrong_abstention"
    if checks.get("abstention_at_start"):
        # Abstaining on an answerable query is a distinct outcome, not a success. It may be correct
        # caution (a compound question only half-supported) or over-abstention; either way it must
        # surface rather than score as `complete`.
        return "unexpected_abstention"
    if checks.get("malformed_citations") or checks.get("unknown_handles"):
        return "invalid_citation"
    if checks.get("doc_leaks") or checks.get("page_leaks") or checks.get("slide_leaks") \
            or checks.get("path_leaks"):
        return "invalid_citation"
    if not checks.get("valid_handles"):
        return "other_failure"
    return "complete"


def preflight() -> dict[str, Any]:
    renderer = TemplateRenderer()
    tokenizer = GenerationTokenizer()
    prompt_text = load_system_prompt()
    config = GenerationConfig(tokenizer_sha256=tokenizer.tokenizer_sha256,
                              template_sha256=renderer.template_sha256)
    rendered = renderer.render(prompt_text, "PREFLIGHT")
    return {
        "harness_version": HARNESS_VERSION, "model_id": MODEL_ID, "upstream_model": UPSTREAM_MODEL,
        "model_dir": str(MODEL_DIR), "loaded_context_length_expected": LOADED_CONTEXT_LENGTH,
        "tokenizer_sha256": tokenizer.tokenizer_sha256,
        "template_sha256": renderer.template_sha256,
        "system_prompt_sha256": sha256_text(prompt_text),
        "system_prompt_verified": sha256_text(prompt_text) == SYSTEM_PROMPT_SHA256,
        "renderer": "jinja2 in-process, actual local chat_template.jinja",
        "template_helper_audit": renderer.audit,
        "endpoint": config.endpoint, "forbidden_endpoint": FORBIDDEN_ENDPOINT,
        "thinking_mode": THINKING_MODE, "stop": list(STOP_STRINGS),
        "generation_config_hash": config.config_hash(),
        "validator_version": VALIDATOR_VERSION,
        "rendered_preflight_prompt_tokens": tokenizer.count(rendered),
        "pre_closed_think_block": rendered.endswith("<|im_start|>assistant\n<think>\n\n</think>\n\n"),
        "benchmark_status": "NOT BUILT", "pilot_status": "PENDING",
        "max_tokens": "pilot_pending",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="TunnelBookAI generation evaluation harness")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--validate-answer")
    parser.add_argument("--evidence-ids", default="")
    for flag in ("--pilot", "--resume", "--grade", "--report"):
        parser.add_argument(flag, action="store_true")
    parser.add_argument("--run-query")
    parser.add_argument("--run-range", nargs=2)
    args = parser.parse_args()

    if args.preflight:
        print(json.dumps(preflight(), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.validate_answer:
        ids = [i for i in args.evidence_ids.split(",") if i]
        result = {**validate_citations(args.validate_answer, ids),
                  **validate_abstention(args.validate_answer)}
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.pilot or args.run_query or args.run_range or args.resume or args.grade or args.report:
        print(json.dumps({"error": "benchmark_not_built",
                          "detail": "generation_eval_v1.jsonl does not exist; author and freeze the "
                                    "benchmark before running, resuming, grading or reporting.",
                          "benchmark_status": "NOT BUILT"}, indent=2))
        return 2
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
