# Unified Ingest Engine — Pre-Implementation Audit

- **Project:** TunnelBookAI V1 (`~/Projects/tunnelbookai_v1`)
- **Audit date:** 2026-09-02
- **Author:** Claude (Sonnet 5) — Phase A of the Unified Multimodal Ingest Engine task
- **Status:** Phase A complete. No source code changed. No destructive operation performed.

---

## 0. Executive summary

TunnelBookAI V1 already contains a **mature, resumable document pipeline** (`scripts/01_*`–`16_*`)
that converts a Windows-era source tree into a 214-document canonical Markdown corpus, plus a
**migrated PaperCrawler discovery pipeline** (`crawler/`) and a **staging materializer**
(`scripts/materialize_handoff.py`). The pieces that the Unified Ingest Engine needs but that
**do not exist yet** are:

| Needed capability | Exists today? |
|---|---|
| SHA256 inventory + exact/logical dedup | ✅ `scripts/01_inventory.py`, `scripts/02_duplicates.py` |
| Docling Markdown conversion | ⚠️ present but **bounded** (`docling_eligible()` caps: PDF ≤ 3 pages / 5 MB) |
| Local OCR (RapidOCR/Torch) | ✅ `scripts/03_convert.py` (`get_ocr_engine`, `pdf_rapidocr`, `image_convert`) |
| LibreOffice headless renderer detection | ✅ `utils.find_libreoffice()`, `03_convert.libreoffice_run()` |
| Legacy `.doc/.ppt/.xls` → OOXML | ✅ `03_convert.convert_legacy()` |
| **Page / slide / sheet PNG snapshots** | ❌ none (`07_snapshot.py` is an *inventory* snapshot, not page rendering) |
| **Embedded figure / picture extraction** | ❌ none |
| **Table extraction to CSV/JSON/PNG** | ❌ none (tables only survive as Markdown pipes) |
| **Chart data extraction** | ❌ none |
| **Docling structured JSON (`document.json`)** | ❌ none (only `export_to_markdown()` is called) |
| **XLSX structural model** (formulas, merged cells, named ranges, hidden sheets) | ❌ none (`fallback_xlsx` flattens to Markdown, `data_only=True` loses formulas) |
| Metadata schema + provenance | ⚠️ rich but CSV-shaped and crawler-specific (`09_metadata_enrichment.py`) |
| Metadata provenance map | ⚠️ per-field `*_evidence` / `*_confidence` columns exist, no JSON provenance object |
| Local vision / VLM adapter | ❌ none |
| Final section classification on TunnelBookAI side | ❌ none — only the **crawler's** `hybrid_classifier.py` exists |
| Canonical taxonomy (single source of truth) | ✅ `book/scope/normalized/book_scope.json` (66 sections) + `crawler/config/taxonomy.yaml` |
| `incoming/crawler` + `incoming/manual` inbox architecture | ❌ none |
| PaperCrawler **schema 2.0** contract consumer | ⚠️ only a schema **1.1** migrated package + `materialize_handoff.py` |
| Document-level ingest state machine / checkpoint | ⚠️ per-stage CSV manifests + `crawler/src/pipeline_state.py`, no unified doc state |
| Ingest quality gate (GO/REVIEW/REJECT per document) | ⚠️ `shared/project_quality_gate.py` is corpus/batch-level, not per-document |
| Corpus staging adapter | ✅ `scripts/materialize_handoff.py` (crawler-only) |
| Explicit `--dry-run` promotion script | ❌ none (`08_final_corpus.py` writes directly) |

**Bottom line:** ~55 % of the engine can be assembled by **reusing and refactoring** existing
code (`utils.py`, `03_convert.py`, `crawler/src/hybrid_classifier.py`, `materialize_handoff.py`,
`book_scope.json`). The remaining ~45 % — snapshots, asset extraction, structured Docling JSON,
XLSX structural model, vision adapter, per-document state machine, unified quality gate — is
**new work** and must be built as a proper `tunnelbookai/ingest/` package rather than more
numbered scripts.

---

## 1. Current project structure

