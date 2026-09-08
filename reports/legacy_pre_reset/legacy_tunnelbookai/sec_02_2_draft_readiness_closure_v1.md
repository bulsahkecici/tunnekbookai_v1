# SEC-02-2 Draft Readiness Closure v1

## Executive Decision

**SEC-02-2 DRAFT READINESS CLOSURE V1 - CLOSED / GO**

**SEC-02-2: READY_WITH_LIMITATIONS**

Required topics covered: **3 / 3**. Candidate claims: 57; allowlisted 27, denylisted 38. Critical limitations: 0. Generation calls: 0. Retrieval calls: 0. Every closure in this phase came out of evidence already inside the frozen ContextPackets.

## Why READY_WITH_LIMITATIONS Was Not Enough

The P0 Evidence Gap Resolution phase reported SEC-02-2 as READY_WITH_LIMITATIONS and routed it to the drafting contract. Both halves of that were wrong, and for the same reason.

The readiness contract that phase applied tested P0 questions only: every P0 question carries a citation-ready claim, no P0 clause is unsupported, numerics are source-stated, cross-lingual mappings are faithful. SEC-02-2 passed all four. What no clause of that contract asked is the question the SectionPlan poses - **are the required topics covered?** SEC-02-2 requires three: `çimento dozajı`, `kaplama kalınlığı`, `dayanım sınıfı`. The third is answered by Q-02-2-03, which is P1. A P1 question is invisible to a P0 contract.

So the entry `P1/P2 questions without a citation-ready claim: ['Q-02-2-03', 'Q-02-2-04', 'Q-02-2-06']` was filed as a limitation when the first element of it meant a **required topic had zero citation-ready claims**. Recomputed under this phase's contract without any closure work, SEC-02-2 would have been NOT_READY, not READY_WITH_LIMITATIONS. Two further points hold independently of that:

- Q-02-2-03 is marked `required: true` in the research questions. Its P1 priority describes retrieval urgency, not whether the section can be written without it.
- READY_WITH_LIMITATIONS is not READY_FOR_DRAFT under any reading, and this phase does not treat the two as interchangeable.

What this phase then found is that none of the three was an evidence gap. The packets carry the propositions; the failures were extraction and span-mapping failures of exactly the kind the P0 phase repaired for P0 questions and never ran for P1/P2 ones.

## Frozen Inputs

| Input | State |
|---|---|
| P0 resolution manifest | `ce8e0a16d07823d1` |
| P0 resolution bundle SEC-02-2 | `ec4d32d5f4238120` |
| Frozen integrity checks | 77, all unchanged |
| Source registry v1 | untouched |
| Qdrant | **not reachable during this run** - count unobserved; 0 writes |
| Generation calls | 0 |
| Retrieval calls | 0 |

Source keys for packet chunks that neither the frozen registry nor the P0 registry had seen are derived with Book Pipeline v1's own key function and written to this phase's own registry file, leaving both upstream registries byte-identical.

**On Qdrant.** Qdrant was not reachable at http://localhost:6333 during this run, so the point count could not be observed and is reported as unknown rather than as the expected 5992. This does not weaken the write claim: the phase performs no retrieval, opens no Qdrant client and holds no write path, and retrieval_calls is 0. The expected count is 5992; it is reported as unknown rather than restated from the previous phase's manifest, because a number nobody measured in this run is not an observation.

## Acceptance Criteria

Written to `data/metadata/sec_02_2_draft_readiness_acceptance_v1.json` (`af97c1937480fc8c`) **before any closure result was computed**, and not touched afterwards. The closure engine refuses to run without it.

READY_FOR_DRAFT requires all of:

- every required topic has at least one SUPPORTED + citation_ready REQUIRED_CORE claim
- every required topic's coverage status is COMPLETE or COMPLETE_WITH_QUALIFIER
- all P0 questions remain RESOLVED and no P0 claim regressed
- no unresolved P1/P2 gap classified CRITICAL
- no unresolved critical numeric clause
- no unresolved contradictory numeric condition
- no context difference classified BLOCKING_CONFLICT or INSUFFICIENT_TO_DECIDE
- no dropped synthesis classified BLOCKING_MISSING_SYNTHESIS
- every allowlisted claim traceable to a verified span in a frozen packet
- provenance complete: every source key on an allowlisted claim resolves
- no allowlisted claim presents a derived conversion as source-stated
- drafting_enabled is false at phase end

## Required Topic Coverage

