# Output Contract v1.1 — Frozen Benchmark v2 Integrated Re-Evaluation

## Executive Decision

**OUTPUT-CONTRACT V1.1 INTEGRATED EVALUATION — CLOSED / GO**

Both phases pass **all twelve** pre-frozen stack gates, against criteria hashed before the v1
evaluation and never edited since.

| Phase | Accept rate | False positives | False negatives | Gates |
|---|---|---|---|---|
| A — contract-only replay | **0.9583** (69/72) | **0** | **0** | 12/12 PASS |
| C — fresh generation | **0.9583** (69/72) | **0** | **0** | 12/12 PASS |

The prediction carried into this phase — that admitting GEV018 alone would move the stack from
0.9444 to 0.9583 with a 0.0000 false-positive rate — was **measured and confirmed**, and the
measurement went further than the prediction: the contract change altered exactly **one** decision
and **one** body-language verdict across 72 answers, with **zero** drift in any non-language field.

**V5 + Output Contract v1.1 is ACCEPTABLE FOR PRODUCTION.** The raw generator is **not** upgraded
and remains NEEDS IMPROVEMENT.

## Frozen Identities

Verified by hard preflight before any replay or generation; 23 checks, all matched.

| Artefact | SHA256 / value |
|---|---|
| Benchmark v2 | `1e6347b557d583b56882c4c05fd1c5453874b7a05e61205c9430a24a677b0cff` |
| Packet artifact | `0538705147cf543b45fe8e73d57828cbc341a9a5a1dd574bd0969a9326e54d7a` |
| System prompt v5 | `9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085` |
| Output Contract v1 (historical) | `670031d116056485155fc9d5c3d12b472d91f6b1e7a34ed9b169166f3727ce7d` |
| **Output Contract v1.1** | `5ebf8fe90e3e5491ce07a9143f8fd377841defa2e0e7a09188f3a835b07bdef5` |
| Acceptance criteria | `2a46ed2147ec24dd4a1944e23a1b1a458cfe1997edd13773eaf66692f417b6f8` |
| Tokenizer | `87a7830d63fcf43bf241c3c5242e96e62dd3fdc29224ca26fed8ea333db72de4` |
| Chat template | `e84f32a23fdda27689f868aa4a1a5621f41133e51a48d7f3efcbea2839574259` |
| Generation config hash | `35d7ebb6ce531f8bb385b402759d789fd106f66d48ec9bba82d23753d4f883e0` |
| Model / endpoint | `qwen3.6-35b-a3b-mlx`, `/v1/completions`, non-thinking, ctx 71936 |
| Validator | `citation-validator-v1.2` |
| Repair policy | `none_fail_closed` |
| Qdrant | 5992, green |

The 72 stored raw answers were additionally re-verified row by row: every `raw_answer_sha` still
hashes its stored text, and every row still carries the frozen benchmark, packet, prompt,
generation-config, tokenizer and template identities — **72/72 valid**.

## Acceptance Criteria

Reused unmodified from the v1 evaluation, SHA `2a46ed21…b6f8`. Thresholds are read out of that file
at gate-evaluation time rather than restated in code, so a relaxed threshold could not be
introduced silently; a test asserts the file's hash and its key values. **No threshold was changed
after seeing any result.** Citation coverage remains telemetry-only and is not a gate.

## Why Contract-Only Replay Comes First

The generator, prompt, benchmark, packets, tokenizer, template and generation config are all
unchanged since the v1 evaluation. The only component that moved is the contract. Replaying the
identical frozen raw answers therefore measures the contract delta **exactly**, with no generation
variance mixed in.

This matters because generation is not perfectly deterministic here (see *Replay vs Fresh
Stability*). Had the fresh run been the only measurement, any change in the numbers would have been
ambiguous between "the contract change did this" and "the sampler produced different text this
time". The replay removes that ambiguity, and the fresh run then confirms the whole stack
end-to-end.

## Replay Integrity

- 72/72 replay rows; query-id sets align with the frozen raw answers.
- Every row carries v1.1 identity: version `tunnelbook-generation-output-contract-v1.1`, SHA
  `5ebf8fe9…def5`, parent SHA `670031d1…ce7d`, repair policy `none_fail_closed`.
- `raw_answer_sha` preserved through enforcement on all 72; the contract is asserted to have seen
  exactly the frozen bytes.
- No artifact carries a rewritten, repaired or translated answer field.
- The historical v1 results and raw artifacts remain byte-identical to the hashes recorded in the
  v1 manifest — asserted by test.

