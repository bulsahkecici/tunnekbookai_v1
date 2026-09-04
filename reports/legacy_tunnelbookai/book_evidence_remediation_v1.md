# Book Evidence Remediation v1

## Executive Decision

**BOOK EVIDENCE REMEDIATION V1 + PIPELINE EXTRACTOR V1.1 - CLOSED / GO**

Extractor `tunnelbook-book-pipeline-extractor-v1.1`, parent `tunnelbook-book-writing-pipeline-v1`. Drafting stays disabled and all three sections remain **NOT_READY**. That is the honest outcome, not a failure of the gate: the machinery is now correct, and what it shows is that the pilot evidence does not support a chapter yet.

- 159 pilot notes in, 131 remediated notes out
- 39 claims dropped as NON_PROPOSITION - they assert nothing and never should have been notes
- SUPPORTED 18, PARTIALLY_SUPPORTED 14, INSUFFICIENT_EVIDENCE 99
- 18 citation-ready claims across three sections
- 209/209 regression cases pass; 0 generation calls, 0 retrieval calls, Qdrant 5992 -> 5992, 0 writes

## Why Remediation Was Needed

The pilot manual evidence audit read all 159 notes against their evidence and found that 68 notes marked SUPPORTED contained only 15 that were demonstrably supported. Reading found the numbers; it also found *why*, and the why was structural:

1. **Materiality was decided on text that still contained citation handles.** `_is_material` asked whether a unit contained a number, of a string that still read `* Püskürtme Beton [E001]`. The `001` is a pointer to evidence, not a measurement, and it promoted a bare noun phrase into a factual note.
2. **A label with a citation is still a label.** "Püskürtme Beton", "Çelik İksa", "Temel Kiriş Betonu" cannot be true or false. Some carried SUPPORTED/high.
3. **Compound claims were credited whole.** Q-02-1-06-N06 asserts stability, watertightness and operating economy; only the operating-economy clause is carried by the cited span, and v1 marked the note SUPPORTED.
4. **Derived numbers rode along as source-stated ones.** The 150 mm in "15 cm'yi (150 mm)" was computed by the generator; no source states it.

### Before and after

| | Book Pipeline v1 | Manual audit v1 | Remediation v1 |
|---|---|---|---|
| notes | 159 | 159 audited | 131 |
| SUPPORTED | 68 | 15 | 18 |
| PARTIALLY_SUPPORTED | 0 | 15 | 14 |
| INSUFFICIENT_EVIDENCE | 91 | 129 | 99 |
| not a proposition at all | not representable | not representable | 39 |

**These columns do not mean the same thing, and comparing them naively would mislead.** v1's 68 SUPPORTED is a machine verdict on whole notes. The audit's 15 is a human verdict on the same 159 notes. Remediation's number counts a different population: 39 claims that assert nothing have left it, 9 of the 14 compound notes have become independent children, and support is decided clause by clause rather than note by note. The one comparison that is like-for-like is the direction of travel on the original 159: no claim gained support that a human reading had denied it, except through the recorded upgrade gate, whose every use is listed in `literal_span_remediation_v1.jsonl`.

## Frozen Inputs

| Input | SHA-256 |
|---|---|
| manual note audit (159 rows) | `e8ae6cdbbad372abfa8c3cd6538d23e0…` |
| manual clause audit (249 rows) | `b33b3f21e86b572b4fcf950ef57e2496…` |
| audit manifest | `66c807e131d7a10819d87c724afff8c4…` |

Evidence text comes from the frozen `data/chunks*` files; packet-local `[E###]` identity is rebuilt from `data/production/generation_audit_v1.jsonl`, whose ordered `retrieved_chunk_ids` resolve `E00k` without any retrieval. Manual adjudication is treated as authoritative throughout.

## Pipeline Extractor v1.1

`tunnelbook-book-pipeline-extractor-v1.1` is an extractor revision, not a new pipeline. It changes materiality detection, proposition extraction, clause decomposition, numeric verification, cross-lingual representation, note construction, support aggregation, readiness inputs and conflict candidate generation - and nothing else. Retriever v1, Context v1, Prompt v5, Output Contract v1.1, the Production Grounded Generator and Evidence Note Contract v1 are imported read-only or not at all.

It deliberately does not import `scripts/36_`: doing so would load the retrieval and context stack. Frozen identities are verified by reading the pinned SHA constants out of that file textually, so this module cannot retrieve or generate even by accident.

## Materiality Bug

