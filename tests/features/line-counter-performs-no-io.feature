Feature: Line count in word-count output

Scenario: line counter performs no I/O
  Given  the source of src/hello/lines.py
  When  the test tests/arch/test_layering.py::test_line_counter_performs_no_io runs
  Then  it passes
  And  the test asserts that hello.lines imports only standard-library modules and references none of open, print, input, sys.stdin, sys.stdout, sys.stderr, os, pathlib or subprocess
