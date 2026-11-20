Feature: Standard input through an explicit '-' argument

Scenario: file and standard input give identical output for the same bytes
  Given  the byte samples b'a b\n', b'a\r\nb\r\n', b'a\rb\r' and 'café naïve 日本\n' encoded as UTF-8
  And  each sample is written unchanged to its own temporary file
  When  for each sample, `wordcount PATH` runs on its file and `wordcount -` runs with the sample on standard input
  Then  for every sample, the two stdout lines are byte-for-byte identical
  And  for every sample, both runs exit with status 0
  And  the sample b'a\rb\r' reports `lines: 2` from both sources
