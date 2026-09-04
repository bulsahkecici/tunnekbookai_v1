# Generation Prompt v4 Remediation

## Decision

**GENERATION PROMPT V4 REMEDIATION — CLOSED / GO** (development scope only.)

Both Phase B citation-adherence failures close on the development regression set: malformed
citations **6 → 0**, per-claim citation coverage **0.840 → 0.936**. No grounding, abstention,
numeric or injection regression. Benchmark v1 untouched, Qdrant 5992 with 0 writes.

**This is a development result and nothing more.** Three v4 drafts were iterated against this set,
so the set can no longer speak to generalisation. Confirmation belongs to a fresh holdout
(benchmark v2). v4 has **not** been promoted: the candidate descriptor still pins v3.

## Scope

Built a development regression suite, wrote system prompt v4, ran v3 and v4 over the identical
packets, and scored the two failure modes. The frozen 72-query benchmark was **not** re-run,
benchmark v2 was not created, and Retriever v1, Context v1, the validator, and the model were all
left untouched.

## Development Regression Set

`data/evaluation/generation_dev_regression_v1.jsonl` — **16 items**, every row labelled
`dataset_role: development_regression`.

- **3 diagnostic** items reuse the exact frozen packets whose failures Phase B recorded
  (GEV061, GEV064, GEV070), so the suite can prove the failure reproduces before claiming it closed.
- **13 independent** items are fresh queries against the corpus with their own newly assembled
  packets — not clones of benchmark rows.

Shapes covered: Turkish suffixed bare handles in abstention prose, English "Evidence E003"
reference prose, multi-reference sentences, multi-level and continuation bullets, summary
statements, must-abstain explanations, adversarial/template evidence, numeric bullets, multi-source
synthesis, and a numeric-conflict case. Both languages; contexts 21k–39k tokens.

## System Prompt v4

`data/metadata/generation_system_prompt_v4.txt`, SHA `5950baff…17dba072`, registered in the
versioned loader (fails closed on unknown version, missing file, SHA mismatch). v1, v2 and v3 are
byte-identical to before.

v4 is v3 plus three narrow additions; the grounding policy, untrusted-evidence rule, abstention
contract, conflict preservation, language matching, coordinate ban, no-CoT rule and the `[Eddd]`
grammar are all unchanged.

1. **Bare references in prose** — the bracket rule holds when a sentence talks *about* an item, not
   only when citing it: "According to [E003]", never "Evidence E003"; "[E002] ve [E003]'te", never
   "E002 ve E003'te". There is no second grammar for referring to evidence.
2. **Per-claim coverage** — every sentence, bullet or table row asserting a material fact carries
   its own handle; a handle on a heading, a parent bullet or an earlier sentence does not cover what
   follows. Headings, transitions and the abstention marker assert nothing and need none.
3. **Pre-output self-check** — scan the answer once and bracket any bare E-number before emitting.

| Prompt | Tokens |
|---|---|
| v3 | 514 |
| v4 | **739** (+225, +44%) |

The growth is more than I wanted. Two-thirds of it is rules 1–2; the self-check block cost the rest
and is what finally closed the failure (below).

## Drafting History

Recorded because it is the most informative result here. The failure is **migratory**: each
example-based tweak fixed the item it targeted and the failure reappeared on a different item.

| Draft | Change | Malformed | Items | Coverage |
|---|---|---|---|---|
| v3 (baseline) | — | 6 | 4 | 0.840 |
| v4 draft 1 | rules 1 + 2 | 2 | 1 (DEV007) | 0.868 |
| v4 draft 2 | + bracket rule restated inside the abstention section | 2 | 1 (DEV003) | 0.935 |
| v4 final | + pre-output self-check | **0** | **0** | **0.936** |

Draft 1 fixed all four v3 failures and broke DEV007. Draft 2 fixed DEV007 and DEV003 broke. That is
the same relocation pattern as v1 (suffixes) → v2 (ranges) → v3 (prose references). Only the
structural change — a self-check over the finished answer rather than another example — reached
zero. I stopped there deliberately rather than continue chasing items, which would have overfitted
the development set.

## Results

