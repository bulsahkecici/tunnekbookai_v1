# Crawler Removal Audit

This repository must consume PaperCrawler source packs; it must not contain a runnable
PaperCrawler implementation. The standalone `paper-crawler-agent` repository is out of scope
and is not modified here.

| Path / group | Type | Used by | Action | Reason | Risk |
| --- | --- | --- | --- | --- | --- |
| `crawler/src/` | crawler implementation | legacy scripts/tests only | remove after migration | discovery, acquisition, harvesting and crawler CLIs belong to PaperCrawler | high until active imports are removed |
| `crawler/tests/` | crawler tests | crawler implementation | remove with component | tests cannot survive without the component | low after removal |
| `crawler/config/taxonomy.yaml` | generic section-term dictionary | ingest classifier, Book QA | migrate to `config/taxonomy.yaml` | generic TunnelBookAI classification asset, not crawler logic | medium |
| `crawler/config/classification_policy.yaml` | crawler policy | documentation/comments only | do not migrate wholesale | contains source-pack acceptance and legacy model policy | low |
| other `crawler/config/*.yaml` | discovery/acquisition policy | crawler only | remove with component | PaperCrawler owns discovery, coverage, routing and harvesting | low |
| `config/classification.yaml` | active ingest configuration | classifier | rewrite | eliminate crawler paths, section hints and substring model fallback | high |
| `config/paths.json` | root map | ingest paths | rewrite | remove crawler source/config roots | medium |
| `shared/book_qa.py` | Book QA | tests / QA CLI | repoint | taxonomy must remain available independently of crawler | medium |
| `tunnelbookai/ingest/sources/crawler_contract.py` | Source Pack consumer | unified ingest | retain and refactor | consumer is required; legacy book-section fields become ignored compatibility input | high |
| `tunnelbookai/ingest/cli.py`, `paths.py` | active ingest | CLI | rename input authority | authoritative path becomes `incoming/papercrawler/releases/` | high |
| `scripts/controlled_smoke.py`, migration tests | legacy test support | tests | rewrite/remove crawler coupling | empty-corpus architecture must not import crawler | medium |
| README and `docs/*.md` | active documentation | users | rewrite | document source-oriented PaperCrawler boundary | medium |
| legacy reports/audits | historical evidence | no runtime consumer | archive | preserve history but prevent it being read as active state | low |

## Dependency conclusion

Only the term dictionary is generic book-classification logic that must survive. It will move
to `config/taxonomy.yaml`; all active TunnelBookAI code/configuration will reference that path.
No discovery, acquisition, harvesting, provider, coverage, or crawler CLI code will be copied
into `tunnelbookai/`.