```text
tunnelbookai_v1/            (NOT a git repo — no .git present)
├── config/                 config.yaml, paths.json, book_sections.json, metadata_llm*.{json,yaml}, book_qa.yaml
├── crawler/                migrated PaperCrawler discovery pipeline (src/ + config/ + tests/)
├── corpus/
│   ├── canonical/          214 *.md files, 25 MB — the FROZEN corpus (see §5 baseline)
│   ├── staging/            122 CAN_* bundles (source.md + provenance.json) from a prior crawler run
│   ├── metadata/           ~40 CSV/JSON manifests (final_metadata_master.csv = 214 rows, …)
│   ├── sidecars/full_docling_chunks/   per-DOC chunk sidecars
│   └── rejects/stale_handoff/
├── data/                   pipeline working area — inventory/, duplicates/, markdown/,
│                           markdown_full_docling/ (146 *.md), embeddings/ (BGE-M3), qdrant_storage/, …
│   └── <source tree mirror> "Leyla Literatür", "Sunumlar_2022", … (the ORIGINAL documents live here)
├── handoff/
│   ├── accepted/TunnelBookAI_Source_Pack/   migrated crawler package (schema_version 1.1)
│   │   ├── 00_registry/    handoff_contract.json, handoff_manifest.jsonl, checksums.sha256
│   │   ├── 01_originals/<ROUTE>/PC_*/   source.pdf|source.md + metadata.json + classification.json
│   │   └── 99_audit/       handoff_audit.json, review_queue.*, rejected_manifest.jsonl
│   ├── manifests/handoff_manifest.jsonl
│   └── review/review_queue.csv
├── book/
│   ├── scope/normalized/book_scope.json   ← CANONICAL TAXONOMY (66 sections, 59 QB sections)
│   ├── audits/            taxonomy_integration.json, question_bank_integrity.json (2950 questions)
│   └── drafts/ final/ evidence/
├── scripts/               139 entries — 01..16 = ingest/corpus, 17..107 = retrieval/book/prewriting
│   ├── utils.py           ← shared path/config/hash/CSV/LibreOffice helpers (REUSE)
│   ├── 03_convert.py      ← Docling + RapidOCR + LibreOffice + native fallbacks (REUSE/EXTEND)
│   ├── local_qwen.py      ← loopback-only LM Studio native chat client (REUSE)
│   └── materialize_handoff.py  ← crawler → corpus/staging bundle writer (REUSE/EXTEND)
├── shared/
│   ├── project_quality_gate.py   migration + crawler + corpus fail-closed gate
│   ├── book_qa.py
│   └── tunnelbookai-requirements.txt   ← docling>=2.0, openpyxl, pypdf, python-docx, python-pptx,
│                                          Pillow, pypdfium2, rapidocr>=3.0, PyYAML, cryptography
├── tests/                 104 test_*.py (unittest, `PYTHONPATH=.`)
├── audit/                 migration_manifest.json, pipeline_state.json, corpus_quality_gate.json,
│                          controlled_smoke_test.json
├── reports/               migration + stabilization + status reports
└── docs/architecture.md   responsibility boundary (crawler never writes canonical)
```

### Path / config system

- `config/paths.json` — declarative root map (`corpus_root`, `canonical_corpus_root`,
  `corpus_staging_root`, `handoff_root`, `audit_root`, …). **Authoritative; extend this, do not fork it.**
- `config/config.yaml` — source-tree scan config (`source_root: '..'`, supported extensions).
  Loaded by a **hand-rolled 2-level YAML parser** in `utils.load_config()` (PyYAML optional here).
- `scripts/utils.py` — `load_config`, `ensure_project_dirs`, `setup_logging`, `sha256_file`,
  `normalize_title`, `canonical_sort_key`, `extension_priority`, `read_csv/write_csv/write_jsonl`,
  `iso_time`, `mime_type_for`, `find_libreoffice`, `run_checked`, `strip_front_matter`, `native_path`.
- `crawler/src/project_paths.py` — separate path module for the crawler subtree
  (`CRAWLER_CONFIG_ROOT`, …). Crawler code uses `PYTHONPATH=crawler/src`.
- Env overrides: `TUNNEL_ROOT` (source root), `TUNNEL_EMBEDDING_SERVER`, `TUNNEL_LLM_SERVER`
  (both default `http://127.0.0.1:1234/v1`), `TUNNEL_PAPERS_DIR`, `OPENALEX_MAILTO`.

**Decision:** add `tunnelbookai/ingest/paths.py` that *reads* `config/paths.json` and adds the new
`incoming_*` / `processing_*` keys. Keep `scripts/utils.py` as the low-level helper library and
import from it.

---

## 2. Existing conversion code

### `scripts/03_convert.py` (baseline conversion — the main reuse target)

