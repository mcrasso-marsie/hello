Feature: Line count in word-count output

Scenario: non-boundary characters do not end a line
  Given  the text 'a' + c + 'b', for each c in TAB '\t', SPACE ' ', US '\x1f', NBSP '\xa0', ZERO WIDTH SPACE '\u200b' and IDEOGRAPHIC SPACE '\u3000'
  When  count_lines is called on that text
  Then  it returns 0 for every one of the six cases
