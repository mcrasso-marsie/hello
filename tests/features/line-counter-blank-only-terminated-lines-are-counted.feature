Feature: Line count in word-count output

Scenario: blank-only terminated lines are counted
  Given  the text '\n\n'
  When  count_lines is called on it
  Then  it returns 2
