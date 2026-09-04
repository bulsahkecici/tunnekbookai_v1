# TunnelBookAI Generation Runtime Harness v1

## Decision

**GENERATION PHASE A1 RUN 1 — CLOSED / GO**

Runtime foundation only. No benchmark authored, no reserve pilot, no grading.

## Frozen System Prompt

- `data/metadata/generation_system_prompt_v1.txt` · SHA256 `303691ec02501fa4637a2618ceb90f21bba4c558e41124325ed8915ef7a64817`
- Verified on every harness start; a mismatch raises `HarnessConfigError` and **fails closed** rather than evaluating under a modified prompt.
- Carries all thirteen contract rules, the untrusted-evidence boundary, the technical-imperative carve-out, and canonical markers **`YETERSİZ KANIT`** (dotted İ) / `INSUFFICIENT EVIDENCE`.

## Renderer

- Actual local `chat_template.jinja`, SHA256 `e84f32a23fdda27689f868aa4a1a5621f41133e51a48d7f3efcbea2839574259` — loaded from disk, never embedded in Python
- Jinja2 3.1.6 in-process; helper audit found `raise_exception`, `namespace`, `tojson` referenced and **all supported**; an unsupported helper raises `TemplateUnsupported`
- `enable_thinking=false` → pre-closed `<think>\n\n</think>`; `true` → open `<think>`; the two differ
- Canonical system+user structure: 3 `<|im_start|>`, 2 `<|im_end|>`, 1 `<think>`, 1 `</think>`, exactly one assistant prefix. Counts are asserted for that frozen structure only, not universally.

## Tokenizer

- `tokenizer.json` SHA256 `87a7830d63fcf43bf241c3c5242e96e62dd3fdc29224ca26fed8ea333db72de4` from the same artefact
- Authoritative count is `tokenizer(exact_rendered_prompt, add_special_tokens=False)` — never a re-tokenisation of the raw messages

## Generation Endpoint

- **`/v1/completions` only.** `GenerationConfig` raises on `/v1/chat/completions`, on a full URL containing it, and on any other endpoint.
- Rationale is measured, not stylistic: the chat endpoint silently ignores `chat_template_kwargs`, so `enable_thinking` never reaches the template (387 reasoning tokens either way).
- Stop policy frozen: `['<|im_end|>', '<|im_start|>']`

## Citation Validator

- Version `citation-validator-v1.1` — deterministic, no LLM

### Known validator bug fixed

The previous single-alternation `MALFORMED` regex flagged **valid** `[E001]` as malformed, for both reasons identified in review: the bare-handle branch matched `E001` inside its own brackets, and `\[\s*E\s*\d+\s*\]` matches a canonical handle because every `\s*` can match zero characters.

Replaced with **valid-first parsing**: canonical `\[E\d{3}\]` handles are extracted and their spans recorded first; bracketed candidates are then checked with `fullmatch` against the canonical form; bare handles are only reported when they fall outside an already-matched valid span.

Verified: `[E001]` and `[E001][E004]` are valid with **zero** malformed; `[E001][E001]` is valid with occurrence count 2; `[E009]` is *unknown but syntactically valid*, explicitly not malformed; and `[E1] [E01] [E0001] [ E001] [E001 ] [e001] [E 001]`, bare `E001` and unclosed `[E001` are all malformed.

### Leak detection

Flags `page 15`, `s. 15`, `ss. 15-17`, `ss. 15–17`, `Slayt 12`, `slide 12`, `DOC000123`, `tunnel_report.pdf`, `/Users/x/corpus/a.pdf`, and template tokens.

Does **not** flag `15 cm`, `25 MPa`, `RMR 60`, `GSI 45`, `2 m`, `EN 1997`, `ASTM D1586`, `2024`, `351.08.07`, `C30/37`, `10–20 mm`.

A second false positive was found and fixed while testing: `C30/37` matched the path regex via `/37`. Paths now require a real document extension or an absolute path of at least two segments preceded by whitespace. Detected leaks are normalised for trailing prose punctuation; `raw_answer` is never modified.

## Abstention Contract

Markers must open the response after leading whitespace only. A marker appearing mid-prose returns `abstention_at_start=false` with `abstention_marker_present_anywhere=true`, so a response cannot abstain and then continue asserting uncited facts unnoticed.