`strip_handles()` now runs before every materiality, numeric and proposition test. Citation-handle digits can no longer make anything material. The regression suite pins this in five shapes, including `Kaya Bulonu [E100][E200][E300]` - nine digits, still no assertion - and the control `Püskürtme beton kalınlığı 15 cm'dir [E001]`, which must survive.

## Bare Enumeration Labels

A unit is a proposition when it contains a predicate: a Turkish copular or finite-verb suffix, an infinitive predicate, a listed verb, an English copula/modal/verb, or a measured value with its unit. Token count and digits decide nothing.

Two ambiguities cost real accuracy and are handled explicitly:

- The Turkish third-person plural `-lar/-ler` is dropped from the suffix family, because "kriterler" (plural noun) and "önlerler" (verb) are indistinguishable by suffix. Plural verb forms are covered by an explicit lexicon instead. Without this, "*3. Genel Proje ve Ekonomik Kriterler**" reads as an assertion.
- The bare necessitative `-malı/-meli` is dropped for the same reason: it is identical to the derivational adjective `-ma+lı`, and "C1 Grubu (Kaya patlamalı)" was being read as a claim - which then cost the rock class when the clause was split. Written necessitatives here always carry the copula (`-malıdır`) and are matched by that family.
- In English, a participle inside a title-case noun phrase is an adjective: "Steel Fibre Reinforced Shotcrete" names a material and is NON_PROPOSITION.

39 of the 159 pilot claims are NON_PROPOSITION: all 28 that the manual audit flagged `narrow_claim`, plus 11 the audit had classified otherwise - five bare labels (including Q-02-1-01-N04 "Süren (Boru veya Demir Çubuk)", which the audit had left as `retain_supported`), five markdown headings and one list lead-in. NON_PROPOSITION exists only at extraction time and prevents note creation; Evidence Note Contract v1 never sees it and is unmodified.

## Proposition Reconstruction

37 of the 39 dropped fragments sit under a parent lead-in that does assert something about them. Each is restated - "Püskürtme Beton" under "**Birincil Destekleme Sistemi:** … Bu sistemin elemanları şunlardır:" becomes "Püskürtme Beton, Birincil Destekleme Sistemi elemanlarından biridir." - and recorded with `proposition_origin = parent_child_reconstruction` and `requires_support_validation = true`.

Reconstruction is authoring, so it earns nothing. Each reconstructed claim is then validated by exactly the same clause machinery as every other clause - there is deliberately no bespoke "membership" check, because a special-case validator for reconstructions would be a second, looser standard of support. **0 of 37 reconstructions reached even PARTIALLY_SUPPORTED.** Every one of them is recorded in the remediation queue, with its parent statement and its reconstruction reason, and produces no note.

## Clause Decomposition

195 clauses from 131 notes. Splitting happens on sentence boundaries, semicolons, contrastive connectives, coordinated purpose lists and comma-parallel assertions - but only when every resulting unit is independently truth-evaluable. Four guards, each of which caught a real bad split during development:

- **Balanced brackets.** Splitting inside `(e.g., shotcrete)` produces debris, not claims.
- **No leading subordinator.** "which reduces shrinkage cracking" is not a proposition.
- **A subject must survive.** "maksimum 100 mm olmalıdır" left its subject in the other half of the sentence; crediting it would evidence a claim nobody made. The short-numeric exemption applies only to parts that keep a label head.
- **Conditions travel.** "B1 Sınıfı: Üst yarı kazısında 2,0-3,0 m, alt yarıda 4,0 m" makes two claims, and both hold only for class B1, so the head is repeated onto each part or the split does not happen. Sentence splitting also refuses to break after a roman-numeral enumerator, which was silently deleting the rock class from "III. Sınıf (Orta kaya): …".

## Q-02-1-06-N06 Regression

The mandatory case. v1.1 decomposes it deterministically into three clauses and preserves the audited verdict for each:

| Clause | Proposition | Status |
|---|---|---|
| Q-02-1-06-N06-C01 | Bu elemanlar, tünelin duraylılığını sağlamak açısından gereklidir. | **UNSUPPORTED** |
| Q-02-1-06-N06-C02 | Bu elemanlar, su geçirimsizliğini temin etmek açısından gereklidir. | **UNSUPPORTED** |
| Q-02-1-06-N06-C03 | Bu elemanlar, işletme ekonomisi (sürtünmenin azalması) açısından gereklidir. | **SUPPORTED** |

The note is split into three children with independent evidence and status; `Q-02-1-06-N06-S03` is SUPPORTED and the other two are INSUFFICIENT_EVIDENCE. There is no note that carries all three propositions and a single SUPPORTED status. This is enforced by a test, not only by the data.