| Function | What it does | Reuse verdict |
|---|---|---|
| `docling_convert(source)` | Lazy-inits a module-global `DocumentConverter()`, returns `result.document.export_to_markdown()`. Sets `HF_HOME`/`TORCH_HOME` under `data/temp/model_cache`, `TORCHDYNAMO_DISABLE=1`. | **Refactor** — needs `PdfPipelineOptions` (page images, picture images, table structure, OCR) + `export_to_dict()` for `document.json`. |
| `docling_eligible(source, ext)` | Caps Docling to tiny files (PDF ≤ 3 pp & ≤ 5 MB; DOCX ≤ 1 MB; PPTX ≤ 2 MB; XLSX ≤ 1 MB), else native fallback. | **Drop the cap for the new engine** — the whole point of the "Full-Docling" pass (`05_full_docling.py`) is to run Docling unconditionally. Keep a config knob for CI/fixtures. |
| `fallback_pdf/docx/pptx/xlsx` | pypdf / python-docx / python-pptx / openpyxl(`data_only=True`) → Markdown. | **Keep as graceful degradation only.** `fallback_xlsx` with `data_only=True` **loses formulas** — must not be the XLSX authority (stop-condition §93). |
| `get_ocr_engine()` / `ocr_text(image)` | `RapidOCR(params={Det/Cls/Rec.engine_type: TORCH})`, returns `result.txts`. No language config, no confidence. | **Reuse** — wrap in an `OcrProvider` and add `ocr_languages` config; RapidOCR confidence is not exposed → leave `ocr_confidence: null` (never fabricate, §25). |
| `image_convert(source)` | PIL size + filename caption + RapidOCR. Explicitly labels the caption "conservative", no LLM. Emits `"OCR ile metin tespit edilmedi."` when empty. | **Good pattern — reuse.** Already separates OCR text from a non-hallucinated caption (aligns with §26). |
| `pdf_rapidocr(source, root, logger)` | pypdfium2 render @ scale 1.2 → RapidOCR per page, JSONL page cache keyed by SHA. | **Reuse for the OCR path**; the render loop is 80 % of the page-snapshot renderer (just needs scale 2.0 + PNG persistence + dimensions). |
| `convert_legacy(...)` | OOXML-magic-copy or LibreOffice `--convert-to`. | **Reuse** for `.doc/.ppt/.xls`. |
| `libreoffice_run(...)` / `libreoffice_to_pdf(...)` | Isolated `UserInstallation` profile, `SAL_USE_VCLPLUGIN=svp`, `SAL_DISABLE_OPENCL=1`. | **Reuse as the `OfficeRenderer` backend** (DOCX/PPTX/XLSX → temp PDF → PNG). |
| `detected_ooxml_extension(source)` | ZIP magic sniff (`word/`, `ppt/`, `xl/`). | **Reuse** in the format registry / MIME detection. |
| `recover_empty_output(...)` | Forces LibreOffice-PDF + RapidOCR when a fast converter yields no text. | **Reuse** as the "native-text-empty ⇒ OCR" branch of the PDF/DOCX pipeline. |

### `scripts/05_full_docling.py` (the "full pass")

- Iterates `conversion_manifest.csv` rows where converter ≠ docling, extension ∈
  `{.pdf,.docx,.pptx,.pptm,.xlsx}`, sorted by size ascending, resumable (SHA + output-exists check).
- Calls `convert.docling_convert(source)` and writes **only Markdown** to
  `data/markdown_full_docling/<mirror>.md` with YAML front-matter.
- **No page images, no `document.json`, no assets.** This is the file to supersede.

### `scripts/07_snapshot.py` — **NOT a page renderer**

Despite the name, this produces an **immutable inventory snapshot** (`data/inventory/snapshots/…`)
with an `archive_digest` and Office-lock detection. Keep it; it is unrelated to page PNGs.

### Docling API usage today

Only `DocumentConverter().convert(path).document.export_to_markdown()`. **No** `PdfPipelineOptions`,
`ConversionResult` inspection, `export_to_dict()`, `document.pages[*].image`,
`picture.get_image()`, or `TableItem.export_to_dataframe()`. Task §10/§78 require **runtime API
inspection** — mandatory because the installed Docling version is currently **unknown / not installed**
(see §11).

---

## 3. Existing Docling / OCR / renderer dependency reality

| Dependency | Declared | Installed now |
|---|---|---|
| Python | 3.10–3.12 implied by `docling` | **3.14.6** is the only interpreter with `pip`; 3.12 & 3.13 available via `uv` / Homebrew |
| `docling` | `>=2.0` (`shared/tunnelbookai-requirements.txt`) | **NOT installed anywhere** (checked global, `paper-crawler-agent/.venv`, `survey_docx_pipeline/.venv`) |
| `rapidocr`, `pypdfium2`, `torch`, `openpyxl`, `python-docx`, `python-pptx`, `Pillow` | declared | **none installed** (`pip list` = pip, wheel only) |
| LibreOffice | runtime-detected | `/Applications/LibreOffice.app/Contents/MacOS/soffice` — **presence unverified** (check at build time) |
| local embedding server | `http://127.0.0.1:1234/v1` (nomic-embed via LM Studio) | not running during audit |
| local LLM (Qwen) | `http://127.0.0.1:1234/v1` model `qwen3.6-35b-a3b-mlx` | not running during audit |

