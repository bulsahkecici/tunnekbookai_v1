from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/05_metadata_llm_review.py"
SPEC = importlib.util.spec_from_file_location("metadata_llm_review", SCRIPT)
llm = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(llm)


def response_json(**overrides) -> str:
    response = {
        "title": {"value": "Tunnel Safety Manual", "confidence": "high", "evidence": "Tunnel Safety Manual"},
        "organization": {"value": "FHWA", "confidence": "high", "evidence": "Federal Highway Administration"},
        "year": {"value": 2020, "confidence": "high", "evidence": "Published 2020"},
        "language": {"value": "en", "confidence": "high", "evidence": "not_requested"},
        "document_type": {"value": "manual", "confidence": "high", "evidence": "not_requested"},
        "authority_level": {"value": "A", "confidence": "high", "evidence": "Federal Highway Administration official manual"},
        "topics": {"value": ["safety"], "confidence": "high", "evidence": "not_requested"},
    }
    response.update(overrides)
    return json.dumps(response)


def master_row() -> dict[str, str]:
    return {
        "document_id": "DOC1", "source_relative_path": "Manuals/FHWA Manual.pdf",
        "source_filename": "FHWA Manual.pdf", "source_extension": ".pdf",
        "source_sha256": "a" * 64, "selected_variant": "full_docling",
        "authority_level_current": "", "authority_level_suggested": "unclassified",
        "authority_evidence": "deterministic uncertain", "authority_confidence": "low",
        "document_type_current": "manual", "document_type_suggested": "manual",
        "document_type_evidence": "verified", "document_type_confidence": "high",
        "language_current": "en", "language_suggested": "en", "language_confidence": "high",
        "year_current": "", "year_suggested": "", "year_evidence": "missing", "year_confidence": "low",
        "topics_current": "safety", "topics_suggested": "safety", "topics_evidence": "verified",
        "topics_confidence": "high", "organization_suggested": "",
        "title_suggested": "Tunnel Safety Manual", "citation_mode": "pdf_page",
        "citation_sidecar": "x.json", "original_page_provenance_available": "true",
        "requires_human_review": "true", "review_status": "pending",
    }


def fixture(root: Path) -> None:
    row = master_row()
    metadata = root / "data/metadata"
    llm.atomic_write(metadata / "final_metadata_master.csv", llm.csv_bytes([row], list(row)))
    corpus = root / "data/corpus_final/Manuals/FHWA Manual.md"
    corpus.parent.mkdir(parents=True)
    corpus.write_text(
        "---\ndocument_id: DOC1\n---\n# Tunnel Safety Manual\n"
        "Federal Highway Administration official manual. Published 2020. "
        + "Tunnel safety inspection and maintenance guidance. " * 120,
        encoding="utf-8",
    )


