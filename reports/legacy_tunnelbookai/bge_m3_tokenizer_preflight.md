# TunnelBookAI BGE-M3 Tokenizer Preflight

## Result

**TOKENIZER GO**

## Model / Tokenizer Identity

- Model: `BAAI/bge-m3`
- Revision (commit SHA): `5617a9f61b028005a4858fdac845db406aefb181`
- Tokenizer class: `XLMRobertaTokenizer` (fast: **True**)
- Config model type: `xlm-roberta`
- Hidden size / dense dimension: **1024**
- transformers: **5.8.1** · torch: **2.13.0**
- Tokenizer availability: **loaded successfully**, coverage **6039/6039 chunks**
- Tokenization wall time: **1.33s**

## Declared Context Limits

- `tokenizer.model_max_length`: **8192**
- `config.max_position_embeddings`: **8194** (XLM-RoBERTa reserves 2 positional offsets, so usable = **8192**)
- `sentence_bert_config.json` `max_seq_length`: **8192**
- **Effective embedding max length: 8192 tokens** (smallest declared limit governs)
- These three agree at 8192; no library-specific default silently undercuts them.

## Lexical Token Distribution (`unicode-lexical-v1`)

- min: **3**
- p10: **53.00**
- p25: **398.00**
- median: **818.00**
- p75: **975.00**
- p90: **1180.00**
- p95: **1200.00**
- p99: **3094.30**
- max: **7878**
- mean: **749.45**

## BGE-M3 Token Distribution (real tokenizer)

- min: **4**
- p10: **83.80**
- p25: **453.50**
- median: **973.00**
- p75: **1288.00**
- p90: **1519.20**
- p95: **1657.00**
- p99: **2140.34**
- max: **5176**
- mean: **899.47**

## Size Buckets (BGE-M3 tokens)

- <250: **1116**
- 250–1200: **3039**
- 1200–1500: **1209**
- 1500–8192: **675**
- >8192 (model limit): **0**

## Lexical vs BGE-M3 Ratio

- median ratio: **1.3462**
- mean ratio: **1.3326**
- p95 ratio: **1.8262**
- max ratio: **3.4545**

## Stratified Review

| Category | n | median ratio | p95 ratio | median BGE | max BGE |
|---|---|---|---|---|---|
| Turkish | 4407 | 1.466 | 1.900 | 1038 | 5176 |
| English | 1607 | 1.209 | 1.438 | 840 | 4742 |
| Undetermined language | 25 | 1.426 | 2.104 | 1012 | 2029 |
| Table chunks | 2038 | 1.078 | 1.480 | 998 | 5176 |
| Non-table chunks | 4001 | 1.487 | 1.951 | 947 | 3210 |
| URL/DOI-heavy (>=5 refs) | 47 | 1.300 | 1.694 | 1029 | 2125 |
| Regulation | 313 | 1.449 | 1.968 | 226 | 2423 |
| Formula placeholder | 129 | 1.255 | 1.600 | 1045 | 3132 |
| Image placeholder | 3140 | 1.376 | 1.668 | 1127 | 4121 |
| source_only provenance | 539 | 1.257 | 1.606 | 1336 | 3196 |
| Lexical >1500 | 190 | 0.634 | 1.476 | 1536 | 5176 |

## Truncation Audit

- Effective embedding max length: **8192**
- Longest chunk (BGE-M3): **5176 tokens**
- Headroom to limit: **3016 tokens**
- Chunks exceeding the limit: **0**
- **Silent truncation risk: 0**

Truncation is additionally disabled during measurement (`truncation=False`), so these counts are the true untruncated lengths rather than clipped ones.

## Top 30 Longest Chunks

| chunk_id | BGE-M3 | lexical | ratio | table | lang |
|---|---|---|---|---|---|
| `DOC000177-C0030` | 5176 | 4539 | 1.140 | True | tr |
| `DOC000007-C0008` | 4742 | 2981 | 1.591 | True | en |
| `DOC000007-C0001` | 4667 | 3017 | 1.547 | True | en |
| `DOC000007-C0007` | 4545 | 2900 | 1.567 | True | en |
| `DOC000007-C0009` | 4148 | 2665 | 1.556 | True | en |
| `DOC000007-C0005` | 4142 | 2662 | 1.556 | True | en |
| `DOC000176-C0003` | 4121 | 3807 | 1.082 | True | tr |
| `DOC000206-C0003` | 4121 | 3807 | 1.082 | True | tr |
| `DOC000200-C0002` | 4104 | 3806 | 1.078 | True | tr |
| `DOC000205-C0003` | 4091 | 3807 | 1.075 | True | tr |
| `DOC000007-C0004` | 3843 | 2502 | 1.536 | True | en |
| `DOC000244-C0001` | 3738 | 2551 | 1.465 | True | tr |
| `DOC000007-C0006` | 3710 | 2500 | 1.484 | True | en |
| `DOC000235-C0016` | 3567 | 3612 | 0.988 | True | tr |
| `DOC000007-C0003` | 3564 | 2557 | 1.394 | True | en |
| `DOC000235-C0018` | 3540 | 3614 | 0.980 | True | tr |
| `DOC000047-C0121` | 3425 | 2834 | 1.209 | True | en |
| `DOC000047-C0405` | 3371 | 4848 | 0.695 | True | en |
| `DOC000175-C0002` | 3311 | 3054 | 1.084 | True | tr |
| `DOC000202-C0002` | 3299 | 3054 | 1.080 | True | tr |
| `DOC000203-C0002` | 3299 | 3054 | 1.080 | True | tr |
| `DOC000048-C0061` | 3270 | 2195 | 1.490 | True | tr |
| `DOC000202-C0023` | 3210 | 1194 | 2.688 | False | tr |
| `DOC000124-C0093` | 3196 | 2833 | 1.128 | True | tr |
| `DOC000203-C0011` | 3132 | 1120 | 2.796 | False | tr |
| `DOC000235-C0004` | 3098 | 3144 | 0.985 | True | tr |
| `DOC000235-C0020` | 3012 | 3100 | 0.972 | True | tr |
| `DOC000235-C0010` | 2941 | 2962 | 0.993 | True | tr |
| `DOC000235-C0006` | 2883 | 2969 | 0.971 | True | tr |
| `DOC000048-C0059` | 2868 | 2296 | 1.249 | True | tr |

## Findings

- Turkish chunks expand markedly more than English under SentencePiece (1.466 vs 1.209 median ratio), which is the expected effect of agglutinative morphology on subword vocabularies.
- Table chunks expand least (1.078): their cells are mostly numerals and short tokens.
- Chunks above the lexical 1500 limit have a median ratio of 0.634 — **below 1.0**. These are dot-leader tables of contents where `unicode-lexical-v1` counted every punctuation glyph separately while SentencePiece merges the runs. The lexical count overstated them; under the real tokenizer they are smaller, not larger.
- 58 chunks (0.96%) across 3 documents contain dense control-character residue from failed glyph extraction. This predates chunking and is a corpus-quality issue, not a tokenizer one — see Warnings.

## Determinism

- Second tokenization pass identical: **PASS**

## Recut Policy

- Chunks requiring recut: **0**
- No recut is recommended or performed. The recut triggers are a substantive chunk over the real effective limit, or silent library truncation; neither occurs. Exceeding the *lexical* 1500 guideline is explicitly not a recut trigger, and the 190 atomic table chunks were measured as-is.

## Blockers

- Yok.

## Decision

**TOKENIZER GO**
