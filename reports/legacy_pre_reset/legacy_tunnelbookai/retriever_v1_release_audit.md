# TunnelBookAI Retriever V1 Release Audit

## Decision

**RETRIEVER V1 — FROZEN / GO**

**PRODUCTION RETRIEVER: DENSE_V1**

Release `tunnelbook-retriever-v1` v1.0.0, status `frozen`.

## Release Architecture

```
query → BAAI/bge-m3 (CLS pooling, L2 norm, no prefix) → Qdrant cosine top-k → ranked results
```

| component | state | why |
|---|---|---|
| bm25 | **excluded** | cross-lingual regression (probe v2 R@10 0.111 vs 0.259) |
| document_cap | **excluded** | reduced nDCG |
| language_routing | **excluded** | all variants worsened cross-lingual (0.074-0.111) |
| low_content_penalty | **excluded** | nDCG delta +0.003, within noise |
| neighbor_expansion | **excluded** | significantly worse on every metric |
| reranker | **excluded** | lowered R@1 and MRR at ~100x search cost |
| rrf | **excluded** | only used with bm25 |
| score_threshold | **excluded** | relevant/non-relevant score distributions overlap |
| translation | **excluded** | failed production preflight: latency 5-16s, unreliable output, terminology drift |

Nothing above runs in production. Each was measured and rejected on evidence, not assumption.

## Model Identity

- Model: `BAAI/bge-m3`
- Revision: `5617a9f61b028005a4858fdac845db406aefb181`
- Pooling **cls** · normalization **l2** · query prefix **none**
- Dimension **1024** · effective max sequence length **8192**
- Query embedding reproduces the exact behaviour the index was built with; verified unit-normalised 1024-d.

## Qdrant Identity

- Collection `tunnelbook_dense_v1` · distance **COSINE**
- Exact points **5992 → 5992** (read-only; zero writes, ingests or deletes)
- Documents represented: **214**

## Dependency Hashes

| artefact | SHA256 |
|---|---|
| `data/chunks/chunks.jsonl` | `e751fcfc3cc6828b05f75f494fd9a31b44388abd…` |
| `data/chunks_recovery/chunks.jsonl` | `835fc871ee53253d4d95eca14c7c13d908f7d06e…` |
| `data/embeddings/bge_m3_chunk_ids.json` | `7497af0d7d7032eb4c2400f74f6f1f694ab80ce3…` |
| `data/embeddings/bge_m3_dense.npy` | `99e3b79033a996ffb08b4b742faf68ec217a5a49…` |
| `data/evaluation/crosslingual_probe_v2.jsonl` | `90078d0af5097f9b6e5d06e93d4440d4392cf070…` |
| `data/evaluation/retrieval_benchmark_v1_manifest.json` | `093bdcc1b7521121e5bd369e4e9e0d876cb3e573…` |
| `data/evaluation/retrieval_queries_v1.jsonl` | `90aac5f98a75373fea0a0c6d04527a0e68231bd3…` |
| `data/metadata/full_embedding_input_manifest.csv` | `4af9d60a8cbfbb712c27c8129a622b6118166954…` |
| `data/metadata/full_embedding_manifest.csv` | `68be1f5fa0b7b6078cd9f492a8732aa796b2ab65…` |
| `data/metadata/qdrant_dense_release.json` | `c7d3f536eae7112df2617ebe82ef1655ee3835e7…` |
| `data/metadata/retriever_selection_history.json` | `fa5a836439e7e60a61c819e17dd92be8ac082f21…` |
| `data/metadata/retriever_v1_release.json` | `7667e29364e661d376a8b100b1a14d2fdc89a4b7…` |
| `reports/language_aware_retrieval_gate.md` | `7e70104f219160748c844753f9dd469d21fbbd42…` |
| `scripts/19_retriever_v1.py` | `8ada31f64d8ef51c3b4d3b8b04f3fcc3e9fb7338…` |

## Retrieval API

```python
retrieve(query: str, top_k: int = 10, filters: dict | None = None) -> list[RetrievalResult]
```

