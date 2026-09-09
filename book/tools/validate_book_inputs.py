#!/usr/bin/env python3
"""Compatibility entry point for the central Book Production input loader."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from tunnelbookai.book.errors import BookEngineError  # noqa: E402
from tunnelbookai.book.inputs import load_book_inputs  # noqa: E402


try:
    inputs = load_book_inputs(PROJECT_ROOT)
except BookEngineError as exc:
    print("BOOK INPUT VALIDATION: FAIL")
    print(f"- {exc.code}: {exc}")
    raise SystemExit(1)

print("BOOK INPUT VALIDATION: PASS")
print(f"{len(inputs.question_section_ids)} question-bank sections / {len(inputs.questions)} questions")
print("Publication coverage hard gate: 1770 answered / 60%")
