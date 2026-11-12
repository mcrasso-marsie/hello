"""Tests for the wordcount command-line entry point."""

from pathlib import Path

import pytest

from hello import cli
from hello.cli import main


@pytest.mark.parametrize(
    "content",
    [
        "one two three\n",
        "  alpha\t\tbeta\n\ngamma  ",
        "Hello, world! It's-fine.",
        "café naïve 日本",
    ],
)
def test_prints_word_count_of_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], content: str
) -> None:
    path = tmp_path / "notes.txt"
    path.write_text(content, encoding="utf-8")

    assert main([str(path)]) == 0

    captured = capsys.readouterr()
    assert captured.out == "3\n"
    assert captured.err == ""


def test_empty_file_reports_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "empty.txt"
    path.write_bytes(b"")

    assert main([str(path)]) == 0

    assert capsys.readouterr().out == "0\n"


def test_counting_is_delegated_to_count_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[str] = []

    def fake_count_words(text: str) -> int:
        calls.append(text)
        return 42

    monkeypatch.setattr(cli, "count_words", fake_count_words)
    path = tmp_path / "notes.txt"
    path.write_text("one two three\n", encoding="utf-8")

    assert main([str(path)]) == 0

    assert calls == ["one two three\n"]
    assert capsys.readouterr().out == "42\n"


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
