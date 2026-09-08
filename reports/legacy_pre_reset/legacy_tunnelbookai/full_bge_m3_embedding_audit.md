# TunnelBookAI Full BGE-M3 Dense Embedding Audit

## Decision

**FULL BGE-M3 EMBEDDINGS — GO**

Embedding only. No vector database, retrieval benchmark, reranker or RAG was started.

## Input

- Authoritative manifest: `data/metadata/full_embedding_input_manifest.csv`
- Vectors planned: **5992**
- canonical_chunk: **5980**
- recovery_chunk: **12**
- Documents represented: **214/214**
- Superseded canonical chunks present: **0** (validated against the eligibility manifest)
- `text_sha256` verified for every input against the manifest: **all match**

## Recovery mini-gate

- Recovery chunks inspected: **12/12** (no sampling)
- DOC000009: **3** · DOC000041: **4** · DOC000051: **5**
- Glyph residue (`/Gxx` or `GxxGxx`): **0**
- Control-character corruption: **0**
- Duplicate recovery text: **0**
- Provenance retained: **12/12**
- Canonical/recovery duplicate indexing: **0**
- BGE-M3 tokens — min **112**, median **848**, max **2916**
- Over 8192: **0**

- Full detail: `reports/recovery_chunk_embedding_gate.md`

## Model

- Model: `BAAI/bge-m3`
- Revision pin: `5617a9f61b028005a4858fdac845db406aefb181`
- Architecture: `XLMRobertaModel`, CLS pooling + L2 normalization
- Query prefix: **none** · Document prefix: **none**
- Embedding dimension: **1024** · effective max sequence length: **8192**
- transformers **5.8.1** · torch **2.13.0**
- Dense path is byte-for-byte the same code path validated in the preflight pilot; nothing changed between pilot and full run.

## Token statistics

- min **4** · median **969** · mean **897.4** · max **5176**
- Total tokens embedded: **5,377,400**
- Over 8192: **0** — measured with `truncation=False`, so no length was hidden
- Canonical counts cross-checked against `bge_m3_tokenizer_audit.csv`: **all agree**

## Device

- Device used: **mps**
- CUDA unavailable and unused; Apple Silicon MPS with CPU fallback available.

## Batch strategy

- Length-bucketed batching: inputs sorted by token count, batch closed when `batch_size x longest_sequence > 16384` padded tokens or size reaches 16.
- Batches: **446** · mean batch size **13.4**
- This keeps 100-token chunks from being padded up to sit beside 5000-token chunks.
- Final vector order is restored to `vector_index` order before any output is written.

## Runtime

Measured on the cold run that actually computed all 5992 vectors. A resumed run completes in milliseconds, so its timings are not reported as embedding performance.

- Model load: **0.8s**
- Embedding wall time: **436.2s** (7.3 min)
- Throughput: **13.74 chunks/sec**, **12,328 tokens/sec**
- Batches computed this run: **0** · resumed from checkpoint: **5992**
- Peak process memory: **~1.87 GB** of 36 GB unified
- Measurement basis: cold run, all vectors computed

## Vector integrity

- Shape: **(5992, 1024)**
- Finite vectors: **5992/5992**
- NaN: **0** · Inf: **0** · zero vectors: **0**
- Norms — min **1.000000** · median **1.000000** · max **1.000000**

## Mapping integrity

- `vector_index -> chunk_id -> document_id -> text_sha256` verified for **all 5992** rows, not a sample.
- All **12** recovery chunk mappings verified explicitly.
- Duplicate chunk_id: **0** · duplicate vector_index: **0**
- Duplicate text_sha256 groups: **143** covering **305** vectors

## Low-content

- `eligible_low_content` chunks embedded and flagged: **143** = **142** canonical (the 142 carried forward from the eligibility stage) + **1** recovery (`DOC000009-R1-C0003`, the blank recovered page).
- Kept per policy; their retrieval effect is deferred to retrieval evaluation.

## Provenance mix

- page_resolved: **4228**
- section_resolved: **659**
- slide_resolved: **566**
- source_only: **539**

## Similarity smoke tests

Corpus-wide top-10 per query. Semantic sanity only - not retrieval benchmarking, and no threshold is tuned from these.

### English

#### `NATM support systems`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.6395 | `DOC000302-C0130` | DOC000302 | Slayt 139 | ## Slayt 139 Destek Sisteminin Ortam Koşullarına Göre Sonlu Elemanlar Yöntemi İle Analizi KONTROL MÜHENDİSİ GELİŞTİRME K |
| 2 | 0.6228 | `DOC000302-C0144` | DOC000302 | Slayt 154 | ## Slayt 154 KONTROL MÜHENDİSİ GELİŞTİRME KURSU NATM (New Austrian Tunneling Method) YATAM (Yeni Avusturya Tünel Açma Me |
| 3 | 0.6208 | `DOC000125-C0003` | DOC000125 | NATM YÖNTEM İ N İ N ESASLARI | ## NATM YÖNTEM İ N İ N ESASLARI - NATM yöntemi ile tünel aç ı lmas ı nda ana ilke, tünel kayas ı n ı kendisine ta ş ı tm |
| 4 | 0.6183 | `DOC000308-C0007` | DOC000308 | 4. Sequential Excavation Method NATM | ## 4. Sequential Excavation Method NATM The Sequential Excavation Method (SEM), also commonly referred to as the New Aus |
| 5 | 0.6166 | `DOC000302-C0142` | DOC000302 | Slayt 151 | ## Slayt 151 ## Slayt 152 KONTROL MÜHENDİSİ GELİŞTİRME KURSU NATM (Yeni Avusturya Tünel Açma Yöntemi) kesinlikle bir kay |
| 6 | 0.6107 | `DOC000302-C0143` | DOC000302 | Slayt 153 | ## Slayt 153 KONTROL MÜHENDİSİ GELİŞTİRME KURSU Pratik olarak Q, RMR, GSI ışığında belirlenen NATM Kazı Kaya Sınıfı’na g |
| 7 | 0.6098 | `DOC000047-C0198` | DOC000047 | 9.2 BACKGROUND AND CONCEPTS | ## 9.2 BACKGROUND AND CONCEPTS The origins of the NATM lie in the alpine tunnel engineering in the early 1960s. In 1948, |
| 8 | 0.6075 | `DOC000118-C0001` | DOC000118 | Requirements for a successful application of NATM | **Project and site organization of a NATM tunnel project on the example of the Koralm tunnel** **Hanns Wagner** OBB – Au |
| 9 | 0.6046 | `DOC000131-C0008` | DOC000131 | E.7.6 Önemli Tasar ı m Özellikleri | ## E.7.6 Önemli Tasar ı m Özellikleri - NATM tüneli için jeoteknik risk yönetimi - A ş amal ı kaz ı - Ön destek - İ lave |
| 10 | 0.6015 | `DOC000124-C0020` | DOC000124 |  | Yeni Avusturya Tünel Açma Yöntemi (NATM) esasen bir kaya sınıflama sistemi olmayıp tünel inşaası sırasında yeraltı kazıl |

