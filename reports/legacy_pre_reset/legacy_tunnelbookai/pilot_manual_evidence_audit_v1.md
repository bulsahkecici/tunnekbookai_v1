# Pilot Manual Evidence Audit v1

## Executive Decision

**PILOT MANUAL EVIDENCE AUDIT V1 — CLOSED / GO**

All **159 of 159** pilot evidence notes were read against their evidence and adjudicated at clause
level: **249 material clauses, every one resolved**. Zero generation calls, zero retrieval calls,
Qdrant unchanged at 5992 with 0 writes.

The audit changed the picture substantially. Of 68 notes v1 called SUPPORTED, **54 were downgraded**;
6 were upgraded from INSUFFICIENT_EVIDENCE. All three pilot sections are now **NOT_READY**, where v1
reported two as READY_WITH_LIMITATIONS.

The gate is GO because the *audit* is complete and correct, not because the sections are ready.

## Why This Gate Was Reopened

The architecture report carried the label `BOOK-WRITING PIPELINE ARCHITECTURE V1 — CLOSED / GO`
while its own text stated that 35 of 159 notes had been read and 124 were "verified programmatically
on all checkable properties, not read individually". The frozen gate required **all** pilot notes
manually audited. The label therefore overclaimed what had been done, and this task completes it.

## Frozen Inputs

Nothing was generated or retrieved. The evidence universe was reconstructed from frozen artifacts:

- **Packet-local identity** from `data/production/generation_audit_v1.jsonl`. Context v1 assigns
  `E001..E0nn` in selection order and the production audit records that order as
  `retrieved_chunk_ids`, so `<packet_sha>::E00k` resolves to `retrieved_chunk_ids[k-1]` with no
  guessing. **All 230 evidence refs resolved; 0 mismatches.**
- **Chunk text** from frozen `data/chunks/chunks.jsonl` and `data/chunks_recovery/chunks.jsonl`.
  All 68 cited chunks resolved.

Audit code contains no `urlopen`, `requests.`, `RetrieverV1(` or `gen.complete` — asserted by test.

## Manual Audit Scope

Every note was read with its claim, its clauses, its existing spans, its cited evidence text, its
numeric facts and its modality. Automation was assistive only — clause segmentation, candidate-span
search, numeric-presence checks — and every final flag is recorded as
`audit_method = manual_evidence_read`. A test asserts no row carries `deterministic_verified`.

Where reading contradicted the mechanical outcome, an explicit override is recorded in the audit
implementation: **9 note-level overrides** and **1 manual clause split**, each with a written reason.

## 159/159 Completion

`data/book/audits/pilot_evidence_note_manual_audit_v1.jsonl` — exactly 159 rows, all with
`manual_audit_completed = true`. Note ids match the original set exactly.

## Clause-Level Method

Claims were split into independently truth-evaluable propositions on strong separators (semicolons,
contrastive connectives, colon-plus-enumeration) rather than every grammatical phrase, because
over-splitting manufactures clauses no source was asked to support.

A clause is SUPPORTED when a verbatim span from the cited evidence covers ≥50% of its content
tokens **and** every material number in it occurs in that evidence; PARTIALLY_SUPPORTED at ≥25%;
UNSUPPORTED otherwise. A note is SUPPORTED only when **every** material clause is SUPPORTED.

## Clause Audit Results

`pilot_clause_support_audit_v1.jsonl` — **249 clauses**, all resolved:

| Status | Count |
|---|---|
| SUPPORTED | 43 |
| PARTIALLY_SUPPORTED | 49 |
| UNSUPPORTED | 157 |

No clause carries UNKNOWN, UNVERIFIED or UNREVIEWED — asserted by test.

## Literal Span Review

Every pre-existing span was re-verified to occur in its cited evidence: **159/159 pass**. Occurrence
was then checked separately against whether the span *supports the claim* — the distinction that
produced the downgrades.

Of the 73 notes awaiting span work, the audit disposed of them as: spans locatable and attached
(6 upgrades), paraphrase/synthesis with no locatable span (**81 → needs_manual_span**), cross-lingual
(**11 → attach_cross_lingual_mapping**), and non-propositional fragments (**28 → narrow_claim**).

## Cross-Lingual Support

**11 notes** are Turkish claims over English evidence. None was upgraded on lexical grounds: a
Turkish claim cannot have a literal Turkish span in an English source, and no Turkish quote was
fabricated. They are recorded `cross_lingual_support = true` with action
`attach_cross_lingual_mapping`, requiring a manual faithful-mapping decision before use.

