# Book-Writing Pipeline Architecture v1

## Executive Decision

**BOOK-WRITING PIPELINE ARCHITECTURE V1 — CLOSED / GO**

`tunnelbook-book-writing-pipeline-v1` and `tunnelbook-evidence-note-contract-v1` are implemented,
exercised on a real three-section pilot through the frozen production generator, and audited by
hand. **159 evidence notes, 159 contract-valid, 0 unsupported notes marked SUPPORTED, 0 invented
evidence refs, 0 missing provenance, 0 silent conflict resolution, 0 Qdrant writes.**

`drafting_enabled` is **false** and `draft_section` raises `NotImplementedError`. No chapter, no
section prose, no manuscript text was produced.

The pilot's most valuable output is not the notes — it is that the manual audit **found real
defects in the extractor** and the readiness logic, and that fixing them made two of three sections
*less* ready, not more. That is the layer working as intended.

## Why Evidence Notes Come Before Prose

A model asked to "write a chapter" produces fluent text whose relationship to the corpus cannot be
checked afterwards. The evidence note inverts the order: every proposition is extracted, bound to a
chunk, and required to show a literal span *before* anyone writes a sentence. Prose then becomes a
rendering problem over approved material rather than a generation problem over memory.

The pilot justified this concretely. Of 159 extracted notes, only **68 could demonstrate literal
support**. The other 91 cite real evidence but could not be shown to follow from it by deterministic
matching. Had the accepted answers been treated as chapter material directly, all 159 propositions
would have entered the book with equal apparent authority.

## Architecture

```
BookProject
   └─ ChapterPlan
        └─ SectionPlan
             └─ ResearchQuestion[]        (atomic, typed, P0/P1/P2)
                  └─ ProductionGroundedGenerator v1   (unchanged, accept/reject)
                       └─ GroundedAnswer
                            └─ EvidenceNote[]        (decomposed, literal spans, provenance)
                                 └─ ClaimLedger      (dedup candidates, conflict groups)
                                      └─ SectionEvidenceBundle  (readiness + bundle_sha)
                                           └─ draft_section(...)  ← NotImplementedError
```

Path note: the pipeline was requested at `scripts/37_*`, but slot 37 is already the production
orchestration smoke runner, so it lives at `scripts/39_book_writing_pipeline.py` with the path
pinned in both manifest and descriptor.

## Frozen Dependencies

| Component | Identity | Used |
|---|---|---|
| Retriever | `tunnelbook-retriever-v1` | unchanged |
| Context | `tunnelbook-context-v1` | unchanged |
| Prompt | `generation-system-prompt-v5`, `9bae1362…4085` | unchanged |
| Output Contract | `…-v1.1`, `5ebf8fe9…def5` | unchanged |
| Production generator | `tunnelbook-production-grounded-generator-v1` | unchanged |

Every research question runs through `scripts/36_production_grounded_generator.py`. The pipeline
duplicates none of its chain — a test asserts the absence of `assemble_context`,
`validate_citations`, `embed_query` and any HTTP call in the pipeline source.

The packet is obtained by **observing** the generator, not by retrieving again: `build_packet` is
wrapped for the duration of the call, and the observed packet's sha is recomputed and compared
against the generation's `context_packet_sha`. A mismatch raises rather than proceeding, because
every evidence ref derived from a wrong packet would be unsound.

## Source Policy

`corpus_only`. The `BookProject` constructor **refuses** any other value. No web access, no
external sources, no general model knowledge as evidence. A note that cannot name its chunk cannot
exist.

## Book Project Schema

`BookProject(book_id, working_title, language, audience, technical_level, purpose, chapter_ids,
source_policy, citation_policy, status, created_at)`. Production language is Turkish; source
language is retained per evidence item, so an English source summarised in Turkish keeps its
provenance and its own-language span requirement.

## Chapter Plan

`ChapterPlan(chapter_id, chapter_number, title, purpose, scope_in, scope_out, prerequisites,
section_ids, target_audience, technical_depth, status)`. `scope_out` is as load-bearing as
`scope_in`: it is what stops a section from wandering into material it has no evidence for.

## Section Plan

`SectionPlan(section_id, chapter_id, section_number, title, objective, questions, required_topics,
optional_topics, excluded_topics, expected_claim_types, status)`. It states **what must be
established**, never how the finished text will read. A test asserts no `draft`/`prose` key exists
and that objectives stay short.

## Research Question Contract

