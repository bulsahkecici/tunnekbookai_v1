# SEC-02-2 Limitation Resolution v1

## Executive Decision

**SEC-02-2 LIMITATION RESOLUTION V1 - CLOSED / GO**

**SEC-02-2: READY_FOR_DRAFT**

The two composition limitations that held this section short of READY_FOR_DRAFT are now enforced by a deterministic validator: 3 mandatory qualifier rule, 1 forbidden-synthesis rule with 10 patterns, 1 derived-numeric rule and 6 claim-pair constraints, scored against 71 regression fixtures (35 positive / 36 negative) with 0 false accepts and 0 false rejects. Generation calls: 0. Retrieval calls: 0. `drafting_authorized` is **false**.

## Why Composition Needed Its Own Gate

SYN-001 is the whole argument, so it is worth being precise about what it was.

Its two components were individually well-supported. The 360 kg/m³ maximum is stated verbatim in Tablo-308-23-b, in an authority-A source, with a verified span and a resolvable citation key. The 350 and 400 kg/m³ minimums are stated verbatim in the shotcrete specification, likewise verified and citable. Every claim-level check the pipeline can run - support status, span verification, numeric source-statedness, provenance, citation readiness - passes on both.

The defect was the word *between* them. `belirtilse de` - "although it is stated" - asserts that the shotcrete minimums stand in a concessive relation to the general maximum, that one is an exception to or a tension with the other. No source says that. The figures govern different materials by different design routes in different chapters.

A pipeline that validates claims one at a time cannot see this, because **at the level of a single claim there is nothing wrong**. That is why the previous phase declined READY_FOR_DRAFT despite every enumerated condition passing: the allowlist and denylist bound which claims may be used, and neither can express "these two may not share a sentence". This phase builds the layer that can.

The core principle it encodes:

> supported claim A + supported claim B does NOT imply 'A therefore B', 'A although B', 'A contradicts B' or 'A is an exception to B' unless that relationship is itself supported by a source or an approved synthesis contract.

## Frozen Inputs

| Input | State |
|---|---|
| Closure v1 manifest | `07b3272adb0b7d3d` |
| Parent readiness bundle | `2408c295a0d833a7` |
| Input evidence allowlist | 27 claims |
| Frozen integrity checks | 98, all unchanged |
| Source registries | untouched (book, P0, closure) |
| Qdrant | **not reachable during this run** - count unobserved; 0 writes |
| Generation calls | 0 |
| Retrieval calls | 0 |

**On Qdrant.** Qdrant was not reachable at http://localhost:6333 during this run, so the point count could not be observed and is reported as unknown rather than as the expected 5992. The phase performs no retrieval, opens no Qdrant client and holds no write path. The expected count is 5992; it is reported as unknown rather than restated from a previous manifest, because a number nobody measured in this run is not an observation.

## CF-P0-001

The apparent conflict and why it is not one:

| | 360 kg/m³ | 350 / 400 kg/m³ |
|---|---|---|
| Material | general concrete | shotcrete (dry / wet system) |
| Requirement direction | **maximum** | **minimum** |
| Document | Tablo-308-23-b, exposure-class design table | shotcrete specification |
| Design route | designed by exposure class | shotcrete mix specification |

Four independent axes of difference. Drop any one of them and the numbers look like they contradict - a 400 minimum above a 360 maximum. Keep all four and there is no tension at all, because the two figures never apply to the same concrete.

That is exactly why the qualifier is **mandatory rather than merely useful**: the bare figure is not incomplete, it is misleading in a way a reader cannot detect.

## Scope Binding

All 27 allowlisted claims carry an authored scope, each with the evidence that establishes it. Scope is never inferred where the source does not establish it.

