# TunnelBookAI V1 — Controlled Real-Data Pilot Audit

Pilot: `TUNNELBOOKAI_REALDATA_PILOT_001`
Date: 2026-09-03
Machine report: [`audit/real_data_pilot.json`](../audit/real_data_pilot.json)
Input manifest: [`audit/real_data_pilot_manifest.json`](../audit/real_data_pilot_manifest.json)

Not executed: embeddings, Qdrant, canonical promotion, the 2950-question evaluation, book
generation. Canonical corpus unchanged; canonical promotions = 0.

---

## Executive Summary

Six real documents — one PaperCrawler PDF and five manual documents (PDF, DOCX, PPTX, XLSX,
PNG) — were run end to end through the Unified Ingest Engine.

**All six originals survived byte-identical. Four passed the quality gate (GO), two were sent
to REVIEW for truthful reasons. Zero rejects, zero failures, zero false merges, zero duplicate
chunks.** Structural extraction was accurate everywhere it could be checked against the source:
170/170 XLSX formulas byte-exact, 15/15 slides, 10/10 and 9/9 PDF pages, 17/17 DOCX images.

**Two real defects were found and fixed** (§43), both in crawler metadata handling. Both are
covered by new regression tests; the ingest suite is now **206/206**.

The pilot's main negative finding is not in the ingest engine at all: **the embedding signal is
flat on real data** — a mean top1–top2 margin of 0.0066 across six documents. Section
classification is still mostly correct because deterministic rule and chunk-vote signals and the
local arbiter carry it, but the embedding contributes almost no discrimination, and one document
received a *confident wrong* section as a result.

| Verdict | Result |
| --- | --- |
| Unified Ingest Engine | **GO** |
| Embedding / Classification Signal | **CONDITIONAL_GO** |
| Qdrant / Retrieval Phase Readiness | **CONDITIONAL_GO** |

---

## 1. Pilot Inputs

The manual inbox and the crawler release directory were **not** populated at the start of this
task: `incoming/manual/inbox/` contained only synthetic test fixtures byte-identical to
`tests/ingest/fixtures/`, and `incoming/crawler/releases/` was empty. The synthetic fixtures were
moved out to `data/temp/pilot_parked_synthetic_fixtures/` so they could not enter the pilot, and
six real documents were staged instead.

| Role | Format | Document | Size | SHA256 (16) |
| --- | --- | --- | --- | --- |
| crawler_pdf | PDF | Engineering Geological Investigation of the Kırık Tunnel Route | 1 932 051 B | `b8667b0178e8102a` |
| manual_pdf | PDF | 12_1_Fire Safety in Tunnels.pdf | 1 098 657 B | `b952814dcd0347a8` |
| manual_docx | DOCX | Dünyada Tünel Felaketleri.docx | 2 581 142 B | `991e7004905db22e` |
| manual_pptx | PPTX | 7-TÜNEL TARİF-ANALİZ-YBF.pptx | 896 489 B | `804ea857fe56576c` |
| manual_xlsx | XLSX | 2019 KGM TÜNEL İCMALİ.xlsx | 20 419 B | `296bae6c6d0e76f8` |
| manual_image | PNG | InvertBetonUygulaması.png | 502 783 B | `c77a14960e997ca9` |

The five manual documents were copied read-only from the user's archive at
`~/Projects/tunnel/`; all five originals were verified unchanged afterwards. Original filenames
were preserved, including Turkish characters, spaces and parentheses.

### PaperCrawler release (§7)

The packages on disk were schema **1.1**, which §7 does not accept. Rather than ingest a legacy
package or hand-author a v2 envelope, one existing SHA-verified real source was **re-exported by
the unmodified PaperCrawler v1.0.0 code itself** (`handoff_export.py`), with no crawl:

