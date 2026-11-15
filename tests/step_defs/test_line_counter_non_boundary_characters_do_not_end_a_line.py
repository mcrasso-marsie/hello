"""Step definitions for the 'non-boundary characters do not end a line' scenario."""

from pytest_bdd import given, scenario, then, when

from hello.lines import count_lines

NON_BOUNDARY_CHARACTERS = (
    "\t",  # TAB
    " ",  # SPACE
    "\x1f",  # US
    "\xa0",  # NBSP
    "\u200b",  # ZERO WIDTH SPACE
    "\u3000",  # IDEOGRAPHIC SPACE
)


@scenario(
    "../features/line-counter-non-boundary-characters-do-not-end-a-line.feature",
    "non-boundary characters do not end a line",
)
def test_non_boundary_characters_do_not_end_a_line() -> None:
    """Run the scenario end to end."""


@given(
    "the text 'a' + c + 'b', for each c in TAB '\\t', SPACE ' ', US '\\x1f', "
    "NBSP '\\xa0', ZERO WIDTH SPACE '\\u200b' and IDEOGRAPHIC SPACE '\\u3000'",
    target_fixture="texts",
)
def build_texts() -> list[str]:
    return ["a" + character + "b" for character in NON_BOUNDARY_CHARACTERS]


@when("count_lines is called on that text", target_fixture="results")
def call_count_lines(texts: list[str]) -> list[int]:
    return [count_lines(text) for text in texts]


@then("it returns 0 for every one of the six cases")
def check_results(results: list[int]) -> None:
    assert len(results) == 6
    assert results == [0] * 6
