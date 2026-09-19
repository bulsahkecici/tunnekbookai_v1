"""Repair PDF text layers that isolate Turkish glyphs with spaces (``TEKN İ K``, ``k ı sa``).

Some Turkish PDFs (notably older theses and KGM publications) embed ı/İ/ş/Ş/ğ/Ğ/ü/Ü/ö/Ö/ç/Ç
through a separate font program; the extracted text layer then carries a space on both
sides of every such glyph.  A lone special glyph is never a Turkish word, so each one belongs
to its left neighbour, its right neighbour, or both — and only a lexicon can say which
(``k ı salmas ı ve`` is ``kısalması ve``, ``Ak ı ll ı Ş ehir`` is ``Akıllı Şehir``).

The repair walks maximal runs of ``word glyph word glyph …`` tokens, enumerates every
left/right attachment choice for the glyphs in the run, and keeps the choice whose resulting
words are best covered by ``config/turkish_lexicon.txt`` (folded forms harvested from the
undamaged Turkish canonical documents).  Ties prefer fewer, longer words.  Documents whose
damage density is below ``MIN_DENSITY`` are left untouched so ordinary text never changes.
"""

from __future__ import annotations

import itertools
import math
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping

LEXICON_RELATIVE_PATH = Path("config") / "turkish_lexicon.txt"
SPECIAL = "ışğüöçİŞĞÜÖÇ"
MIN_DENSITY = 1.0 / 2000.0  # one isolated glyph per 2,000 characters
MIN_OCCURRENCES = 8
MAX_RUN_GLYPHS = 8

_ISOLATED = re.compile(rf"(?<!\S)[{SPECIAL}](?!\S)")
# Apostrophe suffixes stay attached (``KGM'nin``) so bare suffixes are never harvested as words.
_WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?", re.UNICODE)
_TURKISH_LOWER = str.maketrans({"I": "ı", "İ": "i"})
_TOKEN_SPLIT = re.compile(r"(\s+)")


def fold_word(value: str) -> str:
    """Turkish-aware lowercase that keeps ı and i distinct (``ızın`` must not match ``izin``).

    The corpus-wide ``textfold`` table collapses ı/İ onto i because ALL-CAPS headings must
    match lowercase taxonomy terms; here the opposite is needed, since the whole question is
    which dotted/dotless reading forms a real word.
    """

    return unicodedata.normalize("NFC", value.translate(_TURKISH_LOWER).lower())


class Lexicon(dict):
    """Folded word form -> corpus frequency; hashable so it can back an lru_cache."""

    def __hash__(self) -> int:  # type: ignore[override]
        return id(self)


@lru_cache(maxsize=4)
def load_lexicon(path: Path) -> Lexicon:
    lexicon = Lexicon()
    if not path.is_file():
        return lexicon
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        word, _, count = line.partition("\t")
        lexicon[word] = int(count) if count.isdigit() else 1
    return lexicon


def damage_stats(text: str) -> dict[str, Any]:
    occurrences = len(_ISOLATED.findall(text))
    chars = max(len(text), 1)
    return {
        "isolated_glyphs": occurrences,
        "chars": len(text),
        "density": occurrences / chars,
        "damaged": occurrences >= MIN_OCCURRENCES and occurrences / chars >= MIN_DENSITY,
    }


def _is_glyph(token: str) -> bool:
    return len(token) == 1 and token in SPECIAL


_EDGE_PUNCTUATION = re.compile(r"^[^\w]+|[^\w]+$", re.UNICODE)


def _core(token: str) -> str:
    return _EDGE_PUNCTUATION.sub("", token)


def _word_like(token: str) -> bool:
    return bool(token) and bool(_WORD.fullmatch(_core(token)))


# Corpus frequency a glyph-adjacent fragment needs before it may stand as a word without
# document-local evidence; shorter fragments are more often suffix debris, so they need more.
GLOBAL_FREQUENCY_BY_LENGTH = ((8, 2), (6, 5), (4, 20))


def standalone_tokens(text: str) -> frozenset[str]:
    """Casefolded tokens that occur in ``text`` with no isolated glyph on either side.

    Suffix fragments produced by the damage (``undan``, ``nda``, ``ım``) only ever appear next
    to an isolated glyph, whereas genuine words also appear on their own somewhere in the same
    document.  Fragments of three characters or fewer are accepted only on this local
    evidence, never on corpus frequency alone.
    """

    tokens = text.split()
    found: set[str] = set()
    for index, token in enumerate(tokens):
        core = _core(token)
        if not core or _is_glyph(core):
            continue
        left = tokens[index - 1] if index > 0 else ""
        right = tokens[index + 1] if index + 1 < len(tokens) else ""
        if _is_glyph(left) or _is_glyph(right):
            continue
        found.add(fold_word(core))
    return frozenset(found)


