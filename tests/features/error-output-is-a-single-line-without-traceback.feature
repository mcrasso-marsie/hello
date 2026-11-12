Feature: Word-count command

Scenario: error output is a single line without traceback
  Given  the missing-file, directory and undecodable-file cases
  When  the test tests/test_cli.py::test_errors_are_single_line_without_traceback runs
  Then  it passes
