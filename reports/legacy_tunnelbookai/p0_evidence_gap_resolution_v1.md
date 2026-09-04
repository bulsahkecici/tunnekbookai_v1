# P0 Evidence Gap Resolution v1

## Executive Decision

**P0 EVIDENCE GAP RESOLUTION V1 - CLOSED / GO**

All six P0 gaps were processed under the existing-evidence-first protocol: 2 resolved, 4 partially resolved, 0 unresolved. 43 P0 claims were decided, of which 25 are citation-ready, from 43 manual span mappings and 21 cross-lingual mappings over 64 verified source spans. Generation calls: 0. Retrieval calls: 0. Every resolution came out of evidence that was already inside the frozen packets.

- **SEC-02-1**: NOT_READY
- **SEC-02-2**: READY_WITH_LIMITATIONS
- **SEC-02-3**: NOT_READY

## Why Drafting Is Still Blocked

Drafting is not enabled by this phase under any outcome; that decision belongs to the Section Drafting Contract. What changed is that SEC-02-2 now passes the readiness contract, so a drafting phase has something to be run against.

**SEC-02-1** (NOT_READY):
  - unsupported clauses under P0 objectives: 1
  - cross-lingual clauses under P0 objectives without a faithful mapping: 1

**SEC-02-2** (READY_WITH_LIMITATIONS):
  - P1/P2 questions without a citation-ready claim: ['Q-02-2-03', 'Q-02-2-04', 'Q-02-2-06']
  - numeric clauses unresolved outside P0: 1
  - context difference retained and surfaced: CF-P0-001
  - generator synthesis dropped and recorded: SYN-001

**SEC-02-3** (NOT_READY):
  - unsupported clauses under P0 objectives: 3
  - cross-lingual clauses under P0 objectives without a faithful mapping: 13

`drafting_enabled` remains `false` in both the manifest and the descriptor.

## Frozen Inputs

| Input | State |
|---|---|
| Remediation v1 manifest | `01ce81c8f7e9684b` |
| Frozen integrity checks | 46, all unchanged |
| Source registry v1 | untouched |
| Qdrant | 5992 before / 5992 after / 0 writes |

New source keys needed by this phase are derived with Book Pipeline v1's own key function and written to `data/book/p0_resolution/evidence/p0_source_registry_v1.jsonl`, leaving the frozen registry byte-identical.

## Resolution Strategy

Order was fixed in advance and is the same for every gap: reconstruct what extraction dropped (A), then search the whole frozen packet rather than the cited handles (B), then map Turkish claims onto exact English spans (C), then - and only if the packet is exhausted - consider controlled regeneration (D), retrieval gap (E) and corpus gap (F).

Two rules did most of the work. First, the unit of inspection is the **packet**, not the citation: a generator that cited E001 next to a sentence whose support sits in E006 produced an unsupported note in v1 and a supported claim here, with no new evidence entering the system. Second, a claim may be **narrowed** to what a source says but never widened - which is why the classification claim lost its unsourced basis clause and the TBM threshold stayed broken.

## P0 Gap Inventory

| Gap | Question | Section | Entering classes | Status |
|---|---|---|---|---|
| GAP-P0-01 | Q-02-1-01 | SEC-02-1 | EXTRACTION_FAILURE, SPAN_MAPPING_FAILURE | **PARTIALLY_RESOLVED** |
| GAP-P0-02 | Q-02-1-02 | SEC-02-1 | EXTRACTION_FAILURE | **PARTIALLY_RESOLVED** |
| GAP-P0-03 | Q-02-2-01 | SEC-02-2 | GENERATOR_SYNTHESIS_DEFECT, SPAN_MAPPING_FAILURE | **RESOLVED** |
| GAP-P0-04 | Q-02-2-02 | SEC-02-2 | SPAN_MAPPING_FAILURE | **RESOLVED** |
| GAP-P0-05 | Q-02-3-01 | SEC-02-3 | CROSS_LINGUAL_MAPPING_FAILURE, SPAN_MAPPING_FAILURE | **PARTIALLY_RESOLVED** |
| GAP-P0-06 | Q-02-3-02 | SEC-02-3 | CROSS_LINGUAL_MAPPING_FAILURE, EXTRACTION_FAILURE, SPAN_MAPPING_FAILURE | **PARTIALLY_RESOLVED** |

