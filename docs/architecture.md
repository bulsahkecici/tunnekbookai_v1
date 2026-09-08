# TunnelBookAI V1 Architecture

## Boundary

TunnelBookAI is the authoritative ingest, classification, quality, chunking and
readiness system. PaperCrawler is an independent acquisition product; TunnelBookAI
does not contain its discovery, crawling or scheduling implementation.

```text
PaperCrawler release                 Manual document
incoming/papercrawler/releases/      incoming/manual/inbox/
              \                         /
               \                       /
                Unified Ingest Engine
                        |
      originals -> processing -> corpus/staging -> chunks
                        |
        quality gate, audit and controlled promotion only
```

`corpus/canonical` is empty after the 2026 reset. It can be populated only by an
explicit, separately approved promotion. The engine never builds embeddings,
writes Qdrant, or promotes a document during ordinary ingest.

## Authorities

| Concern | Authority |
| --- | --- |
| Book scope and question coverage | `book/` source files, when intentionally introduced |
| Classification scope | `book/scope/normalized/book_scope.json` |
| Classification term dictionary | `config/taxonomy.yaml` |
| Exact local models | `config/models.yaml` |
| External source pack | `incoming/papercrawler/releases/` |
| Manual source pack | `incoming/manual/inbox/` |
| Source bytes | `originals/<document_id>/source.*` |
| Structural extraction and chunks | `processing/<document_id>/` |

Producer fields such as `provisional_primary_section` are accepted only for schema
2.x compatibility. They are recorded as `DEPRECATED_PRODUCER_SECTION_FIELD` audit
notes and never influence final classification.

## Local model policy

Only loopback endpoints are valid. `config/models.yaml` is the single model
authority: embedding is `text-embedding-baai-bge-m3-568m`, and the local arbiter is
`qwen/qwen3.8-27b`. Selection is exact; a model-list fallback or substring match is
not permitted. A missing/unavailable service yields `MODEL_SERVICE_UNAVAILABLE`.

## Empty-reset gate

Run `PYTHONPATH=. .venv/bin/python shared/project_quality_gate.py`. It writes
`audit/empty_corpus_reset_gate.json` and returns `GO` only when legacy corpus,
processing, chunk, embedding and vector state are absent while both input roots
exist.
