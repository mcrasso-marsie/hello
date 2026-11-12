Feature: Word-count command

Scenario: no third-party runtime dependencies
  Given  pyproject.toml at the repository root
  When  the test tests/arch/test_dependencies.py::test_no_runtime_dependencies runs
  Then  it passes