#### `tunnel ventilation`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.6891 | `DOC000197-C0023` | DOC000197 | 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) | ## 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) - 15 kV line supplies the explosion-proof IM2 cabinet on  |
| 2 | 0.6865 | `DOC000037-C0026` | DOC000037 | 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) | ## 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) To ensure the correct amount of fresh air in all working  |
| 3 | 0.6727 | `DOC000047-C0049` | DOC000047 | 2.4.5 Ventilation Requirements | ## 2.4.5 Ventilation Requirements The ventilation system of a tunnel operates to maintain acceptable air quality levels  |
| 4 | 0.6557 | `DOC000003-C0075` | DOC000003 | 4.2.1 Typical Road Tunnels | ## 4.2.1 Typical Road Tunnels Road tunnels that are longer than 1,000 feet (304 meters) typically have forced air ventil |
| 5 | 0.6541 | `DOC000015-C0024` | DOC000015 | Basic Types of Ventilation Systems 1.4.9.1 | ## Basic Types of Ventilation Systems 1.4.9.1 There are five basic types of tunnel ventilation systems: - Natural Ventil |
| 6 | 0.6420 | `DOC000174-C0077` | DOC000174 | 5.1.2 Recognised recommendations | <!-- image --> / Title / Issued by / Reference (link) / Date / Administrative status / Comments / Still in use / /------ |
| 7 | 0.6268 | `DOC000003-C0184` | DOC000003 | Countermeasure 2: Ventilation System | ## Countermeasure 2: Ventilation System The ventilation system is usually the most important life safety system in the t |
| 8 | 0.6242 | `DOC000170-C0118` | DOC000170 | Position of fire in tunnel has been considered the following | ## Position of fire in tunnel has been considered the following: <!-- image --> Conditions for road users during develop |
| 9 | 0.6236 | `DOC000003-C0119` | DOC000003 | Note s : | / S afety S y s tem / S afety S y s tem / Life S afety / Tunnel Operation s / Operation Re s toration / /--------------- |
| 10 | 0.6218 | `DOC000003-C0157` | DOC000003 | Path to Tar g et: Tunnel Air | ## Path to Tar g et: Tunnel Air S upply S y s tem Tar g et: Tunnel Occupant s and S urroundin g Population in Di s char  |

