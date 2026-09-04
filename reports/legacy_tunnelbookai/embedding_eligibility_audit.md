# TunnelBookAI Embedding Eligibility & Extraction Recovery Audit

## Result

**FULL EMBEDDING INPUT — GO**

No embedding, vector database, retrieval or RAG was run in this stage.

## Input

- Canonical chunks classified: **6039/6039**
- Every chunk received exactly one eligibility status: **True**

## Extraction Failures

- Chunks with extraction damage: **59**

| document | damaged chunks | total chunks | signature |
|---|---|---|---|
| DOC000009 | 6 | 6 | control_character_residue, glyph_index_sequence, under_8_real_words |
| DOC000041 | 8 | 8 | glyph_index_sequence |
| DOC000051 | 45 | 45 | control_character_residue |

## Low-content

- Total flagged `eligible_low_content`: **142**
- Kept in embedding input: **142**
- Quarantined: **0**
- Policy is keep + flag. Short regulation articles (`MADDE 3- Bu Karar yayımı tarihinde yürürlüğe girer.`), table chunks and technical labels are legitimate content and are not deleted. A retrieval-time score threshold is the right lever, and is deferred to retrieval evaluation.

## Recovery

### DOC000009

- Method: **glyph_index_decode(+29)**
- Source variant used: **full_docling**
- Result: **recovered**
- Replacement chunks: **3**

| metric | before | after |
|---|---|---|
| glyph sequences | 2034 | 0 |
| residual glyph runs | 157 | 0 |
| control characters | 0 | 0 |
| replacement chars | 0 | 0 |
| real words | 155 | **363** |
| digits | 4291 | 645 |
| table lines | 43 | 43 |
| headings | 9 | 9 |
| page markers | 2 | 2 |

### DOC000041

- Method: **glyph_index_decode(+29)**
- Source variant used: **normalized**
- Result: **recovered**
- Replacement chunks: **4**

| metric | before | after |
|---|---|---|
| glyph sequences | 3649 | 0 |
| residual glyph runs | 244 | 0 |
| control characters | 0 | 0 |
| replacement chars | 0 | 0 |
| real words | 10 | **385** |
| digits | 6942 | 564 |
| table lines | 0 | 0 |
| headings | 5 | 5 |
| page markers | 0 | 0 |

### DOC000051

- Method: **utf16be_pair_decode**
- Source variant used: **normalized**
- Result: **recovered**
- Replacement chunks: **5**

| metric | before | after |
|---|---|---|
| glyph sequences | 0 | 0 |
| residual glyph runs | 0 | 0 |
| control characters | 24951 | 0 |
| replacement chars | 0 | 0 |
| real words | 4 | **1877** |
| digits | 9773 | 9104 |
| table lines | 0 | 0 |
| headings | 2 | 2 |
| page markers | 0 | 0 |

## Final Embedding Eligibility

- `eligible`: **5838**
- `eligible_low_content`: **142**
- `replacement_available` (canonical, superseded): **59**
- `quarantined_extraction_failure`: **0**

- Canonical eligible in input: **5980**
- Recovery chunks in input: **12**
- **Total vectors planned: 5992**
- Baseline without any recovery would have been 6039 − 59 = **5980**

## Duplication Guard

- Documents contributing both canonical and recovery content: **0**
- For each recovered document the damaged canonical chunks are marked `replacement_available` and excluded, so the same source text is never embedded twice.

## Integrity

- Frozen corpus changed: **false**
- Frozen chunks changed: **false**
- Frozen metadata changed: **false**
- Total frozen artefacts changed: **0**
- Recovery output is written only to `data/corpus_recovery/` and `data/chunks_recovery/`.

## Tests

- Main tests (`tests/`): **270/270 PASS** (226 previous + 44 new eligibility/recovery tests; 2 model-download tests opt-in)
- Report/Colab tests (`rapor/tests/`): **16/16 PASS**
- Project-wide total: **286/286 PASS**
- New tests cover: glyph failure detector (both forms), control-character detector, legitimate short regulation not quarantined, table with few words not quarantined, exact 58 known-failure reproduction, zero false positives, eligibility manifest = 6039 unique canonical chunks, quarantined chunks absent from embedding input, deterministic replacement IDs, no canonical/recovery duplicate indexing, recovery provenance, decoded-number arithmetic consistency, frozen artefacts unchanged, idempotency.

## Warnings

- Recovery decoders are deterministic character-mapping repairs, not OCR and not generation. The glyph decoder inverts a subset-font mapping (`char = chr(gid + 29)`, verified by decoding known titles such as `Estimate of annual operating costs`); the UTF-16 decoder reassembles byte-split code units. No text was invented at any point.
- Recovered documents keep `source_only` provenance: the damaged extractions carried no usable page anchors, and none were fabricated.
- Recovery chunks are new content entering the corpus and have not been through the full chunking audit that the frozen 6039 passed. They were produced with the same chunker rules, but review them before treating them as equal-confidence sources.
- The original damaged chunks remain in the frozen corpus by design; they are excluded at the manifest level, not deleted.

## Blockers

- Yok.

## Final Decision

**FULL EMBEDDING INPUT — GO**

`data/metadata/full_embedding_input_manifest.csv` is the single input list for the full embedding run: **5992 vectors**.
