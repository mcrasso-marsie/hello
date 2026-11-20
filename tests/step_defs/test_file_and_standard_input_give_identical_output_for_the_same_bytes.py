"""Step definitions for the 'file and standard input give identical output for the same bytes' scenario (SPEC-0004)."""

import io
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from hello.cli import main


@dataclass(frozen=True)
class Run:
    status: int
    stdout: bytes


@dataclass
class Comparison:
    samples: list[bytes] = field(default_factory=list)
    files: list[Path] = field(default_factory=list)
    file_runs: list[Run] = field(default_factory=list)
    stdin_runs: list[Run] = field(default_factory=list)


@scenario(
    "../features/file-and-standard-input-give-identical-output-for-the-same-bytes.feature",
    "file and standard input give identical output for the same bytes",
)
def test_file_and_standard_input_give_identical_output_for_the_same_bytes() -> None:
    """Run the scenario end to end."""


@given(
    "the byte samples b'a b\\n', b'a\\r\\nb\\r\\n', b'a\\rb\\r' and 'café naïve 日本\\n' encoded as UTF-8",
    target_fixture="comparison",
)
def define_samples() -> Comparison:
    return Comparison(
        samples=[
            b"a b\n",
            b"a\r\nb\r\n",
            b"a\rb\r",
            "café naïve 日本\n".encode(),
        ]
    )


@given("each sample is written unchanged to its own temporary file")
def write_samples(comparison: Comparison, tmp_path: Path) -> None:
    for index, data in enumerate(comparison.samples):
        path = tmp_path / f"sample-{index}.txt"
        path.write_bytes(data)
        comparison.files.append(path)


@when(
    "for each sample, `wordcount PATH` runs on its file and `wordcount -` runs "
    "with the sample on standard input"
)
def run_both_sources(
    comparison: Comparison,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    for data, path in zip(comparison.samples, comparison.files, strict=True):
        status = main([str(path)])
        comparison.file_runs.append(
            Run(status, capsys.readouterr().out.encode("utf-8"))
        )

        monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(data)))
        status = main(["-"])
        comparison.stdin_runs.append(
            Run(status, capsys.readouterr().out.encode("utf-8"))
        )


@then("for every sample, the two stdout lines are byte-for-byte identical")
def check_stdout_identical(comparison: Comparison) -> None:
    for file_run, stdin_run in zip(
        comparison.file_runs, comparison.stdin_runs, strict=True
    ):
        assert file_run.stdout == stdin_run.stdout


@then("for every sample, both runs exit with status 0")
def check_exit_status(comparison: Comparison) -> None:
    for run in [*comparison.file_runs, *comparison.stdin_runs]:
        assert run.status == 0


@then("the sample b'a\\rb\\r' reports `lines: 2` from both sources")
def check_lone_cr_lines(comparison: Comparison) -> None:
    lone_cr_index = comparison.samples.index(b"a\rb\r")
    expected = b"words: 2 characters: 2 lines: 2\n"
    assert comparison.file_runs[lone_cr_index].stdout == expected
    assert comparison.stdin_runs[lone_cr_index].stdout == expected
