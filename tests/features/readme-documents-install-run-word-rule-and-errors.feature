Feature: Word-count command

Scenario: README documents install, run, word rule and errors
  Given  README.md at the repository root
  When  the test tests/test_readme.py::test_readme_documents_install_run_and_word_rule runs
  Then  it passes, confirming README.md contains "uv sync", "uv run wordcount", the sentence defining a word as a run of non-whitespace characters, and the exit statuses 1 and 2
