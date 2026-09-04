import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.tunnelbook_section_runner import RunnerError, assemble_book


class AssembleBookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

        (self.root / "config").mkdir(parents=True)
        (self.root / "data" / "book" / "final").mkdir(parents=True)

        self.final_dir = self.root / "data" / "book" / "final"

        (self.root / "config" / "book_sections.json").write_text(
            json.dumps(
                {
                    "CH-A-S01": {
                        "section_title": "First",
                        "search_queries": ["q"],
                    },
                    "CH-A-S02": {
                        "section_title": "Second",
                        "search_queries": ["q"],
                    },
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def _write_frozen_section(self, slug, section_id, title, body):
        draft_path = self.final_dir / f"{slug}.md"
        draft_path.write_text(f"# {title}\n\n{body}\n", encoding="utf-8")

        manifest_path = self.final_dir / f"{slug}_freeze_manifest.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "section_id": section_id,
                    "section_title": title,
                    "status": "FROZEN",
                    "draft_path": str(draft_path),
                    "draft_sha256": "deadbeef",
                    "audit_identity": "id-" + slug,
                    "evidence_contract_version": "SENTENCE_ID_V2",
                    "editorial_policy_version": "DETERMINISTIC_EDITORIAL_GATE_V1",
                    "model_id": "test-model",
                    "frozen_at": "2026-01-01T00:00:00+00:00",
                }
            ),
            encoding="utf-8",
        )

    def test_assembles_book_from_frozen_sections(self):
        self._write_frozen_section("ch_a_s01", "CH-A-S01", "First", "Body one.")
        self._write_frozen_section("ch_a_s02", "CH-A-S02", "Second", "Body two.")

        with mock.patch(
            "scripts.tunnelbook_section_runner.ROOT", self.root
        ), mock.patch(
            "scripts.tunnelbook_section_runner.FINAL_DIR", self.final_dir
        ):
            assemble_book()

        book_md = (self.final_dir / "book.md").read_text(encoding="utf-8")
        self.assertIn("Body one.", book_md)
        self.assertIn("Body two.", book_md)
        self.assertLess(book_md.index("Body one."), book_md.index("Body two."))

        manifest = json.loads(
            (self.final_dir / "book_manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["section_count"], 2)
        self.assertEqual(
            [s["section_id"] for s in manifest["sections"]],
            ["CH-A-S01", "CH-A-S02"],
        )

    def test_fails_closed_when_section_not_frozen(self):
        self._write_frozen_section("ch_a_s01", "CH-A-S01", "First", "Body one.")
        # CH-A-S02 has no manifest at all -> not frozen.

        with mock.patch(
            "scripts.tunnelbook_section_runner.ROOT", self.root
        ), mock.patch(
            "scripts.tunnelbook_section_runner.FINAL_DIR", self.final_dir
        ):
            with self.assertRaises(RunnerError):
                assemble_book()

        self.assertFalse((self.final_dir / "book.md").exists())


if __name__ == "__main__":
    unittest.main()
