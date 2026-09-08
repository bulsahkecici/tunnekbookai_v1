# TunnelBookAI V1 — Pilot Readiness

Date: 2026-09-03
Scope: LibreOffice enablement, legacy test cleanup, pilot readiness assessment.
Not executed in this task: production ingestion, embeddings, Qdrant, canonical promotion,
the 2950-question evaluation, and any real user document.

**Decision: GO for the 6-document real-data pilot.**

---

## 1. Canonical baseline

`scripts/verify_canonical_baseline.py` was run before any change and again after all work.

| Run | Documents | Tree digest | Result |
| --- | --- | --- | --- |
| Before | 214 / 214 | `6c49a13c0f3715ac54f44cb206a18096d596c80ad5ea47891dbeebd9bdef0470` | PASS |
| After | 214 / 214 | `6c49a13c0f3715ac54f44cb206a18096d596c80ad5ea47891dbeebd9bdef0470` | PASS |

Identical. The canonical corpus was not touched.

## 2. LibreOffice

Absent at the start of the task; installed via the Homebrew cask route
(`brew install --cask libreoffice`, exit 0). No unsafe installation method was used and no
system security setting was changed.

| Item | Value |
| --- | --- |
| Status | **AVAILABLE** |
| Version | `LibreOffice 26.2.5.2 cd7284b4cbbfeb507e630c1aac019f4157393acb` |
| Binary | `/Applications/LibreOffice.app/Contents/MacOS/soffice` |
| Backend | `libreoffice` |

Detection reuses the two pre-existing locators
(`tunnelbookai/ingest/office_renderer.py::find_libreoffice` for the ingest engine,
`scripts/utils.py::find_libreoffice` for the legacy pipeline). No duplicate locator was added.

## 3. Office rendering

Validated against the synthetic fixtures in `tests/ingest/fixtures/` only. Full evidence,
including per-snapshot SHA256 digests, is in
[`reports/libreoffice_renderer_validation.md`](libreoffice_renderer_validation.md).

| Format | Pipeline | Snapshots | Valid PNG | SHA256 recorded | Warnings | Result |
| --- | --- | --- | --- | --- | --- | --- |
| DOCX | DOCX → LO → temp PDF → page snapshots | 1 | yes | yes | none | **PASS** |
| PPTX | PPTX → LO → temp PDF → slide snapshots | 2 | yes | yes | none | **PASS** |
| XLSX | XLSX → LO → temp PDF → sheet snapshots | 2 | yes | yes | none | **PASS** |

The temporary PDF lives only inside a `TemporaryDirectory`; no PDF and no LibreOffice profile
survives in a document bundle. Fixture source digests are unchanged before and after rendering.

### Structural authority preserved

| Format | `structural_authority` | Snapshot role |
| --- | --- | --- |
| DOCX | `original_docx` (Docling) | `VISUAL_PROVENANCE` |
| PPTX | `original_pptx` (native + Docling) | `VISUAL_PROVENANCE` |
| XLSX | `openpyxl_workbook_model` | `VISUAL_PROVENANCE` |

The rendered PDF contributes images only — never text, tables, elements or headings.

### Quality gate

With the renderer present, an otherwise valid DOCX/PPTX/XLSX no longer receives the
`VISUAL_RENDERER_UNAVAILABLE` review reason. No quality threshold was changed; the gate code
itself is untouched. Both directions are now pinned by tests
(`test_missing_office_renderer_is_review_never_reject` and the new
`test_present_office_renderer_clears_the_review_reason`).

## 4. Tests

### New ingest / chunk engine

```
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests/ingest -p 'test_*.py'
Ran 197 tests — OK
```

**197 / 197 PASS**, up from the 161 baseline. Nothing skipped: the LibreOffice-guarded tests
all executed against the real binary.

| Addition | Tests |
| --- | --- |
| `tests/ingest/test_office_renderer.py` | 21 |
| `tests/ingest/test_turkish_normalization.py` | 14 |
| `tests/ingest/test_pipeline.py` (gate, renderer present) | 1 |
| Previous baseline | 161 |

### Relevant legacy suites

Run with `PYTHONPATH=.:scripts:crawler/src:tests`.

