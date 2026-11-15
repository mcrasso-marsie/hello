"""End-to-end check that the ``wordcount`` console script is installed and runs."""

# The subprocess argv is a fixed literal plus a file this test created (no untrusted
# input), and `uv` is resolved from PATH on purpose: the directive names it.
import subprocess  # nosec B404
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_console_script_is_installed_and_runs(tmp_path: Path) -> None:
    path = tmp_path / "notes.txt"
    path.write_text("one two three", encoding="utf-8")

    result = subprocess.run(  # nosec B603 B607
        ["uv", "run", "wordcount", str(path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == "words: 3 characters: 11 lines: 0\n"
