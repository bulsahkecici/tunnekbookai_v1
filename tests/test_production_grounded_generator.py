"""Tests for the production grounded generator v1 orchestration layer.

The security-relevant assertions are the ones about what is NOT done: no repair, no retry, no
release of a contract-invalid answer, no raw rejected text in production logs, no Qdrant writes.

Live-model tests are gated behind TUNNELBOOK_LIVE_MODEL=1 so the normal suite runs offline.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = os.environ.get("TUNNELBOOK_LIVE_MODEL") == "1"
SMOKE = ROOT / "data/evaluation/production_orchestration_smoke_v1.jsonl"
DESCRIPTOR = ROOT / "data/metadata/production_grounded_generator_v1.json"

PROMPT_V5_SHA = "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085"
CONTRACT_V1_1_SHA = "5ebf8fe90e3e5491ce07a9143f8fd377841defa2e0e7a09188f3a835b07bdef5"
RETRIEVER_SCRIPT_SHA = "8ada31f64d8ef51c3b4d3b8b04f3fcc3e9fb7338b1554d1a5a9118a3a231b071"


def load_script(file_name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "scripts" / file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


orch = load_script("36_production_grounded_generator.py", "production_generator")


class _FakePacket:
    """Minimal stand-in so the accept/reject policy can be tested without retrieval or a model."""

    def __init__(self, evidence_ids=("E001", "E002")):
        self.context_text = "\n".join(f"=== {e} ===\nevidence body text" for e in evidence_ids)
        self.token_count = 100
        self.token_budget = orch.DEFAULT_CONTEXT_TOKEN_BUDGET
        self.selected_count = len(evidence_ids)
        self.insufficient_evidence = False
        self.evidence_items = tuple(
            type("Item", (), {
                "evidence_id": e, "chunk_id": f"DOC000001-C{i:04d}", "document_id": "DOC000001",
                "title": "t", "citation_mode": "document_section",
                "provenance_status": "source_only", "original_page_start": None,
                "original_page_end": None, "slide_start": None, "slide_end": None,
                "source_relative_path": "src/doc.pdf", "retrieval_rank": i + 1,
                "retrieval_score": 0.5, "text": "evidence body text"})()
            for i, e in enumerate(evidence_ids))

    def to_json(self, indent=None):
        return json.dumps({"evidence": [i.evidence_id for i in self.evidence_items]},
                          sort_keys=True)


def build_offline_runtime(tmp: Path, answer: str, debug_save_raw: bool = False):
    """A runtime with services unverified, retrieval stubbed and generation stubbed."""
    runtime = orch.ProductionGroundedGenerator(verify_services=False, debug_save_raw=debug_save_raw)
    runtime.build_packet = lambda request: _FakePacket()
    orch.gen.complete = lambda prompt, config, max_tokens, **kw: {
        "text": answer, "finish_reason": "stop",
        "usage": {"prompt_tokens": runtime.tokenizer.count(prompt), "completion_tokens": 10},
        "latency_seconds": 0.0}
    orch.AUDIT_LOG = tmp / "generation_audit_v1.jsonl"
    orch.ACCEPTED_LOG = tmp / "accepted_generations_v1.jsonl"
    orch.REJECTED_LOG = tmp / "rejected_generations_v1.jsonl"
    orch.DEBUG_RAW_LOG = tmp / "debug_raw_generations_v1.jsonl"
    return runtime


class TestFrozenStartup(unittest.TestCase):
    def test_frozen_identities_verified(self):
        tokenizer = orch.gen.GenerationTokenizer()
        renderer = orch.gen.TemplateRenderer()
        identity = orch.verify_frozen_identities(tokenizer, renderer)
        self.assertTrue(identity["ok"], identity["failures"])

    def test_pinned_shas(self):
        self.assertEqual(orch.PROMPT_V5_SHA, PROMPT_V5_SHA)
        self.assertEqual(orch.CONTRACT_V1_1_SHA, CONTRACT_V1_1_SHA)
        self.assertEqual(orch.RETRIEVER_SCRIPT_SHA, RETRIEVER_SCRIPT_SHA)
        self.assertEqual(
            hashlib.sha256((ROOT / "scripts/31_generation_output_contract_v1_1.py").read_bytes())
            .hexdigest(), CONTRACT_V1_1_SHA)
        self.assertEqual(
            hashlib.sha256((ROOT / "data/metadata/generation_system_prompt_v5.txt").read_bytes())
            .hexdigest(), PROMPT_V5_SHA)

    def test_startup_refuses_on_identity_mismatch(self):
        original = orch.contract.CONTRACT_VERSION
        try:
            orch.contract.CONTRACT_VERSION = "tampered"
            with self.assertRaises(orch.StartupRefused):
                orch.ProductionGroundedGenerator(verify_services=False)
        finally:
            orch.contract.CONTRACT_VERSION = original

    def test_delegates_rather_than_reimplements(self):
        self.assertEqual(orch.retriever_v1.RELEASE_NAME, "tunnelbook-retriever-v1")
        self.assertEqual(orch.rag_context.CONTEXT_CONTRACT_VERSION, "tunnelbook-context-v1")
        self.assertEqual(orch.contract.CONTRACT_VERSION,
                         "tunnelbook-generation-output-contract-v1.1")
        self.assertEqual(orch.contract.REPAIR_POLICY, "none_fail_closed")
        source = (ROOT / "scripts/36_production_grounded_generator.py").read_text(encoding="utf-8")
        for forbidden in ("def validate_citations", "def assemble_context", "def build_evidence",
                          "def embed_query", "def enforce("):
            self.assertNotIn(forbidden, source)

    def test_generation_config_is_frozen(self):
        self.assertEqual((orch.TEMPERATURE, orch.SEED, orch.MAX_TOKENS), (0.0, 11, 3072))
        self.assertEqual(orch.LOADED_CONTEXT, 71936)
        self.assertEqual(orch.MODEL_ID, "qwen3.6-35b-a3b-mlx")
        self.assertEqual(list(orch.gen.STOP_STRINGS), ["<|im_end|>", "<|im_start|>"])


class TestRequestSchema(unittest.TestCase):
    def test_request_id_autogenerated(self):
        request = orch.ProductionGenerationRequest(query="tünel")
        self.assertTrue(request.request_id)
        self.assertNotEqual(request.request_id,
                            orch.ProductionGenerationRequest(query="tünel").request_id)

    def test_empty_query_rejected(self):
        for bad in ("", "   ", None, 5):
            with self.assertRaises(orch.RequestRejected):
                orch.ProductionGenerationRequest(query=bad)

    def test_unsupported_language_rejected(self):
        with self.assertRaises(orch.RequestRejected):
            orch.ProductionGenerationRequest(query="q", query_language="de")

    def test_top_k_bounds_enforced(self):
        with self.assertRaises(orch.RequestRejected):
            orch.ProductionGenerationRequest(query="q", top_k=0)
        with self.assertRaises(orch.RequestRejected):
            orch.ProductionGenerationRequest(query="q", top_k=10_000)

    def test_defaults_match_frozen_production_values(self):
        request = orch.ProductionGenerationRequest(query="q")
        self.assertEqual(request.top_k, 20)
        self.assertEqual(request.top_k, orch.rag_context.DEFAULT_RETRIEVAL_TOP_K)
        self.assertEqual(request.context_token_budget, 64610)


class TestQueryLanguage(unittest.TestCase):
    def setUp(self):
        self.runtime = orch.ProductionGroundedGenerator(verify_services=False)

    def test_explicit_language_is_used(self):
        request = orch.ProductionGenerationRequest(query="anything at all", query_language="en")
        self.assertEqual(self.runtime.resolve_language(request), ("en", "provided"))

    def test_detection_is_delegated_to_the_contract(self):
        self.assertIs(orch.detect_query_language.__wrapped__
                      if hasattr(orch.detect_query_language, "__wrapped__")
                      else orch.contract.detect_language, orch.contract.detect_language)

    def test_ambiguous_query_is_rejected_not_guessed(self):
        request = orch.ProductionGenerationRequest(query="12345 6789 ::: --- +++")
        with self.assertRaises(orch.RequestRejected) as caught:
            self.runtime.resolve_language(request)
        self.assertIn("query_language_ambiguous", str(caught.exception))


class TestAcceptPath(unittest.TestCase):
    ANSWER = ("The initial shotcrete lining is applied immediately after excavation and it "
              "provides support pressure to the ground [E001]. The membrane is installed "
              "between the initial support and the final lining [E002].")

    def test_accept_releases_answer_with_handles(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = build_offline_runtime(Path(tmp), self.ANSWER)
            result = runtime.generate(orch.ProductionGenerationRequest(
                query="What is the shotcrete lining for?", query_language="en"))
            self.assertEqual(result.status, "accepted")
            self.assertEqual(result.answer, self.ANSWER)
            self.assertEqual(result.evidence_handles, ["E001", "E002"])
            self.assertIsNone(result.safe_message)
            public = result.to_public_dict()
            self.assertIn("answer", public)
            self.assertIn("[E001]", public["answer"])

    def test_accept_writes_audit_and_accepted_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runtime = build_offline_runtime(tmp_path, self.ANSWER)
            result = runtime.generate(orch.ProductionGenerationRequest(
                query="What is the shotcrete lining for?", query_language="en"))
            audit = [json.loads(l) for l in (tmp_path / "generation_audit_v1.jsonl")
                     .read_text(encoding="utf-8").splitlines()]
            accepted = [json.loads(l) for l in (tmp_path / "accepted_generations_v1.jsonl")
                        .read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(audit), 1)
            self.assertEqual(audit[0]["production_action"], "accept")
            self.assertEqual(audit[0]["audit_id"], result.audit_id)
            self.assertEqual(len(accepted), 1)
            self.assertEqual(accepted[0]["visible_evidence_handles"], ["E001", "E002"])
            self.assertTrue(accepted[0]["internal_provenance"])

    def test_raw_answer_sha_preserved_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runtime = build_offline_runtime(tmp_path, self.ANSWER)
            runtime.generate(orch.ProductionGenerationRequest(
                query="q", query_language="en"))
            audit = json.loads((tmp_path / "generation_audit_v1.jsonl")
                               .read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(audit["raw_answer_sha"],
                             hashlib.sha256(self.ANSWER.encode("utf-8")).hexdigest())


class TestRejectPath(unittest.TestCase):
    MALFORMED = ("Kaya sınıflarına göre ilerleme boyu (E001) başlığı altında verilmiştir ve "
                 "bu değerler projeye göre değişmektedir [E002].")

    def _run(self, tmp, answer, language="tr"):
        runtime = build_offline_runtime(Path(tmp), answer)
        return runtime.generate(orch.ProductionGenerationRequest(
            query="Kaya sınıflarına göre ilerleme boyu nedir?", query_language=language))

    def test_contract_invalid_answer_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(tmp, self.MALFORMED)
            self.assertEqual(result.status, "rejected")
            self.assertIn("malformed_citation", result.failure_reasons)

    def test_rejected_answer_is_never_released(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(tmp, self.MALFORMED)
            self.assertIsNone(result.answer)
            public = result.to_public_dict()
            self.assertNotIn("answer", public)
            self.assertNotIn(self.MALFORMED[:40], json.dumps(public, ensure_ascii=False))

    def test_safe_message_is_deterministic_and_localised(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(tmp, self.MALFORMED, language="tr")
            self.assertEqual(result.safe_message,
                             "Bu yanıt doğrulama sözleşmesini geçemedi. Yanıt yayımlanmadı.")
        english = ("The value (E001) is given in the heading above and it is used for the "
                   "design of the tunnel lining [E002].")
        with tempfile.TemporaryDirectory() as tmp:
            runtime = build_offline_runtime(Path(tmp), english)
            result = runtime.generate(orch.ProductionGenerationRequest(
                query="What is the advance length?", query_language="en"))
            self.assertEqual(result.status, "rejected")
            self.assertEqual(result.safe_message,
                             "This response failed the output validation contract and was "
                             "not released.")

    def test_no_fabricated_replacement_answer(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(tmp, self.MALFORMED)
            self.assertIsNone(result.answer)
            self.assertEqual(result.evidence_handles, [])

    def test_rejected_raw_text_not_written_to_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self._run(tmp, self.MALFORMED)
            blob = ((tmp_path / "generation_audit_v1.jsonl").read_text(encoding="utf-8")
                    + (tmp_path / "rejected_generations_v1.jsonl").read_text(encoding="utf-8"))
            self.assertNotIn(self.MALFORMED[:40], blob)
            rejected = json.loads((tmp_path / "rejected_generations_v1.jsonl")
                                  .read_text(encoding="utf-8").splitlines()[0])
            self.assertNotIn("raw_answer", rejected)
            self.assertIn("raw_answer_sha", rejected)
            self.assertFalse((tmp_path / "accepted_generations_v1.jsonl").exists())

    def test_no_repair_of_malformed_citation(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runtime = build_offline_runtime(tmp_path, self.MALFORMED, debug_save_raw=True)
            runtime.generate(orch.ProductionGenerationRequest(
                query="q", query_language="tr"))
            debug = json.loads((tmp_path / "debug_raw_generations_v1.jsonl")
                               .read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(debug["raw_answer"], self.MALFORMED)   # untouched, not normalised
            self.assertIn("(E001)", debug["raw_answer"])

    def test_debug_artifact_is_off_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runtime = build_offline_runtime(tmp_path, self.MALFORMED)
            self.assertFalse(runtime.debug_save_raw)
            runtime.generate(orch.ProductionGenerationRequest(query="q", query_language="tr"))
            self.assertFalse((tmp_path / "debug_raw_generations_v1.jsonl").exists())


class TestNoRetryNoRepair(unittest.TestCase):
    def test_retry_policy_defaults_disabled(self):
        policy = orch.RetryPolicy()
        self.assertFalse(policy.enabled)
        self.assertEqual(policy.kind, "disabled")
        self.assertEqual(policy.max_attempts, 1)

    def test_enabling_retry_is_refused(self):
        with self.assertRaises(orch.StartupRefused):
            orch.RetryPolicy(enabled=True)

    def test_generation_called_exactly_once_per_request(self):
        calls = []
        answer = "The lining is installed after excavation [E001] and sealed [E002]."
        with tempfile.TemporaryDirectory() as tmp:
            runtime = build_offline_runtime(Path(tmp), answer)
            inner = orch.gen.complete
            orch.gen.complete = lambda *a, **k: (calls.append(1), inner(*a, **k))[1]
            runtime.generate(orch.ProductionGenerationRequest(query="q", query_language="en"))
            self.assertEqual(len(calls), 1)

    def test_rejected_request_does_not_retrieve_again(self):
        malformed = "Değer (E001) başlığında verilmiştir ve projeye göre değişmektedir [E002]."
        retrievals = []
        with tempfile.TemporaryDirectory() as tmp:
            runtime = build_offline_runtime(Path(tmp), malformed)
            packet = _FakePacket()
            runtime.build_packet = lambda request: (retrievals.append(1), packet)[1]
            result = runtime.generate(orch.ProductionGenerationRequest(
                query="q", query_language="tr"))
            self.assertEqual(result.status, "rejected")
            self.assertEqual(len(retrievals), 1)

    def test_contract_receives_the_raw_answer_unmodified(self):
        """The strongest no-repair assertion available: intercept what enforce() actually sees."""
        malformed = "Değer (E001) başlığında verilmiştir ve projeye göre değişmektedir [E002]."
        seen = {}
        original = orch.contract.enforce
        with tempfile.TemporaryDirectory() as tmp:
            runtime = build_offline_runtime(Path(tmp), malformed)
            def spy(answer, language, evidence, **kw):
                seen["answer"] = answer
                return original(answer, language, evidence, **kw)
            orch.contract.enforce = spy
            try:
                result = runtime.generate(orch.ProductionGenerationRequest(
                    query="q", query_language="tr"))
            finally:
                orch.contract.enforce = original
        self.assertEqual(seen["answer"], malformed)
        self.assertIn("(E001)", seen["answer"])          # malformed form reached the contract intact
        self.assertEqual(result.status, "rejected")

    def test_no_marker_or_citation_rewriting_helpers_exist(self):
        source = (ROOT / "scripts/36_production_grounded_generator.py").read_text(encoding="utf-8")
        self.assertIn("none_fail_closed", source)
        for forbidden in ("raw_answer =", "raw_answer.replace", "answer = answer.replace",
                          "re.sub(", "translate("):
            self.assertNotIn(forbidden, source.split("raw_answer = response[\"text\"]")[-1])


class TestSecurityBoundaries(unittest.TestCase):
    def test_query_cannot_corrupt_jsonl_logs(self):
        answer = "The lining is installed [E001] and inspected [E002]."
        nasty = 'evil"}\n{"injected": true, "query": "x\r\n\\u0000 --top-k 999'
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runtime = build_offline_runtime(tmp_path, answer)
            runtime.generate(orch.ProductionGenerationRequest(query=nasty, query_language="en"))
            lines = (tmp_path / "generation_audit_v1.jsonl").read_text(
                encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            row = json.loads(lines[0])
            self.assertEqual(row["query"], nasty)
            self.assertNotIn("injected", row)

    def test_query_is_never_interpolated_into_commands_or_paths(self):
        source = (ROOT / "scripts/36_production_grounded_generator.py").read_text(encoding="utf-8")
        for forbidden in ("os.system", "subprocess.", "eval(", "exec(", "__import__",
                          "shell=True", "os.popen"):
            self.assertNotIn(forbidden, source)

    def test_logs_written_via_json_dumps_only(self):
        source = (ROOT / "scripts/36_production_grounded_generator.py").read_text(encoding="utf-8")
        self.assertIn("json.dumps(row, ensure_ascii=False, sort_keys=True)", source)

    def test_evidence_stays_untrusted_data(self):
        self.assertIn("UNTRUSTED", orch.rag_context.INJECTION_NOTICE.upper())
        self.assertIn("EVIDENCE", orch.rag_context.EVIDENCE_BEGIN.upper())

    def test_qdrant_is_never_written(self):
        source = (ROOT / "scripts/36_production_grounded_generator.py").read_text(encoding="utf-8")
        for forbidden in ("upsert", "delete_collection", "create_collection", "set_payload",
                          "delete_points", "recreate_collection"):
            self.assertNotIn(forbidden, source)


class TestHealthcheckAndDryRun(unittest.TestCase):
    def test_healthcheck_reports_structured_status(self):
        report = orch.healthcheck()
        self.assertIn(report["status"], ("healthy", "unhealthy"))
        self.assertIn("frozen_identities", report["checks"])
        self.assertIn("qdrant", report["checks"])
        self.assertIn("lm_studio", report["checks"])
        self.assertEqual(report["version"], orch.VERSION)

    def test_dry_run_never_calls_generation(self):
        calls = []
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runtime = build_offline_runtime(tmp_path, "unused")
            orch.gen.complete = lambda *a, **k: calls.append(1)
            result = runtime.generate(orch.ProductionGenerationRequest(
                query="q", query_language="tr"), dry_run=True)
            self.assertEqual(calls, [])
            self.assertEqual(result.status, "dry_run")
            self.assertIsNone(result.answer)
            self.assertTrue(result.context_packet_sha)
            audit = json.loads((tmp_path / "generation_audit_v1.jsonl")
                               .read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(audit["production_action"], "dry_run")
            self.assertIsNone(audit["raw_answer_sha"])


class TestSmokeSuiteArtifacts(unittest.TestCase):
    def test_smoke_suite_shape(self):
        cases = [json.loads(l) for l in SMOKE.read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertEqual(len(cases), 16)
        groups = {}
        for case in cases:
            groups[case["group"]] = groups.get(case["group"], 0) + 1
        self.assertEqual(groups["factual"], 4)
        self.assertEqual(groups["numeric"], 2)
        self.assertEqual(groups["multi_source"], 2)
        self.assertEqual(groups["cross_lingual"], 2)
        self.assertEqual(groups["must_abstain"], 2)
        self.assertEqual(groups["adversarial"], 2)
        self.assertEqual(groups["contract_failure_diagnostic"], 2)

    def test_contract_failure_cases_use_frozen_fixtures(self):
        cases = [json.loads(l) for l in SMOKE.read_text(encoding="utf-8").splitlines() if l.strip()]
        fixtures = [c for c in cases if c["mode"] == "fixture"]
        self.assertEqual(len(fixtures), 2)
        raw = {r["query_id"]: r["raw_answer"] for r in
               (json.loads(l) for l in
                (ROOT / "data/evaluation/generation_output_contract_eval_raw_v1.jsonl")
                .read_text(encoding="utf-8").splitlines() if l.strip())}
        for case in fixtures:
            self.assertEqual(case["fixture_raw_answer"], raw[case["fixture_source"]])
            self.assertEqual(case["expected_status"], "rejected")

    def test_smoke_report_all_passed_and_no_leak(self):
        report_path = ROOT / "data/production/orchestration_smoke_report_v1.json"
        if not report_path.exists():
            self.skipTest("smoke run has not been executed in this environment")
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(report["failed"], 0)
        self.assertEqual(report["passed"], report["cases"])
        self.assertEqual(report["contract_failures_released"], 0)
        self.assertEqual(report["qdrant_writes"], 0)
        self.assertEqual(report["qdrant_before"]["points"], 5992)
        self.assertEqual(report["qdrant_after"]["points"], 5992)


class TestDescriptor(unittest.TestCase):
    def test_descriptor_identity(self):
        if not DESCRIPTOR.exists():
            self.skipTest("descriptor not yet written")
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        self.assertEqual(descriptor["version"], "tunnelbook-production-grounded-generator-v1")
        self.assertEqual(descriptor["entrypoint"], "scripts/36_production_grounded_generator.py")
        self.assertEqual(descriptor["production_policy"], "accept_if_contract_valid_else_reject")
        self.assertEqual(descriptor["retry_policy"]["enabled"], False)
        self.assertEqual(descriptor["output_contract"]["sha256"], CONTRACT_V1_1_SHA)
        self.assertEqual(descriptor["prompt"]["sha256"], PROMPT_V5_SHA)
        self.assertIn("citation_coverage", json.dumps(descriptor["known_limitations"]))

    def test_raw_generator_status_not_upgraded(self):
        candidate = json.loads((ROOT / "data/metadata/generation_candidate_v1.json")
                               .read_text(encoding="utf-8"))
        self.assertNotEqual(candidate["status"], "acceptable")
        if DESCRIPTOR.exists():
            descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
            self.assertIn("NEEDS IMPROVEMENT", descriptor["raw_generator_status"])


@unittest.skipUnless(LIVE, "live model test; set TUNNELBOOK_LIVE_MODEL=1 to run")
class TestLiveIntegration(unittest.TestCase):
    def test_live_healthcheck_is_healthy(self):
        self.assertEqual(orch.healthcheck()["status"], "healthy")

    def test_live_dry_run(self):
        runtime = orch.ProductionGroundedGenerator()
        result = runtime.generate(orch.ProductionGenerationRequest(
            query="Tünelde püskürtme betonun işlevi nedir?", query_language="tr"), dry_run=True)
        self.assertEqual(result.status, "dry_run")
        self.assertTrue(result.evidence_handles)

    def test_live_end_to_end(self):
        result = orch.generate_grounded("Tünelde su yalıtımı membranı ne işe yarar?", "tr")
        self.assertIn(result.status, ("accepted", "rejected"))
        if result.status == "accepted":
            self.assertIn("[E", result.answer)
        else:
            self.assertIsNone(result.answer)


if __name__ == "__main__":
    unittest.main()
