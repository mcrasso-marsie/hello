# hello

Local, dependency-free text utilities. The first utility is `wordcount`, which reports the number of words in one text file.

## Install

Requires Python 3.11 or newer. From the repository root, run:

```sh
uv sync
```

This creates the project environment and installs the `wordcount` command into it. Nothing is installed from a public package index, and the runtime has no third-party dependencies.

## Run

```sh
uv run wordcount PATH
```

`PATH` is exactly one path to a UTF-8 text file. On success, `wordcount` prints the word count followed by a newline and exits with status 0.

For example, for a file containing `one two three`:

```sh
uv run wordcount notes.txt
3
```

## Word rule

A word is a run of non-whitespace characters separated by whitespace. Tabs, newlines and repeated spaces only separate words. Punctuation attached to a word stays part of that word, so `Hello, world! It's-fine.` counts as 3 words.

## Errors and exit status

Every error prints exactly one line to standard error, starts with `wordcount: error:`, and prints nothing to standard output. No error prints a Python traceback.

- File errors have exit status 1:
  - `wordcount: error: file not found: PATH` when the path does not exist.
  - `wordcount: error: cannot read file: PATH` when the path exists but cannot be read, for example a directory or a file without read permission.
  - `wordcount: error: file is not valid UTF-8 text: PATH` when the file's bytes are not valid UTF-8.
- Usage errors have exit status 2. Running `wordcount` with no argument, or with more than one argument, prints the usage line from argparse to standard error.
