"""Tests for the wordcount command-line entry point."""

import os
import re
from pathlib import Path
from typing import Any

import pytest

from hello import cli
from hello.cli import main


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("one two three\n", "words: 3 characters: 11 lines: 1\n"),
        ("  alpha\t\tbeta\n\ngamma  ", "words: 3 characters: 14 lines: 2\n"),
        ("Hello, world! It's-fine.", "words: 3 characters: 22 lines: 0\n"),
        ("café naïve 日本", "words: 3 characters: 11 lines: 0\n"),
        ("café", "words: 1 characters: 4 lines: 0\n"),
        ("e\u0301", "words: 1 characters: 1 lines: 0\n"),
        ("", "words: 0 characters: 0 lines: 0\n"),
        ("  \t\n\n ", "words: 0 characters: 0 lines: 2\n"),
    ],
)
def test_success_output_is_labeled_three_field_line(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    content: str,
    expected: str,
) -> None:
    path = tmp_path / "notes.txt"
    path.write_text(content, encoding="utf-8")

    assert main([str(path)]) == 0

    captured = capsys.readouterr()
    assert captured.out == expected
    assert captured.err == ""


def test_success_output_is_one_labeled_three_field_line(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """SPEC-0003: the success line always has exactly the three labeled fields (ADR-0008)."""
    path = tmp_path / "notes.txt"
    path.write_text("hello world\nbye\n", encoding="utf-8")

    assert main([str(path)]) == 0

    captured = capsys.readouterr()
    assert re.match(r"^words: \d+ characters: \d+ lines: \d+\n$", captured.out)
    assert captured.err == ""


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("hello world\nbye\n", "words: 3 characters: 13 lines: 2\n"),
        ("a\nb", "words: 2 characters: 2 lines: 1\n"),
        ("café", "words: 1 characters: 4 lines: 0\n"),
        ("\n\n", "words: 0 characters: 0 lines: 2\n"),
        ("", "words: 0 characters: 0 lines: 0\n"),
    ],
)
def test_success_output_matches_spec0003_examples(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    content: str,
    expected: str,
) -> None:
    path = tmp_path / "notes.txt"
    path.write_text(content, encoding="utf-8")

    assert main([str(path)]) == 0

    captured = capsys.readouterr()
    assert captured.out == expected
    assert captured.err == ""


def test_crlf_bytes_count_as_one_line(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A file whose raw bytes are b'a\\r\\n' reports lines: 1 (SPEC-0003)."""
    path = tmp_path / "notes.txt"
    path.write_bytes(b"a\r\n")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == "words: 1 characters: 1 lines: 1\n"


def test_lone_cr_bytes_count_as_two_lines(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A file whose raw bytes are b'a\\rb\\r' reports lines: 2 (SPEC-0003)."""
    path = tmp_path / "notes.txt"
    path.write_bytes(b"a\rb\r")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == "words: 2 characters: 2 lines: 2\n"


def test_unicode_ls_ps_ff_bytes_count_as_three_lines(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """UTF-8 LS, PS and FF boundaries each end a line, unaffected by newline translation."""
    path = tmp_path / "notes.txt"
    path.write_bytes("a\u2028b\u2029\x0c".encode())

    assert main([str(path)]) == 0
    assert capsys.readouterr().out.endswith("lines: 3\n")


def _make_recording_counter(calls: list[str], result: int) -> Any:
    """Return a fake counter that records the text it is called with and returns result."""

    def _recording_counter(text: str) -> int:
        calls.append(text)
        return result

    return _recording_counter


def test_counting_is_delegated_to_all_three_counters(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    word_calls: list[str] = []
    character_calls: list[str] = []
    line_calls: list[str] = []

    monkeypatch.setattr(cli, "count_words", _make_recording_counter(word_calls, 7))
    monkeypatch.setattr(
        cli, "count_characters", _make_recording_counter(character_calls, 42)
    )
    monkeypatch.setattr(cli, "count_lines", _make_recording_counter(line_calls, 5))
    path = tmp_path / "notes.txt"
    path.write_text("x", encoding="utf-8")

    assert main([str(path)]) == 0

    assert (word_calls, character_calls, line_calls) == (["x"], ["x"], ["x"])
    assert word_calls[0] is character_calls[0] is line_calls[0]
    assert capsys.readouterr().out == "words: 7 characters: 42 lines: 5\n"


def test_file_is_read_and_decoded_only_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """main() reads and decodes PATH exactly once, reusing the same str for all counters."""
    path = tmp_path / "notes.txt"
    path.write_text("a b\nc\n", encoding="utf-8")

    real_open = open
    open_calls: list[str] = []

    def counting_open(*args: Any, **kwargs: Any) -> Any:
        open_calls.append(str(args[0]))
        return real_open(*args, **kwargs)

    monkeypatch.setattr("builtins.open", counting_open)

    assert main([str(path)]) == 0
    assert open_calls == [str(path)]


def test_extra_lines_flag_is_rejected_as_usage_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """SPEC-0003 adds no new flag: an extra --lines argument is still a usage error."""
    path = tmp_path / "notes.txt"
    path.write_text("one two three\n", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(path), "--lines"])

    assert excinfo.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_missing_argument_is_usage_error(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main([])

    assert excinfo.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_too_many_arguments_is_usage_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    first = tmp_path / "a.txt"
    second = tmp_path / "b.txt"
    first.write_text("one\n", encoding="utf-8")
    second.write_text("two\n", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(first), str(second)])

    assert excinfo.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_missing_file_reports_one_line_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "missing.txt"

    assert main([str(path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == f"wordcount: error: file not found: {path}\n"


def test_directory_reports_cannot_read_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert len(captured.err.splitlines()) == 1
    assert captured.err.startswith("wordcount: error: cannot read file: ")


@pytest.mark.skipif(
    os.name != "posix" or os.geteuid() == 0,
    reason="needs a POSIX system and a non-root user to enforce file permissions",
)
def test_unreadable_file_reports_cannot_read_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "locked.txt"
    path.write_text("one two three\n", encoding="utf-8")
    path.chmod(0)

    assert main([str(path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert len(captured.err.splitlines()) == 1
    assert captured.err.startswith("wordcount: error: cannot read file: ")


def test_invalid_utf8_reports_one_line_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff\xfe\xfa")

    assert main([str(path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == (f"wordcount: error: file is not valid UTF-8 text: {path}\n")


def _assert_one_error_line(capsys: pytest.CaptureFixture[str]) -> None:
    captured = capsys.readouterr()
    assert captured.out == ""
    assert len(captured.err.splitlines()) == 1
    assert captured.err.startswith("wordcount: error: ")
    assert "Traceback" not in captured.err


def test_errors_are_single_line_without_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    undecodable = tmp_path / "binary.txt"
    undecodable.write_bytes(b"\xff\xfe\xfa")
    error_paths = [tmp_path / "missing.txt", tmp_path, undecodable]

    for path in error_paths:
        assert main([str(path)]) == 1
        _assert_one_error_line(capsys)
