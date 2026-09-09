# Chunking Contract

The single authoritative chunk location is
`processing/<document_id>/chunks/chunk_manifest.jsonl`. `embedding_ready.jsonl` and
`chunk_quality.json` live beside it. Chunks are structure-aware: text respects
heading and paragraph boundaries; tables, figures, slides and sheets retain their
own types and provenance.

Chunking creates no embedding and writes no vector database. Each chunk must retain
the source SHA256, source kind, structural location (page, slide or sheet where
available), final classification from the ingest engine, and the configured policy
version. A future embedding/index stage consumes only the ready manifest after a
separate operator decision.

Controlled canonical promotion preserves the producer chunk IDs, independently
recomputes them, and creates `chunk_identities.jsonl` containing semantic hashes of each
full chunk and corresponding embedding-ready row. The active canonical manifest records
the ledger hash and aggregate chunk identity digest.

The future retrieval layer must consume only
`corpus/canonical/objects/.../chunks/embedding_ready.jsonl` paths admitted by the verified
canonical manifest. It must not read the mutable staging reference or the processing
manifest directly.
