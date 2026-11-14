"""Unit tests for the pure character counter."""

import pytest

from hello.characters import count_characters


def test_whitespace_is_not_counted() -> None:
    assert count_characters("a b\tc\n") == 3


@pytest.mark.parametrize("text", ["", "  \t\n\n "])
def test_empty_and_whitespace_only_text_has_no_characters(text: str) -> None:
    assert count_characters(text) == 0


def test_non_ascii_characters_are_counted() -> None:
    assert count_characters("café naïve 日本") == 11


@pytest.mark.parametrize("text", ["\u00e9", "e\u0301"])
def test_combining_marks_do_not_add_to_count(text: str) -> None:
    assert count_characters(text) == 1
