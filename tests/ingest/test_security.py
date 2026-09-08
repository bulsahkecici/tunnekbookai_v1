"""Security boundary tests (task §80).

The engine is local-only. These tests assert that every AI endpoint and every conversion
path REFUSES to leave the loopback interface, and that a manual document is never sent
anywhere.

Run:  PYTHONPATH=. .venv/bin/python -m unittest tests.ingest.test_security -v
"""

from __future__ import annotations

import contextlib
import io
import unittest
from types import SimpleNamespace

from tunnelbookai.ingest import docling_adapter
from tunnelbookai.ingest.classify.arbiter import LocalChatClient, arbitrate
from tunnelbookai.ingest.classify.embeddings import LocalEmbeddingClient, build_index
from tunnelbookai.ingest.classify.taxonomy import load_taxonomy
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.vision.provider import (
    DisabledVisionProvider, LocalOpenAICompatibleVisionProvider, RemoteEndpointRejected,
    assert_loopback, build_provider,
)

REMOTE_URLS = [
    "https://api.openai.com/v1",
    "http://10.0.0.5:1234/v1",
    "http://192.168.1.20:1234/v1",
    "https://example.com/v1",
    "http://169.254.169.254/latest",          # cloud metadata service
    "http://0.0.0.0:1234/v1",
    "http://[2001:db8::1]:1234/v1",
    "http://evil.com:1234/v1",
    "//api.openai.com/v1",
]
LOOPBACK_URLS = [
    "http://127.0.0.1:1234/v1",
    "http://localhost:1234/v1",
    "http://[::1]:1234/v1",
    "http://127.0.0.2:11434/v1",
]


class LoopbackGuardTests(unittest.TestCase):
    def test_remote_hosts_rejected(self):
        for url in REMOTE_URLS:
            with self.subTest(url=url):
                with self.assertRaises(RemoteEndpointRejected):
                    assert_loopback(url)

    def test_loopback_hosts_accepted(self):
        for url in LOOPBACK_URLS:
            with self.subTest(url=url):
                self.assertTrue(assert_loopback(url).startswith("http"))

    def test_empty_endpoint_rejected(self):
        for url in ("", None, "not-a-url", "file:///etc/passwd"):
            with self.subTest(url=url):
                with self.assertRaises(RemoteEndpointRejected):
                    assert_loopback(url)


class VisionSecurityTests(unittest.TestCase):
    """§26, §80 — no vision provider may be constructed against a remote host."""

    def test_remote_vision_endpoint_rejected(self):
        for url in REMOTE_URLS[:4]:
            with self.subTest(url=url):
                with self.assertRaises(RemoteEndpointRejected):
                    LocalOpenAICompatibleVisionProvider(url)

    def test_remote_allowed_flag_is_refused_outright(self):
        config = SimpleNamespace(vision={"enabled": "auto", "remote_allowed": True,
                                         "provider": "local_openai_compatible"})
        with self.assertRaises(RemoteEndpointRejected):
            build_provider(config)

    def test_non_loopback_allowed_hosts_refused(self):
        config = SimpleNamespace(vision={
            "enabled": "auto", "remote_allowed": False,
            "allowed_hosts": ["127.0.0.1", "api.openai.com"],
            "provider": "local_openai_compatible"})
        with self.assertRaises(RemoteEndpointRejected):
            build_provider(config)

    def test_disabled_provider_never_describes(self):
        provider = DisabledVisionProvider()
        self.assertFalse(provider.available())
        result = provider.describe("/nonexistent.png")
        self.assertIsNone(result["visual_description"])
        self.assertEqual(result["visual_description_status"], "DISABLED")

    def test_no_vision_flag_yields_the_disabled_provider(self):
        provider = build_provider(load_config(), enabled=False)
        self.assertIsInstance(provider, DisabledVisionProvider)

    def test_shipped_config_is_loopback_only(self):
        config = load_config()
        self.assertFalse(config.vision.get("remote_allowed", False))
        self.assertTrue(set(config.vision["allowed_hosts"]) <= {"127.0.0.1", "localhost", "::1"})
        base_url = config.vision["local_openai_compatible"]["base_url"]
        self.assertTrue(assert_loopback(base_url))


class EmbeddingSecurityTests(unittest.TestCase):
    """§38, §80 — the classifier's embedding server must be loopback, with no cloud fallback."""

    def test_remote_embedding_endpoint_rejected(self):
        for url in REMOTE_URLS[:4]:
            with self.subTest(url=url):
                with self.assertRaises(RemoteEndpointRejected):
                    LocalEmbeddingClient(url, "configured-model")

    def test_configured_servers_are_all_loopback(self):
        config = load_config()
        self.assertTrue(assert_loopback(config.models["embedding"]["default_endpoint"]))

    def test_remote_server_in_config_raises_rather_than_falling_back(self):
        config = SimpleNamespace(classification={"embedding": {"enabled": True}}, models={
            "embedding": {"model": "configured-model", "default_endpoint": "https://api.openai.com/v1"}})
        with self.assertRaises(RemoteEndpointRejected):
            build_index(config, load_taxonomy())


