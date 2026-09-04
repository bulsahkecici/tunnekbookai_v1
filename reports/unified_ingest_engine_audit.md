# Unified Ingest Engine — Final Audit

- **Date:** 2026-09-03
- **Scope:** Phase C → J (format adapters, assets, OCR/vision, metadata, dedup, final
  classification, evidence model, quality gate, staging, structure-aware chunking,
  chunk quality gate, embedding-ready manifest, docs, tests)
- **Decision:** **CONDITIONAL_GO** — every required capability is implemented and verified;
  one optional capability is unavailable in this environment (LibreOffice) and one is
  deliberately disabled on evidence (Docling chart extraction).

---

## 1. Baseline guardrails

| Check | Result |
|---|---|
| `scripts/verify_canonical_baseline.py` | **PASS** — 214 files, digest `6c49a13c0f3715ac54f44cb206a18096d596c80ad5ea47891dbeebd9bdef0470` |
| Canonical corpus files written | 0 |
| `corpus/staging/` legacy bundles | 122, all byte-identical (engine writes only `corpus/staging/v2/`) |
| `book/scope/normalized/book_scope.json` | Unchanged — 66 sections, 59 question-bank sections |
| `~/Projects/paper-crawler-agent` | `git diff --stat HEAD` empty; no tracked file differs from HEAD |
| `scripts/08_final_corpus.py` | Not executed |
| `promote_staging.py --apply` | Not executed (dry run only) |
| Qdrant / production embeddings / 2950-question evaluation | Not executed |

## 2. What was built

| Area | Modules |
|---|---|
| Docling wrapper | `docling_adapter.py` — every option applied through a `hasattr` guard; versions + resolved options recorded per document |
| Common models | `extraction.py` (`ExtractionResult`), `elements.py` (shared structural element stream) |
| Format adapters | `adapters/{pdf,docx,pptx,xlsx,image,text}.py` |
| Assets | `assets/{snapshots,figures,tables,charts}.py`, `office_renderer.py` |
| OCR / vision | `ocr/provider.py` (RapidOCR-Torch), `vision/provider.py` (Disabled / local OpenAI-compatible / Docling-local) |
| Metadata | `metadata/{schema,enrich,provenance}.py` |
| Dedup | `dedup.py` + `audit/source_registry.jsonl` |
| Classification | `classify/{taxonomy,rules,embeddings,arbiter,evidence,pipeline}.py` |
| Evidence / gate / staging | `evidence.py`, `quality_gate.py`, `staging.py` |
| Chunking | `chunking/{tokenizer,policy,chunker,quality,manifest}.py` |
| Orchestration | `pipeline.py`, `cli.py`, `scripts/promote_staging.py` |
| Config | `config/chunking.yaml` (new); `config/ingest.yaml` charts flag changed (see §5) |

Reuse rather than duplication: controlled vocabularies and the `infer_*` evidence
discipline are **imported** from `scripts/09_metadata_enrichment.py`; the fusion math and
loopback guard follow `crawler/src/hybrid_classifier.py`; the chunk tokenizer and token
budgets are carried over from the validated `scripts/11_semantic_chunking.py` policy.

## 3. Controlled smoke run

Synthetic fixtures only (`tests/ingest/fixtures/make_fixtures.py`), plus one synthetic
schema-2.0 crawler release. Command:
`.venv/bin/python scripts/ingest_incoming.py --source all --resume`.

| Metric | Value |
|---|---|
| Inputs detected | 9 (8 manual + 1 crawler) |
| Document identities | 8 — the DOCX arrived from **both** sources and collapsed into one document with two provenance sources |
| Originals preserved | 8/8 byte-identical, read-only |
| Formats recognized | PDF ×2, DOCX, PPTX, XLSX, PNG, JPG, TXT |
| Quality decisions | GO 4, REVIEW 4, REJECT 0, FAILED 0 |
| Evidence levels | STRUCTURED_DOCUMENT 3, IMAGE_OCR 2, STRUCTURED_TABULAR 1, VISUAL_ONLY 1, PARTIAL 1 |
| Chunks | 18 — TEXT 6, FIGURE 5, SHEET 3, TABLE 2, SLIDE 2 |
| Chunk quality | 2 PASS, 6 WARN, 0 FAIL |
| Embedding-ready | 8 eligible; 9 `DOCUMENT_NOT_STAGED` (REVIEW documents), 1 `TOO_SHORT` |
| Embeddings computed | **0** |
| Canonical promoted | **0** |

