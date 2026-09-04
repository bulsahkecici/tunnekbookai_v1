# ARCHITECTURE V2 PILOT FAILURE ANALYSIS V1

**CLOSED / GO.** ARCHITECTURE V2 PILOT #1 remains REJECTED. Root cause is the authorisation option universe, not the model, the renderer or the validator.


## Reproduced contradiction

- `all_points_confirmed`: True
- `condition_offered`: False
- `feasibility_proof_skipped_c005`: True
- `nothing_rendered`: True
- `option_set_available_roles`: ['CLAIM_STATEMENT', 'NUMERIC_CRITERIA', 'REQUIREMENT']
- `option_set_marked_requires_condition_slot`: True
- `planner_rule_demanding_it`: a claim with requires_condition_slot needs a CONDITION slot in the same paragraph
- `planner_rule_restricting_selection`: only roles listed in available_roles may be selected (prompt rule 5)
- `planner_selected_it`: True
- `planner_selected_pair`: ['SEC-02-2-C-005', 'CONDITION']
- `realization_reason`: a registered condition is not Turkish and has no frozen gloss frame
- `realization_status`: UNREALIZABLE
- `rejected_before_rendering`: True
- `validator_rejection_code`: ['PLAN_ROLE_UNREALIZABLE']


## Set-consistency audit

Invariant: `required_roles ⊆ available_roles ⊆ realizable_roles`, over 16 exposed claims.

| Claim | core | required | available | realizable | req⊆avail | avail⊆realiz |
|---|---|---|---|---|---|---|
| SEC-02-2-C-001 | yes | — | 3 | 3 | ok | ok |
| SEC-02-2-C-002 |  | QUALIFIER_SCOPE | 4 | 4 | ok | ok |
| SEC-02-2-R001 | yes | — | 2 | 2 | ok | ok |
| SEC-02-2-P0-001 | yes | CONDITION | 3 | 3 | ok | ok |
| SEC-02-2-P0-006 | yes | CONDITION | 4 | 4 | ok | ok |
| SEC-02-2-P0-005 |  | — | 2 | 2 | ok | ok |
| SEC-02-2-P0-004 |  | — | 2 | 2 | ok | ok |
| SEC-02-2-P0-007 | yes | CONDITION | 2 | 2 | ok | ok |
| SEC-02-2-P0-008 | yes | CONDITION | 3 | 3 | ok | ok |
| SEC-02-2-C-003 |  | CONDITION | 3 | 3 | ok | ok |
| SEC-02-2-C-004 |  | — | 3 | 3 | ok | ok |
| SEC-02-2-C-005 |  | CONDITION | 3 | 3 | **FAIL** | ok |
| SEC-02-2-C-007 |  | — | 2 | 2 | ok | ok |
| SEC-02-2-C-006 |  | CONDITION | 3 | 3 | ok | ok |
| SEC-02-2-C-012 |  | — | 2 | 2 | ok | ok |
| SEC-02-2-C-009 |  | QUALIFIER_SCOPE | 5 | 5 | ok | ok |

- **form_1_required_role_not_offered**: 1 — ['SEC-02-2-C-005']
- **form_2_offered_role_not_realizable**: 0 — none
- **form_3_mandatory_claim_with_no_satisfiable_role_set**: 1 — ['SEC-02-2-C-005']
- **form_4_feasibility_excludes_a_pair_the_payload_requires**: 1 — ['SEC-02-2-C-005']
- **form_5_planner_universe_differs_from_feasibility_universe**: 0 — none


## Was the obligation real?

No. C-005's CLAIM_STATEMENT rendered alone validates **ACCEPT** with histogram `{}`.

`paragraph_scoped_conditions` asks whether ALL of a condition's anchors appear in the canonical wording, and classifies the condition as paragraph-scoped when they do not. Stage E — the rule that actually scores — asks whether ANY anchor reaches the required scope. C-005's condition 'priz hızlandırıcı katkı tipi' loses only the anchor 'tipi', which fails prefix agreement against the canonical's 'tipine' because both are under the five-character minimum. The other three anchors are present, so stage E is satisfied and the gate demanded a slot for a condition the sentence already carried.

*the defect is not specific to C-005: any claim whose condition has one non-agreeing anchor and several agreeing ones acquires a false obligation*


## Was the role really unrealizable?

No. `REAL.is_turkish` searches for the characters çğıöşü. A Turkish string written without them — 'takip eden tabakalar', 'ilk tabaka', 'ilave tabakalar' — is classified as not Turkish and its role marked UNREALIZABLE.

3 false negatives of 4 entries citing a non-Turkish field; 1 correctly refused.

