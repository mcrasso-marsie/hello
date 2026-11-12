"""Command-line entry point: ``wordcount PATH`` prints the word count of a UTF-8 file."""

import argparse
import sys

from hello.counter import count_words


def _fail(message: str) -> int:
    """Print one error line to stderr and return the failure exit status."""
    print(f"wordcount: error: {message}", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    """Parse ``PATH``, count the words in that file and print the count."""
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description="Print the number of words in a UTF-8 text file.",
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

    print(count_words(text))
    return 0
