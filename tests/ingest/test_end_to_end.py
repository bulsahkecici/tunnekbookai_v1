"""Controlled end-to-end smoke (task §76, §77, §82, §83).

Runs the real CLI over an isolated project root containing ONLY synthetic fixtures — the
production corpus, canonical files and question bank are never touched. Covers:

  * six formats in one batch, originals preserved byte-for-byte
  * the PaperCrawler schema-2.0 handoff accepted and its provisional section preserved
    while the final section is computed independently (§76)
  * the same bytes arriving from BOTH the crawler and the manual inbox collapsing into one
    document with two provenance sources (§77)
  * chunks, chunk quality and the embedding-ready manifest produced (§83)
  * canonical promotion count = 0

Run:  PYTHONPATH=. .venv/bin/python -m unittest tests.ingest.test_end_to_end -v
"""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tunnelbookai.ingest.ids import sha256_file

FIX = Path(__file__).resolve().parent / "fixtures"
SMOKE_FORMATS = ["sample_rich.pdf", "sample.docx", "sample.pptx", "sample.xlsx",
                 "sample_text.png", "sample_photo.jpg"]


def _write_crawler_release(releases_root: Path, source: Path, *, canonical_id: str,
                           provisional_section: str) -> Path:
    release = releases_root / "RELEASE_2026_09_03"
    registry = release / "00_registry"
    originals = release / "01_originals" / "C_ACADEMIC" / "ARTICLES" / canonical_id
    registry.mkdir(parents=True, exist_ok=True)
    originals.mkdir(parents=True, exist_ok=True)
    target = originals / source.name
    target.write_bytes(source.read_bytes())
    registry.joinpath("handoff_contract.json").write_text(json.dumps({
        "schema_version": "2.0", "producer": "paper-crawler-agent", "consumer": "TunnelBookAI",
        "handoff_manifest": "00_registry/handoff_manifest.jsonl",
    }), encoding="utf-8")
    record = {
        "schema_version": "2.0", "document_id": "PC_E2E01", "canonical_id": canonical_id,
        "producer": "paper-crawler-agent", "source_kind": "EXTERNAL_DISCOVERY",
        "title": "Tunel Bakim Maliyet Raporu",
        "local_path": f"01_originals/C_ACADEMIC/ARTICLES/{canonical_id}/{source.name}",
        "sha256": sha256_file(target),
        "provisional_primary_section": provisional_section,
        "provisional_secondary_sections": [],
        "provisional_section_confidence": 0.91,
        "crawler_evidence_level": "LIGHT_PDF_TEXT",
        "final_primary_section": None, "final_section_status": "NOT_EVALUATED",
        "paper_crawler_status": "READY_FOR_HANDOFF", "tunnelbookai_status": "NOT_INGESTED",
        "provenance": {"source_url": "https://example.org/rapor.pdf",
                       "discovery_source": "crossref"},
    }
    registry.joinpath("handoff_manifest.jsonl").write_text(
        json.dumps(record) + "\n", encoding="utf-8")
    return release


