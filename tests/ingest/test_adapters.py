"""Per-format adapter tests (task §70-§75).

Every fixture is synthetic (`tests/ingest/fixtures/make_fixtures.py`); nothing here touches
the production corpus. Docling runs for real — these are integration tests, not mocks — so
the suite needs the project venv and the cached Docling models.

Run:  PYTHONPATH=. .venv/bin/python -m unittest tests.ingest.test_adapters -v
"""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tunnelbookai.ingest.adapters import AdapterContext, get_adapter
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.format_registry import detect
from tunnelbookai.ingest.ocr.provider import OcrProvider
from tunnelbookai.ingest.office_renderer import OfficeRenderer
from tunnelbookai.ingest.paths import PROJECT_ROOT
from tunnelbookai.ingest.vision.provider import DisabledVisionProvider

FIX = Path(__file__).resolve().parent / "fixtures"


class AdapterHarness(unittest.TestCase):
    """Runs one adapter against one fixture inside a throwaway bundle."""

    @classmethod
    def setUpClass(cls):
        cls.config = load_config()
        cls.ocr = OcrProvider(cls.config)
        cls.vision = DisabledVisionProvider()
        cls.renderer = OfficeRenderer()
        cls.tmp = Path(tempfile.mkdtemp(prefix="tbai_adapter_tests_"))
        cls._cache: dict[str, tuple] = {}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def run_adapter(self, filename: str, *, do_ocr: bool = True):
        """Cached so an expensive Docling conversion runs once per fixture per class."""
        key = f"{filename}:{do_ocr}"
        if key in self._cache:
            return self._cache[key]
        source = FIX / filename
        detection = detect(source)
        bundle = self.tmp / key.replace(".", "_").replace(":", "_")
        bundle.mkdir(parents=True, exist_ok=True)
        context = AdapterContext(
            document_id="ING_" + filename.replace(".", "")[:20],
            original_path=source, original_filename=filename, bundle=bundle,
            detection=detection, config=self.config, ocr=self.ocr, vision=self.vision,
            office_renderer=self.renderer, root=PROJECT_ROOT, do_ocr=do_ocr, do_vision=False,
        )
        result = get_adapter(detection.adapter)(context)
        self._cache[key] = (result, bundle)
        return result, bundle

    def assertNormalizedOutputs(self, result, bundle):
        """document.{md,json,txt} must all exist, with document.json as the authority (§5)."""
        for name in ("document.md", "document.json", "document.txt"):
            self.assertTrue((bundle / "normalized" / name).is_file(), f"missing {name}")
        self.assertTrue(result.normalized_json_path.endswith("normalized/document.json"))
        payload = json.loads((bundle / "normalized" / "document.json").read_text(encoding="utf-8"))
        self.assertIn("elements", payload)
        self.assertEqual(payload["document_id"], result.document_id)
        return payload


