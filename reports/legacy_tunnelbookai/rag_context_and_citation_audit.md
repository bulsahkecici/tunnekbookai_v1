# TunnelBookAI RAG Context + Citation Contract Audit

## Decision

**RAG CONTEXT + CITATION CONTRACT — GO**

Contract `tunnelbook-context-v1` / `tunnelbook-citation-v1`. Deterministic evidence layer between Retriever v1 and a future generation model. No LLM was called.

## Inputs

- Retriever v1 (`DENSE_V1`), release `tunnelbook-retriever-v1` v1.0.0, script SHA `8ada31f6…` — **unchanged**
- Qdrant `tunnelbook_dense_v1`, 5992 points — **read-only, unchanged**
- Frozen citation inventory used as the regression baseline

## Retriever Identity

`scripts/19_retriever_v1.py` is imported as the sole retrieval source; retrieval is never reimplemented. Tests assert the module contains no BM25, no experimental-script imports and no LLM endpoints.

## Context Contract

- Selection: retrieve → validate → drop duplicate `chunk_id` → drop duplicate `text_sha256` → preserve retrieval order → add whole items until budget → never truncate mid-chunk
- No semantic reranking, no neighbour expansion (v1 uses only what the retriever returned)
- Artifact: `data/metadata/rag_context_contract_v1.json`

## Evidence Model

`EvidenceItem` (frozen dataclass) carries evidence_id, retrieval rank/score, point/chunk/document ids, exact text + sha256, token count, title/heading/section_path, source_kind, language, document_type, authority_level, year, topics, citation_mode, provenance_status, page/slide ranges, source path/extension, table/formula/image flags, is_low_content, recovery_version, recovery_method, and a `CitationRef`.

## Selection Policy

| policy | behaviour |
|---|---|
| duplicates | exact only (`chunk_id`, `text_sha256`); no fuzzy dedup in v1 |
| ordering | retrieval order preserved |
| truncation | never — an item that does not fit is excluded whole, with a reason |
| tables | atomic; excluded whole as `token_budget_atomic_table` |
| low-content | retained and flagged; only budget pressure excludes, and it is recorded |
| recovery chunks | included, flagged `recovery_chunk`, recovery metadata preserved |

## Token Budget Policy

- Counter: `whitespace-word-v1` — **provisional and pluggable**
- BGE-M3's tokenizer is deliberately **not** used: it is the retrieval tokenizer and says nothing about a generation model's context window.
- Default budget **12000**, marked provisional; the production value belongs to the generation-model stage.

## Citation Mode Semantics

| mode | primary anchor | never does |
|---|---|---|
| `pdf_page` | document + page range | invent a page; missing anchor ⇒ degraded |
| `slide` | document + slide range | substitute a page number |
| `document_section` | section_path / heading | become `pdf_page` when a page exists |
| `table_or_sheet` | heading / section identity | flatten into a page reference |
| `image` | source provenance | fabricate figure/page numbering |
| `source_only` | the source | imply pages are absent — 50 of 71 legitimately have them |

## Provenance Status Semantics

| status | meaning |
|---|---|
| `page_resolved` | page anchor exists and may be cited |
| `slide_resolved` | slide anchor exists and may be cited |
| `section_resolved` | section anchor; cite section |
| `source_only` | **no resolvable coordinate**; never emit page or slide |

**Precedence:** `provenance_status == source_only` overrides the mode's preferred anchor and drops to source level. It suppresses *coordinates* only — the chunk's own heading/section text is not a coordinate and is still shown when present.

## Citation Rendering

| case | display |
|---|---|
| single page | `[DOC000123, s. 14]` |
| page range | `[DOC000123, ss. 14–16]` |
| slide | `[DOC000287, Slayt 71]` |
| section | `[DOC000050, "Tünel Havalandırması"]` |
| source-only | `[DOC000237]` |

`document_id` is always retained internally; titles are never the sole identifier because duplicates exist.

## Machine Citation Schema

`evidence_id, document_id, chunk_id, citation_mode, provenance_status, citation_quality, page_start, page_end, slide_start, slide_end, section_path, heading, source_relative_path, source_kind, supplemental_source_location`

The generation model will cite `[E003]` only. It never decides document, page or slide — those are precomputed here from frozen payload metadata, which is the whole point of this layer.

## Source-only Dual Semantics

The distinction this stage exists to protect:

| | count | contract |
|---|---|---|
| `citation_mode == source_only` | 71 | cite the source; 50 carry source-derived pages, kept as `supplemental_source_location`, **never** promoted to a page citation |
| `provenance_status == source_only` | 539 | no coordinate at all; page and slide are never emitted |

