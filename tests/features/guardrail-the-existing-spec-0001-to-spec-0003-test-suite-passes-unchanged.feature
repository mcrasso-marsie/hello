Feature: Standard input through an explicit '-' argument

Scenario: guardrail: the existing SPEC-0001 to SPEC-0003 test suite passes unchanged
  Given  the test files tracked in tests/ before this change
  And  the expected `JUDGMENT_BOUNDARIES` list in tests/test_agents_md.py lists the three Judgment Boundaries bullets in AGENTS.md
  When  `uv run pytest` runs on the finished change
  Then  the exit status is 0
  And  `git diff` against the pre-change commit shows no modified or removed test function in those files
  And  the only change to a pre-existing test file is the `JUDGMENT_BOUNDARIES` list in tests/test_agents_md.py
