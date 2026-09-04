"""Generation Phase B: frozen 72-query execution, claim audit, repeatability, long-context stress.

These tests protect execution integrity rather than model quality. They assert that the run was
made against the frozen benchmark with the frozen runtime, that nothing stale was resumed, that
prompt accounting was exact, that no reasoning text was persisted, and that the acceptance criteria
were frozen before aggregation.
"""
from __future__ import annotations

import collections
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "data/evaluation/generation_eval_benchmark_v1.jsonl"
RESULTS = ROOT / "data/evaluation/generation_eval_results_v1.jsonl"
MANIFEST = ROOT / "data/evaluation/generation_eval_results_v1_manifest.json"
CLAIMS = ROOT / "data/evaluation/generation_claim_audit_v1.jsonl"
REPEATS = ROOT / "data/evaluation/generation_repeatability_v1.jsonl"
STRESS = ROOT / "data/evaluation/generation_long_context_stress_v1.jsonl"
CRITERIA = ROOT / "data/metadata/generation_eval_acceptance_criteria_v1.json"

BENCHMARK_SHA = "de3c1684ad26b459e6a209a9ef770c1a0f0fae39b44d0d251bc492ca3f75bd6b"
PROMPT_V3_SHA = "d3cadd465e2733d0cdd451d146407f28f80cefc784b432088fc20ecf7526dc74"
REQUIRED_RESULT_FIELDS = (
    "query_id", "primary_query_type", "language", "answerability", "must_abstain",
    "retrieval_limited", "model_id", "system_prompt_version", "system_prompt_sha", "benchmark_sha",
    "context_packet_sha", "generation_config_hash", "prompt_sha", "prompt_tokens_local",
    "prompt_tokens_api", "prompt_token_delta", "completion_tokens", "answer_tokens",
    "latency_seconds", "finish_reason", "raw_answer", "syntactically_valid_handles",
    "valid_handles", "unknown_handles", "malformed_citations", "doc_leaks", "page_leaks",
    "slide_leaks", "path_leaks", "template_leaks", "abstention_marker", "abstention_at_start",
    "completion_state", "started_at", "completed_at",
)
FORBIDDEN_REASONING_FIELDS = ("reasoning_text", "thinking", "chain_of_thought", "reasoning_content")


def _rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class PhaseBTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not RESULTS.is_file():
            raise unittest.SkipTest("Phase B results not produced")
        cls.results = sorted(_rows(RESULTS), key=lambda r: r["query_id"])
        cls.benchmark = {r["query_id"]: r for r in _rows(BENCHMARK)}
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.is_file() else None


class TestExecutionCompleteness(PhaseBTestCase):
    def test_benchmark_sha_unchanged(self):
        self.assertEqual(hashlib.sha256(BENCHMARK.read_bytes()).hexdigest(), BENCHMARK_SHA,
                         "benchmark changed; results are not attributable to v1")

    def test_exactly_72_rows_one_per_query(self):
        self.assertEqual(len(self.results), 72)
        ids = [r["query_id"] for r in self.results]
        self.assertEqual(len(set(ids)), 72)
        self.assertEqual(set(ids), set(self.benchmark))

    def test_every_row_ran_against_the_frozen_benchmark_and_prompt(self):
        for row in self.results:
            self.assertEqual(row["benchmark_sha"], BENCHMARK_SHA, row["query_id"])
            self.assertEqual(row["system_prompt_sha"], PROMPT_V3_SHA, row["query_id"])
            self.assertEqual(row["system_prompt_version"], "generation-system-prompt-v3")
            self.assertEqual(row["model_id"], "qwen3.6-35b-a3b-mlx")
            self.assertEqual(row["validator_version"], "citation-validator-v1.2")

    def test_frozen_generation_parameters_not_swept(self):
        self.assertEqual({r["max_tokens"] for r in self.results}, {3072})
        self.assertEqual({r["temperature"] for r in self.results}, {0.0})
        self.assertEqual({r["seed"] for r in self.results}, {11})
        self.assertEqual(len({r["generation_config_hash"] for r in self.results}), 1)

    def test_results_use_the_frozen_context_packets(self):
        for row in self.results:
            self.assertEqual(row["context_packet_sha"],
                             self.benchmark[row["query_id"]]["context_packet_sha"],
                             f"{row['query_id']} answered against a different packet")

    def test_required_fields_present(self):
        for row in self.results:
            for field in REQUIRED_RESULT_FIELDS:
                self.assertIn(field, row, f"{row['query_id']} missing {field}")