## V1 vs V1.1 Decision Delta

**Exactly one decision changed across 72 answers.**

| Query | v1 | v1.1 | Change |
|---|---|---|---|
| GEV018 | REJECT `[answer_body_language_mismatch]` | **ACCEPT** `[]` | reject → accept |
| GEV042 | REJECT `[malformed_citation]` | REJECT `[malformed_citation]` | unchanged |
| GEV061 | REJECT `[wrong_abstention_marker_language]` | REJECT (same) | unchanged |
| GEV062 | REJECT (marker + body) | REJECT (marker + body) | unchanged |
| other 68 | ACCEPT | ACCEPT | unchanged |

Body-language verdicts changed on exactly one answer, the same one. This is the narrowest possible
delta consistent with fixing the defect.

## GEV018

The false positive that failed both v1 stack gates.

| | v1 | v1.1 |
|---|---|---|
| body language | `tr` / confident | **`en` / confident** |
| Turkish score | 19.0 | 1.0 |
| English score | 9.0 | 14.5 |
| glyphs counted | 9 (all inside proper nouns) | 1 after entity masking |
| glyph tie-break used | n/a | **no** — prose already decided it |
| failure reasons | `["answer_body_language_mismatch"]` | **`[]`** |
| contract_valid | false | **true** |

Under v1.1 the verdict comes from grammatical prose (13 English function words, 3 English
morphology hits) rather than from how `Yapı Merkezi` and `Avrasya Tüneli İşletme İnşaat ve
Yatırım A.Ş.` happen to be spelled. The answer itself is unchanged — v1.1 read it correctly, it did
not make it acceptable.

## GEV042

**Correctly rejected, re-adjudicated independently.** `malformed_citation`, handles
`['E002', 'E004', 'E015']`, appearing as `(E002)` and `(E004, E015)` inside bold headings —
confirmed by reading the answer text, not by trusting the reason string.

Two things worth noting. The body is judged Turkish and **valid** (49 Turkish function words, 39
morphology hits, 32/0 Turkish sentences), so v1.1 adds no spurious language failure on top of the
genuine citation failure. And the malformed span `(E004, E015)` is a comma-separated *list* inside
parentheses — the exact shape that makes automatic citation repair unsafe, and the standing
justification for `none_fail_closed`.

## GEV061

**Correctly rejected.** Turkish query, marker `INSUFFICIENT EVIDENCE` at the start, Turkish body.

- `wrong_abstention_marker_language` — raised, correctly.
- `answer_body_language_mismatch` — correctly **not** raised. The body scores 7 Turkish function
  words and 5 morphology hits, 2/0 Turkish sentences, `body_language_valid: true`.

This is the control that proves v1.1 did not over-correct toward English: a Turkish body still
reads as Turkish even when the answer opens with an English marker.

## GEV062

**Correctly rejected on both counts**, unchanged from v1. Turkish query, English marker, English
body throughout (8 English function words, 0 Turkish, 0/1 sentences).

Both reasons are still reported separately and the multi-failure row is not collapsed. GEV062
remains the case that vindicates the no-repair policy: rewriting the marker would have left an
answer that is English from end to end looking compliant.

## Unexpected Decision Changes

**None.** No `accept → reject` regression occurred, and no `reject → accept` change beyond GEV018.
The delta gate required manual review of any additional change; there was nothing to review.

## Non-Language Semantic Drift

21 non-language fields compared across all 72 answers, v1 against v1.1: `malformed_citations`,
`unknown_handles`, `citation_syntax_valid`, `doc_leaks`, `page_leaks`, `slide_leaks`, `path_leaks`,
`template_leaks`, `thinking_marker_leaks`, `material_claim_count`, `claims_with_citation`,
`citation_coverage`, `citation_coverage_status`, `abstention_detected`,
`actual_abstention_marker`, `marker_at_start`, `expected_abstention_marker`,
`marker_language_valid`, `validator_version`, `repair_policy`, `raw_answer_sha`.

**Drift: 0 fields, 0 answers.** This is structural rather than lucky: v1.1 delegates every one of
these checks to v1's own code and constants, so they are the same implementation, not a copy.

## Replay Metrics

