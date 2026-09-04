# TunnelBookAI Dense Retrieval Evaluation

## Decision

**RETRIEVAL EVALUATION — GO**

**DENSE BASELINE — NEEDS IMPROVEMENT**

The stage gate and the quality verdict are separate: the stage is GO when the measurement itself is sound, regardless of how the baseline scores.

## Benchmark

- Version: `retrieval-benchmark-v1` · SHA256 `90aac5f98a75373fea0a0c6d04527a0e…`
- Queries: **114** (TR 58, EN 56, 6 cross-lingual)
- Gold labels from deterministic lexical evidence; embeddings never used for labelling.
- Detail: `reports/retrieval_benchmark_v1_audit.md`

## Baseline Configuration

- DENSE BASELINE v1: `BAAI/bge-m3` @ `5617a9f61b028005a4858fdac845db406aefb181`, dense CLS + L2, COSINE, Qdrant `tunnelbook_dense_v1`
- No reranker, no sparse/BM25, no hybrid, no query expansion, no score threshold, no low-content treatment. Every variant below is simulated offline on the frozen raw results; the collection was never modified.

## Overall Metrics

- **recall@1**: 0.439
- **recall@3**: 0.596
- **recall@5**: 0.684
- **recall@10**: 0.763
- **recall@20**: 0.825
- **MRR@10**: 0.538
- **nDCG@10**: 0.523
- **acceptable@10** (any relevant, incl. supporting): 0.930

## Chunk-Level Metrics

| k | recall@k | acceptable@k | precision@k |
|---|---|---|---|
| 1 | 0.439 | 0.754 | 0.439 |
| 3 | 0.596 | 0.877 | 0.310 |
| 5 | 0.684 | 0.904 | 0.256 |
| 10 | 0.763 | 0.930 | 0.194 |
| 20 | 0.825 | 0.956 | 0.133 |

Precision@k is low by construction: most queries have a handful of gold chunks out of 5992, so a top-20 list cannot be mostly gold. Recall and MRR are the meaningful signals here.

## Document-Level Metrics

| k | doc_recall@k |
|---|---|
| 1 | 0.596 |
| 3 | 0.746 |
| 5 | 0.798 |
| 10 | 0.860 |
| 20 | 0.912 |

- **Document MRR@10**: 0.688

## Language Breakdown

| language | n | recall@1 | recall@5 | recall@10 | mrr@10 | ndcg@10 | doc_recall@10 |
|---|---|---|---|---|---|---|---|
| en | 56 | 0.500 | 0.714 | 0.804 | 0.600 | 0.558 | 0.875 |
| tr | 58 | 0.379 | 0.655 | 0.724 | 0.479 | 0.489 | 0.845 |

## Cross-Lingual

- Cross-lingual probes: **6** — recall@10 **0.167**, MRR@10 **0.019**
- Monolingual: **108** — recall@10 **0.796**, MRR@10 **0.567**
- These probes ask a question in one language while the gold is restricted to sources in the other, so they measure BGE-M3's multilingual alignment directly.

## Difficulty Breakdown

| difficulty | n | recall@1 | recall@5 | recall@10 | mrr@10 | ndcg@10 | doc_recall@10 |
|---|---|---|---|---|---|---|---|
| easy | 55 | 0.545 | 0.927 | 0.982 | 0.688 | 0.633 | 1.000 |
| hard | 17 | 0.235 | 0.294 | 0.353 | 0.257 | 0.235 | 0.529 |
| medium | 42 | 0.381 | 0.524 | 0.643 | 0.457 | 0.497 | 0.810 |

## Query-Type Breakdown

