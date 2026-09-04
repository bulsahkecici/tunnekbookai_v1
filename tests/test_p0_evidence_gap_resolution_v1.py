"""Tests for P0 Evidence Gap Resolution v1 - the protocol, not the outcome.

The phase is allowed to resolve nothing. It is not allowed to resolve something dishonestly, so
almost every assertion here is about the *route* a claim took rather than about how many claims
there are: was the packet searched before anything was generated, does every span actually exist,
did a moved threshold stay broken, can a partially resolved gap call itself resolved, can a
section be ready with a P0 requirement open.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "data/book"
P0 = BOOK / "p0_resolution"
MANIFEST = BOOK / "manifests/p0_evidence_gap_resolution_v1.json"
DESCRIPTOR = ROOT / "data/metadata/p0_evidence_gap_resolution_v1.json"
REPORT = ROOT / "reports/p0_evidence_gap_resolution_v1.md"
REMEDIATION_MANIFEST = BOOK / "manifests/book_evidence_remediation_v1.json"
SECTIONS = ("SEC-02-1", "SEC-02-2", "SEC-02-3")

_spec = importlib.util.spec_from_file_location(
    "p0_resolution_v1", ROOT / "scripts/43_p0_evidence_gap_resolution_v1.py")
R = importlib.util.module_from_spec(_spec)
sys.modules["p0_resolution_v1"] = R
_spec.loader.exec_module(R)


def load(path) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


MANIFEST_DATA = json.loads(MANIFEST.read_text(encoding="utf-8"))
DESCRIPTOR_DATA = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
GAPS = [json.loads(p.read_text(encoding="utf-8"))
        for p in sorted((P0 / "questions").glob("GAP-P0-*.json"))]
MAPPINGS = load(P0 / "evidence/manual_support_mappings_v1.jsonl")
CROSS_LINGUAL = load(P0 / "evidence/cross_lingual_p0_mappings_v1.jsonl")
CLAUSES = {c["clause_id"]: c for c in load(P0 / "evidence/clause_universe_v1.jsonl")}
GENERATION = load(P0 / "audits/p0_generation_attempts_v1.jsonl")
EXPANSION = load(P0 / "audits/p0_retrieval_expansion_v1.jsonl")
PROBES = load(P0 / "audits/p0_retrieval_gap_probes_v1.jsonl")
NUMERIC = load(P0 / "audits/p0_numeric_review_v1.jsonl")
LEDGERS = {s: load(P0 / f"claims/{s}.jsonl") for s in SECTIONS}
BUNDLES = {s: json.loads((P0 / f"bundles/{s}.json").read_text(encoding="utf-8"))
           for s in SECTIONS}
UNIVERSE = R.FrozenPacketUniverse()


class TestPhaseShape(unittest.TestCase):
    def test_all_six_p0_gaps_processed(self):
        self.assertEqual(len(GAPS), 6)
        self.assertEqual(MANIFEST_DATA["p0_gap_count"], 6)
        self.assertEqual(sorted(g["question_id"] for g in GAPS),
                         ["Q-02-1-01", "Q-02-1-02", "Q-02-2-01", "Q-02-2-02",
                          "Q-02-3-01", "Q-02-3-02"])

    def test_gap_statuses_are_from_the_allowed_vocabulary(self):
        for gap in GAPS:
            self.assertIn(gap["status"], R.GAP_STATUSES)

    def test_every_gap_records_its_entering_classes(self):
        remediation = json.loads(REMEDIATION_MANIFEST.read_text(encoding="utf-8"))
        expected = {q: classes for summary in remediation["section_summaries"].values()
                    for q, classes in summary["p0_gap_classification"].items()}
        for gap in GAPS:
            self.assertEqual(gap["gap_classes"], expected[gap["question_id"]])

    def test_outputs_exist(self):
        for name in ("questions", "evidence", "claims", "bundles", "audits"):
            self.assertTrue((P0 / name).is_dir(), name)
        self.assertTrue(REPORT.exists())


class TestExistingEvidenceFirst(unittest.TestCase):
    """Rule 8/11/12/26: the packet is inspected before anything else happens."""

    def test_every_gap_inspected_its_full_packet(self):
        for gap in GAPS:
            self.assertTrue(gap["packet_exhausted"], gap["gap_id"])
            self.assertEqual(gap["packet_items_inspected"],
                             len(UNIVERSE.evidence_ids(gap["question_id"])))
            self.assertGreater(gap["packet_items_inspected"], 0)

    def test_no_generation_occurred_before_the_packet_was_exhausted(self):
        for attempt in GENERATION:
            gap = next(g for g in GAPS if g["gap_id"] == attempt["gap_id"])
            if attempt["status"] != "NOT_EXECUTED":
                self.assertTrue(gap["packet_exhausted"], attempt["gap_id"])
            self.assertIn("decision_reason", attempt)

    def test_no_retrieval_ran_before_the_packet_was_exhausted(self):
        for row in EXPANSION:
            if row["decision"] != "NOT_PERFORMED":
                gap = next(g for g in GAPS if g["gap_id"] == row["gap_id"])
                self.assertTrue(gap["packet_exhausted"])
                self.assertTrue(row["retrieval_gap_confirmed"])

    def test_manifest_reports_zero_generation_and_retrieval_calls(self):
        self.assertEqual(MANIFEST_DATA["generation_calls"], 0)
        self.assertEqual(MANIFEST_DATA["retrieval_calls"], 0)


class TestSpanIntegrity(unittest.TestCase):
    """Rule: no invented spans. Every one is re-derived from the frozen chunk here, independently
    of the controller's own verification."""

    def test_every_manual_span_is_verbatim_in_its_named_packet_item(self):
        self.assertTrue(MAPPINGS)
        for mapping in MAPPINGS:
            self.assertTrue(mapping["span_verified"], mapping["mapping_id"])
            self.assertTrue(
                UNIVERSE.contains_span(mapping["question_id"], mapping["evidence_id"],
                                       mapping["source_span"]),
                f"{mapping['mapping_id']} span not in {mapping['evidence_id']}")

    def test_every_cross_lingual_span_is_verbatim_in_its_named_packet_item(self):
        self.assertTrue(CROSS_LINGUAL)
        for mapping in CROSS_LINGUAL:
            evidence_id = mapping["source_evidence_ref"]["evidence_id"]
            self.assertTrue(
                UNIVERSE.contains_span(mapping["question_id"], evidence_id,
                                       mapping["source_span_en"]),
                f"{mapping['mapping_id']} span not in {evidence_id}")

    def test_no_span_comes_from_outside_the_question_packet(self):
        for mapping in MAPPINGS:
            item = UNIVERSE.item(mapping["question_id"], mapping["evidence_id"])
            self.assertIsNotNone(item, mapping["mapping_id"])
            self.assertEqual(item["chunk_id"], mapping["chunk_id"])
            self.assertEqual(item["context_packet_sha"], mapping["context_packet_sha"])

    def test_support_relations_and_verdicts_are_from_the_allowed_vocabulary(self):
        for mapping in MAPPINGS:
            self.assertIn(mapping["support_relation"], R.SUPPORT_RELATIONS)
            self.assertIn(mapping["manual_verdict"], R.MANUAL_VERDICTS)
        for mapping in CROSS_LINGUAL:
            self.assertIn(mapping["mapping_status"], R.CROSS_LINGUAL_STATUSES)


