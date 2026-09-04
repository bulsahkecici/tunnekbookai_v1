from __future__ import annotations

import unittest
import tempfile
import zipfile
from pathlib import Path

from _loader import load_script


conversion = load_script("03_convert.py", "conversion_recovery_script")


class RecoveryTests(unittest.TestCase):
    def test_rtf_uses_safe_libreoffice_modernization(self):
        self.assertEqual(conversion.LEGACY_MAP[".rtf"], ".docx")

    def test_images_have_local_conversion_route(self):
        for extension in (".jpg", ".jpeg", ".png"):
            self.assertIn(extension, conversion.MODERN_EXTENSIONS)

    def test_meaningful_text_rejects_title_only(self):
        self.assertFalse(conversion.meaningful_text("# Belge\n", "Belge"))
        self.assertTrue(conversion.meaningful_text("# Belge\n\nBu belge yeterli miktarda gerçek içerik taşır.", "Belge"))

    def test_misnamed_ooxml_is_detected_by_content(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "yanlis_uzanti.doc"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("[Content_Types].xml", "<Types/>")
                archive.writestr("word/document.xml", "<document/>")
            self.assertEqual(conversion.detected_ooxml_extension(path), ".docx")


if __name__ == "__main__":
    unittest.main()