- `top_k` default **10**, maximum **100**; invalid values raise `ValueError`
- Results are frozen dataclasses carrying rank, score, point_id, chunk_id, document_id, text, title, heading, section_path, source_kind, citation_mode, provenance_status, page/slide ranges, source path, language, document_type, authority_level, year, topics, content flags and `is_low_content`
- `RetrieverUnavailable` is raised when Qdrant or the model cannot be reached — never a fake empty success
- `QueryTooLong` is raised above 8192 tokens — **no silent truncation**

## Citation Payload

- Provenance is passed through unmodified. `source_only` stays `source_only`; missing page numbers are never fabricated (verified: every `source_only` result has `original_page_start = None`).
- All 12 recovery chunks remain retrievable as `source_kind = recovery_chunk` with their `recovery_version` / `recovery_method` intact — not hidden, not promoted to canonical.
- Smoke check: every result across 16 queries carried non-empty text and a citation mode (**pass**).

## Filters

- Supported, caller-supplied only: `document_id`, `language`, `document_type`, `authority_level`, `year`, `source_kind`, `topics`
- **No filter is ever applied automatically.**
- `automatic_language_filter: false` is a deliberate safety property, not an omission: the language-aware gate measured that auto-filtering by detected query language destroys cross-lingual recall (0.074–0.111 vs 0.259). A Turkish query must still be able to return English sources — asserted by test.
- Explicit filters verified working: `document_id=DOC000041` returned only that document; `language=tr` returned only Turkish chunks.

## Dense Benchmark Regression

All 114 frozen v1 queries run through `scripts/19_retriever_v1.py`:

| metric | expected | produced | match |
|---|---|---|---|
| recall@1 | 0.4386 | 0.4386 | ✅ |
| recall@5 | 0.6842 | 0.6842 | ✅ |
| recall@10 | 0.7632 | 0.7632 | ✅ |
| recall@20 | 0.8246 | 0.8246 | ✅ |
| mrr@10 | 0.5383 | 0.5383 | ✅ |
| ndcg@10 | 0.5231 | 0.5231 | ✅ |
| doc_recall@10 | 0.8596 | 0.8596 | ✅ |

**No behavioural drift.** The production module reproduces the DENSE_V1 baseline exactly.

## Cross-lingual Regression

- Probe v2 (27 queries): Recall@10 **0.2593** (expected 0.2593), DocRecall@10 **0.4074** (expected 0.4074) — **reproduced**
- This is the capability the whole selection was made to protect.

## Smoke Queries

16 queries (5 Turkish, 5 English, 6 technical/code). Every one returned 5 results with finite scores, non-empty text and citation provenance present.

| query | top-1 | score |
|---|---|---|
| `tünel havalandırması` | `DOC000096-C0004` | 0.6907 |
| `kaya bulonu` | `DOC000124-C0053` | 0.4632 |
| `püskürtme beton` | `DOC000072-C0018` | 0.7143 |
| `jeoteknik araştırma` | `DOC000302-C0050` | 0.5936 |
| `tünel bakım ve işletmesi` | `DOC000036-C0030` | 0.6978 |
| `tunnel ventilation` | `DOC000197-C0023` | 0.6891 |
| `rock bolt design` | `DOC000047-C0131` | 0.6120 |
| `shotcrete` | `DOC000047-C0358` | 0.5600 |
| `geotechnical investigation` | `DOC000047-C0051` | 0.6417 |
| `tunnel maintenance` | `DOC000002-C0003` | 0.7007 |
| `NATM` | `DOC000302-C0144` | 0.5721 |
| `TBM` | `DOC000068-C0002` | 0.6030 |
| `RMR` | `DOC000037-C0087` | 0.5308 |
| `GSI` | `DOC000302-C0128` | 0.5240 |
| `EN 1997` | `DOC000272-C0011` | 0.4864 |
| `ASTM D1586` | `DOC000087-C0393` | 0.5146 |

### Cross-lingual release smoke (5 TR→EN, 5 EN→TR)

