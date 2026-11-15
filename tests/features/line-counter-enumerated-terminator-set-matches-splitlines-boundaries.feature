Feature: Line count in word-count output

Scenario: enumerated terminator set matches str.splitlines boundaries
  Given  every code point from U+0000 to U+10FFFF, excluding surrogates U+D800 to U+DFFF
  When  the test tests/test_lines.py::test_line_terminators_match_str_splitlines_boundaries runs
  Then  it passes
  And  the test asserts that LINE_TERMINATORS equals the set of code points c for which ('a' + c + 'b').splitlines() has length 2