#### `rock bolt design`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.6120 | `DOC000047-C0131` | DOC000047 | 6.5.2.2 Rock Bolts | ## 6.5.2.2 Rock Bolts Rock bolts (Figure 6-18) have a friction or grout anchor in the rock and are tensioned as soon as  |
| 2 | 0.5606 | `DOC000047-C0215` | DOC000047 | 9.5.2.2 Practical Aspects | ## 9.5.2.2 Practical Aspects Several practical aspects related to rock dowel/bolt installation in the field have been su |
| 3 | 0.5516 | `DOC000047-C0214` | DOC000047 | 9.5.2 Rock Reinforcement | ## 9.5.2 Rock Reinforcement As discussed in Chapter 6, rock reinforcement and rock mass act as a complex interactive sys |
| 4 | 0.5455 | `DOC000047-C0136` | DOC000047 | 6.6.1 Empirical Method | Also note that the Q-system was developed from over 1000 tunnel projects, most of which are in Scandinavia and all of wh |
| 5 | 0.5357 | `DOC000037-C0034` | DOC000037 | 3.2 Ground Reinforcement | ## 3.2 Ground Reinforcement There are three distinct types of ground reinforcement methods (Woodward, 2005) and (Whittak |
| 6 | 0.5351 | `DOC000047-C0182` | DOC000047 | 8.2.3 Blocky Rock | ## 8.2.3 Blocky Rock As discussed in Chapter 6, rock is a basically strong material which requires little or no structur |
| 7 | 0.5267 | `DOC000047-C0134` | DOC000047 | 6.6 DESIGN AND EVALUATION OF TUNNEL SUPPORTS | ## 6.6 DESIGN AND EVALUATION OF TUNNEL SUPPORTS There exists a wide range of tunnel support systems as shown in previous |
| 8 | 0.5256 | `DOC000308-C0009` | DOC000308 | Elements of Commonly Used Excavation and Support Classes (ES | ## Elements of Commonly Used Excavation and Support Classes (ESC) in Rock / Ground Mass Quality - Rock / Excavation Sequ |
| 9 | 0.5245 | `DOC000003-C0083` | DOC000003 | Lining Failure from Explosion | / Type / Description / Sketch / /--------------------------------------/------------------------------------------------ |
| 10 | 0.5202 | `DOC000121-C0026` | DOC000121 | Excavation cost € per m3 Tunnelling Classes 5/xx and 6/xx | / **Top heading** / / üm=0.10 m / **6/7.92** / / / /-------------------------------------------------------------------- |

#### `tunnel maintenance inspection`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.7303 | `DOC000002-C0002` | DOC000002 | 14.1.2 Inspection | ## 14.1.2 Inspection Inspection of a tunnel must be undertaken daily by an inspection team, and check the following: -  |
| 2 | 0.7198 | `DOC000002-C0003` | DOC000002 | 14.1.3 Maintenance of Tunnel | ## 14.1.3 Maintenance of Tunnel Routine maintenance activities are summarized in Table 14.1-2. Routine maintenance shoul |
| 3 | 0.6992 | `DOC000015-C0055` | DOC000015 | Inspection Practices 4.5.1 | ## Inspection Practices 4.5.1 The tunnel inspection organization should develop a set of best practices to help maintain |
| 4 | 0.6915 | `DOC000015-C0056` | DOC000015 | Initial Inspection 4.6.1 | ## Initial Inspection 4.6.1 An initial inspection should be performed on existing highway tunnels within the interval sp |
| 5 | 0.6893 | `DOC000015-C0033` | DOC000015 | Chapter 3 - Maintenance | ## Chapter 3 - Maintenance Figure 3.1 - Groundwater induced corrosion and deterioration. <!-- image --> Figure 3.2 - Lea |
| 6 | 0.6844 | `DOC000015-C0016` | DOC000015 | 1.2.4.2 Tunnel Inspection | ## 1.2.4.2 Tunnel Inspection The SNTI is used with the TOMIE to collect comprehensive tunnel inspection data on the stru |
| 7 | 0.6778 | `DOC000015-C0048` | DOC000015 | Responsibilities 4.3.1 | ## Responsibilities 4.3.1 The tunnel inspection organization is responsible for developing and maintaining inspection po |
| 8 | 0.6777 | `DOC000015-C0026` | DOC000015 | Operations 1.5.1 | ## Operations 1.5.1 Chapter 2 discusses the operation of tunnels. This chapter presents an organizational structure for  |
| 9 | 0.6770 | `DOC000015-C0096` | DOC000015 | 4.12 Tunnel Inventory and Inspection Documents | ## 4.12 Tunnel Inventory and Inspection Documents Tunnel inventory and inspection data should be collected and documente |
| 10 | 0.6692 | `DOC000004-C0003` | DOC000004 | 7.5 Service Life Considerations | ## 7.5 Service Life Considerations The various components of a tunnel have very different service lives. The structure i |

#### `TBM excavation`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.6683 | `DOC000011-C0011` | DOC000011 | 2.2.2. Mechanized Tunnelling | / Description of the construction method / TBM tunnelling allows to maintain continuous active support onto the tunnel f |
| 2 | 0.6507 | `DOC000015-C0019` | DOC000015 | Bored Tunnels 1.4.1.3 | ## Bored Tunnels 1.4.1.3 A Tunnel Boring Machine (TBM) is a shield with bits mounted on a rotating cutter head that exca |
| 3 | 0.6488 | `DOC000011-C0010` | DOC000011 | 2.2.2. Mechanized Tunnelling | ## 2.2.2. Mechanized Tunnelling Since the 1990s, mechanized tunnelling and in particular TBM excavation has took hold as |
| 4 | 0.6484 | `DOC000193-C0008` | DOC000193 | TBM TEKNİK ÖZELLİKLERİ | ## TBM TEKNİK ÖZELLİKLERİ - T-1 Tünelinde Robbins marka 13.77 m çapında 105 metre uzunluğunda Crossover (EPB/Hard Rock)  |
| 5 | 0.6451 | `DOC000037-C0045` | DOC000037 | R. Hasanpour | ## R. Hasanpour Hacettepe University, Mining Engineering Dept., Ankara, Turkey ABSTRACT In this study, the authors prese |
| 6 | 0.6427 | `DOC000037-C0061` | DOC000037 | 2.4 The Excavation System | ## 2.4 The Excavation System The main component of the excavation system was the HR shielded TBM having the characterist |
| 7 | 0.6424 | `DOC000177-C0013` | DOC000177 | 5. SEÇİLMİŞ ARALIKLARDA ÜÇ TBM İN PERFORMANSLARININ KARŞILAŞ | ## 5. SEÇİLMİŞ ARALIKLARDA ÜÇ TBM İN PERFORMANSLARININ KARŞILAŞTIRILMASI laminalı ve ara geçişli silttaşı, çamurtaşı ve  |
| 8 | 0.6374 | `DOC000037-C0050` | DOC000037 | 5 CONCLUSIONS | ## 5 CONCLUSIONS In this article, the authors presented an analytical procedure based on the approach of Aydan et al. (1 |
| 9 | 0.6367 | `DOC000037-C0090` | DOC000037 | REFERENCES | ## REFERENCES Alber, M., 2000. Advance rates of hard rock TBMs and their effects on project economics. Tunnell. Undergr. |
| 10 | 0.6360 | `DOC000205-C0022` | DOC000205 | Two more JimT/TerraTec ePBmS delivered for Taiwan'S Taoyuan  | ## Two more JimT/TerraTec ePBmS delivered for Taiwan'S Taoyuan mrT green line on behalf of Jim Technology (JimT), TerraT |

#### `tunnel fire safety`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.7076 | `DOC000047-C0310` | DOC000047 | 14.5 HEALTH &amp; SAFETY | Fires in tunnels are especially dangerous and can lead to extensive damage and risk to worker's safety and life. The Tun |
| 2 | 0.6637 | `DOC000003-C0017` | DOC000003 | Fire (Unintentional) | ## Fire (Unintentional) Unintentional fire is more probable than intentional fire and has occurred in several tunnel sys |
| 3 | 0.6620 | `DOC000047-C0040` | DOC000047 | 1.3.6 Fire-Life Safety Systems | ## 1.3.6 Fire-Life Safety Systems Safety in the event of a fire is of paramount importance in a tunnel. The catastrophic |
| 4 | 0.6607 | `DOC000015-C0029` | DOC000015 | 2.4 Emergency Response and Incident Management | ## 2.4 Emergency Response and Incident Management Incidents requiring immediate action can occur in tunnels. Emergency o |
| 5 | 0.6489 | `DOC000003-C0048` | DOC000003 | References | ## References Anderson,T.,&amp; Paaske,B.J. (2002).'Safety in Railway Tunnels and Selection of Tunnel Concept.'Paper pre |
| 6 | 0.6387 | `DOC000170-C0118` | DOC000170 | Position of fire in tunnel has been considered the following | ## Position of fire in tunnel has been considered the following: <!-- image --> Conditions for road users during develop |
| 7 | 0.6376 | `DOC000209-C0008` | DOC000209 | Sayfa 9 | ## Sayfa 9 SUMMARY OF TUNNEL FIRES AND SAFETY STRATEGY Søvik emphasises that heavy vehicles are over-represented in the  |
| 8 | 0.6339 | `DOC000156-C0002` | DOC000156 | ULUSLAR ARASI MEVZUATTA TÜNEL YANGIN GÜVENLİĞİ | ## ULUSLAR ARASI MEVZUATTA TÜNEL YANGIN GÜVENLİĞİ <!-- image --> RecommendationsOf The Group Of Experts On The Safety of |
| 9 | 0.6326 | `DOC000021-C0009` | DOC000021 | Safety and security | ## Safety and security The entrance to the Pont de l'Alma tunnel, the site where Diana's car hit a Fiat and then the wal |
| 10 | 0.6307 | `DOC000003-C0050` | DOC000003 | Conclusions | ## Conclusions Although safety procedures called for a train to speed through the tunnel if fire broke out, the train st |

#### `geological investigation`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.5953 | `DOC000047-C0057` | DOC000047 | 3.3.6 Structure Preconstruction Survey | ## 3.3.6 Structure Preconstruction Survey Structures located within the zone of potential influe nce may experience a ce |
| 2 | 0.5928 | `DOC000047-C0051` | DOC000047 | 3.1.1 Phasing of Geotechnical Investigations | ## 3.1.1 Phasing of Geotechnical Investigations Amid the higher cost of a complete geotechnical investigation program fo |
| 3 | 0.5920 | `DOC000111-C0002` | DOC000111 | Geological and geotechnical investigation | ### Geological and geotechnical investigation - laboratory analyses and testing - swelling tests (48 samples) - free swe |
| 4 | 0.5885 | `DOC000047-C0067` | DOC000047 | 3.5.4.2 Geophysical Testing | ## 3.5.4.2 Geophysical Testing Geophysical tests are indirect methods of exploration in which changes in certain physica |
| 5 | 0.5865 | `DOC000047-C0081` | DOC000047 | 3.8.2 Geologic Face Mapping | ## 3.8.2 Geologic Face Mapping With open-face tunneling methods, including the sequential excavation method (SEM), open- |
| 6 | 0.5796 | `DOC000302-C0051` | DOC000302 | Slayt 55 | ## Slayt 55 KONTROL MÜHENDİSİ GELİŞTİRME KURSU JEOFİZİK ARAŞTIRMALARI genellikle iki metotla yapılmaktadır: Sismik Kırıl |
| 7 | 0.5748 | `DOC000047-C0058` | DOC000047 | 3.5.1 General | ## 3.5.1 General Ground conditions including geological, geotechnical, a nd hydrological conditions, have a major impact |
| 8 | 0.5734 | `DOC000047-C0061` | DOC000047 | 3.5.1 General | A general approach to control the cost of subsurface investigations while obtaining the information necessary for design |
| 9 | 0.5723 | `DOC000307-C0011` | DOC000307 | Akış, Satıcı | ## Akış, Satıcı - Hoek, E. 1994. Strength of rock and rock masses, ISRM News Journal, 2(2), 4-16. - Hoek, E., 2007. Prac |
| 10 | 0.5673 | `DOC000302-C0050` | DOC000302 | Slayt 54 | ## Slayt 54 KONTROL MÜHENDİSİ GELİŞTİRME KURSU TÜNEL GÜZERGAHLARINDA JEOFİZİK ARAŞTIRMALARI Tünelde yapılan jeofizik ara |

#### `shotcrete`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.5600 | `DOC000047-C0358` | DOC000047 | GLOSSARY | / Flashcrete (Sealing Shotcrete) / Typically unreinforced or steel fiber re inforced sprayed concrete layer to seal off  |
| 2 | 0.5573 | `DOC000047-C0250` | DOC000047 | 10.7 SHOTCRETE LINING | ## 10.7 SHOTCRETE LINING As discussed in Chapter 9, shotcrete represents a structurally and qualitatively equal alternat |
| 3 | 0.5543 | `DOC000007-C0012` | DOC000007 | Table of Contents | / 2.8.3 / Shotcrete / /----------------------------------------------------/-------------------------------------------- |
| 4 | 0.5436 | `DOC000227-C0004` | DOC000227 |  | K.T.Ş. nin ilgili kısımlarındaki esaslar ve şartlara, projeye ve İdarenin talimatına uygun olarak her dozda püskürtme be |
| 5 | 0.5357 | `DOC000047-C0212` | DOC000047 | 9.5.1.1 Effect of Shotcrete | ## 9.5.1.1 Effect of Shotcrete When concrete is sprayed on a rough ground surface, it fills small openings, cracks and f |
| 6 | 0.5271 | `DOC000047-C0211` | DOC000047 | 9.4.7 Excavation Methods | ## 9.4.7 Excavation Methods During the history of application of the SEM/NATM, tunneling methods for a wide variety of g |
| 7 | 0.5212 | `DOC000047-C0351` | DOC000047 | 16.4.5 Shotcrete Repairs | ## 16.4.5 Shotcrete Repairs As discussed in Chapter 10, there are two processes for the application of shotcrete; Dry Pr |
| 8 | 0.5199 | `DOC000047-C0349` | DOC000047 | 16.4 STRUCTURAL REPAIR - CONCRETE | ## 16.4 STRUCTURAL REPAIR - CONCRETE ## 16.4.1 Introduction The repair of concrete delaminations and spalls in tunnels h |
| 9 | 0.5015 | `DOC000047-C0213` | DOC000047 | 9.5.1.1 Effect of Shotcrete | In contrast for tunnels under high overburden the prevention of ground deformation and surface settlement plays a second |
| 10 | 0.5010 | `DOC000018-C0003` | DOC000018 | Support | ## Support Where the tunneling ground comprises massive, strong, and intact rock, the tunnel can be safely excavated to  |

#### `tunnel construction cost`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.7044 | `DOC000016-C0006` | DOC000016 | Appendix A - Tunnel estimate example | ## Appendix A - Tunnel estimate example This example assumes a 7km tunnel is constructed using slurry machines in a rura |
| 2 | 0.6680 | `DOC000012-C0001` | DOC000012 |  | **COSTS OF CONSTRUCTION, OPERATION, UPGRADING - FINANCIAL ASPECTS** - [**1. Foreword**](https://tunnelsmanual.piarc.org/ |
| 3 | 0.6589 | `DOC000011-C0019` | DOC000011 | Results | ## Results The average unit costs related to difference in construction method and tunnel sections are reported in the f |
| 4 | 0.6533 | `DOC000018-C0005` | DOC000018 | V. Tunneling Costs | ## V. Tunneling Costs Tunneling costs vary widely across the world and are dependent on a number of key factors includin |
| 5 | 0.6475 | `DOC000014-C0005` | DOC000014 | 4 COMPARING GREEK TUNNEL COST DATA WITH INTERNATIONAL EXAMPL | It can be seen that for all data there is a positive correlation between construction cost and the span of tunnel. This  |
| 6 | 0.6455 | `DOC000017-C0003` | DOC000017 | International Research Journal of Engineering and Technology | ## International Research Journal of Engineering and Technology (IRJET) e-ISSN: 2395-0056 Volume: 08 Issue: 07 / July 20 |
| 7 | 0.6434 | `DOC000041-R1-C0001` | DOC000041 | Estimate of annual operating costs Highway Tunnel | # Estimate of annual operating costs Highway Tunnel ## Sayfa 1 Newfoundland Fixed Link Pre-feasibility StudyPage 1 of 2  |
| 8 | 0.6365 | `DOC000017-C0002` | DOC000017 | 3. LCCA OF TUNNEL | ## 3. LCCA OF TUNNEL Life cycle cost of tunnel include agency costs, user costs and society costs with further subdivisi |
| 9 | 0.6361 | `DOC000041-R1-C0002` | DOC000041 | Sayfa 2 | ## Sayfa 2 Newfoundland Fixed Link Pre-feasibility StudyPage 2 of 2 Highway Tunnel Estimate of annual operating costs D. |
| 10 | 0.6347 | `DOC000016-C0003` | DOC000016 | 3 Principal Cost Elements | ## 3 Principal Cost Elements For the purposes of this guide, costs have been separated into the following categories: -  |

#### `waterproofing`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.6467 | `DOC000047-C0271` | DOC000047 | 11.5.1 External Waterproofing of Tunnels | ## 11.5.1 External Waterproofing of Tunnels External waterproofing for tunnel elements should be considered for both ste |
| 2 | 0.6458 | `DOC000047-C0039` | DOC000047 | Allowable Infiltration | ## Allowable Infiltration / Tunnels / ≤ 0.002 gal/sq. ft/day / /--------------------------/--------------------------/ / |
| 3 | 0.6253 | `DOC000047-C0201` | DOC000047 | 9.3.4 Waterproofing | ## 9.3.4 Waterproofing The SEM uses flexible, continuous membranes for tunnel waterproofing. Most frequently PVC membran |
| 4 | 0.6244 | `DOC000015-C0036` | DOC000015 | Interior Composite Tunnel Liners (NCHRP, 2010; FHWA 2005) 3. | ## Interior Composite Tunnel Liners (NCHRP, 2010; FHWA 2005) 3.6.2 A composite liner can be constructed on the interior  |
| 5 | 0.5945 | `DOC000007-C0006` | DOC000007 | Table of Contents | / / 5.3.1.7 / Requirements of the users . . . . . . . . . . . . . . . . . . . . . . . . . . / . 214 / /-----/----------- |
| 6 | 0.5822 | `DOC000047-C0109` | DOC000047 | 5.7.1 Construction Dewatering | ## 5.7.1 Construction Dewatering When groundwater levels are higher than the base level of the tunnel, excavations will  |
| 7 | 0.5786 | `DOC000087-C0253` | DOC000087 | 350.06.01.02.03 Aksesuar | ## 350.06.01.02.03 Aksesuar Malzemenin tespit edilmesi, koruma bandı, genleşme derzlerinin güçlendirilmesi, yapıştırma f |
| 8 | 0.5776 | `DOC000015-C0035` | DOC000015 | Catchment Troughs and Pipes 3.6.1 | ## Catchment Troughs and Pipes 3.6.1 Troughs may be installed on the inside of the liner to catch leaking water and conv |
| 9 | 0.5704 | `DOC000236-C0254` | DOC000236 | 350.06.01.03.01 Yüzey Hazirlanması | ## 350.06.01.03.01 Yüzey Hazirlanması - d dz n zi y y i yadd d dnn arındırılmış olacaktır. 2. Su yalıtımının uygulanması |
| 10 | 0.5694 | `DOC000087-C0250` | DOC000087 | 350.06.01.01 Genel | ## 350.06.01.01 Genel Bu bölüm nihai beton kaplama dışına monte edilen sürekli su yalıtım membranı vasıtasıyla tüm yer a |

### Turkish

#### `tünel havalandırması`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.6907 | `DOC000096-C0004` | DOC000096 | 3 Korunma Hücreleri | ### 3 Korunma Hücreleri ĠĢletme amacına uygun olarak; bakım-onarım, kurtarma ve diğer ihtiyaçlara cevap verecek üniteler |
| 2 | 0.6717 | `DOC000045-C0005` | DOC000045 | TÜNEL GÜVENLİĞİ PROJE KRİTERLERİ (1) | / / Dayanıklılığı / / / / / / / yerlerde zorunludur. / /-------------------------/-------------------------------------- |
| 3 | 0.6615 | `DOC000075-C0014` | DOC000075 |  | / Aydınlatma / Normal Aydınlatma / 8.1 / • / • / • / • / • / / /--------------------------/----------------------------- |
| 4 | 0.6539 | `DOC000075-C0065` | DOC000075 |  | Her tünel belirli oranda doğal havalandırmaya sahiptir. Bu durum tünelin iki portalı arasındaki basınç farkından, araçla |
| 5 | 0.6492 | `DOC000287-C0068` | DOC000287 | Slayt 71 | ## Slayt 71 Tünellerde güvenli ve duman kalitesi çok daha iyi olan emülsyon patlayıcıların kullanılması kapalı alanda ça |
| 6 | 0.6424 | `DOC000075-C0092` | DOC000075 |  | Jet fanların grup halinde çalışması sebebiyle rezonansa girmesinin önlenmesi gerekmektedir. Her fanın kendi süspansiyon  |
| 7 | 0.6319 | `DOC000197-C0023` | DOC000197 | 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) | ## 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) - 15 kV line supplies the explosion-proof IM2 cabinet on  |
| 8 | 0.6277 | `DOC000075-C0100` | DOC000075 |  | Tünel içinde yangını görenlerin tünel yönetimi ikaz edebilmesi için gerekebilecek araçlardan biri de Yangın İhbar Butonl |
| 9 | 0.6274 | `DOC000075-C0066` | DOC000075 |  | **Acil Durum** **Tünel İçi Acil Durum** **Portalı Amsteg Erişim** **Tüneli (Hav. Amaçlı)** Şekil 42. Gotthard Base Tünel |
| 10 | 0.6272 | `DOC000167-C0010` | DOC000167 | 4.2. Türkiye'de Karayolu Tünellerinde Meydana Gelen Trafik K | Türkiye'deki Karayolu Tünellerinde Trafik Güvenliği |

#### `kaya bulonu`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.4632 | `DOC000124-C0053` | DOC000124 |  | Bulonlara etkiyen kuvvetler aşağıdaki çizelgede özetlenmiştir. Plaxis'de elde edilen çıktılar bulonun , metresi içindir. |
| 2 | 0.4542 | `DOC000216-C0001` | DOC000216 | Tünel Kontrol Mühendisi Geliştirme Kursu Tünel Destekleme El | <!-- image --> <!-- image --> # Tünel Kontrol Mühendisi Geliştirme Kursu Tünel Destekleme Elemanları 24~28.02.2020, Anka |
| 3 | 0.4475 | `DOC000290-C0004` | DOC000290 | Kaya şevlerinin duraylılığı hesaplamaları genel olarak; | Lb = 0,019 x 616 x 420 / (20)1/2 = 1,09m <!-- image --> / SUNUM ADI / / /-------------/----------------/ / / www.kgm.gov |
| 4 | 0.4443 | `DOC000294-C0023` | DOC000294 | ÖLÇÜM VERİLERİNİN DEĞERLENDİRİLMESİ | # ÖLÇÜM VERİLERİNİN DEĞERLENDİRİLMESİ <!-- image --> # ÖLÇÜM VERİLERİNİN DEĞERLENDİRİLMESİ Ölçüm Bulonu Detayı <!-- imag |
| 5 | 0.4370 | `DOC000293-C0009` | DOC000293 | Tünel Kazısı Sırasında Deney | # Tünel Kazısı Sırasında Deney - - Uygulanacak deney kuvveti, deneye tabii tutulacak kaya bulonu kopma yükünün en az %80 |
| 6 | 0.4361 | `DOC000285-C0025` | DOC000285 | KALİTE KONTROL LABORATUVARINDA YAPILAN DENEYLER | # KALİTE KONTROL LABORATUVARINDA YAPILAN DENEYLER TÜNEL DENEYLERİ # 1.BULON ÇEKME DENEYLERİ Amaç Tünel yapım projesinde  |
| 7 | 0.4260 | `DOC000087-C0064` | DOC000087 | 252.04 Yapım Şartları | ## 252.04 Yapım Şartları Donatılı toprakarme duvar yapımında çalışan ekipte daha önce bu tür duvar yapımında çalışmış, d |
| 8 | 0.4253 | `DOC000126-C0010` | DOC000126 | SEÇENEK 4 | ## SEÇENEK 4 / Süren / Süren / Süren / Bulon (SN) / Bulon (SN) / Bulon (SN) / Bulon (SN) / /---------------------------- |
| 9 | 0.4231 | `DOC000076-C0002` | DOC000076 |  | Bulon ana destek elemanlarından birisidir. Zeminin kayma dayanımını arttırır. Kaya bloklarının sabitlenmesinde noktasal  |
| 10 | 0.4211 | `DOC000236-C0063` | DOC000236 | 252.04 Yapım Şartları | ## 252.04 Yapım Şartları Donatılı toprakarme duvar yapımında çalışan ekipte daha önce bu tür duvar yapımında çalışmış, d |

#### `püskürtme beton`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.7143 | `DOC000072-C0018` | DOC000072 | 47 Püskürtme Beton Kaplamalar | #### 47 Püskürtme Beton Kaplamalar Püskürtme beton, onarım yada yapım amacıyla önceden kuru yada ıslak yolla hazırlanara |
| 2 | 0.7103 | `DOC000087-C0276` | DOC000087 | 351.08.02 Alt Yüzey | ## 351.08.02 Alt Yüzey Klasik betonla karşılaştırıldığında püskürtme beton kalınlığı genellikle daha azdır. Püskürtme be |
| 3 | 0.6843 | `DOC000214-C0002` | DOC000214 | Tünel Kontrol Mühendisi Geliştirme Kursu Tünel Destekleme El | - ‘Tünelde Püskürtme Betonu (Shotcrete) Yapılması’ teklif birim fiyatı üzerinden ‘m3’ cinsinden yapılır - Birim Fiyat Ta |
| 4 | 0.6781 | `DOC000087-C0278` | DOC000087 | 351.08.07 Püskürtmenin Uygulanma Tekniği | ## 351.08.07 Püskürtmenin Uygulanma Tekniği Püskürtme beton uygulamasına geçmeden önce uygulama sırasında aşağıdaki husu |
| 5 | 0.6758 | `DOC000236-C0277` | DOC000236 | 351.07.04 Çevresel Şartlarla İlgili Gereksinimler | ## 351.07.04 Çevresel Şartlarla İlgili Gereksinimler Püskürtme beton, projecinin öngördüğü gereksinimlere, Tablo-308-22- |
| 6 | 0.6722 | `DOC000236-C0279` | DOC000236 | 351.08.07 Püskürtmenin Uygulanma Tekniği | ## 351.08.07 Püskürtmenin Uygulanma Tekniği Püskürtme beton uygulamasına geçmeden önce uygulama sirasında aşağıdaki husu |
| 7 | 0.6687 | `DOC000283-C0059` | DOC000283 | Slayt 63 | ## Slayt 63 Çelik tel tel donatılı beton ,yüksek enerji yutma kapasitesine ve dayanıklılığa sahip sünek betondur. Çelik  |
| 8 | 0.6687 | `DOC000304-C0059` | DOC000304 | Slayt 63 | ## Slayt 63 Çelik tel tel donatılı beton ,yüksek enerji yutma kapasitesine ve dayanıklılığa sahip sünek betondur. Çelik  |
| 9 | 0.6659 | `DOC000196-C0024` | DOC000196 | 3 SONUÇLAR | ## 3 SONUÇLAR Püskürtme beton uygulamalarında en büyük pay, madencilik sektörüne aittir. En önemli uygulama alanları ram |
| 10 | 0.6641 | `DOC000293-C0011` | DOC000293 | Püskürtme Beton | # Püskürtme Beton - Uygulanan her 100 m3 teorik ölçüm püskürtme betonu için bir deney panosuna püskürtme yapılacak ve pa |

#### `tünel bakım ve işletmesi`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.6978 | `DOC000036-C0030` | DOC000036 | ÜÇÜNCÜ BÖLÜM Tünel İşletmesi ile İlgili Görevler Tünel işlet | MADDE 6 (1) Devlet veya il yollarındaki tünel veya grup tünellerin işletmesi; - a) Kontrol Merkezi olan tünel veya grup  |
| 2 | 0.6887 | `DOC000036-C0031` | DOC000036 | Risk analizi | MADDE 7 (1) Tünel işletmesinden sorumlu birimlerin görevleri şunlardır; - a) Tünellere ait nihai projelerin kopyalarını  |
| 3 | 0.6644 | `DOC000036-C0029` | DOC000036 | Taşra teşkilat yapısı | MADDE 5 (1) Devlet ve il yollarındaki tünel veya grup tünellerin işletmesi, Tesisler ve Bakım Dairesi Başkanlığına bağlı |
| 4 | 0.6357 | `DOC000036-C0033` | DOC000036 | Protokol | MADDE 9 (1) Karayolu kullanıcılarının güvenliğini açıkça etkileyen tünellerdeki yangınlar ve kazalar ile bunların sıklığ |
| 5 | 0.6343 | `DOC000075-C0001` | DOC000075 |  | <!-- image --> <!-- image --> **T.C.** **ULAŞTIRMA DENİZCİLİK VE HABERLEŞME BAKANLIĞI Karayolları Genel Müdürlüğü** TÜNE |
| 6 | 0.6319 | `DOC000036-C0035` | DOC000036 | Alternatif güzergahlar ve gabariler | MADDE 11 (1) Tünel güvenliği ile ilgili olarak aşağıdaki önlemler alınır: - a) Tünelden geçen trafiğin sürekli ve güvenl |
| 7 | 0.6298 | `DOC000075-C0168` | DOC000075 |  | **ı) Risk analizi: Belirli bir tünelin bir gün için tahmin edilen ağır vasıta sayısının yanı sıra, trafik özellikleri, t |
| 8 | 0.6278 | `DOC000075-C0018` | DOC000075 |  | *Öneri:* Yukarıda belirtilen kurumlar arasında koordinasyonu ve denetimi sağlayacak idari yetkisi bulunan bir otoıite/ku |
| 9 | 0.6269 | `DOC000075-C0116` | DOC000075 |  | S **Yangın İhbar ve Önleme Sistemi** üç aylık/aylık bakımlarında aşağıdaki hususlara dikkat edilmelidir; - Aylık bakım y |
| 10 | 0.6263 | `DOC000096-C0004` | DOC000096 | 3 Korunma Hücreleri | ### 3 Korunma Hücreleri ĠĢletme amacına uygun olarak; bakım-onarım, kurtarma ve diğer ihtiyaçlara cevap verecek üniteler |