## Existing Evidence First

Every gap's full packet was inspected before any other step: 120 evidence items across six packets. 64 authored spans were re-verified verbatim against frozen chunk text; 0 failed. A failed span aborts the phase, so no mapping in the artifacts rests on text that is not in the corpus.

## Extraction Failures

Q-02-1-01 and Q-02-1-02 had lost their answers entirely. Both were answered as a lead-in sentence followed by a list, and v1.1 is right to refuse to make a note out of a bare label - but the lead-in went with them, because it ends in a colon and carries no citation handle. So the classification proposition Q-02-1-01 asks for was never extracted, and Q-02-1-02 ended with zero notes while its packet held the enumeration verbatim. That is an extraction defect, not an evidence gap, and it is why this phase starts at A rather than at retrieval.

| Reconstruction | Proposition | Narrowing | Status |
|---|---|---|---|
| `R-Q-02-1-01-01` | Tünel destekleme sistemi, birincil destekleme sistemi ve ikincil destekleme sistemi olmak … | The unit's basis 'kullanılan malzeme ve uygulama zamanına göre' is dropped: no p… | SUPPORTED |
| `R-Q-02-1-01-02` | Birincil destekleme sistemi elemanları, karşılaşılan kaya sınıfı ve jeolojik koşullara gör… | 'tünelin açılma sürecinde stabiliteyi sağlayan sistemdir' is dropped: E007 state… | SUPPORTED |
| `R-Q-02-1-01-03` | Tünellerde kullanılan birincil destekleme elemanları süren, püskürtme beton, hasır çelik, … | None. The eight labels are restated as the single enumeration their parent lead-… | SUPPORTED |
| `R-Q-02-1-01-04` | Tünellerde kullanılan ikincil destekleme elemanları invert betonu, temel kiriş betonu, su … | 'Taban Kemeri' is dropped as an unsourced gloss on 'İnvert Betonu'.… | SUPPORTED |
| `R-Q-02-1-02-01` | Tünellerde kullanılan birincil destekleme elemanları süren, püskürtme beton, hasır çelik, … | None for these eight. The ninth answer item, 'İç hasır çelik tabakası (bazı duru… | SUPPORTED |
| `R-Q-02-1-02-02` | Püskürtme beton kaplamada, beton tabakaları arasına bir çelik hasır tabakası uygulanır.… | 'bazı durumlarda' is dropped and the claim is restated as what E001 describes: m… | PARTIALLY_SUPPORTED |
| `R-Q-02-3-01-01` | TBM rekabet formülünün sonucu 1'in altında olduğunda genellikle geleneksel yöntem tercih e… | The source threshold is restored: 1, not 1,5. The generator's 1,5 lower bound an… | SUPPORTED |
| `R-Q-02-3-01-02` | 1,5 değeri, geleneksel yöntem ile TBM yöntemi arasındaki denge sınırını temsil eder ve yal… | 1,5 is a single trade-off value in the source, not the lower edge of a band.… | SUPPORTED |

## Manual Span Mapping

28 same-language mappings were authored over 43 spans. Relations used: literal_direct, manual_paraphrase_mapping, multi_span_composition, numeric_direct, qualified_support.

