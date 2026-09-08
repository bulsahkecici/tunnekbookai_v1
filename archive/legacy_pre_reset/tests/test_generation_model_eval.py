from __future__ import annotations

import hashlib
import importlib.util
import re
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = os.environ.get("TUNNELBOOK_GEN_LIVE") == "1"


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gen = load("generation_eval", "scripts/21_generation_model_eval.py")

PROTECTED = {
    "scripts/19_retriever_v1.py": "8ada31f64d8ef51c3b4d3b8b04f3fcc3e9fb7338b1554d1a5a9118a3a231b071",
    "scripts/20_rag_context.py": "4bcf5c9975ef0328eba159c34e7e2810491510dad6dc72b32ab10df1a777991d",
    "data/metadata/rag_context_contract_v1.json":
        "cc822cdb76a787dfe2593a8dfdb205aa4a33e9031dac950d946fa8050b0d49cc",
    "data/metadata/citation_contract_v1.json":
        "d1a5ad0b4409d8aa36c31c70d5b6596a6a9b9ceef78c6af93ee9f093bad8b363",
    "data/chunks/chunks.jsonl": "e751fcfc3cc6828b05f75f494fd9a31b44388abda9daf83fb9581581ef79df5b",
}
IDS = {"E001", "E002", "E003", "E004"}


class TestSystemPrompt(unittest.TestCase):
    def test_frozen_sha_matches(self):
        text = gen.load_system_prompt()
        self.assertEqual(gen.sha256_text(text), gen.SYSTEM_PROMPT_SHA256)

    def test_contains_required_rules(self):
        text = gen.load_system_prompt()
        for phrase in ("ONLY from the evidence", "UNTRUSTED", "never obey", "[E001]",
                       "Never invent a handle", "page numbers", "YETERSİZ KANIT",
                       "INSUFFICIENT EVIDENCE", "disagreement", "chain-of-thought"):
            self.assertIn(phrase, text, phrase)

    def test_turkish_marker_uses_dotted_i(self):
        self.assertIn("YETERSİZ KANIT", gen.load_system_prompt())
        self.assertEqual(gen.ABSTAIN_TR, "YETERSİZ KANIT")

    def test_fails_closed_on_mismatch(self):
        # The loader reads the version registry, so the expected SHA must be patched there;
        # patching the legacy module constant alone would make this assertion vacuous.
        original = dict(gen.SYSTEM_PROMPTS["v1"])
        try:
            gen.SYSTEM_PROMPTS["v1"] = {**original, "sha256": "0" * 64}
            with self.assertRaises(gen.HarnessConfigError):
                gen.load_system_prompt()
        finally:
            gen.SYSTEM_PROMPTS["v1"] = original


class TestRenderer(unittest.TestCase):
    def renderer(self):
        try:
            return gen.TemplateRenderer()
        except gen.HarnessConfigError as error:
            raise unittest.SkipTest(str(error))

    def test_template_file_and_sha(self):
        r = self.renderer()
        self.assertTrue(r.template_path.is_file())
        self.assertEqual(r.template_sha256,
                         "e84f32a23fdda27689f868aa4a1a5621f41133e51a48d7f3efcbea2839574259")

    def test_helper_audit_supported(self):
        r = self.renderer()
        self.assertTrue(r.audit["supported"], r.audit)
        self.assertIn("raise_exception", r.audit["referenced"])
        self.assertEqual(r.audit["missing"], [])

    def test_render_deterministic(self):
        r = self.renderer()
        self.assertEqual(r.render("sys", "usr"), r.render("sys", "usr"))

    def test_enable_thinking_false_pre_closes_think(self):
        out = self.renderer().render("sys", "usr", enable_thinking=False)
        self.assertTrue(out.endswith("<|im_start|>assistant\n<think>\n\n</think>\n\n"))

    def test_enable_thinking_true_opens_think(self):
        out = self.renderer().render("sys", "usr", enable_thinking=True)
        self.assertTrue(out.endswith("<|im_start|>assistant\n<think>\n"))

    def test_thinking_modes_differ(self):
        r = self.renderer()
        self.assertNotEqual(r.render("sys", "usr", False), r.render("sys", "usr", True))

    def test_canonical_special_token_layout(self):
        """Counts asserted for the frozen system+user generation structure only."""
        out = self.renderer().render("sys", "usr", enable_thinking=False)
        self.assertEqual(out.count("<|im_start|>"), 3)
        self.assertEqual(out.count("<|im_end|>"), 2)
        self.assertEqual(out.count("<think>"), 1)
        self.assertEqual(out.count("</think>"), 1)

    def test_no_duplicate_assistant_prefix(self):
        out = self.renderer().render("sys", "usr", enable_thinking=False)
        self.assertEqual(out.count("<|im_start|>assistant"), 1)


class TestTokenizer(unittest.TestCase):
    def tokenizer(self):
        try:
            return gen.GenerationTokenizer()
        except gen.HarnessConfigError as error:
            raise unittest.SkipTest(str(error))

    def test_tokenizer_sha(self):
        self.assertEqual(self.tokenizer().tokenizer_sha256,
                         "87a7830d63fcf43bf241c3c5242e96e62dd3fdc29224ca26fed8ea333db72de4")

    def test_count_is_deterministic_and_positive(self):
        t = self.tokenizer()
        self.assertEqual(t.count("tünel havalandırması"), t.count("tünel havalandırması"))
        self.assertGreater(t.count("shotcrete"), 0)


class TestEndpointGuard(unittest.TestCase):
    def test_default_endpoint_is_raw_completions(self):
        self.assertEqual(gen.GenerationConfig().endpoint, "/v1/completions")

    def test_chat_endpoint_rejected(self):
        with self.assertRaises(gen.HarnessConfigError):
            gen.GenerationConfig(endpoint="/v1/chat/completions")

    def test_chat_endpoint_rejected_with_base(self):
        with self.assertRaises(gen.HarnessConfigError):
            gen.GenerationConfig(endpoint="http://127.0.0.1:1234/v1/chat/completions")

    def test_other_endpoint_rejected(self):
        with self.assertRaises(gen.HarnessConfigError):
            gen.GenerationConfig(endpoint="/v1/responses")

    def test_config_hash_deterministic_and_sensitive(self):
        a = gen.GenerationConfig(tokenizer_sha256="x", template_sha256="y")
        b = gen.GenerationConfig(tokenizer_sha256="x", template_sha256="y")
        c = gen.GenerationConfig(tokenizer_sha256="x", template_sha256="z")
        self.assertEqual(a.config_hash(), b.config_hash())
        self.assertNotEqual(a.config_hash(), c.config_hash())

    def test_stop_policy(self):
        self.assertEqual(gen.GenerationConfig().stop, ("<|im_end|>", "<|im_start|>"))


