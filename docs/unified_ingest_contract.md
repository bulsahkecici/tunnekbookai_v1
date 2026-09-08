# Unified Ingest Contract

## Inputs

TunnelBookAI accepts two independent sources:

| Source | Root | Contract |
| --- | --- | --- |
| PaperCrawler | `incoming/papercrawler/releases/<release>/` | schema major 2 release, manifest SHA256 must match local bytes |
| Manual | `incoming/manual/inbox/` | supported local document; no network call |

PaperCrawler is a producer, not a component of this repository. Its release must
declare `paper_crawler_status: READY_FOR_HANDOFF`; paths must resolve beneath the
release root. Schema 1.x and unknown major versions are rejected.

Schema 2.x packages may contain legacy producer classification fields. The engine
accepts them, emits `DEPRECATED_PRODUCER_SECTION_FIELD:<field>`, does not map them
into final metadata, and computes all final sections from source content, the canonical
book scope, and the matching terms in `config/taxonomy.yaml`.

## Output ownership

For a source SHA256, `document_id = ING_<sha256[:20]>`. The immutable source is
stored at `originals/<document_id>/`; extraction, provenance, classification,
quality output and the authoritative chunk manifest are under
`processing/<document_id>/`. A successful candidate may be materialized in
`corpus/staging/`, but canonical promotion is a distinct operator action.

Rendered Office PDFs provide visual provenance only. DOCX/PPTX/XLSX structural
authority remains their original packages or the `openpyxl` workbook model.

## Model capability

Before a model-dependent operation, run the capability probe for the exact models
in `config/models.yaml`. It verifies a loopback endpoint, model availability, a
non-empty stable embedding dimension, and a minimal structured local-LLM response.
Any failure is reported as `MODEL_SERVICE_UNAVAILABLE`; no cloud fallback is used.
