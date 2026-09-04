"""TunnelBookAI production grounded generator v1 - the canonical production orchestration path.

    QUERY -> Retriever v1 -> ContextPacket v1 -> Prompt v5 -> Generator -> Output Contract v1.1
          -> ACCEPT / REJECT -> immutable audit record

Every stage is delegated to its frozen implementation; nothing is reimplemented here. This module
is orchestration and policy only: it decides what to call, in what order, what to refuse, and what
to record. It contains no retrieval logic, no context assembly, no citation semantics and no
language detection of its own.

Policy is fail-closed throughout:
  * startup refuses to serve if any frozen identity or the Qdrant collection does not match,
  * a query whose language cannot be determined is rejected rather than guessed,
  * a prompt that does not fit its budget is rejected before generation rather than truncated,
  * a contract-invalid answer is never released, never repaired and never retried.

Retrieval is read-only. Nothing in this path writes to Qdrant.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import importlib.util
import json
import os
import sys
import time
import urllib.request
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / "data/production"
AUDIT_LOG = PRODUCTION / "generation_audit_v1.jsonl"
ACCEPTED_LOG = PRODUCTION / "accepted_generations_v1.jsonl"
REJECTED_LOG = PRODUCTION / "rejected_generations_v1.jsonl"
DEBUG_RAW_LOG = PRODUCTION / "debug_raw_generations_v1.jsonl"

VERSION = "tunnelbook-production-grounded-generator-v1"
PRODUCTION_POLICY = "accept_if_contract_valid_else_reject"

# Frozen identities. Startup refuses to serve unless every one of these matches exactly.
RETRIEVER_SCRIPT_SHA = "8ada31f64d8ef51c3b4d3b8b04f3fcc3e9fb7338b1554d1a5a9118a3a231b071"
PROMPT_V5_SHA = "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085"
CONTRACT_V1_1_SHA = "5ebf8fe90e3e5491ce07a9143f8fd377841defa2e0e7a09188f3a835b07bdef5"
TOKENIZER_SHA = "87a7830d63fcf43bf241c3c5242e96e62dd3fdc29224ca26fed8ea333db72de4"
TEMPLATE_SHA = "e84f32a23fdda27689f868aa4a1a5621f41133e51a48d7f3efcbea2839574259"
QDRANT_COLLECTION = "tunnelbook_dense_v1"
QDRANT_EXPECTED_POINTS = 5992
QDRANT_URL = os.environ.get("TUNNELBOOK_QDRANT_URL", "http://localhost:6333")
LMSTUDIO_URL = os.environ.get("TUNNELBOOK_LMSTUDIO", "http://127.0.0.1:1234")

SYSTEM_PROMPT_VERSION = "v5"
MODEL_ID = "qwen3.6-35b-a3b-mlx"
TEMPERATURE, SEED, MAX_TOKENS = 0.0, 11, 3072
LOADED_CONTEXT = 71936
DEFAULT_TOP_K = 20                      # Context v1's frozen production default
DEFAULT_CONTEXT_TOKEN_BUDGET = 64610    # the frozen planning budget the benchmark packets used
SUPPORTED_LANGUAGES = ("tr", "en")

SAFE_REJECT_MESSAGE = {
    "tr": "Bu yanıt doğrulama sözleşmesini geçemedi. Yanıt yayımlanmadı.",
    "en": "This response failed the output validation contract and was not released.",
}


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


retriever_v1 = _load("retriever_v1", "scripts/19_retriever_v1.py")
rag_context = _load("rag_context", "scripts/20_rag_context.py")
gen = _load("generation_eval", "scripts/21_generation_model_eval.py")
contract = _load("output_contract_v1_1", "scripts/31_generation_output_contract_v1_1.py")


class StartupRefused(RuntimeError):
    """A frozen identity or backing service does not match; the orchestrator will not serve."""


class RequestRejected(ValueError):
    """The request itself is not servable - refused before any model call."""


# ---------------------------------------------------------------- request / result

@dataclass(frozen=True)
class RetryPolicy:
    """Placeholder for a future controlled-retry experiment. v1 ships disabled.

    Same-config retry measured 0/4 recovery on the frozen benchmark, so retrying an identical
    request cannot help; a changed-seed policy is a separate experiment that has not been run.
    """
    enabled: bool = False
    kind: str = "disabled"
    max_attempts: int = 1

    def __post_init__(self):
        if self.enabled:
            raise StartupRefused("retry is not implemented in production v1; keep it disabled")


@dataclass
class ProductionGenerationRequest:
    query: str
    query_language: str | None = None
    request_id: str | None = None
    top_k: int = DEFAULT_TOP_K
    context_token_budget: int = DEFAULT_CONTEXT_TOKEN_BUDGET
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.query, str) or not self.query.strip():
            raise RequestRejected("query must be a non-empty string")
        if self.query_language is not None and self.query_language not in SUPPORTED_LANGUAGES:
            raise RequestRejected(f"unsupported query_language {self.query_language!r}; "
                                  f"supported: {SUPPORTED_LANGUAGES}")
        if not isinstance(self.top_k, int) or isinstance(self.top_k, bool):
            raise RequestRejected("top_k must be an integer")
        if not 1 <= self.top_k <= retriever_v1.MAXIMUM_TOP_K:
            raise RequestRejected(f"top_k must be within 1..{retriever_v1.MAXIMUM_TOP_K}")
        if not isinstance(self.context_token_budget, int) or self.context_token_budget <= 0:
            raise RequestRejected("context_token_budget must be a positive integer")
        if self.request_id is None:
            self.request_id = str(uuid.uuid4())


@dataclass
class ProductionGenerationResult:
    status: str                       # "accepted" | "rejected"
    request_id: str
    answer: str | None
    failure_reasons: list[str]
    safe_message: str | None
    evidence_handles: list[str]
    context_packet_sha: str | None
    audit_id: str
    latency: dict[str, float]
    generation_identity: dict[str, Any] | None = None
    contract_identity: dict[str, Any] | None = None

    def to_public_dict(self) -> dict[str, Any]:
        """What a normal production caller sees. A rejected answer is never included."""
        if self.status == "accepted":
            return {"status": self.status, "request_id": self.request_id, "answer": self.answer,
                    "evidence_handles": self.evidence_handles,
                    "context_packet_sha": self.context_packet_sha,
                    "generation_identity": self.generation_identity,
                    "contract_identity": self.contract_identity,
                    "audit_id": self.audit_id, "latency": self.latency}
        if self.status == "dry_run":
            # Diagnostic shape: what WOULD have been sent, with no answer because none was made.
            return {"status": self.status, "request_id": self.request_id,
                    "evidence_handles": self.evidence_handles,
                    "context_packet_sha": self.context_packet_sha,
                    "audit_id": self.audit_id, "latency": self.latency}
        return {"status": self.status, "request_id": self.request_id,
                "failure_reasons": self.failure_reasons, "safe_message": self.safe_message,
                "audit_id": self.audit_id, "latency": self.latency}


# ---------------------------------------------------------------- helpers

def _sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    """Append one JSON object per line. json.dumps escapes control characters, so a query
    containing newlines or braces cannot corrupt the log structure."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def qdrant_collection_state(url: str = QDRANT_URL) -> tuple[int, str]:
    with urllib.request.urlopen(f"{url}/collections/{QDRANT_COLLECTION}", timeout=10) as response:
        result = json.loads(response.read())["result"]
    return result["points_count"], result["status"]


