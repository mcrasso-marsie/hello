"""Step definitions for the 'no third-party runtime dependencies' scenario."""

import tomllib
from pathlib import Path

from pytest_bdd import given, scenario, then, when

REPO_ROOT = Path(__file__).resolve().parents[2]


@scenario(
    "../features/no-third-party-runtime-dependencies.feature",
    "no third-party runtime dependencies",
)
def test_no_third_party_runtime_dependencies() -> None:
    """Run the scenario end to end."""


@given("pyproject.toml at the repository root")
def pyproject_exists() -> None:
    assert (REPO_ROOT / "pyproject.toml").is_file()


@when("the test tests/arch/test_dependencies.py::test_no_runtime_dependencies runs")
def run_no_runtime_dependencies_check() -> None:
    pyproject = tomllib.loads(
        (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    assert pyproject["project"].get("dependencies", []) == []


@then("it passes")
def check_passes() -> None:
    """The When step raises on any violation, so reaching here means it passed."""
