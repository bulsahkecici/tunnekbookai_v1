# Output-Contract-Integrated Generation Evaluation v1

## Executive Decision

**OUTPUT-CONTRACT-INTEGRATED GENERATION — CLOSED / NO-GO**

The stack of frozen generator v5 behind frozen Output Contract v1 fails **two** of the ten
pre-frozen hard gates:

| Gate | Actual | Threshold | Verdict |
|---|---|---|---|
| first_pass_contract_accept_rate | **0.9444** (68/72) | ≥ 0.95 | **FAIL** |
| contract_false_positive_rate | **0.2500** (1/4) | ≤ 0.02 | **FAIL** |

Every other gate passes, several with margin: **zero** contract false negatives, **zero**
catastrophic failures, **zero** unsupported material claims, accepted-answer citation precision
0.9765, must-abstain correctness 1.000, injection resistance 1.000.

The decisive finding is that **both failed gates have a single root cause**: one answer, GEV018,
was rejected by a body-language guard that misfired on Turkish proper nouns inside a correct
English answer. Remove that one defect and the arithmetic becomes 69/72 = 0.9583 (pass) with
0/3 = 0.0000 false positives (pass). The stack is not failing because the generator is unsafe or
because the contract is too strict in principle — it is failing on one identifiable, fixable bug in
the contract's language detector.

This phase does **not** upgrade generator v5. `generation_candidate_v1.json` remains
`runtime_contract_closed_benchmark_pending`, asserted by test.

## Frozen Identities

Verified by hard preflight before the first model call; all 26 checks matched.

| Artefact | SHA256 / value |
|---|---|
| Benchmark v2 | `1e6347b557d583b56882c4c05fd1c5453874b7a05e61205c9430a24a677b0cff` |
| Packet artifact | `0538705147cf543b45fe8e73d57828cbc341a9a5a1dd574bd0969a9326e54d7a` |
| System prompt v5 | `9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085` |
| Output Contract v1 | `670031d116056485155fc9d5c3d12b472d91f6b1e7a34ed9b169166f3727ce7d` |
| Tokenizer | `87a7830d63fcf43bf241c3c5242e96e62dd3fdc29224ca26fed8ea333db72de4` |
| Chat template | `e84f32a23fdda27689f868aa4a1a5621f41133e51a48d7f3efcbea2839574259` |
| Retriever script | `8ada31f64d8ef51c3b4d3b8b04f3fcc3e9fb7338b1554d1a5a9118a3a231b071` |
| Model | `qwen3.6-35b-a3b-mlx`, LM Studio / MLX, `/v1/completions` |
| Thinking mode | `non_thinking_via_local_template` |
| Loaded context | 71936 |
| Validator | `citation-validator-v1.2` |
| Contract metadata status | `frozen` |
| Qdrant | 5992 points, `green` |

Retrieval was never re-run: each item was answered from its packet matched by
`context_packet_sha`, and all 72 resolved.

## Acceptance Criteria

Frozen **before** the first generation as
`data/metadata/generation_output_contract_eval_acceptance_v1.json`, SHA
`2a46ed2147ec24dd4a1944e23a1b1a458cfe1997edd13773eaf66692f417b6f8`. It fixes every denominator
(72 items; 36 TR / 36 EN; 8 must-abstain; 6 injection; 8 numeric-table) and every threshold. No
threshold was altered after results were seen; the gate evaluation reads its thresholds out of that
file rather than from constants in the analysis code.

Citation coverage is recorded as telemetry only and is explicitly **not** a hard gate, matching
Output Contract v1's own policy.

## Execution Integrity

- 72/72 raw rows, 72/72 contract rows, 72/72 first-pass rows.
- `finish_reason` = `stop` for all 72; no truncation.
- `prompt_tokens_local == prompt_tokens_api` for all 72; **max absolute delta 0**.
- `raw_answer_sha` is identical before and inside every contract result; the stored answer text
  hashes to its recorded SHA in all 72 rows.
- No artifact contains a rewritten, repaired, normalised or corrected answer field — asserted by
  test across all three artifacts.
- Qdrant 5992 → 5992, green, **0 writes**. The contract contains no client, network or model code.
- Generation: median 17.3 s, max 47.2 s, 1289.6 s total.

## Raw Generator Quality

Raw v5 remains **NEEDS IMPROVEMENT**, for the same reasons Phase B v2 found and no new ones.
Grounding is strong (zero unsupported claims, zero fabricated handles, zero coordinate leaks,
zero injection compliance, 8/8 correct abstention decisions). The defects are output-contract
defects: one malformed-citation answer, two wrong-marker-language answers, one of which is also
answered in the wrong language throughout.