def detect_query_language(query: str) -> dict[str, Any]:
    """Delegated to the frozen contract detector. No second model, no separate heuristic here."""
    return contract.detect_language(query)


# ---------------------------------------------------------------- startup / health

def verify_frozen_identities(tokenizer=None, renderer=None) -> dict[str, Any]:
    checks: dict[str, dict[str, Any]] = {}
    failures: list[str] = []

    def check(name, actual, expected):
        ok = actual == expected
        checks[name] = {"expected": expected, "actual": actual, "ok": ok}
        if not ok:
            failures.append(name)

    check("retriever_script_sha", retriever_v1.script_sha256(), RETRIEVER_SCRIPT_SHA)
    check("retriever_release", retriever_v1.RELEASE_NAME, "tunnelbook-retriever-v1")
    check("context_contract_version", rag_context.CONTEXT_CONTRACT_VERSION, "tunnelbook-context-v1")
    check("context_retriever_script_sha", rag_context.retriever_v1.script_sha256(),
          RETRIEVER_SCRIPT_SHA)
    check("system_prompt_v5_sha", _sha_file(ROOT / "data/metadata/generation_system_prompt_v5.txt"),
          PROMPT_V5_SHA)
    check("output_contract_sha", _sha_file(ROOT / "scripts/31_generation_output_contract_v1_1.py"),
          CONTRACT_V1_1_SHA)
    check("output_contract_version", contract.CONTRACT_VERSION,
          "tunnelbook-generation-output-contract-v1.1")
    check("output_contract_repair_policy", contract.REPAIR_POLICY, "none_fail_closed")
    check("validator_version", contract.VALIDATOR_VERSION, "citation-validator-v1.2")
    check("marker_mapping", contract.MARKER_FOR_LANGUAGE,
          {"tr": "YETERSİZ KANIT", "en": "INSUFFICIENT EVIDENCE"})
    check("model_id", gen.MODEL_ID, MODEL_ID)
    check("endpoint", gen.COMPLETIONS_ENDPOINT, "/v1/completions")
    check("thinking_mode", gen.THINKING_MODE, "non_thinking_via_local_template")
    check("loaded_context_length", gen.LOADED_CONTEXT_LENGTH, LOADED_CONTEXT)

    if tokenizer is not None:
        check("tokenizer_sha", tokenizer.tokenizer_sha256, TOKENIZER_SHA)
    if renderer is not None:
        check("template_sha", renderer.template_sha256, TEMPLATE_SHA)
    return {"checks": checks, "failures": failures, "ok": not failures}


