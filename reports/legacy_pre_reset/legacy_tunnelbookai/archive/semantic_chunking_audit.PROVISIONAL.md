# TunnelBookAI Semantic Chunking Audit

## Result

**GO**

## Documents

- Documents: **214/214**
- Metadata source: `data/metadata/final_metadata_verified_candidate.csv`

## Chunks

- Total: **18179**
- Duplicate chunk IDs: **0**

## Distribution

- min: **1**
- p10: **10.00**
- p25: **32.00**
- median: **94.00**
- p75: **286.00**
- p90: **715.00**
- p95: **1104.10**
- max: **7833**
- mean: **248.96**

- Under 250: **13162**
- 250–1200: **4718**
- 1200–1500: **109**
- Over 1500: **190**

## By Source Type

- .doc: **10**
- .docx: **1238**
- .jpg: **6**
- .pdf: **15913**
- .png: **3**
- .ppt: **515**
- .pptm: **5**
- .pptx: **464**
- .rtf: **1**
- .xls: **20**
- .xlsx: **4**

## By Document Type

- academic_article: **578**
- book_or_book_chapter: **319**
- conference_paper: **341**
- cost_analysis: **30**
- drawing: **40**
- inventory: **319**
- magazine: **3710**
- manual: **1639**
- presentation: **399**
- project_document: **206**
- regulation: **705**
- spreadsheet: **24**
- standard: **11**
- technical_specification: **2922**
- thesis: **303**
- training_material: **5021**
- unresolved: **1553**
- web_article: **59**

## Semantic Structures

- Tables: **2371**
- Lists: **3681**
- Regulations: **188**
- Formula placeholders: **184**
- Image placeholders: **5811**

## Provenance

- page resolved: **15743**
- slide resolved: **664**
- section resolved: **1233**
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
- Metadata protected files changed: **0**
- Missing documents: **0**
- Duplicate IDs: **0**

## Review

- P0: **0**
- P1: **259**
- P2: **41**

## Pilot

- Selected: **15/15**
- Passed: **15/15**

## Tests

- Tests pending after gated semantic chunking run

## Idempotency

- Deterministic second-run hash: **PASS**

## Warnings

- Nonblocking P1/P2 review records: **300**
- BGE-M3 tokenizer was not locally cached; deterministic Unicode lexical tokenizer abstraction was used.
- No embeddings, Qdrant, RAG or LLM generation were run.

## Blockers

- Yok.

## Final Decision

**GO**
