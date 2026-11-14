"""Unit tests for the pure word and non-whitespace character counters."""

import pytest

from hello.counter import count_non_whitespace_chars, count_words


def test_counts_whitespace_separated_runs() -> None:
    assert count_words("one two three") == 3


def test_whitespace_variants_act_only_as_separators() -> None:
    assert count_words("  alpha\t\tbeta\n\ngamma  ") == 3


@pytest.mark.parametrize("text", ["", " \t\n "])
def test_empty_and_whitespace_only_text_has_no_words(text: str) -> None:
    assert count_words(text) == 0


def test_count_non_whitespace_chars_counts_hello_world() -> None:
    assert count_non_whitespace_chars("Hello, world!\n") == 12


def test_count_non_whitespace_chars_excludes_whitespace_variants() -> None:
    assert count_non_whitespace_chars("  alpha\t\tbeta\n\ngamma  ") == 14


@pytest.mark.parametrize("text", ["", " \t\n\r\u00a0"])
def test_count_non_whitespace_chars_empty_and_whitespace_only(text: str) -> None:
    assert count_non_whitespace_chars(text) == 0


def test_count_non_whitespace_chars_counts_unicode_characters() -> None:
    assert count_non_whitespace_chars("héllo, 世界!") == 9
