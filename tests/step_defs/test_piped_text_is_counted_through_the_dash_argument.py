"""Step definitions for the 'piped text is counted through the dash argument' scenario."""

import io
import sys
from dataclasses import dataclass

import pytest
from pytest_bdd import given, scenario, then, when

from hello.cli import main


@dataclass(frozen=True)
class Outcome:
    status: int
    stdout: str
    stderr: str


@scenario(
    "../features/piped-text-is-counted-through-the-dash-argument.feature",
    "piped text is counted through the dash argument",
)
def test_piped_text_is_counted_through_the_dash_argument() -> None:
    """Run the scenario end to end."""


@given("standard input holds the bytes b'a b\\n'")
def stdin_holds_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(b"a b\n")))


@when("`wordcount -` runs", target_fixture="outcome")
def run_wordcount_dash(capsys: pytest.CaptureFixture[str]) -> Outcome:
    status = main(["-"])
    captured = capsys.readouterr()
    return Outcome(status=status, stdout=captured.out, stderr=captured.err)


@then("stdout is exactly `words: 2 characters: 2 lines: 1\\n`")
def check_stdout(outcome: Outcome) -> None:
    assert outcome.stdout == "words: 2 characters: 2 lines: 1\n"


@then("stderr is empty")
def check_stderr_empty(outcome: Outcome) -> None:
    assert outcome.stderr == ""


@then("the exit status is 0")
def check_exit_status(outcome: Outcome) -> None:
    assert outcome.status == 0
