# ARCHITECTURE V2 PLANNER OPTION UNIVERSE REMEDIATION V1

**CLOSED / GO** — remediation only. 0 generation calls, 0 renders released, 0 retrieval calls, 0 Qdrant writes, 0 corpus reads. ARCHITECTURE V2 PILOT #2 is not authorised by this phase and was not run.

## Frozen preflight

- rethink inputs 15, drift 0
- implementation artifacts 4, drift 0
- Pilot #1 artifacts drift 0
- Architecture V2 acceptance contract unamended: True
- **total drift 0**

## Acceptance contract

`data/book/drafting/sec_02_2/architecture_v2/remediation_v1/contracts/planner_universe_remediation_acceptance_contract_v1.json`

SHA256 `117e9ea4b67e536d54bb0cd262e8860649f7415f600f66f4acc742ebca480560`, 20 conditions. Authored from the phase brief and frozen before the feasibility proof, the static proof, the negative fixtures and this gate were run. Unmet: none.

## RM-3 — Claim Realization Contract v2.1

M2 v2 decided whether a frozen claim field could be emitted as Turkish by looking for `çğıöşü`. That is a character heuristic, not a language test, and it is what marked `ilk tabaka`, `takip eden tabakalar` and `ilave tabakalar` as not Turkish.

v2.1 reads language from frozen data instead. A claim's conditions and qualifiers are excerpts of the same source sentence as its canonical claim, so they carry the claim's language; and the claim's language is already recorded, because a claim whose source is English is exactly a claim for which `translation_glosses` and `condition_glosses` were authored. The mapping is not taken on trust: every canonical sentence is put to the frozen Draft Language Validator — stage J, which already governs every rendered unit — and a disagreement fails the build.

Corroboration: 27 claims checked, mismatches none. 60 distinct frozen field strings indexed, 0 cross-language collisions.

No LLM judge, no external detector, no replacement character rule, no new lexicon or gloss entry.

### Realizable pairs

| | v2 | v2.1 |
|---|---|---|
| REALIZABLE | 77 | 80 |
| UNREALIZABLE | 112 | 109 |
| pairs | 189 | 189 |

Net widening +3. Newly UNREALIZABLE: 0.

- **SEC-02-2-C-004 / CONDITION** UNREALIZABLE → REALIZABLE
- **SEC-02-2-C-005 / CONDITION** UNREALIZABLE → REALIZABLE
- **SEC-02-2-C-007 / CONDITION** UNREALIZABLE → REALIZABLE

Each of those was rendered together with its statement and put to the unchanged Draft Validator v1.2: ALL_ACCEPT_EMPTY_HISTOGRAM. Realizable means deterministically constructible *and* valid — the ownership guard, containment, numeric safety, condition and qualifier preservation, language validation and source-key ownership are unchanged and all of them still run.

SEC-02-2-R025's `normally` remains UNREALIZABLE: R025 is an English-source claim and no frozen gloss frame exists for its qualifier.

## RM-2 — obligation derivation

`requires_condition_slot` was derived from an all-anchors test. All-anchors is stage E's rule for deciding *where* a condition is checked, not *whether* it survived; stage E's satisfaction test is any-anchor. The gate was asking a stricter, different question from the one that scores.

v2.1 asks the validator instead of reimplementing it. For every exposed claim the statement realization is rendered alone and put to the unchanged Draft Validator v1.2; a CONDITION slot is required only where v1.2 raises `CONDITION_DROPPED`. Where the probe cannot run, the obligation stands — the failure direction is toward demanding a slot.

Claims probed 14. Obligation asserted for 1: SEC-02-2-P0-001. Withdrawn against the old all-anchors rule for 6.

Qualifier obligations are deliberately **not** derived this way and are unchanged. Stage E scores a qualifier on half its anchors, and DF-01 established that a claim's own canonical sentence can clear that threshold while saying nothing the qualifier says. Deriving the qualifier obligation from stage E would reintroduce the defect Draft Validator v1.2 exists to close. A registered qualifier stays mandatory wherever its claim is stated.

No claim-specific branch exists. The rule is uniform over claims and sections.

## RM-1 — the canonical planner option universe

`data/book/drafting/sec_02_2/architecture_v2/contracts/planner_option_universe_v2_1.json`

Universe SHA256 `fafa8b4ceebe788d9765ac8f82463fde5b4c1253c38222fe178113874d37c000`.

Exposed 16 of 16 allocated claims; 0 excluded.

One artifact, derived mechanically from M1's plan rules, M2 v2.1's realizable pairs, the frozen claim obligations and the frozen draft plan. There is no second hand-maintained option list, because two derivations of one thing is the defect this phase closes.

### The subset invariant

```
required_roles ⊆ available_roles ⊆ realizable_roles
```

Holds for all 16 exposed claims: True. Violations: none.

