# SEC-02-2 ARCHITECTURE V2 PILOT #2 — ACCEPTED

**CLOSED / GO. Pilot ACCEPTED.** One generation call. Nothing repaired, nothing regenerated,
nothing retried. The first prose the project has produced.

Acceptance contract `architecture_v2_pilot_2_acceptance_contract_v1.json`, SHA256
`14c0130b54ab3a86922febc0c2af52388e3df6f80e163e87b590e9dd22a5c452`, 21 conditions, authored from
the phase brief and frozen before the first gate was run; re-hashed unamended after the outcome was
known. 0 unmet.

## Pre-generation gates

| Gate | Result |
|---|---|
| 1 frozen preflight | PASS, drift 0 (rethink inputs, implementation modules, Pilot #1 artifacts, remediation outputs, lexicon/gloss tables) |
| 2 Architecture V2 acceptance contract | unamended, `c9766e437bd00222574d1aeee5ede17ff74a51bf5ae0cea37e0f3f496f6ebccd` |
| 3 remediation acceptance contract | unamended, `117e9ea4b67e536d54bb0cd262e8860649f7415f600f66f4acc742ebca480560` |
| 4 canonical universe | loaded, recorded and rebuilt SHAs all `fafa8b4c…`, 16 claims exposed, 0 exclusions, 0 UNREALIZABLE exposed |
| 5 subset invariant | `required ⊆ available ⊆ realizable`, 16/16 claims, **0 violations** |
| 6 deterministic feasibility proof | PASS — 19 slots, 19 units, ACCEPT, empty histogram, topics 3/3, all 16 allocated claims stated, source keys valid, relations supported, 0 UNREALIZABLE selected |
| 7 static containment proof under M2 v2.1 | PASS — empty histogram, 0 false accepts, 0 false rejects, determinism byte-identical in-process and cross-process |
| 8 byte identity | PASS |

`claim_realization_contract_v2_1.json` re-hashed at
`6d0b3e3ff5619d23fe6896cbf97d0fa010c2ac732c5222d004e06c475fb19eb7`.

## The byte-identity gate

This is the gate Pilot #1 did not have, and it is the reason this phase exists.

| Universe | SHA256 |
|---|---|
| canonical artifact | `fafa8b4ceebe788d9765ac8f82463fde5b4c1253c38222fe178113874d37c000` |
| deterministic feasibility proof | `fafa8b4ceebe788d9765ac8f82463fde5b4c1253c38222fe178113874d37c000` |
| **model payload, extracted from the prompt string** | `fafa8b4ceebe788d9765ac8f82463fde5b4c1253c38222fe178113874d37c000` |

All equal. The comparison is on bytes, not on reconstructed objects: the universe is embedded in
the prompt as the canonical serialization the remediation contract specifies, delimited, and the
segment is then cut back out of the *finished* prompt string — the exact text handed to the model —
and hashed as UTF-8. Equal Python objects were never the thing in doubt in Pilot #1; equal bytes
were. 15 909 bytes, 6 465 prompt tokens.

The payload exposes only the canonical universe. No role set is derived in the pilot controller and
no claim-specific exception is appended.

## Gate-design correction, made before the generation

Pilot #1's `coverage_report` scores a condition by hunting its anchors in the paragraph and does
**not** add the frozen `condition_glosses` that stage E adds for exactly this case — an
English-source claim rendered in Turkish cannot retain an English anchor. It is a second
implementation of stage E's rule, stricter than the rule itself and structurally false-rejecting:
it scores 0.8696 on the deterministic feasibility plan that Draft Validator v1.2 accepts with an
empty histogram, missing on `SEC-02-2-P0-007` and `SEC-02-2-P0-008`.

That is Pilot #1's own defect class — one rule implemented twice, disagreeing — surviving in the
reporting layer, where Pilot #1 never exercised it because it was rejected before rendering. The
remediation's principle applies unchanged: ask the validator that owns the question instead of
reimplementing it. Condition and qualifier coverage are therefore read from the unchanged Draft
Validator v1.2's own failures, counted as the remediation's feasibility proof counts them.

Nothing was weakened. Stage E, stage L, `CONDITION_DROPPED`, `QUALIFIER_DROPPED` and
`SEMANTIC_SCOPE_MISMATCH` are untouched and still reject; the discarded measurement was not a
stricter check but a wrong one. `65_sec_02_2_architecture_v2_pilot_1.py` is byte-identical and
Pilot #1's figures are still computed and reported alongside, so the divergence stays visible.
The correction was made and recorded in `pre_generation_gate_v1.json` before the model was called.

## The generation

One call to `qwen3.6-35b-a3b-mlx`, temperature 0.0, seed 11, `finish_reason=stop`. Raw bytes
preserved before parsing at SHA256
`df99ad48d66d02150f2d1ff622a2ab362b323e9d9795f65a90c30296a08a9ec4`. 1 537 completion tokens.

**Zero prose fields.** The plan carried only declared field names and parsed against the frozen M1
schema without repair. 19 slots, 16 claims, 4 subsections, 16 paragraphs — the planner's own
structure, one claim per paragraph except where an obligation required a companion slot, and not
the feasibility proof's shape.

| Role | Slots |
|---|---|
| REQUIREMENT | 11 |
| CLAIM_STATEMENT | 5 |
| QUALIFIER_SCOPE | 2 |
| CONDITION | 1 |

**`SEC-02-2-C-005` was selected and accepted.** The claim that rejected Pilot #1 was offered as
REQUIREMENT, selected, rendered and validated. The contradiction that made it unplannable is not
merely absent; it is unconstructible.

## Plan validation and plan/universe consistency

Plan validation ACCEPT. Every selected pair proven against the canonical universe and against
M2 v2.1 independently: 0 claims outside the universe, 0 roles outside `available_roles`, 0 roles
outside `realizable_roles`, **0 UNREALIZABLE selections**, 0 mandatory obligations unmet, 0
required core claims missing. Required topics 3/3 at plan level.

## Render and post-render validation

Deterministic renderer under M2 v2.1. No LLM after semantic planning, no style rewrite, no
post-generation repair, 0 post-render model calls.

19 rendered units, render SHA256 `7451c9e58e20a04195100f87103e2045a17b3ff560fae888ad9767a2c7b09c17`.
Unchanged Draft Validator v1.2: **ACCEPT, failure histogram `{}`**, 0 rejected units, 0
zero-tolerance violations across `UNSUPPORTED_PROPOSITION`, `CLAIM_EXPANSION`, `NUMERIC_DRIFT`,
`UNIT_DRIFT`, `MODALITY_DRIFT`, `CONDITION_DROPPED`, `QUALIFIER_DROPPED`,
`SEMANTIC_SCOPE_MISMATCH`, `LANGUAGE_MISMATCH`, `CLAIM_DENYLISTED`, `UNKNOWN_CITATION`.

| Coverage | Result |
|---|---|
| required topics | 3/3 |
| citation coverage | 100% (19/19 material units), 0 unknown citations |
| language | 100%, 0 failures |
| condition preservation | 100%, 0 dropped of 19 obligations |
| qualifier preservation | 100%, 0 dropped of 2 obligations |

Determinism: 3 in-process renders and 1 fresh subprocess, all byte-identical at
`7451c9e5…`.

## The draft

Rendered with the frozen Book Citation Renderer v1, 12 citations, SHA256
`4994c5db7d0fc6615ae54150165371bcda4efe7526d3a3904b6c4e07547ecd07`, at
`data/book/drafting/sec_02_2/architecture_v2/pilot_2/rendered/sec_02_2_pilot_2_draft.md`.

Labelled **`PILOT_DRAFT_ACCEPTED`**. It is not a final manuscript, it has had no human technical
review and no style contract, and it is not released.

## Consequence to resolve deliberately

`tests/test_book_writing_pipeline.py::TestNoProse::test_no_prose_artifacts_were_produced` asserts
that no `.md` exists anywhere under `data/book/`. It now fails, because this phase was authorised
to produce exactly one labelled prose artifact and did. **The fixture was not touched.** It
encodes the state fact "rendered draft: NONE", which is no longer true; re-scoping it is a
deliberate contract decision for the next phase, not something to be done in the phase whose pass
depends on it. Three further failures are environmental — Qdrant is not running locally and this
phase made 0 Qdrant writes.

## Frozen integrity

17 frozen artifacts, 11 frozen modules and 4 lexicon/gloss tables byte-identical after the pilot.
0 validators weakened, 0 thresholds moved, 0 fixtures changed, 0 failure codes renamed or removed,
0 lexicon or gloss entries added, 0 frozen artifacts modified. The remediation's own
`realization_universe_v2_1.json` fixture was not rewritten — the static proof's output path was
redirected into the pilot's own directory, and the regenerated file is byte-identical to the frozen
one. Pilot #1 remains REJECTED and is not reinterpreted.

## Accounting

generation calls 1 · retrieval calls 0 · Qdrant writes 0 · corpus reads 0 · post-render model
calls 0 · automatic retries 0 · regenerations 0 · repairs 0.

Evidence: `data/book/drafting/sec_02_2/architecture_v2/pilot_2/`,
`data/book/manifests/sec_02_2_architecture_v2_pilot_2.json`.