class TestGenerationBounds(unittest.TestCase):
    """Rules 31/32/36: at most two revised-query attempts, and never a same-question retry."""

    def test_no_gap_exceeds_two_generation_attempts(self):
        for gap in GAPS:
            self.assertLessEqual(gap["generation_attempts"],
                                 R.MAX_GENERATION_ATTEMPTS_PER_GAP, gap["gap_id"])
        counts: dict[str, int] = {}
        for attempt in GENERATION:
            if attempt["status"] != "NOT_EXECUTED":
                counts[attempt["gap_id"]] = counts.get(attempt["gap_id"], 0) + 1
        for gap_id, count in counts.items():
            self.assertLessEqual(count, R.MAX_GENERATION_ATTEMPTS_PER_GAP, gap_id)

    def test_a_revised_query_is_never_the_original_question(self):
        questions = {q["question_id"]: q["question"] for q in R.load_questions()}
        for revision in load(P0 / "audits/p0_query_revisions_v1.jsonl"):
            self.assertNotEqual(revision["revised_question"].strip(),
                                questions[revision["original_question_id"]].strip())
            self.assertNotEqual(revision["revised_question_id"],
                                revision["original_question_id"])
            self.assertTrue(revision["revision_reason"])

    def test_a_revised_query_does_not_lead_the_answer(self):
        """Rule 30: the query may name the missing proposition, never supply its content."""
        for revision in load(P0 / "audits/p0_query_revisions_v1.jsonl"):
            self.assertNotRegex(revision["revised_question"], r"\d{3}\s*kg/m")

    def test_generation_only_considered_for_a_synthesis_defect(self):
        for attempt in GENERATION:
            gap = next(g for g in GAPS if g["gap_id"] == attempt["gap_id"])
            self.assertIn("GENERATOR_SYNTHESIS_DEFECT", gap["gap_classes"])


