"""Step definitions for the 'lone CR followed by CRLF is two boundaries' scenario."""

from pytest_bdd import given, scenario, then, when

from hello.lines import count_lines


@scenario(
    "../features/line-counter-lone-cr-followed-by-crlf-is-two-boundaries.feature",
    "lone CR followed by CRLF is two boundaries",
)
def test_lone_cr_followed_by_crlf_is_two_boundaries() -> None:
    """Run the scenario end to end."""


@given("the text '\\r\\r\\n'", target_fixture="text")
def build_text() -> str:
    return "\r\r\n"


@when("count_lines is called on it", target_fixture="result")
def call_count_lines(text: str) -> int:
    return count_lines(text)


@then("it returns 2")
def check_result(result: int) -> None:
    assert result == 2
