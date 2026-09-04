#!/usr/bin/env python3

import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


EVIDENCE_CONTRACT_VERSION = "SENTENCE_ID_V2"
EDITORIAL_POLICY_VERSION = "DETERMINISTIC_EDITORIAL_GATE_V1"

VALID_STATUSES = {
    "SUPPORTED",
    "NARRATIVE_SYNTHESIS",
    "PARTIALLY_SUPPORTED",
    "UNSUPPORTED",
    "SCOPE_LEAKAGE",
    "UNSUPPORTED_SOURCE_IDENTITY",
    "REDUNDANCY",
}

# Statuses that are never allowed to reach freeze. NARRATIVE_SYNTHESIS is
# excluded here on purpose: it is a bounded-synthesis status, not a
# rescue path, and its safety is enforced separately by
# _narrative_synthesis_violations() rather than by a blanket ban.
FREEZE_BLOCKING_STATUSES = VALID_STATUSES - {
    "SUPPORTED",
    "NARRATIVE_SYNTHESIS",
}

# Ranking/superlative language a narrative-synthesis sentence may not
# introduce unless the same phrase already appears in its grounding claims.
_SUPERLATIVE_PATTERNS = (
    "en eski", "en uzun", "en büyük", "en önemli", "en derin", "en yüksek",
    "dünyanın ilk", "tarihin ilk", "ilk kez", "ilk defa", "ilkin",
)

# Causal-assertion language a narrative-synthesis sentence may not
# introduce unless the same phrase already appears in its grounding claims.
_CAUSAL_PATTERNS = (
    "bu nedenle", "bu sayede", "bu yüzden", "sonucunda", "nedeniyle",
    "sayesinde", "bunun sonucu",
)


def _narrative_synthesis_violations(
    sentence_text: str,
    claim_texts: list[str],
) -> list[str]:
    """
    Deterministic contract check for the NARRATIVE_SYNTHESIS status.

    A narrative/transition sentence may only recombine information already
    present in its own supporting claims. It may not introduce a new date,
    number, proper noun, superlative/ranking claim, or causal assertion
    that isn't already grounded in those same claims. This is what stops
    NARRATIVE_SYNTHESIS from being usable to rescue an otherwise
    UNSUPPORTED, PARTIALLY_SUPPORTED, or SCOPE_LEAKAGE sentence: any such
    sentence carries facts the claims don't contain, so it fails here.
    """

    combined = " ".join(claim_texts)
    combined_fold = combined.casefold()

    violations: list[str] = []

    claim_numbers = set(re.findall(r"\d+", combined))
    for number in re.findall(r"\d+", sentence_text):
        if number not in claim_numbers:
            violations.append(f"NEW_NUMBER:{number}")

    # A single sentence is passed in per call (one sentence_audit row).
    # The first word of that sentence is sentence-initial capitalization,
    # not evidence of a proper noun, so it is excluded from this check.
    tokens = re.findall(r"[A-ZÇĞİÖŞÜ][a-zçğıöşü]+", sentence_text)
    for word in tokens[1:]:
        if word.casefold() not in combined_fold:
            violations.append(f"NEW_PROPER_NOUN:{word}")

    sentence_fold = sentence_text.casefold()

    for phrase in _SUPERLATIVE_PATTERNS:
        if phrase in sentence_fold and phrase not in combined_fold:
            violations.append(f"SUPERLATIVE_OR_RANKING:{phrase}")

    for phrase in _CAUSAL_PATTERNS:
        if phrase in sentence_fold and phrase not in combined_fold:
            violations.append(f"CAUSAL_CLAIM:{phrase}")

    return violations


class AuditContractError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AuditContractError(
            f"INVALID_JSON: {path}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise AuditContractError(
            f"JSON_ROOT_NOT_OBJECT: {path}"
        )

    return data


def _book_body(draft: str) -> str:
    lines = []

    for raw in draft.splitlines():
        s = raw.strip()

        if not s:
            continue

        if s.startswith("#"):
            continue

        if s == "---":
            continue

        if s.startswith("Section ID:"):
            continue

        if s.startswith("Status:"):
            continue

        if s.startswith("Evidence limitations:"):
            continue

        lines.append(s)

    return " ".join(lines)