A design decision worth stating: where a v1.1 clause is **equivalent** to a clause the auditor read, the manual verdict stands and the lexical heuristic does not get to re-decide it. Where a v1.1 clause is **finer** than what the auditor read as one clause, the manual verdict becomes a ceiling and the weaker of the two applies. Without that distinction, v1.1's stricter modality rule would have downgraded this note's supported clause - replacing a human reading with a heuristic, which is what the audit exists to correct.

## Literal Span Remediation

All 81 `needs_manual_span` notes processed, using only the frozen cited chunks. No retrieval, no generation.

| Decision | Notes |
|---|---|
| `dropped_non_proposition` | 5 |
| `retain_insufficient` | 73 |
| `span_attached` | 3 |

3 new spans attached. An upgrade above the audited verdict is deliberately harder than ordinary support: it needs a single verbatim span at ≥0.60 clause-token coverage that carries every number the clause states, its modality, and - where the clause is condition-bearing - the condition itself within ±600 characters in the source.

Candidate upgrades the gate refused, by which condition failed:

| Blocked by | Clauses |
|---|---|
| `computed_not_supported` | 22 |
| `coverage_below_upgrade_threshold` | 6 |
| `condition_not_bound_in_source` | 3 |

The 3 blocked by condition binding are the ones worth naming: a 2,0-3,0 m advance figure appearing somewhere in a document is not evidence for a claim about rock class B1, however verbatim the match.

**Method, stated plainly.** These upgrades are machine-verified verbatim against the frozen cited chunk, not re-read end to end by a human. The reading in this pass went into the 11 cross-lingual mappings and the 2 numeric defects. Most of the queue - 73 notes - correctly stays INSUFFICIENT_EVIDENCE. No paraphrase mappings were authored, so a claim that is semantically supported with no contiguous span remains unsupported and visible as a gap.

## Cross-Lingual Mapping

All 11 cross-lingual notes processed into 29 clause-level mappings, each authored by reading the claim beside its cited chunk. Nothing here was produced by string matching; every `source_span` is copied verbatim from the frozen chunk and re-verified at run time, so an invented quote cannot survive.

| Mapping status | Clauses |
|---|---|
| FAITHFUL | 16 |
| PARTIAL | 5 |
| NOT_SUPPORTED | 8 |

Two findings are worth naming:

- **A moved threshold.** Q-02-3-01-N03 claims "below 1.5 the conventional method is appropriate". The source says *lower than 1*; 1.5 is the trade-off limit. Translation may change language, not a number - the clause is NOT_SUPPORTED.
- **A moved attribution.** Q-02-1-07-N03 credits the waterproofing membrane with preventing hydrostatic pressure. The Turkish source attributes that to the protective felt/drainage layer. Re-attributing it would be a new fact, so that clause is NOT_SUPPORTED while the chemical-protection clause beside it is FAITHFUL.

Cross-lingual clauses can never be upgraded by lexical overlap; a mapping is the only route to support, and an unmapped cross-lingual clause is UNSUPPORTED by construction.

The decomposition of a cross-lingual note is the authored mapping itself. Letting the lexical splitter decide those clauses briefly made Q-02-3-02-N05 come out SUPPORTED: one mapped clause was FAITHFUL, the unmapped remainder was invisible, and the note inherited the support of the half that mapped.

## Numeric Remediation

80 numeric clause-facts audited value by value. Every value carries its unit, range, minimum, maximum, condition, source span and whether the source stated it.

- **No automatic unit conversion.** 4 values are parenthetical restatements in another unit. They are stored with `derived = true` and `source_stated = false`, and a note carrying one can never be citation-ready. Q-02-2-04-N06's 150 mm is the canonical case: the source states 15 cm and nothing else.
- **Values absent from evidence make a clause UNSUPPORTED however well its words match.** Q-02-2-01-N04 asserts 360 kg/m³ and 400 kg/m³; neither occurs in the cited evidence.
- The converter also understands ranges written with "to"/"ile", which is how "4 to 16 inches (100 to 400 mm)" previously leaked 400 mm through as a source-stated figure.

Both historically known numeric defects remain contained: neither note is SUPPORTED and neither is citation-ready.

## Requirements / Modality

