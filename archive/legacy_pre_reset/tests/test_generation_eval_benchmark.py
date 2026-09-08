"""Frozen 72-item generation evaluation benchmark.

These tests protect the benchmark contract: exact size and category distribution, schema
completeness, and above all that every gold claim resolves to an EXACT literal span inside the
frozen ContextPacket it was authored from. A benchmark whose gold drifts from its evidence is
worse than no benchmark, so span exactness is asserted byte-for-byte, not approximately.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "data/evaluation/generation_eval_benchmark_v1.jsonl"
MANIFEST = ROOT / "data/evaluation/generation_eval_benchmark_v1_manifest.json"
PACKETS = ROOT / "data/evaluation/generation_eval_benchmark_v1_packets.jsonl"

EXPECTED_DISTRIBUTION = {
    "direct_factual_conceptual": 18,
    "design_construction": 10,
    "multi_source_synthesis": 10,
    "numeric_table": 8,
    "regulation_specification": 6,
    "cross_lingual": 6,
    "must_abstain": 8,
    "injection_adversarial": 6,
}
REQUIRED_FIELDS = (
    "benchmark_version", "query_id", "primary_query_type", "secondary_tags", "language", "query",
    "answerability", "must_abstain", "retrieval_limited", "retrieval_limited_reason",
    "retriever_release", "retriever_config", "context_contract", "context_packet_sha",
    "context_text_sha", "context_token_count", "context_token_budget", "evidence_ids",
    "evidence_count", "document_ids_or_source_keys", "gold_claims", "gold_answer_summary",
    "gold_support", "numeric_gold", "conflict_gold", "injection_metadata", "notes",
    "authoring_status",
)
ANSWERABILITY = {"answerable", "partially_answerable", "unanswerable"}
CLAIM_TYPES = {"factual", "numeric", "procedural", "comparative", "synthesis", "regulatory",
               "conflict", "abstention"}
FORBIDDEN_FIELDS = ("model_answer", "generated_answer", "qwen_answer", "completion", "raw_answer",
                    "model_output", "prediction")


def _rows():
    return [json.loads(line) for line in BENCHMARK.read_text(encoding="utf-8").splitlines() if line.strip()]


class BenchmarkTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not BENCHMARK.is_file():
            raise unittest.SkipTest("benchmark artifact not built")
        cls.rows = _rows()
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.is_file() else None
        cls.packets = {}
        if PACKETS.is_file():
            for line in PACKETS.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    packet = json.loads(line)
                    cls.packets[packet["packet_sha"]] = packet


class TestSizeAndIdentity(BenchmarkTestCase):
    def test_exactly_72_items(self):
        self.assertEqual(len(self.rows), 72)

    def test_sequential_unique_ids(self):
        ids = [row["query_id"] for row in self.rows]
        self.assertEqual(len(set(ids)), 72)
        self.assertEqual(ids, [f"GEV{i:03d}" for i in range(1, 73)])

    def test_benchmark_version_is_uniform(self):
        self.assertEqual({row["benchmark_version"] for row in self.rows},
                         {"generation-eval-benchmark-v1"})


class TestDistribution(BenchmarkTestCase):
    def test_exact_category_distribution(self):
        counts = collections.Counter(row["primary_query_type"] for row in self.rows)
        self.assertEqual(dict(counts), EXPECTED_DISTRIBUTION)

    def test_language_balance_within_tolerance(self):
        counts = collections.Counter(row["language"] for row in self.rows)
        self.assertEqual(set(counts), {"tr", "en"})
        for language, count in counts.items():
            self.assertLessEqual(abs(count - 36), 2, f"{language}={count} outside 36+-2")

    def test_answerability_and_difficulty_values_are_legal(self):
        for row in self.rows:
            self.assertIn(row["answerability"], ANSWERABILITY, row["query_id"])
            self.assertIn(row["difficulty"], {"easy", "medium", "hard"}, row["query_id"])


class TestSchema(BenchmarkTestCase):
    def test_required_fields_present(self):
        for row in self.rows:
            for field in REQUIRED_FIELDS:
                self.assertIn(field, row, f"{row['query_id']} missing {field}")

    def test_context_packet_identity_recorded(self):
        for row in self.rows:
            self.assertRegex(row["context_packet_sha"], r"^[0-9a-f]{64}$")
            self.assertRegex(row["context_text_sha"], r"^[0-9a-f]{64}$")
            self.assertGreater(row["context_token_count"], 0)
            self.assertEqual(row["context_contract"], "tunnelbook-context-v1")
            self.assertEqual(row["retriever_release"], "tunnelbook-retriever-v1")

    def test_queries_are_non_empty_and_distinct(self):
        queries = [row["query"].strip() for row in self.rows]
        self.assertTrue(all(queries))
        self.assertEqual(len(set(q.lower() for q in queries)), 72, "duplicate query text")

    def test_no_model_output_fields(self):
        """The benchmark must never carry generator output; gold is human authored."""
        for row in self.rows:
            for field in FORBIDDEN_FIELDS:
                self.assertNotIn(field, row, f"{row['query_id']} carries {field}")
            self.assertEqual(row["authoring_status"], "human_authored_evidence_verified")

    def test_claim_types_are_legal(self):
        for row in self.rows:
            self.assertTrue(row["gold_claims"], row["query_id"])
            for claim in row["gold_claims"]:
                self.assertIn(claim["claim_type"], CLAIM_TYPES, row["query_id"])
                self.assertIn(claim["support_status"], {"supported", "unsupported"})
                self.assertTrue(claim["claim_text"].strip())


class TestGoldIntegrity(BenchmarkTestCase):
    def test_gold_cites_only_evidence_present_in_the_packet(self):
        for row in self.rows:
            exposed = set(row["evidence_ids"])
            for claim in row["gold_claims"]:
                for evidence_id in claim["supporting_evidence_ids"]:
                    self.assertIn(evidence_id, exposed,
                                  f"{row['query_id']} cites {evidence_id} not in packet")
            for support in row["gold_support"]:
                self.assertIn(support["evidence_id"], exposed, row["query_id"])

    def test_evidence_handles_are_canonical(self):
        for row in self.rows:
            for evidence_id in row["evidence_ids"]:
                self.assertRegex(evidence_id, r"^E\d{3}$")

    def test_supported_claims_have_evidence(self):
        for row in self.rows:
            for claim in row["gold_claims"]:
                if claim["support_status"] == "supported":
                    self.assertTrue(claim["supporting_evidence_ids"],
                                    f"{row['query_id']} {claim['claim_id']} supported without evidence")
                else:
                    self.assertFalse(claim["supporting_evidence_ids"],
                                     f"{row['query_id']} {claim['claim_id']} unsupported yet cites evidence")

    def test_required_claims_supported_on_answerable_items(self):
        for row in self.rows:
            if row["answerability"] != "answerable":
                continue
            for claim in row["gold_claims"]:
                if claim["required"]:
                    self.assertEqual(claim["support_status"], "supported",
                                     f"{row['query_id']} {claim['claim_id']}")

    def test_literal_spans_resolve_exactly_against_frozen_evidence(self):
        """The core guarantee: every recorded span is a byte-exact substring of its evidence item."""
        if not self.packets:
            self.skipTest("frozen packet archive not present")
        checked = 0
        for row in self.rows:
            packet = self.packets.get(row["context_packet_sha"])
            self.assertIsNotNone(packet, f"{row['query_id']} packet not archived")
            evidence = {e["evidence_id"]: e for e in packet["evidence"]}
            for support in row["gold_support"]:
                self.assertEqual(support["span_scope"], "evidence_item")
                item = evidence[support["evidence_id"]]
                self.assertEqual(item["text"][support["span_start"]:support["span_end"]],
                                 support["literal_span"],
                                 f"{row['query_id']} span drift on {support['evidence_id']}")
                self.assertEqual(item["text_sha256"], support["evidence_text_sha256"],
                                 f"{row['query_id']} evidence text changed")
                checked += 1
        self.assertGreater(checked, 100, "span coverage unexpectedly small")

    def test_gold_never_cites_excluded_evidence(self):
        if not self.packets:
            self.skipTest("frozen packet archive not present")
        for row in self.rows:
            packet = self.packets[row["context_packet_sha"]]
            excluded = {x["chunk_id"] for x in packet["excluded"]}
            evidence = {e["evidence_id"]: e for e in packet["evidence"]}
            for support in row["gold_support"]:
                self.assertNotIn(evidence[support["evidence_id"]]["chunk_id"], excluded,
                                 f"{row['query_id']} cites excluded chunk")

    def test_no_gold_span_is_reused_across_items(self):
        seen = collections.Counter()
        for row in self.rows:
            for support in row["gold_support"]:
                seen[(support["evidence_text_sha256"], support["span_start"],
                      support["span_end"])] += 1
        reused = [key for key, count in seen.items() if count > 1]
        self.assertFalse(reused, f"{len(reused)} gold spans reused across benchmark items")


class TestNumericGold(BenchmarkTestCase):
    def test_numeric_items_carry_numeric_gold(self):
        for row in self.rows:
            if row["primary_query_type"] == "numeric_table":
                self.assertTrue(row["numeric_gold"], row["query_id"])

    def test_numeric_records_are_complete_and_literal(self):
        for row in self.rows:
            for entry in row["numeric_gold"] or []:
                for field in ("value", "unit", "operation", "supporting_evidence_id",
                              "literal_span", "span_start", "span_end", "tolerance"):
                    self.assertIn(field, entry, row["query_id"])
                self.assertTrue(entry["unit"], f"{row['query_id']} numeric without unit")
                self.assertIn(entry["supporting_evidence_id"], row["evidence_ids"])
                for number in re.findall(r"\d+(?:[.,]\d+)?", entry["value"]):
                    self.assertIn(number, entry["literal_span"],
                                  f"{row['query_id']} value {number} absent from its literal span")

    def test_unit_conversion_is_explicit_when_allowed(self):
        for row in self.rows:
            for entry in row["numeric_gold"] or []:
                self.assertIn("unit_conversion_allowed", entry, row["query_id"])
                self.assertIsInstance(entry["unit_conversion_allowed"], bool)


class TestAbstention(BenchmarkTestCase):
    def test_must_abstain_category_flags_and_answerability(self):
        for row in self.rows:
            if row["primary_query_type"] == "must_abstain":
                self.assertTrue(row["must_abstain"], row["query_id"])
            if row["must_abstain"]:
                self.assertEqual(row["answerability"], "unanswerable", row["query_id"])

    def test_must_abstain_items_carry_no_supported_answer(self):
        """A must-abstain item may explain the gap, but must never contain a gold answer."""
        for row in self.rows:
            if not row["must_abstain"]:
                continue
            types = {claim["claim_type"] for claim in row["gold_claims"]}
            self.assertEqual(types, {"abstention"},
                             f"{row['query_id']} must-abstain item has answer claims {types}")
            self.assertIsNone(row["numeric_gold"], f"{row['query_id']} must-abstain with numeric gold")

    def test_must_abstain_count(self):
        typed = sum(1 for row in self.rows if row["primary_query_type"] == "must_abstain")
        self.assertEqual(typed, 8)

    def test_retrieval_limited_items_are_documented(self):
        for row in self.rows:
            if row["retrieval_limited"]:
                self.assertTrue((row["retrieval_limited_reason"] or "").strip(),
                                f"{row['query_id']} retrieval_limited without a reason")
            else:
                self.assertIsNone(row["retrieval_limited_reason"], row["query_id"])


class TestMultiSource(BenchmarkTestCase):
    def test_multi_source_items_need_at_least_two_evidence_items(self):
        for row in self.rows:
            if row["primary_query_type"] != "multi_source_synthesis":
                continue
            self.assertGreaterEqual(len(row["gold_evidence_ids"]), 2, row["query_id"])
            self.assertIsNotNone(row["minimum_required_evidence_count"], row["query_id"])
            self.assertGreaterEqual(row["minimum_required_evidence_count"], 2, row["query_id"])

    def test_multi_source_items_span_at_least_two_documents(self):
        if not self.packets:
            self.skipTest("frozen packet archive not present")
        for row in self.rows:
            if row["primary_query_type"] != "multi_source_synthesis":
                continue
            packet = self.packets[row["context_packet_sha"]]
            evidence = {e["evidence_id"]: e for e in packet["evidence"]}
            documents = {evidence[e]["document_id"] for e in row["gold_evidence_ids"]}
            self.assertGreaterEqual(len(documents), 2,
                                    f"{row['query_id']} synthesis from a single document")


class TestCrossLingualAndAdversarial(BenchmarkTestCase):
    def test_cross_lingual_metadata(self):
        for row in self.rows:
            if row["primary_query_type"] != "cross_lingual":
                continue
            meta = row["cross_lingual_metadata"]
            self.assertIsNotNone(meta, row["query_id"])
            for field in ("query_language", "dominant_evidence_language",
                          "cross_lingual_direction", "evidence_language_counts"):
                self.assertIn(field, meta, row["query_id"])
            self.assertIn(meta["cross_lingual_direction"],
                          {"tr_query_en_evidence", "en_query_tr_evidence"}, row["query_id"])
            self.assertEqual(meta["query_language"], row["language"], row["query_id"])

    def test_adversarial_metadata(self):
        for row in self.rows:
            if row["primary_query_type"] != "injection_adversarial":
                continue
            meta = row["injection_metadata"]
            self.assertIsNotNone(meta, row["query_id"])
            for field in ("injection_present", "injection_type", "technical_imperative_control",
                          "expected_behavior"):
                self.assertIn(field, meta, row["query_id"])
            self.assertEqual(meta["expected_behavior"], "ignore_as_instruction_use_as_data")

    def test_at_least_two_benign_imperative_controls(self):
        controls = [row["query_id"] for row in self.rows
                    if (row["injection_metadata"] or {}).get("technical_imperative_control")]
        self.assertGreaterEqual(len(controls), 2, f"only {len(controls)} benign imperative controls")


class TestConflictGold(BenchmarkTestCase):
    def test_conflict_items_record_both_sides(self):
        for row in self.rows:
            conflict = row["conflict_gold"]
            if not conflict:
                continue
            self.assertTrue(conflict["conflict_present"], row["query_id"])
            self.assertEqual(conflict["expected_behavior"], "report_both_without_silent_resolution")
            self.assertGreaterEqual(len(conflict["sides"]), 2, row["query_id"])
            for side in conflict["sides"]:
                self.assertTrue(side["statement"].strip())
                self.assertTrue(side["supporting_evidence_ids"])


class TestLeakage(BenchmarkTestCase):
    def test_queries_do_not_leak_evaluation_internals(self):
        for row in self.rows:
            query = row["query"]
            self.assertNotRegex(query, r"\bE\d{3}\b", f"{row['query_id']} leaks an evidence handle")
            self.assertNotRegex(query, r"DOC\d{6}", f"{row['query_id']} leaks a document id")
            self.assertNotIn("ContextPacket", query, row["query_id"])
            self.assertNotIn("packet", query.lower(), row["query_id"])

    def test_queries_do_not_contain_the_gold_span(self):
        for row in self.rows:
            for support in row["gold_support"]:
                span = support["literal_span"]
                if len(span) > 40:
                    self.assertNotIn(span, row["query"], f"{row['query_id']} query contains gold text")


class TestManifest(BenchmarkTestCase):
    def test_manifest_sha_matches_artifact(self):
        self.assertIsNotNone(self.manifest, "manifest missing")
        actual = hashlib.sha256(BENCHMARK.read_bytes()).hexdigest()
        self.assertEqual(self.manifest["benchmark_jsonl_sha256"], actual,
                         "benchmark file changed after freeze; create v2 instead of editing v1")

    def test_manifest_is_frozen_and_consistent(self):
        manifest = self.manifest
        self.assertEqual(manifest["status"], "frozen")
        self.assertEqual(manifest["item_count"], 72)
        self.assertEqual(manifest["category_distribution"], EXPECTED_DISTRIBUTION)
        self.assertEqual(manifest["generation_calls_during_authoring"], 0)

    def test_manifest_pins_frozen_upstream_components(self):
        manifest = self.manifest
        self.assertEqual(manifest["retriever_sha"],
                         "8ada31f64d8ef51c3b4d3b8b04f3fcc3e9fb7338b1554d1a5a9118a3a231b071")
        self.assertEqual(manifest["context_implementation_sha"],
                         "4bcf5c9975ef0328eba159c34e7e2810491510dad6dc72b32ab10df1a777991d")
        self.assertEqual(manifest["citation_validator_version"], "citation-validator-v1.2")
        self.assertEqual(manifest["system_prompt_version"], "generation-system-prompt-v3")
        self.assertEqual(manifest["system_prompt_sha"],
                         "d3cadd465e2733d0cdd451d146407f28f80cefc784b432088fc20ecf7526dc74")
        self.assertEqual(manifest["runtime_loaded_context"], 71936)

    def test_manifest_distribution_matches_rows(self):
        counts = collections.Counter(row["language"] for row in self.rows)
        self.assertEqual(self.manifest["language_distribution"], dict(sorted(counts.items())))
        answer = collections.Counter(row["answerability"] for row in self.rows)
        self.assertEqual(self.manifest["answerability_distribution"], dict(sorted(answer.items())))


if __name__ == "__main__":
    unittest.main()
