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

The CLI declares `assemble` as a future command. Until its contract is implemented it
returns structured `NOT_IMPLEMENTED` with a non-zero exit status. This is intentional: no
placeholder artifact or unsupported book is created.

`build-index` and `search` now implement Book Retrieval Layer V1. The index consumes only
the independently verified canonical manifest and its admitted `embedding_ready.jsonl`
members. It stores normalized float32 vector shards under `book/retrieval/indexes/` and
atomically publishes `book/retrieval/index_manifest.json` only after full coverage and hash
verification. The manifest binds the derivative index to the canonical corpus digest,
canonical manifest hash, exact local embedding model and frozen book-input identities.

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book build-index --batch-size 32
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book search \
  --query "tünel yapım maliyeti" --section 6 --top-k 10
```

Interrupted builds are resumable by default. No cloud endpoint, model fallback, staging or
processing artifact is accepted as retrieval evidence.

Retrieval is hybrid (`hybrid-rrf-v1`). After the dense index is published, `build-index`
also builds a BM25 lexical index over the same rows under `book/retrieval/lexical/<BRI_id>/`
(Turkish fold before NFKD, F5 prefix stemming, broken-letter-spacing repair, per-row noise
flags). `search` and the audit retriever fuse the dense and lexical rankings with
reciprocal-rank fusion, scale by chunk-type weight (TEXT 1.0 … FIGURE 0.6) and exclude rows
shorter than 150 characters or table-of-contents like. The policy is recorded in every
result and audit identity. The lexical index is a derivative bound to the dense index id
and never becomes evidence authority.

`evidence-audit` implements the pre-writing audit. It retrieves from the complete verified
canonical index with the hybrid retriever (query = section title + question, top-k 8 after
overlap de-duplication), sends Qwen the query-focused ~1,000-character window of each chunk
rather than its prefix (structure-aware chunks start with the previous chunk's tail), asks
the exact configured local Qwen model to classify each frozen question as `SUPPORTED`,
`PARTIAL` or `UNSUPPORTED`, and preserves deterministic retrieval provenance (dense and
lexical ranks) for every result. Section readiness is derived from the contract coverage
ratio (`ceil(questions × 0.6)`); sections flagged `HUMAN_ANALYSIS_ARTIFACT_REQUIRED` in the
scope keep that state regardless of literature support. Section checkpoints are atomic and
a repeated command resumes from the last valid section.

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book evidence-audit \
  --all --batch-size 8 --top-k 8
```

The active machine-readable summary is
`audit/book/prewriting_evidence_audit.json`; the complete question-level output is stored
under its content-addressed audit directory, and the operator summary is
`reports/prewriting_evidence_audit.md`.

`prepare` turns the completed audit into immutable, content-addressed section evidence
packets and canonical claim registries. Only evidence explicitly selected by the Qwen
audit is admitted. `UNSUPPORTED` questions receive no allowed claim; `PARTIAL` questions
are restricted to qualified drafting. Every registered claim stores the exact canonical
passage, document/chunk identity, locator, text digest and linked question IDs.

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book prepare --all
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book prepare --section 1.1
```

The active preparation manifest is `book/production/preparation/manifest.json`; its
content-addressed packets contain `evidence_packet.json` and `claim_registry.json`.
`reports/section_preparation.md` is the operator summary.

`write` implements a resumable, local-Qwen, outline-first section writer. It admits only
questions marked `SUPPORTED` or `PARTIAL` and resolves all model references against the
prepared claim registry. Pass one asks Qwen for a section plan: 2–8 ordered themes, each
owning a subset of the registered passages and the questions it addresses (off-topic
passages such as tables of contents are simply left out of every theme). Pass two writes
each theme as connected paragraphs from that theme's passages only, so the draft reads in
chapter order rather than as a sequence of question answers. Every sentence must cite at
least one claim; its question links are the union of Qwen's explicit tags and the eligible
questions those claims were retrieved for, so coverage auditing keeps working without
forcing question-shaped prose. The plan and each theme have atomic checkpoints. The
resulting Markdown remains `DRAFTED_UNAUDITED` until the downstream evidence, coverage and
editorial gates pass.

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book write \
  --section 1.1 --batch-size 8
```

Drafts are content-addressed under `book/production/drafts/`; each contains `section.md`,
`sentence_map.json`, a manifest (with the theme plan) and resumable plan/theme checkpoints.
Active draft pointers
are under `book/production/drafts/active/` and appear in `book status`.