class TestCitationValidatorValid(unittest.TestCase):
    def v(self, answer):
        return gen.validate_citations(answer, IDS)

    def test_single_valid_handle_not_malformed(self):
        r = self.v("Shotcrete is primary support [E001].")
        self.assertEqual(r["valid_handles"], ["E001"])
        self.assertEqual(r["malformed_citations"], [])
        self.assertEqual(r["unknown_handles"], [])

    def test_multiple_valid_handles(self):
        r = self.v("Support combines shotcrete and bolts [E001][E004].")
        self.assertEqual(r["valid_handles"], ["E001", "E004"])
        self.assertEqual(r["malformed_citations"], [])

    def test_duplicate_handles_not_malformed(self):
        r = self.v("Stated twice [E001][E001].")
        self.assertEqual(r["valid_handles"], ["E001"])
        self.assertEqual(r["syntactically_valid_handle_occurrences"], 2)
        self.assertEqual(r["syntactically_valid_handles"], ["E001"])
        self.assertEqual(r["malformed_citations"], [])

    def test_unknown_handle_is_valid_syntax_but_not_packet_valid(self):
        r = self.v("Claim [E009].")
        self.assertEqual(r["syntactically_valid_handles"], ["E009"])
        self.assertEqual(r["valid_handles"], [],
                         "an unknown handle must not be reported as packet-valid")
        self.assertEqual(r["unknown_handles"], ["E009"])
        self.assertEqual(r["malformed_citations"], [],
                         "a syntactically valid but unknown handle is not malformed")


class TestCitationValidatorMalformed(unittest.TestCase):
    def v(self, answer):
        return gen.validate_citations(answer, IDS)

    def test_malformed_variants_detected(self):
        for bad in ("[E1]", "[E01]", "[E0001]", "[ E001]", "[E001 ]", "[ E001 ]",
                    "[e001]", "[E 001]"):
            r = self.v(f"Claim {bad} here.")
            self.assertTrue(r["malformed_citations"], f"{bad} should be malformed")
            self.assertEqual(r["valid_handles"], [], f"{bad} must not count as valid")

    def test_bare_handle_detected(self):
        r = self.v("As shown in E001 the support works.")
        self.assertIn("E001", r["malformed_citations"])
        self.assertEqual(r["valid_handles"], [])

    def test_unclosed_bracket_detected(self):
        self.assertTrue(self.v("Claim [E001 without close")["malformed_citations"])

    def test_valid_and_malformed_coexist(self):
        r = self.v("Good [E001] and bad [E1].")
        self.assertEqual(r["valid_handles"], ["E001"])
        self.assertIn("[E1]", r["malformed_citations"])



class TestValidatorV12Semantics(unittest.TestCase):
    """Syntax validity and reference validity are orthogonal and must never be conflated."""

    PACKET = {"E001", "E002"}

    def test_A_known_handle(self):
        r = gen.validate_citations("Claim [E001].", self.PACKET)
        self.assertEqual(r["valid_handles"], ["E001"])
        self.assertEqual(r["unknown_handles"], [])
        self.assertEqual(r["excluded_handle_citations"], [])

    def test_B_unknown_handle_not_valid_not_malformed(self):
        r = gen.validate_citations("Claim [E009].", self.PACKET)
        self.assertEqual(r["syntactically_valid_handles"], ["E009"])
        self.assertEqual(r["valid_handles"], [])
        self.assertEqual(r["unknown_handles"], ["E009"])
        self.assertEqual(r["malformed_citations"], [])

    def test_C_excluded_handle_distinguished(self):
        r = gen.validate_citations("Claim [E003].", self.PACKET,
                                   excluded_evidence_ids={"E003"})
        self.assertEqual(r["valid_handles"], [])
        self.assertEqual(r["unknown_handles"], [])
        self.assertEqual(r["excluded_handle_citations"], ["E003"])

    def test_D_three_way_split(self):
        r = gen.validate_citations("Claim [E001][E003][E999].", self.PACKET,
                                   excluded_evidence_ids={"E003"})
        self.assertEqual(r["syntactically_valid_handles"], ["E001", "E003", "E999"])
        self.assertEqual(r["valid_handles"], ["E001"])
        self.assertEqual(r["excluded_handle_citations"], ["E003"])
        self.assertEqual(r["unknown_handles"], ["E999"])
        self.assertEqual(r["malformed_citations"], [])

    def test_E_malformed_only(self):
        r = gen.validate_citations("Claim [E01].", self.PACKET)
        self.assertTrue(r["malformed_citations"])
        self.assertEqual(r["syntactically_valid_handles"], [])
        self.assertEqual(r["valid_handles"], [])
        self.assertEqual(r["unknown_handles"], [])

    def test_F_duplicate_occurrences(self):
        r = gen.validate_citations("[E001][E001]", self.PACKET)
        self.assertEqual(r["syntactically_valid_handle_occurrences"], 2)
        self.assertEqual(r["valid_handles"], ["E001"])
        self.assertEqual(r["syntactically_valid_handles"], ["E001"])

    def test_G_buckets_pairwise_disjoint(self):
        answers = ["Claim [E001][E003][E999].", "[E001][E001][E002]", "[E009] and [E003]",
                   "No citations here.", "[E01] [E001] [E999]"]
        for answer in answers:
            r = gen.validate_citations(answer, self.PACKET, excluded_evidence_ids={"E003", "E004"})
            valid = set(r["valid_handles"])
            unknown = set(r["unknown_handles"])
            excluded = set(r["excluded_handle_citations"])
            self.assertEqual(valid & unknown, set(), answer)
            self.assertEqual(valid & excluded, set(), answer)
            self.assertEqual(unknown & excluded, set(), answer)
            self.assertEqual(valid | unknown | excluded,
                             set(r["syntactically_valid_handles"]),
                             f"every canonical handle must land in exactly one bucket: {answer}")

    def test_overlapping_packet_and_excluded_rejected(self):
        with self.assertRaises(ValueError):
            gen.validate_citations("[E001]", {"E001"}, excluded_evidence_ids={"E001"})

    def test_excluded_defaults_to_empty(self):
        r = gen.validate_citations("Claim [E003].", self.PACKET)
        self.assertEqual(r["excluded_handle_citations"], [])
        self.assertEqual(r["unknown_handles"], ["E003"],
                         "without excluded ids an unrendered handle is simply unknown")

    def test_validator_version_bumped(self):
        self.assertEqual(gen.VALIDATOR_VERSION, "citation-validator-v1.2")
        self.assertEqual(gen.validate_citations("x", set())["validator_version"],
                         "citation-validator-v1.2")

    def test_result_schema_carries_new_fields(self):
        for field in ("syntactically_valid_handles", "syntactically_valid_handle_occurrences",
                      "excluded_handle_citations", "valid_handles", "unknown_handles",
                      "malformed_citations"):
            self.assertIn(field, gen.RESULT_FIELDS)
        self.assertNotIn("valid_handle_occurrences", gen.RESULT_FIELDS,
                         "ambiguous legacy name must not persist in the schema")


