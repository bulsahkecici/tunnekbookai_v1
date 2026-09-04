from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    spec = importlib.util.spec_from_file_location("semantic_chunking", ROOT / "scripts/11_semantic_chunking.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


chunker = load_module()

_CORPUS_CACHE: dict[str, object] = {}


def corpus():
    """Chunk the whole normalized corpus once and share it across the corpus-level tests."""
    if "documents" not in _CORPUS_CACHE:
        documents, metadata_source = chunker.analyze_all(ROOT)
        _CORPUS_CACHE["documents"] = documents
        _CORPUS_CACHE["metadata_source"] = metadata_source
        _CORPUS_CACHE["chunks"] = [chunk for document in documents for chunk in document["chunks"]]
    return _CORPUS_CACHE["documents"], _CORPUS_CACHE["chunks"]


FRONT_MATTER = """---
document_id: "{document_id}"
title: "Synthetic Fixture"
source_relative_path: "synthetic/{document_id}.pdf"
source_extension: "{extension}"
sha256: "{sha}"
---

"""


def write_document(directory: Path, body: str, document_id: str = "DOC000999", extension: str = ".pdf") -> Path:
    path = directory / f"{document_id}.md"
    front = FRONT_MATTER.format(document_id=document_id, extension=extension, sha="0" * 64)
    path.write_text(front + body, encoding="utf-8")
    return path


def chunk_body(body: str, document_id: str = "DOC000999", extension: str = ".pdf",
               verified: dict | None = None, master: dict | None = None) -> dict:
    with tempfile.TemporaryDirectory() as directory:
        path = write_document(Path(directory), body, document_id, extension)
        base = {"source_relative_path": f"synthetic/{document_id}.pdf", "source_extension": extension,
                "source_sha256": "0" * 64}
        return chunker.chunk_document(path, ROOT, {**base, **(verified or {})}, master or {})


def prose(tokens: int, word: str = "tunnel") -> str:
    return " ".join([word] * tokens)


class TestChunkIdentity(unittest.TestCase):
    def test_deterministic_chunk_ids(self):
        body = "\n\n".join(f"## Section {index}\n\n{prose(400)}" for index in range(4))
        first = chunk_body(body)["chunks"]
        second = chunk_body(body)["chunks"]
        self.assertEqual([chunk["chunk_id"] for chunk in first], [chunk["chunk_id"] for chunk in second])
        self.assertEqual([chunk["text"] for chunk in first], [chunk["text"] for chunk in second])

    def test_chunk_id_format_and_ordering(self):
        body = "\n\n".join(f"## Section {index}\n\n{prose(900)}" for index in range(3))
        chunks = chunk_body(body, document_id="DOC000123")["chunks"]
        self.assertGreater(len(chunks), 1)
        for position, chunk in enumerate(chunks, start=1):
            self.assertEqual(chunk["chunk_id"], f"DOC000123-C{position:04d}")
            self.assertEqual(chunk["chunk_index"], position)

    def test_duplicate_ids_impossible_within_document(self):
        body = "\n\n".join(f"## Section {index}\n\n{prose(700)}" for index in range(12))
        chunks = chunk_body(body)["chunks"]
        self.assertEqual(len(chunks), len({chunk["chunk_id"] for chunk in chunks}))


class TestStructure(unittest.TestCase):
    def test_heading_hierarchy_tracks_levels(self):
        hierarchy = [None, None, None, None]
        for text, expected_path, expected_parent in (("# Top\n", "Top", None),
                                                     ("## Middle\n", "Top > Middle", "Top"),
                                                     ("### Leaf\n", "Top > Middle > Leaf", "Middle")):
            hierarchy, heading, parent, path = chunker.heading_context(text, hierarchy)
            self.assertEqual(path, expected_path)
            self.assertEqual(parent, expected_parent)
        self.assertEqual(heading, "Leaf")

    def test_sibling_heading_resets_deeper_levels(self):
        hierarchy = [None, None, None, None]
        for text in ("# Top\n", "## A\n", "### Deep\n"):
            hierarchy, *_ = chunker.heading_context(text, hierarchy)
        hierarchy, heading, parent, path = chunker.heading_context("## B\n", hierarchy)
        self.assertEqual(heading, "B")
        self.assertEqual(path, "Top > B")
        self.assertEqual(parent, "Top")

    def test_section_path_attaches_to_document_chunks(self):
        body = ("# Top\n\n" + prose(1200) + "\n\n## Middle\n\n" + prose(1200) +
                "\n\n### Leaf\n\n" + prose(1200))
        chunks = chunk_body(body)["chunks"]
        paths = {chunk["section_path"] for chunk in chunks}
        self.assertIn("Top", paths)
        self.assertIn("Top > Middle", paths)
        self.assertIn("Top > Middle > Leaf", paths)

    def test_small_subsections_coalesce_instead_of_fragmenting(self):
        body = ("# Top\n\n" + prose(120) + "\n\n## Middle\n\n" + prose(120) +
                "\n\n### Leaf\n\n" + prose(120))
        chunks = chunk_body(body)["chunks"]
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["section_path"], "Top")

    def test_paragraph_splitting_uses_blank_line_blocks(self):
        blocks = chunker.paragraph_blocks("one\n\ntwo\n\nthree")
        self.assertEqual(len(blocks), 3)
        self.assertEqual("".join(blocks), "one\n\ntwo\n\nthree")

    def test_small_semantic_section_preserved_not_shattered(self):
        body = "## Short Note\n\n" + prose(60)
        chunks = chunk_body(body)["chunks"]
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["heading"], "Short Note")

    def test_regulation_madde_is_strong_boundary(self):
        body = ("MADDE 1 - " + prose(300) + "\n\nMADDE 2 - " + prose(300) +
                "\n\nMADDE 3 - " + prose(300))
        chunks = chunk_body(body)["chunks"]
        starts = [chunk["text"].lstrip()[:8] for chunk in chunks]
        self.assertGreaterEqual(len(chunks), 3)
        self.assertTrue(all(start.startswith("MADDE") for start in starts), starts)

    def test_article_boundary_recognised(self):
        self.assertTrue(chunker.REGULATION_RE.match("Article 12 - Scope"))
        self.assertTrue(chunker.REGULATION_RE.match("MADDE 7/A"))


