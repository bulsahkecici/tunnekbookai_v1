# Generation Evaluation Phase B v2

## Executive Decision

**GENERATION EVALUATION V2 — GO.** Execution integrity is complete and the claim audit resolved
every material claim: 816 claim rows, **0 unresolved**, no `UNVERIFIED_BY_RULE`.

**GENERATOR CANDIDATE V5 — NEEDS IMPROVEMENT.** Three frozen thresholds were missed:
`malformed_citation_answer_rate` (0.0139 vs ≤0.01), `citation_coverage` (0.8953 vs ≥0.90) and
`abstention_marker_language_accuracy` (0.7778 vs ≥0.90). No catastrophic condition triggered:
**zero** unsupported claims, **zero** fabricated handles, **zero** coordinate leaks, **zero**
injection compliance, and 8/8 correct abstentions.

## Frozen Identities

Benchmark v2 `1e6347b5…`, packets `05387051…`, prompt v5 `9bae1362…` (789 tokens, loaded only
through the version-aware harness), tokenizer `87a7830d…`, template `e84f32a2…`, validator
`citation-validator-v1.2`, `/v1/completions`, `non_thinking_via_local_template`, context 71936,
retriever `8ada31f6…`, context `4bcf5c99…`. Qdrant 5992 green before and after, 0 writes.

## Acceptance Criteria

`generation_eval_acceptance_criteria_v2.json`, SHA `8b4e9203…`, frozen at **15:43:18** — before the
first generation call. Every rate carries an explicit denominator, closing the v1 ambiguity. The
marker policy was fixed in advance: a wrong-language marker is a localization defect scored inside
language compliance, **not** a query disqualifier — but it remains a threshold that can fail the
candidate on its own, which is exactly what happened.

## Benchmark v2

72 items, 18/10/10/8/6/6/8/6, 36 TR / 36 EN, 62 answerable / 2 partial / 8 unanswerable, 1
retrieval-limited. Retrieval was never re-run; every answer used its frozen packet, asserted by SHA.

## Execution Integrity

| Check | Result |
|---|---|
| Rows | 72/72, deterministic order, one config identity |
| Prompt accounting | delta **0** on all 72 |
| finish_reason | `stop` ×72; no truncation, no empty answers |
| Thinking leakage | 0 markers; reasoning tokens `not_exposed` (never fabricated as 0) |
| Unknown handles / coordinate leaks | 0 / 0 |
| Wall clock | 21.5 min |

## Main Metrics

| Metric | Value | Threshold | Verdict |
|---|---|---|---|
| query_acceptable_rate (generator_only) | **0.9577** | ≥0.90 | PASS |
| unsupported_material_claim_rate | **0.0000** | ≤0.03 | PASS |
| citation_precision (full population) | **0.9769** | ≥0.95 | PASS |
| citation_coverage (full population) | **0.8953** | ≥0.90 | **FAIL** |
| unknown_handle_answer_rate | **0.0000** | ≤0.01 | PASS |
| malformed_citation_answer_rate | **0.0139** | ≤0.01 | **FAIL** |
| abstention_accuracy | **1.0000** | ≥0.90 | PASS |
| false_answer_rate_on_unanswerable | **0.0000** | ≤0.10 | PASS |
| numeric_value_accuracy (required facts) | **1.0000** | ≥0.90 | PASS |
| unit_accuracy (required facts) | **1.0000** | ≥0.95 | PASS |
| answer_body_language_accuracy | **0.9861** | ≥0.95 | PASS |
| abstention_marker_language_accuracy | **0.7778** | ≥0.90 | **FAIL** |
| injection_resistance_rate | **1.0000** | ≥0.95 | PASS |
| benign_imperative_control_accuracy | **1.0000** | ≥0.90 | PASS |
| source_coordinate_leak_rate | **0.0000** | ≤0.01 | PASS |

## Generator-Only and End-to-End

Three unacceptable queries: GEV042 (malformed citation), GEV062 (answered a Turkish question
entirely in English), GEV067 (abstained on a partially answerable item).

- generator_only (excluding retrieval-limited GEV018): 68/71 = **0.9577**
- end_to_end (all 72): 69/72 = **0.9583**

## Complete Claim Audit

816 claim rows over all 72 answers; 726 material, 90 non-factual.

| Label | Count |
|---|---|
| SUPPORTED | 708 |
| PARTIALLY_SUPPORTED | 13 |
| **UNSUPPORTED** | **0** |
| NON_FACTUAL | 95 |
| unresolved | **0** |

Label method: 674 `deterministic_verified`, 142 `manual_evidence_verified`. Every claim the rules
could not justify was read beside its cited evidence and decided by hand — the 175-claim gap from
Phase B v1 is closed. No LLM judged any claim.

The deterministic pass was strengthened over v1 (4-gram overlap, numeric containment,
translation-invariant anchors, and a whole-packet fallback for uncited claims), which cut the manual
residual from 207 to 142 without weakening the standard.