**Consequences / required first build step:**

1. Create a dedicated **Python 3.12** virtualenv (`uv venv --python 3.12 .venv` at project root;
   `.venv/` is already git-ignored). Python 3.14 is too new for the Docling/torch stack.
2. `uv pip install -r shared/tunnelbookai-requirements.txt` (pin exact versions into a new
   `requirements-ingest.lock` — task §77 "pinned/locked existing policy").
3. **Then** run a one-off `python -c "import docling; print(docling.__version__)"` + introspect
   `docling.datamodel.pipeline_options` and `docling_core.types.doc` to write the API-compat
   adapter (`tunnelbookai/ingest/docling_adapter.py`). Do **not** assume 2.x names.
4. The pre-existing pipeline was demonstrably run **on Windows** (`data/inventory/inventory.csv`
   holds `C:\Users\bulsa\…` paths). The macOS run will need a fresh inventory anyway — the new
   engine reads from `incoming/`, not from `inventory.csv`, so this is not a blocker.

---

## 4. Existing metadata pipeline

- `scripts/04_metadata.py` — regex/keyword inference (title from first H1, years, ~35 topic rules,
  language guess). Deterministic, no LLM. Writes `data/metadata/markdown_metadata.csv`.
- `scripts/09_metadata_enrichment.py` — the **master** metadata model. Controlled vocabularies:
  - `LANGUAGES = {tr,en,de,mixed,unknown}`
  - `AUTHORITY_LEVELS = {A,B,C,D,unclassified}`
  - `DOCUMENT_TYPES` — 24 values (`regulation`, `technical_specification`, `standard`, `manual`,
    `academic_article`, `thesis`, `technical_report`, `presentation`, `cost_analysis`,
    `inventory`, `drawing`, `spreadsheet`, …)
  - `TOPICS` — ~55 controlled tags
  - `CITATION_MODES = {pdf_page, slide, document_section, table_or_sheet, image, source_only}`
  - Per-field `*_current` / `*_suggested` / `*_evidence` / `*_confidence` columns +
    `requires_human_review` / `review_status`.
- `scripts/05_metadata_llm_review.py`, `06_metadata_review.py`, `06_metadata_adjudication.py`,
  `07_metadata_verification.py` — LLM review + human adjudication loop.
  `config/metadata_llm.yaml` (`enabled: false`, loopback base_url, qwen model).
- Output: `corpus/metadata/final_metadata_master.csv` (**214 rows**, header verified).

**Reuse verdict:** the **vocabularies and the `*_evidence`/`*_confidence` discipline are the
canonical metadata contract** — the new `metadata.json` schema (§30) must map onto them
(`document_type`, `authority_level` → `final_evidence_level` is *separate*, `topics`, `language`).
The CSV master stays the corpus-level index; per-document `processing/<id>/metadata.json` +
`metadata_provenance` (§31) is the new artifact. **Add** the fields the master lacks:
`confidentiality` (§33), `document_status` (§34), `source_kind`, `organization`, `department`,
`revision`, `doi`, `source_url`, `final_primary_section`, `final_secondary_sections`,
`final_section_confidence`, `final_evidence_level`, `content_capabilities`.

**Hallucination guard (already partly enforced):** `09_metadata_enrichment.py` uses `MISSING =
{"", "unknown", "unclassified", "null", "none"}` and keeps `*_evidence`. The new LLM enrichment
must keep `inferred=true`/`confidence`/`reason` and never fill `organization`/`date`/`author`
without evidence (§32, stop-condition §93).

---

## 5. Existing corpus integrity baseline (Phase A step 5)

Captured **before any implementation** so non-destructiveness can be proven later:

```text
corpus/canonical/           214 *.md files, 25 MB
canonical_corpus_tree_digest
    = sha256( "".join( f"{sha256(file)}  {relpath}\n"
                       for *.md sorted by POSIX relpath under corpus/canonical/ ) )
    = 6c49a13c0f3715ac54f44cb206a18096d596c80ad5ea47891dbeebd9bdef0470
    (reproduce: scripts/verify_canonical_baseline.py)

corpus/staging/              122 CAN_* bundles, 244 files  (prior crawler materialization)
corpus/metadata/             576 files
  final_metadata_master.csv    214 data rows
  final_corpus_manifest.csv    214 data rows
book/scope/normalized/book_scope.json   section_count = 66, question_bank_section_count = 59
book/audits/taxonomy_integration.json   total_questions = 2950, decision = PASS
book/audits/question_bank_integrity.json  decision = PASS
```

The digest command is recorded in `audit/unified_ingest_quality.json` (to be produced in Phase I)
and re-checked as a **stop condition** (§93 "existing canonical corpus changed").
A helper `scripts/verify_canonical_baseline.py` should be added that recomputes this digest and
fails non-zero on drift.