class ArbiterSecurityTests(unittest.TestCase):
    """§39, §80 — the local Qwen arbiter is loopback-only."""

    def test_remote_arbiter_endpoint_rejected(self):
        for url in REMOTE_URLS[:4]:
            with self.subTest(url=url):
                with self.assertRaises(RemoteEndpointRejected):
                    LocalChatClient(url)

    def test_configured_arbiter_is_loopback(self):
        config = load_config()
        self.assertTrue(assert_loopback(config.models["llm"]["default_endpoint"]))
        self.assertTrue(assert_loopback(config.metadata["llm_enrichment"]["base_url"]))

    def test_remote_arbiter_config_raises(self):
        config = SimpleNamespace(classification={"llm_arbiter": {"enabled": True}}, models={
            "llm": {"model": "configured-model", "default_endpoint": "https://api.openai.com/v1"}})
        with self.assertRaises(RemoteEndpointRejected):
            arbitrate("metin", [{"id": "1.1", "score": 0.5}], load_taxonomy(), config)


class DoclingSecurityTests(unittest.TestCase):
    """§26, §80 — Docling never enables remote services or external plugins."""

    def test_remote_services_forced_off(self):
        options, applied, _ = docling_adapter.build_pdf_options(load_config(), do_ocr=False)
        self.assertFalse(applied["enable_remote_services"])
        self.assertFalse(applied["allow_external_plugins"])
        self.assertFalse(options.enable_remote_services)
        self.assertFalse(options.allow_external_plugins)

    def test_config_cannot_turn_remote_services_on(self):
        """Even a config that asks for it must not produce a remote-enabled pipeline."""
        config = load_config()
        hostile = SimpleNamespace(
            ingest={**config.ingest,
                    "docling": {**config.docling_options, "enable_remote_services": True}},
            ocr=config.ocr, docling_options={**config.docling_options,
                                             "enable_remote_services": True})
        options, applied, _ = docling_adapter.build_pdf_options(hostile, do_ocr=False)
        self.assertFalse(options.enable_remote_services)
        self.assertFalse(applied["enable_remote_services"])

    def test_shipped_config_disables_remote_services(self):
        self.assertFalse(load_config().docling_options.get("enable_remote_services", False))


class LocalOnlyConfigTests(unittest.TestCase):
    def test_local_only_is_the_shipped_default(self):
        self.assertTrue(load_config().local_only)

    def test_manual_ingest_makes_no_network_call(self):
        """A manual document must reach no socket at all (§26). Guard by making every
        outbound connection raise for the duration of a full text-adapter extraction."""
        import socket
        import tempfile
        from pathlib import Path

        from tunnelbookai.ingest.adapters import AdapterContext, get_adapter
        from tunnelbookai.ingest.format_registry import detect
        from tunnelbookai.ingest.paths import PROJECT_ROOT

        original_socket = socket.socket
        original_create = socket.create_connection

        class Tripwire(original_socket):
            def connect(self, *args, **kwargs):
                raise AssertionError(f"manual ingest attempted a network connection: {args}")

            def connect_ex(self, *args, **kwargs):
                raise AssertionError(f"manual ingest attempted a network connection: {args}")

        def blocked(*args, **kwargs):
            raise AssertionError(f"manual ingest attempted a network connection: {args}")

        socket.socket = Tripwire
        socket.create_connection = blocked
        try:
            with tempfile.TemporaryDirectory() as d:
                source = Path(d) / "gizli_rapor.md"
                source.write_text("# Gizli Tünel Raporu\n\nİç kullanım.\n", encoding="utf-8")
                bundle = Path(d) / "bundle"
                bundle.mkdir()
                context = AdapterContext(
                    document_id="ING_secure", original_path=source,
                    original_filename="gizli_rapor.md", bundle=bundle,
                    detection=detect(source), config=load_config(), ocr=None,
                    vision=DisabledVisionProvider(), office_renderer=None,
                    root=PROJECT_ROOT, do_ocr=False, do_vision=False)
                result = get_adapter("text")(context)
                self.assertTrue(result.succeeded, result.errors)
                self.assertIn("Gizli Tünel Raporu",
                              (bundle / "normalized" / "document.txt").read_text(encoding="utf-8"))
        finally:
            socket.socket = original_socket
            socket.create_connection = original_create


class PromotionSafetyTests(unittest.TestCase):
    """§2, §47 — the promotion script can never target the canonical corpus."""

    def test_canonical_target_refused(self):
        import importlib.util

        from tunnelbookai.ingest.paths import PROJECT_ROOT

        spec = importlib.util.spec_from_file_location(
            "promote_staging_under_test", PROJECT_ROOT / "scripts" / "promote_staging.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for target in ("corpus/canonical", "corpus/canonical/", "corpus/canonical/subdir"):
            with self.subTest(target=target), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(module.main(["--apply", "--target", target]), 2)

    def test_default_is_a_dry_run(self):
        import importlib.util

        from tunnelbookai.ingest.paths import PROJECT_ROOT

        spec = importlib.util.spec_from_file_location(
            "promote_staging_dry", PROJECT_ROOT / "scripts" / "promote_staging.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with contextlib.redirect_stdout(io.StringIO()):
            exit_code = module.main(["--json"])
        self.assertEqual(exit_code, 0)
        self.assertFalse((PROJECT_ROOT / "corpus" / "promoted_v2").exists(),
                         "a dry run must not create the target directory")


if __name__ == "__main__":
    unittest.main()
