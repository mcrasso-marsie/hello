"""Architecture guardrail: hello.counter, hello.characters and hello.lines perform no I/O
(ADR-0002, ADR-0005, ADR-0007).
"""

import ast
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
COUNTER_SOURCE = REPO_ROOT / "src" / "hello" / "counter.py"
CHARACTERS_SOURCE = REPO_ROOT / "src" / "hello" / "characters.py"
LINES_SOURCE = REPO_ROOT / "src" / "hello" / "lines.py"
FORBIDDEN_MODULES = frozenset({"os", "sys", "io", "pathlib", "subprocess", "builtins"})
ALLOWED_CHARACTERS_IMPORTS = frozenset({"unicodedata"})
FORBIDDEN_CALLS = frozenset({"open", "print", "input"})
FORBIDDEN_LINE_COUNTER_NAMES = frozenset(
    {"open", "print", "input", "os", "pathlib", "subprocess"}
)
FORBIDDEN_SYS_STREAMS = frozenset({"stdin", "stdout", "stderr"})


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


def _calls_open(tree: ast.AST) -> bool:
    return any(
        isinstance(node, ast.Name) and node.id == "open" for node in ast.walk(tree)
    )


def test_word_counter_has_no_io_imports() -> None:
    tree = ast.parse(COUNTER_SOURCE.read_text(encoding="utf-8"))
    imported = _top_level_imports(tree)

    assert not imported & FORBIDDEN_MODULES, f"forbidden imports: {imported}"
    assert not _calls_open(tree), "counter.py must not call open()"


def _called_names(tree: ast.AST) -> set[str]:
    return {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }


def test_characters_module_performs_no_io() -> None:
    tree = ast.parse(CHARACTERS_SOURCE.read_text(encoding="utf-8"))
    imported = _top_level_imports(tree)

    assert imported <= ALLOWED_CHARACTERS_IMPORTS, f"unexpected imports: {imported}"
    assert not _called_names(tree) & FORBIDDEN_CALLS, "characters.py must not do I/O"


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


def test_line_counter_performs_no_io() -> None:
    """hello.lines imports only the standard library and never references I/O (ADR-0007)."""
    tree = ast.parse(LINES_SOURCE.read_text(encoding="utf-8"))
    imported = _top_level_imports(tree)
    referenced = _referenced_names(tree)

    assert imported <= set(sys.stdlib_module_names), f"non-stdlib imports: {imported}"
    assert not referenced & FORBIDDEN_LINE_COUNTER_NAMES, (
        f"forbidden references: {referenced}"
    )
    assert not _sys_stream_attributes(tree) & FORBIDDEN_SYS_STREAMS, (
        "lines.py must not reference sys.stdin, sys.stdout or sys.stderr"
    )