| Mapping | Target | Relation | Verdict |
|---|---|---|---|
| MS-001 | `R-Q-02-1-01-01` | literal_direct | FULL |
| MS-002 | `R-Q-02-1-01-01` | manual_paraphrase_mapping | FULL |
| MS-003 | `R-Q-02-1-01-02` | literal_direct | FULL |
| MS-004 | `R-Q-02-1-01-03` | multi_span_composition | FULL |
| MS-005 | `R-Q-02-1-01-04` | multi_span_composition | FULL |
| MS-006 | `Q-02-1-01-N16-E` | qualified_support | PARTIAL |
| MS-007 | `R-Q-02-1-02-01` | multi_span_composition | FULL |
| MS-008 | `R-Q-02-1-02-02` | qualified_support | PARTIAL |
| MS-009 | `Q-02-2-01-N03-C01` | numeric_direct | FULL |
| MS-010 | `Q-02-2-01-N04-C01` | qualified_support | FULL |
| MS-011 | `Q-02-2-01-N04-C02` | numeric_direct | FULL |
| MS-012 | `Q-02-2-01-N05-C01` | literal_direct | FULL |
| MS-013 | `Q-02-2-01-N06-C01` | multi_span_composition | FULL |
| MS-014 | `Q-02-2-01-N07-C01` | numeric_direct | FULL |
| MS-015 | `Q-02-2-02-N01-C01` | numeric_direct | FULL |
| MS-016 | `Q-02-2-02-N02-C01` | multi_span_composition | FULL |
| MS-017 | `Q-02-3-01-N06-C01` | multi_span_composition | PARTIAL |
| MS-018 | `Q-02-3-01-N07-C01` | multi_span_composition | PARTIAL |
| MS-019 | `Q-02-3-01-N07-C02` | manual_paraphrase_mapping | FULL |
| MS-020 | `Q-02-3-01-N07-C03` | literal_direct | FULL |
| MS-021 | `Q-02-3-01-N07-C04` | multi_span_composition | FULL |
| MS-022 | `Q-02-3-01-N07-C05` | literal_direct | FULL |
| MS-023 | `Q-02-3-02-N08-C01` | literal_direct | FULL |
| MS-024 | `Q-02-3-02-N06-C01` | multi_span_composition | PARTIAL |
| MS-025 | `Q-02-3-02-N09-C01` | qualified_support | PARTIAL |
| MS-026 | `Q-02-3-02-N15-C01` | qualified_support | PARTIAL |
| MS-027 | `Q-02-3-02-N18-C01` | qualified_support | PARTIAL |
| MS-028 | `Q-02-3-02-N10-C01` | multi_span_composition | PARTIAL |

## Same-Language Paraphrase Mapping

2 claims are carried by a Turkish source that says the same thing in different words. Remediation v1 had no way to represent this, which is why they sat unsupported beside evidence that supported them.
- `R-Q-02-1-01-01` ← E014: "destekleme elemanlarını birincil destekleme elemanları ve ikincil destekleme elemanları olarak ayırabiliriz…" (FULL)
- `Q-02-3-01-N07-C02` ← E004: "yerleşim yeri ve/veya sanayi alanları yakınlarında tahribata sebep olunabileceğinden…" (FULL)

## Cross-Lingual Mapping

| Mapping | Target | Status | Numeric | Modality | Condition | Scope |
|---|---|---|---|---|---|---|
| XL-P0-001 | `Q-02-1-01-N16-A` | **FAITHFUL** | ✓ | ✓ | ✓ | ✓ |
| XL-P0-002 | `Q-02-1-01-N16-B` | **FAITHFUL** | ✓ | ✓ | ✓ | ✓ |
| XL-P0-003 | `Q-02-1-01-N16-C` | **FAITHFUL** | ✓ | ✓ | ✓ | ✓ |
| XL-P0-004 | `Q-02-1-01-N16-D` | **NOT_SUPPORTED** | ✓ | ✗ | ✗ | ✗ |
| XL-P0-005 | `R-Q-02-3-01-01` | **FAITHFUL** | ✓ | ✓ | ✓ | ✓ |
| XL-P0-006 | `R-Q-02-3-01-02` | **FAITHFUL** | ✓ | ✓ | ✓ | ✓ |
| XL-P0-007 | `Q-02-3-01-N03-C02` | **NOT_SUPPORTED** | ✗ | ✓ | ✓ | ✓ |
| XL-P0-008 | `Q-02-3-01-N03-C04` | **NOT_SUPPORTED** | ✗ | ✓ | ✗ | ✗ |
| XL-P0-009 | `Q-02-3-01-N04-C04` | **FAITHFUL** | ✓ | ✓ | ✓ | ✓ |
| XL-P0-010 | `Q-02-3-02-N05-C02` | **PARTIAL** | ✓ | ✗ | ✗ | ✓ |
| XL-P0-011 | `Q-02-3-02-N04-C02` | **PARTIAL** | ✓ | ✗ | ✓ | ✓ |
| XL-P0-012 | `Q-02-3-02-N11-C01` | **PARTIAL** | ✓ | ✓ | ✓ | ✗ |
| XL-P0-013 | `Q-02-3-02-N16-C01` | **PARTIAL** | ✓ | ✓ | ✓ | ✗ |
| XL-P0-014 | `Q-02-3-02-N14-C02` | **FAITHFUL** | ✓ | ✓ | ✓ | ✓ |
| XL-P0-015 | `Q-02-3-02-N14-C03` | **PARTIAL** | ✓ | ✓ | ✓ | ✗ |
| XL-P0-016 | `Q-02-3-02-N19-C01` | **PARTIAL** | ✓ | ✓ | ✓ | ✗ |