#### `jeoteknik araştırma`

| # | score | chunk_id | document | heading | preview |
|---|---|---|---|---|---|
| 1 | 0.5936 | `DOC000302-C0050` | DOC000302 | Slayt 54 | ## Slayt 54 KONTROL MÜHENDİSİ GELİŞTİRME KURSU TÜNEL GÜZERGAHLARINDA JEOFİZİK ARAŞTIRMALARI Tünelde yapılan jeofizik ara |
| 2 | 0.5680 | `DOC000302-C0001` | DOC000302 | TÜNELLERDE GÜZERGAH SEÇİMİ VE jeoteknik araştırmalar son | # TÜNELLERDE GÜZERGAH SEÇİMİ VE jeoteknik araştırmalar son ## Slayt 1 JEOLOJİK HİZMETLER ŞUBESİ MÜDÜRLÜĞÜ AYDIN DURUKAN  |
| 3 | 0.5665 | `DOC000302-C0040` | DOC000302 | Slayt 44 | ## Slayt 44 KONTROL MÜHENDİSİ GELİŞTİRME KURSU Tünel Jeolojik – Jeoteknik Raporu Tünel jeolojik – Jeoteknik raporu; Gene |
| 4 | 0.5585 | `DOC000302-C0039` | DOC000302 | Slayt 43 | ## Slayt 43 KONTROL MÜHENDİSİ GELİŞTİRME KURSU Jeoteknik Modelin Kurulumu Tünel jeolojik - jeoteknik model için; Arazi ç |
| 5 | 0.5534 | `DOC000302-C0051` | DOC000302 | Slayt 55 | ## Slayt 55 KONTROL MÜHENDİSİ GELİŞTİRME KURSU JEOFİZİK ARAŞTIRMALARI genellikle iki metotla yapılmaktadır: Sismik Kırıl |
| 6 | 0.5425 | `DOC000047-C0051` | DOC000047 | 3.1.1 Phasing of Geotechnical Investigations | ## 3.1.1 Phasing of Geotechnical Investigations Amid the higher cost of a complete geotechnical investigation program fo |
| 7 | 0.5389 | `DOC000205-C0041` | DOC000205 | KAYNAKLAR | Rostami, J., Ozdemir, L., Neil, D.M. 1994. Performance prediction: a key issue in mechanical hard rock mining. Min Eng,  |
| 8 | 0.5343 | `DOC000047-C0057` | DOC000047 | 3.3.6 Structure Preconstruction Survey | ## 3.3.6 Structure Preconstruction Survey Structures located within the zone of potential influe nce may experience a ce |
| 9 | 0.5299 | `DOC000302-C0053` | DOC000302 | Slayt 57 | ## Slayt 57 KONTROL MÜHENDİSİ GELİŞTİRME KURSU Jeoteknik Model ; Birimlerin Yaşı, Litolojisi, Dokusu, Tane Boyu, Konumla |
| 10 | 0.5291 | `DOC000222-C0001` | DOC000222 |  | SUNUM ADI AYNA HARİTALAMALARI VE DEĞERLENDİRMELERİ AYDIN DURUKAN JEOLOJİK HİZMETLER ŞUBESİ MÜDÜRLÜĞÜ KONTROL MÜHENDİSİ G |