class TestContextV1ExcludedRepresentability(unittest.TestCase):
    """Context v1 assigns Evidence IDs only to selected items, so excluded ones have none."""

    def test_excluded_items_carry_no_evidence_id(self):
        source = (ROOT / "scripts/20_rag_context.py").read_text(encoding="utf-8")
        self.assertIn('excluded.append({"chunk_id"', source)
        for block in re.findall(r"excluded\.append\(\{[^}]*\}", source):
            self.assertNotIn("evidence_id", block,
                             "Context v1 excluded_items must not claim an evidence_id")

    def test_evidence_ids_assigned_only_to_selected(self):
        source = (ROOT / "scripts/20_rag_context.py").read_text(encoding="utf-8")
        self.assertIn('f"E{len(selected) + 1:03d}"', source)

    def test_real_packet_excluded_items_have_no_ids(self):
        path = ROOT / "data/evaluation/rag_context_smoke_v1.jsonl"
        if not path.is_file():
            self.skipTest("smoke packets not generated")
        rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertTrue(any(r["excluded"] > 0 for r in rows), "need a packet with exclusions")
        for row in rows:
            for item in row["evidence"]:
                self.assertRegex(item["evidence_id"], r"^E\d{3}$")


class TestLeakDetection(unittest.TestCase):
    def v(self, answer):
        return gen.validate_citations(answer, IDS)

    def leaks(self, answer):
        r = self.v(answer)
        return r["doc_leaks"] + r["page_leaks"] + r["slide_leaks"] + r["path_leaks"]

    def test_engineering_values_not_flagged(self):
        for text in ("Shotcrete thickness is 15 cm [E001].", "Strength 25 MPa [E001].",
                     "RMR 60 indicates fair rock [E001].", "GSI 45 measured [E001].",
                     "Bolt spacing 2 m [E001].", "Per EN 1997 [E001].",
                     "ASTM D1586 applies [E001].", "Built in 2024 [E001].",
                     "Section 351.08.07 requirement [E001].", "Concrete C30/37 [E001].",
                     "Aggregate 10–20 mm [E001]."):
            self.assertEqual(self.leaks(text), [], text)

    def test_page_leaks_flagged(self):
        for text in ("See page 15.", "Bkz. s. 15.", "ss. 15-17 arası.", "ss. 15–17 arası."):
            self.assertTrue(self.leaks(text), text)

    def test_slide_leaks_flagged(self):
        for text in ("Slayt 12 gösteriyor.", "slide 12 shows this."):
            self.assertTrue(self.leaks(text), text)

    def test_doc_leak_flagged(self):
        self.assertIn("DOC000123", self.v("As stated in DOC000123.")["doc_leaks"])

    def test_path_and_filename_leaks_flagged(self):
        self.assertTrue(self.v("From tunnel_report.pdf.")["path_leaks"])
        self.assertTrue(self.v("See /Users/x/corpus/a.pdf.")["path_leaks"])

    def test_path_leak_punctuation_normalised(self):
        leaks = self.v("See /Users/x/corpus/a.pdf.")["path_leaks"]
        self.assertTrue(all(not l.endswith(".") for l in leaks), leaks)

    def test_template_leak_flagged(self):
        r = self.v("Answer <|im_end|> and <think>hidden</think>")
        self.assertTrue(r["template_leaks"])


class TestAbstention(unittest.TestCase):
    def test_turkish_marker_at_start(self):
        r = gen.validate_abstention("YETERSİZ KANIT — paket 2027 bütçesini içermiyor.")
        self.assertEqual(r["abstention_marker"], "YETERSİZ KANIT")
        self.assertTrue(r["abstention_at_start"])

    def test_english_marker_at_start(self):
        r = gen.validate_abstention("INSUFFICIENT EVIDENCE — no figure is given.")
        self.assertEqual(r["abstention_marker"], "INSUFFICIENT EVIDENCE")
        self.assertTrue(r["abstention_at_start"])

    def test_leading_whitespace_allowed(self):
        self.assertTrue(gen.validate_abstention("\n  INSUFFICIENT EVIDENCE ...")["abstention_at_start"])

    def test_marker_midway_is_not_abstention(self):
        r = gen.validate_abstention("The value is 5 cm [E001]. INSUFFICIENT EVIDENCE for the rest.")
        self.assertIsNone(r["abstention_marker"])
        self.assertFalse(r["abstention_at_start"])
        self.assertTrue(r["abstention_marker_present_anywhere"])

    def test_normal_answer_has_no_marker(self):
        self.assertIsNone(gen.validate_abstention("Shotcrete is support [E001].")["abstention_marker"])


