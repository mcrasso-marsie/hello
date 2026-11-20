"""Step definitions for the 'guardrail: a file literally named dash is still counted through ./-' scenario."""

import io
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from hello.cli import main


@dataclass(frozen=True)
class Outcome:
    status: int
    stdout: str
    stderr: str


@scenario(
    "../features/guardrail-file-literally-named-dash-is-counted-through-dot-slash.feature",
    "guardrail: a file literally named dash is still counted through ./-",
)
def test_guardrail_file_literally_named_dash_is_counted_through_dot_slash() -> None:
    """Run the scenario end to end."""


@given(
    "the working directory holds a file named `-` containing 'x y\\n'",
    target_fixture="working_dir",
)
def write_dash_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    (tmp_path / "-").write_bytes(b"x y\n")
    monkeypatch.chdir(tmp_path)
    return tmp_path


@given("standard input holds zero bytes and is closed")
def stdin_is_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(b"")))


@when("`wordcount ./-` runs in that directory", target_fixture="outcome")
def run_wordcount_dot_slash_dash(
    working_dir: Path, capsys: pytest.CaptureFixture[str]
) -> Outcome:
    status = main(["./-"])
    captured = capsys.readouterr()
    return Outcome(status=status, stdout=captured.out, stderr=captured.err)


@then("stdout is exactly `words: 2 characters: 2 lines: 1\\n`")
def check_stdout(outcome: Outcome) -> None:
    assert outcome.stdout == "words: 2 characters: 2 lines: 1\n"


@then("the exit status is 0")
def check_exit_status(outcome: Outcome) -> None:
    assert outcome.status == 0
