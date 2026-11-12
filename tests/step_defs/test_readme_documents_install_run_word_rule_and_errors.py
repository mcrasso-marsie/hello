"""Step definitions for the 'README documents install, run, word rule and errors' scenario."""

from pathlib import Path

from pytest_bdd import given, scenario, then, when

from tests.test_readme import test_readme_documents_install_run_and_word_rule

REPO_ROOT = Path(__file__).resolve().parents[2]


@scenario(
    "../features/readme-documents-install-run-word-rule-and-errors.feature",
    "README documents install, run, word rule and errors",
)
def test_readme_documents_install_run_word_rule_and_errors() -> None:
    """Run the scenario end to end."""


@given("README.md at the repository root")
def readme_exists() -> None:
    assert (REPO_ROOT / "README.md").is_file()


@when(
    "the test tests/test_readme.py::test_readme_documents_install_run_and_word_rule runs"
)
def run_readme_check() -> None:
    test_readme_documents_install_run_and_word_rule()


@then(
    'it passes, confirming README.md contains "uv sync", "uv run wordcount", '
    "the sentence defining a word as a run of non-whitespace characters, "
    "and the exit statuses 1 and 2"
)
def check_passes() -> None:
    """The When step asserts the README content, so reaching here means it passed."""