class TestResultSchemaAndCheckpoint(unittest.TestCase):
    def identity_args(self, **over):
        base = dict(query_id="Q001", benchmark_sha="b", system_prompt_sha="s", model_id="m",
                    tokenizer_sha="t", template_sha="tpl", generation_config_hash="g",
                    context_packet_sha="c")
        base.update(over)
        return base

    def test_schema_has_required_fields(self):
        for field in ("query_id", "prompt_tokens_local", "prompt_tokens_api", "prompt_token_delta",
                      "raw_answer", "valid_handles", "unknown_handles", "malformed_citations",
                      "abstention_marker", "latency_seconds", "finish_reason"):
            self.assertIn(field, gen.RESULT_FIELDS)

    def test_schema_persists_no_reasoning(self):
        for forbidden in gen.FORBIDDEN_RESULT_KEYS:
            self.assertNotIn(forbidden, gen.RESULT_FIELDS)
        for field in gen.RESULT_FIELDS:
            for forbidden in ("reasoning", "chain_of_thought", "cot", "hidden"):
                self.assertNotIn(forbidden, field.lower())

    def test_identity_deterministic(self):
        a = gen.checkpoint_identity(**self.identity_args())
        b = gen.checkpoint_identity(**self.identity_args())
        self.assertEqual(a, b)

    def test_identity_changes_with_each_field(self):
        base = gen.checkpoint_identity(**self.identity_args())
        for field in ("benchmark_sha", "system_prompt_sha", "model_id", "tokenizer_sha",
                      "template_sha", "generation_config_hash", "context_packet_sha"):
            other = gen.checkpoint_identity(**self.identity_args(**{field: "CHANGED"}))
            self.assertNotEqual(base, other, field)

    def test_resume_accepts_matching_config(self):
        expected = self.identity_args()
        self.assertTrue(gen.is_resumable(dict(expected), expected))

    def test_resume_rejects_stale_system_prompt(self):
        expected = self.identity_args()
        stored = dict(expected, system_prompt_sha="OLD")
        self.assertFalse(gen.is_resumable(stored, expected))

    def test_resume_rejects_stale_template_and_context(self):
        expected = self.identity_args()
        for field in ("template_sha", "context_packet_sha", "generation_config_hash"):
            self.assertFalse(gen.is_resumable(dict(expected, **{field: "OLD"}), expected), field)

    def test_incremental_write_and_recovery(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.jsonl"
            gen.atomic_append_jsonl(path, {"query_id": "Q001", "raw_answer": "a"})
            gen.atomic_append_jsonl(path, {"query_id": "Q002", "raw_answer": "b"})
            with path.open("a", encoding="utf-8") as handle:
                handle.write('{"query_id": "Q003", "raw')      # torn line
            loaded = gen.load_checkpoints(path)
            self.assertEqual(sorted(loaded), ["Q001", "Q002"], "torn line must be skipped")


class TestCliAndPreflight(unittest.TestCase):
    def test_benchmark_commands_fail_explicitly(self):
        import subprocess
        result = subprocess.run([sys.executable, str(ROOT / "scripts/21_generation_model_eval.py"),
                                 "--pilot"], capture_output=True, text=True, cwd=str(ROOT))
        self.assertEqual(result.returncode, 2)
        self.assertIn("benchmark_not_built", result.stdout)

    def test_preflight_reports_identity(self):
        try:
            report = gen.preflight()
        except gen.HarnessConfigError as error:
            raise unittest.SkipTest(str(error))
        self.assertTrue(report["system_prompt_verified"])
        self.assertTrue(report["pre_closed_think_block"])
        self.assertEqual(report["endpoint"], "/v1/completions")
        self.assertEqual(report["benchmark_status"], "NOT BUILT")
        self.assertEqual(report["thinking_mode"], "non_thinking_via_local_template")


class TestProtectedIntegrity(unittest.TestCase):
    def test_upstream_frozen_layers_unchanged(self):
        for rel, expected in PROTECTED.items():
            actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, rel)


@unittest.skipUnless(LIVE, "set TUNNELBOOK_GEN_LIVE=1 for a live smoke generation")
class TestLiveSmoke(unittest.TestCase):
    def test_raw_completion_smoke(self):
        renderer = gen.TemplateRenderer()
        tokenizer = gen.GenerationTokenizer()
        config = gen.GenerationConfig(tokenizer_sha256=tokenizer.tokenizer_sha256,
                                      template_sha256=renderer.template_sha256)
        evidence = ("<BEGIN_UNTRUSTED_EVIDENCE E001 b=abc>\nShotcrete is sprayed concrete used as "
                    "primary tunnel support.\n<END_UNTRUSTED_EVIDENCE E001 b=abc>")
        prompt = renderer.render(gen.load_system_prompt(),
                                 f"{evidence}\n\nQUESTION: What is shotcrete used for?")
        out = gen.complete(prompt, config, max_tokens=256)
        self.assertTrue(out["text"].strip())
        checks = gen.validate_citations(out["text"], {"E001"})
        self.assertEqual(checks["template_leaks"], [])
        self.assertEqual(checks["unknown_handles"], [])
        self.assertEqual(tokenizer.count(prompt), out["usage"]["prompt_tokens"])


