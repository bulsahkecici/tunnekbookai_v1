"""Dedup, classification, evidence, quality-gate and crawler-contract tests
(task §76, §77, §78).

Run:  PYTHONPATH=. .venv/bin/python -m unittest tests.ingest.test_pipeline -v
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from tunnelbookai.ingest import evidence as evidence_module
from tunnelbookai.ingest import quality_gate as gate_module
from tunnelbookai.ingest.classify import pipeline as classify_module
from tunnelbookai.ingest.classify.taxonomy import is_valid_section, load_taxonomy
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.dedup import (
    DedupKey, SourceRegistry, normalize_doi, normalize_title, normalize_url, resolve,
)
from tunnelbookai.ingest.extraction import ExtractionResult
from tunnelbookai.ingest.metadata.provenance import ProvenanceError, ProvenanceLog, record
from tunnelbookai.ingest.metadata.schema import empty_metadata, validate
from tunnelbookai.ingest.sources import papercrawler_contract

FIX = Path(__file__).resolve().parent / "fixtures"


def _metadata(document_id: str, **overrides):
    metadata = empty_metadata(document_id)
    metadata.update({
        "source_kind": "MANUAL_INTERNAL",
        "original_filename": "x.pdf",
        "original_sha256": "a" * 64,
        "format": "PDF",
        "mime_type": "application/pdf",
        "ingest_method": "manual_inbox",
    })
    metadata.update(overrides)
    return metadata


class TaxonomyTests(unittest.TestCase):
    """§35 — one canonical taxonomy, and only that one."""

    def test_canonical_baseline_counts(self):
        taxonomy = load_taxonomy()
        self.assertEqual(len(taxonomy.sections), 66)
        question_bank = [s for s in taxonomy.sections.values() if s.is_question_bank_section]
        self.assertEqual(len(question_bank), 59)
        self.assertEqual(taxonomy.source_path, "book/scope/normalized/book_scope.json")

    def test_crawler_terms_never_add_sections(self):
        taxonomy = load_taxonomy()
        self.assertEqual(taxonomy.unknown_term_sections, ())

    def test_invalid_section_rejected(self):
        self.assertTrue(is_valid_section("1.1"))
        self.assertFalse(is_valid_section("99.99"))
        self.assertFalse(is_valid_section(None))
        self.assertFalse(is_valid_section(""))


class DedupTests(unittest.TestCase):
    """§32, §77 — one identity, many provenance sources."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.registry = SourceRegistry(Path(self.tmp.name) / "source_registry.jsonl")

    def tearDown(self):
        self.tmp.cleanup()

    def test_same_sha_from_crawler_and_manual_is_one_document(self):
        sha = "b" * 64
        metadata = _metadata("ING_same", original_sha256=sha, title="Tünel Bakım Raporu")
        resolve(self.registry, metadata, source_kinds=["EXTERNAL_DISCOVERY"], state="DEDUP",
                provenance_sources=[{"kind": "EXTERNAL_DISCOVERY", "canonical_id": "CAN_1"}])
        # the identical bytes arrive again, this time from the manual inbox
        match, warnings = resolve(
            self.registry, metadata, source_kinds=["MANUAL_INTERNAL"], state="DEDUP",
            provenance_sources=[{"kind": "MANUAL_INTERNAL", "inbox_relative_path": "x.pdf"}])

        self.assertIsNone(match, "the same document_id must not match itself")
        self.assertEqual(len(self.registry.rows), 1, "one document identity")
        row = self.registry.rows["ING_same"]
        self.assertEqual(row["source_kinds"], ["EXTERNAL_DISCOVERY", "MANUAL_INTERNAL"])
        self.assertEqual(row["provenance_source_count"], 2, "two provenance sources")
        self.assertEqual(warnings, [])

    def test_different_ids_same_sha_flagged_exact(self):
        sha = "c" * 64
        resolve(self.registry, _metadata("ING_a", original_sha256=sha),
                source_kinds=["EXTERNAL_DISCOVERY"], state="DEDUP")
        match, warnings = resolve(self.registry, _metadata("ING_b", original_sha256=sha),
                                  source_kinds=["MANUAL_INTERNAL"], state="DEDUP")
        self.assertIsNotNone(match)
        self.assertEqual((match.rule, match.strength), ("sha256", "EXACT"))
        self.assertTrue(any(w.startswith("DUPLICATE_EXACT:sha256") for w in warnings))
        self.assertEqual(self.registry.rows["ING_b"]["duplicate_of"], "ING_a")

    def test_doi_and_url_normalization(self):
        self.assertEqual(normalize_doi("https://doi.org/10.1234/AbC"), "10.1234/abc")
        self.assertEqual(normalize_doi("DOI:10.1234/abc."), "10.1234/abc")
        self.assertEqual(normalize_url("https://WWW.Example.com/a/?utm_source=x"),
                         "https://example.com/a")
        self.assertEqual(normalize_title("  Tünel   Bakımı!  "), "tunel bakimi")

    def test_doi_match_merges(self):
        resolve(self.registry, _metadata("ING_1", original_sha256="d" * 64,
                                         doi="10.1000/xyz", title="A"),
                source_kinds=["EXTERNAL_DISCOVERY"], state="DEDUP")
        match, _ = resolve(self.registry, _metadata("ING_2", original_sha256="e" * 64,
                                                    doi="https://doi.org/10.1000/XYZ", title="B"),
                           source_kinds=["MANUAL_INTERNAL"], state="DEDUP")
        self.assertEqual((match.rule, match.strength), ("doi", "EXACT"))

    def test_filename_derived_title_never_merges(self):
        """Two unrelated files both called source.pdf must NOT collapse into one document."""
        first = _metadata("ING_x", original_sha256="1" * 64, title="source",
                          title_inferred_from_filename=True, document_date="2024")
        second = _metadata("ING_y", original_sha256="2" * 64, title="source",
                           title_inferred_from_filename=True, document_date="2024")
        resolve(self.registry, first, source_kinds=["MANUAL_INTERNAL"], state="DEDUP")
        match, warnings = resolve(self.registry, second, source_kinds=["MANUAL_INTERNAL"],
                                  state="DEDUP")
        self.assertIsNone(match)
        self.assertEqual(warnings, [])

    def test_fuzzy_title_is_a_candidate_never_an_automatic_merge(self):
        base = _metadata("ING_p", original_sha256="3" * 64,
                         title="Tünel Bakım Onarım Maliyet Raporu 2024",
                         document_date="2024", organization="KGM")
        near = _metadata("ING_q", original_sha256="4" * 64,
                         title="Tünel Bakım Onarım Maliyet Raporu 2024.",
                         document_date="2024", organization="KGM")
        resolve(self.registry, base, source_kinds=["MANUAL_INTERNAL"], state="DEDUP")
        match, warnings = resolve(self.registry, near, source_kinds=["MANUAL_INTERNAL"],
                                  state="DEDUP")
        self.assertIsNotNone(match)
        self.assertIn(match.strength, {"STRONG", "PROBABLE"})
        if match.strength == "PROBABLE":
            self.assertTrue(any(w.startswith("DUPLICATE_CANDIDATE") for w in warnings))
            self.assertNotIn("duplicate_of", self.registry.rows["ING_q"])

    def test_registry_round_trips(self):
        resolve(self.registry, _metadata("ING_r", original_sha256="f" * 64, title="T"),
                source_kinds=["MANUAL_INTERNAL"], state="DEDUP")
        self.registry.flush()
        reloaded = SourceRegistry(self.registry.path)
        self.assertIn("ING_r", reloaded.rows)