def _known(core: str, lexicon: Mapping[str, int], standalone: frozenset[str]) -> int:
    """Corpus frequency when ``core`` may stand as a word here, else 0."""

    frequency = lexicon.get(fold_word(core), 0)
    if not frequency:
        return 0
    if fold_word(core) in standalone:
        return frequency
    for minimum_length, minimum_frequency in GLOBAL_FREQUENCY_BY_LENGTH:
        if len(core) >= minimum_length:
            return frequency if frequency >= minimum_frequency else 0
    return 0


_VOWELS = set("aeıioöuüAEIİOÖUÜ")
_LOAN_ONSETS = {"tr", "pr", "kr", "gr", "br", "dr", "fr", "pl", "kl", "gl", "bl", "fl", "sp", "st", "sk", "sl", "sm", "sn", "ps", "sf"}


def _suffix_debris(core: str) -> bool:
    """An unknown fragment that cannot begin a Turkish word: vowel-initial or bad onset."""

    lowered = fold_word(core)
    if not lowered:
        return False
    if lowered[0] in _VOWELS:
        return True
    if len(lowered) >= 2 and lowered[1] not in _VOWELS and lowered[:2] not in _LOAN_ONSETS:
        return True
    return False


def _score(
    pieces: Iterable[tuple[str, bool]], lexicon: Mapping[str, int], standalone: frozenset[str]
) -> tuple[int, float, int]:
    """(-unknown weight, frequency-weighted covered characters, -word count).

    ``pieces`` are (word, follows_glyph) pairs.  A split is preferred only when it leaves no
    unknown fragment; among fully recognised readings the everyday one wins (``Kazılar
    İçin`` over ``Kazıları Çin``).  An unknown fragment that starts right after a detached
    glyph and could not begin a Turkish word (``ımızın``, ``undan``, ``ndan``) counts double,
    so the fully joined word is kept instead of shredding it into suffix debris.
    """

    covered = 0.0
    count = 0
    unknown = 0
    for word, follows_glyph in pieces:
        count += 1
        core = _core(word)
        if not core:
            continue
        frequency = _known(core, lexicon, standalone)
        if frequency:
            covered += len(core) * math.log1p(frequency)
        elif follows_glyph and _suffix_debris(core):
            unknown += 2
        else:
            unknown += 1
    return -unknown, covered, -count


def _resolve_run(tokens: list[str], lexicon: Mapping[str, int], standalone: frozenset[str]) -> list[str]:
    """Attach every glyph in ``tokens`` (words and isolated glyphs) using the best-scoring choice.

    Each glyph chooses whether the space before it and the space after it survive:
    ``B`` removes both (mid-word), ``L`` keeps the space after (word-final glyph), ``R`` keeps
    the space before (word-initial glyph).  Every combination is scored against the lexicon.
    """

    glyph_positions = [index for index, token in enumerate(tokens) if _is_glyph(token)]
    if not glyph_positions:
        return tokens
    if len(glyph_positions) > MAX_RUN_GLYPHS or not lexicon:
        return [_join_all(tokens)]
    best: tuple[tuple[int, float, int], list[str]] | None = None
    for choices in itertools.product("BLR", repeat=len(glyph_positions)):
        choice_by_position = dict(zip(glyph_positions, choices))
        separators = [" "] * (len(tokens) - 1)  # separator i sits between token i and i+1
        for position, choice in choice_by_position.items():
            if choice in {"B", "L"} and position > 0:
                separators[position - 1] = ""
            if choice in {"B", "R"} and position < len(tokens) - 1:
                separators[position] = ""
        pieces: list[tuple[str, bool]] = []
        current = tokens[0]
        follows = False
        for index, separator in enumerate(separators):
            if separator:
                pieces.append((current, follows))
                current = tokens[index + 1]
                # A piece that follows a detached glyph, or starts with one, is where
                # suffix debris shows up.
                follows = _is_glyph(tokens[index]) or _is_glyph(tokens[index + 1])
            else:
                current += tokens[index + 1]
        pieces.append((current, follows))
        score = _score(pieces, lexicon, standalone)
        if best is None or score > best[0]:
            best = (score, [piece for piece, _ in pieces])
    return best[1] if best else [_join_all(tokens)]


def _join_all(tokens: list[str]) -> str:
    return "".join(tokens)


def repair_text(text: str, lexicon: Mapping[str, int], standalone: frozenset[str] | None = None) -> tuple[str, int]:
    """Return the repaired text and the number of glyphs attached.

    ``standalone`` should be computed once from the whole document (``standalone_tokens``)
    when repairing individual elements, so short elements still benefit from document-wide
    evidence about which fragments are real words.
    """

    if not _ISOLATED.search(text):
        return text, 0
    if standalone is None:
        standalone = standalone_tokens(text)
    parts = _TOKEN_SPLIT.split(text)
    # parts alternates token, whitespace, token, ...; keep newlines intact by only merging
    # runs joined by single spaces.
    output: list[str] = []
    joined = 0
    index = 0
    while index < len(parts):
        token = parts[index]
        if index % 2 == 1:  # whitespace
            output.append(token)
            index += 1
            continue
        # Collect a run: token (sp) glyph (sp) token (sp) glyph ... where separators are " ".
        run = [token]
        cursor = index
        while (
            cursor + 2 < len(parts)
            and parts[cursor + 1] == " "
            and (_is_glyph(parts[cursor + 2]) or _is_glyph(run[-1]))
            and (_word_like(parts[cursor + 2]) or _is_glyph(parts[cursor + 2]))
        ):
            run.append(parts[cursor + 2])
            cursor += 2
        if any(_is_glyph(piece) for piece in run) and len(run) > 1:
            resolved = _resolve_run(run, lexicon, standalone)
            joined += sum(1 for piece in run if _is_glyph(piece))
            output.append(" ".join(resolved))
            index = cursor + 1
        else:
            output.append(token)
            index += 1
    return "".join(output), joined


