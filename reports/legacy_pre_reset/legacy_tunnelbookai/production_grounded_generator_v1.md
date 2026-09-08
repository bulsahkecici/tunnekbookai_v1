# Production Grounded Generator v1

## Executive Decision

**PRODUCTION GROUNDED GENERATOR V1 — CLOSED / GO**

`tunnelbook-production-grounded-generator-v1`, entrypoint
`scripts/36_production_grounded_generator.py`, status **frozen**.

The canonical production path — retrieve, ground, generate, enforce, decide, audit — is live and
fail-closed. The 16-case orchestration smoke suite passes **16/16**, **zero** contract failures were
released, Qdrant is unchanged at 5992 with **0 writes**, and the full suite is at **1114 tests**.

This ships a *guarded* stack. The bare generator is still **NEEDS IMPROVEMENT**; what makes it
deployable is an enforcement layer that fails closed and never repairs.

## Architecture

```
ProductionGenerationRequest
        │
        ├─ fail-closed startup: frozen SHAs + Qdrant 5992/green  ──► StartupRefused
        ├─ query language: explicit, else deterministic detection ──► RequestRejected
        │                                                              (ambiguous)
        ▼
  Retriever v1 ──► ContextPacket v1 ──► Prompt v5 render ──► budget guard ──► reject before
        │              (real gen tokenizer)                                    generation
        ▼
  /v1/completions  (temp 0.0, seed 11, max_tokens 3072)
        ▼
  raw_answer  ──sha──►  Output Contract v1.1  ──►  ACCEPT  ──► answer + [E###] + provenance
                                               └►  REJECT  ──► safe message only
        ▼
  immutable audit record  (raw text never in the main log)
```

Orchestration and policy only. The module contains no retrieval logic, no context assembly, no
citation semantics and no language detection of its own — a test asserts the absence of
`validate_citations`, `assemble_context`, `build_evidence`, `embed_query` and `enforce(`
definitions in it.

## Frozen Dependencies

| Component | Identity |
|---|---|
| Retriever | `tunnelbook-retriever-v1`, script SHA `8ada31f6…b071`, collection `tunnelbook_dense_v1` |
| Context | `tunnelbook-context-v1` + `tunnelbook-citation-v1` |
| Prompt | `generation-system-prompt-v5`, SHA `9bae1362…4085` |
| Model | `qwen3.6-35b-a3b-mlx`, LM Studio / MLX, `/v1/completions`, non-thinking, ctx 71936 |
| Tokenizer | `87a7830d…2de4` |
| Template | `e84f32a2…4259` |
| Output Contract | `tunnelbook-generation-output-contract-v1.1`, SHA `5ebf8fe9…def5` |
| Validator | `citation-validator-v1.2` |
| Repair policy | `none_fail_closed` |

Startup verifies **16 identity checks** plus the Qdrant collection. Any mismatch raises
`StartupRefused` with structured detail and **no query is served**. A test tampers with the
contract version in memory and asserts the refusal fires.

## Request Contract

`ProductionGenerationRequest(query, query_language=None, request_id=None, top_k=20,
context_token_budget=64610, metadata={})`.