def split_sentences(text: str) -> list[str]:
    """
    Deterministic splitter for Turkish technical prose.

    Protects:
    - M.Ö. / M.S.
    - decimal values such as 4.5
    - ordinal century notation such as 19. yüzyıl
    - leading enumerated list markers such as "11. Bölge ..."
    """

    text = re.sub(r"\s+", " ", text).strip()

    protected = text

    protected = protected.replace(
        "M.Ö.",
        "M<DOT>Ö<DOT>",
    )
    protected = protected.replace(
        "M.S.",
        "M<DOT>S<DOT>",
    )

    # Common abbreviations that must not terminate sentences.
    abbreviations = (
        "St.",
        "Dr.",
        "Prof.",
        "Doç.",
        "Sn.",
        "No.",
        "Bkz.",
        "örn.",
        "Örn.",
        "vb.",
        "vs.",
        "K.K.",
    )

    for abbreviation in abbreviations:
        protected = protected.replace(
            abbreviation,
            abbreviation[:-1] + "<DOT>",
        )

    # Decimal numbers: 4.5
    protected = re.sub(
        r"(?<=\d)\.(?=\d)",
        "<DOT>",
        protected,
    )

    # 19. yüzyıl
    protected = re.sub(
        r"\b(\d{1,2})\.(?=\s+yüzyıl)",
        r"\1<DOT>",
        protected,
        flags=re.IGNORECASE,
    )

    # Leading enumerated list markers, e.g. "11. Bölge Müdürlüğü ..."
    # A short number at the very start of the text, or right after a
    # previous sentence boundary, is a list-item marker rather than a
    # sentence-ending number and must not be split from what follows.
    protected = re.sub(
        r"^(\d{1,2})\.(?=\s)",
        r"\1<DOT>",
        protected,
    )
    protected = re.sub(
        r"(?<=[.!?]\s)(\d{1,2})\.(?=\s)",
        r"\1<DOT>",
        protected,
    )

    parts = re.split(
        r'(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9])',
        protected,
    )

    sentences = []

    for part in parts:
        sentence = (
            part
            .replace("<DOT>", ".")
            .strip()
        )

        if sentence:
            sentences.append(sentence)

    return sentences


def build_sentence_map(
    draft_path: Path,
    output_path: Path,
    section_id: str,
) -> dict:

    if not draft_path.exists():
        raise AuditContractError(
            f"DRAFT_NOT_FOUND: {draft_path}"
        )

    draft = draft_path.read_text(
        encoding="utf-8"
    )

    body = _book_body(draft)
    sentences = split_sentences(body)

    if not sentences:
        raise AuditContractError(
            "NO_SENTENCES_EXTRACTED"
        )

    data = {
        "section_id": section_id,
        "draft_path": str(draft_path),
        "draft_sha256": sha256_file(draft_path),
        "sentence_count": len(sentences),
        "sentences": [
            {
                "sentence_id": f"S{i:03d}",
                "text": sentence,
            }
            for i, sentence in enumerate(
                sentences,
                1,
            )
        ],
    }

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    return data


def build_evidence_audit_input(
    sentence_map_path: Path,
    packet_path: Path,
    output_path: Path,
) -> None:

    if not sentence_map_path.exists():
        raise AuditContractError(
            "SENTENCE_MAP_NOT_FOUND"
        )

    if not packet_path.exists():
        raise AuditContractError(
            "COMPACT_PACKET_NOT_FOUND"
        )

    sentence_map = sentence_map_path.read_text(
        encoding="utf-8"
    )

    packet = packet_path.read_text(
        encoding="utf-8"
    )

    output_path.write_text(
        "===== SENTENCE MAP =====\n"
        + sentence_map
        + "\n===== END SENTENCE MAP =====\n\n"
        + "===== EVIDENCE PACKET =====\n"
        + packet
        + "\n===== END EVIDENCE PACKET =====\n",
        encoding="utf-8",
    )


def build_editorial_input(
    draft_path: Path,
    output_path: Path,
) -> None:

    if not draft_path.exists():
        raise AuditContractError(
            "DRAFT_NOT_FOUND"
        )

    draft = draft_path.read_text(
        encoding="utf-8"
    )

    output_path.write_text(
        "===== CURRENT DRAFT ONLY =====\n"
        + draft
        + "\n===== END CURRENT DRAFT =====\n",
        encoding="utf-8",
    )