class MetadataSchemaTests(unittest.TestCase):
    """§29, §30, §31 — schema validity and no-hallucination provenance."""

    def test_valid_metadata_passes(self):
        self.assertEqual(validate(_metadata("ING_ok")), [])

    def test_missing_required_field_reported(self):
        metadata = _metadata("ING_bad")
        metadata["original_sha256"] = None
        self.assertIn("MISSING_REQUIRED_FIELD:original_sha256", validate(metadata))

    def test_unknown_document_type_rejected(self):
        metadata = _metadata("ING_dt", document_type="wharrgarbl")
        self.assertIn("INVALID_DOCUMENT_TYPE:wharrgarbl", validate(metadata))

    def test_unknown_values_stay_unknown_not_invented(self):
        metadata = empty_metadata("ING_empty")
        self.assertIsNone(metadata["organization"])
        self.assertIsNone(metadata["document_date"])
        self.assertEqual(metadata["confidentiality"], "UNKNOWN")
        self.assertEqual(metadata["document_status"], "UNKNOWN")
        self.assertEqual(metadata["authors"], [])

    def test_inferred_value_requires_reason_and_confidence(self):
        with self.assertRaises(ProvenanceError):
            record("title", "X", source="document_content", inferred=True)
        with self.assertRaises(ProvenanceError):
            record("title", "X", source="document_content", inferred=True, reason="because")
        entry = record("title", "X", source="document_content", inferred=True,
                       reason="heading", confidence="high")
        self.assertTrue(entry["inferred"])
        self.assertEqual(entry["confidence"], 0.9)

    def test_unknown_provenance_source_rejected(self):
        with self.assertRaises(ProvenanceError):
            record("title", "X", source="a_wild_guess")

    def test_provenance_log_records_misses(self):
        log = ProvenanceLog()
        metadata = empty_metadata("ING_l")
        log.miss("organization")
        log.set(metadata, "title", "T", source="document_heading", confidence="high")
        self.assertEqual(metadata["title"], "T")
        self.assertIsNone(metadata["organization"])
        payload = log.to_dict("ING_l")
        missed = [f for f in payload["fields"] if f["field"] == "organization"][0]
        self.assertEqual(missed["source"], "not_found")
        self.assertIsNone(missed["value"])


