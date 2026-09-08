# TunnelBookAI V1 — Pre-cleanup Baseline

Date: 2026-09-04

## Git rollback boundary

- Repository root: `/Users/bulsahkecici/Projects/tunnelbookai_v1`
- Repository identity: `bulsahkecici/tunnekbookai_v1`
- Commit: `222b9bcecf1d2603cf443db058a8a0821ae155a2` (`Initial TunnelBookAI V1 import`)
- Branch: `main`
- Origin: `https://github.com/bulsahkecici/tunnekbookai_v1.git`
- Dirty files before cleanup: none.

No history will be amended, rewritten, squashed, or deleted. No commit or push is part of
this cleanup task.

## Legacy state inventory

| Item | Baseline |
| --- | ---: |
| Tracked `crawler/` files | 44 |
| Canonical documents | 214 |
| Canonical/metadata files | 576 |
| Staging files | 316 |
| Original source bundles | 14 |
| Processing files | 314 |
| Legacy chunk rows (`data/chunks/chunks.jsonl`) | 6,039 |
| Pilot chunk rows | 2,476 |
| Qdrant local storage | 304 MB |
| Qdrant snapshots | 425 MB |
| Embedding state | 50 MB |
| Retrieval index/state | 1.4 MB |
| Legacy PaperCrawler release files | 15 |
| Manual inbox files | 5 |

## Preserved book contract

- Scope sections: 66
- Question-bank sections: 59
- Questions: 2,950

## Active legacy dependencies found

- `config/classification.yaml`, `tunnelbookai/ingest/classify/*`, and `shared/book_qa.py`
  load `crawler/config/taxonomy.yaml`.
- `config/ingest.yaml`, `tunnelbookai/ingest/paths.py`, and the CLI use
  `incoming/crawler/releases/`.
- Active embedding selection uses substring discovery (`nomic-embed`/`embed`) and lacks a
  single authoritative model configuration.
- README, ingest contract, architecture documentation, migration tests, and selected scripts
  describe or import the embedded crawler implementation.

The recoverability gate and crawler-removal audit are the required next controls before any
active legacy state is removed.