def validate_evidence_audit(
    sentence_map_path: Path,
    audit_path: Path,
    packet_path: Path,
) -> dict:

    sentence_map = load_json(
        sentence_map_path
    )
    audit = load_json(
        audit_path
    )
    packet = load_json(
        packet_path
    )

    if (
        audit.get("section_id")
        != sentence_map.get("section_id")
    ):
        raise AuditContractError(
            "AUDIT_SECTION_MISMATCH"
        )

    expected_ids = [
        row["sentence_id"]
        for row in sentence_map.get(
            "sentences",
            [],
        )
    ]

    rows = audit.get(
        "sentence_audit",
        [],
    )

    if not isinstance(rows, list):
        raise AuditContractError(
            "AUDIT_SENTENCE_LIST_INVALID"
        )

    returned_ids = [
        row.get("sentence_id")
        for row in rows
    ]

    counts = Counter(returned_ids)

    missing = [
        sid
        for sid in expected_ids
        if counts[sid] == 0
    ]

    duplicates = [
        sid
        for sid, count in counts.items()
        if sid and count > 1
    ]

    extras = [
        sid
        for sid in returned_ids
        if sid not in expected_ids
    ]

    if missing:
        raise AuditContractError(
            f"MISSING_SENTENCE_IDS: {missing}"
        )

    if duplicates:
        raise AuditContractError(
            f"DUPLICATE_SENTENCE_IDS: "
            f"{duplicates}"
        )

    if extras:
        raise AuditContractError(
            f"EXTRA_SENTENCE_IDS: {extras}"
        )

    claim_text_by_id = {
        c.get("claim_id"): c.get("claim_text", "")
        for c in packet.get(
            "admitted_claims",
            [],
        )
        if c.get("claim_id")
    }
    valid_claim_ids = set(claim_text_by_id)

    sentence_text_by_id = {
        s.get("sentence_id"): s.get("text", "")
        for s in sentence_map.get("sentences", [])
    }

    for row in rows:
        sid = row.get("sentence_id")
        status = row.get("status")
        claim_ids = row.get(
            "supporting_claim_ids",
            [],
        )

        if status not in VALID_STATUSES:
            raise AuditContractError(
                f"INVALID_AUDIT_STATUS: "
                f"{sid}: {status}"
            )

        if (
            status in ("SUPPORTED", "NARRATIVE_SYNTHESIS")
            and not claim_ids
        ):
            raise AuditContractError(
                f"{status}_WITHOUT_CLAIMS: "
                f"{sid}"
            )

        if not isinstance(claim_ids, list):
            raise AuditContractError(
                f"INVALID_CLAIM_ID_LIST: {sid}"
            )

        for cid in claim_ids:
            if cid not in valid_claim_ids:
                raise AuditContractError(
                    f"UNKNOWN_CLAIM_ID: "
                    f"{sid} -> {cid}"
                )

        if status == "NARRATIVE_SYNTHESIS":
            violations = _narrative_synthesis_violations(
                sentence_text_by_id.get(sid, ""),
                [claim_text_by_id.get(cid, "") for cid in claim_ids],
            )
            if violations:
                raise AuditContractError(
                    f"NARRATIVE_SYNTHESIS_CONTRACT_VIOLATION: "
                    f"{sid}: {violations}"
                )

    # Authoritative counts are always recomputed from sentence_audit
    # rows. The model's self-reported "summary" and "decision" fields
    # are NEVER trusted for gating: a model can emit an internally
    # inconsistent JSON (e.g. summary says 34/0 while the rows show
    # 32 SUPPORTED + 2 PARTIALLY_SUPPORTED). A mismatch there is a
    # signal about model unreliability, not a reason to hard-fail an
    # otherwise-valid, fully-SUPPORTED draft — and it is not a reason
    # to accept an unsafe one either, since the rows (not the summary)
    # decide the outcome either way.
    calculated = {
        "supported": sum(
            row.get("status") == "SUPPORTED"
            for row in rows
        ),
        "partially_supported": sum(
            row.get("status") == "PARTIALLY_SUPPORTED"
            for row in rows
        ),
        "unsupported": sum(
            row.get("status") == "UNSUPPORTED"
            for row in rows
        ),
        "scope_leakage": sum(
            row.get("status") == "SCOPE_LEAKAGE"
            for row in rows
        ),
        "unsupported_source_identity": sum(
            row.get("status") == "UNSUPPORTED_SOURCE_IDENTITY"
            for row in rows
        ),
        "redundancy": sum(
            row.get("status") == "REDUNDANCY"
            for row in rows
        ),
        "narrative_synthesis": sum(
            row.get("status") == "NARRATIVE_SYNTHESIS"
            for row in rows
        ),
    }

    reported_summary = audit.get("summary", {})

    summary_mismatch = [
        key
        for key, value in calculated.items()
        if reported_summary.get(key) != value
    ]

    if audit.get("qualifier_issues"):
        raise AuditContractError(
            "QUALIFIER_ISSUES"
        )

    if audit.get("required_actions"):
        raise AuditContractError(
            "EVIDENCE_REQUIRED_ACTIONS"
        )

    for key in (
        "partially_supported",
        "unsupported",
        "scope_leakage",
        "unsupported_source_identity",
        "redundancy",
    ):
        if calculated.get(key, 0) != 0:
            raise AuditContractError(
                f"EVIDENCE_BLOCKER: "
                f"{key}={calculated.get(key)}"
            )

    return {
        "decision": "PASS",
        "sentence_count": len(expected_ids),
        "supported": calculated["supported"],
        "narrative_synthesis": calculated["narrative_synthesis"],
        "deterministic_gate": "PASS",
        "model_reported_summary": reported_summary,
        "model_reported_decision": audit.get("decision"),
        "model_summary_mismatch": summary_mismatch,
    }


