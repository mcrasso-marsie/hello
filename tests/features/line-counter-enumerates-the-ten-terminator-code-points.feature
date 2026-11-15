Feature: Line count in word-count output

Scenario: LINE_TERMINATORS enumerates exactly the ten terminator code points
  Given  the module hello.lines is importable
  When  LINE_TERMINATORS is read
  Then  it equals frozenset({'\n', '\x0b', '\x0c', '\r', '\x1c', '\x1d', '\x1e', '\x85', '\u2028', '\u2029'})
  And  its length is 10
