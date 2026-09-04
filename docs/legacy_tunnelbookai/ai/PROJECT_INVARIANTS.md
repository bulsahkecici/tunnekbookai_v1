# TunnelBookAI — Project Invariants

Standing rules. These do not change between phases. Facts about *state* belong
in `CURRENT_STATE.md`, not here.

## Evidence

- Evidence-only. Every asserted fact traces to a corpus source.
- Unresolved is an allowed outcome. Blank beats guessed.
- Wrong metadata is worse than blank metadata.
- No hallucinated repair. A gap is reported, never filled in.
- No web or external evidence unless a phase explicitly authorizes it.
- General model knowledge is not evidence.
- Book pipeline source policy is `corpus_only`.

## Provenance

- `document_id`, source SHA and provenance relationships are immutable.
- `source_key` is the stable book-level source identity.
- Packet-local `[E###]` handles are retrieval-packet addresses. They are never
  stable book references and never appear in visible prose.
- Bibliography metadata is registry-backed only. A null renders as an omission,
  never as a plausible guess.

## Frozen state

- Frozen upstream artifacts are immutable: corpus, normalized documents, chunks,
  embeddings, Retriever v1, Context v1, Prompt v5, Output Contract v1.1,
  Production Grounded Generator v1, Evidence Note Contract v1, Book Pipeline v1,
  Extractor v1.1, P0 artifacts, SEC-02-2 readiness and composition-safety
  artifacts, and the drafting / citation / draft-validation contracts.
- A formal GO/NO-GO gate stays frozen once authored. Later phases add new
  versioned artifacts; they do not mutate an existing one in place.
- Qdrant is read-only unless a phase explicitly authorizes a write.
- No Prompt v6 without separate approval.

## Validation

- Never weaken a validator, threshold, fixture or failure code to obtain a pass.
- Never rename or remove an existing failure code.
- No silent auto-repair. A failed unit must remain visible as a failure.
- Rejected output is never released or rendered.
- Drafting is permitted only for a section marked `READY_FOR_DRAFT`.

## Working method

- Full corpus and full repository scans are prohibited by default.
- Targeted reads and targeted tests are the default; breadth needs a reason.
