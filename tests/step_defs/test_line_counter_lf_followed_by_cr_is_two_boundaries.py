"""Step definitions for the 'LF followed by CR is two boundaries' scenario."""

from pytest_bdd import given, scenario, then, when

from hello.lines import count_lines


@scenario(
    "../features/line-counter-lf-followed-by-cr-is-two-boundaries.feature",
    "LF followed by CR is two boundaries",
)
def test_lf_followed_by_cr_is_two_boundaries() -> None:
    """Run the scenario end to end."""


@given("the text '\\n\\r'", target_fixture="text")
def build_text() -> str:
    return "\n\r"


@when("count_lines is called on it", target_fixture="result")
def call_count_lines(text: str) -> int:
    return count_lines(text)


@then("it returns 2")
def check_result(result: int) -> None:
    assert result == 2
