"""Step definitions for the 'unterminated final segment is not counted' scenario."""

from pytest_bdd import given, scenario, then, when

from hello.lines import count_lines


@scenario(
    "../features/line-counter-unterminated-final-segment-is-not-counted.feature",
    "unterminated final segment is not counted",
)
def test_unterminated_final_segment_is_not_counted() -> None:
    """Run the scenario end to end."""


@given("the texts 'a' and 'a\\nb'", target_fixture="texts")
def build_texts() -> tuple[str, str]:
    return ("a", "a\nb")


@when("count_lines is called on each", target_fixture="results")
def call_count_lines(texts: tuple[str, str]) -> tuple[int, int]:
    first, second = texts
    return (count_lines(first), count_lines(second))


@then("count_lines('a') returns 0")
def check_a(results: tuple[int, int]) -> None:
    assert results[0] == 0


@then("count_lines('a\\nb') returns 1")
def check_a_newline_b(results: tuple[int, int]) -> None:
    assert results[1] == 1
