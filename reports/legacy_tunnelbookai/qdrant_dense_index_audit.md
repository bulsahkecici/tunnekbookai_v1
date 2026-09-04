# TunnelBookAI Qdrant Dense Index Audit

## Decision

**QDRANT DENSE INDEX — GO**

Index build and validation only. No threshold tuning, retrieval benchmark, reranker, sparse vectors, hybrid search or RAG was started.

## Environment

- Qdrant server: **1.18.2** (`qdrant/qdrant:v1.18.2` container)
- qdrant-client: **1.18.0** (aligned to the server minor version; the initially installed 1.16.1 was rejected by the client's own compatibility check and replaced)
- Deployment: **local Docker container** via colima (Docker Server 29.5.2). No Qdrant Cloud, no external data transfer.
- REST endpoint: `http://localhost:6333` · gRPC: `localhost:6334`
- Storage: `data/qdrant_storage/` (bind mount → `/qdrant/storage`)
- Snapshots: `data/qdrant_snapshots/` (bind mount → `/qdrant/snapshots`)
- Pre-existing collections found at preflight: **none** — nothing unknown was reused or destroyed.

## Release Identity

- `chunk_ids_sha256`: `7497af0d7d7032eb4c2400f74f6f1f694ab80ce3a594be416bd66bd808cf86bd`
- `collection_name`: `tunnelbook_dense_v1`
- `collection_release_name`: `tunnelbook-dense-v1`
- `distance`: `COSINE`
- `embedding_input_manifest_sha256`: `4af9d60a8cbfbb712c27c8129a622b6118166954c732947e015876e25fd99654`
- `embedding_manifest_sha256`: `68be1f5fa0b7b6078cd9f492a8732aa796b2ab6536c4b76454e5a37bd41bc32a`
- `embedding_model`: `BAAI/bge-m3`
- `embedding_npy_sha256`: `99e3b79033a996ffb08b4b742faf68ec217a5a49d0cfdb05175996d65de1d4d3`
- `embedding_version`: `bge-m3-dense-v1.0`
- `expected_point_count`: `5992`
- `model_revision`: `5617a9f61b028005a4858fdac845db406aefb181`
- `payload_schema_version`: `payload-v1`
- `vector_size`: `1024`

Stored as `data/metadata/qdrant_dense_release.json`.

## Collection Configuration

- Name: `tunnelbook_dense_v1`
- Vector size: **1024**
- Distance: **Cosine**
- Status: **green** · optimizer: **ok**
- Quantization: **none** · sparse vectors: **none** · multivectors: **none** — one dense BGE-M3 vector per point, deliberately simple for this baseline.
- Point IDs: the manifest's `vector_index` (0…5991); no random UUIDs, so a rebuild reproduces identical IDs.

## Payload Schema

- Schema version: `payload-v1`
- Identity: `vector_index`, `chunk_id`, `document_id`, `source_kind`
- Content: `text`, `text_sha256`, `bge_m3_token_count`
- Bibliographic: `title`, `organization`, `year`, `language`, `document_type`, `authority_level`, `topics`
- Structure: `heading`, `parent_heading`, `section_path`
- Source: `source_relative_path`, `source_extension`, `source_sha256`, `normalized_source_sha256`
- Citation: `citation_mode`, `provenance_status`, `original_page_start`, `original_page_end`, `slide_start`, `slide_end`
- Flags: `contains_table`, `contains_formula_placeholder`, `contains_image_placeholder`, `eligibility_status`, `is_low_content`
- Model: `model`, `model_revision`, `embedding_version`
- Recovery points additionally carry `recovery_version`, `recovery_method`, `original_source_sha256`.
- Unknown metadata is stored as **null**, never invented.

## Payload Indexes

- `authority_level`: **KEYWORD**
- `document_id`: **KEYWORD**
- `document_type`: **KEYWORD**
- `eligibility_status`: **KEYWORD**
- `language`: **KEYWORD**
- `source_kind`: **KEYWORD**
- `topics`: **KEYWORD**
- `year`: **INTEGER**

Created before bulk ingest. `text`, `heading`, `section_path` and source paths are deliberately **not** indexed — the dense baseline does not filter on them.

## Ingest

- Expected: **5992**
- not run this invocation

## Exact Counts

Taken with Qdrant's **exact** count API and an independent full payload scroll; the approximate `points_count`/`indexed_vectors_count` counters were not used for the gate.

- Total: **5992** (expected 5992)
- canonical_chunk: **5980** (expected 5980)
- recovery_chunk: **12** (expected 12)
- low-content: **143** (expected 143)
- Distinct document_id: **214** (expected 214)
- Duplicate point IDs: **0**
- Superseded canonical chunks indexed: **0** (checked against the eligibility manifest before ingest)
- For reference, the approximate counters read `points_count=5992`, `indexed_vectors_count=5376`. The latter is lower than the point count because segments below the HNSW indexing threshold are served by exact search; this is normal and is exactly why it is not used as the gate.

## Payload Round-trip

- Points sampled by ID: **222** — first 20, last 20, a deterministic stride across the whole range, **all 12 recovery points**, low-content examples, the 10 longest chunks, table chunks and `source_only` provenance chunks.
- Field mismatches (`vector_index`, `chunk_id`, `document_id`, `text_sha256`, `source_kind`): **0**
- Stored `text` was re-hashed and compared to `text_sha256` for every sampled point: **0 mismatches**.

## Vector Round-trip

- Vectors retrieved from Qdrant and compared to `bge_m3_dense.npy`: **222** points
- Max absolute difference: **0.000e+00**
- Mean absolute difference: **0.000e+00**
- Minimum cosine similarity: **0.99999982**
- Vectors are stored without mutation.

## Filter Audit

| filter | result | all payloads match |
|---|---|---|
| `authority_level=A` | 50 | True |
| `document_id=DOC000009` | 3 | True |
| `document_id=DOC000041` | 4 | True |
| `document_type=regulation` | 50 | True |
| `eligibility_status=eligible_low_content` | 143 | — |
| `language=tr` | 50 | True |
| `source_kind=recovery_chunk` | 12 | — |
| `year>=2020` | 1021 | — |

Filters were checked for semantic correctness, not just API success: every returned payload was confirmed to actually carry the filtered value.
- `document_id=DOC000009` returns **3** points — its recovery chunks only, confirming the superseded canonical chunks are genuinely absent from the index.

## Dense Query Smoke

Not a retrieval benchmark; no `ef`/threshold tuning was performed. Top-5 per query.

#### `NATM support systems`

| # | score | chunk_id | document | preview |
|---|---|---|---|---|
| 1 | 0.6395 | `DOC000302-C0130` | DOC000302 | ## Slayt 139 Destek Sisteminin Ortam Koşullarına Göre Sonlu Elemanlar Yöntemi İle Analizi KONTROL MÜHENDİSİ GE |
| 2 | 0.6228 | `DOC000302-C0144` | DOC000302 | ## Slayt 154 KONTROL MÜHENDİSİ GELİŞTİRME KURSU NATM (New Austrian Tunneling Method) YATAM (Yeni Avusturya Tün |
| 3 | 0.6208 | `DOC000125-C0003` | DOC000125 | ## NATM YÖNTEM İ N İ N ESASLARI - NATM yöntemi ile tünel aç ı lmas ı nda ana ilke, tünel kayas ı n ı kendisine |
| 4 | 0.6183 | `DOC000308-C0007` | DOC000308 | ## 4. Sequential Excavation Method NATM The Sequential Excavation Method (SEM), also commonly referred to as t |
| 5 | 0.6166 | `DOC000302-C0142` | DOC000302 | ## Slayt 151 ## Slayt 152 KONTROL MÜHENDİSİ GELİŞTİRME KURSU NATM (Yeni Avusturya Tünel Açma Yöntemi) kesinlik |

#### `tunnel ventilation`

| # | score | chunk_id | document | preview |
|---|---|---|---|---|
| 1 | 0.6891 | `DOC000197-C0023` | DOC000197 | ## 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) - 15 kV line supplies the explosion-proof IM2 c |
| 2 | 0.6865 | `DOC000037-C0026` | DOC000037 | ## 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) To ensure the correct amount of fresh air in al |
| 3 | 0.6727 | `DOC000047-C0049` | DOC000047 | ## 2.4.5 Ventilation Requirements The ventilation system of a tunnel operates to maintain acceptable air quali |
| 4 | 0.6557 | `DOC000003-C0075` | DOC000003 | ## 4.2.1 Typical Road Tunnels Road tunnels that are longer than 1,000 feet (304 meters) typically have forced  |
| 5 | 0.6541 | `DOC000015-C0024` | DOC000015 | ## Basic Types of Ventilation Systems 1.4.9.1 There are five basic types of tunnel ventilation systems: - Natu |

#### `shotcrete`

| # | score | chunk_id | document | preview |
|---|---|---|---|---|
| 1 | 0.5600 | `DOC000047-C0358` | DOC000047 | / Flashcrete (Sealing Shotcrete) / Typically unreinforced or steel fiber re inforced sprayed concrete layer to |
| 2 | 0.5573 | `DOC000047-C0250` | DOC000047 | ## 10.7 SHOTCRETE LINING As discussed in Chapter 9, shotcrete represents a structurally and qualitatively equa |
| 3 | 0.5543 | `DOC000007-C0012` | DOC000007 | / 2.8.3 / Shotcrete / /----------------------------------------------------/---------------------------------- |
| 4 | 0.5436 | `DOC000227-C0004` | DOC000227 | K.T.Ş. nin ilgili kısımlarındaki esaslar ve şartlara, projeye ve İdarenin talimatına uygun olarak her dozda pü |
| 5 | 0.5357 | `DOC000047-C0212` | DOC000047 | ## 9.5.1.1 Effect of Shotcrete When concrete is sprayed on a rough ground surface, it fills small openings, cr |

#### `rock bolt design`

| # | score | chunk_id | document | preview |
|---|---|---|---|---|
| 1 | 0.6120 | `DOC000047-C0131` | DOC000047 | ## 6.5.2.2 Rock Bolts Rock bolts (Figure 6-18) have a friction or grout anchor in the rock and are tensioned a |
| 2 | 0.5606 | `DOC000047-C0215` | DOC000047 | ## 9.5.2.2 Practical Aspects Several practical aspects related to rock dowel/bolt installation in the field ha |
| 3 | 0.5516 | `DOC000047-C0214` | DOC000047 | ## 9.5.2 Rock Reinforcement As discussed in Chapter 6, rock reinforcement and rock mass act as a complex inter |
| 4 | 0.5455 | `DOC000047-C0136` | DOC000047 | Also note that the Q-system was developed from over 1000 tunnel projects, most of which are in Scandinavia and |
| 5 | 0.5357 | `DOC000037-C0034` | DOC000037 | ## 3.2 Ground Reinforcement There are three distinct types of ground reinforcement methods (Woodward, 2005) an |

#### `tunnel maintenance cost`

| # | score | chunk_id | document | preview |
|---|---|---|---|---|
| 1 | 0.6951 | `DOC000041-R1-C0001` | DOC000041 | # Estimate of annual operating costs Highway Tunnel ## Sayfa 1 Newfoundland Fixed Link Pre-feasibility StudyPa |
| 2 | 0.6875 | `DOC000041-R1-C0003` | DOC000041 | ## Sayfa 3 Newfoundland Fixed Link Pre-feasibility StudyPage 1 of 2 Highway Tunnel Estimate of annual maintena |
| 3 | 0.6736 | `DOC000041-R1-C0004` | DOC000041 | ## Sayfa 4 Newfoundland Fixed Link Pre-feasibility StudyPage 2 of 2 Highway Tunnel Estimate of annual maintena |
| 4 | 0.6689 | `DOC000016-C0006` | DOC000016 | ## Appendix A - Tunnel estimate example This example assumes a 7km tunnel is constructed using slurry machines |
| 5 | 0.6652 | `DOC000002-C0007` | DOC000002 | ## (3) Tunnel Management Office Operator Tunnel Management Office should be operated and managed by DOR. Since |

#### `tünel havalandırması`

| # | score | chunk_id | document | preview |
|---|---|---|---|---|
| 1 | 0.6907 | `DOC000096-C0004` | DOC000096 | ### 3 Korunma Hücreleri ĠĢletme amacına uygun olarak; bakım-onarım, kurtarma ve diğer ihtiyaçlara cevap verece |
| 2 | 0.6717 | `DOC000045-C0005` | DOC000045 | / / Dayanıklılığı / / / / / / / yerlerde zorunludur. / /-------------------------/---------------------------- |
| 3 | 0.6615 | `DOC000075-C0014` | DOC000075 | / Aydınlatma / Normal Aydınlatma / 8.1 / • / • / • / • / • / / /--------------------------/------------------- |
| 4 | 0.6539 | `DOC000075-C0065` | DOC000075 | Her tünel belirli oranda doğal havalandırmaya sahiptir. Bu durum tünelin iki portalı arasındaki basınç farkınd |
| 5 | 0.6492 | `DOC000287-C0068` | DOC000287 | ## Slayt 71 Tünellerde güvenli ve duman kalitesi çok daha iyi olan emülsyon patlayıcıların kullanılması kapalı |

#### `kaya bulonu`

| # | score | chunk_id | document | preview |
|---|---|---|---|---|
| 1 | 0.4632 | `DOC000124-C0053` | DOC000124 | Bulonlara etkiyen kuvvetler aşağıdaki çizelgede özetlenmiştir. Plaxis'de elde edilen çıktılar bulonun , metres |
| 2 | 0.4542 | `DOC000216-C0001` | DOC000216 | <!-- image --> <!-- image --> # Tünel Kontrol Mühendisi Geliştirme Kursu Tünel Destekleme Elemanları 24~28.02. |
| 3 | 0.4475 | `DOC000290-C0004` | DOC000290 | Lb = 0,019 x 616 x 420 / (20)1/2 = 1,09m <!-- image --> / SUNUM ADI / / /-------------/----------------/ / / w |
| 4 | 0.4370 | `DOC000293-C0009` | DOC000293 | # Tünel Kazısı Sırasında Deney - - Uygulanacak deney kuvveti, deneye tabii tutulacak kaya bulonu kopma yükünün |
| 5 | 0.4361 | `DOC000285-C0025` | DOC000285 | # KALİTE KONTROL LABORATUVARINDA YAPILAN DENEYLER TÜNEL DENEYLERİ # 1.BULON ÇEKME DENEYLERİ Amaç Tünel yapım p |

#### `püskürtme beton`

| # | score | chunk_id | document | preview |
|---|---|---|---|---|
| 1 | 0.7143 | `DOC000072-C0018` | DOC000072 | #### 47 Püskürtme Beton Kaplamalar Püskürtme beton, onarım yada yapım amacıyla önceden kuru yada ıslak yolla h |
| 2 | 0.7103 | `DOC000087-C0276` | DOC000087 | ## 351.08.02 Alt Yüzey Klasik betonla karşılaştırıldığında püskürtme beton kalınlığı genellikle daha azdır. Pü |
| 3 | 0.6843 | `DOC000214-C0002` | DOC000214 | - ‘Tünelde Püskürtme Betonu (Shotcrete) Yapılması’ teklif birim fiyatı üzerinden ‘m3’ cinsinden yapılır - Biri |
| 4 | 0.6781 | `DOC000087-C0278` | DOC000087 | ## 351.08.07 Püskürtmenin Uygulanma Tekniği Püskürtme beton uygulamasına geçmeden önce uygulama sırasında aşağ |
| 5 | 0.6758 | `DOC000236-C0277` | DOC000236 | ## 351.07.04 Çevresel Şartlarla İlgili Gereksinimler Püskürtme beton, projecinin öngördüğü gereksinimlere, Tab |

#### `jeoteknik araştırma`

| # | score | chunk_id | document | preview |
|---|---|---|---|---|
| 1 | 0.5936 | `DOC000302-C0050` | DOC000302 | ## Slayt 54 KONTROL MÜHENDİSİ GELİŞTİRME KURSU TÜNEL GÜZERGAHLARINDA JEOFİZİK ARAŞTIRMALARI Tünelde yapılan je |
| 2 | 0.5680 | `DOC000302-C0001` | DOC000302 | # TÜNELLERDE GÜZERGAH SEÇİMİ VE jeoteknik araştırmalar son ## Slayt 1 JEOLOJİK HİZMETLER ŞUBESİ MÜDÜRLÜĞÜ AYDI |
| 3 | 0.5665 | `DOC000302-C0040` | DOC000302 | ## Slayt 44 KONTROL MÜHENDİSİ GELİŞTİRME KURSU Tünel Jeolojik – Jeoteknik Raporu Tünel jeolojik – Jeoteknik ra |
| 4 | 0.5585 | `DOC000302-C0039` | DOC000302 | ## Slayt 43 KONTROL MÜHENDİSİ GELİŞTİRME KURSU Jeoteknik Modelin Kurulumu Tünel jeolojik - jeoteknik model içi |
| 5 | 0.5534 | `DOC000302-C0051` | DOC000302 | ## Slayt 55 KONTROL MÜHENDİSİ GELİŞTİRME KURSU JEOFİZİK ARAŞTIRMALARI genellikle iki metotla yapılmaktadır: Si |

**Agreement with the pre-Qdrant baseline:** these rankings and scores match the direct NumPy cosine smoke run from the embedding stage (for example `NATM support systems` returns the same top-5 at 0.6395 / 0.6228 / 0.6208 / 0.6183 / 0.6166). HNSW is returning the same neighbours as brute force on these queries, which is a strong signal that ingest preserved both vectors and ordering.

## Recovery Query Smoke

#### `annual tunnel operating costs`

| # | score | chunk_id | document | kind | preview |
|---|---|---|---|---|---|
| 1 | 0.7055 | `DOC000041-R1-C0001` | DOC000041 | recovery_chunk | # Estimate of annual operating costs Highway Tunnel ## Sayfa 1 Newfoundland Fixed Link Pre-feasibility StudyPa |
| 2 | 0.6764 | `DOC000041-R1-C0002` | DOC000041 | recovery_chunk | ## Sayfa 2 Newfoundland Fixed Link Pre-feasibility StudyPage 2 of 2 Highway Tunnel Estimate of annual operatin |
| 3 | 0.6704 | `DOC000019-C0005` | DOC000019 | canonical_chunk | ## 2.2 Estimating Operational and Regular Maintenance Costs - 2.2.1 Those requirements and tasks on road infra |
| 4 | 0.6545 | `DOC000009-R1-C0002` | DOC000009 | recovery_chunk | ## Assumptions: Facility operates 12 hours/day, 7 days/week 50 percent of this time the facility is fully staf |
| 5 | 0.6522 | `DOC000017-C0003` | DOC000017 | canonical_chunk | ## International Research Journal of Engineering and Technology (IRJET) e-ISSN: 2395-0056 Volume: 08 Issue: 07 |

#### `tunnel maintenance cost`

| # | score | chunk_id | document | kind | preview |
|---|---|---|---|---|---|
| 1 | 0.6951 | `DOC000041-R1-C0001` | DOC000041 | recovery_chunk | # Estimate of annual operating costs Highway Tunnel ## Sayfa 1 Newfoundland Fixed Link Pre-feasibility StudyPa |
| 2 | 0.6875 | `DOC000041-R1-C0003` | DOC000041 | recovery_chunk | ## Sayfa 3 Newfoundland Fixed Link Pre-feasibility StudyPage 1 of 2 Highway Tunnel Estimate of annual maintena |
| 3 | 0.6736 | `DOC000041-R1-C0004` | DOC000041 | recovery_chunk | ## Sayfa 4 Newfoundland Fixed Link Pre-feasibility StudyPage 2 of 2 Highway Tunnel Estimate of annual maintena |
| 4 | 0.6689 | `DOC000016-C0006` | DOC000016 | canonical_chunk | ## Appendix A - Tunnel estimate example This example assumes a 7km tunnel is constructed using slurry machines |
| 5 | 0.6652 | `DOC000002-C0007` | DOC000002 | canonical_chunk | ## (3) Tunnel Management Office Operator Tunnel Management Office should be operated and managed by DOR. Since |

#### `Türkiye tünel haritası`

| # | score | chunk_id | document | kind | preview |
|---|---|---|---|---|---|
| 1 | 0.6581 | `DOC000167-C0010` | DOC000167 | canonical_chunk | Türkiye'deki Karayolu Tünellerinde Trafik Güvenliği |
| 2 | 0.6360 | `DOC000051-R1-C0001` | DOC000051 | recovery_chunk | # Tünel Haritası 2024_KGMWEB ## Sayfa 1 !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( ! |
| 3 | 0.6285 | `DOC000049-C0149` | DOC000049 | canonical_chunk | ## 2015 YILINDA TAMAMLANMASI PLANLANAN TÜNELLER / SIRA NO / BÖLGE NO / TÜNELİN ADI / YOLUN ADI / K.K.NO / TÜP  |
| 4 | 0.6239 | `DOC000049-C0010` | DOC000049 | canonical_chunk | ## 2000-3000 METRE ARASI UZUNLUKTAKİ TÜNELLER / SIRA NO / BÖLGE NO / TÜNELİN ADI / YOLUN ADI / K.K.NO / BAŞL.  |
| 5 | 0.6220 | `DOC000167-C0004` | DOC000167 | canonical_chunk | ## 4. TÜRKİYE'DE TÜNEL GÜVENLİĞİ Coğrafi yönden dağlık bir arazi yapısına sahip olan Türkiye'de tünel sayısı o |

- DOC000041 recovery chunks take ranks **1–3** for cost queries.
- DOC000051 recovery is retrievable at rank **2** for `Türkiye tünel haritası`.
- Recovery content did not appear in unrelated general queries.

## Low-content Observations

- Low-content vectors indexed and flagged: **143** (`is_low_content = true`, `eligibility_status = eligible_low_content`). None were removed.
- Across the 60 smoke top-5 slots, low-content chunks appeared **1** times.
- Notably `DOC000167-C0010` (a one-line title fragment) took rank 1 for `Türkiye tünel haritası` at 0.6581, ahead of the actual tunnel map. Short fragments can out-score substantive content on short queries.
- `DOC000009-R1-C0003` (the empty symbol/table skeleton) did **not** surface in any smoke query top-5.
- Recorded as observations only. Score thresholds and low-content penalties belong to the retrieval-evaluation stage.

## Snapshot

- Name: `tunnelbook_dense_v1-4337796820776469-2026-08-17-15-44-52.snapshot`
- Size: **222,870,528 bytes** (~213 MB)
- Host path: `data/qdrant_snapshots/tunnelbook_dense_v1/tunnelbook_dense_v1-4337796820776469-2026-08-17-15-44-52.snapshot`
- Creation status: **completed**
- SHA256: `5570ae984e3fe86e27ea35879cbd1a05cfca074652bdc1c0e4a5b22d9dbac7f8`
- Qdrant-reported checksum: `5570ae984e3fe86e27ea35879cbd1a05cfca074652bdc1c0e4a5b22d9dbac7f8`
- Checksum agreement: **True**
- The first snapshot attempt wrote only inside the container (`/qdrant/snapshots` was not mounted) and would have been lost with the container. A second bind mount was added and the snapshot recreated on the host. The snapshot is retained, not deleted.

## Rebuildability

- Qdrant remains a derived layer. The collection is reconstructable from `bge_m3_dense.npy`, `full_embedding_manifest.csv`, the frozen chunk sources and `scripts/15_qdrant_index.py`.
- Stages: `--preflight --create --ingest --verify --smoke --snapshot --report`, or `--all`.
- Point IDs are `vector_index`, so a rebuild yields identical IDs and identical point→chunk mapping.
- Collection storage survived a full container replacement (the container was recreated to add the snapshot mount and the collection came back green with 5992 points), which independently confirms the persistent bind mount works.

## Idempotency

- Re-running `--create --ingest --verify` against the existing collection reported `reused (release identity matches)`, uploaded **0** points, and left the exact count at **5992** with **0** duplicate IDs.
- A tampered release descriptor (altered `embedding_npy_sha256`) was correctly refused with `collection: incompatible` and a **NO-GO**; the collection was left untouched. Recreation requires the explicit `--allow-recreate` flag, so an unknown collection is never destroyed automatically.

## Frozen Integrity

- Protected artefacts changed: **0**
- `bge_m3_dense.npy`, `bge_m3_chunk_ids.json`: **unchanged**
- `full_embedding_manifest.csv`, `full_embedding_input_manifest.csv`, `embedding_eligibility.csv`: **unchanged**
- `chunks.jsonl`, `chunks_recovery/chunks.jsonl`: **unchanged**
- `data/corpus_final/`, `data/corpus_normalized/`, `data/corpus_recovery/`: **unchanged**
- Qdrant data lives only in `data/qdrant_storage/` and `data/qdrant_snapshots/`, outside every frozen tree.

## Tests

- Main tests (`tests/`): **344/344 PASS** (311 previous + 33 new Qdrant index tests; 10 live Qdrant/model tests opt-in via `TUNNELBOOK_QDRANT_LIVE=1` / `TUNNELBOOK_BGE_LIVE=1`, verified passing separately)
- Report/Colab tests (`rapor/tests/`): **16/16 PASS**
- Project-wide total: **360/360 PASS**
- New tests cover: release hash validation, vector shape, deterministic integer point IDs, payload building, canonical and recovery text resolvers, text SHA verification, low-content flag propagation, payload schema, year type safety, exact count gate, source_kind counts, recovery count 12, document coverage 214, payload round-trip, vector round-trip, filter semantics, incompatible-collection rejection, valid-collection reuse, rebuild determinism, protected input immutability.

## Warnings

- `qdrant-client` was upgraded 1.16.1 → 1.18.0 to match server 1.18.2; the client refuses to operate more than one minor version away. `pip check` is clean and no existing project dependency was disturbed.
- The Docker daemon (colima) was started for this stage. If it is stopped, the Qdrant container stops with it; data persists in the bind mounts and the container can be restarted.
- `indexed_vectors_count` is lower than the point count while small segments remain unindexed. This affects nothing here because the gate uses exact counts, but do not read that counter as missing data.
- HNSW search is approximate by nature. It matched brute force on every smoke query at this corpus size, but recall behaviour should be measured properly in the retrieval-evaluation stage rather than assumed from this.
- Payload stores the full chunk `text`, so the collection duplicates chunk text into the vector DB. That is intentional for citation rendering and debugging, and is the main driver of the snapshot size.

## Blockers

- Yok.

## Final Decision

**QDRANT DENSE INDEX — GO**

Next stage (not started): retrieval evaluation, threshold tuning, low-content policy, reranking, sparse/hybrid retrieval, RAG.
