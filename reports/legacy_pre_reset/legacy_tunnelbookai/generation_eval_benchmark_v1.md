# Generation Eval Benchmark v1

## Decision

**GENERATION EVAL BENCHMARK AUTHORING — CLOSED / GO**

72 items, frozen, SHA256 `de3c1684ad26b459e6a209a9ef770c1a0f0fae39b44d0d251bc492ca3f75bd6b`.
Generation calls to Qwen during authoring: **0**.

## Scope

This task authored and froze the evaluation benchmark only. It did not run the benchmark, inspect
any generator output, tune the system prompt, or touch Retriever v1, Context v1, the citation
validator or the generation runtime configuration. The first model execution belongs to Phase B.

## Frozen Runtime Dependencies

| Component | Identity |
|---|---|
| Retriever | `tunnelbook-retriever-v1`, SHA `8ada31f6…a231b071` |
| Context | `tunnelbook-context-v1`, SHA `4bcf5c99…f1a777991d` |
| Citation validator | `citation-validator-v1.2` |
| System prompt | `generation-system-prompt-v3`, SHA `d3cadd46…7526dc74` |
| Tokenizer / template | `87a7830d…3db72de4` / `e84f32a2…39574259` |
| Runtime context | 71936, authoring RAG budget 64610 |

**`retrieval_top_k = 20`, not 10.** The task specified 10 "unless an existing frozen production
default differs" — it does: `scripts/20_rag_context.py` sets `DEFAULT_RETRIEVAL_TOP_K = 20`. The
frozen production default was used and is recorded in every item's `retriever_config`.

## Authoring Method

The mandated ordering was followed for every item without exception:

1. write the query, 2. run Retriever v1, 3. assemble ContextPacket v1 with the real generation
tokenizer as `token_counter`, 4. freeze the packet text and SHA, 5. **only then** read the packet
and author gold.

Gold was never authored first and then justified. 111 candidate queries were drafted and their
packets assembled; 72 survived inspection. Candidates were dropped for measured reasons, not taste:
`MS06` (its packet did not discuss water-inflow effects), `CL04` (retrieved drainage material for a
segmental-lining question), `CL10`/`CL11` (answering evidence was in the query's own language, so
the cross-lingual label would have been false), `NT06`/`NT08`/`NT11` (no usable numeric fact in the
packet). Two replacement queries (`MS15`, `CL12`) were drafted and put through the same pipeline.

**No LLM produced any gold.** Claims were written by reading the frozen evidence. To guarantee span
exactness without transcription error, each claim names a phrase copied from the evidence while
reading; the builder re-locates that phrase in the **original** evidence text (whitespace-flexible,
because the reading view is whitespace-normalised) and records the exact original substring with its
offsets. The recorded `literal_span` is therefore always a byte-exact substring of the frozen
evidence item, never a paraphrase. All 161 gold-support records resolve this way.

## Query Distribution

| Primary type | Count |
|---|---|
| direct_factual_conceptual | 18 |
| design_construction | 10 |
| multi_source_synthesis | 10 |
| numeric_table | 8 |
| regulation_specification | 6 |
| cross_lingual | 6 |
| must_abstain | 8 |
| injection_adversarial | 6 |
| **Total** | **72** |

Every item carries exactly one `primary_query_type`; 54 distinct secondary tags overlap freely.

## Language Distribution

**36 Turkish / 36 English** — the target, with no deviation used.

## Answerability Distribution

| Value | Count |
|---|---|
| answerable | 61 |
| partially_answerable | 2 |
| unanswerable | 9 |

`must_abstain = true` on 9 items: the 8 in the must-abstain category plus `GEV058`, a cross-lingual
item whose packet genuinely cannot answer it (see Retrieval-Limited Cases).

## Difficulty Distribution

easy 8 · medium 36 · hard 28.

## Source Diversity

44 unique source documents supply gold. Items per document (top 10):

`DOC000047` 21 · `DOC000236` 7 · `DOC000015` 7 · `DOC000003` 7 · `DOC000087` 6 · `DOC000002` 4 ·
`DOC000011` 4 · `DOC000124` 3 · `DOC000302` 3 · `DOC000076` 3.

`DOC000047` (the FHWA road tunnel manual, 434 chunks) supplies gold for 21 of 72 items — 29%. This
concentration is real and is reported rather than engineered away: it is by a wide margin the
corpus's most substantial English-language technical manual, and forcing a diversity quota would
have meant citing weaker evidence for English conceptual and design questions. No cap was imposed.

## Evidence Diversity

116 unique evidence chunks carry gold. Maximum reuse of any single chunk: **3** items. No gold span
is reused across items — an audit gate, tripped twice during authoring (`DF16`/`MS09` sharing a
ventilation-design sentence, later `IA02`/`CL03` sharing an IED sentence) and resolved both times by
re-authoring rather than by relaxing the check.

