# Book Production Engine V1

## Purpose and authority boundary

TunnelBookAI produces a defensible technical book; it is not a generic RAG chatbot.
The authoritative outline and question bank remain frozen under `book/scope/` and
`book/question_bank/`. The Book Production Engine cannot add, remove or infer headings.

Unified Ingest remains the sole owner of extraction, metadata, provenance,
classification, deduplication, quality and chunking. Book production reads only evidence
that has passed a separately controlled promotion into `corpus/canonical/`. Files under
`incoming/`, `processing/`, `corpus/staging/`, `archive/` and the internet are never
silent book evidence.

## Book Contract

`book/config/book_contract.json` is the single machine-readable policy authority. Its
validator is `tunnelbookai.book.contract`. The contract freezes:

- 7 top-level chapters, 66 structural headings and 59 question-bank subsections;
- 50 questions per question subsection and 2,950 questions overall;
- the SHA-256 identities of normalized inputs, integrity audit and source manifest;
- the global publication hard gate and the preferred section target;
- evidence, citation, model, analysis-artifact, revision, freeze and publication rules.

Exact model identifiers are deliberately not duplicated in the Book Contract.
`config/models.yaml` remains their sole authority; the contract pins that file's identity
and requires local, loopback-only endpoints with no fallback or model substitution.

## Coverage contract

Every post-writing question evaluation has exactly one semantic state:

| State | Publication coverage contribution |
| --- | ---: |
| `ANSWERED` | 1 |
| `PARTIAL` | 0 |
| `NOT_ANSWERED` | 0 |

An `ANSWERED` record is rejected unless it identifies an actual paragraph or sentence
span and supporting claim IDs, document IDs and source locators. Publication requires a
complete 2,950-question audit, at least 1,770 `ANSWERED` results, and coverage of at least
0.60. The preferred section target is 30/50; it is explicitly not a V1 hard gate.

## Evidence and section lifecycle

Pre-writing evidence uses `SUPPORTED`, `PARTIAL` or `UNSUPPORTED`. That audit asks whether
canonical evidence can answer a question. The post-writing audit separately asks whether
the written section actually answers it.

The declared lifecycle is:

```text
canonical manifest
  -> retrieval index
  -> pre-writing evidence audit and gap report
  -> constrained section evidence packet and claim registry
  -> local section writer
  -> sentence map and evidence audit
  -> question coverage audit
  -> editorial audit and bounded revision
  -> hash-verified checkpoint / rollback
  -> section freeze
  -> deterministic assembly
  -> complete global coverage and consistency audits
```

A section may be `READY`, `READY_WITH_LIMITATIONS`, `EVIDENCE_GAP`,
`HUMAN_ANALYSIS_ARTIFACT_REQUIRED` or `BLOCKED`. Literature may not stand in for absent
project analysis, and the model may not invent project findings.

## Current foundation and canonical commands

```bash
python -m tunnelbookai.book validate
python -m tunnelbookai.book status
python -m tunnelbookai.canonical status
python -m tunnelbookai.canonical plan --document-id ING_...
python -m tunnelbookai.canonical verify
```

The CLI also declares the future commands `build-index`, `evidence-audit`, `prepare`,
`write`, `evidence-review`, `coverage-audit`, `editorial-audit`, `freeze` and `assemble`.
At the foundation milestone each returns structured `NOT_IMPLEMENTED` with a non-zero exit
status. This is intentional: no placeholder artifact, fake audit or unsupported prose is
created.

`status` is read-only. It reports book-input identities, canonical inventory, retrieval
readiness, section counts and publication blockers. A non-empty canonical root without a
valid manifest is `INVALID`; an empty canonical root is the valid bootstrap state `EMPTY`
but is not ready for writing.

## Recovery and resume policy

Future revisions must create write-once checkpoints containing verified artifact hashes.
Every edit invalidates the sentence map, evidence audit and question coverage audit; all
must be rebuilt. A failed revision restores only the last evidence-valid checkpoint and
verifies the restored hashes. Frozen sections are immutable until an explicit controlled
unfreeze/revision operation exists.

## Controlled canonical promotion

`tunnelbookai.canonical` is the sole authority for deterministic plan creation, exact-plan
approval, stale-plan rejection, content-addressed canonical materialization and independent
disk verification. Apply retains originals, processing and staging and atomically commits
the complete active evidence set through `corpus/canonical/canonical_manifest.json`.

`EMPTY` remains a valid non-retrievable bootstrap state. `READY` requires a non-empty,
hash-verified manifest and every referenced document/chunk artifact. `INVALID` fails
closed. Book status consumes this same validator.

## Next milestone

**Book Retrieval Layer V1**: implement a reproducible derivative index over only a verified
canonical snapshot. Embeddings, retrieval and pre-writing evidence audits remain
`NOT_IMPLEMENTED` in the canonical-promotion milestone.
