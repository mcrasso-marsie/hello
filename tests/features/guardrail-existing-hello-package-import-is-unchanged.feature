Feature: Word-count command

Scenario: guardrail: existing hello package import is unchanged
  Given  the names exported by src/hello/__init__.py before this change are recorded in the test
  When  the test tests/test_package.py::test_existing_package_surface_unchanged runs
  Then  it passes, confirming `import hello` succeeds and every recorded name is still present
