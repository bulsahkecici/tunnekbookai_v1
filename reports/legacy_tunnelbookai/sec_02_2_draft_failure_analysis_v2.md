# SEC-02-2 Draft Failure Analysis v2

`tunnelbook-sec-02-2-draft-failure-analysis-v2`


## Executive Decision

Both attempt-#2 failures are root-caused against the artifacts, both validator verdicts are correct, and both remediations are the same kind of change: a new draft plan. Nothing was generated, nothing was rendered, no validator was touched.

**SEC-02-2 DRAFT FAILURE ANALYSIS V2 — CLOSED / GO**


## What Attempt #2 Actually Did

| | |
|---|---|
| Material units | 16 |
| Single-claim units | 16 |
| Byte-identical copies of the canonical claim | 14 (88%) |
| Composed units | 2 — ['U-C-P01-S01', 'U-C-P01-S02'] |
| Units per claim | exactly one, for every allocated claim |
| Qualifiers scored preserved by stage E | 1/2 |
| Qualifiers whose meaning actually reached the prose | 0/2 |

The census is the finding the rest of the analysis rests on. Every unit whose claim was already Turkish is the claim's own sentence, copied. The only two composed units are the two English claims, which could not be copied. This writer composes when copying is impossible and not otherwise — and a qualifier delivered beside a copy-ready sentence is, to a copying writer, invisible.


## A — U-A-P01-S02 / SEC-02-2-C-002, QUALIFIER_DROPPED

**Root cause class:** `CLAIM_QUALIFIER_REPRESENTATION_MISMATCH` (secondary: `PLAN_UNIT_ALLOCATION_DEFECT`)

SEC-02-2-C-002's mandatory semantic content is split across two fields that share no vocabulary: a canonical_claim that is already a complete, copy-ready Turkish sentence, and a qualifier string whose meaning that sentence does not contain. The writer reproduced the canonical sentence byte-for-byte, as it did for 14 of 16 single-claim units - every one whose claim was already Turkish. A mandatory-qualifier flag delivered beside a copy-ready sentence cannot change that output, because the compliant output is unreachable by reproduction and reachable only by composing past the canonical text. Nothing in the plan or the payload allocates a unit for the composed part, and the frozen prompt's one-proposition-per-sentence rule pushes against putting it in the claim's own sentence.

Against the candidates the phase brief named:

| Candidate | Verdict | Evidence |
|---|---|---|
| a. canonical-claim / qualifier representation mismatch | **supported, primary** | the unit is byte-identical to `canonical_claim`; the qualifier shares no vocabulary with it |
| b. generation payload omission | refuted | the rebuilt payload carries the qualifier verbatim, `qualifiers_are_mandatory: true`, and DSC-C002-001 with its `required_meaning` and `required_action` |
| c. prompt-compliance failure | contributing, not primary | prompt v1.1 does say qualifiers are mandatory — and also says one proposition per sentence, with no unit allocated for the second one |
| d. validator semantic-boundary design issue | refuted | two different compliant shapes validate under the same rules, unchanged |
| e. plan allocates no unit slot for the qualifier | **supported** | the plan allocates claims to subsections only; the writer resolved that to one unit per claim |

**Validator verdict: correct.** The paragraph states that Tablo-351-5 gives minimum strength values and never says the table is an acceptance criterion. A reader can take it as the table imposing the requirement, which is the meaning SEC-02-2-C-001 owns. Stage E and stage K fired independently on the same absence, and the probes show two compliant shapes the same rules accept, so the boundary is not drawn too tightly.

### Probes

Validator inputs, not draft prose.

| Shape | Result |
|---|---|
| one unit, canonical claim copied verbatim | QUALIFIER_DROPPED@E_conditions, QUALIFIER_DROPPED@K_semantic |
| one unit carrying the acceptance-table identity and the numeric criteria | ACCEPT |
| identity/scope unit + numeric-criteria unit, both declaring SEC-02-2-C-002 | ACCEPT |
| identity unit stripped of SEC-02-2-C-002's own conditions | CONDITION_DROPPED@E_conditions |

### Smallest safe remediation

Plan change only. In a draft plan v1.2, allocate SEC-02-2-C-002 two bound unit slots in subsection A - (1) acceptance-table identity and scope, carrying the qualifier's meaning and the claim's own conditions, (2) the numeric acceptance criteria - both declaring SEC-02-2-C-002, both citing SRC-DOC000087-ea64db4f1a7f, both INDEPENDENT. Slot 1 has no canonical sentence to copy, so copying stops being an available strategy. No validator, threshold, failure code, claim, allowlist, gloss, prompt or frozen contract changes.

Generality: generic mechanism, SEC-02-2-specific instance. The mechanism - a claim carrying a non-empty qualifier whose anchors are absent from its canonical sentence gets an explicit qualifier unit slot - is general and applies to SEC-02-2-C-009 in the same section. Only the allocation itself is section-local.


## B — U-C-P01-S02 / SEC-02-2-P0-008, UNSUPPORTED_PROPOSITION

**Root cause class:** `WRITER_VOCABULARY_CHOICE`

The writer chose two words the claim's frozen glosses do not license when licensed words for the same meaning were available and, in one case, already in the same sentence. 'kayaç' was written three words after the licensed 'kaya'; 'spesifik' duplicates the 'In some' condition that 'bazı' and the licensed 'belirli' already carry. Three natural Turkish renderings pass support containment against the current pool unchanged. The gloss set is not too narrow, and the containment rule did what it exists to do.

