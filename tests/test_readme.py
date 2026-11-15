"""README checks: install, run, the word, character and line rules and the error exit statuses are documented.

Traceability: SPEC-0003 (README Definition-of-Done items), ADR-0003 (Quality Gate).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PHRASES = (
    "uv sync",
    "uv run wordcount",
    "a word is a run of non-whitespace characters",
    "exit status 1",
    "exit status 2",
    "words: <n> characters: <m> lines: <l>",
    "a visible character is a non-whitespace character",
    "combining marks",
    "bare-integer output",
)

LINE_TERMINATORS = {
    "LF": "U+000A",
    "CR": "U+000D",
    "CRLF": "U+000D U+000A",
    "VT": "U+000B",
    "FF": "U+000C",
    "FS": "U+001C",
    "GS": "U+001D",
    "RS": "U+001E",
    "NEL": "U+0085",
    "LS": "U+2028",
    "PS": "U+2029",
}

LINE_RULE_PHRASES = (
    "crlf counts as one terminator",
    "a final segment with no terminator is not counted",
    "| `a\\nb` | 1 |",
    "| `\\n\\n` | 2 |",
    "| `a\\r\\n` | 1 |",
    "| empty file | 0 |",
    "`wc -l`",
    "counts only lf",
)

EXACT_TEXTS = (
    "earlier two-field output `words: <N> characters: <M>` also no longer applies",
    "words: 3 characters: 13 lines: 2",
    "words: 3 characters: 11 lines: 0",
)


def _readme() -> str:
    return (REPO_ROOT / "README.md").read_text(encoding="utf-8")


def test_readme_documents_install_run_and_word_rule() -> None:
    readme = _readme().lower()

    missing = [phrase for phrase in REQUIRED_PHRASES if phrase not in readme]

    assert not missing, f"README.md is missing: {missing}"


def _missing_terminators(readme: str) -> list[str]:
    return [
        f"| {name} | {code_point}"
        for name, code_point in LINE_TERMINATORS.items()
        if f"| {name} | {code_point}" not in readme
    ]


def _missing_exact(readme: str) -> list[str]:
    return [text for text in EXACT_TEXTS if text not in readme]


def test_readme_documents_three_field_line_and_explicit_line_rule() -> None:
    readme = _readme()
    lowered = readme.lower()

    missing = [phrase for phrase in LINE_RULE_PHRASES if phrase not in lowered]
    missing += _missing_terminators(readme)
    missing += _missing_exact(readme)

    assert not missing, f"README.md is missing: {missing}"
