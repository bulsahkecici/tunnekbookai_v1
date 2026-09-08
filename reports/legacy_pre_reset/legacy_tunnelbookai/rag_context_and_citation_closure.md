# TunnelBookAI RAG Context V1 Budget + Boundary Closure

## Decision

**RAG CONTEXT + CITATION CONTRACT — CLOSED / GO**

Two P1 audit defects fixed. Citation semantics, Retriever v1 and Qdrant untouched.

## Token Budget Bug

`context_max_tokens` bounded only the concatenated chunk text. The rendered `context_text` also carries the injection notice, per-evidence headers (document, chunk, citation, mode, provenance, quality, title, heading, section, authority, language, warnings) and both delimiters — none of which were counted.

Demonstrated before the fix:

| | |
|---|---|
| declared `token_count` | 150 |
| declared budget | 200 |
| **actual rendered tokens** | **324** |
| overshoot | **+124 (62%)** |

Harmless with a whitespace counter; unsafe the moment a real generation tokenizer is installed, which is exactly what this layer exists to feed.

## Corrected Budget Semantics

- `context_max_tokens` now bounds the **full rendered `context_text`**.
- Each candidate is accepted only if `token_counter(render_context(selected + [candidate])) <= context_max_tokens`. The tentative context is genuinely re-rendered rather than estimated additively, because a real BPE tokenizer can differ at block boundaries. N ≤ 20, so the cost is trivial.
- Invariant now enforced by test: `token_count == token_counter(context_text)` exactly.
- `evidence_text_token_count` is reported separately so the text-only figure is still visible.
- It excludes future system prompt, user instruction and answer tokens — those reserves belong to the generation stage.

## Context Overhead

Measured with the provisional counter: empty context **54** tokens; each rendered block adds about **42** tokens of metadata and delimiters on top of its text.

If `context_max_tokens` is below the mandatory overhead the packet returns `insufficient_evidence` with reason `context_budget_below_mandatory_overhead` rather than silently exceeding the declared budget.

Across the 18 smoke queries: **0** packets exceed budget; median rendered context **5548** tokens (first query: 4862 evidence-text tokens → 5373 rendered).

## Boundary Collision Threat

Evidence text is preserved byte-for-byte by design, so a source document could contain a literal `<END_UNTRUSTED_EVIDENCE E001>`. Confirmed before the fix: the marker appeared **twice** in the rendered context, making the structure ambiguous — a document could appear to close its own evidence block and have following text read as trusted.

## Deterministic Boundary Design

- `boundary_id = SHA256(context_contract_version + chunk_id + text_sha256)[:12]`
- Markers: `<BEGIN_UNTRUSTED_EVIDENCE E001 b=7af92c8163e4>` / `<END_… b=…>`
- Both complete markers are checked against the exact evidence text; on collision the prefix extends deterministically **12 → 20 → 32 → 64**.
- If no collision-free marker exists, `BoundaryCollision` is raised. The source is never rewritten.
- No randomness: same evidence ⇒ same boundary, verified by test.
- `boundary_id` is structural only. The model still cites `[E001]` and never reproduces it.

## Adversarial Boundary Test

Evidence text containing both `<BEGIN_UNTRUSTED_EVIDENCE E001>` and `<END_UNTRUSTED_EVIDENCE E001>` plus an injected instruction:

- source text **byte-identical** to the retriever's output
- injected marker still present **verbatim** in the context
- derived markers occur exactly **once** each — structure unambiguous
- boundary id identical on repeat

## Exact Text Preservation

No escaping of `<`, `>`, `[`, `]`, Markdown, HTML-like text or imperative language. A specification reading "apply bolts at 2 m spacing" survives intact. Security is boundary identity, not source modification.

## Citation Contract Regression

Unchanged and re-verified: `citation_mode != provenance_status`; `provenance_status == source_only` emits no page/slide; `citation_mode == source_only` cites the source with page metadata supplemental; degraded citations keep a real section fallback and fabricate nothing.

| citation_mode | count |
|---|---|
| pdf_page | 4228 |
| document_section | 868 |
| slide | 798 |
| source_only | 71 |
| table_or_sheet | 24 |
| image | 3 |

Smoke citation quality unchanged: exact 130 · section 10 · source 30 · degraded 8.

## Retriever Integrity

`scripts/19_retriever_v1.py` byte-identical (`8ada31f6…`); release, manifest and citation inventory unchanged.

## Qdrant Integrity

`tunnelbook_dense_v1`: **5992 → 5992**, zero writes.

## Tests

