# TunnelBookAI BGE-M3 Embedding Preflight Audit

## Result

**BGE-M3 EMBEDDING PREFLIGHT — GO**

This stage measured and piloted only. No full embedding run, vector database, retrieval or RAG was started.

## Environment

- Machine: MacBook Pro, Apple Silicon (arm64), 36 GB unified memory
- Environment: native `.venv` (no Windows site-packages fallback, no CUDA)
- torch: **2.13.0** · transformers: **5.8.1**
- `pip check`: **No broken requirements found**
- Dependencies added: **none** — `torch`, `transformers`, `tokenizers`, `huggingface_hub`, `numpy` and `safetensors` were already present, so no new framework was installed and no existing project dependency was disturbed. `sentence-transformers`/`FlagEmbedding` were deliberately not installed: BGE-M3 dense is CLS pooling plus L2 normalization, which plain `transformers` reproduces exactly.

## Model

- Model: `BAAI/bge-m3`
- Revision (commit SHA): `5617a9f61b028005a4858fdac845db406aefb181`
- Architecture: `xlm-roberta` / `XLMRobertaModel`, 567.75M parameters
- Tokenizer class: `XLMRobertaTokenizer` (fast: True)
- Model files are served from the standard Hugging Face cache; nothing was written into the project corpus.

## Tokenizer Compatibility

- Coverage: **6039/6039 chunks** tokenized with the real tokenizer
- Tokenizer stage decision: **TOKENIZER GO**
- Full detail: `reports/bge_m3_tokenizer_preflight.md`

## Token Statistics

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

- Median lexical→BGE-M3 ratio: **1.3462**
- Mean ratio: **1.3326** · p95: **1.8262** · max: **3.4545**

## Model Max Length

- `tokenizer.model_max_length`: **8192**
- `config.max_position_embeddings`: **8194** (usable **8192**)
- `sentence_bert_config.json` `max_seq_length`: **8192**
- **Effective: 8192**

## Truncation Risk

- Chunks over effective max length: **0**
- Longest chunk: **5176** tokens · headroom **3016**
- Measurement ran with `truncation=False`, so no length was hidden by clipping.
- **Silent truncation: 0**

## Pilot Selection

- Selected: **100** chunks (deterministic stratified selection, no randomness)
- Distinct documents covered: **35**
- Pilot token volume: **92445** BGE-M3 tokens

| category | chunks |
|---|---|
| academic | 6 |
| english | 8 |
| formula | 5 |
| image_placeholder | 1 |
| longest_safe | 8 |
| manual | 6 |
| median_sized | 8 |
| p90_sized | 8 |
| short | 8 |
| source_only | 3 |
| table | 3 |
| topup | 23 |
| turkish | 8 |
| url_doi_heavy | 5 |

## Embedding Dimension

- Vector dimension: **1024** (matches `config.hidden_size` 1024, resolved from the model, not assumed)
- Vectors produced: **100**
- Pooling: **CLS token** (`1_Pooling/config.json` → `pooling_mode_cls_token: true`)
- Normalization: **normalize_embeddings=true**. This is the model's own documented behaviour — `modules.json` declares a `2_Normalize` module — not a library default taken on faith. It makes cosine similarity equal to a dot product, which is what the retrieval stage will use.
- Query prefix: **none** · Document prefix: **none**. The official model card states BGE-M3 "no longer requires adding instructions to the queries", so no prefix was invented.

## Device

- Device used: **mps**
- CUDA was not used and is unavailable; Apple Silicon MPS was used with CPU fallback available.

## Performance

- Model load: **1.1s**
- Pilot embedding: **10.3s** for 100 chunks
- Throughput: **9.67 chunks/sec**, **8937 tokens/sec**
- Extrapolated full-corpus estimate: **~10.4 minutes** for 6039 chunks (indicative only; the pilot is length-stratified, so the real run may differ).
- Peak process memory: **~1.46 GB** of 36 GB unified

## Semantic Sanity Queries

Top-5 nearest pilot chunks per query. This is a smoke test for obvious semantic failure, not a retrieval benchmark: the pool is only ~100 stratified chunks, so absolute scores matter less than whether the ranking is topically coherent.