class TestCheckpointIdentity(PhaseBTestCase):
    def test_identity_recorded_with_all_required_components(self):
        for row in self.results:
            identity = row["checkpoint_identity"]
            for field in ("query_id", "benchmark_sha", "system_prompt_sha", "model_id",
                          "tokenizer_sha", "template_sha", "generation_config_hash",
                          "context_packet_sha"):
                self.assertIn(field, identity, row["query_id"])

    def test_identity_matches_the_row_it_belongs_to(self):
        for row in self.results:
            identity = row["checkpoint_identity"]
            self.assertEqual(identity["query_id"], row["query_id"])
            self.assertEqual(identity["benchmark_sha"], row["benchmark_sha"])
            self.assertEqual(identity["context_packet_sha"], row["context_packet_sha"])
            self.assertEqual(identity["generation_config_hash"], row["generation_config_hash"])

    def test_no_stale_identity_across_rows(self):
        """All 72 rows must share one config identity; a mixed run is not a valid benchmark run."""
        self.assertEqual(len({r["checkpoint_identity"]["generation_config_hash"]
                              for r in self.results}), 1)
        self.assertEqual(len({r["checkpoint_identity"]["tokenizer_sha"] for r in self.results}), 1)
        self.assertEqual(len({r["checkpoint_identity"]["template_sha"] for r in self.results}), 1)


class TestPromptAccountingAndThinking(PhaseBTestCase):
    def test_prompt_tokens_local_equals_api(self):
        for row in self.results:
            self.assertEqual(row["prompt_tokens_local"], row["prompt_tokens_api"], row["query_id"])
            self.assertEqual(row["prompt_token_delta"], 0, row["query_id"])

    def test_no_thinking_markers_in_any_answer(self):
        for row in self.results:
            self.assertEqual(row["thinking_marker_leaks"], [], row["query_id"])
            for marker in ("<think>", "</think>", "<|im_start|>", "<|im_end|>"):
                self.assertNotIn(marker, row["raw_answer"], row["query_id"])

    def test_reasoning_text_is_never_persisted(self):
        for row in self.results:
            for field in FORBIDDEN_REASONING_FIELDS:
                self.assertNotIn(field, row, f"{row['query_id']} persisted {field}")

    def test_reasoning_token_status_is_honest(self):
        """If the API does not expose reasoning tokens we must say so, not record a fabricated 0."""
        for row in self.results:
            self.assertIn(row["reasoning_tokens_status"], {"exposed", "not_exposed"})
            if row["reasoning_tokens_status"] == "not_exposed":
                self.assertIsNone(row["reasoning_tokens"], row["query_id"])

    def test_all_completions_finished_naturally(self):
        for row in self.results:
            self.assertEqual(row["finish_reason"], "stop", row["query_id"])
            self.assertNotIn(row["completion_state"], {"truncated", "empty"}, row["query_id"])


class TestValidatorOutputs(PhaseBTestCase):
    def test_no_unknown_or_excluded_handles(self):
        for row in self.results:
            self.assertEqual(row["unknown_handles"], [], row["query_id"])
            self.assertEqual(row["excluded_handle_citations"], [], row["query_id"])

    def test_cited_handles_exist_in_the_packet(self):
        for row in self.results:
            exposed = set(self.benchmark[row["query_id"]]["evidence_ids"])
            for handle in row["valid_handles"]:
                self.assertIn(handle, exposed, row["query_id"])

    def test_no_source_coordinate_leaks(self):
        for field in ("doc_leaks", "page_leaks", "slide_leaks", "path_leaks", "template_leaks"):
            offenders = [r["query_id"] for r in self.results if r[field]]
            self.assertEqual(offenders, [], f"{field} leaked in {offenders}")

    def test_malformed_citations_are_recorded_not_normalised(self):
        """Malformed output must stay malformed in the record; scoring never repairs it.

        The two validator axes are independent: an answer may use both a bracketed [E002] and a
        bare E002 for the same evidence, in which case the handle legitimately appears on the valid
        axis and the malformed axis at once. What must never happen is a malformed occurrence being
        rewritten into bracketed form or dropped.
        """
        offenders = [r for r in self.results if r["malformed_citations"]]
        self.assertTrue(offenders, "expected the run to contain the recorded malformed cases")
        for row in offenders:
            for handle in row["malformed_citations"]:
                self.assertNotIn("[", handle, f"{row['query_id']} malformed handle was normalised")
                self.assertNotIn("]", handle, f"{row['query_id']} malformed handle was normalised")
                self.assertRegex(handle, r"^[Ee]\d{2,4}$")
            self.assertNotEqual(row["completion_state"], "complete_without_issues")

    def test_malformed_answers_are_counted_as_such(self):
        recorded = {r["query_id"] for r in self.results if r["malformed_citations"]}
        self.assertEqual(recorded, {"GEV061", "GEV064", "GEV070"},
                         "the set of answers with malformed citations changed")


