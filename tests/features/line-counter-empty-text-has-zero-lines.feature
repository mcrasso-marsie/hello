Feature: Line count in word-count output

Scenario: empty text has zero lines
  Given  the empty string ''
  When  count_lines is called on it
  Then  it returns 0