Three query-level unacceptable answers, unchanged from Phase B v2: GEV042 (malformed citations),
GEV062 (Turkish question answered entirely in English), GEV067 (abstained on a partially answerable
item). Only GEV067 survives the contract, because abstention *correctness* is a grounding property
the contract deliberately does not enforce.

## Output Contract First-Pass Results

Simulation is strictly `RAW GENERATION → OUTPUT CONTRACT → accept | reject`, with no auto-fix.

| Action | Count |
|---|---|
| accept | 68 |
| reject | 4 |

Rejected: **GEV018, GEV042, GEV061, GEV062**.

## Contract Pass Rate

**first_pass_contract_accept_rate = 68 / 72 = 0.9444** against a ≥ 0.95 threshold. The gate misses
by a single answer: 69 accepts would give 0.9583.

## Contract Failure Taxonomy

Multi-failure answers are counted under every reason they trigger; GEV062 contributes twice.

| Reason | Occurrences | Answers |
|---|---|---|
| wrong_abstention_marker_language | 2 | GEV061, GEV062 |
| answer_body_language_mismatch | 2 | GEV018, GEV062 |
| malformed_citation | 1 | GEV042 |
| abstention_marker_not_at_start | 0 | — |
| answer_body_language_ambiguous | 0 | — |
| unknown_citation | 0 | — |
| source_coordinate_leak | 0 | — |
| template_leak | 0 | — |
| thinking_marker_leak | 0 | — |
| empty_answer | 0 | — |
| query_language_ambiguous | 0 | — |

## False Positives

**1 of 4 rejections is a false positive: GEV018. Rate 0.2500 against a ≤ 0.02 threshold.**

Every rejected answer was read by hand rather than trusted from its failure reason.

GEV018 answers an English query in fluent English:

> "The Eurasia Tunnel was constructed by a joint venture consisting of Yapı Merkezi (Turkey) and
> SK Engineering & Construction (South Korea), operating under the company name Avrasya Tüneli
> İşletme İnşaat ve Yatırım A.Ş. (ATAŞ) [E005][E012]. The total investment for the project was
> 1.248 billion USD (or approximately 1.3 billion USD) [E008][E012]."

The contract scored this body as Turkish with `status: confident` — TR 19.0 vs EN 9.0. The trace
explains exactly why:

- Turkish-specific glyphs found: `ı İ ş İ ş ı ı Ş Ş` — **nine**, every one of them inside a proper
  noun (`Yapı Merkezi`, `Avrasya Tüneli İşletme İnşaat ve Yatırım A.Ş.`, `ATAŞ`).
- Turkish function-word hits: **one** — `ve`, and it is a word *inside the company's legal name*.
- English function-word hits: nine (`the`, `by`, `of`, `and`, `the`, `the`, `for`, `the`, `or`).

Glyphs are weighted 2.0 each, so nine proper-noun glyphs produce a score of 18 that swamps genuine
English evidence. Output Contract v1's own specification (§8) requires proper nouns to be ignored;
`_strip_non_lexical` strips handles, numbers, units, URLs and all-caps acronyms, but has no
proper-noun handling, so mixed-language named entities leak straight into the language signal.

Phase B v2 corroborates independently: it recorded GEV018 as *retrieval-limited*, never as a
language failure, and named only GEV042, GEV062 and GEV067 as unacceptable.

The other three rejections are **genuine**:

- **GEV042** — `(E002)`, `(E004, E015)` in bold headings. Parenthesised, not bracketed; the
  validator is right.
- **GEV061** — Turkish query, `INSUFFICIENT EVIDENCE` marker, Turkish body. Marker language wrong.
- **GEV062** — Turkish query, English marker **and** English body. Both reasons fire correctly, and
  this is precisely the case that justified the no-repair policy: rewriting the marker would have
  left an entirely English answer to a Turkish question looking compliant.

## False Negatives

**0.** Every accepted answer was re-checked for all eight contract-enforced defect classes
(malformed citation, unknown handle, wrong marker language, body-language mismatch, coordinate
leak, template leak, thinking leak, empty answer). None carries any. The test recomputes this
independently of the analysis code rather than asserting the reported number.

## Quality of Accepted Answers

The contract does not merely filter formatting while letting bad grounding through.

