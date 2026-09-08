# SEC-02-2 DRAFTING APPROACH RETHINK V1

**CLOSED / GO.** Architecture A rejected on three-attempt evidence. Architecture D selected. No generation, no attempt #4.


## The census

Every material unit of every preserved attempt, classified by how it was produced and counted for containment separately.

| Attempt | Reproduced units | Unlicensed / content tokens | Composed units | Unlicensed / content tokens | Composed rate |
|---|---|---|---|---|---|
| attempt_1 | 16 | 0 / 184 | 0 | 0 / 0 | None |
| attempt_2 | 14 | 0 / 166 | 2 | 2 / 26 | 0.0769 |
| attempt_3 | 14 | 0 / 166 | 4 | 4 / 53 | 0.0755 |
| **total** | **44** | **0 / 516** | **6** | **6 / 79** | **0.0759** |

Containment failure is a property of the composed mode, not of the writer's diligence in a given attempt. Three attempts produced 516 content tokens by reproduction with 0 unlicensed, and 79 by composition with 6 unlicensed. Plan v1.2 closed every fidelity cause and moved the composed-mode rate from 0.0769 to 0.0755. Because a qualifier whose vocabulary its canonical sentence lacks is unreachable by reproduction, each fidelity fix converts reproduced units into composed ones: the composed-unit count went [0, 2, 4]. Fidelity and containment are not two independent defects being fixed in turn; under this architecture one is paid for with the other.

Projected section-level outcome at the measured rate:

| Composed units in a section | P(section clean) |
|---|---|
| 2 | 0.125037 |
| 4 | 0.015634 |
| 8 | 0.000244 |
| 16 | 0.0 |
| 32 | 0.0 |


## What attempts #1–#3 prove

**attempt 1.** Reproduction alone satisfies containment and cannot satisfy fidelity. 16 material units, all reproduced, 0 unlicensed content tokens, and rejected for a dropped qualifier and a dropped condition — the two things reproduction cannot supply.

**attempt 2.** Composition satisfies fidelity and breaks containment. The two units that could not be copied — the English-source claims — were the only composed ones, and one of them carried the section's first UNSUPPORTED_PROPOSITION.

**attempt 3.** Instructions govern fidelity and do not govern containment. Every attempt-#2 cause closed, qualifier realisation 0/2 to 2/2, and the composed-mode rate stayed where it was. The remediation worked exactly as designed and the pilot was rejected anyway.

**the series.** The three attempts are not three failures of one kind. They are a demonstration that the architecture has two requirements it can satisfy one at a time. Attempt #1 bought containment with fidelity, attempt #2 bought fidelity with containment, attempt #3 bought more fidelity with more containment exposure at an unchanged rate.


## Refined attempt #3 root cause

**Status: INSUFFICIENT.**

The previous inference: `licensed_alternative_was_in_hand = true` was taken to show the writer made an avoidable choice, and therefore that the unlicensed word was semantically harmless and the defect was the writer's diligence.

- It conflates the existence of a licensed string with semantic equivalence between it and the unlicensed one. `durumlarında` and the exempt `durumlarda` are one morpheme apart and mean the same thing. `ifade eder` and the qualifier's `-dir` are a modality apart and do not. The same flag was attached to both, so the flag distinguishes nothing.
- It reasons from availability to reachability. The pool was exposed to the writer verbatim, as analysis v2 specified, and nothing in free-form generation makes an exposed vocabulary a constraint on the next token. Showing a writer the licensed words does not remove the unlicensed ones from its output space.
- It made a testable prediction — better instructions would close the class — and plan v1.2 tested it. The remediation was implemented exactly, every fidelity cause closed, and the composed-mode containment rate moved from 0.0769 to 0.0755. The prediction failed.
- For one of the four words it is not even true. `sağlar` renders the relation SEC-02-2-C-002's own canonical states as `gives`, and that claim's pool contains no Turkish lexical verb for it — only the copula. The licensed options were to restructure the sentence around `-dir` or to leave the pool. The flag records neither, because it asks whether some licensed token existed and not whether a licensed way to say this thing existed.
- It is a description of the symptom. Every containment failure is by definition a word the writer chose; naming that as the cause cannot be wrong and cannot be acted on.

**Refined cause class: ARCHITECTURAL — UNCONSTRAINED_SURFACE_REALIZATION.**

