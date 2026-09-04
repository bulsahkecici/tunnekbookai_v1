"""The single Turkish case-folding table used by every text-matching surface (task §13).

NFKD decomposes ş/ğ/ç/ö/ü into a base letter plus a combining mark, so stripping combining
marks folds them onto ASCII. The Turkish dotless ı (U+0131) has NO decomposition, and the
dotted İ (U+0130) casefolds to `i` + U+0307 rather than to `i`. Without an explicit table:

    * "Bakımı" normalizes to "bak m" wherever non-ASCII is dropped (the original dedup bug);
    * "KAZI".casefold() is "kazi" while "kazı" stays "kazı", so an ALL-CAPS Turkish heading
      never matches the same lowercase taxonomy term (the classification bug).

Turkish headings and document titles are very frequently ALL CAPS in this corpus, so both
directions of that asymmetry have to collapse to one form. One table, imported everywhere,
so the two normalizers can never drift apart again.
"""

from __future__ import annotations

# ligature ﬁ is folded here too: NFKD expands it to "fi", but folding first keeps the
# behaviour identical whether or not a caller reaches NFKD.
TURKISH_FOLD = str.maketrans({"ı": "i", "İ": "i", "ﬁ": "fi"})


def fold_turkish(value: str) -> str:
    """Collapse the Turkish dotted/dotless i distinction before any NFKD/casefold pass."""
    return str(value).translate(TURKISH_FOLD)
