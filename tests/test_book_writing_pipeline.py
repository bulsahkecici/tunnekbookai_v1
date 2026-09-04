"""Tests for the book-writing pipeline v1 (evidence preparation controller).

The load-bearing assertions are about restraint: no prose is produced, gaps stay visible, rejected
generations are preserved as gaps rather than filled, and packet-local evidence ids are never
treated as globally meaningful.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "data/book"
PROSE_CONTROL = BOOK / "contracts/prose_artifact_control_contract_v1.json"
LIVE = os.environ.get("TUNNELBOOK_LIVE_MODEL") == "1"


def load_script(file_name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "scripts" / file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


bp = load_script("39_book_writing_pipeline.py", "book_pipeline")
nc = bp.notes_contract

PACKET = "c" * 64


def make_note(note_id="N1", question_id="Q1", status="SUPPORTED", claim="Bir iddia cümlesidir.",
              doc="DOC000001", chunk="DOC000001-C0001", review="unreviewed"):
    return nc.EvidenceNote(
        note_id=note_id, book_id="B1", chapter_id="C1", section_id="S1", question_id=question_id,
        note_type="fact", claim=claim, claim_language="tr", support_status=status,
        confidence="high" if status == "SUPPORTED" else "low",
        evidence_refs=[nc.EvidenceRef(evidence_id="E001", context_packet_sha=PACKET,
                                      chunk_id=chunk, document_id=doc,
                                      source_key=f"SRC-{doc}-abcdef123456")],
        literal_support=([nc.LiteralSupport(evidence_id="E001", support_text="bir iddia",
                                            support_type="direct")]
                         if status == "SUPPORTED" else []),
        source_count=1, provenance={"context_packet_sha": PACKET}, review_status=review)


def make_question(qid="Q1", priority="P0", section="S1"):
    return bp.ResearchQuestion(question_id=qid, section_id=section, question="Soru?",
                               question_language="tr", question_type="definition",
                               priority=priority, required=True, expected_answer_type="definition")


class TestPipelineIdentity(unittest.TestCase):
    def test_version_and_policy(self):
        self.assertEqual(bp.PIPELINE_VERSION, "tunnelbook-book-writing-pipeline-v1")
        self.assertEqual(bp.SOURCE_POLICY, "corpus_only")
        self.assertFalse(bp.DRAFTING_ENABLED)

    def test_delegates_to_frozen_production_generator(self):
        self.assertEqual(bp.production.VERSION, "tunnelbook-production-grounded-generator-v1")
        self.assertEqual(bp.production.PRODUCTION_POLICY,
                         "accept_if_contract_valid_else_reject")
        source = (ROOT / "scripts/39_book_writing_pipeline.py").read_text(encoding="utf-8")
        for forbidden in ("def assemble_context", "def validate_citations", "def embed_query",
                          "urllib.request.urlopen", "requests.get"):
            self.assertNotIn(forbidden, source)

    def test_source_policy_cannot_be_relaxed(self):
        with self.assertRaises(ValueError):
            bp.BookProject(book_id="B", working_title="T", language="tr", audience="a",
                           technical_level="x", purpose="p", source_policy="web_allowed")


class TestNoProse(unittest.TestCase):
    def test_draft_section_raises(self):
        with self.assertRaises(NotImplementedError):
            bp.draft_section(None, None)
        with self.assertRaises(bp.DraftingDisabled):
            bp.draft_section(None, None)

    def test_no_prose_artifacts_were_produced(self):
        """OC-01: allow only the exact accepted, validated and labelled Pilot #2 draft."""
        control = json.loads(PROSE_CONTROL.read_text(encoding="utf-8"))
        self.assertEqual(control["decision_id"], "OC-01")
        self.assertEqual(control["status"], "CLOSED")

        authorised = {entry["path"]: entry for entry in control["authorised_artifacts"]}
        found_markdown = {
            path.relative_to(ROOT).as_posix(): path for path in BOOK.rglob("*.md")
        }
        self.assertEqual(set(found_markdown), set(authorised),
                         "uncontrolled or missing Markdown prose artifact")

        for relative, path in found_markdown.items():
            attestation = authorised[relative]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                             attestation["sha256"])
            manifest = json.loads((ROOT / attestation["manifest_path"]).read_text(
                encoding="utf-8"))
            citation_render = manifest["post_render"]["citation_render"]
            self.assertEqual(citation_render["path"], relative)
            self.assertEqual(citation_render["sha256"], attestation["sha256"])
            self.assertEqual(citation_render["label"], attestation["required_label"])
            self.assertEqual(manifest["post_render"]["draft_status"],
                             attestation["required_label"])
            self.assertEqual(manifest["gate"]["verdict"],
                             attestation["required_gate_verdict"])
            self.assertEqual(manifest["post_render"]["validator"]["status"],
                             attestation["required_validator_status"])
            self.assertEqual(attestation["release_status"], "NOT_RELEASED")

        for extension in control["prohibited_extensions"]:
            self.assertEqual(list(BOOK.rglob(f"*{extension}")), [],
                             f"unexpected prose artifact {extension}")

    def test_section_plan_holds_no_narrative(self):
        plans = list((BOOK / "section_plans").glob("*.json"))
        if not plans:
            self.skipTest("pilot not run")
        for path in plans:
            plan = json.loads(path.read_text(encoding="utf-8"))
            self.assertNotIn("draft", plan)
            self.assertNotIn("prose", plan)
            self.assertLess(len(plan["objective"]), 400)


