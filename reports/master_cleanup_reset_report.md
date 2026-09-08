# Master Cleanup, Reset & Architecture Alignment

Date: 2026-09-04

## Outcome

The repository is in an intentional empty-corpus bootstrap state. TunnelBookAI owns
ingest, extraction, final classification, quality gates and chunking. PaperCrawler is
an external Source Pack producer only. No commit, force-push, history rewrite, or
automatic push was performed during this reset.

## Baseline and recoverability gate

The pre-cleanup baseline is recorded in `reports/pre_cleanup_baseline.md`. Before
removal, `scripts/pre_reset_recoverability.py` produced:

- `reports/pre_reset_recoverability.md`
- `audit/pre_reset_recoverability.jsonl`
- `audit/pre_reset_delete_plan.jsonl`

Result: **GO** — 350 source references were assessed and 0 unique source bytes were
unrecoverable. The former canonical Markdown is recoverable from Git; the remaining
source artifacts have verified external or staging recovery paths. `data/downloads/`
was retained as that source archive.

## Removed and retained state

Removed after the recoverability gate:

- legacy corpus, staging, originals, processing and chunk artifacts;
- embeddings, Qdrant storage/snapshots, retrieval/evaluation/production output;
- the internal `crawler/` implementation and its crawler-only scripts;
- legacy handoff and obsolete incoming crawler location.

Retained or recreated:

- source archive: `data/downloads/`;
- PaperCrawler source-pack input: `incoming/papercrawler/releases/`;
- manual input and quarantine roots;
- empty tracked markers for canonical, staging, metadata, originals, processing and
  temporary locations;
- book scope and question-bank authority used by the classification scope;
- generic term dictionary at `config/taxonomy.yaml`.

Historical reports and audits are preserved under `reports/legacy_pre_reset/` and
`audit/legacy_pre_reset/`. Corpus-dependent legacy tests are preserved under
`archive/legacy_pre_reset/tests/`, outside active test discovery.

## Architecture alignment

`config/models.yaml` is the sole exact-model authority:

| Capability | Required model | Endpoint policy |
| --- | --- | --- |
| Embedding | `text-embedding-baai-bge-m3-568m` | loopback only |
| Local arbiter | `qwen/qwen3.8-27b` | loopback only |

There is no model-list fallback or substring selection. The capability probe verifies
the exact configured embedding model and a minimal structured LLM response. On this
machine the local service is not running, so the correct result is
`MODEL_SERVICE_UNAVAILABLE`, not a cloud fallback.

Schema-2.x producer section fields remain parse-compatible. They emit
`DEPRECATED_PRODUCER_SECTION_FIELD:<field>` notes and are not used by final
classification or written as final section metadata.

## Verification

`PYTHONPATH=. .venv/bin/python shared/project_quality_gate.py` returned **GO**:

| Check | Result |
| --- | --- |
| Canonical, staging, originals, processing | 0 documents |
| Chunks, embeddings, vectors | 0 |
| Internal crawler directory | absent |
| PaperCrawler and manual input roots | present |

`PYTHONPATH=. .venv/bin/python -m unittest discover -s tests/ingest -p 'test_*.py'`
ran **205 tests — OK** in the real local environment. This includes architecture,
Source Pack, security, chunking, adapter, renderer and controlled end-to-end coverage.
LibreOffice renderer tests must run outside the filesystem sandbox because the macOS app
silently produces no output under sandbox confinement; in the real local environment it
generated the expected PDF snapshots. The controlled end-to-end suite uses
`--no-ocr --no-vision --no-arbiter` to remain deterministic; OCR and visual provenance
are protected by their dedicated adapter tests.

## Deliberate non-results

- No real Source Pack ingestion was run after the reset.
- No canonical promotion, embedding creation, Qdrant indexing or book generation was run.
- Local model capability is currently unavailable until the required loopback services
  are started with the exact configured model identifiers.

## Next operator action

Start the two local model services, run the capability probe, then ingest one approved
PaperCrawler release or manual document into staging. Review the resulting quality and
classification audits before any separate canonical-promotion decision.