Modality detection is now suffix-anchored (`-malıdır`, `-melidir`, `-mamalıdır`, `-memelidir`, `-meyecektir`) rather than a fixed list of verbs, so "tamamlanmalıdır" is recognised as exactly as normative as "olmalıdır". A span that does not carry the clause's modality cannot fully support it, and no modality is ever strengthened: nothing is upgraded from *should* to *must*, or *önerilir* to *zorunlu*.

## Conditions

Support is bound to conditions in two places: the splitter repeats a label head onto every part, and an upgrade must find the condition near the span in the source. A figure stated for rock class B1, for the dry-mix system, or for one tunnel type does not become a generic figure by being quoted without its condition.

## Conflict Candidate Improvements

v1 produced 30 candidates: 29 false positives, 1 context difference, 0 true conflicts. It matched on unit alone and treated a chunk as "about" a variable if two loose keywords appeared anywhere in it - which is how a cover thickness, a specific surface in cm²/g and a lap length ended up in one "çimento dozajı / cm" bucket.

v1.1 requires the concept next to the value, rejects compound units, and buckets on a condition signature built from jurisdiction, method, ground class and minimum/maximum/average marking. Candidates fall to 8.

This is still a deterministic candidate generator and nothing more. It does not adjudicate, and no model is asked to. Because the pilot contains zero true conflicts, recall cannot be measured - the only measurable improvement is the reduction in candidates that manual reading had already rejected, and that is all this section claims.

## Remediated Evidence Notes

| | Notes |
|---|---|
| SUPPORTED | 18 |
| PARTIALLY_SUPPORTED | 14 |
| INSUFFICIENT_EVIDENCE | 99 |
| dropped as NON_PROPOSITION | 39 |

Every note carries `parent_note_id`, `parent_note_sha`, `revision = 2`, its clause decomposition with per-clause status and status source, its evidence refs, source keys and manual audit refs. Originals and audited revision-1 artifacts are untouched.

Aggregation follows the strict reading: SUPPORTED needs every material clause supported, and PARTIALLY_SUPPORTED needs at least one *fully* supported clause. A note whose clauses are all merely partial has no proposition adequately supported and stays INSUFFICIENT_EVIDENCE. The looser reading would have promoted dozens of notes on no new evidence.

## Remediated Claim Ledgers

18 claims are citation-ready. The gate is narrow by design: SUPPORTED status, every material clause supported, evidence refs complete, source keys resolved, no unsupported unit conversion, and any cross-lingual mapping manually completed. PARTIALLY_SUPPORTED notes stay in the bundle and may inform the writing, but may never be cited as whole claims.

## P0 Gap Classification

| Section | P0 question | Gap classes |
|---|---|---|
| SEC-02-1 | Q-02-1-01 | EXTRACTION_FAILURE, SPAN_MAPPING_FAILURE |
| SEC-02-1 | Q-02-1-02 | EXTRACTION_FAILURE |
| SEC-02-2 | Q-02-2-01 | GENERATOR_SYNTHESIS_DEFECT, SPAN_MAPPING_FAILURE |
| SEC-02-2 | Q-02-2-02 | SPAN_MAPPING_FAILURE |
| SEC-02-3 | Q-02-3-01 | CROSS_LINGUAL_MAPPING_FAILURE, SPAN_MAPPING_FAILURE |
| SEC-02-3 | Q-02-3-02 | CROSS_LINGUAL_MAPPING_FAILURE, EXTRACTION_FAILURE, SPAN_MAPPING_FAILURE |

`RETRIEVAL_GAP` and `CORPUS_GAP` are recorded and deliberately left unsolved. Retrieval expansion is a separate controlled phase, and running new retrieval here to close a gap would be that phase wearing this one's name.

## SEC-02-1

**NOT_READY**

- notes 28 (SUPPORTED 10, PARTIAL 1, INSUFFICIENT 17)
- clauses 36 (SUPPORTED 13, PARTIAL 12, UNSUPPORTED 11)
- citation-ready claims 10
- dropped as NON_PROPOSITION 22
- P0 questions with a citation-ready claim: 1/3

  - P0 questions without a citation-ready claim: ['Q-02-1-01', 'Q-02-1-02']
  - unsupported clauses under P0 objectives: 2

## SEC-02-2

**NOT_READY**

- notes 32 (SUPPORTED 2, PARTIAL 1, INSUFFICIENT 29)
- clauses 42 (SUPPORTED 3, PARTIAL 13, UNSUPPORTED 26)
- citation-ready claims 2
- dropped as NON_PROPOSITION 3
- P0 questions with a citation-ready claim: 1/2

  - P0 questions without a citation-ready claim: ['Q-02-2-02']
  - unsupported clauses under P0 objectives: 5
  - unresolved numeric clauses under P0 objectives: 2

