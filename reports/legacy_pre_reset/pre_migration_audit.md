# PRE-IMPLEMENTATION FINDINGS / PRE-MIGRATION AUDIT

Audit date: 2026-09-01  
Target: `/Users/bulsahkecici/Projects/tunnelbookai_v1`

No source file was moved, deleted, or modified during this audit.

## SOURCE PROJECTS

Paper crawler root: `/Users/bulsahkecici/Projects/paper-crawler-agent`  
TunnelBookAI root: `/Users/bulsahkecici/Projects/tunnel/_TunnelBookAI`  
Prepared book package: `/Users/bulsahkecici/Projects/tunnelbookai_v1/tunnelbookai_v1_book_inputs/book`

### Paper crawler

- Logical project size: 6.0 GB; `.venv`: 337 MB; crawler output `tunel_makaleleri`: 5.6 GB.
- Python modules at project root/max depth 2: 33.
- Tests: 10 `test_*.py` files (20 files including fixtures/cache entries).
- Configs: 8 files.
- Generated crawler data: 1,858 PDFs, 250 HTML files, 1,542 Markdown files, 4,392 JSON files and 8 JSONL files.
- Current catalogs: classic 831 rows; discovery 909 rows; classification index 1,652 rows.
- Current handoff package: `tunel_makaleleri/exports/TunnelBookAI_Source_Pack` (inside a 2.4 GB exports tree).
- Current audit/state: `tunel_makaleleri/audit/` contains 10 files, including classification, gap discovery, source health, quality gate, and pipeline state.
- The source worktree contains extensive tracked modifications and untracked stabilization/output files. Migration must preserve the working tree, not only Git `HEAD`.

### TunnelBookAI

- Logical project size: 9.0 GB. Large derived directories include `data/temp` (3.3 GB), Qdrant snapshots (425 MB), Qdrant storage (213 MB), converted Office files (123 MB), and archive data (99 MB).
- Canonical Markdown corpus: `data/corpus_final`, 214 `.md` documents, ~25 MB.
- Canonical metadata master: `data/metadata/final_metadata_master.csv`, 214 data rows.
- Canonical corpus manifest: `data/metadata/final_corpus_manifest.csv`, 214 data rows.
- Metadata/sidecar directory: `data/metadata`, 575 non-`.DS_Store` files, ~7.4 MB.
- Corpus scripts: 311 non-`.DS_Store` files under `scripts/` (including historical/QA tooling).
- Tests: 288 non-`.DS_Store` files under `tests/`; generated caches are excluded from migration.
- Documentation: 10 non-`.DS_Store` files under `docs/`; reports: 89 non-`.DS_Store` files.
- The canonical corpus is frozen source-of-truth material and will be copied byte-for-byte. New crawler documents must remain in staging until a quality gate succeeds.

### Book package

- Package SHA-256 manifest: PASS (15/15 files).
- Package validator: PASS.
- Scope/question-bank result: 59 question-bank sections, 2,950 questions.
- The package currently lives one level below the target root and will be copied—not moved—to canonical `book/`.

## GIT REPOSITORIES

### paper-crawler-agent

- Branch: `hardening`
- HEAD: `ebe597a69ba0808621b4a1c4a7a3aff387af3985`
- Remote: `https://github.com/bulsahkecici/paper-crawler-agent.git`
- State: dirty; tracked and untracked implementation changes plus generated data.

### old TunnelBookAI

- Branch: `master`
- HEAD: `a5d5c0f1feb0cd5896e7faeb010bbaa7a0a28c22`
- Remote: `https://github.com/bulsahkecici/_TunnelBokkAI.git`
- State: eight untracked `.pre_*` backup files; otherwise no reported tracked changes.

The target had no `.git` directory at audit time. Source `.git` directories will not be migrated and no nested repository will be created.

## PYTHON ENVIRONMENTS

- System Python: 3.14.6.
- Crawler `.venv`: Python 3.14.6 (excluded from migration).
- TunnelBookAI `.venv`: Python 3.12.14 (excluded from migration).
- Dependency declarations are present in both source roots and will be preserved/merged without copying virtual environments.

## CRITICAL SHA-256 VALUES

