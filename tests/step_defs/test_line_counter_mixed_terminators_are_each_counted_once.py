"""Step definitions for the 'mixed terminators are each counted once' scenario."""

from pytest_bdd import given, scenario, then, when

from hello.lines import count_lines


@scenario(
    "../features/line-counter-mixed-terminators-are-each-counted-once.feature",
    "mixed terminators are each counted once",
)
def test_mixed_terminators_are_each_counted_once() -> None:
    """Run the scenario end to end."""


@given(
    "the text 'a\\nb\\rc\\r\\nd\\x0be\\x0cf\\x1cg\\x1dh\\x1ei\\x85j\\u2028k\\u2029'",
    target_fixture="text",
)
def build_text() -> str:
    return "a\nb\rc\r\nd\x0be\x0cf\x1cg\x1dh\x1ei\x85j\u2028k\u2029"


@when("count_lines is called on it", target_fixture="result")
def call_count_lines(text: str) -> int:
    return count_lines(text)


@then("it returns 11")
def check_result(result: int) -> None:
    assert result == 11