## SEC-02-3

**NOT_READY**

- notes 71 (SUPPORTED 6, PARTIAL 12, INSUFFICIENT 53)
- clauses 117 (SUPPORTED 24, PARTIAL 23, UNSUPPORTED 70)
- citation-ready claims 6
- dropped as NON_PROPOSITION 14
- P0 questions with a citation-ready claim: 2/2

  - unsupported clauses under P0 objectives: 21
  - cross-lingual clauses under P0 objectives without a faithful mapping: 11

## Recomputed Readiness

| Section | Readiness |
|---|---|
| SEC-02-1 | **NOT_READY** |
| SEC-02-2 | **NOT_READY** |
| SEC-02-3 | **NOT_READY** |

Recomputed from scratch; nothing inherited from the v1 or audited bundles. Readiness sees what extraction dropped as well as what it kept, so a section cannot become ready by having its failures deleted. No threshold was moved to produce a ready section, and none became ready.

## Remaining Evidence Gaps

- Same-language paraphrase support has no representation yet: a claim genuinely carried by the source but not by any contiguous span stays INSUFFICIENT_EVIDENCE.
- Literal-span upgrades are machine-verified, not human-re-read.
- The conflict detector's recall is unmeasurable against a pilot containing no true conflict.
- Source authority is still unweighted.
- Every remaining P0 gap classifies as CROSS_LINGUAL_MAPPING_FAILURE, EXTRACTION_FAILURE, GENERATOR_SYNTHESIS_DEFECT, SPAN_MAPPING_FAILURE. No `RETRIEVAL_GAP` or `CORPUS_GAP` was identified in this pass, so nothing here is waiting on retrieval expansion; the classes stay available because the next phase will need them.

## Regression Suite

`data/evaluation/book_pipeline_extractor_v1_1_regression.jsonl` - 209 cases, 209 passing, 0 failing.

- clause_decomposition: 8
- materiality: 197
- numeric: 4

The suite pins the whole pilot population, not only the memorable examples, and it is built to fail in both directions - labels that must not become facts, and propositions that must not be lost. It caught three real defects during development that hand inspection had missed: an English participle making a title-case material name into a proposition, a contrastive split being rejected as a fragment, and a converted range ("4 to 16 inches (100 to 400 mm)") leaking 400 mm through as a source-stated figure.

## Frozen Integrity

| Frozen input | Unchanged |
|---|---|
| Retriever v1 | yes |
| Prompt v5 | yes |
| Output Contract v1.1 | yes |
| Production Grounded Generator v1 | yes |
| Evidence Note Contract v1 | yes |
| Book Pipeline v1 | yes |
| Pilot Manual Evidence Audit v1 | yes |
| Context v1 | yes (first record) |
| audited notes SEC-02-1 | yes |
| audited ledger SEC-02-1 | yes |
| audited bundle SEC-02-1 | yes |
| original notes SEC-02-1 | yes (first record) |
| audited notes SEC-02-2 | yes |
| audited ledger SEC-02-2 | yes |
| audited bundle SEC-02-2 | yes |
| original notes SEC-02-2 | yes (first record) |
| audited notes SEC-02-3 | yes |
| audited ledger SEC-02-3 | yes |
| audited bundle SEC-02-3 | yes |
| original notes SEC-02-3 | yes (first record) |
| manual note audit | yes |
| manual clause audit | yes |
| conflict candidates v1 | yes |
| duplicate audit | yes |
| chunks | yes (first record) |
| recovery chunks | yes (first record) |
| production audit log | yes (first record) |

Qdrant `tunnelbook_dense_v1`: 5992 points before, 5992 after, 0 writes. Generation calls 0, retrieval calls 0.

## Tests

- `tests/test_book_pipeline_extractor_v1_1.py` - materiality, bare labels, parent-context reconstruction, clause decomposition, compound claims, numerics, derived conversions, modality, conditions, cross-lingual, thresholds.
- `tests/test_book_evidence_remediation_v1.py` - queue completeness, provenance, no invented spans or refs, P0 gap visibility, readiness honesty, frozen integrity, drafting disabled.

## Final Decision

**CLOSED / GO.** The extractor and remediation machinery are correct. Readiness is unchanged at NOT_READY for all three sections, and that is the point: GO means the machinery can be trusted, not that a section may be written. Drafting stays disabled.

Next phase: **P0 Evidence Gap Resolution v1**, since no section is ready. Not drafting.