`evidence-review` independently asks local Qwen whether each drafted sentence is actually
entailed by its mapped canonical passages. Cross-sentence claim selection is rejected; a
failed batch is recursively split down to a single sentence when necessary. Results are
`SUPPORTED`, `PARTIAL`, `UNSUPPORTED` or `NON_FACTUAL_OR_EDITORIAL`. Any partial or
unsupported sentence places the section on `AUDIT_HOLD` for revision.

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book evidence-review \
  --section 1.1 --batch-size 12
```

Machine audits are under `audit/book/postwriting/`; human issue reports are written as
`reports/postwriting_evidence_review_<section>.md`.

`coverage-audit` evaluates all 50 frozen questions against real draft sentence spans and
the accepted post-writing evidence chain. `ANSWERED` is possible only with independently
`SUPPORTED` sentences and complete claim/document/locator provenance. A model answer based
on a `PARTIAL` sentence is conservatively downgraded to `PARTIAL`; a reference-free partial
answer becomes `NOT_ANSWERED`.

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book coverage-audit \
  --section 1.1 --batch-size 10
```

Machine results are under `audit/book/coverage/`; human summaries are written as
`reports/question_coverage_<section>.md`. Partial answers never count toward coverage.

`revise` performs one bounded, immutable evidence-first revision after a sentence audit
returns `REVISION_REQUIRED`. It removes `PARTIAL` and `UNSUPPORTED` sentences instead of
inventing replacement prose. It also merges only high-similarity repetitions that share a
canonical claim, preserving the union of their existing question/claim provenance. The
contract limit of two revisions is enforced, the previous draft remains write-once, and
the new active draft is always `DRAFTED_UNAUDITED` until both downstream audits are rerun.

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book revise --section 1.1
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book evidence-review --section 1.1 --batch-size 12
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book coverage-audit --section 1.1 --batch-size 10
```

`editorial-audit` runs an objective deterministic hard gate and stores a separate local-Qwen
advisory review. The deterministic gate verifies exact draft/sentence-map agreement, ID and
Unicode integrity, complete prose termination, and absence of exact paragraph/sentence or
consecutive-word duplication. Qwen may report chronology, naming, language, synthesis or
structure advice, but its subjective result cannot independently reject an evidence-valid
section or introduce external corrections.

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book editorial-audit --section 1.1
```

`approve-section` records that a person read the exact audited draft and accepts it as a
book section. The approval is bound to the draft id, the Markdown hash and the editorial
audit id; any rewrite, revision or re-audit invalidates it. The machine gates prove evidence
and structure — they cannot prove the text reads as a chapter, which is why the contract's
`OPERATOR_READ_APPROVAL_PASS` requirement exists.

`freeze` independently verifies every Book Contract freeze requirement (including the
operator approval), reconstructs the sentence-to-claim/document/locator chain, and writes a
content-addressed, read-only snapshot of the section, sentence map, audits, claim registry,
evidence packet and approval record. Repeated execution is idempotent. A valid active
freeze blocks both `write` and `revise`; no unfreeze operation exists.

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book approve-section \
  --section 1.1 --note "Read end to end; acceptable as a book section."
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book freeze --section 1.1
```

`status` is read-only. It reports book-input identities, canonical inventory, retrieval
readiness, section counts and publication blockers. A non-empty canonical root without a
valid manifest is `INVALID`; an empty canonical root is the valid bootstrap state `EMPTY`
but is not ready for writing.

## Recovery and resume policy

Revisions create write-once, content-addressed drafts containing verified artifact hashes.
Every edit invalidates the sentence map, evidence audit and question coverage audit; all
must be rebuilt. A failed revision leaves the previously active hash-verified draft intact.
Frozen sections remain immutable because no controlled unfreeze operation exists.

## Controlled canonical promotion

`tunnelbookai.canonical` is the sole authority for deterministic plan creation, exact-plan
approval, stale-plan rejection, content-addressed canonical materialization and independent
disk verification. Apply retains originals, processing and staging and atomically commits
the complete active evidence set through `corpus/canonical/canonical_manifest.json`.

`EMPTY` remains a valid non-retrievable bootstrap state. `READY` requires a non-empty,
hash-verified manifest and every referenced document/chunk artifact. `INVALID` fails
closed. Book status consumes this same validator.

## Next milestone

The retrieval index, benchmark, pre-writing audit and all 59 constrained section evidence
packets/claim registries are complete. The local Qwen writer, bounded revision, editorial
audit and hash-verified freeze contracts are implemented and verified with section 1.1.
The frozen pilot has a passing sentence-evidence audit and 34/50 answered-question coverage.
The next milestone is to use the frozen pilot as the operating pattern for evidence-ready
sections while remediating corpus gaps; deterministic book assembly remains `NOT_IMPLEMENTED`.
