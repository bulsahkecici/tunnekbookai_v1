"""Phase B smoke tests for the Unified Ingest Engine.

Covers: format detection, stable ids, manual discovery, original archive immutability,
state machine persistence/resume, and the PaperCrawler schema-2.0 contract consumer
(valid accept, SHA mismatch reject, wrong producer reject, unsupported schema reject,
READY_FOR_HANDOFF-only, provisional section preserved).

Run:  PYTHONPATH=. .venv/bin/python -m unittest tests.ingest.test_ingest_smoke -v
"""

from __future__ import annotations

import json
import os
import stat
import tempfile
import unittest
from pathlib import Path

from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.format_registry import Format, detect, is_supported
from tunnelbookai.ingest.ids import document_id_for_file, sha256_file
from tunnelbookai.ingest.original_archive import ArchiveConflict, archive_original
from tunnelbookai.ingest.sources import papercrawler_contract, manual_inbox
from tunnelbookai.ingest.state import IngestState, State, rank

FIX = Path(__file__).resolve().parent / "fixtures"


class FormatRegistryTests(unittest.TestCase):
    def test_ooxml_sniff_beats_extension(self):
        # a .docx renamed to .pdf must still be detected DOCX
        with tempfile.TemporaryDirectory() as d:
            fake = Path(d) / "mislabelled.pdf"
            fake.write_bytes((FIX / "sample.docx").read_bytes())
            self.assertEqual(detect(fake).fmt, Format.DOCX)
            self.assertEqual(detect(fake).detected_by, "ooxml_magic")

    def test_pdf_sniff_beats_html_extension(self):
        with tempfile.TemporaryDirectory() as d:
            fake = Path(d) / "source_raw.html"
            fake.write_bytes((FIX / "sample.pdf").read_bytes())
            self.assertEqual(detect(fake).fmt, Format.PDF)
            self.assertEqual(detect(fake).detected_by, "pdf_magic")

    def test_known_extensions(self):
        self.assertEqual(detect(FIX / "sample.pdf").fmt, Format.PDF)
        self.assertEqual(detect(FIX / "sample_photo.jpg").fmt, Format.JPG)
        self.assertEqual(detect(FIX / "sample_text.txt").fmt, Format.TXT)

    def test_unsupported_not_silently_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            weird = Path(d) / "thing.xyz"
            weird.write_text("x")
            det = detect(weird)
            self.assertEqual(det.fmt, Format.UNKNOWN)
            self.assertFalse(is_supported(det, libreoffice_available=True))

    def test_legacy_needs_libreoffice(self):
        with tempfile.TemporaryDirectory() as d:
            legacy = Path(d) / "old.doc"
            legacy.write_bytes(b"\xd0\xcf\x11\xe0legacy")
            det = detect(legacy)
            self.assertTrue(det.is_legacy)
            self.assertFalse(is_supported(det, libreoffice_available=False))
            self.assertTrue(is_supported(det, libreoffice_available=True))


class IdTests(unittest.TestCase):
    def test_stable_and_sha_derived(self):
        a, sha_a = document_id_for_file(FIX / "sample.pdf")
        b, sha_b = document_id_for_file(FIX / "sample.pdf")
        self.assertEqual(a, b)
        self.assertEqual(sha_a, sha_b)
        self.assertTrue(a.startswith("ING_"))
        self.assertEqual(a, "ING_" + sha_a[:20])


class ManualDiscoveryTests(unittest.TestCase):
    def test_discovers_supported_ignores_readme(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "inbox").mkdir()
            (root / "README.md").write_text("ignore me")
            (root / "inbox" / "a.pdf").write_bytes((FIX / "sample.pdf").read_bytes())
            (root / "inbox" / ".gitkeep").write_text("")
            items = manual_inbox.discover(load_config(), manual_root=root)
            names = sorted(p.input_path.name for p in items)
            self.assertEqual(names, ["a.pdf"])
            self.assertEqual(items[0].source_kind, "MANUAL_INTERNAL")
            self.assertIn("dropped_at", items[0].provenance)


class OriginalArchiveTests(unittest.TestCase):
    def test_archive_is_immutable_and_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            originals = Path(d) / "originals"
            meta1 = archive_original(FIX / "sample.pdf", source_kind="MANUAL_INTERNAL",
                                     originals_root=originals)
            archived = originals / meta1["document_id"] / "source.pdf"
            self.assertTrue(archived.exists())
            self.assertEqual(sha256_file(archived), meta1["original_sha256"])
            # read-only
            self.assertFalse(bool(archived.stat().st_mode & stat.S_IWUSR))
            # idempotent
            meta2 = archive_original(FIX / "sample.pdf", source_kind="EXTERNAL_DISCOVERY",
                                     originals_root=originals)
            self.assertEqual(meta2["archive_mode"], "existing")
            self.assertEqual(sorted(meta2["source_kinds"]),
                             ["EXTERNAL_DISCOVERY", "MANUAL_INTERNAL"])

    def test_sha_conflict_raises(self):
        with tempfile.TemporaryDirectory() as d:
            originals = Path(d) / "originals"
            meta = archive_original(FIX / "sample.pdf", source_kind="MANUAL_INTERNAL",
                                    originals_root=originals)
            archived = originals / meta["document_id"] / "source.pdf"
            os.chmod(archived, 0o644)
            archived.write_bytes(b"tampered")
            with self.assertRaises(ArchiveConflict):
                archive_original(FIX / "sample.pdf", source_kind="MANUAL_INTERNAL",
                                 originals_root=originals)


