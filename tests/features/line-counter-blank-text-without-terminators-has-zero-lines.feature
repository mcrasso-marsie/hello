Feature: Line count in word-count output

Scenario: blank text without terminators has zero lines
  Given  the text '  \t '
  When  count_lines is called on it
  Then  it returns 0
