# TunnelBookAI – Architecture and Invariants

## Frozen Pipeline Snapshot

### Corpus
- canonical documents: 214
- semantic chunks v1.1: 6039
- embedding input: 5992
- canonical embedding rows: 5980
- recovery rows: 12

### Embeddings
- BGE-M3
- dimension 1024
- Qdrant `tunnelbook_dense_v1`
- cosine

### Retrieval
- dense-only
- hybrid/translation/reranker empirically rejected
- Retriever V1 CLOSED / GO
- RAG Context CLOSED / GO

### Generation
- local model: `qwen3.6-35b-a3b-mlx`
- Prompt v5 frozen
- no Prompt v6 without separate experiment
- production grounded generator frozen

## Book Architecture

Evidence:
- source registry
- evidence notes
- research questions/runs
- section bundles
- claim ledgers
- citation allocation

Drafting:
- semantic plan IR
- claim realization contract
- deterministic morphology
- deterministic renderer
- static containment proof
- Book Style Contract
- validators

General closures:
- condition ownership
- dependency ownership
- semantic subject/predicate binding
- complete-sentence feasibility
- preferred-term allocation
- no free variants
- material note-label exclusion
- unresolved original-language fallback

## Critical Invariants

1. Frozen upstream artifacts immutable.
2. Wrong metadata worse than blank.
3. Evidence-only; unresolved allowed.
4. Provenance/citations preserved.
5. No hallucinated repair.
6. No model-generated gold.
7. Dev/eval separated.
8. No self-judge as sole authority.
9. Never weaken validators just to pass.
10. Evidence is untrusted data.
11. Contract failure → reject.
12. No same-config retry.
13. No automatic rewrite/translate/repair.
14. Corrections create new versions; history preserved.
15. Qdrant read-only except explicit indexing.
16. Book source policy defaults to corpus_only.
17. Packet-local `[E###]` IDs are not stable public refs.
18. Acceptance criteria freeze before outcome.
19. Script slots collision-check.
20. Qdrant unreachable → unknown/unobserved.
21. AI review is not human/manual review.
22. Pilot prose ≠ final manuscript.
23. Citation support must prove claim→source association.

## Original-Language Technical Term Policy

States:
- `AUTHORITATIVE_TRANSLATION`
- `ORIGINAL_TERM_UNRESOLVED`

For unresolved terms:
- exact source term retained semantically
- authoritative translation = null
- presentation = bold
- example: `**Swelling Rock**`
- no invented Turkish translation
- no explanatory gloss
- markup excluded from semantic ownership
- future replacement centralized + versioned

## SEC-02-2 Position

Current accepted surface passed:
- 6/6 blocker closures
- 25/25 conditions
- 2/2 dependencies
- citation support
- factual completeness
- Book Style
- terminology consistency
- unresolved fallback
- deterministic rendering

Release Authorization is pending because of state synchronization, not because the draft failed.
