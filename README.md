# hello

Local, dependency-free text utilities. The first utility is `wordcount`, which reports the number of words, the number of visible characters and the number of terminated lines in one text file.

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

`PATH` is exactly one path to a UTF-8 text file. On success, `wordcount` prints exactly one line of the form `words: <N> characters: <M> lines: <L>` followed by a newline and exits with status 0.

For example, for a file containing `one two three`:

```sh
uv run wordcount notes.txt
words: 3 characters: 11 lines: 0
```

The file has no line terminator, so its line count is 0. For a file containing `hello world`, a newline, `bye` and a final newline:

```sh
uv run wordcount notes.txt
words: 3 characters: 13 lines: 2
```

The line count adds no new flag: the three counts are always reported together.

## Word rule

A word is a run of non-whitespace characters separated by whitespace. Tabs, newlines and repeated spaces only separate words. Punctuation attached to a word stays part of that word, so `Hello, world! It's-fine.` counts as 3 words.

## Character rule

A visible character is a non-whitespace character, using the same whitespace definition as the word rule. Combining marks never add to the count, so a base character followed by combining marks counts once: both the precomposed `é` (U+00E9) and `e` followed by U+0301 count as 1 character. Non-ASCII characters such as `ï` or `日` count as one character each, so `café` is 4 characters.

## Line rule

A line is a segment of text ended by a line terminator, and `<L>` is the number of terminators. A final segment with no terminator is not counted as a line. The line terminators are exactly these, listed explicitly:

| Name | Code point |
|------|------------|
| LF | U+000A |
| CR | U+000D |
| CRLF | U+000D U+000A, counted as one terminator |
| VT | U+000B |
| FF | U+000C |
| FS | U+001C |
| GS | U+001D |
| RS | U+001E |
| NEL | U+0085 |
| LS | U+2028 |
| PS | U+2029 |

CRLF counts as one terminator, not two. No other character ends a line; tabs, spaces and non-breaking spaces do not.

| Text | Lines |
|------|-------|
| `a\nb` | 1 |
| `\n\n` | 2 |
| `a\r\n` | 1 |
| empty file | 0 |

The line rule differs from `wc -l`, which counts only LF (U+000A). `wordcount` also counts CR, CRLF, VT, FF, FS, GS, RS, NEL, LS and PS, so a file that uses only CR line endings has lines here but 0 for `wc -l`.

## Output change

The earlier bare-integer output (just the word count, for example `3`) no longer applies. The earlier two-field output `words: <N> characters: <M>` also no longer applies. Every successful run now prints the labeled `words: <N> characters: <M> lines: <L>` line, so anything that parsed an earlier output must parse this line instead. There is no flag to restore either old output.

## Errors and exit status

Every error prints exactly one line to standard error, starts with `wordcount: error:`, and prints nothing to standard output. No error prints a Python traceback.

- File errors have exit status 1:
  - `wordcount: error: file not found: PATH` when the path does not exist.
  - `wordcount: error: cannot read file: PATH` when the path exists but cannot be read, for example a directory or a file without read permission.
  - `wordcount: error: file is not valid UTF-8 text: PATH` when the file's bytes are not valid UTF-8.
- Usage errors have exit status 2. Running `wordcount` with no argument, or with more than one argument, prints the usage line from argparse to standard error.
