# TunnelBookAI Recovery Chunk Embedding Gate

## Result

**RECOVERY CHUNKS — GO**

All 12 recovery chunks were inspected individually. No sampling.

## Counts

- Recovery chunks: **12/12**
- DOC000009: **3**
- DOC000041: **4**
- DOC000051: **5**

## Quality

- Readable (>=8 real words): **11/12**
- Glyph residue (`/Gxx` or `GxxGxx`): **0**
- Control-character corruption: **0**
- Duplicate recovery text: **0**
- Provenance failure: **0**
- Chunk IDs unique: **True**
- Collision with frozen canonical IDs: **0**

## BGE-M3 tokens (real tokenizer, `truncation=False`)

- min: **112** · median: **848** · max: **2916**
- Over 8192: **0**
- Effective model limit: **8192** · revision pin: `5617a9f61b028005a4858fdac845db406aefb181`

## Per-chunk

| chunk_id | doc | BGE tokens | glyph | ctrl | words | provenance | pages | table | heading |
|---|---|---|---|---|---|---|---|---|---|
| `DOC000009-R1-C0001` | DOC000009 | 777 | 0 | 0 | 218 | section_resolved | 1-5 | False | Newfoundland Fixed Link Pre-feasib |
| `DOC000009-R1-C0002` | DOC000009 | 918 | 0 | 0 | 145 | section_resolved | 1-5 | True | Assumptions: |
| `DOC000009-R1-C0003` | DOC000009 | 125 | 0 | 0 | 0 | section_resolved | 1-5 | True | $ |
| `DOC000041-R1-C0001` | DOC000041 | 448 | 0 | 0 | 115 | section_resolved | 1-1 | False | Estimate of annual operating costs |
| `DOC000041-R1-C0002` | DOC000041 | 112 | 0 | 0 | 46 | section_resolved | 2-2 | False | Sayfa 2 |
| `DOC000041-R1-C0003` | DOC000041 | 479 | 0 | 0 | 130 | section_resolved | 3-3 | False | Sayfa 3 |
| `DOC000041-R1-C0004` | DOC000041 | 292 | 0 | 0 | 94 | section_resolved | 4-4 | False | Sayfa 4 |
| `DOC000051-R1-C0001` | DOC000051 | 2832 | 0 | 0 | 560 | section_resolved | 1-1 | False | Tünel Haritası 2024_KGMWEB |
| `DOC000051-R1-C0002` | DOC000051 | 2662 | 0 | 0 | 158 | section_resolved | 1-1 | False | Tünel Haritası 2024_KGMWEB |
| `DOC000051-R1-C0003` | DOC000051 | 2916 | 0 | 0 | 322 | section_resolved | 1-1 | False | Tünel Haritası 2024_KGMWEB |
| `DOC000051-R1-C0004` | DOC000051 | 2231 | 0 | 0 | 511 | section_resolved | 1-1 | False | Tünel Haritası 2024_KGMWEB |
| `DOC000051-R1-C0005` | DOC000051 | 1305 | 0 | 0 | 326 | section_resolved | 1-1 | False | Tünel Haritası 2024_KGMWEB |

## Notes

- `DOC000009-R1-C0003` has 0 real words: an empty table skeleton of symbol placeholders (`$`, `!"`, `%`, `&`) plus an image placeholder, from a graphics-only source page. No glyph or control residue - this is a genuinely blank page, not corruption. Kept as `eligible_low_content`.
- `DOC000051` was inspected closely as required. It is a Turkish highway tunnel/pass registry: mountain-pass names with elevations (`Tendürek Geç. 2644`, `Ilgazdağı Geç. 1850`), KGM road-segment codes (`340-06`, `795-02`) and 645 distinct place/tunnel names. This is genuine, source-derived content and is accepted; it is not rejected for being registry rather than prose.
- `DOC000051-R1-C0001` is dominated by repeated `!(` map-marker symbols alongside real names. Genuine map content, but low semantic signal per token.
- Numeric preservation was verified independently: decoded cost tables satisfy rate x quantity = total across 14/14 equations.
- Tables in `DOC000009-R1-C0002` are structurally valid Markdown with header and separator rows intact.

## Decision

**RECOVERY CHUNKS — GO**