class TestPinnedDefects(unittest.TestCase):
    """The specific errors this phase is forbidden to launder."""

    def test_the_tbm_threshold_was_not_moved(self):
        for clause_id in R.PINNED_THRESHOLD_DEFECT["clause_ids"]:
            self.assertEqual(CLAUSES[clause_id]["resolution_status"], "UNSUPPORTED", clause_id)
            self.assertTrue(CLAUSES[clause_id].get("threshold_defect_pinned"))
        self.assertTrue(MANIFEST_DATA["go_conditions"]["moved_threshold_still_unsupported"])

    def test_no_mapping_accepts_below_1_5_as_the_conventional_threshold(self):
        for mapping in CROSS_LINGUAL:
            if mapping["clause_id"] in R.PINNED_THRESHOLD_DEFECT["clause_ids"]:
                self.assertEqual(mapping["mapping_status"], "NOT_SUPPORTED")
        for claim in (e for s in SECTIONS for e in LEDGERS[s]
                      if e.get("origin") == "p0_resolution_v1"):
            if claim["citation_ready"]:
                self.assertNotRegex(claim["canonical_claim"], r"1[.,]5\s*'?[iı]n\s+alt")

    def test_the_source_threshold_of_1_survives_in_the_reconstruction(self):
        reconstructed = [c for c in CLAUSES.values()
                         if c["clause_id"] == "R-Q-02-3-01-01"]
        self.assertEqual(len(reconstructed), 1)
        self.assertIn("1'in altında", reconstructed[0]["clause_text"])

    def test_derived_conversion_stays_derived(self):
        derived = [row for row in NUMERIC if row.get("value") == "150"]
        self.assertEqual(len(derived), 1)
        self.assertTrue(derived[0]["derived"])
        self.assertFalse(derived[0]["source_stated"])

    def test_360_and_400_are_promoted_only_with_evidence_ids(self):
        for value in ("360", "400"):
            row = next(r for r in NUMERIC if r.get("value") == value)
            self.assertTrue(row["source_stated"], value)
            self.assertTrue(row["evidence_ids"], value)
            for evidence_id in row["evidence_ids"]:
                text = UNIVERSE.text(row["question_id"], evidence_id)
                self.assertTrue(R.number_in(value, text),
                                f"{value} not literally in {evidence_id}")

    def test_the_20_bar_misattribution_is_recorded_and_not_promoted(self):
        row = next(r for r in NUMERIC if r.get("value") == "20" and r.get("unit") == "bar")
        self.assertFalse(row["source_stated"])
        self.assertNotEqual(CLAUSES["Q-02-3-02-N10-C01"]["resolution_status"], "SUPPORTED")


class TestNumericSafety(unittest.TestCase):
    def test_every_value_in_a_supported_clause_is_in_its_mapped_evidence(self):
        for clause in CLAUSES.values():
            if clause["resolution_status"] != "SUPPORTED" or not clause["resolution_mappings"]:
                continue
            texts = [UNIVERSE.text(clause["question_id"], e)
                     for e in clause.get("supporting_evidence_ids") or []]
            for value in R.numeric_literals(clause["clause_text"]):
                self.assertTrue(any(R.number_in(value, t) for t in texts),
                                f"{clause['clause_id']} promotes {value} with no source span")

    def test_no_citation_ready_claim_carries_an_unstated_value(self):
        for section in SECTIONS:
            for entry in LEDGERS[section]:
                if entry.get("origin") != "p0_resolution_v1" or not entry["citation_ready"]:
                    continue
                for fact in entry.get("numeric_data") or []:
                    self.assertTrue(fact["source_stated"], entry["claim_id"])
                    self.assertFalse(fact["derived"], entry["claim_id"])