`request_id` is auto-assigned as UUID4 when absent and flows into every artifact. Validation is
strict and refuses before any model call: empty/non-string query, unsupported language, `top_k`
outside `1..100` (Retriever v1's own bound), non-positive budget. Defaults are the frozen
production values — `top_k=20` is Context v1's own `DEFAULT_RETRIEVAL_TOP_K`, asserted equal by
test so the default cannot drift silently.

## Retrieval

Delegated wholly to `RetrieverV1`. Full provenance is preserved into the packet and the audit
record: `chunk_id`, `document_id`, rank, score, citation mode, provenance status, page/slide
coordinates and source path. Retrieval is **read-only** — a test greps the entrypoint for `upsert`,
`delete_collection`, `create_collection`, `set_payload`, `delete_points` and
`recreate_collection`, and the smoke run measured Qdrant 5992 → 5992, **0 writes**.

## Context Construction

`rag_context.assemble_context(...)` with one deliberate production choice: the token counter passed
in is **the real generation tokenizer**, not Context v1's provisional whitespace counter. The
budget therefore governs the actual rendered prompt in the units the model measures.

Each packet yields `context_packet_sha` (over the deterministic packet JSON) and `context_text_sha`,
both computed after assembly and never recomputed on mutated content.

## Prompt Rendering

Prompt v5 through the version-aware loader (which verifies its own SHA), rendered with the **actual
local `chat_template.jinja`** at `enable_thinking=False`, `add_generation_prompt=True`,
`tools=None`. The exact rendered string is what goes to `/v1/completions`.

## Generation

Frozen config: `temperature=0.0`, `seed=11`, `max_tokens=3072`,
`stop=["<|im_end|>","<|im_start|>"]`. No sweep, no fallback model.

The budget guard runs **before** generation:
`rendered_prompt_tokens + max_tokens + safety_margin ≤ 71936`. A prompt that does not fit is
rejected, never silently truncated. Token accounting is recorded per request; across the smoke run
`prompt_token_delta` was **0** for every request.

## Output Contract

`contract.enforce(raw_answer, query_language, exposed_evidence_ids)`. The orchestrator asserts that
the SHA the contract reports equals the SHA of the raw response, so a mismatch between "what was
generated" and "what was judged" is a hard runtime error rather than a silent divergence.

## Accept / Reject Policy

`accept_if_contract_valid_else_reject`, with nothing in between.

**Accepted** returns the answer with its visible `[E###]` handles, `context_packet_sha`, generation
identity, contract identity and `audit_id`.

**Rejected** returns *only* status, request id, failure reasons, a deterministic safe message and
`audit_id`. `to_public_dict()` structurally omits the answer key on the reject path, and a test
asserts the rejected text appears nowhere in the serialised payload.

Safe messages are fixed strings, never generated:

- TR — "Bu yanıt doğrulama sözleşmesini geçemedi. Yanıt yayımlanmadı."
- EN — "This response failed the output validation contract and was not released."

No replacement answer is ever fabricated.

## No-Repair Policy

Inherited from the contract and enforced at the orchestration boundary. The strongest available
assertion is made by test: `contract.enforce` is intercepted and the exact string it received is
compared against the raw model output — a malformed `(E001)` reaches the contract **intact**. The
orchestrator never rewrites a marker, translates a body, normalises a citation or inserts a handle.

## Retry Policy

**Disabled.** `RetryPolicy` exists as a typed placeholder for a future experiment and *refuses to
be constructed with `enabled=True`*. Same-config retry measured 0/4 recovery on the frozen
benchmark, so retrying an identical request cannot help.

On rejection the orchestrator does not retrieve again, change `top_k`, change evidence, change the
prompt, or regenerate. Tests assert generation is called exactly once per request and retrieval
exactly once even when the contract rejects.

## Provenance

Two layers, deliberately separated.

**Model-visible** stays `[E###]` only — the orchestrator never asks the model to emit document ids,
paths or page coordinates, and the contract still rejects coordinate leaks.

**Internal** keeps the full mapping for audit and future book traceability: evidence id → chunk id,
document id, title, citation mode, provenance status, page/slide range, source path, retrieval rank
and score. Stored with accepted generations, not exposed in the public payload.

## Audit Logging

Append-only JSONL at `data/production/generation_audit_v1.jsonl`, one row per request, carrying all
30 required fields: ids, timestamp, query, language, retriever release/SHA/top-k/chunk ids, context
contract version, packet and text SHAs, token counts, prompt version/SHA, model, tokenizer,
template, config hash, prompt SHA, token accounting, `raw_answer_sha`, contract version/SHA,
validity, failure reasons, action and latency breakdown.

**Raw answer text is never written to the main audit log** — only its SHA. Accepted answers live in
`accepted_generations_v1.jsonl`; rejected records carry `raw_answer_sha` and **no text at all**.
A test writes a malformed answer and asserts its text appears in neither log. `--debug-save-raw` is
opt-in, off by default, and writes to a separate artifact; a test asserts the debug file does not
exist unless explicitly enabled — and that when enabled the stored text is byte-identical, proving
no repair occurred.

## User-Facing Output

Accepted answers retain their `[E###]` citation grammar (verified across all 13 accepted smoke
answers). Rejected requests receive the safe message and nothing else. Internal coordinates never
reach the caller.

## Healthcheck

`--healthcheck` verifies LM Studio reachability and model availability, Qdrant reachability and
`5992/green`, and all frozen identities — **without generating anything**. Returns structured
`healthy` / `unhealthy` with per-check detail and a non-zero exit on failure. Verified healthy.

## Dry Run

`--dry-run` retrieves, builds context, renders the prompt and validates the budget, then stops. A
test replaces `gen.complete` with a call recorder and asserts it is **never invoked**. The audit row
records `production_action: dry_run` with a null `raw_answer_sha`.

## Security Boundaries

- **Evidence is untrusted data.** Context v1's untrusted-evidence boundary and injection notice are
  preserved verbatim; the orchestrator adds no path by which evidence text could reach a shell, the
  filesystem, an import or a tool.
- **The user query is data too.** It cannot alter the system prompt, model configuration, contract
  behaviour, retrieval implementation or audit policy — all of those are module constants verified
  at startup, not request fields.
- **No interpolation.** A test asserts the entrypoint contains no `os.system`, `subprocess.`,
  `eval(`, `exec(`, `__import__`, `shell=True` or `os.popen`. The query never reaches a path,
  import or collection name.
- **Log integrity.** All logs are written with `json.dumps`. A test submits a query containing
  `"}`, a raw newline, a CR and a NUL escape, then asserts the audit file still has exactly one
  line, round-trips, and contains no injected key.
- **Adversarial smoke cases** (imperative-bearing regulatory and security evidence) were answered
  without template leak, coordinate leak or instruction compliance.

## Smoke Test

**16/16 PASS.** 4 factual, 2 numeric, 2 multi-source, 2 cross-lingual, 2 must-abstain,
2 adversarial, 2 contract-failure diagnostics. 13 accepted, 3 rejected,
**contract failures released: 0**, audit rows +16, Qdrant 5992 → 5992 with 0 writes.

This validates **orchestration, not model quality** — no generalisation metric may be claimed from
16 cases.

Two findings worth recording:

- The contract-failure cases use **frozen fixtures** (GEV042, GEV062) injected at the generation
  boundary, so the reject path is exercised deterministically instead of hoping the model
  reproduces a malformed answer. The injection is test-time only; the orchestrator has no
  answer-injection parameter, so no production backdoor exists.
- **SMK-A1 was rejected live.** A genuine new production query — the daily Marmaray ridership for
  2025, which the corpus cannot answer — produced a Turkish-query answer with the English marker and
  an English body, and the contract caught it with
  `wrong_abstention_marker_language` + `answer_body_language_mismatch`. That is the known v5 defect
  firing on traffic that appears in no benchmark, and being contained.

## Performance

Per-request, over the smoke run (seconds):

| Stage | median | p90 | max |
|---|---|---|---|
| retrieval + context | 0.541 | 0.699 | 7.784 |
| prompt render | 0.022 | 0.030 | 0.039 |
| generation | 16.311 | 25.616 | 29.737 |
| **contract** | **0.0031** | **0.0051** | **0.0064** |
| total | 16.784 | 27.116 | 32.071 |

Generation dominates at ~97% of wall time. Contract enforcement is ~3 ms — about **0.02%** of a
request. The retrieval maximum of 7.8 s is first-call model loading, not steady state.

## Citation Coverage Debt

Measured coverage is approximately **0.88** against a 0.90 reference. It is recorded per request in
the audit log (`citation_coverage`, `material_claim_count`, `claims_with_citation`,
`citation_coverage_status`) and **not enforced**.

This orchestration does **not** improve coverage and no such claim is made. The uncovered claims are
opening summary sentences and continuation bullets that restate already-cited content — a citation
*placement* weakness rather than ungrounded content, which is why the integrated evaluation found
zero unsupported material claims alongside it. It remains open quality debt.

## Known Limitations

- **Coverage ≈ 0.88**, telemetry only, unchanged by this layer.
- **The raw generator still misbehaves**: malformed citations, wrong abstention marker language,
  wrong answer-body language. The contract catches these; the orchestrator rejects and never
  repairs.
- **~1 request in 24 is rejected outright** on benchmark evidence and returns no answer.
- **Rejections are deterministic** for a given request, so a rejected query stays rejected until
  the generator improves. There is no retry that can rescue it.
- **Contract v1.1 language detection** does not mask sentence-initial proper nouns and uses
  capitalisation as its only entity signal.
- **Generation is near- but not byte-deterministic** at temperature 0 (71/72 reproduced across runs).
- **The smoke suite validates wiring, not quality**, and its two failure cases are fixtures.
- **Single-process, synchronous.** No concurrency control, rate limiting, request queue or
  authentication is implemented; the retriever holds a lazily-loaded model in memory.

## Frozen Integrity

Unchanged and asserted: Retriever v1, Context v1, Prompt v5 (`9bae1362…4085`), Output Contract v1,
Output Contract v1.1 (`5ebf8fe9…def5`), citation-validator-v1.2, Benchmark v1 and v2, both packet
artifacts, embeddings, chunks and corpus. No prompt v6. `generation_candidate_v1.json` untouched —
the raw generator was not upgraded.

Qdrant: **5992 before, 5992 after, 0 writes**, green.

Full suite: **1114 tests pass** (40 skipped, including 4 live-model integration tests gated behind
`TUNNELBOOK_LIVE_MODEL=1`).

## Final Decision

**PRODUCTION GROUNDED GENERATOR V1 — CLOSED / GO**, status **frozen**.

Every gate holds: the canonical entrypoint, healthcheck and dry-run all work; Retriever v1,
Context v1, Prompt v5 and Output Contract v1.1 are used unchanged and verified by SHA at startup;
contract failures were never released; accepted answers retain their evidence handles; audit
logging is complete and rejected raw text is written nowhere; same-config retry is disabled; no
repair path exists; Qdrant is untouched; smoke and unit tests pass.

What this authorises is a production runtime that is honest about its own limits — it answers when
it can prove the answer meets the contract, and returns a plain refusal when it cannot, roughly one
time in twenty-four. That refusal rate is the cost of the guarantee and the next thing worth
improving, by fixing the generator rather than loosening the contract.

The next stage is **book-writing pipeline architecture + evidence note contract**. No chapter,
outline, section draft or book prose has been produced in this phase.
