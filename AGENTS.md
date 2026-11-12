---
artifact_type: agent constitution
status: Draft
version: 2
---

# AGENTS.md

> **Project:** hello

---

## Toolchain

| Action | Command | Authority |
|--------|---------|-----------|
| format | `uv run ruff format --check .` | Quality Gate (ADR-0003) |
| lint | `uv run ruff check .` | Quality Gate (ADR-0003) |
| type-check | `uv run mypy --strict src tests` | Quality Gate (ADR-0003) |
| test | `uv run pytest` | Quality Gate (ADR-0003) |

---

## Judgment Boundaries

- Every external dependency requires a documented rationale in SPECs or ADRs.
- Never bypass the Quality Gate.

## ADR Conventions

- All four Quality Gate commands are run and pass before any change lands (ADR-0003)