## Result Schema

- 30 fields including local/API prompt tokens and their delta, all validator outputs, latency and finish reason
- **No reasoning is persisted.** Tests assert no field name matches `reasoning`, `chain_of_thought`, `cot` or `hidden`.

## Checkpoint Identity

Identity spans all eight required fields (query_id, benchmark, system prompt, model, tokenizer, template, generation config, context packet). Changing **any one** produces a different identity, verified field by field.

## Resume Safety

`is_resumable` rejects a stored result whose system prompt, template, context packet or generation config has drifted. Results append durably per query with `fsync`, and a torn final line from an interrupted run is skipped rather than crashing recovery.

## Offline Tests

- `tests/test_generation_model_eval.py`: **52/52 PASS** (1 live test skipped offline, passing with `TUNNELBOOK_GEN_LIVE=1`)
- Live smoke confirms raw-completions generation, no template leakage, no unknown handles, and `local tokenizer == API prompt_tokens`.

## Frozen Integrity

`19_retriever_v1.py`, `20_rag_context.py`, both contracts and `chunks.jsonl` byte-identical; Qdrant untouched (read-only, 5992).

## Remaining Work

1. **Run 2** — reserve pilot (5 real queries × 512/768/1024/1536/2048), prompt-accounting study across real prompts, template-overhead invariance decision, operational budget derivation
2. **Run 3** — author and freeze the 72-item benchmark with ContextPackets and literal supporting spans
3. **Phase B** — execution, claim audit, metrics

`--pilot`, `--run-query`, `--run-range`, `--resume`, `--grade` and `--report` deliberately exit with `benchmark_not_built` rather than pretending to work.

## Validator v1.2 Semantic Closure

Run 1's validator collected every canonical `[E###]` handle into `valid_handles` and computed `unknown_handles` separately, so `[E009]` against a packet of E001–E002 appeared in **both**. That is ambiguous for any downstream metric: a hallucinated reference would have counted as a valid citation.

### Two orthogonal axes

| axis | question | fields |
|---|---|---|
| **syntax** | is it written as canonical `[E###]`? | `syntactically_valid_handles`, `syntactically_valid_handle_occurrences`, `malformed_citations` |
| **reference** | does it exist in the rendered packet? | `valid_handles`, `excluded_handle_citations`, `unknown_handles` |

`[E009]` is correct syntax with an invalid reference — **unknown, never malformed**. `[E01]` is a syntax error. The two failures are reported separately because they mean different things about the model.

### Classification precedence

1. in `packet_evidence_ids` → `valid_handles`
2. else in `excluded_evidence_ids` → `excluded_handle_citations`
3. else → `unknown_handles`

Every canonical handle lands in **exactly one** bucket. A test asserts the three sets are pairwise disjoint *and* that their union equals `syntactically_valid_handles`, across five answer shapes. Passing an id as both present and excluded raises `ValueError` rather than silently resolving.

Worked example — packet `{E001, E002}`, excluded `{E003}`, answer `Claim [E001][E003][E999].`:

```
syntactically_valid_handles : ['E001', 'E003', 'E999']
valid_handles              : ['E001']
excluded_handle_citations  : ['E003']
unknown_handles            : ['E999']
malformed_citations        : []
```

### Excluded evidence is not representable under Context v1

I inspected the real schema before designing this rather than assuming it. `ContextPacket.excluded_items` records `{chunk_id, rank, reason}` and carries **no `evidence_id`** — Evidence IDs are assigned only to selected items, by position, via `f"E{len(selected) + 1:03d}"`. An excluded chunk therefore never receives an E-handle and never appears in `context_text`.

Consequence: under Context v1 an excluded-evidence citation **cannot be distinguished** from a hallucinated one. A model citing an unrendered handle is indistinguishable from one inventing `[E999]`, and both correctly land in `unknown_handles`. No IDs were fabricated to close that gap.

`excluded_evidence_ids` is implemented and tested as a **forward-compatible hook** for a future context version that assigns stable IDs before selection. Callers passing real Context v1 packets should leave it empty, and `excluded_handle_citations` will always be empty for them. Three tests pin this fact against the actual `20_rag_context.py` source and against real smoke packets.

