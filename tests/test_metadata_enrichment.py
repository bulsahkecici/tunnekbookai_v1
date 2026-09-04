from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts/09_metadata_enrichment.py"
SPEC = importlib.util.spec_from_file_location("metadata_enrichment", SCRIPT)
metadata = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(metadata)


class MetadataRuleTests(unittest.TestCase):
    def test_migrated_filename_can_resolve_by_unique_front_matter_document_id(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            actual = root / "data/corpus_final/K/ROCKBIT-3.5_9m.md"
            actual.parent.mkdir(parents=True)
            actual.write_text("---\ndocument_id: DOC239\n---\n\n# Belge\n", encoding="utf-8")
            row = {"document_id": "DOC239", "final_output": "data/corpus_final/K/ROCKBIT-3.5''9m.md"}
            self.assertEqual(metadata.resolve_final_markdown(root, row), actual)

    def test_publication_year_never_uses_filesystem_time(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "document.pdf"
            path.write_text("Published without a stated date", encoding="utf-8")
            path.touch()
            year, evidence, confidence, conflict = metadata.infer_year(
                str(path), "Document without year", path.read_text(), ""
            )
            self.assertEqual(year, "")
            self.assertIn("filesystem tarihi kullanılmadı", evidence)
            self.assertEqual(confidence, "low")
            self.assertFalse(conflict)

    def test_known_official_source_gets_a_only_with_document_evidence(self):
        text = "# Karayolları Genel Müdürlüğü Tünel İşletme Yönetmeliği\nResmî Gazete"
        doc_type, _, _ = metadata.infer_document_type("KGM/Yönetmelik.pdf", "Tünel Yönetmeliği", text, "unknown", ".pdf")
        authority, evidence, confidence, organization = metadata.infer_authority(
            "KGM/Yönetmelik.pdf", "Tünel Yönetmeliği", text, "", doc_type
        )
        self.assertEqual(doc_type, "regulation")
        self.assertEqual((authority, confidence), ("A", "high"))
        self.assertIn("KGM", organization)
        self.assertTrue(evidence)

    def test_official_acronym_is_recognized_next_to_filename_underscore(self):
        authority, _, confidence, organization = metadata.infer_authority(
            "Manuals/tunnel_manual_FHWA.pdf", "tunnel_manual_FHWA", "# Tunnel Manual", "", "manual"
        )
        self.assertEqual((authority, confidence, organization), ("A", "high", "FHWA"))

    def test_institution_name_alone_does_not_blindly_get_a(self):
        authority, _, confidence, _ = metadata.infer_authority(
            "KGM/adsız.pdf", "Adsız belge", "KGM", "", "unknown"
        )
        self.assertEqual(authority, "unclassified")
        self.assertEqual(confidence, "low")

    def test_regulation_mention_inside_generic_content_does_not_get_a(self):
        authority, evidence, confidence, _ = metadata.infer_authority(
            "Training/Fire Safety.pdf", "Fire Safety", "This training discusses the tunnel regulation and KGM guidance.", "", "unknown"
        )
        self.assertEqual(authority, "unclassified")
        self.assertEqual(confidence, "low")
        self.assertIn("atıf", evidence)

    def test_academic_thesis_and_article_classification(self):
        thesis = "A thesis submitted to Istanbul Technical University for the degree of Master of Science"
        doc_type, _, _ = metadata.infer_document_type("Research/thesis.pdf", "Rock Mechanics", thesis, "unknown", ".pdf")
        authority, _, confidence, _ = metadata.infer_authority("Research/thesis.pdf", "Rock Mechanics", thesis, "", doc_type)
        self.assertEqual(doc_type, "thesis")
        self.assertEqual((authority, confidence), ("B", "high"))

        article = "# Research Article\nAbstract tunnel construction. DOI 10.1000/example. Journal of Tunnelling"
        article_type, _, _ = metadata.infer_document_type("Papers/article.pdf", "Article", article, "unknown", ".pdf")
        article_authority, _, article_confidence, _ = metadata.infer_authority("Papers/article.pdf", "Article", article, "", article_type)
        self.assertEqual(article_type, "academic_article")
        self.assertEqual(article_authority, "B")
        self.assertIn(article_confidence, {"medium", "high"})

    def test_academic_article_mentioning_kgm_and_standard_is_not_promoted_to_a(self):
        article = (
            "# Research Article\nAbstract Keywords tunnel design. DOI 10.1000/example. "
            "The study compares KGM guidance and the ISO 1234 standard. Journal of Tunnelling."
        )
        doc_type, _, _ = metadata.infer_document_type("Papers/study.pdf", "Research Article", article, "unknown", ".pdf")
        authority, _, confidence, _ = metadata.infer_authority("Papers/study.pdf", "Research Article", article, "", doc_type)
        self.assertEqual(doc_type, "academic_article")
        self.assertEqual(authority, "B")
        self.assertEqual(confidence, "medium")

    def test_wikipedia_secondary_source_gets_d(self):
        doc_type, _, _ = metadata.infer_document_type("Web/Tunnel - Wikipedia.pdf", "Tunnel - Wikipedia", "Wikipedia article", "unknown", ".pdf")
        authority, _, confidence, _ = metadata.infer_authority("Web/Tunnel - Wikipedia.pdf", "Tunnel", "Wikipedia article", "", doc_type)
        self.assertEqual(doc_type, "web_article")
        self.assertEqual((authority, confidence), ("D", "high"))

    def test_topic_output_never_leaves_controlled_vocabulary(self):
        topics, _, _ = metadata.infer_topics(
            "Tünel/NATM jet grout.pdf", "NATM Support", "Shotcrete, rock bolt, jet grouting and drainage", "operation|made_up_slug"
        )
        self.assertTrue(topics)
        self.assertTrue(set(topics).issubset(metadata.TOPICS))
        self.assertNotIn("made_up_slug", topics)
        self.assertIn("operations", topics)

    def test_citation_mode_correctness(self):
        cases = {
            (".pdf", True): "pdf_page", (".pdf", False): "source_only",
            (".pptx", False): "slide", (".docx", False): "document_section",
            (".xlsx", False): "table_or_sheet", (".jpg", False): "image",
        }
        for arguments, expected in cases.items():
            self.assertEqual(metadata.citation_mode(*arguments), expected)
            self.assertIn(expected, metadata.CITATION_MODES)

    def test_existing_verified_metadata_is_not_overwritten(self):
        text = "A very long English document " * 100
        language, _ = metadata.infer_language(text, "tr")
        year, _, _, _ = metadata.infer_year("no-year.pdf", "No year", text, "2018")
        doc_type, _, _ = metadata.infer_document_type("x.pdf", "x", text, "manual", ".pdf")
        authority, _, _, _ = metadata.infer_authority("x.pdf", "x", text, "A", doc_type)
        self.assertEqual((language, year, doc_type, authority), ("tr", "2018", "manual", "A"))

    def test_atomic_write_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "artifact.csv"
            self.assertTrue(metadata.atomic_write(path, b"same"))
            first_mtime = path.stat().st_mtime_ns
            self.assertFalse(metadata.atomic_write(path, b"same"))
            self.assertEqual(first_mtime, path.stat().st_mtime_ns)


class MetadataRealCorpusIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.real_root = Path(__file__).resolve().parents[1]
        cls.master_path = cls.real_root / "data/metadata/final_metadata_master.csv"
        cls.final_manifest_path = cls.real_root / "data/metadata/final_corpus_manifest.csv"

    def test_214_canonical_documents_have_214_unique_master_rows(self):
        if not self.master_path.exists():
            self.skipTest("Real generated metadata master not present in isolated unit-test copy")
        master = metadata.read_csv(self.master_path)
        final = metadata.read_csv(self.final_manifest_path)
        self.assertEqual(len(master), 214)
        self.assertEqual(len(final), 214)
        self.assertEqual(len({row["document_id"] for row in master}), 214)
        self.assertEqual({row["document_id"] for row in master}, {row["document_id"] for row in final})
        self.assertTrue(all(row["source_sha256"] for row in master))

    def test_master_vocabularies_and_current_values_are_preserved(self):
        if not self.master_path.exists():
            self.skipTest("Real generated metadata master not present in isolated unit-test copy")
        master = metadata.read_csv(self.master_path)
        current = {row["document_id"]: row for row in metadata.read_csv(self.real_root / "data/metadata/markdown_metadata.csv")}
        for row in master:
            self.assertIn(row["language_suggested"], metadata.LANGUAGES)
            self.assertIn(row["authority_level_suggested"], metadata.AUTHORITY_LEVELS)
            self.assertIn(row["document_type_suggested"], metadata.DOCUMENT_TYPES)
            self.assertIn(row["citation_mode"], metadata.CITATION_MODES)
            self.assertTrue(set(filter(None, row["topics_suggested"].split("|"))).issubset(metadata.TOPICS))
            before = current[row["document_id"]]
            self.assertEqual(row["authority_level_current"], before["authority_level"])
            self.assertEqual(row["document_type_current"], before["document_type"])
            self.assertEqual(row["language_current"], before["language"])
            self.assertEqual(row["year_current"], before["year"])
            self.assertEqual(row["topics_current"], before["topics"])

    def test_human_review_queue_is_deterministic(self):
        if not self.master_path.exists():
            self.skipTest("Real generated metadata master not present in isolated unit-test copy")
        master1, queue1, _ = metadata.build_master(self.real_root)
        master2, queue2, _ = metadata.build_master(self.real_root)
        self.assertEqual(master1, master2)
        self.assertEqual(queue1, queue2)
        self.assertEqual(queue1, sorted(queue1, key=lambda row: (row["document_id"], row["field"])))
        self.assertTrue(all(row["review_status"] == "pending" for row in queue1))


if __name__ == "__main__":
    unittest.main()
