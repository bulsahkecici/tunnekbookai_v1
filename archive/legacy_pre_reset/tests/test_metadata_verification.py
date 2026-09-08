from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


verify = load("metadata_verification", ROOT / "scripts/07_metadata_verification.py")
llm = load("verification_llm", ROOT / "scripts/05_metadata_llm_review.py")
adj = load("verification_adj", ROOT / "scripts/06_metadata_adjudication.py")


def context(text, headings=None, snippets=None):
    return {"title_cover_headings": headings or [], "opening_identity_context": text,
            "field_context_snippets": snippets or [], "source_extension": ".pdf"}


def prior(field, deterministic=""):
    return {"document_id": "DOC1", "field": field, "deterministic_suggestion": deterministic,
            "llm_suggestion": "old", "source_sha256": "a" * 64}


def response(value, evidence, relationship="document_identity", confidence="high"):
    return {"value": value, "evidence": evidence, "relationship": relationship, "confidence": confidence}


class MetadataVerificationTests(unittest.TestCase):
    def safe(self, field, reply, ctx, rows=None):
        return verify.verified_safe(field, reply, ctx, prior(field), rows or {}, llm, adj)

    def test_referenced_organization_is_not_identity(self):
        reply = response("PIARC", "The PIARC report states guidance", "referenced_only")
        self.assertFalse(self.safe("organization", reply, context(reply["evidence"])))

    def test_referenced_and_event_year_are_not_publication_year(self):
        for evidence, relationship in (("A 2015 study showed", "referenced_only"),
                                       ("In 2018 a tunnel opened", "event_only")):
            with self.subTest(evidence=evidence):
                self.assertFalse(self.safe("year", response(evidence.split()[1 if "2015" in evidence else 1], evidence,
                                                                     relationship), context(evidence)))

    def test_title_page_publication_year_is_accepted(self):
        reply = response("2021", "Published 2021", "publication_identity")
        self.assertTrue(self.safe("year", reply, context("Tunnel Report. Published 2021.")))

    def test_journal_issue_year_is_accepted(self):
        evidence = "Journal of Tunnels Volume 8 Issue 2 2020"
        reply = response("2020", evidence, "publication_identity")
        self.assertTrue(self.safe("year", reply, context(evidence)))

    def test_section_title_is_not_document_title(self):
        reply = response("Chapter 4 Ventilation", "Chapter 4 Ventilation")
        self.assertFalse(self.safe("title", reply, context(reply["evidence"], [reply["evidence"]])))

    def test_first_page_organization_ownership_is_accepted(self):
        evidence = "Prepared by AECOM Limited"
        reply = response("AECOM Limited", evidence)
        item = prior("organization")
        item["llm_suggestion"] = "AECOM Limited"
        self.assertTrue(verify.verified_safe("organization", reply, context(evidence, ["AECOM Limited"]), item, {}, llm, adj))

    def test_conflicting_organization_identity_stays_human(self):
        evidence = "Prepared by AECOM Limited"
        reply = response("AECOM Limited", evidence)
        item = prior("organization")
        item["llm_suggestion"] = "Different Publisher"
        self.assertFalse(verify.verified_safe("organization", reply, context(evidence, ["AECOM Limited"]), item, {}, llm, adj))

    def test_sparse_ocr_caption_is_not_dominant_language_proof(self):
        reply = response("tr", "Enjeksiyon fotoğrafı")
        self.assertFalse(self.safe("language", reply, context("Enjeksiyon fotoğrafı")))

    def test_academic_article_structural_verification(self):
        item = {"llm_suggestion": "academic_article", "llm_evidence": "Journal Volume 2 DOI 10.1/x"}
        package = {"headings": ["Journal of Tunnels"], "first_excerpt": "Journal Volume 2 DOI 10.1/x", "tail_publication_or_references_excerpt": ""}
        self.assertTrue(adj.strong_document_type(item, package))

    def test_thesis_structural_verification(self):
        item = {"llm_suggestion": "thesis", "llm_evidence": "University doctoral thesis"}
        package = {"headings": ["Doctoral Thesis"], "first_excerpt": "University doctoral thesis", "tail_publication_or_references_excerpt": ""}
        self.assertTrue(adj.strong_document_type(item, package))

    def test_presentation_and_training_distinction(self):
        presentation = {"llm_suggestion": "presentation", "llm_evidence": "Technical presentation slides"}
        training = {"llm_suggestion": "training_material", "llm_evidence": "Tunnel training course material"}
        p1 = {"headings": ["Presentation"], "first_excerpt": "Technical presentation slides", "tail_publication_or_references_excerpt": ""}
        p2 = {"headings": ["Training Course"], "first_excerpt": "Tunnel training course material", "tail_publication_or_references_excerpt": ""}
        self.assertTrue(adj.strong_document_type(presentation, p1))
        self.assertTrue(adj.strong_document_type(training, p2))

    def test_seminar_identity_without_slide_structure_is_not_verified_presentation(self):
        evidence = "Austrian Tunnelling Seminar Ankara 2015"
        reply = response("presentation", evidence)
        self.assertFalse(self.safe("document_type", reply, context(evidence, [evidence])))

    def test_pptx_slide_structure_can_verify_presentation(self):
        evidence = "SUNUM ADI Tunnel Safety"
        reply = response("presentation", evidence)
        ctx = context(evidence, [evidence])
        ctx["source_extension"] = ".pptx"
        self.assertTrue(self.safe("document_type", reply, ctx))

    def test_authority_requires_source_identity_relationship(self):
        reply = response("A", "FHWA report states", "referenced_only")
        self.assertFalse(self.safe("authority_level", reply, context(reply["evidence"])))

    def test_second_pass_cache_identity_and_resume(self):
        item = prior("year")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = verify.cache_path(root, item, "model")
            path.parent.mkdir(parents=True)
            payload = {"document_id": "DOC1", "source_sha256": "a" * 64, "field": "year", "model": "model",
                       "prompt_version": verify.PROMPT_VERSION, "response": response("2021", "Published 2021")}
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(verify.read_cache(path, item, "model")["response"]["value"], "2021")
            self.assertIsNone(verify.read_cache(path, item, "other-model"))

    def test_v4_serialization_is_deterministic(self):
        row = {field: "" for field in verify.V4_FIELDS}
        self.assertEqual(verify.csv_bytes([row], verify.V4_FIELDS), verify.csv_bytes([row], verify.V4_FIELDS))

    def test_verified_candidate_has_214_unique_and_preserves_base(self):
        base = []
        for index in range(214):
            base.append({"document_id": f"DOC{index:06d}", "language_value": "en", "language_source": "existing_verified",
                         "language_confidence": "high", "language_verification_status": "verified_existing"})
        result, _ = verify.build_verified_candidate(base, [])
        self.assertEqual(len(result), 214)
        self.assertEqual(len({row["document_id"] for row in result}), 214)
        self.assertTrue(all(row["language_value"] == "en" for row in result))

    def test_parse_fenced_json_and_rejects_prose(self):
        raw = json.dumps(response("2021", "Published 2021", "publication_identity"))
        self.assertEqual(verify.parse_response(f"```json\n{raw}\n```")["value"], "2021")
        with self.assertRaises(ValueError):
            verify.parse_response("answer: " + raw)


if __name__ == "__main__":
    unittest.main()