## Numeric Audit

Every numeric fact was checked value-by-value against cited evidence. **Two numeric defects
confirmed**, both correctly kept out of SUPPORTED:

- **Q-02-2-01-N04** — asserts a *360 kg/m³ maximum* and a *400 kg/m³* figure; **neither value occurs
  in cited E001/E003**. This is the same defect class Phase B v2 recorded for GEV040.
- **Q-02-2-04-N06** — asserts "15 cm'yi (150 mm)"; **150 does not occur in the cited evidence**. The
  mm conversion was introduced by the generator.

A test asserts no SUPPORTED note carries a numeric defect. Ranges were preserved as ranges;
no minimum was converted to typical, and no range collapsed to its endpoint.

## Requirement / Modality Audit

**0 modality violations.** Every requirement/recommendation note's modality survives into its claim
text and matches source strength. No `should` became `must`, no `recommended` became `required`.

## Conditions / Exceptions

Conditions, qualifiers and exceptions were checked per note. The dominant failure is not a dropped
condition but a **dropped clause** — a compound claim where the cited span carries one proposition
and the others ride along uncredited.

## Conflict Search Method

A real search was performed, over the **full evidence universe of the 19 frozen packets — 377
evidence items across 253 distinct chunks** — not merely the 68 cited chunks. Candidates were
generated deterministically: the same variable carrying different numeric values under the same unit
across different documents.

## Conflict Results

**30 candidates, all manually classified**: 29 `NOT_CONFLICT`, 1 `CONTEXT_DIFFERENCE`,
**0 `TRUE_CONFLICT`**.

The honest finding is about the detector, not the corpus: keyword bucketing grouped *distinct
measured quantities* — steel-mesh gap, aggregate size distribution, specific surface area, strap
width — under one "variable". Reading the sampled contexts rejected them. The single
`CONTEXT_DIFFERENCE` is the shotcrete single-layer maximum thickness, where differing values
describe different application contexts rather than contradicting each other under equal conditions.

Zero true conflicts is now a searched result rather than an unexamined default — but it is a weak
result, because a coarse detector that produces mostly false candidates may also miss real ones.

## Duplicate Claim Review

The original report's "4 duplicate candidate pairs" was **4 ledger entries carrying a candidate,
i.e. 2 distinct pairs** (each pair counted from both sides). Both pairs were manually adjudicated:
**1 `confirmed_duplicate`, 1 `related_not_duplicate`**. All reviewed, recorded in
`pilot_duplicate_claim_audit_v1.jsonl`.

## Evidence Note Revisions

| Metric | Count |
|---|---|
| Status changes | 60 |
| Downgraded from SUPPORTED | **54** |
| Upgraded from INSUFFICIENT_EVIDENCE | 6 |
| Audited notes emitted | 30 |
| — SUPPORTED | 15 |
| — PARTIALLY_SUPPORTED | 15 |
| Recommended INSUFFICIENT_EVIDENCE | 129 |
| Actions: needs_manual_span / narrow_claim / retain_supported / split_note / cross-lingual / retain_insufficient / downgrade | 81 / 28 / 15 / 14 / 11 / 9 / 1 |

No original artifact was modified. Audited revisions live in `evidence_notes_audited/`,
`claim_ledgers_audited/` and `section_bundles_audited/`, each with `parent_note_id`, `revision = 1`
and a deterministic `audited_note_sha`.

**No Evidence Note Contract v1.1 was created.** Contract v1 expressed every audited revision, so the
narrowly-additive validator permitted by the spec was not needed.

## SEC-02-1

**NOT_READY.** P0 question `Q-02-1-02` has no SUPPORTED audited note. 12 audited notes
(10 SUPPORTED, 2 PARTIALLY_SUPPORTED), 10 citation-ready.

Six notes were bare enumeration labels — "Püskürtme Beton", "Çelik İksa", "Temel Kiriş Betonu",
"Şemsiye Kemer Uygulaması" — and **three of them carried SUPPORTED/high in v1**. They assert nothing
on their own; the proposition ("X is a primary support element") lives in the parent lead-in. All
were downgraded with action `narrow_claim`.

Root cause: the v1 extractor's materiality test accepts any unit containing a digit, and citation
handles contain digits — so `* Püskürtme Beton [E001]` passed as material on the "001". The v1
pipeline is frozen, so this is recorded as a defect for a future pipeline revision, not patched here.