It is enforced while the universe is constructed and re-checked when it is loaded, so a violating artifact cannot be read by either consumer. A claim that fails it is excluded with a recorded reason rather than listed with an obligation it cannot satisfy; if the excluded claim is a required core claim the build fails, because a thinner section is not an acceptable resolution of a contradiction.

### The Pilot #1 contradiction

- SEC-02-2-C-005 exposed: True
- `requires_condition_slot`: False (was `true`, from the all-anchors rule)
- CONDITION available: True (was absent)
- CONDITION realizable: True (was UNREALIZABLE)
- **contradiction present: False**

Both upstream defects are closed independently, as the failure analysis predicted either alone would have sufficed: the obligation is no longer asserted because v1.2 does not raise `CONDITION_DROPPED` on C-005's statement, and CONDITION is now realizable because its condition strings are Turkish. The contradiction is not absent by luck — it is unconstructible, and NEG-U06 rebuilds it deliberately and is refused at load.

## Feasibility proof

- feasible: **True**
- plan `SEC-02-2-FEASIBILITY-V2-1`, 19 slots, 19 units (19 material)
- validation ACCEPT, histogram `{}`
- topics 3/3
- mandatory conditions 19 required, 0 dropped
- mandatory qualifiers 2 required, 0 dropped
- numeric drift 0; source keys valid True; relations supported True
- language failures 0
- UNREALIZABLE pairs selected 0
- required core claims missing none

The plan is built from the serialized universe and nothing else.

### Universe SHA equality

| consumer | universe SHA256 |
|---|---|
| deterministic feasibility proof | `fafa8b4ceebe788d9765ac8f82463fde5b4c1253c38222fe178113874d37c000` |
| planner payload (built, not sent) | `fafa8b4ceebe788d9765ac8f82463fde5b4c1253c38222fe178113874d37c000` |

Equal: **True**. Neither consumer re-derives the universe; each embeds the identical block and hashes it.

## Static containment proof under M2 v2.1

- status **PASS**, Draft Validator tunnelbook-section-draft-validator-v1.2, unchanged
- 189 pairs (80 realizable), 184 cases, 358 units validated
- failure histogram `{}`
- zero-tolerance violations `{}`
- false accepts 0, false rejects 0
- UNREALIZABLE refused 109/109, leaked 0
- M5 negative fixtures 21/21
- determinism in-process True, cross-process True

Written to the remediation's own path. `static_containment_proof_v2.json` and the M5 fixtures are untouched.

## Negative fixtures

14/14 rejected. Not rejected: none.

| fixture | expected | outcome |
|---|---|---|
| NEG-U01 — a required role absent from available_roles | UNIVERSE_LOAD_REFUSED | UNIVERSE_LOAD_REFUSED |
| NEG-U02 — an available role absent from realizable_roles | UNIVERSE_LOAD_REFUSED | UNIVERSE_LOAD_REFUSED |
| NEG-U03 — a mandatory core claim (SEC-02-2-C-001) with no satisfiable role set | UNIVERSE_BUILD_REFUSED | UNIVERSE_BUILD_REFUSED |
| NEG-U04 — the feasibility proof universe differs from the planner payload universe | SHA_MISMATCH_DETECTED | SHA_MISMATCH_DETECTED |
| NEG-U05 — an injected alternate option universe carrying an unsatisfiable claim | UNIVERSE_LOAD_REFUSED | UNIVERSE_LOAD_REFUSED |
| NEG-U06 — the SEC-02-2-C-005 historical contradiction, reconstructed | UNIVERSE_LOAD_REFUSED | UNIVERSE_LOAD_REFUSED |
| NEG-U07 — diacritic-free Turkish classified as not Turkish by the v2 character rule | OLD_RULE_FALSE_NEGATIVE_REPRODUCED_AND_CORRECTED | OLD_RULE_FALSE_NEGATIVE_REPRODUCED_AND_CORRECTED |
| NEG-U08 — English and unattested material offered as admissible Turkish | ALL_REFUSED | ALL_REFUSED |
| NEG-U09 — SEC-02-2-R025 / QUALIFIER_SCOPE (`normally`) selected in a plan | PLAN_VALIDATION_REJECTED | PLAN_VALIDATION_REJECTED |
| NEG-U09b — SEC-02-2-R025 / QUALIFIER_SCOPE offered by the canonical universe | NOT_OFFERED | NOT_OFFERED |
| NEG-U10 — a source key registered to a different claim (source laundering) | PLAN_VALIDATION_REJECTED | PLAN_VALIDATION_REJECTED |
| NEG-U11 — a numeric addressed through another claim's id | PLAN_VALIDATION_REJECTED | PLAN_VALIDATION_REJECTED |
| NEG-U11b — a numeric fact id the claim does not register | PLAN_VALIDATION_REJECTED | PLAN_VALIDATION_REJECTED |
| NEG-U12 — every newly REALIZABLE pair rendered and put to the unchanged validator | ALL_ACCEPT_EMPTY_HISTOGRAM | ALL_ACCEPT_EMPTY_HISTOGRAM |