class TestResolutionCompleteness(unittest.TestCase):
    """Rules 54/55: a partly resolved gap may not call itself RESOLVED."""

    def test_a_resolved_gap_has_no_clause_short_of_supported(self):
        for gap in GAPS:
            if gap["status"] != "RESOLVED":
                continue
            self.assertEqual(gap["remaining_missing_propositions"], [], gap["gap_id"])
            for clause in CLAUSES.values():
                if clause["question_id"] == gap["question_id"] and clause["material"] \
                        and not clause["superseded"]:
                    self.assertEqual(clause["resolution_status"], "SUPPORTED",
                                     f"{gap['gap_id']} / {clause['clause_id']}")

    def test_a_gap_with_remaining_propositions_is_not_resolved(self):
        for gap in GAPS:
            if gap["remaining_missing_propositions"]:
                self.assertNotEqual(gap["status"], "RESOLVED", gap["gap_id"])

    def test_partially_resolved_gaps_still_produced_claims(self):
        for gap in GAPS:
            if gap["status"] == "PARTIALLY_RESOLVED":
                self.assertTrue(gap["resolved_claim_ids"], gap["gap_id"])

    def test_no_gap_was_closed_by_deleting_a_proposition(self):
        """Every superseded clause is replaced, and every dropped synthesis keeps its components."""
        for clause in CLAUSES.values():
            if clause["superseded"]:
                self.assertTrue(clause["superseded_by"], clause["clause_id"])
                for replacement in clause["superseded_by"]:
                    self.assertIn(replacement, CLAUSES)
        for entry in load(P0 / "audits/p0_dropped_syntheses_v1.jsonl"):
            self.assertTrue(entry["components_retained"])
            self.assertFalse(entry["citable_as_compound"])
            for component in entry["components_retained"]:
                self.assertIn(component, CLAUSES)


class TestReadiness(unittest.TestCase):
    """Rules 58/59/60/82: readiness is recomputed, and cannot be reached over an open P0 gap."""

    def test_readiness_recomputed_for_every_section(self):
        self.assertEqual(set(MANIFEST_DATA["section_readiness"]), set(SECTIONS))
        for section in SECTIONS:
            self.assertIn(BUNDLES[section]["readiness_assessment"]["readiness"],
                          ("READY_FOR_DRAFT", "READY_WITH_LIMITATIONS", "NOT_READY"))

    def test_a_ready_section_has_no_open_or_partial_p0_gap(self):
        for section in SECTIONS:
            assessment = BUNDLES[section]["readiness_assessment"]
            if assessment["readiness"] == "NOT_READY":
                continue
            for question_id, status in assessment["p0_gap_status"].items():
                self.assertEqual(status, "RESOLVED", f"{section} / {question_id}")

    def test_a_ready_section_has_no_unsupported_clause_under_a_p0_objective(self):
        for section in SECTIONS:
            assessment = BUNDLES[section]["readiness_assessment"]
            if assessment["readiness"] == "NOT_READY":
                continue
            self.assertEqual(assessment["critical_unsupported_clauses"], [], section)
            self.assertEqual(assessment["critical_numeric_clauses"], [], section)
            self.assertEqual(assessment["critical_cross_lingual_clauses"], [], section)
            self.assertEqual(assessment["p0_without_citation_ready_claim"], [], section)
            self.assertTrue(assessment["provenance_complete"], section)

    def test_ready_with_limitations_actually_records_limitations(self):
        for section in SECTIONS:
            assessment = BUNDLES[section]["readiness_assessment"]
            if assessment["readiness"] == "READY_WITH_LIMITATIONS":
                self.assertTrue(assessment["limitations"], section)
            if assessment["readiness"] == "READY_FOR_DRAFT":
                self.assertEqual(assessment["limitations"], [], section)

    def test_a_not_ready_section_says_why(self):
        for section in SECTIONS:
            assessment = BUNDLES[section]["readiness_assessment"]
            if assessment["readiness"] == "NOT_READY":
                self.assertTrue(assessment["readiness_reasons"], section)

    def test_readiness_thresholds_were_not_loosened(self):
        """The clause thresholds inherited from the manual audit are pinned in v1.1 and unchanged."""
        extractor = R.extractor_v1_1
        self.assertEqual(extractor.CLAUSE_SUPPORTED_COVERAGE, 0.50)
        self.assertEqual(extractor.CLAUSE_PARTIAL_COVERAGE, 0.25)
        self.assertEqual(extractor.UPGRADE_COVERAGE, 0.60)


