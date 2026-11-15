"""Command-line entry point: ``wordcount PATH`` prints a UTF-8 file's word, character and line counts."""

import argparse
import sys

from hello.characters import count_characters
from hello.counter import count_words
from hello.lines import count_lines


def _fail(message: str) -> int:
    """Print one error line to stderr and return the failure exit status."""
    print(f"wordcount: error: {message}", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    """Parse ``PATH``, count the words, characters and lines in that file and print them."""
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description="Print the number of words, characters and lines in a UTF-8 text file.",
    )
    parser.add_argument("path", metavar="PATH", help="path to a UTF-8 text file")
    args = parser.parse_args(argv)

    try:
        with open(args.path, encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        return _fail(f"file not found: {args.path}")
    except UnicodeDecodeError:
        return _fail(f"file is not valid UTF-8 text: {args.path}")
    except OSError:
        return _fail(f"cannot read file: {args.path}")

    words = count_words(text)
    characters = count_characters(text)
    lines = count_lines(text)
    print(f"words: {words} characters: {characters} lines: {lines}")
    return 0
