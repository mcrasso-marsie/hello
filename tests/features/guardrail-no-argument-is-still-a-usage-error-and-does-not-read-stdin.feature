Feature: Standard input through an explicit '-' argument

Scenario: guardrail: no argument is still a usage error and does not read stdin
  Given  standard input is an open pipe holding the bytes b'a b\n' that is never closed
  When  `wordcount` runs with no argument and a 10 second timeout
  Then  the process finishes before the timeout
  And  stderr contains argparse usage text starting with `usage:`
  And  stdout is empty
  And  the exit status is 2