| Claim | Material | System | Requirement | Document |
|---|---|---|---|---|
| `SEC-02-2-C-001` | shotcrete | system_independent | minimum, mandatory | KTS 2013 §351.10.01 |
| `SEC-02-2-C-002` | shotcrete | system_independent | design_table | Tablo-351-5 (KGM 2013) |
| `SEC-02-2-C-003` | shotcrete | system_independent | maximum, mandatory | KTS/KGM 2013 §351.08.08 |
| `SEC-02-2-C-004` | shotcrete | system_independent | recommended, maximum | KTS/KGM 2013 §351.08.08 |
| `SEC-02-2-C-005` | shotcrete | system_independent | typical_range | KTS/KGM 2013 §351.08.08 |
| `SEC-02-2-C-006` | shotcrete | system_independent | mandatory | KTS/KGM 2013 §351.08.08 |
| `SEC-02-2-C-007` | shotcrete | system_independent | maximum, mandatory | KTS/KGM 2013 §351.08.08 |
| `SEC-02-2-C-008` | steel_fibre_shotcrete | system_independent | typical_range | KTS/KGM 2013 §351.08.09 |
| `SEC-02-2-C-009` | shotcrete | system_independent | typical_range, case_specific | KTS 2013 §351.08.10.02 |
| `SEC-02-2-C-010` | shotcrete | system_independent | recommended, case_specific | KTS/KGM 2013 §351.08.11 |
| `SEC-02-2-C-011` | shotcrete | system_independent | recommended, case_specific | KTS/KGM 2013 §351.08.11 |
| `SEC-02-2-C-012` | shotcrete | system_independent | typical_range, case_specific | KTS/KGM 2013 §351.08.11 |
| `SEC-02-2-C-013` | steel_mesh | not_applicable | design_table | DOC000215 'Çelik hasır montajı' |
| `SEC-02-2-C-014` | steel_mesh | not_applicable | design_table | DOC000215 'Çelik hasır montajı' |
| `SEC-02-2-C-015` | steel_mesh | not_applicable | design_table | DOC000124 / DOC000098 |
| `SEC-02-2-C-016` | steel_mesh | not_applicable | design_table | DOC000215 'Çelik hasır montajı' |
| `SEC-02-2-C-017` | steel_mesh | not_applicable | case_specific | DOC000195 |
| `SEC-02-2-P0-001` | wet_system_shotcrete | wet_system | minimum | püskürtme beton şartnamesi |
| `SEC-02-2-P0-002` | general_concrete | not_applicable | maximum, design_table | Tablo-308-23-b (KGM/KTS 2013) |
| `SEC-02-2-P0-003` | shotcrete | system_independent | minimum | püskürtme beton şartnamesi |
| `SEC-02-2-P0-004` | shotcrete | system_independent | case_specific | püskürtme beton şartnamesi |
| `SEC-02-2-P0-005` | shotcrete | system_independent | minimum, project_specific | püskürtme beton şartnamesi |
| `SEC-02-2-P0-006` | shotcrete | system_independent | minimum | püskürtme beton şartnamesi |
| `SEC-02-2-P0-007` | initial_shotcrete_lining | not_applicable | typical_range | FHWA Technical Manual (DOC000047) §9.3.3 |
| `SEC-02-2-P0-008` | initial_shotcrete_lining | not_applicable | typical_range, case_specific | FHWA Technical Manual (DOC000047) support-class table |
| `SEC-02-2-R001` | dry_system_shotcrete | dry_system | minimum | püskürtme beton şartnamesi |
| `SEC-02-2-R025` | flashcrete | not_applicable | typical_range | FHWA Technical Manual (DOC000047) |

The three restricted figures - the only ones whose composition is constrained:

| Figure | Claim | Material | Direction |
|---|---|---|---|
| 360 kg/m³ general-concrete maximum | `SEC-02-2-P0-002` | general_concrete | maximum |
| 350 kg/m³ dry-system shotcrete minimum | `SEC-02-2-R001` | dry_system_shotcrete | minimum |
| 400 kg/m³ wet-system shotcrete minimum | `SEC-02-2-P0-001` | wet_system_shotcrete | minimum |

Figure detection is **unit-scoped throughout**. Matching on bare values would make the `400` in "4 to 16 inches (100 to 400 mm)" collide with the 400 kg/m³ wet-system cement minimum - a different quantity in a different material sharing a numeral. Fixture `POS-LINING-01` pins that.

## Mandatory Qualifiers

**MQ-001** - `SEC-02-2-P0-002` - severity **BLOCKING** (from CF-P0-001)

- Required scope: `general_concrete`
- Required qualifier: *Tablo-308-23-b, etki sınıflarına göre projelendirmede esas alınacak GENEL beton özelliklerine ilişkindir; püskürtme beton şartnamesi değildir*
- Forbidden bare form: *"Maksimum çimento miktarı 360 kg/m³'tür."* → `UNQUALIFIED_SCOPE`
- Forbidden scopes: ['shotcrete', 'dry_system', 'wet_system'] → `AMBIGUOUS_SCOPE`
- Presenting the general-concrete maximum as a shotcrete figure states something false about shotcrete while citing a true statement about general concrete - the citation would resolve and the sentence would still be wrong.