def repair_elements(elements: list[dict[str, Any]], lexicon: Mapping[str, int], standalone: frozenset[str]) -> int:
    """Repair element text and heading paths in place; returns the number of glyphs attached."""

    joined = 0
    for element in elements:
        for key in ("text", "caption"):
            value = element.get(key)
            if isinstance(value, str) and value:
                repaired, count = repair_text(value, lexicon, standalone)
                if count:
                    element[key] = repaired
                    joined += count
        path = element.get("heading_path")
        if isinstance(path, list):
            new_path = []
            for entry in path:
                repaired, count = repair_text(str(entry), lexicon, standalone)
                joined += count
                new_path.append(repaired)
            element["heading_path"] = new_path
    return joined


def build_lexicon(texts: Iterable[str], *, minimum_frequency: int = 2, minimum_length: int = 2) -> list[tuple[str, int]]:
    """Harvest (folded word form, frequency) from undamaged text for ``config/turkish_lexicon.txt``."""

    counts: dict[str, int] = {}
    for text in texts:
        if damage_stats(text)["damaged"]:
            continue
        for match in _WORD.finditer(text):
            word = fold_word(match.group(0))
            if len(word) >= minimum_length:
                counts[word] = counts.get(word, 0) + 1
    return sorted((word, count) for word, count in counts.items() if count >= minimum_frequency)


def repair_extraction(result: Any, bundle: Path, root: Path) -> dict[str, Any] | None:
    """Post-extraction hook: repair a damaged text layer in place and rewrite normalized files.

    Runs for every adapter after extraction succeeded.  Returns the repair record (also
    stored on ``result.text_repair`` and surfaced as a warning code) or ``None`` when the
    document is not damaged.  The immutable original is never touched; only the derived
    normalized representations, element stream and asset captions change.
    """

    import json

    from .extraction import write_normalized

    if not result.normalized_text_path or not result.normalized_json_path:
        return None
    text_path = root / result.normalized_text_path
    json_path = root / result.normalized_json_path
    markdown_path = root / result.normalized_markdown_path if result.normalized_markdown_path else None
    try:
        text = text_path.read_text(encoding="utf-8")
    except OSError:
        return None
    stats = damage_stats(text)
    if not stats["damaged"]:
        return None
    lexicon = load_lexicon(root / LEXICON_RELATIVE_PATH)
    if not lexicon:
        result.warn("TURKISH_GLYPH_SPACING_DETECTED_NO_LEXICON")
        return None
    standalone = standalone_tokens(text)
    joined = repair_elements(result.text_elements, lexicon, standalone)
    for records in (result.figures, result.tables, result.charts):
        for record in records:
            caption = record.get("caption")
            if isinstance(caption, str) and caption:
                repaired, count = repair_text(caption, lexicon, standalone)
                if count:
                    record["caption"] = repaired
                    joined += count
    repaired_text, text_joined = repair_text(text, lexicon, standalone)
    markdown = markdown_path.read_text(encoding="utf-8") if markdown_path and markdown_path.is_file() else ""
    repaired_markdown, markdown_joined = repair_text(markdown, lexicon, standalone) if markdown else ("", 0)
    document_json = json.loads(json_path.read_text(encoding="utf-8"))
    if isinstance(document_json, dict):
        document_json["elements"] = result.text_elements
        document_json["text_repair"] = {"isolated_glyphs": stats["isolated_glyphs"], "attached": text_joined}
    write_normalized(bundle, result, markdown=repaired_markdown or markdown, document_json=document_json, text=repaired_text)
    record = {
        "reason": "TURKISH_GLYPH_SPACING",
        "isolated_glyphs_before": stats["isolated_glyphs"],
        "isolated_glyphs_after": damage_stats(repaired_text)["isolated_glyphs"],
        "attached_in_text": text_joined,
        "attached_in_markdown": markdown_joined,
        "attached_in_elements": joined,
        "lexicon": LEXICON_RELATIVE_PATH.as_posix(),
    }
    result.text_repair = record
    result.warn(f"TURKISH_GLYPH_SPACING_REPAIRED:{stats['isolated_glyphs']}")
    return record


__all__ = [
    "LEXICON_RELATIVE_PATH",
    "Lexicon",
    "build_lexicon",
    "damage_stats",
    "fold_word",
    "load_lexicon",
    "repair_elements",
    "repair_extraction",
    "repair_text",
    "standalone_tokens",
]
