"""Step definitions for the 'guardrail: the existing SPEC-0001 to SPEC-0003 test suite passes unchanged' scenario."""

# The subprocess argv are fixed literals (no untrusted input), and `git` and `uv` are
# resolved from PATH on purpose, as in the other step definitions.
import ast
import subprocess  # nosec B404
from pathlib import Path

from pytest_bdd import given, scenario, then, when

from tests import test_agents_md

REPO_ROOT = Path(__file__).resolve().parents[2]

# Running the suite from inside this scenario would recurse into it, and the Quality Gate
# scenario runs the whole suite too, so both are deselected from the nested run.
DESELECTED = (
    "tests/step_defs/test_guardrail_the_existing_spec_0001_to_spec_0003_test_suite_passes_unchanged.py",
    "tests/step_defs/test_quality_gate_passes_on_the_finished_change.py",
)

# The one allowed edit to a pre-existing test file: (path, top-level statement).
ALLOWED_CHANGES = {("tests/test_agents_md.py", "assign JUDGMENT_BOUNDARIES")}


def _git(*args: str) -> str:
    completed = subprocess.run(  # nosec B603 B607
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    )
    return completed.stdout


def _tracked_test_files() -> list[str]:
    """Python files under tests/ as committed in HEAD, i.e. before this change."""
    names = _git("ls-tree", "-r", "--name-only", "HEAD", "tests").split()
    return [name for name in names if name.endswith(".py")]


def _statements(source: str) -> list[tuple[str, str]]:
    """Top-level statements of a module as (kind, AST dump); kind names the function or assignment."""
    statements = []
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef):
            kind = f"def {node.name}"
        elif isinstance(node, ast.Assign):
            kind = f"assign {ast.unparse(node.targets[0])}"
        else:
            kind = "other"
        statements.append((kind, ast.dump(node)))
    return statements


def _current_statements(path: str) -> list[tuple[str, str]]:
    """Statements of ``path`` as it is in the working tree now, or none if it was deleted."""
    current = REPO_ROOT / path
    return _statements(current.read_text(encoding="utf-8")) if current.is_file() else []


def _changes(path: str) -> list[tuple[str, str]]:
    """(action, kind) for each HEAD statement of ``path`` removed or altered, and each one added."""
    old = _statements(_git("show", f"HEAD:{path}"))
    new = _current_statements(path)
    removed = [("removed", kind) for kind, dump in old if (kind, dump) not in new]
    added = [("added", kind) for kind, dump in new if (kind, dump) not in old]
    return removed + added


def _all_changes() -> list[tuple[str, str, str]]:
    """(path, action, kind) for every change to every test file tracked in HEAD."""
    return [
        (path, action, kind)
        for path in _tracked_test_files()
        for action, kind in _changes(path)
    ]


@scenario(
    "../features/guardrail-the-existing-spec-0001-to-spec-0003-test-suite-passes-unchanged.feature",
    "guardrail: the existing SPEC-0001 to SPEC-0003 test suite passes unchanged",
)
def test_guardrail_the_existing_spec_0001_to_spec_0003_test_suite_passes_unchanged() -> (
    None
):
    """Run the scenario end to end."""


@given("the test files tracked in tests/ before this change")
def tracked_test_files_exist() -> None:
    assert _tracked_test_files(), "no test files are tracked in HEAD"


@given(
    "the expected `JUDGMENT_BOUNDARIES` list in tests/test_agents_md.py lists the three Judgment Boundaries bullets in AGENTS.md"
)
def judgment_boundaries_listed() -> None:
    assert len(test_agents_md.JUDGMENT_BOUNDARIES) == 3


@when("`uv run pytest` runs on the finished change", target_fixture="suite_run")
def run_suite() -> subprocess.CompletedProcess[str]:
    deselect = [option for path in DESELECTED for option in ("--deselect", path)]
    return subprocess.run(  # nosec B603 B607
        ["uv", "run", "pytest", *deselect],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


@then("the exit status is 0")
def check_suite_exit_status(suite_run: subprocess.CompletedProcess[str]) -> None:
    assert suite_run.returncode == 0, suite_run.stdout[-2000:]


@then(
    "`git diff` against the pre-change commit shows no modified or removed test function in those files"
)
def check_no_test_function_changed() -> None:
    removed = [
        f"{path}: {kind}"
        for path, action, kind in _all_changes()
        if action == "removed" and kind.startswith("def test_")
    ]
    assert not removed, removed


@then(
    "the only change to a pre-existing test file is the `JUDGMENT_BOUNDARIES` list in tests/test_agents_md.py"
)
def check_only_allowed_change() -> None:
    unexpected = [
        f"{path}: {action} {kind}"
        for path, action, kind in _all_changes()
        if (path, kind) not in ALLOWED_CHANGES
    ]
    assert not unexpected, unexpected
