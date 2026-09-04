"""Token counting for the chunk policy (task §51).

`unicode-lexical-v1` is the same lexical tokenizer the validated legacy chunker uses
(`scripts/11_semantic_chunking.py`), so the token budgets carried over from that policy mean
the same thing here. It is a deterministic proxy for model tokens, not a model tokenizer —
which is exactly what a stable, offline chunk policy needs.
"""

from __future__ import annotations

import re

TOKENIZER_NAME = "unicode-lexical-v1"
TOKEN_RE = re.compile(r"\w+(?:[-'’]\w+)*|[^\w\s]", re.UNICODE)


def tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text or "")


def count(text: str) -> int:
    return len(TOKEN_RE.findall(text or ""))


def truncate_to(text: str, limit: int) -> str:
    """Cut `text` at a whitespace boundary so it fits `limit` tokens."""
    if count(text) <= limit:
        return text
    words = (text or "").split()
    low, high = 0, len(words)
    while low < high:
        mid = (low + high + 1) // 2
        if count(" ".join(words[:mid])) <= limit:
            low = mid
        else:
            high = mid - 1
    return " ".join(words[:low])


def tail_tokens(text: str, limit: int) -> str:
    """The last `limit` tokens of `text`, used to build chunk overlap."""
    if limit <= 0:
        return ""
    words = (text or "").split()
    low, high = 0, len(words)
    while low < high:
        mid = (low + high + 1) // 2
        if count(" ".join(words[len(words) - mid:])) <= limit:
            low = mid
        else:
            high = mid - 1
    return " ".join(words[len(words) - low:]) if low else ""
