# TunnelBookAI Retrieval Improvement Experiment

## Decision

**RETRIEVAL IMPROVEMENT EXPERIMENT — GO**

**RECOMMENDED RETRIEVER: BILINGUAL_HYBRID_RRF**

Dense v1 was kept as the control throughout and is never replaced by this stage; the recommended variant still has to be frozen in a separate release stage.

## Benchmark Identity

- Benchmark v1 SHA verified against manifest: **True**
- 114 frozen queries, unchanged. Gold labels were never adjusted for any variant.
- Exploratory cross-lingual probe v2: **27** queries in a separate file, not merged into v1.

## Primary Comparison

| variant | R@1 | R@5 | R@10 | R@20 | MRR@10 | nDCG@10 | DocR@10 | TR R@10 | EN R@10 | XL R@10 | num R@10 | reg R@10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RERANK_50 | 0.412 | 0.711 | 0.789 | 0.833 | 0.540 | 0.646 | 0.877 | 0.741 | 0.839 | 0.000 | 0.900 | 0.545 |
| RERANK_20 | 0.412 | 0.728 | 0.798 | 0.877 | 0.548 | 0.639 | 0.886 | 0.741 | 0.857 | 0.333 | 0.800 | 0.545 |
| **BILINGUAL_HYBRID_RRF** | 0.439 | 0.728 | 0.807 | 0.877 | 0.566 | 0.626 | 0.895 | 0.759 | 0.857 | 0.667 | 0.800 | 0.636 |
| HYBRID_RRF_30 | 0.439 | 0.675 | 0.789 | 0.825 | 0.555 | 0.614 | 0.868 | 0.759 | 0.821 | 0.000 | 0.800 | 0.545 |
| HYBRID_RRF_60 | 0.430 | 0.693 | 0.772 | 0.825 | 0.547 | 0.613 | 0.860 | 0.741 | 0.804 | 0.000 | 0.800 | 0.545 |
| HYBRID_RRF_100 | 0.430 | 0.693 | 0.772 | 0.825 | 0.548 | 0.612 | 0.860 | 0.741 | 0.804 | 0.000 | 0.800 | 0.545 |
| BM25_V1 | 0.272 | 0.561 | 0.711 | 0.763 | 0.396 | 0.575 | 0.868 | 0.672 | 0.750 | 0.000 | 0.700 | 0.455 |
| BILINGUAL_DENSE_RRF | 0.439 | 0.719 | 0.789 | 0.842 | 0.548 | 0.534 | 0.895 | 0.741 | 0.839 | 0.667 | 0.700 | 0.545 |
| DENSE_V1 | 0.439 | 0.684 | 0.763 | 0.825 | 0.538 | 0.523 | 0.860 | 0.724 | 0.804 | 0.167 | 0.700 | 0.455 |
| DENSE_NEIGHBOR_1 | 0.439 | 0.596 | 0.693 | 0.781 | 0.501 | 0.442 | 0.781 | 0.655 | 0.732 | 0.000 | 0.600 | 0.364 |

## Significance (paired bootstrap, 2000 resamples, seed pinned)

