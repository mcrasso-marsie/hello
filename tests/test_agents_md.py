"""Checks that AGENTS.md records the Quality Gate and keeps its Judgment Boundaries (ADR-0003)."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

QUALITY_GATE_COMMANDS = {
    "format": "uv run ruff format --check .",
    "lint": "uv run ruff check .",
    "type-check": "uv run mypy --strict src tests",
    "test": "uv run pytest",
}

JUDGMENT_BOUNDARIES = [
    "- Every external dependency requires a documented rationale in SPECs or ADRs.",
    "- Never bypass the Quality Gate.",
    "- Accept changes only through a Synthesis workflow; never land a change made outside one.",
]


def _read_agents_md() -> str:
    return (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    """Return the body of a level-2 section, up to the next level-2 heading."""
    body = text.split(f"## {heading}", 1)[1]
    return body.split("\n## ", 1)[0]


def _toolchain_commands(text: str) -> dict[str, str]:
    rows = [
        line.strip().strip("|").split("|")
        for line in _section(text, "Toolchain").splitlines()
        if line.startswith("|")
    ]
    # The first row is the header and the second is the separator.
    return {cells[0].strip(): cells[1].strip().strip("`") for cells in rows[2:]}


def test_toolchain_lists_quality_gate_commands() -> None:
    commands = _toolchain_commands(_read_agents_md())

    for action, command in QUALITY_GATE_COMMANDS.items():
        assert commands.get(action) == command, action


def test_judgment_boundaries_preserved() -> None:
    bullets = [
        line
        for line in _section(_read_agents_md(), "Judgment Boundaries").splitlines()
        if line.startswith("- ")
    ]

    assert bullets == JUDGMENT_BOUNDARIES
