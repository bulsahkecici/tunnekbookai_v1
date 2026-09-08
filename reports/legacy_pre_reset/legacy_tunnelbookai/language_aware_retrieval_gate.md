# TunnelBookAI Language-Aware Retrieval Gate

## Decision

**LANGUAGE-AWARE RETRIEVAL — NO-GO**

**RECOMMENDED RETRIEVER V1: DENSE_V1**

Goal: keep HYBRID_RRF_30's monolingual ranking gain without its cross-lingual collapse. No translation, no LLM, no new model.

## Language Detector

- Version: `corpus-logodds-lang-v1` — corpus-derived log-odds, built from the indexed chunks themselves. Nothing downloaded.
- Rules were fixed before any variant metric was computed: technical tokens (acronyms, codes, numbers) carry no language evidence; a Turkish diacritic is decisive; otherwise |log-odds| must reach 2.0 or the verdict is `unknown`.

- Audit set: **50** queries (40 language, 10 technical/ambiguous)
- Correct: **40/40** (accuracy **1.000**) · incorrect: **0** · abstained: **0**
- Technical-only queries correctly returned `unknown`: **10/10** · misclassified: **0**
- `TBM`, `NATM RMR GSI`, `EN 1997`, `ASTM D1586`, `KGM`, `351.08.07` all abstain rather than guess, which is what routes them to the dense-only path.
- Evidence: `data/evaluation/language_detector_audit.jsonl`

## Variants

| variant | policy |
|---|---|
| DENSE_V1 | control: dense top-50, no lexical |
| HYBRID_RRF_30 | control: dense top-50 + BM25 top-50 (whole corpus), RRF k=30 |
| LANG_HYBRID_SAME_RRF30 | BM25 restricted to same-language chunks, RRF k=30; unknown → dense |
| LANG_HYBRID_SAME_RRF60 | as above, RRF k=60 |
| LANG_HYBRID_GATED_RRF30 | same-language BM25 enters RRF only if ≥2 distinct non-technical query terms occur in that sub-corpus; otherwise dense unchanged |
| LANG_HYBRID_DENSE_PROTECTED_3 / _5 | dense top-3 / top-5 pinned, remainder fused |

## Frozen Benchmark v1 (114 queries)

| variant | recall@1 | recall@5 | recall@10 | recall@20 | mrr@10 | ndcg@10 | doc_recall@10 |
|---|---|---|---|---|---|---|---|
| DENSE_V1 | 0.439 | 0.684 | 0.763 | 0.825 | 0.538 | 0.523 | 0.860 |
| HYBRID_RRF_30 | 0.439 | 0.675 | 0.789 | 0.825 | 0.555 | 0.614 | 0.868 |
| LANG_HYBRID_SAME_RRF30 | 0.412 | 0.632 | 0.746 | 0.816 | 0.524 | 0.589 | 0.825 |
| LANG_HYBRID_SAME_RRF60 | 0.404 | 0.649 | 0.728 | 0.816 | 0.516 | 0.587 | 0.816 |
| LANG_HYBRID_GATED_RRF30 | 0.412 | 0.632 | 0.746 | 0.816 | 0.524 | 0.589 | 0.825 |
| LANG_HYBRID_DENSE_PROTECTED_3 | 0.439 | 0.728 | 0.772 | 0.825 | 0.545 | 0.581 | 0.860 |
| LANG_HYBRID_DENSE_PROTECTED_5 | 0.439 | 0.684 | 0.772 | 0.825 | 0.541 | 0.571 | 0.860 |

## Monolingual Subset (108 queries)

This is where hybrid's advantage has to survive.

| variant | recall@10 | mrr@10 | ndcg@10 |
|---|---|---|---|
| DENSE_V1 | 0.796 | 0.567 | 0.551 |
| HYBRID_RRF_30 | 0.833 | 0.586 | 0.648 |
| LANG_HYBRID_SAME_RRF30 | 0.787 | 0.553 | 0.622 |
| LANG_HYBRID_SAME_RRF60 | 0.769 | 0.545 | 0.619 |
| LANG_HYBRID_GATED_RRF30 | 0.787 | 0.553 | 0.622 |
| LANG_HYBRID_DENSE_PROTECTED_3 | 0.815 | 0.575 | 0.612 |
| LANG_HYBRID_DENSE_PROTECTED_5 | 0.815 | 0.571 | 0.602 |

## Cross-lingual Probe v2 (27 queries, exploratory)

TR→EN and EN→TR probes. Gold untouched; never merged into benchmark v1.

| variant | recall@1 | recall@5 | recall@10 | mrr@10 | ndcg@10 | doc_recall@10 |
|---|---|---|---|---|---|---|
| DENSE_V1 | 0.037 | 0.111 | 0.259 | 0.084 | 0.041 | 0.407 |
| HYBRID_RRF_30 | 0.000 | 0.111 | 0.111 | 0.044 | 0.023 | 0.148 |
| LANG_HYBRID_SAME_RRF30 | 0.000 | 0.074 | 0.074 | 0.017 | 0.007 | 0.148 |
| LANG_HYBRID_SAME_RRF60 | 0.000 | 0.037 | 0.074 | 0.014 | 0.006 | 0.148 |
| LANG_HYBRID_GATED_RRF30 | 0.000 | 0.074 | 0.074 | 0.017 | 0.007 | 0.148 |
| LANG_HYBRID_DENSE_PROTECTED_3 | 0.037 | 0.074 | 0.074 | 0.056 | 0.014 | 0.148 |
| LANG_HYBRID_DENSE_PROTECTED_5 | 0.037 | 0.111 | 0.111 | 0.063 | 0.019 | 0.185 |