class TestAbstentionScoring(PhaseBTestCase):
    def test_must_abstain_category_items_abstained(self):
        items = [r for r in self.results
                 if self.benchmark[r["query_id"]]["primary_query_type"] == "must_abstain"]
        self.assertEqual(len(items), 8)
        for row in items:
            self.assertIsNotNone(row["abstention_marker"], row["query_id"])
            self.assertTrue(row["abstention_at_start"], row["query_id"])

    def test_abstention_marker_is_a_contract_marker(self):
        for row in self.results:
            if row["abstention_marker"]:
                self.assertIn(row["abstention_marker"],
                              {"YETERSİZ KANIT", "INSUFFICIENT EVIDENCE"}, row["query_id"])

    def test_retrieval_limited_items_are_identifiable(self):
        rl = [r["query_id"] for r in self.results if r["retrieval_limited"]]
        self.assertEqual(sorted(rl), ["GEV018", "GEV058"])
        for row in self.results:
            self.assertEqual(row["retrieval_limited"],
                             self.benchmark[row["query_id"]]["retrieval_limited"])


class TestClaimAudit(PhaseBTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not CLAIMS.is_file():
            raise unittest.SkipTest("claim audit not produced")
        cls.claims = _rows(CLAIMS)

    def test_every_executed_query_has_claim_rows(self):
        covered = {c["query_id"] for c in self.claims}
        self.assertEqual(covered, {r["query_id"] for r in self.results},
                         "claim audit does not cover all 72 answers")

    def test_claim_schema(self):
        for claim in self.claims:
            for field in ("query_id", "claim_id", "claim_text", "claim_label", "cited_evidence_ids",
                          "supporting_evidence_ids", "supporting_literal_spans",
                          "unsupported_reason", "numeric_claim", "auditor_notes", "label_method"):
                self.assertIn(field, claim, claim.get("query_id"))

    def test_claim_labels_are_legal(self):
        legal = {"SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED", "NON_FACTUAL",
                 "UNVERIFIED_BY_RULE"}
        for claim in self.claims:
            self.assertIn(claim["claim_label"], legal, claim["query_id"])

    def test_supported_claims_cite_evidence_present_in_the_packet(self):
        for claim in self.claims:
            if claim["claim_label"] != "SUPPORTED":
                continue
            exposed = set(self.benchmark[claim["query_id"]]["evidence_ids"])
            for handle in claim["supporting_evidence_ids"]:
                self.assertIn(handle, exposed, claim["query_id"])

    def test_label_method_is_recorded_for_every_claim(self):
        """Audit depth must be legible: each label says how it was produced."""
        methods = {c["label_method"] for c in self.claims}
        self.assertTrue(methods <= {"auditor_verified_against_cited_evidence",
                                    "rule_based_grounding_check", "rule_based_non_factual",
                                    "rule_unmatched_not_hand_verified"}, methods)

    def test_no_claim_asserts_a_number_absent_from_its_packet(self):
        offenders = [(c["query_id"], c["claim_id"], c["numbers_absent_from_packet"])
                     for c in self.claims
                     if c["numbers_absent_from_packet"] and c["claim_label"] == "SUPPORTED"
                     and c["label_method"] == "rule_based_grounding_check"]
        self.assertEqual(offenders, [], f"unverified fabricated numbers: {offenders}")


class TestRepeatability(PhaseBTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not REPEATS.is_file():
            raise unittest.SkipTest("repeatability not produced")
        cls.repeats = _rows(REPEATS)

    def test_twenty_items_three_runs_each(self):
        counts = collections.Counter(r["query_id"] for r in self.repeats)
        self.assertEqual(len(counts), 20)
        self.assertEqual(set(counts.values()), {3})
        self.assertEqual(len(self.repeats), 60)

    def test_repeat_indices(self):
        by_query = collections.defaultdict(set)
        for row in self.repeats:
            by_query[row["query_id"]].add(row["repeat_index"])
        for query_id, indices in by_query.items():
            self.assertEqual(indices, {1, 2, 3}, query_id)

    def test_repeats_used_the_same_frozen_config_and_packet(self):
        self.assertEqual(len({r["generation_config_hash"] for r in self.repeats}), 1)
        for row in self.repeats:
            self.assertEqual(row["context_packet_sha"],
                             self.benchmark[row["query_id"]]["context_packet_sha"])

    def test_subset_covers_the_required_dimensions(self):
        types = {r["primary_query_type"] for r in self.repeats}
        for required in ("direct_factual_conceptual", "multi_source_synthesis", "numeric_table",
                         "must_abstain", "cross_lingual", "injection_adversarial"):
            self.assertIn(required, types)
        self.assertEqual({r["language"] for r in self.repeats}, {"tr", "en"})

    def test_abstention_is_stable_across_repeats(self):
        by_query = collections.defaultdict(list)
        for row in self.repeats:
            by_query[row["query_id"]].append(bool(row["abstention_marker"]))
        for query_id, decisions in by_query.items():
            self.assertEqual(len(set(decisions)), 1, f"{query_id} abstention flapped")


class TestLongContextStress(PhaseBTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not STRESS.is_file():
            raise unittest.SkipTest("stress not produced")
        cls.stress = _rows(STRESS)

    def test_schema_and_fractions(self):
        fractions = collections.Counter(r["target_context_fraction"] for r in self.stress)
        self.assertEqual(set(fractions), {"25", "50", "75"})
        for row in self.stress:
            for field in ("query_id", "target_context_fraction", "actual_context_tokens",
                          "rendered_prompt_tokens", "answer", "latency_seconds",
                          "cited_gold_evidence_ids", "malformed_citations", "unknown_handles"):
                self.assertIn(field, row)

    def test_gold_support_evidence_was_not_altered_away(self):
        for row in self.stress:
            self.assertEqual(row["gold_chunks_missing"], [],
                             f"{row['query_id']} {row['target_context_fraction']}% dropped gold evidence")
            self.assertEqual(row["gold_chunks_present"], row["gold_chunks_total"])

    def test_never_exceeds_the_operational_prompt_ceiling(self):
        for row in self.stress:
            self.assertLessEqual(row["rendered_prompt_tokens"], 65268, row["query_id"])
            self.assertEqual(row["prompt_token_delta"], 0, row["query_id"])

    def test_context_grows_with_the_target_fraction(self):
        by_fraction = collections.defaultdict(list)
        for row in self.stress:
            by_fraction[row["target_context_fraction"]].append(row["actual_context_tokens"])
        means = {k: sum(v) / len(v) for k, v in by_fraction.items()}
        self.assertLess(means["25"], means["50"])
        self.assertLess(means["50"], means["75"])


class TestAcceptanceCriteriaAndManifest(PhaseBTestCase):
    def test_criteria_were_frozen_before_aggregation(self):
        criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
        self.assertTrue(criteria["frozen_before_aggregation"])
        self.assertTrue(criteria["frozen_before_execution"])
        self.assertEqual(criteria["primary_view"], "generator_only")
        for metric in ("query_acceptable_rate", "unsupported_material_claim_rate",
                       "citation_precision", "citation_coverage", "abstention_accuracy",
                       "injection_resistance_rate"):
            self.assertIn(metric, criteria["thresholds"])

    def test_criteria_sha_recorded_in_manifest(self):
        self.assertIsNotNone(self.manifest)
        actual = hashlib.sha256(CRITERIA.read_bytes()).hexdigest()
        self.assertEqual(self.manifest["acceptance_criteria_sha"], actual,
                         "acceptance criteria changed after the run")

    def test_manifest_matches_result_artifact(self):
        self.assertEqual(self.manifest["result_row_count"], 72)
        self.assertEqual(self.manifest["result_artifact_sha"],
                         hashlib.sha256(RESULTS.read_bytes()).hexdigest())
        self.assertEqual(self.manifest["benchmark_sha"], BENCHMARK_SHA)
        self.assertEqual(self.manifest["prompt_token_delta_max_abs"], 0)
        self.assertEqual(self.manifest["thinking_marker_leaks"], 0)

    def test_manifest_records_retrieval_was_not_rerun(self):
        self.assertFalse(self.manifest["retrieval_rerun_for_main_benchmark"])

    def test_qdrant_unchanged(self):
        self.assertEqual(self.manifest["qdrant_points_before"], 5992)
        self.assertEqual(self.manifest["qdrant_points_after"], 5992)
        self.assertEqual(self.manifest["qdrant_writes"], 0)


if __name__ == "__main__":
    unittest.main()
