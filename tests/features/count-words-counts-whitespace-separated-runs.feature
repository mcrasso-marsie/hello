Feature: Word-count command

Scenario: count_words counts whitespace-separated runs
  Given  the hello.counter module is importable
  When  count_words is called with the string "one two three"
  Then  it returns the integer 3