Claim-bound lexical containment is a closed-set membership test applied to the output of an open-set generator. The licensed pool is a filter downstream of generation, never a constraint on it, so the containment outcome of any composed sentence is a sample from the writer's surface-form distribution rather than a property the architecture establishes. The three attempts measure that sample: 6 unlicensed tokens in 79 composed content tokens, against 0 in 516 reproduced ones. Reproduction succeeds because it is not sampling — the tokens come from the pool by construction. That is the whole difference between the two modes, and it is a difference in architecture.

| Cause | Weight | Accounts for |
|---|---|---|
| RC-01 GENERATOR_UNCONSTRAINED | primary | all 6 unlicensed tokens across attempts #2 and #3 |
| RC-02 CONTAINMENT_BOUNDARY_MORPHOLOGY | contributory | `durumlarında` specifically; 1 of 6 observed tokens |
| RC-03 STRUCTURAL_TENSION_FIDELITY_VS_CONTAINMENT | aggravating | the trend across attempts |

**CF-01.** All three attempts used the same writer: qwen3.6-35b-a3b-mlx, temperature 0.0, seed 11. The three attempts varied the instructions, never the writer. Reading 4 of the phase brief — the approach is sound and the writer is not — is UNTESTED by this evidence, not refuted. Nothing here shows a stronger writer would fail. The architectural argument does not require reading 4 to be false. A better writer lowers the per-token rate; it does not make the rate zero, and the section-level outcome compounds over every composed token. Nor does a better writer see the boundary: the `durumlarda` / `durumlarında` line is invisible to any writer, however strong, because it is an artifact of which forms were enumerated. Selecting on 'a better model might be enough' is an unbounded bet whose cost is one generation per test.


## Attempt #3 word classification

Categories: 1 grammatical/discourse surface · 2 semantic paraphrase · 3 relationship-bearing · 4 proposition-changing.

| Word | Categories | Primary | Category 4 excluded | Basis |
|---|---|---|---|---|
| `ifade` | 2, 3 | 2 | **no** | A paraphrase of a licensed copula, and it bears the relation it paraphrases. It is not grammar: `eder` is exempt as a function word and `ifade` is the lexical half that carries the meaning, which is why only one of the pair was flagged. |
| `sağlar` | 3, 2 | 3 | yes | A light verb by form, a relation by function: it asserts that the table stands in a providing relation to the criteria. That the relation happens to be the licensed one here is a fact about this sentence, not about the word. |
| `durumlarında` | 1, 2 | 1 | yes | Discourse surface vocabulary that the containment boundary already treats as such in three of its four forms. It also restates the licensed `koşullarında` three words later, which makes it a paraphrase as well as grammar. |
| `örneğin` | 1, 3 | 1 | yes | A discourse marker, and the closest analogue already exempt: `gibi` — the word attempt #2 used for this same relation in this same claim — is in the function lexicon. It does bear a relation, which is why category 3 is listed, but the relation is the claim's own. |

**`ifade`** — 'expression'; the construction written was `ifade eder`, 'expresses'. Cannot be excluded. SEC-02-2-C-002's qualifier states the identity flatly — 'kabul kriteridir', it *is* the acceptance criterion. `ifade eder` substitutes a metalinguistic predicate for that copula: the table *expresses* the criterion. DSC-C002-001 exists precisely because what this table is, versus what it is taken to establish, is the distinction the claim is fragile on. A modality shift on that exact copula is the one place in the sentence where it could matter.

**`sağlar`** — 'provides/gives'; third-person present of sağlamak. Excluded in this slot only. The claim's own English canonical uses `gives` for the same relation, so the proposition asserted is the source's. The exclusion does not travel: `sağlamak` also means 'to ensure/to satisfy', and '... gerekli dayanımı sağlar' is a performance assertion no source states. Same surface form, different proposition, decided by the slot it fills.

**`durumlarında`** — 'in the cases/situations of'; durum + plural + possessive + locative. Excluded, and demonstrably so. The function lexicon already exempts three inflections of the same lexeme. The fourth was rejected because the exemption test is exact string membership while the licensing test is five-character prefix agreement — two different matching regimes over an agglutinative language. Had the writer produced `durumlarda`, one morpheme away and equally grammatical, stage C would have said nothing.

**`örneğin`** — 'for example'. Excluded. It marks an exemplification relation, and that relation is stated by the source: the claim's English canonical reads 'such as crushed or squeezing rock', and both `such` and `as` are in the pool. The Turkish marker asserts nothing the English one did not.

