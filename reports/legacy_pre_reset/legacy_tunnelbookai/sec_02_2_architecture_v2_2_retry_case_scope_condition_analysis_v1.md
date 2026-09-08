# SEC-02-2 ARCHITECTURE V2.2 RETRY CASE-SCOPE CONDITION ALLOCATION FAILURE ANALYSIS V1

**CLOSED / GO.** The preserved failure is reproduced exactly: Draft Validator v1.2 rejects
`U-C-P02-S02` (`SEC-02-2-P0-008`, `CASE_SCOPE`) with `CONDITION_DROPPED` for `In some`.

P0-008 is split between accepted `CLAIM_STATEMENT` `U-C-P02-S01` and rejected `CASE_SCOPE`
`U-C-P02-S02`. Because `In some` occurs in the canonical claim, stage E requires its anchor in
every claim-bearing unit. The statement emits `Belirli`; the case enumeration does not. The other
condition, `dependent on tunnel size`, is absent from the canonical claim and therefore
paragraph-scoped; the adjacent statement satisfies it. Targeted controls prove both decisions.

Root cause: `MULTI_ROLE_CLAIM_CONDITION_ALLOCATION_DEFECT`, with a secondary
`CASE_SCOPE_REALIZATION_CONTRACT_GAP`. Role feasibility was closed without condition feasibility.
The exact constructed set is unsatisfiable: the CASE_SCOPE unit must satisfy a unit condition it
was neither allocated nor able to realize. This is not a validator, Book Style, or terminology
fallback fault. `ORIGINAL_TERM_UNRESOLVED` passed independently. The observed failure is not a
renderer fault; however, a related latent contradiction is recorded: `required_dependency` is
contracted but the retry case renderer emits only terms, masked by paragraph scope.

Smallest safe remediation: add a general, versioned claim-role condition-closure contract. For
every emitted claim-bearing role, derive condition scope with unchanged Validator v1.2; require
unit-scoped conditions in that role's realization, and paragraph-scoped conditions in one bound
unit of the same paragraph. Make required semantic conditions explicit renderer inputs and prove
the projected unit/paragraph allocation before integration. No claim branch and no validator,
fallback, gloss, or lexicon change.

Tests: phase + preserved retry 19/19; validator/fallback regressions 107/107. Frozen drift 0.
Counts: generation 0, rendering 0, retrieval 0, Qdrant writes 0, corpus-wide reads 0.
