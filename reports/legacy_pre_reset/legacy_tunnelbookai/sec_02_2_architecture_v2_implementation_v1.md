# SEC-02-2 DRAFTING ARCHITECTURE V2 IMPLEMENTATION

**CLOSED / GO.** Contracts, renderer and tests only. No prose was generated, no pilot was rendered, and ARCHITECTURE V2 PILOT #1 is not authorised here.


## Acceptance contract

Authored and frozen before any implementation existed, and unamended since.

- SHA256 `c9766e437bd00222574d1aeee5ede17ff74a51bf5ae0cea37e0f3f496f6ebccd`
- Unamended after results were seen: **True**

| Condition | Result |
|---|---|
| AC-01_preflight_frozen_drift | PASS |
| AC-02_plan_ir_has_no_prose_field | PASS |
| AC-03_plan_validation_fails_closed | PASS |
| AC-04_realization_data_is_frozen | PASS |
| AC-05_morphology_is_deterministic | PASS |
| AC-06_renderer_is_pure | PASS |
| AC-07_static_containment_proof | PASS |
| AC-08_no_false_accepts_or_rejects | PASS |
| AC-09_construction_invariant | PASS |
| AC-10_unrealizable_is_explicit | PASS |
| AC-11_frozen_integrity | PASS |
| AC-12_no_generation_in_this_phase | PASS |
| AC-13_no_style_layer | PASS |
| AC-14_historical_regression | PASS |


## Static containment proof

The claim is capability, not behaviour: every output the renderer can construct within the declared universe is valid under the unchanged Draft Validator v1.2.

| | |
|---|---|
| Claims × roles enumerated | 27 × 7 = 189 |
| REALIZABLE pairs | 77 |
| UNREALIZABLE pairs, all refused | 112 |
| Pairs no permitted plan contains | 4 |
| Plans enumerated and rendered | 171 |
| Units rendered and validated | 353 |
| Accepted | 171 |
| Validator failure histogram | `{}` |
| False accepts / false rejects | 0 / 0 |


## Realization coverage

77 of 189 claim/role pairs are realizable from frozen approved semantics. The remainder are UNREALIZABLE with a recorded reason and are refused by the renderer — a gap left visible rather than filled from model knowledge.


## Negative fixtures

21 of 21 reject, and each is recorded with the layer that caught it.

| Fixture | Description | Caught at |
|---|---|---|
| NEG-01 | a claim that is not on the allowlist | PLAN_VALIDATION_REJECTED |
| NEG-02 | a claim on the composition denylist | PLAN_VALIDATION_REJECTED |
| NEG-03 | a relation the claim does not allow | PLAN_VALIDATION_REJECTED |
| NEG-04 | a source key registered to a different claim (source laundering) | PLAN_VALIDATION_REJECTED |
| NEG-05 | a numeric the declaring claim does not register | PLAN_VALIDATION_REJECTED |
| NEG-06 | a numeric addressed through another claim's id | PLAN_VALIDATION_REJECTED |
| NEG-07 | a condition the claim does not carry | PLAN_VALIDATION_REJECTED |
| NEG-08 | a qualifier id belonging to no registered qualifier | PLAN_VALIDATION_REJECTED |
| NEG-09 | an invented realization role | PLAN_PARSE_REJECTED |
| NEG-10 | a free-text field injected into a slot | PLAN_PARSE_REJECTED |
| NEG-11 | prose smuggled under an undeclared but innocent field name | PLAN_PARSE_REJECTED |
| NEG-12 | a paragraph stating C-002 without its paragraph-scoped qualifier | PLAN_VALIDATION_REJECTED |
| NEG-13 | a paragraph stating C-009 without its scope limitation | PLAN_VALIDATION_REJECTED |
| NEG-14 | a role the contract marks UNREALIZABLE for this claim | PLAN_VALIDATION_REJECTED |
| NEG-15a | a supporting role standing without the statement it supports | PLAN_VALIDATION_REJECTED |
| NEG-15b | a paragraph-scoped condition with no slot to carry it | PLAN_VALIDATION_REJECTED |
| NEG-15c | both statement roles for one claim in one paragraph | PLAN_VALIDATION_REJECTED |
| NEG-15 | a language the section policy does not permit | PLAN_PARSE_REJECTED |
| NEG-16 | 15 cm presented as a derived 150 mm source-stated figure | REJECTED |
| NEG-17 | SEC-02-2-C-009's clay-zone thickness generalised to all first layers | REJECTED |
| NEG-18 | Tablo-351-5 presented as establishing the C25/30 strength class | REJECTED |


## Determinism

- In-process, 3 runs identical: True
- Fresh process identical: True
- Universe digest `4351ae07779ebff27d7b4fad94f800ccda97108d8399ea710e6dffa2649f6517`


## Phase accounting

| | |
|---|---|
| corpus reads | 0 |
| generation calls | 0 |
| post render model passes | 0 |
| qdrant writes | 0 |
| rendered pilot | NONE |
| retrieval calls | 0 |
| validators weakened | none |
| frozen inputs drift | 0 |
| pilot authorised | False |