class ProductionGroundedGenerator:
    """Holds the frozen runtime. Constructing it performs the fail-closed startup verification."""

    def __init__(self, retry_policy: RetryPolicy | None = None, verify_services: bool = True,
                 debug_save_raw: bool = False):
        self.retry_policy = retry_policy or RetryPolicy()
        self.debug_save_raw = bool(debug_save_raw)
        self.tokenizer = gen.GenerationTokenizer()
        self.renderer = gen.TemplateRenderer()
        self.prompt = gen.load_system_prompt_versioned(SYSTEM_PROMPT_VERSION)
        self.config = gen.GenerationConfig(
            max_tokens=MAX_TOKENS, temperature=TEMPERATURE, seed=SEED,
            tokenizer_sha256=self.tokenizer.tokenizer_sha256,
            template_sha256=self.renderer.template_sha256,
            system_prompt_version=SYSTEM_PROMPT_VERSION,
            system_prompt_sha256=self.prompt["sha256"])

        identity = verify_frozen_identities(self.tokenizer, self.renderer)
        if not identity["ok"]:
            raise StartupRefused(json.dumps(
                {"error": "frozen_identity_mismatch", "failed_checks": identity["failures"],
                 "detail": {k: v for k, v in identity["checks"].items() if not v["ok"]}},
                ensure_ascii=False))
        self.identity = identity

        self.qdrant_points, self.qdrant_status = (None, None)
        if verify_services:
            try:
                points, status = qdrant_collection_state()
            except Exception as error:
                raise StartupRefused(json.dumps(
                    {"error": "qdrant_unavailable", "detail": f"{type(error).__name__}: {error}"}))
            if points != QDRANT_EXPECTED_POINTS or status != "green":
                raise StartupRefused(json.dumps(
                    {"error": "qdrant_state_mismatch", "expected_points": QDRANT_EXPECTED_POINTS,
                     "actual_points": points, "status": status}))
            self.qdrant_points, self.qdrant_status = points, status
        self._retriever = None

    @property
    def retriever(self):
        if self._retriever is None:
            self._retriever = retriever_v1.RetrieverV1()
        return self._retriever

    # ---- stages ---------------------------------------------------------------------------

    def resolve_language(self, request: ProductionGenerationRequest) -> tuple[str, str]:
        if request.query_language is not None:
            return request.query_language, "provided"
        detected = detect_query_language(request.query)
        if detected["language"] is None:
            raise RequestRejected("query_language_ambiguous")
        return detected["language"], f"detected_{detected['status']}"

    def build_packet(self, request: ProductionGenerationRequest):
        """Context v1, measured with the real generation tokenizer rather than the provisional one."""
        return rag_context.assemble_context(
            query=request.query, retrieval_top_k=request.top_k,
            context_max_tokens=request.context_token_budget,
            retriever=self.retriever, token_counter=self.tokenizer.count)

    def render_prompt(self, packet, query: str) -> str:
        user = f"EVIDENCE PACKET:\n\n{packet.context_text}\n\nQUESTION: {query}"
        return self.renderer.render(self.prompt["text"], user, enable_thinking=False,
                                    add_generation_prompt=True)

    # ---- main path ------------------------------------------------------------------------

    def generate(self, request: ProductionGenerationRequest,
                 dry_run: bool = False) -> ProductionGenerationResult:
        began_total = time.perf_counter()
        audit_id = str(uuid.uuid4())
        latency: dict[str, float] = {}

        language, language_status = self.resolve_language(request)

        began = time.perf_counter()
        packet = self.build_packet(request)
        latency["retrieval_and_context_seconds"] = round(time.perf_counter() - began, 4)

        context_packet_sha = _sha_text(packet.to_json(indent=None))
        context_text_sha = _sha_text(packet.context_text)
        evidence_ids = [item.evidence_id for item in packet.evidence_items]

        began = time.perf_counter()
        rendered = self.render_prompt(packet, request.query)
        prompt_tokens_local = self.tokenizer.count(rendered)
        latency["prompt_render_seconds"] = round(time.perf_counter() - began, 4)

        # Hard budget guard. Never truncate silently to fit.
        gen.validate_prompt_budget(prompt_tokens_local, MAX_TOKENS)

        base_audit = {
            "audit_id": audit_id, "request_id": request.request_id, "timestamp": _now(),
            "query": request.query, "query_language": language,
            "query_language_status": language_status,
            "retriever_release": retriever_v1.RELEASE_NAME,
            "retriever_sha": retriever_v1.script_sha256(),
            "retrieval_top_k": request.top_k,
            "retrieved_chunk_ids": [item.chunk_id for item in packet.evidence_items],
            "context_contract_version": rag_context.CONTEXT_CONTRACT_VERSION,
            "context_packet_sha": context_packet_sha, "context_text_sha": context_text_sha,
            "context_token_count": packet.token_count,
            "context_token_budget": packet.token_budget,
            "context_selected_count": packet.selected_count,
            "context_insufficient_evidence": packet.insufficient_evidence,
            "system_prompt_version": self.prompt["name"],
            "system_prompt_sha": self.prompt["sha256"],
            "model_id": self.config.model_id, "tokenizer_sha": self.tokenizer.tokenizer_sha256,
            "template_sha": self.renderer.template_sha256,
            "generation_config_hash": self.config.config_hash(),
            "prompt_sha": _sha_text(rendered), "prompt_tokens_local": prompt_tokens_local,
            "orchestrator_version": VERSION,
            "production_policy": PRODUCTION_POLICY,
            "retry_policy": self.retry_policy.kind,
        }

        if dry_run:
            latency["total_seconds"] = round(time.perf_counter() - began_total, 4)
            _append_jsonl(AUDIT_LOG, {**base_audit, "production_action": "dry_run",
                                      "contract_valid": None, "failure_reasons": [],
                                      "raw_answer_sha": None, "latency": latency})
            return ProductionGenerationResult(
                status="dry_run", request_id=request.request_id, answer=None, failure_reasons=[],
                safe_message=None, evidence_handles=evidence_ids,
                context_packet_sha=context_packet_sha, audit_id=audit_id, latency=latency)

        began = time.perf_counter()
        response = gen.complete(rendered, self.config, max_tokens=MAX_TOKENS)
        latency["generation_seconds"] = round(time.perf_counter() - began, 4)

        raw_answer = response["text"]                     # never mutated from here on
        raw_answer_sha = _sha_text(raw_answer)
        usage = response.get("usage", {})

        began = time.perf_counter()
        verdict = contract.enforce(raw_answer, language, set(evidence_ids))
        latency["contract_seconds"] = round(time.perf_counter() - began, 4)
        if verdict.raw_answer_sha != raw_answer_sha:
            raise RuntimeError("contract received an answer other than the raw model output")

        latency["total_seconds"] = round(time.perf_counter() - began_total, 4)
        action = "accept" if verdict.contract_valid else "reject"

        audit = {**base_audit,
                 "prompt_tokens_api": usage.get("prompt_tokens"),
                 "prompt_token_delta": (usage.get("prompt_tokens") or 0) - prompt_tokens_local,
                 "completion_tokens": usage.get("completion_tokens"),
                 "answer_tokens": self.tokenizer.count(raw_answer),
                 "finish_reason": response.get("finish_reason"),
                 "raw_answer_sha": raw_answer_sha,          # text itself is deliberately not logged
                 "contract_version": verdict.contract_version,
                 "contract_sha": verdict.contract_sha256,
                 "contract_valid": verdict.contract_valid,
                 "failure_reasons": list(verdict.failure_reasons),
                 "answer_body_language": verdict.answer_body_language,
                 "marker_language_valid": verdict.marker_language_valid,
                 "citation_coverage": verdict.citation_coverage,
                 "material_claim_count": verdict.material_claim_count,
                 "claims_with_citation": verdict.claims_with_citation,
                 "citation_coverage_status": verdict.citation_coverage_status,
                 "production_action": action, "latency": latency}
        _append_jsonl(AUDIT_LOG, audit)

        if self.debug_save_raw:
            _append_jsonl(DEBUG_RAW_LOG, {"audit_id": audit_id, "request_id": request.request_id,
                                          "created_at": _now(), "raw_answer": raw_answer,
                                          "raw_answer_sha": raw_answer_sha,
                                          "contract_valid": verdict.contract_valid})

        provenance = [{"evidence_id": item.evidence_id, "chunk_id": item.chunk_id,
                       "document_id": item.document_id, "title": item.title,
                       "citation_mode": item.citation_mode,
                       "provenance_status": item.provenance_status,
                       "page_start": item.original_page_start, "page_end": item.original_page_end,
                       "slide_start": item.slide_start, "slide_end": item.slide_end,
                       "source_relative_path": item.source_relative_path,
                       "retrieval_rank": item.retrieval_rank,
                       "retrieval_score": item.retrieval_score}
                      for item in packet.evidence_items]

        if verdict.contract_valid:
            visible = _visible_handles(raw_answer)
            _append_jsonl(ACCEPTED_LOG, {
                "request_id": request.request_id, "audit_id": audit_id, "query": request.query,
                "answer": raw_answer, "visible_evidence_handles": visible,
                "context_packet_sha": context_packet_sha, "created_at": _now(),
                "internal_provenance": provenance})
            return ProductionGenerationResult(
                status="accepted", request_id=request.request_id, answer=raw_answer,
                failure_reasons=[], safe_message=None, evidence_handles=visible,
                context_packet_sha=context_packet_sha, audit_id=audit_id, latency=latency,
                generation_identity={"model_id": self.config.model_id,
                                     "system_prompt_version": self.prompt["name"],
                                     "system_prompt_sha": self.prompt["sha256"],
                                     "generation_config_hash": self.config.config_hash()},
                contract_identity={"contract_version": verdict.contract_version,
                                   "contract_sha256": verdict.contract_sha256,
                                   "repair_policy": verdict.repair_policy})

        # Rejected: the raw answer is not released and its text is not written to any normal log.
        _append_jsonl(REJECTED_LOG, {
            "request_id": request.request_id, "audit_id": audit_id, "query": request.query,
            "failure_reasons": list(verdict.failure_reasons),
            "raw_answer_sha": raw_answer_sha, "created_at": _now()})
        return ProductionGenerationResult(
            status="rejected", request_id=request.request_id, answer=None,
            failure_reasons=list(verdict.failure_reasons),
            safe_message=SAFE_REJECT_MESSAGE[language], evidence_handles=[],
            context_packet_sha=context_packet_sha, audit_id=audit_id, latency=latency)


