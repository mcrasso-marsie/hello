"""Step definitions for the 'Quality Gate commands are recorded in AGENTS.md' scenario."""

from pathlib import Path

from pytest_bdd import given, scenario, then, when

from tests.test_agents_md import QUALITY_GATE_COMMANDS, _toolchain_commands

REPO_ROOT = Path(__file__).resolve().parents[2]


@scenario(
    "../features/quality-gate-commands-are-recorded-in-agents-md.feature",
    "Quality Gate commands are recorded in AGENTS.md",
)
def test_quality_gate_commands_are_recorded_in_agents_md() -> None:
    """Run the scenario end to end."""


@given("AGENTS.md at the repository root")
def agents_md_exists() -> None:
    assert (REPO_ROOT / "AGENTS.md").is_file()


@when(
    "the test tests/test_agents_md.py::test_toolchain_lists_quality_gate_commands runs"
)
def check_quality_gate_commands() -> None:
    commands = _toolchain_commands(
        (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    )
    assert commands == QUALITY_GATE_COMMANDS


@then("it passes")
def check_passes() -> None:
    """The When step asserts the Toolchain rows, so reaching here means it passed."""