Tested against real production fixtures: the six dual-source_only chunks (`DOC000237-C0001`, `DOC000237-C0002`, `DOC000239-C0001`, `DOC000246-C0001`, `DOC000246-C0002`, `DOC000254-C0001`) render source-level with no anchor, and the `DOC000159` family keeps its page metadata supplemental while remaining `source_only`.

## Citation Inventory

Regression against the frozen inventory before any context work: citation modes and provenance statuses both total **5992**, matching exactly.

| citation_mode | count |
|---|---|
| `pdf_page` | 4228 |
| `document_section` | 868 |
| `slide` | 798 |
| `source_only` | 71 |
| `table_or_sheet` | 24 |
| `image` | 3 |

## Duplicate Handling

Exact `chunk_id` and `text_sha256` duplicates are removed before budgeting so the same evidence cannot consume the budget twice. Exclusions are reported with reasons. No fuzzy deduplication.

## Low-content Handling

- Low-content evidence included across the smoke set: **10** items, all flagged
- Never deleted blindly: a short legal clause or table may be exactly the right citation
- Excluded only under budget pressure, always with a recorded reason

## Recovery Evidence

- Recovery chunks appearing in smoke packets: **5**
- Marked `source_kind = recovery_chunk` with `recovery_version` / `recovery_method` preserved; not hidden, not promoted to canonical

## Prompt Injection Boundary

Every evidence block is wrapped in `<BEGIN_UNTRUSTED_EVIDENCE E00n>` / `<END_UNTRUSTED_EVIDENCE E00n>` and preceded by an explicit notice stating that instruction-like wording inside evidence is data, not a directive. Technical content is **not** sanitised merely for containing imperatives — a specification that says "apply bolts at 2 m spacing" must survive intact.

## Context Smoke Tests

- Queries: **18** (Turkish, English, technical codes, recovery-targeted)
- All produced sufficient evidence; none flagged `insufficient_evidence`

| citation mode | evidence items |
|---|---|
| `pdf_page` | 108 |
| `document_section` | 32 |
| `slide` | 31 |
| `source_only` | 7 |

| citation quality | count |
|---|---|
| `exact` | 130 |
| `source` | 30 |
| `section` | 10 |
| `degraded` | 8 |

- Evidence with `provenance_status == source_only` that emitted a page or slide: **0**
- The 8 `degraded` items are `slide`-mode chunks whose slide anchor is absent. They are reported as degraded and emit no coordinate, but still display their real section heading rather than discarding usable provenance.

`table_or_sheet` and `image` did not surface in the smoke queries, so both are covered by real production fixtures by chunk id instead of synthetic metadata.

## Determinism

- Same query + same frozen release + same settings ⇒ identical evidence ids, order and JSON bytes
- `to_json()` uses sorted keys and carries no timestamp or randomness
- Verified live on repeated assembly

## Frozen Integrity

- `scripts/19_retriever_v1.py`: **unchanged** (`8ada31f6…`)
- Retriever release / manifest / citation inventory: **unchanged**
- Chunks, recovery chunks, embeddings, corpus trees, benchmark: **unchanged**
- Qdrant: **5992 → 5992**, zero writes

## Tests

- `tests/` **575/575 PASS** · `rapor/tests/` **16/16 PASS** → **591/591 PASS**
- Also 575/575 with `TUNNELBOOK_QDRANT_LIVE=1 TUNNELBOOK_BGE_LIVE=1`
- 50 new context/citation tests covering every citation mode, every provenance status, dual source_only fixtures, source_only-with-page fixtures, invalid ranges, duplicates, token budget, atomic tables, injection delimiters, exact text preservation, recovery metadata, determinism and retriever-unavailable propagation

## Warnings

- The token counter is **provisional** (whitespace words). The context budget must be recomputed with the generation model's own tokenizer before production; 12000 here is a test default, not a model limit.
- 8 of 168 smoke evidence items carry `degraded` citations — `slide` mode without a slide anchor. They are usable (section shown) but cannot be cited to a slide.
- Same-document neighbour expansion is deliberately absent from v1; if answers need surrounding context, that is a separate experiment, not a silent addition.
- Cross-lingual retrieval remains weak upstream (probe v2 R@10 0.259). This layer faithfully passes through whatever Retriever v1 returns and cannot compensate for it.

## Blockers

- Yok.

## Final Decision

**RAG CONTEXT + CITATION CONTRACT — GO**

Next stage: GENERATION MODEL SELECTION + GROUNDED ANSWER / CITATION VALIDATION.
