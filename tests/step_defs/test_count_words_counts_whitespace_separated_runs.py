"""Step definitions for the 'count_words counts whitespace-separated runs' scenario."""

import importlib

from pytest_bdd import given, scenario, then, when


@scenario(
    "../features/count-words-counts-whitespace-separated-runs.feature",
    "count_words counts whitespace-separated runs",
)
def test_count_words_counts_whitespace_separated_runs() -> None:
    """Run the scenario end to end."""


@given("the hello.counter module is importable")
def counter_module_importable() -> None:
    importlib.import_module("hello.counter")


@when(
    'count_words is called with the string "one two three"',
    target_fixture="count",
)
def call_count_words() -> int:
    from hello.counter import count_words

    return count_words("one two three")


@then("it returns the integer 3")
def check_count(count: int) -> None:
    assert count == 3
