# TunnelBookAI Semantic Chunking Dry Run

## Result

**GO**

- Documents: **214/214**
- Estimated chunks: **6039**
- Metadata source: `data/metadata/final_metadata_verified_candidate.csv`
- Tokenizer: `unicode-lexical-v1` (BGE-M3 tokenizer not locally cached; no download/inference)
- Chunker: `semantic-markdown-v1.1`
- Final `chunks.jsonl` written by dry-run: **false**

## Token Distribution

- min: **3**
- p10: **53.00**
- p25: **398.00**
- median: **818.00**
- p75: **975.00**
- p90: **1180.00**
- p95: **1200.00**
- max: **7878**
- mean: **749.45**

## Size Buckets

- <250: **1225**
- 250–1200: **4513**
- 1200–1500: **111**
- >1500: **190**

## Content Types

- Table chunks: **2038**
- Formula-placeholder chunks: **129**
- Image-placeholder chunks: **3140**
- Regulation/article chunks: **188**

## Provenance

- page resolved: **4228**
- slide resolved: **566**
- section resolved: **706**
- source only: **539**

## Safety

- Dropped substantive text: **0**
- Duplicate chunk IDs: **0**
- Provenance corruption: **0**
- Table corruption: **0**
- Missing documents: **0**

## Review

- P0: **0**
- P1: **209**
- P2: **41**

## Hard-Limit Documents (P1, non-blocking)

- DOC000002
- DOC000003
- DOC000007
- DOC000015
- DOC000019
- DOC000036
- DOC000047
- DOC000048
- DOC000049
- DOC000071
- DOC000072
- DOC000075
- DOC000087
- DOC000124
- DOC000125
- DOC000158
- DOC000167
- DOC000170
- DOC000174
- DOC000175
- DOC000176
- DOC000177
- DOC000193
- DOC000196
- DOC000197
- DOC000198
- DOC000199
- DOC000200
- DOC000201
- DOC000202
- DOC000203
- DOC000204
- DOC000205
- DOC000206
- DOC000207
- DOC000208
- DOC000229
- DOC000231
- DOC000232
- DOC000235
- DOC000236
- DOC000240
- DOC000244
- DOC000267
- DOC000308

## Blockers (P0)

- Yok.

## Gate

**GO FOR STRATIFIED PILOT**

P1/P2 findings are review signals and do not gate this stage; only P0 conditions block.