## Recovery retrieval sanity

Queries targeting the recovered documents, to confirm the repaired text is reachable without dominating unrelated queries.

### Cost documents (DOC000009 / DOC000041)

#### `annual tunnel operating costs`

| # | score | chunk_id | document | kind | preview |
|---|---|---|---|---|---|
| 1 | 0.7055 | `DOC000041-R1-C0001` | DOC000041 | recovery_chunk | # Estimate of annual operating costs Highway Tunnel ## Sayfa 1 Newfoundland Fixed Link Pre-feasibility StudyPage 1 of 2  |
| 2 | 0.6764 | `DOC000041-R1-C0002` | DOC000041 | recovery_chunk | ## Sayfa 2 Newfoundland Fixed Link Pre-feasibility StudyPage 2 of 2 Highway Tunnel Estimate of annual operating costs D. |
| 3 | 0.6704 | `DOC000019-C0005` | DOC000019 | canonical_chunk | ## 2.2 Estimating Operational and Regular Maintenance Costs - 2.2.1 Those requirements and tasks on road infrastructure  |
| 4 | 0.6545 | `DOC000009-R1-C0002` | DOC000009 | recovery_chunk | ## Assumptions: Facility operates 12 hours/day, 7 days/week 50 percent of this time the facility is fully staffed with t |
| 5 | 0.6522 | `DOC000017-C0003` | DOC000017 | canonical_chunk | ## International Research Journal of Engineering and Technology (IRJET) e-ISSN: 2395-0056 Volume: 08 Issue: 07 / July 20 |

