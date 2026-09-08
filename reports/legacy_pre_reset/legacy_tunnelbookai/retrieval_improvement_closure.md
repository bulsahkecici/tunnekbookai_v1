# TunnelBookAI Retrieval Improvement Closure

## Decision

**RETRIEVAL IMPROVEMENT — CLOSED / GO**

**RECOMMENDED RETRIEVER V1: HYBRID_RRF_30**

The experiment report written mid-run named BILINGUAL_HYBRID_RRF as best-scoring. That remains true on benchmark v1, but it is **not** the production recommendation: its advantage depends on hand-authored translations that no deployable mechanism reproduces. This closure supersedes that recommendation.

## Production Retriever Selection

| | |
|---|---|
| Retriever | **HYBRID_RRF_30** |
| Input | original user query only |
| Dense | BAAI/bge-m3 @ 5617a9f6…, collection `tunnelbook_dense_v1`, top 50 |
| Lexical | BM25+ (`bm25plus-v1`), top 50 |
| Fusion | Reciprocal Rank Fusion, k=30 |
| Translation | none |
| Reranker | none |
| Neighbor expansion | none |
| Score threshold / low-content penalty / document cap | none |

## Benchmark Identity

- `retrieval_queries_v1.jsonl` SHA256: `90aac5f98a75373fea0a0c6d04527a0e68231bd368a2d2b20fcc83ea78b71dd6`
- Manifest SHA256: `90aac5f98a75373fea0a0c6d04527a0e68231bd368a2d2b20fcc83ea78b71dd6`
- Match: **True** · Queries: **114**
- No gold mutation; the same frozen labels scored every variant.

## Artifact Verification

All 12 required artifacts present:

| artifact | bytes |
|---|---|
| `data/evaluation/retrieval_improvement_results.jsonl` | 392,990 |
| `data/evaluation/retrieval_improvement_metrics.json` | 16,031 |
| `data/evaluation/failure_transition_matrix.csv` | 2,723 |
| `data/evaluation/crosslingual_query_expansion_v1.json` | 1,308 |
| `data/evaluation/crosslingual_probe_v2.jsonl` | 30,918 |
| `data/evaluation/translation_pilot_v1.json` | 1,946 |
| `reports/retrieval_improvement_experiment.md` | 8,926 |
| `reports/retrieval_improvement_manual_review.md` | 6,157 |
| `tests/test_retrieval_improvement.py` | 15,060 |
| `data/retrieval/bm25_v1/index_stats.json` | 319 |
| `data/retrieval/bm25_v1/chunk_ids.json` | 119,878 |
| `data/retrieval/bm25_v1/vocabulary.txt` | 1,312,580 |

- `retrieval_improvement_results.jsonl`: **1140 rows = 10 variants × 114 queries**, exactly as expected. One row per variant-query holding that query's metrics and top-10 chunk IDs.

## Dense Baseline (control)

| metric | value |
|---|---|
| recall@1 | 0.4386 |
| recall@5 | 0.6842 |
| recall@10 | 0.7632 |
| recall@20 | 0.8246 |
| mrr@10 | 0.5383 |
| ndcg@10 | 0.5231 |
| doc_recall@10 | 0.8596 |

## Hybrid RRF30 Results

| metric | DENSE_V1 | HYBRID_RRF_30 | Δ |
|---|---|---|---|
| recall@1 | 0.4386 | 0.4386 | +0.0000 |
| recall@5 | 0.6842 | 0.6754 | -0.0088 |
| recall@10 | 0.7632 | 0.7895 | +0.0263 |
| recall@20 | 0.8246 | 0.8246 | +0.0000 |
| mrr@10 | 0.5383 | 0.5550 | +0.0167 |
| ndcg@10 | 0.5231 | 0.6141 | +0.0910 |
| doc_recall@10 | 0.8596 | 0.8684 | +0.0088 |

| group | DENSE_V1 | HYBRID_RRF_30 |
|---|---|---|
| TR R@10 | 0.724 | 0.759 |
| EN R@10 | 0.804 | 0.821 |
| cross-lingual R@10 | 0.167 | 0.000 |
| numeric R@10 | 0.700 | 0.800 |
| regulation R@10 | 0.455 | 0.545 |