class PdfAdapterTests(AdapterHarness):
    """§71 — normalized outputs, snapshot count, tables, figures, page provenance."""

    def test_text_layer_pdf_full_extraction(self):
        result, bundle = self.run_adapter("sample_rich.pdf")
        self.assertTrue(result.succeeded, result.errors)
        payload = self.assertNormalizedOutputs(result, bundle)

        # page snapshots: one PNG per page, recorded as visual provenance
        self.assertEqual(result.page_count, 2)
        self.assertEqual(len(result.pages), 2)
        for snapshot in result.pages:
            self.assertTrue((PROJECT_ROOT / snapshot["path"]).is_file())
            self.assertEqual(snapshot["role"], "VISUAL_PROVENANCE")
            self.assertEqual(len(snapshot["sha256"]), 64)
            self.assertGreater(snapshot["width"], 0)
        self.assertEqual([s["asset_id"] for s in result.pages], ["PAGE0001", "PAGE0002"])

        # tables: structured JSON is authoritative, CSV emitted for a rectangular table
        self.assertGreaterEqual(len(result.tables), 1)
        table = result.tables[0]
        self.assertEqual(table["table_id"], "TABLE0001")
        self.assertTrue((PROJECT_ROOT / table["structured_path"]).is_file())
        self.assertTrue(table["rectangular"])
        self.assertTrue((PROJECT_ROOT / table["csv_path"]).is_file())
        grid = json.loads((PROJECT_ROOT / table["structured_path"]).read_text())["grid"]
        flat = " ".join(" ".join(str(c) for c in row) for row in grid)
        self.assertIn("Kalem", flat)
        self.assertIn("Toplam", flat)

        # figures with page provenance
        self.assertGreaterEqual(len(result.figures), 1)
        figure = result.figures[0]
        self.assertEqual(figure["asset_id"], "FIG0001")
        self.assertTrue((PROJECT_ROOT / figure["path"]).is_file())
        self.assertIsNotNone(figure["page"])

        # page provenance on the element stream
        pages_with_elements = [p for p in payload["pages"] if p["element_ids"]]
        self.assertTrue(pages_with_elements, "no element carried page provenance")
        self.assertTrue(any(e.get("page_start") for e in payload["elements"]))

        self.assertTrue(result.capabilities["text"])
        self.assertTrue(result.capabilities["tables"])
        self.assertTrue(result.capabilities["page_snapshots"])

    def test_image_only_pdf_is_recovered_by_ocr_and_labelled_as_such(self):
        """sample.pdf has no text layer at all. Whichever OCR path recovers it — Docling's
        in-pipeline OCR or our pdfium+RapidOCR page fallback — the result must be text plus
        an honest record that OCR, not the file, produced it (§42)."""
        from tunnelbookai.ingest import evidence as evidence_module

        result, _ = self.run_adapter("sample.pdf")
        self.assertTrue(result.succeeded, result.errors)
        self.assertEqual(result.engine["native_text_layer_chars"], 0)
        self.assertIn(result.engine["native_text_layer"], {"ABSENT_OCR_RECOVERED", "THIN"})

        text = (PROJECT_ROOT / result.normalized_text_path).read_text(encoding="utf-8")
        self.assertIn("Tunel", text)
        self.assertTrue(result.capabilities["ocr"])

        recovered_by_fallback = "NATIVE_TEXT_LAYER_THIN_OCR_FALLBACK" in result.warnings
        recovered_by_docling = "NATIVE_TEXT_LAYER_THIN_DOCLING_OCR_RECOVERED" in result.warnings
        self.assertTrue(recovered_by_fallback or recovered_by_docling, result.warnings)
        if recovered_by_fallback:
            self.assertEqual(len(result.ocr_items), 2)
            self.assertTrue(any(i["ocr_status"] == "SUCCESS" for i in result.ocr_items))

        # a scan must never be graded FULL_TEXT
        level, _reasons = evidence_module.determine(result)
        self.assertEqual(level, evidence_module.IMAGE_OCR)

    def test_ocr_disabled_is_reported_not_silent(self):
        result, _ = self.run_adapter("sample.pdf", do_ocr=False)
        self.assertIn("NATIVE_TEXT_LAYER_THIN_OCR_DISABLED", result.warnings)
        self.assertEqual(result.ocr_items, [])

    def test_invalid_pdf_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            broken = Path(d) / "broken.pdf"
            broken.write_bytes(b"not a pdf at all")
            from tunnelbookai.ingest.adapters.pdf import validate_pdf
            self.assertIn("PDF_BAD_HEADER", validate_pdf(broken))


