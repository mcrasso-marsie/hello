Feature: Line count in word-count output

Scenario: lone CR followed by CRLF is two boundaries
  Given  the text '\r\r\n'
  When  count_lines is called on it
  Then  it returns 2
