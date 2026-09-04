from __future__ import annotations

import unittest

from _loader import load_script
from utils import strip_front_matter


metadata = load_script("04_metadata.py", "metadata_script")


class MetadataTests(unittest.TestCase):
    def test_yaml_front_matter_generation(self):
        payload = {
            "document_id": "DOC000001", "title": "KGM Teknik Şartnamesi",
            "organization": None, "topics": ["geology", "NATM"], "preferred_variant": True,
        }
        rendered = metadata.render_front_matter(payload)
        self.assertTrue(rendered.startswith("---\n"))
        self.assertIn('title: "KGM Teknik Şartnamesi"', rendered)
        self.assertIn("organization: null", rendered)
        self.assertIn('topics: ["geology", "NATM"]', rendered)

    def test_front_matter_is_replaceable_not_duplicated(self):
        first = metadata.render_front_matter({"title": "İlk"}) + "# Body\n"
        second = metadata.render_front_matter({"title": "İkinci"}) + strip_front_matter(first)
        self.assertEqual(second.count("---\n"), 2)
        self.assertNotIn("İlk", second)

    def test_conservative_rules(self):
        inferred = metadata.infer_metadata("KGM Teknik Şartnamesi.pdf", "# KGM Teknik Şartnamesi\n\n## NATM ve kaya bulonu")
        self.assertEqual(inferred["authority_level"], "A")
        self.assertEqual(inferred["document_type"], "technical_specification")
        self.assertIn("NATM", inferred["topics"])
        self.assertIn("rock_bolt", inferred["topics"])

    def test_unknown_when_evidence_is_insufficient(self):
        inferred = metadata.infer_metadata("Belge.pdf", "# Belge")
        self.assertEqual(inferred["document_type"], "unknown")
        self.assertIsNone(inferred["authority_level"])
        self.assertEqual(inferred["topics"], [])

    def test_turkish_uppercase_i_is_normalized_for_authority(self):
        inferred = metadata.infer_metadata("2015 RESMİ GAZETE Yönetmelik.pdf", "# Tünel İşletme Yönetmeliği")
        self.assertEqual(inferred["authority_level"], "A")
        self.assertEqual(inferred["document_type"], "regulation")


if __name__ == "__main__":
    unittest.main()
