# Controlled Canonical Promotion Contract V1

## Authority and boundary

`tunnelbookai.canonical` is the sole owner of canonical planning, apply, manifest creation,
verification and status. Unified Ingest remains authoritative for originals, extraction,
metadata, provenance, classification, deduplication, quality, chunking and staging.
Promotion verifies those outputs; it does not reproduce their decisions.

Book evidence is limited to members of the verified manifest at
`corpus/canonical/canonical_manifest.json`. Raw originals remain outside the book evidence
boundary and are read only by the verifier to confirm the admitted source SHA.

## Operator protocol

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical plan --document-id ING_... --json
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical plan \
  --document-id-file audit/corpus_population/promotion_batches/CPP_....json --json
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical apply \
  --plan audit/canonical_promotions/plans/CCP_....json \
  --approve CCP_....
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical verify --json
```

Planning writes a deterministic audit plan but makes no canonical mutation. Apply requires
the exact `CCP_<sha256>` from that plan. Under an exclusive lock it rebuilds the plan from
disk; any difference returns `STALE_CANONICAL_PROMOTION_PLAN` before canonical mutation.
The optional `--document-id-file` accepts only an identity-valid, root-confined `CPP_`
selector created by Corpus Population. A selector is not an eligibility verdict and cannot
approve or apply its resulting plan.

## Eligibility

An eligible direct `corpus/staging/v2/<document_id>` child must have the active staging
shape, a document ID derived from the source SHA, a hash-valid immutable original, an exact
processing/staging artifact match, valid metadata and provenance, final sections in the
frozen book scope, clean `GO` document quality, `PASS` or error-free `WARN` chunk quality,
consistent ingest ledgers and at least one eligible retrieval chunk. Chunk IDs are unique,
bound to the same document/source/classification and independently recomputable.

An exact/strong upstream duplicate is rejected. Against canonical state, an identical
document and semantic identity is an idempotent no-op; a reused document ID with different
identity is `DOCUMENT_ID_CONFLICT`; a reused source SHA under another ID is
`EXACT_SOURCE_DUPLICATE`.

## Storage and manifest

Each admitted object is immutable and content-addressed:

```text
corpus/canonical/objects/<document_id>/<document_digest>/
```

It contains normalized Markdown, metadata/provenance/classification/quality/extraction
sidecars, `chunk_manifest.jsonl`, `embedding_ready.jsonl` and the derived
`chunk_identities.jsonl`. Raw source bytes, page snapshots and processing asset trees are
not copied.

The single manifest records schema/contract version, document and chunk totals, the
canonical corpus digest and sorted document records. Each record provides original,
processing and staging identities; canonical paths and file hashes; quality,
classification and provenance identities; chunk counts and ledger identity; document
digest; and admitting plan ID. It embeds no document content or timestamp.

Chunk hashes are SHA-256 values over canonical JSON records. A document digest covers its
source identity, normalized text, semantic sidecars and chunk identity digest. The corpus
digest covers only the sorted `(document_id, document_digest, source_sha256)` projection
plus schema/contract identity. Digests exclude mtimes, timestamps, absolute paths and
filesystem order.

## Replacing a canonical document's derived outputs

A candidate whose `document_id` and source SHA256 are already canonical but whose document
digest differs (its processing/staging artifacts were legitimately re-derived, for example
after an extraction fix applied through `ingest --reprocess-canonical`) is planned with the
action `REPLACE`. Apply materializes the new object under
`objects/<document_id>/<new_digest>/`, replaces the manifest record and leaves the previous
object directory unreferenced and inert (`UNREFERENCED_CANONICAL_OBJECT` warning; never
deleted automatically). Like every write, it requires the exact plan identity and explicit
approval and changes the corpus digest, so retrieval indexes and book audits bound to the
old digest become stale. A candidate with the same `document_id` but a different source SHA
remains a `DOCUMENT_ID_CONFLICT`.

## Atomicity, audits and recovery

Apply is all-or-nothing at the manifest level. It builds and verifies objects in a sibling
temporary directory, atomically renames complete objects into the canonical object store,
then atomically replaces the root manifest as the single commit point. Files and relevant
directories are fsynced. A controlled failure restores the previous manifest and removes
only transaction-owned objects after validating their exact paths.

Each valid apply invocation first creates a pending record and finishes with an immutable
audit at `audit/canonical_promotions/applies/<promotion_id>.json`. A process interruption
leaves the pending record for operator investigation; unreferenced objects remain inert and
are reported but never admitted or automatically deleted.

`verify` reconstructs trust from disk: strict schema/serialization, path safety, exact file
inventory, original SHA, document/source uniqueness, provenance, classification, chunk IDs,
chunk and retrieval-row hashes, counts, document digests and corpus digest. Its states are:

- `EMPTY`: marker-only canonical root; valid bootstrap, retrieval forbidden.
- `READY`: non-empty manifest and every integrity check passes; retrieval allowed.
- `INVALID`: missing/corrupt manifest or any identity/integrity failure; retrieval forbidden.

The empty-reset gate is not a production gate. Once ingest data exists, use architecture
isolation plus canonical verification; never delete valid data merely to make the reset gate
return `GO`.
