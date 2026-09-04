# LibreOffice Renderer Validation

Date: 2026-09-03
Scope: task §3–§9, §16, §17. Synthetic fixtures only; no production or user documents were
rendered, no canonical data was touched.

---

## 1. Detection and installation

LibreOffice was **absent** at the start of this task (`/Applications/LibreOffice.app` missing,
`which soffice` and `which libreoffice` both empty). Homebrew was present at
`/opt/homebrew/bin/brew`, so the safe cask route applied:

```bash
NONINTERACTIVE=1 HOMEBREW_NO_AUTO_UPDATE=1 brew install --cask libreoffice
```

Exit code 0. No `curl | sh`, no system security settings changed, no sudo escalation.

| Item | Value |
| --- | --- |
| Binary path | `/Applications/LibreOffice.app/Contents/MacOS/soffice` |
| Version | `LibreOffice 26.2.5.2 cd7284b4cbbfeb507e630c1aac019f4157393acb` |
| Homebrew wrapper | `/opt/homebrew/bin/soffice` (also linked, not used by the locator) |
| Renderer available | **yes** |
| Backend | `libreoffice` |
| Subprocess timeout | 300 s (default) |

### Detection logic — reused, not duplicated

Two locators already existed and both were left in place; no third was added.

* `tunnelbookai/ingest/office_renderer.py::find_libreoffice` — used by the Unified Ingest
  Engine (`OfficeRenderer`, `cli.py`, `format_registry.is_supported`).
* `scripts/utils.py::find_libreoffice` — used by the legacy `scripts/` pipeline and asserted
  by `tests/test_inventory.py`.

Both resolve `/Applications/LibreOffice.app/Contents/MacOS/soffice` first and fall back to
`shutil.which`. Both now find the installed binary.

---

## 2. Rendering pipeline verified

```
DOCX → LibreOffice --headless --convert-to pdf → temporary PDF → PNG page snapshots
PPTX → LibreOffice --headless --convert-to pdf → temporary PDF → PNG slide snapshots
XLSX → LibreOffice --headless --convert-to pdf → temporary PDF → PNG sheet snapshots
```

The intermediate PDF is written into a `tempfile.TemporaryDirectory` and destroyed when the
context exits. It is never written into the document bundle and never becomes an output.

## 3. Visual output validation

All three fixtures render with **zero warnings**.

| Fixture | Renderer success | Temp PDF | Snapshots | All valid PNG | SHA256 recorded | Source unchanged |
| --- | --- | --- | --- | --- | --- | --- |
| `sample.docx` | yes | 22 892 B, `%PDF-` | 1 | yes | yes | yes |
| `sample.pptx` | yes | 23 751 B, `%PDF-` | 2 | yes | yes | yes |
| `sample.xlsx` | yes | 20 091 B, `%PDF-` | 2 | yes | yes | yes |

### Snapshot inventory

| Fixture | Asset id | Type | Size | Dimensions | SHA256 |
| --- | --- | --- | --- | --- | --- |
| `sample.docx` | `PAGE0001` | `PAGE` | 44 380 B | 1224×1584 | `bdc67e9d95527a3d92ad4339197ed813fb1fba7f3a5f3d0c8d8cd3b5afa90101` |
| `sample.pptx` | `SLIDE0001` | `SLIDE` | 26 215 B | 1440×1080 | `57633b775c6fdd9e43bc3ac370e398d0496310a8b98b66979eb7a0f972ea58d6` |
| `sample.pptx` | `SLIDE0002` | `SLIDE` | 23 030 B | 1440×1080 | `2418b8e69e8d708bd53200a0f97885d40c14831e7c3d0a61901b397702fdb5b8` |
| `sample.xlsx` | `SHEETIMG0001` | `SHEET_SNAPSHOT` | 22 370 B | 1191×1684 | `779d17cbf245599f158249697717e86e4ddedf45c0eb4fc9562f48443780584e` |
| `sample.xlsx` | `SHEETIMG0002` | `SHEET_SNAPSHOT` | 16 357 B | 1191×1684 | `bcda42179e37e62b33ebbddc93a479628b3a78b4054b87000cf8a209571e73ce` |

Every record's `sha256` field matches a fresh digest of the bytes on disk. Every file starts
with the PNG magic number. No `*.pdf` is left anywhere in a bundle after rendering.

Fixture source digests are byte-identical before and after rendering — the originals are never
modified:

```
sample.docx  57becb9d556c76914574dc1a9a7f5063dc38e9758e2907b485893e9deb3710f3
sample.pptx  7ddb38890c09de88b33013852c047a100c664aa407a57f3345a03f348a33af9e
sample.xlsx  02d1954711200c69b122e8f41d72e4a59d6643c5f79ab73497eb46a901661570
```

## 4. Provenance — snapshots are derived data only

Every snapshot record carries:

```
renderer      = "libreoffice+pypdfium2"
role          = "VISUAL_PROVENANCE"
derived_from  = "temporary_rendered_pdf"
```

## 5. Structural authority unchanged (§8)

Confirmed by running each fixture through its real adapter and reading
`normalized/document.json`:

| Format | `structural_authority` | Source of structure |
| --- | --- | --- |
| DOCX | `original_docx` | original DOCX + Docling |
| PPTX | `original_pptx` | original PPTX + python-pptx native structure + Docling |
| XLSX | `openpyxl_workbook_model` | original XLSX + openpyxl structured model |

The rendered PDF contributes **no** text, tables, elements or headings. It contributes images
only. Removing the renderer changes the snapshot list and nothing else.

## 6. Quality gate recheck (§9)

`tunnelbookai/ingest/quality_gate.py` raises `VISUAL_RENDERER_UNAVAILABLE` as a **review**
reason (never a rejection) for `DOCX/PPTX/DOC/PPT/RTF` when the extraction warned about a
missing renderer. With LibreOffice installed:

| Fixture | Warnings | `VISUAL_RENDERER_UNAVAILABLE` |
| --- | --- | --- |
| `sample.docx` | none | no |
| `sample.pptx` | none | no |
| `sample.xlsx` | `XLSX_CSV_SKIPPED_UNRESOLVED_FORMULAS:Maliyetler` (pre-existing, unrelated) | no |

No quality threshold was changed. The gate code is untouched; a new test
(`test_present_office_renderer_clears_the_review_reason`) pins the cleared path alongside the
existing test that pins the degraded path.

## 7. Security (§17)

| Requirement | Status | Evidence |
| --- | --- | --- |
| Argument array, never a string | met | `subprocess.run([...])`, asserted by `test_command_is_an_argument_array_and_never_uses_a_shell` |
| No `shell=True` | met | `shell` is never passed; asserted in the same test |
| Isolated temporary user profile | met | `-env:UserInstallation=<file URI>/_lo_profile` inside the temp dir |
| Timeout enforced | met | `timeout=self.timeout_seconds`, `TimeoutExpired` → `OFFICE_RENDER_TIMEOUT` |
| stderr captured | met | `capture_output=True`; last stderr line is folded into `OFFICE_RENDER_NO_OUTPUT` |
| Originals never modified | met | digests above; conversion writes only into `--outdir` |

### Defect found and fixed

The profile argument was built as `f"-env:UserInstallation=file://{profile}"` — a raw,
un-encoded path. When the output directory contained a space, a parenthesis or a Turkish
character the URL was malformed and LibreOffice aborted:

```
out_dir='out (ışık) dir'
  → OFFICE_RENDER_NO_OUTPUT:libc++abi: terminating due to uncaught exception
    of type com::sun::star::uno::RuntimeException
```

Fixed in `tunnelbookai/ingest/office_renderer.py` by using `Path.as_uri()`, which
percent-encodes, and by resolving both the output directory and the source to absolute paths
(which also prevents a leading-dash filename being parsed as an option).

After the fix, every hostile-path case renders cleanly:

| Case | Result |
| --- | --- |
| `ovit tuneli raporu.docx` (spaces) | 1 snapshot, no warnings |
| `rapor (final) v2.docx` (parentheses) | 1 snapshot, no warnings |
| `ışık İSTANBUL şğüöç.docx` (Turkish) | 1 snapshot, no warnings |
| `Tünel Bakımı (2024) ölçüm şeması.docx` (all three) | 1 snapshot, no warnings |
| output dir `out (ışık) dir` | PDF produced, no warnings |
| output dir `İSTANBUL şğüöç (2)` | PDF produced, no warnings |
| source dir `kaynak (arşiv) ışık` | renders, no warnings |

## 8. Tests added

`tests/ingest/test_office_renderer.py` — 21 tests, all passing:

* detection (locator returns a real executable; availability tracks the locator; the detected
  binary reports a version)
* DOCX / PPTX / XLSX snapshot success paths, each validating PNG magic, size, digest and
  provenance fields
* renderer-unavailable degradation, with `find_libreoffice` mocked to `None`: warning returned,
  no exception, and **no subprocess launched**
* renderer-present-but-failing: timeout and no-output both degrade to warnings
* subprocess safety assertions (§17)
* temporary-PDF lifecycle: a real PDF is produced, and no PDF or profile survives in the bundle
* hostile path matrix

The tests that need a real conversion are guarded with `skipUnless(HAVE_LIBREOFFICE)`, so the
suite still passes on a machine without LibreOffice; the degradation tests always run.

## 9. Chart extraction (§14)

Unchanged and still disabled. `config/ingest.yaml` keeps `charts.enabled: false` with the
documented reason (Docling 2.124.0's `do_chart_extraction` fabricated a complete "Bar chart"
series table from a plain colour-gradient image). Deterministic PPTX/XLSX native chart metadata
read from the original package remains enabled.

---

**Renderer availability: PASS.**