- `tests/` **592/592 PASS** · `rapor/tests/` **16/16 PASS** → **608/608 PASS**
- Also passes with `TUNNELBOOK_QDRANT_LIVE=1 TUNNELBOOK_BGE_LIVE=1`
- 17 new closure tests: rendered-token invariant, budget never exceeded across five budgets, mandatory overhead counted, non-zero empty-context cost, the two-texts-fit-but-two-blocks-do-not regression (fails against the old implementation), atomic table under rendered accounting, pluggable counter governing the full context, deterministic boundary id, derived-not-random check, adversarial marker collision, deterministic prefix extension, no source escaping, `[E001]` handle unchanged, injection notice preserved, citation inventory and retriever SHA guards.

## Warnings

- The token counter remains **provisional** (`whitespace-word-v1`). The point of this closure is that any tokenizer plugged into `token_counter` now automatically governs the full rendered context — but the production budget still must be set with the generation model's own tokenizer.
- Rendered contexts are materially larger than evidence text alone (≈42 tokens per block plus 54 fixed). Budget planning in the generation stage should use rendered figures, not chunk-text sums.
- Four of my own test expectations were wrong and were corrected against measured overhead rather than loosening the implementation; one fixture had been silently measuring deduplication instead of the budget.

## Minimum Budget Contract Closure

A third audit defect: the previous fix *flagged* an impossible budget but still returned a packet whose `context_text` exceeded it.

### Old counterexample

| | |
|---|---|
| requested budget | 5 |
| mandatory rendered overhead | 54 |
| returned `token_count` | **54** |
| returned `token_budget` | 5 |
| `insufficient_evidence` | true |

The flag was correct but insufficient: downstream code that ignores `insufficient_evidence` would have sent a 54-token context under a 5-token budget straight to the generation model.

### New behaviour

- `ContextBudgetTooSmall(ValueError)` is raised, carrying `requested_budget`, `mandatory_overhead` and `token_counter_version`.
- Message: `context_max_tokens=5 is below mandatory rendered context overhead=54 (token counter: …)`
- `context_max_tokens` must be a positive integer; `0`, negatives and non-integers raise `ValueError`.
- The overhead is measured with the **caller's own** `token_counter`, so a future generation tokenizer governs the minimum exactly as it governs evidence blocks (verified: a doubling counter raises at overhead 108 instead of 54).

### Invariant now guaranteed

For every successfully returned `ContextPacket`:

```
token_count == token_counter(context_text)
token_count <= token_budget
```

Asserted across all 18 smoke packets and over a swept range of budgets in tests.

### Configuration failure vs evidence state

| condition | outcome |
|---|---|
| budget below mandatory overhead | **raises** `ContextBudgetTooSmall` (configuration failure) |
| budget exactly equals overhead, zero evidence | valid packet, `token_count == token_budget` |
| zero retrieved evidence, sufficient budget | normal packet, `insufficient_evidence=true`, reason `no_evidence_selected` |

These are deliberately not conflated: one is a caller misconfiguration, the other is a legitimate retrieval outcome.

### Incidental fix

The exception message exposed a latent bug of mine: `TOKEN_COUNTER_VERSION` was built from two adjacent string literals on separate lines without parentheses, so the second half was silently discarded and the recorded version read `"whitespace-word-v1 (provisional; replace with the generation model's own "`. Fixed and covered by a test asserting the string is complete.

### Unchanged

Collision-safe SHA boundaries and their 12→20→32→64 extension, byte-identical source text, `[E001]` handles, `citation_mode` / `provenance_status` distinction, source_only semantics, degraded fallbacks, exact duplicate removal, atomic tables — all untouched and re-verified.

### Verification

- `tests/` **603/603 PASS** · `rapor/tests/` **16/16 PASS** → **619/619 PASS**
- Also passes with `TUNNELBOOK_QDRANT_LIVE=1 TUNNELBOOK_BGE_LIVE=1`
- 12 new tests: below-overhead raises with diagnostics, exact-overhead budget valid, zero-evidence distinct from budget failure, zero/negative/non-integer budgets rejected, custom counter governs the minimum, invariant across eight budgets, no packet exceeds budget across a swept range, token-counter version complete
- One earlier test asserting the superseded behaviour was updated to expect the raise
- `scripts/19_retriever_v1.py` byte-identical `8ada31f6…`; Qdrant **5992 → 5992**, zero writes

## Final Decision

**RAG CONTEXT + CITATION CONTRACT — CLOSED / GO**

Next stage: GENERATION MODEL SELECTION + GROUNDED ANSWER / CITATION VALIDATION.
