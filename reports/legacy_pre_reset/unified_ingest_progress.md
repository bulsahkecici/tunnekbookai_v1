# Unified Ingest Engine — Build Progress

Tracks the phased plan from the master task against what is on disk.
**All phases are now complete.** Final audit: `reports/unified_ingest_engine_audit.md`.
Last updated: 2026-09-03.

## Guardrails held (verified this session)

- `scripts/verify_canonical_baseline.py` → **PASS** (214 files,
  digest `6c49a13c0f3715ac54f44cb206a18096d596c80ad5ea47891dbeebd9bdef0470`). Canonical corpus untouched.
- No edits under `~/Projects/paper-crawler-agent` (read-only inspection of `docs/handoff_contract.md` only).
- No `08_final_corpus.py`, no `promote_staging.py --apply`, no Qdrant / embedding / question-bank runs.
- Manual ingest path performs zero network calls.

## Phase A — Audit ✅ COMPLETE

- `reports/unified_ingest_preimplementation_audit.md` — full reuse/refactor/extend ledger,
  contract version-gap analysis, corpus baseline, risks, decision.
- `reports/docling_api_probe.md` — runtime Docling 2.124.0 / docling-core 2.93.0 API surface
  (page/picture/table images, `export_to_dict`, chart extraction, local VLM, RapidOCR options).

## Phase B — Foundations ✅ COMPLETE (runnable)

| Item | File | Status |
|---|---|---|
| Python 3.12 venv + deps | `.venv/`, `requirements-ingest.lock` (106 pinned pkgs) | ✅ docling, torch 2.14, rapidocr, openpyxl, python-docx/pptx, pypdfium2 |
| `incoming/` architecture | `incoming/{crawler/releases,manual/inbox,quarantine}/` | ✅ |
| Manual inbox README | `incoming/manual/README.md` | ✅ (TR, task §61) |
| Config files | `config/{ingest,ocr,vision,metadata,classification,quality_gate}.yaml` | ✅ (task §59, §60) |
| Path resolution | `tunnelbookai/ingest/paths.py` (extends `config/paths.json`) | ✅ |
| Config loader | `tunnelbookai/ingest/config.py` | ✅ |
| Stable document ID (§8) | `tunnelbookai/ingest/ids.py` (`ING_<sha256[:20]>` + `DocumentIdMap`) | ✅ |
| Format registry (§9) | `tunnelbookai/ingest/format_registry.py` (OOXML magic sniff, legacy gating) | ✅ |
| State machine (§55, §56) | `tunnelbookai/ingest/state.py` (atomic jsonl, 16 states, resume rank) | ✅ |
| Original archive (§7) | `tunnelbookai/ingest/original_archive.py` (immutable, read-only, idempotent, SHA-conflict guard) | ✅ |
| Manual source (§6) | `tunnelbookai/ingest/sources/manual_inbox.py` | ✅ |
| PaperCrawler contract consumer (§5, §72) | `tunnelbookai/ingest/sources/crawler_contract.py` (schema-2.0, legacy-1.1 opt-in remap, per-record gate, provisional preserved) | ✅ |
| CLI (§62, §63) | `tunnelbookai/ingest/cli.py` + `scripts/ingest_incoming.py` | ✅ `--source`, `--dry-run`, `--resume`, `--force-reprocess`, `--document-id`, `--max-documents`, `--no-ocr`, `--no-vision`, `--allow-legacy-1x` |
| Baseline verifier (§2, §91) | `scripts/verify_canonical_baseline.py` | ✅ |
| Test fixtures (§65) | `tests/ingest/fixtures/make_fixtures.py` (synthetic pdf/docx/pptx/xlsx/png-text/jpg-photo/txt) | ✅ |
| Phase-B tests | `tests/ingest/test_ingest_smoke.py` | ✅ 16/16 pass (format detect, ids, discovery, archive immutability, state resume, crawler contract accept/reject matrix) |

**Verified end-to-end:** drop 4 fixtures in `incoming/manual/inbox/` → `--dry-run` inventory →
`--resume` → 4 immutable originals archived + `original.json` + per-doc `provenance.json` +
`audit/ingest_state.jsonl` + `audit/ingest_manifest.jsonl`. Documents stop at `QUEUED` with
warning `EXTRACTION_NOT_IMPLEMENTED` (Phase C boundary).

## Phase C — Format adapters ✅ COMPLETE

`docling_adapter.py` (version-guarded, retries a partial page parse, forces
`enable_remote_services=False`), `extraction.py` (`ExtractionResult`), `elements.py`
(shared structural element stream), and `adapters/{pdf,docx,pptx,xlsx,image,text}.py`.
Each writes `processing/<id>/normalized/{document.md,document.json,document.txt}`.
XLSX uses openpyxl with `data_only=False` **and** a cached-value pass; a formula without a
cached value stays `null`.

## Phase D — Assets / OCR / Vision ✅ COMPLETE

`assets/{snapshots,figures,tables,charts}.py`, `office_renderer.py`, `ocr/provider.py`
(RapidOCR-Torch, `ocr_confidence: null`, photographic skip gate), `vision/provider.py`
(Disabled / local OpenAI-compatible / Docling-local, loopback-only). Chart extraction is
**disabled on evidence** — see the audit report §5.

## Phase E — Metadata / Dedup ✅ COMPLETE

`metadata/{schema,enrich,provenance}.py` (vocabularies imported from
`scripts/09_metadata_enrichment.py`; `inferred=true` requires reason + confidence at code
level) and `dedup.py` + `audit/source_registry.jsonl` (sha → doi → url → title → fuzzy).

## Phase F — Classification / Evidence / Gate / Staging ✅ COMPLETE

`classify/{taxonomy,rules,embeddings,arbiter,evidence,pipeline}.py`, `evidence.py`,
`quality_gate.py`, `staging.py` (`corpus/staging/v2/`, legacy 122 bundles untouched),
`scripts/promote_staging.py` (dry run by default; refuses `corpus/canonical`).

## Phase J — Structure-aware chunking ✅ COMPLETE

`config/chunking.yaml` + `chunking/{tokenizer,policy,chunker,quality,manifest}.py`.
Six chunk types, heading path and page/slide/sheet provenance, stable content-derived ids,
intra-document near-duplicate suppression, chunk quality gate, embedding-ready manifest.
Authoritative location: `processing/<id>/chunks/chunk_manifest.jsonl`.

## Phase G/H/I — CLI / tests / docs ✅ COMPLETE

CLI runs the full stage chain (§67) with `--no-chunking`, `--no-arbiter` and `--from-stage`
added. 161/161 tests in `tests/ingest/`. Docs: `docs/unified_ingest_contract.md`,
`docs/chunking_contract.md`, updated `docs/architecture.md` and `README.md`.

## Overall decision

**CONDITIONAL_GO** — see `reports/unified_ingest_engine_audit.md` for the evidence, the
13 defects found and fixed, the two documented deviations (LibreOffice absent, Docling
chart extraction disabled) and the two pre-existing legacy test failures.