**MQ-002** - `SEC-02-2-R001` - severity **BLOCKING** (from CF-P0-001)

- Required scope: `shotcrete`
- Required qualifier: *püskürtme beton (kuru sistem) şartname hükmüdür*
- Forbidden bare form: *"(bare form permitted - the section's subject supplies the correct scope)"* → `UNQUALIFIED_SCOPE`
- Forbidden scopes: ['general_concrete'] → `AMBIGUOUS_SCOPE`
- The mirror of MQ-001: a dry-system shotcrete minimum presented as a general-concrete requirement. Tablo-308-23-b sets no cement minimum at all, so this attributes to it a requirement it does not contain.

**MQ-003** - `SEC-02-2-P0-001` - severity **BLOCKING** (from CF-P0-001)

- Required scope: `shotcrete`
- Required qualifier: *püskürtme beton (yaş sistem) şartname hükmüdür*
- Forbidden bare form: *"(bare form permitted - the section's subject supplies the correct scope)"* → `UNQUALIFIED_SCOPE`
- Forbidden scopes: ['general_concrete'] → `AMBIGUOUS_SCOPE`
- The mirror of MQ-001 for the wet-system minimum. Attributing it to general concrete would also place a 400 kg/m³ minimum above Tablo-308-23-b's 360 kg/m³ maximum, manufacturing the very contradiction CF-P0-001 exists to prevent.

**The negation trap.** The qualifier this rule mandates ends "...GENEL beton özelliklerine ilişkindir; **püskürtme beton şartnamesi değildir**". A wrong-scope check that simply looked for shotcrete markers near the 360 figure would reject the one form the contract requires. Negation handling is therefore load-bearing, not a nicety: a marker followed by a denial within 60 characters is not an assertion of that scope. Fixture `POS-360-03` is the qualifier verbatim and must pass.

## SYN-001

**FS-001** - severity **BLOCKING** - safe representation: `SEPARATE_SUPPORTED_CLAIMS`

Forbidden relationship: concessive / exception relation between the general-concrete maximum and the shotcrete minimums

Components (each individually supported and separately draftable): `SEC-02-2-P0-002`, `SEC-02-2-P0-003`, `SEC-02-2-R001`, `SEC-02-2-P0-001`

## Forbidden Synthesis Rules

Two layers, and the second is the one that matters.

**Layer 1 - 10 patterns** matching the historical wording and its variants:

- historical SYN-001 wording: 360 joined to 350 or 400 by a concessive
- the same construction in reverse order (minimum first, maximum second)
- the 350/400 slash abbreviation placed after 360
- the 350/400 slash abbreviation placed before 360
- 360 named as having an exception
- 360 named as being an exception
- 360 asserted to contradict the shotcrete minimums - no TRUE_CONFLICT record exists, CF-P0-001 is a CONTEXT_DIFFERENCE
- the same contradiction claim in reverse order
- a fabricated 350-400 interval collapsing the dry/wet system distinction
- 360 recast as a ceiling or upper limit over the shotcrete minimums

**Layer 2 - the same-sentence prohibition.** The 360 figure may not share a sentence with 350 or 400 under *any* phrasing. No connector analysis, no pattern.

This layering is deliberate. A pattern list is only ever as good as the imagination of whoever wrote it; a drafter who picks a conjunction nobody enumerated walks straight through it. Fixture `NEG-SYN-05` makes the point - it joins the two figures with `iken`, which appears in no connector list in this contract, and it is caught anyway because the juxtaposition itself is the defect.

A semicolon is deliberately **not** treated as a sentence boundary. "X is 360; Y is 400" is one sentence inviting the comparison the rule exists to prevent, and splitting on `;` would let it through on punctuation (`NEG-SYN-03`).

What remains permitted, and must: separate sentences, each scoped, no connector (`POS-PARA-01`), or separate list items (`POS-PARA-02`). And 350 vs 400 in one sentence **passes** (`POS-350-400-01`), because that comparison is the source's own - it states both minimums in one span, distinguished by system. The contract does not forbid figures from meeting; it forbids asserting relations no source states.

