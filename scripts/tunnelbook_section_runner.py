#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import re
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.section_audit_v2 import (
    AuditContractError,
    build_sentence_map,
    build_evidence_audit_input,
    build_editorial_input,
    validate_evidence_audit,
    freeze_exact,
)
from scripts.editorial_hard_gate import (
    EditorialHardGateError,
    deterministic_editorial_gate,
)
from scripts.audit_cache import AuditCache, compute_key
from scripts.section_state import (
    SectionStateError,
    checkpoint_revision,
    restore_revision,
    sha256_bytes,
)

AUDIT_CONTRACT_VERSION = "v2"


ROOT = Path(__file__).resolve().parents[1]

LOCAL_QWEN = ROOT / "scripts" / "local_qwen.py"

BOOK_DIR = ROOT / "data" / "book"
REMEDIATION_DIR = BOOK_DIR / "remediation"
DRAFT_DIR = BOOK_DIR / "drafts"
FINAL_DIR = BOOK_DIR / "final"
FINAL_AUDIT_DIR = FINAL_DIR / "audits"
AUDIT_CACHE_DIR = REMEDIATION_DIR / "_audit_cache"

PROMPT_DIR = ROOT / "prompts"


class RunnerError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str], env: dict[str, str] | None = None) -> None:
    print("+", " ".join(str(x) for x in cmd))

    result = subprocess.run(
        cmd,
        cwd=ROOT,
        env=env,
    )

    if result.returncode != 0:
        raise RunnerError(
            f"COMMAND_FAILED exit={result.returncode}: {' '.join(cmd)}"
        )


def section_slug(section_id: str) -> str:
    return section_id.lower().replace("-", "_")


def section_paths(section_id: str) -> dict[str, Path]:
    slug = section_slug(section_id)

    remediation = (
        ROOT
        / "data"
        / "book"
        / "remediation"
        / slug
    )

    return {
        "remediation": remediation,

        "packet": (
            remediation
            / f"{slug}_writer_evidence_packet.json"
        ),

        "compact_packet": (
            remediation
            / f"{slug}_writer_evidence_packet_compact.json"
        ),

        "draft": (
            ROOT
            / "data"
            / "book"
            / "drafts"
            / f"{slug}.md"
        ),

        "sentence_map": (
            remediation
            / f"{slug}_sentence_map.json"
        ),

        "evidence_audit_input": (
            remediation
            / f"{slug}_evidence_audit_input.txt"
        ),

        "evidence_audit": (
            remediation
            / f"{slug}_evidence_audit.json"
        ),

        "editorial_input": (
            remediation
            / f"{slug}_editorial_input.txt"
        ),

        "editorial_audit": (
            remediation
            / f"{slug}_editorial_audit.json"
        ),
    }


def resolve_latest_packet(section_id: str, remediation_dir: Path) -> Path:
    slug = section_slug(section_id)
    pointer = remediation_dir / f"{slug}_latest_run.json"

    require_file(pointer, "LATEST_RUN_POINTER_NOT_FOUND")

    data = load_json(pointer)

    if data.get("section_id") != section_id:
        raise RunnerError("LATEST_RUN_SECTION_MISMATCH")

    relative = data.get("packet_path")
    expected_hash = data.get("packet_sha256")

    if not relative or not expected_hash:
        raise RunnerError("WRITER_PACKET_NOT_CREATED")

    packet = (ROOT / relative).resolve()
    root_resolved = ROOT.resolve()

    if root_resolved not in packet.parents:
        raise RunnerError("LATEST_RUN_PACKET_OUTSIDE_PROJECT")

    require_file(packet, "WRITER_PACKET_NOT_FOUND")

    actual_hash = sha256(packet)

    if actual_hash != expected_hash:
        raise RunnerError("WRITER_PACKET_HASH_MISMATCH")

    print(f"exact_packet={packet.relative_to(ROOT)}")
    print(f"exact_packet_sha256={actual_hash}")

    return packet



def resolve_resume_packet(
    section_id: str,
    remediation_dir: Path,
) -> Path:
    latest = remediation_dir / (
        f"{section_slug(section_id)}_latest_run.json"
    )

    require_file(
        latest,
        "RESUME_LATEST_RUN_NOT_FOUND",
    )

    data = load_json(latest)

    if data.get("section_id") != section_id:
        raise RunnerError(
            "RESUME_SECTION_MISMATCH"
        )

    if data.get("privacy_mode") != "LOCAL_ONLY":
        raise RunnerError(
            "RESUME_PRIVACY_MODE_INVALID"
        )

    packet_raw = data.get("packet_path")
    packet_hash = data.get("packet_sha256")

    manifest_raw = data.get("manifest_path")
    manifest_hash = data.get("manifest_sha256")

    if not packet_raw or not packet_hash:
        raise RunnerError(
            "RESUME_PACKET_POINTER_INVALID"
        )

    if not manifest_raw or not manifest_hash:
        raise RunnerError(
            "RESUME_MANIFEST_POINTER_INVALID"
        )

    packet = Path(packet_raw)
    manifest = Path(manifest_raw)

    if not packet.is_absolute():
        packet = ROOT / packet

    if not manifest.is_absolute():
        manifest = ROOT / manifest

    require_file(
        packet,
        "RESUME_PACKET_NOT_FOUND",
    )

    require_file(
        manifest,
        "RESUME_MANIFEST_NOT_FOUND",
    )

    if sha256(packet) != packet_hash:
        raise RunnerError(
            "RESUME_PACKET_SHA256_MISMATCH"
        )

    if sha256(manifest) != manifest_hash:
        raise RunnerError(
            "RESUME_MANIFEST_SHA256_MISMATCH"
        )

    manifest_data = load_json(manifest)

    if manifest_data.get("section_id") != section_id:
        raise RunnerError(
            "RESUME_MANIFEST_SECTION_MISMATCH"
        )

    readiness = (
        manifest_data.get("readiness")
        or manifest_data.get(
            "summary",
            {},
        ).get("readiness")
    )

    if readiness not in (None, "READY"):
        raise RunnerError(
            f"RESUME_NOT_READY: {readiness}"
        )

    print("phase=REMEDIATION_RESUME_CHECK")
    print("remediation_reused=true")
    print("packet_integrity=PASS")
    print("manifest_integrity=PASS")

    return packet