class TestSizing(unittest.TestCase):
    def test_target_token_sizing_stays_within_soft_max(self):
        body = "## Body\n\n" + "\n\n".join(prose(120) for _ in range(40))
        chunks = chunk_body(body)["chunks"]
        self.assertTrue(all(chunk["token_count"] <= chunker.SOFT_MAX for chunk in chunks))
        self.assertGreater(max(chunk["token_count"] for chunk in chunks), chunker.SOFT_MIN)

    def test_hard_limit_split_at_line_boundaries(self):
        oversized = "## Refs\n\n" + "\n".join(f"{index}. {prose(30)}" for index in range(80))
        chunks = chunk_body(oversized)["chunks"]
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(chunk["token_count"] <= chunker.HARD_MAX for chunk in chunks))

    def test_justified_atomic_hard_limit_exception_for_tables(self):
        header = "| A | B |\n|---|---|\n"
        rows = "".join(f"| {prose(20)} | {prose(20)} |\n" for _ in range(60))
        result = chunk_body("## Table\n\n" + header + rows)
        oversized = [chunk for chunk in result["chunks"] if chunk["token_count"] > chunker.HARD_MAX]
        self.assertTrue(oversized, "fixture should exceed the hard limit")
        self.assertTrue(all(chunk["contains_table"] for chunk in oversized))
        self.assertIn("huge_atomic_table_over_hard_limit", result["warnings"])

    def test_enforce_hard_limit_keeps_tables_atomic(self):
        table = "| A | B |\n|---|---|\n" + "".join(f"| {prose(25)} | {prose(25)} |\n" for _ in range(50))
        pieces, warnings = chunker.enforce_hard_limit([table])
        self.assertEqual(pieces, [table])
        self.assertEqual(warnings, ["huge_atomic_table_over_hard_limit"])

    def test_enforce_hard_limit_splits_plain_prose(self):
        block = "\n".join(prose(60) for _ in range(40))
        pieces, warnings = chunker.enforce_hard_limit([block])
        self.assertGreater(len(pieces), 1)
        self.assertEqual(warnings, [])
        self.assertEqual("".join(pieces), block)


