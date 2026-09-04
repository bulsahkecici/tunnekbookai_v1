# Generation Prompt v5 — Abstention Language Remediation

## Decision

**GENERATION PROMPT V5 LANGUAGE REMEDIATION — CLOSED / NO-GO.**

The gate requires **zero** wrong-language abstention markers. v5 reduced them from **6 to 1** — the
English direction is fully fixed (0/6 → 6/6 correct) — but one Turkish case still opens with the
English marker. One residual failure is not zero, so this does not pass as specified.

Everything else held: 0 malformed citations, 0 unknown handles, 0 coordinate or template leaks,
marker-at-start 9/9, no citation-coverage regression, no control regression.

## Dev Item Count

`data/evaluation/generation_language_dev_regression_v1.jsonl` — **14 items**, all labelled
`dataset_role: development_regression`.

- **3 diagnostics** reusing the frozen packets of DEV002 / DEV011 / DEV016 (the v4 failures).
- **11 independent** queries with freshly assembled packets.
- **6 answerable controls** (3 TR, 3 EN) to catch the rule causing needless abstention.
- Mixed-language cases in both directions: EN question over Turkish-dominant evidence
  (LNG013: 10 tr / 10 en) and TR question over English-dominant evidence (LNG014: 18 en / 2 tr).

Abstention split as executed: **6 English**, **3 Turkish** (9 of 14 items abstained under both prompts).

## Results

| | v4 baseline | v5 |
|---|---|---|
| English abstention marker accuracy | **0/6 = 0.000** | **6/6 = 1.000** |
| Turkish abstention marker accuracy | 3/3 = 1.000 | **2/3 = 0.667** |
| Wrong-language markers | **6** | **1** (LNG006) |
| marker_at_start | 9/9 | 9/9 |
| Malformed citations | 0 | **0** |
| Unknown handles | 0 | **0** |
| Coordinate / template leaks | 0 | **0** |
| Citation coverage | 56/65 = 0.8615 | 62/72 = 0.8611 |
| Unexpected abstention on controls | LNG013 | LNG013 (unchanged) |
| Prompt token delta | 0 | 0 |

v4 reproduced the bug decisively: **every** English abstention opened with `YETERSİZ KANIT`. v5
corrected all six, including LNG013, whose English abstention had a Turkish-dominant packet — so the
marker is now following the question, not the evidence, in that direction.

## The Residual Failure

**LNG006** — "Bolu Dağı Tüneli'nde 2026 yılında kaç adet jet fan yenilenmiştir?" — a Turkish
question over an entirely Turkish packet (20/20 tr). v5 opens with `INSUFFICIENT EVIDENCE` and then
writes the **whole body in Turkish**. The marker is decoupled from the answer language the model
otherwise gets right, and the evidence language cannot explain it: there is no English evidence here.

## Drafting History

Three v5 drafts were run. The residual failure is **migratory**, the same pattern seen in v1→v2→v3
and in the v4 remediation.

| Draft | Change | Wrong markers | Malformed | Tokens |
|---|---|---|---|---|
| v4 baseline | — | 6 (all EN) | 0 | 739 |
| **v5 draft 1 (frozen)** | marker chosen only by question language | **1** (LNG006) | **0** | **789** |
| v5 draft 2 (discarded) | marker anchored to the answer body's language | 1 (LNG006) | 1 | 814 |
| v5 draft 3 (discarded) | explicit "a Turkish answer must never open with INSUFFICIENT EVIDENCE" | 1 (LNG008) | 1 | 841 |

Draft 2 restated the rule in terms of the answer's own language and did not move LNG006, while
introducing a malformed citation. Draft 3 fixed LNG006 and the failure jumped to LNG008 — a
different Turkish item — and also cost a malformed citation. The wrong-marker count stayed pinned at
exactly 1 of 8–9 abstentions in every draft while the failing item moved.

