# Generation Eval Benchmark v2

## Decision

**GENERATION EVAL BENCHMARK V2 — CLOSED / GO**

72 items, frozen. Benchmark SHA `1e6347b557d583b56882c4c05fd1c5453874b7a05e61205c9430a24a677b0cff`,
packets SHA `0538705147cf543b45fe8e73d57828cbc341a9a5a1dd574bd0969a9326e54d7a`.
Generation calls during authoring: **0**.

## Why v2 Exists

Phase B exposed two separate problems with v1. Four items had **authoring defects** — gold that did
not match its own query, gold that excluded equally valid packet-supported answers, and one item
labelled unanswerable when the packet did support an answer. Separately, several v1 items were read
in detail while developing prompts v4 and v5, which means their failure modes directly shaped the
prompt. Those items can still serve as historical evidence but can no longer serve as holdout.

v1 is untouched and remains the historical record.

## Benchmark-v1 Defects

| v1 item | Defect |
|---|---|
| GEV042 | gold asked for specimen dimensions while the query asked for sample count and age |
| GEV045 | gold fixed one numeric path (1–6 m/day) while the packet also supports 15–30 m/day ARAr, 9.49/29.4 m and 4.2 m/day |
| GEV051 | gold used lay-by spacing and gradient, which are not escape-route properties |
| GEV058 | gold labelled the item unanswerable/retrieval-limited although E007 carries substantive alignment material |

**A fifth defect was found during this audit.** GEV063 asked for the Gotthard Base Tunnel's total
construction cost and was labelled unanswerable, but its packet contains
"Gotthard Base Tüneli **11,3 milyar $** bütçeli". The v1 probe missed it because the figure is
written in Turkish while the probe searched English cost terms — the same single-language mistake
that produced the GEV058 defect. GEV063 was therefore replaced as well.

## Contamination Policy

An item is contaminated once its content influenced prompt development. Removed on that basis:
GEV061, GEV064, GEV070 (malformed-citation diagnostics reused in `generation_dev_regression_v1`) and
GEV065, GEV066 (wrong-language-marker cases inspected during the v5 work).

Every v2 item carries `contamination_status`, and all 72 are `clean_holdout`.

## Items Replaced

**10 replaced, 62 carried forward.**

| v1 item | Category | Reason | Fresh query focus |
|---|---|---|---|
| GEV042 | numeric_table | gold_query_mismatch | advance length by rock class (TR) |
| GEV045 | numeric_table | gold_excluded_valid_alternative_values | cast-in-place final lining thickness (EN) |
| GEV051 | regulation_specification | gold_did_not_answer_requested_property | ADR dangerous-goods requirements (EN) |
| GEV058 | cross_lingual | gold_mislabelled_unanswerable | shotcrete measurement and payment in Turkish contracts (EN → TR evidence) |
| GEV061 | must_abstain | development_exposed | 2022 national maintenance length (TR) |
| GEV063 | must_abstain | hidden_packet_support_found_in_v2_audit | fire-incident count 2015–2020 (EN) |
| GEV064 | must_abstain | development_exposed | Bolu 2022 vehicle count (EN) |
| GEV065 | must_abstain | development_exposed | 2021 national tunnel length completed (EN) |
| GEV066 | must_abstain | development_exposed | shotcrete unit price per m³ in 2024 (EN) |
| GEV070 | injection_adversarial | development_exposed | post-blast sequencing (TR) |

Replacements preserve both the primary category and the language of the item they replace
(3 TR / 7 EN), so the distribution and the 36/36 balance are unchanged.

## Fresh Holdout Construction

Each replacement followed the mandatory order: finalize query → run frozen Retriever v1
(`retrieval_top_k = 20`) → assemble ContextPacket v1 with the real generation tokenizer → freeze
packet and SHA → **only then** author gold.

Two candidates were discarded and re-drafted after their packets were read, before any gold existed:

- The first R045 query asked for concrete cover over reinforcement; the packet contained lining
  thickness, membrane thickness and strengths but no cover value. Replaced with cast-in-place lining
  thickness, which the packet supports with two distinct values.
- The first two R058 candidates returned English-dominant answering evidence, which would have made
  the cross-lingual label false. The third — shotcrete measurement and payment in Turkish contracts —
  returns Turkish answering evidence (DOC000227, DOC000214) for an English question.

## Distribution

18 direct_factual_conceptual · 10 design_construction · 10 multi_source_synthesis · 8 numeric_table ·
6 regulation_specification · 6 cross_lingual · 8 must_abstain · 6 injection_adversarial = **72**.

## Language Balance

**36 Turkish / 36 English**, exact.

## Answerability

62 answerable · 2 partially_answerable · 8 unanswerable. The count of unanswerable items now equals
the must_abstain category exactly (v1 had nine because GEV058 was mislabelled).

Difficulty: 8 easy · 36 medium · 28 hard.

## Must-Abstain Audit

All 8 carry `manual_packet_absence_verified: true` and a written `absence_audit_note`. Each was
audited in **both languages** and by reading, not only by grep:

- **R061** — every probe (2022, bakım+kilometre, toplam bakım, maintenance+km) returned zero.
- **R063** — fire+count coupling returned only a Swedish report title and a Norwegian incident.
- **R064** — AADT tables for Bolu exist but from an earlier study; no 2022 vehicle count.
- **R065** — E020 was read in full: the 21,473 m figure is an Antalya-region statement with no year,
  not a national 2021 total.
- **R066** — "Birim Fiyat" appears 16 times as a payment *definition*; no monetary value, nothing dated 2024.
- Carried **GEV059** (per-km 2010 figure, not a 2024 total), **GEV060** and **GEV062** were re-audited
  with entity+quantity coupling in both languages; GEV060 and GEV062 returned zero couplings.