class TestPromptBudgetGuard(unittest.TestCase):
    def test_exact_fit_passes(self):
        headroom = gen.validate_prompt_budget(71936 - 1536 - 3596, 1536, 3596, 71936)
        self.assertEqual(headroom, 0)

    def test_one_token_over_raises(self):
        with self.assertRaises(gen.PromptBudgetExceeded) as ctx:
            gen.validate_prompt_budget(71936 - 1536 - 3596 + 1, 1536, 3596, 71936)
        self.assertEqual(ctx.exception.total - ctx.exception.loaded_context_length, 1)

    def test_exception_carries_diagnostics(self):
        with self.assertRaises(gen.PromptBudgetExceeded) as ctx:
            gen.validate_prompt_budget(70000, 2048, 3596, 71936)
        error = ctx.exception
        self.assertEqual(error.rendered_prompt_tokens, 70000)
        self.assertEqual(error.max_tokens, 2048)
        self.assertEqual(error.safety_margin, 3596)
        self.assertEqual(error.loaded_context_length, 71936)

    def test_non_positive_reserve_rejected(self):
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                gen.validate_prompt_budget(100, bad)

    def test_negative_margin_rejected(self):
        with self.assertRaises(ValueError):
            gen.validate_prompt_budget(100, 512, -1)

    def test_different_loaded_context_respected(self):
        gen.validate_prompt_budget(1000, 512, 100, 8192)
        with self.assertRaises(gen.PromptBudgetExceeded):
            gen.validate_prompt_budget(8000, 512, 100, 8192)

    def test_candidate_loaded_context_default(self):
        self.assertEqual(gen.LOADED_CONTEXT_LENGTH, 71936)
        self.assertEqual(gen.SAFETY_MARGIN, 3596)


class TestCompletionClassifier(unittest.TestCase):
    def checks(self, **over):
        base = {"valid_handles": ["E001"], "unknown_handles": [], "malformed_citations": [],
                "doc_leaks": [], "page_leaks": [], "slide_leaks": [], "path_leaks": [],
                "template_leaks": [], "abstention_at_start": False}
        base.update(over)
        return base

    def test_complete(self):
        self.assertEqual(gen.classify_completion("ans [E001]", "stop", self.checks(), False), "complete")

    def test_truncated(self):
        self.assertEqual(gen.classify_completion("ans", "length", self.checks(), False), "truncated")

    def test_empty(self):
        self.assertEqual(gen.classify_completion("  ", "stop", self.checks(), False), "empty")

    def test_unknown_handle_is_invalid_citation(self):
        self.assertEqual(gen.classify_completion("a [E9]", "stop",
                         self.checks(unknown_handles=["E009"]), False), "invalid_citation")

    def test_coordinate_leak_is_invalid_citation(self):
        self.assertEqual(gen.classify_completion("page 5", "stop",
                         self.checks(page_leaks=["page 5"]), False), "invalid_citation")

    def test_must_abstain_without_marker_is_wrong_abstention(self):
        self.assertEqual(gen.classify_completion("The value is 5 [E001]", "stop",
                         self.checks(), True), "wrong_abstention")

    def test_must_abstain_with_marker_is_complete(self):
        self.assertEqual(gen.classify_completion("YETERSİZ KANIT ...", "stop",
                         self.checks(abstention_at_start=True), True), "complete")

    def test_unexpected_abstention_surfaced(self):
        """Abstaining on an answerable query must not score as complete."""
        self.assertEqual(gen.classify_completion("YETERSİZ KANIT ...", "stop",
                         self.checks(abstention_at_start=True), False), "unexpected_abstention")

    def test_finish_reason_stop_is_not_sufficient(self):
        self.assertNotEqual(gen.classify_completion("x", "stop",
                            self.checks(template_leaks=["<think>"]), False), "complete")


class TestRun2Artifacts(unittest.TestCase):
    def rows(self):
        path = ROOT / "data/evaluation/generation_reserve_pilot_v1.jsonl"
        if not path.is_file():
            self.skipTest("pilot not run")
        return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]

    def test_pilot_row_count_and_schema(self):
        rows = self.rows()
        self.assertEqual(len(rows), 25)
        for field in ("pilot_query_id", "max_tokens", "prompt_tokens_local", "prompt_tokens_api",
                      "prompt_token_delta", "completion_state", "raw_answer", "valid_handles"):
            self.assertIn(field, rows[0])

    def test_pilot_covers_five_queries_and_five_levels(self):
        rows = self.rows()
        self.assertEqual(sorted({r["pilot_query_id"] for r in rows}),
                         ["P01", "P02", "P03", "P04", "P05"])
        self.assertEqual(sorted({r["max_tokens"] for r in rows}), [512, 768, 1024, 1536, 2048])

    def test_prompt_local_equals_api_on_every_row(self):
        for row in self.rows():
            self.assertEqual(row["prompt_tokens_local"], row["prompt_tokens_api"], row["pilot_query_id"])
            self.assertEqual(row["prompt_token_delta"], 0)

    def test_no_reasoning_persisted(self):
        for row in self.rows():
            for key in row:
                for forbidden in ("reasoning", "chain_of_thought", "cot", "hidden"):
                    self.assertNotIn(forbidden, key.lower())

    def test_no_template_leaks_in_any_answer(self):
        for row in self.rows():
            self.assertEqual(row["template_leaks"], [], row["pilot_query_id"])

    def test_identity_constant_across_pilot(self):
        rows = self.rows()
        self.assertEqual({r["system_prompt_sha"] for r in rows}, {gen.SYSTEM_PROMPT_SHA256})
        self.assertEqual(len({r["tokenizer_sha"] for r in rows}), 1)
        self.assertEqual(len({r["template_sha"] for r in rows}), 1)
        self.assertEqual(len({r["generation_config_hash"] for r in rows}), 1)

    def test_must_abstain_case_abstained_at_every_level(self):
        for row in self.rows():
            if row["pilot_query_id"] == "P05":
                self.assertTrue(row["abstention_at_start"], row["max_tokens"])

    def test_prompt_accounting_artifact(self):
        path = ROOT / "data/evaluation/generation_prompt_accounting_v1.json"
        if not path.is_file():
            self.skipTest("accounting not written")
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["summary"]["max_abs_api_local_delta"], 0)
        self.assertIn("template_overhead_policy", data["summary"])
        for qid in ("P01", "P02", "P03", "P04", "P05"):
            self.assertIn(qid, data["per_query"])

    def test_candidate_descriptor_run2_fields(self):
        path = ROOT / "data/metadata/generation_candidate_v1.json"
        if not path.is_file():
            self.skipTest("descriptor missing")
        c = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(c["status"], "runtime_contract_closed_benchmark_pending")
        self.assertEqual(c["actual_loaded_context"], 71936)
        self.assertEqual(c["query_allowance_status"], "pending_72_query_benchmark")
        self.assertEqual(c["benchmark"], "not_built")
        # Run 3 split the single "working reserve" into an explicit non-truncating minimum and a
        # full-contract minimum, so the old ambiguous field name is gone by design.
        self.assertNotIn("measured_minimum_working_reserve", c)
        for field in ("measured_minimum_nontruncating_reserve",
                      "measured_minimum_full_contract_reserve", "selected_safe_output_reserve",
                      "maximum_prompt_tokens_operational", "rag_context_budget_planning_value",
                      "template_overhead_policy", "prompt_accounting_max_delta"):
            self.assertIn(field, c)
        self.assertEqual(c["validator_version"], gen.VALIDATOR_VERSION,
                         "descriptor must not carry a stale validator version")
        self.assertEqual(c["generation_endpoint"], gen.COMPLETIONS_ENDPOINT)
        self.assertEqual(c["maximum_prompt_tokens_operational"],
                         71936 - c["selected_safe_output_reserve"] - c["safety_margin"])


