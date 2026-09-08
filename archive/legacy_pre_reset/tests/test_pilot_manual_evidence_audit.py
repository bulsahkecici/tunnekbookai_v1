"""Tests for the pilot manual evidence audit v1 (clause-level support audit)."""
from __future__ import annotations

import hashlib, importlib.util, json, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "data/book"; AUD = BOOK / "audits"
NOTE_AUDIT = AUD / "pilot_evidence_note_manual_audit_v1.jsonl"
CLAUSE_AUDIT = AUD / "pilot_clause_support_audit_v1.jsonl"
CONFLICTS = AUD / "pilot_conflict_candidates_v1.jsonl"
DUPLICATES = AUD / "pilot_duplicate_claim_audit_v1.jsonl"
MANIFEST = BOOK / "manifests/pilot_manual_evidence_audit_v1.json"


def load(p): return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


spec = importlib.util.spec_from_file_location("aud", ROOT / "scripts/41_pilot_manual_evidence_audit_v1.py")
A = importlib.util.module_from_spec(spec); sys.modules["aud"] = A; spec.loader.exec_module(A)

ROWS = load(NOTE_AUDIT); CLAUSES = load(CLAUSE_AUDIT)
ORIGINAL = []
for f in sorted((BOOK / "evidence_notes").glob("*.jsonl")): ORIGINAL += load(f)
AUDITED = []
for f in sorted((BOOK / "evidence_notes_audited").glob("*.jsonl")): AUDITED += load(f)


class TestAuditPopulation(unittest.TestCase):
    def test_159_original_notes_and_159_audit_rows(self):
        self.assertEqual(len(ORIGINAL), 159)
        self.assertEqual(len(ROWS), 159)
        self.assertEqual({r["original_note_id"] for r in ROWS}, {n["note_id"] for n in ORIGINAL})

    def test_all_manually_audited(self):
        self.assertTrue(all(r["manual_audit_completed"] for r in ROWS))
        self.assertTrue(all(r["audit_method"] == "manual_evidence_read" for r in ROWS))

    def test_no_deterministic_only_method(self):
        for r in ROWS:
            self.assertNotEqual(r["audit_method"], "deterministic_verified")


class TestClauseCoverage(unittest.TestCase):
    def test_every_clause_resolved(self):
        self.assertTrue(CLAUSES)
        for c in CLAUSES:
            self.assertIn(c["status"], ("SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED"))
            for forbidden in ("UNKNOWN", "UNVERIFIED", "UNREVIEWED"):
                self.assertNotEqual(c["status"], forbidden)

    def test_clause_counts_match_note_rows(self):
        per_note = {}
        for c in CLAUSES:
            per_note[c["original_note_id"]] = per_note.get(c["original_note_id"], 0) + 1
        for r in ROWS:
            self.assertEqual(r["clause_count"], per_note.get(r["original_note_id"], 0),
                             r["original_note_id"])


class TestStatusConsistency(unittest.TestCase):
    def test_supported_requires_all_clauses_supported(self):
        by_note = {}
        for c in CLAUSES:
            by_note.setdefault(c["original_note_id"], []).append(c["status"])
        for r in ROWS:
            if r["recommended_support_status"] == "SUPPORTED":
                self.assertTrue(r["full_claim_supported"], r["original_note_id"])
                self.assertEqual(set(by_note.get(r["original_note_id"], ["SUPPORTED"])),
                                 {"SUPPORTED"}, r["original_note_id"])

    def test_no_compound_partial_marked_fully_supported(self):
        for r in ROWS:
            if r["unsupported_clauses"] or r["partially_supported_clauses"]:
                self.assertNotEqual(r["recommended_support_status"], "SUPPORTED",
                                    r["original_note_id"])

    def test_partially_supported_has_support_and_a_gap(self):
        for r in ROWS:
            if r["recommended_support_status"] == "PARTIALLY_SUPPORTED":
                self.assertGreater(r["supported_clause_count"], 0, r["original_note_id"])
                self.assertTrue(r["unsupported_clauses"] or r["partially_supported_clauses"])

    def test_known_compound_defect_downgraded(self):
        row = next(r for r in ROWS if r["original_note_id"] == "Q-02-1-06-N06")
        self.assertEqual(row["original_support_status"], "SUPPORTED")
        self.assertEqual(row["recommended_support_status"], "PARTIALLY_SUPPORTED")
        self.assertEqual(row["recommended_action"], "split_note")


class TestNumericAndModality(unittest.TestCase):
    def test_numeric_defects_identified(self):
        defects = {r["original_note_id"] for r in ROWS if not r["numeric_values_verified"]}
        self.assertIn("Q-02-2-01-N04", defects)
        self.assertIn("Q-02-2-04-N06", defects)
        for nid in defects:
            row = next(r for r in ROWS if r["original_note_id"] == nid)
            self.assertNotEqual(row["recommended_support_status"], "SUPPORTED")

    def test_no_supported_note_carries_a_numeric_defect(self):
        for r in ROWS:
            if r["recommended_support_status"] == "SUPPORTED":
                self.assertTrue(r["numeric_values_verified"], r["original_note_id"])

    def test_modality_preserved(self):
        self.assertTrue(all(r["modality_verified"] for r in ROWS))