The WARNs are all `CHUNK_UNDER_MIN`: the synthetic fixtures are 9–52 tokens against a
250-token floor. That is the correct report for tiny inputs, not a defect.

`--dry-run` was verified to write nothing beyond `audit/ingest_dry_run.json`: no archive,
no Docling, no OCR, no staging, no chunks.

### Environment capabilities detected at run time

```json
{"libreoffice_available": false, "office_renderer_backend": null,
 "ocr_available": true, "ocr_engine": "rapidocr_torch",
 "vision_provider": "LocalOpenAICompatibleVisionProvider", "vision_available": true,
 "embedding_status": "AVAILABLE", "embedding_model": "text-embedding-nomic-embed-text-v1.5"}
```

Docling 2.124.0 / docling-core 2.93.0 / docling-ibm-models 4.0.1 / docling-parse 7.16.0.
The local Qwen arbiter (`qwen3.6-35b-a3b-mlx`) was reachable and was invoked only on
unsettled cases.

## 4. Verified end-to-end behaviours

- **Crawler contract (§76).** Schema-2.0 accepted; SHA mismatch, wrong producer and
  unsupported schema major rejected; schema 1.x only under `--allow-legacy-1x`; only
  `READY_FOR_HANDOFF` records processed.
- **Provisional is a hint, never the answer (§36, §42).** In the smoke run the crawler
  proposed `1.1` for the shared DOCX. The engine computed `2.1` independently, recorded
  `crawler_final_agreement: false` and raised `CRAWLER_FINAL_SECTION_DISAGREEMENT`, which
  moved the document to REVIEW. The provisional value is preserved in
  `classification.json` and in provenance.
- **One identity, many sources (§77).** Same bytes from crawler + manual →
  1 `originals/` entry, 1 `processing/` bundle, 1 `source_registry.jsonl` row with
  `source_kinds: [EXTERNAL_DISCOVERY, MANUAL_INTERNAL]` and `provenance_source_count: 2`.
- **Excel formulas survive (§16).** `=SUM(B2:B3)` is stored verbatim with `value: null`
  because openpyxl wrote no cached value. CSV emission is skipped for that sheet and the
  skip is reported (`XLSX_CSV_SKIPPED_UNRESOLVED_FORMULAS`); the values-only sheet does
  get a CSV.
- **OCR does not hallucinate (§75).** The text PNG OCRs to "Puskurtme Beton 20 cm / Kaya
  Bulonu / Celik Hasir". The gradient JPG yields `ocr_status: EMPTY`, `ocr_text: null`,
  evidence `VISUAL_ONLY`, decision REVIEW.
- **OCR text ≠ visual description (§24).** Both fields are populated independently. The
  gradient images received honest local-VLM descriptions ("mavi, mor ve kırmızı tonlarının
  yumuşak geçişleri") rather than invented tunnel content.
- **Local only (§80).** Every remote endpoint form — public API hosts, LAN addresses, the
  cloud metadata IP, scheme-relative URLs — raises `RemoteEndpointRejected` for vision,
  embedding and the LLM arbiter. A config asking for `enable_remote_services: true` still
  produces a pipeline with it off. A manual document was processed with every socket
  connection trapped, and none was attempted.

## 5. Deviations and the evidence for them

**Docling chart extraction disabled.** `PdfPipelineOptions.do_chart_extraction` exists in
2.124.0, but on a probe it emitted a complete fabricated "Bar chart" series table (X/Y/Value
rows) for a plain colour-gradient image with no chart in it. §22 conditions chart
extraction on the feature being "available *and stable*", and fabricated data is a stop
condition (§90), so `config/ingest.yaml → charts.enabled` is `false` with the reason
recorded in the file. Deterministic PPTX/XLSX chart metadata read from the original package
is still extracted. Status reported per document as `DISABLED`.

**Chunk token policy kept at the validated legacy values.** The task suggested 700/1000/150
as a starting point but §51 says to reuse tested values when a policy already exists. This
project's `scripts/11_semantic_chunking.py` policy (target 850, min 250, max 1200, hard max
1500, `unicode-lexical-v1`) was validated against the real 214-document corpus, so it was
carried over rather than re-tuned blind. `overlap_tokens: 80` is new.