class IsolatedRunMixin(unittest.TestCase):
    """Reroutes the ingest engine at an isolated project root for the duration of a run."""

    @classmethod
    def build_root(cls) -> Path:
        root = Path(tempfile.mkdtemp(prefix="tbai_e2e_"))
        real = Path(__file__).resolve().parents[2]
        for relative in ("config", "book/scope/normalized", "crawler/config", "scripts"):
            (root / relative).mkdir(parents=True, exist_ok=True)
        for name in ("ingest", "ocr", "vision", "metadata", "classification",
                     "quality_gate", "chunking"):
            shutil.copy2(real / "config" / f"{name}.yaml", root / "config" / f"{name}.yaml")
        shutil.copy2(real / "config" / "paths.json", root / "config" / "paths.json")
        shutil.copy2(real / "book/scope/normalized/book_scope.json",
                     root / "book/scope/normalized/book_scope.json")
        shutil.copy2(real / "crawler/config/taxonomy.yaml", root / "crawler/config/taxonomy.yaml")
        shutil.copy2(real / "scripts" / "utils.py", root / "scripts" / "utils.py")
        shutil.copy2(real / "scripts" / "09_metadata_enrichment.py",
                     root / "scripts" / "09_metadata_enrichment.py")
        shutil.copy2(real / "config" / "config.yaml", root / "config" / "config.yaml")
        for relative in ("incoming/manual/inbox", "incoming/crawler/releases",
                         "incoming/quarantine", "originals", "processing", "audit",
                         "corpus/staging", "corpus/canonical"):
            (root / relative).mkdir(parents=True, exist_ok=True)
        # a decoy legacy staging bundle: it must survive the run untouched (§33)
        legacy = root / "corpus" / "staging" / "CAN_LEGACY0001"
        legacy.mkdir(parents=True, exist_ok=True)
        (legacy / "source.md").write_text("# legacy bundle\n", encoding="utf-8")
        (root / "corpus" / "canonical" / "frozen.md").write_text("# frozen\n", encoding="utf-8")
        return root

    @contextlib.contextmanager
    def isolated(self, root: Path):
        """Point PATHS, the taxonomy cache and the config cache at `root`."""
        import tunnelbookai.ingest.paths as paths_module
        from tunnelbookai.ingest.classify import taxonomy as taxonomy_module
        from tunnelbookai.ingest.config import load_config
        from tunnelbookai.ingest.metadata import schema as schema_module

        original = paths_module.PATHS
        paths_module.PATHS = paths_module.IngestPaths(root=root)
        patched = paths_module.PATHS
        modules = [
            "tunnelbookai.ingest.cli", "tunnelbookai.ingest.pipeline",
            "tunnelbookai.ingest.staging", "tunnelbookai.ingest.original_archive",
            "tunnelbookai.ingest.config", "tunnelbookai.ingest.sources.manual_inbox",
            "tunnelbookai.ingest.sources.crawler_contract",
        ]
        import importlib
        saved = {}
        for name in modules:
            module = importlib.import_module(name)
            if hasattr(module, "PATHS"):
                saved[name] = module.PATHS
                module.PATHS = patched
        load_config.cache_clear()
        taxonomy_module.load_taxonomy.cache_clear()
        schema_module.legacy_vocabularies.cache_clear()
        original_project_root = paths_module.PROJECT_ROOT
        paths_module.PROJECT_ROOT = root
        try:
            yield patched
        finally:
            paths_module.PATHS = original
            paths_module.PROJECT_ROOT = original_project_root
            for name, value in saved.items():
                importlib.import_module(name).PATHS = value
            load_config.cache_clear()
            taxonomy_module.load_taxonomy.cache_clear()
            schema_module.legacy_vocabularies.cache_clear()

    def run_cli(self, argv: list[str]) -> tuple[int, str]:
        from tunnelbookai.ingest.cli import main

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = main(argv)
        return code, buffer.getvalue()