**Draft 1 is frozen as v5** because it is strictly best: same single wrong marker, but zero malformed
citations, so it preserves the v4 citation gains intact. Drafts 2 and 3 were discarded, and v5's
file was reconstructed deterministically from frozen v4 and verified to hash back to draft 1's
`9bae1362…396e4085` before its results were retained.

I stopped after three attempts rather than continue: with 14 dev items and a binary marker choice,
further example-chasing would fit the set rather than the behaviour.

## System Prompt v5

`data/metadata/generation_system_prompt_v5.txt`, SHA `9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085`,
registered in the version-aware loader (fails closed on unknown version, missing file, SHA mismatch).

| Prompt | Tokens |
|---|---|
| v3 | 514 |
| v4 | 739 |
| **v5** | **789** (+50) |

v5 is a narrow delta on v4. Every v4 rule is retained verbatim — `[Eddd]`-only grammar, the
talk-about-it-still-brackets rule, per-claim citation coverage, the non-factual exemption, untrusted
evidence, conflicts, coordinate prohibition, no chain-of-thought. Two changes only:

1. The abstention marker is chosen **only by the question's language**, stated as an explicit
   mapping, with "the language of the evidence never affects this choice, even when every source is
   in the other language."
2. The existing pre-output self-check gained a third item: the opening marker matches the question's
   language.

## Contracts Preserved

- **Citation syntax** — 0 malformed across all 14 items, unchanged from v4.
- **Grounding** — 0 unknown handles, 0 coordinate leaks, 0 template leaks.
- **Coverage** — 0.8615 → 0.8611, flat; no regression.
- **Controls** — the five controls v4 answered, v5 also answered. LNG013 abstains under **both**
  prompts, so it is not a v5 regression. I did not verify whether its packet actually supports an
  answer, so I am not calling it an over-abstention — it is an unverified authored expectation.
- **Validator** — `citation-validator-v1.2` untouched. No marker was ever post-processed; the
  expected marker is derived from the query language alone and compared to what the model emitted.

## Frozen Integrity

Unchanged: benchmark v1 `de3c1684…` and its manifest, the 72 frozen packets, Retriever v1
`8ada31f6…`, Context v1 `4bcf5c99…`, contracts, prompts v1 `303691ec…` / v2 `0063b9bc…` /
v3 `d3cadd46…` / v4 `5950baff…`, validator semantics, chunks, embeddings, corpus.

Qdrant `tunnelbook_dense_v1`: **5992 → 5992, 0 writes**, green.

Tests: **847 in `tests/` + 16 in `rapor/tests/` = 863, all passing** (37 skipped, live-gated),
including v1–v4 SHA immutability, the v5 SHA and loader, v4≠v5 config hash, v4 checkpoint rejected
under v5, marker derivation for both languages, evidence language not controlling the marker,
marker-at-start, and validator immutability. One test deliberately pins the residual failure set to
`["LNG006"]` so a silent change in what still fails cannot pass unnoticed.

## Not Promoted

v5 remains a **development prompt**. The candidate descriptor still pins
`generation-system-prompt-v3` with status `runtime_contract_closed_benchmark_pending`, and a test
asserts v4/v5 are absent from its prompt history. No quality, benchmark-improvement or
generalisation claim is made from these 14 items.

## Recommended Next Step

The English direction is solved by prompt alone; the Turkish direction has resisted three distinct
phrasings while the answer body language stays correct throughout. That asymmetry suggests the
marker token choice is not reliably steerable by instruction for this model, and the smallest honest
next experiment is **not** a v6 rewrite. Options, cheapest first:

1. Carry the residual into benchmark v2 measurement and quantify it on fresh holdout data before
   spending more prompt budget — 1 in 8 abstentions on 14 dev items is a weak estimate.
2. If it persists at scale, treat marker emission as a constrained-decoding or output-contract
   concern rather than a prompt concern. That sits outside prompt scope and was not implemented here.

Benchmark v2 must still correct the four recorded v1 defects (GEV058, GEV042, GEV045, GEV051), and
the Phase B claim-audit gap of **175 `UNVERIFIED_BY_RULE`** claims remains open and is not
retroactively resolved.