## Selection

Predeclared criteria: keep at least half of hybrid's monolingual nDCG gain over dense, **and** restore probe v2 recall@10 to at least the dense level.

| variant | monolingual nDCG@10 | probe v2 R@10 | keeps gain | restores cross-lingual | qualifies |
|---|---|---|---|---|---|
| LANG_HYBRID_GATED_RRF30 | 0.6218 | 0.074 | True | False | no |
| LANG_HYBRID_SAME_RRF30 | 0.6218 | 0.074 | True | False | no |
| LANG_HYBRID_SAME_RRF60 | 0.6193 | 0.074 | True | False | no |
| LANG_HYBRID_DENSE_PROTECTED_3 | 0.6123 | 0.074 | True | False | no |
| LANG_HYBRID_DENSE_PROTECTED_5 | 0.6016 | 0.111 | True | False | no |

## Group Breakdown (benchmark v1)

| variant | TR R@10 | EN R@10 | numeric R@10 | regulation R@10 |
|---|---|---|---|---|
| DENSE_V1 | 0.724 | 0.804 | 0.700 | 0.455 |
| HYBRID_RRF_30 | 0.759 | 0.821 | 0.800 | 0.545 |
| LANG_HYBRID_SAME_RRF30 | 0.741 | 0.750 | 0.800 | 0.545 |
| LANG_HYBRID_SAME_RRF60 | 0.724 | 0.732 | 0.800 | 0.545 |
| LANG_HYBRID_GATED_RRF30 | 0.741 | 0.750 | 0.800 | 0.545 |
| LANG_HYBRID_DENSE_PROTECTED_3 | 0.741 | 0.804 | 0.800 | 0.455 |
| LANG_HYBRID_DENSE_PROTECTED_5 | 0.759 | 0.786 | 0.800 | 0.455 |

## Failure Transition (original 27 dense failures)

| variant | fixed |
|---|---|
| DENSE_V1 | 0/27 |
| HYBRID_RRF_30 | 7/27 |
| LANG_HYBRID_SAME_RRF30 | 6/27 |
| LANG_HYBRID_SAME_RRF60 | 5/27 |
| LANG_HYBRID_GATED_RRF30 | 6/27 |
| LANG_HYBRID_DENSE_PROTECTED_3 | 5/27 |
| LANG_HYBRID_DENSE_PROTECTED_5 | 4/27 |

| cause | DENSE_V1 | HYBRID_RRF_30 | LANG_HYBRID_SAME_RRF30 | LANG_HYBRID_SAME_RRF60 | LANG_HYBRID_GATED_RRF30 | LANG_HYBRID_DENSE_PROTECTED_3 | LANG_HYBRID_DENSE_PROTECTED_5 |
|---|---|---|---|---|---|---|---|
| chunk_boundary | 0 | 4 | 3 | 3 | 3 | 2 | 2 |
| embedding_semantics | 0 | 2 | 2 | 2 | 2 | 2 | 2 |
| gold_annotation_scope | 0 | 1 | 1 | 0 | 1 | 1 | 0 |

## Latency

| stage | median | p95 |
|---|---|---|
| detect | 0.01 ms | 0.02 ms |
| query_embedding | 0.79 ms | 5.88 ms |
| dense | 2.00 ms | 2.43 ms |
| bm25 | 2.64 ms | 5.16 ms |
| **total (est.)** | **5.4 ms** | — |

Language detection is a dictionary lookup over query tokens, so it adds effectively nothing. No LLM is involved anywhere in this path.

## Integrity

- Protected artefacts changed: **0**
- Qdrant `tunnelbook_dense_v1` exact count: **5992 → 5992**, read-only queries, zero writes
- Benchmark v1 and probe v2 gold unchanged; `retriever_v1_candidate.json` not overwritten
- Routing metadata written additively to `data/retrieval/language_routing_v1/`; the core `bm25_v1` index was not mutated

## No Gold Leakage

Routing consumes only the query string, the corpus-derived detector, chunk `language` metadata and retrieval ranks. Gold labels, gold languages and benchmark annotations are never read at routing time — the cross-lingual probes are routed by the same detector as everything else.

## Tests

- Main tests (`tests/`): **466/466 PASS**
- Report/Colab tests (`rapor/tests/`): **16/16 PASS**
- Project-wide total: **482/482 PASS**
- New: 26 language-aware tests (detector determinism, TR/EN detection, acronym→unknown, no gold leakage, same-language BM25 filtering, unknown→dense fallback, RRF determinism, dense protection, benchmark v1 + probe v2 unchanged, Qdrant read-only, protected artefacts unchanged)

## Final Decision

**LANGUAGE-AWARE RETRIEVAL — NO-GO**

**RECOMMENDED RETRIEVER V1: DENSE_V1**