| Candidate | Verdict |
|---|---|
| a. unsupported semantic additions | partially — `spesifik` restates the `In some` condition the licensed `bazı`/`belirli` already carry |
| b. faithful paraphrase blocked by lexical containment | refuted — three faithful renderings pass against the pool unchanged |
| c. avoidable writer vocabulary choice | **supported, primary** |
| d. broader cross-lingual licensing defect | refuted — the defect is that the writer is never shown the vocabulary, not that the vocabulary is missing |

| Word | Licensed today |
|---|---|
| `kayaç` | no |
| `spesifik` | no |
| `kaya` | yes |
| `bazı` | yes |
| `belirli` | yes |

The rejected sentence contains `kaya` and `kayaç` three words apart. The licensed form was in the writer's hand as it wrote the unlicensed one — which is what makes this a choice rather than a gap. `kayaç` misses `kaya` only because prefix agreement needs five characters and `kaya` has four; that is a property of the containment rule, not a reason to widen a lexicon, because the faithful renderings pass without it.

Licensed alternatives that existed: `['P0008_bazi_belirli', 'P0008_belirli', 'P0008_kaya_for_kayac']`.

**Validator verdict: correct.** Containment rejects content words no declared claim licenses. Both words are such words, and the rejection cost nothing that a faithful rendering needed, since faithful renderings validate. Loosening the rule to admit them would admit every near-synonym a writer reaches for, which is the failure mode the stage exists to prevent.

### Smallest safe remediation

Plan change only, and it is not a loosening. Expose the already-frozen translation_glosses for each English-source claim to the writer in the payload, as the vocabulary its rendering may use, alongside the approved condition renderings the payload already carries. This states what the validator already accepts; it does not change what it accepts. The paraphrase lexicon, the glosses and the containment rule are untouched.

Generality: generic. Every cross-lingual claim in every future section has the same gap: the writer is told to translate and is not told which vocabulary survives containment.


## Should SEC-02-2-C-002 Be Two Components?

**one frozen claim, two bound downstream units.** The frozen claim is not altered by this phase.

The claim stays one claim. It is frozen, it is one source's statement, and the probes show a single unit carrying both components validates, so nothing forces a split at the claim level. What the evidence does force is a split downstream: the shape that failed twice is the shape where one unit must both reproduce the canonical sentence and add a meaning that sentence does not contain. DSC-C002-001's required_action already describes the two-component form, and stage K already scopes the required marker to the paragraph precisely because the qualifier cannot live inside the claim's own sentence. The plan is the only artifact that never learned this.

If the downstream split is taken, four things bind:

- both units declare SEC-02-2-C-002 and cite SRC-DOC000087-ea64db4f1a7f
- both units are INDEPENDENT; neither may imply C-002 proves C-001
- the identity unit carries C-002's own conditions, or stage E rejects it
- the identity unit names Tablo-351-5 without an attribution marker, or stage K rejects it as SEMANTIC_SCOPE_MISMATCH


## Regression Cases Required Before Any Attempt #3

- RC-A1 attempt #2's shape must still be rejected, QUALIFIER_DROPPED at E and K
- RC-A2 the two-bound-unit shape must validate
- RC-A3 the single-unit combined shape must validate
- RC-A4 an identity unit stripped of C-002's conditions must fail CONDITION_DROPPED
- RC-A5 the forbidden attribution shape must still fail SEMANTIC_SCOPE_MISMATCH
- RC-A6 DSC-C002-001's marker set and paragraph scope must be unchanged
- RC-B1 attempt #2's sentence must still fail on exactly ['kayaç', 'spesifik']
- RC-B2 the three licensed renderings must show zero unlicensed content words
- RC-B3 'kayaç' must stay unlicensed and 'kaya' licensed - a widening tripwire
- RC-B4 SEC-02-2-P0-008's frozen glosses must be byte-identical to today's


## Deferred Finding

**DF-01.** Stage E scores a qualifier preserved when half its anchors appear in the paragraph. A qualifier that reuses its claim's own vocabulary therefore passes on a verbatim copy that never states it - SEC-02-2-C-009 did exactly this in attempt #2. Direction: tightening, not loosening. Not actioned here — Out of scope: this phase does not modify validators, and a tightening deserves its own fixtures and its own gate.


## Recommendation

**plan change (claim-to-unit allocation, plus payload vocabulary exposure) - one new artifact, draft plan v1.2.**

Neither half changes what any validator accepts. The allocation changes what the writer is asked to produce; the vocabulary exposure states glosses that are already frozen and already enforced. No threshold, marker set, failure code, gloss, lexicon entry or claim is edited.

Attempt #3 is justified, and is not authorised here. It becomes permissible only when:

- draft plan v1.2 exists and allocates SEC-02-2-C-002 two bound unit slots
- draft plan v1.2 exposes the frozen translation glosses for English claims
- RC-A1..A6 and RC-B1..B4 all pass before any generation call
- exactly one attempt, authorised by its own phase, no automatic retry


## Phase Accounting

| | |
|---|---|
| Generation attempts | 0 |
| Retrieval calls | 0 |
| Qdrant writes | 0 |
| Corpus reads | 0 |
| Validators weakened | none |
| Frozen artifacts modified | none |
| Prose rendered | none |