English source spans are stored verbatim and are never rendered into quotable Turkish.

## Generator Synthesis Defects

**SYN-001** (Q-02-2-01, from `Q-02-2-01-N04`)

- Dropped: Yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m³ olarak belirtilse de, püskürtme beton spesifikasyonlarında minimum 350/400 kg/m³ öngörülmüştür (karşıtlık ilişkisi).
- Reason: The concessive relation between the two figures is asserted by no source. The 360 kg/m³ maximum belongs to Tablo-308-23-b, which governs general concrete by exposure class; the 350/400 kg/m³ minimums belong to the shotcrete specification. They are different scopes, not a stated exception to one another.
- Components retained as separate claims: `Q-02-2-01-N04-C01`, `Q-02-2-01-N04-C02`
- Citable as a compound: False

## Controlled Revised Queries

1 revised query was authored and 0 were executed.

- **GAP-P0-03** → `SKIPPED_EXISTING_EVIDENCE_SUFFICIENT`. Rule 25/26: regeneration is unlocked only after existing packet evidence is exhausted. It is not. All three propositions the revised query would target are stated verbatim inside this question's own frozen packet (350 and 400 kg/m3 in E005/E009, the 360 kg/m3 table limit in E004/E006), and are resolved here by manual span mapping. Generating would add an answer, not evidence.

The revision is recorded even though it was not run, because the decision not to generate is the substantive one: rule 26 makes existing evidence the default and regeneration the exception, and this gap's three target propositions were all already in its own packet.

## Retrieval Gap Assessment

| Clause | Missing proposition | Packet searched | Verdict |
|---|---|---|---|
| `Q-02-3-01-N05-C03` | Delme-patlatma kısa mesafeli veya sık değişen jeolojide TBM'den daha h… | 20 items | present_but_insufficient |
| `Q-02-3-02-N18-C01` | Kısa mesafeli kazılarda TBM ekonomik olmayabilir.… | 20 items | present_but_insufficient |
| `Q-02-1-01-N16-D` | İkincil destek, ek yükleri taşımak amacıyla inşa edilir.… | 20 items | present_but_insufficient |
| `Q-02-3-01-N07-C01` | Patlatma kaynaklı titreşimler kaçınılmazdır.… | 20 items | present_but_insufficient |
| `Q-02-3-02-N15-C01` | Titreşim ve gürültü kısıtlaması olan durumlarda TBM tercih edilir.… | 20 items | candidate_retrieval_gap |

A missing proposition is only a retrieval-gap candidate once the whole packet has been searched for it and come back empty. Where related passages exist but do not carry the proposition, the verdict is `present_but_insufficient`, not a retrieval gap.

## Retrieval Expansion

Attempts performed: **0**. Production default top_k=20 is unchanged; Qdrant writes: 0.

Expansion was declined for every candidate. Two reasons, both recorded per row: the sections concerned are already NOT_READY on requirements expansion cannot touch, and evidence retrieved outside a frozen ContextPacket has no packet sha, so it could not produce a citation-ready claim in this phase even if it were found.

## Corpus Gap Assessment

Confirmed corpus gaps: **0**. No corpus gap is claimed, and none can be: rule 84 requires expanded retrieval to be exhausted first, and no expansion was run. Retrieval-gap candidates are handed forward as candidates.

## Question Design Defects

None. All six questions are single-obligation and answerable in principle; the failures were in extraction, span mapping and synthesis, not in question design. No question was decomposed and no technical objective was removed.