### Schema change

Added `syntactically_valid_handles`, `syntactically_valid_handle_occurrences`, `excluded_handle_citations`. The ambiguous `valid_handle_occurrences` was **removed** rather than redefined — a test asserts it is absent from `RESULT_FIELDS`, since a name that could mean either axis is worse than no name.

### Regression

- `test_generation_model_eval.py`: **66/66 PASS** offline and live (was 52)
- `tests/`: **669/669 PASS** · `rapor/tests/`: **16/16 PASS** → **685/685 PASS**
- Leak detection, abstention contract, renderer, endpoint guard, checkpoint identity: unchanged and still passing
- System prompt, generation endpoint and template renderer untouched; validator version bumped `v1.1` → `v1.2`

## Run 2 Reserve Pilot

25 generations: 5 real queries × max_tokens 512/768/1024/1536/2048. Only `max_tokens` varied; model, prompt, ContextPacket, temperature (0), seed (11), template, thinking mode and stop strings were held constant.

## Pilot Queries

| id | type | lang | evidence | docs | context tokens |
|---|---|---|---|---|---|
| P01 | Turkish factual | tr | 10 | 5 | 18,775 |
| P02 | English factual | en | 10 | 3 | 11,389 |
| P03 | multi-source | en | 10 | 6 | 10,720 |
| P04 | numeric/technical | tr | 10 | 3 | 14,117 |
| P05 | must-abstain | tr | 10 | 7 | 20,266 |

Suitability was verified **before** generating: P01–P04 packets each carry 10 substantive evidence items across multiple documents, P04 contains real numeric spans (15 cm, 60–100 mm, 350 kg/m³), and P05's packet contains no `bütçe` evidence at all, so the requested 2031 maintenance figure is genuinely unsupported. No pilot query had to be rejected as retrieval-limited.

## True Non-Thinking Regression

All 25 generations: visible answer non-empty, **zero** template leaks, no `<think>`/`</think>`/`<|im_start|>`/`<|im_end|>` in any answer, no reasoning persisted. The non-thinking contract held throughout.

## Reserve Sweep

| max_tokens | truncated | hard failures | unknown handles | leaks | verdict |
|---|---|---|---|---|---|
| 512 | P01, P02, P03 | – | 0 | 0 | FAIL |
| 768 | P01, P03 | – | 0 | 0 | FAIL |
| **1024** | – | – | 0 | 0 | **PASS** |
| 1536 | – | – | 0 | 0 | PASS |
| 2048 | – | – | 0 | 0 | PASS |

Answers are stable once they fit: P01 settles at 830 tokens, P02 at 573, P03 at 780, P04/P05 at 158 — identical from the first sufficient level upward, so the sweep is measuring truncation, not sampling variation.

## Prompt Accounting

| query | system | context | question | user msg | rendered local | API | delta |
|---|---|---|---|---|---|---|---|
| P01 | 348 | 18775 | 10 | 18793 | 19157 | 19157 | 0 |
| P02 | 348 | 11389 | 9 | 11406 | 11770 | 11770 | 0 |
| P03 | 348 | 10720 | 7 | 10734 | 11098 | 11098 | 0 |
| P04 | 348 | 14117 | 14 | 14139 | 14503 | 14503 | 0 |
| P05 | 348 | 20266 | 22 | 20296 | 20660 | 20660 | 0 |

**Local tokenizer equals API `prompt_tokens` exactly on all 25 rows — max |delta| = 0.** Component counts are reported as descriptive only: BPE is not additive, so full rendered-prompt tokenization remains the hard source of truth.

## Template / Boundary Overhead

- min **16**, median **16**, max **16** tokens across all five prompts
- Policy: **empirically_fixed_for_canonical_structure** — identical for every prompt, so it is fixed *for the canonical system+user structure only*, not for arbitrary message shapes.
- The earlier figure of 17 from the toy probe was an artifact of a 14-token system message; the real value under the frozen prompt is 16.

## Safe Output Reserve

- `measured_minimum_working_reserve` = **1024** (first level with zero truncation)
- max observed answer = **830** tokens
- `selected_safe_output_reserve` = **1536** (~1.9× the longest observed answer)
- Provisional for the grounded-answer benchmark. **Not** a chapter-writing reserve, and it may move once the 72-query distribution exists.