class DocxAdapterTests(AdapterHarness):
    """§72 — headings, paragraphs, table, embedded image, renderer degradation."""

    def test_structure_comes_from_the_original_docx(self):
        result, bundle = self.run_adapter("sample.docx")
        self.assertTrue(result.succeeded, result.errors)
        payload = self.assertNormalizedOutputs(result, bundle)
        self.assertEqual(payload["structural_authority"], "original_docx")

        headings = [e["text"] for e in result.text_elements if e["type"] == "heading"]
        self.assertIn("NATM Destek Sistemi", headings)
        paragraphs = [e["text"] for e in result.text_elements if e["type"] == "paragraph"]
        self.assertTrue(any("Püskürtme beton" in p for p in paragraphs))

        # heading path is maintained down the tree (§52)
        nested = [e for e in result.text_elements if len(e["heading_path"]) >= 2]
        self.assertTrue(nested, "no element carried a nested heading path")

    def test_table_extracted_to_structured_files(self):
        result, _ = self.run_adapter("sample.docx")
        self.assertEqual(len(result.tables), 1)
        table = result.tables[0]
        self.assertEqual((table["rows"], table["columns"]), (2, 2))
        grid = json.loads((PROJECT_ROOT / table["structured_path"]).read_text())["grid"]
        self.assertEqual(grid[0][0], "Eleman")

    def test_embedded_image_extracted_once_and_ocred(self):
        result, _ = self.run_adapter("sample.docx")
        # exactly one figure: the picture reaches us both as a Docling PictureItem and as an
        # OOXML package member, and pixel-level de-duplication must collapse them (§12).
        self.assertEqual(len(result.figures), 1, [f.get("origin") for f in result.figures])
        figure = result.figures[0]
        self.assertTrue((PROJECT_ROOT / figure["path"]).is_file())
        self.assertIn(figure.get("origin"), {None, "ooxml_media"})
        self.assertEqual(figure["ocr_status"], "SUCCESS")
        self.assertIn("ENKESIT", (figure["ocr_text"] or "").upper())
        # OCR text and visual description stay separate (§24)
        self.assertIsNone(figure["visual_description"])
        self.assertEqual(figure["visual_description_status"], "NOT_RUN")

    def test_missing_renderer_warns_but_never_rejects(self):
        result, _ = self.run_adapter("sample.docx")
        if not self.renderer.available():
            self.assertIn("VISUAL_RENDERER_UNAVAILABLE", result.warnings)
            self.assertTrue(result.succeeded)
            self.assertEqual(result.errors, [])
        else:
            self.assertTrue(result.pages)


class PptxAdapterTests(AdapterHarness):
    """§73 — slide count, titles, body text, image/table extraction, renderer degradation."""

    def test_slides_extracted_in_order(self):
        result, bundle = self.run_adapter("sample.pptx")
        self.assertTrue(result.succeeded, result.errors)
        payload = self.assertNormalizedOutputs(result, bundle)
        self.assertEqual(payload["slide_count"], 2)
        self.assertEqual([s["slide_number"] for s in result.slides], [1, 2])
        self.assertEqual(result.slides[0]["title"], "Ovit Tuneli")
        self.assertIn("Sentetik sunum", result.slides[0]["text"])
        self.assertEqual(result.slides[1]["title"], "Maliyetler")
        self.assertIn("Toplam: 100", result.slides[1]["text"])

    def test_speaker_notes_preserved(self):
        result, _ = self.run_adapter("sample.pptx")
        notes = [s["notes"] for s in result.slides if s["notes"]]
        self.assertTrue(notes)
        self.assertIn("maliyet", notes[0].lower())

    def test_slide_image_extracted(self):
        result, _ = self.run_adapter("sample.pptx")
        self.assertGreaterEqual(len(result.figures), 1)
        figure = result.figures[0]
        self.assertEqual(figure["origin"], "pptx_shape")
        self.assertEqual(figure["slide_number"], 2)
        self.assertIn(figure["asset_id"], result.slides[1]["figures"])

    def test_missing_renderer_is_non_blocking(self):
        result, _ = self.run_adapter("sample.pptx")
        if not self.renderer.available():
            self.assertIn("VISUAL_RENDERER_UNAVAILABLE", result.warnings)
        self.assertTrue(result.succeeded)

    def test_docling_text_fallback_keeps_legacy_ppt_chunkable(self):
        from tunnelbookai.ingest.adapters.pptx import _fallback_text_elements
        from tunnelbookai.ingest.chunking.chunker import (
            ChunkingContext,
            build_text_chunks,
        )
        from tunnelbookai.ingest.chunking.policy import ChunkPolicy

        elements = _fallback_text_elements(
            "# Tünel Yapımı\n\nEski sunumdan çıkarılan okunabilir metin.", ""
        )
        chunks = build_text_chunks(
            elements,
            ChunkingContext(
                document_id="ING_legacy_ppt",
                original_sha256="0" * 64,
                source_kind="MANUAL_INTERNAL",
                final_primary_section="2.4",
                format="PPT",
                evidence_level="FULL_TEXT",
            ),
            ChunkPolicy(),
        )

        self.assertEqual([row["type"] for row in elements], ["heading", "paragraph"])
        self.assertEqual(len(chunks), 1)
        self.assertIn("Eski sunumdan", chunks[0]["text"])

    def test_legacy_ppt_is_converted_before_structural_parse(self):
        source = self.tmp / "legacy.ppt"
        source.write_bytes(b"legacy-placeholder")
        bundle = self.tmp / "legacy_ppt_bundle"
        bundle.mkdir(exist_ok=True)
        renderer = mock.Mock()
        renderer.available.return_value = True

        def convert_to_pptx(_source, out_dir):
            converted = Path(out_dir) / "legacy.pptx"
            shutil.copy(FIX / "sample.pptx", converted)
            return converted, []

        renderer.convert_to_pptx.side_effect = convert_to_pptx
        renderer.render_pages.return_value = ([], [])
        context = AdapterContext(
            document_id="ING_legacyppt",
            original_path=source,
            original_filename="legacy.ppt",
            bundle=bundle,
            detection=SimpleNamespace(fmt=SimpleNamespace(value="PPT")),
            config=self.config,
            office_renderer=renderer,
            root=PROJECT_ROOT,
            do_ocr=False,
            do_vision=False,
        )
        with mock.patch(
            "tunnelbookai.ingest.adapters.pptx.docling_adapter.convert",
        ) as convert:
            result = get_adapter("pptx")(context)

        self.assertTrue(result.succeeded, result.errors)
        self.assertEqual(len(result.slides), 2)
        self.assertTrue(result.engine["legacy_ppt_conversion"])
        self.assertEqual(result.engine["docling_status"], "SKIPPED_LEGACY_NATIVE")
        self.assertEqual(result.engine["native_parser"], "libreoffice+python-pptx")
        self.assertEqual(result.engine["structural_authority"], "libreoffice_converted_pptx")
        self.assertIn("PPT_CONVERTED_TO_PPTX", result.warnings)
        convert.assert_not_called()
        renderer.convert_to_pptx.assert_called_once()