class TestContentPreservation(unittest.TestCase):
    def test_markdown_table_never_split(self):
        table = "| A | B |\n|---|---|\n" + "".join(f"| {index} | {prose(5)} |\n" for index in range(30))
        result = chunk_body("## Table\n\n" + table)
        with_table = [chunk for chunk in result["chunks"] if chunk["contains_table"]]
        self.assertEqual(len(with_table), 1)
        self.assertEqual(result["table_corruption"], [])

    def test_big_table_header_stays_with_its_rows(self):
        header = "| Metric | Value |\n|---|---|\n"
        table = header + "".join(f"| {prose(18)} | {index} |\n" for index in range(90))
        result = chunk_body("## Big Table\n\n" + table)
        holders = [chunk for chunk in result["chunks"] if "| Metric | Value |" in chunk["text"]]
        self.assertEqual(len(holders), 1)
        self.assertIn("|---|---|", holders[0]["text"])
        self.assertEqual(result["table_corruption"], [])

    def test_table_corruption_detected_when_header_orphaned(self):
        chunks = [{"chunk_id": "DOC-C0001", "text": "| A | B |\n|---|---|\n| 1 | 2 |\n"},
                  {"chunk_id": "DOC-C0002", "text": "| 3 | 4 |\n| 5 | 6 |\n"}]
        self.assertEqual(chunker.table_corruption(chunks), ["DOC-C0002"])

    def test_adjacent_distinct_tables_are_not_corruption(self):
        chunks = [{"chunk_id": "DOC-C0001", "text": "| A | B |\n|---|---|\n| 1 | 2 |\n"},
                  {"chunk_id": "DOC-C0002", "text": "| C | D |\n|---|---|\n| 5 | 6 |\n"}]
        self.assertEqual(chunker.table_corruption(chunks), [])

    def test_list_preserved_without_mid_item_split(self):
        items = "\n".join(f"- inspection step {index}: {prose(12)}" for index in range(40))
        result = chunk_body("## Checklist\n\n" + items)
        for chunk in result["chunks"]:
            for line in chunk["text"].splitlines():
                if line.strip() and not line.startswith("#") and not line.startswith("<!--"):
                    self.assertTrue(line.lstrip().startswith("- inspection step"), line[:60])

    def test_formula_placeholder_preserved(self):
        body = "## Formula\n\n" + prose(200) + "\n\n<!-- formula-not-decoded -->\n\n" + prose(200)
        result = chunk_body(body)
        self.assertIn("<!-- formula-not-decoded -->", "".join(chunk["text"] for chunk in result["chunks"]))
        self.assertTrue(any(chunk["contains_formula_placeholder"] for chunk in result["chunks"]))

    def test_image_placeholder_preserved(self):
        body = "## Figure\n\n" + prose(200) + "\n\n<!-- image -->\n\n" + prose(200)
        result = chunk_body(body)
        self.assertIn("<!-- image -->", "".join(chunk["text"] for chunk in result["chunks"]))
        self.assertTrue(any(chunk["contains_image_placeholder"] for chunk in result["chunks"]))

    def test_dropped_substantive_text_is_zero_for_mixed_document(self):
        body = ("# Doc\n\n" + prose(400) + "\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n"
                "- item one\n- item two\n\n<!-- image -->\n\nMADDE 4 - " + prose(400))
        result = chunk_body(body)
        self.assertEqual(result["dropped_substantive_text"], 0)
        self.assertEqual("".join(chunk["text"] for chunk in result["chunks"]), result["body"])


