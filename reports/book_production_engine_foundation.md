# Book Production Engine V1 — Foundation Milestone

Date: 2026-09-08

## 1. Inspected

The audit covered the active README and architecture/ingest/chunking contracts; reset
reports; book scope, question bank, integrity artifacts and schemas; all active
configuration; root scripts; `shared/`; `tunnelbookai/`; active corpus/input/output
roots; and the current Git state. Selected legacy book-pipeline, revision-state and test
files were read only to understand earlier traceability and rollback ideas. No legacy
file was imported, executed or copied into the active runtime.

## 2. Architecture discovered

Unified Ingest remains authoritative for source admission, immutable originals,
extraction, metadata, provenance, classification, deduplication, quality, chunking and
staging. `scripts/promote_staging.py` can only copy eligible bundles to a non-canonical
target and explicitly refuses `corpus/canonical/`; therefore final controlled canonical
promotion is not yet implemented.

The live ignored data roots now contain one original bundle, one processing bundle and
one staging bundle. These are valid post-reset ingest outputs and were left untouched.
`corpus/canonical/` contains zero evidence documents. The reset-only quality gate reports
`NO_GO` because the repository is no longer in an empty bootstrap state; architecture,
script allow-list and legacy-isolation checks still pass.

`config/models.yaml` remains the exact model authority. The real-environment capability
probe returned `AVAILABLE` for both configured loopback models: the embedding response is
stable at 1,024 values and the structured LLM probe passed. No fallback was attempted.

## 3. Changed

- Added a canonical Book Contract with frozen authority hashes and validated policy for
  structure, coverage, evidence, citations, local models, analysis artifacts, section
  readiness, revision/freeze behavior and publication.
- Added typed semantic states, answer-span records, claim records and strict reference
  validation.
- Added a deterministic central loader that validates the complete 66/59/2,950 input
  graph, source files, integrity audit, index mappings, SHA-256 identities and exact
  local/loopback model policy.
- Added central global and section coverage mathematics. `PARTIAL` contributes zero;
  publication requires a complete audit plus both 1,770 answers and 60% coverage.
- Added read-only, canonical-root-only evidence inventory. Empty canonical is represented
  truthfully as `EMPTY`; non-canonical paths are rejected.
- Added a module CLI for validation and status. Every future production command currently
  returns structured `NOT_IMPLEMENTED` and creates no artifact.
- Aligned active audit schemas, helper status names and evidence-audit prompts with the
  Book Contract.
- Isolated the empty-reset test from live ignored ingest data so it tests a synthetic
  empty layout without deleting operator data.

No book prose, retrieval index, evidence audit, draft, freeze or assembled book was
generated.

## 4. Files created

- `book/config/book_contract.json`
- `docs/book_production_engine.md`
- `tunnelbookai/book/__init__.py`
- `tunnelbookai/book/__main__.py`
- `tunnelbookai/book/canonical.py`
- `tunnelbookai/book/cli.py`
- `tunnelbookai/book/contract.py`
- `tunnelbookai/book/coverage.py`
- `tunnelbookai/book/errors.py`
- `tunnelbookai/book/inputs.py`
- `tunnelbookai/book/models.py`
- `tunnelbookai/book/stages.py`
- `tunnelbookai/book/status.py`
- `tests/book/__init__.py`
- `tests/book/test_foundation.py`
- `reports/book_production_engine_foundation.md`

## 5. Files modified

- `README.md`
- `book/README.md`
- the three active schemas under `book/audits/schemas/`
- `book/tools/validate_book_inputs.py`
- `docs/architecture.md`
- `shared/book_qa.py`
- `shared/prompts/generic_section_audit.txt`
- `shared/prompts/generic_section_audit_v2.txt`
- `tests/ingest/test_reset_architecture.py`

## 6. Tests and commands run

- `python -m tunnelbookai.book validate --json`
- `python -m tunnelbookai.book status`
- compatibility book-input validator and taxonomy integration audit
- compile check for new/modified Python modules
- foundation unit tests
- complete test discovery under `tests/` outside filesystem confinement, as required by
  macOS LibreOffice/native OCR coverage
- exact local model capability probe
- reset-only repository quality gate
- `git diff --check`

## 7. Results

- Book input validation: **PASS** — 66 headings, 59 question sections, 2,950 questions.
- Foundation tests: **14 tests — OK**.
- Complete active suite: **228 tests — OK**.
- Git whitespace validation: **PASS**.
- Exact local model capability: **AVAILABLE** — stable 1,024-value embedding and successful
  structured LLM response. (The restricted sandbox cannot reach the loopback service; the
  authoritative probe was therefore run in the real local environment.)
- Reset-only empty-corpus gate: **NO_GO**, expected for the current populated
  original/processing/staging state; canonical remains empty and all legacy-isolation
  checks pass.

## 8. Current book-production readiness

The policy and input-validation foundation is ready. Canonical document count is zero,
retrieval is not implemented, all 66 headings are `NOT_STARTED`, frozen count is zero,
and zero questions have been pre- or post-writing audited. Publication eligibility is
**false**.

## 9. Remaining blockers

- No controlled, manifest-producing promotion into `corpus/canonical/` exists.
- Canonical evidence is empty.
- Retrieval, evidence readiness, packet construction, writing, post-writing audits,
  checkpoint/rollback/freeze and assembly remain explicitly `NOT_IMPLEMENTED`.
- Global 2,950-question coverage has not been run; no publication status can be claimed.

## 10. Exact next implementation task

Implement the controlled canonical promotion milestone and canonical manifest contract.
It must consume only eligible Unified Ingest staging bundles and provide dry-run planning,
explicit apply approval, original/chunk/provenance SHA verification, dedup and quality
verification, atomic/idempotent materialization, a deterministic corpus digest, and a
complete audit manifest. Retrieval should remain blocked until this authority passes its
tests.
