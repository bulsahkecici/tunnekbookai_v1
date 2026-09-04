# Generation Output Contract v1

## Decision

**GENERATION OUTPUT CONTRACT V1 — CLOSED / GO**

`tunnelbook-generation-output-contract-v1`, implementation SHA
`670031d116056485155fc9d5c3d12b472d91f6b1e7a34ed9b169166f3727ce7d`, repair policy
`none_fail_closed`. All three known Phase B v2 defects are caught with exactly the expected reasons;
all 14 clean controls pass; zero false positives. System prompt v5 and both benchmarks are unchanged
and no model was called in this task.

This does **not** make generator v5 acceptable. It builds the enforcement layer that must exist
before re-evaluation, and a test asserts the candidate descriptor is not marked acceptable.

## Why Prompt v6 Was Rejected

Five prompt generations have attacked this defect class and it migrated every time:

| Version | Fixed | Broke / remained |
|---|---|---|
| v1 → v2 | bare suffixed handles (`E001'de`) | compressed ranges (`E003-E010`) |
| v2 → v3 | ranges | bare references in prose |
| v3 → v4 | prose references | migrated item-to-item across three drafts before closing |
| v4 → v5 | English marker direction (6/6) | Turkish direction (2/4 on holdout) |
| v5 (holdout) | — | `(E002)` inside a **heading** — a new sub-shape |

Each fix was correct and each time the model found a surface the prompt had not named. Marker
selection in particular is a two-token decision fully determined by the query *before* generation
starts, so asking for it in prose is the wrong mechanism. The contract enforces at the boundary
where the property is actually decidable.

## Contract Scope

Deterministic, testable, fail-closed, auditable, reproducible. It takes the answer text, the query
language (when known), and the packet's exposed evidence IDs. It performs **no** web access, no
corpus lookup, no retrieval, and involves no second model. It never invents technical content and
never repairs a factual claim.

Note on path: the task specified `scripts/25_generation_output_contract.py`, but slot 25 was already
occupied by `25_generation_phase_b_v2.py`. The contract lives at
`scripts/26_generation_output_contract.py` and the path is pinned in the metadata file.

## Marker Enforcement

Expected marker is derived **only** from the query language — Turkish → `YETERSİZ KANIT`,
English → `INSUFFICIENT EVIDENCE`. Evidence language is never consulted. When the answer abstains,
the expected marker must be the first thing in it; a marker buried mid-answer raises
`abstention_marker_not_at_start`.

## Body Language Guard

Deterministic tr/en identification over the body **after** the marker. Before scoring it strips
citation handles, numbers, units, acronyms and standard codes, URLs and symbols, so the verdict
rests on prose alone. Turkish-specific glyphs (`ğ ı ş`) are weighted as strong evidence; `ü ö ç`
are deliberately excluded because they appear in other languages. Turkish and English function
words carry the rest, and the winner must beat the other by a 1.5× margin.

Tested explicitly against the hard cases: Turkish prose carrying English technical terms
("shotcrete", "rock bolt", "lattice girder") stays Turkish, and English prose full of Turkish place
names ("Bolu", "Zigana", "Ovit", "Marmaray") stays English. Below 8 body tokens the verdict is
`insufficient_text`; when neither language wins by the margin it is `ambiguous`. Neither is guessed.

This guard is why the marker must not be rewritten — see below.

## Citation Syntax Enforcement

`citation-validator-v1.2` is reused **unmodified**; the contract adds no citation semantics of its
own. Syntax passes only when `malformed_citations == []` **and** `unknown_handles == []`. The full
matrix is pinned by test:

| Form | Verdict |
|---|---|
| `[E001]`, `[E001]'de`, `[E001][E004]` | valid |
| `(E001)`, `Evidence E001`, `E001`, `E001'de` | malformed |
| `E001-E004`, `[E001-E004]`, `[E01]` | malformed |
| `[E999]` when not exposed | unknown |

## No-Repair Policy

`repair_policy: none_fail_closed`. The contract cannot return altered text — the result object has
no field capable of carrying a rewritten answer, and `raw_answer_sha` is the hash of the untouched
input. Tests assert that malformed handles are reported in their original bare form and that a wrong
marker is reported rather than replaced.

