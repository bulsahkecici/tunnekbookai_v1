# TunnelBookAI Retrieval Benchmark v1 Audit

## Result

**BENCHMARK VALID**

## Composition

- Total queries: **114**
- Turkish: **58** (51%)
- English: **56** (49%)
- Cross-lingual probes: **6**

### By query type

- construction: **13**
- definition: **12**
- design: **13**
- geotechnical: **14**
- named_entity: **8**
- numeric: **10**
- operations: **13**
- regulation: **11**
- safety: **10**
- source_specific: **10**

### By difficulty

- easy: **55** (48%)
- hard: **17** (15%)
- medium: **42** (37%)

Difficulty is **derived, not hand-assigned**: it counts how many of the query's content words actually appear in the gold chunks' headings (2+ = easy, 1 = medium, 0 = hard); cross-lingual probes are hard by construction. The realised split (48% / 37% / 15%) is easier than the 30/45/25 target. I kept the measured labels rather than reweighting to hit the target, because forcing the distribution would have meant mislabelling queries.

### By annotation method

- `body_density_anchor`: **8**
- `body_presence_anchor`: **2**
- `heading_anchor`: **98**
- `heading_anchor_language_restricted`: **6**

## Gold Label Safety

- Gold was resolved by **deterministic lexical anchors over source text**. Embedding similarity was never consulted, so the benchmark is not circular with the system under test.
- `heading_anchor`: the chunk's own heading/section path matches the anchor - the section is titled about the topic.
- `body_density_anchor`: no section in the corpus is titled for the concept, so repeated in-body occurrence is used instead. Weaker, and recorded per query.
- `body_presence_anchor`: last resort, plain presence. Used for 2 queries.
- `*_language_restricted`: gold confined to one source language, for cross-lingual probes.
- Every row carries `source_evidence` with the matched snippet, so each label is inspectable.

## Gold Set Sizes

- Gold chunks per query - min **1**, median **7**, p90 **37**, max **154**
- Gold documents per query - median **4**
- An earlier draft matched anchors anywhere in the text and produced a median of 94 and a maximum of 1832 gold chunks per query - about a third of the corpus. Recall@10 would have been trivially ~1.0. Requiring heading-level evidence brought this down to a median of 7, which is what makes the metrics discriminating.

## Validation

- Queries with no gold: **0**
- Duplicate query IDs: **0** · duplicate query text: **0**
- Gold chunks missing from the Qdrant release: **0**
- Gold documents missing: **0**
- Queries reused from earlier smoke tests: **0** (limit 15%)

## Freeze

- `benchmark_version`: `retrieval-benchmark-v1`
- `sha256`: `90aac5f98a75373fea0a0c6d04527a0e68231bd368a2d2b20fcc83ea78b71dd6`
- Query file: `data/evaluation/retrieval_queries_v1.jsonl`
- Frozen before results were inspected. A genuine annotation error found later becomes v2 rather than a silent edit to v1.