class StateMachineTests(unittest.TestCase):
    def test_persist_and_resume(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ingest_state.jsonl"
            s = IngestState(p)
            s.transition("ING_x", State.ORIGINAL_ARCHIVED, source_kind="MANUAL_INTERNAL", sha256="a")
            s.transition("ING_x", State.EXTRACTED)
            reloaded = IngestState(p)
            self.assertEqual(reloaded.state_of("ING_x"), State.EXTRACTED)
            self.assertGreater(rank(State.EXTRACTED), rank(State.ORIGINAL_ARCHIVED))
            self.assertEqual(len(reloaded.get("ING_x")["history"]), 2)

    def test_terminal_detection(self):
        # Since Phase J, STAGED is no longer terminal — chunking continues past it (§65),
        # so a staged-but-unchunked document is still resumable.
        with tempfile.TemporaryDirectory() as d:
            s = IngestState(Path(d) / "s.jsonl")
            s.transition("ING_y", State.STAGED)
            self.assertFalse(s.is_terminal("ING_y"))
            s.transition("ING_y", State.EMBEDDING_READY)
            self.assertTrue(s.is_terminal("ING_y"))
            s.transition("ING_z", State.REJECTED)
            self.assertTrue(s.is_terminal("ING_z"))


def _write_papercrawler_release(root: Path, *, schema="2.0", producer="paper-crawler-agent",
                                corrupt_sha=False, status="READY_FOR_HANDOFF", deprecated=False) -> Path:
    rel = root / "RELEASE_2026_09_02"
    reg = rel / "00_registry"
    orig = rel / "01_originals" / "C_ACADEMIC" / "ARTICLES" / "PC_TEST01"
    reg.mkdir(parents=True)
    orig.mkdir(parents=True)
    src = orig / "source.pdf"
    src.write_bytes((FIX / "sample.pdf").read_bytes())
    sha = sha256_file(src)
    (reg / "handoff_contract.json").write_text(json.dumps({
        "schema_version": schema, "producer": producer, "consumer": "TunnelBookAI",
        "handoff_manifest": "00_registry/handoff_manifest.jsonl",
    }))
    record = {
        "schema_version": schema, "document_id": "PC_TEST01", "canonical_id": "CAN_TEST01",
        "producer": producer, "source_kind": "EXTERNAL_DISCOVERY", "title": "Synthetic",
        "local_path": "01_originals/C_ACADEMIC/ARTICLES/PC_TEST01/source.pdf",
        "sha256": ("0" * 64) if corrupt_sha else sha,
        "final_primary_section": None, "final_section_status": "NOT_EVALUATED",
        "paper_crawler_status": status, "tunnelbookai_status": "NOT_INGESTED",
        "provenance": {"source_url": "https://example.org/p", "discovery_source": "crossref"},
    }
    if deprecated:
        record.update({"provisional_primary_section": "5.5.2", "book_sections": [{"id": "5.4"}]})
    (reg / "handoff_manifest.jsonl").write_text(json.dumps(record) + "\n")
    return rel


class PaperCrawlerContractTests(unittest.TestCase):
    def test_clean_schema_2_package_is_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            releases = Path(d)
            _write_papercrawler_release(releases)
            res = papercrawler_contract.consume_release(releases / "RELEASE_2026_09_02")
            self.assertEqual(res.blockers, [])
            self.assertEqual(len(res.accepted), 1)
            self.assertEqual(res.accepted[0].notes, [])

    def test_deprecated_section_fields_are_accepted_but_not_mapped(self):
        with tempfile.TemporaryDirectory() as d:
            releases = Path(d)
            _write_papercrawler_release(releases, deprecated=True)
            res = papercrawler_contract.consume_release(releases / "RELEASE_2026_09_02")
            self.assertEqual(len(res.accepted), 1)
            self.assertIn("DEPRECATED_PRODUCER_SECTION_FIELD:provisional_primary_section", res.accepted[0].notes)
            self.assertNotIn("provisional_primary_section", res.accepted[0].provenance)
            self.assertNotIn("book_sections", res.accepted[0].provenance)

    def test_sha_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            _write_papercrawler_release(Path(d), corrupt_sha=True)
            res = papercrawler_contract.consume_release(Path(d) / "RELEASE_2026_09_02")
            self.assertEqual(res.accepted, [])
            self.assertEqual(res.skipped[0]["reason"], "sha256_mismatch")

    def test_wrong_producer_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            _write_papercrawler_release(Path(d), producer="evil-agent")
            res = papercrawler_contract.consume_release(Path(d) / "RELEASE_2026_09_02")
            self.assertTrue(any("wrong_producer" in b for b in res.blockers))

    def test_unsupported_schema_major_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            _write_papercrawler_release(Path(d), schema="3.0")
            res = papercrawler_contract.consume_release(Path(d) / "RELEASE_2026_09_02")
            self.assertTrue(any("unsupported_contract_schema" in b for b in res.blockers))

    def test_legacy_1x_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            _write_papercrawler_release(Path(d), schema="1.1")
            rel = Path(d) / "RELEASE_2026_09_02"
            self.assertTrue(papercrawler_contract.consume_release(rel).blockers)

    def test_not_ready_status_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            _write_papercrawler_release(Path(d), status="MANUAL_REVIEW")
            res = papercrawler_contract.consume_release(Path(d) / "RELEASE_2026_09_02")
            self.assertEqual(res.accepted, [])
            self.assertTrue(res.skipped[0]["reason"].startswith("status_"))


if __name__ == "__main__":
    unittest.main()