class LocalLLMReviewTests(unittest.TestCase):
    def package(self):
        row = master_row()
        markdown = (
            "# Tunnel Safety Manual\nFederal Highway Administration official manual. Published 2020. "
            + "Tunnel safety inspection and maintenance guidance. " * 100
        )
        return llm.context_package(row, markdown)

    def test_local_endpoint_disabled_by_default(self):
        config = llm.load_yaml(ROOT / "config/metadata_llm.yaml")
        self.assertIs(config["enabled"], False)
        self.assertEqual(config["base_url"], "http://127.0.0.1:1234/v1")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            calls = []
            summary = llm.run(root, config, explicit_run=False, transport=lambda *args: calls.append(args))
            self.assertEqual(summary["endpoint_status"], "disabled")
            self.assertEqual(summary["documents_sent"], 0)
            self.assertFalse(calls)

    def test_valid_structured_json_parsing(self):
        parsed = llm.parse_structured_json(response_json())
        self.assertEqual(set(parsed), set(llm.FIELDS))
        self.assertEqual(parsed["authority_level"]["value"], "A")
        fenced = llm.parse_structured_json("```json\n" + response_json() + "\n```")
        self.assertEqual(fenced["year"]["value"], 2020)
        with self.assertRaises(llm.InvalidStructuredOutput):
            llm.parse_structured_json("Here is JSON:\n" + response_json())

    def test_invalid_json_retries_then_succeeds(self):
        replies = iter(["not json", response_json()])
        calls = []

        def transport(*_):
            calls.append(1)
            return next(replies)

        result, retries = llm.call_with_retry(
            "http://127.0.0.1:1234/v1", "local-model", self.package(), 0.1, 10, 2, transport
        )
        self.assertEqual(len(calls), 2)
        self.assertEqual(retries, 1)
        self.assertEqual(result["year"]["value"], 2020)

    def test_transient_local_http_error_retries_then_succeeds(self):
        replies = iter([
            urllib.error.HTTPError("http://127.0.0.1:1234/v1/chat/completions", 400, "model crash", {}, None),
            response_json(),
        ])

        def transport(*_):
            reply = next(replies)
            if isinstance(reply, Exception):
                raise reply
            return reply

        result, retries = llm.call_with_retry(
            "http://127.0.0.1:1234/v1", "local-model", self.package(), 0.1, 10, 2, transport
        )
        self.assertEqual(retries, 1)
        self.assertEqual(result["year"]["value"], 2020)

    def test_hallucinated_evidence_is_low_confidence_and_reviewed(self):
        item = {"value": "NASA", "confidence": "high", "evidence": "NASA headquarters official publication"}
        validated = llm.validated_item("organization", item, self.package())
        self.assertEqual(validated["confidence"], "low")
        self.assertIn("evidence_not_grounded", validated["evidence"])
        response = llm.parse_structured_json(response_json(organization=item))
        response = llm.validate_response(response, self.package())
        rows = llm.suggestion_rows_for_document(master_row(), response, "model", "time")
        organization = next(row for row in rows if row["field"] == "organization")
        self.assertEqual(organization["requires_human_review"], "true")

    def test_controlled_vocabulary_enforcement(self):
        invalid_type = llm.validated_item(
            "document_type", {"value": "invented_slug", "confidence": "high", "evidence": "Tunnel Safety Manual"}, self.package()
        )
        invalid_topics = llm.validated_item(
            "topics", {"value": ["safety", "invented_topic"], "confidence": "high", "evidence": "Tunnel safety"}, self.package())
        self.assertEqual((invalid_type["value"], invalid_type["confidence"]), ("unknown", "low"))
        self.assertEqual(invalid_topics["value"], ["safety"])
        self.assertEqual(invalid_topics["confidence"], "low")

    def test_authority_a_requires_strong_in_document_context(self):
        package = self.package()
        package["headings"] = ["Tunnel Manual"]
        package["first_excerpt"] = "General professional training material without an official publisher."
        item = {"value": "A", "confidence": "high", "evidence": "FHWA in filename"}
        validated = llm.validated_item("authority_level", item, package)
        self.assertEqual(validated["value"], "unclassified")
        self.assertEqual(validated["confidence"], "low")

    def test_authority_a_needs_official_signal_in_evidence_not_elsewhere(self):
        package = self.package()
        item = {"value": "A", "confidence": "high", "evidence": "Academic journal article"}
        validated = llm.validated_item("authority_level", item, package)
        self.assertEqual(validated["value"], "unclassified")
        self.assertEqual(validated["confidence"], "low")

    def test_identity_value_must_be_supported_by_its_evidence(self):
        item = {"value": "Invented Handbook", "confidence": "high", "evidence": "Tunnel safety inspection"}
        validated = llm.validated_item("title", item, self.package())
        self.assertEqual(validated["confidence"], "low")
        self.assertIn("suggested_value_not_supported", validated["evidence"])

    def test_authority_b_c_d_require_matching_evidence_class(self):
        package = self.package()
        for value in ("B", "C", "D"):
            with self.subTest(value=value):
                item = {"value": value, "confidence": "high", "evidence": "Tunnel safety manual"}
                validated = llm.validated_item("authority_level", item, package)
                self.assertEqual(validated["value"], "unclassified")
                self.assertEqual(validated["confidence"], "low")
        academic_package = dict(package)
        academic_package["first_excerpt"] = str(package["first_excerpt"]) + " Academic journal article."
        academic = llm.validated_item(
            "authority_level", {"value": "B", "confidence": "high", "evidence": "Academic journal article"}, academic_package
        )
        self.assertEqual(academic["value"], "B")

    def test_cache_resume_avoids_second_llm_call_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            config = {"enabled": False, "base_url": "http://127.0.0.1:1234/v1", "model": "local-model",
                      "temperature": 0.1, "max_retries": 2, "timeout_seconds": 10}
            calls = []

            def transport(*_):
                calls.append(1)
                return response_json()

            master_before = (root / "data/metadata/final_metadata_master.csv").read_bytes()
            discovery = lambda *_: "local-model"
            first = llm.run(root, config, explicit_run=True, transport=transport, model_discovery=discovery)
            artifacts = [root / "data/metadata/metadata_llm_suggestions.csv",
                         root / "data/metadata/final_metadata_review_queue_v2.csv"]
            first_hashes = [llm.sha256_bytes(path.read_bytes()) for path in artifacts]
            second = llm.run(root, config, explicit_run=True, transport=transport, model_discovery=discovery)
            second_hashes = [llm.sha256_bytes(path.read_bytes()) for path in artifacts]
            self.assertEqual(first["documents_sent"], 1)
            self.assertEqual(second["cache_hits"], 1)
            self.assertEqual(len(calls), 1)
            self.assertEqual(first_hashes, second_hashes)
            self.assertEqual(master_before, (root / "data/metadata/final_metadata_master.csv").read_bytes())

            rows = llm.read_csv(artifacts[0])
            self.assertTrue(rows)
            self.assertTrue(all(row["source_sha256"] == "a" * 64 for row in rows))

    def test_cache_identity_changes_for_sha_model_and_prompt(self):
        row = master_row()
        first = llm.cache_identity(row, "model-a")
        changed = dict(row, source_sha256="b" * 64)
        self.assertNotEqual(first, llm.cache_identity(changed, "model-a"))
        self.assertNotEqual(first, llm.cache_identity(row, "model-b"))
        with patch.object(llm, "PROMPT_VERSION", "different-prompt"):
            self.assertNotEqual(first, llm.cache_identity(row, "model-a"))

    def test_model_discovery_prefers_exact_configured_id(self):
        class Response:
            def __enter__(self):
                return self
            def __exit__(self, *_):
                return False
            def read(self):
                return json.dumps({"data": [{"id": "other"}, {"id": "preferred-model"}]}).encode()

        with patch.object(llm.urllib.request, "urlopen", return_value=Response()):
            self.assertEqual(llm.discover_model("http://127.0.0.1:1234/v1", 10, "preferred-model"), "preferred-model")
            with self.assertRaises(llm.LLMReviewError):
                llm.discover_model("http://127.0.0.1:1234/v1", 10, "missing-model")

    def test_unreachable_endpoint_is_no_go_without_transport_call(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            config = {"enabled": True, "base_url": "http://127.0.0.1:1234/v1", "model": "local-model"}
            calls = []

            def unavailable(*_):
                raise OSError("offline")

            summary = llm.run(root, config, explicit_run=True, transport=lambda *args: calls.append(args),
                              model_discovery=unavailable)
            self.assertEqual(summary["decision"], "NO-GO")
            self.assertEqual(summary["endpoint_status"], "unavailable")
            self.assertFalse(calls)

    def test_only_loopback_endpoint_is_allowed(self):
        llm.assert_local_endpoint("http://localhost:1234/v1")
        with self.assertRaises(llm.LLMReviewError):
            llm.assert_local_endpoint("https://api.example.com/v1")

    def test_json_schema_uses_controlled_vocabularies(self):
        response_format = llm.structured_response_format()
        schema = response_format["json_schema"]["schema"]
        self.assertEqual(response_format["type"], "json_schema")
        self.assertEqual(schema["properties"]["document_type"]["properties"]["value"]["type"], "string")
        self.assertFalse(schema["additionalProperties"])
        rejected = llm.validated_item(
            "document_type", {"value": "outside_vocab", "confidence": "high", "evidence": "Smoke Test"}, self.package()
        )
        self.assertEqual((rejected["value"], rejected["confidence"]), ("unknown", "low"))

    def test_context_window_is_deterministic_and_character_bounded(self):
        row = master_row()
        markdown = "# Dense OCR\n" + (("abcdefghij " * 3000) + ("tailtoken " * 1000))
        first = llm.context_package(row, markdown)
        second = llm.context_package(row, markdown)
        self.assertEqual(first, second)
        self.assertLessEqual(len(first["first_excerpt"]), 12000)
        self.assertLessEqual(len(first["tail_publication_or_references_excerpt"]), 4000)

    def test_conflict_detection_and_priority(self):
        self.assertEqual(llm.agreement("year", "", "2018", 2020, "high"), "deterministic_llm_conflict")
        row = {"field": "year", "agreement_status": "deterministic_llm_conflict",
               "deterministic_suggestion": "2018", "llm_suggestion": "2020"}
        self.assertEqual(llm.review_priority(row), "P0")
        row.update(field="organization", agreement_status="llm_only", deterministic_suggestion="", llm_suggestion="FHWA")
        self.assertEqual(llm.review_priority(row), "P1")
        row.update(field="topics")
        self.assertEqual(llm.review_priority(row), "P2")


if __name__ == "__main__":
    unittest.main()
