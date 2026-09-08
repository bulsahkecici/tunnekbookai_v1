"""Generation Phase B v2 - clean holdout execution and complete claim audit.

The defining requirement of this phase is that the claim audit resolves EVERY material claim.
Phase B v1 left 175 unresolved; these tests make that failure mode impossible to repeat silently.
"""
from __future__ import annotations

import collections
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "data/evaluation/generation_eval_benchmark_v2.jsonl"
PACKETS = ROOT / "data/evaluation/generation_eval_benchmark_v2_packets.jsonl"
RESULTS = ROOT / "data/evaluation/generation_eval_results_v2.jsonl"
CLAIMS = ROOT / "data/evaluation/generation_claim_audit_v2.jsonl"
REPEATS = ROOT / "data/evaluation/generation_repeatability_v2.jsonl"
STRESS = ROOT / "data/evaluation/generation_long_context_stress_v2.jsonl"
MANIFEST = ROOT / "data/evaluation/generation_eval_results_v2_manifest.json"
CRITERIA = ROOT / "data/metadata/generation_eval_acceptance_criteria_v2.json"

BENCHMARK_SHA = "1e6347b557d583b56882c4c05fd1c5453874b7a05e61205c9430a24a677b0cff"
PACKET_SHA = "0538705147cf543b45fe8e73d57828cbc341a9a5a1dd574bd0969a9326e54d7a"
PROMPT_V5_SHA = "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085"
LEGAL_LABELS = {"SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED", "NON_FACTUAL"}
LEGAL_METHODS = {"deterministic_verified", "manual_evidence_verified"}


