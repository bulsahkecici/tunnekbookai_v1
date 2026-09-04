# SEC-02-2 TECHNICAL DRAFT AUDIT V1 + BOOK STYLE CONTRACT V1

**CLOSED / NO-GO.** OC-01 is closed. Book Style Contract v1 is CLOSED / GO as a contract, but
the accepted Architecture V2 Pilot #2 draft is not technically or stylistically releasable.
It remains immutable, labelled `PILOT_DRAFT_ACCEPTED`, and not final manuscript.

## OC-01

The historical zero-prose test was re-scoped, not removed or weakened. It now permits exactly the
named Pilot #2 Markdown file and verifies its path, SHA256, accepted gate, accepted validator,
pilot label and non-release status. Any other Markdown, DOCX or TEX artifact under `data/book/`
still fails. The decision and future-change rule are recorded in
`data/book/contracts/prose_artifact_control_contract_v1.json`.

## Technical audit — NO-GO

All 19 rendered units and 16 claims were checked against only their 12 cited source keys in
DOC000047, DOC000087 and DOC000236. Literal figures and units match; there is no numeric drift or
unsupported factual addition. Six blocking and two advisory findings remain:

- C-004 and C-005 omit their source's wet-system application scope.
- C-012 omits its source's repair-work scope and reads as a general inter-layer rule.
- P0-008 replaces the named crushed/squeezing/swelling rock cases with vague “belirli” conditions.
- The dosage claim set omits the cited 500 kg/m³ maximum and cement-type consequence.
- Cement claims cite a source key rendered under the unrelated “Tokluk İndeksi” heading.
- C-002's qualifier makes the C25/30 class, rather than the 22.5/25.5 MPa values, the grammatical
  subject of “acceptance criterion”.

Factual: FAIL. Citation: FAIL. Language: PASS WITH FINDINGS. Condition: FAIL despite frozen
validator coverage of 100%. Qualifier: PASS WITH FINDINGS.

## Book Style Contract v1 — CLOSED / GO

The contract preserves one claim slot per material unit, claim-owned citations, numeric fidelity
and the ban on model or post-render style passes. Coherence must be deterministic: frozen section
and subsection headings, semantic paragraph groups, general-to-specific ordering, immediate scope
and qualifier placement, construction-sequence order, terminology control and redundancy
suppression. Cross-claim connectives remain forbidden unless a frozen relationship licenses them.

Pilot prose fails this contract: bare identifier title, no subsection headings, isolated note-like
paragraphs, an orphan fragment, duplicated dosage summary, inconsistent katman/tabaka terminology
and an ambiguous qualifier sentence.

## Integrity and accounting

0 generation calls, 0 model style calls, 0 retrieval calls, 0 Qdrant writes, 3 cited corpus
documents read, 0 validators/thresholds/failure codes changed, 0 claims/lexicons/glosses changed,
0 frozen or Pilot artifacts modified, 0 drafts released. Pilot #1 remains REJECTED; Architecture
V1 remains retired.

Next: SEC-02-2 TECHNICAL CLAIM SCOPE + CITATION ALLOCATION REMEDIATION V1.