## Numeric Safety

| Value | Context | Source-stated | Derived | Note |
|---|---|---|---|---|
| 350 kg/m³ | kuru sistem püskürtme beton minimum çimento | yes | no | Already source-stated in v1; unchanged.… |
| 400 kg/m³ | yaş sistem püskürtme beton minimum çimento | yes | no | Flagged in v1 because the citing note pointed at E001/E003. E005 and E009 - one of them au… |
| 360 kg/m³ | Tablo-308-23-b genel beton maksimum çimento | yes | no | Same pattern as 400. Promoted only with the mandatory scope qualifier: this is the general… |
| 150 mm | 15 cm -> 150 mm dönüşümü (Q-02-2-04) | **no** | yes | Unchanged from v1: a conversion the generator performed, not a value any source states. St… |
| 20 bar | Delaware Su Kemeri su basıncı iddiası | **no** | no | NEW defect found in this phase. The figure exists in the packet but denotes the drilling p… |

360 and 400 kg/m³ were promoted, but on source spans, not on the generator's word: both occur verbatim in the question's own packet, in items the citing note did not point at. 150 mm stays derived and non-citable. One new numeric defect was found here: the 20 bar in the Delaware claim denotes a drill's pressure capability in the source, not the groundwater pressure, so the clause carrying it stays partial.

## Conflict Review

| Review | Section | Result | Decision |
|---|---|---|---|
| CF-P0-001 | SEC-02-2 | **CONTEXT_DIFFERENCE** | Not a true conflict: the two figures govern different materials and different design routes. Both are retained… |
| CF-P0-002 | SEC-02-1 | **NO_CONFLICT_FOUND** | Identical enumeration from the same source chunk reached through two packets; recorded as a duplicate-claim ca… |
| CF-P0-003 | SEC-02-3 | **INSUFFICIENT_TO_DECIDE** | The packet states the first and is silent on the second, so no comparison can be adjudicated. The second stays… |

## Resolved Claims

43 claims were produced, 25 of them citation-ready.

| Claim | Question | Status | Citation-ready | Resolution source |
|---|---|---|---|---|
| SEC-02-1-P0-001 | Q-02-1-01 | SUPPORTED | yes | cross_lingual_mapping |
| SEC-02-1-P0-002 | Q-02-1-01 | SUPPORTED | yes | cross_lingual_mapping |
| SEC-02-1-P0-003 | Q-02-1-01 | SUPPORTED | yes | cross_lingual_mapping |
| SEC-02-1-P0-004 | Q-02-1-01 | UNSUPPORTED | no | cross_lingual_mapping |
| SEC-02-1-P0-005 | Q-02-1-01 | PARTIALLY_SUPPORTED | no | manual_span_mapping |
| SEC-02-2-P0-001 | Q-02-2-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-2-P0-002 | Q-02-2-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-2-P0-003 | Q-02-2-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-2-P0-004 | Q-02-2-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-2-P0-005 | Q-02-2-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-2-P0-006 | Q-02-2-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-2-P0-007 | Q-02-2-02 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-2-P0-008 | Q-02-2-02 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-3-P0-001 | Q-02-3-01 | UNSUPPORTED | no | cross_lingual_mapping |
| SEC-02-3-P0-002 | Q-02-3-01 | UNSUPPORTED | no | cross_lingual_mapping |
| SEC-02-3-P0-003 | Q-02-3-01 | SUPPORTED | yes | cross_lingual_mapping |
| SEC-02-3-P0-004 | Q-02-3-01 | PARTIALLY_SUPPORTED | no | manual_span_mapping |
| SEC-02-3-P0-005 | Q-02-3-01 | PARTIALLY_SUPPORTED | no | manual_span_mapping |
| SEC-02-3-P0-006 | Q-02-3-01 | SUPPORTED | yes | manual_paraphrase_mapping |
| SEC-02-3-P0-007 | Q-02-3-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-3-P0-008 | Q-02-3-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-3-P0-009 | Q-02-3-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-3-P0-010 | Q-02-3-02 | PARTIALLY_SUPPORTED | no | cross_lingual_mapping |
| SEC-02-3-P0-011 | Q-02-3-02 | PARTIALLY_SUPPORTED | no | cross_lingual_mapping |
| SEC-02-3-P0-012 | Q-02-3-02 | PARTIALLY_SUPPORTED | no | manual_span_mapping |
| SEC-02-3-P0-013 | Q-02-3-02 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-3-P0-014 | Q-02-3-02 | PARTIALLY_SUPPORTED | no | manual_span_mapping |
| SEC-02-3-P0-015 | Q-02-3-02 | PARTIALLY_SUPPORTED | no | manual_span_mapping |
| SEC-02-3-P0-016 | Q-02-3-02 | PARTIALLY_SUPPORTED | no | cross_lingual_mapping |
| SEC-02-3-P0-017 | Q-02-3-02 | SUPPORTED | yes | cross_lingual_mapping |
| SEC-02-3-P0-018 | Q-02-3-02 | PARTIALLY_SUPPORTED | no | cross_lingual_mapping |
| SEC-02-3-P0-019 | Q-02-3-02 | PARTIALLY_SUPPORTED | no | manual_span_mapping |
| SEC-02-3-P0-020 | Q-02-3-02 | PARTIALLY_SUPPORTED | no | cross_lingual_mapping |
| SEC-02-3-P0-021 | Q-02-3-02 | PARTIALLY_SUPPORTED | no | manual_span_mapping |
| SEC-02-3-P0-022 | Q-02-3-02 | PARTIALLY_SUPPORTED | no | cross_lingual_mapping |
| SEC-02-1-P0-006 | Q-02-1-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-1-P0-007 | Q-02-1-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-1-P0-008 | Q-02-1-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-1-P0-009 | Q-02-1-01 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-1-P0-010 | Q-02-1-02 | SUPPORTED | yes | manual_span_mapping |
| SEC-02-1-P0-011 | Q-02-1-02 | PARTIALLY_SUPPORTED | no | manual_span_mapping |
| SEC-02-3-P0-023 | Q-02-3-01 | SUPPORTED | yes | cross_lingual_mapping |
| SEC-02-3-P0-024 | Q-02-3-01 | SUPPORTED | yes | cross_lingual_mapping |

