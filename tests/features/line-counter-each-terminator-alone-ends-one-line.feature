Feature: Line count in word-count output

Scenario: each terminator alone ends one line
  Given  the text 'a' followed by one terminator, for each of LF '\n', CR '\r', CRLF '\r\n', VT '\x0b', FF '\x0c', FS '\x1c', GS '\x1d', RS '\x1e', NEL '\x85', LS '\u2028' and PS '\u2029'
  When  count_lines is called on that text
  Then  it returns 1 for every one of the 11 cases