| Metric | v3 | v4 |
|---|---|---|
| malformed citations (occurrences) | 6 | **0** |
| answers with malformed citations | 4 / 16 | **0 / 16** |
| citation coverage (per material claim) | 84/100 = **0.840** | 73/78 = **0.936** |
| unknown handles | 0 | 0 |
| coordinate / template leaks | 0 | 0 |
| prompt token delta | 0 | 0 |
| truncation | none | none |

Per-item malformed counts went 2/1/2/1 (DEV001, DEV002, DEV003, DEV006) under v3 to zero
everywhere. The v3 failures included a shape Phase B had not seen: DEV006 emitted `[E11]` —
bracketed but two digits — which the unchanged validator correctly rejected.

## Citation Coverage Audit

Coverage is measured **per claim**, not per paragraph: an answer is split at bullet / list-item /
paragraph granularity, each block that asserts a material fact is counted, and a block counts as
covered only if it contains a handle itself. A handle on the parent bullet never covers the child.
Headings, list lead-ins and the bare abstention marker are excluded as non-factual, so the score
measures material-claim coverage rather than rewarding mechanical handle-stuffing.

One confound worth stating: v4 answers are also more concise (78 material claims vs 100 under v3),
so coverage improved partly through denser writing, not only through more citations. Both effects
are real; neither is separable from this sample.

## Regression Checks

- **Abstention** — no regression. One change: DEV003 (= GEV070) stopped abstaining and answered.
  That is a **fix**, since Phase B recorded GEV070 as an unexpected abstention on an answerable item.
  All must-abstain-style items still abstain with the marker at the start.
- **Numeric** — no regression; numeric bullets remained cited and grounded.
- **Injection / template** — no regression; the template-evidence item (DEV015) still reports the
  form's headings as data and does not fill in the blanks.
- **Grounding** — zero unknown handles and zero coordinate or template leaks under both prompts.
- **Validator** — `citation-validator-v1.2` unchanged. No output was normalised into valid syntax;
  v4 had to satisfy the existing contract.

## Open Issue Not Addressed by v4

The **wrong-language abstention marker** persists: DEV002, DEV011 and DEV016 are English queries
that opened with `YETERSİZ KANIT` before continuing in English (Phase B saw the same on GEV064,
GEV065, GEV066). v4 did not target this and did not fix it. It is a marker-selection bug, not a
grounding or citation bug, and belongs in the next prompt iteration or in benchmark v2 scoring.

## Recorded, Not Repaired

**Benchmark v1 defects** (for benchmark v2, unchanged here):

- `GEV058` — labelled unanswerable/retrieval-limited, but E007 (`DOC000024`) contains substantive
  alignment material; the gold is wrong and the model's answer was grounded.
- `GEV042` — gold asked specimen dimensions while the query asked sample count and age.
- `GEV045` — gold selected different (also valid) advance-rate figures than the model used.
- `GEV051` — gold used lay-by and gradient numbers that are not escape-route requirements.

**Phase B claim-audit gap**: of 825 claim rows, **175 remain `UNVERIFIED_BY_RULE`** and are *not*
retroactively declared supported here. The next clean evaluation must drive every material claim to
a resolved, evidence-backed label rather than leaving unresolved ones.

## Frozen Integrity

Unchanged and verified: `generation_eval_benchmark_v1.jsonl` `de3c1684…`, its manifest, the 72
frozen packets, Retriever v1 `8ada31f6…`, Context v1 `4bcf5c99…`, both contracts, prompts v1
`303691ec…` / v2 `0063b9bc…` / v3 `d3cadd46…`, validator v1.2 semantics, chunks, embeddings, corpus.

Qdrant `tunnelbook_dense_v1`: **5992 → 5992, 0 writes**, green.

Test totals: **822 tests in `tests/` + 16 in `rapor/tests/` = 838, all passing** (37 skipped,
live-gated), including new tests for the v4 SHA and loader, v3≠v4 config hash and checkpoint
identity, every bare-versus-bracketed reference shape, bullet-level coverage, uncited continuation
bullets, and the non-factual heading exemption.

## Final Decision

**GENERATION PROMPT V4 REMEDIATION — CLOSED / GO** (development).

v4 remains a **development prompt**. The frozen candidate descriptor still pins v3, and no quality,
benchmark-improvement or generalisation claim is made from these 16 items. The next step is
benchmark v2 — correcting the four defects above and freezing a fresh holdout — on which v4 can be
evaluated honestly for the first time.
