"""Step definitions for the 'wordcount prints the count of a simple file' scenario."""

import codecs
from dataclasses import dataclass
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenario, then, when

from hello.cli import main


@dataclass(frozen=True)
class Outcome:
    status: int
    stdout: str
    stderr: str


def _unescape(text: str) -> str:
    """Turn the literal escapes written in the Gherkin text (such as ``\\n``) into characters."""
    return codecs.decode(text, "unicode_escape")


@scenario(
    "../features/wordcount-prints-the-count-of-a-simple-file.feature",
    "wordcount prints the count of a simple file",
)
def test_wordcount_prints_the_count_of_a_simple_file() -> None:
    """Run the scenario end to end."""


@given(
    parsers.parse('a temporary file notes.txt containing "{content}" encoded as UTF-8'),
    target_fixture="notes_path",
)
def write_notes_file(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "notes.txt"
    path.write_bytes(_unescape(content).encode("utf-8"))
    return path


@when(
    'main(["<path to notes.txt>"]) is called with stdout and stderr captured',
    target_fixture="outcome",
)
def call_main(notes_path: Path, capsys: pytest.CaptureFixture[str]) -> Outcome:
    status = main([str(notes_path)])
    captured = capsys.readouterr()
    return Outcome(status=status, stdout=captured.out, stderr=captured.err)


@then("the return value is 0")
def check_return_value(outcome: Outcome) -> None:
    assert outcome.status == 0


@then(parsers.parse('stdout is exactly "{expected}"'))
def check_stdout(outcome: Outcome, expected: str) -> None:
    assert outcome.stdout == _unescape(expected)


@then("stderr is empty")
def check_stderr_empty(outcome: Outcome) -> None:
    assert outcome.stderr == ""