class TestSchemas(unittest.TestCase):
    def test_question_validation(self):
        with self.assertRaises(ValueError):
            bp.ResearchQuestion(question_id="Q", section_id="S", question="q",
                                question_language="de", question_type="definition",
                                priority="P0", required=True, expected_answer_type="x")
        with self.assertRaises(ValueError):
            bp.ResearchQuestion(question_id="Q", section_id="S", question="q",
                                question_language="tr", question_type="not_a_type",
                                priority="P0", required=True, expected_answer_type="x")
        with self.assertRaises(ValueError):
            bp.ResearchQuestion(question_id="Q", section_id="S", question="q",
                                question_language="tr", question_type="definition",
                                priority="P9", required=True, expected_answer_type="x")

    def test_bundle_hash_is_deterministic_and_ignores_timestamp(self):
        def build():
            return bp.SectionEvidenceBundle(
                section_id="S1", book_id="B1", chapter_id="C1", research_questions=[],
                research_results=[], evidence_notes=[], claim_ledger=[], unanswered_questions=[],
                rejected_questions=[], conflicts=[], numeric_facts=[], requirements=[],
                source_summary={}, coverage_summary={}, readiness="NOT_READY",
                readiness_reasons=[]).finalise()
        first, second = build(), build()
        self.assertEqual(first.bundle_sha, second.bundle_sha)
        self.assertTrue(first.bundle_sha)

    def test_bundle_hash_changes_with_content(self):
        base = bp.SectionEvidenceBundle(
            section_id="S1", book_id="B1", chapter_id="C1", research_questions=[],
            research_results=[], evidence_notes=[], claim_ledger=[], unanswered_questions=[],
            rejected_questions=[], conflicts=[], numeric_facts=[], requirements=[],
            source_summary={}, coverage_summary={}, readiness="NOT_READY",
            readiness_reasons=[]).finalise()
        changed = bp.SectionEvidenceBundle(
            section_id="S1", book_id="B1", chapter_id="C1", research_questions=[],
            research_results=[], evidence_notes=[{"note_id": "N1"}], claim_ledger=[],
            unanswered_questions=[], rejected_questions=[], conflicts=[], numeric_facts=[],
            requirements=[], source_summary={}, coverage_summary={}, readiness="NOT_READY",
            readiness_reasons=[]).finalise()
        self.assertNotEqual(base.bundle_sha, changed.bundle_sha)


class TestSourceRegistry(unittest.TestCase):
    def test_source_key_is_stable_and_deterministic(self):
        first = bp.source_key("DOC000123", "DOC000123-C0007")
        self.assertEqual(first, bp.source_key("DOC000123", "DOC000123-C0007"))
        self.assertNotEqual(first, bp.source_key("DOC000123", "DOC000123-C0008"))
        self.assertTrue(first.startswith("SRC-DOC000123-"))

    def test_registry_deduplicates_the_same_chunk(self):
        if not bp.SOURCE_REGISTRY.exists():
            self.skipTest("pilot not run")
        rows = [json.loads(l) for l in bp.SOURCE_REGISTRY.read_text(encoding="utf-8").splitlines()
                if l.strip()]
        keys = [r["source_key"] for r in rows]
        self.assertEqual(len(keys), len(set(keys)), "source registry contains duplicate keys")
        for row in rows:
            self.assertEqual(row["source_key"],
                             bp.source_key(row["document_id"], row["chunk_id"]))

    def test_no_internal_path_in_source_key(self):
        key = bp.source_key("DOC000123", "DOC000123-C0007")
        self.assertNotIn("/", key)
        self.assertNotIn(".pdf", key)


