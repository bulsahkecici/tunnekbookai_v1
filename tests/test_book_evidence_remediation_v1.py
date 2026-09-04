"""Tests for Book Evidence Remediation v1 - the artifacts, not the algorithms.

These assert the properties a book depends on: every queue was processed, every span and reference
resolves to real frozen evidence, no gap was closed by deletion, and readiness was not tuned.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "data/book"
REMEDIATION = BOOK / "remediation"
NOTES_DIR = BOOK / "evidence_notes_remediated_v1"
LEDGER_DIR = BOOK / "claim_ledgers_remediated_v1"
BUNDLE_DIR = BOOK / "section_bundles_remediated_v1"
MANIFEST = BOOK / "manifests/book_evidence_remediation_v1.json"
DESCRIPTOR = ROOT / "data/metadata/book_pipeline_extractor_v1_1.json"
REGRESSION = ROOT / "data/evaluation/book_pipeline_extractor_v1_1_regression.jsonl"
SECTIONS = ("SEC-02-1", "SEC-02-2", "SEC-02-3")

_spec = importlib.util.spec_from_file_location(
    "extractor_v1_1_artifacts", ROOT / "scripts/42_book_pipeline_extractor_v1_1.py")
E = importlib.util.module_from_spec(_spec)
sys.modules["extractor_v1_1_artifacts"] = E
_spec.loader.exec_module(E)


def load(path):
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


MANIFEST_DATA = json.loads(MANIFEST.read_text(encoding="utf-8"))
NOTES = [n for section in SECTIONS for n in load(NOTES_DIR / f"{section}.jsonl")]
LEDGERS = [e for section in SECTIONS for e in load(LEDGER_DIR / f"{section}.jsonl")]
BUNDLES = {s: json.loads((BUNDLE_DIR / f"{s}.json").read_text(encoding="utf-8"))
           for s in SECTIONS}
SPAN_QUEUE = load(REMEDIATION / "literal_span_remediation_v1.jsonl")
XL_MAPS = load(REMEDIATION / "cross_lingual_support_maps_v1.jsonl")
NON_PROP = load(REMEDIATION / "non_proposition_remediation_v1.jsonl")
SPLITS = load(REMEDIATION / "split_note_remediation_v1.jsonl")
NUMERIC = load(REMEDIATION / "numeric_remediation_v1.jsonl")
ORIGINALS = {n["note_id"]: n
             for f in sorted((BOOK / "evidence_notes").glob("*.jsonl")) for n in load(f)}
AUDIT = {r["original_note_id"]: r
         for r in load(BOOK / "audits/pilot_evidence_note_manual_audit_v1.jsonl")}

_UNIVERSE = {}


def universe():
    if "u" not in _UNIVERSE:
        _UNIVERSE["u"] = E.EvidenceUniverse(list(ORIGINALS.values()))
    return _UNIVERSE["u"]


class TestQueuesProcessed(unittest.TestCase):
    def test_all_81_literal_span_notes_processed(self):
        queued = {nid for nid, row in AUDIT.items()
                  if row["recommended_action"] == "needs_manual_span"}
        self.assertEqual(len(queued), 81)
        self.assertEqual({r["original_note_id"] for r in SPAN_QUEUE}, queued)
        for row in SPAN_QUEUE:
            self.assertIn(row["decision"],
                          ("span_attached", "retain_insufficient", "dropped_non_proposition"))

    def test_all_11_cross_lingual_notes_processed(self):
        queued = {nid for nid, row in AUDIT.items()
                  if row["recommended_action"] == "attach_cross_lingual_mapping"}
        self.assertEqual(len(queued), 11)
        self.assertEqual({r["original_note_id"] for r in XL_MAPS}, queued)

    def test_all_28_non_proposition_notes_processed(self):
        queued = {nid for nid, row in AUDIT.items()
                  if row["recommended_action"] == "narrow_claim"}
        self.assertEqual(len(queued), 28)
        processed = {r["original_note_id"] for r in NON_PROP if r["queue_member"]}
        self.assertEqual(processed, queued)
        for row in NON_PROP:
            self.assertIn(row["decision"], E.NON_PROPOSITION_DECISIONS)

    def test_all_14_split_note_notes_processed(self):
        queued = {nid for nid, row in AUDIT.items()
                  if row["recommended_action"] == "split_note"}
        self.assertEqual(len(queued), 14)
        self.assertEqual({r["parent_note_id"] for r in SPLITS}, queued)
        for row in SPLITS:
            self.assertIn(row["decision"], ("split", "not_split"))

    def test_every_original_note_has_an_outcome(self):
        """Nothing may vanish: a note is either remediated or explicitly dropped, never lost."""
        remediated = {n["parent_note_id"] for n in NOTES}
        dropped = {r["original_note_id"] for r in NON_PROP}
        self.assertEqual(remediated | dropped, set(ORIGINALS))


class TestNoInventedEvidence(unittest.TestCase):
    def test_every_literal_span_occurs_verbatim_in_its_cited_chunk(self):
        chunk_by_handle = {}
        for note in NOTES:
            for ref in note["evidence_refs"]:
                chunk_by_handle[(note["parent_note_id"], ref["evidence_id"])] = ref["chunk_id"]
        for note in NOTES:
            for support in note["literal_support"]:
                chunk_id = chunk_by_handle.get((note["parent_note_id"], support["evidence_id"]))
                self.assertIsNotNone(chunk_id, note["note_id"])
                haystack = E.notes_contract.normalise_for_span_match(universe().text(chunk_id))
                probe = E.notes_contract.normalise_for_span_match(support["support_text"])
                self.assertIn(probe, haystack,
                              f"{note['note_id']}: span not found in {chunk_id}")

    def test_every_cross_lingual_source_span_occurs_in_its_chunk(self):
        for row in XL_MAPS:
            chunk_id = row["source_evidence_ref"]["chunk_id"]
            haystack = E.notes_contract.normalise_for_span_match(universe().text(chunk_id))
            probe = E.notes_contract.normalise_for_span_match(row["source_span"])
            self.assertIn(probe, haystack, f"{row['mapping_id']}: span not found in {chunk_id}")

    def test_no_evidence_ref_was_invented(self):
        """Every ref must be one the parent note already carried, resolving under its own packet."""
        packet_map = universe().packet_map
        for note in NOTES:
            original = {r["evidence_id"] for r in ORIGINALS[note["parent_note_id"]]["evidence_refs"]}
            for ref in note["evidence_refs"]:
                self.assertIn(ref["evidence_id"], original, note["note_id"])
                key = f"{ref['context_packet_sha']}::{ref['evidence_id']}"
                self.assertIn(key, packet_map, note["note_id"])
                self.assertEqual(packet_map[key]["chunk_id"], ref["chunk_id"], note["note_id"])

    def test_source_identities_resolve_for_every_supported_note(self):
        for note in NOTES:
            if note["support_status"] != "SUPPORTED":
                continue
            self.assertTrue(note["provenance"]["context_packet_sha"], note["note_id"])
            self.assertTrue(note["source_keys"], note["note_id"])
            for ref in note["evidence_refs"]:
                for field in ("evidence_id", "chunk_id", "document_id", "context_packet_sha",
                              "source_key"):
                    self.assertTrue(ref.get(field), f"{note['note_id']}.{field}")

    def test_no_note_is_missing_provenance_or_an_audit_trace(self):
        for note in NOTES:
            self.assertTrue(note["provenance"].get("context_packet_sha"), note["note_id"])
            self.assertTrue(note["manual_audit_refs"], note["note_id"])
            self.assertEqual(note["revision"], 2, note["note_id"])
            self.assertTrue(note["parent_note_sha"], note["note_id"])


class TestCompoundClaims(unittest.TestCase):
    def test_q_02_1_06_n06_is_split_and_never_fully_supported(self):
        children = [n for n in NOTES if n["parent_note_id"] == "Q-02-1-06-N06"]
        self.assertEqual(len(children), 3)
        statuses = sorted(n["support_status"] for n in children)
        self.assertEqual(statuses, ["INSUFFICIENT_EVIDENCE", "INSUFFICIENT_EVIDENCE", "SUPPORTED"])
        supported = [n for n in children if n["support_status"] == "SUPPORTED"][0]
        self.assertIn("işletme ekonomisi", supported["claim"])
        for child in children:
            self.assertEqual(child["parent_note_id"], "Q-02-1-06-N06")
            self.assertTrue(child["split_clause_id"])
            self.assertTrue(child["split_reason"])
            self.assertTrue(child["parent_note_sha"])

    def test_no_note_is_supported_while_a_material_clause_is_not(self):
        for note in NOTES:
            if note["support_status"] != "SUPPORTED":
                continue
            for clause in note["clauses"]:
                if clause["material"]:
                    self.assertEqual(clause["status"], "SUPPORTED", note["note_id"])

    def test_split_children_carry_independent_support(self):
        for row in SPLITS:
            if row["decision"] != "split":
                continue
            self.assertGreaterEqual(row["child_count"], 2)
            for child in row["children"]:
                self.assertIn(child["support_status"], E.NOTE_STATUSES)


class TestNonPropositions(unittest.TestCase):
    def test_no_bare_label_became_a_note(self):
        dropped = {r["original_note_id"] for r in NON_PROP}
        for label_note in ("Q-02-1-01-N03", "Q-02-1-01-N06", "Q-02-1-01-N14",
                           "Q-02-1-01-N04", "Q-02-1-02-N02"):
            self.assertIn(label_note, dropped, label_note)

    def test_historically_false_supported_fragment_is_not_supported(self):
        """Q-02-1-01-N04 carried SUPPORTED in v1 and survived the audit as retain_supported."""
        self.assertEqual(AUDIT["Q-02-1-01-N04"]["recommended_support_status"], "SUPPORTED")
        self.assertEqual([n for n in NOTES if n["parent_note_id"] == "Q-02-1-01-N04"], [])

    def test_dropped_fragments_are_recorded_not_silently_deleted(self):
        for row in NON_PROP:
            self.assertTrue(row["original_fragment"])
            self.assertTrue(row["extraction_reason"])
            self.assertEqual(row["extraction_result"], "NON_PROPOSITION")

    def test_reconstruction_is_never_published_as_supported_without_validation(self):
        for row in NON_PROP:
            if row["decision"] != "RECONSTRUCT_FROM_PARENT_CONTEXT":
                continue
            self.assertTrue(row["requires_support_validation"])
            if row["note_created"]:
                created = [n for n in NOTES if n["note_id"] == row["remediated_note_id"]]
                self.assertTrue(created)
                self.assertEqual(created[0]["proposition_origin"], "parent_child_reconstruction")


class TestNumeric(unittest.TestCase):
    def test_every_value_in_a_supported_note_is_source_stated(self):
        for note in NOTES:
            if note["support_status"] != "SUPPORTED":
                continue
            for fact in note["numeric_data"]:
                self.assertTrue(fact["source_stated"], note["note_id"])
                self.assertFalse(fact["derived"], note["note_id"])

    def test_derived_conversions_are_never_citation_ready(self):
        derived_notes = {n["note_id"] for n in NOTES
                         if any(f["derived"] for f in n["numeric_data"])}
        for entry in LEDGERS:
            if set(entry["note_ids"]) & derived_notes:
                self.assertFalse(entry["citation_ready"], entry["claim_id"])

    def test_both_historical_numeric_defects_stay_contained(self):
        for note_id in ("Q-02-2-01-N04", "Q-02-2-04-N06"):
            children = [n for n in NOTES if n["parent_note_id"] == note_id]
            for child in children:
                self.assertNotEqual(child["support_status"], "SUPPORTED", note_id)
            ready = [e for e in LEDGERS
                     if any(n in {c["note_id"] for c in children} for n in e["note_ids"])
                     and e["citation_ready"]]
            self.assertEqual(ready, [], note_id)

    def test_150mm_conversion_is_recorded_as_derived(self):
        rows = [r for r in NUMERIC if r["original_note_id"] == "Q-02-2-04-N06"]
        self.assertTrue(rows)
        derived = [r for r in rows if r["derived"]]
        self.assertTrue(derived, "the 150 mm conversion was not marked derived")
        self.assertEqual(derived[0]["value"], "150")
        self.assertEqual(derived[0]["derived_from_value"], "15")
        self.assertFalse(derived[0]["source_stated"])

    def test_every_numeric_clause_was_audited(self):
        for row in NUMERIC:
            self.assertIn("numeric_ok", row)
            self.assertIn(row["clause_status"], E.CLAUSE_STATUSES)


class TestCrossLingual(unittest.TestCase):
    def test_no_cross_lingual_clause_is_supported_without_an_explicit_mapping(self):
        mapped = {row["mapping_id"] for row in XL_MAPS}
        for note in NOTES:
            for clause in note["clauses"]:
                if clause["status_source"] != "cross_lingual_manual_mapping":
                    continue
                self.assertTrue(note["cross_lingual_mapping_ids"], note["note_id"])
                for mapping_id in note["cross_lingual_mapping_ids"]:
                    self.assertIn(mapping_id, mapped, note["note_id"])

    def test_mapping_rows_are_complete(self):
        for row in XL_MAPS:
            for field in ("mapping_id", "claim_language", "source_language", "claim_clause",
                          "source_span", "source_evidence_ref", "mapping_status", "mapping_method",
                          "translator_note", "review_status"):
                self.assertTrue(row.get(field), f"{row.get('mapping_id')}.{field}")
            self.assertIn(row["mapping_status"], E.CROSS_LINGUAL_STATUSES)
            self.assertNotEqual(row["claim_language"], row["source_language"],
                                row["mapping_id"])

    def test_non_faithful_mappings_do_not_confer_support(self):
        for row in XL_MAPS:
            if row["mapping_status"] == "FAITHFUL":
                self.assertEqual(row["clause_support_status"], "SUPPORTED", row["mapping_id"])
            else:
                self.assertNotEqual(row["clause_support_status"], "SUPPORTED", row["mapping_id"])


class TestLedgerAndReadiness(unittest.TestCase):
    def test_citation_ready_requires_full_support(self):
        for entry in LEDGERS:
            if entry["citation_ready"]:
                self.assertEqual(entry["support_status"], "SUPPORTED", entry["claim_id"])
                self.assertEqual(entry["citation_block_reasons"], [], entry["claim_id"])

    def test_partially_supported_claims_are_never_citation_ready(self):
        for entry in LEDGERS:
            if entry["support_status"] == "PARTIALLY_SUPPORTED":
                self.assertFalse(entry["citation_ready"], entry["claim_id"])

    def test_p0_gaps_stay_visible(self):
        """A section may not look better because failing notes were dropped."""
        for section, bundle in BUNDLES.items():
            self.assertIn("p0_gap_classification", bundle)
            self.assertIn("notes_dropped_as_non_proposition", bundle)
            for classes in bundle["p0_gap_classification"].values():
                self.assertTrue(classes)
                for gap in classes:
                    self.assertIn(gap, E.P0_GAP_CLASSES)

    def test_dropped_notes_are_still_counted_in_the_bundle(self):
        for section, bundle in BUNDLES.items():
            dropped = bundle["coverage_summary"]["dropped_non_propositions"]
            self.assertEqual(dropped, len(bundle["dropped_non_propositions"]))

    def test_no_section_is_ready_while_a_p0_objective_has_unsupported_clauses(self):
        for section, bundle in BUNDLES.items():
            if bundle["readiness"] == "READY_FOR_DRAFT":
                self.assertEqual(bundle["critical_unsupported_clauses"], [], section)
                self.assertEqual(bundle["critical_numeric_clauses"], [], section)
                self.assertEqual(bundle["critical_cross_lingual_clauses"], [], section)

    def test_readiness_was_recomputed_not_inherited(self):
        audited = {"SEC-02-1": "NOT_READY", "SEC-02-2": "NOT_READY", "SEC-02-3": "NOT_READY"}
        for section, bundle in BUNDLES.items():
            self.assertIn(bundle["readiness"], E.READINESS if hasattr(E, "READINESS")
                          else ("READY_FOR_DRAFT", "READY_WITH_LIMITATIONS", "NOT_READY"))
            if bundle["readiness"] != audited[section]:
                self.assertTrue(bundle["readiness_reasons"], section)

    def test_not_ready_sections_say_why(self):
        for section, bundle in BUNDLES.items():
            if bundle["readiness"] == "NOT_READY":
                self.assertTrue(bundle["readiness_reasons"], section)


class TestFrozenIntegrity(unittest.TestCase):
    def test_all_frozen_inputs_unchanged(self):
        integrity = MANIFEST_DATA["frozen_integrity"]
        self.assertEqual(integrity["changed"], [])
        self.assertTrue(integrity["all_unchanged"])

    def test_originals_and_audited_artifacts_were_not_overwritten(self):
        audit_manifest = json.loads(
            (BOOK / "manifests/pilot_manual_evidence_audit_v1.json").read_text(encoding="utf-8"))
        for section in SECTIONS:
            for kind, folder in (("audited_notes", "evidence_notes_audited"),
                                 ("audited_ledgers", "claim_ledgers_audited")):
                path = BOOK / folder / f"{section}.jsonl"
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(actual, audit_manifest["artifact_shas"][kind][section],
                                 f"{folder}/{section}")

    def test_no_generation_or_retrieval_and_no_qdrant_writes(self):
        self.assertEqual(MANIFEST_DATA["generation_calls"], 0)
        self.assertEqual(MANIFEST_DATA["retrieval_calls"], 0)
        self.assertEqual(MANIFEST_DATA["qdrant_writes"], 0)
        self.assertEqual(MANIFEST_DATA["qdrant_points_before"], 5992)
        self.assertEqual(MANIFEST_DATA["qdrant_points_after"], 5992)

    def test_drafting_stays_disabled(self):
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        self.assertFalse(descriptor["drafting_enabled"])
        self.assertFalse(MANIFEST_DATA["drafting_enabled"])
        self.assertFalse(E.DRAFTING_ENABLED)

    def test_descriptor_names_its_parent_and_scope(self):
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        self.assertEqual(descriptor["version"], "tunnelbook-book-pipeline-extractor-v1.1")
        self.assertEqual(descriptor["parent_version"], "tunnelbook-book-writing-pipeline-v1")
        self.assertTrue(descriptor["known_fixed_defects"])
        self.assertTrue(descriptor["known_remaining_defects"])


class TestRegressionArtifact(unittest.TestCase):
    def test_regression_file_has_at_least_50_cases_and_passes(self):
        cases = load(REGRESSION)
        self.assertGreaterEqual(len(cases), 50)
        self.assertEqual(MANIFEST_DATA["regression"]["failed"], 0)
        self.assertEqual(MANIFEST_DATA["regression"]["passed"], len(cases))

    def test_regression_includes_the_historical_defects(self):
        categories = {c["category"] for c in load(REGRESSION)}
        for required in ("citation_handle_digits", "bare_label", "heading", "compound_claim",
                         "derived_conversion", "cross_lingual", "requirement",
                         "numeric_proposition", "table_fragment", "short_proposition",
                         "condition_preservation"):
            self.assertIn(required, categories, required)


class TestManifest(unittest.TestCase):
    def test_manifest_reports_every_queue(self):
        queues = MANIFEST_DATA["queues"]
        self.assertEqual(queues["literal_span"], {"queued": 81, "processed": 81})
        self.assertEqual(queues["cross_lingual"]["processed"], 11)
        self.assertEqual(queues["non_proposition"]["processed"], 28)
        self.assertEqual(queues["split_note"], {"queued": 14, "processed": 14})
        self.assertEqual(queues["numeric_defects"], {"queued": 2, "contained": 2})

    def test_manifest_counts_match_the_artifacts(self):
        self.assertEqual(MANIFEST_DATA["remediated_note_count"], len(NOTES))
        self.assertEqual(MANIFEST_DATA["dropped_non_propositions"], len(NON_PROP))
        self.assertEqual(MANIFEST_DATA["cross_lingual_mappings"], len(XL_MAPS))
        self.assertEqual(
            MANIFEST_DATA["remediated_SUPPORTED"],
            sum(1 for n in NOTES if n["support_status"] == "SUPPORTED"))

    def test_manifest_status_is_a_gate_not_a_label(self):
        self.assertIn(MANIFEST_DATA["status"], ("closed", "no_go"))
        if MANIFEST_DATA["status"] == "closed":
            self.assertEqual(MANIFEST_DATA["regression"]["failed"], 0)
            self.assertEqual(MANIFEST_DATA["frozen_integrity"]["changed"], [])


if __name__ == "__main__":
    unittest.main()
