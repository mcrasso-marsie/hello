"""Step definitions for 'count_non_whitespace_chars counts non-whitespace characters'."""

import codecs

from pytest_bdd import given, parsers, scenario, then, when

from hello.counter import count_non_whitespace_chars


@scenario(
    "../features/count-non-whitespace-chars-counts-non-whitespace-characters.feature",
    "count_non_whitespace_chars counts non-whitespace characters",
)
def test_count_non_whitespace_chars_counts_non_whitespace_characters() -> None:
    """Run the scenario end to end."""


@given(parsers.parse('the string "{text}"'), target_fixture="input_text")
def given_string(text: str) -> str:
    return codecs.decode(text, "unicode_escape")


@when(
    "count_non_whitespace_chars is called with that string",
    target_fixture="char_count",
)
def call_count_non_whitespace_chars(input_text: str) -> int:
    return count_non_whitespace_chars(input_text)


@then(parsers.parse("it returns {expected:d}"))
def check_char_count(char_count: int, expected: int) -> None:
    assert char_count == expected
