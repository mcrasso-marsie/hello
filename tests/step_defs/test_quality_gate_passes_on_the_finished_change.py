"""Step definitions for the 'Quality Gate passes on the finished change' scenario."""

# The subprocess argv are fixed literals (no untrusted input), and `uv` is resolved from
# PATH on purpose, as in tests/test_console_script.py.
import subprocess  # nosec B404
from pathlib import Path

from pytest_bdd import given, scenario, then, when

REPO_ROOT = Path(__file__).resolve().parents[2]

# Running the whole suite from inside this scenario would recurse into it, so the
# pytest command deselects this scenario's own test.
GATE_COMMANDS = (
    ["uv", "run", "ruff", "format", "--check", "."],
    ["uv", "run", "ruff", "check", "."],
    ["uv", "run", "mypy", "--strict", "src", "tests"],
    [
        "uv",
        "run",
        "pytest",
        "--deselect",
        "tests/step_defs/test_quality_gate_passes_on_the_finished_change.py",
    ],
)


@scenario(
    "../features/quality-gate-passes-on-the-finished-change.feature",
    "Quality Gate passes on the finished change",
)
def test_quality_gate_passes_on_the_finished_change() -> None:
    """Run the scenario end to end."""


@given("the finished change in the working tree")
def working_tree_exists() -> None:
    assert (REPO_ROOT / "src" / "hello" / "characters.py").is_file()


@when(
    "`uv run ruff format --check .`, `uv run ruff check .`, "
    "`uv run mypy --strict src tests` and `uv run pytest` are run",
    target_fixture="exit_codes",
)
def run_quality_gate() -> list[tuple[list[str], int, str]]:
    results = []
    for command in GATE_COMMANDS:
        completed = subprocess.run(  # nosec B603 B607
            command, cwd=REPO_ROOT, capture_output=True, text=True, check=False
        )
        results.append((command, completed.returncode, completed.stdout[-2000:]))
    return results


@then("all four commands exit with status 0")
def all_exit_zero(exit_codes: list[tuple[list[str], int, str]]) -> None:
    failures = [(cmd, out) for cmd, code, out in exit_codes if code != 0]
    assert not failures, failures