## Derived Numeric Rule

**DN-001** - `SEC-02-2-C-003` - severity **BLOCKING** - policy `SOURCE_STATED_ONLY`

- Source-stated: **15 cm**
- Derived only: **150 mm** (derived=True, source_stated=False)
- Fires in context: ['bir defada', 'tek seferde', 'tek geçişte', 'bir kerede', 'maksimum kalınlık', 'maksimum kalınlığı', 'single pass', 'in one pass', 'single application']
- Stands down in context: ['kil zonu', 'kil zonlu', 'clay zone', '351.08.10.02', '100-150', '100 - 150', '100–150']

**The exemption is the difficulty.** SEC-02-2-C-009 states 'İlk püskürtme beton katmanı genellikle 100-150 mm'dir' for clay-zone layers. That 150 mm is source-stated and cited; it is a different clause with different provenance and must keep passing.

A later drafting contract may choose to render '15 cm (150 mm)' with the conversion explicitly marked as calculated and the citation making clear that 150 mm is not source-stated. That is not the default here. For SEC-02-2 Drafting Contract v1 the policy is SOURCE_STATED_ONLY, so 150 mm stays out of the draft allowlist entirely.

## Composition-Safe Allowlist

27 claims, from 27 on the evidence allowlist. No claim was dropped: a claim bound by a mandatory qualifier is **constrained, not removed**. It remains draftable; it simply cannot be drafted bare.

| Claim | Topic | Scope | Rules | Same-sentence restrictions |
|---|---|---|---|---|
| `SEC-02-2-C-001` | dayanım sınıfı | shotcrete | - | no |
| `SEC-02-2-C-002` | dayanım sınıfı | shotcrete | - | no |
| `SEC-02-2-C-003` | kaplama kalınlığı | shotcrete | DN-001 | no |
| `SEC-02-2-C-004` | kaplama kalınlığı | shotcrete | - | no |
| `SEC-02-2-C-005` | kaplama kalınlığı | shotcrete | - | no |
| `SEC-02-2-C-006` | kaplama kalınlığı | shotcrete | - | no |
| `SEC-02-2-C-007` | kaplama kalınlığı | shotcrete | - | no |
| `SEC-02-2-C-008` | kaplama kalınlığı | steel_fibre_shotcrete | - | no |
| `SEC-02-2-C-009` | kaplama kalınlığı | shotcrete | - | no |
| `SEC-02-2-C-010` | kaplama kalınlığı | shotcrete | - | no |
| `SEC-02-2-C-011` | kaplama kalınlığı | shotcrete | - | no |
| `SEC-02-2-C-012` | kaplama kalınlığı | shotcrete | - | no |
| `SEC-02-2-C-013` | - | steel_mesh | - | no |
| `SEC-02-2-C-014` | - | steel_mesh | - | no |
| `SEC-02-2-C-015` | - | steel_mesh | - | no |
| `SEC-02-2-C-016` | - | steel_mesh | - | no |
| `SEC-02-2-C-017` | - | steel_mesh | - | no |
| `SEC-02-2-P0-001` | çimento dozajı | wet_system_shotcrete | MQ-003, FS-001 | yes |
| `SEC-02-2-P0-002` | çimento dozajı | general_concrete | MQ-001, FS-001 | yes |
| `SEC-02-2-P0-003` | çimento dozajı | shotcrete | FS-001 | yes |
| `SEC-02-2-P0-004` | çimento dozajı | shotcrete | - | no |
| `SEC-02-2-P0-005` | çimento dozajı | shotcrete | - | yes |
| `SEC-02-2-P0-006` | çimento dozajı | shotcrete | - | yes |
| `SEC-02-2-P0-007` | kaplama kalınlığı | initial_shotcrete_lining | - | no |
| `SEC-02-2-P0-008` | kaplama kalınlığı | initial_shotcrete_lining | - | no |
| `SEC-02-2-R001` | çimento dozajı | dry_system_shotcrete | MQ-002, FS-001 | yes |
| `SEC-02-2-R025` | - | flashcrete | - | no |

## Composition Denylist

45 entries, in two layers.

| Layer | Entries |
|---|---|
| composition | 7 |
| evidence | 38 |