| Topic | Questions | Required-core claims | Citation-ready | Numeric | Conditions | Status |
|---|---|---|---|---|---|---|
| `çimento dozajı` | Q-02-2-01 | SEC-02-2-P0-001, SEC-02-2-P0-003, SEC-02-2-P0-006, SEC-02-2-R001 | 7 | SOURCE_STATED | QUALIFIED | **COMPLETE_WITH_QUALIFIER** |
| `kaplama kalınlığı` | Q-02-2-02, Q-02-2-04 | SEC-02-2-P0-007, SEC-02-2-P0-008 | 12 | SOURCE_STATED | QUALIFIED | **COMPLETE_WITH_QUALIFIER** |
| `dayanım sınıfı` | Q-02-2-03 | SEC-02-2-C-001 | 2 | SOURCE_STATED | QUALIFIED | **COMPLETE_WITH_QUALIFIER** |

`dayanım sınıfı` had no citation-ready claim at all when this phase began. It is the single reason the section could not have gone to drafting on the previous phase's word.

## Q-02-2-03

**Püskürtme beton için hangi dayanım sınıfı öngörülmektedir?**

| Field | Value |
|---|---|
| Priority | P1 |
| SectionPlan `required` | True |
| Packet items read | 20 |
| Citation-ready claims before | 0 |
| Citation-ready claims after | 2 (SEC-02-2-C-001, SEC-02-2-C-002) |
| Affects required-topic coverage | True |
| Affects numeric completeness | True |
| Affects requirement completeness | True |
| Affects technical correctness | True |
| Affects safety-critical meaning | True |
| Affects objective scope | True |
| **Criticality** | **CRITICAL** |
| **Disposition** | **RESOLVED** |
| Non-critical class | - |
| Remaining unsupported clauses | none |
| Audit method | `manual_evidence_read` |

**What the packet holds.** The frozen packet states it outright. E001 (DOC000236-C0285, 351.10.01 Basinc Dayanim Siniflari) carries the sentence 'Puskurtme betonun basinc dayanim sinifi minimum C25/30 MPa sinifinda olacaktir', and Tablo-351-5 appears in both E001 and the authority-A E002 (DOC000087-C0284) with the C 25/30 row giving 22,5 MPa individual minimum and 25,5 MPa three-sample-group mean on 28-day cores. E001 is the very chunk the note already cited.

**Why this criticality.** This question is the sole carrier of the required topic 'dayanim sinifi', the SectionPlan marks it required=true, and a section that states cement dosage and lining thickness but never states the strength class does not fulfil an objective whose subject is numeric requirements and specification provisions. It could not have been classified NON_CRITICAL_ENRICHMENT or OPTIONAL_DETAIL under any reading. It was never an evidence gap: v1 scored clause token coverage at 0.22 and 0.00 and called that UNSUPPORTED, which measured wording distance from the cited span, not whether the packet says it. Closed by manual span mapping over the frozen packet - no retrieval, no generation.

## Q-02-2-04

**Püskürtme beton uygulamasında kaç kat uygulanır ve kalınlıkları nedir?**

| Field | Value |
|---|---|
| Priority | P1 |
| SectionPlan `required` | False |
| Packet items read | 20 |
| Citation-ready claims before | 0 |
| Citation-ready claims after | 10 (SEC-02-2-C-003, SEC-02-2-C-004, SEC-02-2-C-005, SEC-02-2-C-006, SEC-02-2-C-007, SEC-02-2-C-008, SEC-02-2-C-009, SEC-02-2-C-010, SEC-02-2-C-011, SEC-02-2-C-012) |
| Affects required-topic coverage | False |
| Affects numeric completeness | True |
| Affects requirement completeness | True |
| Affects technical correctness | True |
| Affects safety-critical meaning | False |
| Affects objective scope | True |
| **Criticality** | **IMPORTANT_NON_BLOCKING** |
| **Disposition** | **RESOLVED** |
| Non-critical class | NON_CRITICAL_ENRICHMENT |
| Remaining unsupported clauses | Q-02-2-04-N01-C01, Q-02-2-04-N02-C01, Q-02-2-04-N08-C02, Q-02-2-04-N15-C01, Q-02-2-04-N15-C02, Q-02-2-04-N15-C03 |
| Audit method | `manual_evidence_read` |

**What the packet holds.** Section 351.08.08 Katman Kalinligi, in both the authority-A E002 (DOC000087-C0279) and E001 (DOC000236-C0280), states the single-pass maximum (15 cm), the first-layer preference (about 60 mm, max 100 mm), the subsequent-layer range (50-200 mm), the inter-layer strength gate and the three-day completion limit. Sections 351.08.09, 351.08.10.02 and 351.08.11 add the steel-fibre, clay-zone and repair-works cases. What the packet does NOT state is a fixed layer count - because the specification does not set one.