## SEC-02-1

**Tünel Destekleme Sistemleri: Kavramlar ve Elemanlar** — NOT_READY

- P0 questions with a citation-ready claim: 3/3
- Citation-ready claims in the rebuilt ledger: 18
- New P0 claims: 11 (8 citation-ready)
- Unsupported clauses under P0 objectives: 1

#### GAP-P0-01 - Q-02-1-01 (PARTIALLY_RESOLVED)

*Tünel destekleme sistemleri hangi ana gruplara ayrılır?*

- Entering gap classes: EXTRACTION_FAILURE, SPAN_MAPPING_FAILURE
- Packet inspected: 20 evidence items (packet sha `213c02793ef07ef8`)
- Manual span mappings: 6  |  cross-lingual mappings: 6
- Resolved claims: 9 (7 citation-ready)
- Controlled regenerations: 0  |  retrieval expansions: 0
- Remaining unsupported propositions: `Q-02-1-01-N16-D`, `Q-02-1-01-N16-E`

#### GAP-P0-02 - Q-02-1-02 (PARTIALLY_RESOLVED)

*Tünellerde birincil destekleme elemanları nelerdir?*

- Entering gap classes: EXTRACTION_FAILURE
- Packet inspected: 20 evidence items (packet sha `94224ddfaa8ca1d7`)
- Manual span mappings: 2  |  cross-lingual mappings: 0
- Resolved claims: 2 (1 citation-ready)
- Controlled regenerations: 0  |  retrieval expansions: 0
- Remaining unsupported propositions: `R-Q-02-1-02-02`

## SEC-02-2

**Püskürtme Beton: Malzeme ve Uygulama Gereklilikleri** — READY_WITH_LIMITATIONS

- P0 questions with a citation-ready claim: 2/2
- Citation-ready claims in the rebuilt ledger: 10
- New P0 claims: 8 (8 citation-ready)
- Unsupported clauses under P0 objectives: 0

#### GAP-P0-03 - Q-02-2-01 (RESOLVED)

*Püskürtme beton için minimum çimento dozajı ne kadardır?*