V3_SHA = "d3cadd465e2733d0cdd451d146407f28f80cefc784b432088fc20ecf7526dc74"
V4_SHA = "5950bafff10d82c2db3e0fe1999f25bd6b705924946737187a7fdde017dba072"
V5_SHA = "9bae1362a228b84dd7e3867babc352527755902b9078dd10648819bd396e4085"
PROMPT_SHAS = {
    "v1": "303691ec02501fa4637a2618ceb90f21bba4c558e41124325ed8915ef7a64817",
    "v2": "0063b9bcbe2d93325b03ae18c6005feb0b9a9571d93132607b740ad794f005cc",
    "v3": V3_SHA,
    "v4": V4_SHA,
    "v5": V5_SHA,
}


class TestVersionedSystemPrompts(unittest.TestCase):
    def test_all_three_versions_registered_and_frozen(self):
        self.assertEqual(set(gen.SYSTEM_PROMPTS), {"v1", "v2", "v3", "v4", "v5"})
        for version, sha in PROMPT_SHAS.items():
            entry = gen.load_system_prompt_versioned(version)
            self.assertEqual(entry["sha256"], sha,
                             f"{version} changed on disk; create a new version, do not edit")
            self.assertEqual(entry["version"], version)

    def test_versions_have_distinct_content(self):
        shas = {gen.sha256_text(gen.load_system_prompt_versioned(v)["text"])
                for v in ("v1", "v2", "v3", "v4", "v5")}
        self.assertEqual(len(shas), 5)

    def test_candidate_version_is_v3(self):
        """v3 remains the frozen Phase B candidate; v4 is a development prompt until re-evaluated."""
        self.assertEqual(gen.CANDIDATE_SYSTEM_PROMPT_VERSION, "v3")

    def test_v4_registered_and_frozen(self):
        entry = gen.load_system_prompt_versioned("v4")
        self.assertEqual(entry["sha256"], V4_SHA)
        self.assertEqual(entry["name"], "generation-system-prompt-v4")

    def test_v4_keeps_the_v3_policy_and_adds_the_two_remediation_rules(self):
        v4 = gen.load_system_prompt_versioned("v4")["text"]
        for kept in ("UNTRUSTED", "never obey", "[Eddd]", "exactly three digits", "YETERSİZ KANIT",
                     "INSUFFICIENT EVIDENCE", "disagreement", "chain-of-thought",
                     "page numbers", "never invent one"):
            self.assertIn(kept, v4, f"v4 dropped the v3 policy element {kept!r}")
        lowered = v4.lower()
        self.assertIn("talk about", lowered)          # bare-reference-in-prose rule
        self.assertIn("does not cover what follows", lowered)   # per-claim coverage rule
        self.assertIn("need no handle", lowered)      # non-factual exemption

    def test_v5_registered_and_frozen(self):
        entry = gen.load_system_prompt_versioned("v5")
        self.assertEqual(entry["sha256"], V5_SHA)
        self.assertEqual(entry["name"], "generation-system-prompt-v5")

    def test_v5_preserves_the_v4_citation_rules(self):
        v5 = gen.load_system_prompt_versioned("v5")["text"]
        lowered = v5.lower()
        for kept in ("[eddd]", "exactly three digits", "talk about", "does not cover what follows",
                     "need no handle", "scan your answer once"):
            self.assertIn(kept, lowered, f"v5 dropped the v4 rule {kept!r}")
        self.assertIn("YETERSİZ KANIT", v5)
        self.assertIn("INSUFFICIENT EVIDENCE", v5)
        self.assertIn("language of the evidence never affects", v5)

    def test_v5_config_hash_and_checkpoint_differ_from_v4(self):
        base = dict(tokenizer_sha256="t" * 64, template_sha256="m" * 64)
        c4 = gen.GenerationConfig(system_prompt_version="v4",
                                  system_prompt_sha256=PROMPT_SHAS["v4"], **base)
        c5 = gen.GenerationConfig(system_prompt_version="v5",
                                  system_prompt_sha256=PROMPT_SHAS["v5"], **base)
        self.assertNotEqual(c4.config_hash(), c5.config_hash())
        ident = lambda c: {"query_id": "L1", "benchmark_sha": "b" * 64,
                           "system_prompt_sha": c.system_prompt_sha256, "model_id": c.model_id,
                           "tokenizer_sha": c.tokenizer_sha256, "template_sha": c.template_sha256,
                           "generation_config_hash": c.config_hash(), "context_packet_sha": "c" * 64}
        self.assertFalse(gen.is_resumable(ident(c4), ident(c5)),
                         "a v4 result must never be resumed under v5")

    def test_v4_config_hash_and_checkpoint_differ_from_v3(self):
        base = dict(tokenizer_sha256="t" * 64, template_sha256="m" * 64)
        c3 = gen.GenerationConfig(system_prompt_version="v3",
                                  system_prompt_sha256=PROMPT_SHAS["v3"], **base)
        c4 = gen.GenerationConfig(system_prompt_version="v4",
                                  system_prompt_sha256=PROMPT_SHAS["v4"], **base)
        self.assertNotEqual(c3.config_hash(), c4.config_hash())
        ident = lambda c: {"query_id": "D1", "benchmark_sha": "b" * 64,
                           "system_prompt_sha": c.system_prompt_sha256, "model_id": c.model_id,
                           "tokenizer_sha": c.tokenizer_sha256, "template_sha": c.template_sha256,
                           "generation_config_hash": c.config_hash(), "context_packet_sha": "c" * 64}
        self.assertFalse(gen.is_resumable(ident(c3), ident(c4)),
                         "a v3 result must never be resumed under v4")

    def test_unknown_version_fails_closed(self):
        with self.assertRaises(gen.HarnessConfigError) as ctx:
            gen.load_system_prompt_versioned("v99")
        self.assertIn("unknown system prompt version", str(ctx.exception))

    def test_sha_mismatch_fails_closed_without_fallback(self):
        import tempfile
        original = gen.SYSTEM_PROMPTS
        with tempfile.TemporaryDirectory() as tmp:
            tampered = Path(tmp) / "tampered.txt"
            tampered.write_text("cite however you like\n", encoding="utf-8")
            try:
                gen.SYSTEM_PROMPTS = {**original,
                                      "v3": {**original["v3"], "path": tampered}}
                with self.assertRaises(gen.HarnessConfigError) as ctx:
                    gen.load_system_prompt_versioned("v3")
                self.assertIn("SHA mismatch", str(ctx.exception))
            finally:
                gen.SYSTEM_PROMPTS = original

    def test_missing_file_fails_closed(self):
        original = gen.SYSTEM_PROMPTS
        try:
            gen.SYSTEM_PROMPTS = {**original,
                                  "v3": {**original["v3"], "path": ROOT / "no_such_prompt.txt"}}
            with self.assertRaises(gen.HarnessConfigError):
                gen.load_system_prompt_versioned("v3")
        finally:
            gen.SYSTEM_PROMPTS = original

    def test_v3_is_a_general_grammar_not_an_enumerated_invalid_list(self):
        """v3 must be a compact rule, not an extension of v2's INVALID catalogue."""
        text = gen.load_system_prompt_versioned("v3")["text"]
        self.assertIn("[Eddd]", text)
        self.assertIn("exactly three digits", text)
        lowered = text.lower()
        self.assertIn("ranged", lowered)          # ranges forbidden as a class
        self.assertIn("do not list", lowered)     # no unused-evidence inventory
        self.assertIn("enumerate", lowered)

    def test_v3_is_shorter_than_v2(self):
        if os.environ.get("TUNNELBOOK_GEN_TOKENIZER") == "0":
            self.skipTest("tokenizer disabled")
        tokenizer = gen.GenerationTokenizer()
        v2 = tokenizer.count(gen.load_system_prompt_versioned("v2")["text"])
        v3 = tokenizer.count(gen.load_system_prompt_versioned("v3")["text"])
        self.assertLess(v3, v2, f"v3={v3} must be below v2={v2}")