`ResearchQuestion(question_id, section_id, question, question_language, question_type, priority,
required, expected_answer_type, minimum_sources, notes, status)`, validated on construction against
18 question types, three priorities and two languages.

Decomposition is enforced by design, not by convention. The pilot's ventilation-style monolith
("Explain tunnel ventilation") does not exist; sections carry 6–7 atomic questions each — for
example §2.2 asks separately for minimum cement dosage, initial lining thickness, strength class,
layer counts and flashcrete thickness.

## Research Execution

19 questions across three sections. Each returns one of: `answered`, `insufficient_evidence`
(a valid abstention, recorded as a research result rather than a failure), `generator_rejected`
(the contract refused the answer), or `request_rejected`.

Per-question artifacts land in `data/book/research_runs/<section_id>.jsonl` with the production
request id, audit id, status, failure reasons, context packet sha and evidence handles.

## Production Generator Delegation

Rejections are never repaired, never re-queried and never removed. On rejection the pipeline records
`question_status = generator_rejected`, stores no answer, produces no notes, and lets the gap reach
the readiness decision. A test asserts a rejected run carries a null answer and an empty note list.

## Evidence Note Contract

`tunnelbook-evidence-note-contract-v1`, repair policy `none_fail_closed`. It validates and rejects;
it never edits a claim, supplies a unit, softens a modality or reconciles a conflict.

Enforced checks include: missing id or claim; assertive status without evidence refs; evidence id
absent from the associated packet; chunk/document mismatch against the packet; literal support
absent or not found in the cited evidence; high confidence without a span; source coordinates in the
claim; a markdown table pasted as a "claim"; numeric note without data, without source, without a
unit the source shows, **or whose value does not appear in its own span**; incomplete formula marked
supported; requirement without modality or whose modality vanished from the claim; conflict without
refs; unknown chunk identity.

## Support Status

`SUPPORTED`, `PARTIALLY_SUPPORTED`, `INSUFFICIENT_EVIDENCE`, `CONFLICTING_EVIDENCE`, `REJECTED` —
no `UNKNOWN`. Confidence is **evidence** confidence, decided by literal support and source counts,
never by how assured the prose sounds. A note with no literal span cannot be `high`.

## Literal Evidence

Producer and validator share **one** normaliser, `normalise_for_span_match`, exported by the
contract and imported by the extractor. This was a defect found during the pilot: the extractor
stripped punctuation while the validator did not, so **49 spans the extractor had genuinely located
were rejected as "not found"**. A producer and validator that normalise differently manufacture
spans the contract then refuses.

Where no span is locatable — paraphrase, synthesis across items, or a Turkish claim drawn from
English evidence — the note is marked `INSUFFICIENT_EVIDENCE` with
`review_status = needs_manual_literal_span`, keeping its refs so a human can attach the span and
upgrade it. **91 of 159 notes are in this state.** The pipeline does not assert support it cannot
show.

## Numeric Evidence

Numeric facts are structured (`value`, `range`, `minimum`, `maximum`, `unit`, `condition`,
`source_evidence_ids`), never flattened into prose.

The manual audit found the sharpest defect here. Before the fix, notes like *"B1 Sınıfı: Üst yarı
2,0-3,0 m, alt yarıda 4,0 m"* were `SUPPORTED / high` on a span reading only `"m, alt yarıda 4,0 m"`
— the second figure evidenced, the first not. Worse, *"…yüksek su basıncına (örneğin 20 bar)…"* was
supported by a span reading `"Tek Kalkanlı Sert Kaya"`, which contains no number at all.

Both extractor and contract now require **every** numeric fact in a note to appear in that note's
own span. The extractor was initially lenient (any value sufficed) while the contract was strict
(each value); the extractor was aligned to the contract, not the reverse.

## Standards / Requirements

Modality is preserved and must survive into the claim text, not merely sit in a field. Matching is
word-boundary anchored after the audit found two false positives: `"en az"` firing inside
`"en aza indirmek"` (*to minimise*) and `"en fazla"` inside `"birden fazla"` (*more than one*) — each
silently converting ordinary prose into a normative requirement.

## Conditions / Exceptions

`conditions`, `qualifiers` and `exceptions` are extracted per note (Turkish and English condition
markers) and travel with the claim. A claim may not be detached from a material condition to make
it shorter.

## Conflicts

Representable and never silently resolved: `conflict_status`, `conflict_refs`, a
`CONFLICTING_EVIDENCE` status, and a `conflict_group` on the ledger. The contract rejects a conflict
marked without refs, and rejects `CONFLICTING_EVIDENCE` without the conflict marker.

