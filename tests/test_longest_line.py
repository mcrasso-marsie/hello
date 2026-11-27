"""Unit tests for the pure longest-line counter (SPEC-0006)."""

import pytest

from hello.counter import count_words
from hello.longest_line import longest_line_words

TERMINATORS_BY_NAME = {
    "LF": "\n",
    "CR": "\r",
    "CRLF": "\r\n",
    "VT": "\x0b",
    "FF": "\x0c",
    "FS": "\x1c",
    "GS": "\x1d",
    "RS": "\x1e",
    "NEL": "\x85",
    "LS": "\u2028",
    "PS": "\u2029",
}

NON_TERMINATORS_BY_NAME = {
    "TAB": "\t",
    "SPACE": " ",
    "NBSP": "\xa0",
    "US": "\x1f",
    "IDEOGRAPHIC SPACE": "\u3000",
}


def test_longest_line_is_the_line_with_the_most_words() -> None:
    assert longest_line_words("one two\nthree four five\nsix\n") == 3


def test_unterminated_final_segment_counts_as_a_line() -> None:
    assert longest_line_words("a b c") == 3


def test_unterminated_final_segment_can_be_the_longest() -> None:
    assert longest_line_words("a\nb c d") == 3


def test_trailing_terminator_adds_no_extra_line() -> None:
    assert longest_line_words("a b\n") == 2


@pytest.mark.parametrize(
    "text", ["", "  \t ", "\n\n"], ids=["empty", "blank", "newlines"]
)
def test_text_without_words_gives_zero(text: str) -> None:
    assert longest_line_words(text) == 0


@pytest.mark.parametrize(
    "terminator", TERMINATORS_BY_NAME.values(), ids=TERMINATORS_BY_NAME.keys()
)
def test_each_terminator_ends_a_line(terminator: str) -> None:
    assert longest_line_words("a b c" + terminator + "d") == 3


def test_crlf_is_one_terminator() -> None:
    assert longest_line_words("a b\r\nc d e\rf") == 3


@pytest.mark.parametrize(
    "separator", NON_TERMINATORS_BY_NAME.values(), ids=NON_TERMINATORS_BY_NAME.keys()
)
def test_non_terminator_separators_keep_words_on_one_line(separator: str) -> None:
    assert longest_line_words("a" + separator + "b") == 2


@pytest.mark.parametrize(
    "text",
    [
        "",
        "alpha\t\tbeta  gamma ",
        "caf\u00e9 na\u00efve \u65e5\u672c",
        "Hello, world! It's-fine.",
    ],
)
def test_text_without_terminators_agrees_with_the_word_rule(text: str) -> None:
    assert longest_line_words(text) == count_words(text)