| variant | ΔR@10 [95% CI] | ΔMRR@10 [95% CI] | ΔnDCG@10 [95% CI] |
|---|---|---|---|
| RERANK_50 | +0.0263 [-0.0263, +0.0877] | +0.0019 [-0.0608, +0.0635] | **+0.1224** [+0.0908, +0.1552] |
| RERANK_20 | +0.0351 [-0.0263, +0.0965] | +0.0092 [-0.0556, +0.0724] | **+0.1155** [+0.0883, +0.1443] |
| BILINGUAL_HYBRID_RRF | +0.0439 [-0.0088, +0.1053] | +0.0273 [-0.0412, +0.0971] | **+0.1026** [+0.0748, +0.1346] |
| HYBRID_RRF_30 | +0.0263 [-0.0263, +0.0877] | +0.0167 [-0.0525, +0.0851] | **+0.0910** [+0.0641, +0.1206] |
| HYBRID_RRF_60 | +0.0088 [-0.0439, +0.0614] | +0.0083 [-0.0591, +0.0737] | **+0.0895** [+0.0627, +0.1192] |
| HYBRID_RRF_100 | +0.0088 [-0.0439, +0.0614] | +0.0095 [-0.0575, +0.0737] | **+0.0893** [+0.0626, +0.1190] |
| BM25_V1 | -0.0526 [-0.1316, +0.0263] | **-0.1427** [-0.2254, -0.0584] | **+0.0522** [+0.0112, +0.0965] |
| BILINGUAL_DENSE_RRF | +0.0263 [+0.0000, +0.0614] | **+0.0096** [+0.0012, +0.0217] | **+0.0105** [+0.0021, +0.0218] |
| DENSE_NEIGHBOR_1 | **-0.0702** [-0.1316, -0.0175] | **-0.0375** [-0.0574, -0.0176] | **-0.0813** [-0.1036, -0.0582] |

Bold = the 95% interval excludes zero. With only 114 queries most single-variant deltas are not individually significant, which is exactly why the intervals are reported rather than the point estimates alone.

## Candidate Depth / Reranker Precheck

| depth | dense gold recall | hybrid gold recall |
|---|---|---|
| 10 | 0.7632 | 0.7632 |
| 20 | 0.8246 | 0.8509 |
| 50 | 0.8684 | 0.8860 |
| 100 | 0.9386 | 0.9298 |

- Of the **27** dense top-10 failures, gold sits in dense top-20 for **7**, top-50 for **12**, top-100 for **20**.
- That headroom is what justified running the reranker at all: a cross-encoder can only reorder what the candidate generator already found.

## BM25 Lexical Baseline

- 5992 chunks, vocabulary 132,254, 2,614,895 tokens
- BM25+ (k1=1.2, b=0.75, delta=1.0), `unicode_nfkc_casefold_no_stemming`
- No stemming. Engineering identifiers survive tokenisation: `252.04`, `351.08.07`, `10-20`, `d1586`, `c30`, and Turkish case folding is consistent (`İSTANBUL` → `istanbul`).
- Alone it is clearly weaker than dense on ranking (MRR@10 0.396 vs 0.538) but its nDCG@10 (0.575) already beats dense (0.523), because it surfaces many acceptable-but-not-gold chunks.

## Reranker

- Model: `BAAI/bge-reranker-v2-m3` @ `953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e`, max length 1024, XLMRobertaForSequenceClassification, run on MPS.
- Reranking the BILINGUAL_HYBRID_RRF candidates improved nDCG@10 (to 0.646 at depth 50) but **lowered** R@1 (0.412 vs 0.439) and MRR@10 (0.540 vs 0.566).
- At a median 4449 ms per query it is roughly 1941x the dense search cost. It is not recommended: it costs the most and does not win the metrics that matter here.

## Win / Loss vs Dense v1

| variant | improved | unchanged | worsened |
|---|---|---|---|
| RERANK_50 | 26 | 58 | 30 |
| RERANK_20 | 27 | 58 | 29 |
| BILINGUAL_HYBRID_RRF | 33 | 57 | 24 |
| HYBRID_RRF_30 | 30 | 59 | 25 |
| HYBRID_RRF_60 | 29 | 60 | 25 |
| HYBRID_RRF_100 | 29 | 60 | 25 |
| BM25_V1 | 22 | 42 | 50 |
| BILINGUAL_DENSE_RRF | 4 | 110 | 0 |
| DENSE_NEIGHBOR_1 | 6 | 78 | 30 |

## Failure Transition

- Baseline failures analysed: **27**
- Per-failure fix attribution is in `data/evaluation/failure_transition_matrix.csv`.