| query_id | direction | top-1 |
|---|---|---|
| X01 | tr->en | `DOC000096-C0004` |
| X02 | tr->en | `DOC000072-C0018` |
| X03 | tr->en | `DOC000290-C0004` |
| X04 | tr->en | `DOC000167-C0010` |
| X05 | tr->en | `DOC000072-C0059` |
| X18 | en->tr | `DOC000047-C0250` |
| X19 | en->tr | `DOC000047-C0218` |
| X20 | en->tr | `DOC000047-C0310` |
| X21 | en->tr | `DOC000041-R1-C0001` |
| X22 | en->tr | `DOC000047-C0051` |

Gold appeared in top-5 for **0/10** of these probes. That is consistent with the measured probe v2 Recall@5 of 0.111 and is *not* a release regression — these are the hardest cross-lingual cases in the corpus, and the release reproduces dense behaviour exactly. Cross-lingual remains the known weak area, recorded below.

## Latency

Warm, measured over all 114 benchmark queries.

| stage | median | p95 |
|---|---|---|
| query embedding | 12.1 ms | 19.6 ms |
| Qdrant search | 15.8 ms | 19.9 ms |
| **total** | **28.1 ms** | **37.0 ms** |

No BM25, translation or reranker runs — there is nothing else in the path.

## Determinism

- Same query + same filters + same release ⇒ identical ranking (verified).
- Ties are broken by point id, so ordering cannot vary between runs.
- Point id ↔ chunk id mapping is carried in every result.

## Historical Candidate Supersession

- `data/metadata/retriever_v1_candidate.json` (HYBRID_RRF_30, `candidate_pending_freeze`) is **retained unmodified** as historical experiment evidence and was **not promoted**.
- `data/metadata/retriever_selection_history.json` records the supersession: candidate HYBRID_RRF_30, `not_released`, reason `cross_lingual_regression`, with the benchmark, probe v2 and language-gate evidence.
- Experimental systems retained for future work: HYBRID_RRF_30, BILINGUAL_HYBRID_RRF, the five language-aware variants, RERANK_20/50, DENSE_NEIGHBOR_1, BM25_V1.

## Protected Integrity

- Protected artefacts changed: **0**
- Corpus trees (`corpus_final`, `corpus_normalized`, `corpus_recovery`), chunks, recovery chunks, embedding files, embedding manifests, benchmark v1 and the Qdrant release descriptor: **all unchanged**
- Qdrant: **5992 → 5992**, zero writes

## Tests

- `tests/`: **511/511 PASS** · `rapor/tests/`: **16/16 PASS** · **project-wide 527/527 PASS**
- 45 new retriever tests: release config is DENSE_V1, revision pinned, 1024-d unit-normalised query vector, no query prefix, no silent truncation, collection name, deterministic ranking, top_k validation, filter mapping, no automatic language filtering, no translation/BM25/reranker dependency (AST-checked), payload and citation mapping, recovery chunk handling, low-content flag preserved, unavailable error, frozen benchmark metrics, cross-lingual regression, protected immutability, live exact count 5992
- Full suite also passes with `TUNNELBOOK_QDRANT_LIVE=1 TUNNELBOOK_BGE_LIVE=1` (511/511, no skips)

## Warnings

- **Cross-lingual retrieval is weak in absolute terms** (probe v2 Recall@10 0.259). Dense is the best option measured, but it is not good. This is the top candidate for future work — a properly aligned multilingual approach, not BM25 and not runtime translation, both of which were measured and rejected.
- **A statistically significant monolingual nDCG gain was deliberately given up.** HYBRID_RRF_30 scored +0.0910 nDCG@10 (CI [+0.0641, +0.1206]) over dense. That gain is real; it was traded for cross-lingual capability because the corpus is bilingual. If cross-lingual ceases to be a requirement, revisit this.
- Retriever v1 returns ranked results with **no score threshold**. Modest scores are returned rather than suppressed; deciding what is good enough belongs to the RAG context layer.
- The 143 low-content vectors remain indexed and unpenalised, flagged via `is_low_content` for the RAG layer to act on.
- Qdrant runs in a local Docker container under colima; if that daemon stops, the retriever raises `RetrieverUnavailable` rather than returning empty results.

## Blockers

- Yok.

## Final Closure Corrections