**LibreOffice absent.** DOCX/PPTX/XLSX visual snapshots cannot be produced on this machine.
The `OfficeRenderer` abstraction is implemented and exercised; when unavailable it emits
`VISUAL_RENDERER_UNAVAILABLE`, which is a REVIEW reason and never a rejection (§11, §45).
Installing LibreOffice enables slide/page snapshots with no code change.

## 6. Defects found and fixed during this phase

| # | Defect | Fix |
|---|---|---|
| 1 | Titles fell back to the **archived** filename (`source.pdf`), so unrelated documents all got the title "source" and were merged as duplicates | `AdapterContext.original_filename` carries the incoming name; metadata infers from it |
| 2 | A filename-derived title could still merge two unrelated documents | `title_inferred_from_filename` marks the title weak; weak titles never drive rules 4/5 |
| 3 | Turkish dotless `ı` has no NFKD decomposition, so `normalize_title("Bakımı") == "bak m"` — Turkish title dedup was broken | explicit Turkish folding table before NFKD |
| 4 | `_crawler_provisional` read a flat key, but the contract consumer nests it under `crawler_provisional` — the crawler hint never reached the classifier | lookup covers the real nested shape (plus flat / `crawler_record` fallbacks) |
| 5 | A duplicate arriving in the same run was skipped as ALREADY_PROCESSED before its provenance was merged, losing the second source | inputs are grouped by identity **before** processing; every source contributes provenance, extraction runs once |
| 6 | A chunk of "H1, H1.1, body" took its heading path from the opening H1 instead of its content's H1 > H1.1 | heading path comes from the first content element |
| 7 | `capabilities["vision"]` was computed in the adapter, before the pipeline's vision stage ran, so it was always stale/false | recomputed after the OCR/vision stage; extraction report rewritten |
| 8 | A scanned PDF that Docling's own OCR recovered was graded `FULL_TEXT` | pdfium probes the native text layer before Docling; OCR-recovered scans are `IMAGE_OCR` |
| 9 | The same DOCX picture was extracted twice (Docling PictureItem + OOXML package member) whenever the re-encode differed by a byte | de-duplicate on **decoded pixels**, not file bytes |
| 10 | Docling's RapidOCR path defaulted to the onnxruntime backend, which is not installed, failing every OCR-enabled PDF conversion | backend pinned from `config/ocr.yaml` (`torch`), plus a retry without Docling OCR |
| 11 | docling-parse intermittently drops one page on first touch (non-deterministic across identical runs) | one retry, keeping whichever pass produced more content |
| 12 | `relpath()` captured `PROJECT_ROOT` as a default argument, so a relocated root produced absolute paths | base resolved at call time |
| 13 | `validate_pdf` leaked a file handle | context manager |

## 7. Tests

| Suite | Tests | Result |
|---|---|---|
| `tests/ingest/test_ingest_smoke.py` | 16 | OK |
| `tests/ingest/test_adapters.py` (§70–§75) | 26 | OK |
| `tests/ingest/test_pipeline.py` (§76–§78) | 39 | OK |
| `tests/ingest/test_chunking.py` (§79) | 40 | OK |
| `tests/ingest/test_security.py` (§80) | 22 | OK |
| `tests/ingest/test_end_to_end.py` (§76, §77, §82) | 18 | OK |
| **Total** | **161** | **161 PASS** |

