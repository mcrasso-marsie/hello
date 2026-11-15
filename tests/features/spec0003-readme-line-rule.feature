Feature: Line count in word-count output

Scenario: README documents the three-field line and the explicit line rule
  Given  the repository README.md
  When  its text is read
  Then  it contains 'words: <N> characters: <M> lines: <L>'
  And  it names each of LF, CR, CRLF, VT, FF, FS, GS, RS, NEL, LS and PS as line terminators
  And  it states that CRLF counts as one terminator and that an unterminated final line is not counted
  And  it mentions 'wc -l' and that it counts only LF
  And  it states that the two-field `words: <N> characters: <M>` output no longer applies