## Bootstrap Confidence Intervals

Paired bootstrap over queries, 2000 resamples, seed pinned. Δ vs DENSE_V1.

| variant | ΔRecall@10 | ΔMRR@10 | ΔnDCG@10 |
|---|---|---|---|
| HYBRID_RRF_30 | +0.0263 [-0.0263, +0.0877] not significant | +0.0167 [-0.0525, +0.0851] not significant | +0.0910 [+0.0641, +0.1206] **significant** |
| HYBRID_RRF_60 | +0.0088 [-0.0439, +0.0614] not significant | +0.0083 [-0.0591, +0.0737] not significant | +0.0895 [+0.0627, +0.1192] **significant** |
| HYBRID_RRF_100 | +0.0088 [-0.0439, +0.0614] not significant | +0.0095 [-0.0575, +0.0737] not significant | +0.0893 [+0.0626, +0.1190] **significant** |
| BILINGUAL_HYBRID_RRF | +0.0439 [-0.0088, +0.1053] not significant | +0.0273 [-0.0412, +0.0971] not significant | +0.1026 [+0.0748, +0.1346] **significant** |
| BILINGUAL_DENSE_RRF | +0.0263 [+0.0000, +0.0614] not significant | +0.0096 [+0.0012, +0.0217] **significant** | +0.0105 [+0.0021, +0.0218] **significant** |
| RERANK_20 | +0.0351 [-0.0263, +0.0965] not significant | +0.0092 [-0.0556, +0.0724] not significant | +0.1155 [+0.0883, +0.1443] **significant** |
| RERANK_50 | +0.0263 [-0.0263, +0.0877] not significant | +0.0019 [-0.0608, +0.0635] not significant | +0.1224 [+0.0908, +0.1552] **significant** |
| BM25_V1 | -0.0526 [-0.1316, +0.0263] not significant | -0.1427 [-0.2254, -0.0584] **significant** | +0.0522 [+0.0112, +0.0965] **significant** |
| DENSE_NEIGHBOR_1 | -0.0702 [-0.1316, -0.0175] **significant** | -0.0375 [-0.0574, -0.0176] **significant** | -0.0813 [-0.1036, -0.0582] **significant** |

**This is the most important table in the closure.** For every hybrid variant, the Recall@10 and MRR@10 gains sit inside their 95% intervals — they are not distinguishable from noise on 114 queries. Only the **nDCG@10** improvement is significant (HYBRID_RRF_30: +0.0910, CI [+0.0641, +0.1206]). The honest reading is that hybrid fusion reliably improves *ranking quality across the whole list*, not top-10 hit rate.

Two variants are significantly **worse**: DENSE_NEIGHBOR_1 on all three metrics, and BM25_V1 on MRR@10 (−0.1427, CI [−0.2254, −0.0584]).

## Win / Loss

MRR@10 criterion, vs DENSE_V1.

| variant | improved | unchanged | worsened | net |
|---|---|---|---|---|
| HYBRID_RRF_30 | 30 | 59 | 25 | +5 |
| BILINGUAL_HYBRID_RRF | 33 | 57 | 24 | +9 |
| RERANK_20 | 27 | 58 | 29 | -2 |
| BM25_V1 | 22 | 42 | 50 | -28 |
| DENSE_NEIGHBOR_1 | 6 | 78 | 30 | -24 |

HYBRID_RRF_30 is net **+5** queries (30 improved, 25 worsened) — a real but modest edge, consistent with the non-significant MRR interval above.

## Failure Transition

Original DENSE_V1 failures: **27**

| mechanism | fixed |
|---|---|
| BM25_V1 | 9/27 |
| HYBRID_RRF_30 | 7/27 |
| HYBRID_RRF_60 | 6/27 |
| HYBRID_RRF_100 | 6/27 |
| BILINGUAL_DENSE_RRF | 3/27 |
| BILINGUAL_HYBRID_RRF | 9/27 |
| RERANK_20 | 9/27 |
| RERANK_50 | 7/27 |
| DENSE_NEIGHBOR_1 | 2/27 |