### `NATM support systems`

- **0.4909** `DOC000003-C0001` (academic) — <!-- Docling chunk 1/8 --> <!-- original_page_start: 1 --> <!-- original_page_end: 25 --> <!-- citation_rule: original_page = original_page_start + chunk_local_
- **0.4825** `DOC000007-C0009` (longest_safe) — ## XXII Table of Contents | 11 | DAUB recommendations for the selection of tunnelling machines . . . . . . . . | DAUB recommendations for the selection of tunne
- **0.4686** `DOC000061-C0001` (source_only) — ITU Yüksek Lisans Tez [https://nek.istanbul.edu.tr/ekos/TEZ/37091.pdf](https://nek.istanbul.edu.tr/ekos/TEZ/37091.pdf) 19 Mayıs Üniversitesi 14. Hafta Ders Notl
- **0.4638** `DOC000003-C0003` (academic) — ## NOTICE The project that is the subject of this report was a part of the Transit Cooperative Research Program conducted by the Transportation Research Board w
- **0.4552** `DOC000003-C0004` (academic) — ## NOTICE The project that is the subject of this report was a part of the National Cooperative Highway Research Program conducted by the Transportation Researc

### `tunnel ventilation`

- **0.5810** `DOC000023-C0001` (source_only) — [https://tunnelsmanual.piarc.org/en/strategy-and-general-design-strategic-issues/tunnel-complex-system](https://tunnelsmanual.piarc.org/en/strategy-and-general-
- **0.5568** `DOC000001-C0009` (table) — | Luminance | (cd/m 2 ) | |-------------|-------------| | L seq | 169 | | L atm | 324 | | L par | 33 | | L cru | 33 | Table 12 Average luminance coefficients (U
- **0.5440** `DOC000001-C0010` (table) — ## 3.2. Lighting systems design results According to the standard UNI 11095 (2011), the minimum luminance curve is the target standard curve for a specific ligh
- **0.5421** `DOC000003-C0006` (academic) — ## F O R E W O R D By S. A. Parker Staff Officer Transportation Research Board This twelfth volume of both NCHRP Report 525: Surface Transportation Security and
- **0.5347** `DOC000001-C0008` (english) — ## 3.1. Materials and methods The lighting system for the tunnel was designed with lightemitting diodes or LEDs, according to the characteristics provided by th

### `rock bolt design`

- **0.4437** `DOC000206-C0010` (p90_sized) — ## ABSTRACT Vertical or inclined shafts were excavated by drilling-blasting or manual methods in the past; however, nowadays specialpurpose machines developed f
- **0.4294** `DOC000087-C0368` (median_sized) — ## Tablo-408-7 Mineral Elyaf Özellikleri | Fiber Uzunluğu (maksimum) | 6 mm | |---------------------------------|-------------| | No.40 (0,425 mm) elekten geçen
- **0.4267** `DOC000011-C0008` (formula) — ## The TBM Competitiveness formula 32 The TBM Competitiveness formula captures the ratio between the length and diameter of the tunnel and the unconfined compre
- **0.4083** `DOC000007-C0001` (longest_safe) — <!-- Docling chunk 1/1 --> <!-- original_page_start: 1 --> <!-- original_page_end: 16 --> <!-- citation_rule: original_page = original_page_start + chunk_local_
- **0.4053** `DOC000198-C0048` (p90_sized) — ## İSKİ Avrupa 1. Bölge Tünel Projesİ (Ayvalıdere Atıksu Tünelİ) ## Istanbul Water and Sewerage Administration (ISKI) European Area 1 Tunnel Project (Ayvalıdere

### `tunnel maintenance inspection`

- **0.6562** `DOC000015-C0001` (manual) — <!-- Docling chunk 1/11 --> <!-- original_page_start: 1 --> <!-- original_page_end: 25 --> <!-- citation_rule: original_page = original_page_start + chunk_local
- **0.6521** `DOC000002-C0001` (short) — <!-- Docling chunk 1/5 --> <!-- original_page_start: 1 --> <!-- original_page_end: 25 --> <!-- citation_rule: original_page = original_page_start + chunk_local_
- **0.5928** `DOC000002-C0007` (short) — ## (3) Tunnel Management Office Operator Tunnel Management Office should be operated and managed by DOR. Since this is the first tunnel construction project in 
- **0.5920** `DOC000013-C0004` (formula) — ## 2. Data Te source of the routine maintenance of tunnels data used in this study was provided by Shaanxi Transportation Holding Group (STHG), over the fscal y
- **0.5877** `DOC000012-C0002` (manual) — *Note: these diagrams show how important the operation and maintenance costs are and how it is necessary to choose from the first stages of the tunnel design th

### `TBM excavation`

- **0.5964** `DOC000011-C0008` (formula) — ## The TBM Competitiveness formula 32 The TBM Competitiveness formula captures the ratio between the length and diameter of the tunnel and the unconfined compre
- **0.5902** `DOC000206-C0010` (p90_sized) — ## ABSTRACT Vertical or inclined shafts were excavated by drilling-blasting or manual methods in the past; however, nowadays specialpurpose machines developed f
- **0.5422** `DOC000198-C0048` (p90_sized) — ## İSKİ Avrupa 1. Bölge Tünel Projesİ (Ayvalıdere Atıksu Tünelİ) ## Istanbul Water and Sewerage Administration (ISKI) European Area 1 Tunnel Project (Ayvalıdere
- **0.4984** `DOC000007-C0009` (longest_safe) — ## XXII Table of Contents | 11 | DAUB recommendations for the selection of tunnelling machines . . . . . . . . | DAUB recommendations for the selection of tunne
- **0.4912** `DOC000047-C0098` (median_sized) — ## 5.4.1.1 Structural Element Sizing As described in Chapter 1, the shape of the cut and cover tunnels is generally rectangular. The dimensions of the rectangul

### `tunnel fire safety`

- **0.5980** `DOC000167-C0010` (topup) — Türkiye'deki Karayolu Tünellerinde Trafik Güvenliği
- **0.5934** `DOC000003-C0036` (url_doi_heavy) — ## References Anderson, T. &amp; B.J. Paaske (2002). 'Safety in Railway Tunnels and Selection of Tunnel Concept.' Paper presented at the ESReDA 23rd Seminar, No
- **0.5680** `DOC000003-C0006` (academic) — ## F O R E W O R D By S. A. Parker Staff Officer Transportation Research Board This twelfth volume of both NCHRP Report 525: Surface Transportation Security and
- **0.5678** `DOC000003-C0033` (url_doi_heavy) — ## References 'Arsonist Jailed for Life Over Subway Deaths.'(2003,Aug.7). The Age . Available: http://www.theage.com.au/articles/2003/ 08/06/1060145722512.html 
- **0.5560** `DOC000001-C0002` (english) — ## a b s t r a c t This work computes and compares the life cycle costs of two different road tunnel pavements and their corresponding lighting systems. The stu

### `geological investigation`

- **0.5505** `DOC000007-C0005` (longest_safe) — | 4.4 | Geophysical exploration ahead of the face . . . . . . . . . . . . . . . . . . . . . . . . . . . . | Geophysical exploration ahead of the face . . . . . 
- **0.5471** `DOC000124-C0002` (p90_sized) — - 9.1. Giriş ve Çalışmanın Amacı 74 - 9.2. İnceleme Alanının Jeolojisi 76 - 9.2.2. Genel Jeoloji 77 - 9.2.3. Güzergah Jeolojisi 79 - 9.2.4. Yapısal Jeoloji 80 -
- **0.5159** `DOC000071-C0029` (median_sized) — | Km: 5 + 963 40 - 6 + 066 00 ( Hat-2) | | | | | | | | | | | | | | |--------------------------------------------------------------------------------------------
- **0.4992** `DOC000007-C0008` (longest_safe) — | 8.4 | Transport, storage and handling of explosives . . . . . . . . . . . . . . . . . . . . . . . . . | Transport, storage and handling of explosives . . . . 
- **0.4935** `DOC000007-C0001` (longest_safe) — <!-- Docling chunk 1/1 --> <!-- original_page_start: 1 --> <!-- original_page_end: 16 --> <!-- citation_rule: original_page = original_page_start + chunk_local_

### `shotcrete`

- **0.3847** `DOC000170-C0015` (topup) — 6. 7.
- **0.3690** `DOC000036-C0002` (turkish) — MADDE 1- (1) Grizu gazı ve/veya yanıcı gazlar veya tozlar nedeniyle muhtemel patlayıcı ortama sahip yeraltı kömür ocakları ile bu tip madenlerin yerüstü tesisle
- **0.3581** `DOC000302-C0101` (topup) — ## Slayt 105 BURSA 11-15 KASIM 2013
- **0.3435** `DOC000007-C0007` (longest_safe) — | XX | Table of Contents | Table of Contents | | |------|-------------------------------------------------------------------------------------------------------
- **0.3373** `DOC000036-C0001` (turkish) — <!-- Docling chunk 1/4 --> <!-- original_page_start: 1 --> <!-- original_page_end: 25 --> <!-- citation_rule: original_page = original_page_start + chunk_local_

### `tunnel construction cost`

- **0.6680** `DOC000012-C0001` (manual) — **COSTS OF CONSTRUCTION, OPERATION, UPGRADING - FINANCIAL ASPECTS** - [**1. Foreword**](https://tunnelsmanual.piarc.org/en/strategy-and-general-design-strategic
- **0.6115** `DOC000002-C0007` (short) — ## (3) Tunnel Management Office Operator Tunnel Management Office should be operated and managed by DOR. Since this is the first tunnel construction project in 
- **0.6088** `DOC000001-C0013` (image_placeholder) — ## 4. Analysis of the results The authors analysed the cumulative costs and net present value of the construction and maintenance activities related with the pa
- **0.6055** `DOC000012-C0002` (manual) — *Note: these diagrams show how important the operation and maintenance costs are and how it is necessary to choose from the first stages of the tunnel design th
- **0.5867** `DOC000023-C0001` (source_only) — [https://tunnelsmanual.piarc.org/en/strategy-and-general-design-strategic-issues/tunnel-complex-system](https://tunnelsmanual.piarc.org/en/strategy-and-general-

### `waterproofing`

- **0.5052** `DOC000007-C0005` (longest_safe) — | 4.4 | Geophysical exploration ahead of the face . . . . . . . . . . . . . . . . . . . . . . . . . . . . | Geophysical exploration ahead of the face . . . . . 
- **0.5047** `DOC000047-C0252` (median_sized) — ## 11.1 INTRODUCTION This chapter describes the structural design of immersed tunnels in accordance with the AASHTO LRFD Bridge Design Specifications (AASHTO). 
- **0.4896** `DOC000001-C0017` (url_doi_heavy) — [Synnefa, A., Karlessi, T., Gaitani, N., Papakatsikas, C., 2011. Experimental testing of cool colored thin layer asphalt and estimation of its potential to impr
- **0.4856** `DOC000007-C0009` (longest_safe) — ## XXII Table of Contents | 11 | DAUB recommendations for the selection of tunnelling machines . . . . . . . . | DAUB recommendations for the selection of tunne
- **0.4768** `DOC000001-C0009` (table) — | Luminance | (cd/m 2 ) | |-------------|-------------| | L seq | 169 | | L atm | 324 | | L par | 33 | | L cru | 33 | Table 12 Average luminance coefficients (U

### `tünel havalandırması`

- **0.6272** `DOC000167-C0010` (topup) — Türkiye'deki Karayolu Tünellerinde Trafik Güvenliği
- **0.5493** `DOC000072-C0015` (p90_sized) — #### 31 Tünel İnşaatlarında Karşılaşılabilen Bazı Sorunlar #### 32 İnşa Esnasında Su Çıkması Tünel açımı ile yeraltı suları; duvar ve tavandan sızıntı şeklinde,
- **0.5446** `DOC000023-C0001` (source_only) — [https://tunnelsmanual.piarc.org/en/strategy-and-general-design-strategic-issues/tunnel-complex-system](https://tunnelsmanual.piarc.org/en/strategy-and-general-
- **0.5312** `DOC000001-C0009` (table) — | Luminance | (cd/m 2 ) | |-------------|-------------| | L seq | 169 | | L atm | 324 | | L par | 33 | | L cru | 33 | Table 12 Average luminance coefficients (U
- **0.5290** `DOC000021-C0022` (median_sized) — <!-- Docling chunk 2/2 --> <!-- original_page_start: 26 --> <!-- original_page_end: 29 --> <!-- citation_rule: original_page = original_page_start + chunk_local

### `kaya bulonu`

- **0.3880** `DOC000170-C0015` (topup) — 6. 7.
- **0.3832** `DOC000047-C0027` (topup) — This page is intentionally left blank.
- **0.3832** `DOC000047-C0019` (topup) — This page is intentionally left blank.
- **0.3815** `DOC000048-C0041` (topup) — :…….…..……………...
- **0.3717** `DOC000236-C0388` (topup) — gösteren ulusal işarettir. <!-- image -->

### `püskürtme beton`

- **0.5053** `DOC000056-C0001` (source_only) — Enjeksiyon Fotoları [https://www.ozdemirenjeksiyon.com/uygulamalar-detay/tunel-kazisi-sirasinda-su-yalitimi-enjeksiyon-uygulamasi](https://www.ozdemirenjeksiyon
- **0.4904** `DOC000001-C0016` (url_doi_heavy) — ## References AASHTO, 1993. Guide for Design of Pavement Structures. ANAS, 2015a. Elenco prezzi Nuove Costruzioni e Manutenzione Straordinaria. ANAS, 2015b. Ele
- **0.4810** `DOC000001-C0002` (english) — ## a b s t r a c t This work computes and compares the life cycle costs of two different road tunnel pavements and their corresponding lighting systems. The stu
- **0.4754** `DOC000007-C0008` (longest_safe) — | 8.4 | Transport, storage and handling of explosives . . . . . . . . . . . . . . . . . . . . . . . . . | Transport, storage and handling of explosives . . . . 
- **0.4660** `DOC000001-C0007` (english) — ## 2.4. Pavement-related costs The economic pavement analysis was carried out after assuming that both pavements were built in a natural road tunnel section, wh

### `tünel bakım ve işletmesi`

- **0.6154** `DOC000167-C0010` (topup) — Türkiye'deki Karayolu Tünellerinde Trafik Güvenliği
- **0.5882** `DOC000002-C0001` (short) — <!-- Docling chunk 1/5 --> <!-- original_page_start: 1 --> <!-- original_page_end: 25 --> <!-- citation_rule: original_page = original_page_start + chunk_local_
- **0.5519** `DOC000015-C0001` (manual) — <!-- Docling chunk 1/11 --> <!-- original_page_start: 1 --> <!-- original_page_end: 25 --> <!-- citation_rule: original_page = original_page_start + chunk_local
- **0.5482** `DOC000002-C0007` (short) — ## (3) Tunnel Management Office Operator Tunnel Management Office should be operated and managed by DOR. Since this is the first tunnel construction project in 
- **0.5368** `DOC000061-C0001` (source_only) — ITU Yüksek Lisans Tez [https://nek.istanbul.edu.tr/ekos/TEZ/37091.pdf](https://nek.istanbul.edu.tr/ekos/TEZ/37091.pdf) 19 Mayıs Üniversitesi 14. Hafta Ders Notl

### `jeoteknik araştırma`

- **0.5119** `DOC000124-C0002` (p90_sized) — - 9.1. Giriş ve Çalışmanın Amacı 74 - 9.2. İnceleme Alanının Jeolojisi 76 - 9.2.2. Genel Jeoloji 77 - 9.2.3. Güzergah Jeolojisi 79 - 9.2.4. Yapısal Jeoloji 80 -
- **0.4985** `DOC000007-C0005` (longest_safe) — | 4.4 | Geophysical exploration ahead of the face . . . . . . . . . . . . . . . . . . . . . . . . . . . . | Geophysical exploration ahead of the face . . . . . 
- **0.4526** `DOC000001-C0017` (url_doi_heavy) — [Synnefa, A., Karlessi, T., Gaitani, N., Papakatsikas, C., 2011. Experimental testing of cool colored thin layer asphalt and estimation of its potential to impr
- **0.4522** `DOC000007-C0008` (longest_safe) — | 8.4 | Transport, storage and handling of explosives . . . . . . . . . . . . . . . . . . . . . . . . . | Transport, storage and handling of explosives . . . . 
- **0.4481** `DOC000071-C0029` (median_sized) — | Km: 5 + 963 40 - 6 + 066 00 ( Hat-2) | | | | | | | | | | | | | | |--------------------------------------------------------------------------------------------

## Integrity

- Frozen chunk artefacts changed: **0**
- `data/chunks/chunks.jsonl`: **unchanged**
- `data/chunks_pilot/chunks.jsonl`: **unchanged**
- `data/metadata/chunk_manifest.csv`: **unchanged**
- `data/metadata/chunk_review_queue.csv`: **unchanged**
- `data/corpus_final/`, `data/corpus_normalized/`: **unchanged**
- Chunk text was never modified; chunk boundaries were never recut.
- NaN values: **0** · Inf values: **0**
- All vectors finite: **True**
- Vector norms: min **1.000000**, max **1.000000** (unit-normalized as expected)
- Chunk/vector mapping: **100 rows ↔ 100 vectors**, index-aligned

## Idempotency

- Tokenizer audit: **deterministic** — identical counts on a second pass.
- Pilot selection: **deterministic** — fixed categories and fixed sort keys, no randomness.
- Embedding re-run drift (16-chunk re-embed): **max |Δ| = 0.00e+00**. Byte-identical output is not expected from floating-point inference; this is well inside numerical equivalence.

## Tests

- Main tests (`tests/`): **226/226 PASS** (190 previous + 36 new BGE-M3 preflight tests; 2 model-download tests opt-in via `TUNNELBOOK_BGE_LIVE=1`, verified passing separately)
- Report/Colab tests (`rapor/tests/`): **16/16 PASS**
- Project-wide total: **242/242 PASS**
- New preflight tests cover: tokenizer load, chunk ID uniqueness, deterministic counts, zero silent truncation, resolved model max length, deterministic pilot selection, stable dimensions, finite vectors, no NaN, no Inf, exact vector/chunk mapping, manifest integrity, unchanged frozen artefacts.

## Warnings

- **Corpus quality, not a preflight blocker:** 58 chunks (0.96%) are text-extraction failures — raw PDF glyph-index sequences (`/G49/G72/G90/…`) or dense control-character residue rather than readable text. Affected: DOC000009 (5/6 chunks), DOC000041 (8/8 chunks), DOC000051 (45/45 chunks). Two of these documents are *entirely* unusable. They tokenize and embed without error — about 69,573 BGE-M3 tokens of them — but the resulting vectors are semantically meaningless and will sit in the index as noise. This originates upstream of chunking, in text extraction. Recommend excluding or re-extracting these 3 documents before the full run, as an explicit decision rather than a silent pass.
- **Low-content chunks:** 201 chunks (3.33%) carry fewer than 8 real words. Many are legitimate short regulation articles (e.g. `MADDE 3- Bu Karar yayımı tarihinde yürürlüğe girer.`) and should be kept. But the sanity queries showed that when no relevant chunk exists, boilerplate such as `This page is intentionally left blank.` becomes a top hit at low absolute scores. A score floor at retrieval time handles this better than deleting chunks; worth setting deliberately during retrieval evaluation.
- Token counts in the frozen chunk artefacts remain `unicode-lexical-v1` values. They are a systematic underestimate (median ratio 1.35); the real counts now live in `data/metadata/bge_m3_tokenizer_audit.csv`. Downstream stages should read token lengths from there.
- 675 chunks exceed the 1500-token chunking guideline under the real tokenizer versus 190 under the lexical count, as predicted. All remain far below the 8192 limit, so this affects retrieval granularity, not correctness.
- The throughput figure comes from a ~100-chunk stratified pilot on MPS and should be treated as indicative rather than a firm full-run estimate.

## Blockers

- Yok.

## Final Decision

**BGE-M3 EMBEDDING PREFLIGHT — GO**

Next stage (not started): full 6039-chunk embedding run, then Qdrant indexing, then retrieval evaluation.