| Suite | Tests | Result |
| --- | --- | --- |
| `test_migration_integrity` | 16 | OK |
| `test_inventory` | 5 | OK |
| `test_duplicates` | 5 | OK |
| `test_metadata` | 5 | OK |
| `test_metadata_adjudication` | 17 | OK |
| `test_metadata_enrichment` | 16 | OK |
| `test_metadata_verification` | 18 | OK |
| `test_text_normalization` | 27 | OK |
| `test_final_corpus` | 5 | OK |
| `test_recovery` (conversion / RTF modernization) | 4 | OK |
| `test_snapshot` | 3 | OK |
| `test_semantic_chunking` | 67 | OK |
| `test_audit_cache` | 8 | OK |
| `test_dev_regression` | 21 | OK |
| `test_embedding_eligibility` | 44 | OK |
| `test_project_quality_gate` | 2 | OK |
| **Total** | **263** | **263 / 263 PASS** |

This is the set relevant to ingest, conversion and corpus integrity. The remaining ~88 legacy
suites (book writing, generation, retrieval, prewriting audits) were **not** run — they are
unrelated to this task and are not claimed to pass.

## 5. Root `.venv` integrity rule — RESOLVED

`tests/test_migration_integrity.py::test_no_nested_git_or_virtual_environment` rejected any
directory named `.venv` or `venv` anywhere under the project root. That predates the project
standardising on a root-level Python 3.12 virtual environment, so it failed against an
intentional, gitignored, actively used `.venv`.

The `.venv` was **not** moved. The rule was narrowed instead, keeping the original intention
intact. It is now a pure function, `virtual_environment_violations`, with these semantics:

```
Tracked/migrated virtual environments are forbidden.

A root-level .venv is allowed ONLY if:
  - path == project_root/.venv
  - it is covered by .gitignore
  - it appears in no manifest, hash list or corpus inventory
```

Nested `.git` detection is unchanged, and is now its own test.

Five scenario tests pin the boundary:

| Scenario | Expected | Result |
| --- | --- | --- |
| root `.venv`, gitignored | PASS | PASS |
| root `.venv`, not gitignored | FAIL | fails as `root_virtualenv_not_gitignored` |
| nested venv in migrated source (`crawler/src/.venv`) | FAIL | fails as `non_root_or_nested_virtualenv` |
| tracked virtualenv artifact in the manifest | FAIL | fails as `virtualenv_artifact_is_tracked_or_migrated` |
| legacy `venv/` at root | FAIL | fails as `non_root_or_nested_virtualenv` |

Three tests assert the same rule against the real repository: only `ROOT/.venv` exists, it is
gitignored, and no manifest entry, hash entry or corpus path mentions a virtual environment.

Because the project is currently unversioned (no `.git` directory), the gitignore check uses
`git check-ignore` when a repository is present and parses `.gitignore` directly otherwise.

**Result: PASS.**

## 6. Text normalization legacy failures — RESOLVED

Both failures were audited before any change. Neither was a behaviour regression.

### `test_dry_run_and_pilot_artifacts` — category B (missing historical artifacts)

Required `reports/text_normalization_dry_run.md` and `reports/text_normalization_pilot_audit.md`.
Neither exists in this repository — they were migration-era progress reports that were never
carried into V1. The test asserted the presence of a document, not a property of the corpus.

No report was fabricated. The test was rewritten as
`test_stratified_pilot_output_agrees_with_the_full_run`, which asserts the invariant those
reports stood in for, directly against the files: `data/corpus_normalized_pilot/` holds exactly
15 documents, each is **byte-identical** to its counterpart in the full
`data/corpus_normalized/` run, and each has a non-failed manifest row. Verified: 15/15
byte-identical, 0 divergent, 0 missing.

### `test_review_queue_has_no_p0_and_final_audit_has_no_corruption` — category C (stale assumption)

The queue half passed. The corruption half grepped `reports/text_normalization_audit.md` for
lines like `- numeric mismatch: **0**`. The audit generator in
`scripts/10_text_normalization.py` no longer emits per-corruption-class counters, so the
assertion tested the report's wording rather than the corpus.

Rewritten as `test_review_queue_has_no_p0_and_no_document_is_corrupted`, reading the reasons
`audit_safety` actually writes into `data/metadata/text_normalization_manifest.csv`. Across all
214 rows, zero carry any of `front_matter_changed`,
`citation_or_provenance_comment_changed`, `numeric_token_mismatch`,
`url_doi_isbn_standard_token_mismatch`, `markdown_table_changed` or `engineering_symbol_changed`,
and zero have status `manual_review_required` or `failed`. The only reasons present are the two
benign ones — `repeated_header_footer_candidate_not_removed` (14) and
`replacement_character_marked_unresolved` (16). The audit report is still required to exist and
to record the `GO` decision.

This is strictly stronger than the string match it replaces. Normalization code was not changed.

**Result: RESOLVED — no real normalization regression. 27 / 27 PASS.**

## 7. Turkish normalization — a real bug was found and fixed

