Feature: Standard input through an explicit '-' argument

Scenario: piped text is counted through the dash argument
  Given  standard input holds the bytes b'a b\n'
  When  `wordcount -` runs
  Then  stdout is exactly `words: 2 characters: 2 lines: 1\n`
  And  stderr is empty
  And  the exit status is 0
