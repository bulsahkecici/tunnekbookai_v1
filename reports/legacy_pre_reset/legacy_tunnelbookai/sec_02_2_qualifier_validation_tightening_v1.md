# SEC-02-2 Qualifier Preservation Validation Tightening v1

**CLOSED / GO.** Closes DF-01. Validator-tightening phase: 0 generation attempts, 0 retrieval calls, 0 Qdrant writes, 0 corpus reads, 0 validators weakened, no prose rendered, attempt #3 not authorised here.

## DF-01, reproduced

Stage E scores a qualifier preserved when at least half of its lexical anchors reach the paragraph. A qualifier phrased in its own claim's vocabulary is therefore scored preserved by a verbatim copy of the canonical sentence, which states the qualifier's meaning nowhere.

| # | Assertion | Holds |
|---|---|---|
| 1 | SEC-02-2-C-002's qualifier is actually missing and already rejected | yes |
| 2 | SEC-02-2-C-009's qualifier is actually missing | yes |
| 3 | existing stage E nevertheless scores it preserved | yes |
| 4 | the apparent pass comes from anchor overlap with canonical claim vocabulary | yes |

`U-D-P01-S03` is byte-identical to `SEC-02-2-C-009`'s canonical sentence: true. Stage E scored 5/6 anchors present — ['kil', 'zonlu', 'tabakalara', 'katman', 'kalınlığı'] — of which ['katman', 'kil', 'tabakalara', 'zonlu'] are tokens of the sentence the writer copied and ['kalınlığı'] came from neighbouring units. The copied sentence alone already scores 4/6, clearing the threshold on its own, so nothing the prose said was needed to earn the pass. The one anchor the copy misses, `özgüdür`, is the single word carrying the scope limitation. The control claim `SEC-02-2-C-002` scored 3/9 and was correctly rejected.

**Root cause.** lexical anchor overlap is used as a proxy for semantic realisation; the proxy is vacuous whenever the qualifier's anchors are drawn from the claim it qualifies.

## The remedy, and the one that was rejected

Rejected: raising the half-anchor threshold to a higher percentage; it is the same lexical heuristic with a different constant, would create false rejects on faithful prose that renders the meaning in other words, and would still pass a verbatim copy whose anchor overlap happens to be total.

Adopted: registered qualifier semantics - explicit, deterministic required-meaning constructions per registered qualifier, following DSC-C002-001. Stage `L_qualifier_semantics` scores a registered qualifier by whether some clause satisfies a declared construction — an operator and the thing it is applied to, in the same clause. Clause scope is what separates meaning from padding: a paragraph can contain `özgü` and it can contain `kil` without ever having said one about the other.

Two registry integrity properties are enforced fail-closed before any verdict: the registered qualifier text must equal the frozen allowlist qualifier byte for byte, and the claim's own canonical sentence must **not** satisfy the constructions. The second is DF-01 restated as a general property — an entry a verbatim copy would satisfy cannot tell realisation from reproduction, and is refused.

No new failure code. `QUALIFIER_DROPPED` for absent required meaning; `SEMANTIC_SCOPE_MISMATCH` only where prose actively states the generalised scope.

## SEC-02-2-C-009's historical wording

| | |
|---|---|
| Before | PASS - stage E scored 5/6 anchors preserved; validator v1.1 returned no failure |
| After | REJECT - QUALIFIER_DROPPED at stage L_qualifier_semantics |

## Fixtures

| Case | Category | Expected | Outcome | Codes |
|---|---|---|---|---|
| QV-B1 | meaning_realised_canonical_unit | valid | PASS | — |
| QV-B2 | meaning_realised_scope_unit | valid | PASS | — |
| QV-E1 | c002_historical_bad_form | reject | PASS | QUALIFIER_DROPPED |
| QV-E2 | c002_forbidden_attribution | reject | PASS | UNSUPPORTED_PROPOSITION, SEMANTIC_SCOPE_MISMATCH |
| QV-F1 | c002_two_bound_units_identity | valid | PASS | — |
| QV-F2 | c002_two_bound_units_numeric | valid | PASS | — |
| QV-F3 | c002_single_unit_combined | valid | PASS | — |
| QV-H-U-A-P01-S01 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-H-U-B-P01-S01 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-H-U-B-P01-S02 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-H-U-B-P01-S03 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-H-U-B-P01-S04 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-H-U-B-P01-S05 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-H-U-C-P01-S01 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-H-U-C-P01-S03 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-H-U-C-P01-S04 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-H-U-C-P01-S05 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-H-U-C-P01-S06 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-H-U-D-P01-S01 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-H-U-D-P01-S02 | unrelated_unit_not_newly_rejected | valid | PASS | — |
| QV-A | df_01_historical_false_pass | reject | PASS | QUALIFIER_DROPPED |
| QV-B3 | meaning_realised_exclusivity_only | valid | PASS | — |
| QV-B4 | meaning_realised_non_generality_only | valid | PASS | — |
| QV-C | canonical_alone | reject | PASS | QUALIFIER_DROPPED |
| QV-D1 | lexical_padding | reject | PASS | QUALIFIER_DROPPED |
| QV-D2 | generalised_scope_asserted | reject | PASS | QUALIFIER_DROPPED, SEMANTIC_SCOPE_MISMATCH |

26/26 pass. False accepts: 0. False rejects: 0.

## Inherited behaviour

| | |
|---|---|
| Attempt #2 rejected under v1.1 | ['U-A-P01-S02', 'U-C-P01-S02'] |
| Attempt #2 rejected under v1.2 | ['U-A-P01-S02', 'U-C-P01-S02', 'U-D-P01-S03'] |
| Newly rejected | ['U-D-P01-S03'] |
| Newly accepted | none |
| Inherited codes unchanged | True |
| New codes invented | none |

- `draft_validator_v1` sha256 `a72406aafdd40a26…` — unchanged: True
- `draft_validator_v1_1` sha256 `5adb41329da31c28…` — unchanged: True

## Gate

| Condition | Result |
|---|---|
| df 01 reproduced | True |
| false pass eliminated | True |
| c009 semantic qualifier enforced | True |
| c002 behaviour preserved | True |
| no validator weakened | True |
| prior validator versions unchanged | True |
| all targeted tests pass | True |
| false accepts | 0 |
| false rejects | 0 |
| registry integrity | True |

**CLOSED / GO**

