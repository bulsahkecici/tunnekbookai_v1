# Controlled Canonical Promotion Milestone

Date: 2026-09-08

## 1. Inspected

The active Book Production Engine foundation, Unified Ingest contracts, source/original/
processing/staging artifacts, audit ledgers, chunk identity algorithm, preliminary book
canonical validator, promotion helper, architecture gate and live ignored data were
inspected before implementation.

## 2. Previous state

Canonical was the valid empty bootstrap state, but no active authority could admit an
eligible staged document. `scripts/promote_staging.py` copied only to a non-canonical
location and deliberately refused `corpus/canonical/`. Book status had a preliminary
manifest validator that would have competed with a production implementation.

## 3. Architecture decision

`tunnelbookai.canonical` is now the sole plan/apply/verify/status authority. It uses one
deterministic manifest at `corpus/canonical/canonical_manifest.json` and immutable,
content-addressed objects under `corpus/canonical/objects/<document_id>/<document_digest>/`.
The manifest replacement is the all-or-nothing authority commit point.

## 4. Implemented

- strict cross-artifact eligibility over original, processing, staging, ingest ledgers,
  metadata, provenance, classification, document quality and chunks;
- deterministic `CCP_<sha256>` plans and exact-ID approval;
- stale-plan rebuilding under an exclusive apply lock;
- immutable canonical copies and per-chunk semantic checksum ledgers;
- deterministic document and corpus digests;
- atomic object materialization, manifest replacement and controlled rollback;
- pending/final apply-attempt audits;
- independent `EMPTY`, `READY`, `INVALID` verification;
- book-status delegation to the same verifier;
- explicit separation of empty-reset and active isolation/production gates.

## 5. Files created

- `tunnelbookai/canonical/`: models, hashing, paths, eligibility, verifier, promotion and CLI.
- `tests/canonical/`: isolated synthetic fixtures and 26 safety/integrity tests.
- `docs/canonical_promotion_contract.md`: normative contract.
- this milestone report.

## 6. Files modified

The ingest path/staging contracts expose safe root injection and public staging sidecars;
the root promotion script is now a non-owning compatibility shim; book status uses the
canonical verifier; the reset quality gate exposes separate empty-reset and isolation
modes; architecture, ingest, chunking, book and root documentation describe the new
boundary. Historical reset and foundation records remain intact.

## 7. Canonical manifest contract

The manifest records schema/contract identity, exact document/chunk totals, sorted
document records and `canonical_corpus_digest`. Each record binds the source, original,
processing, staging and ingest-ledger identities to canonical file hashes, quality,
classification, provenance, chunk ledger, document digest and admitting plan. It includes
no source content, absolute path, mtime or timestamp.

## 8. Safety guarantees

Planning never mutates canonical. Apply requires a matching plan ID and fails stale before
mutation. Originals, processing and staging are opened read-only and never moved or
cleaned. Paths are project-relative, root-confined, regular and non-symlinked. Multi-document
plans commit together through the manifest. Existing identities are no-op, conflicting IDs
or source hashes fail closed, and retrieval is permitted only for verified `READY` state.

## 9. Tests

Verification results in the real local environment:

- canonical tests: **26 — OK**;
- book tests: **14 — OK**;
- ingest tests, including LibreOffice/OCR adapters: **214 — OK**;
- complete active discovery: **254 — OK**;
- compileall: **PASS**;
- `git diff --check`: **PASS**;
- active architecture isolation gate: **GO**.

## 10. Results

The canonical CLI, manifest contract, independent verifier, book integration and safety
tests are implemented. No retrieval index, embedding, vector store, evidence audit, prose
or book artifact was created.

## 11. Live dry-run

The live candidate was planned without applying:

```text
plan_id: CCP_c89c16e1bde1cd0254134425107babed68225f77b935551204a088530426729f
document_id: ING_b6a2b2e47753afe8699c
source_sha256: b6a2b2e47753afe8699c10da551fe4afc311dcac8f4504a34c8e83d71fd157c8
action: PROMOTE
chunk_count: 385
retrieval_ready_chunk_count: 385
applicable: true
```

Canonical file inventory was empty before and after planning. Independent verification
continued to report `EMPTY`; no apply was run.

## 12. Current readiness

Canonical promotion and verification are operational. The live canonical corpus remains
deliberately `EMPTY`, so retrieval remains disallowed until the operator reviews and
explicitly approves the exact live plan.

## 13. Remaining blockers

- explicit operator approval/apply of an eligible plan;
- Book Retrieval Layer V1 after canonical reaches verified `READY`.

## 14. Exact next milestone

**Book Retrieval Layer V1** — a reproducible derivative index consuming only a verified
canonical snapshot. It must not read staging or processing directly.

The exact reviewed apply command, not executed during this milestone, is:

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical apply \
  --plan audit/canonical_promotions/plans/CCP_c89c16e1bde1cd0254134425107babed68225f77b935551204a088530426729f.json \
  --approve CCP_c89c16e1bde1cd0254134425107babed68225f77b935551204a088530426729f
```