```bash
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests/ingest -p 'test_*.py'
# Ran 161 tests — OK
```

### Relevant existing project tests (actually run)

Correct invocation is `PYTHONPATH=.:scripts:tests` — without `tests` on the path several
suites fail to import their `_loader` helper.

| Suite | Result |
|---|---|
| `test_metadata_enrichment` | 16 OK |
| `test_metadata_verification` | 18 OK |
| `test_metadata` | OK |
| `test_final_corpus` | 5 OK |
| `test_semantic_chunking` | 67 OK |
| `test_embedding_eligibility` | 44 OK |
| `test_duplicates`, `test_inventory`, `test_snapshot`, `test_recovery` | OK |
| `test_project_quality_gate` | 2 OK |
| `test_section_state` | 6 OK |
| `test_audit_cache` | 8 OK |
| `test_migration_integrity` | 7/8 — see below |
| `test_text_normalization` | 25/27 — see below |

**Two pre-existing failures, neither caused by this phase:**

1. `test_migration_integrity::test_no_nested_git_or_virtual_environment` asserts that no
   `.venv` exists anywhere under the project root. The Python 3.12 `.venv` the ingest engine
   requires was created in Phase B (2026-09-02 23:00) and is gitignored. The migration rule
   was written to catch environments *dragged in during migration*, which a deliberate,
   ignored root-level `.venv` is not. **Recommendation (not applied — this is a deliberate
   integrity guard and the call is yours):** either relax the assertion to ignore a
   gitignored root-level `.venv`, or move the virtualenv outside the project root.
2. `test_text_normalization` — one error and one failure asserting on artifacts that do not
   exist in this repository state (`reports/text_normalization_dry_run.md` is missing, and
   `reports/text_normalization_audit.md` uses a different section format than the test
   expects). Nothing in this phase touches `reports/` or `data/corpus_normalized/`.

Full-suite runs of the remaining ~90 legacy test files were **not** attempted: many require
Qdrant, production embeddings or the 2950-question evaluation, all of which are forbidden
here. No claim is made about them.

## 8. Artifacts

| Path | Contents |
|---|---|
| `reports/unified_ingest_engine_audit.md` | this document |
| `audit/unified_ingest_quality.json` | run summary, per-document detail, environment capabilities |
| `audit/ingest_manifest.jsonl` | one row per document per run |
| `audit/source_registry.jsonl` | dedup ledger: one row per document identity |
| `audit/embedding_ready_manifest.jsonl` | one row per chunk, eligibility + reason, **no vectors** |
| `audit/ingest_state.jsonl` | state machine with full transition history |
| `audit/document_id_map.jsonl` | SHA ↔ legacy/crawler id aliases |
| `docs/unified_ingest_contract.md` | input contract, bundle, asset/metadata schemas, gate, promotion |
| `docs/chunking_contract.md` | chunk types, boundaries, token policy, provenance, stable ids |
| `docs/architecture.md` | updated with the unified ingest flow |
| `README.md` | updated usage |

## 9. Decision

**CONDITIONAL_GO.**

Everything §92 requires is implemented and demonstrated: both input paths through one
engine, originals and provenance preserved, full local extraction with snapshots, tables,
figures, OCR and local vision, metadata without hallucination, global dedup, final
book-section classification against the single canonical taxonomy, per-document quality
gate, staging, structure-aware multimodal chunking with stable provenance, chunk quality
gate, and an embedding-ready manifest. Production embeddings, Qdrant indexing,
question-bank evaluation and canonical promotion were intentionally not executed.

The condition is environmental and documented, not structural:

- LibreOffice is not installed → Office visual snapshots unavailable (degrades to REVIEW).
- Docling chart extraction is disabled on evidence of fabrication.

Neither blocks a controlled real-data pilot. Before that pilot, expect classification on
short documents to lean on the rule/vote signals: the loopback embedding model maps most
section profiles into a narrow similarity band (0.83–0.84 on the smoke inputs), so
embedding contributes little separation on thin text. That is worth revisiting with real
documents, where the text is long enough for the signal to spread.