class TestProvenance(unittest.TestCase):
    def test_page_provenance_propagates_to_following_chunks(self):
        body = ("<!-- original_page_start: 12 -->\n<!-- original_page_end: 18 -->\n\n"
                "## Section\n\n" + "\n\n".join(prose(300) for _ in range(6)))
        chunks = chunk_body(body)["chunks"]
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertEqual(chunk["original_page_start"], 12)
            self.assertEqual(chunk["original_page_end"], 18)
            self.assertEqual(chunk["provenance_status"], "page_resolved")

    def test_page_range_uses_min_and_max_across_markers(self):
        text = ("<!-- original_page_start: 4 --><!-- original_page_start: 9 -->"
                "<!-- original_page_end: 7 --><!-- original_page_end: 11 -->")
        self.assertEqual(chunker.page_range(text, (None, None)), (4, 11))

    def test_slide_provenance_for_presentations(self):
        body = "\n\n".join(f"## Slayt {index}\n\n{prose(200)}" for index in range(1, 5))
        chunks = chunk_body(body, extension=".pptx")["chunks"]
        slides = [chunk for chunk in chunks if chunk["slide_start"] is not None]
        self.assertTrue(slides)
        self.assertTrue(all(chunk["citation_mode"] == "slide" for chunk in chunks))
        self.assertTrue(any(chunk["provenance_status"] == "slide_resolved" for chunk in chunks))
        for chunk in slides:
            self.assertLessEqual(chunk["slide_start"], chunk["slide_end"])

    def test_section_provenance_for_documents(self):
        body = "# Chapter\n\n## Clause\n\n" + prose(300)
        chunks = chunk_body(body, extension=".docx")["chunks"]
        self.assertTrue(all(chunk["citation_mode"] == "document_section" for chunk in chunks))
        self.assertEqual(chunks[0]["provenance_status"], "section_resolved")
        self.assertTrue(chunks[0]["section_path"])

    def test_source_only_fallback_when_nothing_resolves(self):
        chunks = chunk_body(prose(300), extension=".zzz")["chunks"]
        self.assertTrue(all(chunk["provenance_status"] == "source_only" for chunk in chunks))
        self.assertTrue(all(chunk["citation_mode"] == "source_only" for chunk in chunks))

    def test_provenance_corruption_detector_flags_inverted_pages(self):
        chunks = [{"chunk_id": "DOC-C0001", "original_page_start": 9, "original_page_end": 3,
                   "slide_start": None, "slide_end": None, "provenance_status": "page_resolved",
                   "section_path": "A"}]
        self.assertEqual(chunker.provenance_corruption(chunks), ["DOC-C0001"])

    def test_provenance_corruption_detector_accepts_sound_anchors(self):
        chunks = [{"chunk_id": "DOC-C0001", "original_page_start": 3, "original_page_end": 9,
                   "slide_start": None, "slide_end": None, "provenance_status": "page_resolved",
                   "section_path": "A"}]
        self.assertEqual(chunker.provenance_corruption(chunks), [])

    def test_citation_mode_derived_from_extension(self):
        self.assertEqual(chunker.citation_mode_for_extension(".pdf"), "pdf_page")
        self.assertEqual(chunker.citation_mode_for_extension(".pptx"), "slide")
        self.assertEqual(chunker.citation_mode_for_extension(".docx"), "document_section")
        self.assertEqual(chunker.citation_mode_for_extension(".unknown"), "source_only")