* an isolated staging root was given a single-record `classification_index.jsonl` pointing at a
  byte-identical copy of the archived PDF (so the exporter's hardlink never touched the original);
* `export_handoff()` was called with that root and `destination=incoming/crawler/releases/PILOT_RELEASE_001`.

PaperCrawler source was not modified (only `__pycache__` byte-code was written), and the archived
original was not modified.

Contract validation through `crawler_contract.discover()` (schema 2 required, legacy **not**
allowed):

```
schema_version  2.0        producer  paper-crawler-agent
blockers        []         accepted  1        skipped  0
paper_crawler_status  READY_FOR_HANDOFF
tunnelbookai_status   NOT_INGESTED
declared sha256  b8667b0178e8102a697e371611f812b6bafef514d37a4dd1280570b77ce6fe39  (verified)
provenance       landing_url, pdf_url, discovery_source, discovery_query, doi, publisher
```

**Contract note.** The v2 handoff manifest carries `provisional_document_type`,
`provisional_source_tier`, `provisional_authority_tier` and `provisional_classification_status`,
but **not** `provisional_primary_section`. The section hint (`primary_section: "2.4.1"`, score
0.95) exists only in the package's own `classification.json`, which the contract reader does not
open. So `crawler_provisional_section` is `null` and `crawler_final_agreement` is `null` — correct
behaviour for the input given, not an engine defect. §25's rule that a crawler hint must never
override stronger evidence was therefore not exercised. See Recommendations.

## 2. Original Integrity (§10)

| Role | incoming SHA256 | archive SHA256 | archive file | archive read-only | source archive |
| --- | --- | --- | --- | --- | --- |
| crawler_pdf | `b8667b0178e810` | match | match | yes | n/a |
| manual_pdf | `b952814dcd0347` | match | match | yes | unchanged |
| manual_docx | `991e7004905db2` | match | match | yes | unchanged |
| manual_pptx | `804ea857fe5657` | match | match | yes | unchanged |
| manual_xlsx | `296bae6c6d0e76` | match | match | yes | unchanged |
| manual_image | `c77a14960e997c` | match | match | yes | unchanged |

**6 / 6 PASS.** Archived originals are stored read-only (mode `-r--r--r--`).

## 3. PDF — PaperCrawler (§11, §12)

10 pages, 10 page snapshots, 8 figures, 15 table artefacts, 32 251 native text characters,
evidence `FULL_TEXT`, gate **GO**.

Heading order on page 1 matches the source exactly, including the journal masthead ahead of the
article title. Tables carry real structure — `Table 1. Dividing the tunnel route into structural
zones` with `KM | Formation | Lithology | Meter`, `Table 2. … pressurized water test results`,
`Table 3. RMR classification system for tunnel route`. Turkish author names survive intact
(`Özgür Fatih ÇÜMEN`, `Ahmet KARAKAŞ`).

**§12 scanned-PDF rule: satisfied.** `text_char_count = 32 251` from native extraction and
`ocr_items = 0`; no OCR-derived text was counted as native. `FULL_TEXT` is honest here.

Quality note: Table 3 shows garbled cell text (`DrGogd Marsber Onil`) — a complex rotated
classification table Docling's cell recogniser could not resolve. Not fabricated, just poor; the
structured JSON records what was read.

## 4. PDF — Manual (§11, §12)

9 pages, 9 page snapshots, 27 figures, 2 970 native characters, evidence `FULL_TEXT`, gate **GO**.

This is a slide deck exported to PDF (fire-damper testing, `www.tunnelturkey.org`), so text
density per page is low and figure count is high — faithful to the source. Native text is real
(`Isıl Genleşme`, `Young Modülü`, `Termal Şok`, damper performance clauses), `ocr_items = 0`.

## 5. DOCX (§13)

11 rendered page snapshots, 17 figures, **0 native text characters**, evidence `VISUAL_ONLY`,
gate **GO**.

Checked against the source with `python-docx`: the original has **22 paragraphs, all empty**, and
17 embedded images. The document is an image album of tunnel-disaster web-page screenshots. The
engine's output is therefore *correct*: 17 `figure_ref` elements, no text, `VISUAL_ONLY` —
it did not invent a text layer, and it did not claim `FULL_TEXT`.

Structural authority remained `original_docx` + Docling; the LibreOffice-rendered PDF contributed
page snapshots only. Figure OCR recovered the screenshot text (e.g. *"Recently, a part of a huge
tunnel under construction in Uttarkashi, Uttarakhand has collapsed"*), which is what makes this
document classifiable at all.

Content-provenance observation (not an engine defect): this document's evidence is screenshots of
third-party news pages. Provenance is recorded accurately, but the *authority* of that content is
a news website — a corpus-curation question for the book, not an ingest question.

## 6. PPTX (§14)

15 slides, 15 slide snapshots, 5 figures, 0 tables, 0 charts, 0 speaker notes, evidence
`FULL_TEXT`, gate **REVIEW** (`LOW_SECTION_CONFIDENCE`, 0.45).

Verified against `python-pptx`: slide count, slide order, the single title placeholder (slide 1)
and the picture distribution (2 on slide 1; one each on slides 4, 5, 9) all match exactly. Zero
tables and zero charts is correct — the deck has none.

Slide 1's rendered snapshot was inspected visually and matches the original presentation
faithfully, with Turkish diacritics rendered correctly
(`TÜNEL İŞLERİNDE TARİF – ANALİZ – YBF`, `YOL YAPIM ŞEFİ`).

Docling AI chart extraction remained **disabled** (`charts.enabled: false`); both PDFs recorded
`CHART_EXTRACTION_DISABLED_BY_CONFIG`. Deterministic native chart metadata stayed enabled and
correctly found none.

## 7. XLSX (§15, §16)

3 sheets, 2 sheet snapshots, evidence `STRUCTURED_TABULAR`, gate **GO**.

| Sheet | State | Used range | Cells | Formulas | Merged | Tables | Charts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `15.11.2019` | visible | A1:Q25 | 124 | 75 | 18 | 0 | 0 |
| `2018 sonu` | visible | A1:Q25 | 124 | 95 | 18 | 0 | 0 |
| `Sayfa2` | visible | A1:A1 | 0 | 0 | 0 | 0 | 0 |

Sheet names, order, used ranges, cell coordinates and merged ranges all match `openpyxl` ground
truth exactly.

**Formula preservation: 170 / 170 formula cells byte-exact** (full sweep, not a sample). This
includes external-workbook references containing Turkish characters:

```
15.11.2019!F7   =+'[1]İCMAL 2017.04.15'!J261     exact
15.11.2019!H7   =+G7/$G$17                        exact
15.11.2019!L7   =+F7+I7                           exact
15.11.2019!N7   =+M7/$M$17                        exact
15.11.2019!G17  =+G16+G13+G10                     exact
2018 sonu!F7    =+'[1]İCMAL 2017.04.15'!J261     exact
2018 sonu!M7    =+G7+J7                           exact
15.11.2019!K7   =+J7/$J$17                        exact
```

Cached values were preserved where the workbook stored them (66, 0.0612…, 83, 361179) and **no
value was invented**. CSV export was skipped with the honest reason
`XLSX_CSV_SKIPPED_MERGED_CELLS` on both populated sheets — correct, since 18 merged ranges cannot
be flattened losslessly; the structured JSON remains authoritative.

**§16 hidden sheets:**
* structured hidden sheets = **N/A** — this workbook has no hidden sheets (all three `visible`).
  The structured model does carry `hidden` / `sheet_state` per sheet and a `hidden_sheets` list,
  and hidden-sheet representation is covered by the synthetic-fixture test suite.
* visual hidden sheets = **N/A** (nothing hidden to render).

## 8. Image (§17, §18)

1 figure, evidence `VISUAL_ONLY`, gate **REVIEW** (`OCR_EMPTY_TEXT_IMAGE`).

```
ocr_status                 EMPTY        ocr_text            null
visual_description_status  SUCCESS
visual_description         "İnşaat halindeki bir tünelin iç mekan görüntüsü."
```

`OCR_TEXT != VISUAL_DESCRIPTION` is strictly preserved. The image was inspected directly: it
shows the interior of a tunnel under construction with an invert-concrete formwork gantry. The
description is accurate and appropriately conservative, and the REVIEW is truthful — there is no
legible text in the photo.

**§18 safety sweep across all 58 figure chunks:** exactly one contains an engineering quantity
(`40cm`), and it is OCR'd text transcribed from a technical drawing
(`TÜNEL EKSENI / YAPIM TOLERANSI KAZI HATTI (10m)`), not an inference. No fabricated
measurements, material properties, failure mechanisms, project identity or geography anywhere.

## 9. Metadata Accuracy (§19, §20)

Every populated field was classified against the source.

| Role | title | source | verdict |
| --- | --- | --- | --- |
| crawler_pdf | Engineering Geological Investigation of the Kırık Tunnel Route | `crawler_manifest` | SUPPORTED *(after D1/D2 fix)* |
| manual_pdf | TÜNEL DAMPERİ TASARIM DETAYLARI - ŞARTNAME | `document_heading` | SUPPORTED (a real in-document heading) |
| manual_docx | Dünyada Tünel Felaketleri | `ooxml_properties` | SUPPORTED |
| manual_pptx | KAYA  SINIFLANDIRMASI | `ooxml_properties` | SUPPORTED-but-contradicted |
| manual_xlsx | 15.11.2019 | `ooxml_properties` | SUPPORTED-but-weak |
| manual_image | InvertBetonUygulaması | `original_file` (inferred, flagged) | INFERRED_WITH_EVIDENCE |

**UNSUPPORTED populated metadata: 0.** Unknown fields are left `null` / `UNKNOWN` rather than
guessed — `organization` and `department` are `null` on all six, with the recorded reason
*"organization is never inferred from filename or body text"*.

**§20 title regression: 0 archive-name titles.** No document uses `source.pdf` / `source.docx` /
`source.pptx` / `source.xlsx` as a semantic title. The one filename-derived title
(`InvertBetonUygulaması`) is explicitly recorded as `inferred: true`, source `original_file`,
confidence `low`, with `title_inferred_from_filename` set — and the dedup registry flags it
`title_is_weak`, so it cannot drive a title merge.

Two honest weaknesses worth recording:

* **manual_pptx** — OOXML `dc:title` says `KAYA  SINIFLANDIRMASI` and `dc:creator` says `TCK`,
  but slide 1 says `TÜNEL İŞLERİNDE TARİF – ANALİZ – YBF` by `Suhan Mutlu`. The file was created
  2001-11-09 and revised 218 times; the property is a stale template leftover. The value is
  genuinely supported by document metadata, so it is not an UNSUPPORTED claim — but it is
  misleading. See Recommendations.
* **manual_xlsx** — title `15.11.2019` is the first sheet name; the workbook's own heading in
  cell D4 is `TÜM TÜNELLER İCMALİ`. Weak, not wrong.

## 10. Dedup Accuracy (§22)

| Signal | Result |
| --- | --- |
| duplicate SHA256 | none |
| duplicate DOI | none |
| duplicate normalized URL | none |
| duplicate strong normalized title | none |
| **false merges** | **0** |
| **missed exact duplicates** | **0** |

All six carry `duplicate_of: null`. The registry's `title_is_weak` guard correctly flags
filename-derived titles (`invertbetonuygulamasi`, `dunyada tunel felaketleri`) so they cannot
trigger a STRONG title+year merge.

The crawler+manual same-source case did not arise in this pilot (the six inputs are six distinct
documents), so "one identity, two provenance sources" was not exercised on real data.

**Dedup hazard closed by D1.** Before the fix, the crawler document's title was
`kocaeli university` with `title_is_weak = False` — a generic institutional name eligible for
STRONG title+year merging. Any other Kocaeli University paper of the same year would have been a
false-merge candidate. The fix replaces it with the real article title.

## 11. Turkish Normalization (§21)

Real-data check across all six titles and every ALL-CAPS Turkish heading in the corpus:

| Input | Normalized | Case-symmetric |
| --- | --- | --- |
| `TÜNEL DAMPERİ TASARIM DETAYLARI - ŞARTNAME` | `tunel damperi tasarim detaylari sartname` | yes |
| `Dünyada Tünel Felaketleri` | `dunyada tunel felaketleri` | yes |
| `KAYA  SINIFLANDIRMASI` | `kaya siniflandirmasi` | yes |
| `InvertBetonUygulaması` | `invertbetonuygulamasi` | yes |
| `Engineering … Kırık Tunnel Route` | `engineering … kirik tunnel route` | yes |

Every Turkish letter (`ı İ i I ş Ş ğ Ğ ü Ü ö Ö ç Ç`) folded correctly; none was dropped. The real
ALL-CAPS heading `TÜNEL DAMPERİ TASARIM DETAYLARI - ŞARTNAME` normalizes identically to its
lowercase form under the classification normalizer, confirming on real data the shared-fold fix
made in the previous task. Non-breaking spaces (`\xa0`) present in the source are normalized away.

**PASS.**

## 12. Final Section Classification (§23, §24, §25)

| Role | Final | Section title | Conf. | Secondary | Assessment |
| --- | --- | --- | --- | --- | --- |
| crawler_pdf | `2` | TÜNEL ANA ELEMANLARI… | 0.79 | 2.4.2.1 | defensible but coarse |
| manual_pdf | `5.9.1` | Ulusal Literatür Taraması | 0.58 | — | **misclassified** |
| manual_docx | `1.5` | Tünel Felaketleri | 0.92 | 1.5.1, 1.4.1, 2.1.1 | excellent |
| manual_pptx | `2.4.3` | KGM'de Tünel Projelendirilmesi Esasları | 0.45 | 2.1.1 | defensible (REVIEW) |
| manual_xlsx | `1.4.2` | Türkiye'de Karayolu Tünelleri | 0.85 | 3 | excellent |
| manual_image | `2.1.1` | Tünellerle İlgili Tanımlamalar | 0.81 | — | weak / marginal |

**Plausible primary sections: 4 / 6.**

* `manual_pdf → 5.9.1` is wrong. The document is a fire-damper design specification (thermal
  expansion, Young's modulus, thermal shock, damper performance clauses); "National Literature
  Review" is not a content match. The taxonomy has **no ventilation or fire-safety section** at
  all — the nearest legitimate home would be `5.4.2` (electrical/electromechanical systems). This
  is a taxonomy coverage gap amplified by a flat embedding, not an extraction fault. It is the
  worst outcome in the pilot because it was a *confident* wrong answer that passed the gate.
* `manual_image → 2.1.1` ("definitions") is weak for a construction photo; `2.1.2` (support
  elements) would fit better. With a single-sentence vision description as the only evidence, a
  generic section is understandable.
* `crawler_pdf → 2` is the broad parent. The crawler's own LLM had said `2.4.1` — *Jeolojik ve
  Geoteknik İncelemeler* — which is a better fit for a geological route investigation. The engine
  could not see that hint because the v2 manifest does not carry it (§1 above).

**§24 single taxonomy: 12 / 12 section ids valid**, every one present and `active: true` in
`book/scope/normalized/book_scope.json` (66 sections, `taxonomy_source` recorded per document).
No invented ids, no second taxonomy.

## 13. Classifier Signal Contributions (§25)

| Role | rule | chunk vote | embedding | crawler hint | arbiter | decision path |
| --- | --- | --- | --- | --- | --- | --- |
| crawler_pdf | 0.556 | 0.198 | 0.881 | none | NOT_RUN | strong agreement, gap 0.103 |
| manual_pdf | 0.200 | 0.182 | 0.852 | none | NOT_RUN | strong agreement, gap 0.197 |
| manual_docx | 0.750 | 0.000 | 0.841 | none | SUCCESS | gap 0.089 |
| manual_pptx | 0.000 | 0.000 | 0.849 | none | SUCCESS | gap 0.003 |
| manual_xlsx | 0.000 | 0.000 | 0.809 | none | SUCCESS | gap 0.001 |
| manual_image | 0.333 | 1.000 | 0.832 | none | NOT_RUN | strong agreement, gap 0.440 |

The two documents classified best (`manual_docx` 1.5, `manual_xlsx` 1.4.2) were carried by the
rule signal and the arbiter respectively — not by the embedding. The crawler hint never fired
because it is absent from the v2 manifest, so §25's "hint must never override stronger evidence"
was not put to the test.

Observation: `manual_pdf` recorded `disagreement=True` in its decision path yet resolved to
`arbiter:not_needed_strong_agreement` on a fused gap of 0.197, and produced the pilot's one
confident misclassification. Worth a look when the classifier is next tuned — out of scope here.

## 14. Embedding Separation Diagnostic (§26, §27)

Model: `text-embedding-nomic-embed-text-v1.5` (local). Top-10 candidate sections per document.

| Role | top1 | top2 | top3 | margin 1–2 | spread 1–5 | mean top10 | sd top10 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| crawler_pdf | 0.8891 | 0.8881 | 0.8863 | **0.0010** | 0.0067 | 0.8842 | 0.0034 |
| manual_pdf | 0.8524 | 0.8502 | 0.8483 | 0.0022 | 0.0079 | 0.8461 | 0.0039 |
| manual_docx | 0.8411 | 0.8260 | 0.8236 | 0.0151 | 0.0190 | 0.8241 | 0.0069 |
| manual_pptx | 0.8584 | 0.8527 | 0.8490 | 0.0057 | 0.0109 | 0.8475 | 0.0060 |
| manual_xlsx | 0.8112 | 0.8100 | 0.8094 | **0.0012** | 0.0046 | 0.8072 | 0.0030 |
| manual_image | 0.8317 | 0.8174 | 0.8153 | 0.0143 | 0.0171 | 0.8165 | 0.0060 |

**Aggregate — mean top1 0.8473, mean top1–top2 margin 0.0066, mean top1–top5 spread 0.0110,
mean sd 0.0049.**

**Verdict: FLAT.** The pre-pilot observation (similarities clustering around 0.83–0.84) is
confirmed and now quantified on real documents. A 0.1–1.5 percentage-point gap between the best
and second-best of 66 sections is not usable discrimination on its own; four of six documents sit
under a 0.6-point margin. No model or config was changed during the pilot (§26).

## 15. Qwen Arbitration (§28)

**3 calls of 6 documents**, model `qwen3.6-35b-a3b-mlx` — a **local MLX** model. No remote LLM
endpoint was contacted.

| Role | Called | Reason |
| --- | --- | --- |
| crawler_pdf | no | strong deterministic agreement (gap 0.103) |
| manual_pdf | no | strong deterministic agreement (gap 0.197) |
| manual_docx | **yes** | unsettled; arbiter confirmed 1.5 from the title *Dünyada Tünel Felaketleri* |
| manual_pptx | **yes** | unsettled (gap 0.003); arbiter reasoned KGM unit-price / payment rules → 2.4.3 |
| manual_xlsx | **yes** | unsettled (gap 0.001); arbiter reasoned Turkish road-tunnel count/length distribution → 1.4.2 |
| manual_image | no | strong agreement (gap 0.440, chunk vote 1.0) |

The arbiter was called only where deterministic signals disagreed, and in both XLSX and DOCX it
produced the correct answer where the embedding could not. This is the mitigation that keeps
classification usable despite the flat embedding.

## 16. Structure-Aware Chunk Quality (§29–§36)

**90 chunks total.**

| Role | TEXT | TABLE | FIGURE | SLIDE | SHEET | chunk quality |
| --- | --- | --- | --- | --- | --- | --- |
| crawler_pdf | 9 | 5 | 8 | – | – | PASS |
| manual_pdf | 2 | 1 | 27 | – | – | PASS |
| manual_docx | – | – | 17 | – | – | PASS |
| manual_pptx | – | – | 5 | 12 | – | PASS |
| manual_xlsx | – | – | – | – | 2 | **FAIL** |
| manual_image | 1 | – | 1 | – | – | PASS |
| **Total** | **12** | **6** | **58** | **12** | **2** | |

Every chunk carries `heading_path`, `page_start`/`page_end` (or `slide_number` / `sheet_name` /
`cell_range`), `source_elements`, `token_count`, `tokenizer`, `chunk_policy_version` and a
`provenance` block with `original_sha256`, `source_kind`, `format` and `evidence_level`.

* **§30 text chunks** — paragraph integrity preserved; heading paths real (e.g. `["Kocaeli Journal
  of Science and Engineering"]`); each chunk readable standalone.
* **§33 table chunks** — caption, page, structured JSON path and CSV path retained; the structured
  table stays authoritative and no summary overwrote numeric data.
* **§34 figure chunks** — figure id, page, caption, OCR text and provenance retained; no
  unsupported engineering interpretation (see §8 above).
* **§35 slide chunks** — one chunk per slide, `slide_number` preserved, `source_elements` a single
  `SLIDE000N`. No slide was mixed with an unrelated neighbour.
* **§36 sheet chunks** — the workbook did **not** collapse into one prose chunk. Each populated
  sheet became its own chunk with `sheet_name`, `cell_range` (`R4C4:R17C14`) and cell-addressed
  content (`D4: TÜM TÜNELLER İCMALİ | L4: …`). Structurally this is the best output in the pilot.

**The one chunking failure is the XLSX.** Both sheet chunks exceed the token policy —
1329 tokens (`CHUNK_OVER_MAX`, warning) and 1831 tokens (`CHUNK_OVER_HARD_MAX`, error) against
`max 1200 / hard_max 1500`. The chunker emits one chunk per sheet with no row-window splitting,
so `chunk_quality = FAIL` and **both chunks became embedding-ineligible**. A well-extracted,
GO-gated document therefore contributes nothing to retrieval. Policy was **not** retuned (§31).

## 17. Token Distribution (§32)

`TEXT_CHUNK` only, n = 12. Policy unchanged: target 850, min 250, max 1200, hard max 1500,
overlap 80, `structure-aware-v1`, tokenizer `unicode-lexical-v1`.

| count | min | p25 | median | p75 | mean | p95 | max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 12 | 1 | 411 | 568 | 748 | 578.0 | 986 | 997 |

* below minimum (250): **8.3 %** (1 chunk)
* above normal max (1200): **0 %**
* above hard max (1500): **0 %**

The single sub-minimum chunk is the image document's 1-token title chunk
(`'InvertBetonUygulaması'`). Note the `TEXT_CHUNK` sample is small (12) because four of the six
documents are figure-, slide- or sheet-dominated; the `SHEET_CHUNK` over-length problem above is
not visible in this table.

## 18. Multimodal Chunks & OCR Duplication (§37, §38)

| Metric | Result |
| --- | --- |
| exact duplicate chunk rate | **0.0 %** |
| near-duplicate chunk rate (≥0.90 intra-document) | **0.0 %** |
| figure-chunk text duplicating native text | **0 of 58** |
| `ocr_items` counted as native text | **0** |

No duplication flood. The native-vs-OCR hazard did not materialise: where a document had native
text (both PDFs, PPTX, XLSX) the figure OCR did not restate it, and where OCR text is the only
content (DOCX screenshots, 17 chunks) there was no native text to duplicate. OCR supplemented
rather than flooded.

## 19. Document Quality Gate (§39)

| Role | Decision | Reasons |
| --- | --- | --- |
| crawler_pdf | GO | — |
| manual_pdf | GO | — |
| manual_docx | GO | — |
| manual_pptx | **REVIEW** | `LOW_SECTION_CONFIDENCE` (0.45) |
| manual_xlsx | GO | — |
| manual_image | **REVIEW** | `OCR_EMPTY_TEXT_IMAGE` |

**GO 4 / REVIEW 2 / REJECT 0 / FAILED 0.** Both REVIEWs are truthful and were verified against
the sources. The one gate result that deserves scrutiny is `manual_pdf`: a **GO** carrying a
misclassified section (§12) — an incorrect GO, which §39 rates worse than a correct REVIEW. The
gate itself behaved as specified; the wrong section came from the classifier.

## 20. Staging (§40)

| Store | Before | After |
| --- | --- | --- |
| legacy `corpus/staging/` (CAN_*) | 122 | **122 (untouched)** |
| legacy `handoff/manifests/handoff_manifest.jsonl` | 122 rows | **122 rows (untouched)** |
| `corpus/staging/v2/` | 4 (earlier smoke test) | **8** (+4 pilot GO documents) |
| `corpus/promoted_v2/` | 0 | **0** |

Only GO documents were staged into v2. The two REVIEW documents were not staged.

## 21. Embedding-Ready Manifest (§41)

90 pilot rows in `audit/embedding_ready_manifest.jsonl` (plus 18 from the earlier synthetic smoke
test, which the manifest accumulates globally).

| Check | Result |
| --- | --- |
| chunk ids unique | **yes** (90/90) |
| document ids valid | yes |
| chunk types valid | TEXT / TABLE / FIGURE / SLIDE / SHEET |
| section ids valid | **0 invalid** |
| provenance present | **0 missing** |
| `embedding_text` non-empty for eligible chunks | **0 empty** |
| review-only evidence incorrectly eligible | **none** |

| Role | Gate | Rows | Eligible | Ineligible reason |
| --- | --- | --- | --- | --- |
| crawler_pdf | GO | 22 | 22 | — |
| manual_pdf | GO | 30 | 30 | — |
| manual_docx | GO | 17 | 16 | `TOO_SHORT` (1) |
| manual_pptx | REVIEW | 17 | **0** | `DOCUMENT_NOT_STAGED` |
| manual_xlsx | GO | 2 | **0** | `CHUNK_QUALITY_FAILED` |
| manual_image | REVIEW | 2 | **0** | `DOCUMENT_NOT_STAGED` |

**68 embedding-ready chunks.** The REVIEW documents are correctly excluded.

## 22. Defects Found and Fixed (§43)

### D1 — crawler bibliographic metadata was silently discarded

`cli._merge_provenance` wrote `{"kind": …, **item.provenance}` and dropped
`DiscoveredInput.crawler_record`. `metadata/enrich.py` prefers a crawler-manifest title over its
body-heading heuristic — correctly — but could never see the record, so **every**
`EXTERNAL_DISCOVERY` document fell through to `_first_heading`.

On the pilot's real journal PDF that produced `title = "Kocaeli University"` — the page-1 journal
masthead — asserted at confidence 0.9 with `inferred: false`, while the manifest carried the real
title, both authors and the year. It was also a dedup false-merge hazard (§10).

A first fix was incomplete: `_merge_provenance` *skips* an already-matching source entry, so a
bundle written by the older engine never gained the record. The final fix refreshes the matching
entry instead of skipping it, without blanking fields that are already present.

Verified on real data — title, authors and DOI now come from `crawler_manifest`.

### D2 — the crawler's publication year was ignored

`enrich.py` read only `published_date` / `date`; the handoff manifest carries `year`. The
document's `document_date` stayed `null` even though the manifest said `2021`. A bare year is
already an accepted `document_date` shape in the body-text fallback path, so the manifest year is
now consulted after the full-date fields. `document_date` is now `"2021"` from `crawler_manifest`.

**Regression tests:** `tests/ingest/test_crawler_metadata_provenance.py` (9 tests) covering
persistence, manual sources, idempotent re-merge, backfill of an older bundle, non-blanking, the
masthead-vs-manifest priority, and year handling.

**Full ingest suite after the fixes: 206 / 206 PASS** (197 before, +9 new).

## 23. Remaining Risks

1. **Flat embedding signal.** Mean top1–top2 margin 0.0066 over 66 sections. Section assignment
   currently depends on rule/chunk signals and the local arbiter. This is the single biggest risk
   to retrieval quality.
2. **One confident misclassification.** `manual_pdf` → `5.9.1` at 0.58 with gate GO. The failure
   mode — flat embedding plus a taxonomy gap producing a *confident* wrong answer — is more
   dangerous than a low-confidence REVIEW.
3. **Taxonomy coverage gap.** No ventilation / fire-safety section exists, yet tunnel fire safety
   is a real and well-represented topic in the source archive.
4. **XLSX sheet chunks exceed the hard token cap**, so structurally excellent spreadsheet
   extraction yields zero retrievable chunks.
5. **The v2 handoff contract drops the section hint.** `provisional_primary_section` is not in the
   manifest, so crawler classification work (here, a 0.95-confidence `2.4.1`) is discarded, and
   §25's override rule is untested on real data.
6. **Stale OOXML properties can outrank document content** (PPTX title `KAYA SINIFLANDIRMASI`).
7. **Small sample.** Six documents, one crawler document, one image, no legacy DOC/PPT/XLS, no
   scanned-only PDF, no crawler+manual same-source pair.

## 24. Recommendations

Captured only — none applied in this pilot (§44).

1. Evaluate the embedding model against the 66-section taxonomy before relying on it for
   retrieval; consider a domain-tuned or Turkish-aware model, or per-section centroid
   calibration. Do not tune during ingest work.
2. Add a confidence floor or a mandatory arbiter call when the fused top-1 gap is small **or** the
   embedding margin is below a threshold, so cases like `manual_pdf` become REVIEW rather than a
   confident GO.
3. Add a ventilation / fire-safety section to the book taxonomy, or an explicit
   `OUT_OF_SCOPE` outcome for documents no section fits.
4. Split `SHEET_CHUNK` by row windows to respect `hard_max_tokens`, preserving the header row and
   the `cell_range` provenance that already works well.
5. Ask PaperCrawler to carry `provisional_primary_section` (and its score) in the v2 handoff
   manifest, so the hint reaches the consumer and §25 can be exercised.
6. Prefer a document's own first slide/heading over an OOXML `dc:title` when the property is much
   older than the content or the two disagree strongly; record both.
7. Re-run this pilot with a wider set once the above land — include a scanned-only PDF, a legacy
   DOC/PPT/XLS, and the same source arriving via both crawler and manual channels.

## 25. Decision

| Verdict | Result | Basis |
| --- | --- | --- |
| **A. Unified Ingest Engine** | **GO** | 6/6 originals intact; all six formats processed meaningfully; UNSUPPORTED metadata = 0; false dedup = 0; classification fully traceable; quality gate correct; multimodal chunks structurally sound; chunk provenance valid; embedding-ready manifest valid; canonical unchanged |
| **B. Embedding / Classification Signal** | **CONDITIONAL_GO** | classification correct on 4/6 via rule/chunk/arbiter signals, but the embedding is FLAT (mean margin 0.0066) and produced one confident misclassification; model evaluation required before it is relied upon |
| **C. Qdrant / Retrieval Phase Readiness** | **CONDITIONAL_GO** | chunk quality good, manifest clean, no duplicate flood, metadata reliable after D1/D2 — but the embedding model must be evaluated first, and the XLSX sheet-chunk over-length gap should be closed so tabular documents are retrievable |

Canonical corpus: **UNCHANGED** (`6c49a13c…def0470`, 214/214). Canonical promotions: **0**.
Embeddings computed: **0**. Qdrant writes: **0**.
