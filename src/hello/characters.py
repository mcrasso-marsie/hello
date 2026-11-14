"""The character rule: a visible character is a non-whitespace code point that is not a mark.

Whitespace is ``str.isspace()``, the same definition the word rule uses. Combining marks
(Unicode categories Mn, Mc, Me) never add to the count, so a base character followed by
combining marks counts once.

This module performs no file, process or console I/O (ADR-0002).
"""

import unicodedata


def count_characters(text: str) -> int:
    """Return the number of visible characters in ``text``."""
    return sum(
        1
        for char in text
        if not char.isspace() and not unicodedata.category(char).startswith("M")
    )
