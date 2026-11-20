"""Step definitions for the 'guardrail: no argument is still a usage error and does not read stdin' scenario."""

# The subprocess argv is a fixed literal and `uv` is resolved from PATH on purpose, as in
# tests/test_console_script.py.
import os
import subprocess  # nosec B404
from dataclasses import dataclass
from pathlib import Path

from pytest_bdd import given, scenario, then, when

REPO_ROOT = Path(__file__).resolve().parents[2]
STDIN_TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class Outcome:
    returncode: int
    stdout: str
    stderr: str


def _run_without_argument(stdin_data: bytes) -> Outcome:
    """Run ``wordcount`` with no argument while its stdin is a pipe whose write end stays open.

    A command that reads stdin would block forever on that pipe, so it raises
    ``subprocess.TimeoutExpired`` instead of finishing.
    """
    read_fd, write_fd = os.pipe()
    try:
        os.write(write_fd, stdin_data)
        process = subprocess.Popen(  # nosec B603 B607
            ["uv", "run", "wordcount"],
            cwd=REPO_ROOT,
            stdin=read_fd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        os.close(read_fd)
        try:
            stdout, stderr = process.communicate(timeout=STDIN_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            raise
    finally:
        os.close(write_fd)
    return Outcome(returncode=process.returncode, stdout=stdout, stderr=stderr)


def _finished(outcome: Outcome | None) -> Outcome:
    assert outcome is not None, (
        f"wordcount did not finish within {STDIN_TIMEOUT_SECONDS}s"
    )
    return outcome


@scenario(
    "../features/guardrail-no-argument-is-still-a-usage-error-and-does-not-read-stdin.feature",
    "guardrail: no argument is still a usage error and does not read stdin",
)
def test_guardrail_no_argument_is_still_a_usage_error_and_does_not_read_stdin() -> None:
    """Run the scenario end to end."""


@given(
    "standard input is an open pipe holding the bytes b'a b\\n' that is never closed",
    target_fixture="stdin_data",
)
def stdin_is_open_pipe() -> bytes:
    return b"a b\n"


@when(
    "`wordcount` runs with no argument and a 10 second timeout",
    target_fixture="outcome",
)
def run_without_argument(stdin_data: bytes) -> Outcome | None:
    try:
        return _run_without_argument(stdin_data)
    except subprocess.TimeoutExpired:
        return None


@then("the process finishes before the timeout")
def check_finished(outcome: Outcome | None) -> None:
    _finished(outcome)


@then("stderr contains argparse usage text starting with `usage:`")
def check_usage_on_stderr(outcome: Outcome | None) -> None:
    assert _finished(outcome).stderr.startswith("usage:")


@then("stdout is empty")
def check_stdout_empty(outcome: Outcome | None) -> None:
    assert _finished(outcome).stdout == ""


@then("the exit status is 2")
def check_exit_status_two(outcome: Outcome | None) -> None:
    assert _finished(outcome).returncode == 2