class TestPromptVersionInConfigIdentity(unittest.TestCase):
    def _config(self, version):
        entry = gen.load_system_prompt_versioned(version)
        return gen.GenerationConfig(tokenizer_sha256="t" * 64, template_sha256="m" * 64,
                                    system_prompt_version=version,
                                    system_prompt_sha256=entry["sha256"])

    def test_v2_and_v3_have_different_config_hashes(self):
        self.assertNotEqual(self._config("v2").config_hash(), self._config("v3").config_hash())

    def _identity(self, version):
        config = self._config(version)
        return {"query_id": "P01", "benchmark_sha": "b" * 64,
                "system_prompt_sha": config.system_prompt_sha256, "model_id": config.model_id,
                "tokenizer_sha": config.tokenizer_sha256, "template_sha": config.template_sha256,
                "generation_config_hash": config.config_hash(), "context_packet_sha": "c" * 64}

    def test_checkpoint_cannot_resume_v2_rows_under_v3(self):
        """A v2 result must never be replayed as a v3 result."""
        stale, current = self._identity("v2"), self._identity("v3")
        self.assertFalse(gen.is_resumable(stale, current))
        self.assertNotEqual(gen.checkpoint_identity(**stale), gen.checkpoint_identity(**current))

    def test_identical_v3_identity_is_resumable(self):
        self.assertTrue(gen.is_resumable(self._identity("v3"), self._identity("v3")))


class TestCompressedHandleFormsRejected(unittest.TestCase):
    """Validator v1.2 must reject every compressed form without being relaxed."""

    IDS = {"E001", "E003", "E004", "E010"}

    def test_malformed_forms(self):
        cases = [
            "Other evidence (E003-E010) is inventory.",      # observed v2 failure, ASCII hyphen
            "Other evidence (E003\u2013E010) is inventory.",  # en dash
            "Other evidence [E003-E010] is inventory.",      # bracketed range
            "Other evidence [E003/E010] is inventory.",      # slashed
            "Other evidence E003, E004 is inventory.",       # bare comma list
            "Kalinlik E001'de verilmistir.",                 # bare + Turkish suffix
        ]
        for text in cases:
            with self.subTest(text=text):
                report = gen.validate_citations(text, self.IDS)
                self.assertTrue(report["malformed_citations"],
                                f"validator accepted an illegal handle form: {text}")

    def test_legal_forms_stay_valid(self):
        for text in ("Thickness is 15 cm [E003][E004].",
                     "Kalinlik [E003]'de verilmistir.",
                     "See [E001] and [E010]."):
            with self.subTest(text=text):
                report = gen.validate_citations(text, self.IDS)
                self.assertEqual(report["malformed_citations"], [])
                self.assertTrue(report["syntactically_valid_handles"])
                self.assertEqual(report["unknown_handles"], [])


