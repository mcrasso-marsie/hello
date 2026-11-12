"""Unit tests for the pure word counter."""

import pytest

from hello.counter import count_words


def test_counts_whitespace_separated_runs() -> None:
    assert count_words("one two three") == 3


def test_whitespace_variants_act_only_as_separators() -> None:
    assert count_words("  alpha\t\tbeta\n\ngamma  ") == 3


@pytest.mark.parametrize("text", ["", " \t\n "])
def test_empty_and_whitespace_only_text_has_no_words(text: str) -> None:
    assert count_words(text) == 0