## Q-02-1-06-N06

The known compound-claim defect, confirmed and decomposed. The claim asserts three propositions:

| Clause | Verdict |
|---|---|
| …tünelin duraylılığını sağlamak açısından gereklidir | **UNSUPPORTED** — no span in cited E003 carries it |
| …su geçirimsizliğini temin etmek açısından gereklidir | **UNSUPPORTED** — no span in cited E003 carries it |
| …işletme ekonomisi (sürtünmenin azalması) açısından gereklidir | **SUPPORTED** — span carries it verbatim |

Recommended: `PARTIALLY_SUPPORTED`, action **`split_note`**. This required a manual clause split,
because automatic segmentation kept the three propositions in one clause and would have hidden the
gap inside it.

## SEC-02-2

**NOT_READY.** P0 question `Q-02-2-02` has no SUPPORTED audited note. Only 3 audited notes survive
(2 SUPPORTED, 1 PARTIALLY_SUPPORTED), 2 citation-ready — the sharpest drop of the three sections,
and the numeric section, which is where partial numeric coverage bites hardest. Both confirmed
numeric defects are here.

## SEC-02-3

**NOT_READY.** Two P0 questions now lack SUPPORTED notes — `Q-02-3-01` (already known) **and
`Q-02-3-02`**, newly exposed by clause-level audit. 15 audited notes, but only 3 SUPPORTED against
12 PARTIALLY_SUPPORTED.

Manual review of `Q-02-3-01` confirms the gap is **real, not an artefact**: its answer is Turkish
prose synthesised from English sources, and no clause reaches the support threshold in the source
language. Readiness was not forced.

## Audited Claim Ledgers

Rebuilt from audited notes only. Ledger entries are created **exclusively from SUPPORTED audited
notes** — nothing INSUFFICIENT_EVIDENCE, REJECTED or conflict-blocked contributes a citation-ready
claim. Every entry carries resolved source keys.

## Recomputed Section Readiness

| Section | v1 readiness | **Audited readiness** |
|---|---|---|
| SEC-02-1 | READY_WITH_LIMITATIONS | **NOT_READY** |
| SEC-02-2 | READY_WITH_LIMITATIONS | **NOT_READY** |
| SEC-02-3 | NOT_READY | **NOT_READY** |

Readiness was recomputed from audited evidence, not inherited.

## Remaining Gaps

- **81 notes need manual literal-span attachment** and **11 need cross-lingual mapping** before they
  can support anything.
- **28 non-propositional fragments** must be restated as propositions or dropped; restating them is
  authoring, deliberately not done here.
- **The conflict detector is coarse** — 29 of 30 candidates were false. Absence of true conflicts is
  weakly evidenced.
- **The v1 extractor's materiality bug** (digits inside citation handles) is recorded, not fixed.
- **Clause coverage thresholds (0.50 / 0.25) are a judgement**, calibrated during the read.
- **No prose has been produced or evaluated.**

## Frozen Integrity

Unchanged and asserted by test: Prompt v5 (`9bae1362…4085`), Output Contract v1.1
(`5ebf8fe9…def5`), Evidence Note Contract v1, Book Pipeline v1, Retriever v1, Context v1,
Production Generator v1, all original pilot artifacts, corpus, chunks, embeddings.

Generation calls **0**, retrieval calls **0**, Qdrant **5992 → 5992, 0 writes**.
`drafting_enabled` remains **false**.

## Tests

`tests/test_pilot_manual_evidence_audit.py` — **27 tests, all passing**: population completeness,
manual method on every row, clause resolution, status consistency (no compound partial marked fully
supported), numeric defect identification, modality preservation, packet-local identity, provenance,
deterministic audited-note hashing, conflict search performed and every candidate classified, all
duplicates reviewed, original immutability, no generation/retrieval, drafting disabled.

## Final Decision

**PILOT MANUAL EVIDENCE AUDIT V1 — CLOSED / GO.**

The audit is complete and its findings are unflattering to the previous phase, which is the point.
A full clause-level read cut demonstrably supported notes from 68 to 15, exposed a second unsupported
P0 question, confirmed two numeric claims asserting values absent from their evidence, and found
three SUPPORTED notes that were bare list labels asserting nothing.

**Formally, `BOOK-WRITING PIPELINE ARCHITECTURE V1` may now be recorded as CLOSED / GO** — its gate
required this audit, and the audit is done. But the pilot's evidence yield is much lower than v1
implied, and **no section is ready to draft**.
