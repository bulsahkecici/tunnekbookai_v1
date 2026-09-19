from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tunnelbookai.ingest.extraction import ExtractionResult, write_normalized
from tunnelbookai.ingest.glyph_repair import (
    Lexicon,
    build_lexicon,
    damage_stats,
    repair_extraction,
    repair_text,
    standalone_tokens,
)


def _lexicon(**words: int) -> Lexicon:
    lexicon = Lexicon()
    lexicon.update(words)
    return lexicon


class GlyphRepairTests(unittest.TestCase):
    def test_mid_final_and_initial_glyphs_are_attached_by_lexicon(self):
        lexicon = _lexicon(**{
            "kısalması": 40, "ve": 5000, "trafik": 300, "akıllı": 60, "şehir": 90, "için": 6000,
            "kazılar": 50, "çin": 96, "kazıları": 30, "teşkilat": 20, "izin": 405,
        })
        text = "k ı salmas ı ve trafik; Ak ı ll ı Ş ehir için; Kazılar İ çin; Te ş kilat ı m ı z ı n"
        repaired, joined = repair_text(text, lexicon)
        self.assertEqual(repaired, "kısalması ve trafik; Akıllı Şehir için; Kazılar İçin; Teşkilatımızın")
        self.assertEqual(joined, 10)

    def test_suffix_debris_needs_document_local_evidence(self):
        # ``ızın`` must not be vouched for by ``izin`` (dotted/dotless kept distinct), and short
        # fragments in the lexicon are accepted only when they stand alone in the document.
        lexicon = _lexicon(**{"teşkilat": 20, "izin": 405, "ım": 50})
        self.assertEqual(repair_text("Te ş kilat ı m ı z ı n", lexicon)[0], "Teşkilatımızın")
        self.assertEqual(standalone_tokens("ım ile yaz ı ld ı ; ım"), frozenset({"ım", "ile"}))

    def test_undamaged_text_is_untouched_and_newlines_survive(self):
        lexicon = _lexicon(tünel=100)
        self.assertEqual(repair_text("Tünel kazısı ve destek.", lexicon), ("Tünel kazısı ve destek.", 0))
        repaired, _ = repair_text("Ba ş lık\n\nParagraf ı burada", lexicon)
        self.assertIn("\n\n", repaired)
        self.assertFalse(damage_stats("Kısa metin ı burada")["damaged"])
        self.assertTrue(damage_stats(" ".join(["kelime ı"] * 20))["damaged"])

    def test_build_lexicon_skips_damaged_text_and_keeps_apostrophe_suffixes_attached(self):
        words = dict(build_lexicon(["KGM'nin tünelleri tünelleri", "damaged ı text ı " * 10], minimum_frequency=1))
        self.assertIn("tünelleri", words)
        self.assertNotIn("nin", words)
        self.assertNotIn("damaged", words)

    def test_repair_extraction_rewrites_normalized_files_and_reports(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "config").mkdir()
            (root / "config" / "turkish_lexicon.txt").write_text(
                "# test\n" + "\n".join(f"{word}\t{count}" for word, count in {"teknik": 100, "üniversitesi": 80, "tünel": 200, "kazısı": 40}.items()) + "\n",
                encoding="utf-8",
            )
            bundle = root / "processing" / "ING_test"
            bundle.mkdir(parents=True)
            damaged = " ".join(["TEKN İ K ÜN İ VERS İ TES İ tünel kaz ı s ı"] * 4)
            result = ExtractionResult(document_id="ING_test", format="PDF", adapter="pdf")
            result.text_elements = [{"element_id": "E1", "type": "heading", "text": "TEKN İ K ÜN İ VERS İ TES İ", "heading_path": []},
                                    {"element_id": "E2", "type": "paragraph", "text": "tünel kaz ı s ı", "heading_path": ["TEKN İ K ÜN İ VERS İ TES İ"]}]
            result.figures = [{"asset_id": "F1", "caption": "Şekil 1. Tünel kaz ı s ı"}]
            import os
            cwd = os.getcwd()
            os.chdir(root)
            try:
                write_normalized(bundle, result, markdown="# " + damaged, document_json={"elements": result.text_elements}, text=damaged)
                record = repair_extraction(result, bundle, root)
            finally:
                os.chdir(cwd)
            self.assertIsNotNone(record)
            self.assertEqual(record["isolated_glyphs_after"], 0)
            self.assertEqual(result.text_elements[0]["text"], "TEKNİK ÜNİVERSİTESİ")
            self.assertEqual(result.text_elements[1]["heading_path"], ["TEKNİK ÜNİVERSİTESİ"])
            self.assertEqual(result.figures[0]["caption"], "Şekil 1. Tünel kazısı")
            self.assertIn("TURKISH_GLYPH_SPACING_REPAIRED:", " ".join(result.warnings))
            self.assertIn("TEKNİK ÜNİVERSİTESİ tünel kazısı", (root / result.normalized_text_path).read_text(encoding="utf-8"))
            document = json.loads((root / result.normalized_json_path).read_text(encoding="utf-8"))
            self.assertEqual(document["elements"][0]["text"], "TEKNİK ÜNİVERSİTESİ")


if __name__ == "__main__":
    unittest.main()
