Feature: Standard input through an explicit '-' argument

Scenario: README documents the dash argument and its workaround
  Given  the README.md file at the repository root
  When  the README text is read
  Then  it contains `wordcount -`
  And  it contains the phrase `end of input`
  And  it contains `./-`
