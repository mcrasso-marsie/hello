Feature: Standard input through an explicit '-' argument

Scenario: invalid UTF-8 on standard input fails with one line naming <stdin>
  Given  standard input holds the bytes b'\xff\xfe' and is closed
  When  `wordcount -` runs
  Then  stderr is exactly one line `wordcount: error: file is not valid UTF-8 text: <stdin>`
  And  stderr does not contain `Traceback`
  And  stdout is empty
  And  the exit status is 1
