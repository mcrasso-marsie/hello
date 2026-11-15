"""Step definitions for the 'LINE_TERMINATORS enumerates exactly the ten
terminator code points' scenario.
"""

import importlib

from pytest_bdd import given, scenario, then, when


@scenario(
    "../features/line-counter-enumerates-the-ten-terminator-code-points.feature",
    "LINE_TERMINATORS enumerates exactly the ten terminator code points",
)
def test_line_terminators_enumerates_exactly_the_ten_terminator_code_points() -> None:
    """Run the scenario end to end."""


@given("the module hello.lines is importable")
def lines_module_importable() -> None:
    importlib.import_module("hello.lines")


@when("LINE_TERMINATORS is read", target_fixture="line_terminators")
def read_line_terminators() -> frozenset[str]:
    from hello.lines import LINE_TERMINATORS

    return LINE_TERMINATORS


@then(
    "it equals frozenset({'\\n', '\\x0b', '\\x0c', '\\r', '\\x1c', '\\x1d', "
    "'\\x1e', '\\x85', '\\u2028', '\\u2029'})"
)
def check_line_terminators_value(line_terminators: frozenset[str]) -> None:
    assert line_terminators == frozenset(
        {"\n", "\x0b", "\x0c", "\r", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"}
    )


@then("its length is 10")
def check_line_terminators_length(line_terminators: frozenset[str]) -> None:
    assert len(line_terminators) == 10