class EvidenceModelTests(unittest.TestCase):
    """§42 — the ingest engine's own evidence levels."""

    def _extraction(self, **kwargs):
        result = ExtractionResult(document_id="ING_e", format="PDF", adapter="pdf")
        result.normalized_json_path = "processing/ING_e/normalized/document.json"
        for key, value in kwargs.items():
            setattr(result, key, value)
        return result

    def test_full_text(self):
        result = self._extraction(text_char_count=5000, page_count=4,
                                  capabilities={"text": True, "tables": True})
        self.assertEqual(evidence_module.determine(result)[0], evidence_module.FULL_TEXT)

    def test_structured_tabular_for_workbooks(self):
        result = self._extraction(text_char_count=50, page_count=3,
                                  capabilities={"sheets": True, "text": True})
        self.assertEqual(evidence_module.determine(result)[0],
                         evidence_module.STRUCTURED_TABULAR)

    def test_visual_only_for_a_textless_image(self):
        result = self._extraction(adapter="image", text_char_count=0, page_count=1,
                                  capabilities={"figures": True})
        self.assertEqual(evidence_module.determine(result)[0], evidence_module.VISUAL_ONLY)

    def test_unusable_when_extraction_failed(self):
        result = self._extraction(errors=["boom"])
        self.assertEqual(evidence_module.determine(result)[0], evidence_module.UNUSABLE)

    def test_capabilities_always_complete(self):
        capabilities = evidence_module.content_capabilities(self._extraction(capabilities={}))
        for key in evidence_module.CAPABILITY_KEYS:
            self.assertIn(key, capabilities)
            self.assertIsInstance(capabilities[key], bool)