**No conflicts were detected in the pilot — and none were *looked for*.** v1 provides the
representation, not a detector. This is a stated gap, not a finding of corpus consistency.

## Claim Ledger

68 entries over the three sections (one per demonstrably supported note), each with
`canonical_claim`, `note_ids`, support status, duplicate candidates, conflict group, numeric flag
and `citation_ready`. Duplicate detection is lexical Jaccard overlap at 0.75; **4 duplicate
candidate pairs** were flagged for human confirmation. No model is asked to merge claims — a test
asserts the ledger builder contains no generation call.

`citation_ready` requires a valid note, valid refs, a resolved registry key and no unresolved
conflict: **68/68**.

## Section Evidence Bundle

Carries questions, results, notes, ledger, unanswered and rejected questions, conflicts, numeric
facts, requirements, source and coverage summaries, readiness with written reasons, and a
`bundle_sha` over canonical JSON excluding timestamps. Bundles are immutable; corrections create a
new revision.

## Section Readiness

| Section | Pattern | Readiness |
|---|---|---|
| SEC-02-1 Destekleme Sistemleri | concept-heavy | **READY_WITH_LIMITATIONS** |
| SEC-02-2 Püskürtme Beton | numeric/spec-heavy | **READY_WITH_LIMITATIONS** |
| SEC-02-3 Kazı Yöntemi Seçimi | multi-source comparative | **NOT_READY** |

SEC-02-3 is NOT_READY for a specific, printed reason: *P0 question Q-02-3-01 produced no SUPPORTED
evidence note.* It was answered and the answer was contract-valid — but nothing in it could be tied
to a literal span, because the Turkish answer draws on English sources. The section therefore cannot
be drafted, and the gap is named rather than papered over.

A readiness defect was corrected mid-pilot. Initially, contract-invalid notes were dropped and
readiness assessed only the survivors, so a section that had lost most of its notes still reported
`READY_FOR_DRAFT`. Readiness now takes discarded notes, unsupported P0 questions and
awaiting-span counts as first-class inputs — precisely the "do not write around gaps" rule.

## Packet-Local Evidence IDs

`[E001]` denotes nothing on its own; it is assigned per packet. Every `EvidenceRef` therefore
carries `evidence_id` **and** `context_packet_sha`, and the contract rejects a ref missing either.
A test proves the same handle under two different packet shas is not conflated: it resolves to a
different chunk and validation fails with `evidence_ref_chunk_mismatch`.

## Book-Level Source Registry

`data/book/source_registry_v1.jsonl`, append-only, **68 entries**. Keys are
`SRC-<document_id>-<12-hex of sha256(document_id|chunk_id)>` — deterministic, stable, containing no
internal path. The same document/chunk always maps to the same key regardless of which packet
surfaced it; a test recomputes every stored key and asserts no duplicates.

## Traceability

Every citation-ready claim resolves the full chain:

```
claim_id → note_id → (evidence_id + context_packet_sha) → chunk_id → document_id → SRC- key
        → title, citation_mode, provenance_status, page/slide range, retrieval rank & score
```

Internal coordinates stay internal; the model-visible grammar remains `[E###]`, and the contract
rejects a claim containing document ids, page or slide numbers.

## No-Prose Gate

`draft_section(section_plan, section_evidence_bundle)` raises `DraftingDisabled(NotImplementedError)`.
`drafting_enabled: false` in the descriptor. Tests assert the raise, assert no `.md`/`.docx`/`.tex`
artifact exists anywhere under `data/book/`, and assert section plans carry no narrative field.

Drafting stays unimplemented because the pilot has just demonstrated why: an extractor that looked
correct produced numeric notes whose spans carried no numbers. Introducing prose before that class
of defect is closed would bury it.

## Pilot Design

Three sections of one chapter, chosen for different evidence patterns, 19 questions total (6–7 per
section, each with ≥2 P0 and ≥3 P1). Executed against the real frozen production generator with no
bypass.

## Pilot Results

| Metric | Value |
|---|---|
| Research questions | 19 |
| Answered | 19 |
| Generator rejections | 0 |
| Valid abstentions | 0 |
| Evidence notes extracted | 159 |
| Contract-valid | **159 / 159** |
| SUPPORTED | 68 |
| INSUFFICIENT_EVIDENCE | 91 |
| Awaiting manual span | 73 |
| Claim ledger entries | 68 |
| Citation-ready claims | 68 / 68 |
| Duplicate candidate pairs | 4 |
| Conflict groups | 0 (none detected; none sought) |
| Source registry entries | 68 |
| Qdrant writes | **0** |