**Why this criticality.** The required topic 'kaplama kalinligi' is already carried by Q-02-2-02's P0 claims (4-16 in / 100-400 mm initial lining, 12 in / 300 mm in crushed and squeezing rock), so this question is not load-bearing for topic coverage and the plan marks it required=false. But it is the section's main source of numeric requirements at layer level and the objective is explicitly about numeric requirements, so it is IMPORTANT rather than OPTIONAL, and it is closed rather than classified away. Six clauses remain unsupported and stay unsupported: they are generator framing and summary sentences, not source propositions.

## Q-02-2-06

**Püskürtme beton uygulamasında hasır çelik hangi tiplerde kullanılır?**

| Field | Value |
|---|---|
| Priority | P2 |
| SectionPlan `required` | False |
| Packet items read | 19 |
| Citation-ready claims before | 0 |
| Citation-ready claims after | 5 (SEC-02-2-C-013, SEC-02-2-C-014, SEC-02-2-C-015, SEC-02-2-C-016, SEC-02-2-C-017) |
| Affects required-topic coverage | False |
| Affects numeric completeness | False |
| Affects requirement completeness | False |
| Affects technical correctness | False |
| Affects safety-critical meaning | False |
| Affects objective scope | False |
| **Criticality** | **OPTIONAL** |
| **Disposition** | **RESOLVED** |
| Non-critical class | OPTIONAL_DETAIL |
| Remaining unsupported clauses | none |
| Audit method | `manual_evidence_read` |

**What the packet holds.** E014 (DOC000215-C0002, Celik hasir montaji) enumerates the (R) and (Q) types with their bar counts, the 5.00 x 2.15 m standard sheet and TS 4559. E016 (DOC000124) and E009 (DOC000098) both state the chain-link and welded pair; E016 is used because E009's text is OCR-damaged. E002 (DOC000195) gives one mine's 7 mm / 15x15 cm mesh.

**Why this criticality.** Mesh reinforcement is bound to none of the three required topics and to neither optional topic ('lif donati' is fibre, not mesh); the plan marks the question required=false and priority P2. The section objective is fulfilled without it. It is classified OPTIONAL on those grounds and not because it was unresolved (rule 17): it was in fact resolvable, and it is resolved. Its claims sit on the allowlist as OPTIONAL_ENRICHMENT so a drafter may use them but is not required to. Note that E014 also carries birim fiyat material, which the SectionPlan excludes; no claim is drawn from it.

## Unresolved Numeric Clause

The P0 bundle recorded exactly one: `Q-02-2-04-N06-C01`.

| Clause | Value | Unit | Status | Criticality | Citable |
|---|---|---|---|---|---|
| `Q-02-2-04-N06-C01` | 15 | cm | **SUPPORTED** | IMPORTANT_NON_BLOCKING | yes |
| `Q-02-2-04-N06-C01#derived` | 150 | mm | **DERIVED_ONLY** | IMPORTANT_NON_BLOCKING | no |
| `Q-02-2-02-P0-007#conversion` | 100 to 400 | mm | **SUPPORTED** | CRITICAL | yes |
| `Q-02-2-02-P0-008#conversion` | 300 | mm | **SUPPORTED** | CRITICAL | yes |
| `Q-02-2-05-N04-C02#conversion` | 30 to 50 | mm | **NOT_REQUIRED_FOR_OBJECTIVE** | OPTIONAL | no |

The clause splits cleanly in two. The requirement - *Bir defada uygulanacak püskürtme betonunun maksimum kalınlığı 15 cm'yi geçmeyecektir* - is stated verbatim in the authority-A copy (DOC000087-C0279, §351.08.08) and is now allowlisted as `SEC-02-2-C-003` in the source's own unit. The `150 mm` that travelled beside it is a conversion the generator performed and no source states; it stays DERIVED_ONLY, lives only in structured metadata with `derived=true`, and its wording is on the denylist as `SEC-02-2-DENY-NUM-150MM`. Being arithmetically correct is not the test.

Three further numerics were re-verified rather than inherited, because they carry required topics through bracketed metric conversions of the same shape: the initial lining's `4 to 16 inches (100 to 400 mm)` and `12 in (300 mm) and more` are inside DOC000047's own parentheses, so the source does the converting there and both claims stay allowlisted. A fourth, flashcrete's `30 to 50 mm (1.2 to 2 in)`, turns out to carry a false-positive `unsupported_unit_conversion` flag on SEC-02-2-R026; that is recorded as LIM-006 rather than acted on, because Q-02-2-05 is outside this phase's scope.

## CF-P0-001

**Final status: REQUIRES_QUALIFIER** (criticality IMPORTANT_NON_BLOCKING, same scope: False, difference type `different_material_scope`)

