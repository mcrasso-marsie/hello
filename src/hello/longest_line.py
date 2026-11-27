"""The longest-line rule: the highest word count found on any single line.

Text is split into lines at ``hello.lines.LINE_TERMINATORS``, with the CRLF pair
counting as one terminator, and each line's words are counted with the word rule
from ``hello.counter``. Unlike the line counter, an unterminated final segment
counts as a line for this measure. A trailing terminator adds no extra line, and
text with no words on any line gives 0.

This module performs no file, process or console I/O.
"""

from hello.counter import count_words
from hello.lines import LINE_TERMINATORS


def longest_line_words(text: str) -> int:
    """Return the highest word count among the lines of ``text``.

    CRLF pairs are first coalesced into a single LF so they split once. Every
    code point in ``LINE_TERMINATORS`` then ends a line; the segment after the
    last terminator is a line too, and is simply empty when text ends with one.
    """
    longest = 0
    line_start = 0
    coalesced = text.replace("\r\n", "\n")
    for index, char in enumerate(coalesced):
        if char in LINE_TERMINATORS:
            longest = max(longest, count_words(coalesced[line_start:index]))
            line_start = index + 1
    return max(longest, count_words(coalesced[line_start:]))
