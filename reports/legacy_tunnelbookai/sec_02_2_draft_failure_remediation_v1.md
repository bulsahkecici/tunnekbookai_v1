# SEC-02-2 Draft Failure Remediation v1

`tunnelbook-sec-02-2-draft-failure-remediation-v1`


## Executive Decision

Both historical failures were root-caused and every remediation gate passed. The one authorised generation produced a schema-valid DraftIR whose prose did not validate: 2 of 16 units were rejected with codes ['UNSUPPORTED_PROPOSITION', 'QUALIFIER_DROPPED']. Nothing was rendered, nothing was repaired and no second attempt was taken.


**SEC-02-2 DRAFT FAILURE REMEDIATION V1 — CLOSED / GO; SEC-02-2 PILOT ATTEMPT #2 — REJECTED**


## Historical Pilot Failure

The first controlled SEC-02-2 pilot produced 20 units. Eighteen validated, two did not, and the pilot was rejected whole. No Markdown was rendered, no prose was released and no retry was taken.

| | |
|---|---|
| Draft id | `SEC-02-2-PILOT-V1` |
| Units | 20 |
| Material units | 16 |
| Validated | 18 |
| Rejected | U-A-P01-S03, U-C-P01-S03 |
| Failure codes | CONDITION_DROPPED, QUALIFIER_DROPPED |
| Rendered draft | not created |
| Automatic retries | 0 |


## Why the Rejection Was Correct

Both rejected units carried a real defect, and the rules that fired were the rules that should have fired.

- **U-A-P01-S03** stated Tablo-351-5's acceptance values while dropping the qualifier that says they are acceptance criteria. Read on its own, the sentence can be taken as the table establishing the C25/30 class. It does not: the class requirement is SEC-02-2-C-001's, and Tablo-351-5 tests it.
- **U-C-P01-S03** dropped SEC-02-2-P0-008's `dependent on tunnel size` condition. A thickness that holds for some tunnel sizes, stated without the size, is a wider claim than the source makes.

§6 of this phase's contract forbids recording a validator as faulty for correctly rejecting bad prose, and neither rejection was wrong. The remediation therefore targets the draft input, the drafting instructions, and the one place where there was no rule at all - never the thresholds of the rules that worked.


## Frozen Inputs

19 artifacts were checked against the SHAs scripts/47's manifest recorded, not against whatever is on disk now.

| | |
|---|---|
| historical rejected pilot raw output | unchanged |
| historical truncated attempt 1 raw output | unchanged |
| historical pilot draft audit | unchanged |
| historical pilot draft authorization | unchanged |
| section drafting contract v1 | unchanged |
| book citation rendering contract v1 | unchanged |
| draft validation contract v1 | unchanged |
| draft plan v1 | unchanged |
| section drafting system prompt v1 | unchanged |
| section drafting controller (scripts/47) | unchanged |
| book citation renderer v1 (scripts/48) | unchanged |
| section draft validator v1 (scripts/49) | unchanged |
| composition validator (scripts/46) | unchanged |
| composition-safe allowlist | unchanged |
| composition denylist | unchanged |
| claim pair constraints | unchanged |
| drafting fixtures v1 | unchanged |
| citation fixtures v1 | unchanged |
| historical generation raw_text SHA | unchanged |


Upstream frozen integrity (inherited from the drafting phase): 116 checks, all unchanged.


## Root Cause — U-A-P01-S03

> Tablo-351-5'e göre C25/30 sınıfı püskürtme betonda, 28 günlük karot numunelerde bireysel minimum dayanım 22,5 MPa ve üç adet numuneden oluşan grubun ortalama minimum dayanımı 25,5 MPa'dır.

