"""Tests for the output-contract-integrated frozen benchmark v2 re-evaluation."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_script(file_name: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "scripts" / file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


EV = ROOT / "data/evaluation"
RAW = EV / "generation_output_contract_eval_raw_v1.jsonl"
CONTRACT = EV / "generation_output_contract_eval_results_v1.jsonl"
CLAIMS = EV / "generation_output_contract_claim_audit_v1.jsonl"
FIRST_PASS = EV / "generation_output_contract_first_pass_v1.jsonl"
RETRY = EV / "generation_output_contract_retry_same_config_v1.jsonl"
MANIFEST = EV / "generation_output_contract_eval_manifest_v1.json"
CRITERIA = ROOT / "data/metadata/generation_output_contract_eval_acceptance_v1.json"

BENCHMARK_SHA = "1e6347b557d583b56882c4c05fd1c5453874b7a05e61205c9430a24a677b0cff"
PACKET_SHA = "0538705147cf543b45fe8e73d57828cbc341a9a5a1dd574bd0969a9326e54d7a"
PROMPT_V5_SHA = "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085"
CONTRACT_SHA = "670031d116056485155fc9d5c3d12b472d91f6b1e7a34ed9b169166f3727ce7d"

analysis = load_script("29_output_contract_eval_analysis.py", "oc_eval_analysis")

FAILURE_REASON_ENUM = analysis.FAILURE_REASON_ENUM


def rows(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TestFrozenIdentities(unittest.TestCase):
    def test_benchmark_and_packets_unchanged(self):
        self.assertEqual(sha(EV / "generation_eval_benchmark_v2.jsonl"), BENCHMARK_SHA)
        self.assertEqual(sha(EV / "generation_eval_benchmark_v2_packets.jsonl"), PACKET_SHA)

    def test_system_prompt_v5_unchanged(self):
        self.assertEqual(sha(ROOT / "data/metadata/generation_system_prompt_v5.txt"), PROMPT_V5_SHA)

    def test_output_contract_unchanged(self):
        self.assertEqual(sha(ROOT / "scripts/26_generation_output_contract.py"), CONTRACT_SHA)

    def test_no_prompt_v6_was_created(self):
        self.assertFalse((ROOT / "data/metadata/generation_system_prompt_v6.txt").exists())

    def test_acceptance_criteria_frozen_before_execution(self):
        criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
        self.assertTrue(criteria["frozen_before_execution"])
        self.assertEqual(criteria["primary_metric"]["threshold"], 0.95)
        self.assertEqual(criteria["denominators"]["first_pass_denominator"], 72)


class TestArtifactShape(unittest.TestCase):
    def test_row_counts(self):
        self.assertEqual(len(rows(RAW)), 72)
        self.assertEqual(len(rows(CONTRACT)), 72)
        self.assertEqual(len(rows(FIRST_PASS)), 72)

    def test_query_ids_align_across_artifacts(self):
        ids = {r["query_id"] for r in rows(RAW)}
        self.assertEqual(ids, {c["query_id"] for c in rows(CONTRACT)})
        self.assertEqual(ids, {f["query_id"] for f in rows(FIRST_PASS)})
        self.assertEqual(len(ids), 72)

    def test_every_row_carries_full_checkpoint_identity(self):
        required = {"query_id", "benchmark_sha", "packet_artifact_sha", "context_packet_sha",
                    "system_prompt_version", "system_prompt_sha", "model_id", "tokenizer_sha",
                    "template_sha", "generation_config_hash", "output_contract_version",
                    "output_contract_sha"}
        for row in rows(RAW):
            self.assertTrue(required <= set(row["checkpoint_identity"]), row["query_id"])

    def test_contract_result_required_fields(self):
        required = {"contract_version", "contract_sha256", "repair_policy", "raw_answer_sha",
                    "query_language", "query_language_status", "abstention_detected",
                    "expected_abstention_marker", "actual_abstention_marker", "marker_at_start",
                    "marker_language_valid", "answer_body_language", "answer_body_language_status",
                    "body_language_valid", "malformed_citations", "unknown_handles",
                    "citation_syntax_valid", "doc_leaks", "page_leaks", "slide_leaks", "path_leaks",
                    "template_leaks", "thinking_marker_leaks", "material_claim_count",
                    "claims_with_citation", "citation_coverage", "citation_coverage_status",
                    "contract_valid", "failure_reasons"}
        for row in rows(CONTRACT):
            self.assertTrue(required <= set(row), row["query_id"])

    def test_contract_result_identity(self):
        for row in rows(CONTRACT):
            self.assertEqual(row["contract_version"], "tunnelbook-generation-output-contract-v1")
            self.assertEqual(row["contract_sha256"], CONTRACT_SHA)
            self.assertEqual(row["repair_policy"], "none_fail_closed")
            self.assertEqual(row["citation_coverage_status"], "telemetry_only_not_enforced")


class TestNoRepair(unittest.TestCase):
    def test_raw_answer_sha_preserved_through_contract(self):
        contract = {c["query_id"]: c for c in rows(CONTRACT)}
        for row in rows(RAW):
            verdict = contract[row["query_id"]]
            self.assertEqual(row["raw_answer_sha"], verdict["raw_answer_sha"])
            self.assertEqual(verdict["raw_answer_sha"], verdict["raw_answer_sha_before_contract"])

    def test_raw_answer_sha_matches_the_stored_text(self):
        for row in rows(RAW):
            digest = hashlib.sha256(row["raw_answer"].encode("utf-8")).hexdigest()
            self.assertEqual(digest, row["raw_answer_sha"], row["query_id"])

    def test_no_rewritten_answer_field_anywhere(self):
        for path in (RAW, CONTRACT, FIRST_PASS):
            for row in rows(path):
                for key in row:
                    self.assertNotIn("rewritten", key)
                    self.assertNotIn("repaired", key)
                    self.assertNotIn("normalised", key)
                    self.assertNotIn("corrected", key)

    def test_malformed_citations_were_reported_not_fixed(self):
        contract = {c["query_id"]: c for c in rows(CONTRACT)}
        raw = {r["query_id"]: r for r in rows(RAW)}
        self.assertEqual(contract["GEV042"]["malformed_citations"], ["E002", "E004", "E015"])
        self.assertIn("(E002)", raw["GEV042"]["raw_answer"])

    def test_wrong_marker_was_reported_not_replaced(self):
        raw = {r["query_id"]: r for r in rows(RAW)}
        self.assertTrue(raw["GEV061"]["raw_answer"].lstrip().startswith("INSUFFICIENT EVIDENCE"))
        self.assertTrue(raw["GEV062"]["raw_answer"].lstrip().startswith("INSUFFICIENT EVIDENCE"))


class TestFailureReasonsAndFirstPass(unittest.TestCase):
    def test_failure_reasons_are_all_in_the_enum(self):
        for row in rows(CONTRACT):
            self.assertTrue(set(row["failure_reasons"]) <= FAILURE_REASON_ENUM, row["query_id"])

    def test_contract_valid_iff_no_failure_reasons(self):
        for row in rows(CONTRACT):
            self.assertEqual(row["contract_valid"], not row["failure_reasons"], row["query_id"])

    def test_first_pass_action_consistent_with_contract_valid(self):
        contract = {c["query_id"]: c for c in rows(CONTRACT)}
        for row in rows(FIRST_PASS):
            expected = "accept" if contract[row["query_id"]]["contract_valid"] else "reject"
            self.assertEqual(row["production_action"], expected)
            self.assertIn(row["production_action"], {"accept", "reject"})
            self.assertEqual(row["failure_reasons"], contract[row["query_id"]]["failure_reasons"])

    def test_multi_failure_answers_are_not_collapsed(self):
        contract = {c["query_id"]: c for c in rows(CONTRACT)}
        self.assertEqual(sorted(contract["GEV062"]["failure_reasons"]),
                         ["answer_body_language_mismatch", "wrong_abstention_marker_language"])

    def test_known_defects_are_caught(self):
        contract = {c["query_id"]: c for c in rows(CONTRACT)}
        self.assertIn("malformed_citation", contract["GEV042"]["failure_reasons"])
        self.assertIn("wrong_abstention_marker_language", contract["GEV061"]["failure_reasons"])


class TestClaimAudit(unittest.TestCase):
    def test_every_claim_is_resolved(self):
        claims = rows(CLAIMS)
        self.assertTrue(claims)
        self.assertTrue(all(c["resolved"] for c in claims))
        self.assertEqual(sum(1 for c in claims if c["claim_label"] is None), 0)

    def test_labels_are_in_the_frozen_label_set(self):
        allowed = set(json.loads(CRITERIA.read_text(encoding="utf-8"))["claim_label_set"])
        for claim in rows(CLAIMS):
            self.assertIn(claim["claim_label"], allowed)

    def test_no_llm_judged_any_claim(self):
        allowed_methods = {"deterministic_verified", "manual_evidence_verified",
                           "manual_evidence_verified_carried_identical_answer"}
        for claim in rows(CLAIMS):
            self.assertIn(claim["label_method"], allowed_methods)

    def test_carried_labels_only_on_byte_identical_answers(self):
        for claim in rows(CLAIMS):
            if claim["label_method"] == "manual_evidence_verified_carried_identical_answer":
                self.assertTrue(claim["answer_byte_identical_to_phase_b_v2"], claim["query_id"])

    def test_partial_and_unsupported_labels_carry_written_reasons(self):
        for claim in rows(CLAIMS):
            if claim["claim_label"] == "PARTIALLY_SUPPORTED":
                self.assertTrue(claim["partial_reason"], f"{claim['query_id']} {claim['claim_id']}")
            if claim["claim_label"] == "UNSUPPORTED":
                self.assertTrue(claim["unsupported_reason"])

    def test_non_factual_claims_are_not_counted_as_material(self):
        for claim in rows(CLAIMS):
            if claim["claim_label"] == "NON_FACTUAL":
                self.assertFalse(claim["material"])


class TestMetrics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metrics, cls.accepted, cls.rejected = analysis.main()

    def test_first_pass_accept_rate_denominator_is_72(self):
        self.assertEqual(self.metrics["accepted_count"] + self.metrics["rejected_count"], 72)
        self.assertAlmostEqual(self.metrics["first_pass_contract_accept_rate"],
                               self.metrics["accepted_count"] / 72, places=4)

    def test_false_negative_count_computed_over_accepted_answers(self):
        contract = {c["query_id"]: c for c in rows(CONTRACT)}
        recomputed = [q for q in self.accepted
                      if contract[q]["malformed_citations"] or contract[q]["unknown_handles"]
                      or contract[q]["template_leaks"] or contract[q]["thinking_marker_leaks"]
                      or contract[q]["doc_leaks"] or contract[q]["page_leaks"]
                      or contract[q]["slide_leaks"] or contract[q]["path_leaks"]
                      or contract[q]["body_language_valid"] is False
                      or (contract[q]["abstention_detected"]
                          and contract[q]["marker_language_valid"] is False)]
        self.assertEqual(self.metrics["contract_false_negative_count"], len(recomputed))
        self.assertEqual(self.metrics["contract_false_negative_count"], 0)

    def test_false_positive_denominator_is_the_rejected_set(self):
        self.assertEqual(self.metrics["contract_false_positive_rate"],
                         round(self.metrics["contract_false_positive_count"]
                               / self.metrics["rejected_count"], 4))
        self.assertTrue(analysis.CONTRACT_FALSE_POSITIVES <= set(self.rejected))

    def test_every_rejected_answer_was_manually_reviewed(self):
        reviewed = analysis.CONTRACT_FALSE_POSITIVES | {"GEV042", "GEV061", "GEV062"}
        self.assertEqual(set(self.rejected), reviewed)

    def test_coverage_is_reported_but_never_a_rejection_reason(self):
        for row in rows(CONTRACT):
            self.assertNotIn("citation_coverage", row["failure_reasons"])
            self.assertIsNotNone(row["citation_coverage_status"])
        self.assertIsNotNone(self.metrics["all_answers_citation_coverage"])
        self.assertIsNotNone(self.metrics["pass_answer_citation_coverage"])

    def test_coverage_is_not_a_hard_gate(self):
        criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
        for entry in criteria["telemetry_only"]:
            self.assertFalse(entry["hard_gate"])

    def test_no_unsupported_material_claims(self):
        self.assertEqual(self.metrics["all_answers_unsupported_material_claim_rate"], 0.0)

    def test_prompt_accounting_delta_is_zero(self):
        self.assertEqual(self.metrics["prompt_token_delta_max"], 0)

    def test_gates_are_read_from_the_frozen_criteria(self):
        gates = analysis.gate_evaluation(self.metrics)
        failed = {g["metric"] for g in gates if not g["passed"]}
        self.assertEqual(failed, {"first_pass_contract_accept_rate",
                                  "contract_false_positive_rate"})


class TestRetry(unittest.TestCase):
    def test_retry_ran_only_on_rejected_items(self):
        rejected = {f["query_id"] for f in rows(FIRST_PASS)
                    if f["production_action"] == "reject"}
        self.assertEqual({r["query_id"] for r in rows(RETRY)}, rejected)

    def test_retry_is_a_single_extra_attempt(self):
        for row in rows(RETRY):
            self.assertEqual(row["attempt"], 2)

    def test_both_shas_are_tracked(self):
        raw = {r["query_id"]: r for r in rows(RAW)}
        for row in rows(RETRY):
            self.assertEqual(row["raw_answer_sha_original"], raw[row["query_id"]]["raw_answer_sha"])
            self.assertEqual(row["byte_identical"],
                             row["raw_answer_sha_original"] == row["raw_answer_sha_retry"])

    def test_same_config_retry_recovered_nothing(self):
        retry = rows(RETRY)
        self.assertTrue(all(r["byte_identical"] for r in retry))
        self.assertEqual(sum(1 for r in retry if r["recovered"]), 0)


class TestManifestAndEnvironment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_shas_match_artifacts(self):
        self.assertEqual(self.manifest["raw_result_sha"], sha(RAW))
        self.assertEqual(self.manifest["contract_result_sha"], sha(CONTRACT))
        self.assertEqual(self.manifest["claim_audit_sha"], sha(CLAIMS))
        self.assertEqual(self.manifest["first_pass_sha"], sha(FIRST_PASS))
        self.assertEqual(self.manifest["retry_sha"], sha(RETRY))
        self.assertEqual(self.manifest["acceptance_criteria_sha"], sha(CRITERIA))

    def test_manifest_records_frozen_identities(self):
        self.assertEqual(self.manifest["benchmark_v2_sha"], BENCHMARK_SHA)
        self.assertEqual(self.manifest["packet_artifact_sha"], PACKET_SHA)
        self.assertEqual(self.manifest["system_prompt_v5_sha"], PROMPT_V5_SHA)
        self.assertEqual(self.manifest["output_contract_sha"], CONTRACT_SHA)
        self.assertEqual(self.manifest["repair_policy"], "none_fail_closed")

    def test_manifest_counts(self):
        counts = self.manifest["result_counts"]
        self.assertEqual(counts["raw_rows"], 72)
        self.assertEqual(counts["contract_rows"], 72)
        self.assertEqual(counts["first_pass_rows"], 72)
        self.assertEqual(counts["accepted"] + counts["rejected"], 72)

    def test_qdrant_unchanged_and_no_writes(self):
        self.assertEqual(self.manifest["qdrant_points_before"], 5992)
        self.assertEqual(self.manifest["qdrant_points_after"], 5992)
        self.assertEqual(self.manifest["qdrant_writes"], 0)
        with urllib.request.urlopen(
                "http://localhost:6333/collections/tunnelbook_dense_v1", timeout=10) as response:
            result = json.loads(response.read())["result"]
        self.assertEqual(result["points_count"], 5992)
        self.assertEqual(result["status"], "green")

    def test_candidate_status_not_upgraded_to_acceptable(self):
        descriptor = json.loads((ROOT / "data/metadata/generation_candidate_v1.json")
                                .read_text(encoding="utf-8"))
        self.assertNotEqual(descriptor["status"], "acceptable")


if __name__ == "__main__":
    unittest.main()