| Side | Claim | Source | Conditions |
|---|---|---|---|
| A | `SEC-02-2-P0-002` Tablo-308-23-b'ye gore, yuksek dayanimli beton disinda maksimum cimento miktari 360 kg/m3 olmalidir. | DOC000087-C0123 / DOC000236-C0120 - Tablo-308-23-b, Etki Siniflarina Gore Projelendirmelerde Esas Alinacak Beton Ozellikleri | genel beton; etki (maruz kalma) siniflarina gore projelendirme; yuksek dayanimli beton haric; maksimum cimento miktari |
| B | `SEC-02-2-P0-003` Puskurtme beton spesifikasyonlarinda, durabilite geregi kuru sistem icin minimum 350 kg/m3 ve yas sistem icin minimum 400 kg/m3 cimento ongorulmustur. | DOC000236-C0267 / DOC000087-C0265 - puskurtme beton sartname bolumu | puskurtme beton; kuru sistem / yas sistem ayrimi; durabilite gerekcesi; minimum cimento miktari |

**Drafting rule.** Both claims may be drafted. Neither may be drafted without its scope. The 360 kg/m3 figure may only appear together with the qualifier that Tablo-308-23-b governs GENERAL concrete designed by exposure class and is not the shotcrete specification, and the two figures may not be placed in a single comparative or concessive sentence - see SYN-001. No averaging, no 'ranges from 350 to 400 with a ceiling of 360', no reconciliation of any kind.

It is classified REQUIRES_QUALIFIER rather than SAFE_CONTEXT_DIFFERENCE deliberately. The two figures do apply under materially different conditions and those conditions are traceable to named tables and sections, which is what safety would require - but the scope qualifier on the 360 kg/m³ figure is *mandatory*, not merely available. Stated bare, that figure reads as a ceiling the 400 kg/m³ wet-system minimum violates. REQUIRES_QUALIFIER records that the qualifier is a condition of use. It is not blocking, because the qualifier travels in the allowlist row itself and a drafting contract can enforce its presence mechanically.

## SYN-001

**Final status: REPLACE_WITH_SEPARATE_SUPPORTED_CLAIMS** (criticality IMPORTANT_NON_BLOCKING, required by section objective: False)

Original: *Yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m³ olarak belirtilse de, püskürtme beton spesifikasyonlarında minimum 350/400 kg/m³ öngörülmüştür (karşıtlık ilişkisi).*

| Component | Support |
|---|---|
| SEC-02-2-P0-002 (360 kg/m3 maximum, Tablo-308-23-b, general concrete) | SUPPORTED |
| SEC-02-2-P0-003 (350 kg/m3 dry-system and 400 kg/m3 wet-system minimums, shotcrete specification) | SUPPORTED |

**Unsupported relation.** The concessive relation itself - 'although the maximum is 360, the minimums are 350/400' - implying that the shotcrete minimums are a stated exception to the general-concrete maximum. No source says this. The two figures come from different chapters governing different materials by different design routes; treating one as an exception to the other is the generator's inference.

**Future drafting rule.** The components are individually supported and individually draftable, each with its own scope. A later drafting contract may state both. It may NOT join them with 'ancak', 'buna ragmen', 'olmasina ragmen', 'olsa da' or any equivalent concessive, adversative or exception-marking connective, and may not present either figure as a limit on the other, unless a source or an approved synthesis contract supports that relation. Q-02-2-01-N04's compound is not to be reassembled.

The safety the previous phase established is preserved exactly: the components go forward, the relation does not. Both components are on the allowlist as separate rows with their own scopes, and the compound is on the denylist as `SEC-02-2-DENY-SYN-001` so restating it cannot make it draftable.

## Claim Allowlist

27 claims. This is not prose and is not a draft - it is the exact, bounded set a later drafting phase may use.