By original cause:

| cause | n | BM25 | HYBRID_RRF_30 | BILINGUAL_HYBRID | RERANK_20 | RERANK_50 |
|---|---|---|---|---|---|---|
| chunk_boundary | 11 | 4 | 4 | 4 | 3 | 3 |
| cross_lingual | 5 | 0 | 0 | 3 | 2 | 0 |
| embedding_semantics | 2 | 2 | 2 | 2 | 2 | 2 |
| gold_annotation_scope | 2 | 1 | 1 | 0 | 1 | 1 |
| table_numeric | 7 | 2 | 0 | 0 | 1 | 1 |

HYBRID_RRF_30 fixes 7/27, concentrated in `chunk_boundary` (4) and `embedding_semantics` (2).

**Correction to the earlier experiment report:** it argued BM25 would fix numeric/table failures. Measured, HYBRID_RRF_30 fixes **0 of 7** `table_numeric` failures. BM25 *alone* fixes 2, but fusion at k=30 dilutes that back out. The lexical-helps-numbers hypothesis is only weakly supported and should not be used to justify the choice.

## Cross-lingual Probe v2

- Queries: **27** (TR→EN **16**, EN→TR **11**) — exploratory only, **not merged** into benchmark v1 and not used to select the production retriever.

| variant | R@1 | R@5 | R@10 | MRR@10 | nDCG@10 | DocR@10 |
|---|---|---|---|---|---|---|
| DENSE_V1 | 0.037 | 0.111 | 0.259 | 0.084 | 0.041 | 0.407 |
| BM25_V1 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| HYBRID_RRF_30 | 0.000 | 0.111 | 0.111 | 0.044 | 0.023 | 0.148 |
| HYBRID_RRF_60 | 0.000 | 0.111 | 0.111 | 0.044 | 0.023 | 0.148 |

**This is a genuine regression and I am not going to bury it.** On cross-lingual queries HYBRID_RRF_30 is *worse* than the dense control (R@10 0.111 vs 0.259, DocR@10 0.148 vs 0.407). BM25 scores **0.000** across the board — a Turkish query shares no lexical tokens with English documents — and fusing that empty ranking displaces good dense hits.

The 6 cross-lingual probes in benchmark v1 were too few to expose this; 27 probes do. The mitigation is obvious and cheap (skip or down-weight the BM25 list when the query language does not match the target corpus language), but that is a design change, not a closure activity, so it is recorded as a limitation rather than implemented here.

## Translation Production Decision

`production_translation_status`: **rejected_for_v1**

LM Studio was available and tested rather than assumed (`qwen3.6-35b-a3b-mlx`, temperature 0, fixed seed):

| criterion | result |
|---|---|
| Determinism | **PASS** — 0/9 nondeterministic |
| Engineering identifier preservation | **PASS** at max_tokens=3000 (EN 1997, ASTM D1586, 351.08.07, 10-20 mm, NATM/RMR/TBM/KGM/Ovit) |
| Output reliability | **FAIL** — 9B never emits content; 35B empty for 3/9 at 700 tokens, 1/3 at 1500 |
| Latency | **FAIL** — 5.2–15.9 s per query against a 3.7 ms retrieval budget |
| Corpus terminology alignment | **FAIL** — produced *kaya çivisi* where the corpus uses *kaya bulonu* |

Evidence: `data/evaluation/translation_pilot_v1.json`.

## Bilingual Experimental Candidate

`BILINGUAL_HYBRID_RRF` — status **experimental_v2_candidate**. Best scores on benchmark v1 (R@10 0.8070, MRR 0.5656, nDCG 0.6258), and the only mechanism that fixed cross-lingual failures (3/5). Its evaluation data is retained, not deleted. Blocked solely by the translation verdict.

## Reranker Decision

**Not included in v1.** R@1 falls (0.4123 vs 0.4386), MRR gain is not significant, latency is ~100× dense search, and it requires a second ~568M model in memory. Retained as experimental evidence only.

## Neighbor Expansion Decision