The evidence layer is carried forward from the closure phase unaltered, so a consumer reading only this file is still stopped from citing a superseded, partial or unsupported claim. The composition layer adds the forms that are unsafe *as written* even though their figures are true and cited:

- `SEC-02-2-DENY-COMP-150MM-SOURCE-STATED` - *"Kaynak, bir defada uygulanacak maksimum kalınlığı 150 mm olarak vermektedir."* - enforced by ['DN-001']
- `SEC-02-2-DENY-COMP-350-AS-GENERAL` - *"Genel beton için minimum çimento miktarı 350 kg/m³'tür."* - enforced by ['MQ-001']
- `SEC-02-2-DENY-COMP-360-400-CONTRAST` - *"Maksimum 360 kg/m³ sınırına karşın yaş sistemde minimum 400 kg/m³ istenmektedir."* - enforced by ['FS-001', 'PC-002']
- `SEC-02-2-DENY-COMP-360-AS-SHOTCRETE` - *"Püskürtme beton için maksimum çimento miktarı 360 kg/m³'tür."* - enforced by ['MQ-001']
- `SEC-02-2-DENY-COMP-360-UNQUALIFIED` - *"Maksimum çimento miktarı 360 kg/m³'tür."* - enforced by ['MQ-001']
- `SEC-02-2-DENY-COMP-CEMENT-RANGE` - *"Püskürtme betonda çimento dozajı 350 ila 400 kg/m³ arasındadır."* - enforced by ['FS-001', 'FAM-SHOTCRETE-CEMENT-MIN']
- `SEC-02-2-DENY-COMP-SYN-001-COMPOUND` - *"Yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m³ olarak belirtilse de, püskürtme beton spesifikasyonlarında minimum 350/400 kg/m³ öngörülmüştür."* - enforced by ['FS-001', 'PC-001', 'PC-002', 'PC-003', 'PC-004']

`SEC-02-2-DENY-COMP-360-AS-SHOTCRETE` deserves particular note: its citation would resolve perfectly and the sentence would still be false. That is the case that shows why scope binding cannot be left to citation checking.

## Claim Pair Constraints

| Constraint | Pair | Policy | Same sentence | Same paragraph |
|---|---|---|---|---|
| `PC-001` | `SEC-02-2-P0-002` / `SEC-02-2-R001` | INDEPENDENT | **forbidden** | allowed |
| `PC-002` | `SEC-02-2-P0-002` / `SEC-02-2-P0-001` | INDEPENDENT | **forbidden** | allowed |
| `PC-003` | `SEC-02-2-P0-002` / `SEC-02-2-P0-003` | INDEPENDENT | **forbidden** | allowed |
| `PC-004` | `SEC-02-2-P0-002` / `SEC-02-2-P0-006` | INDEPENDENT | **forbidden** | allowed |
| `PC-005` | `SEC-02-2-R001` / `SEC-02-2-P0-001` | SOURCE_SUPPORTED_RELATION | allowed | allowed |
| `PC-006` | `SEC-02-2-P0-002` / `SEC-02-2-P0-005` | INDEPENDENT | **forbidden** | allowed |

Every constraint is decided deterministically; none requires manual review, which is what lets the pair layer be enforced by a validator rather than by a reviewer.

## Composition Validator

`scripts/46_sec_02_2_claim_composition_validator_v1.py` (`db1e458c1280015d`)

It validates claim use, claim combination, scope qualifiers, derived numbers and forbidden synthesis. It is **not** a prose quality validator and does not attempt to be.

Three commitments:

- **Deterministic.** Every decision is a regex, a set membership or a sentence-window comparison. No LLM judge.
- **Fail closed.** No auto-rewrite, no auto-repair, no qualifier injection. An invalid unit is rejected with required actions. A unit whose scope cannot be determined fails as `AMBIGUOUS_SCOPE` rather than passing on the benefit of the doubt.
- **Scoped to SEC-02-2.** It knows about three figures in two materials and says so. Widening it is a later decision, not a side effect of this one.

Failure codes: `UNQUALIFIED_SCOPE`, `FORBIDDEN_SYNTHESIS`, `UNSUPPORTED_RELATION`, `DERIVED_VALUE_AS_SOURCE_STATED`, `CLAIM_NOT_ALLOWLISTED`, `CLAIM_SUPERSEDED`, `CLAIM_PARTIAL`, `CLAIM_UNSUPPORTED`, `MISSING_SOURCE_KEY`, `AMBIGUOUS_SCOPE`

