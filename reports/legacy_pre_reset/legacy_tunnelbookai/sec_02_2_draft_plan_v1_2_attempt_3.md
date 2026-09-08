# SEC-02-2 DRAFT PLAN V1.2 + ATTEMPT #3 AUTHORISATION

**SEC-02-2 DRAFT PLAN V1.2 + ATTEMPT #3 AUTHORISATION — CLOSED / GO; SEC-02-2 PILOT ATTEMPT #3 — REJECTED**

Attempt #3: REJECT. Generation attempts this phase: 1. Retrieval calls: 0. Qdrant writes: 0. Corpus reads: 0.

## Draft plan v1.2

Attempt #2 reproduced canonical_claim verbatim for 14 of 16 single-claim units. Reproduction cannot reach a meaning the canonical sentence does not contain, and no unit was allocated for the part that has to be composed.

**Rule.** A claim whose non-empty qualifier has at least one content anchor absent from its own canonical sentence, or which carries a registered qualifier-semantics entry that its canonical sentence does not satisfy, is allocated two bound unit slots. Every other allocated claim keeps one.

The rule reads the frozen allowlist and the frozen qualifier-semantics registry. It names no claim, and it selects nothing by hand. Applied to the 16 allocated claims it selects ['SEC-02-2-C-002', 'SEC-02-2-C-009'] — 2 two-slot claims, 14 one-slot, 18 slots in total.

| Claim | Subsection | Slots | Selected by |
|---|---|---|---|
| `SEC-02-2-C-001` | A | 1 | — |
| `SEC-02-2-C-002` | A | 2 | anchors absent from canonical |
| `SEC-02-2-R001` | B | 1 | — |
| `SEC-02-2-P0-001` | B | 1 | — |
| `SEC-02-2-P0-006` | B | 1 | — |
| `SEC-02-2-P0-005` | B | 1 | — |
| `SEC-02-2-P0-004` | B | 1 | — |
| `SEC-02-2-P0-007` | C | 1 | — |
| `SEC-02-2-P0-008` | C | 1 | — |
| `SEC-02-2-C-003` | C | 1 | — |
| `SEC-02-2-C-004` | C | 1 | — |
| `SEC-02-2-C-005` | C | 1 | — |
| `SEC-02-2-C-007` | C | 1 | — |
| `SEC-02-2-C-006` | D | 1 | — |
| `SEC-02-2-C-012` | D | 1 | — |
| `SEC-02-2-C-009` | D | 2 | anchors absent from canonical; registered DQS-C009-001 |

## Licensed vocabulary exposure

These are the Turkish words the validator's containment rule already accepts for this claim. They are shown, not added. A rendering that stays inside them passes stage C; one that reaches outside does not.

- `SEC-02-2-P0-007` — 24 words, byte-identical to the frozen glosses: True
- `SEC-02-2-P0-008` — 20 words, byte-identical to the frozen glosses: True

Forbidden additions absent: {'kayaç': True, 'spesifik': True}

## Pre-generation gate

| Condition | Result |
|---|---|
| plan v1 1 unchanged | True |
| plan v1 2 is additive | True |
| plan v1 2 allocation is general | True |
| allocation selects c002 and c009 | True |
| every selected claim has two bound slots | True |
| every other claim has one slot | True |
| bound slots share claim and sources | True |
| c002 remains one claim | True |
| licensed vocabulary byte identical | True |
| licensed vocabulary adds nothing | True |
| translation glosses unchanged | True |
| qualifier registry consistent | True |
| all gate suites pass | True |
| fixture universes all pass | True |
| false accepts zero | True |
| false rejects zero | True |
| code mismatches zero | True |
| no universe newly fails under v1 2 | True |
| frozen integrity holds | True |
| validator v1 unchanged | True |
| validator v1 1 unchanged | True |
| historical attempts unchanged | True |
| no code dropped by v1 2 | True |
| no stage dropped by v1 2 | True |
| retrieval calls zero | True |
| qdrant writes zero | True |
| corpus reads zero | True |

**GO**

Suites: 381 tests, passed. Fixture universes: 156 cases, false accepts 0, false rejects 0.

## Attempt #3