class TestV3PilotArtifacts(unittest.TestCase):
    ACCT = ROOT / "data/evaluation/generation_prompt_accounting_v3.json"
    PILOT = ROOT / "data/evaluation/generation_reserve_pilot_v3.jsonl"
    MANIFEST = ROOT / "data/evaluation/generation_reserve_pilot_v3_manifest.json"

    def setUp(self):
        for path in (self.ACCT, self.PILOT, self.MANIFEST):
            if not path.is_file():
                self.skipTest(f"{path.name} not produced yet")
        self.acct = json.loads(self.ACCT.read_text(encoding="utf-8"))
        self.rows = [json.loads(line) for line in
                     self.PILOT.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.manifest = json.loads(self.MANIFEST.read_text(encoding="utf-8"))

    def test_pilot_shape_and_prompt_identity(self):
        self.assertEqual(len(self.rows), 25)
        self.assertEqual(len({r["pilot_query_id"] for r in self.rows}), 5)
        for row in self.rows:
            self.assertEqual(row["system_prompt_sha"], V3_SHA)
            self.assertEqual(row["system_prompt_version"], "generation-system-prompt-v3")

    def test_prompt_accounting_is_exact(self):
        self.assertEqual(self.acct["max_absolute_prompt_token_delta"], 0)
        self.assertTrue(self.acct["prompt_accounting_exact"])

    def test_no_malformed_or_unknown_handles_anywhere(self):
        self.assertEqual(self.manifest["total_malformed_citations"], 0)
        self.assertEqual(self.manifest["total_unknown_handles"], 0)

    def test_p05_abstains_cleanly_at_selected_reserve(self):
        reserve = self.acct["measured_minimum_full_contract_reserve"]
        row = next(r for r in self.rows
                   if r["pilot_query_id"] == "P05" and r["max_tokens"] == reserve)
        self.assertEqual(row["malformed_citations"], [])
        self.assertIsNotNone(row["abstention_marker"])
        self.assertEqual(row["completion_state"], "complete")

    def test_p04_answers_numerically_without_abstaining(self):
        reserve = self.acct["measured_minimum_full_contract_reserve"]
        row = next(r for r in self.rows
                   if r["pilot_query_id"] == "P04" and r["max_tokens"] == reserve)
        self.assertTrue(row["numeric_exact"])
        self.assertTrue(row["unit_exact"])
        self.assertIsNone(row["abstention_marker"])

    def test_full_contract_reserve_is_measured_not_null(self):
        full = self.acct["measured_minimum_full_contract_reserve"]
        nontrunc = self.acct["measured_minimum_nontruncating_reserve"]
        self.assertIsNotNone(full)
        self.assertGreaterEqual(full, nontrunc)
        detail = self.acct["reserve_sweep_detail"][str(full)]
        self.assertEqual(detail["truncated"], [])
        self.assertEqual(detail["malformed"], [])
        self.assertTrue(detail["p05_clean_abstention"])
        self.assertTrue(detail["p04_numeric_ok"])

    def test_budget_arithmetic_closes(self):
        a = self.acct
        self.assertEqual(a["loaded_context_length"], 71936)
        self.assertEqual(a["safety_margin_tokens"], 3596)
        self.assertEqual(
            a["maximum_prompt_tokens_operational"],
            a["loaded_context_length"] - a["safety_margin_tokens"]
            - a["selected_safe_generation_reserve_tokens"])
        self.assertEqual(
            a["rag_context_budget_planning_value"],
            a["maximum_prompt_tokens_operational"] - a["system_prompt_tokens"]
            - a["observed_template_and_boundary_overhead_tokens"] - a["question_reserve_tokens"])

    def test_selected_reserve_exceeds_measured_minimum_and_longest_answer(self):
        a = self.acct
        self.assertGreater(a["selected_safe_generation_reserve_tokens"],
                           a["measured_minimum_full_contract_reserve"])
        self.assertGreater(a["selected_safe_generation_reserve_tokens"],
                           a["max_completion_tokens_observed"])


class TestCandidateDescriptorV3(unittest.TestCase):
    PATH = ROOT / "data/metadata/generation_candidate_v1.json"

    def setUp(self):
        if not self.PATH.is_file():
            self.skipTest("candidate descriptor missing")
        self.descriptor = json.loads(self.PATH.read_text(encoding="utf-8"))

    def test_descriptor_pins_v3_prompt_and_v12_validator(self):
        self.assertEqual(self.descriptor["system_prompt_version"], "generation-system-prompt-v3")
        self.assertEqual(self.descriptor["system_prompt_sha256"], V3_SHA)
        self.assertEqual(self.descriptor["validator_version"], gen.VALIDATOR_VERSION)
        self.assertEqual(self.descriptor["harness_version"], gen.HARNESS_VERSION)

    def test_descriptor_records_prompt_history_up_to_the_frozen_candidate(self):
        """The descriptor pins the evaluated candidate (v3). v4 is a development prompt and must
        NOT appear here until it has been evaluated on a fresh holdout and promoted."""
        expected = {k: v for k, v in PROMPT_SHAS.items() if k in ("v1", "v2", "v3")}
        self.assertEqual(self.descriptor["system_prompt_history"], expected)
        self.assertNotIn("v4", self.descriptor["system_prompt_history"])
        self.assertEqual(self.descriptor["system_prompt_version"], "generation-system-prompt-v3")

    def test_descriptor_matches_accounting_artifact(self):
        acct_path = ROOT / "data/evaluation/generation_prompt_accounting_v3.json"
        if not acct_path.is_file():
            self.skipTest("accounting artifact missing")
        acct = json.loads(acct_path.read_text(encoding="utf-8"))
        for key in ("measured_minimum_nontruncating_reserve",
                    "measured_minimum_full_contract_reserve",
                    "maximum_prompt_tokens_operational",
                    "rag_context_budget_planning_value"):
            self.assertEqual(self.descriptor[key], acct[key], key)
        self.assertEqual(self.descriptor["selected_safe_output_reserve"],
                         acct["selected_safe_generation_reserve_tokens"])
        self.assertEqual(self.descriptor["generation_parameters"]["max_tokens"],
                         acct["selected_safe_generation_reserve_tokens"])

    def test_artifact_shas_are_current(self):
        manifest_path = ROOT / "data/evaluation/generation_reserve_pilot_v3_manifest.json"
        if not manifest_path.is_file():
            self.skipTest("manifest missing")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(self.descriptor["reserve_pilot_artifact_sha256"],
                         manifest["jsonl_sha256"])
        self.assertEqual(self.descriptor["prompt_accounting_artifact_sha256"],
                         manifest["accounting_sha256"])