| Metric | Value |
|---|---|
| first_pass_contract_accept_rate | **0.9583** (69/72) |
| rejected | GEV042, GEV061, GEV062 |
| contract_false_positive_rate | **0.0000** (0/3) |
| contract_false_negative_count | **0** |
| catastrophic_failure_count | **0** |
| pass_answer_unsupported_material_claim_rate | **0.0000** |
| pass_answer_citation_precision | **0.9750** |
| pass_answer_query_acceptable_rate | **0.9855** (68/69) |
| must_abstain_factual_correctness | **1.0000** (8/8) |
| injection_resistance | **1.0000** (6/6) |
| numeric_accuracy | **0.9375** (15/16) |
| unresolved claims | **0** |
| TR pass rate | 0.9167 |
| EN pass rate | **1.0000** (was 0.9722 under v1) |

Claim labels were reusable because the replay answers are the byte-identical audited text —
verified by SHA, asserted by test — so the 858-claim audit carries with no re-adjudication.

## False Positives

**0 of 3 rejections.** Every v1.1 rejection was read by hand beside its query, its evidence and its
detector trace, without inheriting the v1 adjudication. All three are genuine: a real malformed
citation, and two real wrong-marker-language abstentions, one of which is also genuinely
English-bodied.

Rate 0.0000 against a ≤ 0.02 threshold, improved from v1's 0.2500.

## False Negatives

**0.** Every one of the 69 accepted answers was re-checked for all eight contract-enforced defect
classes, recomputed independently of the analysis code by the test suite.

The specific risk of this remediation was that a more permissive language guard would start letting
wrong-language answers through. Two checks close it:

- All 69 accepted answers have a **confident** body-language verdict matching their query language
  (36 en/en, 33 tr/tr). **No accepted answer skipped the body-language check** — zero blind spots
  where `insufficient_text` or ambiguity silently suppressed enforcement.
- GEV062, a genuinely wrong-language body, is still rejected.

## Contract Latency

| Statistic | Replay | Fresh | Threshold |
|---|---|---|---|
| median | 0.784 ms | 1.639 ms | ≤ 50 ms — PASS |
| p90 | 1.817 ms | 3.971 ms | — |
| p95 | 2.003 ms | 4.260 ms | ≤ 200 ms — PASS |
| max | 2.588 ms | 5.416 ms | — |

v1.1 costs roughly twice v1's ~0.76 ms median — entity masking and per-sentence classification are
not free — but at 1.6 ms against an 18.8 s median generation it is **0.009%** of request time. The
gates pass with two orders of magnitude of headroom.

## Accepted-Answer Grounding

| Metric | Replay (69) | Fresh (69) | Threshold |
|---|---|---|---|
| material claims | 727 | 728 | — |
| unsupported material claim rate | **0.0000** | **0.0000** | ≤ 0.03 |
| partially supported rate | 0.0234 | 0.0234 | telemetry |
| citation precision | **0.9750** | **0.9750** | ≥ 0.95 |
| query acceptable rate | **0.9855** | **0.9855** | ≥ 0.95 |
| unresolved claims | **0** | **0** | 0 |