The reason is concrete rather than theoretical. **GEV062 would have been laundered by a repair
layer**: swapping its opening `INSUFFICIENT EVIDENCE` for `YETERSİZ KANIT` would have produced a
superficially compliant answer whose entire body is still English. A repair that hides a deeper
defect is worse than a rejection. The same logic applies to citations — an E-number may not be
intended as a citation at all, a malformed range may stand for several IDs, and an unknown handle
must never be silently bound to a real one.

## Citation Coverage Telemetry

Coverage is computed (`material_claim_count`, `claims_with_citation`, `citation_coverage`) and
carried as `citation_coverage_status: telemetry_only_not_enforced`. It **never** rejects a response
and no handle is ever attached to an uncited claim. Phase B v2 measured 0.8953 and explicitly flagged
segmentation sensitivity — enforcing a threshold whose denominator moves with the segmentation rule
would manufacture failures. A test asserts a 0.5-coverage answer still passes the contract.

## Development Cases

`data/evaluation/output_contract_dev_v1.jsonl` — **17 cases**, all labelled
`dataset_role: development_validation`, all drawn from existing Phase B v2 outputs. No new generation
was performed, and no additional holdout responses were inspected to shape the rules.

## Known Failures Caught

| Case | Expected | Contract verdict | Reasons produced |
|---|---|---|---|
| GEV042 | invalid | **invalid** | `malformed_citation` |
| GEV061 | invalid | **invalid** | `wrong_abstention_marker_language` |
| GEV062 | invalid | **invalid** | `wrong_abstention_marker_language`, `answer_body_language_mismatch` |

GEV062 produced the required **dual** failure: the contract identified the wrong marker *and*
independently determined the body is English against a Turkish query.

## Clean Controls

**14/14 pass**: 5 Turkish answers, 5 English answers, 2 correct Turkish abstentions, 2 correct
English abstentions.

## False Positive Analysis

**0 false positives and 0 false negatives** across the 17 development cases. The controls were chosen
to stress exactly what a naive guard gets wrong: Turkish answers dense with English technical
vocabulary, English answers dense with Turkish proper nouns, numeric-heavy answers, and short
abstentions whose body is too small to judge. None was rejected.

The contract has deliberately **not** been swept across all 72 Phase B v2 answers. Doing so to adjust
rules would contaminate the holdout; measuring the contract's aggregate false-positive rate on that
set belongs to the next task, the contract-integrated re-evaluation.

## Frozen Integrity

System prompt v5 `9bae1362…` unchanged. Benchmark v1 `de3c1684…`, benchmark v2 `1e6347b5…` and its
packets `05387051…` unchanged. `citation_contract_v1.json` unchanged and validator semantics
untouched. Qdrant `tunnelbook_dense_v1`: **5992 → 5992, 0 writes**, green. Generation calls in this
task: **0**.

Tests: **941 in `tests/` + 16 in `rapor/tests/` = 957, all passing** (37 skipped, live-gated),
including 40 new contract tests.

## Known Limitations

- **Language identification is lexical, not statistical.** It is tuned for tr/en technical prose and
  will not generalise to a third language; `SUPPORTED_LANGUAGES` is enforced and an unsupported
  language raises rather than degrades.
- **`insufficient_text` bodies are not judged.** A bare marker with fewer than 8 body tokens passes
  the body guard by construction; the marker check still applies.
- **`ambiguous` fails closed**, which means a genuinely mixed-language answer is rejected without a
  verdict on which language was intended. That is intentional for v1 but will produce rejections that
  need human reading.
- **Coverage telemetry inherits the segmentation sensitivity** already documented in Phase B v2; the
  numbers it reports are not comparable across different segmentation rules.
- **The contract cannot detect a wrong-language *question*.** It trusts supplied query-language
  metadata when present, and infers only when it is absent.
- **This is validation only.** It reduces bad output reaching a consumer; it does not improve the
  generator. The underlying model still emits these defects at the measured rates.

## Final Decision

**GENERATION OUTPUT CONTRACT V1 — CLOSED / GO**

Generator candidate v5 remains **NEEDS IMPROVEMENT**. The contract is an enforcement layer, not a
fix, and the candidate descriptor was not promoted.

Next: **OUTPUT-CONTRACT-INTEGRATED FROZEN BENCHMARK V2 RE-EVALUATION**
