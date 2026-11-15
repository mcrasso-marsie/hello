"""Step definitions for the 'empty text has zero lines' scenario."""

from pytest_bdd import given, scenario, then, when

from hello.lines import count_lines


@scenario(
    "../features/line-counter-empty-text-has-zero-lines.feature",
    "empty text has zero lines",
)
def test_empty_text_has_zero_lines() -> None:
    """Run the scenario end to end."""


@given("the empty string ''", target_fixture="text")
def build_text() -> str:
    return ""


@when("count_lines is called on it", target_fixture="result")
def call_count_lines(text: str) -> int:
    return count_lines(text)


@then("it returns 0")
def check_result(result: int) -> None:
    assert result == 0