class TestProvenanceAndIdentity(unittest.TestCase):
    def test_packet_local_identity_resolves(self):
        self.assertTrue(all(r["evidence_refs_verified"] for r in ROWS))

    def test_provenance_complete(self):
        self.assertTrue(all(r["provenance_verified"] for r in ROWS))

    def test_existing_spans_occur_in_evidence(self):
        self.assertTrue(all(r["literal_span_verified"] for r in ROWS))

    def test_audited_notes_carry_source_keys(self):
        for n in AUDITED:
            self.assertTrue(n["source_keys"], n["audited_note_id"])
            for ref in n["evidence_refs"]:
                self.assertTrue(ref["context_packet_sha"])

    def test_audited_note_hash_deterministic(self):
        for n in AUDITED:
            payload = {k: v for k, v in n.items()
                       if k not in ("audited_note_id", "created_at", "audited_note_sha")}
            self.assertEqual(n["audited_note_sha"], A.sha_json(payload), n["audited_note_id"])


class TestConflictAndDuplicates(unittest.TestCase):
    def test_conflict_search_was_performed(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertTrue(manifest["conflict_search_performed"])
        self.assertGreater(manifest["conflict_evidence_universe_items"], 300)

    def test_every_conflict_candidate_manually_classified(self):
        candidates = load(CONFLICTS)
        self.assertTrue(candidates)
        for c in candidates:
            self.assertTrue(c["reviewed"])
            self.assertIn(c["manual_classification"], A.CONFLICT_CLASSES)
            self.assertTrue(c["manual_reason"])

    def test_all_duplicate_candidates_reviewed(self):
        dups = load(DUPLICATES)
        self.assertTrue(dups)
        for d in dups:
            self.assertTrue(d["reviewed"])
            self.assertIn(d["manual_decision"], A.DUPLICATE_DECISIONS)


class TestOriginalImmutability(unittest.TestCase):
    def test_frozen_stack_unchanged(self):
        expected = {
            "data/metadata/generation_system_prompt_v5.txt":
                "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085",
            "scripts/31_generation_output_contract_v1_1.py":
                "5ebf8fe90e3e5491ce07a9143f8fd377841defa2e0e7a09188f3a835b07bdef5"}
        for path, digest in expected.items():
            self.assertEqual(sha(ROOT / path), digest, path)

    def test_original_pilot_artifacts_unchanged(self):
        manifest = json.loads((BOOK / "manifests/book_pipeline_architecture_v1.json")
                              .read_text(encoding="utf-8"))
        self.assertEqual(manifest["evidence_note_contract_sha"],
                         sha(ROOT / "scripts/38_evidence_note_contract.py"))
        self.assertEqual(manifest["pipeline_implementation_sha"],
                         sha(ROOT / "scripts/39_book_writing_pipeline.py"))

    def test_audited_artifacts_are_separate_files(self):
        for name in ("evidence_notes", "claim_ledgers", "section_bundles"):
            self.assertTrue((BOOK / name).exists())
            self.assertTrue((BOOK / f"{name}_audited").exists())

    def test_no_generation_or_retrieval(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["generation_calls"], 0)
        self.assertEqual(manifest["retrieval_calls"], 0)
        self.assertEqual(manifest["qdrant_writes"], 0)
        source = (ROOT / "scripts/41_pilot_manual_evidence_audit_v1.py").read_text(encoding="utf-8")
        for forbidden in ("urlopen", "requests.", "RetrieverV1(", "gen.complete"):
            self.assertNotIn(forbidden, source)

    def test_drafting_still_disabled(self):
        descriptor = json.loads((ROOT / "data/metadata/book_writing_pipeline_v1.json")
                                .read_text(encoding="utf-8"))
        self.assertFalse(descriptor["drafting_enabled"])


class TestManifest(unittest.TestCase):
    def test_manifest_hashes_match(self):
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(m["artifact_shas"]["note_audit"], sha(NOTE_AUDIT))
        self.assertEqual(m["artifact_shas"]["clause_audit"], sha(CLAUSE_AUDIT))
        self.assertEqual(m["artifact_shas"]["conflict_candidates"], sha(CONFLICTS))
        self.assertEqual(m["artifact_shas"]["duplicate_audit"], sha(DUPLICATES))

    def test_manifest_reports_full_completion(self):
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(m["audit_row_count"], 159)
        self.assertTrue(m["manual_audit_completed_all"])
        self.assertTrue(m["audit_method_all_manual"])
        self.assertEqual(m["false_supported_full_claims_remaining"], 0)


if __name__ == "__main__":
    unittest.main()