#### `tunnel maintenance cost`

| # | score | chunk_id | document | kind | preview |
|---|---|---|---|---|---|
| 1 | 0.6951 | `DOC000041-R1-C0001` | DOC000041 | recovery_chunk | # Estimate of annual operating costs Highway Tunnel ## Sayfa 1 Newfoundland Fixed Link Pre-feasibility StudyPage 1 of 2  |
| 2 | 0.6875 | `DOC000041-R1-C0003` | DOC000041 | recovery_chunk | ## Sayfa 3 Newfoundland Fixed Link Pre-feasibility StudyPage 1 of 2 Highway Tunnel Estimate of annual maintenance costs  |
| 3 | 0.6736 | `DOC000041-R1-C0004` | DOC000041 | recovery_chunk | ## Sayfa 4 Newfoundland Fixed Link Pre-feasibility StudyPage 2 of 2 Highway Tunnel Estimate of annual maintenance costs  |
| 4 | 0.6689 | `DOC000016-C0006` | DOC000016 | canonical_chunk | ## Appendix A - Tunnel estimate example This example assumes a 7km tunnel is constructed using slurry machines in a rura |
| 5 | 0.6652 | `DOC000002-C0007` | DOC000002 | canonical_chunk | ## (3) Tunnel Management Office Operator Tunnel Management Office should be operated and managed by DOR. Since this is t |