def _rows(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not RESULTS.is_file():
            raise unittest.SkipTest("phase B v2 results not produced")
        cls.results = sorted(_rows(RESULTS), key=lambda r: r["query_id"])
        cls.bench = {r["query_id"]: r for r in _rows(BENCHMARK)}
        cls.claims = _rows(CLAIMS) if CLAIMS.is_file() else []
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.is_file() else None


class TestExecution(Base):
    def test_frozen_inputs_unchanged(self):
        self.assertEqual(hashlib.sha256(BENCHMARK.read_bytes()).hexdigest(), BENCHMARK_SHA)
        self.assertEqual(hashlib.sha256(PACKETS.read_bytes()).hexdigest(), PACKET_SHA)

    def test_72_rows_one_per_query(self):
        self.assertEqual(len(self.results), 72)
        self.assertEqual({r["query_id"] for r in self.results}, set(self.bench))

    def test_every_row_used_v5_and_the_frozen_packet(self):
        for row in self.results:
            self.assertEqual(row["system_prompt_sha"], PROMPT_V5_SHA, row["query_id"])
            self.assertEqual(row["system_prompt_version"], "generation-system-prompt-v5")
            self.assertEqual(row["benchmark_sha"], BENCHMARK_SHA)
            self.assertEqual(row["packet_artifact_sha"], PACKET_SHA)
            self.assertEqual(row["context_packet_sha"],
                             self.bench[row["query_id"]]["context_packet_sha"], row["query_id"])

    def test_checkpoint_identity_complete_and_uniform(self):
        for row in self.results:
            ident = row["checkpoint_identity"]
            for f in ("query_id", "benchmark_v2_sha", "packet_artifact_sha", "context_packet_sha",
                      "system_prompt_version", "system_prompt_sha", "model_id", "tokenizer_sha",
                      "template_sha", "generation_config_hash"):
                self.assertIn(f, ident, row["query_id"])
            self.assertEqual(ident["query_id"], row["query_id"])
        self.assertEqual(len({r["generation_config_hash"] for r in self.results}), 1)

    def test_prompt_accounting_exact_and_no_truncation(self):
        for row in self.results:
            self.assertEqual(row["prompt_token_delta"], 0, row["query_id"])
            self.assertEqual(row["finish_reason"], "stop", row["query_id"])

    def test_no_thinking_or_reasoning_persistence(self):
        for row in self.results:
            self.assertEqual(row["thinking_marker_leaks"], [], row["query_id"])
            self.assertIn(row["reasoning_tokens_status"], {"exposed", "not_exposed"})
            for f in ("reasoning_text", "chain_of_thought", "thinking"):
                self.assertNotIn(f, row)

    def test_no_unknown_handles_or_coordinate_leaks(self):
        for row in self.results:
            self.assertEqual(row["unknown_handles"], [], row["query_id"])
            for f in ("doc_leaks", "page_leaks", "slide_leaks", "path_leaks", "template_leaks"):
                self.assertEqual(row[f], [], f"{row['query_id']} {f}")

    def test_expected_marker_is_derived_from_query_language(self):
        for row in self.results:
            expected = "YETERSİZ KANIT" if row["language"] == "tr" else "INSUFFICIENT EVIDENCE"
            self.assertEqual(row["expected_abstention_marker"], expected, row["query_id"])


class TestClaimAuditCompleteness(Base):
    def test_audit_covers_every_answer(self):
        self.assertTrue(self.claims)
        self.assertEqual({c["query_id"] for c in self.claims}, {r["query_id"] for r in self.results})

    def test_zero_unresolved_claims(self):
        """The Phase B v1 failure: 175 claims left UNVERIFIED_BY_RULE. Never again."""
        unresolved = [c for c in self.claims if not c.get("resolved")]
        self.assertEqual(unresolved, [], f"{len(unresolved)} unresolved claims")

    def test_no_forbidden_labels(self):
        for claim in self.claims:
            self.assertIn(claim["claim_label"], LEGAL_LABELS,
                          f"{claim['query_id']} {claim['claim_id']}")
            self.assertNotEqual(claim["claim_label"], "UNVERIFIED_BY_RULE")

    def test_label_methods_are_decided_not_deferred(self):
        for claim in self.claims:
            self.assertIn(claim["label_method"], LEGAL_METHODS,
                          f"{claim['query_id']} {claim['claim_id']}")

    def test_partial_and_unsupported_claims_carry_a_reason(self):
        for claim in self.claims:
            if claim["claim_label"] == "PARTIALLY_SUPPORTED":
                self.assertTrue((claim["partial_reason"] or "").strip(), claim["query_id"])
            if claim["claim_label"] == "UNSUPPORTED":
                self.assertTrue((claim["unsupported_reason"] or "").strip(), claim["query_id"])

    def test_citation_metrics_use_the_full_population(self):
        material = [c for c in self.claims if c["material"]]
        bearing = [c for c in material if c["citation_bearing"]]
        self.assertGreater(len(material), 500)
        self.assertGreater(len(bearing), 400)
        # every citation-bearing claim has a resolved label, so precision has no unresolved denominator
        self.assertTrue(all(c["claim_label"] in LEGAL_LABELS for c in bearing))

    def test_supported_claims_cite_packet_evidence_only(self):
        for claim in self.claims:
            if claim["claim_label"] not in ("SUPPORTED", "PARTIALLY_SUPPORTED"):
                continue
            exposed = set(self.bench[claim["query_id"]]["evidence_ids"])
            for handle in claim["supporting_evidence_ids"]:
                self.assertIn(handle, exposed, claim["query_id"])


class TestScoringSplits(Base):
    def test_retrieval_limited_split_is_identifiable(self):
        rl = [r["query_id"] for r in self.results if r["retrieval_limited"]]
        self.assertEqual(rl, ["GEV018"])

    def test_must_abstain_population(self):
        ma = [r for r in self.results if r["primary_query_type"] == "must_abstain"]
        self.assertEqual(len(ma), 8)
        for row in ma:
            self.assertIsNotNone(row["abstention_marker"], row["query_id"])
            self.assertTrue(row["abstention_at_start"], row["query_id"])

    def test_marker_language_denominator_is_actual_abstentions(self):
        abstained = [r for r in self.results if r["abstention_marker"]]
        self.assertGreaterEqual(len(abstained), 8)
        for row in abstained:
            self.assertIsNotNone(row["abstention_marker_language_correct"], row["query_id"])
        for row in self.results:
            if not row["abstention_marker"]:
                self.assertIsNone(row["abstention_marker_language_correct"], row["query_id"])

    def test_known_residual_failures_stay_visible(self):
        """Pin what actually failed so a silent change cannot pass unnoticed."""
        malformed = sorted(r["query_id"] for r in self.results if r["malformed_citations"])
        self.assertEqual(malformed, ["GEV042"])
        wrong_marker = sorted(r["query_id"] for r in self.results
                              if r["abstention_marker"] and not r["abstention_marker_language_correct"])
        self.assertEqual(wrong_marker, ["GEV061", "GEV062"])

    def test_numeric_items_have_alternatives_available(self):
        numeric = [q for q, b in self.bench.items() if b["primary_query_type"] == "numeric_table"]
        self.assertEqual(len(numeric), 8)
        with_alts = [q for q in numeric
                     if any(n["alternative_valid_values"] for n in self.bench[q]["numeric_gold"] or [])]
        self.assertTrue(with_alts, "numeric scoring must be able to accept alternatives")


class TestRepeatabilityAndStress(Base):
    def test_repeatability_shape(self):
        if not REPEATS.is_file():
            self.skipTest("repeatability not produced")
        rows = _rows(REPEATS)
        counts = collections.Counter(r["query_id"] for r in rows)
        self.assertEqual(len(counts), 20)
        self.assertEqual(set(counts.values()), {3})
        self.assertEqual(len(rows), 60)
        self.assertEqual({r["system_prompt_version"] for r in rows},
                         {"generation-system-prompt-v5"})

    def test_repeatability_is_deterministic(self):
        if not REPEATS.is_file():
            self.skipTest("repeatability not produced")
        by = collections.defaultdict(list)
        for row in _rows(REPEATS):
            by[row["query_id"]].append(row)
        for qid, runs in by.items():
            self.assertEqual(len({r["answer_sha"] for r in runs}), 1, f"{qid} not deterministic")

    def test_stress_preserves_gold_and_respects_ceiling(self):
        if not STRESS.is_file():
            self.skipTest("stress not produced")
        rows = _rows(STRESS)
        self.assertEqual({r["target_context_fraction"] for r in rows}, {"25", "50", "75"})
        for row in rows:
            self.assertEqual(row["gold_chunks_missing"], [], row["query_id"])
            self.assertLessEqual(row["rendered_prompt_tokens"], 65268, row["query_id"])
            self.assertEqual(row["prompt_token_delta"], 0, row["query_id"])


class TestCriteriaAndManifest(Base):
    def test_criteria_frozen_before_execution_with_explicit_denominators(self):
        criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
        self.assertTrue(criteria["frozen_before_execution"])
        self.assertTrue(criteria["frozen_before_aggregation"])
        for metric in ("malformed_citation_answer_rate", "citation_coverage", "citation_precision",
                       "abstention_marker_language_accuracy"):
            self.assertIn(metric, criteria["metric_definitions"])
            self.assertIn("denominator", criteria["metric_definitions"][metric])
        self.assertTrue(criteria["marker_policy"]["decided_before_execution"])
        self.assertEqual(criteria["claim_audit_requirements"]["unresolved_material_claims_allowed"], 0)

    def test_manifest_matches_artifacts(self):
        self.assertIsNotNone(self.manifest)
        self.assertEqual(self.manifest["result_row_count"], 72)
        self.assertEqual(self.manifest["result_artifact_sha"],
                         hashlib.sha256(RESULTS.read_bytes()).hexdigest())
        self.assertEqual(self.manifest["claim_audit_sha"],
                         hashlib.sha256(CLAIMS.read_bytes()).hexdigest())
        self.assertEqual(self.manifest["acceptance_criteria_sha"],
                         hashlib.sha256(CRITERIA.read_bytes()).hexdigest())
        self.assertEqual(self.manifest["unresolved_claims"], 0)
        self.assertEqual(self.manifest["prompt_token_delta_max_abs"], 0)
        self.assertEqual(self.manifest["thinking_marker_leaks"], 0)
        self.assertFalse(self.manifest["retrieval_rerun_for_main_benchmark"])

    def test_qdrant_unchanged(self):
        self.assertEqual(self.manifest["qdrant_points_before"], 5992)
        self.assertEqual(self.manifest["qdrant_points_after"], 5992)
        self.assertEqual(self.manifest["qdrant_writes"], 0)


if __name__ == "__main__":
    unittest.main()