The four words are not one class. Two are discourse surface vocabulary the containment boundary arguably never meant to catch; one bears a relation that happens to be licensed here and would not be elsewhere; one shifts the modality of the exact copula its claim is fragile on. Attempt #3's cause record described them collectively as connectives and light verbs carrying no technical content. That is true of two of them.

No single remedy addresses the set. A lexicon entry that admits `durumlarında` correctly admits `sağlar` incorrectly, because the exemption mechanism cannot see which slot a word fills.


## Current architecture verdict

**NOT AN APPROPRIATE SCALABLE DRAFTING ARCHITECTURE.**

- its containment guarantee is a filter, so the outcome is sampled rather than established
- the sampled rate does not respond to the only lever it offers
- its two requirements trade against each other, and the trade worsens as fidelity improves
- the section-level outcome compounds over composed tokens, so it degrades as sections grow

What would have refuted this: a composed-mode containment rate comparable to the reproduced mode's, or a rate that fell materially between attempt #2 and attempt #3. Neither is observed.


## A / B / C / D

| | Containment guarantee | Weakens stage C | Scaling | Verdict |
|---|---|---|---|---|
| **A** current — free-form Turkish prose + strict claim-bound lexical containment | none; filter after the fact | no | P(clean section) ≈ 0.015634 at 4 composed units, 0.0 at 16 | REJECTED — not scalable; the failure rate is invariant under the only lever the architecture offers |
| **B** expanded function / paraphrase lexicon | none; the same filter with a larger accept set | **yes** | unbounded. Six new words after two attempts with no saturation evidence, and Turkish morphology multiplies every lemma: the exemption list covers 3 of 9 tested forms of the single lexeme `durum`, in a list of 124 entries | REJECTED — explicitly weakens the validator, and cannot be bounded |
| **C** controlled claim-specific realization templates | yes, within a template; none for text outside one | no | authoring cost is claims × rhetorical roles, per section. SEC-02-2 alone allowlists 27 claims. Templates are section-local and do not compose. | VIABLE BUT SUBSUMED — this is D's renderer with a hand-written, non-compositional grammar and no separation of concerns |
| **D** structured semantic plan (LLM) + deterministic surface renderer | by construction. The renderer's output alphabet is the licensed pool plus a frozen closed grammatical scaffold, which is a static property provable over all plans | no | realization data is per claim and reusable across sections; the renderer and the morphology are written once | SELECTED |

**Why lexicon widening is rejected.** This option works by making stage C more permissive. `sağlar` and `ifade` are relationship-bearing; a global exemption for them makes stage C accept 'püskürtme beton gerekli dayanımı sağlar' — an unsupported performance assertion — in any unit of any section, because the exemption mechanism cannot see which slot a word fills. That is a loosening in the direction the stage exists to block.


## Decision

**ADR-001 — SEC-02-2 drafting architecture v2 — structured plan plus deterministic renderer. ACCEPTED.**

Adopt architecture D. The LLM emits a structured semantic plan and no prose. A deterministic renderer produces every surface form.

Decided on:

- *primary evidence* — Reproduced units: 516 content tokens, 0 unlicensed, across all three attempts. Composed units: 79 content tokens, 6 unlicensed. The containment outcome is determined by production mode, and reproduction's guarantee comes from the tokens being drawn from the pool by construction rather than sampled and filtered.
- *invariance evidence* — The composed-mode rate did not respond to the one lever architecture A offers. Plan v1.2 was implemented exactly as analysis v2 specified and the rate went 0.0769 to 0.0755.
- *tension evidence* — Composed units rose [0, 2, 4] across the attempts, because fidelity fixes are only reachable by composition. Under A, fidelity is bought with containment exposure.
- *volume evidence* — 44 of 50 material units are already produced by verbatim reproduction. Free generation supplies a minority of the volume and all of the risk.

Not decided on:

- Not selected because a phase brief proposed it. The brief lists four readings and requires the evidence to choose; the census chooses, and it would have selected A had the composed and reproduced rates been comparable.
- Not selected on a claim that the writer is inadequate. CF-01 records that all three attempts used one writer and that reading 4 is untested.
- Not selected to make validation easier. Stage C is unchanged and every rejection code is retained; the renderer must pass the validator that rejected all three attempts.


## Responsibility split