class XlsxAdapterTests(AdapterHarness):
    """§74 — multiple sheets, hidden sheet, formulas, coordinates, sheet JSON + CSV."""

    def test_all_sheets_including_hidden(self):
        result, bundle = self.run_adapter("sample.xlsx")
        self.assertTrue(result.succeeded, result.errors)
        payload = self.assertNormalizedOutputs(result, bundle)
        names = [s["sheet_name"] for s in result.sheets]
        self.assertEqual(names, ["Maliyetler", "Ozet", "Gizli"])
        self.assertEqual(payload["hidden_sheets"], ["Gizli"])
        hidden = next(s for s in result.sheets if s["sheet_name"] == "Gizli")
        self.assertTrue(hidden["hidden"])

    def test_formula_retained_verbatim_and_value_not_faked(self):
        result, _ = self.run_adapter("sample.xlsx")
        sheet = next(s for s in result.sheets if s["sheet_name"] == "Maliyetler")
        self.assertEqual(sheet["formula_count"], 1)
        cells = json.loads((PROJECT_ROOT / sheet["structured_path"]).read_text())["cells"]
        formula_cell = next(c for c in cells if c["formula"])
        self.assertEqual(formula_cell["cell"], "B4")
        self.assertEqual(formula_cell["formula"], "=SUM(B2:B3)")
        # openpyxl wrote no cached value; it must stay null rather than be invented (§16)
        self.assertIsNone(formula_cell["value"])
        self.assertEqual(formula_cell["data_type"], "f")

    def test_cell_coordinates_present(self):
        result, _ = self.run_adapter("sample.xlsx")
        sheet = next(s for s in result.sheets if s["sheet_name"] == "Maliyetler")
        cells = json.loads((PROJECT_ROOT / sheet["structured_path"]).read_text())["cells"]
        by_coord = {c["cell"]: c for c in cells}
        self.assertEqual(by_coord["A1"]["value"], "Kalem")
        self.assertEqual(by_coord["B2"]["value"], 40)
        self.assertEqual(by_coord["A1"]["row"], 1)
        self.assertEqual(by_coord["A1"]["column"], 1)

    def test_csv_only_when_safe(self):
        result, _ = self.run_adapter("sample.xlsx")
        by_name = {s["sheet_name"]: s for s in result.sheets}
        # values-only sheet -> CSV is safe
        self.assertTrue(by_name["Ozet"]["csv_path"])
        self.assertTrue((PROJECT_ROOT / by_name["Ozet"]["csv_path"]).is_file())
        csv_text = (PROJECT_ROOT / by_name["Ozet"]["csv_path"]).read_text(encoding="utf-8")
        self.assertIn("Yil,Tutar", csv_text)
        # sheet with an unresolved formula -> no CSV, and the skip is reported
        self.assertIsNone(by_name["Maliyetler"]["csv_path"])
        self.assertIn("XLSX_CSV_SKIPPED_UNRESOLVED_FORMULAS:Maliyetler", result.warnings)

    def test_merged_cells_and_named_ranges_recorded(self):
        result, bundle = self.run_adapter("sample.xlsx")
        sheet = next(s for s in result.sheets if s["sheet_name"] == "Maliyetler")
        self.assertIn("D2:E2", sheet["merged_cells"])
        payload = json.loads((bundle / "normalized" / "document.json").read_text())
        self.assertIn("named_ranges", payload)
        self.assertEqual(payload["structural_authority"], "openpyxl_workbook_model")

    def test_workbook_not_flattened_to_markdown_only(self):
        result, _ = self.run_adapter("sample.xlsx")
        self.assertTrue(result.capabilities["sheets"])
        for sheet in result.sheets:
            self.assertTrue((PROJECT_ROOT / sheet["structured_path"]).is_file())

    def test_legacy_xls_is_converted_before_openpyxl_reads_it(self):
        source = self.tmp / "legacy.xls"
        source.write_bytes(b"legacy-placeholder")
        bundle = self.tmp / "legacy_xls_bundle"
        bundle.mkdir(exist_ok=True)
        renderer = mock.Mock()
        renderer.available.return_value = True

        def convert_to_xlsx(_source, out_dir):
            converted = Path(out_dir) / "legacy.xlsx"
            shutil.copy(FIX / "sample.xlsx", converted)
            return converted, []

        renderer.convert_to_xlsx.side_effect = convert_to_xlsx
        context = AdapterContext(
            document_id="ING_legacyxls",
            original_path=source,
            original_filename="legacy.xls",
            bundle=bundle,
            detection=SimpleNamespace(fmt=SimpleNamespace(value="XLS")),
            config=self.config,
            office_renderer=renderer,
            root=PROJECT_ROOT,
        )
        result = get_adapter("xlsx")(context)

        self.assertTrue(result.succeeded, result.errors)
        self.assertEqual(result.engine["native_parser"], "libreoffice+openpyxl")
        self.assertTrue(result.engine["legacy_xls_conversion"])
        self.assertIn("XLS_CONVERTED_TO_XLSX", result.warnings)
        self.assertGreater(result.engine["formula_count"], 0)
        renderer.convert_to_xlsx.assert_called_once()


