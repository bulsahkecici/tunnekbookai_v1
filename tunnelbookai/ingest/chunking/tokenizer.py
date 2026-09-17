"""Token counting for the chunk policy (task §51).

`unicode-lexical-v1` is the same lexical tokenizer the validated legacy chunker uses
(the former validated semantic chunker), so the token budgets carried over from that policy mean
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
    """Return a source-text prefix containing at most ``limit`` lexical tokens.

    Cutting by whitespace-delimited words is unsafe for dense punctuation or binary-looking
    input: one such "word" can contain thousands of lexical tokens and yield an empty prefix.
    Token spans guarantee progress and preserve an exact prefix of the source string.
    """
    if limit <= 0 or not text:
        return ""
    cut = 0
    for index, match in enumerate(TOKEN_RE.finditer(text), 1):
        if index > limit:
            return text[:cut].rstrip()
        cut = match.end()
    return text


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