Packets hold 18–20 evidence items; context sizes run 18,590–41,354 tokens (median 25,340), all far
inside the 64,610-token authoring budget.

## Numeric Cases

11 items carry numeric gold (20 numeric records), spanning the 8 `numeric_table` items plus numeric
requirements inside regulation items. Operations used: `exact`, `range`, `maximum`, `minimum`.
Default tolerance is `exact_textual`. Unit conversion is disallowed by default and set explicitly
(`unit_conversion_allowed`) only where the evidence itself states both units — `GEV043`, where the
source writes "4 to 16 inch (100 to 400 mm)". Every numeric value is asserted to appear literally
inside its own supporting span.

Examples: `GEV039` 15 cm maximum shotcrete layer; `GEV040` 350 / 400 / 500 kg/m³ cement dosage;
`GEV042` 150 mm × 300 mm cylinders at 28 days; `GEV044` 4% preferred / 6% used gradients;
`GEV046` 300 m exit spacing and 500 m cross-connections.

## Multi-source Cases

All 10 synthesis items require ≥2 evidence items and are additionally audited to draw gold from
**≥2 distinct source documents**; `minimum_required_evidence_count` is recorded per item. Items
answerable from a single evidence item were replaced during authoring, not relabelled.

## Cross-lingual Cases

6 items, 3 in each direction:

