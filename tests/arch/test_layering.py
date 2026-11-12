"""Architecture guardrail: hello.counter performs no I/O (ADR-0002)."""

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
COUNTER_SOURCE = REPO_ROOT / "src" / "hello" / "counter.py"
FORBIDDEN_MODULES = frozenset({"os", "sys", "io", "pathlib", "subprocess", "builtins"})


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