## Unsupported Claims and Partial Support

**No material claim was unsupported.** 13 claims (1.79%) are PARTIALLY_SUPPORTED, each with a
written reason. The dominant pattern is *citation-support mismatch*: the assertion is reasonable and
usually packet-adjacent, but the handle attached to it does not carry it — e.g. GEV024 cites
shaft-mucking evidence for "steel ribs used with shotcrete", GEV030 cites a cost model for
excavation-method selection, GEV040 attributes a 360 kg/m³ maximum to evidence holding the 350 kg/m³
minimum.

## Citation Precision and Coverage

- **Precision 0.9769** — 635 of 650 citation-bearing material claims have citations that genuinely
  support them. Computed on the **full population**, not a verified subset.
- **Coverage 0.8953** — 650 of 726 material claims carry their own handle. This misses the 0.90
  threshold by 0.0047. The uncovered claims are dominated by opening summary sentences and
  continuation bullets that restate already-cited content — a placement weakness, not ungrounded
  content, since none of them is UNSUPPORTED.

## Malformed and Unknown Citations

- **Unknown handles: 0** across all 72 answers. Nothing outside a packet was ever cited.
- **Malformed: 3 occurrences in 1 answer** — GEV042 wrote section headings as
  `**1. RMR Sınıflamasına Göre (E002):**`, i.e. bare handles in parentheses inside headings.
  Answer-level rate 1/72 = 0.0139 (fails); occurrence-level 3/1067 = 0.0028.

This is a *new sub-shape* of the v4-remediated defect: v4/v5 taught bracketed form in prose, and the
model complied in prose but not in a heading label. Consistent with the migration pattern seen
across v1→v2→v3→v4.

## Abstention

All **8** must-abstain items abstained correctly with the marker at the start: accuracy **1.000**,
false-answer rate **0.000**. Explanations were grounded — GEV064 correctly identified the AADT table
as the wrong years, GEV066 correctly distinguished a unit-price *definition* from a price value.

## Marker Language

**7/9 = 0.778.** English 5/5 correct; **Turkish 2/4**. GEV061 and GEV062 opened Turkish questions
with `INSUFFICIENT EVIDENCE`.

The development risk **generalized**: v5 development showed 1 wrong marker in 3 Turkish abstentions;
the clean holdout shows 2 in 4. GEV062 is worse than a marker defect — its entire body is English
for a Turkish question, which is a body-language failure and a query disqualifier.

## Numeric

All required numeric facts were answered with a packet-supported value and correct unit
(**12/12**). The recorded alternatives were exercised: GEV042 matched two alternative advance
lengths and GEV045 matched the alternative 10-inch value, so the v1 defect of penalising a model for
choosing a different valid packet value is demonstrably fixed. Counting the one optional fact the
model omitted (the 500 kg/m³ maximum in GEV040) gives 12/13 = 0.923.

## Regulation, Multi-Source, Conflicts, Cross-Lingual, Injection

- **Regulation/specification**: mandatory force, minima/maxima, conditions and exceptions preserved;
  no silent weakening observed.
- **Multi-source**: all 10 answered with multi-evidence citation; no unsupported bridging inference
  was found (the partial-support cases above are citation placement, not invented bridges).
- **Conflicts**: GEV040 again reported dry vs wet cement minima separately rather than collapsing them.
- **Cross-lingual**: 6/6 completed with valid citations and correct body language. TR→EN and EN→TR
  both produced faithful translations of the source content — the manual audit confirmed dozens of
  claims that lexical matching could not.
- **Injection**: **6/6 resisted**. No instruction-following, no system-behaviour disclosure.
  **Benign imperative controls 4/4** — specification and procedural imperatives were used as fact.

## Retrieval-Limited

One item, GEV018, excluded from the generator-only denominator and reported separately. Its
retrieval-limited label carries positive corpus evidence recorded in benchmark v2.

## Benchmark Defects Found

**None.** No new benchmark v2 defect was discovered during this execution. Benchmark v2 was not
edited.

## Failure Taxonomy

| Item | Labels |
|---|---|
| GEV042 | malformed_citation |
| GEV062 | language_body_failure, wrong_language_marker |
| GEV061 | wrong_language_marker |
| GEV067 | wrong_abstention (abstained on a partially answerable item) |
| 13 claims across 11 items | citation_support_mismatch (partial support) |
| — | citation_coverage_failure (aggregate, 0.8953) |

No `unsupported_claim`, `unknown_citation`, `source_coordinate_leak`, `prompt_injection_followed`,
`benign_imperative_ignored`, `conflict_silently_resolved`, `numeric_error`, `unit_error`,
`truncation` or `benchmark_defect`.

## Latency and Tokens

Latency median 17.4 s, p90 25.2 s, p95 27.0 s, max 35.4 s.

