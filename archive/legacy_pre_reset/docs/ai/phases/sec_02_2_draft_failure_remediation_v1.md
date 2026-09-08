# PHASE (COMPLETED) — SEC-02-2 DRAFT FAILURE REMEDIATION V1

Status: **CLOSED / GO**. Executed 2026-08-19. Its one authorised generation was
spent and pilot attempt #2 was rejected. Do not re-execute this brief.

Kept as the template for phase briefs and as the record of what was required.

## Goal

Close the root causes of U-A-P01-S03 and U-C-P01-S03, add deterministic
per-unit language validation, preserve qualifier and condition requirements,
and run one controlled pilot attempt only after every gate passes.

## Root cause A — U-A-P01-S03

SEC-02-2-C-002 must preserve the meaning: Tablo-351-5 gives 28-day core-sample
acceptance criteria for C25/30 shotcrete. It must not be presented as
establishing or defining the minimum strength-class requirement — that is
SEC-02-2-C-001's. Frozen as semantic constraint `DSC-C002-001`.

## Root cause B — U-C-P01-S03

A Turkish section received an English visible material unit, and the source
claim's condition `dependent on tunnel size` was dropped. Required: a draft
language contract, a deterministic language validator, Draft Validation
Contract v1.1, Draft Validator v1.1, prompt v1.1, plan v1.1, and a frozen
English→Turkish condition mapping (`dependent on tunnel size` →
`tünel boyutuna bağlı olarak`). Translations are frozen in advance, never
invented at runtime.

## Language rule

Section language `tr`; visible material prose Turkish. Technical terms
(shotcrete, flashcrete, C25/30, MPa, FHWA, TS 4559, kg/m³) must not trigger
false failures. A complete English material sentence must reject. Codes added:
`LANGUAGE_MISMATCH`, `LANGUAGE_AMBIGUOUS`, `SEMANTIC_SCOPE_MISMATCH`. No
existing code renamed or removed.

## Regression

Historical bad units stay rejected; corrected synthetic forms pass; ≥40 focused
fixtures; targeted drafting/citation/composition tests plus new remediation
tests. Full suite only for the final gate.

## Generation

One controlled attempt, same model, temperature 0.0, seed 11, no automatic
retry. Render only on acceptance, using the frozen citation contract.

## Outcome

All gates passed: 324 tests, 51/51 remediation fixtures, 107/107 v1 fixtures,
0 false accepts, 0 false rejects, frozen integrity intact. Attempt #2 rejected
on U-A-P01-S02 (QUALIFIER_DROPPED) and U-C-P01-S02 (UNSUPPORTED_PROPOSITION).
Nothing rendered. Next phase: SEC-02-2 DRAFT FAILURE ANALYSIS V2.
