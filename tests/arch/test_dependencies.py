"""Architecture guardrail: the runtime stays on the standard library (ADR-0001)."""

import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_no_runtime_dependencies() -> None:
    pyproject = tomllib.loads(
        (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    assert pyproject["project"].get("dependencies", []) == []