| | |
|---|---|
| Claims | SEC-02-2-C-002 |
| Failure codes | QUALIFIER_DROPPED |
| Detected language | tr |
| Declared section language | tr |
| Root cause | PROMPT_INSTRUCTION_GAP |
| All classes | PROMPT_INSTRUCTION_GAP, GENERATOR_COMPLIANCE_FAILURE |
| Drafting input carried the claim in full | yes |
| Validator behaved correctly | yes |


The drafting input carried SEC-02-2-C-002's qualifier verbatim, so the writer had what it needed and did not use it. The prompt never said a qualifier is semantic content that must appear in the sentence - it listed things not to add, not things not to drop - so the omission is first a prompt gap and second a compliance failure. It is not a validator gap: v1 rejected the unit.


**SEC-02-2-C-002** — dropped conditions: none; dropped qualifiers: ['Tablo-351-5 kalite kontrol kriterleridir; dayanım sınıfının kendisi değil, kabul kriteridir'].


Remediation targets:

- `data/metadata/section_drafting_system_prompt_v1_1.txt`
- `data/book/drafting/sec_02_2/draft_plan_v1_1.json`
- `data/book/drafting/sec_02_2/remediation_v1/contracts/draft_semantic_constraints_v1.json`
- `scripts/52_section_draft_validator_v1_1.py (stage K)`


## Root Cause — U-C-P01-S03

> In some specific rock conditions, such as crushed or squeezing rock, the thickness may be 12 inches (300 mm) and more.

| | |
|---|---|
| Claims | SEC-02-2-P0-008 |
| Failure codes | CONDITION_DROPPED |
| Detected language | en |
| Declared section language | tr |
| Root cause | LANGUAGE_VALIDATION_GAP |
| All classes | LANGUAGE_VALIDATION_GAP, PROMPT_INSTRUCTION_GAP, GENERATOR_COMPLIANCE_FAILURE |
| Drafting input carried the claim in full | yes |
| Validator behaved correctly | yes |


Two defects in one unit. The dropped 'dependent on tunnel size' condition is a prompt gap plus a compliance failure: the condition was supplied and the prompt's condition section did not mark conditions as mandatory content. The untranslated English is an architectural gap - v1 had no per-unit language rule, and the neighbouring English unit U-C-P01-S02 passed all nine stages, which is the proof that the condition rule caught this one by accident. The prompt did instruct translation, so the writer also disobeyed an instruction it had.


**SEC-02-2-P0-008** — dropped conditions: ['dependent on tunnel size']; dropped qualifiers: none.


Remediation targets:

- `data/book/drafting/contracts/draft_language_contract_v1.json`
- `scripts/51_draft_language_validator_v1.py`
- `scripts/52_section_draft_validator_v1_1.py (stage J)`
- `data/metadata/section_drafting_system_prompt_v1_1.txt`
- `data/book/drafting/sec_02_2/remediation_v1/contracts/cross_lingual_condition_mappings_v1.json`


## C-002 Semantic Boundary

| | |
|---|---|
| Constraint | `DSC-C002-001` |
| Claim | SEC-02-2-C-002 |
| Type | QUALIFIER_PRESERVATION |
| Required meaning | Tablo-351-5 provides 28-day core-sample acceptance criteria for C25/30 shotcrete. |
| Forbidden meaning | Tablo-351-5 establishes or defines the minimum C25/30 strength class. |
| Requirement claim | SEC-02-2-C-001 |
| Acceptance claim | SEC-02-2-C-002 |
| Missing-qualifier code | QUALIFIER_DROPPED |
| Forbidden-meaning code | SEMANTIC_SCOPE_MISMATCH |


Both claims may be stated, separately. The draft must not imply that SEC-02-2-C-002 proves SEC-02-2-C-001; no approved relationship supports that inference.


The rule matches on scope fields and declared markers - a claim whose allowlist scope says `design_table`, prose that names the reference attributively, and a clause putting a class designation in predicate position after a strength-class noun. The pilot's exact sentence appears nowhere in the matching logic (§11); it is a regression case, not the rule.


## Condition Preservation