class ClassificationTests(unittest.TestCase):
    """Final classification is solely TunnelBookAI's responsibility."""

    @classmethod
    def setUpClass(cls):
        cls.config = load_config()
        cls.taxonomy = load_taxonomy()

    def _classify(self, text, headings=None, **kwargs):
        elements = []
        for index, heading in enumerate(headings or [], start=1):
            elements.append({"element_id": f"HEAD{index:04d}", "type": "heading",
                             "text": heading, "heading_path": [heading], "level": 1,
                             "page_start": 1, "page_end": 1, "asset_id": None})
        elements.append({"element_id": "PARA0001", "type": "paragraph", "text": text,
                         "heading_path": list(headings or []), "level": None,
                         "page_start": 1, "page_end": 1, "asset_id": None})
        return classify_module.classify(
            metadata={"title": (headings or [""])[0], "document_type": None, "topics": []},
            elements=elements, tables=[], figures=[], normalized_text=text,
            config=self.config, taxonomy=self.taxonomy,
            embedding_index=None, embedding_status="DISABLED", embedding_model=None,
            allow_arbiter=False, **kwargs)

    def test_single_strong_section(self):
        result = self._classify(
            "Tünelin tanımı: yeraltında inşa edilen geçiş yapısı. tunnel definition ve "
            "tunnel terminology bu bölümde açıklanır.",
            headings=["Tünelin Tanımı"])
        self.assertEqual(result.final_primary_section, "1.1")
        self.assertTrue(is_valid_section(result.final_primary_section))
        self.assertIn("heading_rules", result.classification_methods)

    def test_result_is_always_inside_the_canonical_taxonomy(self):
        result = self._classify("shotcrete rock bolt NATM tunnel support system",
                                headings=["Destek Sistemleri"])
        for section_id in [result.final_primary_section, *result.final_secondary_sections]:
            if section_id:
                self.assertIn(section_id, self.taxonomy)

    def test_multi_section_support(self):
        result = self._classify(
            "tunnel maintenance cost ve tunnel repair cost analizi; ayrıca operation cost "
            "ve maintenance cost kalemleri incelenmiştir. bakım maliyeti ve işletme maliyeti.",
            headings=["Bakım-Onarım Maliyetleri"])
        self.assertIsNotNone(result.final_primary_section)
        self.assertIsInstance(result.final_secondary_sections, list)
        self.assertNotIn(result.final_primary_section, result.final_secondary_sections)

    def test_low_confidence_produces_no_invented_section(self):
        result = self._classify("aaa bbb ccc", headings=[])
        if result.final_primary_section is None:
            self.assertIn("NO_SECTION_CANDIDATES", result.warnings)
        else:
            self.assertIn(result.final_primary_section, self.taxonomy)


    def test_section_evidence_points_at_real_elements(self):
        result = self._classify("tunnel definition tünel tanımı yapısı",
                                headings=["Tünelin Tanımı"])
        if result.section_evidence:
            known = {"HEAD0001", "PARA0001"}
            for entry in result.section_evidence:
                self.assertIn(entry["section_id"], self.taxonomy)
                for ref in entry["supporting_elements"]:
                    self.assertIn(ref, known)


