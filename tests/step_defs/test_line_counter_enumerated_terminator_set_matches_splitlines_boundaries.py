"""Step definitions for the 'enumerated terminator set matches str.splitlines
boundaries' scenario.

This is PBI-0001's own Verification Pointer scenario: it re-runs the exhaustive
cross-check that ``tests/test_lines.py::test_line_terminators_match_str_splitlines_boundaries``
performs, scanning every code point rather than sampling or skipping any of them.
"""

from pytest_bdd import given, scenario, then, when

from hello.lines import LINE_TERMINATORS

SURROGATE_RANGE = range(0xD800, 0xE000)


@scenario(
    "../features/line-counter-enumerated-terminator-set-matches-splitlines-boundaries.feature",
    "enumerated terminator set matches str.splitlines boundaries",
)
def test_enumerated_terminator_set_matches_splitlines_boundaries() -> None:
    """Run the scenario end to end."""


@given(
    "every code point from U+0000 to U+10FFFF, excluding surrogates U+D800 to U+DFFF",
    target_fixture="code_points",
)
def all_code_points_excluding_surrogates() -> range:
    return range(0x110000)


@when(
    "the test tests/test_lines.py::test_line_terminators_match_str_splitlines_boundaries runs",
    target_fixture="discovered_boundaries",
)
def run_the_cross_check(code_points: range) -> set[str]:
    boundaries: set[str] = set()
    for codepoint in code_points:
        if codepoint in SURROGATE_RANGE:
            continue
        character = chr(codepoint)
        if len(("a" + character + "b").splitlines()) == 2:
            boundaries.add(character)
    return boundaries


@then("it passes")
def check_passes() -> None:
    """The When step performs the scan; reaching here means it did not raise."""


@then(
    "the test asserts that LINE_TERMINATORS equals the set of code points c for "
    "which ('a' + c + 'b').splitlines() has length 2"
)
def check_boundaries_match(discovered_boundaries: set[str]) -> None:
    assert discovered_boundaries == set(LINE_TERMINATORS)