| | |
|---|---|
| Model | `qwen3.6-35b-a3b-mlx` |
| Temperature | 0.0 |
| Seed | 11 |
| Draft id | `SEC-02-2-PILOT-V1-2` |
| Raw preserved before parsing | `data/book/drafting/sec_02_2/attempt_3/raw/sec_02_2_draft_raw_attempt_3.json` |
| Units | 22 |
| Material units | 18 |
| Validator | `tunnelbook-section-draft-validator-v1.2` |
| Verdict | **REJECT** |

| Unit | Claims | Codes |
|---|---|---|
| `U-A-P01-S03` | ['SEC-02-2-C-002'] | ['UNSUPPORTED_PROPOSITION'] |
| `U-C-P01-S03` | ['SEC-02-2-P0-008'] | ['UNSUPPORTED_PROPOSITION'] |

| Compliance | |
|---|---|
| Language | 100% |
| Conditions | 100% |
| Qualifiers (anchor) | 100% |
| Qualifier semantics (stage L) | satisfied (2 bound units) |
| Required topics | 3 / 3 |
| Citation coverage | 100% |

### What plan v1.2 changed

| Claim | Planned slots | Material units written |
|---|---|---|
| `SEC-02-2-C-002` | 2 | 2 |
| `SEC-02-2-C-009` | 2 | 2 |

| Attempt-#2 cause | Closed by plan v1.2 |
|---|---|
| SEC-02-2-C-002 qualifier (QUALIFIER_DROPPED, stages E and K) | yes |
| SEC-02-2-C-009 qualifier semantics (QUALIFIER_DROPPED, stage L) | yes |
| language (LANGUAGE_MISMATCH, stage J) | yes |
| conditions (CONDITION_DROPPED, stage E) | yes |

### Why attempt #3 was rejected

- `U-A-P01-S03` (SEC-02-2-C-002) — UNSUPPORTED_PROPOSITION at C_support on `['ifade', 'sağlar']`. Licensed alternative in the same sentence: True.
- `U-C-P01-S03` (SEC-02-2-P0-008) — UNSUPPORTED_PROPOSITION at C_support on `['durumlarında', 'örneğin']`. Licensed alternative in the same sentence: True.

**Cause class:** `WRITER_VOCABULARY_CHOICE - recurrence`. Every unlicensed word was written beside a licensed content word from the same claim's own pool, which is attempt #2's signature and not a new one. The remediation analysis v2 specified was implemented exactly and the failure class it targeted recurred on different words.

Not repaired, not patched, not translated, no unit deleted, not regenerated. There is no attempt #4.

### Attempt gate

| Condition | Result |
|---|---|
| draft ir schema valid | True |
| every material unit validates | False |
| every material unit claim bound | True |
| every used claim allowlisted | True |
| no denylisted claim used | True |
| no unsupported proposition | False |
| no claim expansion | True |
| no numeric drift | True |
| no unit drift | True |
| no modality drift | True |
| no dropped condition | True |
| no dropped qualifier | True |
| cf p0 001 passes | True |
| syn 001 passes | True |
| derived numeric guard passes | True |
| required topics 3 of 3 | True |
| material citation coverage 100 | True |
| citation resolution 100 | True |
| unknown citations zero | NOT_EVALUATED |
| packet eid leaks zero | NOT_EVALUATED |
| internal claim id leaks zero | NOT_EVALUATED |
| bibliography registry backed | NOT_EVALUATED |
| rendering deterministic | NOT_EVALUATED |
| composition safe coverage | True |
| no language mismatch | True |
| no language ambiguity | True |
| no semantic scope mismatch | True |
| language compliance 100 | True |
| condition preservation 100 | True |
| qualifier preservation 100 | True |
| semantic constraints satisfied | True |
| qualifier semantics all satisfied | True |
| no stage l failure | True |

## Phase accounting

| | |
|---|---|
| Generation attempts | 1 |
| Retrieval calls | 0 |
| Qdrant writes | 0 |
| Corpus reads | 0 |
| Automatic retries | 0 |
| Validators weakened | none |
| Frozen artifacts modified | none |

**Next phase.** SEC-02-2 DRAFTING APPROACH RETHINK V1 — plan v1.2 closed every cause attempt #2 failed on and the pilot was still rejected, on the one class analysis v2 had already remediated. The next question is whether claim-bound lexical containment and fluent Turkish prose are reachable together under this drafting approach, not which instruction to add fourth.