class ImageAdapterTests(AdapterHarness):
    """§75 — a text image must OCR; a photo must not hallucinate text."""

    def test_text_image_produces_expected_ocr(self):
        result, bundle = self.run_adapter("sample_text.png")
        self.assertTrue(result.succeeded, result.errors)
        self.assertNormalizedOutputs(result, bundle)
        text = (PROJECT_ROOT / result.normalized_text_path).read_text(encoding="utf-8").upper()
        self.assertIn("BETON", text)
        self.assertIn("BULONU", text)
        self.assertEqual(result.figures[0]["ocr_status"], "SUCCESS")
        # RapidOCR exposes no calibrated score — it must stay null, never fabricated (§23)
        self.assertIsNone(result.figures[0]["ocr_confidence"])

    def test_photograph_produces_no_hallucinated_text(self):
        result, _ = self.run_adapter("sample_photo.jpg")
        self.assertTrue(result.succeeded, result.errors)
        self.assertIn("OCR_EMPTY_TEXT_IMAGE", result.warnings)
        self.assertIsNone(result.figures[0]["ocr_text"])
        self.assertEqual(result.figures[0]["ocr_status"], "EMPTY")
        self.assertFalse(result.capabilities["text"])
        # and no visual description was invented either (§27)
        self.assertIsNone(result.figures[0]["visual_description"])

    def test_image_metadata_captured(self):
        result, bundle = self.run_adapter("sample_text.png")
        payload = json.loads((bundle / "normalized" / "document.json").read_text())
        self.assertEqual(payload["image"]["width"], 600)
        self.assertEqual(payload["image"]["height"], 200)


