# TunnelBookAI Semantic Chunking Audit

## Result

**GO**

## Documents

- Documents: **214/214**
- Metadata source: `data/metadata/final_metadata_verified_candidate.csv`

## Chunks

- Total: **6039**
- Duplicate chunk IDs: **0**

## Distribution

- min: **3**
- p10: **53.00**
- p25: **398.00**
- median: **818.00**
- p75: **975.00**
- p90: **1180.00**
- p95: **1200.00**
- max: **7878**
- mean: **749.45**

- Under 250: **1225**
- 250–1200: **4513**
- 1200–1500: **111**
- Over 1500: **190**

## By Source Type

- .doc: **10**
- .docx: **857**
- .jpg: **2**
- .pdf: **4346**
- .png: **1**
- .ppt: **421**
- .pptm: **4**
- .pptx: **373**
- .rtf: **1**
- .xls: **20**
- .xlsx: **4**

## By Document Type

- academic_article: **297**
- book_or_book_chapter: **71**
- conference_paper: **165**
- cost_analysis: **5**
- drawing: **5**
- inventory: **150**
- magazine: **1046**
- manual: **682**
- presentation: **140**
- project_document: **56**
- regulation: **313**
- spreadsheet: **24**
- standard: **5**
- technical_specification: **485**
- thesis: **244**
- training_material: **1815**
- unresolved: **510**
- web_article: **26**

## Semantic Structures

- Tables: **2038**
- Lists: **2266**
- Regulations: **188**
- Formula placeholders: **129**
- Image placeholders: **3140**

## Provenance

- page resolved: **4228**
- slide resolved: **566**
- section resolved: **706**
- source only: **539**

## Conservation

- Dropped substantive text: **0**
- Source body characters: **24656658**
- Total chunk characters: **24656658**
- Overlap characters: **0**
- Duplication ratio: **0.000000**
- Overlap ratio: **0.000000**

## Integrity

- Normalized corpus changed: **false**
- Raw corpus changed: **false**
- Markdown trees changed: **false**
- Metadata protected files changed: **0**
- Missing documents: **0**
- Duplicate IDs: **0**
- Provenance corruption: **0**
- Table corruption: **0**

## Review

- P0: **0**
- P1: **209**
- P2: **41**

## DOC000021 Hard-Limit Status

- Chunks: **26**
- Chunks over hard limit (1500): **0**
- Largest chunk: **1497 tokens**
- The earlier P1 hard-limit finding is **resolved**: the oversized block was a numbered
  reference list, which `enforce_hard_limit` now divides at list-item/line boundaries.
  No table was split, no citation anchor changed, and no substantive text was dropped.
- Dropped substantive text: **0**

## Pilot

- Selected: **15/15**
- Passed: **15/15**

## Tests

- Main tests (`tests/`): **190/190 PASS**
- Report/Colab tests (`rapor/tests/`): **16/16 PASS**
- Project-wide total: **206/206 PASS**
- Executed on the native macOS venv (`.venv`, Python 3.12.14); no Windows site-packages fallback.

## Idempotency

- Deterministic second-run hash: **PASS**

## Warnings

- Nonblocking P1/P2 review records: **250**
- Token counts were produced with `unicode-lexical-v1` because the BGE-M3 tokenizer was not in the local cache; nothing was downloaded and no inference was run. Chunk boundaries are NOT re-cut for this reason and stay as audited here. **Action for the embedding stage:** run a separate BGE-M3 tokenizer compatibility preflight over `data/chunks/chunks.jsonl` to re-measure the true token distribution before indexing. Expect drift on the tails — subword tokenization of Turkish morphology and of URL/DOI-dense reference chunks will read longer than the lexical count, so the >1500-token band may widen. Re-cut only if that preflight shows real breaches.
- No embeddings, BGE-M3 download or inference, Qdrant, retrieval, reranking, RAG or LLM generation were run at any point in this stage.
- Overlap is deliberately 0 tokens: boundaries fall on heading/regulation/paragraph/list edges, so chunks already carry their own semantic context. Chunk text concatenates back to the source byte for byte, which is what proves dropped-text = 0. Blind or fixed overlap would forfeit that proof and inflate the corpus; `overlap_previous_tokens` is carried in the schema for later tuning. 5465/6039 chunks carry a resolved section path.
- 1225 chunks fall under the 250-token soft minimum. These are short-by-nature units (slide bodies, figure/caption blocks, brief regulation articles) that coalescing kept whole rather than fusing across a citation boundary; none is a non-substantive fragment.

## Blockers

- Yok.

## Final Decision

**GO**
