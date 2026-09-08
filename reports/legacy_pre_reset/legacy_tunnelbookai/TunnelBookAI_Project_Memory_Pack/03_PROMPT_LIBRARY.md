# TunnelBookAI – Prompt Library

## Normal New Phase

```text
Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Follow AGENTS.md.
Execute NEXT_PHASE exactly.

Use targeted reads/tests only.
Do not commit or push.
```

## Phase Identity Guard

```text
Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Follow AGENTS.md.

Confirm NEXT_PHASE is:
<EXACT_PHASE_NAME>

If it matches, execute that phase exactly.
If not, STOP and report the mismatch.

Use targeted reads/tests only.
Do not scan the corpus.
Do not commit or push.
```

## Technical Audit

```text
Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Follow AGENTS.md.

Confirm NEXT_PHASE is:
<TECHNICAL_AUDIT_PHASE>

If it matches, execute that phase exactly.

Audit only the authorized accepted draft.
Do not regenerate or rewrite it.
Do not scan the corpus.
Do not modify frozen historical artifacts.
Do not commit or push.

Focus on:
- technical correctness
- factual completeness
- claim-to-citation support
- scope fidelity
- terminology consistency
- sentence and paragraph quality
- ambiguity and redundancy
- prior blocker preservation
- new blockers

Return only:
- status
- blocking findings
- advisory findings
- blocker status
- citation/support status
- scope/terminology status
- release recommendation
- tests/probes
- changed files
- next phase

Final <= 220 words.
```

## Failure Analysis

```text
Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Follow AGENTS.md.

Confirm NEXT_PHASE is:
<FAILURE_ANALYSIS_PHASE>

If it matches, execute that phase exactly.

Analyze only preserved failure evidence.
Do not rewrite/regenerate.
Do not scan the corpus.
Do not weaken validators.
Do not commit or push.

Determine root cause per finding:
- realization contract
- style integration
- terminology allocation
- renderer
- validator coverage gap
- other evidenced cause

Specify the smallest general remediation.
No claim-specific patch.

Return only:
- status
- root cause per finding
- validator fault yes/no
- renderer fault yes/no
- style-contract fault yes/no
- smallest remediation
- tests/probes
- changed files
- next phase

Final <= 220 words.
```

## State Reconciliation Pattern

```text
Follow AGENTS.md.

This is state reconciliation only.

Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Then read only the authoritative artifacts for:
<COMPLETED_PHASE>

Verify the phase completed GO.

Do NOT rerun the phase.
Do NOT regenerate/render.
Do NOT scan the corpus.
Do NOT modify historical artifacts.
Do NOT commit or push.

If authoritative artifacts confirm GO:
Update only:
- docs/ai/CURRENT_STATE.md
- docs/ai/NEXT_PHASE.md

CURRENT_STATE must record the phase as CLOSED / GO.

NEXT_PHASE must become exactly:
<NEXT_PHASE>

If evidence does not support this:
make no changes and report mismatch.

Return only:
- status
- evidence checked
- state docs changed
- resulting NEXT_PHASE

Final <= 150 words.
```

## LAST PROMPT GIVEN — NOT YET RUN

Bu kullanıcı tarafından “aklında tut” denilen son prompttur.

```text
Follow AGENTS.md.

This is state reconciliation only.

Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Then read only the authoritative artifacts for:

SEC-02-2 TECHNICAL DRAFT RE-AUDIT V3

Verify that V3 actually completed GO with:

- no blocking findings
- six blockers 6/6 CLOSED
- citation/support 19/19 PASS
- conditions 25/25
- dependencies 2/2
- unresolved Swelling Rock fallback preserved
- terminology/scope PASS
- validator histogram {}
- release recommendation = RELEASE
- accepted draft unchanged

Do NOT rerun V3.
Do NOT regenerate/render anything.
Do NOT scan the corpus.
Do NOT modify historical artifacts.
Do NOT commit or push.

If authoritative V3 artifacts confirm GO:

Update only:
- docs/ai/CURRENT_STATE.md
- docs/ai/NEXT_PHASE.md

CURRENT_STATE must record:

SEC-02-2 TECHNICAL DRAFT RE-AUDIT V3 = CLOSED / GO

NEXT_PHASE must become exactly:

SEC-02-2 RELEASE AUTHORISATION V1

Preserve the two V3 advisories as non-blocking advisories.

If evidence does not support this transition:
make no changes and report the mismatch.

Return only:
- status
- evidence checked
- state docs changed
- resulting NEXT_PHASE

Final <= 150 words.
```

## Release Authorisation Template

State reconciliation başarıyla tamamlandıktan sonra:

```text
Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Follow AGENTS.md.

Confirm NEXT_PHASE is:
SEC-02-2 RELEASE AUTHORISATION V1

If it matches, execute that phase exactly.

Use only:
- accepted V2.2 general-closure rerun draft
- Technical Draft Re-Audit V3
- frozen release/citation/style/technical evidence required by NEXT_PHASE

Do not regenerate or rewrite the draft.
Do not scan the corpus.
Do not modify frozen historical artifacts.
Do not commit or push.

Release only if all required gates remain satisfied:
- V3 re-audit GO
- 6/6 blockers closed
- citation/support PASS
- factual completeness PASS
- scope/terminology PASS
- condition/dependency closure PASS
- unresolved-term fallback PASS
- Book Style PASS
- validator histogram {}
- accepted draft hash unchanged

Preserve advisory findings as advisories.

Return only:
- status
- release decision
- release gates
- draft/hash identity
- unresolved advisories
- frozen integrity
- changed files
- next phase

Final <= 200 words.
```