def validate_editorial_audit(
    audit_path: Path,
) -> dict:

    audit = load_json(audit_path)

    if audit.get("decision") != "PASS":
        raise AuditContractError(
            "EDITORIAL_AUDIT_NOT_PASS"
        )

    blockers = (
        "chronology_issues",
        "naming_ambiguities",
        "language_issues",
        "overgeneralizations",
        "structure_issues",
        "required_actions",
    )

    for key in blockers:
        if audit.get(key):
            raise AuditContractError(
                f"EDITORIAL_BLOCKER: {key}"
            )

    return {
        "decision": "PASS",
    }


def freeze_exact(
    *,
    section_id: str,
    section_title: str,
    version: str,
    draft_path: Path,
    evidence_audit_path: Path,
    editorial_audit_path: Path,
    sentence_map_path: Path,
    compact_packet_path: Path,
    final_dir: Path,
    model_id: str = "unknown",
    model_config: dict | None = None,
    evidence_audit_input_path: Path | None = None,
    editorial_input_path: Path | None = None,
) -> Path:

    validate_evidence_audit(
        sentence_map_path,
        evidence_audit_path,
        compact_packet_path,
    )

    from scripts.editorial_hard_gate import (
        EditorialHardGateError,
        deterministic_editorial_gate,
    )

    try:
        editorial_gate_result = deterministic_editorial_gate(
            draft_path,
            editorial_audit_path,
        )
    except EditorialHardGateError as exc:
        raise AuditContractError(
            f"EDITORIAL_HARD_GATE_FAILED: {exc}"
        ) from exc

    sentence_map = load_json(
        sentence_map_path
    )

    if (
        sentence_map.get("section_id")
        != section_id
    ):
        raise AuditContractError(
            "FREEZE_SECTION_MISMATCH"
        )

    expected_draft_hash = (
        sentence_map.get("draft_sha256")
    )

    actual_draft_hash = sha256_file(
        draft_path
    )

    if (
        expected_draft_hash
        and expected_draft_hash
        != actual_draft_hash
    ):
        raise AuditContractError(
            "DRAFT_CHANGED_AFTER_SENTENCE_MAP"
        )

    slug = section_id.lower().replace(
        "-",
        "_",
    )

    audits_dir = final_dir / "audits"

    final_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    audits_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    final_draft = (
        final_dir / f"{slug}.md"
    )

    final_evidence = (
        audits_dir
        / f"{slug}_evidence_audit.json"
    )

    final_editorial = (
        audits_dir
        / f"{slug}_editorial_audit.json"
    )

    final_sentence_map = (
        audits_dir
        / f"{slug}_sentence_map.json"
    )

    manifest = (
        final_dir
        / f"{slug}_freeze_manifest.json"
    )

    # Write only after every gate passed.
    final_draft.write_bytes(
        draft_path.read_bytes()
    )

    final_evidence.write_bytes(
        evidence_audit_path.read_bytes()
    )

    final_editorial.write_bytes(
        editorial_audit_path.read_bytes()
    )

    final_sentence_map.write_bytes(
        sentence_map_path.read_bytes()
    )

    audit_identity_hasher = hashlib.sha256()
    for path in (
        draft_path,
        evidence_audit_path,
        editorial_audit_path,
        compact_packet_path,
    ):
        audit_identity_hasher.update(path.read_bytes())
        audit_identity_hasher.update(b"\x00")
    audit_identity_hasher.update(model_id.encode("utf-8"))
    audit_identity = audit_identity_hasher.hexdigest()

    data = {
        "section_id": section_id,
        "section_title": section_title,
        "status": "FROZEN",
        "frozen_version": version,
        "frozen_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "audit_identity": audit_identity,

        "evidence_contract_version":
            EVIDENCE_CONTRACT_VERSION,

        "editorial_policy_version":
            EDITORIAL_POLICY_VERSION,

        "model_id": model_id,

        "model_config": model_config or {},

        "human_review_refs": [],

        "evidence_audit_contract":
            "SENTENCE_ID_V2",

        "deterministic_audit_gate":
            "PASS",

        "evidence_audit_decision":
            "PASS",

        "editorial_audit_decision":
            editorial_gate_result["decision"],

        "editorial_model_review":
            editorial_gate_result[
                "model_editorial_review"
            ],

        "sentence_count":
            sentence_map.get(
                "sentence_count"
            ),

        "draft_path":
            str(final_draft),

        "draft_sha256":
            sha256_file(final_draft),

        "evidence_audit_path":
            str(final_evidence),

        "evidence_audit_sha256":
            sha256_file(final_evidence),

        "evidence_audit_input_sha256":
            sha256_file(evidence_audit_input_path)
            if evidence_audit_input_path
            and evidence_audit_input_path.exists()
            else None,

        "editorial_audit_path":
            str(final_editorial),

        "editorial_audit_sha256":
            sha256_file(final_editorial),

        "editorial_input_sha256":
            sha256_file(editorial_input_path)
            if editorial_input_path
            and editorial_input_path.exists()
            else None,

        "sentence_map_path":
            str(final_sentence_map),

        "sentence_map_sha256":
            sha256_file(final_sentence_map),

        "source_compact_packet_path":
            str(compact_packet_path),

        "source_compact_packet_sha256":
            sha256_file(
                compact_packet_path
            ),

        "privacy_mode":
            "LOCAL_ONLY",

        "next_section_auto_start":
            False,
    }

    manifest.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    return manifest