## Historical regression and frozen integrity

- frozen artifacts 17, drift none
- frozen modules 11, drift none
- lexicons and gloss tables 4, drift none
- **byte-identical: True**

M1 v2, M2 v2, M3, M4, M5's artifacts, Draft Validators v1 / v1.1 / v1.2, the citation renderer and the preserved Pilot #1 raw plan, option set, feasibility proof and rejection are unchanged. Pilot #1 remains REJECTED and is not reinterpreted.

M2 v2.1 and the obligation rule are additive. The v2.1 build runs M2 v2's own builder with the language predicate substituted on the imported module object, and the obligation rule is substituted on M1's imported module object; neither script file is written to, and both are re-hashed above. No failure code is renamed, removed or made unreachable — `PLAN_ROLE_UNREALIZABLE` is untouched and `PLAN_PARAGRAPH_CONDITION_MISSING` still fires for every claim whose statement really does drop its condition.

## Accounting

| | count |
|---|---|
| generation calls | 0 |
| rendered/released drafts | 0 |
| retrieval calls | 0 |
| Qdrant writes | 0 |
| corpus reads | 0 |
| validators weakened | 0 |
| failure codes renamed or removed | 0 |
| lexicon or gloss entries added | 0 |
| frozen artifacts modified | 0 |
| claim-specific branches | 0 |

## Gate

| condition | satisfied |
|---|---|
| AC-R01 — Frozen Architecture V2 inputs re-hashed with drift 0 before implementation. | yes |
| AC-R02 — Exactly one canonical planner option universe artifact exists, versioned, carrying its own SHA. | yes |
| AC-R03 — The universe is derived mechanically from M1 rules, M2 v2.1 realizable pairs, frozen claim obligations and the frozen draft plan. No second hand-maintained option list exists. | yes |
| AC-R04 — required_roles ⊆ available_roles ⊆ realizable_roles holds for every exposed claim, enforced at construction and re-checked on load. | yes |
| AC-R05 — A universe artifact violating the subset invariant fails closed and cannot be loaded. | yes |
| AC-R06 — The Pilot #1 contradiction (a claim requiring CONDITION while not offering it) is impossible by construction, demonstrated by a direct regression. | yes |
| AC-R07 — Condition obligations are derived from the frozen Draft Validator v1.2 itself, not from a reimplementation, and no claim-specific branch exists anywhere. | yes |
| AC-R08 — M2 v2.1 is additive: claim_realization_contract_v2.json and script 60 are byte-identical after the phase. | yes |
| AC-R09 — The Turkishness fix uses frozen language metadata corroborated by the frozen Draft Language Validator. No character heuristic, no LLM judge, no external detector. | yes |
| AC-R10 — M2 v2.1 only widens realizability. Old and new realizable-pair counts recorded. Every newly REALIZABLE pair passes the unchanged containment, ownership, numeric, condition, qualifier, language and source-key guards. | yes |
| AC-R11 — SEC-02-2-R025's 'normally' remains refused. English visible prose remains impossible. | yes |
| AC-R12 — translation_glosses, condition_glosses, function lexicon and paraphrase lexicon are byte-identical. No new factual synonym is introduced. | yes |
| AC-R13 — A complete feasible SEC-02-2 plan exists, built from the canonical universe alone: topics 3/3, mandatory conditions and qualifiers satisfied, required numerics preserved, valid source keys, no unsupported relation, no UNREALIZABLE pair selected. | yes |
| AC-R14 — The feasibility proof and the independently built planner payload record an identical universe SHA. | yes |
| AC-R15 — The Architecture V2 static containment proof re-run under M2 v2.1 passes with an empty Draft Validator v1.2 failure histogram and zero occurrences of every zero-tolerance code. | yes |
| AC-R16 — False accepts 0 and false rejects 0 over the declared remediation fixture universe. | yes |
| AC-R17 — All declared negative fixtures reject deterministically, including the C-005 historical contradiction, a diverging payload universe, an injected alternate universe, an English token admitted as Turkish, R025's 'normally' offered, a wrong source key and an unsupported numeric or unit. | yes |
| AC-R18 — Historical regression: M1 v2, M2 v2, M3, M4, M5, Draft Validators v1/v1.1/v1.2, the citation renderer, the Pilot #1 raw plan and rejection, and prior frozen artifacts are byte-identical. | yes |
| AC-R19 — No validator, threshold, fixture or failure code is weakened; no failure code is renamed or removed. | yes |
| AC-R20 — 0 generation calls, 0 renders released, 0 retrieval calls, 0 Qdrant writes, 0 corpus reads. Pilot #2 is not run. | yes |

**CLOSED / GO**

## Next phase

SEC-02-2 ARCHITECTURE V2 PILOT #2 AUTHORISATION — reachable now that this remediation closes GO. That phase may allow exactly one semantic-plan generation. It is not run here.
