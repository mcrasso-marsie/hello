"""The line rule: a line is a segment of text ended by a line terminator.

The terminator set is enumerated explicitly rather than inherited silently from
``str.splitlines()``, so the rule does not depend on interpreter behaviour
(ADR-0007). It is exactly the ten single-code-point boundaries LF (U+000A), VT
(U+000B), FF (U+000C), CR (U+000D), FS (U+001C), GS (U+001D), RS (U+001E), NEL
(U+0085), LS (U+2028) and PS (U+2029), plus the two-code-point CRLF pair, which
counts as one terminator rather than two. A final segment with no terminator is
never counted as a line.

This module performs no file, process or console I/O (ADR-0007).
"""

LINE_TERMINATORS: frozenset[str] = frozenset(
    {
        "\n",  # LF U+000A
        "\x0b",  # VT U+000B
        "\x0c",  # FF U+000C
        "\r",  # CR U+000D
        "\x1c",  # FS U+001C
        "\x1d",  # GS U+001D
        "\x1e",  # RS U+001E
        "\x85",  # NEL U+0085
        "\u2028",  # LS U+2028
        "\u2029",  # PS U+2029
    }
)


def count_lines(text: str) -> int:
    """Return the number of terminated lines in ``text``.

    Each code point in ``LINE_TERMINATORS`` ends one line. A CR immediately
    followed by LF (the CRLF pair) is coalesced into exactly one terminator
    instead of two: replacing every CRLF pair with a single LF first removes
    the second half of each pair before the remaining characters are counted,
    so an unterminated final segment is still never counted.
    """
    coalesced = text.replace("\r\n", "\n")
    return sum(1 for char in coalesced if char in LINE_TERMINATORS)
