"""Step definitions for the 'CRLF is a single boundary' scenario."""

from pytest_bdd import given, scenario, then, when

from hello.lines import count_lines


@scenario(
    "../features/line-counter-crlf-is-a-single-boundary.feature",
    "CRLF is a single boundary",
)
def test_crlf_is_a_single_boundary() -> None:
    """Run the scenario end to end."""


@given("the text 'a\\r\\n'", target_fixture="text")
def build_text() -> str:
    return "a\r\n"


@when("count_lines is called on it", target_fixture="result")
def call_count_lines(text: str) -> int:
    return count_lines(text)


@then("it returns 1")
def check_result(result: int) -> None:
    assert result == 1
