"""Tests for output contract v1.1 - the proper-noun-aware body language guard.

Two obligations pull against each other here and both are asserted: v1.1 must stop rejecting
correct English answers that name Turkish entities, and it must NOT become permissive enough to
let a genuinely wrong-language answer through. GEV018 and GEV062 are the two poles.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEV = ROOT / "data/evaluation/output_contract_language_v1_1_dev.jsonl"
V1_DEV = ROOT / "data/evaluation/output_contract_dev_v1.jsonl"
METADATA = ROOT / "data/metadata/generation_output_contract_v1_1.json"

PARENT_SHA = "670031d116056485155fc9d5c3d12b472d91f6b1e7a34ed9b169166f3727ce7d"
PROMPT_V5_SHA = "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085"
BENCHMARK_SHA = "1e6347b557d583b56882c4c05fd1c5453874b7a05e61205c9430a24a677b0cff"
PACKET_SHA = "0538705147cf543b45fe8e73d57828cbc341a9a5a1dd574bd0969a9326e54d7a"

NON_LANGUAGE_FIELDS = [
    "malformed_citations", "unknown_handles", "citation_syntax_valid", "doc_leaks", "page_leaks",
    "slide_leaks", "path_leaks", "template_leaks", "thinking_marker_leaks", "material_claim_count",
    "claims_with_citation", "citation_coverage", "citation_coverage_status", "abstention_detected",
    "actual_abstention_marker", "marker_at_start", "expected_abstention_marker",
    "marker_language_valid", "validator_version", "repair_policy", "raw_answer_sha",
]


def load_script(file_name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "scripts" / file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


v11 = load_script("31_generation_output_contract_v1_1.py", "oc_v1_1")
v1 = v11.v1


def rows(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


DEV_ROWS = rows(DEV)
BY_ID = {r["case_id"]: r for r in DEV_ROWS}


class TestContractIdentity(unittest.TestCase):
    def test_version_and_parent(self):
        self.assertEqual(v11.CONTRACT_VERSION, "tunnelbook-generation-output-contract-v1.1")
        self.assertEqual(v11.PARENT_CONTRACT_VERSION, "tunnelbook-generation-output-contract-v1")
        self.assertEqual(v11.PARENT_CONTRACT_SHA, PARENT_SHA)

    def test_metadata_records_implementation_sha(self):
        meta = json.loads(METADATA.read_text(encoding="utf-8"))
        actual = sha(ROOT / "scripts/31_generation_output_contract_v1_1.py")
        self.assertEqual(meta["implementation_sha"], actual)
        self.assertEqual(meta["implementation_sha"], v11.implementation_sha256())
        self.assertEqual(meta["status"], "frozen")

    def test_change_scope_is_language_only(self):
        meta = json.loads(METADATA.read_text(encoding="utf-8"))
        self.assertIn("proper-noun-aware deterministic language detection only",
                      meta["change_scope"])
        self.assertFalse(meta["marker_policy_changed"])
        self.assertFalse(meta["validator_modified"])

    def test_result_carries_both_contract_identities(self):
        result = v11.enforce("The lining is applied after each round of excavation [E001].",
                             "en", {"E001"})
        self.assertEqual(result.contract_version, "tunnelbook-generation-output-contract-v1.1")
        self.assertEqual(result.parent_contract_version, v11.PARENT_CONTRACT_VERSION)
        self.assertEqual(result.parent_contract_sha256, PARENT_SHA)
        self.assertEqual(result.language_detection_version, "proper-noun-aware-lexical-v1.1")


class TestParentAndFrozenArtifactsUnchanged(unittest.TestCase):
    def test_parent_contract_v1_unmodified(self):
        self.assertEqual(sha(ROOT / "scripts/26_generation_output_contract.py"), PARENT_SHA)

    def test_system_prompt_v5_unmodified(self):
        self.assertEqual(sha(ROOT / "data/metadata/generation_system_prompt_v5.txt"), PROMPT_V5_SHA)

    def test_no_prompt_v6(self):
        self.assertFalse((ROOT / "data/metadata/generation_system_prompt_v6.txt").exists())

    def test_benchmark_and_packets_unmodified(self):
        self.assertEqual(sha(ROOT / "data/evaluation/generation_eval_benchmark_v2.jsonl"),
                         BENCHMARK_SHA)
        self.assertEqual(sha(ROOT / "data/evaluation/generation_eval_benchmark_v2_packets.jsonl"),
                         PACKET_SHA)

    def test_validator_semantics_unchanged(self):
        self.assertEqual(v11.VALIDATOR_VERSION, "citation-validator-v1.2")
        self.assertEqual(v11.gen.VALIDATOR_VERSION, v1.gen.VALIDATOR_VERSION)


class TestPrimaryBugFixed(unittest.TestCase):
    """GEV018 - the false positive that failed both stack gates."""

    def setUp(self):
        self.case = BY_ID["GEV018"]

    def test_v1_rejected_it(self):
        result = v1.enforce(self.case["text"], "en", set(self.case["evidence_ids"]))
        self.assertFalse(result.contract_valid)
        self.assertIn("answer_body_language_mismatch", result.failure_reasons)
        self.assertEqual(result.answer_body_language, "tr")

    def test_v1_1_classifies_the_body_as_english(self):
        detected = v11.detect_language(self.case["text"])
        self.assertEqual(detected["language"], "en")
        self.assertEqual(detected["status"], "confident")

    def test_v1_1_accepts_it_with_no_language_failure(self):
        result = v11.enforce(self.case["text"], "en", set(self.case["evidence_ids"]))
        self.assertNotIn("answer_body_language_mismatch", result.failure_reasons)
        self.assertTrue(result.body_language_valid)
        self.assertTrue(result.contract_valid)
        self.assertEqual(result.failure_reasons, [])

    def test_the_turkish_glyphs_were_entity_borne(self):
        """The glyphs that misled v1 all sat inside proper nouns, and masking removes them."""
        raw_glyphs = sum(1 for ch in self.case["text"] if ch in v11.TURKISH_CHARS)
        detected = v11.detect_language(self.case["text"])
        self.assertGreaterEqual(raw_glyphs, 8)
        self.assertLess(detected["glyphs_after_masking"], raw_glyphs)
        self.assertFalse(detected["glyph_tie_break_applied"])


class TestRealDefectsPreserved(unittest.TestCase):
    """v1.1 must not buy GEV018 by going blind to genuine language defects."""

    def test_gev062_still_fails_body_language(self):
        case = BY_ID["GEV062"]
        result = v11.enforce(case["text"], "tr", set(case["evidence_ids"]))
        self.assertFalse(result.contract_valid)
        self.assertIn("answer_body_language_mismatch", result.failure_reasons)
        self.assertIn("wrong_abstention_marker_language", result.failure_reasons)
        self.assertEqual(result.answer_body_language, "en")

    def test_gev061_marker_failure_preserved_and_body_not_flagged(self):
        case = BY_ID["GEV061"]
        result = v11.enforce(case["text"], "tr", set(case["evidence_ids"]))
        self.assertFalse(result.contract_valid)
        self.assertIn("wrong_abstention_marker_language", result.failure_reasons)
        self.assertNotIn("answer_body_language_mismatch", result.failure_reasons)
        self.assertEqual(result.answer_body_language, "tr")
        self.assertTrue(result.body_language_valid)

    def test_gev042_malformed_citation_preserved(self):
        v1_case = {r["case_id"]: r for r in rows(V1_DEV)}["GEV042"]
        result = v11.enforce(v1_case["raw_answer"], "tr", set(v1_case["evidence_ids"]))
        self.assertFalse(result.contract_valid)
        self.assertEqual(result.malformed_citations, ["E002", "E004", "E015"])


class TestProperNounMatrix(unittest.TestCase):
    def _check_group(self, group, expected_language):
        cases = [r for r in DEV_ROWS if r["group"] == group]
        self.assertGreaterEqual(len(cases), 5)
        for case in cases:
            detected = v11.detect_language(case["text"])
            self.assertEqual(detected["language"], expected_language,
                             f"{case['case_id']}: {case['text'][:80]}")
            self.assertEqual(detected["status"], "confident", case["case_id"])

    def test_english_prose_with_turkish_proper_nouns(self):
        self._check_group("english_prose_with_turkish_proper_nouns", "en")

    def test_turkish_prose_with_english_proper_nouns(self):
        self._check_group("turkish_prose_with_english_proper_nouns", "tr")

    def test_plain_english(self):
        self._check_group("plain_english", "en")

    def test_plain_turkish(self):
        self._check_group("plain_turkish", "tr")

    def test_no_inverse_failure_turkish_without_many_glyphs(self):
        """Turkish prose light on special characters must still read as Turkish."""
        text = ("Bu bolumde tunel destek sistemi ele alinmakta ve kaya sinifina bagli olarak "
                "uygulanan yontemler karsilastirilmaktadir.")
        detected = v11.detect_language(text)
        self.assertEqual(detected["glyphs_after_masking"], 0)
        self.assertEqual(detected["language"], "tr")

    def test_entity_masking_uses_no_name_list(self):
        """A never-before-seen Turkish entity must be handled by the same rule."""
        text = ("The Kızılırmak Vadisi Tüneli was completed by the contractor and the ventilation "
                "system was commissioned before the road was opened to traffic.")
        self.assertEqual(v11.detect_language(text)["language"], "en")

    def test_sentence_initial_entity_does_not_flip_english(self):
        text = ("İstanbul Büyükşehir Belediyesi confirmed that the tunnel was inspected and that "
                "the drainage system was found to be in good condition.")
        self.assertEqual(v11.detect_language(text)["language"], "en")


class TestAmbiguousAndShort(unittest.TestCase):
    def test_mixed_language_is_reported_ambiguous_not_guessed(self):
        cases = [r for r in DEV_ROWS if r["group"] == "mixed_language_ambiguous"]
        self.assertGreaterEqual(len(cases), 5)
        for case in cases:
            detected = v11.detect_language(case["text"])
            self.assertIsNone(detected["language"], case["case_id"])
            self.assertEqual(detected["status"], "ambiguous", case["case_id"])
            self.assertTrue(detected["mixed_language_detected"], case["case_id"])

    def test_ambiguous_body_fails_closed(self):
        case = BY_ID["MIX01"]
        result = v11.enforce(case["text"], "tr", set())
        self.assertIn("answer_body_language_ambiguous", result.failure_reasons)
        self.assertFalse(result.contract_valid)

    def test_short_answers_report_insufficient_text(self):
        cases = [r for r in DEV_ROWS if r["group"] == "short_or_numeric_heavy"]
        self.assertGreaterEqual(len(cases), 5)
        for case in cases:
            detected = v11.detect_language(case["text"])
            self.assertEqual(detected["status"], "insufficient_text", case["case_id"])
            self.assertIsNone(detected["language"])

    def test_glyph_tie_break_cannot_decide_alone(self):
        """Turkish glyphs with no Turkish function-word support must not flip a verdict."""
        self.assertEqual(v11.MIN_TURKISH_WORDS_FOR_GLYPH_SUPPORT, 1)
        self.assertLessEqual(v11.GLYPH_TIE_BREAK_CAP, 2.0)


class TestDevSetShapeAndOutcomes(unittest.TestCase):
    def test_dev_set_meets_required_group_sizes(self):
        counts = {}
        for row in DEV_ROWS:
            counts[row["group"]] = counts.get(row["group"], 0) + 1
        self.assertGreaterEqual(len(DEV_ROWS), 40)
        self.assertGreaterEqual(counts["english_prose_with_turkish_proper_nouns"], 10)
        self.assertGreaterEqual(counts["turkish_prose_with_english_proper_nouns"], 10)
        self.assertGreaterEqual(counts["plain_english"], 5)
        self.assertGreaterEqual(counts["plain_turkish"], 5)
        self.assertGreaterEqual(counts["mixed_language_ambiguous"], 5)
        self.assertGreaterEqual(counts["short_or_numeric_heavy"], 5)

    def test_zero_false_positives_and_negatives_on_dev_set(self):
        mismatches = []
        for row in DEV_ROWS:
            detected = v11.detect_language(v11._body_after_marker(row["text"]))
            if (detected["language"] != row["expected_body_language"]
                    or detected["status"] != row["expected_body_status"]):
                mismatches.append(row["case_id"])
        self.assertEqual(mismatches, [])

    def test_v1_1_is_strictly_better_than_v1_on_this_set(self):
        def misses(module):
            return sum(1 for row in DEV_ROWS
                       if module.detect_language(module._body_after_marker(row["text"]))["language"]
                       != row["expected_body_language"])
        self.assertEqual(misses(v11), 0)
        self.assertGreater(misses(v1), 0)


class TestSemanticRegressionAgainstV1(unittest.TestCase):
    def _compare(self, answer, query_language, evidence):
        a = v1.enforce(answer, query_language, evidence).to_dict()
        b = v11.enforce(answer, query_language, evidence).to_dict()
        return [f for f in NON_LANGUAGE_FIELDS if a[f] != b[f]]

    def test_no_non_language_drift_on_v1_dev_set(self):
        for row in rows(V1_DEV):
            drift = self._compare(row["raw_answer"], row.get("query_language"),
                                  set(row.get("evidence_ids", [])))
            self.assertEqual(drift, [], row["case_id"])

    def test_no_non_language_drift_on_language_dev_set(self):
        for row in DEV_ROWS:
            drift = self._compare(row["text"], row.get("query_language"),
                                  set(row.get("evidence_ids", [])))
            self.assertEqual(drift, [], row["case_id"])

    def test_v1_clean_controls_all_still_pass(self):
        controls = [r for r in rows(V1_DEV) if r["expected_contract_valid"]]
        self.assertGreaterEqual(len(controls), 14)
        for row in controls:
            result = v11.enforce(row["raw_answer"], row["query_language"],
                                 set(row["evidence_ids"]))
            self.assertTrue(result.contract_valid, f"{row['case_id']}: {result.failure_reasons}")

    def test_citation_matrix_identical_to_v1(self):
        matrix = [("[E001]", "valid"), ("[E001]'de", "valid"), ("[E001][E004]", "valid"),
                  ("(E001)", "invalid"), ("Evidence E001", "invalid"), ("E001", "invalid"),
                  ("E001'de", "invalid"), ("E001-E004", "invalid"), ("[E001-E004]", "invalid"),
                  ("[E01]", "invalid"), ("[E999]", "unknown")]
        exposed = {"E001", "E004"}
        for fragment, want in matrix:
            text = f"Beton dayanımı {fragment} değerine göre belirlenir."
            a, b = v1.enforce(text, "tr", exposed), v11.enforce(text, "tr", exposed)
            self.assertEqual(a.malformed_citations, b.malformed_citations, fragment)
            self.assertEqual(a.unknown_handles, b.unknown_handles, fragment)
            if want == "valid":
                self.assertEqual(b.malformed_citations, [])
                self.assertEqual(b.unknown_handles, [])
            elif want == "unknown":
                self.assertTrue(b.unknown_handles)
            else:
                self.assertTrue(b.malformed_citations)

    def test_marker_mapping_unchanged(self):
        self.assertEqual(v11.MARKER_FOR_LANGUAGE, v1.MARKER_FOR_LANGUAGE)
        self.assertEqual(v11.MARKER_FOR_LANGUAGE,
                         {"tr": "YETERSİZ KANIT", "en": "INSUFFICIENT EVIDENCE"})

    def test_marker_at_start_rule_unchanged(self):
        text = "Bir açıklama. YETERSİZ KANIT sonrasında gelir ve bu kabul edilemez."
        self.assertIn("abstention_marker_not_at_start", v11.enforce(text, "tr", set()).failure_reasons)

    def test_coverage_remains_telemetry_only(self):
        text = ("Tünel kazısında ilerleme boyu kaya sınıfına göre değişmektedir. "
                "Bu değerler projeye göre belirlenmektedir.")
        result = v11.enforce(text, "tr", {"E001"})
        self.assertEqual(result.citation_coverage_status, "telemetry_only_not_enforced")
        self.assertNotIn("citation_coverage", result.failure_reasons)


class TestNoRepair(unittest.TestCase):
    def test_repair_policy_unchanged(self):
        self.assertEqual(v11.REPAIR_POLICY, "none_fail_closed")
        self.assertEqual(v11.REPAIR_POLICY, v1.REPAIR_POLICY)

    def test_no_rewritten_answer_field(self):
        result = v11.enforce("(E002) başlığı altında verilmiştir.", "tr", {"E002"}).to_dict()
        for key in result:
            self.assertNotIn("rewritten", key)
            self.assertNotIn("repaired", key)
            self.assertNotIn("translated", key)

    def test_wrong_marker_is_reported_not_replaced(self):
        case = BY_ID["GEV062"]
        result = v11.enforce(case["text"], "tr", set(case["evidence_ids"]))
        self.assertEqual(result.actual_abstention_marker, "INSUFFICIENT EVIDENCE")
        self.assertEqual(result.expected_abstention_marker, "YETERSİZ KANIT")
        self.assertTrue(case["text"].lstrip().startswith("INSUFFICIENT EVIDENCE"))

    def test_raw_answer_hash_is_of_untouched_input(self):
        text = "The tunnel lining was installed [E001] and the invert was closed shortly after."
        result = v11.enforce(text, "en", {"E001"})
        self.assertEqual(result.raw_answer_sha,
                         hashlib.sha256(text.encode("utf-8")).hexdigest())


class TestStackNotPromoted(unittest.TestCase):
    def test_candidate_not_marked_acceptable(self):
        descriptor = json.loads((ROOT / "data/metadata/generation_candidate_v1.json")
                                .read_text(encoding="utf-8"))
        self.assertNotEqual(descriptor["status"], "acceptable")

    def test_metadata_states_stack_is_not_promoted(self):
        meta = json.loads(METADATA.read_text(encoding="utf-8"))
        self.assertIn("does NOT make the production stack acceptable", meta["stack_status_effect"])


if __name__ == "__main__":
    unittest.main()