class TestRetrievalAndCorpus(unittest.TestCase):
    """Rules 37-46, 83-84."""

    def test_a_retrieval_gap_is_only_claimed_after_the_packet_was_searched(self):
        for probe in PROBES:
            self.assertEqual(probe["packet_items_searched"],
                             len(UNIVERSE.evidence_ids(probe["question_id"])))
            if probe["retrieval_gap_candidate"]:
                self.assertFalse(probe["proposition_carried_after_resolution"])
                self.assertEqual(probe["items_mentioning_any_term"], [])

    def test_expansion_only_for_confirmed_gaps_and_within_the_ceiling(self):
        for row in EXPANSION:
            if row["decision"] == "NOT_PERFORMED":
                self.assertIsNone(row["experimental_top_k"])
                continue
            self.assertTrue(row["retrieval_gap_confirmed"])
            self.assertLessEqual(row["experimental_top_k"], R.RETRIEVAL_EXPANSION_CEILING)
            self.assertIn(row["experimental_top_k"], R.RETRIEVAL_EXPANSION_LADDER)
            self.assertEqual(row["qdrant_writes"], 0)

    def test_production_retrieval_default_is_untouched(self):
        self.assertEqual(R.RETRIEVAL_BASELINE_TOP_K, 20)
        self.assertTrue(DESCRIPTOR_DATA["retrieval_expansion_policy"]
                        ["production_default_unchanged"])

    def test_a_corpus_gap_requires_retrieval_to_have_been_exhausted(self):
        if MANIFEST_DATA["corpus_gap_candidates"]:
            self.assertGreater(MANIFEST_DATA["retrieval_expansion_attempts"], 0)

    def test_no_claim_rests_on_expanded_retrieval(self):
        for section in SECTIONS:
            for entry in LEDGERS[section]:
                if entry.get("origin") == "p0_resolution_v1":
                    self.assertNotEqual(entry["resolution_source"], "expanded_retrieval")


class TestProvenance(unittest.TestCase):
    """Rule 85: packet sha, evidence id, chunk, document and source key must all resolve."""

    def test_every_citation_ready_claim_resolves_end_to_end(self):
        chunks = R.audit_v1.load_chunks(
            {item["chunk_id"] for item in UNIVERSE.items.values()})
        for section in SECTIONS:
            for entry in LEDGERS[section]:
                if entry.get("origin") != "p0_resolution_v1" or not entry["citation_ready"]:
                    continue
                self.assertTrue(entry["evidence_refs"], entry["claim_id"])
                self.assertTrue(entry["source_keys"], entry["claim_id"])
                for ref in entry["evidence_refs"]:
                    self.assertTrue(ref["context_packet_sha"], entry["claim_id"])
                    self.assertIn(ref["chunk_id"], chunks, entry["claim_id"])
                    self.assertEqual(chunks[ref["chunk_id"]]["document_id"], ref["document_id"])
                    expected = "SRC-{}-{}".format(
                        ref["document_id"],
                        hashlib.sha256(f"{ref['document_id']}|{ref['chunk_id']}"
                                       .encode("utf-8")).hexdigest()[:12])
                    self.assertEqual(ref["source_key"], expected, entry["claim_id"])
                    self.assertEqual(
                        UNIVERSE.item(entry["question_id"], ref["evidence_id"])["chunk_id"],
                        ref["chunk_id"])

    def test_the_frozen_source_registry_was_not_modified(self):
        self.assertFalse(MANIFEST_DATA["source_registry_modified"])
        check = next(c for c in MANIFEST_DATA["frozen_integrity"]["checks"]
                     if c["name"].startswith("source registry v1"))
        self.assertTrue(check["unchanged"])

    def test_new_source_keys_live_in_this_phase_own_registry(self):
        frozen = {row["chunk_id"] for row in
                  load(BOOK / "source_registry_v1.jsonl")}
        local = {row["chunk_id"] for row in load(P0 / "evidence/p0_source_registry_v1.jsonl")}
        self.assertFalse(frozen & local)


