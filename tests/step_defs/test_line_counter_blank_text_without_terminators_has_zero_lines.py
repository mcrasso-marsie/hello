"""Step definitions for the 'blank text without terminators has zero lines' scenario."""

from pytest_bdd import given, scenario, then, when

from hello.lines import count_lines


@scenario(
    "../features/line-counter-blank-text-without-terminators-has-zero-lines.feature",
    "blank text without terminators has zero lines",
)
def test_blank_text_without_terminators_has_zero_lines() -> None:
    """Run the scenario end to end."""


@given("the text '  \\t '", target_fixture="text")
def build_text() -> str:
    return "  \t "


@when("count_lines is called on it", target_fixture="result")
def call_count_lines(text: str) -> int:
    return count_lines(text)


@then("it returns 0")
def check_result(result: int) -> None:
    assert result == 0