class TestMetadata(unittest.TestCase):
    def test_metadata_propagates_to_every_chunk(self):
        verified = {"title_value": "Tunnel Handbook", "title_verification_status": "verified",
                    "organization_value": "AFAD", "organization_verification_status": "verified",
                    "year_value": "2021", "year_verification_status": "verified",
                    "topics_value": "tbm|natm", "topics_verification_status": "verified"}
        chunks = chunk_body("## S\n\n" + prose(600), verified=verified)["chunks"]
        for chunk in chunks:
            self.assertEqual(chunk["title"], "Tunnel Handbook")
            self.assertEqual(chunk["organization"], "AFAD")
            self.assertEqual(chunk["year"], "2021")
            self.assertEqual(chunk["topics"], ["tbm", "natm"])

    def test_unresolved_metadata_is_not_promoted(self):
        verified = {"title_value": "Guessed Title", "title_verification_status": "still_human_review",
                    "year_value": "1999", "year_verification_status": "unresolved",
                    "organization_value": "Maybe Org", "organization_verification_status": "rejected"}
        chunks = chunk_body("## S\n\n" + prose(300), verified=verified)["chunks"]
        for chunk in chunks:
            self.assertIsNone(chunk["title"])
            self.assertIsNone(chunk["year"])
            self.assertIsNone(chunk["organization"])

    def test_missing_metadata_stays_none_and_is_never_invented(self):
        chunks = chunk_body("## S\n\n" + prose(300))["chunks"]
        for field in ("title", "organization", "year", "language", "document_type", "authority_level"):
            self.assertIsNone(chunks[0][field])

    def test_schema_carries_every_required_field(self):
        required = {"chunk_id", "document_id", "chunk_index", "source_relative_path", "source_extension",
                    "source_sha256", "normalized_source_sha256", "title", "organization", "year", "language",
                    "document_type", "authority_level", "topics", "section_path", "heading", "parent_heading",
                    "text", "token_count", "character_count", "citation_mode", "original_page_start",
                    "original_page_end", "slide_start", "slide_end", "citation_sidecar", "provenance_status",
                    "contains_table", "contains_formula_placeholder", "contains_image_placeholder",
                    "overlap_previous_tokens", "chunker_version"}
        chunk = chunk_body("## S\n\n" + prose(300))["chunks"][0]
        self.assertTrue(required.issubset(chunk.keys()), required - set(chunk.keys()))
        self.assertEqual(chunk["chunker_version"], chunker.CHUNKER_VERSION)


class TestOverlap(unittest.TestCase):
    def test_overlap_is_controlled_and_reported(self):
        body = "## S\n\n" + "\n\n".join(prose(300) for _ in range(8))
        result = chunk_body(body)
        self.assertEqual(result["duplicated_characters"], 0)
        for chunk in result["chunks"]:
            self.assertEqual(chunk["overlap_previous_tokens"], 0)

    def test_no_duplication_explosion_chunk_chars_equal_body_chars(self):
        body = "\n\n".join(f"## S{index}\n\n{prose(500)}" for index in range(6))
        result = chunk_body(body)
        self.assertEqual(sum(len(chunk["text"]) for chunk in result["chunks"]), len(result["body"]))


