"""Step definitions for the 'line counter performs no I/O' scenario.

Re-runs the assertions that
``tests/arch/test_layering.py::test_line_counter_performs_no_io`` performs,
against the real source of src/hello/lines.py.
"""

import ast
import sys
from pathlib import Path

from pytest_bdd import given, scenario, then, when

REPO_ROOT = Path(__file__).resolve().parents[2]
LINES_SOURCE = REPO_ROOT / "src" / "hello" / "lines.py"
FORBIDDEN_NAMES = frozenset({"open", "print", "input", "os", "pathlib", "subprocess"})
FORBIDDEN_SYS_STREAMS = frozenset({"stdin", "stdout", "stderr"})


@scenario(
    "../features/line-counter-performs-no-io.feature",
    "line counter performs no I/O",
)
def test_line_counter_performs_no_io_scenario() -> None:
    """Run the scenario end to end."""


@given("the source of src/hello/lines.py", target_fixture="tree")
def read_lines_source() -> ast.AST:
    return ast.parse(LINES_SOURCE.read_text(encoding="utf-8"))


@when(
    "the test tests/arch/test_layering.py::test_line_counter_performs_no_io runs",
    target_fixture="check_result",
)
def run_the_layering_check(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    imported = _top_level_imports(tree)
    referenced = _referenced_names(tree)
    sys_attrs = _sys_stream_attributes(tree)

    assert imported <= set(sys.stdlib_module_names), f"non-stdlib imports: {imported}"
    assert not referenced & FORBIDDEN_NAMES, f"forbidden references: {referenced}"
    assert not sys_attrs & FORBIDDEN_SYS_STREAMS, "forbidden sys stream reference"

    return imported, referenced, sys_attrs


def _imported_module_names(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    if isinstance(node, ast.ImportFrom):
        return [node.module or ""]
    return []


def _top_level_imports(tree: ast.AST) -> set[str]:
    return {
        name.split(".")[0]
        for node in ast.walk(tree)
        for name in _imported_module_names(node)
    }


def _referenced_names(tree: ast.AST) -> set[str]:
    return {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}


def _sys_stream_attributes(tree: ast.AST) -> set[str]:
    return {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "sys"
    }


@then("it passes")
def check_passes() -> None:
    """The When step raises on any violation, so reaching here means it passed."""


@then(
    "the test asserts that hello.lines imports only standard-library modules and "
    "references none of open, print, input, sys.stdin, sys.stdout, sys.stderr, os, "
    "pathlib or subprocess"
)
def check_assertions_made(
    check_result: tuple[set[str], set[str], set[str]],
) -> None:
    imported, referenced, sys_attrs = check_result
    assert not referenced & FORBIDDEN_NAMES
    assert not sys_attrs & FORBIDDEN_SYS_STREAMS
    assert imported <= set(sys.stdlib_module_names)
