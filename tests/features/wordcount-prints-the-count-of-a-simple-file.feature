Feature: Word-count command

Scenario: wordcount prints the count of a simple file
  Given  a temporary file notes.txt containing "one two three\n" encoded as UTF-8
  When  main(["<path to notes.txt>"]) is called with stdout and stderr captured
  Then  the return value is 0
  And  stdout is exactly "3\n"
  And  stderr is empty