class TestGatePolicy(unittest.TestCase):
    def make_document(self, **overrides):
        base = {"document_id": "DOC000001", "chunks": [{"chunk_id": "DOC000001-C0001", "token_count": 900,
                                                        "contains_table": False, "text": prose(900),
                                                        "provenance_status": "page_resolved"}],
                "dropped_substantive_text": 0, "table_corruption": [], "provenance_corruption": [],
                "warnings": []}
        return {**base, **overrides}

    def documents_214(self, **overrides):
        return [self.make_document(document_id=f"DOC{index:06d}", **(overrides if index == 1 else {}))
                for index in range(1, 215)]

    def test_p1_hard_limit_is_not_a_blocker(self):
        huge = {"chunk_id": "DOC000001-C0001", "token_count": 4000, "contains_table": True,
                "text": prose(4000), "provenance_status": "page_resolved"}
        documents = self.documents_214(chunks=[huge])
        self.assertEqual(chunker.blocking_conditions(documents, []), [])

    def test_p1_excessive_tiny_chunks_is_not_a_blocker(self):
        tiny = [{"chunk_id": f"DOC000001-C{index:04d}", "token_count": 20, "contains_table": False,
                 "text": prose(20), "provenance_status": "page_resolved"} for index in range(1, 21)]
        documents = self.documents_214(chunks=tiny)
        self.assertEqual(chunker.blocking_conditions(documents, []), [])

    def test_p0_dropped_text_is_a_blocker(self):
        documents = self.documents_214(dropped_substantive_text=42)
        self.assertTrue(any("dropped substantive text" in item for item in chunker.blocking_conditions(documents, [])))

    def test_p0_table_corruption_is_a_blocker(self):
        documents = self.documents_214(table_corruption=["DOC000001-C0002"])
        self.assertTrue(any("table corruption" in item for item in chunker.blocking_conditions(documents, [])))

    def test_p0_provenance_corruption_is_a_blocker(self):
        documents = self.documents_214(provenance_corruption=["DOC000001-C0002"])
        self.assertTrue(any("provenance corruption" in item for item in chunker.blocking_conditions(documents, [])))

    def test_p0_unchunked_document_is_a_blocker(self):
        documents = self.documents_214(chunks=[])
        self.assertTrue(any("unchunked" in item for item in chunker.blocking_conditions(documents, [])))

    def test_p0_duplicate_chunk_id_is_a_blocker(self):
        documents = self.documents_214()
        self.assertTrue(any("duplicate chunk" in item for item in chunker.blocking_conditions(documents, ["X-C0001"])))

    def test_p0_missing_document_is_a_blocker(self):
        documents = self.documents_214()[:213]
        self.assertTrue(any("coverage" in item for item in chunker.blocking_conditions(documents, [])))

    def test_review_queue_classifies_hard_limit_as_p1(self):
        huge = {"chunk_id": "DOC000001-C0001", "token_count": 4000, "contains_table": True,
                "text": prose(4000), "provenance_status": "page_resolved"}
        rows = chunker.review_queue([self.make_document(chunks=[huge])], [])
        hard = [row for row in rows if row["reason"] == "huge_table_special_case"]
        self.assertTrue(hard)
        self.assertEqual(hard[0]["priority"], "P1")
        self.assertIn("justified_special_case", hard[0]["details"])


class TestCorpus(unittest.TestCase):
    def test_214_document_coverage(self):
        documents, _ = corpus()
        self.assertEqual(len(documents), 214)
        self.assertEqual(len({document["document_id"] for document in documents}), 214)

    def test_no_dropped_substantive_text_across_corpus(self):
        documents, _ = corpus()
        self.assertEqual(sum(document["dropped_substantive_text"] for document in documents), 0)

    def test_no_duplicate_chunk_ids_across_corpus(self):
        documents, chunks = corpus()
        self.assertEqual(chunker.duplicate_chunk_ids(documents), [])
        self.assertEqual(len(chunks), len({chunk["chunk_id"] for chunk in chunks}))

    def test_no_table_or_provenance_corruption_across_corpus(self):
        documents, _ = corpus()
        self.assertEqual(sum(len(document["table_corruption"]) for document in documents), 0)
        self.assertEqual(sum(len(document["provenance_corruption"]) for document in documents), 0)

    def test_corpus_has_no_p0_blockers(self):
        documents, _ = corpus()
        self.assertEqual(chunker.blocking_conditions(documents, chunker.duplicate_chunk_ids(documents)), [])

    def test_every_document_produces_at_least_one_chunk(self):
        documents, _ = corpus()
        self.assertEqual([doc["document_id"] for doc in documents if not doc["chunks"]], [])

    def test_no_pathological_non_substantive_fragments(self):
        _, chunks = corpus()
        self.assertEqual([chunk["chunk_id"] for chunk in chunks if chunker.is_fragment(chunk["text"])], [])

    def test_hard_limit_violations_are_all_justified_atomic_tables(self):
        _, chunks = corpus()
        oversized = [chunk for chunk in chunks if chunk["token_count"] > chunker.HARD_MAX]
        self.assertEqual([chunk["chunk_id"] for chunk in oversized if not chunk["contains_table"]], [])

    def test_doc000021_hard_limit_resolved(self):
        documents, _ = corpus()
        document = next(doc for doc in documents if doc["document_id"] == "DOC000021")
        self.assertEqual([chunk["chunk_id"] for chunk in document["chunks"]
                          if chunk["token_count"] > chunker.HARD_MAX], [])
        self.assertEqual(document["dropped_substantive_text"], 0)

    def test_median_token_size_within_planned_band(self):
        _, chunks = corpus()
        median = chunker.percentile([chunk["token_count"] for chunk in chunks], .50)
        self.assertGreaterEqual(median, 600)
        self.assertLessEqual(median, 1000)

    def test_idempotency_second_pass_matches_first(self):
        _, chunks = corpus()
        documents_again, _ = chunker.analyze_all(ROOT)
        again = [chunk for document in documents_again for chunk in document["chunks"]]
        self.assertEqual(chunker.sha256(chunker.jsonl_bytes(chunks)),
                         chunker.sha256(chunker.jsonl_bytes(again)))

    def test_jsonl_payload_carries_no_timestamp(self):
        _, chunks = corpus()
        payload = chunker.jsonl_bytes(chunks[:50]).decode("utf-8")
        for marker in ("processed_at", "generated_at", "timestamp", "run_at"):
            self.assertNotIn(marker, payload)