## Regression Fixtures

`data/evaluation/sec_02_2_claim_composition_v1.jsonl` - **71 cases** (35 positive, 36 negative), all synthetic. Several are deliberately wrong. None is SEC-02-2 prose.

| Metric | Value |
|---|---|
| Cases | 71 |
| Passed | 71 |
| **False accepts** | **0** |
| **False rejects** | **0** |
| Code mismatches | 0 |

A false accept is a case the contract says must fail that the validator passed - the dangerous direction. A code mismatch is tracked separately because a case that fails for the wrong reason is a rule that is not doing the job it claims to.

The cases that carry the most weight:

| Case | What it pins |
|---|---|
| `POS-360-03` (PASS) | The mandatory qualifier verbatim. This is the trap case: the qualifier itself contains 'püskürtme beton', and negation handling must stop that reading as a shotcrete scope. |
| `NEG-360-01` (FAIL) | The bare form named in the qualifier rule. |
| `NEG-360-03` (FAIL) | Misattribution: a true general-concrete figure asserted about shotcrete. The citation would resolve and the sentence would still be false. |
| `NEG-SYN-01` (FAIL) | The historical SYN-001 wording, verbatim. |
| `NEG-SYN-05` (FAIL) | No connective from any enumerated list - just 'iken'. Caught by the same-sentence rule, which is the point of having it: the prohibition does not depend on the word chosen. |
| `NEG-SYN-11` (FAIL) | Separate sentences, each correctly scoped - and the second opens with 'Buna rağmen', which ties them back together. This is the cross-sentence case the paragraph allowance must not let through. |
| `POS-350-400-01` (PASS) | The comparison the source itself makes, with both systems named. Must PASS - this is the case that proves the contract does not simply forbid figures from meeting. |
| `POS-PARA-01` (PASS) | Both claims in one paragraph, separate sentences, each scoped, no connector. This is the arrangement CF-P0-001 permits and the reason the pair policy is INDEPENDENT rather than a ban. |
| `NEG-150MM-02` (FAIL) | The requirement restated in the derived unit. True by arithmetic, unstated by any source. |
| `POS-150MM-EXEMPT-01` (PASS) | The exemption that matters: this 150 mm IS source-stated, in a different clause with different provenance. A guard keyed on the string would reject a true, cited claim. |
| `POS-LINING-01` (PASS) | Critical regression: this sentence contains '400 mm'. Unit-scoped figure detection must not read it as the 400 kg/m³ wet-system cement minimum. |
| `POS-MESH-02` (PASS) | Contains '15 cm' twice in a completely unrelated sense. Must not trip the thickness rules. |

## Required Topic Coverage After Constraints

| Topic | Before | After | Core claims | Constrained | Dropped |
|---|---|---|---|---|---|
| `çimento dozajı` | COMPLETE_WITH_QUALIFIER | **COMPLETE_WITH_QUALIFIER** | 4 | 3 | 0 |
| `kaplama kalınlığı` | COMPLETE_WITH_QUALIFIER | **COMPLETE_WITH_QUALIFIER** | 2 | 1 | 0 |
| `dayanım sınıfı` | COMPLETE_WITH_QUALIFIER | **COMPLETE_WITH_QUALIFIER** | 1 | 0 | 0 |

Composition safety removed support from no required topic. That check exists because the failure mode it guards against is silent: a constraint that quietly eliminated a topic's only core claim would leave the section looking safer and actually be incomplete.

## Remaining Limitations

Resolved by this phase:

- CF-P0-001 - enforced by MQ-001 and pair constraints PC-001..PC-004, PC-006; unqualified and misattributed forms are rejected
- SYN-001 - enforced by FS-001 pattern rules plus the same-sentence prohibition, which catches constructions no pattern lists
- 15 cm / 150 mm guard - enforced by DN-001, with the source-stated clay-zone 150 mm correctly exempted

None. Every composition limitation carried into this phase is now enforced by a rule with a regression case proving it fires.

Carried forward unchanged, and out of scope here: the OPTIONAL limitations the closure phase registered (LIM-004's six unsupported Q-02-2-04 framing clauses, LIM-005's single-item provenance for the C25/30 sentence, LIM-006's flashcrete false-positive flag, LIM-007's mine-specific mesh scope). None is a composition constraint and none blocks drafting; LIM-007's scope qualifier travels on `SEC-02-2-C-017` as a claim field.