---

## 6. Existing image / table / figure extraction

**Table extraction:** none beyond Markdown pipe tables emitted by Docling / `fallback_*`.
No `tables/TABLExxxx.{csv,json,png}`. `openpyxl` is used with `data_only=True` (values only,
**formulas discarded**). → **new work** (§15, §21, §22).

**Figure / embedded-image extraction:** none. Docling is never asked for `generate_picture_images`;
DOCX `word/media/*` and PPTX slide images are never unpacked. → **new work** (§14, §18, §19).

**Page/slide/sheet snapshots:** none. `pdf_rapidocr` renders pages via pypdfium2 but discards the
bitmaps after OCR. → **new work**, but the render loop is reusable (§13, §20, §23).

**Charts:** none. → **new work, non-blocking** (§16 — `NOT_SUPPORTED`/`NOT_RUN`/`SUCCESS`/`FAILED_NONBLOCKING`).

---

## 7. Existing section classifier

**On the TunnelBookAI side:** none for documents. (`book/` has question-bank taxonomy tooling and
`scripts/55_cp3_coverage_mapping.py` for coverage, but no doc→section classifier.)

**On the crawler side (reusable pattern, do not modify in place):**

- `crawler/src/classification_engine.py` — deterministic first pass: `DOCUMENT_TYPES` (20),
  `TOPIC_TERMS` (~40), rule-based section scoring against `crawler/config/taxonomy.yaml`.
- `crawler/src/hybrid_classifier.py` — **rules + local embeddings + local LLM review**, with a
  hard security boundary:
  - `is_loopback_url()` — only `localhost/127.0.0.1/::1` (+ loopback IP range check via `ipaddress`).
  - Embeddings never use cloud fallback; LLM may only pick **existing taxonomy section IDs**;
    LLM cannot change type/authority/evidence/route/SHA/provenance.
- `crawler/config/classification_policy.yaml` — fusion weights (`rule_weight 0.55`,
  `embedding_weight 0.45`, `auto_accept 0.88`, `llm_review 0.52`, `disagreement_margin 0.10`),
  `max_candidate_sections 8`, `max_selected_sections 5`, embedding model term `nomic-embed`,
  local servers `127.0.0.1:{1234,11434,8000}`.
- `crawler/config/taxonomy.yaml` — section id → `{title, strong_terms, medium_terms}` for **all 66
  `book_scope.json` sections** (verified: ids `1`, `1.1`, … `1.5.2`, `2`, `2.1`, … match).

**Decision:** the TunnelBookAI **final** classifier (`tunnelbookai/ingest/classify/`) should
**import** `crawler.src.hybrid_classifier` logic (or copy the loopback-guard + fusion math into a
shared module) and drive it with the *full normalized document* (headings + full text + table
captions + figure captions + OCR text), not just title+abstract. It must:
- treat `provisional_primary_section` as a **feature only** (§42, stop-condition §93);
- emit `classification.json` with `classification_methods`, `crawler_provisional_section`,
  `crawler_final_agreement`, `supporting_elements` (element-ref evidence, §46);
- support `final_secondary_sections` with a configurable threshold (§47);
- use the **hierarchical** flow of §41 (chunk → embed candidate retrieval → chunk votes → rule
  signals → Qwen arbitration only on disagreement/low-confidence).

**Embedding stacks — note the split:** retrieval uses local **BGE-M3** weights via `transformers`
(`scripts/14_full_embedding.py`); crawler classification uses the **loopback OpenAI-compatible
nomic-embed** server. §43 says "reuse local embedding setup, read endpoint from config, loopback
only" → reuse the **crawler/classification** stack (nomic via `127.0.0.1:1234/v1`), configured in
`config/classification.yaml`, not the BGE-M3 retrieval path.

---

## 8. Existing corpus staging & canonical promotion logic

- **Staging:** `scripts/materialize_handoff.py` — reads `handoff/accepted/TunnelBookAI_Source_Pack/
  00_registry/handoff_manifest.jsonl`, hardlink-or-copy into `corpus/staging/<canonical_id>/`,
  writes `provenance.json` sidecar per bundle, moves unknown staging dirs to
  `corpus/rejects/stale_handoff/`. **Crawler-only, schema 1.1.** Bundle shape today:
  `corpus/staging/CAN_*/{source.md|source.pdf, provenance.json}` — **flat**, not the rich
  `processing/<id>/` bundle of §37.