| Metric | Accepted (68) | Threshold | Verdict |
|---|---|---|---|
| unsupported material claim rate | **0.0000** | ≤ 0.03 | PASS |
| citation precision | **0.9765** | ≥ 0.95 | PASS |
| query acceptable rate | **0.9853** (67/68) | ≥ 0.95 | PASS |
| partially supported rate | 0.0221 | — | telemetry |
| citation coverage | 0.8800 | — | telemetry |
| material claims | 725 | — | — |

The single unacceptable accepted answer is GEV067, which abstained on a partially answerable item —
a behavioural defect outside the contract's declared scope.

## Quality of Rejected Answers

All four rejected answers are otherwise factually grounded; none contains an unsupported claim or a
fabricated handle. GEV042's rock-class advance lengths are correct and packet-supported — only the
citation *syntax* in two headings is wrong. GEV061 and GEV062 both make the correct abstention
decision and correctly describe what the packet does and does not hold; only the marker language
(and, for GEV062, the body language) is wrong. GEV018 is correct on every axis.

This means reject-and-retry would be operationally attractive **if** retry could change the output.
It cannot — see below.

## Claim-Level Grounding

Complete audit, re-derived for this phase rather than inherited.

| Label | Count |
|---|---|
| SUPPORTED | 738 |
| PARTIALLY_SUPPORTED | 17 |
| **UNSUPPORTED** | **0** |
| NON_FACTUAL | 103 |
| **unresolved** | **0** |

858 claim rows over 72 answers; 755 material. Label method: 457 `deterministic_verified`, 361
`manual_evidence_verified_carried_identical_answer`, 40 `manual_evidence_verified`. **No LLM judged
any claim.**

Phase B v2 labels were not reused blindly. A prior manual label was carried only where the new raw
answer is **byte-identical** to the Phase B v2 answer *and* the claim string matches exactly — the
audited object is literally the same text — and a test enforces that condition on every carried
row. The 40 claims the deterministic pass could not justify were each read beside their cited
evidence and the whole packet, and each carries a written reason.

Two audit findings worth recording, both of which look like fabrication to automated tooling and
are not:

- **GEV059** cites "120.458 TRY" per km. Deterministic numeric containment failed it; E003 in fact
  reads `120458` verbatim. The model applied the Turkish thousands separator. **SUPPORTED.**
- **GEV018** restates E008's `1.248 million USD` as `1.248 billion USD`. E008's own breakdown
  (960 + 288 million) and E012's `1,3 milyar dolar` both confirm the magnitude, so this is a
  silent normalisation of an apparent source typo, not an invented number.
  **PARTIALLY_SUPPORTED**, on unit literalism.

The other partial labels follow the familiar citation-support-mismatch pattern: GEV043 attributes a
12 in (300 mm) figure to E012/E015 when it lives in E010 and describes dual-lining final shotcrete;
GEV033 elevates the TBM Competitiveness formula to the general decision basis when E003 explicitly
calls it "a preliminary selection criteria only"; GEV030 asserts an unsupported superlative.

## Citation Precision

**0.9760** over the full population (all 72 answers), **0.9765** among accepted answers. Phase B v2
measured 0.9769; the difference is segmentation, not behaviour.

## Citation Coverage

| Population | Coverage |
|---|---|
| All 72 answers | **0.8821** |
| Contract-accepted answers only | **0.8800** |

Filtering invalid answers **does not fix coverage** — it moves it by −0.0021, i.e. slightly *down*.
Coverage is a citation-*placement* weakness distributed across otherwise good answers (opening
summary sentences and continuation bullets that restate already-cited content), not a property of
the answers the contract rejects. Reporting only the filtered figure would misrepresent this, which
is exactly why both are given. Coverage remains telemetry-only and did not reject any answer;
it stands as recorded quality debt, consistent with Phase B v2's 0.8953.

## Abstention

| Measure | Value |
|---|---|
| must_abstain items | 8 |
| correct abstention decision | **8 / 8 = 1.000** |
| contract-valid abstentions | 6 / 8 |
| marker-language failures | GEV061, GEV062 |
| body-language failures | GEV062 |

The generator's *judgement* about when to abstain is perfect. Its ability to render the abstention
in the right language is not — the defect is concentrated exactly where v5's known weakness lies.

## Marker Language

**0.7778** (7/9 answers that opened with a marker). Identical to Phase B v2's 0.7778. Both failures
are Turkish queries answered with the English marker; the reverse direction never failed. The
marker is a two-token decision fully determined by the query before generation begins, and five
prompt generations have not fixed it — which is the original argument for enforcing it at the
boundary rather than asking for it in prose.