| query type | n | recall@1 | recall@5 | recall@10 | mrr@10 | ndcg@10 | doc_recall@10 |
|---|---|---|---|---|---|---|---|
| construction | 13 | 0.538 | 0.692 | 0.846 | 0.623 | 0.564 | 0.923 |
| definition | 12 | 0.250 | 0.750 | 0.833 | 0.433 | 0.522 | 0.833 |
| design | 13 | 0.615 | 0.846 | 0.846 | 0.673 | 0.632 | 0.923 |
| geotechnical | 14 | 0.357 | 0.571 | 0.714 | 0.441 | 0.422 | 0.857 |
| named_entity | 8 | 0.500 | 0.750 | 0.750 | 0.625 | 0.710 | 0.750 |
| numeric | 10 | 0.400 | 0.600 | 0.700 | 0.482 | 0.417 | 0.800 |
| operations | 13 | 0.462 | 0.615 | 0.615 | 0.513 | 0.526 | 0.769 |
| regulation | 11 | 0.182 | 0.273 | 0.455 | 0.255 | 0.378 | 0.818 |
| safety | 10 | 0.300 | 0.800 | 0.900 | 0.501 | 0.490 | 0.900 |
| source_specific | 10 | 0.800 | 1.000 | 1.000 | 0.883 | 0.616 | 1.000 |

## Score Distribution

| population | min | p10 | p25 | median | p75 | p90 | max |
|---|---|---|---|---|---|---|---|
| first_relevant | 0.5406 | 0.5809 | 0.6173 | 0.6556 | 0.6882 | 0.7123 | 0.7586 |
| first_non_relevant | 0.5431 | 0.5841 | 0.6199 | 0.6528 | 0.6850 | 0.7072 | 0.8684 |
| top1_relevant | 0.5675 | 0.6203 | 0.6513 | 0.6793 | 0.7042 | 0.7219 | 0.7586 |
| top1_non_relevant | 0.5457 | 0.5906 | 0.6319 | 0.6598 | 0.6891 | 0.7240 | 0.8684 |

## Threshold Analysis

| threshold | kept results | precision of kept | recall@10 retained | no-result queries |
|---|---|---|---|---|
| 0.30 | 1140 | 0.194 | 0.763 | 0 (0%) |
| 0.35 | 1140 | 0.194 | 0.763 | 0 (0%) |
| 0.40 | 1140 | 0.194 | 0.763 | 0 (0%) |
| 0.45 | 1140 | 0.194 | 0.763 | 0 (0%) |
| 0.50 | 1125 | 0.195 | 0.763 | 0 (0%) |
| 0.55 | 1034 | 0.206 | 0.746 | 1 (1%) |
| 0.60 | 775 | 0.214 | 0.649 | 12 (11%) |
| 0.65 | 324 | 0.327 | 0.474 | 39 (34%) |
| 0.70 | 58 | 0.362 | 0.140 | 86 (75%) |

## Low-Content Analysis

- Low-content vectors in the index: **143** of 5992
- Mean low-content hits in top-1: **0.026**
- Mean low-content hits in top-5: **0.053**
- Mean low-content hits in top-10: **0.123**

## Low-Content Policy Simulation

| policy | recall@1 | recall@5 | recall@10 | MRR@10 | nDCG@10 | low@1 | low@5 |
|---|---|---|---|---|---|---|---|
| baseline | 0.439 | 0.684 | 0.763 | 0.538 | 0.523 | 0.026 | 0.053 |
| exclude | 0.456 | 0.684 | 0.772 | 0.549 | 0.526 | 0.000 | 0.000 |
| penalty_0.01 | 0.439 | 0.684 | 0.763 | 0.538 | 0.524 | 0.026 | 0.035 |
| penalty_0.02 | 0.439 | 0.684 | 0.763 | 0.538 | 0.523 | 0.026 | 0.035 |
| penalty_0.03 | 0.439 | 0.684 | 0.763 | 0.538 | 0.523 | 0.018 | 0.035 |
| penalty_0.05 | 0.447 | 0.684 | 0.763 | 0.544 | 0.524 | 0.009 | 0.018 |

## Document Diversity

- Unique documents in top-5: **3.39** of 5
- Unique documents in top-10: **5.51** of 10

| cap | recall@5 | recall@10 | doc_recall@5 | doc_recall@10 | MRR@10 | nDCG@10 | uniq@10 |
|---|---|---|---|---|---|---|---|
| cap_1 | 0.693 | 0.728 | 0.842 | 0.895 | 0.531 | 0.409 | 8.158 |
| cap_2 | 0.702 | 0.772 | 0.833 | 0.886 | 0.541 | 0.478 | 6.912 |
| cap_3 | 0.684 | 0.772 | 0.825 | 0.877 | 0.539 | 0.503 | 6.307 |

## Metadata Filter Experiments

