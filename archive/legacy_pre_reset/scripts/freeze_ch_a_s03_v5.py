import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

SECTION_ID = "CH-A-S03"
SECTION_TITLE = "Tünellerin Tarihçesi"
VERSION = "v5"

draft = Path("data/book/drafts/ch_a_s03_v5.md")

evidence_audit = Path(
    "data/book/remediation/ch_a_s03/"
    "ch_a_s03_v5_audit_v2.json"
)

editorial_audit = Path(
    "data/book/remediation/ch_a_s03/"
    "ch_a_s03_v5_editorial_audit.json"
)

sentence_map = Path(
    "data/book/remediation/ch_a_s03/"
    "ch_a_s03_v5_sentence_map.json"
)

packet = Path(
    "data/book/remediation/ch_a_s03/"
    "ch_a_s03_writer_evidence_packet_compact.json"
)

final_dir = Path("data/book/final")
audit_dir = final_dir / "audits"

final_draft = final_dir / "ch_a_s03.md"
final_evidence = audit_dir / "ch_a_s03_evidence_audit.json"
final_editorial = audit_dir / "ch_a_s03_editorial_audit.json"
final_sentence_map = audit_dir / "ch_a_s03_sentence_map.json"

manifest = final_dir / "ch_a_s03_freeze_manifest.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------
# Required files
# --------------------------------------------------

for path in (
    draft,
    evidence_audit,
    editorial_audit,
    sentence_map,
    packet,
):
    if not path.exists():
        raise SystemExit(f"ERROR: MISSING_FILE: {path}")


evidence = json.loads(
    evidence_audit.read_text(encoding="utf-8")
)

editorial = json.loads(
    editorial_audit.read_text(encoding="utf-8")
)

sentence_data = json.loads(
    sentence_map.read_text(encoding="utf-8")
)

packet_data = json.loads(
    packet.read_text(encoding="utf-8")
)


# --------------------------------------------------
# Section identity
# --------------------------------------------------

if evidence.get("section_id") != SECTION_ID:
    raise SystemExit("ERROR: EVIDENCE_SECTION_MISMATCH")

if sentence_data.get("section_id") != SECTION_ID:
    raise SystemExit("ERROR: SENTENCE_MAP_SECTION_MISMATCH")


# --------------------------------------------------
# Editorial gate
# --------------------------------------------------

if editorial.get("decision") != "PASS":
    raise SystemExit("ERROR: EDITORIAL_NOT_PASS")

for key in (
    "chronology_issues",
    "naming_ambiguities",
    "language_issues",
    "overgeneralizations",
    "structure_issues",
    "required_actions",
):
    if editorial.get(key):
        raise SystemExit(
            f"ERROR: EDITORIAL_BLOCKER: {key}"
        )


# --------------------------------------------------
# Evidence semantic gate
# --------------------------------------------------

if evidence.get("decision") != "PASS":
    raise SystemExit("ERROR: EVIDENCE_NOT_PASS")

summary = evidence.get("summary", {})

for key in (
    "partially_supported",
    "unsupported",
    "scope_leakage",
    "unsupported_source_identity",
):
    if summary.get(key, 0) != 0:
        raise SystemExit(
            f"ERROR: EVIDENCE_BLOCKER: "
            f"{key}={summary.get(key)}"
        )

if evidence.get("qualifier_issues"):
    raise SystemExit("ERROR: QUALIFIER_ISSUES")

if evidence.get("required_actions"):
    raise SystemExit("ERROR: EVIDENCE_REQUIRED_ACTIONS")


# --------------------------------------------------
# Sentence-ID contract
# --------------------------------------------------

expected_ids = [
    row["sentence_id"]
    for row in sentence_data.get("sentences", [])
]

rows = evidence.get("sentence_audit", [])

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
    raise SystemExit(
        f"ERROR: MISSING_SENTENCE_IDS: {missing}"
    )

if duplicates:
    raise SystemExit(
        f"ERROR: DUPLICATE_SENTENCE_IDS: {duplicates}"
    )

if extras:
    raise SystemExit(
        f"ERROR: EXTRA_SENTENCE_IDS: {extras}"
    )


# --------------------------------------------------
# Claim-ID contract
# --------------------------------------------------

valid_claim_ids = {
    c["claim_id"]
    for c in packet_data.get("admitted_claims", [])
    if c.get("claim_id")
}

for row in rows:
    sid = row.get("sentence_id")
    status = row.get("status")
    claim_ids = row.get("supporting_claim_ids", [])

    if status == "SUPPORTED" and not claim_ids:
        raise SystemExit(
            f"ERROR: SUPPORTED_WITHOUT_CLAIMS: {sid}"
        )

    for cid in claim_ids:
        if cid not in valid_claim_ids:
            raise SystemExit(
                f"ERROR: UNKNOWN_CLAIM_ID: "
                f"{sid} -> {cid}"
            )


# --------------------------------------------------
# Recalculate summary
# --------------------------------------------------

calculated = {
    "supported": sum(
        r.get("status") == "SUPPORTED"
        for r in rows
    ),
    "partially_supported": sum(
        r.get("status") == "PARTIALLY_SUPPORTED"
        for r in rows
    ),
    "unsupported": sum(
        r.get("status") == "UNSUPPORTED"
        for r in rows
    ),
    "scope_leakage": sum(
        r.get("status") == "SCOPE_LEAKAGE"
        for r in rows
    ),
}

for key, value in calculated.items():
    if summary.get(key) != value:
        raise SystemExit(
            f"ERROR: SUMMARY_MISMATCH: "
            f"{key}: reported={summary.get(key)} "
            f"calculated={value}"
        )


# --------------------------------------------------
# Only after every gate passes: write final artifacts
# --------------------------------------------------

audit_dir.mkdir(
    parents=True,
    exist_ok=True,
)

final_draft.write_bytes(draft.read_bytes())
final_evidence.write_bytes(evidence_audit.read_bytes())
final_editorial.write_bytes(editorial_audit.read_bytes())
final_sentence_map.write_bytes(sentence_map.read_bytes())


freeze = {
    "section_id": SECTION_ID,
    "section_title": SECTION_TITLE,
    "status": "FROZEN",
    "frozen_version": VERSION,
    "frozen_at": datetime.now(timezone.utc).isoformat(),

    "evidence_audit_contract": "SENTENCE_ID_V2",
    "deterministic_audit_gate": "PASS",

    "evidence_audit_decision": "PASS",
    "editorial_audit_decision": "PASS",

    "sentence_count": len(expected_ids),

    "draft_path": str(final_draft),
    "draft_sha256": sha256(final_draft),

    "evidence_audit_path": str(final_evidence),
    "evidence_audit_sha256": sha256(final_evidence),

    "editorial_audit_path": str(final_editorial),
    "editorial_audit_sha256": sha256(final_editorial),

    "sentence_map_path": str(final_sentence_map),
    "sentence_map_sha256": sha256(final_sentence_map),

    "source_compact_packet_path": str(packet),
    "source_compact_packet_sha256": sha256(packet),

    "privacy_mode": "LOCAL_ONLY",
    "next_section_auto_start": False,
}

manifest.write_text(
    json.dumps(
        freeze,
        ensure_ascii=False,
        indent=2,
    ) + "\n",
    encoding="utf-8",
)

print("FROZEN =", SECTION_ID)
print("version =", VERSION)
print("draft_sha256 =", freeze["draft_sha256"])
print("sentence_count =", len(expected_ids))
print("evidence_audit = PASS")
print("editorial_audit = PASS")
print("deterministic_gate = PASS")
print("manifest =", manifest)
print("next_section_auto_start = false")