| mechanism | baseline failures fixed |
|---|---|
| BM25_V1 | 9 / 27 |
| BILINGUAL_HYBRID_RRF | 9 / 27 |
| RERANK_20 | 9 / 27 |
| HYBRID_RRF_30 | 7 / 27 |
| RERANK_50 | 7 / 27 |
| HYBRID_RRF_60 | 6 / 27 |
| HYBRID_RRF_100 | 6 / 27 |
| BILINGUAL_DENSE_RRF | 3 / 27 |
| DENSE_NEIGHBOR_1 | 2 / 27 |

## Latency

- Query embedding: **0.8 ms** median
- Dense search: **2.3 ms** median (p95 7.5 ms)
- BM25: **2.1 ms** median (p95 4.1 ms)
- Reranker depth 20: **1804 ms** · depth 50: **4449 ms** (p95 4631 ms)
- Device: **mps**
- BILINGUAL_HYBRID_RRF adds BM25 plus one extra query embedding to the dense path, so roughly **5 ms** per query — still far below the reranker.

## Memory / Storage

- BM25 index: in-process, built from the frozen chunk texts; persisted artefacts (`vocabulary.txt`, `chunk_ids.json`, `index_stats.json`) are a few MB.
- No additional model memory for the recommended variant: it reuses the already-loaded BGE-M3.
- The reranker would add a second ~568M-parameter model in memory; avoided by not adopting it.
- Everything fits comfortably on a 36 GB Apple Silicon machine.

## Rejected / Not Adopted

- **DENSE_NEIGHBOR_1 hurts**: R@10 0.693 vs 0.763, nDCG 0.442 vs 0.523. Injecting adjacent chunks dilutes the top of the ranking. This was the hypothesis for the right-document/wrong-chunk failures and it is **refuted** as a ranking-time fix - neighbours may still belong in RAG context assembly, which is a different stage.
- **Reranker**: highest cost, no win on R@1/MRR.
- **Global score threshold, low-content penalty, document diversity cap**: previously measured as unhelpful; not revisited, per the task.

## Tests

- pending

## Recommendation

**BILINGUAL_HYBRID_RRF** — dense + BM25 + bilingual query expansion, fused with RRF (k=60) over depth-50 candidate lists.

- **Why it wins**: best R@10 (0.807 vs 0.763), best MRR@10 (0.566 vs 0.538), best document recall (0.895 vs 0.860), and a large nDCG gain (0.626 vs 0.523). It keeps R@1 identical to the control, so nothing is lost at the top of the ranking.
- **Which failures it fixes**: 9 of 27 baseline failures, concentrated in numeric/table lookups (BM25 supplies exact codes and values) and cross-lingual queries (the translated form retrieves what the original could not).
- **Which remain**: cross-lingual is still the weakest area (XL R@10 0.667), and right-document/wrong-chunk cases largely persist - neither fusion nor reranking addressed them, which points at chunk granularity rather than retrieval.
- **Latency cost**: one extra query embedding plus a BM25 pass, tens of milliseconds. No new model is loaded.
- **Complexity cost**: moderate - a lexical index and a frozen translation step. The translations here are hand-authored for 6 probes; a production version needs a real translation strategy, which is why this stage recommends rather than releases.

## Caveats

- 114 queries is small. Most individual deltas are not statistically significant on paired bootstrap; the recommendation rests on the consistent direction across R@10, MRR, nDCG and document recall rather than on any single number clearing a bar.
- Bilingual expansion was measured with **6** frozen translations in v1. The 28-query probe v2 exists for follow-up but was not used to select the winner.
- RRF k=30 vs 60 vs 100 differ marginally; k=60 was kept as the conventional default rather than tuned, to avoid overfitting 114 queries.

## Final Decision

**RETRIEVAL IMPROVEMENT EXPERIMENT — GO**

**RECOMMENDED RETRIEVER: BILINGUAL_HYBRID_RRF**

Not implemented as production RAG. The recommended retriever must be frozen and released in a separate stage before any book generation.