| LLM | Deterministic renderer |
|---|---|
| which claims to draft and which to omit | factual surface realization from licensed stems |
| order of claims within a paragraph and of paragraphs within a subsection | numeric rendering with the unit its source uses |
| rhetorical role assignment per slot — identity, requirement, qualifier, condition, exemplification, scope limitation | qualifier realization against registered constructions |
| whether a qualifier gets its own unit or rides with its claim | condition realization against approved renderings |
| paragraph and subsection grouping, and topic coverage | modality — every requirement verb comes from a frozen scaffold |
|  | citation binding through Book Citation Rendering Contract v1 |
|  | Turkish morphology |

The LLM emits no surface word. It is explicitly not responsible for: any surface word, numeric rendering, unit symbols, qualifier wording, condition wording, modality, citation strings, morphology.


## Migration scope

Unchanged and frozen:

- corpus, normalized documents, chunks, embeddings
- Retriever v1, Context v1, Prompt v5, Output Contract v1.1
- Production Grounded Generator v1, Evidence Note Contract v1, Book Pipeline v1
- Extractor v1.1, P0 artifacts, SEC-02-2 readiness and composition-safety artifacts
- composition-safe allowlist, composition denylist, pair constraints
- function lexicon, paraphrase lexicon, translation glosses
- Section Drafting Contract v1, Book Citation Rendering Contract v1
- Draft Validator v1, v1.1, v1.2 — every stage, every rejection code
- draft plans v1, v1.1, v1.2
- preserved attempts #1, #2, #3 and every audit and rejection record
- DQS-C009-001 and the qualifier semantics registry

New in the implementation phase:

| | Artifact | Kind | Purpose |
|---|---|---|---|
| M1 | `draft_plan_ir_contract_v2` | contract | the symbolic structure the LLM emits: an ordered list of typed slots — claim id, rhetorical role, which conditions and qualifiers to realise, citation intent, paragraph and subsection grouping |
| M2 | `claim_realization_contract_v2` | contract | per-claim frozen realization data: canonical form, role-to-frame bindings, approved condition renderings, registered qualifier constructions, numeric and unit rendering, citation binding |
| M3 | `turkish_morphology_v2` | module | deterministic suffixation — vowel harmony, buffer consonants, k/ğ and p/b mutation — so the renderer can inflect licensed stems instead of selecting inflected surface forms |
| M4 | `deterministic_surface_renderer_v2` | module | plan IR to Turkish prose. A pure function. No model call. |
| M5 | `static_containment_proof_v2` | test harness | enumerate every claim by every rhetorical role the contract admits, render each, and assert zero failures from validator v1.2 stages A through L — without generating anything |

Sequence:

1. M1 and M2 authored and frozen, with fixtures, before any renderer code
1. M3 with morphology unit tests
1. M4 against M1/M2, no model in the loop
1. M5 as the gate: static containment proof over the full enumeration
1. regression: the preserved attempts' accepted units must remain acceptable, and every rejected unit must remain rejected under the unchanged validator
1. only then may a later phase authorise ARCHITECTURE V2 PILOT #1 on its own evidence


## Deferred findings

**DF-02.** Function-word exemption is exact string membership over an agglutinative language; `durumlarda` is exempt and `durumlarında` is not. Direction: a morphology-aware exemption test would place the boundary where it was meant to be, without admitting relationship-bearing words. Not actioned — this phase widens nothing, and under architecture D the renderer inflects licensed stems rather than selecting surface forms, so the defect stops being reachable. It remains a real defect in the validator and is recorded, not fixed.

**DF-03.** The licensed pool is built from every field of the claim record and so contains English record metadata; it licenses `specific` and not `spesifik` for a Turkish section. Direction: pool construction could be restricted to claim-bearing fields. Not actioned — narrowing the pool is a tightening, not a loosening, but it is still a validator change and this phase makes none.

**CF-01.** All three attempts used one writer at temperature 0.0, seed 11. Reading 4 of the phase brief is untested, not refuted. Direction: if architecture D's build ever stalls, a writer comparison under architecture A is the cheapest remaining experiment. Not actioned — it costs a generation, and the decision does not depend on it.


## Phase accounting

| | |
|---|---|
| attempt 4 authorised | False |
| corpus reads | 0 |
| frozen artifacts modified | none |
| generation attempts | 0 |
| lexicons widened | none |
| prose rendered | 0 |
| qdrant writes | 0 |
| retrieval calls | 0 |
| validators weakened | none |