class TestProtectedTrees(unittest.TestCase):
    def test_normalized_corpus_immutable_across_chunking(self):
        before = chunker.protected_state(ROOT)
        chunker.analyze_all(ROOT)
        after = chunker.protected_state(ROOT)
        self.assertEqual(before, after)

    def test_protected_state_covers_required_trees(self):
        state = chunker.protected_state(ROOT)
        for relative in ("data/corpus_final", "data/corpus_normalized", "data/markdown", "data/markdown_full_docling"):
            self.assertIn(relative, state)
        self.assertIn("data/metadata/final_corpus_manifest.csv", state)
        self.assertIn("data/metadata/final_metadata_master.csv", state)

    def test_protected_state_excludes_chunking_outputs(self):
        state = chunker.protected_state(ROOT)
        self.assertNotIn("data/metadata/chunk_manifest.csv", state)
        self.assertNotIn("data/metadata/chunk_review_queue.csv", state)


class TestArtifacts(unittest.TestCase):
    def test_manifest_carries_required_columns(self):
        required = {"document_id", "source_sha256", "normalized_sha256", "chunk_count", "min_tokens",
                    "max_tokens", "mean_tokens", "page_resolved_chunks", "slide_resolved_chunks",
                    "section_resolved_chunks", "source_only_chunks", "table_chunks", "formula_chunks",
                    "image_chunks", "warning_count", "chunker_version"}
        self.assertTrue(required.issubset(set(chunker.MANIFEST_FIELDS)))

    def test_manifest_rows_are_sorted_and_complete(self):
        path = ROOT / "data/metadata/chunk_manifest.csv"
        if not path.is_file():
            self.skipTest("chunk manifest not generated yet")
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 214)
        self.assertEqual([row["document_id"] for row in rows], sorted(row["document_id"] for row in rows))

    def test_review_queue_has_no_p0_rows(self):
        path = ROOT / "data/metadata/chunk_review_queue.csv"
        if not path.is_file():
            self.skipTest("review queue not generated yet")
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([row for row in rows if row["priority"] == "P0"], [])

    def test_final_chunks_jsonl_matches_corpus(self):
        path = ROOT / "data/chunks/chunks.jsonl"
        if not path.is_file():
            self.skipTest("final chunks.jsonl not generated yet")
        _, chunks = corpus()
        self.assertEqual(chunker.sha256(path.read_bytes()), chunker.sha256(chunker.jsonl_bytes(chunks)))

    def test_final_chunks_jsonl_is_parseable_and_unique(self):
        path = ROOT / "data/chunks/chunks.jsonl"
        if not path.is_file():
            self.skipTest("final chunks.jsonl not generated yet")
        ids = Counter()
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                ids[json.loads(line)["chunk_id"]] += 1
        self.assertEqual([chunk_id for chunk_id, count in ids.items() if count > 1], [])


if __name__ == "__main__":
    unittest.main()
