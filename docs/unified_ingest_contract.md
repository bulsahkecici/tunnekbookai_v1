# Unified Ingest Contract

## Inputs

TunnelBookAI accepts two independent sources:

| Source | Root | Contract |
| --- | --- | --- |
| PaperCrawler | `incoming/papercrawler/releases/<release>/` | schema major 2 release, manifest SHA256 must match local bytes |
| Manual | `incoming/manual/inbox/` | supported local document; no network call |

Manual discovery is recursive beneath exactly `incoming/manual/inbox/`. Files elsewhere
under `incoming/manual/`, hidden path components, symlinks, `README.md`, platform noise and
temporary Office files are excluded. Archives are ordinary unsupported files and are never
unpacked. JSON/YAML files have no implicit metadata-sidecar meaning.

PaperCrawler is a producer, not a component of this repository. Its release must
declare `paper_crawler_status: READY_FOR_HANDOFF`; paths must resolve beneath the
release root. Schema 1.x and unknown major versions are rejected.

Schema 2.x packages may contain legacy producer classification fields. The engine
accepts them, emits `DEPRECATED_PRODUCER_SECTION_FIELD:<field>`, does not map them
into final metadata, and computes all final sections from source content, the canonical
book scope, and the matching terms in `config/taxonomy.yaml`.

## Turkish glyph-spacing repair

Some Turkish PDFs embed ı/İ/ş/Ş/ğ/Ğ/ü/Ü/ö/Ö/ç/Ç through a separate font program, so the
extracted text layer isolates every such glyph with spaces (``TEKN İ K``, ``k ı salmas ı``).
After any adapter succeeds, `tunnelbookai.ingest.glyph_repair.repair_extraction` measures
the damage density of the normalized text; when at least eight isolated glyphs occur at a
density of one per 2,000 characters or more, it re-attaches each glyph to its left and/or
right neighbour by scoring every attachment choice against `config/turkish_lexicon.txt`
(Turkish word forms with corpus frequency, ı and i kept distinct) plus document-local
evidence of which fragments stand alone. The repaired text replaces the normalized
Markdown/JSON/text, the element stream, heading paths and asset captions before metadata,
classification and chunking read them; the immutable original is untouched. The extraction
report records `text_repair` and the warning `TURKISH_GLYPH_SPACING_REPAIRED:<count>`.
Undamaged documents are never modified. The lexicon is a versioned configuration input; it
was generated from the undamaged Turkish canonical documents and can be regenerated with
`build_lexicon`.

## Output ownership

For a source SHA256, `document_id = ING_<sha256[:20]>`. The immutable source is
stored at `originals/<document_id>/`; extraction, provenance, classification,
quality output and the authoritative chunk manifest are under
`processing/<document_id>/`. A successful candidate may be materialized in
`corpus/staging/`, but canonical promotion is a distinct operator action.

Before any archive or provenance write, ingest independently verifies canonical. An input
whose content identity is already admitted is reported `ALREADY_CANONICAL` and skipped. An
invalid canonical snapshot blocks ingest. With `--resume`, a successful ledger state is a
no-op only when its required original, processing, quality, chunks and staging artifacts are
present and consistent; otherwise the document is rebuilt from its incoming bytes. The
stored engine state remains the real terminal state, while `ALREADY_PROCESSED` is only an
execution disposition.

Exact and strong DOI/URL/title duplicates stop after metadata and dedup audit and never
reach staging. Probable duplicates finish as `REVIEW`/`NEEDS_REVIEW`. Artifact-orphaned
registry rows remain preserved but cannot suppress a real input or satisfy canonical
eligibility.

Rendered Office PDFs provide visual provenance only. DOCX/PPTX/XLSX structural
authority remains their original packages or the `openpyxl` workbook model.

## Canonical handoff

Unified Ingest stops at staging. `tunnelbookai.canonical` independently verifies the
content-derived document ID, archived source bytes, processing/staging byte agreement,
metadata, metadata provenance, source provenance, final classification, `GO` document
quality, non-failing chunk quality, ingest ledgers and chunk identities. It does not rerun
or replace ingest decisions.

Planning is non-destructive. Approved apply copies the normalized document, staging
sidecars, authoritative chunk manifest and embedding-ready rows. It never moves or edits
`originals/`, `processing/` or `corpus/staging/`, and it performs no automatic cleanup.

## Model capability

Before a model-dependent operation, run the capability probe for the exact models
in `config/models.yaml`. It verifies a loopback endpoint, model availability, a
non-empty stable embedding dimension, and a minimal structured local-LLM response.
Any failure is reported as `MODEL_SERVICE_UNAVAILABLE`; no cloud fallback is used.
PaperCrawler schema 2.1 releases are accepted only when release metadata, the manifest fingerprint, the package-local `GO` quality gate, and the checksum ledger agree. `source_representation.original_or_raw` is the authoritative input and must remain inside the release root. If it is declared but missing, unsafe, or has no valid checksum, ingest fails closed; crawler-normalized Markdown is never substituted. Schema 2.0 remains compatible through its verified `local_path` fallback.

`--release <release-id>` limits discovery to that exact PaperCrawler release. Hidden and `.partial` directories are never discovered. Dry-run reports each release separately and returns a nonzero status for release blockers, unreadable files, or unsupported formats.

`tunnelbookai.ingest.runner.run_selected` is the public single-writer execution entry point
shared by the direct CLI and Corpus Population. It builds local services once per selected
batch, processes documents sequentially, isolates per-document failures and supports an
atomic checkpoint callback. It does not implement parallel workers.