## Prompt Budget Guard

`validate_prompt_budget()` raises `PromptBudgetExceeded` **before** any API call when `rendered_prompt + reserve + margin > loaded_context`. LM Studio is never the component that discovers overflow. Exact fit passes; one token over raises; non-positive reserves and negative margins are rejected.

## Operational Context Budget

```
model_context_length_loaded        71936

- selected_safe_output_reserve     1536
- safety_margin                    3596
= maximum_prompt_tokens_operational 66804

- system_prompt_tokens             348
- template_overhead                16
- provisional query allowance      22+100
= rag_context_budget_planning_value 66318
```

The planning value is for benchmark authoring only. **Full rendered-prompt validation remains authoritative** — the planning figure is never a hard model limit.

## Provisional RAG Context Planning Value

**66318** tokens. Pilot query tokens: min 7, median 10, max 22 — far too few queries to freeze an allowance, so `query_allowance_status = pending_72_query_benchmark`.

## Latency

| max_tokens | median | max |
|---|---|---|
| 512 | 8.45 s | 26.66 s |
| 768 | 5.66 s | 7.71 s |
| 1024 | 5.65 s | 8.33 s |
| 1536 | 5.64 s | 8.35 s |
| 2048 | 5.65 s | 8.48 s |

Latency is dominated by prefill, not by the reserve: raising `max_tokens` from 768 to 2048 changes the median by hundredths of a second because generation stops at the same natural point. The 26.7 s outlier is the first call (cold cache). No tokens/sec claim is made — the API does not expose decode timing separately.

## Limitations

- **Bare-handle contract violations.** In P05's abstention the model refers to evidence as `E001'de`, `E002'de`, `E008/E009'daki` — Turkish locative suffixes on bare handles rather than canonical `[E001]`. The validator correctly flags 4 such citations, and the count is **identical at every reserve level**, confirming it is a prompt-adherence issue that no sizing change fixes. This is a Phase B finding and may warrant a system-prompt v2 — the v1 prompt is frozen and was not edited.
- **P04 abstained on an answerable query.** Its answer opens with `YETERSİZ KANIT` yet correctly reports the thickness specs it does have, with citations. My query was compound ("kalınlığı ve dozajı") and the packet supports only half of it, so this reads as defensible caution rather than failure. It did expose a classifier gap: abstention on an answerable query was scoring `complete`. Added `unexpected_abstention` so it can never be silently counted as success.
- Five queries size the runtime; they do **not** measure model quality.

## Run 2 Decision

**GENERATION PHASE A1 RUN 2 — CLOSED / GO**

## Final Decision

**GENERATION PHASE A1 RUN 1 — CLOSED / GO**

---

# Run 3 — System Prompt v3 + Full-Contract Pilot Closure

## Why v3 exists

Two prior prompts each fixed the previous failure and introduced a new one:

| Version | SHA256 (first 16) | Tokens | Citation outcome |
|---|---|---|---|
| v1 | `303691ec02501fa4` | 348 | 4 malformed — bare handles with Turkish suffixes (`E001'de`) |
| v2 | `0063b9bcbe2d9332` | 569 | 2 malformed — compressed range form `(E003-E010)` |
| v3 | `d3cadd465e2733d0` | 514 | **0 malformed at every reserve level** |

v2 failed because it taught the model a *list of forbidden examples*, and the model complied with the list while inventing a form the list did not name. v3 does not extend that list. It replaces the enumerated block with a **general grammar** — "the only legal evidence identifier is `[Eddd]`, a capital E and exactly three digits, fully enclosed in square brackets" — plus a closed statement that any E-number not wholly inside its own brackets is forbidden *as a class*, naming bare/suffixed/ranged/slashed/comma-joined only as instances of that class.

v3 also adds the behavioural rule that produced both v1's and v2's violations in the first place: **do not list, enumerate or dismiss unused evidence by its E-number.** Both failures occurred in the same sentence shape — an inventory of evidence the model had decided *not* to use. Removing the reason to write that sentence removes the pressure to compress its handles.

v3 is 514 tokens, below v2's 569. v1 and v2 were not modified.

