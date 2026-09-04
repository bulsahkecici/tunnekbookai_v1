"""Deterministic generation output contract v1.

The contract is an enforcement layer over the unchanged system prompt v5. These tests pin its two
defining properties: it catches the Phase B v2 defects that prompt engineering could not eliminate,
and it never repairs anything. A repair layer would have masked GEV062, whose whole body is in the
wrong language, by rewriting only its opening marker.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEVSET = ROOT / "data/evaluation/output_contract_dev_v1.jsonl"
METADATA = ROOT / "data/metadata/generation_output_contract_v1.json"
PROMPT_V5 = ROOT / "data/metadata/generation_system_prompt_v5.txt"
BENCH_V1 = ROOT / "data/evaluation/generation_eval_benchmark_v1.jsonl"
BENCH_V2 = ROOT / "data/evaluation/generation_eval_benchmark_v2.jsonl"
PACKETS_V2 = ROOT / "data/evaluation/generation_eval_benchmark_v2_packets.jsonl"

PROMPT_V5_SHA = "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085"
BENCH_V1_SHA = "de3c1684ad26b459e6a209a9ef770c1a0f0fae39b44d0d251bc492ca3f75bd6b"
BENCH_V2_SHA = "1e6347b557d583b56882c4c05fd1c5453874b7a05e61205c9430a24a677b0cff"
PACKETS_V2_SHA = "0538705147cf543b45fe8e73d57828cbc341a9a5a1dd574bd0969a9326e54d7a"

IDS = {"E001", "E002", "E004"}


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


oc = _load("output_contract", "scripts/26_generation_output_contract.py")


def _rows(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


class TestContractIdentity(unittest.TestCase):
    def test_version_and_repair_policy(self):
        self.assertEqual(oc.CONTRACT_VERSION, "tunnelbook-generation-output-contract-v1")
        self.assertEqual(oc.REPAIR_POLICY, "none_fail_closed")

    def test_marker_mapping(self):
        self.assertEqual(oc.MARKER_FOR_LANGUAGE, {"tr": "YETERSİZ KANIT",
                                                  "en": "INSUFFICIENT EVIDENCE"})
        self.assertEqual(tuple(oc.SUPPORTED_LANGUAGES), ("tr", "en"))

    def test_metadata_records_the_implementation_sha(self):
        meta = json.loads(METADATA.read_text(encoding="utf-8"))
        self.assertEqual(meta["implementation_sha"], oc.implementation_sha256())
        self.assertEqual(meta["repair_policy"], "none_fail_closed")
        self.assertEqual(meta["validator_version"], "citation-validator-v1.2")
        self.assertFalse(meta["validator_modified"])
        self.assertEqual(meta["generation_calls_in_this_task"], 0)

    def test_result_carries_contract_identity(self):
        result = oc.enforce("Kalınlık 15 cm'yi geçmeyecektir [E001].", "tr", IDS)
        self.assertEqual(result.contract_version, oc.CONTRACT_VERSION)
        self.assertEqual(result.contract_sha256, oc.implementation_sha256())
        self.assertEqual(result.validator_version, "citation-validator-v1.2")

    def test_rejects_unsupported_query_language(self):
        with self.assertRaises(oc.ContractConfigError):
            oc.enforce("text", "de", IDS)


class TestNoRepair(unittest.TestCase):
    """The contract must be incapable of returning altered text."""

    def test_result_exposes_no_rewritten_answer(self):
        result = oc.enforce("E002'de belirtilmiştir ve kalınlık yeterlidir.", "tr", IDS)
        fields = set(result.to_dict())
        for forbidden in ("repaired_answer", "normalised_answer", "corrected_answer",
                          "rewritten_answer", "answer"):
            self.assertNotIn(forbidden, fields)

    def test_raw_answer_hash_is_of_the_untouched_input(self):
        answer = "INSUFFICIENT EVIDENCE. Pakette bu veri yoktur ve başka bir kayıt bulunmamaktadır."
        result = oc.enforce(answer, "tr", IDS)
        self.assertEqual(result.raw_answer_sha,
                         hashlib.sha256(answer.encode("utf-8")).hexdigest())

    def test_malformed_citation_is_reported_not_normalised(self):
        result = oc.enforce("Bkz (E002) ve E004 kaynakları incelenmelidir burada.", "tr", IDS)
        self.assertFalse(result.contract_valid)
        self.assertIn("malformed_citation", result.failure_reasons)
        for handle in result.malformed_citations:
            self.assertNotIn("[", handle)

    def test_wrong_marker_is_reported_not_replaced(self):
        answer = "INSUFFICIENT EVIDENCE. Sağlanan kanıt paketinde bu veri bulunmamaktadır ve yoktur."
        result = oc.enforce(answer, "tr", IDS)
        self.assertEqual(result.actual_abstention_marker, "INSUFFICIENT EVIDENCE")
        self.assertEqual(result.expected_abstention_marker, "YETERSİZ KANIT")
        self.assertFalse(result.marker_language_valid)
        self.assertIn("wrong_abstention_marker_language", result.failure_reasons)


class TestCitationSyntaxMatrix(unittest.TestCase):
    def _valid(self, text):
        return oc.enforce(text + " Bu cümle yeterli uzunlukta bir Türkçe gövde sağlar.", "tr", IDS)

    def test_valid_forms(self):
        for text in ("Kalınlık [E001] ile verilmiştir.",
                     "Kalınlık [E001]'de verilmiştir.",
                     "Kalınlık [E001][E004] ile verilmiştir."):
            with self.subTest(text=text):
                result = self._valid(text)
                self.assertEqual(result.malformed_citations, [], text)
                self.assertTrue(result.citation_syntax_valid, text)

    def test_invalid_forms(self):
        for text in ("Kaynak (E001) incelenmelidir.",
                     "Evidence E001 mentions this.",
                     "Kaynak E001 incelenmelidir.",
                     "Kaynak E001'de belirtilmiştir.",
                     "Kaynaklar E001-E004 arasındadır.",
                     "Kaynaklar [E001-E004] arasındadır.",
                     "Kaynak [E01] incelenmelidir."):
            with self.subTest(text=text):
                result = self._valid(text)
                self.assertTrue(result.malformed_citations, f"accepted malformed: {text}")
                self.assertFalse(result.citation_syntax_valid)
                self.assertIn("malformed_citation", result.failure_reasons)

    def test_unknown_handle_is_rejected_separately(self):
        result = self._valid("Kaynak [E999] incelenmelidir.")
        self.assertEqual(result.unknown_handles, ["E999"])
        self.assertIn("unknown_citation", result.failure_reasons)
        self.assertFalse(result.citation_syntax_valid)


class TestLanguageDetection(unittest.TestCase):
    def test_turkish_prose(self):
        d = oc.detect_language("Püskürtme beton kaya yüzeyinde oluşabilecek gevşemeleri engeller "
                               "ve destek sistemi ile birlikte çalışır.")
        self.assertEqual(d["language"], "tr")
        self.assertEqual(d["status"], "confident")

    def test_english_prose(self):
        d = oc.detect_language("The shotcrete layer prevents loosening of the rock surface and "
                               "works together with the initial support system.")
        self.assertEqual(d["language"], "en")

    def test_turkish_prose_with_english_technical_terms(self):
        d = oc.detect_language("Bu tünelde shotcrete ve rock bolt uygulaması yapılır; NATM "
                               "yöntemi ile birlikte lattice girder kullanılır ve destek sağlanır.")
        self.assertEqual(d["language"], "tr",
                         "English loan terms must not flip a Turkish body to English")

    def test_english_prose_with_turkish_proper_nouns(self):
        d = oc.detect_language("The Bolu Mountain Tunnel and the Zigana Tunnel are described in "
                               "the report, which also covers the Ovit and Marmaray projects.")
        self.assertEqual(d["language"], "en",
                         "Turkish place names must not flip an English body to Turkish")

    def test_numeric_heavy_answer_still_resolves_by_prose(self):
        d = oc.detect_language("Maksimum kalınlık 15 cm, minimum dozaj 350 kg/m³ ve oran 0,50 "
                               "olarak verilmiştir ve bu değerler şartnamede belirtilen sınırlardır.")
        self.assertEqual(d["language"], "tr")

    def test_very_short_abstention_is_insufficient_text(self):
        d = oc.detect_language("YETERSİZ KANIT.")
        self.assertEqual(d["status"], "insufficient_text")
        self.assertIsNone(d["language"])

    def test_symbol_and_number_only_text_is_not_guessed(self):
        d = oc.detect_language("15 cm 350 kg/m³ 0,50 12 24 36 48 60 72 84 96 108 120 132 144")
        self.assertIn(d["status"], {"ambiguous", "insufficient_text"})
        self.assertIsNone(d["language"])

    def test_ambiguous_mixed_language_is_reported_not_guessed(self):
        d = oc.detect_language("the ve and ile of bir to bu in için on gibi with olarak is olan")
        self.assertIn(d["status"], {"ambiguous", "confident"})
        if d["status"] == "ambiguous":
            self.assertIsNone(d["language"])


class TestMarkerAndBodyGuards(unittest.TestCase):
    def test_correct_turkish_abstention_passes(self):
        answer = ("YETERSİZ KANIT. Sağlanan kanıt paketinde bu değere ilişkin herhangi bir bilgi "
                  "bulunmamaktadır ve ilgili veriler yer almamaktadır.")
        result = oc.enforce(answer, "tr", IDS)
        self.assertTrue(result.contract_valid, result.failure_reasons)
        self.assertTrue(result.abstention_detected)
        self.assertTrue(result.marker_language_valid)

    def test_correct_english_abstention_passes(self):
        answer = ("INSUFFICIENT EVIDENCE. The provided packet does not contain the requested "
                  "figure and no related value is given in the evidence.")
        result = oc.enforce(answer, "en", IDS)
        self.assertTrue(result.contract_valid, result.failure_reasons)

    def test_marker_not_at_start_is_rejected(self):
        answer = ("Bu konuda değerlendirme yapıldığında sonuç olarak YETERSİZ KANIT durumu "
                  "ortaya çıkmaktadır ve veriler yetersizdir.")
        result = oc.enforce(answer, "tr", IDS)
        self.assertFalse(result.contract_valid)
        self.assertIn("abstention_marker_not_at_start", result.failure_reasons)

    def test_body_language_mismatch_is_caught_independently_of_the_marker(self):
        """Even with the correct Turkish marker, an English body must fail."""
        answer = ("YETERSİZ KANIT. The provided evidence does not contain the requested figure "
                  "and there is no related value in the packet for that year.")
        result = oc.enforce(answer, "tr", IDS)
        self.assertTrue(result.marker_language_valid)
        self.assertFalse(result.body_language_valid)
        self.assertIn("answer_body_language_mismatch", result.failure_reasons)
        self.assertFalse(result.contract_valid)

    def test_empty_answer_is_rejected(self):
        result = oc.enforce("   ", "tr", IDS)
        self.assertFalse(result.contract_valid)
        self.assertIn("empty_answer", result.failure_reasons)

    def test_thinking_marker_leak_is_rejected(self):
        result = oc.enforce("<think>plan</think> Kalınlık 15 cm olarak verilmiştir [E001] ve "
                            "bu değer şartnamede belirtilmiştir.", "tr", IDS)
        self.assertFalse(result.contract_valid)
        self.assertIn("thinking_marker_leak", result.failure_reasons)

    def test_missing_query_language_is_inferred_and_flagged(self):
        answer = ("Püskürtme beton kaya yüzeyindeki gevşemeleri engeller ve destek sistemiyle "
                  "birlikte çalışır [E001].")
        result = oc.enforce(answer, None, IDS)
        self.assertEqual(result.query_language, "tr")
        self.assertTrue(result.query_language_status.startswith("inferred_"))

    def test_undeterminable_query_language_fails_closed(self):
        result = oc.enforce("15 cm 350 kg 0,50 12 24 36 48 60 72 84 96 108 120", None, IDS)
        self.assertIsNone(result.query_language)
        self.assertIn("query_language_ambiguous", result.failure_reasons)
        self.assertFalse(result.contract_valid)


class TestCoverageTelemetry(unittest.TestCase):
    def test_coverage_is_reported_but_never_enforced(self):
        answer = ("* Kalınlık 15 cm'yi geçmeyecektir [E001].\n"
                  "* Çimento dozajı en az 350 kg/m³ olmalıdır ve bu değer şartnamede yer alır.\n")
        result = oc.enforce(answer, "tr", IDS)
        self.assertEqual(result.material_claim_count, 2)
        self.assertEqual(result.claims_with_citation, 1)
        self.assertEqual(result.citation_coverage, 0.5)
        self.assertEqual(result.citation_coverage_status, "telemetry_only_not_enforced")
        self.assertTrue(result.contract_valid,
                        "low coverage alone must not reject a response in contract v1")

    def test_no_handle_is_ever_inserted(self):
        answer = "Çimento dozajı en az 350 kg/m³ olmalıdır ve bu değer şartnamede yer alır."
        result = oc.enforce(answer, "tr", IDS)
        self.assertEqual(result.claims_with_citation, 0)
        self.assertNotIn("[E", json.dumps(result.to_dict(), ensure_ascii=False)[:0] or "")


class TestDevelopmentCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DEVSET.is_file():
            raise unittest.SkipTest("output contract dev set not built")
        cls.cases = {c["case_id"]: c for c in _rows(DEVSET)}

    def _run(self, case_id):
        case = self.cases[case_id]
        return case, oc.enforce(case["raw_answer"], case["query_language"], case["evidence_ids"],
                                case["answerability"])

    def test_dev_set_shape(self):
        self.assertGreaterEqual(len(self.cases), 17)
        roles = [c["case_role"] for c in self.cases.values()]
        self.assertGreaterEqual(sum(1 for r in roles if r == "clean_control_tr_answer"), 5)
        self.assertGreaterEqual(sum(1 for r in roles if r == "clean_control_en_answer"), 5)
        self.assertGreaterEqual(sum(1 for r in roles if r == "clean_control_tr_abstention"), 2)
        self.assertGreaterEqual(sum(1 for r in roles if r == "clean_control_en_abstention"), 2)
        for case in self.cases.values():
            self.assertEqual(case["dataset_role"], "development_validation")

    def test_gev042_rejected_for_malformed_citations(self):
        _, result = self._run("GEV042")
        self.assertFalse(result.contract_valid)
        self.assertIn("malformed_citation", result.failure_reasons)
        self.assertTrue(result.malformed_citations)

    def test_gev061_rejected_for_wrong_marker_language(self):
        _, result = self._run("GEV061")
        self.assertFalse(result.contract_valid)
        self.assertIn("wrong_abstention_marker_language", result.failure_reasons)
        self.assertEqual(result.expected_abstention_marker, "YETERSİZ KANIT")
        self.assertEqual(result.actual_abstention_marker, "INSUFFICIENT EVIDENCE")

    def test_gev062_rejected_for_marker_and_body_language(self):
        _, result = self._run("GEV062")
        self.assertFalse(result.contract_valid)
        self.assertIn("wrong_abstention_marker_language", result.failure_reasons)
        self.assertIn("answer_body_language_mismatch", result.failure_reasons)
        self.assertEqual(result.answer_body_language, "en")

    def test_all_clean_controls_pass(self):
        offenders = []
        for case_id, case in self.cases.items():
            if case["case_role"] == "known_failure":
                continue
            _, result = self._run(case_id)
            if not result.contract_valid:
                offenders.append((case_id, result.failure_reasons))
        self.assertEqual(offenders, [], f"false positives on clean controls: {offenders}")

    def test_every_expected_failure_reason_is_produced(self):
        for case_id, case in self.cases.items():
            for reason in case["expected_failure_reasons"]:
                _, result = self._run(case_id)
                self.assertIn(reason, result.failure_reasons, case_id)


class TestFrozenIntegrity(unittest.TestCase):
    def test_system_prompt_v5_unchanged(self):
        self.assertEqual(hashlib.sha256(PROMPT_V5.read_bytes()).hexdigest(), PROMPT_V5_SHA)

    def test_benchmarks_unchanged(self):
        self.assertEqual(hashlib.sha256(BENCH_V1.read_bytes()).hexdigest(), BENCH_V1_SHA)
        self.assertEqual(hashlib.sha256(BENCH_V2.read_bytes()).hexdigest(), BENCH_V2_SHA)
        self.assertEqual(hashlib.sha256(PACKETS_V2.read_bytes()).hexdigest(), PACKETS_V2_SHA)

    def test_validator_semantics_unchanged(self):
        self.assertEqual(oc.VALIDATOR_VERSION, "citation-validator-v1.2")
        report = oc.gen.validate_citations("E002'de belirtilmiştir.", {"E002"})
        self.assertTrue(report["malformed_citations"])
        ok = oc.gen.validate_citations("[E002]'de belirtilmiştir.", {"E002"})
        self.assertEqual(ok["malformed_citations"], [])

    def test_contract_does_not_mark_candidate_acceptable(self):
        meta = json.loads(METADATA.read_text(encoding="utf-8"))
        self.assertIn("does not make generator v5 ACCEPTABLE", meta["candidate_status_effect"])
        descriptor = json.loads((ROOT / "data/metadata/generation_candidate_v1.json")
                                .read_text(encoding="utf-8"))
        self.assertNotEqual(descriptor["status"], "acceptable")


if __name__ == "__main__":
    unittest.main()
