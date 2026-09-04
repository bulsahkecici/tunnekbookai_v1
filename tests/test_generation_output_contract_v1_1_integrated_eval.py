"""Tests for the Output Contract v1.1 integrated re-evaluation (replay + fresh confirmation)."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "data/evaluation"
REPLAY = EV / "generation_output_contract_v1_1_replay_results.jsonl"
V1_RESULTS = EV / "generation_output_contract_eval_results_v1.jsonl"
V1_RAW = EV / "generation_output_contract_eval_raw_v1.jsonl"
FRESH_RAW = EV / "generation_output_contract_v1_1_fresh_raw.jsonl"
FRESH_RESULTS = EV / "generation_output_contract_v1_1_fresh_results.jsonl"
FRESH_CLAIMS = EV / "generation_output_contract_v1_1_fresh_claim_audit.jsonl"
MANIFEST = EV / "generation_output_contract_v1_1_eval_manifest.json"
CRITERIA = ROOT / "data/metadata/generation_output_contract_eval_acceptance_v1.json"

BENCHMARK_SHA = "1e6347b557d583b56882c4c05fd1c5453874b7a05e61205c9430a24a677b0cff"
PACKET_SHA = "0538705147cf543b45fe8e73d57828cbc341a9a5a1dd574bd0969a9326e54d7a"
PROMPT_V5_SHA = "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085"
CONTRACT_V1_SHA = "670031d116056485155fc9d5c3d12b472d91f6b1e7a34ed9b169166f3727ce7d"
CONTRACT_V1_1_SHA = "5ebf8fe90e3e5491ce07a9143f8fd377841defa2e0e7a09188f3a835b07bdef5"
CRITERIA_SHA = "2a46ed2147ec24dd4a1944e23a1b1a458cfe1997edd13773eaf66692f417b6f8"

NON_LANGUAGE_FIELDS = [
    "malformed_citations", "unknown_handles", "citation_syntax_valid", "doc_leaks", "page_leaks",
    "slide_leaks", "path_leaks", "template_leaks", "thinking_marker_leaks", "material_claim_count",
    "claims_with_citation", "citation_coverage", "citation_coverage_status", "abstention_detected",
    "actual_abstention_marker", "marker_at_start", "expected_abstention_marker",
    "marker_language_valid", "validator_version", "repair_policy", "raw_answer_sha",
]
REJECTED = {"GEV042", "GEV061", "GEV062"}


def load_script(file_name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "scripts" / file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


analysis = load_script("33_output_contract_v1_1_eval_analysis.py", "oc_v11_analysis")


def rows(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def by_id(path):
    return {r["query_id"]: r for r in rows(path)}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TestFrozenIdentities(unittest.TestCase):
    def test_benchmark_and_packets(self):
        self.assertEqual(sha(EV / "generation_eval_benchmark_v2.jsonl"), BENCHMARK_SHA)
        self.assertEqual(sha(EV / "generation_eval_benchmark_v2_packets.jsonl"), PACKET_SHA)

    def test_system_prompt_v5_and_no_v6(self):
        self.assertEqual(sha(ROOT / "data/metadata/generation_system_prompt_v5.txt"), PROMPT_V5_SHA)
        self.assertFalse((ROOT / "data/metadata/generation_system_prompt_v6.txt").exists())

    def test_contract_v1_still_frozen(self):
        self.assertEqual(sha(ROOT / "scripts/26_generation_output_contract.py"), CONTRACT_V1_SHA)

    def test_contract_v1_1_unchanged_during_evaluation(self):
        self.assertEqual(sha(ROOT / "scripts/31_generation_output_contract_v1_1.py"),
                         CONTRACT_V1_1_SHA)
        meta = json.loads((ROOT / "data/metadata/generation_output_contract_v1_1.json")
                          .read_text(encoding="utf-8"))
        self.assertEqual(meta["implementation_sha"], CONTRACT_V1_1_SHA)
        self.assertEqual(meta["status"], "frozen")

    def test_acceptance_criteria_not_relaxed(self):
        self.assertEqual(sha(CRITERIA), CRITERIA_SHA)
        criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
        self.assertEqual(criteria["primary_metric"]["threshold"], 0.95)
        gates = {g["metric"]: g["threshold"] for g in criteria["stack_gates"]}
        self.assertEqual(gates["contract_false_positive_rate"], 0.02)
        self.assertEqual(gates["contract_false_negative_count"], 0)

    def test_historical_v1_results_untouched(self):
        manifest_v1 = json.loads((EV / "generation_output_contract_eval_manifest_v1.json")
                                 .read_text(encoding="utf-8"))
        self.assertEqual(sha(V1_RESULTS), manifest_v1["contract_result_sha"])
        self.assertEqual(sha(V1_RAW), manifest_v1["raw_result_sha"])


class TestReplayIntegrity(unittest.TestCase):
    def test_72_replay_rows(self):
        self.assertEqual(len(rows(REPLAY)), 72)

    def test_replay_used_the_frozen_raw_answers_unmodified(self):
        replay, raw = by_id(REPLAY), by_id(V1_RAW)
        self.assertEqual(set(replay), set(raw))
        for query_id, row in replay.items():
            self.assertEqual(row["raw_answer_sha"], raw[query_id]["raw_answer_sha"])

    def test_replay_carries_v1_1_contract_identity(self):
        for row in rows(REPLAY):
            self.assertEqual(row["contract_version"], "tunnelbook-generation-output-contract-v1.1")
            self.assertEqual(row["contract_sha256"], CONTRACT_V1_1_SHA)
            self.assertEqual(row["parent_contract_sha256"], CONTRACT_V1_SHA)
            self.assertEqual(row["repair_policy"], "none_fail_closed")

    def test_no_rewritten_answer_field(self):
        for path in (REPLAY, FRESH_RESULTS, FRESH_RAW):
            for row in rows(path):
                for key in row:
                    self.assertNotIn("rewritten", key)
                    self.assertNotIn("repaired", key)
                    self.assertNotIn("translated", key)


class TestDecisionDelta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.replay, cls.historical = by_id(REPLAY), by_id(V1_RESULTS)

    def test_exactly_one_decision_change_and_it_is_gev018(self):
        changed = [q for q in self.replay
                   if self.replay[q]["contract_valid"] != self.historical[q]["contract_valid"]]
        self.assertEqual(changed, ["GEV018"])
        self.assertFalse(self.historical["GEV018"]["contract_valid"])
        self.assertTrue(self.replay["GEV018"]["contract_valid"])

    def test_no_accept_to_reject_regressions(self):
        regressions = [q for q in self.replay
                       if self.historical[q]["contract_valid"]
                       and not self.replay[q]["contract_valid"]]
        self.assertEqual(regressions, [])

    def test_gev018_body_language_corrected(self):
        self.assertEqual(self.historical["GEV018"]["answer_body_language"], "tr")
        self.assertEqual(self.replay["GEV018"]["answer_body_language"], "en")
        self.assertEqual(self.replay["GEV018"]["failure_reasons"], [])

    def test_genuine_failures_preserved(self):
        self.assertIn("malformed_citation", self.replay["GEV042"]["failure_reasons"])
        self.assertIn("wrong_abstention_marker_language", self.replay["GEV061"]["failure_reasons"])
        self.assertEqual(sorted(self.replay["GEV062"]["failure_reasons"]),
                         ["answer_body_language_mismatch", "wrong_abstention_marker_language"])

    def test_gev061_body_not_falsely_flagged(self):
        self.assertEqual(self.replay["GEV061"]["answer_body_language"], "tr")
        self.assertTrue(self.replay["GEV061"]["body_language_valid"])

    def test_zero_non_language_semantic_drift(self):
        for query_id, new in self.replay.items():
            old = self.historical[query_id]
            drift = [f for f in NON_LANGUAGE_FIELDS if old[f] != new[f]]
            self.assertEqual(drift, [], query_id)

    def test_only_one_body_language_verdict_changed(self):
        changed = [q for q in self.replay
                   if self.replay[q]["answer_body_language"]
                   != self.historical[q]["answer_body_language"]]
        self.assertEqual(changed, ["GEV018"])


class TestReplayMetricsAndGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = analysis.analyse(REPLAY, V1_RAW)
        cls.gates = analysis.gate_evaluation(cls.m)

    def test_accept_rate(self):
        self.assertEqual(self.m["accepted_count"], 69)
        self.assertEqual(self.m["first_pass_contract_accept_rate"], 0.9583)

    def test_every_rejection_was_manually_reviewed(self):
        self.assertEqual(set(self.m["rejected_ids"]), REJECTED)

    def test_no_false_positives(self):
        self.assertEqual(self.m["contract_false_positive_count"], 0)
        self.assertEqual(self.m["contract_false_positive_rate"], 0.0)
        self.assertEqual(analysis.CONTRACT_FALSE_POSITIVES, set())

    def test_false_negative_count_recomputed_independently(self):
        contract = by_id(REPLAY)
        accepted = [q for q in contract if contract[q]["contract_valid"]]
        recomputed = [q for q in accepted
                      if contract[q]["malformed_citations"] or contract[q]["unknown_handles"]
                      or contract[q]["template_leaks"] or contract[q]["thinking_marker_leaks"]
                      or contract[q]["doc_leaks"] or contract[q]["page_leaks"]
                      or contract[q]["slide_leaks"] or contract[q]["path_leaks"]
                      or contract[q]["body_language_valid"] is False
                      or (contract[q]["abstention_detected"]
                          and contract[q]["marker_language_valid"] is False)]
        self.assertEqual(recomputed, [])
        self.assertEqual(self.m["contract_false_negative_count"], 0)

    def test_claim_labels_were_reusable_because_bytes_matched(self):
        self.assertTrue(self.m["claim_labels_reusable"])
        self.assertEqual(self.m["unresolved_claims"], 0)

    def test_all_replay_gates_pass(self):
        failed = [g["metric"] for g in self.gates if not g["passed"]]
        self.assertEqual(failed, [])

    def test_latency_gates(self):
        self.assertLessEqual(self.m["contract_latency_ms"]["median"], 50)
        self.assertLessEqual(self.m["contract_latency_ms"]["p95"], 200)

    def test_coverage_is_telemetry_not_a_gate(self):
        criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
        for entry in criteria["telemetry_only"]:
            self.assertFalse(entry["hard_gate"])
        for row in rows(REPLAY):
            self.assertNotIn("citation_coverage", row["failure_reasons"])


class TestFreshConfirmation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = analysis.analyse(FRESH_RESULTS, FRESH_RAW, FRESH_CLAIMS)
        cls.gates = analysis.gate_evaluation(cls.m)

    def test_72_fresh_rows(self):
        self.assertEqual(len(rows(FRESH_RAW)), 72)
        self.assertEqual(len(rows(FRESH_RESULTS)), 72)

    def test_fresh_checkpoint_identity(self):
        required = {"query_id", "benchmark_sha", "packet_artifact_sha", "context_packet_sha",
                    "system_prompt_version", "system_prompt_sha", "model_id", "tokenizer_sha",
                    "template_sha", "generation_config_hash", "output_contract_version",
                    "output_contract_sha"}
        for row in rows(FRESH_RAW):
            identity = row["checkpoint_identity"]
            self.assertTrue(required <= set(identity), row["query_id"])
            self.assertEqual(identity["output_contract_sha"], CONTRACT_V1_1_SHA)
            self.assertEqual(identity["system_prompt_sha"], PROMPT_V5_SHA)
            self.assertEqual(identity["benchmark_sha"], BENCHMARK_SHA)

    def test_fresh_raw_sha_matches_stored_text(self):
        for row in rows(FRESH_RAW):
            self.assertEqual(hashlib.sha256(row["raw_answer"].encode("utf-8")).hexdigest(),
                             row["raw_answer_sha"], row["query_id"])

    def test_fresh_prompt_accounting_exact(self):
        self.assertEqual(max(abs(r["prompt_token_delta"]) for r in rows(FRESH_RAW)), 0)

    def test_fresh_accept_rate_and_rejections(self):
        self.assertEqual(self.m["accepted_count"], 69)
        self.assertEqual(self.m["first_pass_contract_accept_rate"], 0.9583)
        self.assertEqual(set(self.m["rejected_ids"]), REJECTED)

    def test_fresh_claim_audit_fully_resolved(self):
        claims = rows(FRESH_CLAIMS)
        self.assertTrue(claims)
        self.assertTrue(all(c["resolved"] for c in claims))
        self.assertEqual(sum(1 for c in claims if c["claim_label"] is None), 0)
        self.assertEqual(self.m["unresolved_claims"], 0)

    def test_fresh_claim_audit_used_no_llm(self):
        allowed = {"deterministic_verified", "manual_evidence_verified",
                   "manual_evidence_verified_carried_identical_answer"}
        for claim in rows(FRESH_CLAIMS):
            self.assertIn(claim["label_method"], allowed)

    def test_fresh_no_false_negatives(self):
        self.assertEqual(self.m["contract_false_negative_count"], 0)
        self.assertEqual(self.m["catastrophic_failure_count"], 0)

    def test_all_fresh_gates_pass(self):
        failed = [g["metric"] for g in self.gates if not g["passed"]]
        self.assertEqual(failed, [])


class TestReplayVsFreshStability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fresh_raw, cls.replay_raw = by_id(FRESH_RAW), by_id(V1_RAW)
        cls.fresh, cls.replay = by_id(FRESH_RESULTS), by_id(REPLAY)

    def test_decisions_are_stable(self):
        for query_id in self.fresh:
            self.assertEqual(self.fresh[query_id]["contract_valid"],
                             self.replay[query_id]["contract_valid"], query_id)
            self.assertEqual(sorted(self.fresh[query_id]["failure_reasons"]),
                             sorted(self.replay[query_id]["failure_reasons"]), query_id)

    def test_body_language_and_citations_stable(self):
        for query_id in self.fresh:
            self.assertEqual(self.fresh[query_id]["answer_body_language"],
                             self.replay[query_id]["answer_body_language"], query_id)
            self.assertEqual(self.fresh[query_id]["malformed_citations"],
                             self.replay[query_id]["malformed_citations"], query_id)

    def test_generation_is_near_but_not_fully_deterministic(self):
        """71/72 reproduce byte-identically; GEV005 alternates between two equivalent forms."""
        differing = sorted(q for q in self.fresh_raw
                           if self.fresh_raw[q]["raw_answer_sha"]
                           != self.replay_raw[q]["raw_answer_sha"])
        self.assertEqual(differing, ["GEV005"])
        self.assertTrue(self.fresh["GEV005"]["contract_valid"])
        self.assertTrue(self.replay["GEV005"]["contract_valid"])

    def test_rejected_answers_are_byte_identical_so_retry_was_not_rerun(self):
        for query_id in REJECTED:
            self.assertEqual(self.fresh_raw[query_id]["raw_answer_sha"],
                             self.replay_raw[query_id]["raw_answer_sha"])
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertFalse(manifest["same_config_retry_rerun"])


class TestManifestAndEnvironment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_hashes_match_artifacts(self):
        self.assertEqual(self.manifest["replay_artifact_sha"], sha(REPLAY))
        self.assertEqual(self.manifest["fresh_raw_sha"], sha(FRESH_RAW))
        self.assertEqual(self.manifest["fresh_contract_result_sha"], sha(FRESH_RESULTS))
        self.assertEqual(self.manifest["fresh_claim_audit_sha"], sha(FRESH_CLAIMS))
        self.assertEqual(self.manifest["acceptance_criteria_sha"], CRITERIA_SHA)
        self.assertEqual(self.manifest["contract_v1_1_sha"], CONTRACT_V1_1_SHA)
        self.assertEqual(self.manifest["contract_v1_sha"], CONTRACT_V1_SHA)

    def test_manifest_records_both_decisions(self):
        self.assertEqual(self.manifest["replay_decision"], "GO")
        self.assertEqual(self.manifest["fresh_decision"], "GO")
        self.assertEqual(self.manifest["stack_decision"], "GO")
        self.assertEqual(self.manifest["v1_to_v1_1_decision_delta"]["reject_to_accept"], ["GEV018"])
        self.assertEqual(self.manifest["v1_to_v1_1_decision_delta"]["accept_to_reject"], [])
        self.assertEqual(self.manifest["v1_to_v1_1_decision_delta"]["non_language_semantic_drift"], 0)

    def test_qdrant_unchanged(self):
        self.assertEqual(self.manifest["qdrant_points_before"], 5992)
        self.assertEqual(self.manifest["qdrant_points_after"], 5992)
        self.assertEqual(self.manifest["qdrant_writes"], 0)
        with urllib.request.urlopen(
                "http://localhost:6333/collections/tunnelbook_dense_v1", timeout=10) as response:
            result = json.loads(response.read())["result"]
        self.assertEqual(result["points_count"], 5992)
        self.assertEqual(result["status"], "green")

    def test_raw_generator_not_upgraded(self):
        descriptor = json.loads((ROOT / "data/metadata/generation_candidate_v1.json")
                                .read_text(encoding="utf-8"))
        self.assertNotEqual(descriptor["status"], "acceptable")
        self.assertIn("NEEDS IMPROVEMENT", self.manifest["raw_generator_status"])


if __name__ == "__main__":
    unittest.main()