class TestPacketLocalIdentity(unittest.TestCase):
    def test_every_evidence_ref_pairs_handle_with_packet(self):
        files = list((BOOK / "evidence_notes").glob("*.jsonl"))
        if not files:
            self.skipTest("pilot not run")
        for path in files:
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                note = json.loads(line)
                for ref in note["evidence_refs"]:
                    self.assertTrue(ref["context_packet_sha"],
                                    f"{note['note_id']}: handle without packet sha")
                    self.assertTrue(ref["source_key"],
                                    f"{note['note_id']}: no stable book-level source key")

    def test_same_handle_under_different_packets_is_not_conflated(self):
        packet_evidence = {
            f"{'a' * 64}::E001": {"chunk_id": "DOC000001-C0001", "document_id": "DOC000001",
                                  "text": "bir iddia cümlesidir"},
            f"{'b' * 64}::E001": {"chunk_id": "DOC000999-C0009", "document_id": "DOC000999",
                                  "text": "farklı bir metin"}}
        note = make_note()
        note.evidence_refs[0].context_packet_sha = "a" * 64
        self.assertTrue(nc.validate_note(note, packet_evidence).valid)
        note.evidence_refs[0].context_packet_sha = "b" * 64
        result = nc.validate_note(note, packet_evidence)
        self.assertFalse(result.valid)
        self.assertIn("evidence_ref_chunk_mismatch", result.failure_reasons)


class TestClaimLedger(unittest.TestCase):
    def test_duplicate_candidates_detected_lexically(self):
        notes = [make_note("N1", claim="Püskürtme beton erken destek sağlar ve gevşemeyi önler."),
                 make_note("N2", claim="Püskürtme beton erken destek sağlar, gevşemeyi önler.")]
        ledger = bp.build_claim_ledger(notes, "S1")
        self.assertTrue(ledger[0].duplicate_candidates)
        self.assertIn(ledger[1].claim_id, ledger[0].duplicate_candidates)

    def test_distinct_claims_are_not_marked_duplicate(self):
        notes = [make_note("N1", claim="Püskürtme beton erken destek sağlar."),
                 make_note("N2", claim="Kaya bulonları kayma mukavemetini arttırır.")]
        ledger = bp.build_claim_ledger(notes, "S1")
        self.assertEqual(ledger[0].duplicate_candidates, [])

    def test_citation_ready_requires_source_keys(self):
        note = make_note("N1")
        self.assertTrue(bp.build_claim_ledger([note], "S1")[0].citation_ready)
        note.evidence_refs[0].source_key = None
        self.assertFalse(bp.build_claim_ledger([note], "S1")[0].citation_ready)

    def test_no_llm_used_for_merging(self):
        source = (ROOT / "scripts/39_book_writing_pipeline.py").read_text(encoding="utf-8")
        ledger_section = source.split("def build_claim_ledger")[1].split("def ")[0]
        self.assertNotIn("complete(", ledger_section)
        self.assertNotIn("generate", ledger_section)


class TestReadiness(unittest.TestCase):
    def test_p0_without_supported_note_is_not_ready(self):
        questions = [make_question("Q1", "P0")]
        results = [{"question_id": "Q1", "question_status": "answered"}]
        notes = [make_note("N1", question_id="Q1", status="INSUFFICIENT_EVIDENCE")]
        readiness, reasons = bp.assess_readiness(questions, results, notes, [])
        self.assertEqual(readiness, "NOT_READY")
        self.assertTrue(any("without any SUPPORTED" in r for r in reasons))

    def test_p0_generator_rejection_is_not_ready(self):
        questions = [make_question("Q1", "P0")]
        results = [{"question_id": "Q1", "question_status": "generator_rejected"}]
        readiness, reasons = bp.assess_readiness(questions, results, [], [])
        self.assertEqual(readiness, "NOT_READY")

    def test_discarded_invalid_notes_block_readiness(self):
        """A section may not be ready by virtue of its rejected notes having vanished."""
        questions = [make_question("Q1", "P0")]
        results = [{"question_id": "Q1", "question_status": "answered"}]
        notes = [make_note("N1", question_id="Q1")]
        readiness, reasons = bp.assess_readiness(questions, results, notes, [],
                                                 invalid_note_ids=["N2", "N3"])
        self.assertEqual(readiness, "NOT_READY")
        self.assertTrue(any("contract-invalid" in r for r in reasons))

    def test_all_p0_supported_can_advance(self):
        questions = [make_question("Q1", "P0")]
        results = [{"question_id": "Q1", "question_status": "answered"}]
        notes = [make_note("N1", question_id="Q1")]
        readiness, reasons = bp.assess_readiness(questions, results, notes, [])
        self.assertEqual(readiness, "READY_FOR_DRAFT")
        self.assertEqual(reasons, [])

    def test_p1_gap_yields_ready_with_limitations(self):
        questions = [make_question("Q1", "P0"), make_question("Q2", "P1")]
        results = [{"question_id": "Q1", "question_status": "answered"},
                   {"question_id": "Q2", "question_status": "insufficient_evidence"}]
        notes = [make_note("N1", question_id="Q1")]
        readiness, reasons = bp.assess_readiness(questions, results, notes, [])
        self.assertEqual(readiness, "READY_WITH_LIMITATIONS")
        self.assertTrue(reasons)

    def test_readiness_values_are_from_the_fixed_set(self):
        self.assertEqual(set(bp.READINESS),
                         {"READY_FOR_DRAFT", "READY_WITH_LIMITATIONS", "NOT_READY"})