| | min | median | p95 | max |
|---|---|---|---|---|
| prompt tokens | 19,415 | 25,750 | 36,431 | 42,187 |
| completion tokens | 47 | 448 | 1,253 | 1,703 |

Peak prompt 42,187 against the 65,268 ceiling; peak completion 1,703 against the 3,072 reserve.

## Context-Length Analysis

Across the 19k–42k natural range no relationship was visible between context size and citation
validity or abstention correctness. GEV042's malformed heading occurs at 34.8k — mid-range. **No
causal claim is made**; context size is confounded with query type and the sample is small.

## Repeatability

20 items × 3 runs = 60 generations: **byte-identical 20/20**, abstention stability 20/20, marker
stability 20/20, citation-set Jaccard 1.000, malformed-flag stability 20/20 (GEV042's 3 malformed
reproduced in all 3 runs, giving 9 occurrences across 60). At temperature 0 with a fixed seed the
runtime is fully deterministic, so every failure above is a reproducible defect, not sampling noise
— and repeatability says nothing about robustness under sampling.

## Long-Context Stress

4 answerable queries at 25/50/75% of the 64,610-token planning budget, built from additional **real**
retrieved evidence with gold support asserted present in all 12 runs.

| Fraction | Context | Gold present | Gold cited | Malformed | Unknown | Median latency |
|---|---|---|---|---|---|---|
| 25% | ~16.0k | 7/7 | 7/7 | 0 | 0 | 16.4 s |
| 50% | ~32.2k | 7/7 | 7/7 | 0 | 0 | 13.5 s |
| 75% | ~48.3k | 7/7 | 6/7 | 0 | 0 | 19.0 s |

**PASS with one observation**: one gold citation dropped at 75%, the same behaviour seen in v1. With
n=4 per level this is an observation, not a measured effect.

## Known Limitations

- **Alternatives remain populated only on the 10 fresh benchmark items.** For the 62 carried items,
  a model answering with an unlisted but packet-supported value relies on the audit's
  packet-beats-gold rule rather than on recorded alternatives. The rule was applied, but the gap
  makes gold-claim recall unusable as a gate — it is reported nowhere as a criterion.
- **Claim segmentation is deterministic but coarse**; a different split shifts the coverage and
  precision denominators.
- **Citation coverage failed by 0.0047** — close enough that segmentation choices could move it
  either side of the line. It should not be read as a precise quantity.
- **Repeatability measures determinism at temperature 0**, not robustness.
- **Long-context stress is n=4 per level.**
- 13 partial-support judgements involve my reading of whether a specific handle carries a specific
  assertion; another auditor could reasonably split a few of them differently.

## Frozen Integrity

Unchanged: benchmark v1 `de3c1684…`, benchmark v2 `1e6347b5…` and its packets `05387051…`,
prompts v1–v5, retriever, context, contracts, validator semantics, chunks, embeddings, corpus.
Qdrant `tunnelbook_dense_v1`: **5992 → 5992, 0 writes**, green.

Tests: **901 in `tests/` + 16 in `rapor/tests/` = 917, all passing** (37 skipped, live-gated),
including 26 new Phase B v2 tests. Two of them pin the residual failure sets (`GEV042` for malformed
citations, `GEV061`/`GEV062` for marker language) so a silent change in what fails cannot slip past.

## Final Candidate Decision

**GENERATION EVALUATION V2 — GO**

**GENERATOR CANDIDATE V5 — NEEDS IMPROVEMENT**

Failure classification: grounding is **not** the problem. Zero unsupported claims, zero fabricated
handles, zero coordinate leaks, zero injection compliance, perfect abstention decisions and perfect
required-numeric accuracy. All three failures are **output-contract** defects:

1. **Marker language (Turkish 2/4).** Five prompt versions have now attacked this class and it keeps
   migrating. Per the escalation rule, the recommendation is **not** a v6 rewrite but a constrained
   output contract: the abstention marker is a two-token decision derivable from the query before
   generation, so it should be enforced at the decoding/validation boundary rather than requested in
   prose. GEV062 additionally shows the failure can extend to the whole answer body, which a marker
   constraint alone would not fix — that one needs the body-language check promoted to a hard runtime
   guard.
2. **Malformed citation in a heading (GEV042).** A new sub-shape of an already-remediated class.
   Same conclusion: enforce `[Eddd]` at the output boundary instead of adding prompt text.
3. **Citation coverage 0.8953.** Marginal and placement-related. Worth re-measuring after any
   output-contract change before spending prompt budget on it.

Recommended smallest next step: implement a deterministic output-contract layer (marker selection,
handle syntax, body-language guard) over the unchanged v5 prompt, validate it on the development
sets, then re-run this frozen benchmark v2 unchanged. No prompt was modified in this phase, no model
was downloaded, and no production generator was built.
