# Post-reset Repository Alignment

Date: 2026-09-08

## Outcome

The active repository surface is aligned with the empty-corpus Unified Ingest
architecture. Historical implementation material remains recoverable under
`archive/legacy_pre_reset/`, but it is outside active test discovery and supported
operator paths.

## Active operator commands

- `scripts/ingest_incoming.py`
- `scripts/probe_models.py`
- `scripts/promote_staging.py`
- `scripts/reset_legacy_state.py`

## Changes

- Moved pre-reset corpus, embedding, retrieval, Qdrant and book-generation scripts into
  the explicit legacy archive.
- Moved legacy documentation and configuration into the same archive.
- Archived the duplicate `tunnelbookai_v1_book_inputs` package; `book/` remains the sole
  scope and question-bank authority.
- Migrated metadata vocabularies and deterministic inference helpers from the legacy
  script tree into `tunnelbookai.ingest.metadata.vocabularies`.
- Removed the retired metadata model configuration. `config/models.yaml` is now the only
  active exact-model authority.
- Corrected the manual-input documentation to point at
  `incoming/papercrawler/releases/`.
- Expanded the reset gate to reject active legacy topology and runtime references.

`data/downloads/` remains intentionally retained as the recoverable source archive.
Historical reports and audits remain preserved as historical evidence.

## Verification

- `shared/project_quality_gate.py`: **GO**
- Active legacy paths: **0**
- Active legacy runtime references: **0**
- Supported root scripts: **4**
- Archived historical scripts: **138**
- Book input validation: **PASS** — 59 sections and 2,950 questions
- Exact local model capability: **AVAILABLE** — 1,024-value stable embedding and
  successful structured LLM response
- Active ingest suite in the real macOS environment: **207 tests — OK**
