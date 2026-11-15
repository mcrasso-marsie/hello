Feature: Line count in word-count output

Scenario: all three counts come from the same decoded text
  Given  hello.counter.count_words, hello.characters.count_characters and hello.lines.count_lines are patched with recording wrappers
  And  a file containing 'x y\n'
  When  hello.cli.main([PATH]) is called
  Then  each wrapper was called exactly once
  And  all three wrappers received the identical str object 'x y\n'
  And  main returns 0