class TestGapsStayVisible(unittest.TestCase):
    def test_rejected_and_abstained_questions_are_recorded(self):
        bundles = list((BOOK / "section_bundles").glob("*.json"))
        if not bundles:
            self.skipTest("pilot not run")
        for path in bundles:
            bundle = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn("rejected_questions", bundle)
            self.assertIn("unanswered_questions", bundle)
            recorded = set(bundle["rejected_questions"]) | set(bundle["unanswered_questions"])
            for result in bundle["research_results"]:
                if result["question_status"] in ("generator_rejected", "request_rejected",
                                                 "insufficient_evidence"):
                    self.assertIn(result["question_id"], recorded)

    def test_rejected_generation_produces_no_notes(self):
        runs = list((BOOK / "research_runs").glob("*.jsonl"))
        if not runs:
            self.skipTest("pilot not run")
        for path in runs:
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                if row["question_status"] in ("generator_rejected", "request_rejected"):
                    self.assertIsNone(row.get("accepted_answer"))
                    self.assertEqual(row.get("note_ids", []), [])


class TestPilotArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = BOOK / "manifests/pilot_summary_v1.json"
        cls.summary = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None

    def test_three_sections(self):
        if not self.summary:
            self.skipTest("pilot not run")
        self.assertEqual(len(self.summary["sections"]), 3)

    def test_all_notes_contract_valid(self):
        if not self.summary:
            self.skipTest("pilot not run")
        for section in self.summary["sections"]:
            self.assertEqual(section["invalid_notes"], 0,
                             f"{section['section_id']}: {section['failure_histogram']}")

    def test_no_qdrant_writes(self):
        if not self.summary:
            self.skipTest("pilot not run")
        self.assertEqual(self.summary["qdrant_writes"], 0)
        self.assertEqual(self.summary["qdrant_before"][0], 5992)
        self.assertEqual(self.summary["qdrant_after"][0], 5992)

    def test_drafting_remains_disabled(self):
        if not self.summary:
            self.skipTest("pilot not run")
        self.assertFalse(self.summary["pipeline"]["drafting_enabled"])


class TestFrozenStackUnchanged(unittest.TestCase):
    def test_production_stack_files_unchanged(self):
        expected = {
            "data/metadata/generation_system_prompt_v5.txt":
                "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085",
            "scripts/31_generation_output_contract_v1_1.py":
                "5ebf8fe90e3e5491ce07a9143f8fd377841defa2e0e7a09188f3a835b07bdef5"}
        for path, sha in expected.items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), sha, path)

    def test_no_prompt_v6(self):
        self.assertFalse((ROOT / "data/metadata/generation_system_prompt_v6.txt").exists())


@unittest.skipUnless(LIVE, "live model pilot; set TUNNELBOOK_LIVE_MODEL=1 to run")
class TestLivePilot(unittest.TestCase):
    def test_single_question_end_to_end(self):
        project = bp.BookProject(book_id="B-LIVE", working_title="t", language="tr",
                                 audience="a", technical_level="x", purpose="p")
        chapter = bp.ChapterPlan(chapter_id="CH-L", chapter_number=1, title="t", purpose="p")
        section = bp.SectionPlan(section_id="SEC-L", chapter_id="CH-L", section_number="1.1",
                                 title="t", objective="o")
        question = bp.ResearchQuestion(
            question_id="Q-L-1", section_id="SEC-L",
            question="Tünelde püskürtme betonun işlevi nedir?", question_language="tr",
            question_type="mechanism", priority="P0", required=True,
            expected_answer_type="mechanism")
        research = bp.run_section_research(project, chapter, section, [question])
        self.assertEqual(len(research["results"]), 1)
        self.assertIn(research["results"][0]["question_status"],
                      ("answered", "insufficient_evidence", "generator_rejected"))


if __name__ == "__main__":
    unittest.main()