| Claim | Role | Flagged | Genuinely English |
|---|---|---|---|
| SEC-02-2-C-004 | CONDITION | ['ilk tabaka'] | **no** |
| SEC-02-2-C-005 | CONDITION | ['takip eden tabakalar'] | **no** |
| SEC-02-2-C-007 | CONDITION | ['ilave tabakalar'] | **no** |
| SEC-02-2-R025 | QUALIFIER_SCOPE | ['normally'] | yes |

Severity: completeness, not safety — the defect fails closed. It withholds realization material rather than admitting unsafe material, so it could not have produced an unlicensed word and did not affect the static containment proof, which is why it survived the implementation phase untouched.


## Two universes

Two derivations of one universe, written separately, disagreeing on exactly the claim that broke the pilot. Gate 5's builder applied the satisfiability test and dropped SEC-02-2-C-005; gate 4's builder did not and listed it. Only gate 4's output was serialized into the model payload, so the contradiction gate 5 had already found was invisible where it mattered.

- planner universe: 16 claims, 46 pairs
- feasibility universe: 15 claims
- claims only in the planner universe: ['SEC-02-2-C-005']

**Minimal invariant.** ONE CANONICAL PLANNER OPTION UNIVERSE. A single artifact derived mechanically from M2's realizable pairs and M1's obligation rules, admitting a claim only when required_roles ⊆ available_roles ⊆ realizable_roles holds for it, serialized once and consumed by SHA by both the deterministic feasibility proof and the model payload. Neither consumer may re-derive it.


## Classification

| Candidate | Verdict |
|---|---|
| A_MODEL_COMPLIANCE_FAILURE | NOT ESTABLISHED |
| B_SEMANTIC_PLAN_SCHEMA_DEFECT | REFUTED |
| C_CLAIM_REALIZATION_CONTRACT_DEFECT | SUPPORTED — contributing |
| D_AUTHORISATION_OPTION_SET_CONTRADICTION | SUPPORTED — primary |
| E_FEASIBILITY_GATE_PLANNER_OPTION_UNIVERSE_MISMATCH | SUPPORTED — structural |
| F_OTHER | none found beyond C, D and E |

**Root cause: AUTHORISATION_OPTION_UNIVERSE_DEFECT.**

The planner option universe and the deterministic feasibility universe were derived twice by different code from the same frozen data, and disagreed on exactly the claim that broke the pilot. The disagreement was possible because no invariant required required_roles ⊆ available_roles ⊆ realizable_roles of the artifact the model actually consumed. Two upstream defects supplied the contradiction — a false obligation from an all-anchors scope test where stage E scores any-anchor, and a wrongly UNREALIZABLE role from a diacritic-based Turkishness test — and either alone would have prevented the failure had the other been absent.

| Fault | |
|---|---|
| renderer defect | False |
| validator defect | False |
| model defect | NOT ESTABLISHED |
| authorisation layer defect | True |
| realization contract defect | True |


## Smallest safe remediation

No `if claim_id == 'SEC-02-2-C-005'` anywhere. The remediation must hold for every claim and every future section, and must be checkable rather than reviewed.

**RM-1.** one canonical planner option universe: a single artifact derived mechanically from M2's realizable pairs and M1's obligation rules — a claim is admitted only when required_roles ⊆ available_roles ⊆ realizable_roles holds for it; a claim failing the test is excluded with a recorded reason, never listed with an unsatisfiable obligation Prevents: forms 1, 3, 4 and 5 of the contradiction audit, for all claims

**RM-2.** derive requires_condition_slot from the same any-anchor test stage E applies, instead of the all-anchors classification — an obligation is asserted only where the statement realization does not already satisfy it, verified by rendering and validating the statement alone Prevents: false obligations of the C-005 form for every claim

**RM-3.** replace M2's diacritic-presence Turkishness test with one that cannot false-negative on diacritic-free Turkish — a field is judged English on evidence of English, not absence of çğıöşü Prevents: wrongly UNREALIZABLE roles; 3 entries recover, R025's genuinely English 'normally' must still be refused
  Risk: this one widens what M2 marks realizable, so it must be gated by the static containment proof re-run and by fixtures asserting R025 stays refused. It is a realization-contract change and is NOT made here.


## Accounting

| | |
|---|---|
| corpus reads | 0 |
| frozen artifacts modified | 0 |
| generation calls | 0 |
| glosses or lexicons changed | 0 |
| pilot 2 authorised | False |
| qdrant writes | 0 |
| realization contract changed | 0 |
| renders | 0 |
| retrieval calls | 0 |
| validators changed | 0 |