class ControlledSmokeTests(IsolatedRunMixin):
    """§82, §83 — six synthetic inputs through the whole engine."""

    @classmethod
    def setUpClass(cls):
        cls.root = cls.build_root()
        cls.checksums = {}
        for name in SMOKE_FORMATS:
            shutil.copy2(FIX / name, cls.root / "incoming" / "manual" / "inbox" / name)
            cls.checksums[name] = sha256_file(FIX / name)
        cls.canonical_digest_before = sha256_file(cls.root / "corpus" / "canonical" / "frozen.md")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root, ignore_errors=True)

    def setUp(self):
        if not hasattr(type(self), "_ran"):
            with self.isolated(self.root):
                code, output = self.run_cli(["--source", "manual", "--resume"])
            type(self)._ran = (code, output)
        self.code, self.output = type(self)._ran

    def _quality(self):
        return json.loads((self.root / "audit" / "unified_ingest_quality.json")
                          .read_text(encoding="utf-8"))

    def test_run_succeeds_over_six_inputs(self):
        self.assertEqual(self.code, 0)
        self.assertEqual(self._quality()["documents"], 6)

    def test_every_original_preserved_byte_for_byte(self):
        originals = list((self.root / "originals").iterdir())
        self.assertEqual(len(originals), 6)
        archived = {sha256_file(next(d.glob("source.*"))) for d in originals}
        self.assertEqual(archived, set(self.checksums.values()))
        # and the inbox copies are still there, unmodified
        for name, digest in self.checksums.items():
            self.assertEqual(
                sha256_file(self.root / "incoming" / "manual" / "inbox" / name), digest)

    def test_all_formats_recognized_and_normalized(self):
        formats = set()
        for bundle in (self.root / "processing").iterdir():
            payload = json.loads((bundle / "normalized" / "document.json")
                                 .read_text(encoding="utf-8"))
            formats.add(payload["format"])
            for name in ("document.md", "document.json", "document.txt"):
                self.assertTrue((bundle / "normalized" / name).is_file())
        self.assertEqual(formats, {"PDF", "DOCX", "PPTX", "XLSX", "PNG", "JPG"})

    def test_assets_extracted(self):
        totals = {"pages": 0, "figures": 0, "tables": 0, "sheets": 0}
        for bundle in (self.root / "processing").iterdir():
            report = json.loads((bundle / "extraction_report.json").read_text(encoding="utf-8"))
            totals["pages"] += len(report["pages"])
            totals["figures"] += len(report["figures"])
            totals["tables"] += len(report["tables"])
            totals["sheets"] += len(report["sheets"])
        self.assertGreaterEqual(totals["pages"], 2, "PDF page snapshots")
        self.assertGreaterEqual(totals["figures"], 3, "PDF + DOCX + PPTX + image figures")
        self.assertGreaterEqual(totals["tables"], 2, "PDF + DOCX tables")
        self.assertGreaterEqual(totals["sheets"], 3, "XLSX sheets")

    def test_ocr_ran_and_did_not_hallucinate(self):
        quality = self._quality()
        self.assertTrue(quality["environment"]["ocr_available"])
        self.assertIn("VISUAL_ONLY", quality["by_evidence_level"],
                      "the photograph must stay VISUAL_ONLY, with no invented text")

    def test_every_document_got_a_quality_decision(self):
        quality = self._quality()
        self.assertEqual(sum(quality["by_quality_decision"].values()), 6)
        self.assertNotIn("REJECT", quality["by_quality_decision"])

    def test_final_classification_produced_for_every_document(self):
        from tunnelbookai.ingest.classify.taxonomy import load_taxonomy

        with self.isolated(self.root):
            taxonomy = load_taxonomy()
            for bundle in (self.root / "processing").iterdir():
                payload = json.loads((bundle / "classification.json").read_text(encoding="utf-8"))
                self.assertIsNotNone(payload["final_primary_section"], bundle.name)
                self.assertIn(payload["final_primary_section"], taxonomy)
                self.assertEqual(payload["taxonomy_source"],
                                 "book/scope/normalized/book_scope.json")

    def test_chunks_and_chunk_quality_produced(self):
        quality = self._quality()
        self.assertGreater(quality["chunks_total"], 0)
        for bundle in (self.root / "processing").iterdir():
            manifest = bundle / "chunks" / "chunk_manifest.jsonl"
            report = bundle / "chunk_quality.json"
            self.assertTrue(report.is_file(), bundle.name)
            self.assertNotEqual(json.loads(report.read_text())["status"], "FAIL", bundle.name)
            if manifest.is_file():
                for line in manifest.read_text(encoding="utf-8").splitlines():
                    chunk = json.loads(line)
                    self.assertTrue(chunk["text"].strip())
                    self.assertTrue(chunk["provenance"]["original_sha256"])
                    self.assertTrue(chunk["chunk_policy_version"])

    def test_multimodal_chunk_types_present(self):
        by_type = self._quality()["chunks_by_type"]
        for chunk_type in ("TEXT_CHUNK", "TABLE_CHUNK", "FIGURE_CHUNK",
                           "SLIDE_CHUNK", "SHEET_CHUNK"):
            self.assertIn(chunk_type, by_type, by_type)

    def test_embedding_ready_manifest_written_without_vectors(self):
        path = self.root / "audit" / "embedding_ready_manifest.jsonl"
        self.assertTrue(path.is_file())
        rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertTrue(rows)
        for row in rows:
            self.assertIn("embedding_text", row)
            self.assertNotIn("embedding", row)
            self.assertNotIn("vector", row)
            self.assertIn("eligible", row)
        self.assertEqual(self._quality()["embeddings_computed"], 0)

    def test_staging_written_and_legacy_bundles_untouched(self):
        staged = list((self.root / "corpus" / "staging" / "v2").iterdir())
        self.assertTrue(staged)
        for bundle in staged:
            payload = json.loads((bundle / "bundle.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["quality_decision"], "GO")
            self.assertFalse(payload["canonical_promoted"])
            self.assertTrue(payload["chunks_authoritative_path"].startswith("processing/"))
        legacy = self.root / "corpus" / "staging" / "CAN_LEGACY0001" / "source.md"
        self.assertEqual(legacy.read_text(encoding="utf-8"), "# legacy bundle\n")

    def test_canonical_untouched_and_nothing_promoted(self):
        self.assertEqual(
            sha256_file(self.root / "corpus" / "canonical" / "frozen.md"),
            self.canonical_digest_before)
        self.assertEqual(len(list((self.root / "corpus" / "canonical").iterdir())), 1)
        self.assertEqual(self._quality()["canonical_promoted"], 0)

    def test_resume_is_idempotent(self):
        with self.isolated(self.root):
            code, output = self.run_cli(["--source", "manual", "--resume"])
        self.assertEqual(code, 0)
        self.assertEqual(len(list((self.root / "originals").iterdir())), 6)
        self.assertIn("Reused / already processed", output)

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = self.build_root()
            try:
                shutil.copy2(FIX / "sample.docx", root / "incoming/manual/inbox/sample.docx")
                with self.isolated(root):
                    code, output = self.run_cli(["--source", "manual", "--dry-run"])
                self.assertEqual(code, 0)
                self.assertIn("Nothing was processed", output)
                self.assertEqual(list((root / "originals").iterdir()), [])
                self.assertEqual(list((root / "processing").iterdir()), [])
                self.assertFalse((root / "corpus" / "staging" / "v2").exists())
                self.assertFalse((root / "audit" / "embedding_ready_manifest.jsonl").exists())
            finally:
                shutil.rmtree(root, ignore_errors=True)


class CrawlerAndDedupEndToEndTests(IsolatedRunMixin):
    """§76, §77 — the crawler contract end to end, and cross-source identity."""

    @classmethod
    def setUpClass(cls):
        cls.root = cls.build_root()
        source = FIX / "sample_rich.pdf"
        cls.sha = sha256_file(source)
        _write_crawler_release(cls.root / "incoming" / "crawler" / "releases", source,
                               canonical_id="CAN_E2E01", provisional_section="1.1")
        # the SAME bytes also land in the manual inbox, under a different name
        shutil.copy2(source, cls.root / "incoming" / "manual" / "inbox" / "elden_gelen.pdf")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root, ignore_errors=True)

    def setUp(self):
        if not hasattr(type(self), "_ran"):
            with self.isolated(self.root):
                type(self)._ran = self.run_cli(["--source", "all", "--resume"])
        self.code, self.output = type(self)._ran

    def test_run_succeeded(self):
        self.assertEqual(self.code, 0)

    def test_one_document_identity_two_provenance_sources(self):
        """§77 — the same content from two sources is ONE document, not two."""
        originals = list((self.root / "originals").iterdir())
        self.assertEqual(len(originals), 1, [d.name for d in originals])
        self.assertEqual(len(list((self.root / "processing").iterdir())), 1)

        registry = [json.loads(l) for l in
                    (self.root / "audit" / "source_registry.jsonl")
                    .read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertEqual(len(registry), 1)
        row = registry[0]
        self.assertEqual(row["sha256"], self.sha)
        self.assertEqual(sorted(row["source_kinds"]),
                         ["EXTERNAL_DISCOVERY", "MANUAL_INTERNAL"])
        self.assertGreaterEqual(row["provenance_source_count"], 2)
        self.assertNotIn("duplicate_of", row)

        provenance = json.loads(
            (next((self.root / "processing").iterdir()) / "provenance.json")
            .read_text(encoding="utf-8"))
        kinds = {source["kind"] for source in provenance["sources"]}
        self.assertEqual(kinds, {"EXTERNAL_DISCOVERY", "MANUAL_INTERNAL"})

    def test_crawler_provisional_preserved_and_final_computed_independently(self):
        """§76, §36 — the hint is recorded; the answer is recomputed from the document."""
        bundle = next((self.root / "processing").iterdir())
        classification = json.loads((bundle / "classification.json").read_text(encoding="utf-8"))
        self.assertEqual(classification["crawler_provisional_section"], "1.1")
        self.assertIsNotNone(classification["final_primary_section"])
        # the final section came from this engine's own evidence, not from the hint
        self.assertIn("heading_rules", classification["classification_methods"])
        self.assertIsInstance(classification["crawler_final_agreement"], bool)
        if classification["final_primary_section"] != "1.1":
            self.assertFalse(classification["crawler_final_agreement"])
            self.assertIn("CRAWLER_FINAL_SECTION_DISAGREEMENT", classification["warnings"])

    def test_original_matches_the_declared_sha256(self):
        archived = next(next((self.root / "originals").iterdir()).glob("source.*"))
        self.assertEqual(sha256_file(archived), self.sha)


if __name__ == "__main__":
    unittest.main()