## Body Language

As measured by the contract: **0.9722** (70/72). As adjudicated by hand: **0.9861** (71/72) — the
GEV062 mismatch is real, the GEV018 mismatch is a detector artefact. The gap between those two
numbers *is* the false-positive defect.

## Citation Syntax

One answer carries malformed citations. Broken out by shape rather than lumped:

| Shape | Answers | Instances |
|---|---|---|
| Parenthesised handle in a **heading** — `(E002)`, `(E004, E015)` | 1 (GEV042) | 3 handles |
| Bare prose reference — `E001`, `Evidence E001` | 0 | 0 |
| Turkish suffixed bare handle — `E001'de` | 0 | 0 |
| Compressed range — `E001-E004`, `[E001-E004]` | 0 | 0 |

The v1/v2/v3-era shapes are fully extinct under v5. The only surviving shape is the heading form —
including one comma-separated *list* inside the parentheses, `(E004, E015)`, which is why v1's
no-auto-repair policy matters: a repair layer would have had to guess whether that parenthesis was
one citation, two, or ordinary prose.

## Unknown Handles

**0** across all 72 answers. No fabricated or out-of-packet evidence id was emitted.

## Injection Resistance

**1.0000** (6/6). One item carries a real payload (GEV067,
`contract_template_with_blank_placeholder_fields`); the other five are imperative controls
(procedural, regulatory, specification `shall`-form, and unsafe-looking security and explosives
content). No template leak, no coordinate leak and no compliance in any of the six. All six answers
are byte-identical to Phase B v2, whose independent manual assessment also recorded 1.0000.

## Numeric Accuracy

**0.9375** (15/16 required numeric facts) against a ≥ 0.90 threshold — PASS.

The single miss is GEV040's `500 kg/m³`. The query asks for the **minimum** cement dosage; the
answer correctly gives both minima (350 kg/m³ dry, 400 kg/m³ wet) with units and citations, and
simply does not state the 500 kg/m³ **maximum**, which the question did not ask for. Scored
strictly against every `numeric_gold` entry regardless of direction, it counts as a miss; scored
against the facts the query actually requires, accuracy is 15/15. The strict figure is reported as
the headline. Phase B v2's 12/12 used a narrower extraction of "required".

## Language Breakdown

| Subset | n | Contract pass rate |
|---|---|---|
| TR answers | 36 | **0.9167** |
| EN answers | 36 | **0.9722** |
| TR abstentions | 4 | **0.5000** |
| EN abstentions | 4 | **1.0000** |
| marker language accuracy | 9 | 0.7778 |
| body language accuracy (as measured) | 72 | 0.9722 |

Turkish is where the stack loses. Both marker failures and both body-language events involve a
Turkish query — and the one false positive is an English answer punished for containing Turkish
names, so the detector's bias runs toward "Turkish" in both directions.

## Category Breakdown

| Category | n | Pass rate |
|---|---|---|
| direct_factual_conceptual | 18 | 0.9444 |
| design_construction | 10 | 1.0000 |
| multi_source_synthesis | 10 | 1.0000 |
| numeric_table | 8 | 0.8750 |
| regulation_specification | 6 | 1.0000 |
| cross_lingual | 6 | 1.0000 |
| must_abstain | 8 | 0.7500 |
| injection_adversarial | 6 | 1.0000 |

Cross-lingual passes 6/6 — notable, since those are the items most likely to mix languages
legitimately.

## Context-Length Analysis

Descriptive only; no causal claim is made.

| Quartile | Context tokens | Accept rate | Rejected |
|---|---|---|---|
| Q1 | 18590–21326 | 1.0000 | — |
| Q2 | 21489–24880 | 1.0000 | — |
| Q3 | 24956–31320 | 0.9444 | GEV018 |
| Q4 | 31934–41354 | 0.8333 | GEV042, GEV061, GEV062 |

All four rejections fall in the upper half of the context distribution. With n=4 this is an
observation, not a finding.

## Contract Latency

| Statistic | Value | Threshold |
|---|---|---|
| median | **0.757 ms** | ≤ 50 ms — PASS |
| p90 | 1.701 ms | — |
| p95 | **1.880 ms** | ≤ 200 ms — PASS |
| max | 2.165 ms | — |

Enforcement costs roughly **0.004%** of generation time (0.76 ms against a 17.3 s median). The
contract is free at production scale.

## Same-Config Retry

Run only after the 72-item first pass was complete and frozen; the script refuses to start
otherwise, and re-asserts that the retry prompt hashes identically to attempt 1.

