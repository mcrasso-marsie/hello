"""Tests for the wordcount command-line entry point."""

import os
from pathlib import Path

import pytest

from hello import cli
from hello.cli import main


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("one two three\n", "words: 3 characters: 11\n"),
        ("  alpha\t\tbeta\n\ngamma  ", "words: 3 characters: 14\n"),
        ("Hello, world! It's-fine.", "words: 3 characters: 22\n"),
        ("café naïve 日本", "words: 3 characters: 11\n"),
        ("café", "words: 1 characters: 4\n"),
        ("e\u0301", "words: 1 characters: 1\n"),
        ("", "words: 0 characters: 0\n"),
        ("  \t\n\n ", "words: 0 characters: 0\n"),
    ],
)
def test_success_output_is_labeled_combined_line(
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


def test_counting_is_delegated_to_both_counters(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    word_calls: list[str] = []
    character_calls: list[str] = []

    def fake_count_words(text: str) -> int:
        word_calls.append(text)
        return 7

    def fake_count_characters(text: str) -> int:
        character_calls.append(text)
        return 42

    monkeypatch.setattr(cli, "count_words", fake_count_words)
    monkeypatch.setattr(cli, "count_characters", fake_count_characters)
    path = tmp_path / "notes.txt"
    path.write_text("x", encoding="utf-8")

    assert main([str(path)]) == 0

    assert word_calls == ["x"]
    assert character_calls == ["x"]
    assert capsys.readouterr().out == "words: 7 characters: 42\n"


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