def _visible_handles(answer: str) -> list[str]:
    """The [E###] handles the model actually cited, in canonical form only."""
    return sorted({m.strip("[]") for m in contract.HANDLE.findall(answer)})


# ---------------------------------------------------------------- public API

_RUNTIME: ProductionGroundedGenerator | None = None


def _runtime(**kwargs) -> ProductionGroundedGenerator:
    global _RUNTIME
    if _RUNTIME is None:
        _RUNTIME = ProductionGroundedGenerator(**kwargs)
    return _RUNTIME


def generate_grounded(query: str, query_language: str | None = None,
                      request_id: str | None = None, **kwargs) -> ProductionGenerationResult:
    """Canonical production call: retrieve, ground, generate, enforce, decide, audit."""
    request = ProductionGenerationRequest(query=query, query_language=query_language,
                                          request_id=request_id,
                                          top_k=kwargs.pop("top_k", DEFAULT_TOP_K),
                                          context_token_budget=kwargs.pop(
                                              "context_token_budget", DEFAULT_CONTEXT_TOKEN_BUDGET),
                                          metadata=kwargs.pop("metadata", {}))
    return _runtime(**kwargs).generate(request)


def healthcheck() -> dict[str, Any]:
    """Verify every dependency and frozen identity without generating anything."""
    report: dict[str, Any] = {"version": VERSION, "checked_at": _now(), "checks": {}}
    failures: list[str] = []

    try:
        tokenizer = gen.GenerationTokenizer()
        renderer = gen.TemplateRenderer()
        identity = verify_frozen_identities(tokenizer, renderer)
        report["checks"]["frozen_identities"] = {
            "ok": identity["ok"], "failed": identity["failures"]}
        failures += identity["failures"]
    except Exception as error:
        report["checks"]["frozen_identities"] = {"ok": False,
                                                 "error": f"{type(error).__name__}: {error}"}
        failures.append("frozen_identities")

    try:
        points, status = qdrant_collection_state()
        ok = points == QDRANT_EXPECTED_POINTS and status == "green"
        report["checks"]["qdrant"] = {"ok": ok, "collection": QDRANT_COLLECTION,
                                      "points": points, "status": status,
                                      "expected_points": QDRANT_EXPECTED_POINTS}
        if not ok:
            failures.append("qdrant")
    except Exception as error:
        report["checks"]["qdrant"] = {"ok": False, "error": f"{type(error).__name__}: {error}"}
        failures.append("qdrant")

    try:
        with urllib.request.urlopen(f"{LMSTUDIO_URL}/v1/models", timeout=10) as response:
            models = [m["id"] for m in json.loads(response.read())["data"]]
        ok = MODEL_ID in models
        report["checks"]["lm_studio"] = {"ok": ok, "required_model": MODEL_ID,
                                         "model_available": ok}
        if not ok:
            failures.append("lm_studio")
    except Exception as error:
        report["checks"]["lm_studio"] = {"ok": False, "error": f"{type(error).__name__}: {error}"}
        failures.append("lm_studio")

    report["status"] = "healthy" if not failures else "unhealthy"
    report["failures"] = failures
    return report


