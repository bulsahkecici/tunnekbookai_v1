# SEC-02-2 ARCHITECTURE V2 PILOT #1 AUTHORISATION

**Phase CLOSED / GO. ARCHITECTURE V2 PILOT #1 — REJECT.** One generation, rejected at plan validation before any prose was rendered. No repair, no regeneration.


## Pre-generation gates

| Gate | Result |
|---|---|
| 1 frozen inputs (15 checked) | drift 0 |
| 2 acceptance contract `c9766e437bd00222…` | unamended True |
| 3 static containment proof | PASS, universe reproduced True |
| 4 planner option set | 46 REALIZABLE pairs, 0 UNREALIZABLE exposed |
| 5 feasibility | True, 23 units, topics 3/3 |
| 6 known limitations block a pilot | False |
| **generation authorised** | **True** |


## The generation

One call to `qwen3.6-35b-a3b-mlx`, temperature 0.0, seed 11, finish `stop`, 1826 completion tokens. Raw bytes preserved, SHA256 `6cad69f48ec2ec4e5b630e11a693fbd101b01c543a2db8f1d93c09059d3bc194`.


## What the planner produced

25 slots across 16 claims, 4 subsections, 16 paragraphs.

Roles: `{'CLAIM_STATEMENT': 12, 'CONDITION': 7, 'QUALIFIER_SCOPE': 2, 'REQUIREMENT': 4}`

**Prose fields emitted: 0.** The plan carried only the declared field names: `claim_id, language, paragraph_groups, paragraph_id, plan_id, plan_version, realization_role, section_id, slot_id, slots, subsection_id, subsections`.


## The rejection

One failure, code `PLAN_ROLE_UNREALIZABLE`, plan_validation, before any prose was rendered.

**Attributed to: PRE_GENERATION_GATE_OPTION_SET_DEFECT.** Gate 4 exposed SEC-02-2-C-005 with requires_condition_slot: true and an available_roles list that omits CONDITION, because C-005's CONDITION role is UNREALIZABLE — its registered condition is not Turkish and has no frozen gloss frame. The option set demanded a role it did not offer. The planner followed the stated rule, allocated the slot, and plan validation rejected it. Gate 5's feasibility builder had already skipped C-005 for the same reason, so the two gates disagreed and only one was shown to the model.

Not attributed to:

- the model emitting prose — it emitted none
- a containment failure — no prose was rendered
- a validator defect — plan validation caught the selection correctly

What held:

- the planner emitted no prose field of any kind; only the 12 declared field names
- the plan parsed against the frozen schema without repair
- every other selected claim/role pair was REALIZABLE
- the single invalid selection was caught before rendering, not after
- no prose was rendered, so no containment question arose


## Feasibility, for the record

A deterministic full-section plan validates and renders clean. The section is reachable under Architecture V2; this pilot's rejection is about the option set shown to the planner, not about the architecture's reach. The deterministic plan renders 23 units across 15 claims, covers 3/3 required topics, and validates `ACCEPT` with an empty histogram.


## Counts

| | |
|---|---|
| automatic retries | 0 |
| corpus reads | 0 |
| frozen artifacts modified | 0 |
| generation calls | 1 |
| lexicons widened | 0 |
| post render model calls | 0 |
| qdrant writes | 0 |
| regenerations | 0 |
| repairs | 0 |
| retrieval calls | 0 |
| validators weakened | 0 |
| rendered draft | NONE |
| released draft | NONE |


## Route

**ARCHITECTURE V2 PILOT FAILURE ANALYSIS V1.** Regeneration is not authorised. `Attempt #4` remains a retired identifier, and a second Architecture V2 pilot becomes reachable only if that analysis authorises one on its own evidence.

