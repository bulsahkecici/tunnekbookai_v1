from __future__ import annotations

import unittest

from _loader import load_script
from utils import extension_priority, normalize_title


duplicates = load_script("02_duplicates.py", "duplicates_script")


def row(doc_id, name, extension, sha=""):
    return {
        "document_id": doc_id, "file_name": name, "relative_path": name,
        "extension": extension, "size_bytes": "10", "sha256": sha,
    }


class DuplicateTests(unittest.TestCase):
    def test_copy_suffixes_and_turkish_normalization(self):
        expected = "tunel egitim kitabi"
        for name in ("Tünel Eğitim Kitabı (1).pdf", "Tünel_Eğitim-Kitabı copy.pdf", "Tünel Eğitim Kitabı kopya 2.docx"):
            self.assertEqual(normalize_title(name), expected)

    def test_exact_duplicate_selects_clean_canonical(self):
        rows = [row("DOC1", "Belge (1).pdf", ".pdf", "same"), row("DOC2", "Belge.pdf", ".pdf", "same")]
        result = duplicates.find_exact_duplicates(rows)
        canonical = next(item for item in result if item["canonical_candidate"])
        self.assertEqual(canonical["document_id"], "DOC2")

    def test_logical_duplicate_prefers_docx_over_pdf(self):
        rows = [row("DOC1", "Tez.pdf", ".pdf"), row("DOC2", "Tez.docx", ".docx")]
        result = duplicates.find_logical_duplicates(rows)
        self.assertEqual(len(result), 2)
        preferred = next(item for item in result if item["preferred_source"])
        self.assertEqual(preferred["extension"], ".docx")

    def test_same_extension_is_not_logical_duplicate(self):
        rows = [row("DOC1", "Belge.pdf", ".pdf"), row("DOC2", "Belge (1).pdf", ".pdf")]
        self.assertEqual(duplicates.find_logical_duplicates(rows), [])

    def test_extension_priority(self):
        self.assertGreater(extension_priority(".docx"), extension_priority(".pdf"))
        self.assertGreater(extension_priority(".pptx"), extension_priority(".ppt"))
        self.assertGreater(extension_priority(".xlsx"), extension_priority(".xls"))


if __name__ == "__main__":
    unittest.main()