Conditions are mandatory semantic content, not optional metadata. Plan v1.1 says so in `required_condition_fields`, the prompt says so in its own section, and the payload marks each claim's conditions with `conditions_are_mandatory`. The validator's rule is unchanged from v1: a condition whose anchors appear in the claim's own canonical wording must survive into the unit; one carried by surrounding source context must survive into the paragraph.


## Cross-Lingual Condition Mapping

3 mappings, all consistent with the frozen drafting contract's condition glosses.

| | |
|---|---|
| XL-P0-008-001 — dependent on tunnel size | tünel boyutuna bağlı olarak / tünel boyutuna göre / tünel açıklığının boyutuna bağlı olarak |
| XL-P0-008-002 — In some | bazı / belirli / kimi |
| XL-P0-007-001 — depending on ground conditions and size of the tunnel opening | zemin koşullarına ve tünel açıklığının boyutuna bağlı olarak / zemin koşullarına ve tünel boyutuna bağlı olarak |


Every registered anchor is required to be licensed by the frozen contract already. A mapping able to introduce new anchors would be a way to widen what counts as a surviving condition - a loosened validator wearing the costume of a translation table - so scripts/52 verifies the subset relation as a gate rather than trusting it (§50).


## Draft Language Contract

| | |
|---|---|
| Version | `tunnelbook-draft-language-contract-v1` |
| Section language | tr |
| Allowed visible languages | tr |
| Source claim languages | tr, en |
| Detector | `tunnelbook-lexical-orthographic-detector-v1` |
| LLM judge | no |
| Failure codes | LANGUAGE_AMBIGUOUS, LANGUAGE_MISMATCH |
| Material units | reject on mismatch and on ambiguity (fail closed) |
| Non-material units | reject only on confident English; ambiguity tolerated |


## Language Validator

Detection is lexical and orthographic. Turkish has no q, w or x and none of the digraphs th, ck, ph, gh, sh, wh, oo, ee, ea; its own ç, ğ, ı, ö, ş, ü appear in nearly every content word. Function-word lists carry the rest. Domain terms - shotcrete, flashcrete, MPa, C25/30, FHWA, TS 4559, kg/m³ - are declared neutral and score for neither side, which is what lets a Turkish sentence use them freely (§24, §27). A substantive English *clause* is a different thing from a borrowed *term*, and the clause pass is what separates them (§26).


Language fixtures: 21/21 pass, 0 false accepts, 0 false rejects.


## Draft Validation Contract v1.1

v1 is not mutated; it stays on disk at its recorded SHA. v1.1 declares its parent and adds two stages.

| | |
|---|---|
| Version | `tunnelbook-draft-validation-contract-v1.1` |
| Parent | `tunnelbook-draft-validation-contract-v1` |
| Added stages | J_language, K_semantic |
| Added codes | LANGUAGE_MISMATCH, LANGUAGE_AMBIGUOUS, SEMANTIC_SCOPE_MISMATCH |
| Removed | none |
| Weakened | none |
| Renamed codes | none |


## Draft Validator v1.1

| | |
|---|---|
| Implementation | `scripts/52_section_draft_validator_v1_1.py` |
| Parent | `scripts/49_section_draft_validator_v1.py` |
| Parent file unchanged | yes |
| v1 codes dropped | none |
| v1 stages dropped | none |
| Codes added | LANGUAGE_MISMATCH, LANGUAGE_AMBIGUOUS, SEMANTIC_SCOPE_MISMATCH |
| Stages added | J_language, K_semantic |


The validator never translates a rejected unit. It rejects (§35). A validator that repaired its own input would turn a translation failure into a pass and record it as one.


## Drafting Prompt v1.1

