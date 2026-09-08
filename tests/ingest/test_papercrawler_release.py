#!/usr/bin/env python3

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tunnelbookai.ingest import cli
from tunnelbookai.ingest.adapters import AdapterContext, get_adapter
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.format_registry import detect
from tunnelbookai.ingest.ids import sha256_file
from tunnelbookai.ingest.paths import IngestPaths
from tunnelbookai.ingest.sources import papercrawler_contract


def _write_legacy_release(root: Path, name: str = "RELEASE_A") -> tuple[Path, dict]:
    release = root / name
    registry = release / "00_registry"
    originals = release / "01_originals" / "WEB" / "PC_TEST"
    registry.mkdir(parents=True)
    originals.mkdir(parents=True)
    normalized = originals / "source.md"
    raw = originals / "source_raw.html"
    normalized.write_text("# provisional crawler text\n")
    raw.write_text("<html><body><h1>Authoritative</h1></body></html>")
    raw_sha = sha256_file(raw)
    (registry / "handoff_contract.json").write_text(json.dumps({
        "schema_version": "2.0", "producer": "paper-crawler-agent",
        "consumer": "TunnelBookAI", "handoff_manifest": "00_registry/handoff_manifest.jsonl",
    }))
    record = {
        "schema_version": "2.0", "document_id": "PC_TEST", "canonical_id": f"CAN_{name}",
        "local_path": str(normalized.relative_to(release)), "sha256": sha256_file(normalized),
        "source_representation": {
            "original_or_raw": str(raw.relative_to(release)),
            "original_or_raw_sha256": raw_sha,
            "crawler_normalized": str(normalized.relative_to(release)),
            "crawler_normalized_sha256": sha256_file(normalized),
            "crawler_normalized_status": "PROVISIONAL",
        },
        "paper_crawler_status": "READY_FOR_HANDOFF", "tunnelbookai_status": "NOT_INGESTED",
        "provenance": {"source_url": "https://example.org/source"},
    }
    (registry / "handoff_manifest.jsonl").write_text(json.dumps(record) + "\n")
    return release, record


class AuthoritativeSourceTests(unittest.TestCase):
    def test_original_or_raw_wins_over_legacy_local_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release, record = _write_legacy_release(Path(directory))
            result = papercrawler_contract.consume_release(release)
            self.assertEqual(result.blockers, [])
            self.assertEqual(result.accepted[0].input_path.name, "source_raw.html")
            selected = result.accepted[0].provenance["authoritative_source"]
            self.assertEqual(selected["selection"], "source_representation.original_or_raw")
            self.assertEqual(selected["sha256"], record["source_representation"]["original_or_raw_sha256"])

    def test_selected_raw_html_generates_fresh_canonical_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release, _ = _write_legacy_release(root)
            item = papercrawler_contract.consume_release(release).accepted[0]
            bundle = root / "processing" / "ING_HTML"
            context = AdapterContext(
                document_id="ING_HTML", original_path=item.input_path,
                original_filename=item.input_path.name, bundle=bundle,
                detection=detect(item.input_path), config=load_config(), root=root,
                do_ocr=False, do_vision=False,
            )
            result = get_adapter("text")(context)
            canonical = (bundle / "normalized" / "document.md").read_text()
            self.assertTrue(result.succeeded, result.errors)
            self.assertIn("Authoritative", canonical)
            self.assertNotIn("provisional crawler text", canonical)

    def test_raw_source_without_its_checksum_does_not_fall_back_to_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release, record = _write_legacy_release(Path(directory))
            record["source_representation"].pop("original_or_raw_sha256")
            (release / "00_registry" / "handoff_manifest.jsonl").write_text(json.dumps(record) + "\n")
            result = papercrawler_contract.consume_release(release)
            self.assertEqual(result.accepted, [])
            self.assertEqual(result.skipped[0]["reason"], "authoritative_sha256_missing")

    def test_path_traversal_and_symlink_escape_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release, record = _write_legacy_release(root)
            record["source_representation"]["original_or_raw"] = "../outside.html"
            (release / "00_registry" / "handoff_manifest.jsonl").write_text(json.dumps(record) + "\n")
            result = papercrawler_contract.consume_release(release)
            self.assertEqual(result.skipped[0]["reason"], "unsafe_authoritative_path")

            outside = root / "outside.html"
            outside.write_text("outside")
            link = release / "01_originals" / "escape.html"
            link.symlink_to(outside)
            record["source_representation"]["original_or_raw"] = str(link.relative_to(release))
            record["source_representation"]["original_or_raw_sha256"] = sha256_file(outside)
            (release / "00_registry" / "handoff_manifest.jsonl").write_text(json.dumps(record) + "\n")
            result = papercrawler_contract.consume_release(release)
            self.assertEqual(result.skipped[0]["reason"], "unsafe_authoritative_path")


class ReleaseFilterTests(unittest.TestCase):
    def test_partial_directories_are_hidden_and_release_filter_is_exact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            releases = Path(directory)
            _write_legacy_release(releases, "RELEASE_A")
            _write_legacy_release(releases, "RELEASE_B")
            partial, _ = _write_legacy_release(releases, "RELEASE_C.partial")
            self.assertTrue(partial.is_dir())
            found = papercrawler_contract.find_release_dirs(releases, release_id="RELEASE_B")
            self.assertEqual([path.name for path in found], ["RELEASE_B"])
            self.assertNotIn("RELEASE_C.partial", [path.name for path in papercrawler_contract.find_release_dirs(releases)])

    def test_cli_gather_discovers_only_selected_release(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            releases = root / "incoming" / "papercrawler" / "releases"
            _write_legacy_release(releases, "RELEASE_A")
            _write_legacy_release(releases, "RELEASE_B")
            isolated_paths = IngestPaths(root)
            with patch.object(papercrawler_contract, "PATHS", isolated_paths):
                inputs, skipped = cli._gather("papercrawler", release_id="RELEASE_B")
            self.assertEqual(skipped, [])
            self.assertEqual(len(inputs), 1)
            self.assertEqual(inputs[0].provenance["release"], "RELEASE_B")


if __name__ == "__main__":
    unittest.main()
