"""Step definitions for the 'blank-only terminated lines are counted' scenario."""

from pytest_bdd import given, scenario, then, when

from hello.lines import count_lines


@scenario(
    "../features/line-counter-blank-only-terminated-lines-are-counted.feature",
    "blank-only terminated lines are counted",
)
def test_blank_only_terminated_lines_are_counted() -> None:
    """Run the scenario end to end."""


@given("the text '\\n\\n'", target_fixture="text")
def build_text() -> str:
    return "\n\n"


@when("count_lines is called on it", target_fixture="result")
def call_count_lines(text: str) -> int:
    return count_lines(text)


@then("it returns 2")
def check_result(result: int) -> None:
    assert result == 2
