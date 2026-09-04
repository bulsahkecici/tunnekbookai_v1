"""Book Citation Rendering v1.

The renderer has one job that can fail invisibly: printing a field the registry does not hold. A
fabricated page number reads exactly like a real one, and a reference list is the last place a
reader would think to check. So most of what follows asserts absence rather than presence - what
did NOT appear in the output - which is the only direction that catches invention.

Determinism is asserted on bytes rather than on structure, because §118's guarantee is that a
rendered draft can be reviewed as a diff.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


renderer = _load("book_citation_renderer_v1", "scripts/48_book_citation_renderer_v1.py")
validator = _load("section_draft_validator_v1", "scripts/49_section_draft_validator_v1.py")

FIXTURES = ROOT / "data" / "evaluation" / "book_citation_rendering_v1.jsonl"
REGISTRY = validator.load_source_registry()

KTS = "SRC-DOC000236-8dfa5f799b50"
KGM = "SRC-DOC000087-8d778c37de30"
FHWA = "SRC-DOC000047-72f96c5daace"
SLIDE = "SRC-DOC000215-9f39b265f06d"
NO_PAGES = "SRC-DOC000124-1190e1676b28"


def unit(unit_id, *pairs, material=True, text="Bir teknik önerme.",
         unit_type="PARAGRAPH_SENTENCE"):
    return validator.DraftUnit(
        unit_id=unit_id, unit_type=unit_type, text=text, material=material,
        claim_ids=[c for c, _ in pairs],
        source_keys=sorted({k for _, ks in pairs for k in ks}),
        citation_intents=[{"claim_id": c, "source_keys": list(ks)} for c, ks in pairs])


def draft(*units, title="Püskürtme Beton"):
    return validator.DraftIR(section_id="SEC-02-2", draft_id="T", draft_version="v1",
                             language="tr", title=title, units=list(units))


class ReferenceFormatting(unittest.TestCase):
    def test_renders_only_fields_the_registry_holds(self):
        self.assertEqual(
            renderer.format_reference(REGISTRY[KTS]),
            "KTS_2013, 351.10.01 Basınç Dayanım Sınıfları, s. 476-500")

    def test_a_row_without_pages_renders_without_a_page(self):
        rendered = renderer.format_reference(REGISTRY[NO_PAGES])
        self.assertEqual(rendered, "YTU Yuksek Lisans")
        self.assertNotIn("s.", rendered)

    def test_required_128_a_missing_page_is_never_invented(self):
        """§128: no page metadata means no page, not 'p. 1'."""
        for key in (NO_PAGES, SLIDE):
            with self.subTest(source=key):
                row = dict(REGISTRY[key])
                row["page_start"] = row["page_end"] = None
                rendered = renderer.format_reference(row)
                for invented in ("s. 1", "s. 0", "p. 1", "sayfa"):
                    self.assertNotIn(invented, rendered)

    def test_no_author_publisher_or_year_is_ever_added(self):
        for key in (KTS, KGM, FHWA, SLIDE, NO_PAGES):
            with self.subTest(source=key):
                rendered = renderer.format_reference(REGISTRY[key]).lower()
                for invented in ("yayınevi", "publisher", "ankara", "washington", "isbn",
                                 "doi", "http", "n.d.", "ed."):
                    self.assertNotIn(invented, rendered)

    def test_a_page_range_is_rendered_as_a_range(self):
        """25-page buckets are honest as ranges and dishonest as a single page."""
        self.assertIn("s. 476-500", renderer.format_reference(REGISTRY[KTS]))

    def test_a_row_without_a_title_is_refused_rather_than_guessed(self):
        row = dict(REGISTRY[KTS])
        row["title"] = None
        with self.assertRaises(renderer.RenderRefused):
            renderer.format_reference(row)


class Numbering(unittest.TestCase):
    def test_required_129_a_reused_source_gets_one_number(self):
        entries = renderer.build_citation_map(
            [unit("U-A-P01-S01", ("SEC-02-2-C-001", [KTS])),
             unit("U-A-P01-S02", ("SEC-02-2-C-001", [KTS])),
             unit("U-B-P01-S01", ("SEC-02-2-C-001", [KTS]))], REGISTRY)
        self.assertEqual([(e.rendered_number, e.source_key) for e in entries], [(1, KTS)])

    def test_required_130_numbering_follows_first_appearance_not_key_order(self):
        """KTS sorts after KGM lexically; it appears first, so it is [1]."""
        self.assertGreater(KTS, KGM)
        entries = renderer.build_citation_map(
            [unit("U-A-P01-S01", ("SEC-02-2-C-001", [KTS])),
             unit("U-B-P01-S01", ("SEC-02-2-C-003", [KGM]))], REGISTRY)
        self.assertEqual([(e.rendered_number, e.source_key) for e in entries],
                         [(1, KTS), (2, KGM)])

    def test_a_claim_may_cite_two_sources(self):
        entries = renderer.build_citation_map(
            [unit("U-A-P01-S01", ("SEC-02-2-C-003", [KGM, KTS]))], REGISTRY)
        self.assertEqual(len(entries), 2)
        numbering = {e.source_key: e.rendered_number for e in entries}
        self.assertEqual(renderer.marker_for(
            unit("U-A-P01-S01", ("SEC-02-2-C-003", [KGM, KTS])), numbering), "[1,2]")

    def test_non_material_units_contribute_no_references(self):
        entries = renderer.build_citation_map(
            [unit("U-A-P01-S01", material=False, unit_type="HEADING", text="Başlık")], REGISTRY)
        self.assertEqual(entries, [])

    def test_required_127_an_unknown_source_key_is_refused(self):
        with self.assertRaises(renderer.RenderRefused):
            renderer.build_citation_map(
                [unit("U-A-P01-S01", ("SEC-02-2-C-001", ["SRC-UNKNOWN-000000000000"]))],
                REGISTRY)

    def test_citation_map_records_the_first_unit_and_the_claims(self):
        entries = renderer.build_citation_map(
            [unit("U-A-P02-S03", ("SEC-02-2-C-001", [KTS])),
             unit("U-B-P01-S01", ("SEC-02-2-R001", [KTS]))], REGISTRY)
        self.assertEqual(entries[0].first_unit_id, "U-A-P02-S03")
        self.assertEqual(entries[0].claim_ids, ["SEC-02-2-C-001", "SEC-02-2-R001"])


class Rendering(unittest.TestCase):
    def setUp(self):
        self.ir = draft(
            unit("U-A-P01-S01", material=False, unit_type="HEADING", text="Dayanım Sınıfı"),
            unit("U-A-P02-S01", ("SEC-02-2-C-001", [KTS]),
                 text="Püskürtme betonun basınç dayanım sınıfı minimum C25/30 sınıfındadır."),
            unit("U-A-P02-S02", ("SEC-02-2-C-003", [KGM]),
                 text="Bir defada uygulanacak kalınlık 15 cm'yi geçmeyecektir."),
        )

    def test_required_118_rendering_is_byte_identical_across_runs(self):
        first, _ = renderer.render(self.ir, REGISTRY)
        second, _ = renderer.render(self.ir, REGISTRY)
        self.assertEqual(first, second)
        self.assertEqual(first.encode("utf-8"), second.encode("utf-8"))

    def test_markers_follow_their_own_proposition(self):
        markdown, _ = renderer.render(self.ir, REGISTRY)
        self.assertIn("C25/30 sınıfındadır.[1]", markdown)
        self.assertIn("15 cm'yi geçmeyecektir.[2]", markdown)

    def test_sentences_of_one_paragraph_join_into_one_block(self):
        markdown, _ = renderer.render(self.ir, REGISTRY)
        body = markdown.split("## Kaynaklar")[0]
        self.assertIn("sınıfındadır.[1] Bir defada", body)

    def test_the_reference_section_is_present_and_numbered(self):
        markdown, entries = renderer.render(self.ir, REGISTRY)
        self.assertIn("## Kaynaklar", markdown)
        for entry in entries:
            self.assertIn(f"{entry.rendered_number}. {entry.rendered_reference}", markdown)

    def test_no_internal_identifier_reaches_the_page(self):
        markdown, _ = renderer.render(self.ir, REGISTRY)
        self.assertNotIn("SRC-", markdown)
        self.assertNotIn("SEC-02-2-", markdown)
        self.assertNotIn("[E0", markdown)

    def test_render_refuses_output_that_fails_its_own_audit(self):
        bad = draft(unit("U-A-P01-S01", ("SEC-02-2-C-001", [KTS]),
                         text="Dayanım sınıfı C25/30'dur [E003]."))
        with self.assertRaises(renderer.RenderRefused):
            renderer.render(bad, REGISTRY)


class RenderedAudit(unittest.TestCase):
    def test_audit_flags_a_packet_handle(self):
        entries = renderer.build_citation_map(
            [unit("U-A-P01-S01", ("SEC-02-2-C-001", [KTS]))], REGISTRY)
        result = renderer.audit_rendered("# T\n\nBir cümle [E001].[1]\n\n## Kaynaklar\n\n1. x\n",
                                         entries)
        self.assertTrue(result["failures"])
        self.assertEqual(result["eid_leaks"], 1)

    def test_audit_flags_a_citation_number_with_no_entry(self):
        entries = renderer.build_citation_map(
            [unit("U-A-P01-S01", ("SEC-02-2-C-001", [KTS]))], REGISTRY)
        result = renderer.audit_rendered("# T\n\nBir cümle.[4]\n\n## Kaynaklar\n\n1. x\n",
                                         entries)
        self.assertTrue(any("no bibliography entry" in f for f in result["failures"]))

    def test_audit_passes_a_clean_document(self):
        entries = renderer.build_citation_map(
            [unit("U-A-P01-S01", ("SEC-02-2-C-001", [KTS]))], REGISTRY)
        result = renderer.audit_rendered("# T\n\nBir cümle.[1]\n\n## Kaynaklar\n\n1. x\n",
                                         entries)
        self.assertEqual(result["failures"], [])


class FixtureSuite(unittest.TestCase):
    def test_citation_fixture_suite_passes(self):
        fixtures = [json.loads(line) for line in
                    FIXTURES.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertGreaterEqual(len(fixtures), 50,
                                f"§115 requires at least 50 cases, found {len(fixtures)}")
        result = renderer.run_fixtures(fixtures)
        self.assertEqual(result["failed"], [])
        self.assertTrue(result["all_pass"])

    def test_fixture_suite_covers_every_mode(self):
        fixtures = [json.loads(line) for line in
                    FIXTURES.read_text(encoding="utf-8").splitlines() if line.strip()]
        modes = {f["mode"] for f in fixtures}
        self.assertEqual(modes, {"reference", "refuse", "numbering", "marker", "absent", "audit"})


if __name__ == "__main__":
    unittest.main()
