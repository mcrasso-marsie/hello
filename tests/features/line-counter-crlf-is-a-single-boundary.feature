Feature: Line count in word-count output

Scenario: CRLF is a single boundary
  Given  the text 'a\r\n'
  When  count_lines is called on it
  Then  it returns 1
