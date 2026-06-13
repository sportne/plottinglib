from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import numpy as np
import pytest

from plottinglib import cursors


class DummyArtist:
    def __init__(self, label: str = "signal") -> None:
        self._label = label
        self._plottinglib_original_indices = np.array([10, 20, 30])

    def get_label(self) -> str:
        return self._label


class DummyAnnotation:
    def __init__(self) -> None:
        self.text = ""

    def set_text(self, text: str) -> None:
        self.text = text


class DummyCursor:
    def __init__(self) -> None:
        self.callback: Any = None

    def connect(self, event_name: str) -> Any:
        assert event_name == "add"

        def decorator(callback: Any) -> Any:
            self.callback = callback
            return callback

        return decorator


def test_default_cursor_formatter_shows_xy_label_and_original_index() -> None:
    selection = SimpleNamespace(
        target=(1.23456789, 9.87654321),
        index=1,
        artist=DummyArtist("temperature"),
    )

    text = cursors.default_cursor_formatter(selection)

    assert "temperature" in text
    assert "x=1.23457" in text
    assert "y=9.87654" in text
    assert "index=20" in text


def test_default_cursor_formatter_handles_private_labels_and_bad_targets() -> None:
    selection = SimpleNamespace(
        target=object(), index="not an index", artist=DummyArtist("_hidden")
    )

    text = cursors.default_cursor_formatter(selection)

    assert text == "x=?\ny=?"


def test_enable_cursor_connects_add_callback(monkeypatch: pytest.MonkeyPatch) -> None:
    dummy_cursor = DummyCursor()
    calls: list[dict[str, Any]] = []

    def fake_cursor(pickables: Any, **kwargs: Any) -> DummyCursor:
        calls.append({"pickables": pickables, **kwargs})
        return dummy_cursor

    monkeypatch.setattr(cursors, "mplcursors", SimpleNamespace(cursor=fake_cursor), raising=False)
    monkeypatch.setitem(
        __import__("sys").modules, "mplcursors", SimpleNamespace(cursor=fake_cursor)
    )

    returned = cursors.enable_cursor("artist", hover=True, multiple=False, highlight=False)

    assert returned is dummy_cursor
    assert calls == [
        {
            "pickables": "artist",
            "hover": True,
            "multiple": False,
            "highlight": False,
        }
    ]

    annotation = DummyAnnotation()
    selection = SimpleNamespace(
        target=(1, 2), index=0, artist=DummyArtist("a"), annotation=annotation
    )
    dummy_cursor.callback(selection)
    assert annotation.text.startswith("a\nx=1\ny=2")