class QualityGateTests(unittest.TestCase):
    """§43, §44, §45 — GO / REVIEW / REJECT."""

    @classmethod
    def setUpClass(cls):
        cls.config = load_config()

    def _inputs(self, **overrides):
        extraction = ExtractionResult(document_id="ING_g", format="PDF", adapter="pdf")
        extraction.normalized_json_path = "processing/ING_g/normalized/document.json"
        extraction.page_count = 2
        extraction.pages = [{"page_number": 1}, {"page_number": 2}]
        extraction.capabilities = {"text": True, "page_snapshots": True}
        extraction.text_char_count = 4000

        payload = {
            "document_id": "ING_g",
            "archive_meta": {"original_sha256": "a" * 64, "format": "PDF",
                             "original_filename": "x.pdf"},
            "provenance_doc": {"sources": [{"kind": "MANUAL_INTERNAL"}]},
            "extraction": extraction,
            "metadata": _metadata("ING_g"),
            "classification": SimpleNamespace(final_primary_section="1.1",
                                              final_section_confidence=0.9),
            "evidence_level": evidence_module.FULL_TEXT,
            "config": self.config,
        }
        payload.update(overrides)
        return payload

    def test_go_when_every_minimum_holds(self):
        with tempfile.TemporaryDirectory() as d:
            original = Path(d) / "x.pdf"
            original.write_bytes(b"%PDF-1.4")
            result = gate_module.evaluate(**self._inputs(original_path=original))
        self.assertEqual(result.decision, gate_module.GO, result.reject_reasons)
        self.assertTrue(all(result.checks.values()), result.checks)

    def test_missing_original_rejects(self):
        result = gate_module.evaluate(**self._inputs(original_path=Path("/nope/x.pdf")))
        self.assertEqual(result.decision, gate_module.REJECT)
        self.assertIn("ORIGINAL_MISSING", result.reject_reasons)

    def test_invalid_section_rejects(self):
        with tempfile.TemporaryDirectory() as d:
            original = Path(d) / "x.pdf"
            original.write_bytes(b"%PDF")
            result = gate_module.evaluate(**self._inputs(
                original_path=original,
                classification=SimpleNamespace(final_primary_section="99.99",
                                               final_section_confidence=0.9)))
        self.assertEqual(result.decision, gate_module.REJECT)
        self.assertIn("FINAL_SECTION_INVALID_OR_MISSING", result.reject_reasons)

    def test_missing_office_renderer_is_review_never_reject(self):
        """§45 — a DOCX is never rejected just because LibreOffice is absent."""
        extraction = ExtractionResult(document_id="ING_g", format="DOCX", adapter="docx")
        extraction.normalized_json_path = "processing/ING_g/normalized/document.json"
        extraction.capabilities = {"text": True}
        extraction.text_char_count = 3000
        extraction.warnings = ["VISUAL_RENDERER_UNAVAILABLE"]
        with tempfile.TemporaryDirectory() as d:
            original = Path(d) / "x.docx"
            original.write_bytes(b"PK")
            result = gate_module.evaluate(**self._inputs(
                original_path=original, extraction=extraction,
                archive_meta={"original_sha256": "a" * 64, "format": "DOCX",
                              "original_filename": "x.docx"},
                metadata=_metadata("ING_g", format="DOCX",
                                   mime_type="application/vnd.openxmlformats-"
                                             "officedocument.wordprocessingml.document"),
                evidence_level=evidence_module.STRUCTURED_DOCUMENT))
        self.assertEqual(result.decision, gate_module.REVIEW)
        self.assertIn("VISUAL_RENDERER_UNAVAILABLE", result.review_reasons)
        self.assertEqual(result.reject_reasons, [])

    def test_present_office_renderer_clears_the_review_reason(self):
        """§9 — with LibreOffice available, an otherwise valid DOCX is not sent to review.

        The mirror of the test above: the same document, differing only in whether the
        renderer emitted VISUAL_RENDERER_UNAVAILABLE, must come out clean.
        """
        extraction = ExtractionResult(document_id="ING_g", format="DOCX", adapter="docx")
        extraction.normalized_json_path = "processing/ING_g/normalized/document.json"
        extraction.capabilities = {"text": True}
        extraction.text_char_count = 3000
        extraction.warnings = []
        extraction.pages = [{"page_number": 1, "snapshot_asset_id": "PAGE0001"}]
        with tempfile.TemporaryDirectory() as d:
            original = Path(d) / "x.docx"
            original.write_bytes(b"PK")
            result = gate_module.evaluate(**self._inputs(
                original_path=original, extraction=extraction,
                archive_meta={"original_sha256": "a" * 64, "format": "DOCX",
                              "original_filename": "x.docx"},
                metadata=_metadata("ING_g", format="DOCX",
                                   mime_type="application/vnd.openxmlformats-"
                                             "officedocument.wordprocessingml.document"),
                evidence_level=evidence_module.STRUCTURED_DOCUMENT))
        self.assertNotIn("VISUAL_RENDERER_UNAVAILABLE", result.review_reasons)
        self.assertTrue(result.checks["office_visual_snapshots"])
        self.assertEqual(result.reject_reasons, [])

    def test_xlsx_without_structured_workbook_rejects(self):
        extraction = ExtractionResult(document_id="ING_g", format="XLSX", adapter="xlsx")
        extraction.normalized_json_path = "processing/ING_g/normalized/document.json"
        extraction.capabilities = {"text": True}
        extraction.sheets = []
        with tempfile.TemporaryDirectory() as d:
            original = Path(d) / "x.xlsx"
            original.write_bytes(b"PK")
            result = gate_module.evaluate(**self._inputs(
                original_path=original, extraction=extraction,
                archive_meta={"original_sha256": "a" * 64, "format": "XLSX",
                              "original_filename": "x.xlsx"},
                metadata=_metadata("ING_g", format="XLSX", mime_type="application/xlsx"),
                evidence_level=evidence_module.STRUCTURED_TABULAR))
        self.assertIn("XLSX_NO_STRUCTURED_WORKBOOK", result.reject_reasons)

    def test_textless_image_is_review_not_reject(self):
        extraction = ExtractionResult(document_id="ING_g", format="JPG", adapter="image")
        extraction.normalized_json_path = "processing/ING_g/normalized/document.json"
        extraction.capabilities = {"figures": True, "text": False}
        with tempfile.TemporaryDirectory() as d:
            original = Path(d) / "x.jpg"
            original.write_bytes(b"\xff\xd8\xff")
            result = gate_module.evaluate(**self._inputs(
                original_path=original, extraction=extraction,
                archive_meta={"original_sha256": "a" * 64, "format": "JPG",
                              "original_filename": "x.jpg"},
                metadata=_metadata("ING_g", format="JPG", mime_type="image/jpeg"),
                evidence_level=evidence_module.VISUAL_ONLY))
        self.assertEqual(result.decision, gate_module.REVIEW)
        self.assertIn("OCR_EMPTY_TEXT_IMAGE", result.review_reasons)


if __name__ == "__main__":
    unittest.main()