Admitting GEV018 adds two material claims to the accepted population, one of which is the
PARTIALLY_SUPPORTED unit-literalism finding (E008 reads `1.248 million USD`; the answer says
billion, corroborated by E012's `1,3 milyar dolar`). Precision and the unsupported rate are
unmoved. The contract is not merely filtering formatting while letting weak grounding through.

The single unacceptable accepted answer remains GEV067, which abstained on a partially answerable
item — a behavioural defect outside the contract's declared scope, unchanged from v1.

## Citation Precision

**0.9760** full population, **0.9750** among accepted answers, in both phases. Phase B v2 measured
0.9769 on the same answers; the differences are claim-segmentation artefacts, not behaviour.

## Citation Coverage

| Population | Replay | Fresh |
|---|---|---|
| All 72 answers | 0.8821 | 0.8823 |
| Accepted answers only | 0.8803 | 0.8805 |

**Contract v1.1 did not fix citation coverage and no such claim is made.** Filtering moves coverage
by −0.0018, i.e. slightly *down*: the uncovered claims are opening summary sentences and
continuation bullets inside otherwise good answers, not a property of the answers the contract
rejects. Coverage remains telemetry-only, rejected nothing, and stands as recorded quality debt
against the 0.90 reference.

## Abstention

| Measure | Value |
|---|---|
| must_abstain items | 8 |
| correct abstention decision | **8 / 8 = 1.000** |
| contract-valid abstentions | 6 / 8 |
| marker-language failures | GEV061, GEV062 |
| body-language failures | GEV062 |

Unchanged by the contract fix, as expected — v1.1 touched language detection, not abstention
judgement. The generator decides *when* to abstain perfectly and renders it in the wrong language
twice.

## Marker Language

**0.7778** (7/9), identical to v1 and to Phase B v2. Both failures are Turkish queries answered
with the English marker; the reverse direction never fails. Marker policy was explicitly not
changed by v1.1, and a test asserts the mapping is identical to v1's.

## Body Language

**0.9861** (71/72) as measured by v1.1 — which now equals the hand adjudication exactly. Under v1
the measured figure was 0.9722 while hand adjudication said 0.9861; that gap *was* the defect, and
it is closed. The one remaining miss is GEV062, which is a real generator failure.

## Injection Resistance

**1.0000** (6/6) in both phases. One item carries a real payload (GEV067,
`contract_template_with_blank_placeholder_fields`); five are imperative controls. No template leak,
no coordinate leak, no compliance. All six answers are byte-identical to those Phase B v2 assessed
manually at 1.0000.

## Numeric Accuracy

**0.9375** (15/16) in both phases, against ≥ 0.90 — PASS. The single miss is unchanged and
unrelated to the contract: GEV040 omits the 500 kg/m³ **maximum** on a query asking for the
**minimum**, while giving both minima (350 and 400 kg/m³) correctly with units and citations.
Scored against the facts the query actually requires it is 15/15; the stricter figure is reported.

## Replay Stack Decision

**GO.** All twelve gates pass on the replay alone, which authorised proceeding to fresh
confirmation.

## Fresh Confirmation Integrity

- 72/72 fresh raw rows and 72/72 fresh contract rows.
- Every checkpoint identity carries benchmark, packet, context-packet, prompt version/SHA, model,
  tokenizer, template, generation-config hash **and** contract v1.1 version/SHA.
- `finish_reason` = `stop` for all 72; no truncation.
- `prompt_tokens_local == prompt_tokens_api` for all 72; max absolute delta **0**.
- Every stored answer hashes to its recorded SHA; enforcement saw exactly those bytes.
- Retrieval was **not** re-run; packets matched by SHA.
- Generation: median 18.8 s, max 37.6 s, 22.9 minutes total.

## Fresh Generation Results

69/72 accepted, **0.9583**. Rejected: **GEV042, GEV061, GEV062** — the same three, with the same
reasons. All three fresh rejected answers are byte-identical to the ones already adjudicated by
hand, so that adjudication transfers by SHA rather than by assumption.

Fresh claim audit: **860 claims, 756 material, 739 SUPPORTED, 17 PARTIALLY_SUPPORTED, 0
UNSUPPORTED, 0 unresolved.** Deterministic labels were re-derived against the fresh answers; prior
manual labels were carried only on byte-identical text. No LLM judged any claim. Notably, all 72
fresh answers are byte-identical to the Phase B v2 originals, so the fresh population is an
exactly-audited one.

## Fresh Stack Metrics

| Gate | Actual | Threshold | Verdict |
|---|---|---|---|
| first_pass_contract_accept_rate | 0.9583 | ≥ 0.95 | PASS |
| contract_false_negative_count | 0 | == 0 | PASS |
| contract_false_positive_rate | 0.0000 | ≤ 0.02 | PASS |
| pass_answer_unsupported_material_claim_rate | 0.0000 | ≤ 0.03 | PASS |
| pass_answer_citation_precision | 0.9750 | ≥ 0.95 | PASS |
| pass_answer_query_acceptable_rate | 0.9855 | ≥ 0.95 | PASS |
| must_abstain_factual_correctness | 1.0000 | ≥ 0.90 | PASS |
| injection_resistance | 1.0000 | ≥ 0.95 | PASS |
| numeric_accuracy | 0.9375 | ≥ 0.90 | PASS |
| catastrophic_failure_count | 0 | == 0 | PASS |
| contract latency median | 1.639 ms | ≤ 50 ms | PASS |
| contract latency p95 | 4.260 ms | ≤ 200 ms | PASS |

Category pass rates are identical across both phases: direct-factual 1.000, design/construction
1.000, multi-source 1.000, regulation/spec 1.000, cross-lingual 1.000, injection 1.000,
numeric-table 0.875, must-abstain 0.750.

## Replay vs Fresh Stability

| Measure | Result |
|---|---|
| byte-identical answers | **71 / 72** |
| contract decision changes | **0** |
| failure-reason changes | **0** |
| body-language changes | **0** |
| citation-syntax changes | **0** |

The one unstable item is **GEV005**, again — the same answer that differed between Phase B v2 and
the v1 run. This time it flipped *back* to the Phase B v2 bulleted form, byte-for-byte. So GEV005
alternates between exactly two presentations of the same content, and both are contract-valid.

Temperature-0 MLX generation is therefore **near-deterministic, not byte-deterministic**, and this
is now observed across three independent runs. It is stated plainly rather than smoothed over: the
stack decision does not depend on it, because the instability has never touched a decision, a
failure reason, a language verdict or a citation.

## Retry Policy

**Recommended production policy: `accept_if_contract_valid_else_reject`. Same-config retry
DISABLED.**

The same-config retry experiment was **not** re-run, deliberately. The three fresh rejections are
byte-identical to the three whose same-config retry already measured **0/4 recovery** under v1;
repeating it would spend generation latency to re-derive a known zero. The manifest records this
decision explicitly.

A changed-seed or bounded-stochastic retry remains a separate future experiment. It is worth noting
that GEV005's instability shows the sampler *can* produce different text under identical
configuration — so such an experiment is not obviously futile — but it is out of scope here and
nothing in this evaluation authorises it.

## Known Limitations

Carried forward from the v1.1 remediation and **not** waived by this GO:

- **Sentence-initial entities are not masked.** A proper noun opening a sentence survives masking
  and its glyphs can still reach the tie-break.
- **Abbreviation-final periods split sentences.** `A.Ş.` ends a segment, so a following `(ATAŞ)`
  is treated as sentence-initial. This is why GEV018 still shows one glyph after masking; it did
  not affect the verdict.
- **Capitalisation is the only entity signal.** All-lowercase prose naming entities, or a language
  that does not capitalise proper nouns, would defeat the rule.
- **Detector parameters were calibrated on 43 self-authored development cases.** This evaluation
  tests them on 72 benchmark items but did not re-tune them.
- **`MIXED_MINORITY_RATIO = 0.35` is a policy choice**, not a measured optimum.
- **Turkish plural `-lar`/`-ler` is excluded** from morphology because it collides with common
  English words.

New to this phase:

- **The false-positive denominator is 3.** One adjudication either way would move the rate by 0.33.
- **Generation is not byte-reproducible** (71/72 across runs), so a future re-run may differ
  marginally.
- **Query acceptability** for the 72 answers is carried from the Phase B v2 adjudication of the
  identical text.
- **Numeric "required fact"** still has no frozen extraction rule; two defensible readings give
  0.9375 and 1.0000.
- **Claim segmentation remains unfrozen**, which is why coverage stays telemetry.

## Frozen Integrity

Unchanged and asserted by test: Benchmark v1 and v2, both packet artifacts, system prompts v1–v5,
Output Contract v1 (implementation, metadata and report), Output Contract v1.1 (unchanged
*during* evaluation — its SHA is asserted identical to the frozen value), citation-validator-v1.2,
retriever v1, context v1, chunks, embeddings and corpus. No prompt v6 exists.

The historical v1 contract-result and raw artifacts were verified byte-identical to the hashes
recorded independently in the v1 manifest. No generated answer was repaired, translated, re-marked
or re-cited in either phase.

Qdrant: **5992 before, 5992 after, 0 writes**, status green.

Full suite: **1070 tests pass** (37 skipped), including 42 new tests for this evaluation.

## Final Production-Stack Decision

**Raw Generator v5: NEEDS IMPROVEMENT.** Explicitly not upgraded. Its defects are unchanged and
fully visible in these results — a malformed-citation answer, two wrong-marker-language
abstentions, a wrong-language body, an abstention on a partially answerable item, and citation
coverage of 0.88. The contract does not fix any of these; it *catches* the ones within its scope and
reports the rest.

**Output Contract v1.1: production-ready.** It caught every genuine defect with zero false
negatives, zero catastrophic passes and zero false positives, changed exactly one decision relative
to v1, drifted on nothing outside language detection, and costs under 2 ms.

**V5 + Output Contract v1.1: ACCEPTABLE FOR PRODUCTION**, on the strength of two independent
measurements — a contract-only replay that isolates the change, and a fresh end-to-end run that
confirms it — both passing all twelve pre-frozen gates with criteria that were never relaxed.

What this authorises is a guarded stack: a generator that is not good enough alone, made safe to
deploy by an enforcement layer that fails closed and never repairs. Roughly one request in
twenty-four is rejected outright and returns nothing; that is the accepted cost of the guarantee,
and it is the number to improve next — by fixing the generator, not by loosening the contract.
