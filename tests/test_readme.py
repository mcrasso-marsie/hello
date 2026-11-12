"""README checks: install, run, the word rule and the error exit statuses are documented."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PHRASES = (
    "uv sync",
    "uv run wordcount",
    "a word is a run of non-whitespace characters",
    "exit status 1",
    "exit status 2",
)


def test_readme_documents_install_run_and_word_rule() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8").lower()

    missing = [phrase for phrase in REQUIRED_PHRASES if phrase not in readme]

    assert not missing, f"README.md is missing: {missing}"