The previously fixed dotless-ı bug in `dedup.normalize_title` is intact and now guarded.
Auditing the same class of defect across the other matching surfaces found a second, live
instance in the classification path.

**`tunnelbookai/ingest/classify/rules.py::normalize` had no Turkish fold.** NFKD does not
decompose the dotless ı (U+0131), and `"I".casefold()` is `"i"` while `"ı"` stays `"ı"`. So an
ALL-CAPS Turkish heading never matched its own lowercase taxonomy term:

```
term    'tünellerin sınıflandırılması'  → 'tunellerin sınıflandırılması'
HEADING 'TÜNELLERİN SINIFLANDIRILMASI'  → 'tunellerin siniflandirilmasi'
match: False
```

Turkish headings and titles are very frequently ALL CAPS in this corpus, and the taxonomy
carries many Turkish terms, so this silently suppressed rule-based section scoring for exactly
the documents the pilot targets.

Fixed by folding before NFKD, using the **same single table** as `normalize_title`, now living
in the new `tunnelbookai/ingest/textfold.py` so the two normalizers cannot drift apart again.
All ten uppercase/lowercase probe pairs are now symmetric in both normalizers, and
`normalize_title("  Tünel   Bakımı!  ") == "tunel bakimi"` is unchanged.

`tests/ingest/test_turkish_normalization.py` — 14 tests covering `ı İ i I ş Ş ğ Ğ ü Ü ö Ö ç Ç`
across title normalization, dedup matching and classification matching. Verified effective:
reverting the classify fix produces 32 failures, reverting the dedup fold produces 17.

**Result: PASS.**

## 8. Security fix (§17)

A latent defect in the LibreOffice invocation was found and fixed: the isolated-profile
argument was built as `file://{raw path}`, so an output directory containing a space,
parenthesis or Turkish character produced a malformed URL and aborted LibreOffice with an
uncaught `com::sun::star::uno::RuntimeException`. Now built with `Path.as_uri()`, with source
and output directory both resolved to absolute paths.

The invocation already used an argument array, no shell, an isolated temporary profile, an
enforced timeout, captured stderr, and never wrote to the original. All are now asserted by
tests, alongside a hostile-path matrix (spaces, parentheses, Turkish characters, in both file
and directory names).

## 9. Chart extraction

Unchanged. `config/ingest.yaml` keeps `charts.enabled: false` with its documented reason —
Docling 2.124.0's `do_chart_extraction` fabricated a complete "Bar chart" series table from a
plain colour-gradient image during the probe. Deterministic PPTX/XLSX native chart metadata,
read from the original package, remains enabled.

## 10. Known non-blocking issues

1. **`XLSX_CSV_SKIPPED_UNRESOLVED_FORMULAS`** — `sample.xlsx` has a formula sheet with no
   cached values, so the CSV projection is skipped. Pre-existing, documented, correct
   behaviour (the structured JSON keeps the formula with a null value). Not a rejection.
2. **`tests/test_project_quality_gate.py` rewrites `audit/corpus_quality_gate.json` as a side
   effect of running.** Pre-existing. Verified deterministic: the digest is identical before
   and after, only the mtime changes.
3. **XLSX visual snapshots do not cover hidden sheets** — LibreOffice does not render them to
   PDF. Correct: the structured `openpyxl` model is the authority and does include hidden
   sheets. Visual provenance is best-effort by design.
4. **~88 unrelated legacy suites were not run** (book writing, generation, retrieval,
   prewriting audits). Outside this task's scope; their status is unchanged and unclaimed.
5. **The repository is not under version control** (no `.git`). The gitignore-coverage check
   therefore parses `.gitignore` textually. It will switch to `git check-ignore` automatically
   once the project is initialised.

## 11. Readiness

| Criterion | Status |
| --- | --- |
| Canonical corpus unchanged | PASS |
| 161+ ingest/chunk tests pass | PASS (197 / 197) |
| LibreOffice available | PASS (26.2.5.2) |
| DOCX snapshots work | PASS |
| PPTX snapshots work | PASS |
| XLSX snapshots work | PASS |
| Root `.venv` conflict resolved safely | PASS |
| No relevant new regression | PASS (263 / 263 legacy) |

The condition that produced the previous `CONDITIONAL_GO` — LibreOffice unavailable — is
cleared. Two real defects were found and fixed along the way (the LibreOffice profile URL, and
the Turkish fold in classification matching), both now covered by tests.

**Ready for the 6-document real-data pilot: YES.**

Canonical promotion: NOT EXECUTED.
Embedding / Qdrant: NOT EXECUTED.
