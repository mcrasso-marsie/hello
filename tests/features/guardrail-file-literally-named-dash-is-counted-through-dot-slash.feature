Feature: Standard input through an explicit '-' argument

Scenario: guardrail: a file literally named dash is still counted through ./-
  Given  the working directory holds a file named `-` containing 'x y\n'
  And  standard input holds zero bytes and is closed
  When  `wordcount ./-` runs in that directory
  Then  stdout is exactly `words: 2 characters: 2 lines: 1\n`
  And  the exit status is 0