## Versioned prompt loading (harness change)

`SYSTEM_PROMPT_PATH` / `SYSTEM_PROMPT_SHA256` as single-version constants could not express three frozen prompts, so the harness gained a registry:

- `SYSTEM_PROMPTS` — `{version: {path, sha256, name}}` for v1, v2, v3.
- `load_system_prompt_versioned(version)` — **fails closed** on an unknown version, a missing file, or a SHA mismatch. There is no fallback to another version; a tampered prompt aborts the run rather than silently evaluating under different instructions.
- `GenerationConfig` now carries `system_prompt_version` alongside `system_prompt_sha256`, so the config hash — and therefore the checkpoint identity — differs between v2 and v3. A v2 checkpoint can no longer be resumed by a v3 run.

The clean pilot obtained its prompt through `load_system_prompt_versioned()`, not by reading the file directly, so the artifact's `system_prompt_sha` is the harness's verified value.

## Validator: unchanged and not weakened

`citation-validator-v1.2` semantics were not touched. Confirmed against every compressed form:

| Output | Verdict |
|---|---|
| `[E001]`, `[E003][E010]`, `[E001]'de` | valid |
| `E001`, `E001'de` | malformed |
| `E003-E010`, `E003–E010` | malformed (both handles) |
| `[E003-E010]`, `[E003/E010]` | malformed |
| `E003, E004`, `E003 ve E004` | malformed |

Malformed citations remain inside the gate; the full-contract reserve is not computed by ignoring them.

## Clean pilot v3 — 5 queries × 5 reserve levels = 25 generations

Prompt accounting is exact: **max |prompt_tokens_api − prompt_tokens_local| = 0** across all 25. Template + boundary overhead is 16 tokens.

| Reserve | Truncated | Malformed | Unknown handles | P05 clean abstention | P04 numeric+unit exact | Max completion |
|---|---|---|---|---|---|---|
| 512 | P01, P03 | 0 | 0 | yes | yes | 511 |
| 768 | P01 | 0 | 0 | yes | yes | 767 |
| 1024 | P01 | 0 | 0 | yes | yes | 1023 |
| 1536 | P01 | 0 | 0 | yes | yes | 1535 |
| 2048 | — | 0 | 0 | yes | yes | 1969 |

- `measured_minimum_nontruncating_reserve_v3` = **2048**
- `measured_minimum_full_contract_reserve_v3` = **2048** (no longer null)

Both P04 and P05 met their required behaviour at *every* level, so the two minima coincide: under v3 the only remaining constraint is length, not contract adherence.

**P05** (`must_abstain`) opens with `YETERSİZ KANIT`, states what is missing, and emits **no** bare, ranged or inventoried handles — the v2 failure sentence is gone.

**P04** (`numeric_technical`) does not abstain and reports both gold values with exact units at all five levels: maximum layer thickness **15 cm** and minimum cement dosage **350 kg/m³**, each with bracketed handles.

## Operational budget

`measured_minimum_full_contract_reserve = 2048` sits at the ceiling of the swept range, so it is a demonstrated **floor**, not a demonstrated plateau. The operational reserve is set one step above it:

- `selected_safe_generation_reserve` = **3072** (1.56× the longest observed complete answer, 1969 tokens)
- `loaded_context_length` = 71936, `safety_margin` = 3596 (both unchanged)
- `maximum_prompt_tokens_operational` = 71936 − 3596 − 3072 = **65268**
- `rag_context_budget_planning_value` = 65268 − 514 (system) − 16 (overhead) − 128 (question reserve) = **64610**

Observed questions were 7–22 tokens; the 128-token question reserve is deliberate slack for the 72-item benchmark, which is not yet authored.

## Limitations

- Five queries size the runtime and verify format adherence. They do **not** measure answer quality, and 0 malformed over 25 generations is not a guarantee — it is the absence of the two failure modes that were reproducible at every reserve level under v1 and v2.
- `question_reserve_tokens` is a planning allowance, not a measurement; the 72-item benchmark may revise it.
- The reserve sweep ceiling is 2048, so reserves above 3072 are unmeasured.

## Run 3 Decision

**GENERATION SYSTEM PROMPT V3 + FULL-CONTRACT PILOT CLOSURE — GO**
