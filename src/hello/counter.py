"""The counting rules: whitespace-separated words and non-whitespace characters.

This module performs no file, process or console I/O (ADR-0002).
"""


def count_words(text: str) -> int:
    """Return the number of whitespace-separated words in ``text``."""
    return len(text.split())


def count_non_whitespace_chars(text: str) -> int:
    """Return the number of characters in ``text`` where ``ch.isspace()`` is False."""
    return sum(1 for ch in text if not ch.isspace())
