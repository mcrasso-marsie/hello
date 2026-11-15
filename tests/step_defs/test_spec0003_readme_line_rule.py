"""Step definitions for 'README documents the three-field line and the explicit line rule'.

Traceability: SPEC-0003, ADR-0003. Reads README.md only; it does not run the CLI.
"""

from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from tests.test_readme import LINE_TERMINATORS

REPO_ROOT = Path(__file__).resolve().parents[2]


@scenario(
    "../features/spec0003-readme-line-rule.feature",
    "README documents the three-field line and the explicit line rule",
)
def test_readme_documents_the_three_field_line_and_the_explicit_line_rule() -> None:
    """Run the scenario end to end."""


@given("the repository README.md")
def readme_exists() -> None:
    assert (REPO_ROOT / "README.md").is_file()


@when("its text is read", target_fixture="readme")
def read_readme() -> str:
    return (REPO_ROOT / "README.md").read_text(encoding="utf-8")


@then("it contains 'words: <N> characters: <M> lines: <L>'")
def check_three_field_line(readme: str) -> None:
    assert "words: <N> characters: <M> lines: <L>" in readme


@then(
    "it names each of LF, CR, CRLF, VT, FF, FS, GS, RS, NEL, LS and PS "
    "as line terminators"
)
def check_terminators_named(readme: str) -> None:
    missing = [
        name
        for name, code_point in LINE_TERMINATORS.items()
        if f"| {name} | {code_point}" not in readme
    ]
    assert not missing, f"README.md does not list: {missing}"


@then(
    "it states that CRLF counts as one terminator and that an unterminated "
    "final line is not counted"
)
def check_crlf_and_unterminated(readme: str) -> None:
    lowered = readme.lower()
    assert "crlf counts as one terminator" in lowered
    assert "a final segment with no terminator is not counted" in lowered


@then("it mentions 'wc -l' and that it counts only LF")
def check_wc_l(readme: str) -> None:
    assert "`wc -l`" in readme
    assert "counts only LF" in readme


@then(
    "it states that the two-field `words: <N> characters: <M>` output no longer applies"
)
def check_two_field_retired(readme: str) -> None:
    assert "two-field output `words: <N> characters: <M>` also no longer applies" in (
        readme
    )


@pytest.mark.parametrize("example", ["a\\nb", "\\n\\n", "a\\r\\n"])
def test_readme_documents_line_examples(example: str) -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert f"`{example}`" in readme