#### `tunnel energy cost`

| # | score | chunk_id | document | kind | preview |
|---|---|---|---|---|---|
| 1 | 0.6855 | `DOC000041-R1-C0002` | DOC000041 | recovery_chunk | ## Sayfa 2 Newfoundland Fixed Link Pre-feasibility StudyPage 2 of 2 Highway Tunnel Estimate of annual operating costs D. |
| 2 | 0.6530 | `DOC000016-C0006` | DOC000016 | canonical_chunk | ## Appendix A - Tunnel estimate example This example assumes a 7km tunnel is constructed using slurry machines in a rura |
| 3 | 0.6237 | `DOC000041-R1-C0003` | DOC000041 | recovery_chunk | ## Sayfa 3 Newfoundland Fixed Link Pre-feasibility StudyPage 1 of 2 Highway Tunnel Estimate of annual maintenance costs  |
| 4 | 0.6157 | `DOC000012-C0001` | DOC000012 | canonical_chunk | **COSTS OF CONSTRUCTION, OPERATION, UPGRADING - FINANCIAL ASPECTS** - [**1. Foreword**](https://tunnelsmanual.piarc.org/ |
| 5 | 0.6156 | `DOC000041-R1-C0001` | DOC000041 | recovery_chunk | # Estimate of annual operating costs Highway Tunnel ## Sayfa 1 Newfoundland Fixed Link Pre-feasibility StudyPage 1 of 2  |

#### `annual operating costs`

| # | score | chunk_id | document | kind | preview |
|---|---|---|---|---|---|
| 1 | 0.6249 | `DOC000019-C0005` | DOC000019 | canonical_chunk | ## 2.2 Estimating Operational and Regular Maintenance Costs - 2.2.1 Those requirements and tasks on road infrastructure  |
| 2 | 0.6218 | `DOC000041-R1-C0001` | DOC000041 | recovery_chunk | # Estimate of annual operating costs Highway Tunnel ## Sayfa 1 Newfoundland Fixed Link Pre-feasibility StudyPage 1 of 2  |
| 3 | 0.6139 | `DOC000041-R1-C0002` | DOC000041 | recovery_chunk | ## Sayfa 2 Newfoundland Fixed Link Pre-feasibility StudyPage 2 of 2 Highway Tunnel Estimate of annual operating costs D. |
| 4 | 0.5955 | `DOC000009-R1-C0002` | DOC000009 | recovery_chunk | ## Assumptions: Facility operates 12 hours/day, 7 days/week 50 percent of this time the facility is fully staffed with t |
| 5 | 0.5847 | `DOC000075-C0121` | DOC000075 | canonical_chunk | / TÜNEL BAKIM, ONARIM, İŞLETME ŞEFLİKLERİ / Tünel Adeti / Tünel Uzunluğu (km) / İdari Personel Giderleri (TL) / Hizmet A |

### Tunnel registry (DOC000051)

#### `Turkish tunnel names`

| # | score | chunk_id | document | kind | preview |
|---|---|---|---|---|---|
| 1 | 0.5469 | `DOC000098-C0007` | DOC000098 | canonical_chunk | / Tünel Adı / Tünel Adı / Yapım Yılı / Yeri / Yeri / Yeri / Amacı / Amacı / Çapı (m) / / Uzunluk (m) / / /-------------- |
| 2 | 0.5454 | `DOC000307-C0003` | DOC000307 | canonical_chunk | ## ANCIENT TUNNELLING Underground structures have been served for a variety of purposes. One of the oldest underwater tu |
| 3 | 0.5443 | `DOC000176-C0041` | DOC000176 | canonical_chunk | ## CORPORATE MEMBERS OF TURKISH TUNNELLING SOCIETY <!-- image --> <!-- image --> <!-- image --> <!-- image --> <!-- imag |
| 4 | 0.5442 | `DOC000175-C0037` | DOC000175 | canonical_chunk | ## CORPORATE MEMBERS OF TURKISH TUNNELLING SOCIETY <!-- image --> <!-- image --> <!-- image --> <!-- image --> <!-- imag |
| 5 | 0.5412 | `DOC000197-C0031` | DOC000197 | canonical_chunk | / 1. / A Kedi, Turkey / 47. / Geofrost, Norway (Norveç) / 91. / Pena İç ve Dış Ticaret, Turkey / /---------/------------ |

#### `Türkiye tünel haritası`

| # | score | chunk_id | document | kind | preview |
|---|---|---|---|---|---|
| 1 | 0.6581 | `DOC000167-C0010` | DOC000167 | canonical_chunk | Türkiye'deki Karayolu Tünellerinde Trafik Güvenliği |
| 2 | 0.6360 | `DOC000051-R1-C0001` | DOC000051 | recovery_chunk | # Tünel Haritası 2024_KGMWEB ## Sayfa 1 !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( !( |
| 3 | 0.6285 | `DOC000049-C0149` | DOC000049 | canonical_chunk | ## 2015 YILINDA TAMAMLANMASI PLANLANAN TÜNELLER / SIRA NO / BÖLGE NO / TÜNELİN ADI / YOLUN ADI / K.K.NO / TÜP ADEDİ / UZ |
| 4 | 0.6239 | `DOC000049-C0010` | DOC000049 | canonical_chunk | ## 2000-3000 METRE ARASI UZUNLUKTAKİ TÜNELLER / SIRA NO / BÖLGE NO / TÜNELİN ADI / YOLUN ADI / K.K.NO / BAŞL. KM. / TÜP  |
| 5 | 0.6220 | `DOC000167-C0004` | DOC000167 | canonical_chunk | ## 4. TÜRKİYE'DE TÜNEL GÜVENLİĞİ Coğrafi yönden dağlık bir arazi yapısına sahip olan Türkiye'de tünel sayısı oldukça faz |

#### `tünel isimleri`

| # | score | chunk_id | document | kind | preview |
|---|---|---|---|---|---|
| 1 | 0.6411 | `DOC000098-C0007` | DOC000098 | canonical_chunk | / Tünel Adı / Tünel Adı / Yapım Yılı / Yeri / Yeri / Yeri / Amacı / Amacı / Çapı (m) / / Uzunluk (m) / / /-------------- |
| 2 | 0.5698 | `DOC000098-C0006` | DOC000098 | canonical_chunk | İnsanlar tarih öncesi dönemlerde barınma ihtiyaçlarını karşılamak üzere mağaraları kullanmışlar ve zamanla barınmak için |
| 3 | 0.5647 | `DOC000071-C0052` | DOC000071 | canonical_chunk | / **Tünel Adı: (efUS** **Kilometre: Ç -+409°°** / **Formasyon:** **TtAtMA F/*).** / **Kaya sınıflaması (CSIR-RMR):** *** |
| 4 | 0.5637 | `DOC000049-C0010` | DOC000049 | canonical_chunk | ## 2000-3000 METRE ARASI UZUNLUKTAKİ TÜNELLER / SIRA NO / BÖLGE NO / TÜNELİN ADI / YOLUN ADI / K.K.NO / BAŞL. KM. / TÜP  |
| 5 | 0.5618 | `DOC000132-C0003` | DOC000132 | canonical_chunk | ## İ LK Su Geçi ş i (Kanal) Tünelleri / TÜNEL / Tarih / uzunluk [m] / Kazı Miktarı [m³] / Açıklama / /------------------ |

- Recovery chunks appearing in the 15 general top-10 lists: **2** of 150 slots — recovered content is reachable without dominating unrelated queries.

## Checkpoint / resume

- Cache: `data/embeddings/cache/` — one `.npy` + `.json` per batch (446 batches).
- Each checkpoint records start_index, end_index, chunk IDs, input hashes, model revision and vector shape.
- Run identity fingerprint: `3c333209c51827f11a7a246bb5f79bf9…` derived from embedder version, model, revision, device, dimension, input-manifest hash and every (chunk_id, text_sha256) pair.
- A checkpoint is reused only if run identity, batch identity, model revision, chunk-id list, vector shape and finiteness all match; otherwise it is discarded and recomputed. Stale checkpoints cannot silently contaminate a run.
- This run: **0** vectors computed, **5992** resumed.

## Reproducibility

- Deterministic stratified re-embed sample: **122** chunks (length-stratified, plus all 12 recovery chunks).
- Max absolute drift: **0.000e+00**
- Mean absolute drift: **0.000e+00**
- Cosine agreement: min **0.99999982**, mean **1.00000000**
- **Full-run byte identity confirmed.** The complete 5992-vector run was executed twice from an empty checkpoint cache and both produced an identical `bge_m3_dense.npy` (`99e3b79033a996ffb08b4b742faf68ec217a5a49d0cfdb05175996d65de1d4d3`). MPS inference is bit-reproducible on this hardware, so determinism rests on measurement rather than on the pinned revision and input mapping alone.
- Independently, a stale-checkpoint drill (tampering one batch's recorded model revision) forced recomputation of exactly that 16-chunk batch and still reproduced the same output hash.

## Frozen integrity

- Frozen inputs changed: **0**
- `data/chunks/chunks.jsonl`, `data/chunks_pilot/chunks.jsonl`, `data/chunks_recovery/chunks.jsonl`: **unchanged**
- `data/metadata/full_embedding_input_manifest.csv`, `embedding_eligibility.csv`, BGE preflight artefacts: **unchanged**
- `data/corpus_final/`, `data/corpus_normalized/`, `data/corpus_recovery/`: **unchanged**

## Tests

- Main tests (`tests/`): **311/311 PASS** (270 previous + 41 new full-embedding tests; 3 model-inference tests opt-in via `TUNNELBOOK_BGE_LIVE=1`, verified passing separately)
- Report/Colab tests (`rapor/tests/`): **16/16 PASS**
- Project-wide total: **327/327 PASS**
- New tests cover: authoritative manifest loading, 5992 unique contiguous vector indices, canonical/recovery text resolver with SHA verification, recovery token-limit safety, no silent truncation, checkpoint creation and coverage, checkpoint resume, stale-checkpoint rejection (revision / run identity / changed text / wrong shape), vector order restored after token bucketing, embedding shape, 1024 dimension, finite vectors, unit norms, exact chunk/vector mapping, explicit recovery mapping, superseded chunks absent, deterministic sample re-embed, output manifest integrity, frozen artefacts unchanged.

## Warnings

- `DOC000009-R1-C0003` carries no real words: it is an empty table skeleton of symbol placeholders from a graphics-only source page. It is not corruption (no glyph or control residue) and is embedded as `eligible_low_content` under the keep+flag policy.
- `DOC000051-R1-C0001` is dominated by repeated `!(` map-marker symbols. The chunk is genuine map content, but its vector carries little semantic signal; expect it to behave as noise in retrieval.
- DOC000051 chunks expand strongly under SentencePiece (about 2.3x lexical) because Turkish proper nouns subword-split heavily. Still far below the 8192 limit.
- Recovered registry content surfaced in **1** of 15 top-5 slots for the registry-targeted queries, and stayed out of unrelated topical queries.
- Vectors are stored as float32 in `vector_index` order. Any consumer must key on that order or on `bge_m3_chunk_ids.json`; the array carries no identifiers of its own.

## Blockers

- Yok.

## Output hashes

- `bge_m3_chunk_ids.json`: `7497af0d7d7032eb4c2400f74f6f1f694ab80ce3a594be416bd66bd808cf86bd`
- `bge_m3_dense.npy`: `99e3b79033a996ffb08b4b742faf68ec217a5a49d0cfdb05175996d65de1d4d3`
- `full_embedding_input_manifest.csv`: `4af9d60a8cbfbb712c27c8129a622b6118166954c732947e015876e25fd99654`
- `full_embedding_manifest.csv`: `68be1f5fa0b7b6078cd9f492a8732aa796b2ab6536c4b76454e5a37bd41bc32a`
- Model revision: `5617a9f61b028005a4858fdac845db406aefb181`
- Embedding script version: `bge-m3-dense-v1.0`

## Final Decision

**FULL BGE-M3 EMBEDDINGS — GO**

Next stage (not started): Qdrant indexing, retrieval benchmarking, reranking, RAG.