v1 is untouched. v1.1 adds four things the first writer was never told: the whole visible draft must be Turkish and an English claim is paraphrased rather than copied; `conditions` is mandatory semantic content; `qualifiers` is mandatory semantic content when non-empty; and the plan may carry claim-specific semantic constraints that are binding. The C-002 constraint reaches the writer through the plan, not as a hard-coded special case - §40's point being that the general rule must hold for every claim, with C-002 carrying an extra explicit boundary because the first pilot proved that distinction is easy to lose.


## Draft Plan v1.1

| | |
|---|---|
| Version | `tunnelbook-sec-02-2-draft-plan-v1.1` |
| Parent | `tunnelbook-section-drafting-contract-v1` |
| Claim allocation | unchanged from v1 |
| Added | semantic_constraints, language_policy, claim_translation_requirements, required_condition_fields, required_qualifier_fields |
| Semantic constraints | 1 |
| Translation requirements | 2 |
| Claims with mandatory conditions | 14 |
| Claims with mandatory qualifiers | 2 |


## Regression Fixtures

| | |
|---|---|
| Total | 51 |
| Passed | 51 |
| Positive | 26 |
| Negative | 25 |
| Language-scope | 21 |
| False accepts | 0 |
| False rejects | 0 |
| Code mismatches | 0 |


| Category | Passed |
|---|---|
| c002_qualifier_negative | 3/3 |
| c002_qualifier_positive | 3/3 |
| corrected_synthetic | 2/2 |
| cross_lingual_condition_negative | 2/2 |
| cross_lingual_condition_positive | 3/3 |
| cross_lingual_language_negative | 1/1 |
| historical_failed_unit | 2/2 |
| inherited_negative | 7/7 |
| inherited_positive | 3/3 |
| inherited_positive_non_material | 1/1 |
| language_ambiguous | 1/1 |
| language_ambiguous_non_material | 1/1 |
| language_negative | 6/6 |
| language_negative_non_material | 1/1 |
| language_positive | 11/11 |
| language_positive_non_material | 1/1 |
| mixed_language_negative | 2/2 |
| mixed_language_positive | 1/1 |


## Historical Regression

| | |
|---|---|
| v1 drafting fixtures re-scored under v1.1 | 107/107 |
| New false rejects introduced | 0 |
| Historical failed units still rejected | 2/2 |
| Corrected synthetics accepted | 2/2 |
| Historical test suites | 239 tests, passed |
| New test suites | 85 tests, passed |


## Frozen Integrity

| | |
|---|---|
| Remediation freeze checks | 19 |
| Changed | none |
| Upstream checks | 116 |
| Upstream changed | none |
| Composition-safe allowlist | 27 claims |
| Composition denylist | 45 claims |
| Pair constraints | 6 |
| Retrieval calls | 0 |
| Qdrant writes | 0 |


## Attempt #2 Authorization

| Condition | Verdict |
|---|---|
| `code_mismatches_zero` | PASS |
| `composition_safe_claims_27` | PASS |
| `corrected_synthetics_pass` | PASS |
| `cross_lingual_mappings_consistent` | PASS |
| `cross_lingual_mappings_frozen` | PASS |
| `denylist_unchanged_45` | PASS |
| `draft_plan_v1_1_frozen` | PASS |
| `draft_validation_contract_v1_1_frozen` | PASS |
| `drafting_prompt_v1_1_exists` | PASS |
| `drafting_prompt_v1_unchanged` | PASS |
| `false_accepts_zero` | PASS |
| `false_rejects_zero` | PASS |
| `frozen_integrity_holds` | PASS |
| `historical_failed_units_still_reject` | PASS |
| `historical_tests_pass` | PASS |
| `language_contract_frozen` | PASS |
| `language_contract_no_llm_judge` | PASS |
| `language_false_accepts_zero` | PASS |
| `language_false_rejects_zero` | PASS |
| `new_tests_pass` | PASS |
| `pair_constraints_unchanged_6` | PASS |
| `qdrant_writes_zero` | PASS |
| `remediation_fixtures_all_pass` | PASS |
| `remediation_fixtures_at_least_40` | PASS |
| `retrieval_calls_zero` | PASS |
| `root_cause_audit_complete` | PASS |
| `semantic_constraints_frozen` | PASS |
| `v1_fixtures_no_new_false_rejects` | PASS |
| `v1_fixtures_still_pass_under_v1_1` | PASS |
| `validator_v1_unweakened` | PASS |