An external audit of the provisional freeze found two defects. Both are fixed here; the same v1.0.0 was re-frozen because neither touched production code and the freeze was not yet approved.

### Defect A — incorrect release timestamp

- Was: `2026-08-18 (release stamped at freeze; retrieval itself carries no timestamp)` — a free-text string, not ISO-8601, and dated one day in the future.
- Now: `2026-08-17T22:07:44+03:00` — timezone-aware ISO-8601 taken from the system clock at closure (Europe/Istanbul (+03:00)).
- Wrong provenance in a frozen release is not acceptable, so this was corrected rather than documented as a known issue.

### Defect B — source_only test used the wrong field, and was vacuous

- The old test asserted `provenance_status == "source_only" ⇒ original_page_start is None` over a `"tunnel"` top-20. It could pass while examining **zero** source_only results, and it conflated two independent fields.
- **Investigating the frozen data changed what the correct assertion is.** The requested replacement (`citation_mode == "source_only" ⇒ page is None`) would **fail**: 50 of the 71 such chunks carry page numbers.
- Those pages are not fabricated. 44 appear verbatim in the chunk's own text (`## Sayfa 1`); the other 6 are recovery chunks inheriting a marker from an earlier chunk in the same document, which is the chunker's documented page propagation.
- The two fields mean different things, and the release now says so explicitly:

| field | meaning | measured contract |
|---|---|---|
| `provenance_status == source_only` | no resolvable citation anchor | **539** chunks, page **and** slide fields null in every one |
| `citation_mode == source_only` | cite by source rather than by page | **71** chunks, slide always null, page present in 50 and always source-derived |

- Three tests now enforce this, each asserting an exact non-zero population so none can pass vacuously: 539 provenance-source_only chunks scanned via full filtered scroll, 71 citation-mode chunks with exactly 50 carrying pages, and 6 deterministic fixtures that are source_only in both fields (`DOC000237-C0001`, `DOC000237-C0002`, `DOC000239-C0001`, `DOC000246-C0001`, `DOC000246-C0002`, `DOC000254-C0001`).

### Citation-mode inventory

Authoritative inventory over all 5992 production points, for the RAG stage:

| citation_mode | count |
|---|---|
| `pdf_page` | 4228 |
| `document_section` | 868 |
| `slide` | 798 |
| `source_only` | 71 |
| `table_or_sheet` | 24 |
| `image` | 3 |

| provenance_status | count |
|---|---|
| `page_resolved` | 4228 |
| `section_resolved` | 659 |
| `slide_resolved` | 566 |
| `source_only` | 539 |

Artifact: `data/metadata/retriever_v1_citation_inventory.json`. **Fabricated page values: 0.** No Qdrant payload was mutated to produce it.

### Closure verification

| check | result |
|---|---|
| `scripts/19_retriever_v1.py` | **byte-identical** (`8ada31f6…`) — no production code change |
| Release manifest hashes | refreshed; all current, none stale |
| Dense benchmark | reproduced exactly (all 7 metrics) |
| Cross-lingual probe v2 | R@10 0.2593, DocR@10 0.4074 — reproduced |
| Qdrant | 5992 → 5992, zero writes/deletes/payload mutations |
| Protected artefacts | all unchanged, including historical `retriever_v1_candidate.json` |
| Tests | `tests/` **525/525**, `rapor/tests/` **16/16** → **541/541 PASS** (also 525/525 with live flags) |

New closure tests: created_at parses as timezone-aware ISO-8601, carries a UTC offset, is +03:00, is not in the future, and falls on the 2026-08-17 freeze date; manifest hash of the release descriptor equals its actual SHA256; every manifest artefact hash is current; the recorded production-script hash equals the module's own `script_sha256()`.

## Final Decision

**RETRIEVER V1 — FROZEN / GO**

**PRODUCTION RETRIEVER: DENSE_V1**

Frozen files (changes require v1.1 or v2, never in-place edits):

- `scripts/19_retriever_v1.py`
- `data/metadata/retriever_v1_release.json`
- `data/metadata/retriever_v1_manifest.json`

Next stage: RAG CONTEXT ASSEMBLY + CITATION CONTRACT.
