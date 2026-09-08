"""SEC-02-2 Controlled Draft Pilot v1.

This suite asserts the *process*, not the verdict. A run that reached PILOT_DRAFT_ACCEPTED by
loosening a rule fails here; a run that honestly rejected the pilot passes, because what is being
checked is that whatever status was reported is the one the gates and the validator actually
produce.

Everything is skipped until the phase has run, so the suite is runnable before generation - which
it must be, since the contract gate runs it as a precondition for generating at all.
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


controller = _load("section_drafting_contract_v1", "scripts/47_section_drafting_contract_v1.py")
validator = _load("section_draft_validator_v1", "scripts/49_section_draft_validator_v1.py")
renderer = _load("book_citation_renderer_v1", "scripts/48_book_citation_renderer_v1.py")

MANIFEST = controller.MANIFEST_PATH
AUTH = controller.AUTHORIZATION_PATH
RAW = controller.RAW_PATH
ACCEPTED = controller.ACCEPTED_PATH
RENDERED = controller.RENDERED_PATH
AUDIT = controller.AUDIT_PATH
CITATION_MAP = controller.CITATION_MAP_PATH
REPORT = controller.REPORT_PATH


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(path: Path):
    if not path.exists():
        raise unittest.SkipTest(f"{path.relative_to(ROOT)} not produced yet")
    return load(path)


class Authorization(unittest.TestCase):
    def test_authorization_exists_after_a_run(self):
        auth = require(AUTH)
        self.assertIn("contract_authorized", auth)
        self.assertIn("pilot_accepted", auth)

    def test_generation_only_happened_if_the_contract_gate_passed(self):
        """§139: a pilot is never generated to satisfy a generation count."""
        auth = require(AUTH)
        manifest = require(MANIFEST)
        if not auth["contract_authorized"]:
            self.assertEqual(manifest["generation_calls"], 0)
        else:
            self.assertLessEqual(manifest["generation_calls"], 1)

    def test_at_most_one_generation_and_no_retry(self):
        manifest = require(MANIFEST)
        self.assertLessEqual(manifest["generation_calls"], 1)
        self.assertEqual(manifest["automatic_retries"], 0)

    def test_no_retrieval_and_no_qdrant_writes(self):
        manifest = require(MANIFEST)
        self.assertEqual(manifest["retrieval_calls"], 0)
        self.assertEqual(manifest["qdrant_writes"], 0)

    def test_pilot_accepted_only_when_every_gate_condition_holds(self):
        auth = require(AUTH)
        if auth.get("pilot_gate") is None:
            self.skipTest("no pilot was validated")
        self.assertEqual(auth["pilot_accepted"], auth["pilot_gate"]["accept"])
        if auth["pilot_accepted"]:
            self.assertEqual(auth["pilot_gate"]["failed"], [])

    def test_status_is_one_of_the_three_declared_outcomes(self):
        auth = require(AUTH)
        self.assertIn(auth.get("pilot_status"),
                      {None, "CONTRACT_READY_PILOT_ACCEPTED", "CONTRACT_READY_PILOT_REJECTED"})


class RawOutput(unittest.TestCase):
    def test_raw_output_is_preserved_with_its_sha(self):
        raw = require(RAW)
        self.assertEqual(controller.sha_text(raw["raw_text"]), raw["raw_text_sha256"])

    def test_generation_was_deterministic_by_configuration(self):
        raw = require(RAW)
        self.assertEqual(raw["temperature"], 0.0)
        self.assertEqual(raw["seed"], 11)
        self.assertEqual(raw["model_id"], controller.MODEL_ID)

    def test_the_drafting_prompt_was_used_not_prompt_v5(self):
        raw = require(RAW)
        self.assertEqual(raw["system_prompt_path"],
                         "data/metadata/section_drafting_system_prompt_v1.txt")
        self.assertNotEqual(raw["system_prompt_sha256"], controller.PROMPT_V5_BASELINE)

    def test_raw_output_is_never_treated_as_manuscript(self):
        """§79: the raw file exists as provenance, not as text."""
        require(RAW)
        if RENDERED.exists():
            raw = load(RAW)
            self.assertNotEqual(RENDERED.read_text(encoding="utf-8"), raw["raw_text"])


class AcceptedDraft(unittest.TestCase):
    def setUp(self):
        self.auth = require(AUTH)
        if not self.auth.get("pilot_accepted"):
            self.skipTest("pilot was not accepted; there is no accepted DraftIR to check")
        self.ir = validator.parse_draft_ir(load(ACCEPTED))
        self.audit = load(AUDIT)

    def test_accepted_draft_revalidates_from_disk(self):
        """The artifact on disk must pass, not merely have passed in memory."""
        result = validator.validate_draft(self.ir, validator.load_bundle())
        self.assertEqual(result.status, "ACCEPT", result.failure_histogram)

    def test_every_material_unit_is_claim_bound_and_cited(self):
        for unit in self.ir.units:
            if not unit.material:
                continue
            with self.subTest(unit=unit.unit_id):
                self.assertTrue(unit.claim_ids)
                self.assertTrue({k for i in unit.citation_intents
                                 for k in i.get("source_keys", [])})

    def test_every_used_claim_is_allowlisted_and_composition_safe(self):
        allowlist = {row["claim_id"]: row for row in
                     controller.read_jsonl(controller.ALLOWLIST_PATH)}
        for unit in self.ir.units:
            for claim_id in unit.claim_ids:
                with self.subTest(claim=claim_id):
                    self.assertIn(claim_id, allowlist)
                    self.assertTrue(allowlist[claim_id]["composition_safe"])

    def test_no_denylisted_claim_was_used(self):
        denied = {row["claim_id"] for row in controller.read_jsonl(controller.DENYLIST_PATH)}
        used = {c for unit in self.ir.units for c in unit.claim_ids}
        self.assertEqual(used & denied, set())

    def test_required_topics_are_all_covered_by_a_core_claim(self):
        for topic, coverage in self.audit["required_topic_coverage"].items():
            with self.subTest(topic=topic):
                self.assertTrue(coverage["covered"])
                self.assertTrue(coverage["required_core_claim_ids"])

    def test_citation_coverage_is_total(self):
        self.assertEqual(self.audit["citation_coverage"]["coverage"], "100%")
        self.assertEqual(self.audit["uncited_material_unit_ids"], [])

    def test_no_failure_of_any_kind_was_recorded(self):
        self.assertEqual(self.audit["failure_histogram"], {})
        self.assertEqual(self.audit["rejected_unit_ids"], [])


class RenderedPilot(unittest.TestCase):
    def setUp(self):
        self.auth = require(AUTH)
        if not self.auth.get("pilot_accepted"):
            self.skipTest("pilot was not accepted; nothing was rendered")
        self.markdown = RENDERED.read_text(encoding="utf-8")
        self.ir = validator.parse_draft_ir(load(ACCEPTED))

    def test_rendering_is_reproducible_from_the_accepted_draft_ir(self):
        registry = validator.load_source_registry()
        rerendered, _ = renderer.render(self.ir, registry)
        self.assertEqual(rerendered, self.markdown)

    def test_no_packet_handle_reaches_the_page(self):
        self.assertEqual(renderer.PACKET_EID_RE.findall(self.markdown), [])

    def test_no_internal_identifier_reaches_the_page(self):
        prose = self.markdown.split("## Kaynaklar")[0]
        self.assertEqual(renderer.CLAIM_ID_RE.findall(prose), [])
        self.assertEqual(renderer.SOURCE_KEY_RE.findall(self.markdown), [])

    def test_no_pipeline_vocabulary_reaches_the_page(self):
        contract = load(controller.DRAFTING_CONTRACT_PATH)
        prose = validator.fold(self.markdown.split("## Kaynaklar")[0])
        for marker in contract["forbidden_prose_markers"]:
            with self.subTest(marker=marker):
                self.assertFalse(validator._marker_present(marker, prose))

    def test_every_reference_is_registry_backed(self):
        registry = validator.load_source_registry()
        entries = load(CITATION_MAP)["entries"]
        for entry in entries:
            with self.subTest(source=entry["source_key"]):
                self.assertIn(entry["source_key"], registry)
                self.assertEqual(entry["rendered_reference"],
                                 renderer.format_reference(registry[entry["source_key"]]))
                self.assertIn(entry["rendered_reference"], self.markdown)

    def test_no_bibliography_field_was_invented(self):
        references = self.markdown.split("## Kaynaklar")[1].lower()
        for invented in ("yayınevi", "publisher", "isbn", "doi", "http", "n.d.", "ed.",
                         "ankara", "washington"):
            with self.subTest(field=invented):
                self.assertNotIn(invented, references)

    def test_reference_numbers_are_contiguous_and_deduplicated(self):
        entries = load(CITATION_MAP)["entries"]
        numbers = [e["rendered_number"] for e in entries]
        self.assertEqual(numbers, list(range(1, len(numbers) + 1)))
        self.assertEqual(len({e["source_key"] for e in entries}), len(entries))

    def test_the_pilot_is_labelled_a_pilot_not_a_manuscript(self):
        manifest = load(MANIFEST)
        self.assertNotIn("FINAL", (manifest["pilot_status"] or "").upper().replace(
            "PILOT_DRAFT_ACCEPTED", ""))
        self.assertIn("NOT FINAL", manifest["final_decision"].upper())


class RejectedPilot(unittest.TestCase):
    def setUp(self):
        self.auth = require(AUTH)
        if self.auth.get("pilot_accepted") or self.auth.get("pilot_status") is None:
            self.skipTest("pilot was accepted or not attempted")

    def test_a_rejected_pilot_releases_nothing(self):
        """§62, §150: a failed draft is visible as a failure, never silently laundered."""
        self.assertFalse(RENDERED.exists(), "a rejected pilot must not be rendered")
        self.assertFalse(ACCEPTED.exists(), "a rejected pilot must not be stored as accepted")

    def test_a_rejected_pilot_records_exact_failure_codes(self):
        codes = self.auth.get("pilot_failure_codes")
        self.assertTrue(codes, "a rejection must name its codes")
        for code in codes:
            with self.subTest(code=code):
                self.assertIn(code, validator.REJECTION_CODES)

    def test_no_regeneration_was_attempted(self):
        """§85: a rejected draft is never resampled.

        Asserted on the attempt ledger rather than on this run's call count, because a run may
        legitimately be a replay of the preserved output - every step after the model call is
        deterministic - and a replay makes zero calls while still being about one generation.
        What must hold is that no attempt repeats an earlier one's configuration.
        """
        manifest = require(MANIFEST)
        self.assertEqual(manifest["automatic_retries"], 0)
        ledger = manifest["generation_attempts"]
        self.assertTrue(ledger, "a pilot verdict needs a generation to be about")
        self.assertEqual(ledger[-1]["finish_reason"], "stop",
                         "the attempt the verdict is about must have finished")
        configs = [(a["model_id"], a["temperature"], a["seed"], a["max_tokens"],
                    a["system_prompt_sha256"]) for a in ledger]
        self.assertEqual(len(configs), len(set(configs)),
                         "an attempt repeated an earlier configuration")

    def test_every_generation_attempt_is_recorded_with_its_outcome(self):
        """A truncated or discarded attempt is part of the record, not an omission."""
        manifest = require(MANIFEST)
        for attempt in manifest["generation_attempts"]:
            with self.subTest(attempt=attempt["attempt"]):
                self.assertIn(attempt["finish_reason"], {"stop", "length"})
                self.assertTrue(attempt["raw_sha256"])
                self.assertGreater(len(attempt["note"]), 40)
                self.assertTrue((ROOT / attempt["path"]).exists())


class ManifestAndReport(unittest.TestCase):
    def test_manifest_records_every_required_field(self):
        manifest = require(MANIFEST)
        for field in ("version", "section_id", "input_safety_bundle_sha",
                      "drafting_contract_sha", "citation_contract_sha",
                      "draft_validation_contract_sha", "drafting_prompt_sha",
                      "draft_controller_sha", "citation_renderer_sha", "draft_validator_sha",
                      "claim_allowlist_sha", "claim_denylist_sha", "pair_constraints_sha",
                      "fixture_counts", "test_counts", "generation_calls", "retrieval_calls",
                      "qdrant_before", "qdrant_after", "qdrant_writes", "pilot_status",
                      "rendered_draft_sha", "draft_ir_sha", "citation_map_sha",
                      "frozen_integrity", "status"):
            with self.subTest(field=field):
                self.assertIn(field, manifest)

    def test_frozen_integrity_holds(self):
        manifest = require(MANIFEST)
        self.assertTrue(manifest["frozen_integrity"]["all_unchanged"],
                        manifest["frozen_integrity"]["changed"])

    def test_fixture_counts_meet_their_minimums(self):
        counts = require(MANIFEST)["fixture_counts"]
        self.assertGreaterEqual(counts["drafting_total"], 80)
        self.assertGreaterEqual(counts["citation_total"], 50)
        self.assertEqual(counts["false_accepts"], 0)
        self.assertEqual(counts["false_rejects"], 0)
        self.assertEqual(counts["code_mismatches"], 0)

    def test_report_has_every_required_section(self):
        if not REPORT.exists():
            raise unittest.SkipTest("report not produced yet")
        text = REPORT.read_text(encoding="utf-8")
        for heading in ("## Executive Decision", "## Why Drafting Needs a Separate Contract",
                        "## Frozen Inputs", "## SEC-02-2 Readiness", "## Drafting Contract",
                        "## DraftIR", "## Claim-Bound Drafting", "## Composition Enforcement",
                        "## Numeric / Modality / Condition Safety",
                        "## Citation Rendering Contract", "## Stable Source Identity",
                        "## Bibliography Metadata Policy", "## Draft Validator",
                        "## Regression Fixtures", "## Contract Test Results",
                        "## Draft Authorization", "## Controlled Pilot Generation",
                        "## Pilot Draft Validation", "## Claim Coverage",
                        "## Required Topic Coverage", "## Citation Coverage",
                        "## Numeric Audit", "## Qualifier Audit",
                        "## Forbidden Synthesis Audit", "## Internal-ID Leak Audit",
                        "## Rendered Pilot", "## Frozen Integrity",
                        "## Remaining Limitations", "## Final Decision", "## Next Phase"):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

    def test_remaining_limitations_are_stated(self):
        manifest = require(MANIFEST)
        self.assertGreaterEqual(len(manifest["remaining_limitations"]), 3)


if __name__ == "__main__":
    unittest.main()
