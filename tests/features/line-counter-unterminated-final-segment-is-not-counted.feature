Feature: Line count in word-count output

Scenario: unterminated final segment is not counted
  Given  the texts 'a' and 'a\nb'
  When  count_lines is called on each
  Then  count_lines('a') returns 0
  And  count_lines('a\nb') returns 1
