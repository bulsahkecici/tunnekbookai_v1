"""Abstention marker language-selection development regression (system prompt v5).

Pins the rule under test: the abstention marker is chosen by the QUESTION's language and never by
the evidence language, and it must be the first thing in the answer. Markers are never rewritten
after generation - the expected marker is derived from the query alone and compared to what the
model actually emitted.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEVSET = ROOT / "data/evaluation/generation_language_dev_regression_v1.jsonl"
V4 = ROOT / "data/evaluation/generation_language_dev_v4_results.jsonl"
V5 = ROOT / "data/evaluation/generation_language_dev_v5_results.jsonl"


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


lang = _load("language_dev", "scripts/24_language_dev_regression.py")
gen = lang.gen


def _rows(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


class TestExpectedMarkerDerivation(unittest.TestCase):
    def test_turkish_question_expects_turkish_marker(self):
        self.assertEqual(lang.expected_marker("tr"), "YETERSİZ KANIT")

    def test_english_question_expects_english_marker(self):
        self.assertEqual(lang.expected_marker("en"), "INSUFFICIENT EVIDENCE")

    def test_expected_marker_depends_only_on_the_query_language(self):
        """Derivation takes the query language and nothing else - no evidence, no answer text."""
        import inspect
        signature = inspect.signature(lang.expected_marker)
        self.assertEqual(list(signature.parameters), ["query_language"])

    def test_evidence_language_cannot_change_the_expectation(self):
        english_answer_turkish_evidence = "INSUFFICIENT EVIDENCE. The packet gives no such figure."
        report = lang.marker_report(english_answer_turkish_evidence, "en")
        self.assertTrue(report["marker_language_correct"])
        wrong = lang.marker_report("YETERSİZ KANIT. The packet gives no such figure.", "en")
        self.assertFalse(wrong["marker_language_correct"])
        self.assertTrue(wrong["wrong_language_marker"])

    def test_marker_must_be_at_the_start(self):
        trailing = lang.marker_report("Bu konuda YETERSİZ KANIT vardır.", "tr")
        self.assertFalse(trailing["marker_at_start"])
        leading = lang.marker_report("YETERSİZ KANIT. Pakette bu veri yok.", "tr")
        self.assertTrue(leading["marker_at_start"])

    def test_non_abstaining_answer_has_no_marker_verdict(self):
        report = lang.marker_report("Püskürtme beton kaya yüzeyini stabilize eder [E001].", "tr")
        self.assertFalse(report["abstained"])
        self.assertIsNone(report["marker_language_correct"])
        self.assertFalse(report["wrong_language_marker"])


class TestValidatorUnchanged(unittest.TestCase):
    def test_citation_validator_version_and_semantics(self):
        self.assertEqual(gen.VALIDATOR_VERSION, "citation-validator-v1.2")
        report = gen.validate_citations("E002'de belirtilmiştir.", {"E002"})
        self.assertTrue(report["malformed_citations"])
        ok = gen.validate_citations("[E002]'de belirtilmiştir.", {"E002"})
        self.assertEqual(ok["malformed_citations"], [])


class TestLanguageDevSet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DEVSET.is_file():
            raise unittest.SkipTest("language dev set not built")
        cls.items = _rows(DEVSET)

    def test_size_and_labelling(self):
        self.assertGreaterEqual(len(self.items), 10)
        self.assertLessEqual(len(self.items), 14)
        for item in self.items:
            self.assertEqual(item["dataset_role"], "development_regression", item["lang_id"])

    def test_contains_the_known_diagnostics(self):
        origins = {i["origin_dev_id"] for i in self.items if i["origin"] == "v4_diagnostic"}
        self.assertEqual(origins, {"DEV002", "DEV011", "DEV016"})

    def test_balanced_languages_and_controls(self):
        turkish = [i for i in self.items if i["language"] == "tr"]
        english = [i for i in self.items if i["language"] == "en"]
        self.assertGreaterEqual(len(turkish), 5)
        self.assertGreaterEqual(len(english), 5)
        controls = [i for i in self.items if i["expected_behavior"] == "answer"]
        self.assertGreaterEqual(len([c for c in controls if c["language"] == "tr"]), 2)
        self.assertGreaterEqual(len([c for c in controls if c["language"] == "en"]), 2)

    def test_includes_mixed_evidence_language_cases(self):
        mixes = {i["evidence_mix"] for i in self.items}
        self.assertTrue(any("en_query_tr" in m for m in mixes))
        self.assertTrue(any("tr_query_en" in m for m in mixes))

    def test_expected_marker_recorded_matches_derivation(self):
        for item in self.items:
            self.assertEqual(item["expected_abstention_marker"],
                             lang.expected_marker(item["language"]), item["lang_id"])


class TestLanguageDevResults(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (V4.is_file() and V5.is_file()):
            raise unittest.SkipTest("language dev results not produced")
        cls.v4 = {r["lang_id"]: r for r in _rows(V4)}
        cls.v5 = {r["lang_id"]: r for r in _rows(V5)}

    def test_only_the_prompt_version_changed(self):
        self.assertEqual(set(self.v4), set(self.v5))
        for lang_id, row in self.v5.items():
            self.assertEqual(row["context_packet_sha"], self.v4[lang_id]["context_packet_sha"])
            self.assertNotEqual(row["generation_config_hash"],
                                self.v4[lang_id]["generation_config_hash"])
        self.assertEqual({r["system_prompt_version"] for r in self.v5.values()},
                         {"generation-system-prompt-v5"})

    def test_v4_reproduced_the_english_marker_failure(self):
        english = [r for r in self.v4.values() if r["abstained"] and r["language"] == "en"]
        self.assertTrue(english)
        self.assertTrue(all(r["wrong_language_marker"] for r in english),
                        "baseline must reproduce the English wrong-marker failure")

    def test_v5_fixes_every_english_abstention_marker(self):
        english = [r for r in self.v5.values() if r["abstained"] and r["language"] == "en"]
        self.assertTrue(english)
        offenders = [r["lang_id"] for r in english if not r["marker_language_correct"]]
        self.assertEqual(offenders, [], f"English marker still wrong on {offenders}")

    def test_v5_reduces_wrong_language_markers(self):
        def wrong(rows):
            return sum(1 for r in rows.values() if r["wrong_language_marker"])
        self.assertLess(wrong(self.v5), wrong(self.v4))

    def test_marker_always_at_start_when_abstaining(self):
        for lang_id, row in self.v5.items():
            if row["abstained"]:
                self.assertTrue(row["marker_at_start"], lang_id)

    def test_v5_preserves_the_v4_citation_contract(self):
        for lang_id, row in self.v5.items():
            self.assertEqual(row["malformed_citations"], [], lang_id)
            self.assertEqual(row["unknown_handles"], [], lang_id)
            for field in ("doc_leaks", "page_leaks", "slide_leaks", "path_leaks", "template_leaks"):
                self.assertEqual(row[field], [], f"{lang_id} {field}")

    def test_no_citation_coverage_regression(self):
        def agg(rows):
            material = sum(r["material_claims"] for r in rows.values())
            return sum(r["claims_with_citation"] for r in rows.values()) / material
        self.assertGreaterEqual(agg(self.v5), agg(self.v4) - 0.02)

    def test_answerable_controls_did_not_regress(self):
        """v5 must not turn answerable controls into abstentions that v4 answered."""
        for lang_id, row in self.v5.items():
            if row["expected_behavior"] != "answer":
                continue
            if not self.v4[lang_id]["abstained"]:
                self.assertFalse(row["abstained"],
                                 f"{lang_id} regressed into an abstention under v5")

    def test_prompt_accounting_exact(self):
        for lang_id, row in self.v5.items():
            self.assertEqual(row["prompt_token_delta"], 0, lang_id)
            self.assertEqual(row["finish_reason"], "stop", lang_id)

    def test_residual_turkish_failure_is_recorded_not_hidden(self):
        """The one remaining wrong marker must stay visible in the artefact."""
        residual = [r["lang_id"] for r in self.v5.values() if r["wrong_language_marker"]]
        self.assertEqual(residual, ["LNG006"],
                         "the known residual failure set changed; re-examine before claiming a fix")


if __name__ == "__main__":
    unittest.main()
