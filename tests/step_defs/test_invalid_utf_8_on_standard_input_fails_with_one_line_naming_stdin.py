"""Step definitions for the 'invalid UTF-8 on standard input fails with one line naming <stdin>' scenario."""

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
    "../features/invalid-utf-8-on-standard-input-fails-with-one-line-naming-stdin.feature",
    "invalid UTF-8 on standard input fails with one line naming <stdin>",
)
def test_invalid_utf_8_on_standard_input_fails_with_one_line_naming_stdin() -> None:
    """Run the scenario end to end."""


@given("standard input holds the bytes b'\\xff\\xfe' and is closed")
def stdin_holds_invalid_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(b"\xff\xfe")))


@when("`wordcount -` runs", target_fixture="outcome")
def run_wordcount_dash(capsys: pytest.CaptureFixture[str]) -> Outcome:
    status = main(["-"])
    captured = capsys.readouterr()
    return Outcome(status=status, stdout=captured.out, stderr=captured.err)


@then(
    "stderr is exactly one line `wordcount: error: file is not valid UTF-8 text: <stdin>`"
)
def check_stderr_line(outcome: Outcome) -> None:
    assert outcome.stderr == "wordcount: error: file is not valid UTF-8 text: <stdin>\n"


@then("stderr does not contain `Traceback`")
def check_no_traceback(outcome: Outcome) -> None:
    assert "Traceback" not in outcome.stderr


@then("stdout is empty")
def check_stdout_empty(outcome: Outcome) -> None:
    assert outcome.stdout == ""


@then("the exit status is 1")
def check_exit_status(outcome: Outcome) -> None:
    assert outcome.status == 1
