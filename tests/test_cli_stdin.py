"""Tests for reading standard input through the explicit '-' argument."""

import io
import sys
from pathlib import Path

import pytest

from hello.cli import main


def _feed_stdin(monkeypatch: pytest.MonkeyPatch, data: bytes) -> None:
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(data)))


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (b"a b\n", "words: 2 characters: 2 lines: 1\n"),
        (b"", "words: 0 characters: 0 lines: 0\n"),
        (b"a\r\nb\r\n", "words: 2 characters: 2 lines: 2\n"),
        (b"a\rb\r", "words: 2 characters: 2 lines: 2\n"),
        ("café naïve 日本\n".encode(), "words: 3 characters: 11 lines: 1\n"),
    ],
)
def test_dash_counts_stdin_bytes(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    data: bytes,
    expected: str,
) -> None:
    _feed_stdin(monkeypatch, data)

    assert main(["-"]) == 0

    captured = capsys.readouterr()
    assert captured.out == expected
    assert captured.err == ""


def test_dash_does_not_translate_newlines(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A lone CR followed by LF-CR stays three terminators; text-mode stdin would translate."""
    _feed_stdin(monkeypatch, b"a\r\n\rb\r")

    assert main(["-"]) == 0

    assert capsys.readouterr().out == "words: 2 characters: 2 lines: 3\n"


def test_dash_with_extra_argument_is_usage_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _feed_stdin(monkeypatch, b"a b\n")

    with pytest.raises(SystemExit) as excinfo:
        main(["-", "extra"])

    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("usage:")


def test_dash_invalid_utf8_names_stdin(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _feed_stdin(monkeypatch, b"\xff\xfe")

    assert main(["-"]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "wordcount: error: file is not valid UTF-8 text: <stdin>\n"


SAMPLES = [
    b"a b\n",
    b"a\r\nb\r\n",
    b"a\rb\r",
    "café naïve 日本\n".encode(),
]


@pytest.mark.parametrize("data", SAMPLES)
def test_file_and_stdin_give_byte_identical_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    data: bytes,
) -> None:
    path = tmp_path / "sample.txt"
    path.write_bytes(data)

    assert main([str(path)]) == 0
    from_file = capsys.readouterr().out.encode("utf-8")

    _feed_stdin(monkeypatch, data)
    assert main(["-"]) == 0
    from_stdin = capsys.readouterr().out.encode("utf-8")

    assert from_file == from_stdin


def test_lone_cr_sample_reports_two_lines_from_both_sources(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    path = tmp_path / "sample.txt"
    path.write_bytes(b"a\rb\r")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == "words: 2 characters: 2 lines: 2\n"

    _feed_stdin(monkeypatch, b"a\rb\r")
    assert main(["-"]) == 0
    assert capsys.readouterr().out == "words: 2 characters: 2 lines: 2\n"