- Entering gap classes: GENERATOR_SYNTHESIS_DEFECT, SPAN_MAPPING_FAILURE
- Packet inspected: 20 evidence items (packet sha `41eff42098b8f210`)
- Manual span mappings: 12  |  cross-lingual mappings: 0
- Resolved claims: 6 (6 citation-ready)
- Controlled regenerations: 0  |  retrieval expansions: 0
- Remaining unsupported propositions: none

#### GAP-P0-04 - Q-02-2-02 (RESOLVED)

*What is the typical thickness of an initial shotcrete lining?*

- Entering gap classes: SPAN_MAPPING_FAILURE
- Packet inspected: 20 evidence items (packet sha `48c20da05672e706`)
- Manual span mappings: 5  |  cross-lingual mappings: 0
- Resolved claims: 2 (2 citation-ready)
- Controlled regenerations: 0  |  retrieval expansions: 0
- Remaining unsupported propositions: none

## SEC-02-3

**Kazı Yöntemi Seçimi: TBM ve Delme-Patlatma** — NOT_READY

- P0 questions with a citation-ready claim: 2/2
- Citation-ready claims in the rebuilt ledger: 15
- New P0 claims: 24 (9 citation-ready)
- Unsupported clauses under P0 objectives: 3

#### GAP-P0-05 - Q-02-3-01 (PARTIALLY_RESOLVED)

*TBM ile delme-patlatma yöntemi hangi kriterlere göre karşılaştırılır?*

- Entering gap classes: CROSS_LINGUAL_MAPPING_FAILURE, SPAN_MAPPING_FAILURE
- Packet inspected: 20 evidence items (packet sha `146500b498d97a39`)
- Manual span mappings: 9  |  cross-lingual mappings: 6
- Resolved claims: 11 (7 citation-ready)
- Controlled regenerations: 0  |  retrieval expansions: 0
- Remaining unsupported propositions: `Q-02-3-01-N02-C01`, `Q-02-3-01-N03-C02`, `Q-02-3-01-N03-C04`, `Q-02-3-01-N04-C01`, `Q-02-3-01-N05-C03`, `Q-02-3-01-N06-C01`, `Q-02-3-01-N07-C01`

#### GAP-P0-06 - Q-02-3-02 (PARTIALLY_RESOLVED)

*Hangi koşullarda TBM kullanımı uygun görülmektedir?*

- Entering gap classes: CROSS_LINGUAL_MAPPING_FAILURE, EXTRACTION_FAILURE, SPAN_MAPPING_FAILURE
- Packet inspected: 20 evidence items (packet sha `5238b710c5dc2c45`)
- Manual span mappings: 9  |  cross-lingual mappings: 9
- Resolved claims: 13 (2 citation-ready)
- Controlled regenerations: 0  |  retrieval expansions: 0
- Remaining unsupported propositions: `Q-02-3-02-N04-C01`, `Q-02-3-02-N04-C02`, `Q-02-3-02-N04-C03`, `Q-02-3-02-N05-C02`, `Q-02-3-02-N06-C01`, `Q-02-3-02-N09-C01`, `Q-02-3-02-N10-C01`, `Q-02-3-02-N11-C01`, `Q-02-3-02-N13-C02`, `Q-02-3-02-N14-C03`, `Q-02-3-02-N15-C01`, `Q-02-3-02-N16-C01`, `Q-02-3-02-N18-C01`, `Q-02-3-02-N18-C02`, `Q-02-3-02-N19-C01`

## Recomputed Readiness

| Section | Remediation v1 | P0 Resolution v1 | Blocking |
|---|---|---|---|
| SEC-02-1 | NOT_READY | **NOT_READY** | unsupported clauses under P0 objectives: 1; cross-lingual clauses under P0 objectives without a faithful mapping: 1 |
| SEC-02-2 | NOT_READY | **READY_WITH_LIMITATIONS** | P1/P2 questions without a citation-ready claim: ['Q-02-2-03', 'Q-02-2-04', 'Q-02-2-06']; numeric clauses unresolved outs |
| SEC-02-3 | NOT_READY | **NOT_READY** | unsupported clauses under P0 objectives: 3; cross-lingual clauses under P0 objectives without a faithful mapping: 13 |

