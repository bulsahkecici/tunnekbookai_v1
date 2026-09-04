"""Frozen generation evaluation benchmark v2 — corrected, contamination-free holdout.

v2 exists because Phase B exposed four authoring defects in v1 and because several v1 items were
inspected while developing prompts v4/v5. Those items can no longer serve as holdout. These tests
protect the correction: the replaced items are gone, the replacements are genuinely fresh, no
development query or packet leaked in, and every gold span still resolves exactly.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "data/evaluation/generation_eval_benchmark_v2.jsonl"
PACKETS = ROOT / "data/evaluation/generation_eval_benchmark_v2_packets.jsonl"
MANIFEST = ROOT / "data/evaluation/generation_eval_benchmark_v2_manifest.json"
V1 = ROOT / "data/evaluation/generation_eval_benchmark_v1.jsonl"
DEV = ROOT / "data/evaluation/generation_dev_regression_v1.jsonl"
LANGDEV = ROOT / "data/evaluation/generation_language_dev_regression_v1.jsonl"

V1_SHA = "de3c1684ad26b459e6a209a9ef770c1a0f0fae39b44d0d251bc492ca3f75bd6b"
MUST_REPLACE = {"GEV042", "GEV045", "GEV051", "GEV058", "GEV061", "GEV064", "GEV065", "GEV066",
                "GEV070"}
EXPECTED_DISTRIBUTION = {
    "direct_factual_conceptual": 18, "design_construction": 10, "multi_source_synthesis": 10,
    "numeric_table": 8, "regulation_specification": 6, "cross_lingual": 6, "must_abstain": 8,
    "injection_adversarial": 6,
}


def _rows(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


class V2TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not BENCHMARK.is_file():
            raise unittest.SkipTest("benchmark v2 not built")
        cls.items = _rows(BENCHMARK)
        cls.packets = {p["packet_sha"]: p for p in _rows(PACKETS)}
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.v1 = {r["query_id"]: r for r in _rows(V1)}


class TestShape(V2TestCase):
    def test_exactly_72_items_with_stable_ids(self):
        self.assertEqual(len(self.items), 72)
        ids = [i["query_id"] for i in self.items]
        self.assertEqual(ids, [f"GEV{i:03d}" for i in range(1, 73)])

    def test_exact_category_distribution(self):
        counts = collections.Counter(i["primary_query_type"] for i in self.items)
        self.assertEqual(dict(counts), EXPECTED_DISTRIBUTION)

    def test_exact_language_balance(self):
        counts = collections.Counter(i["language"] for i in self.items)
        self.assertEqual(dict(counts), {"tr": 36, "en": 36})

    def test_benchmark_version_uniform(self):
        self.assertEqual({i["benchmark_version"] for i in self.items},
                         {"generation-eval-benchmark-v2"})


class TestReplacementAndContamination(V2TestCase):
    def test_every_required_v1_item_was_replaced(self):
        replaced = {i["benchmark_item_lineage"]["v1_query_id"] for i in self.items
                    if i["benchmark_item_lineage"]["status"] == "replaced"}
        missing = MUST_REPLACE - replaced
        self.assertEqual(missing, set(), f"still carried unchanged: {sorted(missing)}")

    def test_replaced_items_do_not_reuse_the_v1_query_or_packet(self):
        for item in self.items:
            lineage = item["benchmark_item_lineage"]
            if lineage["status"] != "replaced":
                continue
            old = self.v1[lineage["v1_query_id"]]
            self.assertNotEqual(item["query"].strip().lower(), old["query"].strip().lower(),
                                f"{item['query_id']} reused the v1 query")
            self.assertNotEqual(item["context_packet_sha"], old["context_packet_sha"],
                                f"{item['query_id']} reused the v1 packet")
            self.assertTrue(lineage["replacement_is_fresh_holdout"])

    def test_replacement_keeps_the_same_primary_category(self):
        for item in self.items:
            lineage = item["benchmark_item_lineage"]
            if lineage["status"] == "replaced":
                self.assertEqual(item["primary_query_type"],
                                 self.v1[lineage["v1_query_id"]]["primary_query_type"],
                                 item["query_id"])

    def test_carried_items_are_unchanged_in_query_and_packet(self):
        for item in self.items:
            if item["benchmark_item_lineage"]["status"] != "carried_forward_clean":
                continue
            old = self.v1[item["query_id"]]
            self.assertEqual(item["query"], old["query"])
            self.assertEqual(item["context_packet_sha"], old["context_packet_sha"])

    def test_all_items_are_clean_holdout(self):
        for item in self.items:
            self.assertEqual(item["contamination_status"], "clean_holdout", item["query_id"])

    def test_no_development_query_or_packet_leaked_in(self):
        dev_queries, dev_packets = set(), set()
        for path, key in ((DEV, "dev_id"), (LANGDEV, "lang_id")):
            if path.is_file():
                for row in _rows(path):
                    dev_queries.add(row["query"].strip().lower())
                    dev_packets.add(row["context_packet_sha"])
        self.assertTrue(dev_queries, "development sets missing; contamination check is vacuous")
        for item in self.items:
            self.assertNotIn(item["query"].strip().lower(), dev_queries,
                             f"{item['query_id']} reuses a development query")
            self.assertNotIn(item["context_packet_sha"], dev_packets,
                             f"{item['query_id']} reuses a development packet")

    def test_no_duplicate_queries(self):
        queries = [i["query"].strip().lower() for i in self.items]
        self.assertEqual(len(set(queries)), 72)


class TestGoldIntegrity(V2TestCase):
    def test_literal_spans_resolve_exactly(self):
        checked = 0
        for item in self.items:
            packet = self.packets[item["context_packet_sha"]]
            evidence = {e["evidence_id"]: e for e in packet["evidence"]}
            for support in item["gold_support"]:
                self.assertEqual(support["span_scope"], "evidence_item")
                text = evidence[support["evidence_id"]]["text"]
                self.assertEqual(text[support["span_start"]:support["span_end"]],
                                 support["literal_span"],
                                 f"{item['query_id']} span drift on {support['evidence_id']}")
                checked += 1
        self.assertGreater(checked, 100)

    def test_gold_cites_only_packet_evidence(self):
        for item in self.items:
            exposed = set(item["evidence_ids"])
            for claim in item["gold_claims"]:
                for handle in claim["supporting_evidence_ids"]:
                    self.assertIn(handle, exposed, item["query_id"])
                for alt in claim["acceptable_alternatives"]:
                    for handle in alt["supporting_evidence_ids"]:
                        self.assertIn(handle, exposed, item["query_id"])

    def test_every_claim_carries_the_alternatives_field(self):
        for item in self.items:
            for claim in item["gold_claims"]:
                self.assertIn("acceptable_alternatives", claim, item["query_id"])
                self.assertIsInstance(claim["acceptable_alternatives"], list)

    def test_numeric_gold_schema_including_alternatives(self):
        for item in self.items:
            for entry in item["numeric_gold"] or []:
                for field in ("value", "unit", "operation", "direction", "tolerance",
                              "supporting_evidence_ids", "literal_span", "span_start", "span_end",
                              "span_scope", "alternative_valid_values"):
                    self.assertIn(field, entry, item["query_id"])
                self.assertTrue(entry["unit"], item["query_id"])
                packet = self.packets[item["context_packet_sha"]]
                evidence = {e["evidence_id"]: e for e in packet["evidence"]}
                for alt in entry["alternative_valid_values"]:
                    text = evidence[alt["supporting_evidence_id"]]["text"]
                    self.assertEqual(text[alt["span_start"]:alt["span_end"]], alt["literal_span"],
                                     f"{item['query_id']} alternative span drift")

    def test_multiple_valid_values_flag_matches_the_data(self):
        for item in self.items:
            has_alt = any(entry["alternative_valid_values"] for entry in item["numeric_gold"] or [])
            if has_alt:
                self.assertTrue(item["multiple_valid_values"], item["query_id"])

    def test_no_gold_span_reused_across_items(self):
        seen = collections.Counter()
        for item in self.items:
            for support in item["gold_support"]:
                seen[(support["evidence_text_sha256"], support["span_start"],
                      support["span_end"])] += 1
        self.assertFalse([k for k, v in seen.items() if v > 1])


class TestAbstentionAndRetrievalLimited(V2TestCase):
    def test_must_abstain_items_are_manually_absence_verified(self):
        abstain = [i for i in self.items if i["must_abstain"]]
        self.assertEqual(len(abstain), 8)
        for item in abstain:
            self.assertTrue(item["manual_packet_absence_verified"], item["query_id"])
            self.assertTrue((item["absence_audit_note"] or "").strip(),
                            f"{item['query_id']} has no absence audit note")
            self.assertEqual(item["answerability"], "unanswerable", item["query_id"])
            types = {c["claim_type"] for c in item["gold_claims"]}
            self.assertEqual(types, {"abstention"}, item["query_id"])

    def test_gev058_is_no_longer_an_unanswerable_item(self):
        """The v1 defect: alignment evidence was present but the gold said unanswerable."""
        item = next(i for i in self.items if i["query_id"] == "GEV058")
        self.assertFalse(item["must_abstain"])
        self.assertEqual(item["benchmark_item_lineage"]["reason"], "gold_mislabelled_unanswerable")

    def test_retrieval_limited_items_carry_positive_evidence(self):
        for item in self.items:
            if not item["retrieval_limited"]:
                self.assertIsNone(item["retrieval_limited_evidence"], item["query_id"])
                continue
            evidence = item["retrieval_limited_evidence"]
            self.assertIsNotNone(evidence, f"{item['query_id']} retrieval_limited without evidence")
            for field in ("corpus_chunk_id", "document_id", "quote"):
                self.assertIn(field, evidence, item["query_id"])
            self.assertTrue(evidence["quote"].strip())

    def test_every_item_records_a_manual_audit(self):
        for item in self.items:
            audit = item["manual_item_audit"]
            self.assertTrue(audit["reviewed"], item["query_id"])
            self.assertTrue(audit["answerability_verified"], item["query_id"])
            self.assertTrue(audit["spans_verified"], item["query_id"])
            if item["must_abstain"]:
                self.assertTrue(audit["packet_read"], item["query_id"])


class TestCrossLingual(V2TestCase):
    def test_cross_lingual_metadata_present_and_manually_verified(self):
        for item in self.items:
            if item["primary_query_type"] != "cross_lingual":
                continue
            meta = item["cross_lingual_metadata"]
            self.assertIsNotNone(meta, item["query_id"])
            for field in ("query_language", "dominant_evidence_language", "cross_lingual_direction",
                          "evidence_language_counts"):
                self.assertIn(field, meta, item["query_id"])
            self.assertEqual(meta["query_language"], item["language"], item["query_id"])


class TestLeakage(V2TestCase):
    def test_queries_do_not_leak_internals(self):
        for item in self.items:
            self.assertNotRegex(item["query"], r"\bE\d{3}\b", item["query_id"])
            self.assertNotRegex(item["query"], r"DOC\d{6}", item["query_id"])
            self.assertNotIn("packet", item["query"].lower(), item["query_id"])


class TestManifestAndFreeze(V2TestCase):
    def test_manifest_hashes_match_the_artifacts(self):
        self.assertEqual(self.manifest["benchmark_jsonl_sha256"],
                         hashlib.sha256(BENCHMARK.read_bytes()).hexdigest(),
                         "benchmark v2 changed after freeze; corrections become v3")
        self.assertEqual(self.manifest["packets_sha256"],
                         hashlib.sha256(PACKETS.read_bytes()).hexdigest())

    def test_manifest_is_frozen_and_generator_independent(self):
        self.assertEqual(self.manifest["status"], "frozen")
        self.assertEqual(self.manifest["item_count"], 72)
        self.assertEqual(self.manifest["generation_calls"], 0)
        self.assertTrue(self.manifest["authoring_generator_independent"])
        self.assertIsNone(self.manifest["authoring_system_prompt_identity"])
        self.assertTrue(self.manifest["intended_candidate_not_used_in_authoring"])

    def test_manifest_records_lineage_from_v1(self):
        self.assertEqual(self.manifest["benchmark_v1_parent_sha"], V1_SHA)
        self.assertEqual(self.manifest["replaced_item_count"], 10)
        self.assertEqual(self.manifest["carried_forward_count"], 62)
        self.assertTrue(MUST_REPLACE <= set(self.manifest["replaced_query_ids"]))

    def test_benchmark_v1_is_untouched(self):
        self.assertEqual(hashlib.sha256(V1.read_bytes()).hexdigest(), V1_SHA,
                         "benchmark v1 must remain historical evidence")

    def test_packet_archive_covers_every_item(self):
        self.assertEqual(len(self.packets), 72)
        for item in self.items:
            self.assertIn(item["context_packet_sha"], self.packets, item["query_id"])


if __name__ == "__main__":
    unittest.main()
