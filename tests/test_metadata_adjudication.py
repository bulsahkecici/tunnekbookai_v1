from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


adj = load("metadata_adjudication", ROOT / "scripts/06_metadata_adjudication.py")
llm = load("metadata_llm_review_for_adjudication", ROOT / "scripts/05_metadata_llm_review.py")


def package(text: str, headings=None):
    return {
        "headings": headings or [], "first_excerpt": text,
        "tail_publication_or_references_excerpt": "", "requested_fields": list(adj.FIELDS),
    }


def row(field: str, suggestion: str, evidence: str, *, confidence="high", agreement="llm_only",
        deterministic="", current=""):
    return {
        "document_id": "DOC1", "field": field, "current_value": current,
        "deterministic_suggestion": deterministic, "llm_suggestion": suggestion,
        "llm_evidence": evidence, "llm_confidence": confidence, "agreement_status": agreement,
        "source_sha256": "a" * 64,
    }


class MetadataAdjudicationTests(unittest.TestCase):
    def decide(self, item, context, document_rows=None):
        rows = document_rows or {item["field"]: item}
        return adj.adjudicate_row(item, context, rows, llm)

    def test_high_confidence_llm_only_is_not_always_review(self):
        item = row("language", "en", "The tunnel manual is written in English")
        context = package("The tunnel manual is written in English and the document provides guidance for operations. " * 10)
        self.assertEqual(self.decide(item, context)["adjudication_status"], "auto_safe_candidate")

    def test_grounded_language_auto_safe(self):
        item = row("language", "tr", "Tünel bakım ve işletme kılavuzu")
        context = package("Tünel bakım ve işletme kılavuzu için bu bölüm ve güvenlik ile ilgili bilgiler sunar. " * 10)
        self.assertTrue(adj.strong_language(item, context))

    def test_grounded_document_type_auto_safe(self):
        item = row("document_type", "academic_article", "Journal article, Volume 12, Issue 3")
        context = package("Journal article, Volume 12, Issue 3. Abstract. Tunnel research.", ["Journal of Tunnel Research"])
        self.assertEqual(self.decide(item, context)["adjudication_status"], "auto_safe_candidate")

    def test_abstract_without_journal_identity_is_not_academic_article_auto_safe(self):
        item = row("document_type", "academic_article", "ÖZ ABSTRACT")
        context = package("ÖZ ABSTRACT. Tünel araştırmasının sonuçları.", ["ÖZ", "ABSTRACT"])
        self.assertEqual(self.decide(item, context)["adjudication_status"], "human_review_required")

    def test_publication_year_evidence_auto_safe(self):
        item = row("year", "2021", "Published 2021")
        context = package("Tunnel Safety Report. Published 2021.")
        self.assertEqual(self.decide(item, context)["adjudication_status"], "auto_safe_candidate")

    def test_event_year_is_not_publication_year(self):
        item = row("year", "2018", "In September 2018 a tunnelling forum was held")
        context = package("In September 2018 a tunnelling forum was held to discuss safety.")
        decision = self.decide(item, context)
        self.assertEqual(decision["adjudication_status"], "human_review_required")
        self.assertEqual(decision["review_priority"], "P1")

    def test_referenced_organization_is_not_publisher(self):
        item = row("organization", "PIARC", "The PIARC report Classification of tunnels contains guidance")
        context = package("The PIARC report Classification of tunnels contains guidance for operators.")
        self.assertEqual(self.decide(item, context)["adjudication_status"], "human_review_required")

    def test_referenced_piarc_or_kgm_is_not_authority_a(self):
        for institution in ("PIARC", "KGM"):
            with self.subTest(institution=institution):
                evidence = f"The {institution} report states tunnel requirements"
                item = row("authority_level", "A", evidence)
                context = package(evidence)
                self.assertEqual(self.decide(item, context)["adjudication_status"], "human_review_required")

    def test_real_kgm_title_page_identity_can_be_a_candidate(self):
        evidence = "KARAYOLLARI GENEL MÜDÜRLÜĞÜ official BAKIM DAİRESİ BAŞKANLIĞI manual"
        item = row("authority_level", "A", evidence)
        context = package(evidence + " TÜNEL BAKIM İŞLETME", ["KARAYOLLARI GENEL MÜDÜRLÜĞÜ", "BAKIM DAİRESİ BAŞKANLIĞI"])
        self.assertEqual(self.decide(item, context)["adjudication_status"], "auto_safe_candidate")

    def test_academic_journal_identity_can_be_b_candidate(self):
        evidence = "Academic journal article, DOI 10.1234/example"
        authority = row("authority_level", "B", evidence)
        doc_type = row("document_type", "academic_article", "Journal article DOI 10.1234/example")
        rows = {"authority_level": authority, "document_type": doc_type}
        context = package(evidence + " Journal of Tunnel Research", ["Journal of Tunnel Research"])
        self.assertEqual(self.decide(authority, context, rows)["adjudication_status"], "auto_safe_candidate")

    def test_university_affiliation_alone_is_not_authority_b(self):
        evidence = "Graz University of Technology"
        authority = row("authority_level", "B", evidence)
        doc_type = row("document_type", "conference_paper", evidence)
        rows = {"authority_level": authority, "document_type": doc_type}
        context = package(evidence, [evidence])
        self.assertEqual(self.decide(authority, context, rows)["adjudication_status"], "human_review_required")

    def test_wikipedia_identity_can_be_d_candidate(self):
        evidence = "Wikipedia general web article"
        authority = row("authority_level", "D", evidence)
        doc_type = row("document_type", "web_article", "Wikipedia website page")
        context = package("Wikipedia general web article. Wikipedia website page.", ["Wikipedia"])
        rows = {"authority_level": authority, "document_type": doc_type}
        self.assertEqual(self.decide(authority, context, rows)["adjudication_status"], "auto_safe_candidate")

    def test_unresolved_blank_is_nonblocking_not_p0(self):
        item = row("year", "", "[evidence_not_grounded_in_context]", confidence="low", agreement="unresolved")
        decision = self.decide(item, package("No date is supplied."))
        self.assertEqual(decision["adjudication_status"], "unresolved_nonblocking")
        self.assertEqual(decision["review_priority"], "NONBLOCKING")

    def test_true_conflict_remains_p0(self):
        item = row("year", "2021", "Published 2021", deterministic="2020", agreement="deterministic_llm_conflict")
        decision = self.decide(item, package("Published 2021"))
        self.assertEqual(decision["adjudication_status"], "human_review_required")
        self.assertEqual(decision["review_priority"], "P0")

    def test_existing_verified_metadata_is_preserved(self):
        item = row("language", "en", "The document is in English", current="tr")
        decision = self.decide(item, package("The document is in English"))
        self.assertEqual(decision["adjudication_status"], "verified_existing")
        self.assertEqual(decision["selected_candidate"], "tr")

    def test_candidate_master_has_214_unique_document_ids(self):
        master = []
        for index in range(214):
            master.append({
                "document_id": f"DOC{index:06d}", "source_relative_path": f"x/{index}.pdf",
                "source_filename": f"{index}.pdf", "source_extension": ".pdf", "source_sha256": f"{index:064x}",
                "year_current": "", "language_current": "en", "document_type_current": "manual",
                "authority_level_current": "", "topics_current": "safety", "title_suggested": f"Title {index}",
                "organization_suggested": "", "year_suggested": "", "language_suggested": "en",
                "document_type_suggested": "manual", "authority_level_suggested": "unclassified",
                "topics_suggested": "safety", "year_confidence": "low", "language_confidence": "high",
                "document_type_confidence": "high", "authority_confidence": "low", "topics_confidence": "high",
            })
        candidates, _ = adj.build_candidate_master(master, [], llm)
        self.assertEqual(len(candidates), 214)
        self.assertEqual(len({item["document_id"] for item in candidates}), 214)

    def test_serialization_is_idempotent(self):
        item = self.decide(row("year", "2021", "Published 2021"), package("Published 2021"))
        self.assertEqual(adj.csv_bytes([item], adj.ADJUDICATION_FIELDS), adj.csv_bytes([item], adj.ADJUDICATION_FIELDS))


if __name__ == "__main__":
    unittest.main()
