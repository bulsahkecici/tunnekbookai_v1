from __future__ import annotations

import csv
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/08_final_corpus.py"
SPEC = importlib.util.spec_from_file_location("final_corpus", SCRIPT)
final_corpus = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(final_corpus)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class FinalCorpusTests(unittest.TestCase):
    def test_unknown_and_unclassified_are_reported_as_metadata_missing(self):
        self.assertTrue(final_corpus.metadata_is_missing("unknown"))
        self.assertTrue(final_corpus.metadata_is_missing("UNCLASSIFIED"))
        self.assertFalse(final_corpus.metadata_is_missing("technical_report"))

    def test_markdown_paths_are_normalized_to_nfc_for_google_drive(self):
        relative = final_corpus.markdown_relative("K/T1 Tu\u0308neli KY.pdf").as_posix()
        self.assertEqual(relative, "K/T1 Tüneli KY.md")

    def fixture(self, root: Path) -> None:
        documents = [
            ("FULL", "A/full.pdf", "1" * 64),
            ("REJECT", "A/reject.pdf", "2" * 64),
            ("FAILED", "B/failed.pptx", "3" * 64),
            ("OTHER", "C/other.txt", "4" * 64),
        ]
        metadata = []
        conversion = []
        for document_id, source, sha in documents:
            relative = Path(source).with_suffix(".md")
            baseline = root / "data/markdown" / relative
            baseline.parent.mkdir(parents=True, exist_ok=True)
            baseline.write_bytes(f"---\ndocument_id: {document_id}\n---\n\n# Baseline {document_id}\n".encode())
            metadata.append({
                "document_id": document_id, "source_relative_path": source, "sha256": sha,
                "preferred_variant": "True", "conversion_engine": "baseline_converter",
                "authority_level": "", "document_type": "unknown", "language": "tr",
                "year": "", "topics": "",
            })
            conversion.append({
                "document_id": document_id, "source_sha256": sha, "status": "success",
                "converter": "baseline_converter",
            })
        conversion.append({
            "document_id": "DUPLICATE_EXCLUDED", "source_sha256": "1" * 64,
            "status": "skipped_exact_duplicate", "converter": "",
        })
        full = root / "data/markdown_full_docling/A/full.md"
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_bytes(b"---\ndocument_id: FULL\n---\n\n# Full Docling\n")
        sidecar = root / "data/temp/full_docling_chunks/FULL/0001.docling.json"
        sidecar.parent.mkdir(parents=True, exist_ok=True)
        sidecar.write_text('{"pages": []}', encoding="utf-8")
        quality = [
            {"document_id": "FULL", "source_sha256": "1" * 64, "baseline_converter": "base", "full_docling_status": "success", "quality_status": "passed", "recommended_variant": "full_docling"},
            {"document_id": "REJECT", "source_sha256": "2" * 64, "baseline_converter": "base", "full_docling_status": "quality_reject_use_baseline", "quality_status": "rejected", "recommended_variant": "baseline"},
            {"document_id": "FAILED", "source_sha256": "3" * 64, "baseline_converter": "base", "full_docling_status": "failed", "quality_status": "not_evaluated", "recommended_variant": "human_review"},
        ]
        chunks = [{
            "chunk_id": "FULL:p1-2", "document_id": "FULL", "status": "success",
            "output_chunk_json": "data/temp/full_docling_chunks/FULL/0001.docling.json",
            "original_page_start": "1", "original_page_end": "2", "page_map_json": '{"1": 1, "2": 2}',
        }]
        metadata_dir = root / "data/metadata"
        write_csv(metadata_dir / "markdown_metadata.csv", metadata)
        write_csv(metadata_dir / "conversion_manifest.csv", conversion)
        write_csv(metadata_dir / "full_docling_quality_manifest.csv", quality)
        write_csv(metadata_dir / "full_docling_chunk_manifest.csv", chunks)

    def test_assembly_selects_one_variant_preserves_bytes_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            baseline_before = final_corpus.tree_digest(root / "data/markdown")
            full_before = final_corpus.tree_digest(root / "data/markdown_full_docling")
            first = final_corpus.assemble(root)
            first_digest = final_corpus.artifact_digest(root)
            mtimes = {path: path.stat().st_mtime_ns for path in (root / "data/corpus_final").rglob("*.md")}
            second = final_corpus.assemble(root)

            self.assertTrue(first["go"])
            self.assertEqual((first["total"], first["full_docling"], first["baseline"]), (4, 1, 3))
            self.assertEqual(first_digest, final_corpus.artifact_digest(root))
            self.assertEqual(second["changed_outputs"], 0)
            self.assertEqual(mtimes, {path: path.stat().st_mtime_ns for path in (root / "data/corpus_final").rglob("*.md")})
            self.assertEqual(baseline_before, final_corpus.tree_digest(root / "data/markdown"))
            self.assertEqual(full_before, final_corpus.tree_digest(root / "data/markdown_full_docling"))
            self.assertEqual((root / "data/corpus_final/A/full.md").read_bytes(), (root / "data/markdown_full_docling/A/full.md").read_bytes())
            self.assertEqual((root / "data/corpus_final/A/reject.md").read_bytes(), (root / "data/markdown/A/reject.md").read_bytes())

            rows = final_corpus.read_csv(root / "data/metadata/final_corpus_manifest.csv")
            by_id = {row["document_id"]: row for row in rows}
            self.assertEqual(by_id["FULL"]["selected_variant"], "full_docling")
            self.assertEqual(by_id["FULL"]["original_page_provenance_available"], "true")
            self.assertTrue((root / by_id["FULL"]["citation_sidecar"]).is_file())
            self.assertEqual(by_id["FAILED"]["selection_reason"], "persistent_docling_failure_use_baseline")
            self.assertEqual(by_id["OTHER"]["selection_reason"], "canonical_baseline_not_full_docling_candidate")

    def test_duplicate_final_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            metadata_path = root / "data/metadata/markdown_metadata.csv"
            rows = final_corpus.read_csv(metadata_path)
            rows[-1]["source_relative_path"] = "A/full.docx"
            write_csv(metadata_path, rows)
            with self.assertRaisesRegex(final_corpus.FinalCorpusError, "Duplicate final path"):
                final_corpus.build_rows(root)

    def test_missing_selected_markdown_is_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            os.unlink(root / "data/markdown/B/failed.md")
            with self.assertRaisesRegex(final_corpus.FinalCorpusError, "bulunamadı"):
                final_corpus.assemble(root)
            self.assertFalse((root / "data/corpus_final").exists())


if __name__ == "__main__":
    unittest.main()
