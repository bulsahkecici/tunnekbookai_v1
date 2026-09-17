# TunnelBookAI Local Operations Dashboard

The operations dashboard supervises one existing deterministic corpus-population run. It
does not discover sources, create a different batch plan, generate embeddings, or promote
anything to canonical. All document work continues through `tunnelbookai.population` and
the Unified Ingest single-writer boundary.

## Start

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.dashboard \
  --run audit/corpus_population/runs/CPR_<exact-id>.json
```

Open `http://127.0.0.1:8765`. Omitting `--run` selects the most recently modified valid
population run. The server refuses non-loopback bind addresses and Host headers.

## Controls

- **Başlat** starts the selected run from its first incomplete batch.
- **Güvenli durdur** records a durable stop request. The current document finishes and is
  atomically checkpointed; no next document starts.
- **Devam et** removes the stop request and resumes the first incomplete batch. Completed
  documents with verified terminal artifacts are reused rather than rebuilt.

The panel shows the active batch/document, batch and document totals, dispositions, recent
document outcomes, model capability, and the worker log. If a worker disappears without a
final checkpoint, the panel marks it `INTERRUPTED`. The next locked resume closes the
orphaned attempt record and reprocesses only the non-terminal document.

## Corpus explorer

The **Belgeler ve chunklar** tab lists every run document with its source filename, format,
disposition, section and real on-disk chunk count. Search and disposition filters are
server-side and paginated. Selecting a document shows its chunk text and all supported
processing artifacts. Markdown, JSON, JSONL, CSV, text and extracted images are previewed
read-only; preview paths are constrained to that document's processing directory and reject
traversal and symlinks.

A zero chunk count or missing section is explained from the run disposition, extraction
report and quality gate. For example, duplicates point to their canonical document,
recovery-required rows explain their interrupted checkpoint, and readable text with zero
chunks is identified as a chunker defect rather than an extraction failure.

## Semantic search

The **Semantik arama** tab uses the active, independently verified Book Retrieval V1
index. Queries are embedded by the exact loopback-only BGE-M3 model recorded in the index
manifest, then scored with normalized cosine similarity. An optional chapter filter limits
results to that primary or secondary section. Results expose the canonical document and
chunk identifiers, section, similarity score, page/slide/sheet locator when available, and
the canonical retrieval-manifest path. The tab is read-only and never changes corpus data.

The API endpoints are `GET /api/retrieval/status` and
`GET /api/retrieval/search?q=...&section=6&top_k=10`. A stale corpus digest, changed model,
failed shard hash, or unavailable local embedding service makes the request fail closed.

## Statistics and manual review

The **İstatistikler** tab aggregates extracted pages, tables, figures, OCR-bearing documents,
Markdown outputs, text characters and chunk types. Its elapsed-time and remaining-time
estimate comes from the recorded attempt wall times; it is an operational estimate, not a
deadline.

The **Manuel inceleme** queue is projected from failed, rejected, unsupported,
recovery-required, review and suspicious zero-chunk outcomes. Marking an item reviewed only
writes `audit/dashboard/manual_review.json`; it never moves or mutates the source document.
Operator notes can record a future parser, OCR engine or library experiment.

## Warning-driven improvement

The **İyileştirme** tab turns actionable chunk warnings into a bounded repair queue. It
splits chunks above the configured soft maximum and merges adjacent short text chunks only
when they share the same heading path and remain below that maximum. Short standalone
sections that cannot be merged safely are reclassified as `CHUNK_SHORT_STRUCTURAL`, an
informational condition rather than an actionable failure.

The worker preserves normalized text coverage and retrieval eligibility, writes a backup
before replacing derived chunk artifacts, and never changes source files, manual-review
decisions or document classification. Visual/media warnings are shown separately and left
deferred because they require source-specific rendering or OCR rather than a generic chunk
rewrite. Any previous staging audit or canonical-promotion plan must be rebuilt after a
successful repair; canonical promotion remains an explicit, separately approved action.

Evidence-backed bulk review decisions are applied with
`tunnelbookai.dashboard.section_review`. The operation checks the complete reviewed scope
before writing, records the former and new section mappings, synchronizes processing,
staging, embedding-ready and ingest ledgers, and moves excluded staging bundles into a
recoverable quarantine. The dashboard displays both the 3/4/6 section-review summary and
any official-full-text source recoveries. These operations invalidate earlier staging
audits and promotion plans; they never mutate canonical corpus state.

## Throughput safeguards

Within one serial worker process, Docling converters and their loaded models are reused for
identical option sets. OCR and vision results are reused for byte-identical extracted image
pixels, and tiny icons bypass both expensive models. PDF page OCR runs only when the native
text layer is thin; after a scan has been OCRed page-wide its figure crops are not OCRed a
second time. Legacy PPT documents whose text is recovered by Docling but whose binary slide
structure cannot be opened first pass through an isolated LibreOffice `.ppt` to `.pptx`
conversion and are then read structurally with `python-pptx`. Docling is intentionally
skipped on that converted legacy path because its native parser can crash on large binary
presentations. If conversion is unavailable but Docling recovers text, a text-element
fallback still keeps the document chunkable.

When a failed batch is retried, the population runner selects only `PENDING`,
`RECOVERY_REQUIRED`, and `FAILED` checkpoints. Completed `STAGED` documents—including
documents held for manual chunk-quality review—are not expensively extracted a second time.

`PAUSED`, `ERROR`, and `INTERRUPTED` are resumable dashboard states. A batch-level error
stops automatic advancement so the operator can inspect it before retrying. Canonical
identity is verified before and after every batch and remains unchanged by dashboard work.