- **Canonical promotion:** `scripts/08_final_corpus.py` — selects baseline vs full-Docling variant,
  copies into `corpus/canonical/<mirror path>.md`, writes `final_corpus_manifest.csv` +
  `final_metadata_master.csv`, `tree_digest` verification. **Writes canonical directly; no
  `--dry-run`, no `--apply` gate.** Task §53 requires a new `scripts/promote_staging.py` that
  **defaults to dry-run**. `08_final_corpus.py` must **not** be run during this task (§52, §90, §91).
- **Gate:** `shared/project_quality_gate.py` — fail-closed, corpus/batch level
  (`migration_integrity_failed`, `pipeline_incomplete`, `reconciliation_broken`,
  `coverage_accounting_broken`, hash/provenance checks). Decision enum `PASS / CONDITIONAL_GO /
  NO_GO`. **Per-document GO/REVIEW/REJECT (§50) is new** but should feed this gate's inputs.

---

## 9. PaperCrawler contract — version gap

| | This repo (`handoff/accepted/…`) | Current PaperCrawler (`~/Projects/paper-crawler-agent`, VERSION `1.0.0`) |
|---|---|---|
| `handoff_contract.json` `schema_version` | **`1.1`** | **`2.0`** (`docs/handoff_contract.md`) |
| `classification.json` `schema_version` | `2.2` | (per-doc, unchanged layout) |
| producer string | `paper-crawler-agent` | `paper-crawler-agent` |
| section fields | `primary_section`, `book_sections[]`, `classification_confidence` | **`provisional_primary_section`, `provisional_secondary_sections[]`, `provisional_section_confidence`, `provisional_classification_status`** + `final_*` = null / `NOT_EVALUATED` |
| evidence field | `evidence_level` (`ABSTRACT`, …) | **`crawler_evidence_level`** ∈ `{ORIGINAL_ACQUIRED, LIGHT_PDF_TEXT, WEB_SNAPSHOT_TEXT, ABSTRACT, TITLE_METADATA_ONLY}` — **never `FULL_TEXT`/`PDF_EXTRACT`** |
| statuses | `paper_crawler_status`, `tunnelbookai_status` | same + `METADATA_REFERENCE`, `RETRY_ACQUISITION`, `MANUAL_REVIEW`, `AUTO_REJECT` |
| package audit | `handoff_audit.json` | + `handoff_quality_gate.json` (GO/CONDITIONAL_GO/NO_GO), `decision_summary.json`, `retry_acquisition.jsonl`, `reclassify_queue.jsonl`, `metadata_references.jsonl` |
| new fields | — | `source_kind: "EXTERNAL_DISCOVERY"`, `source_representation{original_or_raw, crawler_normalized, crawler_normalized_status}`, `canonical_hint_id` |

**Consumer requirements (task §5, §72):** the ingest engine's `CrawlerContractConsumer` must:

1. Accept **schema major == 2** (`schema_version` starts `"2."`); accept the legacy `1.1`
   migrated package **on read** with a field remap (`primary_section` → `provisional_primary_section`,
   `evidence_level` → `crawler_evidence_level`); **never re-emit** legacy names.
2. Validate: `producer == "paper-crawler-agent"`, `paper_crawler_status == READY_FOR_HANDOFF`,
   `tunnelbookai_status == NOT_INGESTED`, SHA256 of `local_path` == manifest `sha256`,
   source file exists, `provenance` non-empty.
3. Reject: SHA mismatch, wrong producer, `schema_version` major ≠ 2 (with a `--allow-legacy-1x`
   opt-in for the migrated pack), `METADATA_REFERENCE` marked ready, missing provenance.
4. **Preserve** `provisional_*` + `crawler_evidence_level` into `provenance.json`; compute
   `final_primary_section` / `final_evidence_level` **independently** (§39, §48).
5. Expect the release at `incoming/crawler/RELEASE_YYYY_MM_DD/` (or `incoming/crawler/releases/`).

**Do not modify `~/Projects/paper-crawler-agent` (§1, §87).** Read-only inspection only — done.
The in-repo `crawler/` subtree is TunnelBookAI's own migrated copy; prefer **not** to edit
`crawler/src/*` either (keeps the producer boundary clean) — import from it instead.

---

## 10. Existing tests & environment

- 104 `tests/test_*.py`, `unittest`, run with `PYTHONPATH=.` (repo) and
  `PYTHONPATH=crawler/src` (crawler). `tests/_loader.py` helper.
- Relevant existing tests to keep green: `test_inventory.py`, `test_duplicates.py`,
  `test_metadata*.py`, `test_final_corpus.py`, `test_full_embedding.py`.
- No `pyproject.toml` / `setup.py` — the project runs as loose modules on `PYTHONPATH`.
  New engine should follow suit: `tunnelbookai/` importable package + `scripts/ingest_incoming.py`
  thin entrypoint, tests under `tests/ingest/`.
