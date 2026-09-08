# Docling API Probe (runtime, task §10 / §78)

- **Probed:** 2026-09-02 on `.venv` (CPython 3.12.13, macOS ARM)
- `docling` **2.124.0**, `docling-core` **2.93.0**, `torch` **2.14.0**, `rapidocr` present

## Conversion entrypoint

```python
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions

opts = PdfPipelineOptions()
opts.images_scale = 2.0                 # default 1.0
opts.generate_page_images = True        # default False  → page snapshots
opts.generate_picture_images = True     # default False  → figure extraction
opts.generate_table_images = True       # default False  → table PNGs
opts.do_table_structure = True          # default True
opts.do_ocr = True                      # default True
opts.enable_remote_services = False     # default False  (§27 — keep)
opts.allow_external_plugins = False     # default False  (keep)
# optional / feature-flagged:
opts.do_picture_classification = True   # figure type (photo/diagram/chart/…)
opts.do_chart_extraction = True         # chart2csv=True by default → charts/*.csv  (§16)
opts.do_formula_enrichment = True       # formulas → content_capabilities.formulas
opts.ocr_options = RapidOcrOptions(lang=["english"])   # RapidOCR backend

conv = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)})
result = conv.convert(path)             # -> ConversionResult (pydantic)
doc = result.document                   # -> DoclingDocument
```

- `InputFormat` covers everything we need natively: `PDF, DOCX, DOC, PPTX, PPT, XLSX, XLS,
  IMAGE, HTML, MD, CSV` (plus ODT/ODS/ODP, EPUB, …). **Docling can take `.doc/.ppt/.xls`
  directly** — but keep the LibreOffice legacy path as fallback since Docling's legacy backends
  are less reliable.
- `ConversionResult` is a pydantic model: `.status`, `.errors`, `.has_errors()`,
  `.has_parse_errors()`, `.has_timeout_errors()`, `.document`, `.pages`.

## DoclingDocument outputs (§11)

| Need | Call |
|---|---|
| `document.md` | `doc.export_to_markdown()` / `doc.save_as_markdown(path)` |
| `document.json` (lossless) | `doc.export_to_dict()` / `doc.save_as_json(path)` |
| `document.txt` | `doc.export_to_text()` |
| element tree | `doc.export_to_element_tree()` |
| iterate elements | `doc.iterate_items()` → `(item, level)`; also `doc.tables`, `doc.pictures`, `doc.texts`, `doc.pages` |

## Assets

| Asset | Call | Notes |
|---|---|---|
| page image | `doc.pages[page_no].image.pil_image` | requires `generate_page_images=True`; `.image.uri` when embedded |
| figure image | `PictureItem.get_image(doc)` → `PIL.Image` | requires `generate_picture_images=True`; `.prov[0].bbox`, `.prov[0].page_no` |
| figure caption | `PictureItem.caption_text(doc)` | may be empty → leave `caption: null` |
| table → dataframe | `TableItem.export_to_dataframe()` → `pandas.DataFrame` → `.to_csv()` / `.to_json()` | `TABLExxxx.{csv,json}` |
| table image | `TableItem.get_image(doc)` | requires `generate_table_images=True` |
| table HTML/OTSL | `TableItem.export_to_html(doc)` / `export_to_otsl(doc)` | keep OTSL in `TABLExxxx.json` for merged-cell fidelity |
| table bbox / page | `TableItem.prov[0].bbox`, `.prov[0].page_no` | element-level provenance (§38) |

## Vision / picture description (§28)

`do_picture_description=True` + `picture_description_options`. Local options exist
(`smolvlm_picture_description`, `granite_picture_description`) and `PictureDescriptionApiOptions`
for a **loopback** OpenAI-compatible VLM. `enable_remote_services` gates all of it — our
`VisionProvider` keeps it `False` and only flips on for `127.0.0.1` endpoints.
When no VLM is available → `visual_description_status = NOT_RUN` (never fabricate).

## Chart extraction (§16)

`do_chart_extraction=True`, `chart_extraction_options.chart2csv=True` (default). Model
`granite-vision-v4` — large download, VLM-backed. Treat as **`FAILED_NONBLOCKING`** on any error;
`NOT_SUPPORTED` if the option/model is missing in a future version.

## Version-safety adapter rules

- `tunnelbookai/ingest/docling_adapter.py` sets options via `setattr` guarded by
  `hasattr(opts, name)` — unknown flags degrade to `NOT_RUN`/`NOT_SUPPORTED`, never crash.
- Record `docling.__version__` + `docling-core` version + the resolved option dict into every
  `processing/<id>/extraction_report.json`.
- OCR backend: prefer `RapidOcrOptions` (matches the existing `03_convert.py` RapidOCR-Torch
  path); `OcrMacOptions` is available on macOS as a zero-download fallback; `EasyOcrOptions`
  and `TesseractOcrOptions` also present.
