# Corpus Population Contract V1

## Boundary

`tunnelbookai.population` is the single-writer orchestration and accounting layer for
`incoming/manual/inbox/` and accepted PaperCrawler schema-2.x releases. It reuses Unified
Ingest unchanged for conversion, extraction, metadata, provenance, classification, quality
and chunking. It never writes canonical evidence, generates embeddings, builds retrieval or
synthesizes canonical approval.

The active policy is `config/population.yaml`. Identity-bearing documents exclude
timestamps, mtimes and absolute paths and use canonical sorted JSON:

- `CPI_<sha256>`: source inventory and canonical-before identity;
- `CMI_<sha256>`: external manual import plan;
- `CPB_<sha256>`: one deterministic ingest batch;
- `CPR_<sha256>`: population run binding inventory and batch IDs;
- `CSA_<sha256>`: corpus-wide staging audit;
- `CPP_<sha256>`: canonical candidate-ID selector.
- `CPE_<uuid>`: one unique batch-execution attempt and its checkpoints.

Execution attempts and mutable run checkpoints carry timestamps, but timestamps are not
part of deterministic identities.

## Source discovery and import

The sole manual discovery root is exactly `incoming/manual/inbox/`, recursively. Discovery
does not follow symlinks and ignores hidden paths, `README.md`, platform noise and temporary
Office files. Containers such as ZIP, TAR and 7z are never unpacked; a genuine OOXML package
may still be detected by the existing magic-byte detector. Unsupported regular files are
accounted for and never processed.

`manual-import-plan` scans a separate external directory without changing it. Apply requires
the exact `CMI_` ID, rechecks the plan, preserves relative paths, copies via a temporary
tree, verifies size and SHA-256 and atomically renames each destination. Identical existing
bytes are an idempotent no-op. Different bytes at the same path are `PATH_COLLISION`; no
overwrite or automatic rename is allowed. There is no metadata-sidecar convention.

PaperCrawler contract major 2 is accepted. Schema 2.0 uses compatibility validation;
schema 2.1+ additionally requires complete release metadata, package `GO`, manifest and
checksum-ledger agreement. Producer identity fields must be unique, paths root-confined,
authoritative bytes present and checksummed, status `READY_FOR_HANDOFF` / `NOT_INGESTED`,
and provenance non-empty. Original/raw bytes are preferred; crawler-normalized Markdown
cannot substitute for missing authoritative bytes. Invalid releases stay in place and are
reported `BLOCKED_RELEASE`.

## Inventory and artifact truth

Inventory groups every source alias by content-derived `ING_<sha256[:20]>`, records both
channels, supported formats, ignored/unreadable inputs, release decisions, configuration
hashes and the verified canonical manifest SHA/corpus digest. A document can be `NEW`,
`ALREADY_CANONICAL`, `REUSABLE_COMPLETE`, `RECOVERY_REQUIRED` or `UNSUPPORTED`; additional
paths with the same SHA are `EXACT_SOURCE_ALIAS` provenance associations.

Ledger rows do not prove physical completion. A reusable terminal document must have the
matching immutable source and required processing, quality, chunk and staging artifacts.
Missing or inconsistent artifacts make an incoming identity `RECOVERY_REQUIRED`.
Non-selected ledger rows are reported separately as `LEDGER_ONLY` and retained.

## Batch execution and resume

Batches are ordered by source channel, release, processing class and document ID. The
default limits are 10 heavy documents/250 MiB, 50 lightweight documents/100 MiB, with an
oversized document alone. Manual and schema-2.0 Pilot inputs form separate groups. Execution
requires at least 100 GiB free and more than three times the projected batch expansion,
initially estimated at 35×. Processing is strictly sequential.

Before a batch, the controller revalidates `CPI_`, `CPB_`, source SHA values and canonical
identity. Already-canonical inputs are removed before archive or provenance writes. Unified
Ingest checkpoints the `CPR_` run atomically after each outcome and isolates document
failures. The same canonical manifest SHA and corpus digest must verify after the batch.

With `--resume`, complete `EMBEDDING_READY` artifacts are preserved and reported
`ALREADY_PROCESSED`; the engine state is not rewritten. Incomplete/interrupted or ledger-only
documents restart derived processing from extraction using verified incoming/original
bytes. `FAILED` may be explicitly retried; `REVIEW`, `REJECTED` and `UNSUPPORTED` remain
terminal until an explicit operator action. Exact/strong duplicates stop before staging;
probable duplicates require review. No runtime root is deleted to resume.

Population states are `INVENTORIED`, `READY_TO_INGEST`, `INGESTING`, `PAUSED`,
`INGEST_ACCOUNTED`, `STAGING_AUDITED`, `PROMOTION_PENDING_APPROVAL`, `PROMOTING`, `CANONICAL_READY` and
`BLOCKED`. Per-document dispositions are `PENDING`, `STAGED`, `ALREADY_PROCESSED`,
`ALREADY_CANONICAL`, `DUPLICATE`, `NEEDS_REVIEW`, `REJECTED`, `UNSUPPORTED`, `FAILED` and
`RECOVERY_REQUIRED`. A failure or review is accounted only after success or a recorded
exclusion reason; exclusion never changes quality or promotion eligibility.

## Audit and canonical handoff

Staging audit is unavailable until the run is `INGEST_ACCOUNTED`. Immutable `CSA_` output
recomputes canonical actions through `tunnelbookai.canonical`, aggregates document/chunk
quality, provenance/classification/path failures, duplicates and exception reasons, and
reports exclusive primary-section totals separately from non-exclusive secondary-section
associations. Each document and chunk counts once in primary totals.

Promotion selectors contain only sorted candidate IDs and are limited to 25 documents and
1 GiB materialization input, with oversized documents alone. Canonical independently repeats
all eligibility checks. For each selector the operator must run canonical verify, create one
fresh plan, review its exact contents, explicitly apply that exact `CCP_` ID and verify again.
Plans cannot be pre-created because every apply changes canonical state. Population never
calls apply and never supplies `--approve`.

Readiness requires every selected identity to have an explained terminal disposition, every
required staged/reusable identity to be present in a verified `READY` canonical manifest,
and no unresolved failures or reviews. The report records identities, counts, distributions,
reason codes, promotion IDs, manifest SHA and corpus digest. It embeds no source/chunk text
or absolute external paths and explicitly reports retrieval, evidence audit and writing as
`NOT_IMPLEMENTED`.

## Checkpoint, interruption and local control

The run ledger and attempt ledger are atomically checkpointed after every document. A
cooperative stop request is checked before each next document: the active document is
allowed to finish, its outcome is checkpointed, the attempt becomes `PAUSED`, and the batch
is deliberately not marked complete. Resume revalidates source, inventory and canonical
identities, skips complete terminal artifacts, and restarts only an interrupted document
whose terminal artifacts are absent. A prior orphaned `RUNNING` attempt is closed as
`INTERRUPTED` before the locked resume begins.

Only one population writer may hold `audit/corpus_population/population.lock`. The local
dashboard is a supervisor over the same public batch runner; it has no alternate ingest or
canonical write path. Its HTTP server binds only to loopback, rejects non-loopback Host
headers, requires a per-process control token for state-changing requests, and persists
stop intent separately from display state.