class TestFrozenIntegrity(unittest.TestCase):
    def test_nothing_upstream_changed(self):
        integrity = MANIFEST_DATA["frozen_integrity"]
        self.assertEqual(integrity["changed"], [])
        self.assertTrue(integrity["all_unchanged"])
        for check in integrity["checks"]:
            self.assertIsNotNone(check["expected_sha256"], check["name"])
            self.assertEqual(check["actual_sha256"], check["expected_sha256"], check["name"])

    def test_the_baseline_covers_every_frozen_component(self):
        names = {c["name"] for c in MANIFEST_DATA["frozen_integrity"]["checks"]}
        for required in ("Retriever v1", "Context v1", "Prompt v5", "Output Contract v1.1",
                         "Production Grounded Generator v1", "Evidence Note Contract v1",
                         "Book Pipeline v1", "Book Pipeline Extractor v1.1",
                         "Pilot Manual Evidence Audit v1", "chunks", "production audit log"):
            self.assertIn(required, names)

    def test_remediation_v1_artifacts_are_intact(self):
        remediation = json.loads(REMEDIATION_MANIFEST.read_text(encoding="utf-8"))
        checked = {c["path"] for c in MANIFEST_DATA["frozen_integrity"]["checks"]}
        for relative in remediation["artifact_shas"]:
            base = "data/book/" if not relative.startswith("evaluation/") else "data/"
            self.assertIn(base + relative, checked, relative)

    def test_qdrant_is_read_only_and_unchanged(self):
        self.assertEqual(MANIFEST_DATA["qdrant_writes"], 0)
        self.assertEqual(MANIFEST_DATA["qdrant_points_before"],
                         MANIFEST_DATA["qdrant_points_after"])
        if MANIFEST_DATA["qdrant_points_before"] is not None:
            self.assertEqual(MANIFEST_DATA["qdrant_points_before"], R.QDRANT_EXPECTED_POINTS)


class TestDraftingStaysOff(unittest.TestCase):
    def test_drafting_disabled_everywhere(self):
        self.assertFalse(R.DRAFTING_ENABLED)
        self.assertFalse(MANIFEST_DATA["drafting_enabled"])
        self.assertFalse(DESCRIPTOR_DATA["drafting_enabled"])
        for section in SECTIONS:
            self.assertFalse(BUNDLES[section]["drafting_enabled"])

    def test_no_prose_artifact_was_written(self):
        """The phase may write claims and audits. A drafted section would look like a long piece
        of free text under claims/ or bundles/, so assert the shape stays structured."""
        for path in (P0 / "claims").glob("*"):
            self.assertEqual(path.suffix, ".jsonl")
        for path in (P0 / "bundles").glob("*"):
            self.assertEqual(path.suffix, ".json")
        for section in SECTIONS:
            self.assertNotIn("draft", BUNDLES[section])
            self.assertNotIn("prose", BUNDLES[section])


class TestGoGate(unittest.TestCase):
    def test_go_conditions_are_all_evaluated(self):
        conditions = MANIFEST_DATA["go_conditions"]
        for required in ("all_p0_gaps_processed", "existing_packet_evidence_checked_first",
                         "every_mapping_span_verified", "generation_bounded",
                         "retrieval_expansion_justified", "no_unsupported_numeric_promoted",
                         "moved_threshold_still_unsupported", "all_claims_traceable",
                         "readiness_recomputed", "frozen_integrity_holds",
                         "qdrant_writes_zero", "drafting_disabled"):
            self.assertIn(required, conditions)

    def test_status_matches_the_gates(self):
        expected = "closed_go" if all(MANIFEST_DATA["go_conditions"].values()) else "closed_no_go"
        self.assertEqual(MANIFEST_DATA["status"], expected)

    def test_report_separates_processing_from_resolution(self):
        text = REPORT.read_text(encoding="utf-8")
        for heading in ("## Executive Decision", "## Existing Evidence First",
                        "## Extraction Failures", "## Manual Span Mapping",
                        "## Cross-Lingual Mapping", "## Generator Synthesis Defects",
                        "## Retrieval Gap Assessment", "## Corpus Gap Assessment",
                        "## Numeric Safety", "## Conflict Review", "## Recomputed Readiness",
                        "## Remaining P0 Gaps", "## Frozen Integrity", "## Final Decision"):
            self.assertIn(heading, text)
        self.assertIn("processed", text)


if __name__ == "__main__":
    unittest.main()