Question coverage: **P0 7/7, P1 9/9, P2 3/3 answered** — but "answered" is a generation outcome, not
an evidence outcome, which is exactly why SEC-02-3 is still NOT_READY.

## Pilot Manual Audit

Two layers, and the distinction matters:

**Programmatic re-verification of all 159 notes**, independent of the contract code — span present
in cited evidence, refs carry packet sha and provenance, source keys registered, no coordinate leak,
numeric facts sourced, modality present, conflicts referenced. **All seven checks: 0 violations.**

**Human reading of the 35 high-risk SUPPORTED notes** (all numeric and all requirement/recommendation
notes) beside their spans and evidence. This is what found the defects reported above. After the
fixes, 14 high-risk SUPPORTED notes remain and each was re-read: every numeric span carries its
value verbatim (`"Çimento miktarı 350 kg/m³'ten az"`, `"from 4 to 16 inches (100 to 400 mm)"`,
`"typically 30 to 50 mm (1.2 to 2 in)"`, `"5.00 x 2.15 m"`, the RMR advance ranges).

Stated precisely: **manual evidence-note audit 35/35 high-risk notes read; 159/159 notes
contract-valid; 0 unsupported notes marked SUPPORTED.** The 124 lower-risk notes were verified
programmatically on all checkable properties, not read individually.

One residual weakness the audit found and did **not** fix: a compound claim can be credited by a
span covering only one of its clauses (`Q-02-1-06-N06` asserts stability, watertightness *and*
operating economy; its span carries only the economy clause). Clause-level decomposition is future
work, and high-risk technical claims still require human review.

## Metrics

Per section — SUPPORTED / INSUFFICIENT / awaiting-span / single-source / multi-source:

- **SEC-02-1**: 28 / 20 / 20 / 21 / 27
- **SEC-02-2**: 15 / 20 / 15 / 10 / 20
- **SEC-02-3**: 25 / 51 / 38 / 47 / 16

SEC-02-3's profile is the signature of a cross-lingual comparative section: the most notes, the
fewest with locatable spans, and the most single-source claims.

## Known Gaps

- **corpus_only scope** — nothing outside the 214-document corpus is admissible.
- **Citation coverage debt ≈ 0.88** inherited from the generator; this layer does not improve it.
- **Production rejection rate** inherited: roughly 1 request in 24 returns nothing.
- **Retrieval limits**: top-k 20 over one packet per question; a question retrieving poorly yields
  poor evidence, and the pipeline cannot tell that from genuine corpus silence.
- **Packet-local `[E###]`** — meaningless without `context_packet_sha`; handled, but a permanent
  hazard for anything reading these artifacts naively.
- **Source authority is heterogeneous** (specifications, training material, conference slides,
  vendor brochures) and is **not weighted**.
- **Conflicts representable but not detected** in v1.
- **Literal-span extraction is lexical**, so paraphrase and cross-lingual support needs manual
  attachment — 73 notes await it.
- **Compound claims** can be over-credited by a partial span.
- **No prose has been produced or evaluated**, so nothing is known about drafting quality.

## Frozen Integrity

Unchanged and asserted by test: Retriever v1, Context v1, Prompt v5 (`9bae1362…4085`), Output
Contract v1.1 (`5ebf8fe9…def5`), Production Grounded Generator v1, corpus, chunks, embeddings. No
prompt v6. Qdrant **5992 → 5992, 0 writes**.

Tests: **67 new** (34 evidence-note contract, 33 pipeline), full suite green.

## Final Decision

**BOOK-WRITING PIPELINE ARCHITECTURE V1 — CLOSED / GO**, drafting still disabled.

The layer does what it was built to do: it decomposes answers instead of trusting them, it refuses
to call a claim supported without showing where the support is, it keeps packet-local identity
honest, it gives every source a stable book-level key, and it lets a section be declared NOT_READY
for a printed reason.

The strongest evidence for the GO is not the 159 valid notes. It is that a naive reading of the
first pilot would have reported three ready sections and 160 clean notes, and the required manual
audit instead found numeric claims supported by spans containing no numbers, requirements invented
by substring matches, and a readiness function that ignored its own discards. Those are exactly the
failures this layer exists to catch before they reach a page.

Next: **section drafting contract + book citation rendering contract**. No chapter, outline, section
draft or manuscript prose was produced in this phase.