**Rejected for ranking.** Significantly worse on all three metrics (R@10 0.6930, nDCG 0.4419; ΔnDCG −0.0813, CI [−0.1036, −0.0582]). It was the natural hypothesis for right-document/wrong-chunk failures and it is refuted at ranking time. A future RAG context assembler may still test neighbours for *context*, which is a different question.

## BM25 Identity and Determinism

- Chunks: **5992** · vocabulary **132,254** · rebuild **1.4s**
- Chunk ID order identical to the authoritative embedding corpus: **True** (`chunk_ids.json` hash equals the embedding release's `bge_m3_chunk_ids.json` hash)
- Second build byte-identical: **True**

| artifact | SHA256 |
|---|---|
| `index_stats.json` | `d29eb1250bcbc6e02bec4303717eea80ce4875a16472acb7b9d8ed8a145a45f6` |
| `chunk_ids.json` | `7497af0d7d7032eb4c2400f74f6f1f694ab80ce3a594be416bd66bd808cf86bd` |
| `vocabulary.txt` | `118180b535bea47b579b5833ac2912a9e9fae3a097dcc34ea0916bd378905a44` |

- Engineering identifiers survive tokenisation: `252.04`, `351.08.07`, `10-20`, `d1586`, `c30`; Turkish folding consistent (`İSTANBUL` → `istanbul`). No stemming.

## Frozen Integrity

- Protected artefacts checked: **6** · changed: **0**

| artefact | SHA256 |
|---|---|
| `data/embeddings/bge_m3_dense.npy` | `99e3b79033a996ffb08b4b742faf68ec…` |
| `data/metadata/full_embedding_manifest.csv` | `68be1f5fa0b7b6078cd9f492a8732aa7…` |
| `data/chunks/chunks.jsonl` | `e751fcfc3cc6828b05f75f494fd9a31b…` |
| `data/chunks_recovery/chunks.jsonl` | `835fc871ee53253d4d95eca14c7c13d9…` |
| `data/evaluation/retrieval_queries_v1.jsonl` | `90aac5f98a75373fea0a0c6d04527a0e…` |
| `data/evaluation/retrieval_benchmark_v1_manifest.json` | `093bdcc1b7521121e5bd369e4e9e0d87…` |

The previous no-op integrity check (`if False`) has been removed; these are real before/after comparisons and the script now exits non-zero if any protected file changes.

## Qdrant Integrity

- Collection `tunnelbook_dense_v1` exact count before: **5992**
- Exact count after: **5992**
- Unchanged: **True** · writes/deletes/upserts: **0** (read-only queries only)

## Idempotency

Deterministic components re-run (BM25 build, RRF, HYBRID_RRF_30 evaluation over all 114 queries):

| metric | saved | re-run | match |
|---|---|---|---|
| recall@1 | 0.438596 | 0.438596 | True |
| recall@5 | 0.675439 | 0.675439 | True |
| recall@10 | 0.789474 | 0.789474 | True |
| recall@20 | 0.824561 | 0.824561 | True |
| mrr@10 | 0.555002 | 0.555002 | True |
| ndcg@10 | 0.614106 | 0.614106 | True |
| doc_recall@10 | 0.868421 | 0.868421 | True |

BM25 artefacts rebuilt byte-identical. The reranker was **not** re-run for idempotency, as instructed.

## Remaining Limitations

1. **Cross-lingual regression** — the single most important caveat; see probe v2 above.
2. **Only nDCG is statistically significant.** The headline R@10 0.763→0.789 is inside the noise band.
3. **No numeric/table fix** — 0/7 despite this being a motivation for adding BM25.
4. **114 queries is small**, and the difficulty mix skews easy (48%).
5. **Right-document/wrong-chunk persists** — 11 baseline failures, only 4 fixed. This points at chunk granularity rather than retrieval, and no variant tested here addresses it.

## Final Decision

**RETRIEVAL IMPROVEMENT — CLOSED / GO**

**RECOMMENDED RETRIEVER V1: HYBRID_RRF_30**

Candidate descriptor: `data/metadata/retriever_v1_candidate.json` (`status: candidate_pending_freeze`).
