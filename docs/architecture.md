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
        quality gate and Corpus Population audit
                        |
           controlled canonical promotion only
```

`corpus/canonical` begins in the valid `EMPTY` bootstrap state. It can be populated only
by an exact-plan, separately approved promotion. The engine never builds embeddings,
writes Qdrant, or promotes a document during ordinary ingest.

The downstream Book Production Engine consumes this boundary without extending it:

```text
corpus/canonical + canonical_manifest
                 |
                 v
     rebuildable book retrieval index
                 |
                 v
 evidence audit -> constrained packet -> writing -> independent audits -> freeze
                 |
                 v
 deterministic assembly -> complete 2,950-question publication gate
```

`book/config/book_contract.json` is the single book-policy contract. The importable
implementation lives under `tunnelbookai.book`; it does not import or execute anything
from `archive/legacy_pre_reset/`. Retrieval may only consume manifest-admitted canonical
evidence. The index is a derivative and can never become evidence authority.

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
| Book-production policy | `book/config/book_contract.json` |
| Book evidence | `corpus/canonical/canonical_manifest.json` and its canonical members |
| Exact book input loading | `tunnelbookai.book.inputs` |
| Population inventory, batching and accounting | `tunnelbookai.population` |
| Canonical planning, promotion and verification | `tunnelbookai.canonical` |

Producer fields such as `provisional_primary_section` are accepted only for schema
2.x compatibility. They are recorded as `DEPRECATED_PRODUCER_SECTION_FIELD` audit
notes and never influence final classification.

## Population control plane

Corpus Population V1 is an orchestration and audit layer over Unified Ingest. It owns
`CPI_` inventories, `CPB_` sequential batch manifests, mutable per-document `CPR_` run
checkpoints, immutable `CSA_` staging audits and `CPP_` candidate selectors. It does not own
source conversion, classification, chunking or canonical admission.

Every batch requires a verified canonical snapshot and records that the manifest SHA and
corpus digest were unchanged after ingest. Shared JSONL ledgers remain single-writer; no
worker concurrency is supported. A ledger terminal state is reusable only when the expected
immutable original, processing and staging artifacts independently agree. Ledger-only rows
remain audit history and are never completion evidence.

## Local model policy

Only loopback endpoints are valid. `config/models.yaml` is the single model
authority: embedding is `text-embedding-baai-bge-m3-568m`, and the local arbiter is
`qwen/qwen3.8-27b`. Selection is exact; a model-list fallback or substring match is
not permitted. A missing/unavailable service yields `MODEL_SERVICE_UNAVAILABLE`.

## Canonical authority

Canonical evidence uses one manifest and content-addressed document objects:

```text
corpus/canonical/canonical_manifest.json
corpus/canonical/objects/<document_id>/<document_digest>/
```

The manifest is the commit point and the only active-document inventory. Objects not
referenced by it are inert and never retrieval evidence. Promotion copies normalized
Markdown, verified sidecars, the authoritative chunk rows and embedding-ready rows; raw
source bytes remain immutable under `originals/`. `tunnelbookai.book status` delegates to
the same disk verifier and does not implement a second manifest parser.

## Empty-reset gate versus production gates

Run `PYTHONPATH=. .venv/bin/python shared/project_quality_gate.py --mode empty-reset` only
for a new/reset bootstrap. It writes
`audit/empty_corpus_reset_gate.json` and returns `GO` only when legacy corpus,
processing, chunk, embedding and vector state are absent while both input roots
exist. It is expected to fail after legitimate ingest.

Use `shared/project_quality_gate.py --mode isolation` to verify active topology and
`python -m tunnelbookai.canonical verify` to establish canonical production integrity.