Readiness was recomputed from scratch on the same contract v1.1 used - no threshold was loosened, and nothing was inherited from the earlier bundles.

## Remaining P0 Gaps

- **GAP-P0-01 / Q-02-1-01** (PARTIALLY_RESOLVED): `Q-02-1-01-N16-D`, `Q-02-1-01-N16-E`
- **GAP-P0-02 / Q-02-1-02** (PARTIALLY_RESOLVED): `R-Q-02-1-02-02`
- **GAP-P0-05 / Q-02-3-01** (PARTIALLY_RESOLVED): `Q-02-3-01-N02-C01`, `Q-02-3-01-N03-C02`, `Q-02-3-01-N03-C04`, `Q-02-3-01-N04-C01`, `Q-02-3-01-N05-C03`, `Q-02-3-01-N06-C01`, `Q-02-3-01-N07-C01`
- **GAP-P0-06 / Q-02-3-02** (PARTIALLY_RESOLVED): `Q-02-3-02-N04-C01`, `Q-02-3-02-N04-C02`, `Q-02-3-02-N04-C03`, `Q-02-3-02-N05-C02`, `Q-02-3-02-N06-C01`, `Q-02-3-02-N09-C01`, `Q-02-3-02-N10-C01`, `Q-02-3-02-N11-C01`, `Q-02-3-02-N13-C02`, `Q-02-3-02-N14-C03`, `Q-02-3-02-N15-C01`, `Q-02-3-02-N16-C01`, `Q-02-3-02-N18-C01`, `Q-02-3-02-N18-C02`, `Q-02-3-02-N19-C01`

## Frozen Integrity

46 checks, all unchanged.

Retriever v1, Context v1, Prompt v5, Output Contract v1.1, Production Grounded Generator v1, Evidence Note Contract v1, Book Pipeline v1, Extractor v1.1, the manual audit, every remediation v1 artifact, the corpus chunks and the production audit log are byte-identical. So is the source registry.

## Tests

`tests/test_p0_evidence_gap_resolution_v1.py` asserts the protocol rather than the results: existing-evidence-first ordering, the generation bound, no same-question retry, the pinned threshold, the pinned numeric defects, that a partially resolved gap cannot be marked RESOLVED, that a section cannot be READY with an open P0 gap, retrieval expansion justification and ceiling, corpus-gap preconditions, provenance resolution, and frozen integrity.

## Final Decision

**CLOSED / GO**

| Gate | Result |
|---|---|
| all claims traceable | PASS |
| all p0 gaps processed | PASS |
| drafting disabled | PASS |
| every mapping span verified | PASS |
| existing packet evidence checked first | PASS |
| frozen integrity holds | PASS |
| generation bounded | PASS |
| moved threshold still unsupported | PASS |
| no unsupported numeric promoted | PASS |
| qdrant unchanged | PASS |
| qdrant writes zero | PASS |
| readiness recomputed | PASS |
| retrieval expansion justified | PASS |
| tests pass | PASS |

The phase's contract is that all six gaps were *processed*, not that all six were *resolved*. Two were: Q-02-2-01 and Q-02-2-02 now carry every proposition their section objective requires, and SEC-02-2 reaches readiness. The other four are honestly short, and the report says of what.

## Next Phase

**SECTION DRAFTING CONTRACT V1 + BOOK CITATION RENDERING CONTRACT V1**

Why: at least one section reached a ready state with every P0 requirement resolved; it is READY_WITH_LIMITATIONS, so the drafting phase must carry those limitations rather than treat the section as unqualified.

Sections in scope: SEC-02-2.

Carried forward:
- P1/P2 questions without a citation-ready claim: ['Q-02-2-03', 'Q-02-2-04', 'Q-02-2-06']
- context difference retained and surfaced: CF-P0-001
- generator synthesis dropped and recorded: SYN-001
- numeric clauses unresolved outside P0: 1

Routing was computed from the recomputed readiness, not decided in advance. Four P0 gaps remain partially resolved and SEC-02-1 and SEC-02-3 stay NOT_READY; they are not part of the next phase's drafting scope and remain open work.