| Claim | Question | Topic | Use | Sources | Qualifiers |
|---|---|---|---|---|---|
| `SEC-02-2-C-001` Püskürtme betonun basınç dayanım sınıfı minimum C25/30 MPa sınıfında olacaktır. | Q-02-2-03 | dayanım sınıfı | REQUIRED_CORE | 1 | 0 |
| `SEC-02-2-C-002` Tablo-351-5'e göre C25/30 sınıfı püskürtme betonda, 28 günlük karot numunelerde bireysel m… | Q-02-2-03 | dayanım sınıfı | SUPPORTED_CONTEXT | 1 | 1 |
| `SEC-02-2-C-003` Bir defada uygulanacak püskürtme betonunun maksimum kalınlığı 15 cm'yi geçmeyecektir. | Q-02-2-04 | kaplama kalınlığı | SUPPORTED_CONTEXT | 2 | 0 |
| `SEC-02-2-C-004` İlk tabaka, taze betonun akmaması için ince olmalı; tercihen yaklaşık 60 mm, maksimum 100 … | Q-02-2-04 | kaplama kalınlığı | SUPPORTED_CONTEXT | 1 | 0 |
| `SEC-02-2-C-005` Takip eden tabakalar, nihai kalınlığa ve kullanılan priz hızlandırıcı katkı malzemesinin t… | Q-02-2-04 | kaplama kalınlığı | SUPPORTED_CONTEXT | 1 | 0 |
| `SEC-02-2-C-006` Kalınlığın artırılması gerektiğinde müteakip tabaka(lar), önceki tabakanın mukavemeti sonr… | Q-02-2-04 | kaplama kalınlığı | SUPPORTED_CONTEXT | 1 | 0 |
| `SEC-02-2-C-007` İlave tabakalar, üç günü geçmeyen bir süre içerisinde tamamlanmış olacaktır. | Q-02-2-04 | kaplama kalınlığı | SUPPORTED_CONTEXT | 1 | 0 |
| `SEC-02-2-C-008` İstenilen nihai kalınlığa bağlı olarak çelik lifli püskürtme beton uygulaması, geri sıçram… | Q-02-2-04 | kaplama kalınlığı | OPTIONAL_ENRICHMENT | 1 | 0 |
| `SEC-02-2-C-009` Kil zonlu tabakalar üzerine püskürtme beton uygulamasında ilk püskürtme beton katmanı gene… | Q-02-2-04 | kaplama kalınlığı | OPTIONAL_ENRICHMENT | 1 | 1 |
| `SEC-02-2-C-010` Tamir işlerinde, priz hızlandırıcı katkı kullanılmaksızın püskürtülen katmanlar için tavsi… | Q-02-2-04 | kaplama kalınlığı | OPTIONAL_ENRICHMENT | 1 | 1 |
| `SEC-02-2-C-011` Tamir işlerinde, ek katman veya takviye donatısı bulunmayan durumda tavsiye edilen kalınlı… | Q-02-2-04 | kaplama kalınlığı | OPTIONAL_ENRICHMENT | 1 | 1 |
| `SEC-02-2-C-012` Yaklaşık 20 °C sıcaklıkta ve herhangi bir priz hızlandırıcı katkı malzemesi kullanılmaz is… | Q-02-2-04 | kaplama kalınlığı | OPTIONAL_ENRICHMENT | 1 | 0 |
| `SEC-02-2-C-013` (R) tipi hasır çelik 15 adet boy ve 20 adet en çubuktan oluşur. | Q-02-2-06 | - | OPTIONAL_ENRICHMENT | 1 | 0 |
| `SEC-02-2-C-014` (Q) tipi hasır çelik 15 adet boy ve 33 adet en çubuktan oluşur. | Q-02-2-06 | - | OPTIONAL_ENRICHMENT | 1 | 0 |
| `SEC-02-2-C-015` Kaya ve zemin desteklemesinde iki tür çelik hasır kullanılır: birbirlerine zincir şeklinde… | Q-02-2-06 | - | OPTIONAL_ENRICHMENT | 1 | 0 |
| `SEC-02-2-C-016` Standart çelik hasır 5.00 x 2.15 m ebadındadır ve çelik hasıra ilişkin TSE standardı TS 45… | Q-02-2-06 | - | OPTIONAL_ENRICHMENT | 1 | 0 |
| `SEC-02-2-C-017` Bir maden işletmesinde 7 mm kalınlığında ve 15 cm x 15 cm göz aralıklı çelik hasır kullanı… | Q-02-2-06 | - | OPTIONAL_ENRICHMENT | 1 | 1 |
| `SEC-02-2-P0-001` Yaş Sistem: Çimento miktarı 400 kg/m³'ten az olmamalıdır. | Q-02-2-01 | çimento dozajı | REQUIRED_CORE | 2 | 0 |
| `SEC-02-2-P0-002` Tablo-308-23-b'ye göre, yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m³ … | Q-02-2-01 | çimento dozajı | SUPPORTED_CONTEXT | 2 | 1 |
| `SEC-02-2-P0-003` Püskürtme beton spesifikasyonlarında, durabilite gereği kuru sistem için minimum 350 kg/m³… | Q-02-2-01 | çimento dozajı | REQUIRED_CORE | 2 | 0 |
| `SEC-02-2-P0-004` Özel Uygulamalar: Şev kaplama, geçici iksa gibi özel durumlarda İdare onayı ile bu miktarl… | Q-02-2-01 | çimento dozajı | SUPPORTED_CONTEXT | 2 | 0 |
| `SEC-02-2-P0-005` Çevresel Şartlar: Dış çevresel etki sınıfları gereksinimlerine göre, laboratuvar ve ön diz… | Q-02-2-01 | çimento dozajı | SUPPORTED_CONTEXT | 1 | 0 |
| `SEC-02-2-P0-006` Özetle, standart uygulamalarda kuru sistem için minimum 350 kg/m³, yaş sistem için ise min… | Q-02-2-01 | çimento dozajı | REQUIRED_CORE | 2 | 0 |
| `SEC-02-2-P0-007` The typical thickness of an initial shotcrete lining ranges from 4 to 16 inches (100 to 40… | Q-02-2-02 | kaplama kalınlığı | REQUIRED_CORE | 2 | 0 |
| `SEC-02-2-P0-008` In some specific rock conditions, such as crushed or squeezing rock, the thickness may be … | Q-02-2-02 | kaplama kalınlığı | REQUIRED_CORE | 1 | 0 |
| `SEC-02-2-R001` Kuru Sistem: Çimento miktarı 350 kg/m³'ten az olmamalıdır. | Q-02-2-01 | çimento dozajı | REQUIRED_CORE | 1 | 0 |
| `SEC-02-2-R025` Flashcrete is not considered an active support and is normally followed by a systematicall… | Q-02-2-05 | - | OPTIONAL_ENRICHMENT | 1 | 1 |

Every row satisfies all of rule 37: SUPPORTED, citation-ready, every source key resolves, every material numeric source-supported, conditions preserved, not superseded, `readiness_use != DO_NOT_DRAFT`.

## Claim Denylist

38 entries. Nothing unresolved was dropped; it was written down.

| Deny reason | Entries |
|---|---|
| `clause_not_fully_supported` | 30 |
| `not_citation_ready` | 30 |
| `support_status_not_supported` | 30 |
| `superseded` | 23 |
| `unsupported_after_full_packet_read` | 6 |
| `unsupported_unit_conversion` | 5 |
| `evidence_refs_incomplete` | 2 |
| `no_resolvable_source_key` | 2 |
| `source_keys_unresolved` | 2 |
| `concessive_relation_asserted_by_no_source` | 1 |
| `derived_numeric_presented_as_source_stated` | 1 |
| `different_material_scope` | 1 |
| `superseded_by_p0_decomposition` | 1 |
| `unsafe_synthesis` | 1 |

Two entries are representations rather than claims - `SEC-02-2-DENY-NUM-150MM` and `SEC-02-2-DENY-SYN-001`. They exist so that a wording whose underlying requirement is allowlisted in a safe form cannot re-enter through the unsafe form.

## Limitation Register

| ID | Question | Criticality | Topic | Workaround | Status |
|---|---|---|---|---|---|
| `LIM-001` | Q-02-2-04 | **IMPORTANT_NON_BLOCKING** | kaplama kalinligi | `state_supported_narrower_claim` | CONTAINED |
| `LIM-002` | Q-02-2-01 | **IMPORTANT_NON_BLOCKING** | cimento dozaji | `separate_conflicting_contexts` | CONTAINED |
| `LIM-003` | Q-02-2-01 | **IMPORTANT_NON_BLOCKING** | cimento dozaji | `preserve_context_qualifier` | CONTAINED |
| `LIM-004` | Q-02-2-04 | **OPTIONAL** | kaplama kalinligi | `omit_optional_material` | CONTAINED |
| `LIM-005` | Q-02-2-03 | **OPTIONAL** | dayanim sinifi | `preserve_context_qualifier` | CONTAINED |
| `LIM-006` | Q-02-2-05 | **OPTIONAL** | - | `omit_optional_material` | OPEN_OUT_OF_SCOPE |
| `LIM-007` | Q-02-2-06 | **OPTIONAL** | - | `preserve_context_qualifier` | CONTAINED |

- **LIM-001**: The 150 mm conversion in the single-pass maximum clause is stated by no source; only 15 cm is. *Drafting impact:* The requirement is fully draftable, but only in centimetres. A draft may not write 150 mm as a specification figure for this clause, and may not present the conversion as source-stated.
- **LIM-002**: CF-P0-001: the 360 kg/m3 general-concrete maximum and the 400 kg/m3 wet-system shotcrete minimum read as contradictory if their scopes are dropped. *Drafting impact:* Both figures are draftable. Neither may appear without its scope qualifier, and they may not be reconciled, averaged or placed in one comparative sentence.
- **LIM-003**: SYN-001: the concessive relation between the 360 maximum and the 350/400 minimums is asserted by no source. *Drafting impact:* The components stay separately draftable; the relation stays undraftable. No concessive or exception-marking connective may join them.
- **LIM-004**: Six Q-02-2-04 clauses remain unsupported after a full packet read: N01-C01, N02-C01, N08-C02, N15-C01, N15-C02, N15-C03. *Drafting impact:* None on coverage. Every one is a generator framing or summary sentence; the propositions they gesture at are carried in mapped form by SEC-02-2-C-003 through C-007.
- **LIM-005**: The 'minimum C25/30' sentence occurs in one packet item only (DOC000236-C0285, unrated); the authority-A copy in the packet carries Tablo-351-5 but not that sentence. *Drafting impact:* None. The question's minimum_sources is 1, DOC000236 and DOC000087 are two copies of the same 2013 specification with identical section numbering, and the authority-A copy corroborates the class through Tablo-351-5's C 25/30 row. Recorded so the single-item provenance is visible rather than implicit.
- **LIM-006**: SEC-02-2-R026 (flashcrete 30-50 mm) carries an 'unsupported_unit_conversion' block that this phase's reading shows to be a false positive: DOC000047 states '30 to 50 mm (1.2 to 2 in)' in its own parentheses. *Drafting impact:* None. Flashcrete is optional enrichment and Q-02-2-05 already has a citation-ready claim (SEC-02-2-R025). R026 stays denylisted at the status the frozen prior phase gave it.
- **LIM-007**: The 7 mm / 15x15 cm mesh figures describe one named mine operation, not a specification requirement. *Drafting impact:* SEC-02-2-C-017 may only be drafted with its scope qualifier. Without it the figures read as a general requirement, which the source does not state.

No limitation is answered by general knowledge, model memory, the web or an invented synthesis. Every workaround is one of the four permitted forms or NONE.

## Manifest Consistency Audit

| Source | Value |
|---|---|
| `p0_retrieval_gap_probes_v1.jsonl :: retrieval_gap_candidate == true` | 1 |
| `p0_retrieval_gap_probes_v1.jsonl :: verdict == candidate_retrieval_gap` | 1 |
| `p0_retrieval_expansion_v1.jsonl :: retrieval_gap_confirmed == true` | 1 |
| `manifest :: retrieval_gap_candidates` | 1 |
| `manifest :: retrieval_expansion_attempts` | 0 |
| `report :: confirmed retrieval gaps stated as unconfirmed candidates` | 0 |
| **Canonical** | **1** |

Inconsistency found: **True**. The expansion artifact confirms one retrieval gap (Q-02-3-02-N15-C01: the packet contains no item mentioning 'titreşim' or 'gürültü' at all). The manifest records it under the field name `retrieval_gap_candidates` and has no field for confirmed gaps, and the report's Corpus Gap Assessment describes every retrieval gap as an unconfirmed candidate handed forward. So the same gap reads as 1 in the expansion artifact and as 0 confirmed in the report narrative. It is a naming and reporting inconsistency, not a data conflict: all three artifacts point at one clause.

**Confirmed retrieval gaps in P0 Evidence Gap Resolution v1: 1 (Q-02-3-02-N15-C01).** Source of truth: `data/book/p0_resolution/audits/p0_retrieval_expansion_v1.jsonl (retrieval_gap_confirmed), corroborated by p0_retrieval_gap_probes_v1.jsonl (retrieval_gap_candidate)`.

Impact on SEC-02-2: None. The confirmed gap belongs to Q-02-3-02, a SEC-02-3 question. No SEC-02-2 clause is a retrieval-gap candidate, and this phase performed no retrieval.

The historical P0 report is left byte-identical (rule 56); the correction is recorded here and in `audits/p0_manifest_consistency_v1.json`, not applied there.

## Generation / Retrieval Usage

- Generation calls: **0**
- Retrieval calls: **0**
- Retrieval expansion attempts: **0**; production default top_k unchanged
- Revised queries authored: **0**; no same-question retry

Neither budget was needed. Every proposition this phase closed was already inside a frozen ContextPacket, which is also the only place it could have come from: evidence retrieved outside a packet has no packet sha and could not carry a citation-ready claim.

## Frozen Integrity

77 checks, all unchanged.

Retriever v1, Context v1, Prompt v5, Output Contract v1.1, Production Grounded Generator v1, Evidence Note Contract v1, Book Pipeline v1, Extractor v1.1, the manual audit, remediation v1, every P0 Evidence Gap Resolution v1 artifact, the source registry, the corpus chunks and the production audit log are byte-identical.

## Tests

`tests/test_sec_02_2_draft_readiness_closure_v1.py` - passed, 89 tests.

The suite asserts the contract rather than the conclusion: that the acceptance file exists and was authored first, that all three required topics appear in the coverage matrix, that a READY_FOR_DRAFT verdict implies complete coverage and zero critical limitations, that every allowlisted claim is supported, traceable, unsuperseded and numerically safe, that known-unsafe items cannot enter the allowlist, that 150 mm never appears as source-stated, that SYN-001 stays undraftable, that CF-P0-001 keeps explicit conditions, that each of Q-02-2-03/04/06 carries an explicit criticality and disposition, that the canonical retrieval-gap count is recorded once, and that frozen integrity holds.

## Final Readiness Decision

**SEC-02-2: READY_WITH_LIMITATIONS**

| Gate | Result |
|---|---|
| acceptance contract authored before results | PASS |
| acceptance contract unweakened | PASS |
| all p1 p2 gaps classified | PASS |
| all required topics assessed | PASS |
| allowlist fully traceable | PASS |
| context difference closed | PASS |
| derived numeric not allowlisted | PASS |
| drafting disabled | PASS |
| dropped synthesis closed | PASS |
| every authored span verified | PASS |
| existing packet evidence used first | PASS |
| frozen integrity holds | PASS |
| generation calls zero | PASS |
| historical p0 report untouched | PASS |
| manifest consistency audited | PASS |
| no superseded claim allowlisted | PASS |
| numeric clause closed | PASS |
| qdrant unchanged | PASS |
| qdrant writes zero | PASS |
| readiness recomputed | PASS |
| retrieval calls zero | PASS |
| synthesis not recombined | PASS |
| tests pass | PASS |
| unresolved material recorded not dropped | PASS |

### Why not READY_FOR_DRAFT

Read against the acceptance criteria above, every enumerated READY_FOR_DRAFT condition passes: all three required topics are covered by supported, citation-ready, traceable claims; both P0 questions stay resolved with no regression; no P1/P2 gap is CRITICAL and unresolved; no numeric issue is critical; CF-P0-001 is not BLOCKING_CONFLICT; SYN-001 is not BLOCKING_MISSING_SYNTHESIS; the allowlist is fully traceable and numerically safe; drafting is disabled. That tension is real and is the substance of this decision, so it is stated rather than smoothed over.

The section is held at READY_WITH_LIMITATIONS on one ground:

> Every READY_FOR_DRAFT condition in the frozen contract is satisfied except that residual composition constraints remain that no existing contract can enforce: ['CF-P0-001', 'SYN-001']. These bound how allowlisted claims may be joined and qualified, not which may be used, and claim-level allow/deny cannot express them.

The allowlist and denylist bound **which claims** may be used, and any consumer can enforce that today by reading two files. CF-P0-001 and SYN-001 are not selection constraints. They bound **how claims may be joined**: the 360 kg/m³ figure may not appear without its scope qualifier, and it may not be placed in a concessive or comparative sentence with the 350/400 kg/m³ minimums. Nothing in this project can currently enforce either rule, because no contract constrains prose composition - that is what the Section Drafting Contract would be.

This matters because SYN-001 was itself a joining failure, not a selection failure. Both of its components were individually well-supported; the defect was the connective between them. Handing a drafter an allowlist that contains `SEC-02-2-P0-002` and `SEC-02-2-P0-003` as adjacent rows, with the mandatory qualifier travelling as an unenforced data field, reproduces the exact conditions that produced the defect the previous phase had to drop. Marking the section READY_FOR_DRAFT would be asserting a safety property the project cannot yet enforce.

So the honest verdict is READY_WITH_LIMITATIONS, and the limitations that hold it there are specific, named and actionable: they are composition rules, and the next phase's job is to make them enforceable. This is not the previous phase's error repeated in the other direction - the required-topic gap that made the section genuinely unready is closed on verified evidence, and what remains is a smaller, different, and precisely stated thing.

Non-blocking limitations carried forward:

- numeric Q-02-2-04-N06-C01#derived: DERIVED_ONLY
- CF-P0-001: REQUIRES_QUALIFIER
- SYN-001: REPLACE_WITH_SEPARATE_SUPPORTED_CLAIMS

`drafting_enabled` is `false` in the manifest, the bundle and the acceptance contract. This phase does not enable drafting under any outcome.

## Next Phase

**SEC-02-2 LIMITATION RESOLUTION V1**

Why: required topics are covered and no limitation is blocking, but READY_WITH_LIMITATIONS does not authorise drafting.

Sections in scope: SEC-02-2.

Carried forward:

- numeric Q-02-2-04-N06-C01#derived: DERIVED_ONLY
- CF-P0-001: REQUIRES_QUALIFIER
- SYN-001: REPLACE_WITH_SEPARATE_SUPPORTED_CLAIMS