- Crawler `catalog.json`: `680649a3cce688e57ec2425585706ef3263cce551589a04d65479aaefe338f61`
- Crawler `index.jsonl`: `ade156461956f99deeb4cb552d3e20392851aebb1ea4011e788c86d4bc61d7e4`
- Crawler `discovery_catalog.jsonl`: `cfc6d979427855e7b6fe727b9511e5d94eb790a2913a035a4b131f3b349afdc0`
- Crawler `classification_index.jsonl`: `51f58e509b5c8a21646a0c46093f8df05a36b4a396157d88309b5acc2464ce0d`
- Crawler `classification_audit.json`: `33ea6d32f018841c1d392a04e9d997fa6086d4a9b7a467da19b67c456353c7eb`
- Crawler `pipeline_state.json`: `dcc31519937367e0950706493293e17c8174ee5b577dc7451fadb2fd91aa1029`
- TunnelBookAI `final_metadata_master.csv`: `55fe1e44b57b705c8538690b2c0550e7c11fe8a8aed8618b3f1da04fada3d1e0`
- TunnelBookAI `final_corpus_manifest.csv`: `cf59e74f9435635a15f8446c20aa8d6fb5976c0434ee87022e067722cccf44c3`

## CONFIRMED BUG FINDINGS

### 1,193 to 1,160 reconciliation

The initial run combined 831 classic rows and 362 discovery rows. The legacy `_merge_records` keyed records by DOI first and removed exactly 33 repeated DOI rows, yielding 1,160 classification inputs. Therefore the discrepancy was deduplication, not silent record loss. The old audit did not expose this accounting; the working-tree stabilization adds named counters and the invariant `raw_input_total - dedup_removed == classification_input == classification_output`.

### Coverage `current=0`

The interrupted run's gap analyzer read `handoff_candidate_section_coverage`, which counted only directly assigned sections for records with a local/acquired source. It did not roll leaf assignments into parents. Thus a `5.5.1` classification did not contribute to `5.5` or `5`, and accepted metadata-only/non-acquired records were also absent. The zeroes were a coverage-accounting bug, compounded in some leaf sections by a legitimately empty corpus-eligible count. The working-tree implementation introduces explicit `discovered_count`, `accepted_count`, `review_count`, `fulltext_count`, and `corpus_eligible_count` metrics with deterministic ancestor aggregation.

## CURRENT STABILIZATION STATE FOUND IN SOURCE

- Dedup: DOI, canonical URL, SHA-256, normalized exact title, and conservative fuzzy title/year/author logic exists in the dirty working tree; provenance fields are retained.
- Coverage: explicit dimensioned counting and parent aggregation exists, but must be migrated and tested in the target.
- Resume: atomic stage state with `NOT_STARTED/RUNNING/PARTIAL/COMPLETED/FAILED`, legacy bootstrap, and interrupt handling exists; CLI behavior must be verified.
- Circuit breaker: a persistent pipeline-global source health registry exists; retry/backoff and robots cache tests must be verified.
- Gap flow: domain anchoring, relevance filtering, metadata-first ranking, and configurable acquisition budgets exist; behavioral gaps and regression failures will be fixed only in the target.

## POTENTIAL DUPLICATES / CONFLICTS

- The crawler output contains hard-linked/copy-equivalent assets between `pdfs`, `exports`, and other generated trees. Migration must preserve hard links where practical and verify critical hashes.
- The old TunnelBookAI `data/corpus_final` and `data/corpus_normalized` files share storage for many files. Only canonical corpus plus required metadata/sidecars are in migration scope.
- Both projects contain a root `README.md`, `requirements.txt`, `config/`, `tests/`, `reports/`, and `.gitignore`; these cannot be overlaid blindly and will be namespaced or consolidated.
- The prepared package contains canonical `book/`; old TunnelBookAI also has `data/book`. The prepared package is authoritative for this task. Old book-writing artifacts will not overwrite it.

## GENERATED / EXCLUDED CONTENT

Excluded from migration: `.git`, `.venv`, `venv`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.DS_Store`, `node_modules`, `build`, `dist`, IDE caches, and temporary caches. TunnelBookAI's Qdrant storage/snapshots, embeddings, chunks, converted-office output, archives, logs, and `data/temp` are inventoried but are not required for the requested canonical-corpus migration and will not be copied into active target paths.

## MIGRATION RISKS

1. Source crawler code is not committed; copying from Git alone would lose the requested stabilization implementation.
2. Absolute paths embedded in crawler run outputs point to the old crawler root and require manifest-level/path normalization or compatibility handling.
3. Canonical corpus provenance references original source paths that are outside the canonical corpus tree; this migration preserves those references and records the old root rather than pretending the originals were copied.
4. A full crawler-output copy is multi-gigabyte and must preserve resumability without re-downloading successful PDFs.
5. Current crawler quality gate is `CONDITIONAL_GO`, not an unconditional production-ready corpus decision, because the review queue is non-empty and most records are title/abstract evidence only.

## PRE-MIGRATION DECISION

`PROCEED_WITH_COPY_AND_VERIFY`

No critical source file is missing, the prepared book package verifies, and the exact two headline accounting issues are resolved sufficiently to proceed. Old repositories remain `KEEP` until target migration, imports, integrity tests, and target-only stabilization validation complete.
