"""The word rule: a word is a run of non-whitespace characters separated by whitespace.

This module performs no file, process or console I/O (ADR-0002).
"""


def count_words(text: str) -> int:
    """Return the number of whitespace-separated words in ``text``."""
    return len(text.split())