- No CI config found. No `.pre-commit-config`. `.gitignore` covers `.venv/`, `__pycache__`,
  `data/temporary/*`.

---

## 11. Dependency & tooling decisions (locked for Phase B onward)

| Concern | Decision |
|---|---|
| Interpreter | `uv venv --python 3.12 .venv` at project root |
| Install | `uv pip install -r shared/tunnelbookai-requirements.txt`; freeze to `requirements-ingest.lock` |
| Docling API | runtime-introspected adapter `tunnelbookai/ingest/docling_adapter.py`; no hard-coded 2.x symbol names; feature flags degrade to `NOT_SUPPORTED` |
| Snapshot renderer (PDF) | `pypdfium2` (already a dep) @ configurable scale (default 2.0) |
| Snapshot renderer (Office) | `OfficeRenderer` interface over `utils.find_libreoffice()` + `libreoffice_run`; `available()` / `render_to_pdf()` / `render_snapshots()`; unavailable ⇒ `VISUAL_RENDERER_UNAVAILABLE` warning, **not** REJECT (§20, §51) |
| OCR | `OcrProvider` wrapping RapidOCR-Torch; `ocr_languages: [tr, en]`; `ocr_confidence: null` |
| Vision | `VisionProvider` plugin: `DisabledVisionProvider` (default) / `DoclingLocalVisionProvider` / `LocalOpenAICompatibleVisionProvider` — loopback hosts only, autodetect, `visual_description_status = NOT_RUN` when absent (§27, §28) |
| Embeddings (classification) | loopback OpenAI-compatible nomic-embed (`config/classification.yaml`), reuse crawler fusion math |
| LLM (classification arbitration + metadata) | `scripts/local_qwen.py` client, loopback-only, called **only** on disagreement/low-confidence (§44) |
| Network | `local_only: true`, `NETWORK_EGRESS = DENY` for manual ingest; no remote services (§27, §76) |
| Config | new `config/ingest.yaml`, `config/ocr.yaml`, `config/vision.yaml`, `config/metadata.yaml`, `config/classification.yaml`, `config/quality_gate.yaml`; all read through the existing `paths.json`-based resolver |

---

## 12. Target architecture (to be built)

```text
incoming/
├── crawler/releases/RELEASE_YYYY_MM_DD/   (PaperCrawler schema-2.0 packages, read-only input)
├── manual/inbox/                          (user drops PDF/DOCX/PPTX/XLSX/PNG/JPG/TXT/MD/CSV/HTML)
├── manual/README.md
└── quarantine/                            (format/security failures; originals retained)

originals/<document_id>/source.<ext> + original.json        (immutable archive, §7)

processing/<document_id>/
├── normalized/{document.md, document.json, document.txt}
├── pages/  figures/  tables/  charts/  slides/  sheets/
├── metadata.json  metadata_provenance.json  provenance.json
├── extraction_report.json  classification.json  quality_gate.json

audit/
├── ingest_state.jsonl        (per-document state machine, atomic append)
├── ingest_manifest.jsonl     (one row per input)
├── source_registry.jsonl     (merged crawler + manual provenance per canonical doc)
└── unified_ingest_quality.json

tunnelbookai/ingest/
├── paths.py  config.py  state.py  ids.py  format_registry.py
├── original_archive.py
├── docling_adapter.py
├── adapters/{pdf,docx,pptx,xlsx,image}.py
├── assets/{snapshots,figures,tables,charts}.py
├── ocr/provider.py    vision/provider.py
├── metadata/{schema,enrich,provenance}.py
├── dedup.py
├── sources/{crawler_contract,manual_inbox}.py
├── classify/{pipeline,embeddings,rules,arbiter,evidence}.py
├── evidence.py  quality_gate.py  staging.py
└── cli.py     →  scripts/ingest_incoming.py  (thin wrapper)

scripts/
├── ingest_incoming.py            (--source crawler|manual|all, --dry-run, --resume, …)
├── promote_staging.py            (DEFAULT --dry-run; --apply NOT run in this task)
└── verify_canonical_baseline.py  (recompute §5 digest, fail on drift)
```

Stable document ID (§8): `content SHA256` is the identity key; keep a
`audit/document_id_map.jsonl` mapping `sha256 ↔ DOC###### (legacy) ↔ CAN_… (crawler) ↔ ingest id`.
Same SHA from crawler + manual ⇒ **one** canonical document, **two** provenance sources in
`source_registry.jsonl` (`EXTERNAL_DISCOVERY` + `MANUAL_INTERNAL`).

---

## 13. Reuse / Refactor / Extend ledger

