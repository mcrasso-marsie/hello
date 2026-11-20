"""Command-line entry point: ``wordcount PATH|-`` prints a UTF-8 file's or stdin's word, character and line counts."""

import argparse
import sys

from hello.characters import count_characters
from hello.counter import count_words
from hello.lines import count_lines


def _fail(message: str) -> int:
    """Print one error line to stderr and return the failure exit status."""
    print(f"wordcount: error: {message}", file=sys.stderr)
    return 1


STDIN_MARKER = "-"
STDIN_NAME = "<stdin>"


def _read_bytes(path: str) -> bytes:
    """Return the raw bytes of the file at ``path``, or all of standard input for ``-``."""
    if path == STDIN_MARKER:
        return sys.stdin.buffer.read()
    with open(path, "rb") as file:
        return file.read()


def _decode(data: bytes) -> str:
    """Decode bytes as UTF-8 for every source, with no newline translation."""
    return data.decode("utf-8")


def main(argv: list[str] | None = None) -> int:
    """Parse ``PATH`` or ``-``, count the words, characters and lines in that input and print them."""
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description=(
            "Print the number of words, characters and lines in a UTF-8 text file, "
            "or in standard input when PATH is '-'."
        ),
    )
    parser.add_argument(
        "path",
        metavar="PATH",
        help="path to a UTF-8 text file, or '-' to read standard input until end of input",
    )
    args = parser.parse_args(argv)
    source = STDIN_NAME if args.path == STDIN_MARKER else args.path

    try:
        text = _decode(_read_bytes(args.path))
    except FileNotFoundError:
        return _fail(f"file not found: {source}")
    except UnicodeDecodeError:
        return _fail(f"file is not valid UTF-8 text: {source}")
    except OSError:
        return _fail(f"cannot read file: {source}")

    words = count_words(text)
    characters = count_characters(text)
    lines = count_lines(text)
    print(f"words: {words} characters: {characters} lines: {lines}")
    return 0