## Attempt #2 Raw Generation

| | |
|---|---|
| Attempt | 2 |
| Model | `qwen3.6-35b-a3b-mlx` |
| Temperature | 0.0 |
| Seed | 11 |
| Max tokens | 12288 |
| Finish reason | stop |
| Completion tokens | 4046 |
| Prompt SHA | `010e5dc9e734f17f…` |
| Raw text SHA | `4ab3c70ee1247566507b1d943b4c978b11174f73bc42d0fdbe4406c888a9ac4a` |
| Preserved at | `data/book/drafting/sec_02_2/remediation_v1/raw/sec_02_2_draft_raw_attempt_2.json` |
| Generation calls in this run | 0 |
| Attempts spent by this phase | 1 |
| Replayed a preserved attempt | yes |


The raw output was written before parsing. If it had contained a bad unit it would still be there, unedited: §68 forbids rewriting, patching, translating or deleting any part of it.


## Attempt #2 Validation

| | |
|---|---|
| Status | REJECT |
| Units | 16 |
| Material units | 16 |
| Rejected units | 2 |
| Rejected unit ids | U-A-P01-S02, U-C-P01-S02 |
| Failure codes | UNSUPPORTED_PROPOSITION, QUALIFIER_DROPPED |


| Unit | Codes | Detail |
|---|---|---|
| `U-A-P01-S02` | QUALIFIER_DROPPED | SEC-02-2-C-002 carries the qualifier "Tablo-351-5 kalite kontrol kriterleridir; dayanım sınıfının kendisi değil, kabul kriteridir"; only 3 of 9 of its anchors survive into the paragraph |
| `U-C-P01-S02` | UNSUPPORTED_PROPOSITION | content words ['kayaç', 'spesifik'] are licensed by none of the declared claims ['SEC-02-2-P0-008'] |


## Required Topic Coverage

| Topic | Covered | Required core claims |
|---|---|---|
| dayanım sınıfı | yes | SEC-02-2-C-001 |
| kaplama kalınlığı | yes | SEC-02-2-P0-007, SEC-02-2-P0-008 |
| çimento dozajı | yes | SEC-02-2-P0-001, SEC-02-2-P0-006, SEC-02-2-R001 |


3 / 3 required topics covered.


## Language Audit

| | |
|---|---|
| Section language | tr |
| Material units | 16 |
| Compliant material units | 16 |
| Compliance | 100% |
| Non-compliant units | none |


## Condition Audit

| | |
|---|---|
| Required conditions | 19 |
| Preserved | 19 |
| Preservation | 100% |
| Dropped | none |


## Qualifier Audit

| | |
|---|---|
| Required qualifiers | 2 |
| Preserved | 1 |
| Preservation | 50.0% |
| Semantic constraints satisfied | no |
| Dropped | SEC-02-2-C-002:Tablo-351-5 kalite kontrol kriterleridir; dayanım sınıfının kendisi değil, kabul kriteridir |


## Composition Audit

| | |
|---|---|
| Composition validations run | 16 |
| FORBIDDEN_SYNTHESIS | 0 |
| UNSUPPORTED_RELATION | 0 |
| DERIVED_VALUE_AS_SOURCE_STATED | 0 |
| CLAIM_NOT_ALLOWLISTED | 0 |
| CLAIM_DENYLISTED | 0 |
| All used claims composition-safe | yes |


## Citation Audit

| | |
|---|---|
| Material citation coverage | 100% |
| Uncited material units | none |
| Source keys used | 12 |
| References rendered | 0 |
| Packet EID leaks | not rendered |
| Claim id leaks | not rendered |
| Source key leaks | not rendered |


