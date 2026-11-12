"""Command-line entry point: ``wordcount PATH`` prints the word count of a UTF-8 file."""

import argparse

from hello.counter import count_words


def main(argv: list[str] | None = None) -> int:
    """Parse ``PATH``, count the words in that file and print the count."""
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description="Print the number of words in a UTF-8 text file.",
    )
    parser.add_argument("path", metavar="PATH", help="path to a UTF-8 text file")
    args = parser.parse_args(argv)

    with open(args.path, encoding="utf-8") as file:
        text = file.read()
    print(count_words(text))
    return 0
