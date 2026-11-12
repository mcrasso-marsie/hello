"""Step definitions for the 'error output is a single line without traceback' scenario."""

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
    "../features/error-output-is-a-single-line-without-traceback.feature",
    "error output is a single line without traceback",
)
def test_error_output_is_a_single_line_without_traceback() -> None:
    """Run the scenario end to end."""


@given(
    "the missing-file, directory and undecodable-file cases",
    target_fixture="error_paths",
)
def error_paths(tmp_path: Path) -> list[Path]:
    undecodable = tmp_path / "binary.txt"
    undecodable.write_bytes(b"\xff\xfe\xfa")
    return [tmp_path / "missing.txt", tmp_path, undecodable]


@when(
    "the test tests/test_cli.py::test_errors_are_single_line_without_traceback runs",
    target_fixture="outcomes",
)
def run_error_cases(
    error_paths: list[Path], capsys: pytest.CaptureFixture[str]
) -> list[Outcome]:
    outcomes: list[Outcome] = []
    for path in error_paths:
        status = main([str(path)])
        captured = capsys.readouterr()
        outcomes.append(
            Outcome(status=status, stdout=captured.out, stderr=captured.err)
        )
    return outcomes


def _assert_one_error_line(outcome: Outcome) -> None:
    assert outcome.stdout == ""
    assert len(outcome.stderr.splitlines()) == 1
    assert outcome.stderr.startswith("wordcount: error: ")
    assert "Traceback" not in outcome.stderr


@then("it passes")
def check_error_outputs(outcomes: list[Outcome]) -> None:
    for outcome in outcomes:
        assert outcome.status == 1
        _assert_one_error_line(outcome)