- `tr_query_en_evidence`: `GEV053` (PIARC risk analysis), `GEV054` (sabotage/IED threat rating), `GEV055` (pre-support)
- `en_query_tr_evidence`: `GEV056` (EPB TBM), `GEV057` (designer's representative duties), `GEV058` (route selection — abstain)

The mismatch is required at the level of the **gold-bearing evidence**, not merely the packet's
metadata mix. Two candidates were rejected for failing exactly this test. Note that some documents
carry a language label that disagrees with their chunk text (e.g. `DOC000168` is labelled `tr` but
holds English EU-directive text), so `dominant_evidence_language` is recorded alongside the full
per-language evidence counts and the direction was confirmed by reading.

## Must-Abstain Cases

8 category items, all verified unanswerable by scanning the **whole** packet, not just the top
results. None is an artificial nonsense question; each is a realistic question whose packet returns
closely related evidence but not the requested fact. The strongest distractors:

- `GEV059` — the packet **does** contain a Bolu tunnel maintenance figure (120458 TRY per km, from an
  earlier source), but not a 2024 total. Different year, different quantity.
- `GEV062` — real Marmaray ridership for 2017–2021 is present, as annual totals; the question asks a
  2025 daily figure.
- `GEV066` — toll-revenue assumptions in Nepalese rupees are present; a 2031 maintenance budget is not.

Gold states *why* the evidence is insufficient and cites the distractor that explains the gap. No
must-abstain item carries a numeric gold record or any non-abstention claim — both enforced by test.

`MA11` was originally drafted as must-abstain and reclassified after reading: its packet names the
Eurasia Tunnel contractors in two documents but gives no price. It is now `GEV018`,
`partially_answerable`.

## Injection / Adversarial Cases

6 items using **real** packet content — no injection string was fabricated to manufacture a test.

| Item | injection_present | Benign imperative control | Type |
|---|---|---|---|
| GEV067 | true | no | contract template with blank placeholder fields |
| GEV068 | false | no | unsafe-looking security content (IEDs) |
| GEV069 | false | **yes** | procedural imperative in source |
| GEV070 | true | no | blank form template with empty fields |
| GEV071 | false | **yes** | unsafe-looking explosives-transport regulation |
| GEV072 | false | **yes** | specification imperative ("shall" form) |

Three benign imperative controls, above the required two. These guard the opposite failure mode from
injection: `GEV069` (control-centre procedure), `GEV071` (explosives permitting) and `GEV072`
(shotcrete specification) all contain imperatives that are legitimate engineering or regulatory
content and **must** be reported as fact, not treated as instructions and not refused. `GEV068` is an
over-refusal control on documented tunnel-security threats. All six expect
`ignore_as_instruction_use_as_data`.

## Conflict Cases

2 items record `conflict_gold` with both sides and their literal spans:

- `GEV040` — minimum cement dosage given both as a flat 350 kg/m³ "whatever the cement type" and as
  350 kg/m³ dry system / 400 kg/m³ wet system. The generator must preserve the distinction.
- `GEV043` — 100–400 mm initial structural shotcrete lining versus 30–50 mm flashcrete sealing layer.
  Different layers; must not be merged into one thickness.

Both expect `report_both_without_silent_resolution`, and neither picks a winner, because the evidence
does not resolve them. This is fewer than the "several" the specification invited: the selected
packets yielded exactly two defensible cases, and manufacturing more would have meant labelling
non-conflicts as conflicts. Recorded as a limitation rather than padded.

## Retrieval-Limited Cases

2 items, `retrieval_limited = true`, each with a written reason:

- `GEV018` (partially answerable) — contractors present, final price absent from the packet.
- `GEV058` (must abstain) — the corpus demonstrably holds Turkish route-selection material (other
  queries in this very authoring run retrieved it), but this frozen packet contains **zero**
  occurrences of `güzergah` / "route selection". Verified by scanning all 20 evidence items.

For generator-only metrics these must be scored separately: the generator abstaining here is
**correct**, and the failure belongs to retrieval/context.

## Gold Claim Contract

161 claims across 72 items, all claim-level with `claim_id`, `claim_text`, `claim_type`, `required`,
`supporting_evidence_ids` and `support_status`. Type distribution: factual 65, regulatory 29,
procedural 19, synthesis 18, numeric 17, abstention 11, conflict 1, comparative 1.

Two claims are deliberately `unsupported` with no evidence — the price half of `GEV018` and the
notice-requirements half of `GEV067`. Supported claims must cite evidence and unsupported claims must
cite none; both directions are asserted.

## Literal Span Validation

All 161 support records use `span_scope: "evidence_item"` — one coordinate system throughout, never
mixed silently with `context_text` offsets. Each record stores `span_start`, `span_end`,
`literal_span` and the `evidence_text_sha256` of the item it came from, and every one is asserted as
`evidence_text[span_start:span_end] == literal_span`. Numeric spans are validated the same way, plus
a check that each numeric value's digits appear inside the span.

Gold cites only evidence handles exposed by its own packet, never an excluded item, and never a
document ID or page number as a citation handle.

## Leakage Audit

No query contains an evidence handle (`E\d{3}`), a document ID (`DOC\d{6}`), the word "packet", or
any gold span longer than 40 characters. All 72 queries are distinct and read as realistic
tunnel-engineering questions.

## Duplicate Audit

No duplicate query text. No gold span reused across items — the strictest of the duplicate checks,
since two items testing the same sentence would be near-duplicates regardless of wording. Two
candidate pairs were eliminated during selection for sharing top evidence (`DC14`/`IA04`, and the
overlap between `DC13` and `MS10` was resolved by pointing their gold at different sources).

## Frozen Integrity

Unchanged and verified after authoring:

`scripts/19_retriever_v1.py` `8ada31f6…` · `scripts/20_rag_context.py` `4bcf5c99…` ·
`rag_context_contract_v1.json` `cc822cdb…` · `citation_contract_v1.json` `d1a5ad04…` ·
prompts v1 `303691ec…` / v2 `0063b9bc…` / v3 `d3cadd46…` · `chunks.jsonl` `e751fcfc…` ·
`chunks_recovery/chunks.jsonl` `835fc871…`

Qdrant `tunnelbook_dense_v1`: **5992 points before, 5992 after, 0 writes**, status green, dim 1024.

Benchmark SHA was computed, written to the manifest, and re-verified by re-reading the file from
disk. Tests assert the match, so any later edit to v1 fails the suite — corrections must become v2.

Test totals: **756 tests in `tests/` + 16 in `rapor/tests/` = 772, all passing** (37 skipped,
live-model gated), including 37 new benchmark tests.

## Known Limitations

- **Source concentration.** 21 of 72 items draw gold from `DOC000047`. Justified above, but a
  challenger model that happens to suit FHWA phrasing could look better than it is.
- **Only 2 conflict items.** The evidence supported no more genuine ones.
- **Language labels are unreliable in places.** Some chunks carry a document-level language that
  disagrees with the chunk text. Cross-lingual direction was confirmed by reading, but
  `dominant_evidence_language_metadata` is derived from metadata and should not be trusted alone.
- **Gold is claim-level, not exhaustive.** A packet often supports more true statements than the
  gold lists; scoring must treat gold claims as *required* content, not as a closed set.
- **Turkish OCR artefacts.** Some spans contain source-level OCR damage (e.g. `kalınliğı`,
  `tarafindan`, letter-spaced headings). Spans are exact to the frozen evidence, which is the
  contract, but string-equality scoring against clean text would misfire.
- **`retrieval_limited` is a judgement.** It records that the corpus plausibly holds the answer while
  the packet does not; for `GEV058` this was verified directly, for `GEV018` it is inference.
- **Difficulty labels are authored, not measured.** They carry no calibration until Phase B.

## Final Decision

**GENERATION EVAL BENCHMARK AUTHORING — CLOSED / GO**

Next: **GENERATION PHASE B — FROZEN 72-QUERY EXECUTION + CLAIM-LEVEL AUDIT**
