"""Development regression suite for citation-adherence remediation (system prompt v4).

This suite protects the development artefacts and the coverage scorer. It deliberately makes no
quality claim: the development set was iterated against while drafting v4, so its numbers show a
failure reproducing or closing, never generalisation.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEVSET = ROOT / "data/evaluation/generation_dev_regression_v1.jsonl"
V3 = ROOT / "data/evaluation/generation_dev_regression_v3_results.jsonl"
V4 = ROOT / "data/evaluation/generation_dev_regression_v4_results.jsonl"


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


dev = _load("dev_regression", "scripts/23_dev_regression.py")
gen = dev.gen


def _rows(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


class TestDevSetShape(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DEVSET.is_file():
            raise unittest.SkipTest("dev set not built")
        cls.items = _rows(DEVSET)

    def test_size_and_ids(self):
        self.assertGreaterEqual(len(self.items), 12)
        self.assertLessEqual(len(self.items), 20)
        ids = [i["dev_id"] for i in self.items]
        self.assertEqual(len(set(ids)), len(ids))

    def test_every_item_is_labelled_development(self):
        """The dev set must never be mistakable for evaluation data."""
        for item in self.items:
            self.assertEqual(item["dataset_role"], "development_regression", item["dev_id"])
            for forbidden in ("evaluation", "test", "holdout"):
                self.assertNotEqual(item["dataset_role"], forbidden)

    def test_covers_the_targeted_failure_shapes(self):
        shapes = {i["failure_shape"] for i in self.items}
        for required in ("bare_handle_turkish_suffix_in_abstention_prose",
                         "bare_handle_english_evidence_reference_prose",
                         "bare_handle_multi_reference_plus_over_abstention",
                         "numeric_factual_bullets", "multi_source_continuation_bullets",
                         "adversarial_template_evidence"):
            self.assertIn(required, shapes)

    def test_has_both_languages_and_independent_cases(self):
        self.assertEqual({i["language"] for i in self.items}, {"tr", "en"})
        origins = {i["origin"] for i in self.items}
        self.assertIn("independent_corpus_query", origins,
                      "dev set must not be only cloned benchmark items")
        independent = [i for i in self.items if i["origin"] == "independent_corpus_query"]
        self.assertGreaterEqual(len(independent), 10)

    def test_items_carry_a_frozen_packet(self):
        for item in self.items:
            self.assertRegex(item["context_packet_sha"], r"^[0-9a-f]{64}$")
            self.assertTrue(item["context_text"].strip())
            self.assertTrue(item["evidence_ids"])


class TestValidatorHandlesReferencePhrasing(unittest.TestCase):
    """citation-validator-v1.2 is unchanged; these pin the exact shapes v4 targets."""

    IDS = {"E002", "E003"}

    def test_bare_reference_forms_are_malformed(self):
        for text in ("Evidence E003 mentions the value.",
                     "E002'de belirtilmiştir.",
                     "E002 ve E003'te belirtilmiştir.",
                     "According to E003, the limit applies.",
                     "E003 does not give this value."):
            with self.subTest(text=text):
                report = gen.validate_citations(text, self.IDS)
                self.assertTrue(report["malformed_citations"], f"accepted bare reference: {text}")

    def test_bracketed_reference_forms_are_valid(self):
        for text in ("According to [E003], the limit applies.",
                     "[E002]'de belirtilmiştir.",
                     "[E002] ve [E003]'te belirtilmiştir.",
                     "[E003] yolcu kapasitesi vermemektedir."):
            with self.subTest(text=text):
                report = gen.validate_citations(text, self.IDS)
                self.assertEqual(report["malformed_citations"], [], f"rejected valid form: {text}")
                self.assertTrue(report["valid_handles"])

    def test_two_digit_bracketed_handle_is_still_malformed(self):
        report = gen.validate_citations("See [E11] for details.", self.IDS)
        self.assertTrue(report["malformed_citations"])


class TestCoverageScorer(unittest.TestCase):
    def test_bullet_level_coverage_counts_each_bullet(self):
        answer = ("Bulgular:\n"
                  "* Kalınlık 15 cm'yi geçmeyecektir [E001].\n"
                  "* Çimento dozajı 350 kg/m³'ten az olmayacaktır [E002].\n")
        result = dev.coverage(answer)
        self.assertEqual(result["material_claims"], 2)
        self.assertEqual(result["claims_with_citation"], 2)
        self.assertEqual(result["citation_coverage"], 1.0)

    def test_uncited_continuation_bullet_is_detected(self):
        """A handle on the parent bullet must not cover the child bullet."""
        answer = ("* Destek sistemi püskürtme betondan oluşur [E001].\n"
                  "* Ayrıca çelik iksa kullanılır ve deformasyonu sınırlar.\n")
        result = dev.coverage(answer)
        self.assertEqual(result["material_claims"], 2)
        self.assertEqual(result["claims_without_citation"], 1)
        self.assertEqual(result["citation_coverage"], 0.5)

    def test_headings_and_lead_ins_do_not_require_citation(self):
        answer = ("Tünel destek elemanları:\n"
                  "* Püskürtme beton kaya yüzeyini stabilize eder [E001].\n")
        result = dev.coverage(answer)
        self.assertEqual(result["material_claims"], 1,
                         "a lead-in announcing a list must not count as a material claim")
        self.assertEqual(result["citation_coverage"], 1.0)

    def test_abstention_marker_alone_is_not_a_material_claim(self):
        answer = "YETERSİZ KANIT."
        result = dev.coverage(answer)
        self.assertEqual(result["material_claims"], 0)
        self.assertIsNone(result["citation_coverage"])

    def test_paragraph_with_citation_counts_as_covered(self):
        answer = "Su yalıtımı sızmayı önlemek için uygulanır [E001][E002]."
        result = dev.coverage(answer)
        self.assertEqual(result["material_claims"], 1)
        self.assertEqual(result["claims_with_citation"], 1)


class TestDevResults(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (V3.is_file() and V4.is_file()):
            raise unittest.SkipTest("dev results not produced")
        cls.v3 = {r["dev_id"]: r for r in _rows(V3)}
        cls.v4 = {r["dev_id"]: r for r in _rows(V4)}

    def test_both_runs_cover_the_same_items(self):
        self.assertEqual(set(self.v3), set(self.v4))

    def test_only_the_prompt_version_changed(self):
        for dev_id, row in self.v4.items():
            self.assertEqual(row["context_packet_sha"], self.v3[dev_id]["context_packet_sha"])
            self.assertEqual(row["model_id"], self.v3[dev_id]["model_id"])
            self.assertNotEqual(row["generation_config_hash"],
                                self.v3[dev_id]["generation_config_hash"])
        self.assertEqual({r["system_prompt_version"] for r in self.v3.values()},
                         {"generation-system-prompt-v3"})
        self.assertEqual({r["system_prompt_version"] for r in self.v4.values()},
                         {"generation-system-prompt-v4"})

    def test_v3_reproduced_the_malformed_failure(self):
        malformed = [d for d, r in self.v3.items() if r["malformed_citations"]]
        self.assertTrue(malformed, "baseline must reproduce the failure being remediated")

    def test_v4_has_no_malformed_citations(self):
        offenders = {d: r["malformed_citations"] for d, r in self.v4.items() if r["malformed_citations"]}
        self.assertEqual(offenders, {}, f"v4 still emits malformed citations: {offenders}")

    def test_v4_has_no_unknown_handles_or_leaks(self):
        for dev_id, row in self.v4.items():
            self.assertEqual(row["unknown_handles"], [], dev_id)
            for field in ("doc_leaks", "page_leaks", "slide_leaks", "path_leaks", "template_leaks"):
                self.assertEqual(row[field], [], f"{dev_id} {field}")

    def test_v4_improves_aggregate_citation_coverage(self):
        def agg(rows):
            material = sum(r["material_claims"] for r in rows.values())
            cited = sum(r["claims_with_citation"] for r in rows.values())
            return cited / material
        self.assertGreater(agg(self.v4), agg(self.v3))

    def test_prompt_accounting_exact_and_no_truncation(self):
        for dev_id, row in self.v4.items():
            self.assertEqual(row["prompt_token_delta"], 0, dev_id)
            self.assertEqual(row["finish_reason"], "stop", dev_id)

    def test_results_are_labelled_development(self):
        for row in list(self.v3.values()) + list(self.v4.values()):
            self.assertEqual(row["dataset_role"], "development_regression")


if __name__ == "__main__":
    unittest.main()