# ---------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="TunnelBookAI production grounded generator v1")
    parser.add_argument("--query", help="the production query")
    parser.add_argument("--language", choices=list(SUPPORTED_LANGUAGES),
                        help="query language; deterministic detection is used when omitted")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--context-token-budget", type=int, default=DEFAULT_CONTEXT_TOKEN_BUDGET)
    parser.add_argument("--json", action="store_true", help="emit the structured result")
    parser.add_argument("--healthcheck", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="retrieve, build context and render the prompt; never generate")
    parser.add_argument("--debug-save-raw", action="store_true",
                        help="development only: persist raw model output to a debug artifact")
    args = parser.parse_args(argv)

    if args.healthcheck:
        report = healthcheck()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["status"] == "healthy" else 1

    if not args.query:
        parser.error("--query is required unless --healthcheck is used")

    try:
        runtime = ProductionGroundedGenerator(debug_save_raw=args.debug_save_raw)
        request = ProductionGenerationRequest(
            query=args.query, query_language=args.language, top_k=args.top_k,
            context_token_budget=args.context_token_budget)
        result = runtime.generate(request, dry_run=args.dry_run)
    except StartupRefused as error:
        print(json.dumps({"status": "startup_refused", "detail": json.loads(str(error))},
                         ensure_ascii=False, indent=2))
        return 2
    except RequestRejected as error:
        print(json.dumps({"status": "request_rejected", "reason": str(error)},
                         ensure_ascii=False, indent=2))
        return 3

    payload = result.to_public_dict()
    if args.json or args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif result.status == "accepted":
        print(result.answer)
    else:
        print(result.safe_message)
    return 0 if result.status in ("accepted", "dry_run") else 1


if __name__ == "__main__":
    raise SystemExit(main())