HUMAN_REVIEW_DECISIONS = {"APPROVED", "REJECTED"}


def apply_human_review(
    manifest_path: Path,
    *,
    reviewer: str,
    decision: str,
    note: str = "",
    sentence_id: str | None = None,
    claim_ids: list[str] | None = None,
    original_status: str | None = None,
    overridden_status: str | None = None,
    reason: str | None = None,
) -> dict:
    """
    Append a human review record to a frozen section's manifest.

    This is a post-freeze audit trail, not a rescue path: it never
    re-runs or overrides the deterministic evidence/editorial gates,
    and it never deletes or alters the frozen draft/audit artifacts.
    A REJECTED review only marks the manifest so downstream assembly
    can exclude the section; the underlying FROZEN artifacts remain
    immutable evidence of what was produced and why it was rejected.

    Optional sentence_id/claim_ids/original_status/overridden_status
    bind the record to one exact sentence-level override (never a
    hidden or model-generated gold label — the caller must supply a
    human-provided original_status/overridden_status pair explicitly).
    """
    if decision not in HUMAN_REVIEW_DECISIONS:
        raise AuditContractError(
            f"INVALID_HUMAN_REVIEW_DECISION: {decision}"
        )

    if not reviewer:
        raise AuditContractError(
            "HUMAN_REVIEW_REQUIRES_REVIEWER"
        )

    manifest = load_json(manifest_path)

    if manifest.get("status") not in {"FROZEN", "HUMAN_REJECTED"}:
        raise AuditContractError(
            "HUMAN_REVIEW_REQUIRES_FROZEN_SECTION"
        )

    record = {
        "section_id": manifest.get("section_id"),
        "revision": manifest.get("frozen_version"),
        "draft_sha256": manifest.get("draft_sha256"),
        "sentence_id": sentence_id,
        "claim_ids": claim_ids,
        "original_status": original_status,
        "overridden_status": overridden_status,
        "reviewer": reviewer,
        "decision": decision,
        "reason": reason if reason is not None else note,
        "note": note,
        "reviewed_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    manifest.setdefault("human_review_refs", []).append(record)

    manifest["status"] = (
        "HUMAN_REJECTED"
        if decision == "REJECTED"
        else "FROZEN"
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    return manifest
