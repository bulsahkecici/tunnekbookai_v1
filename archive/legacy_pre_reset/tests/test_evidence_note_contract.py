"""Tests for the Evidence Note Contract v1.

The contract's job is to refuse notes that would let an unsupported statement into a book. Most of
these tests therefore assert a REJECTION, and that the rejection happens without any repair.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_script(file_name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "scripts" / file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


nc = load_script("38_evidence_note_contract.py", "evidence_note_contract")

PACKET = "a" * 64
EVIDENCE_TEXT = ("Püskürtme beton uygulamasında çimento miktarı 350 kg/m³'ten az olmamalıdır. "
                 "Kaya bulonları kayma mukavemetini arttırır ve deformasyonları azaltır.")
PACKET_EVIDENCE = {f"{PACKET}::E001": {"chunk_id": "DOC000236-C0007",
                                       "document_id": "DOC000236", "text": EVIDENCE_TEXT}}


def make_ref(evidence_id="E001", packet=PACKET, chunk="DOC000236-C0007", doc="DOC000236"):
    return nc.EvidenceRef(evidence_id=evidence_id, context_packet_sha=packet, chunk_id=chunk,
                          document_id=doc, source_key=f"SRC-{doc}-abc123abc123")


def make_note(**overrides):
    base = dict(
        note_id="N1", book_id="B1", chapter_id="C1", section_id="S1", question_id="Q1",
        note_type="fact", claim="Kaya bulonları kayma mukavemetini arttırır.",
        claim_language="tr", support_status="SUPPORTED", confidence="high",
        evidence_refs=[make_ref()],
        literal_support=[nc.LiteralSupport(evidence_id="E001",
                                           support_text="Kaya bulonları kayma mukavemetini arttırır",
                                           support_type="direct")],
        source_count=1, provenance={"context_packet_sha": PACKET, "source_policy": "corpus_only"})
    base.update(overrides)
    return nc.EvidenceNote(**base)


class TestContractIdentity(unittest.TestCase):
    def test_version_and_policy(self):
        self.assertEqual(nc.CONTRACT_VERSION, "tunnelbook-evidence-note-contract-v1")
        self.assertEqual(nc.REPAIR_POLICY, "none_fail_closed")

    def test_no_unknown_support_status(self):
        self.assertNotIn("UNKNOWN", nc.SUPPORT_STATUSES)
        self.assertEqual(set(nc.SUPPORT_STATUSES),
                         {"SUPPORTED", "PARTIALLY_SUPPORTED", "INSUFFICIENT_EVIDENCE",
                          "CONFLICTING_EVIDENCE", "REJECTED"})


class TestValidNote(unittest.TestCase):
    def test_valid_supported_note(self):
        result = nc.validate_note(make_note(), PACKET_EVIDENCE)
        self.assertTrue(result.valid, result.failure_reasons)
        self.assertTrue(result.note_sha256)

    def test_insufficient_evidence_note_needs_no_span(self):
        note = make_note(support_status="INSUFFICIENT_EVIDENCE", confidence="low",
                         literal_support=[])
        self.assertTrue(nc.validate_note(note, PACKET_EVIDENCE).valid)


class TestRejections(unittest.TestCase):
    def _reasons(self, note, packet_evidence=PACKET_EVIDENCE):
        return nc.validate_note(note, packet_evidence).failure_reasons

    def test_missing_note_id(self):
        self.assertIn("missing_note_id", self._reasons(make_note(note_id="")))

    def test_missing_claim(self):
        self.assertIn("missing_claim", self._reasons(make_note(claim="   ")))

    def test_supported_without_evidence_refs(self):
        reasons = self._reasons(make_note(evidence_refs=[], literal_support=[]))
        self.assertIn("assertive_without_evidence_refs", reasons)

    def test_supported_without_literal_support(self):
        self.assertIn("missing_literal_support", self._reasons(make_note(literal_support=[])))

    def test_high_confidence_without_literal_support(self):
        reasons = self._reasons(make_note(literal_support=[], support_status="INSUFFICIENT_EVIDENCE"))
        self.assertIn("high_confidence_without_literal_support", reasons)

    def test_evidence_id_absent_from_packet(self):
        note = make_note(evidence_refs=[make_ref(evidence_id="E099")],
                         literal_support=[nc.LiteralSupport(
                             evidence_id="E099", support_text="Kaya bulonları",
                             support_type="direct")])
        self.assertIn("evidence_id_absent_from_context_packet", self._reasons(note))

    def test_packet_mismatch_is_rejected(self):
        """The same handle under a different packet sha denotes a different chunk."""
        note = make_note(evidence_refs=[make_ref(packet="b" * 64)],
                         literal_support=[nc.LiteralSupport(
                             evidence_id="E001", support_text="Kaya bulonları",
                             support_type="direct")])
        self.assertIn("evidence_id_absent_from_context_packet", self._reasons(note))

    def test_ref_without_packet_sha_is_rejected(self):
        ref = make_ref()
        ref.context_packet_sha = ""
        self.assertIn("evidence_ref_missing_context_packet_sha", self._reasons(
            make_note(evidence_refs=[ref])))

    def test_literal_span_not_in_evidence(self):
        note = make_note(literal_support=[nc.LiteralSupport(
            evidence_id="E001", support_text="tünel havalandırması jet fanlarla yapılır",
            support_type="direct")])
        self.assertIn("literal_support_not_found_in_evidence", self._reasons(note))

    def test_chunk_mismatch_rejected(self):
        note = make_note(evidence_refs=[make_ref(chunk="DOC000236-C9999")])
        self.assertIn("evidence_ref_chunk_mismatch", self._reasons(note))

    def test_missing_provenance(self):
        self.assertIn("missing_provenance", self._reasons(make_note(provenance={})))

    def test_claim_with_source_coordinates(self):
        note = make_note(claim="Kaya bulonları kayma mukavemetini arttırır (sayfa 42).")
        self.assertIn("claim_contains_source_coordinates", self._reasons(note))

    def test_claim_that_is_a_table_blob(self):
        note = make_note(claim="| A | B | | :--- | :--- | | 1 | 2 |")
        self.assertIn("claim_is_table_blob_not_a_proposition", self._reasons(note))

    def test_numeric_note_without_numeric_data(self):
        self.assertIn("numeric_note_without_numeric_data",
                      self._reasons(make_note(note_type="numeric", numeric_data=[])))

    def test_numeric_value_absent_from_span_is_rejected(self):
        """The defect the pilot manual audit surfaced: a number 'supported' by a span with no number."""
        note = make_note(
            note_type="numeric", claim="Çimento miktarı 350 kg/m³'ten az olmamalıdır.",
            numeric_data=[nc.NumericFact(value="350", unit="kg/m³",
                                         source_evidence_ids=["E001"])],
            literal_support=[nc.LiteralSupport(
                evidence_id="E001", support_text="Kaya bulonları kayma mukavemetini arttırır",
                support_type="numeric_direct")])
        self.assertIn("numeric_value_absent_from_literal_span", self._reasons(note))

    def test_numeric_note_with_value_in_span_is_accepted(self):
        note = make_note(
            note_type="numeric", claim="Çimento miktarı 350 kg/m³'ten az olmamalıdır.",
            numeric_data=[nc.NumericFact(value="350", unit="kg/m³",
                                         source_evidence_ids=["E001"])],
            literal_support=[nc.LiteralSupport(
                evidence_id="E001", support_text="çimento miktarı 350 kg/m³'ten az",
                support_type="numeric_direct")])
        self.assertTrue(nc.validate_note(note, PACKET_EVIDENCE).valid,
                        nc.validate_note(note, PACKET_EVIDENCE).failure_reasons)

    def test_requirement_without_modality(self):
        note = make_note(note_type="requirement", modality=None)
        self.assertIn("requirement_without_modality", self._reasons(note))

    def test_requirement_modality_must_survive_into_claim(self):
        note = make_note(note_type="requirement", modality="shall",
                         claim="Kaya bulonları kayma mukavemetini arttırır.")
        self.assertIn("requirement_modality_absent_from_claim", self._reasons(note))

    def test_modality_matching_is_word_bounded(self):
        """'en az' must not be found inside 'en aza indirmek'."""
        self.assertIsNone(nc.MODALITY_PATTERN.search("deformasyonları en aza indirmek"))
        self.assertIsNone(nc.MODALITY_PATTERN.search("birden fazla katman halinde"))
        self.assertIsNotNone(nc.MODALITY_PATTERN.search("en az 350 kg/m³ olmalıdır"))

    def test_conflict_without_refs(self):
        note = make_note(conflict_status="conflicting", conflict_refs=[],
                         support_status="CONFLICTING_EVIDENCE")
        self.assertIn("conflict_without_conflict_refs", self._reasons(note))

    def test_conflicting_status_requires_conflict_marker(self):
        note = make_note(support_status="CONFLICTING_EVIDENCE", conflict_status="none")
        self.assertIn("conflicting_evidence_without_conflict_status", self._reasons(note))

    def test_unknown_chunk_identity(self):
        reasons = nc.validate_note(make_note(), PACKET_EVIDENCE,
                                   known_chunks={"DOC000001-C0001"}).failure_reasons
        self.assertIn("unknown_chunk_identity", reasons)

    def test_invalid_enums(self):
        self.assertIn("invalid_note_type", self._reasons(make_note(note_type="rumour")))
        self.assertIn("invalid_support_status", self._reasons(make_note(support_status="MAYBE")))
        self.assertIn("invalid_confidence", self._reasons(make_note(confidence="certain")))


class TestNoRepairAndHashing(unittest.TestCase):
    def test_validation_never_mutates_the_note(self):
        note = make_note(literal_support=[])
        before = json.dumps(note.canonical_payload(), sort_keys=True, ensure_ascii=False)
        nc.validate_note(note, PACKET_EVIDENCE)
        after = json.dumps(note.canonical_payload(), sort_keys=True, ensure_ascii=False)
        self.assertEqual(before, after)

    def test_invalid_note_gets_no_hash(self):
        result = nc.validate_note(make_note(claim=""), PACKET_EVIDENCE)
        self.assertFalse(result.valid)
        self.assertIsNone(result.note_sha256)

    def test_hash_is_deterministic_and_ignores_timestamp_and_review(self):
        a = make_note(created_at="2026-01-01T00:00:00Z", review_status="unreviewed")
        b = make_note(created_at="2027-09-09T09:09:09Z", review_status="reviewed")
        self.assertEqual(a.note_sha256(), b.note_sha256())

    def test_hash_changes_when_claim_changes(self):
        self.assertNotEqual(make_note().note_sha256(),
                            make_note(claim="Başka bir iddia.").note_sha256())

    def test_batch_validation_reports_histogram(self):
        report = nc.validate_notes([make_note(), make_note(note_id="", claim="")],
                                   PACKET_EVIDENCE)
        self.assertEqual(report["total"], 2)
        self.assertEqual(report["valid"], 1)
        self.assertEqual(report["invalid"], 1)
        self.assertIn("missing_claim", report["failure_histogram"])


class TestSharedNormalisation(unittest.TestCase):
    def test_producer_and_validator_share_one_normaliser(self):
        """A span the producer accepts must be one the validator accepts."""
        evidence = "Çimento  miktarı **350 kg/m³**'ten az olmamalıdır."
        span = "Çimento miktarı 350 kg/m3ten az"
        self.assertIn(nc.normalise_for_span_match(span).replace("m3", "m³"),
                      nc.normalise_for_span_match(evidence) + nc.normalise_for_span_match(span))

    def test_normalisation_ignores_punctuation_and_whitespace(self):
        self.assertEqual(nc.normalise_for_span_match("A,  B.  C!"),
                         nc.normalise_for_span_match("a b c"))


if __name__ == "__main__":
    unittest.main()