class TextAdapterTests(AdapterHarness):
    """§20 / §70 — TXT, MD, CSV, HTML."""

    def test_txt(self):
        result, bundle = self.run_adapter("sample_text.txt")
        self.assertTrue(result.succeeded, result.errors)
        self.assertNormalizedOutputs(result, bundle)
        self.assertIn("Tunel tanimi", (PROJECT_ROOT / result.normalized_text_path).read_text())

    def _adhoc(self, filename: str, content: str):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / filename
            source.write_text(content, encoding="utf-8")
            bundle = self.tmp / f"adhoc_{filename.replace('.', '_')}"
            bundle.mkdir(parents=True, exist_ok=True)
            context = AdapterContext(
                document_id="ING_adhoc", original_path=source, original_filename=filename,
                bundle=bundle, detection=detect(source), config=self.config,
                ocr=self.ocr, vision=self.vision, office_renderer=self.renderer,
                root=PROJECT_ROOT, do_ocr=False, do_vision=False)
            return get_adapter(detect(source).adapter)(context), bundle

    def test_markdown_headings_become_structure(self):
        result, _ = self._adhoc("note.md", "# Tünel\n\nGiriş metni.\n\n## Alt Başlık\n\nDetay.\n")
        headings = [e["text"] for e in result.text_elements if e["type"] == "heading"]
        self.assertEqual(headings, ["Tünel", "Alt Başlık"])
        deep = [e for e in result.text_elements if e["heading_path"] == ["Tünel", "Alt Başlık"]]
        self.assertTrue(deep)

    def test_csv_preserved_as_a_table(self):
        result, _ = self._adhoc("t.csv", "Kalem,Tutar\nKazi,40\nDestek,60\n")
        self.assertEqual(len(result.tables), 1)
        grid = json.loads((PROJECT_ROOT / result.tables[0]["structured_path"]).read_text())["grid"]
        self.assertEqual(grid[0], ["Kalem", "Tutar"])
        self.assertTrue(result.capabilities["tables"])

    def test_html_structure_from_the_original_markup(self):
        result, bundle = self._adhoc("p.html", """
            <html><head><title>Tünel Raporu</title></head><body>
            <h1>Giriş</h1><p>Birinci paragraf.</p>
            <h2>Tablo</h2><table><tr><th>A</th><th>B</th></tr><tr><td>1</td><td>2</td></tr></table>
            <ul><li>madde bir</li></ul>
            <script>ignored()</script></body></html>""")
        headings = [e["text"] for e in result.text_elements if e["type"] == "heading"]
        self.assertIn("Giriş", headings)
        self.assertEqual(len(result.tables), 1)
        self.assertTrue(any(e["type"] == "list_item" for e in result.text_elements))
        body = (PROJECT_ROOT / result.normalized_text_path).read_text()
        self.assertNotIn("ignored()", body)

    def test_encoding_fallback_recorded(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "legacy.txt"
            source.write_bytes("Tünel ölçüm raporu".encode("cp1254"))
            bundle = self.tmp / "adhoc_cp1254"
            bundle.mkdir(parents=True, exist_ok=True)
            context = AdapterContext(
                document_id="ING_cp1254", original_path=source, original_filename="legacy.txt",
                bundle=bundle, detection=detect(source), config=self.config, ocr=self.ocr,
                vision=self.vision, office_renderer=self.renderer, root=PROJECT_ROOT,
                do_ocr=False, do_vision=False)
            result = get_adapter("text")(context)
            payload = json.loads((bundle / "normalized" / "document.json").read_text())
            self.assertEqual(payload["encoding"], "cp1254")
            self.assertIn("Tünel", (PROJECT_ROOT / result.normalized_text_path).read_text())


if __name__ == "__main__":
    unittest.main()