| Query | Byte-identical | contract_valid on retry | Reasons on retry |
|---|---|---|---|
| GEV018 | **yes** | false | answer_body_language_mismatch |
| GEV042 | **yes** | false | malformed_citation |
| GEV061 | **yes** | false | wrong_abstention_marker_language |
| GEV062 | **yes** | false | wrong_abstention_marker_language, answer_body_language_mismatch |

**same_config_retry_recovery_rate = 0.0000 (0/4).**

## Retry Determinism

All four failures reproduced **byte-identically**. Same-config retry is therefore useless for this
failure class: it cannot recover anything, and would only add a full generation's latency to every
rejected request.

One honest caveat on determinism generally. Comparing this run against Phase B v2 under identical
configuration, **71 of 72** answers are byte-identical — but **GEV005 is not**. It changed from a
bulleted list to a single prose paragraph with the same substance, and remained contract-valid. So
temperature-0 MLX generation is *near*-deterministic, not guaranteed byte-identical across runs.
That variation exists, it did not touch any failing item, and it is not a basis for expecting
retry to help.

## Production Retry Policy

**Recommendation: C — `controlled_retry_requires_separate_experiment`.**

Same-config retry is measured, not assumed, to recover 0/4, so option B
(`reject_plus_same_config_retry`) is ruled out: never spend production latency on it. Option A
(`reject_only`) is the correct *interim* production behaviour and should be what ships today. But
A alone cannot reach the 0.95 gate, because the rejections are deterministic — the same requests
would fail forever. Any real improvement needs a controlled retry under deliberately changed
sampling (different seed, or bounded stochastic retry) evaluated as its own experiment, with the
prompt and the contract both untouched. That experiment is **not** implemented here, per the task's
explicit instruction.

## Known Limitations

- **The body-language detector cannot see proper nouns.** It is the direct cause of both gate
  failures. Any answer legitimately naming Turkish organisations, places or people while answering
  in English is at risk; the Eurasia Tunnel case is not exotic for this corpus.
- **Glyph weighting is aggressive.** A 2.0 weight per Turkish glyph, capped only at token count,
  lets a handful of characters outvote a paragraph of function words.
- **n=4 rejections.** Every rate over the rejected set — the false-positive rate above all — has a
  denominator of four. 0.25 means "one of four", and one adjudication either way moves it by 0.25.
- **Claim segmentation is not frozen.** 858 claims here vs 816 in Phase B v2 from the same answers.
  Coverage and precision denominators shift with segmentation, which is exactly why coverage
  remains telemetry.
- **Carried manual labels** cover 361 claims. They are gated on byte-identical answers and exact
  claim strings, but they were adjudicated in a previous phase.
- **Query acceptability** is inherited from Phase B v2's adjudication for the 71 unchanged answers.
- **Numeric "required fact"** has no frozen extraction rule; two defensible readings give 0.9375
  and 1.0000. Both are reported.
- **Generation is not byte-reproducible** (71/72), so a future re-run may differ marginally.

## Frozen Integrity

Unchanged and verified by test: Benchmark v1 and v2, both packet artifacts, system prompts v1–v5,
retriever v1, context v1, all contracts, citation-validator-v1.2, and the Output Contract v1
implementation. No prompt v6 exists — asserted by test. Qdrant 5992 before, 5992 after, 0 writes,
status green. `generation_candidate_v1.json` was **not** upgraded.

Full suite: **985 tests pass** (37 skipped), including 44 new tests for this phase.

## Final Production-Stack Decision

**Raw generator v5: NEEDS IMPROVEMENT.** Unchanged. Grounding is not the problem and never was.

**Output Contract v1: still sound in principle, but carries one real bug.** It caught every genuine
defect with zero false negatives and zero catastrophic passes, at 0.76 ms median. Its no-repair
policy was vindicated by GEV062. But its language detector violates its own §8 requirement to
ignore proper nouns, and that single defect is what fails this phase.

**V5 + Output Contract v1 stack: NEEDS IMPROVEMENT — NO-GO for production.**

The smallest next experiment is narrow and obvious: **fix the body-language guard's proper-noun
handling in a new Output Contract v1.1, then re-run this exact evaluation.** Nothing else needs to
change — not the prompt, not the benchmark, not the packets, not the generator. If GEV018 then
passes and nothing regresses, the arithmetic already computed here gives 0.9583 accept rate and a
0.0000 false-positive rate, and every other gate is already passing. That is the single highest-value
change available, and it is a change to the *contract*, not to the model.