## Frozen Integrity

98 checks, all unchanged.

Retriever v1, Context v1, Prompt v5, Output Contract v1.1, Production Grounded Generator v1, Evidence Note Contract v1, Book Pipeline v1, Extractor v1.1, the manual audit, remediation v1, every P0 Evidence Gap Resolution v1 artifact, every SEC-02-2 Draft Readiness Closure v1 artifact, all three source registries, the corpus chunks and the production audit log are byte-identical.

### Manifest Consistency (carried)

Confirmed retrieval gaps in P0 Evidence Gap Resolution v1: 1 (Q-02-3-02-N15-C01). Source of truth: `data/book/p0_resolution/audits/p0_retrieval_expansion_v1.jsonl (retrieval_gap_confirmed), corroborated by p0_retrieval_gap_probes_v1.jsonl (retrieval_gap_candidate)`. Impact on SEC-02-2: None. The confirmed gap belongs to Q-02-3-02, a SEC-02-3 question. No SEC-02-2 clause is a retrieval-gap candidate, and this phase performed no retrieval.

Carried verbatim from the closure phase's audit. This phase performed no retrieval, opened no new gap question and altered no historical artifact; the canonical count is restated here so a consumer of this bundle does not have to reach back two phases for it.

## Tests

`tests/test_sec_02_2_limitation_resolution_v1.py`, `tests/test_sec_02_2_claim_composition_validator_v1.py` - passed, 118 tests.

The suites assert the contract and the enforcement, not the wording: that every allowlisted claim has an authored scope, that CF-P0-001 and SYN-001 carry BLOCKING rules, that the qualified 360 form passes and the bare and misattributed forms fail, that the historical SYN-001 compound is rejected, that separate scoped claims are accepted, that 150 mm cannot be attributed to a source while the clay-zone 150 mm still passes, that 350 vs 400 remains comparable, that superseded / partial / unknown claims are rejected, that allowlist and denylist are disjoint, that all three required topics survive, and that no manuscript artifact exists.

## Final Readiness

**SEC-02-2: READY_FOR_DRAFT**

| Gate | Result |
|---|---|
| allowlist denylist disjoint | PASS |
| cf p0 001 has blocking qualifier rule | PASS |
| composition contract authored | PASS |
| derived numeric rule present | PASS |
| drafting disabled | PASS |
| drafting not authorized | PASS |
| every allowlisted claim composition safe | PASS |
| every allowlisted claim has source keys | PASS |
| every allowlisted claim scoped | PASS |
| fixture minimum met | PASS |
| frozen integrity holds | PASS |
| generation calls zero | PASS |
| historical artifacts unmodified | PASS |
| manifest consistency carried | PASS |
| no prose written | PASS |
| pair constraints deterministic | PASS |
| qdrant unchanged | PASS |
| qdrant writes zero | PASS |
| required topics still covered | PASS |
| retrieval calls zero | PASS |
| syn 001 has blocking rule | PASS |
| tests pass | PASS |
| zero code mismatches | PASS |
| zero false accepts | PASS |
| zero false rejects | PASS |

`drafting_enabled` is `false` and `drafting_authorized` is `false`. This phase does not authorise drafting under any outcome - that decision belongs to the Section Drafting Contract, which is the consumer of the bundle this phase produced, not its author.

## Next Phase

**SECTION DRAFTING CONTRACT V1 + BOOK CITATION RENDERING CONTRACT V1**

Why: the evidence layer was closed by the previous phase and the composition layer is now enforced by a deterministic validator that rejects every historical defect and accepts every safe arrangement. The drafting contract inherits a bounded claim set plus the rules governing how those claims may be combined.

Sections in scope: SEC-02-2.

Note: drafting_authorized is still false; authorisation is that phase's call.

Carried forward:

- CF-P0-001 - enforced by MQ-001 and pair constraints PC-001..PC-004, PC-006; unqualified and misattributed forms are rejected
- SYN-001 - enforced by FS-001 pattern rules plus the same-sentence prohibition, which catches constructions no pattern lists
- 15 cm / 150 mm guard - enforced by DN-001, with the source-stated clay-zone 150 mm correctly exempted
