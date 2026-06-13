"""mplcursors integration with consistent annotation formatting."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol

CursorFormatter = Callable[[Any], str]


class _SelectionLike(Protocol):
    """Small structural protocol for mplcursors selections used by formatters."""

    target: Any
    index: Any
    artist: Any


def enable_cursor(
    pickables: Any,
    *,
    hover: bool = False,
    multiple: bool = True,
    highlight: bool = True,
    formatter: CursorFormatter | None = None,
    **kwargs: Any,
) -> Any:
    """Enable Matplotlib data tips using ``mplcursors``.

    Parameters
    ----------
    pickables:
        A Matplotlib artist, axes, figure, or collection of artists supported by
        ``mplcursors.cursor``.
    hover:
        Whether annotations should appear on hover instead of click.
    multiple:
        Whether multiple annotations can remain visible simultaneously.
    highlight:
        Whether selected artists should be highlighted when supported.
    formatter:
        Optional callback that receives an ``mplcursors.Selection`` and returns
        annotation text.
    kwargs:
        Additional keyword arguments passed to ``mplcursors.cursor``.

    Returns
    -------
    Any
        The ``mplcursors.Cursor`` object. Keep a reference if you need to manage
        it later.
    """
    import mplcursors

    cursor = mplcursors.cursor(
        pickables,
        hover=hover,
        multiple=multiple,
        highlight=highlight,
        **kwargs,
    )
    annotation_formatter = formatter or default_cursor_formatter

    @cursor.connect("add")
    def _on_add(selection: Any) -> None:
        selection.annotation.set_text(annotation_formatter(selection))

    return cursor


def default_cursor_formatter(selection: _SelectionLike) -> str:
    """Return a compact default annotation for an mplcursors selection.

    The formatter knows about downsampled artists created by
    :func:`plottinglib.plot_timeseries` and will show the original data
    index when available.
    """
    x_value, y_value = _extract_xy(selection.target)
    lines = [f"x={_format_value(x_value)}", f"y={_format_value(y_value)}"]

    original_index = _mapped_original_index(selection)
    if original_index is not None:
        lines.append(f"index={original_index}")

    label = _artist_label(selection.artist)
    if label:
        lines.insert(0, label)

    return "\n".join(lines)


def _extract_xy(target: Any) -> tuple[Any, Any]:
    try:
        return target[0], target[1]
    except (IndexError, KeyError, TypeError):
        return "?", "?"


def _format_value(value: Any) -> str:
    try:
        return f"{float(value):.6g}"
    except (TypeError, ValueError):
        return str(value)


def _artist_label(artist: Any) -> str | None:
    get_label = getattr(artist, "get_label", None)
    if get_label is None:
        return None
    label = str(get_label())
    if not label or label.startswith("_"):
        return None
    return label


def _mapped_original_index(selection: _SelectionLike) -> int | None:
    indices = getattr(selection.artist, "_plottinglib_original_indices", None)
    if indices is None:
        return _integer_index(selection.index)

    plotted_index = _integer_index(selection.index)
    if plotted_index is None:
        return None

    try:
        return int(indices[plotted_index])
    except (IndexError, TypeError, ValueError):
        return plotted_index


def _integer_index(value: Any) -> int | None:
    try:
        return round(float(value))
    except (TypeError, ValueError):
        return None
