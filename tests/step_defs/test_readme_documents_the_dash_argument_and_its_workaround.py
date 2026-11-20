"""Step definitions for the 'README documents the dash argument and its workaround' scenario."""

from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenario, then, when

REPO_ROOT = Path(__file__).resolve().parents[2]


@scenario(
    "../features/readme-documents-the-dash-argument-and-its-workaround.feature",
    "README documents the dash argument and its workaround",
)
def test_readme_documents_the_dash_argument_and_its_workaround() -> None:
    """Run the scenario end to end."""


@pytest.fixture
def readme_path() -> Path:
    return REPO_ROOT / "README.md"


@given("the README.md file at the repository root")
def readme_exists(readme_path: Path) -> None:
    assert readme_path.is_file()


@when("the README text is read", target_fixture="readme_text")
def read_readme(readme_path: Path) -> str:
    return readme_path.read_text(encoding="utf-8")


@then(parsers.parse("it contains `{text}`"))
def contains_code(readme_text: str, text: str) -> None:
    assert text in readme_text


@then(parsers.parse("it contains the phrase `{text}`"))
def contains_phrase(readme_text: str, text: str) -> None:
    assert text in readme_text