Bibliography behaviour is unchanged in this phase (§77): the frozen Book Citation Rendering Contract v1 and its renderer are used exactly as they are.


## Numeric Audit

| | |
|---|---|
| NUMERIC_DRIFT | 0 |
| UNIT_DRIFT | 0 |
| MODALITY_DRIFT | 0 |
| Numeric material units | 12 |
| 15 cm / 150 mm rule | PASS |
| 350 / 400 system relationship | PASS |
| C25/30 semantics | PASS |
| CF-P0-001 | PASS |
| SYN-001 | PASS |


## Rendered Pilot

Nothing was rendered. A draft is rendered only after it validates (§77, §80).


## Final Decision

**SEC-02-2 DRAFT FAILURE REMEDIATION V1 — CLOSED / GO; SEC-02-2 PILOT ATTEMPT #2 — REJECTED**


| Condition | Verdict |
|---|---|
| `bibliography_registry_backed` | NOT EVALUATED |
| `cf_p0_001_passes` | PASS |
| `citation_resolution_100` | PASS |
| `composition_safe_coverage` | PASS |
| `condition_preservation_100` | PASS |
| `derived_numeric_guard_passes` | PASS |
| `draft_ir_schema_valid` | PASS |
| `every_material_unit_claim_bound` | PASS |
| `every_material_unit_validates` | FAIL |
| `every_used_claim_allowlisted` | PASS |
| `internal_claim_id_leaks_zero` | NOT EVALUATED |
| `language_compliance_100` | PASS |
| `material_citation_coverage_100` | PASS |
| `no_claim_expansion` | PASS |
| `no_denylisted_claim_used` | PASS |
| `no_dropped_condition` | PASS |
| `no_dropped_qualifier` | FAIL |
| `no_language_ambiguity` | PASS |
| `no_language_mismatch` | PASS |
| `no_modality_drift` | PASS |
| `no_numeric_drift` | PASS |
| `no_semantic_scope_mismatch` | PASS |
| `no_unit_drift` | PASS |
| `no_unsupported_proposition` | FAIL |
| `packet_eid_leaks_zero` | NOT EVALUATED |
| `qualifier_preservation_100` | FAIL |
| `rendering_deterministic` | NOT EVALUATED |
| `required_topics_3_of_3` | PASS |
| `semantic_constraints_satisfied` | FAIL |
| `syn_001_passes` | PASS |
| `unknown_citations_zero` | NOT EVALUATED |


## Next Phase

SEC-02-2 DRAFT FAILURE ANALYSIS V2, using the exact attempt #2 failure codes recorded in the rejection artifact.


## Remaining Limitations

- The language detector is lexical and orthographic. It identifies Turkish and English, which is what this corpus contains; a third language would be reported as ambiguous and rejected on a material unit, which fails in the safe direction but is not detection.
- Non-material units are rejected only on confident English, not on ambiguity. A two-word heading carries too little evidence to demand positive proof from, so an English heading made only of domain terms would pass. No such heading exists in this section.
- Stage K's forbidden-meaning rule matches a syntactic shape - reference, attribution, and a class designation in predicate position after a strength-class noun. A paraphrase that asserts the same wrong thing without that shape would not be caught, and closing that gap needs semantic checking of a kind nothing here does.
- The qualifier-retention threshold inherited from v1 is still half of a qualifier's content anchors, a stated heuristic. DSC-C002-001 makes one specific qualifier's presence explicit rather than statistical; the general threshold is unchanged and still unproven.
- Cross-lingual condition mappings are registered per claim, by hand. Three exist. Scaling to a whole book means either many more hand-registered mappings or a different mechanism, and this phase is not evidence about which.
- One remediated attempt is not evidence that the drafting architecture scales, and an accepted pilot is not publishable text. Human technical editorial review has not happened.
