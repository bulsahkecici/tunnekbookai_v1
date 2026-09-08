#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path


class EditorialHardGateError(RuntimeError):
    pass


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def deterministic_editorial_gate(
    draft_path: Path,
    editorial_audit_path: Path,
):
    if not draft_path.exists():
        raise EditorialHardGateError(
            f"DRAFT_NOT_FOUND: {draft_path}"
        )

    if not editorial_audit_path.exists():
        raise EditorialHardGateError(
            f"EDITORIAL_AUDIT_NOT_FOUND: {editorial_audit_path}"
        )

    text = draft_path.read_text(encoding="utf-8")
    audit = load_json(editorial_audit_path)

    blockers = []

    # --------------------------------------------------
    # 1. Empty / effectively empty draft
    # --------------------------------------------------
    body_lines = [
        x.strip()
        for x in text.splitlines()
        if x.strip() and not x.lstrip().startswith("#")
    ]

    if not body_lines:
        blockers.append("EMPTY_DRAFT")

    # --------------------------------------------------
    # 2. Broken Unicode / conversion artifacts
    # --------------------------------------------------
    if "\ufffd" in text:
        blockers.append("UNICODE_REPLACEMENT_CHARACTER")

    # --------------------------------------------------
    # 3. Known malformed-token patterns that are
    # objectively typographical, not stylistic.
    # --------------------------------------------------
    bad_patterns = {
        "yüzyıyıda": "TYPO_YUZYIYIDA",
    }

    for token, code in bad_patterns.items():
        if token in text:
            blockers.append(code)

    # --------------------------------------------------
    # 4. Incomplete final prose line
    # Ignore headings/table-ish/list-ish lines.
    # --------------------------------------------------
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()

        if not s:
            continue

        if s.startswith("#"):
            continue

        if s.startswith(("-", "*", "|", ">")):
            continue

        if re.match(r"^\d+[.)]\s", s):
            continue

        # Long prose lines should terminate normally.
        if len(s) >= 80 and s[-1] not in ".!?;:)”’":
            blockers.append(
                f"POSSIBLE_INCOMPLETE_LINE:{i}"
            )

    # --------------------------------------------------
    # 5. Exact duplicate prose paragraphs
    # --------------------------------------------------
    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", text)
        if p.strip() and not p.lstrip().startswith("#")
    ]

    seen = set()

    for p in paragraphs:
        normalized = re.sub(r"\s+", " ", p).strip()

        if len(normalized) < 80:
            continue

        if normalized in seen:
            blockers.append("EXACT_DUPLICATE_PARAGRAPH")
            break

        seen.add(normalized)

    # --------------------------------------------------
    # Model editorial audit is ADVISORY.
    #
    # It can still report:
    # - chronology preferences
    # - catalogue-like prose
    # - paragraph positioning
    # - repetition/style preferences
    #
    # These are retained but cannot independently reject
    # an evidence-valid section.
    # --------------------------------------------------
    advisory = {
        "model_decision": audit.get("decision"),
        "chronology_issues": audit.get(
            "chronology_issues", []
        ),
        "naming_ambiguities": audit.get(
            "naming_ambiguities", []
        ),
        "language_issues": audit.get(
            "language_issues", []
        ),
        "overgeneralizations": audit.get(
            "overgeneralizations", []
        ),
        "structure_issues": audit.get(
            "structure_issues", []
        ),
        "required_actions": audit.get(
            "required_actions", []
        ),
    }

    result = {
        "decision": "PASS" if not blockers else "HOLD",
        "deterministic_editorial_gate": (
            "PASS" if not blockers else "HOLD"
        ),
        "hard_blockers": blockers,
        "model_editorial_review": advisory,
        "policy": (
            "MODEL_EDITORIAL_ADVISORY_"
            "DETERMINISTIC_HARD_GATE_V1"
        ),
    }

    if blockers:
        raise EditorialHardGateError(
            "EDITORIAL_HARD_GATE_NOT_PASS: "
            + ", ".join(blockers)
        )

    return result


def main():
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: editorial_hard_gate.py "
            "<draft.md> <editorial_audit.json>"
        )

    result = deterministic_editorial_gate(
        Path(sys.argv[1]),
        Path(sys.argv[2]),
    )

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