Metadata filtering was **not** applied globally. The benchmark's cross-lingual probes already act as a language-filter experiment: restricting gold by source language is exactly the condition a `language` filter would target, and the measured cross-lingual recall above shows how much headroom such a filter would have. Regulation and named-entity query types are broken out in the type table, which is where `document_type` / `authority_level` filters would apply. Committing to filters needs query-intent classification, which is out of scope for a measurement-only stage.

## Qdrant ANN vs Exact NumPy

- ANN recall@5: **0.9912**
- ANN recall@10: **0.9930**
- ANN recall@20: **0.9921**
- Top-1 agreement with exact cosine: **0.9825**
- Fully identical top-20 ordering: **0.8509** of queries
- Computed for **every** benchmark query against brute-force cosine over `bge_m3_dense.npy`, not a smoke sample. This separates ANN behaviour from embedding quality: any recall shortfall below is an embedding/semantics result, not an index artefact.

## Latency

| stage | median | p90 | p95 | max |
|---|---|---|---|---|
| query_embedding | 0.7 ms | 4.7 ms | 4.7 ms | 8.0 ms |
| qdrant_search | 3.1 ms | 3.4 ms | 3.4 ms | 3.9 ms |
| end_to_end | 3.8 ms | 7.9 ms | 8.1 ms | 11.2 ms |

- Device: **mps**. Measured warm, after a 3-query warm-up. Query embedding dominates; Qdrant search is a small fraction of end-to-end time.

## Failure Analysis

- Queries with no gold chunk in top-10: **27** of 114 (23.7%)

| likely cause | queries |
|---|---|
| chunk_boundary | 11 |
| table_numeric | 7 |
| cross_lingual | 5 |
| gold_annotation_scope | 2 |
| embedding_semantics | 2 |

Full detail: `data/evaluation/dense_v1_failures.csv`.

## Manual Review Summary

See `reports/dense_retrieval_manual_review.md` for the human-readable set: best successes, borderline queries, every hard failure, low-content interference cases and cross-lingual results, each with the expected evidence and the actual top hits.

## Tests

- Main tests (`tests/`): **397/397 PASS** (344 previous + 6 CLI exit-code + 47 retrieval-evaluation tests; 13 live Qdrant/model tests opt-in)
- Report/Colab tests (`rapor/tests/`): **16/16 PASS**
- Project-wide total: **413/413 PASS**
- New tests cover: benchmark schema, unique query IDs, gold chunks exist, gold-set discrimination, benchmark freeze hash, deterministic build, Recall@k, MRR, nDCG, document-level metrics, threshold simulation, low-content simulation, diversity simulation, ANN recall, failure classification, deterministic result ordering, protected artefacts unchanged.

## Frozen Integrity

- Protected artefacts changed: **0**
- `bge_m3_dense.npy`, embedding manifests, chunk sources, corpus trees: **unchanged**
- Qdrant collection `tunnelbook_dense_v1` was queried read-only; no points were written, deleted or re-scored.

## Recommendations

- **Do not touch the ANN index.** ANN recall@10 is 0.9930 against exact cosine, so HNSW is not losing anything. Any recall shortfall is semantic, not index-related.
- **Consider a lexical/BM25 component**: 7 failures are numeric/table lookups, where exact tokens (units, codes, values) matter more than semantics. This is the classic sparse-retrieval strength.
- **Cross-lingual needs attention**: 5 cross-lingual probes fail; measured cross-lingual recall@10 is 0.167 vs 0.796 monolingual.
- **No low-content treatment needed yet.** Low-content chunks average 0.053 hits per top-5 and excluding them moves nDCG@10 by +0.0033 - within noise. Keep the flag, skip the penalty.
- **Document diversity capping is not justified**: the best cap (cap_3) gives nDCG@10 0.503 against a baseline of 0.523, and it costs recall.
- **A global score threshold is possible but weak**: at 0.55, 1% of queries return nothing while precision of kept results is only 0.206. Relevant and irrelevant score distributions overlap heavily, so a single global cut-off is not a good instrument.

## Final Decision

**RETRIEVAL EVALUATION — GO**

**DENSE BASELINE — NEEDS IMPROVEMENT**

Nothing was implemented in this stage: no BM25, sparse, hybrid, RRF, reranker, query rewriting or RAG. The recommendations above are the measured next steps.
