Feature: Character count in word-count output

Scenario: Quality Gate passes on the finished change
  Given  the finished change in the working tree
  When  `uv run ruff format --check .`, `uv run ruff check .`, `uv run mypy --strict src tests` and `uv run pytest` are run
  Then  all four commands exit with status 0
