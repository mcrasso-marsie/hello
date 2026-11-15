"""Step definitions for the 'each terminator alone ends one line' scenario."""

from pytest_bdd import given, scenario, then, when

from hello.lines import count_lines

TERMINATORS = (
    "\n",  # LF
    "\r",  # CR
    "\r\n",  # CRLF
    "\x0b",  # VT
    "\x0c",  # FF
    "\x1c",  # FS
    "\x1d",  # GS
    "\x1e",  # RS
    "\x85",  # NEL
    "\u2028",  # LS
    "\u2029",  # PS
)


@scenario(
    "../features/line-counter-each-terminator-alone-ends-one-line.feature",
    "each terminator alone ends one line",
)
def test_each_terminator_alone_ends_one_line() -> None:
    """Run the scenario end to end."""


@given(
    "the text 'a' followed by one terminator, for each of LF '\\n', CR '\\r', "
    "CRLF '\\r\\n', VT '\\x0b', FF '\\x0c', FS '\\x1c', GS '\\x1d', RS '\\x1e', "
    "NEL '\\x85', LS '\\u2028' and PS '\\u2029'",
    target_fixture="texts",
)
def build_texts() -> list[str]:
    return ["a" + terminator for terminator in TERMINATORS]


@when("count_lines is called on that text", target_fixture="results")
def call_count_lines(texts: list[str]) -> list[int]:
    return [count_lines(text) for text in texts]


@then("it returns 1 for every one of the 11 cases")
def check_results(results: list[int]) -> None:
    assert len(results) == 11
    assert results == [1] * 11
