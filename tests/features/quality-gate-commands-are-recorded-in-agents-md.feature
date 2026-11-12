Feature: Word-count command

Scenario: Quality Gate commands are recorded in AGENTS.md
  Given  AGENTS.md at the repository root
  When  the test tests/test_agents_md.py::test_toolchain_lists_quality_gate_commands runs
  Then  it passes
