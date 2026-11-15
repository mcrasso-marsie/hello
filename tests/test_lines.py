"""Unit tests for the pure line counter (SPEC-0003, ADR-0007)."""

import pytest

from hello.lines import LINE_TERMINATORS, count_lines

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

NON_BOUNDARY_CHARACTERS_BY_NAME = {
    "TAB": "\t",
    "SPACE": " ",
    "US": "\x1f",
    "NBSP": "\xa0",
    "ZERO WIDTH SPACE": "\u200b",
    "IDEOGRAPHIC SPACE": "\u3000",
}


def test_line_terminators_enumerates_exactly_the_ten_terminator_code_points() -> None:
    assert LINE_TERMINATORS == frozenset(
        {"\n", "\x0b", "\x0c", "\r", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"}
    )
    assert len(LINE_TERMINATORS) == 10


@pytest.mark.parametrize(
    "terminator", TERMINATORS_BY_NAME.values(), ids=TERMINATORS_BY_NAME.keys()
)
def test_each_terminator_alone_ends_one_line(terminator: str) -> None:
    assert count_lines("a" + terminator) == 1


def test_unterminated_final_segment_is_not_counted() -> None:
    assert count_lines("a") == 0
    assert count_lines("a\nb") == 1


def test_empty_text_has_zero_lines() -> None:
    assert count_lines("") == 0


def test_blank_text_without_terminators_has_zero_lines() -> None:
    assert count_lines("  \t ") == 0


def test_blank_only_terminated_lines_are_counted() -> None:
    assert count_lines("\n\n") == 2


def test_crlf_is_a_single_boundary() -> None:
    assert count_lines("a\r\n") == 1


def test_lone_cr_followed_by_crlf_is_two_boundaries() -> None:
    assert count_lines("\r\r\n") == 2


def test_lf_followed_by_cr_is_two_boundaries() -> None:
    assert count_lines("\n\r") == 2


def test_mixed_terminators_are_each_counted_once() -> None:
    text = "a\nb\rc\r\nd\x0be\x0cf\x1cg\x1dh\x1ei\x85j\u2028k\u2029"
    assert count_lines(text) == 11


@pytest.mark.parametrize(
    "character",
    NON_BOUNDARY_CHARACTERS_BY_NAME.values(),
    ids=NON_BOUNDARY_CHARACTERS_BY_NAME.keys(),
)
def test_non_boundary_characters_do_not_end_a_line(character: str) -> None:
    assert count_lines("a" + character + "b") == 0


def test_line_terminators_match_str_splitlines_boundaries() -> None:
    """Cross-check: scan every code point and confirm the enumerated set matches.

    Scans U+0000 through U+10FFFF, excluding the surrogate range U+D800-U+DFFF,
    and compares the complete discovered boundary set with ``LINE_TERMINATORS``
    (ADR-0007), exposing any drift between the enumerated set and the
    interpreter's own ``str.splitlines()`` behaviour.
    """
    boundaries: set[str] = set()
    for codepoint in range(0x110000):
        if 0xD800 <= codepoint <= 0xDFFF:
            continue
        character = chr(codepoint)
        if len(("a" + character + "b").splitlines()) == 2:
            boundaries.add(character)

    assert boundaries == set(LINE_TERMINATORS)
