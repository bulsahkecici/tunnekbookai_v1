from __future__ import annotations

import csv
import importlib.util
import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    spec = importlib.util.spec_from_file_location("embedding_eligibility",
                                                  ROOT / "scripts/13_embedding_eligibility.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


eligibility = load_module()

FROZEN_BASELINE = {
    "data/chunks/chunks.jsonl": "e751fcfc3cc6828b05f75f494fd9a31b44388abda9daf83fb9581581ef79df5b",
    "data/chunks_pilot/chunks.jsonl": "3f79b5c2897e5cae04d9ee0e3fa2b4f06a9a94ad4016ec637676d39ad5b55aaa",
    "data/metadata/chunk_manifest.csv": "e5aed214a30d21ed5819e5b34e332acf3ffe266752dc1e9f1c552968e01af7a8",
    "data/metadata/chunk_review_queue.csv": "37377745a46c206afdf39fbf0e187439f40db21e03e85f1538689e24ef3e00e3",
    "data/metadata/bge_m3_tokenizer_audit.csv": "e2f954becd99223602108be6b9085c563d519f787c753e378037241f393aee14",
}

KNOWN_FAILURES = {"DOC000009": 5, "DOC000041": 8, "DOC000051": 45}

_CACHE: dict[str, object] = {}


def canonical_chunks():
    if "chunks" not in _CACHE:
        text = (ROOT / "data/chunks/chunks.jsonl").read_text(encoding="utf-8")
        _CACHE["chunks"] = [json.loads(line) for line in text.splitlines() if line.strip()]
    return _CACHE["chunks"]


def read_csv(relative: str):
    path = ROOT / relative
    if not path.is_file():
        return None
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class TestDetectors(unittest.TestCase):
    def test_glyph_slash_failure_detected(self):
        text = "".join(f"/G{index % 80 + 10}" for index in range(40))
        self.assertEqual(eligibility.classify(text)[0], "quarantined_extraction_failure")
        self.assertIn("glyph_index_sequence", eligibility.classify(text)[1])

    def test_glyph_concatenated_failure_detected(self):
        text = "".join(f"G{index % 80 + 10}" for index in range(40))
        self.assertEqual(eligibility.classify(text)[0], "quarantined_extraction_failure")

    def test_control_character_failure_detected(self):
        self.assertEqual(eligibility.classify("\x01\x02\x03" * 30)[0], "quarantined_extraction_failure")
        self.assertIn("control_character_residue", eligibility.classify("\x01\x02\x03" * 30)[1])

    def test_a_few_control_characters_do_not_quarantine(self):
        text = "This is a normal technical paragraph about tunnel ventilation systems.\x01\x02"
        self.assertNotEqual(eligibility.classify(text)[0], "quarantined_extraction_failure")

    def test_ordinary_text_mentioning_g_codes_not_quarantined(self):
        text = "The G20 summit and the G7 group discussed tunnel infrastructure funding at length."
        self.assertEqual(eligibility.classify(text)[0], "eligible")

    def test_legitimate_short_regulation_not_quarantined(self):
        text = "MADDE 3- (1) Bu Karar yayımı tarihinde yürürlüğe girer."
        status, _ = eligibility.classify(text)
        self.assertEqual(status, "eligible_low_content")
        self.assertNotEqual(status, "quarantined_extraction_failure")

    def test_table_with_few_words_not_quarantined(self):
        text = "| A | B |\n|---|---|\n| 12 | 34 |\n| 56 | 78 |"
        self.assertNotEqual(eligibility.classify(text)[0], "quarantined_extraction_failure")

    def test_normal_prose_is_eligible(self):
        text = "NATM support systems combine shotcrete and rock bolts to stabilise the excavated tunnel profile."
        self.assertEqual(eligibility.classify(text)[0], "eligible")

    def test_detector_reproduces_exactly_the_known_58_failures(self):
        quarantined = [chunk for chunk in canonical_chunks()
                       if eligibility.classify(str(chunk["text"]))[0] == "quarantined_extraction_failure"]
        self.assertEqual(len(quarantined), 58)
        self.assertEqual(dict(Counter(chunk["document_id"] for chunk in quarantined)), KNOWN_FAILURES)

    def test_no_extraction_failures_outside_known_documents(self):
        quarantined = [chunk for chunk in canonical_chunks()
                       if eligibility.classify(str(chunk["text"]))[0] == "quarantined_extraction_failure"]
        self.assertEqual([chunk["chunk_id"] for chunk in quarantined
                          if chunk["document_id"] not in eligibility.DAMAGED_DOCUMENTS], [])

    def test_classification_is_deterministic(self):
        sample = canonical_chunks()[:400]
        first = [eligibility.classify(str(chunk["text"])) for chunk in sample]
        second = [eligibility.classify(str(chunk["text"])) for chunk in sample]
        self.assertEqual(first, second)


class TestDecoders(unittest.TestCase):
    def test_glyph_decode_recovers_known_phrase(self):
        encoded = "G49G72G90G73G82G88G81G71G79G68G81G71"
        self.assertEqual(eligibility.decode_glyphs(encoded), "Newfoundland")

    def test_glyph_decode_handles_slash_form(self):
        encoded = "/G51/G68/G74/G72/G3/G20"
        self.assertEqual(eligibility.decode_glyphs(encoded), "Page 1")

    def test_glyph_decode_recovers_numbers(self):
        self.assertEqual(eligibility.decode_glyphs("G19G17G20"), "0.1")
        self.assertEqual(eligibility.decode_glyphs("/G28/G24"), "95")

    def test_utf16_pair_decode_recovers_turkish(self):
        encoded = "\x00G\x00Ü\x00V\x00E\x00N\x00L\x010\x00K"
        self.assertEqual(eligibility.decode_utf16_pairs(encoded), "GÜVENLİK")

    def test_decoders_are_deterministic(self):
        encoded = "G49G72G90G73G82G88G81G71G79G68G81G71"
        self.assertEqual(eligibility.decode_glyphs(encoded), eligibility.decode_glyphs(encoded))

    def test_decoding_leaves_clean_text_untouched(self):
        clean = "Ordinary tunnel engineering text with numbers 1234 and symbols."
        self.assertEqual(eligibility.decode_glyphs(clean), clean)
        self.assertEqual(eligibility.decode_utf16_pairs(clean), clean)

    def test_residual_glyph_detection(self):
        self.assertGreater(eligibility.residual_glyph_tokens("value /G28/G24 here"), 0)
        self.assertEqual(eligibility.residual_glyph_tokens("value 95 here"), 0)


class TestEligibilityManifest(unittest.TestCase):
    def rows(self):
        rows = read_csv("data/metadata/embedding_eligibility.csv")
        if rows is None:
            self.skipTest("eligibility manifest not generated yet")
        return rows

    def test_manifest_covers_every_canonical_chunk(self):
        rows = self.rows()
        self.assertEqual(len(rows), 6039)
        self.assertEqual([row["chunk_id"] for row in rows], [chunk["chunk_id"] for chunk in canonical_chunks()])

    def test_manifest_chunk_ids_unique(self):
        rows = self.rows()
        self.assertEqual(len({row["chunk_id"] for row in rows}), len(rows))

    def test_manifest_has_required_columns(self):
        required = {"chunk_id", "document_id", "bge_m3_token_count", "eligibility_status", "quality_reason",
                    "glyph_sequence_count", "control_character_count", "real_word_count", "contains_table",
                    "document_type", "provenance_status", "recovery_status", "replacement_chunk_id"}
        self.assertTrue(required.issubset(set(eligibility.ELIGIBILITY_FIELDS)))
        self.assertTrue(required.issubset(set(self.rows()[0].keys())))

    def test_every_chunk_has_a_valid_status(self):
        valid = {"eligible", "eligible_low_content", "quarantined_extraction_failure", "replacement_available"}
        self.assertTrue(all(row["eligibility_status"] in valid for row in self.rows()))

    def test_low_content_chunks_are_kept_not_quarantined(self):
        rows = self.rows()
        low = [row for row in rows if row["eligibility_status"] == "eligible_low_content"]
        self.assertGreater(len(low), 0)
        for row in low:
            self.assertNotEqual(row["eligibility_status"], "quarantined_extraction_failure")


class TestEmbeddingInput(unittest.TestCase):
    def rows(self):
        rows = read_csv("data/metadata/full_embedding_input_manifest.csv")
        if rows is None:
            self.skipTest("embedding input manifest not generated yet")
        return rows

    def eligibility_rows(self):
        rows = read_csv("data/metadata/embedding_eligibility.csv")
        if rows is None:
            self.skipTest("eligibility manifest not generated yet")
        return rows

    def test_no_quarantined_chunk_in_embedding_input(self):
        excluded = {row["chunk_id"] for row in self.eligibility_rows()
                    if row["eligibility_status"] in {"quarantined_extraction_failure", "replacement_available"}}
        present = {row["chunk_id"] for row in self.rows()}
        self.assertEqual(excluded & present, set())

    def test_no_corrupt_text_in_embedding_input(self):
        by_id = {chunk["chunk_id"]: chunk for chunk in canonical_chunks()}
        for row in self.rows():
            if row["source_kind"] == "canonical_chunk":
                status, _ = eligibility.classify(str(by_id[row["chunk_id"]]["text"]))
                self.assertNotEqual(status, "quarantined_extraction_failure", row["chunk_id"])

    def test_vector_index_is_contiguous_and_ordered(self):
        rows = self.rows()
        self.assertEqual([int(row["vector_index"]) for row in rows], list(range(len(rows))))

    def test_chunk_ids_unique_in_input(self):
        rows = self.rows()
        self.assertEqual(len({row["chunk_id"] for row in rows}), len(rows))

    def test_no_document_contributes_both_canonical_and_recovery(self):
        rows = self.rows()
        canonical = {row["document_id"] for row in rows if row["source_kind"] == "canonical_chunk"}
        recovery = {row["document_id"] for row in rows if row["source_kind"] == "recovery_chunk"}
        self.assertEqual(canonical & recovery, set())

    def test_source_kind_values_are_valid(self):
        self.assertTrue(all(row["source_kind"] in {"canonical_chunk", "recovery_chunk"} for row in self.rows()))

    def test_input_size_is_at_least_the_no_recovery_floor(self):
        self.assertGreaterEqual(len(self.rows()), 6039 - 58)

    def test_text_sha256_present_and_well_formed(self):
        for row in self.rows():
            self.assertRegex(row["text_sha256"], r"^[0-9a-f]{64}$")

    def test_damaged_documents_are_represented_by_recovery_only(self):
        rows = self.rows()
        for document_id in eligibility.DAMAGED_DOCUMENTS:
            kinds = {row["source_kind"] for row in rows if row["document_id"] == document_id}
            self.assertNotIn("canonical_chunk", kinds, document_id)


class TestRecoveryArtifacts(unittest.TestCase):
    def recovery_chunks(self):
        path = ROOT / "data/chunks_recovery/chunks.jsonl"
        if not path.is_file():
            self.skipTest("recovery chunks not generated yet")
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_replacement_chunk_ids_are_deterministic_and_namespaced(self):
        for chunk in self.recovery_chunks():
            self.assertRegex(chunk["chunk_id"], r"^DOC\d{6}-R1-C\d{4}$")

    def test_replacement_ids_do_not_collide_with_frozen_ids(self):
        frozen = {chunk["chunk_id"] for chunk in canonical_chunks()}
        self.assertEqual(frozen & {chunk["chunk_id"] for chunk in self.recovery_chunks()}, set())

    def test_recovery_chunks_are_clean(self):
        for chunk in self.recovery_chunks():
            status, reason = eligibility.classify(str(chunk["text"]))
            self.assertNotEqual(status, "quarantined_extraction_failure", f"{chunk['chunk_id']}: {reason}")

    def test_recovery_documents_carry_provenance(self):
        for document_id in eligibility.DAMAGED_DOCUMENTS:
            path = ROOT / f"data/corpus_recovery/{document_id}.md"
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for field in ("recovery_version", "recovery_method", "original_source_sha256", "recovery_created_at"):
                self.assertIn(field, text, f"{document_id} missing {field}")

    def test_recovery_documents_keep_original_document_id(self):
        for document_id in eligibility.DAMAGED_DOCUMENTS:
            path = ROOT / f"data/corpus_recovery/{document_id}.md"
            if not path.is_file():
                continue
            self.assertIn(f'document_id: "{document_id}"', path.read_text(encoding="utf-8"))

    def test_recovered_documents_have_no_residual_glyph_runs(self):
        for document_id in eligibility.DAMAGED_DOCUMENTS:
            path = ROOT / f"data/corpus_recovery/{document_id}.md"
            if not path.is_file():
                continue
            self.assertEqual(eligibility.residual_glyph_tokens(path.read_text(encoding="utf-8")), 0, document_id)

    def test_recovered_numbers_are_arithmetically_consistent(self):
        """Independent check that decoding is correct: rate x quantity must equal the stated total."""
        path = ROOT / "data/corpus_recovery/DOC000041.md"
        if not path.is_file():
            self.skipTest("DOC000041 recovery not generated")
        text = path.read_text(encoding="utf-8")
        matches = list(re.finditer(r"([\d]+) hrs/yr @ ([\d.]+) \$/hr=\s*\$ ([\d]+)", text))
        self.assertGreater(len(matches), 3, "expected several decodable cost lines")
        for match in matches:
            quantity, rate, total = int(match.group(1)), float(match.group(2)), int(match.group(3))
            self.assertAlmostEqual(quantity * rate, total, delta=1.0)


class TestFrozenIntegrity(unittest.TestCase):
    def test_frozen_artifacts_unchanged(self):
        for relative, expected in FROZEN_BASELINE.items():
            self.assertEqual(eligibility.sha256((ROOT / relative).read_bytes()), expected,
                             f"frozen artefact modified: {relative}")

    def test_recovery_never_writes_into_frozen_trees(self):
        for relative in ("data/corpus_recovery", "data/chunks_recovery"):
            self.assertFalse(str(ROOT / relative).startswith(str(ROOT / "data/corpus_normalized")))
        self.assertTrue((ROOT / "data/corpus_normalized").is_dir())

    def test_frozen_state_is_stable(self):
        self.assertEqual(eligibility.frozen_state(ROOT), eligibility.frozen_state(ROOT))


class TestIdempotency(unittest.TestCase):
    def test_recovery_decode_is_idempotent_on_clean_output(self):
        for document_id in eligibility.DAMAGED_DOCUMENTS:
            path = ROOT / f"data/corpus_recovery/{document_id}.md"
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            again, _ = eligibility.recover_text(text)
            self.assertEqual(again, text, f"{document_id} changed on a second recovery pass")

    def test_manifest_generation_is_deterministic(self):
        rows = read_csv("data/metadata/full_embedding_input_manifest.csv")
        if rows is None:
            self.skipTest("embedding input manifest not generated yet")
        payload = eligibility.csv_bytes(rows, eligibility.INPUT_FIELDS)
        self.assertEqual(eligibility.sha256(payload),
                         eligibility.sha256((ROOT / "data/metadata/full_embedding_input_manifest.csv").read_bytes()))


if __name__ == "__main__":
    unittest.main()
