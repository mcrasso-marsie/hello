Feature: Non-whitespace character count alongside word count

Scenario: count_non_whitespace_chars counts non-whitespace characters
  Given  the string "Hello, world!\n"
  When  count_non_whitespace_chars is called with that string
  Then  it returns 12