| Existing asset | Action | New home |
|---|---|---|
| `scripts/utils.py` | **Reuse** (import) | low-level lib |
| `scripts/03_convert.py` `docling_convert`, `image_convert`, `pdf_rapidocr`, `libreoffice_*`, `convert_legacy`, `detected_ooxml_extension`, `get_ocr_engine` | **Refactor** into `ingest/docling_adapter.py`, `ingest/adapters/*`, `ingest/ocr/`, `ingest/assets/snapshots.py`, `OfficeRenderer` | new package |
| `scripts/05_full_docling.py` resume/skip loop | **Extend** | `ingest/state.py` + `adapters` |
| `scripts/09_metadata_enrichment.py` vocabularies + `*_evidence` discipline | **Reuse** (import constants), **Extend** schema | `ingest/metadata/` |
| `crawler/src/hybrid_classifier.py` + `classification_engine.py` + `config/{taxonomy,classification_policy}.yaml` | **Reuse** (import), **Extend** to full-document hierarchical flow | `ingest/classify/` |
| `crawler/src/pipeline_state.py` (atomic checkpoint pattern) | **Reuse** pattern | `ingest/state.py` |
| `scripts/materialize_handoff.py` | **Refactor/Extend** into `ingest/sources/crawler_contract.py` + `ingest/staging.py` | new package |
| `scripts/local_qwen.py` | **Reuse** (import) | `ingest/classify/arbiter.py`, `ingest/metadata/enrich.py` |
| `book/scope/normalized/book_scope.json` | **Reuse** (single taxonomy — §40) | `ingest/classify/` loads it |
| `shared/project_quality_gate.py` | **Extend** (feed per-doc results in) | keep + `ingest/quality_gate.py` |
| `config/paths.json` | **Extend** (add `incoming_*`, `processing_*`, `originals_root`) | same file |

---

## 14. Risks & open questions

1. **Docling on Python 3.12 / macOS ARM** — install size (torch) is large; first `DocumentConverter`
   call downloads models to `data/temp/model_cache`. Needs a network-allowed *setup* step
   (distinct from the network-denied *manual ingest* runtime, §76). Fixture smoke test must be
   runnable offline once models are cached.
2. **Docling structured JSON schema** varies across 2.x minor versions — the adapter must snapshot
   `docling.__version__` into every `extraction_report.json`.
3. **LibreOffice presence on this Mac is unverified** — DOCX/PPTX/XLSX visual snapshots may be
   `VISUAL_RENDERER_UNAVAILABLE` on first run. That is CONDITIONAL_GO, not NO_GO (§51).
4. **No local LLM/embedding server running** — classification will fall back to rules-only +
   `final_section_confidence` capped; Qwen arbitration path untestable without the server. Tests
   must mock the loopback client.
5. **Contract version drift** — the only crawler package on disk is schema 1.1. A real schema-2.0
   package to test §72 must be **synthesized** as a fixture (task explicitly asks for this).
6. **`corpus/staging/` already holds 122 crawler bundles** in the *old flat shape*. The new engine
   writes the rich `processing/<id>/` bundle; staging adapter must not collide with or delete the
   existing 122 (non-destructive, §52). Use a new sub-path or a shape-version marker.
7. **Python 3.14 default interpreter** — every new script must be robust to being launched with the
   wrong interpreter; add an early version guard that points at `.venv`.

---

## 15. Decision

**PROCEED to Phase B.** Implementation order per task §92, adjusted for the environment reality:

- **B0 (new, blocking):** create `.venv` (py3.12) + install + lock deps + Docling API probe →
  `reports/docling_api_probe.md`.
- **B1–B5:** `incoming/` architecture, `originals/` archive, format registry, `ingest/state.py`,
  unified ingest interface + `config/*.yaml`.
- **C:** PDF → DOCX → PPTX → XLSX → image adapters (reusing `03_convert.py`).
- **D:** snapshots, figures, tables, OCR provider, vision adapter.
- **E:** metadata schema + provenance, global dedup, crawler schema-2.0 contract consumer.
- **F:** final section classification (reuse `hybrid_classifier`), evidence model, per-doc quality
  gate, staging adapter (non-destructive).
- **G:** `scripts/ingest_incoming.py` CLI, checkpoint/resume, logging/audit.
- **H:** unit + integration + synthetic smoke + security tests (fixtures only, §65, §90).
- **I:** README, `docs/architecture.md` update, `docs/unified_ingest_contract.md`,
  `reports/unified_ingest_engine_audit.md`, `audit/unified_ingest_quality.json`.

**Guardrails held throughout:** no writes to `corpus/canonical/` (baseline digest §5), no
`08_final_corpus.py`, no `promote_staging.py --apply`, no edits under `~/Projects/paper-crawler-agent`,
no production question-bank / Qdrant / embedding rebuild, manual-ingest network egress denied,
crawler provisional classification never treated as final.
