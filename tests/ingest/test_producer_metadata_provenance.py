"""Crawler bibliographic metadata must survive into metadata.json (real-data pilot defect D1).

Found by TUNNELBOOKAI_REALDATA_PILOT_001. `enrich.build_metadata` prefers a crawler-manifest
title over a body-heading heuristic, which is correct -- but `cli._merge_provenance` wrote only
`{"kind": ..., **item.provenance}` into provenance.json and dropped `item.crawler_record`
entirely. The crawler branch could therefore never fire, and every EXTERNAL_DISCOVERY document
silently fell back to `_first_heading`.

On the pilot's real journal PDF that produced `title = "Kocaeli University"` -- the journal
masthead on page 1 -- asserted at high confidence with `inferred: false`, while the manifest
carried the real title, both authors and the year. A generic institutional title is also a
false-merge hazard: every paper from that university normalizes to the same dedup key.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from tunnelbookai.ingest.cli import _merge_provenance
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.metadata import enrich
from tunnelbookai.ingest.sources import DiscoveredInput

# the real manifest record and the real page-1 element order from the pilot document
CRAWLER_RECORD = {
    "document_id": "PC_B8667B0178E8102A",
    "canonical_id": "CAN_32BD60929F57FD86CB07",
    "title": "Engineering Geological Investigation of the Kırık Tunnel Route",
    "authors": ["Özgür Fatih ÇÜMEN", "Ahmet Karakaş"],
    "year": "2021",
    "doi": "10.34088/kojose.904895",
    "resolved_url": "https://dergipark.org.tr/en/download/article-file/1668583",
}
# the real page-1 heading order: the journal masthead comes before the article title
MASTHEAD_ELEMENTS = [
    {"text": "Kocaeli University", "type": "heading", "level": 1},
    {"text": "Kocaeli Journal of Science and Engineering", "type": "heading", "level": 1},
    {"text": "http://dergipark.org.tr/kojose", "type": "paragraph"},
    {"text": "Engineering Geological Investigation of the Kırık Tunnel Route",
     "type": "heading", "level": 1},
]
ARCHIVE_META = {
    "document_id": "ING_b8667b0178e8102a697e",
    "original_filename": "source.pdf",
    "original_sha256": "b" * 64,
    "mime_type": "application/pdf",
    "format": "PDF",
    "source_kind": "EXTERNAL_DISCOVERY",
}


class MergeProvenanceTests(unittest.TestCase):
    """The written provenance must carry the crawler record forward."""

    def merge(self, record):
        item = DiscoveredInput(
            input_path=Path("incoming/papercrawler/releases/R1/01_originals/X/source.pdf"),
            source_kind="EXTERNAL_DISCOVERY",
            provenance={"source_kind": "EXTERNAL_DISCOVERY", "producer": "paper-crawler-agent",
                        "release": "R1", "canonical_id": CRAWLER_RECORD["canonical_id"]},
            crawler_record=record,
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "provenance.json"
            _merge_provenance(path, item, ARCHIVE_META)
            return json.loads(path.read_text(encoding="utf-8"))

    def test_crawler_record_is_persisted(self):
        doc = self.merge(CRAWLER_RECORD)
        source = doc["sources"][0]
        self.assertEqual(source["kind"], "EXTERNAL_DISCOVERY")
        self.assertEqual(source.get("crawler_record", {}).get("title"), CRAWLER_RECORD["title"])
        self.assertEqual(source["crawler_record"]["authors"], CRAWLER_RECORD["authors"])

    def test_manual_source_gets_no_crawler_record_key(self):
        item = DiscoveredInput(
            input_path=Path("incoming/manual/inbox/x.pdf"),
            source_kind="MANUAL_INTERNAL",
            provenance={"source_kind": "MANUAL_INTERNAL", "inbox_relative_path": "x.pdf"},
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "provenance.json"
            _merge_provenance(path, item, {**ARCHIVE_META, "source_kind": "MANUAL_INTERNAL"})
            doc = json.loads(path.read_text(encoding="utf-8"))
        self.assertNotIn("crawler_record", doc["sources"][0])

    def test_merging_twice_does_not_duplicate_or_lose_the_record(self):
        item = DiscoveredInput(
            input_path=Path("a/source.pdf"), source_kind="EXTERNAL_DISCOVERY",
            provenance={"canonical_id": CRAWLER_RECORD["canonical_id"]},
            crawler_record=CRAWLER_RECORD)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "provenance.json"
            _merge_provenance(path, item, ARCHIVE_META)
            _merge_provenance(path, item, ARCHIVE_META)
            doc = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(len(doc["sources"]), 1)
        self.assertEqual(doc["sources"][0]["crawler_record"]["title"], CRAWLER_RECORD["title"])


    def test_remerge_backfills_a_record_written_by_an_older_engine(self):
        """A bundle written before the fix must gain the record on the next run."""
        stale = {"document_id": ARCHIVE_META["document_id"], "sources": [
            {"kind": "EXTERNAL_DISCOVERY", "producer": "paper-crawler-agent",
             "canonical_id": CRAWLER_RECORD["canonical_id"]}]}
        item = DiscoveredInput(
            input_path=Path("a/source.pdf"), source_kind="EXTERNAL_DISCOVERY",
            provenance={"producer": "paper-crawler-agent",
                        "canonical_id": CRAWLER_RECORD["canonical_id"]},
            crawler_record=CRAWLER_RECORD)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "provenance.json"
            path.write_text(json.dumps(stale), encoding="utf-8")
            _merge_provenance(path, item, ARCHIVE_META)
            doc = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(len(doc["sources"]), 1)
        self.assertEqual(doc["sources"][0]["crawler_record"]["title"], CRAWLER_RECORD["title"])

    def test_remerge_never_blanks_existing_provenance(self):
        rich = {"document_id": ARCHIVE_META["document_id"], "sources": [
            {"kind": "EXTERNAL_DISCOVERY", "canonical_id": CRAWLER_RECORD["canonical_id"],
             "release": "R1", "declared_sha256": "a" * 64}]}
        item = DiscoveredInput(
            input_path=Path("a/source.pdf"), source_kind="EXTERNAL_DISCOVERY",
            provenance={"canonical_id": CRAWLER_RECORD["canonical_id"], "release": None},
            crawler_record=CRAWLER_RECORD)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "provenance.json"
            path.write_text(json.dumps(rich), encoding="utf-8")
            _merge_provenance(path, item, ARCHIVE_META)
            doc = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(doc["sources"][0]["release"], "R1")
        self.assertEqual(doc["sources"][0]["declared_sha256"], "a" * 64)


class CrawlerTitleWinsOverMastheadTests(unittest.TestCase):
    """§19, §20 — the manifest title must beat a page-1 masthead heading."""

    @classmethod
    def setUpClass(cls):
        cls.config = load_config()

    def build(self, sources):
        extraction = SimpleNamespace(
            normalized_text_path=None, text_elements=MASTHEAD_ELEMENTS,
            capabilities={"text": True}, text_char_count=9000, format="PDF", adapter="pdf")
        with tempfile.TemporaryDirectory() as tmp:
            original = Path(tmp) / "source.pdf"
            original.write_bytes(b"%PDF-1.4\n")
            return enrich.build_metadata(
                document_id=ARCHIVE_META["document_id"], archive_meta=ARCHIVE_META,
                provenance_doc={"sources": sources}, extraction=extraction,
                config=self.config, original_path=original)

    def test_manifest_title_and_authors_win(self):
        metadata, log, _ = self.build([{
            "kind": "EXTERNAL_DISCOVERY", "producer": "paper-crawler-agent",
            "crawler_record": CRAWLER_RECORD,
        }])
        self.assertEqual(metadata["title"], CRAWLER_RECORD["title"])
        self.assertNotEqual(metadata["title"], "Kocaeli University")
        self.assertEqual(metadata["authors"], CRAWLER_RECORD["authors"])

    def test_manifest_year_becomes_the_document_date(self):
        """D2 -- the manifest carries `year`, not `published_date`; it must not be dropped."""
        metadata, _, _ = self.build([{
            "kind": "EXTERNAL_DISCOVERY", "crawler_record": CRAWLER_RECORD}])
        self.assertEqual(metadata["document_date"], "2021")

    def test_full_publication_date_still_wins_over_year(self):
        record = {**CRAWLER_RECORD, "published_date": "2021-06-30"}
        metadata, _, _ = self.build([{"kind": "EXTERNAL_DISCOVERY", "crawler_record": record}])
        self.assertEqual(metadata["document_date"], "2021-06-30")

    def test_without_the_record_the_masthead_leaks_in(self):
        """Documents the pre-fix behaviour so the regression stays visible."""
        metadata, _, _ = self.build([{
            "kind": "EXTERNAL_DISCOVERY", "producer": "paper-crawler-agent",
        }])
        self.assertEqual(metadata["title"], "Kocaeli University")


if __name__ == "__main__":
    unittest.main()
