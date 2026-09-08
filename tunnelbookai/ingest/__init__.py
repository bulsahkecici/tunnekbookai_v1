"""Unified Ingest Engine.

Turns two data sources into one standard:

  1. PaperCrawler schema-2.x Source Packs     ->  incoming/papercrawler/releases/
  2. User / internal documents                ->  incoming/manual/inbox/

into deterministic processing bundles under processing/<document_id>/, quality-gated and
prepared for corpus/staging. Canonical promotion is a separate, explicit, dry-run-by-default
step (scripts/promote_staging.py) and is NOT part of this engine.

Boundary rules (see reports/unified_ingest_preimplementation_audit.md):
  - Originals are never modified. First real operation is SHA256 + originals/ archive.
  - No writes to corpus/canonical/.
  - Manual ingest performs no network egress. Local AI only on loopback hosts.
  - PaperCrawler provisional classification is a feature/hint, never the final.
"""

INGEST_BUNDLE_SHAPE = "unified_ingest_v1"