## Numeric Alternatives

The v1 weakness was gold that fixed one arbitrary numeric path. v2 records
`alternative_valid_values` with exact spans:

- **GEV042** — 3 m (RMR I, full face) with alternatives 1–1,5 m (RMR II) and 2–2,5 m (top heading).
- **GEV045** — 12 inches (two-lane road tunnels) with alternative 10 inches (practical minimum).
- **GEV058** — 5 cm (A1/A2/B1 ground) with alternatives 7,5 cm (B2/B3) and 10 cm (C1/C2/C3).

Claim-level `acceptable_alternatives` is likewise populated on the fresh items, so a future model
that picks a different packet-supported value is not scored wrong for disagreeing with the author.

## Cross-Lingual Audit

GEV058's replacement is verified by reading, not by chunk metadata: the packet is 10 tr / 10 en, and
the two evidence items that carry the answer are Turkish (42 and 54 Turkish-specific glyphs in their
opening text) against an English question. `cross_lingual_metadata` records query language, dominant
evidence language, direction, full language counts and `manually_verified: true`.

## Retrieval-Limited Audit

Exactly one item, **GEV018**, and it is no longer an inference. A full-corpus scan outside the frozen
packet found `DOC000194-C0007`: "Avrasya Tüneli Projesi'nin toplam maliyeti 1 milyar 250 milyon".
The packet itself has no price, so the label is correct and now carries positive evidence
(`retrieval_limited_evidence` with chunk id, document id and quote). No other item claims the label.

## Gold Contract

Every claim records `claim_id`, `claim_text`, `claim_type`, `required`, `support_status`,
`supporting_evidence_ids` and `acceptable_alternatives`. Every support record carries
`evidence_id`, `literal_span`, `span_start`, `span_end`, `span_scope` and the evidence
`text_sha256`. Gold answer summaries state minimal expected content and permitted alternatives
rather than a single polished prose answer.

## Literal-Span Audit

All spans use `span_scope: evidence_item` — one coordinate system, never mixed. Every span,
including every alternative-value span, is asserted as
`evidence_text[span_start:span_end] == literal_span`. No gold span is reused across items; the
build tripped this gate once (R051's Austrian 500 m clause collided with carried GEV050) and R051's
gold was narrowed to ADR evidence rather than relaxing the check.

## Manual 72/72 Audit

Every item carries `manual_item_audit` with `reviewed`, `answerability_verified`, `spans_verified`,
and `packet_read` for the unanswerable items. The 10 fresh items were read end to end during gold
authoring; the 8 must-abstain packets were read specifically to certify absence.

## Source Diversity

40 unique source documents; 116 unique evidence chunks; max chunk reuse 3.

Items per document (top 6): `DOC000047` 22 · `DOC000087` 7 · `DOC000015` 7 · `DOC000003` 7 ·
`DOC000236` 6 · `DOC000124` 4.

The FHWA manual still supplies gold for 22 of 72 items (31%, up from 21 in v1 because R045 draws on
it). No quota was imposed; the concentration is reported rather than engineered away.

## Duplicate and Contamination Audit

- No duplicate query text across the 72.
- No replacement reuses its v1 query or v1 packet SHA.
- No item reuses a query or packet SHA from `generation_dev_regression_v1` or
  `generation_language_dev_regression_v1` — asserted by test, with a guard that fails if the
  development sets are missing so the check can never pass vacuously.
- No gold span appears in two items.

## Frozen Identities

Retriever `tunnelbook-retriever-v1` `8ada31f6…`, Context `tunnelbook-context-v1` `4bcf5c99…`,
`retrieval_top_k = 20`, validator `citation-validator-v1.2`.

Authoring was generator-independent: `authoring_system_prompt_identity` is null and
`generation_calls` is 0. The manifest records `generation-system-prompt-v5` only as the *intended
next* candidate, with `intended_candidate_not_used_in_authoring: true` — no question or gold was
tailored to it.

Unchanged: benchmark v1 `de3c1684…` and its packets, prompts v1–v5, contracts, chunks, embeddings,
corpus. Qdrant `tunnelbook_dense_v1`: **5992 → 5992, 0 writes**, green.

Tests: **875 in `tests/` + 16 in `rapor/tests/` = 891, all passing** (37 skipped, live-gated),
including 28 new v2 tests.

## Known Limitations

- **Alternatives are populated only on the 10 fresh items.** The `acceptable_alternatives` field
  exists on all 72 claims, but the 62 carried items were not re-audited for alternative valid answer
  paths. Some of them likely admit alternatives that are still unrecorded, so gold-claim recall on
  carried items remains a stricter measure than on fresh ones. This is the largest remaining gap.
- **Source concentration**: 22 of 72 items draw gold from `DOC000047`.
- **Evidence overlap between two fresh items**: R058 and R066 both draw on the shotcrete
  payment chunks (`DOC000227`, `DOC000214`). Their gold is disjoint — measurement rules versus the
  absence of a price — and no span is shared, but the packets overlap.
- **Turkish OCR artefacts** persist in some spans; they are exact to the frozen evidence, which is
  the contract, but string-equality scoring against cleaned text would misfire.
- **Carried packets are unchanged**, so any latent defect in the 62 that Phase B did not surface is
  still present. v2 corrects what was found, not what was never tested.
- **Phase B claim-audit gap is still open**: 175 of 825 claim rows remain `UNVERIFIED_BY_RULE` and
  are not retroactively resolved here. Phase B v2 must drive every material claim to a resolved,
  evidence-backed label.

## Final Decision

**GENERATION EVAL BENCHMARK V2 — CLOSED / GO**

Next: **GENERATION PHASE B V2 — FRESH HOLDOUT EXECUTION + COMPLETE CLAIM-LEVEL AUDIT**
