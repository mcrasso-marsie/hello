"""Step definitions for the 'all three counts come from the same decoded text' scenario
(SPEC-0003).
"""

from dataclasses import dataclass, field
from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from hello import cli


@dataclass
class Recorder:
    """Records every text argument it was called with, then returns a fixed count."""

    calls: list[str] = field(default_factory=list)

    def __call__(self, text: str) -> int:
        self.calls.append(text)
        return 0


@dataclass
class Recorders:
    words: Recorder
    characters: Recorder
    lines: Recorder


@scenario(
    "../features/spec0003-command-same-decoded-text.feature",
    "all three counts come from the same decoded text",
)
def test_all_three_counts_come_from_the_same_decoded_text() -> None:
    """Run the scenario end to end."""


@given(
    "hello.counter.count_words, hello.characters.count_characters and "
    "hello.lines.count_lines are patched with recording wrappers",
    target_fixture="recorders",
)
def patch_counters_with_recording_wrappers(
    monkeypatch: pytest.MonkeyPatch,
) -> Recorders:
    recorders = Recorders(words=Recorder(), characters=Recorder(), lines=Recorder())
    monkeypatch.setattr(cli, "count_words", recorders.words)
    monkeypatch.setattr(cli, "count_characters", recorders.characters)
    monkeypatch.setattr(cli, "count_lines", recorders.lines)
    return recorders


@given("a file containing 'x y\\n'", target_fixture="path")
def write_file(tmp_path: Path) -> Path:
    path = tmp_path / "notes.txt"
    path.write_text("x y\n", encoding="utf-8")
    return path


@when("hello.cli.main([PATH]) is called", target_fixture="result")
def call_main(path: Path) -> int:
    return cli.main([str(path)])


@then("each wrapper was called exactly once")
def check_each_wrapper_called_once(recorders: Recorders) -> None:
    assert len(recorders.words.calls) == 1
    assert len(recorders.characters.calls) == 1
    assert len(recorders.lines.calls) == 1


@then("all three wrappers received the identical str object 'x y\\n'")
def check_all_wrappers_received_the_identical_object(recorders: Recorders) -> None:
    text = recorders.words.calls[0]
    assert text == "x y\n"
    assert recorders.characters.calls[0] is text
    assert recorders.lines.calls[0] is text


@then("main returns 0")
def check_main_returns_zero(result: int) -> None:
    assert result == 0
