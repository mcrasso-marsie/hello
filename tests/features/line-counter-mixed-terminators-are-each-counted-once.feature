Feature: Line count in word-count output

Scenario: mixed terminators are each counted once
  Given  the text 'a\nb\rc\r\nd\x0be\x0cf\x1cg\x1dh\x1ei\x85j\u2028k\u2029'
  When  count_lines is called on it
  Then  it returns 11
