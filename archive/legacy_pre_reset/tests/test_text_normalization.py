from __future__ import annotations

import csv
import importlib.util
import json
import tempfile
import unittest
import unicodedata
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    spec = importlib.util.spec_from_file_location("text_normalization", ROOT / "scripts/10_text_normalization.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


normalizer = load_module()


def load_gates():
    spec = importlib.util.spec_from_file_location("text_normalization_gates", ROOT / "scripts/10_text_normalization_gates.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


gates = load_gates()


class TextNormalizationRuleTests(unittest.TestCase):
    def normalize(self, text: str):
        return normalizer.normalize_body(text)

    def test_unicode_nfc_preserves_turkish_and_engineering_symbols(self):
        source = "Tu\u0308rkiye ölçüm: µ μ ² ³ ° ± ≤ ≥ Ø Φ σ τ α β γ\n"
        result, counts, _ = self.normalize(source)
        self.assertEqual(result, unicodedata.normalize("NFC", source))
        self.assertEqual(counts["unicode"], 1)

    def test_conservative_ocr_spacing_dictionary(self):
        result, counts, _ = self.normalize("TÜRK İ YE ve JEOLOJ İ K; TB M ve Q SİSTEMİ\n")
        self.assertEqual(result, "TÜRKİYE ve JEOLOJİK; TB M ve Q SİSTEMİ\n")
        self.assertEqual(counts["ocr_spacing"], 2)

    def test_code_inline_code_and_tables_are_unchanged(self):
        source = "```python\nx  =  1\n```\n| A  B | C |\nMetin  `x  =  1; TÜRK İ YE; �`  sonu\n"
        result, counts, _ = self.normalize(source)
        self.assertIn("```python\nx  =  1\n```", result)
        self.assertIn("| A  B | C |", result)
        self.assertIn("`x  =  1; TÜRK İ YE; �`", result)
        self.assertEqual(counts["unicode"], 0)
        self.assertEqual(counts["ocr_spacing"], 0)
        self.assertEqual(counts["replacement"], 0)

    def test_single_and_multiline_comments_are_byte_preserved(self):
        source = "Önce  <!-- citation_rule:  A  B -->\n<!-- original_page_start: 1\n  exact  spacing\noriginal_page_end -->\nSonra\n"
        result, _, _ = self.normalize(source)
        self.assertEqual(normalizer.COMMENT_RE.findall(source), normalizer.COMMENT_RE.findall(result))

    def test_safe_hyphenation_and_line_wrap(self):
        source = ("Bu oldukça uzun bir jeoteknik açıklama ve devam eden jeo-\n"
                  "teknik değerlendirme metnidir.\n"
                  "EN-1997 ve Q-System ile 10-20 ve -5 değerleri korunur.\n")
        result, counts, _ = self.normalize(source)
        self.assertIn("jeoteknik", result)
        self.assertIn("EN-1997", result)
        self.assertIn("Q-System", result)
        self.assertIn("10-20", result)
        self.assertIn("-5", result)
        self.assertEqual(counts["hyphenation"], 1)

    def test_replacement_character_is_visible_and_flaggable(self):
        result, counts, _ = self.normalize("bozuk � karakter\n")
        self.assertEqual(result, "bozuk [UNRESOLVED_CHAR] karakter\n")
        self.assertEqual(counts["replacement"], 1)

    def test_only_declared_mojibake_is_repaired(self):
        result, counts, _ = self.normalize("TÃ¼nel ÅŸaft ve bilinmeyen Ãx\n")
        self.assertEqual(result, "Tünel şaft ve bilinmeyen Ãx\n")
        self.assertEqual(counts["encoding"], 2)

    def test_formula_and_image_placeholders_are_preserved(self):
        source = "<!-- formula-not-decoded -->\n<!-- image -->\n[image placeholder]\n"
        result, counts, _ = self.normalize(source)
        self.assertEqual(result, source)
        self.assertEqual(counts["placeholder"], 3)

    def test_numeric_and_protected_token_audits(self):
        source = "ISO 9001 DOI: 10.1234/abc ISBN 978-1-2 https://x.test/a 25 MPa\n"
        self.assertEqual(normalizer.audit_safety(source, source, "", ""), [])
        changed = source.replace("25 MPa", "26 MPa").replace("ISO 9001", "ISO 9002")
        reasons = normalizer.audit_safety(source, changed, "", "")
        self.assertIn("numeric_token_mismatch", reasons)
        self.assertIn("url_doi_isbn_standard_token_mismatch", reasons)

    def test_table_pipe_audit_detects_change(self):
        reasons = normalizer.audit_safety("| A | B |\n", "| A | B | C |\n", "", "")
        self.assertIn("markdown_table_changed", reasons)

    def test_repeated_header_is_flagged_but_not_removed(self):
        source = "\n".join(["Page 1 / 8"] * 6) + "\n"
        result, _, candidates = self.normalize(source)
        self.assertEqual(result, source)
        self.assertEqual(candidates, ["Page 1 / 8"])

    def test_front_matter_and_document_identity_preserved_by_process(self):
        front = "---\ndocument_id: DOC000001\nsource_relative_path: books/sample.pdf\ntitle: TÜNEL  A\n---\n"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root = root / "source"
            target_root = root / "target"
            source_root.mkdir()
            source = source_root / "DOC000001.md"
            source.write_bytes((front + "TÜRK İ YE  metni\n").encode("utf-8"))
            row = normalizer.process(source, source_root, target_root, {})
            output = (target_root / source.name).read_text(encoding="utf-8")
            output_front, _ = normalizer.split_front_matter(output)
            self.assertEqual(output_front.encode("utf-8"), front.encode("utf-8"))
            self.assertEqual(row["document_id"], "DOC000001")
            self.assertEqual(row["source_relative_path"], "books/sample.pdf")

    def test_manifest_schema_and_serialization_are_deterministic(self):
        row = {field: "" for field in normalizer.MANIFEST_FIELDS}
        first = normalizer.csv_bytes([row])
        second = normalizer.csv_bytes([row])
        self.assertEqual(first, second)
        reader = csv.DictReader(first.decode("utf-8-sig").splitlines())
        self.assertEqual(reader.fieldnames, normalizer.MANIFEST_FIELDS)

    def test_actual_final_corpus_has_214_unique_document_ids(self):
        paths = sorted((ROOT / "data/corpus_final").rglob("*.md"))
        ids = []
        for path in paths:
            front, _ = normalizer.split_front_matter(path.read_text(encoding="utf-8-sig"))
            ids.append(normalizer.document_id(front))
        self.assertEqual(len(paths), 214)
        self.assertEqual(len(set(ids)), 214)

    def test_actual_normalized_corpus_and_manifest_are_complete(self):
        sources = sorted((ROOT / "data/corpus_final").rglob("*.md"))
        targets = sorted((ROOT / "data/corpus_normalized").rglob("*.md"))
        with (ROOT / "data/metadata/text_normalization_manifest.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(sources), 214)
        self.assertEqual(len(targets), 214)
        self.assertEqual(len(rows), 214)
        self.assertEqual(len({row["document_id"] for row in rows}), 214)
        self.assertFalse(any(row["normalization_status"] == "failed" for row in rows))

    def test_actual_manifest_hashes_and_paths_match_files(self):
        with (ROOT / "data/metadata/text_normalization_manifest.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            with self.subTest(document_id=row["document_id"]):
                source = ROOT / row["source_final_markdown"]
                target = ROOT / row["normalized_markdown"]
                self.assertTrue(source.is_file())
                self.assertTrue(target.is_file())
                self.assertEqual(normalizer.sha256(source.read_bytes()), row["source_sha256"])
                self.assertEqual(normalizer.sha256(target.read_bytes()), row["normalized_sha256"])

    def test_actual_frontmatter_comments_tables_and_tokens_are_preserved(self):
        source_root = ROOT / "data/corpus_final"
        target_root = ROOT / "data/corpus_normalized"
        for source in source_root.rglob("*.md"):
            relative = source.relative_to(source_root)
            target = target_root / relative
            original = source.read_text(encoding="utf-8-sig")
            normalized = target.read_text(encoding="utf-8-sig")
            source_front, _ = normalizer.split_front_matter(original)
            target_front, _ = normalizer.split_front_matter(normalized)
            with self.subTest(path=relative.as_posix()):
                self.assertEqual(source_front, target_front)
                self.assertEqual(normalizer.COMMENT_RE.findall(original), normalizer.COMMENT_RE.findall(normalized))
                self.assertEqual(
                    [line for line in original.splitlines() if line.lstrip().startswith("|")],
                    [line for line in normalized.splitlines() if line.lstrip().startswith("|")],
                )
                self.assertEqual(normalizer.token_counter(normalizer.NUMERIC_RE, original),
                                 normalizer.token_counter(normalizer.NUMERIC_RE, normalized))
                self.assertEqual(normalizer.token_counter(normalizer.PROTECTED_TOKEN_RE, original),
                                 normalizer.token_counter(normalizer.PROTECTED_TOKEN_RE, normalized))

    def test_full_run_is_idempotent(self):
        target_root = ROOT / "data/corpus_normalized"
        manifest = ROOT / "data/metadata/text_normalization_manifest.csv"
        audit = ROOT / "reports/text_normalization_audit.md"
        audit_before = audit.read_bytes() if audit.exists() else None
        before = (normalizer.directory_hash(target_root), normalizer.sha256(manifest.read_bytes()))
        try:
            summary = normalizer.run(ROOT, tests="idempotency test")
        finally:
            if audit_before is not None:
                normalizer.atomic_write(audit, audit_before)
        after = (normalizer.directory_hash(target_root), normalizer.sha256(manifest.read_bytes()))
        self.assertEqual(summary["decision"], "GO")
        self.assertEqual(before, after)

    def test_acronyms_codes_ranges_and_negative_values_are_preserved(self):
        source = "TBM NATM RMR Q-System EN 1997 ASTM D1586 T1-01 M20-25 10-20 mm -5 °C\n"
        result, _, _ = self.normalize(source)
        self.assertEqual(result, source)

    def test_decimals_percent_dimensions_and_units_are_preserved(self):
        source = "3.5 MPa; 3,5 m; %15; 1:100; 120 kN; 25 mm\n"
        result, _, _ = self.normalize(source)
        self.assertEqual(normalizer.token_counter(normalizer.NUMERIC_RE, source),
                         normalizer.token_counter(normalizer.NUMERIC_RE, result))
        for value in ("3.5 MPa", "3,5 m", "%15", "1:100", "120 kN", "25 mm"):
            self.assertIn(value, result)

    def test_url_doi_isbn_issn_regulation_and_standard_are_preserved(self):
        source = ("https://example.org/a DOI: 10.17226/13965 ISBN 978-0-309-09871-7 "
                  "ISSN 1234-5678 EN 1997-1 ASTM D1586 RG-16/7/2011-27996\n")
        result, _, _ = self.normalize(source)
        for pattern in (gates.URL_RE, gates.DOI_RE, gates.ISBN_RE, gates.ISSN_RE, gates.STANDARD_RE):
            self.assertEqual(gates.canonical_tokens(pattern, source), gates.canonical_tokens(pattern, result))

    def test_named_provenance_and_docling_comments_are_preserved(self):
        source = ("<!-- original_page_start: 3 -->\n<!-- citation_rule: page -->\n"
                  "<!-- Docling chunk 2 -->\nText\n<!-- original_page_end: 3 -->\n")
        result, _, _ = self.normalize(source)
        self.assertEqual(normalizer.COMMENT_RE.findall(result), normalizer.COMMENT_RE.findall(source))

    def test_real_section_heading_is_not_removed(self):
        source = "## 3. Jeoteknik Tasarım\nAçıklama  metni.\n"
        result, _, candidates = self.normalize(source)
        self.assertIn("## 3. Jeoteknik Tasarım", result)
        self.assertEqual(candidates, [])

    def test_actual_normalized_corpus_is_a_fixed_point(self):
        for path in (ROOT / "data/corpus_normalized").rglob("*.md"):
            first = path.read_bytes().decode("utf-8-sig")
            front, body = normalizer.split_front_matter(first)
            second_body, _, _ = normalizer.normalize_body(body)
            with self.subTest(path=path.name):
                self.assertEqual(front + second_body, first)

    def test_stratified_pilot_output_agrees_with_the_full_run(self):
        """The stratified pilot is a 15-document subset that the full run reproduces exactly.

        This replaces an assertion against `reports/text_normalization_dry_run.md` and
        `reports/text_normalization_pilot_audit.md`. Those were migration-era progress
        reports and were never carried into this repository; requiring them tested for the
        presence of a document, not for a property of the corpus. The invariant they were
        standing in for -- the pilot selected 15 documents and the later full run introduced
        no divergence from them -- is asserted here against the actual files.
        """
        pilot_root = ROOT / "data/corpus_normalized_pilot"
        full_root = ROOT / "data/corpus_normalized"
        pilot = sorted(pilot_root.rglob("*.md"))
        self.assertEqual(len(pilot), 15)
        with (ROOT / "data/metadata/text_normalization_manifest.csv").open(encoding="utf-8-sig", newline="") as handle:
            statuses = {row["document_id"]: row["normalization_status"] for row in csv.DictReader(handle)}
        for path in pilot:
            relative = path.relative_to(pilot_root)
            full = full_root / relative
            with self.subTest(path=relative.as_posix()):
                self.assertTrue(full.is_file(), "pilot document missing from the full run")
                self.assertEqual(path.read_bytes(), full.read_bytes(), "pilot output diverged from the full run")
                front, _ = normalizer.split_front_matter(path.read_text(encoding="utf-8-sig"))
                identifier = normalizer.document_id(front)
                self.assertIn(identifier, statuses)
                self.assertNotEqual(statuses[identifier], "failed")

    def test_change_log_has_only_real_compact_changes(self):
        path = ROOT / "data/metadata/text_normalization_changes.jsonl"
        changes = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        required = {"document_id", "source_relative_path", "rule", "before", "after", "context", "confidence"}
        self.assertTrue(changes)
        self.assertTrue(all(required <= row.keys() for row in changes))
        self.assertTrue(all(row["before"] != row["after"] for row in changes))
        self.assertTrue(all(len(row["before"]) <= 180 and len(row["after"]) <= 180 for row in changes))
        identities = [(row["document_id"], row["rule"], row["before"], row["after"]) for row in changes]
        self.assertEqual(len(identities), len(set(identities)))

    def test_review_queue_has_no_p0_and_no_document_is_corrupted(self):
        """No document carries a corruption reason, and the review queue has no P0.

        The corruption half of this test used to grep `reports/text_normalization_audit.md`
        for lines such as `- numeric mismatch: **0**`. The audit generator no longer emits
        per-corruption-class counters, so that assertion tested the report's wording rather
        than the corpus. The reasons are read straight out of the manifest instead, which is
        what `audit_safety` actually writes and is strictly stronger than the string match.
        """
        with (ROOT / "data/metadata/text_normalization_review_queue.csv").open(encoding="utf-8-sig", newline="") as handle:
            queue = list(csv.DictReader(handle))
        self.assertEqual(len(queue), 29)
        self.assertFalse(any(row["priority"] == "P0" for row in queue))

        with (ROOT / "data/metadata/text_normalization_manifest.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 214)
        corrupting = {"front_matter_changed", "citation_or_provenance_comment_changed",
                      "numeric_token_mismatch", "url_doi_isbn_standard_token_mismatch",
                      "markdown_table_changed", "engineering_symbol_changed"}
        offenders = []
        for row in rows:
            reasons = [item.strip() for item in row["review_reason"].split(";") if item.strip()]
            if any(reason.split(":")[0] in corrupting for reason in reasons):
                offenders.append((row["document_id"], row["review_reason"]))
        self.assertEqual(offenders, [], f"corrupting normalization reasons recorded: {offenders}")
        self.assertFalse([row for row in rows if row["normalization_status"] in {"manual_review_required", "failed"}])

        # the audit report must still exist and still record the GO decision
        audit = (ROOT / "reports/text_normalization_audit.md").read_text(encoding="utf-8")
        self.assertIn("- Karar: **GO**", audit)
        self.assertIn("- manual_review_required: **0**", audit)
        self.assertIn("- failed: **0**", audit)


if __name__ == "__main__":
    unittest.main()
