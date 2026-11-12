"""Project configuration consistency checks."""

import re
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_requires_python_matches_python_version_file() -> None:
    pyproject = tomllib.loads(
        (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    requires_python = pyproject["project"]["requires-python"]
    lower_bound = re.fullmatch(r">=(\d+\.\d+)(?:\.\d+)?", requires_python)
    assert lower_bound is not None, f"unexpected requires-python: {requires_python!r}"

    version = (REPO_ROOT / ".python-version").read_text(encoding="utf-8").strip()
    assert lower_bound.group(1) == ".".join(version.split(".")[:2])