def require_file(path: Path, code: str) -> None:
    if not path.exists():
        raise RunnerError(f"{code}: {path.relative_to(ROOT)}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RunnerError(f"INVALID_JSON: {path}: {exc}") from exc


def _claim_has_year(claim: dict) -> bool:
    import re

    text = str(claim.get("claim_text") or "")

    return bool(
        re.search(r"\b(?:1[0-9]{3}|20[0-9]{2})\b", text)
        or re.search(
            r"\b(?:MÖ|M\.Ö\.|MS|M\.S\.)\b",
            text,
            re.IGNORECASE,
        )
    )


def _select_writer_claims(
    claims: list[dict],
    max_claims: int = 72,
) -> list[dict]:

    if len(claims) <= max_claims:
        return claims

    selected: list[dict] = []
    selected_ids: set[str] = set()

    def add(claim: dict) -> None:
        cid = str(claim.get("claim_id") or id(claim))

        if cid not in selected_ids and len(selected) < max_claims:
            selected.append(claim)
            selected_ids.add(cid)

    # 1. Kronoloji taşıyan claim'ler.
    for claim in claims:
        if _claim_has_year(claim):
            add(claim)

    # 2. Kaynak çeşitliliği.
    seen_docs: set[str] = set()

    for claim in claims:
        doc = str(claim.get("document_id") or "")

        if doc and doc not in seen_docs:
            add(claim)
            seen_docs.add(doc)

    # 3. Limited claim'leri mümkün olduğunca koru.
    for claim in claims:
        if claim.get("disposition") == "ADMITTED_LIMITED":
            add(claim)

    # 4. Locator çeşitliliği.
    seen_locations: set[tuple[str, str]] = set()

    for claim in claims:
        key = (
            str(claim.get("document_id") or ""),
            str(claim.get("locator") or ""),
        )

        if key not in seen_locations:
            add(claim)
            seen_locations.add(key)

    # 5. Kalan kapasiteyi deterministik doldur.
    for claim in claims:
        add(claim)

    return selected


def build_compact_packet(src: Path, dst: Path) -> None:
    data = load_json(src)

    readiness = data.get("readiness")

    if readiness not in {"READY", "READY_WITH_LIMITATIONS"}:
        raise RunnerError(
            f"EVIDENCE_NOT_READY: readiness={readiness}"
        )

    admitted = data.get("admitted_claims", [])

    if not isinstance(admitted, list) or not admitted:
        raise RunnerError("NO_ADMITTED_CLAIMS")

    selected = _select_writer_claims(
        admitted,
        max_claims=72,
    )

    selected_ids = {
        c.get("claim_id")
        for c in selected
        if c.get("claim_id")
    }

    compact_claims = []

    for c in selected:
        compact_claims.append({
            "claim_id": c.get("claim_id"),
            "claim_text": c.get("claim_text"),
            "qualifier": c.get("qualifier"),
            "disposition": c.get("disposition"),
            "document_id": c.get("document_id"),
            "locator": c.get("locator"),
            "section_applicability": c.get(
                "section_applicability"
            ),
        })

    citation_mapping = [
        m
        for m in data.get("citation_mapping", [])
        if m.get("claim_id") in selected_ids
    ]

    compact = {
        "section_id": data.get("section_id"),
        "section_title": data.get("section_title"),
        "section_scope": data.get("section_scope"),
        "scope_exclusions": data.get(
            "scope_exclusions",
            [],
        ),
        "research_question": data.get(
            "research_question"
        ),
        "readiness": readiness,
        "writer_evidence_selection": {
            "strategy":
                "DETERMINISTIC_DIVERSITY_BUDGET_V1",
            "total_admitted_claims": len(admitted),
            "selected_claims": len(compact_claims),
            "max_claims": 72,
        },
        "admitted_claims": compact_claims,
        "citation_mapping": citation_mapping,
        "evidence_limitations": data.get(
            "evidence_limitations",
            [],
        ),
        "privacy_mode": data.get(
            "privacy_mode",
            "LOCAL_ONLY",
        ),
    }

    dst.parent.mkdir(parents=True, exist_ok=True)

    dst.write_text(
        json.dumps(
            compact,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print(
        f"compact_packet={dst.relative_to(ROOT)} "
        f"claims={len(compact_claims)}/{len(admitted)} "
        f"bytes={dst.stat().st_size}"
    )


def build_audit_input(draft: Path, packet: Path, dst: Path) -> None:
    draft_text = draft.read_text(encoding="utf-8")
    packet_text = packet.read_text(encoding="utf-8")

    dst.write_text(
        "===== DRAFT =====\n"
        + draft_text
        + "\n===== END DRAFT =====\n\n"
        + "===== EVIDENCE PACKET =====\n"
        + packet_text
        + "\n===== END EVIDENCE PACKET =====\n",
        encoding="utf-8",
    )



def validate_audit_integrity(draft_path: Path, audit: dict) -> None:
    import re

    draft = draft_path.read_text(encoding="utf-8")

    def norm(text: str) -> str:
        return re.sub(r"\s+", " ", str(text)).strip()

    draft_norm = norm(draft)

    sentence_audit = audit.get("sentence_audit", [])

    if not isinstance(sentence_audit, list):
        raise RunnerError("AUDIT_SENTENCE_LIST_INVALID")

    for index, item in enumerate(sentence_audit, 1):
        sentence = norm(item.get("sentence", ""))

        if not sentence:
            raise RunnerError(
                f"AUDIT_EMPTY_SENTENCE: index={index}"
            )

        if sentence not in draft_norm:
            raise RunnerError(
                f"AUDIT_QUOTE_MISMATCH: index={index}"
            )

        status = item.get("status")
        claim_ids = item.get("supporting_claim_ids", [])

        if status == "SUPPORTED":
            if not isinstance(claim_ids, list) or not claim_ids:
                raise RunnerError(
                    f"SUPPORTED_WITHOUT_CLAIM_IDS: index={index}"
                )


def validate_dual_audit(
    draft_path: Path,
    evidence_audit_path: Path,
    editorial_audit_path: Path,
) -> None:

    require_file(
        draft_path,
        "DRAFT_NOT_FOUND",
    )
    require_file(
        evidence_audit_path,
        "EVIDENCE_AUDIT_NOT_FOUND",
    )
    require_file(
        editorial_audit_path,
        "EDITORIAL_AUDIT_NOT_FOUND",
    )

    evidence = load_json(evidence_audit_path)
    editorial = load_json(editorial_audit_path)

    validate_audit_integrity(
        draft_path,
        evidence,
    )

    if evidence.get("decision") != "PASS":
        raise RunnerError("EVIDENCE_AUDIT_NOT_PASS")

    summary = evidence.get("summary", {})

    blockers = (
        "partially_supported",
        "unsupported",
        "scope_leakage",
        "unsupported_source_identity",
    )

    for key in blockers:
        if summary.get(key, 0) != 0:
            raise RunnerError(
                f"EVIDENCE_AUDIT_BLOCKER: {key}={summary.get(key)}"
            )

    if evidence.get("qualifier_issues"):
        raise RunnerError("EVIDENCE_QUALIFIER_ISSUES")

    if evidence.get("required_actions"):
        raise RunnerError("EVIDENCE_REQUIRED_ACTIONS")

    if editorial.get("decision") != "PASS":
        raise RunnerError("EDITORIAL_AUDIT_NOT_PASS")

    for key in (
        "chronology_issues",
        "naming_ambiguities",
        "language_issues",
        "overgeneralizations",
        "structure_issues",
        "required_actions",
    ):
        if editorial.get(key):
            raise RunnerError(
                f"EDITORIAL_AUDIT_BLOCKER: {key}"
            )

def validate_audit(audit_path: Path) -> dict:
    audit = load_json(audit_path)

    decision = audit.get("decision")
    summary = audit.get("summary", {})

    if decision not in {"PASS", "HOLD"}:
        raise RunnerError(f"INVALID_AUDIT_DECISION: {decision}")

    return {
        "decision": decision,
        "supported": summary.get("supported", 0),
        "partially_supported": summary.get("partially_supported", 0),
        "unsupported": summary.get("unsupported", 0),
        "scope_leakage": summary.get("scope_leakage", 0),
        "unsupported_source_identity": summary.get(
            "unsupported_source_identity", 0
        ),
        "redundancy": summary.get("redundancy", 0),
    }


def freeze(
    section_id: str,
    paths: dict[str, Path],
    *,
    model: str = "unknown",
    api_base: str = "",
) -> None:
    config = load_json(
        ROOT / "config" / "book_sections.json"
    )

    section = config.get(section_id)

    if not section:
        raise RunnerError(
            f"SECTION_CONFIG_NOT_FOUND: {section_id}"
        )

    section_title = section.get(
        "section_title",
        section_id,
    )

    audit_prompt = audit_prompt_for(section_id)

    expected_key = compute_key(
        draft_path=paths["draft"],
        packet_path=paths["compact_packet"],
        prompt_path=audit_prompt,
        model=model,
        contract_version=AUDIT_CONTRACT_VERSION,
        model_config={"api_base": api_base} if api_base else {},
    )

    cache = AuditCache(AUDIT_CACHE_DIR)
    cached = cache.get(expected_key)

    if cached is None or cached["audit"] != load_json(paths["evidence_audit"]):
        raise RunnerError(
            "STALE_EVIDENCE_AUDIT_IDENTITY: "
            "evidence_audit.json does not match the current "
            "draft/packet/prompt/model identity; rerun the "
            "evidence audit before freezing"
        )

    try:
        manifest = freeze_exact(
            section_id=section_id,
            section_title=section_title,
            version="v1",
            draft_path=paths["draft"],
            evidence_audit_path=paths["evidence_audit"],
            editorial_audit_path=paths["editorial_audit"],
            sentence_map_path=paths["sentence_map"],
            compact_packet_path=paths["compact_packet"],
            final_dir=ROOT / "data" / "book" / "final",
            model_id=model,
            model_config={"api_base": api_base} if api_base else {},
            evidence_audit_input_path=paths.get("evidence_audit_input"),
            editorial_input_path=paths.get("editorial_input"),
        )
    except AuditContractError as exc:
        raise RunnerError(
            f"FREEZE_GATE_FAILED: {exc}"
        ) from exc

    print(
        f"FROZEN={manifest.relative_to(ROOT)}"
    )
    print("status=FROZEN")
    print("next_section_auto_start=false")


def remediation_script_for(section_id: str) -> Path:
    path = ROOT / "scripts" / "section_evidence_remediation.py"

    if not path.exists():
        raise RunnerError("GENERIC_REMEDIATION_NOT_FOUND")

    return path

def writer_prompt_for(section_id: str) -> Path:
    slug = section_slug(section_id)

    candidates = [
        PROMPT_DIR / f"{slug}_writer.txt",
        PROMPT_DIR / "generic_section_writer.txt",
    ]

    for path in candidates:
        if path.exists():
            return path

    raise RunnerError(
        f"WRITER_PROMPT_NOT_FOUND: {section_id}"
    )


def audit_prompt_for(section_id: str) -> Path:
    slug = section_slug(section_id)

    candidates = [
        PROMPT_DIR / f"{slug}_audit.txt",
        PROMPT_DIR / "generic_section_audit_v2.txt",
    ]

    for path in candidates:
        if path.exists():
            return path

    raise RunnerError(
        f"AUDIT_PROMPT_NOT_FOUND: {section_id}"
    )


def execute_section(
    section_id: str,
    model: str,
    api_base: str,
    no_freeze: bool,
    resume: bool = False,
) -> None:
    paths = section_paths(section_id)

    remediation_script = remediation_script_for(section_id)
    writer_prompt = writer_prompt_for(section_id)
    audit_prompt = audit_prompt_for(section_id)

    editorial_prompt = (
        PROMPT_DIR / "generic_editorial_audit.txt"
    )
    reviser_prompt = (
        PROMPT_DIR / "generic_editorial_reviser.txt"
    )

    require_file(
        LOCAL_QWEN,
        "LOCAL_QWEN_NOT_FOUND",
    )
    require_file(
        remediation_script,
        "REMEDIATION_NOT_FOUND",
    )
    require_file(
        editorial_prompt,
        "EDITORIAL_PROMPT_NOT_FOUND",
    )
    require_file(
        reviser_prompt,
        "EDITORIAL_REVISER_PROMPT_NOT_FOUND",
    )

    env = os.environ.copy()
    env["HF_HUB_OFFLINE"] = "1"
    env["TRANSFORMERS_OFFLINE"] = "1"

    print(f"section={section_id}")

    # =====================================================
    # REMEDIATION
    # =====================================================

    if resume:
        paths["packet"] = resolve_resume_packet(
            section_id,
            paths["remediation"],
        )
    else:
        print("phase=REMEDIATION")

        run([
            sys.executable,
            str(remediation_script),
            "--section-id",
            section_id,
            "--use-local-llm",
            "--model",
            model,
            "--api-base",
            api_base,
        ], env=env)

        paths["packet"] = resolve_latest_packet(
            section_id,
            paths["remediation"],
        )

    # =====================================================
    # COMPACT PACKET
    # =====================================================

    print("phase=COMPACT_PACKET")

    build_compact_packet(
        paths["packet"],
        paths["compact_packet"],
    )

    # =====================================================
    # TRY TO REUSE EXISTING EVIDENCE-PASS DRAFT
    # =====================================================

    evidence_ready = False

    if resume:
        required = (
            paths["draft"],
            paths["sentence_map"],
            paths["evidence_audit"],
            paths["compact_packet"],
        )

        if all(path.exists() for path in required):
            print("phase=EVIDENCE_RESUME_CHECK")

            try:
                sentence_data = load_json(
                    paths["sentence_map"]
                )

                bound_hash = sentence_data.get(
                    "draft_sha256"
                )

                actual_hash = sha256(
                    paths["draft"]
                )

                if not bound_hash:
                    raise RunnerError(
                        "RESUME_SENTENCE_MAP_HAS_NO_DRAFT_HASH"
                    )

                if bound_hash != actual_hash:
                    raise RunnerError(
                        "RESUME_DRAFT_HASH_MISMATCH"
                    )

                gate = validate_evidence_audit(
                    paths["sentence_map"],
                    paths["evidence_audit"],
                    paths["compact_packet"],
                )

                evidence_ready = True

                print("draft_reused=true")
                print("sentence_map_reused=true")
                print("evidence_audit_reused=true")
                print(
                    f"sentence_count={gate['sentence_count']}"
                )
                print(
                    f"supported={gate['supported']}"
                )
                print(
                    "deterministic_audit_gate=PASS"
                )

            except (
                AuditContractError,
                RunnerError,
            ) as exc:
                print(
                    f"evidence_resume_rejected={exc}"
                )

    # =====================================================
    # WRITER + FIRST EVIDENCE AUDIT
    # =====================================================

    if not evidence_ready:
        print("phase=WRITER")

        DRAFT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        run([
            sys.executable,
            str(LOCAL_QWEN),
            "--prompt-file",
            str(writer_prompt),
            "--input",
            str(paths["compact_packet"]),
            "--output",
            str(paths["draft"]),
        ], env=env)

        require_file(
            paths["draft"],
            "DRAFT_NOT_CREATED",
        )

        print("phase=SENTENCE_MAP")

        sentence_map = build_sentence_map(
            paths["draft"],
            paths["sentence_map"],
            section_id,
        )

        print(
            f"sentence_map="
            f"{paths['sentence_map'].relative_to(ROOT)} "
            f"sentences={sentence_map['sentence_count']}"
        )

        print("phase=EVIDENCE_AUDIT_INPUT")

        build_evidence_audit_input(
            paths["sentence_map"],
            paths["compact_packet"],
            paths["evidence_audit_input"],
        )

        print("phase=EVIDENCE_AUDIT")

        cache = AuditCache(AUDIT_CACHE_DIR)
        cache_key = compute_key(
            draft_path=paths["draft"],
            packet_path=paths["compact_packet"],
            prompt_path=audit_prompt,
            model=model,
            contract_version=AUDIT_CONTRACT_VERSION,
            model_config={"api_base": api_base} if api_base else {},
        )
        cached = cache.get(cache_key)

        if cached is not None:
            print("evidence_audit_cache=HIT")
            paths["evidence_audit"].write_text(
                json.dumps(
                    cached["audit"],
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        else:
            print("evidence_audit_cache=MISS")
            run([
                sys.executable,
                str(LOCAL_QWEN),
                "--prompt-file",
                str(audit_prompt),
                "--input",
                str(paths["evidence_audit_input"]),
                "--output",
                str(paths["evidence_audit"]),
            ], env=env)

        print("phase=DETERMINISTIC_AUDIT_GATE")

        try:
            gate = validate_evidence_audit(
                paths["sentence_map"],
                paths["evidence_audit"],
                paths["compact_packet"],
            )
        except AuditContractError as exc:
            raise RunnerError(
                f"DETERMINISTIC_AUDIT_GATE_FAILED: {exc}"
            ) from exc

        if cached is None:
            cache.put(
                cache_key,
                section_id=section_id,
                kind="evidence_audit",
                audit_json=load_json(paths["evidence_audit"]),
                gate_result=gate,
            )

        print(
            f"evidence_audit_decision={gate['decision']}"
        )
        print(
            f"sentence_count={gate['sentence_count']}"
        )
        print(
            f"supported={gate['supported']}"
        )
        print("deterministic_audit_gate=PASS")

    # =====================================================
    # EDITORIAL AUDIT + MAX 2 REVISIONS
    # =====================================================

    max_revisions = 2

    for cycle in range(
        0,
        max_revisions + 1,
    ):
        use_existing_editorial = (
            resume
            and cycle == 0
            and paths["editorial_audit"].exists()
        )

        if use_existing_editorial:
            print("phase=EDITORIAL_RESUME_CHECK")

        else:
            print("phase=EDITORIAL_INPUT")

            build_editorial_input(
                paths["draft"],
                paths["editorial_input"],
            )

            print("phase=EDITORIAL_AUDIT")

            run([
                sys.executable,
                str(LOCAL_QWEN),
                "--prompt-file",
                str(editorial_prompt),
                "--input",
                str(paths["editorial_input"]),
                "--output",
                str(paths["editorial_audit"]),
            ], env=env)

        try:
            editorial = deterministic_editorial_gate(
                paths["draft"],
                paths["editorial_audit"],
            )

            print(
                f"editorial_audit_decision="
                f"{editorial['decision']}"
            )
            print(
                "editorial_advisory="
                f"{editorial['model_editorial_review']['model_decision']}"
            )

            break

        except EditorialHardGateError as exc:
            print("editorial_audit_decision=HOLD")
            print(
                f"editorial_revision_cycle={cycle}"
            )
            print(
                f"editorial_hold_reason={exc}"
            )

            if cycle >= max_revisions:
                raise RunnerError(
                    "EDITORIAL_AUDIT_FAILED_AFTER_"
                    f"{max_revisions}_REVISIONS: {exc}"
                ) from exc

        # =================================================
        # EDITORIAL REVISION
        # =================================================

        revision = cycle + 1
        slug = section_slug(section_id)

        before_path = (
            DRAFT_DIR
            / f"{slug}_before_editorial_r"
            f"{revision}.md"
        )

        revision_path = (
            DRAFT_DIR
            / f"{slug}_editorial_r"
            f"{revision}.md"
        )

        revision_input = (
            paths["remediation"]
            / f"{slug}_editorial_r"
            f"{revision}_input.txt"
        )

        before_path.write_bytes(
            paths["draft"].read_bytes()
        )

        try:
            checkpoint_revision(
                remediation_dir=paths["remediation"],
                revision=cycle,
                draft_path=before_path,
                sentence_map_path=paths["sentence_map"],
                evidence_audit_input_path=paths.get("evidence_audit_input"),
                evidence_audit_path=paths["evidence_audit"],
                editorial_input_path=(
                    paths["editorial_input"]
                    if paths.get("editorial_input") and paths["editorial_input"].exists()
                    else None
                ),
                editorial_audit_path=(
                    paths["editorial_audit"]
                    if paths["editorial_audit"].exists()
                    else None
                ),
                status="EVIDENCE_VALID_PRE_REVISION",
                state={"section_id": section_id, "cycle": cycle},
            )
        except SectionStateError as exc:
            if "REVISION_ALREADY_CHECKPOINTED" not in str(exc):
                raise

            from scripts.section_state import (
                load_revision_manifest,
            )

            existing = load_revision_manifest(
                paths["remediation"], cycle
            )
            existing_hash = existing["artifact_sha256"].get(
                "draft.md"
            )

            if existing_hash != sha256_bytes(
                before_path.read_bytes()
            ):
                raise RunnerError(
                    "REVISION_CHECKPOINT_CONFLICT: r"
                    f"{cycle} already recorded a different "
                    "draft than the current resume state"
                ) from exc

        revision_input.write_text(
            "===== CURRENT DRAFT =====\n"
            + paths["draft"].read_text(
                encoding="utf-8"
            )
            + "\n===== END CURRENT DRAFT =====\n\n"
            + "===== EDITORIAL AUDIT =====\n"
            + paths["editorial_audit"].read_text(
                encoding="utf-8"
            )
            + "\n===== END EDITORIAL AUDIT =====\n\n"
            + "===== ADMITTED EVIDENCE PACKET =====\n"
            + paths["compact_packet"].read_text(
                encoding="utf-8"
            )
            + "\n===== END ADMITTED EVIDENCE PACKET =====\n",
            encoding="utf-8",
        )

        print(
            f"phase=EDITORIAL_REVISION_R{revision}"
        )

        run([
            sys.executable,
            str(LOCAL_QWEN),
            "--prompt-file",
            str(reviser_prompt),
            "--input",
            str(revision_input),
            "--output",
            str(revision_path),
        ], env=env)

        require_file(
            revision_path,
            "EDITORIAL_REVISION_NOT_CREATED",
        )

        paths["draft"].write_bytes(
            revision_path.read_bytes()
        )

        # =================================================
        # REVISION MUST PASS EVIDENCE AGAIN
        # =================================================

        print(
            f"phase=REVISION_R{revision}_SENTENCE_MAP"
        )

        sentence_map = build_sentence_map(
            paths["draft"],
            paths["sentence_map"],
            section_id,
        )

        print(
            f"revision_r{revision}_sentence_count="
            f"{sentence_map['sentence_count']}"
        )

        build_evidence_audit_input(
            paths["sentence_map"],
            paths["compact_packet"],
            paths["evidence_audit_input"],
        )

        print(
            f"phase=REVISION_R{revision}_EVIDENCE_AUDIT"
        )

        revision_cache_key = compute_key(
            draft_path=paths["draft"],
            packet_path=paths["compact_packet"],
            prompt_path=audit_prompt,
            model=model,
            contract_version=AUDIT_CONTRACT_VERSION,
            model_config={"api_base": api_base} if api_base else {},
        )
        revision_cached = cache.get(revision_cache_key)

        if revision_cached is not None:
            print(f"revision_r{revision}_evidence_audit_cache=HIT")
            paths["evidence_audit"].write_text(
                json.dumps(
                    revision_cached["audit"],
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        else:
            print(f"revision_r{revision}_evidence_audit_cache=MISS")
            run([
                sys.executable,
                str(LOCAL_QWEN),
                "--prompt-file",
                str(audit_prompt),
                "--input",
                str(paths["evidence_audit_input"]),
                "--output",
                str(paths["evidence_audit"]),
            ], env=env)

        try:
            gate = validate_evidence_audit(
                paths["sentence_map"],
                paths["evidence_audit"],
                paths["compact_packet"],
            )
        except AuditContractError as exc:
            print(
                f"revision_r{revision}_evidence_gate=HOLD"
            )
            print(
                f"phase=REVISION_R{revision}_ROLLBACK"
            )

            # Restore last evidence-valid revision (r{cycle}),
            # verified by hash, not just copied blind.
            restore_revision(
                remediation_dir=paths["remediation"],
                revision=cycle,
                draft_path=paths["draft"],
                sentence_map_path=paths["sentence_map"],
                evidence_audit_input_path=paths.get("evidence_audit_input"),
                evidence_audit_path=paths["evidence_audit"],
                editorial_input_path=paths.get("editorial_input"),
                editorial_audit_path=paths["editorial_audit"],
            )

            # Confirm rollback really restored a valid state.
            try:
                rollback_gate = validate_evidence_audit(
                    paths["sentence_map"],
                    paths["evidence_audit"],
                    paths["compact_packet"],
                )
            except AuditContractError as rollback_exc:
                raise RunnerError(
                    "REVISION_ROLLBACK_VALIDATION_FAILED: "
                    f"r{revision}: {rollback_exc}"
                ) from rollback_exc

            print("rollback_status=PASS")
            print(
                f"rollback_supported="
                f"{rollback_gate['supported']}"
            )

            raise RunnerError(
                "EDITORIAL_REVISION_REJECTED_AND_ROLLED_BACK: "
                f"r{revision}: {exc}"
            ) from exc

        if revision_cached is None:
            cache.put(
                revision_cache_key,
                section_id=section_id,
                kind="evidence_audit",
                audit_json=load_json(paths["evidence_audit"]),
                gate_result=gate,
            )

        print(
            f"revision_r{revision}_evidence_gate=PASS"
        )
        print(
            f"revision_r{revision}_supported="
            f"{gate['supported']}"
        )

        # Force fresh editorial audit next cycle.
        if paths["editorial_audit"].exists():
            paths["editorial_audit"].unlink()

        resume = False

    # =====================================================
    # PASS / FREEZE
    # =====================================================

    if no_freeze:
        print("status=PASS_NOT_FROZEN")
        return

    print("phase=FREEZE")

    freeze(
        section_id,
        paths,
        model=model,
        api_base=api_base,
    )

    print("status=FROZEN")
    print("next_section_auto_start=false")



def section_freeze_manifest(section_id: str) -> Path:
    slug = section_slug(section_id)

    return (
        ROOT
        / "data"
        / "book"
        / "final"
        / f"{slug}_freeze_manifest.json"
    )


def is_section_frozen(section_id: str) -> bool:
    manifest = section_freeze_manifest(section_id)

    if not manifest.exists():
        return False

    try:
        data = load_json(manifest)
    except Exception:
        return False

    return (
        data.get("section_id") == section_id
        and data.get("status") == "FROZEN"
    )


def configured_section_ids() -> list[str]:
    config_path = (
        ROOT
        / "config"
        / "book_sections.json"
    )

    config = load_json(config_path)

    ids = [
        key
        for key in config.keys()
        if re.fullmatch(
            r"CH-[A-Z]-S\d+",
            key,
        )
    ]

    def key(section_id: str):
        match = re.fullmatch(
            r"CH-([A-Z])-S(\d+)",
            section_id,
        )

        if not match:
            return ("Z", 999999)

        return (
            match.group(1),
            int(match.group(2)),
        )

    return sorted(ids, key=key)


def execute_book(
    *,
    model: str,
    api_base: str,
    resume: bool,
) -> None:
    section_ids = configured_section_ids()

    if not section_ids:
        raise RunnerError(
            "BOOK_HAS_NO_CONFIGURED_SECTIONS"
        )

    print("book_mode=true")
    print(
        f"configured_sections={len(section_ids)}"
    )

    for section_id in section_ids:

        if is_section_frozen(section_id):
            print(
                f"section={section_id} "
                "status=FROZEN "
                "action=SKIP"
            )
            continue

        print()
        print(
            f"book_current_section={section_id}"
        )

        try:
            execute_section(
                section_id=section_id,
                model=model,
                api_base=api_base,
                no_freeze=False,
                resume=resume,
            )

        except RunnerError as exc:
            print(
                f"BOOK_RUN_STOPPED "
                f"section={section_id} "
                f"reason={exc}",
                file=sys.stderr,
            )
            raise

        # Fail closed: next section is reached only
        # if this one is actually frozen.
        if not is_section_frozen(section_id):
            raise RunnerError(
                f"BOOK_SECTION_NOT_FROZEN: "
                f"{section_id}"
            )

    print()
    print("BOOK_RUN_COMPLETE")
    print(
        "all_configured_sections_frozen=true"
    )



def build_section_sources_block(section_id: str, manifest: dict) -> str:
    evidence_audit_path = manifest.get("evidence_audit_path") or manifest.get(
        "audit_path"
    )
    compact_packet_path = manifest.get("source_compact_packet_path")

    if not evidence_audit_path:
        return ""

    if not compact_packet_path:
        fallback = section_paths(section_id)["compact_packet"]
        compact_packet_path = fallback if fallback.is_file() else None

    if not compact_packet_path:
        return ""

    evidence_audit = load_json(Path(evidence_audit_path))
    compact_packet = load_json(Path(compact_packet_path))

    citation_by_claim = {
        entry["claim_id"]: entry
        for entry in compact_packet.get("citation_mapping", [])
    }

    used_claim_ids: list[str] = []
    for entry in evidence_audit.get("sentence_audit", []):
        for claim_id in entry.get("supporting_claim_ids", []):
            if claim_id not in used_claim_ids:
                used_claim_ids.append(claim_id)

    sources: dict[tuple, list[str]] = {}
    for claim_id in used_claim_ids:
        citation = citation_by_claim.get(claim_id)
        if citation is None:
            continue
        key = (citation["document_id"], citation.get("source_relative_path", ""))
        sources.setdefault(key, [])
        locator = citation.get("locator", "")
        if locator and locator not in sources[key]:
            sources[key].append(locator)

    if not sources:
        return ""

    lines = [f"**Kaynaklar ({section_id})**", ""]
    for (document_id, source_relative_path), locators in sorted(sources.items()):
        locator_text = f" ({', '.join(sorted(locators))})" if locators else ""
        label = source_relative_path or document_id
        lines.append(f"- {document_id} — {label}{locator_text}")

    return "\n".join(lines)


def assemble_book() -> None:
    section_ids = configured_section_ids()

    if not section_ids:
        raise RunnerError(
            "BOOK_HAS_NO_CONFIGURED_SECTIONS"
        )

    not_frozen = [
        section_id
        for section_id in section_ids
        if not is_section_frozen(section_id)
    ]

    if not_frozen:
        raise RunnerError(
            "BOOK_ASSEMBLY_BLOCKED: "
            f"not_frozen={','.join(not_frozen)}"
        )

    sections: list[dict] = []
    body_parts: list[str] = []

    for section_id in section_ids:
        manifest_path = section_freeze_manifest(section_id)
        manifest = load_json(manifest_path)

        draft_path = Path(manifest["draft_path"])
        if not draft_path.is_absolute():
            draft_path = ROOT / draft_path

        require_file(draft_path, "DRAFT_NOT_FOUND")
        draft_text = draft_path.read_text(encoding="utf-8").strip("\n")

        sources_block = build_section_sources_block(section_id, manifest)
        if sources_block:
            draft_text = f"{draft_text}\n\n{sources_block}"

        body_parts.append(draft_text)

        sections.append(
            {
                "section_id": section_id,
                "section_title": manifest.get("section_title"),
                "status": manifest.get("status"),
                "frozen_at": manifest.get("frozen_at"),
                "draft_sha256": manifest.get("draft_sha256"),
                "audit_identity": manifest.get("audit_identity"),
                "evidence_contract_version": manifest.get(
                    "evidence_contract_version"
                ),
                "editorial_policy_version": manifest.get(
                    "editorial_policy_version"
                ),
                "model_id": manifest.get("model_id"),
                "freeze_manifest_path": str(manifest_path),
            }
        )

    book_md = "\n\n".join(body_parts) + "\n"

    book_path = FINAL_DIR / "book.md"
    book_path.write_text(book_md, encoding="utf-8")

    book_manifest = {
        "assembled_at": datetime.now(timezone.utc).isoformat(),
        "section_count": len(sections),
        "sections": sections,
        "book_path": str(book_path),
        "book_sha256": hashlib.sha256(
            book_md.encode("utf-8")
        ).hexdigest(),
        "privacy_mode": "LOCAL_ONLY",
    }

    manifest_path = FINAL_DIR / "book_manifest.json"
    manifest_path.write_text(
        json.dumps(book_manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"BOOK_ASSEMBLED={book_path}")
    print(f"BOOK_MANIFEST={manifest_path}")
    print(f"section_count={len(sections)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="TunnelBookAI local book/section runner"
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # -----------------------------------------------------
    # SECTION
    # -----------------------------------------------------

    section = sub.add_parser(
        "section",
        help="Run one configured book section.",
    )

    section.add_argument(
        "section_id"
    )

    section.add_argument(
        "--model",
        default="qwen3.6-35b-a3b-mlx",
    )

    section.add_argument(
        "--api-base",
        default="http://127.0.0.1:1234",
    )

    section.add_argument(
        "--no-freeze",
        action="store_true",
    )

    section.add_argument(
        "--resume",
        action="store_true",
        help=(
            "Reuse the latest validated READY "
            "remediation packet."
        ),
    )

    # -----------------------------------------------------
    # FREEZE
    # -----------------------------------------------------

    freeze_cmd = sub.add_parser(
        "freeze",
        help=(
            "Freeze an existing V2-audited section "
            "without rerunning the model."
        ),
    )

    freeze_cmd.add_argument(
        "section_id"
    )

    freeze_cmd.add_argument(
        "--model",
        default="qwen3.6-35b-a3b-mlx",
        help="Model that produced the audited draft (recorded in the manifest).",
    )

    freeze_cmd.add_argument(
        "--api-base",
        default="http://127.0.0.1:1234",
    )

    # -----------------------------------------------------
    # BOOK
    # -----------------------------------------------------

    book = sub.add_parser(
        "book",
        help=(
            "Run configured sections in order, "
            "skipping frozen sections."
        ),
    )

    book.add_argument(
        "--model",
        default="qwen3.6-35b-a3b-mlx",
    )

    book.add_argument(
        "--api-base",
        default="http://127.0.0.1:1234",
    )

    book.add_argument(
        "--resume",
        action="store_true",
        help=(
            "Reuse validated READY remediation "
            "artifacts where available."
        ),
    )

    # -----------------------------------------------------
    # ASSEMBLE
    # -----------------------------------------------------

    sub.add_parser(
        "assemble",
        help=(
            "Assemble book.md and book_manifest.json from "
            "all frozen configured sections."
        ),
    )

    args = parser.parse_args()

    # -----------------------------------------------------
    # DISPATCH
    # -----------------------------------------------------

    if args.command == "section":

        execute_section(
            section_id=args.section_id,
            model=args.model,
            api_base=args.api_base,
            no_freeze=args.no_freeze,
            resume=args.resume,
        )

        return

    if args.command == "freeze":

        paths = section_paths(
            args.section_id
        )

        require_file(
            paths["draft"],
            "DRAFT_NOT_FOUND",
        )

        require_file(
            paths["sentence_map"],
            "SENTENCE_MAP_NOT_FOUND",
        )

        require_file(
            paths["compact_packet"],
            "COMPACT_PACKET_NOT_FOUND",
        )

        require_file(
            paths["evidence_audit"],
            "EVIDENCE_AUDIT_NOT_FOUND",
        )

        require_file(
            paths["editorial_audit"],
            "EDITORIAL_AUDIT_NOT_FOUND",
        )

        try:
            validate_evidence_audit(
                paths["sentence_map"],
                paths["evidence_audit"],
                paths["compact_packet"],
            )
        except AuditContractError as exc:
            raise RunnerError(
                f"FREEZE_REJECTED: {exc}"
            ) from exc

        try:
            deterministic_editorial_gate(
                paths["draft"],
                paths["editorial_audit"],
            )
        except EditorialHardGateError as exc:
            raise RunnerError(
                f"FREEZE_REJECTED: {exc}"
            ) from exc

        freeze(
            args.section_id,
            paths,
            model=args.model,
            api_base=args.api_base,
        )

        return

    if args.command == "book":

        execute_book(
            model=args.model,
            api_base=args.api_base,
            resume=args.resume,
        )

        return

    if args.command == "assemble":

        assemble_book()

        return

    raise RunnerError(
        f"UNKNOWN_COMMAND: {args.command}"
    )


if __name__ == "__main__":
    try:
        main()
    except RunnerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
