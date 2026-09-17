"""Structure-aware chunking tests (task §79).

Covers: stable ids, heading path, page/slide/sheet provenance, one chunk type per modality,
token thresholds, no empty chunks, no duplicate flood, chunk quality gate, embedding-ready
manifest eligibility.

Run:  PYTHONPATH=. .venv/bin/python -m unittest tests.ingest.test_chunking -v
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tunnelbookai.ingest.chunking import manifest as manifest_module
from tunnelbookai.ingest.chunking import quality as quality_module
from tunnelbookai.ingest.chunking import tokenizer
from tunnelbookai.ingest.chunking.chunker import (
    ChunkingContext, chunk_document, deduplicate, read_chunks, write_chunks,
)
from tunnelbookai.ingest.chunking.policy import (
    FIGURE_CHUNK, OCR_CHUNK, SHEET_CHUNK, SLIDE_CHUNK, TABLE_CHUNK, TEXT_CHUNK,
    ChunkPolicy, chunk_id,
)
from tunnelbookai.ingest.config import load_config

LOREM = ("Tünel bakım maliyetleri, yapım aşamasındaki kararlardan doğrudan etkilenir. "
         "Bu bölümde bakım kalemleri, periyodik muayene döngüleri ve yaşam döngüsü "
         "maliyetlerinin hesaplanması ele alınmaktadır. ")


def varied(sentences: int, offset: int = 0) -> str:
    """Distinct sentences. Repeating ONE sentence would (correctly) be collapsed by the
    intra-document near-duplicate suppression, so size tests need real variety — and blocks
    meant to stay separate need a different `offset`."""
    topics = ["kazı", "destek", "havalandırma", "yalıtım", "drenaj", "kaplama", "izleme",
              "portal", "enjeksiyon", "aydınlatma", "yangın", "trafik", "bakım", "onarım"]
    return " ".join(
        f"{topics[i % len(topics)].capitalize()} kalemi {i} için birim maliyet analizi "
        f"yapılmış ve {i * 7 % 97} numaralı ölçüm kaydı ile karşılaştırılmıştır."
        for i in range(offset, offset + sentences))


def _element(element_id, kind, text, **kwargs):
    base = {"element_id": element_id, "type": kind, "text": text, "level": None,
            "heading_path": [], "page_start": None, "page_end": None, "slide_number": None,
            "sheet_name": None, "cell_range": None, "element_ref": None, "asset_id": None}
    base.update(kwargs)
    return base


def _context():
    return ChunkingContext(
        document_id="ING_test", original_sha256="a" * 64, source_kind="MANUAL_INTERNAL",
        final_primary_section="5.5.2", final_secondary_sections=["5.5"],
        format="PDF", evidence_level="FULL_TEXT")


class PolicyTests(unittest.TestCase):
    def test_policy_loads_from_config(self):
        policy = ChunkPolicy.from_config(load_config())
        self.assertEqual(policy.policy_version, "structure-aware-v2")
        self.assertEqual(policy.schema_version, "1.0")
        self.assertEqual(policy.tokenizer_name, "unicode-lexical-v1")
        self.assertGreater(policy.max_tokens, policy.target_tokens)
        self.assertGreater(policy.hard_max_tokens, policy.max_tokens)
        self.assertGreater(policy.target_tokens, policy.min_tokens)
        for chunk_type in (TEXT_CHUNK, TABLE_CHUNK, FIGURE_CHUNK, OCR_CHUNK,
                           SLIDE_CHUNK, SHEET_CHUNK):
            self.assertTrue(policy.allows(chunk_type))


class StableIdTests(unittest.TestCase):
    """§61 — ids are deterministic, and change when the content changes."""

    def setUp(self):
        self.policy = ChunkPolicy.from_config(load_config())

    def test_same_inputs_same_id(self):
        first = chunk_id("ING_a", TEXT_CHUNK, ["PARA0001"], "metin", self.policy)
        second = chunk_id("ING_a", TEXT_CHUNK, ["PARA0001"], "metin", self.policy)
        self.assertEqual(first, second)
        self.assertTrue(first.startswith("ING_a_CH_"))

    def test_changed_content_changes_the_id(self):
        first = chunk_id("ING_a", TEXT_CHUNK, ["PARA0001"], "metin", self.policy)
        second = chunk_id("ING_a", TEXT_CHUNK, ["PARA0001"], "başka metin", self.policy)
        self.assertNotEqual(first, second)

    def test_changed_boundaries_change_the_id(self):
        first = chunk_id("ING_a", TEXT_CHUNK, ["PARA0001"], "metin", self.policy)
        second = chunk_id("ING_a", TEXT_CHUNK, ["PARA0001", "PARA0002"], "metin", self.policy)
        self.assertNotEqual(first, second)

    def test_policy_version_participates(self):
        other = ChunkPolicy.from_config(load_config())
        other = ChunkPolicy(**{**other.__dict__, "policy_version": "structure-aware-test-other"})
        self.assertNotEqual(chunk_id("ING_a", TEXT_CHUNK, ["P"], "m", self.policy),
                            chunk_id("ING_a", TEXT_CHUNK, ["P"], "m", other))

    def test_whitespace_only_change_keeps_the_id(self):
        self.assertEqual(chunk_id("ING_a", TEXT_CHUNK, ["P"], "bir  iki", self.policy),
                         chunk_id("ING_a", TEXT_CHUNK, ["P"], " bir iki ", self.policy))

    def test_full_run_is_reproducible(self):
        elements = [_element("HEAD0001", "heading", "Bölüm", heading_path=["Bölüm"], level=1),
                    _element("PARA0001", "paragraph", LOREM * 8, heading_path=["Bölüm"])]
        first, _ = chunk_document(context=_context(), elements=elements, tables=[], figures=[],
                                  slides=[], sheets=[], ocr_items=[], policy=self.policy,
                                  root=Path("."))
        second, _ = chunk_document(context=_context(), elements=elements, tables=[], figures=[],
                                   slides=[], sheets=[], ocr_items=[], policy=self.policy,
                                   root=Path("."))
        self.assertEqual([c["chunk_id"] for c in first], [c["chunk_id"] for c in second])


class TextChunkTests(unittest.TestCase):
    """§51, §52, §53 — structure boundaries, heading path, page provenance."""

    def setUp(self):
        self.policy = ChunkPolicy.from_config(load_config())

    def _run(self, elements):
        return chunk_document(context=_context(), elements=elements, tables=[], figures=[],
                              slides=[], sheets=[], ocr_items=[], policy=self.policy,
                              root=Path("."))[0]

    def test_heading_path_preserved(self):
        elements = [
            _element("HEAD0001", "heading", "4. MALİYET KAVRAMI", level=1,
                     heading_path=["4. MALİYET KAVRAMI"], page_start=17),
            _element("HEAD0002", "heading", "4.1 Maliyet Tanımları", level=2,
                     heading_path=["4. MALİYET KAVRAMI", "4.1 Maliyet Tanımları"],
                     page_start=17),
            _element("PARA0001", "paragraph", varied(30), page_start=17, page_end=18,
                     heading_path=["4. MALİYET KAVRAMI", "4.1 Maliyet Tanımları"]),
        ]
        chunks = self._run(elements)
        self.assertTrue(chunks)
        self.assertEqual(chunks[0]["heading_path"],
                         ["4. MALİYET KAVRAMI", "4.1 Maliyet Tanımları"])

    def test_page_provenance_preserved(self):
        elements = [_element("PARA0001", "paragraph", varied(30), page_start=17, page_end=18)]
        chunk = self._run(elements)[0]
        self.assertEqual(chunk["page_start"], 17)
        self.assertEqual(chunk["page_end"], 18)

    def test_splits_on_headings_not_blindly(self):
        elements = []
        for index in range(1, 4):
            elements.append(_element(f"HEAD{index:04d}", "heading", f"Bölüm {index}", level=1,
                                     heading_path=[f"Bölüm {index}"], page_start=index))
            elements.append(_element(f"PARA{index:04d}", "paragraph",
                                     varied(40, offset=index * 500),
                                     heading_path=[f"Bölüm {index}"], page_start=index))
        chunks = self._run(elements)
        self.assertGreaterEqual(len(chunks), 3)
        # every chunk sits under exactly one heading
        for chunk in chunks:
            self.assertEqual(len(chunk["heading_path"]), 1)
        self.assertEqual({tuple(c["heading_path"]) for c in chunks},
                         {("Bölüm 1",), ("Bölüm 2",), ("Bölüm 3",)})

    def test_token_thresholds_respected(self):
        elements = [_element("PARA0001", "paragraph", varied(900))]
        chunks = self._run(elements)
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertLessEqual(chunk["token_count"], self.policy.max_tokens)
            self.assertEqual(chunk["token_count"], tokenizer.count(chunk["text"]))

    def test_dense_punctuation_is_split_with_forward_progress(self):
        text = "!" * (self.policy.hard_max_tokens * 3)
        chunks = self._run([_element("PARA0001", "paragraph", text)])
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(chunk["text"] for chunk in chunks))
        self.assertTrue(
            all(chunk["token_count"] <= self.policy.max_tokens for chunk in chunks)
        )
        self.assertEqual("".join(chunk["text"] for chunk in chunks), text)

    def test_overlap_never_pushes_chunk_over_hard_limit(self):
        first = varied(80)
        # This block is intentionally below the hard limit but above the normal
        # target, so it is returned intact by the last-resort splitter.
        second = "!" * (self.policy.hard_max_tokens - 10)
        elements = [
            _element("PARA0001", "paragraph", first),
            _element("PARA0002", "paragraph", second),
        ]
        chunks = self._run(elements)
        self.assertTrue(all(
            chunk["token_count"] <= self.policy.max_tokens for chunk in chunks
        ))

    def test_no_empty_chunks(self):
        elements = [_element("PARA0001", "paragraph", "   "),
                    _element("PARA0002", "paragraph", ""),
                    _element("PARA0003", "paragraph", LOREM * 6)]
        for chunk in self._run(elements):
            self.assertTrue(chunk["text"].strip())
            self.assertGreater(chunk["token_count"], 0)

    def test_source_elements_recorded(self):
        elements = [_element("PARA0001", "paragraph", LOREM * 4),
                    _element("PARA0002", "paragraph", LOREM * 4)]
        chunk = self._run(elements)[0]
        self.assertEqual(chunk["source_elements"], ["PARA0001", "PARA0002"])

    def test_provenance_and_versions_on_every_chunk(self):
        chunks = self._run([_element("PARA0001", "paragraph", LOREM * 10)])
        for chunk in chunks:
            self.assertEqual(chunk["provenance"]["original_sha256"], "a" * 64)
            self.assertEqual(chunk["provenance"]["source_kind"], "MANUAL_INTERNAL")
            self.assertEqual(chunk["chunk_schema_version"], self.policy.schema_version)
            self.assertEqual(chunk["chunk_policy_version"], self.policy.policy_version)
            self.assertEqual(chunk["final_primary_section"], "5.5.2")
            self.assertEqual(chunk["final_secondary_sections"], ["5.5"])


class ModalityChunkTests(unittest.TestCase):
    """§50, §55, §56, §58, §59 — one first-class chunk type per modality."""

    def setUp(self):
        self.policy = ChunkPolicy.from_config(load_config())
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _table(self):
        path = self.root / "tables" / "TABLE0003.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "table_id": "TABLE0003",
            "grid": [["Kalem", "Tutar"], ["Kazı", "40"], ["Destek", "60"]],
        }), encoding="utf-8")
        return {"table_id": "TABLE0003", "asset_id": "TABLE0003", "caption": "Tablo 3. Maliyet",
                "structured_path": "tables/TABLE0003.json", "csv_path": "tables/TABLE0003.csv",
                "image_path": None, "page": 21, "rows": 3, "columns": 2}

    def test_table_becomes_a_table_chunk(self):
        elements = [_element("TREF0001", "table_ref", "Tablo 3. Maliyet",
                             asset_id="TABLE0003", page_start=21, heading_path=["Maliyet"])]
        chunks, _ = chunk_document(context=_context(), elements=elements, tables=[self._table()],
                                   figures=[], slides=[], sheets=[], ocr_items=[],
                                   policy=self.policy, root=self.root)
        table_chunks = [c for c in chunks if c["chunk_type"] == TABLE_CHUNK]
        self.assertEqual(len(table_chunks), 1)
        chunk = table_chunks[0]
        self.assertEqual(chunk["table_id"], "TABLE0003")
        self.assertEqual(chunk["page"], 21)
        self.assertEqual(chunk["structured_path"], "tables/TABLE0003.json")
        # a textual rendering exists for retrieval, but the structured file stays authority
        self.assertIn("Kalem", chunk["text"])
        self.assertIn("Kazı", chunk["text"])
        self.assertEqual(chunk["source_elements"], ["TREF0001"])
        self.assertEqual(chunk["heading_path"], ["Maliyet"])

    def test_oversized_table_is_split_below_hard_limit(self):
        path = self.root / "tables" / "TABLE_BIG.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        grid = [["Kalem", "Açıklama"]] + [
            [f"Satır {index}", varied(8, offset=index * 8)] for index in range(60)
        ]
        path.write_text(json.dumps({"table_id": "TABLE_BIG", "grid": grid}), encoding="utf-8")
        table = {
            "table_id": "TABLE_BIG", "asset_id": "TABLE_BIG", "caption": "Büyük tablo",
            "structured_path": "tables/TABLE_BIG.json", "page": 4,
            "rows": len(grid), "columns": 2,
        }
        elements = [_element(
            "TREF_BIG", "table_ref", "Büyük tablo", asset_id="TABLE_BIG",
            page_start=4, heading_path=["Ek"],
        )]
        chunks, _ = chunk_document(
            context=_context(), elements=elements, tables=[table], figures=[], slides=[],
            sheets=[], ocr_items=[], policy=self.policy, root=self.root,
        )
        table_chunks = [chunk for chunk in chunks if chunk["chunk_type"] == TABLE_CHUNK]
        self.assertGreater(len(table_chunks), 1)
        self.assertTrue(all(chunk["token_count"] <= self.policy.max_tokens for chunk in table_chunks))
        self.assertEqual([chunk["table_part"] for chunk in table_chunks], list(range(1, len(table_chunks) + 1)))
        self.assertTrue(all(chunk["table_parts"] == len(table_chunks) for chunk in table_chunks))
        self.assertTrue(all(chunk["structured_path"] == "tables/TABLE_BIG.json" for chunk in table_chunks))

    def test_figure_becomes_a_figure_chunk_with_separate_ocr_and_description(self):
        figure = {"asset_id": "FIG0008", "caption": "Şekil 8. Enkesit", "page": 33,
                  "path": "figures/FIG0008.png", "ocr_text": "NATM",
                  "ocr_status": "SUCCESS", "visual_description": None,
                  "visual_description_status": "NOT_RUN"}
        elements = [_element("FREF0001", "figure_ref", "Şekil 8. Enkesit",
                             asset_id="FIG0008", page_start=33)]
        chunks, _ = chunk_document(context=_context(), elements=elements, tables=[],
                                   figures=[figure], slides=[], sheets=[], ocr_items=[],
                                   policy=self.policy, root=self.root)
        figure_chunks = [c for c in chunks if c["chunk_type"] == FIGURE_CHUNK]
        self.assertEqual(len(figure_chunks), 1)
        chunk = figure_chunks[0]
        self.assertEqual(chunk["figure_id"], "FIG0008")
        self.assertEqual(chunk["page"], 33)
        self.assertEqual(chunk["ocr_text"], "NATM")
        self.assertIsNone(chunk["visual_description"])
        self.assertEqual(chunk["visual_description_status"], "NOT_RUN")

    def test_figure_with_no_content_produces_no_chunk(self):
        figure = {"asset_id": "FIG0001", "caption": None, "page": 1, "path": "f.png",
                  "ocr_text": None, "ocr_status": "EMPTY", "visual_description": None,
                  "visual_description_status": "NOT_RUN"}
        chunks, _ = chunk_document(context=_context(), elements=[], tables=[], figures=[figure],
                                   slides=[], sheets=[], ocr_items=[], policy=self.policy,
                                   root=self.root)
        self.assertEqual([c for c in chunks if c["chunk_type"] == FIGURE_CHUNK], [])

    def test_slide_becomes_a_slide_chunk(self):
        slides = [{"slide_number": 1, "title": "Ovit Tüneli", "text": "Sunum gövdesi.",
                   "tables": ["TABLE0001"], "figures": ["FIG0001"], "charts": [],
                   "notes": "Konuşmacı notu", "snapshot_path": "slides/slide_0001.png"}]
        chunks, _ = chunk_document(context=_context(), elements=[], tables=[], figures=[],
                                   slides=slides, sheets=[], ocr_items=[], policy=self.policy,
                                   root=self.root)
        slide_chunks = [c for c in chunks if c["chunk_type"] == SLIDE_CHUNK]
        self.assertEqual(len(slide_chunks), 1)
        chunk = slide_chunks[0]
        self.assertEqual(chunk["slide_number"], 1)
        self.assertEqual(chunk["slide_title"], "Ovit Tüneli")
        self.assertEqual(chunk["speaker_notes"], "Konuşmacı notu")
        self.assertEqual(chunk["table_refs"], ["TABLE0001"])
        self.assertEqual(chunk["figure_refs"], ["FIG0001"])
        self.assertIn("Ovit Tüneli", chunk["text"])

    def test_sheet_becomes_sheet_chunks_not_one_giant_text_chunk(self):
        path = self.root / "sheets" / "Maliyetler.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        cells = [{"sheet": "Maliyetler", "cell": "A1", "row": 1, "column": 1,
                  "value": "Kalem", "formula": None, "data_type": "s"},
                 {"sheet": "Maliyetler", "cell": "B22", "row": 22, "column": 2,
                  "value": None, "formula": "=SUM(B2:B21)", "data_type": "f"}]
        for row in range(2, 22):
            cells.append({"sheet": "Maliyetler", "cell": f"A{row}", "row": row, "column": 1,
                          "value": f"kalem {row}", "formula": None, "data_type": "s"})
        path.write_text(json.dumps({"cells": cells}), encoding="utf-8")
        sheets = [{"asset_id": "SHEET0001", "sheet_name": "Maliyetler", "hidden": False,
                   "used_range": "A1:B22", "structured_path": "sheets/Maliyetler.json",
                   "csv_path": None, "excel_tables": []}]
        chunks, _ = chunk_document(context=_context(), elements=[], tables=[], figures=[],
                                   slides=[], sheets=sheets, ocr_items=[],
                                   policy=self.policy, root=self.root)
        sheet_chunks = [c for c in chunks if c["chunk_type"] == SHEET_CHUNK]
        self.assertTrue(sheet_chunks)
        chunk = sheet_chunks[0]
        self.assertEqual(chunk["sheet_name"], "Maliyetler")
        self.assertIsNotNone(chunk["cell_range"])
        self.assertTrue(chunk["formula_present"])
        self.assertIn("=SUM(B2:B21)", chunk["text"])

    def test_large_sheet_is_banded_into_several_chunks(self):
        path = self.root / "sheets" / "Big.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        cells = [{"sheet": "Big", "cell": f"A{row}", "row": row, "column": 1,
                  "value": f"v{row}", "formula": None, "data_type": "s"}
                 for row in range(1, 200)]
        path.write_text(json.dumps({"cells": cells}), encoding="utf-8")
        sheets = [{"asset_id": "SHEET0001", "sheet_name": "Big", "hidden": False,
                   "used_range": "A1:A199", "structured_path": "sheets/Big.json",
                   "csv_path": None, "excel_tables": []}]
        chunks, _ = chunk_document(context=_context(), elements=[], tables=[], figures=[],
                                   slides=[], sheets=sheets, ocr_items=[],
                                   policy=self.policy, root=self.root)
        self.assertGreater(len([c for c in chunks if c["chunk_type"] == SHEET_CHUNK]), 1)

    def test_wide_sheet_is_split_below_hard_limit(self):
        path = self.root / "sheets" / "Wide.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        cells = [{
            "sheet": "Wide", "cell": "A1", "row": 1, "column": 1,
            "value": "!" * (self.policy.hard_max_tokens * 2),
            "formula": None, "data_type": "s",
        }]
        path.write_text(json.dumps({"cells": cells}), encoding="utf-8")
        sheets = [{
            "asset_id": "SHEET0001", "sheet_name": "Wide", "hidden": False,
            "used_range": "A1:A1", "structured_path": "sheets/Wide.json",
            "csv_path": None, "excel_tables": [],
        }]
        chunks, _ = chunk_document(
            context=_context(), elements=[], tables=[], figures=[], slides=[], sheets=sheets,
            ocr_items=[], policy=self.policy, root=self.root,
        )
        sheet_chunks = [chunk for chunk in chunks if chunk["chunk_type"] == SHEET_CHUNK]
        self.assertGreater(len(sheet_chunks), 1)
        self.assertTrue(all(
            chunk["token_count"] <= self.policy.max_tokens for chunk in sheet_chunks
        ))
        self.assertEqual(
            [chunk["sheet_part"] for chunk in sheet_chunks],
            list(range(1, len(sheet_chunks) + 1)),
        )
        self.assertTrue(all(
            chunk["sheet_parts"] == len(sheet_chunks) for chunk in sheet_chunks
        ))

    def test_page_ocr_becomes_an_ocr_chunk(self):
        ocr_items = [{"ocr_item_id": "OCRPAGE0001", "scope": "PAGE", "page": 1,
                      "asset_id": "PAGE0001", "ocr_status": "SUCCESS",
                      "ocr_text": "Taranmış sayfa metni " * 20, "ocr_engine": "rapidocr_torch",
                      "ocr_confidence": None, "ocr_languages": ["tr", "en"]}]
        chunks, _ = chunk_document(context=_context(), elements=[], tables=[], figures=[],
                                   slides=[], sheets=[], ocr_items=ocr_items,
                                   policy=self.policy, root=self.root)
        ocr_chunks = [c for c in chunks if c["chunk_type"] == OCR_CHUNK]
        self.assertEqual(len(ocr_chunks), 1)
        self.assertEqual(ocr_chunks[0]["page"], 1)
        self.assertIsNone(ocr_chunks[0]["ocr_confidence"])

    def test_figure_ocr_is_not_duplicated_as_an_ocr_chunk(self):
        """§57 — OCR text already inside a figure chunk must not be emitted twice."""
        text = "Püskürtme beton 20 cm " * 10
        figure = {"asset_id": "FIG0001", "caption": None, "page": 5, "path": "f.png",
                  "ocr_text": text, "ocr_status": "SUCCESS", "visual_description": None,
                  "visual_description_status": "NOT_RUN"}
        ocr_items = [{"ocr_item_id": "OCRFIG0001", "scope": "FIGURE", "page": 5,
                      "asset_id": "FIG0001", "ocr_status": "SUCCESS", "ocr_text": text,
                      "ocr_engine": "rapidocr_torch", "ocr_confidence": None,
                      "ocr_languages": ["tr"]}]
        chunks, _ = chunk_document(context=_context(), elements=[], tables=[], figures=[figure],
                                   slides=[], sheets=[], ocr_items=ocr_items,
                                   policy=self.policy, root=self.root)
        self.assertEqual(len([c for c in chunks if c["chunk_type"] == FIGURE_CHUNK]), 1)
        self.assertEqual([c for c in chunks if c["chunk_type"] == OCR_CHUNK], [])


class DedupTests(unittest.TestCase):
    """§60 — page OCR plus native text must not create duplicated evidence."""

    def setUp(self):
        self.policy = ChunkPolicy.from_config(load_config())

    def test_native_text_wins_over_identical_page_ocr(self):
        body = LOREM * 12
        chunks, _ = chunk_document(
            context=_context(),
            elements=[_element("PARA0001", "paragraph", body, page_start=1)],
            tables=[], figures=[], slides=[], sheets=[],
            ocr_items=[{"ocr_item_id": "OCRPAGE0001", "scope": "PAGE", "page": 1,
                        "asset_id": "PAGE0001", "ocr_status": "SUCCESS", "ocr_text": body,
                        "ocr_engine": "rapidocr_torch", "ocr_confidence": None,
                        "ocr_languages": ["tr"]}],
            policy=self.policy, root=Path("."))
        types = {c["chunk_type"] for c in chunks}
        self.assertIn(TEXT_CHUNK, types)
        self.assertNotIn(OCR_CHUNK, types)

    def test_dropped_chunks_are_reported(self):
        duplicate = {"chunk_id": "A", "chunk_type": TEXT_CHUNK, "text": LOREM * 5}
        same = {"chunk_id": "B", "chunk_type": OCR_CHUNK, "text": LOREM * 5}
        kept, dropped = deduplicate([duplicate, same], self.policy)
        self.assertEqual(len(kept), 1)
        self.assertEqual(kept[0]["chunk_type"], TEXT_CHUNK)
        self.assertEqual(dropped[0]["duplicate_of"], "A")

    def test_distinct_chunks_are_kept(self):
        kept, dropped = deduplicate(
            [{"chunk_id": "A", "chunk_type": TEXT_CHUNK, "text": "Tünel kazısı yöntemleri."},
             {"chunk_id": "B", "chunk_type": TEXT_CHUNK, "text": "Havalandırma tasarımı."}],
            self.policy)
        self.assertEqual(len(kept), 2)
        self.assertEqual(dropped, [])


class ChunkQualityGateTests(unittest.TestCase):
    """§63 — the chunk quality gate catches what it claims to catch."""

    def setUp(self):
        self.policy = ChunkPolicy.from_config(load_config())
        self.elements = [_element("PARA0001", "paragraph", LOREM * 12, page_start=1)]

    def _chunks(self):
        return chunk_document(context=_context(), elements=self.elements, tables=[],
                              figures=[], slides=[], sheets=[], ocr_items=[],
                              policy=self.policy, root=Path("."))[0]

    def _evaluate(self, chunks):
        return quality_module.evaluate(
            document_id="ING_test", chunks=chunks, elements=self.elements, tables=[],
            figures=[], sheets=[], slides=[], policy=self.policy)

    def test_clean_chunks_pass(self):
        report = self._evaluate(self._chunks())
        self.assertIn(report["status"], {quality_module.PASS, quality_module.WARN})
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["chunk_count"], len(self._chunks()))
        self.assertIn("chunk_policy_version", report["policy"])

    def test_duplicate_ids_fail(self):
        chunks = self._chunks()
        chunks.append(dict(chunks[0]))
        report = self._evaluate(chunks)
        self.assertEqual(report["status"], quality_module.FAIL)
        self.assertTrue(any(e.startswith("DUPLICATE_CHUNK_IDS") for e in report["errors"]))

    def test_unresolved_source_element_fails(self):
        chunks = self._chunks()
        chunks[0]["source_elements"] = ["PARA9999"]
        report = self._evaluate(chunks)
        self.assertTrue(any(e.startswith("UNRESOLVED_SOURCE_ELEMENTS")
                            for e in report["errors"]))

    def test_missing_provenance_fails(self):
        chunks = self._chunks()
        chunks[0]["provenance"] = {}
        report = self._evaluate(chunks)
        self.assertTrue(any(e.startswith("CHUNK_PROVENANCE_MISSING") for e in report["errors"]))

    def test_invalid_section_fails(self):
        chunks = self._chunks()
        chunks[0]["final_primary_section"] = "99.99"
        report = self._evaluate(chunks)
        self.assertTrue(any(e.startswith("INVALID_SECTION") for e in report["errors"]))

    def test_empty_chunk_fails(self):
        chunks = self._chunks()
        chunks[0]["text"] = "   "
        report = self._evaluate(chunks)
        self.assertTrue(any(e.startswith("EMPTY_CHUNK") for e in report["errors"]))

    def test_oversized_chunk_fails(self):
        chunks = self._chunks()
        chunks[0]["text"] = LOREM * 400
        chunks[0]["token_count"] = tokenizer.count(chunks[0]["text"])
        report = self._evaluate(chunks)
        self.assertTrue(any(e.startswith("CHUNK_OVER_HARD_MAX") for e in report["errors"]))

    def test_standalone_short_structural_chunk_is_informational(self):
        elements = [_element("PARA_SHORT", "paragraph", "Kısa sonuç.", page_start=1)]
        chunks = chunk_document(
            context=_context(), elements=elements, tables=[], figures=[], slides=[], sheets=[],
            ocr_items=[], policy=self.policy, root=Path("."),
        )[0]
        report = quality_module.evaluate(
            document_id="ING_test", chunks=chunks, elements=elements, tables=[], figures=[],
            sheets=[], slides=[], policy=self.policy,
        )
        self.assertTrue(any(
            warning.startswith("CHUNK_SHORT_STRUCTURAL") for warning in report["warnings"]
        ))
        self.assertFalse(any(
            warning.startswith("CHUNK_UNDER_MIN") for warning in report["warnings"]
        ))

    def test_duplicate_text_flood_fails(self):
        chunks = self._chunks()
        base = chunks[0]
        for index in range(6):
            copy = dict(base)
            copy["chunk_id"] = f"{base['chunk_id']}_{index}"
            copy["text"] = base["text"] + f" {index}"
            copy["token_count"] = tokenizer.count(copy["text"])
            chunks.append(copy)
        report = self._evaluate(chunks)
        self.assertEqual(report["status"], quality_module.FAIL)
        self.assertTrue(any(e.startswith("DUPLICATE_TEXT_FLOOD") for e in report["errors"]))


class EmbeddingManifestTests(unittest.TestCase):
    """§64 — eligibility decided here; embeddings never computed here."""

    def setUp(self):
        self.policy = ChunkPolicy.from_config(load_config())
        self.chunks = chunk_document(
            context=_context(),
            elements=[_element("PARA0001", "paragraph", LOREM * 12, page_start=3,
                               heading_path=["4. MALİYET"])],
            tables=[], figures=[], slides=[], sheets=[], ocr_items=[],
            policy=self.policy, root=Path("."))[0]

    def test_rows_are_ready_and_carry_no_vector(self):
        rows = manifest_module.build_rows(self.chunks, self.policy)
        self.assertTrue(rows)
        for row in rows:
            self.assertTrue(row["eligible"])
            self.assertEqual(row["reason"], manifest_module.READY)
            self.assertNotIn("embedding", row)
            self.assertNotIn("vector", row)
            self.assertGreater(row["token_count"], 0)
            self.assertEqual(row["section_id"], "5.5.2")
            self.assertEqual(row["page_start"], 3)
            self.assertIn("4. MALİYET", row["embedding_text"])

    def test_unstaged_document_is_not_eligible(self):
        rows = manifest_module.build_rows(self.chunks, self.policy, document_staged=False)
        self.assertFalse(rows[0]["eligible"])
        self.assertEqual(rows[0]["reason"], manifest_module.DOCUMENT_NOT_STAGED)

    def test_failed_chunk_quality_blocks_eligibility(self):
        rows = manifest_module.build_rows(self.chunks, self.policy, chunk_quality_ok=False)
        self.assertEqual(rows[0]["reason"], manifest_module.CHUNK_QUALITY_FAILED)

    def test_sectionless_chunk_is_not_eligible(self):
        chunk = dict(self.chunks[0])
        chunk["final_primary_section"] = None
        row = manifest_module.row_for(chunk, self.policy)
        self.assertFalse(row["eligible"])
        self.assertEqual(row["reason"], manifest_module.NO_SECTION)

    def test_tiny_chunk_is_not_eligible(self):
        chunk = dict(self.chunks[0])
        chunk["text"] = "kısa"
        chunk["heading_path"] = []
        row = manifest_module.row_for(chunk, self.policy)
        self.assertFalse(row["eligible"])
        self.assertEqual(row["reason"], manifest_module.TOO_SHORT)

    def test_merge_replaces_only_the_named_documents(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "embedding_ready_manifest.jsonl"
            path.write_text(json.dumps({"chunk_id": "old", "document_id": "ING_other"}) + "\n",
                            encoding="utf-8")
            rows = manifest_module.build_rows(self.chunks, self.policy)
            manifest_module.merge_into(path, rows, document_ids={"ING_test"})
            written = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
            self.assertEqual(sum(1 for r in written if r["document_id"] == "ING_other"), 1)
            self.assertEqual(sum(1 for r in written if r["document_id"] == "ING_test"),
                             len(rows))


class ManifestIoTests(unittest.TestCase):
    def test_chunks_round_trip_through_the_manifest(self):
        policy = ChunkPolicy.from_config(load_config())
        chunks = chunk_document(
            context=_context(),
            elements=[_element("PARA0001", "paragraph", LOREM * 10)],
            tables=[], figures=[], slides=[], sheets=[], ocr_items=[],
            policy=policy, root=Path("."))[0]
        with tempfile.TemporaryDirectory() as d:
            bundle = Path(d)
            path = write_chunks(bundle, chunks)
            self.assertTrue(path.is_file())
            self.assertEqual(read_chunks(bundle), chunks)


if __name__ == "__main__":
    unittest.main()
