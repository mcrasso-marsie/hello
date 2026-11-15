Feature: Line count in word-count output

Scenario: LF followed by CR is two boundaries
  Given  the text '\n\r'
  When  count_lines is called on it
  Then  it returns 2
