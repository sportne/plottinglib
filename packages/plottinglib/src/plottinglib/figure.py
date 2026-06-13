"""Figure creation helpers.

These wrappers remove repetitive setup while returning ordinary Matplotlib
objects so users can keep using the Matplotlib API directly.
"""

from __future__ import annotations

from typing import Any

from plottinglib.style import apply_style

FigureSize = tuple[float, float]


def figure(
    title: str | None = None,
    *,
    size: FigureSize | None = None,
    apply_default_style: bool = False,
    **kwargs: Any,
) -> tuple[Any, Any]:
    """Create a single-axis Matplotlib figure.

    Parameters
    ----------
    title:
        Optional window and axes title.
    size:
        Optional figure size in inches.
    apply_default_style:
        If true, apply :func:`plottinglib.apply_style` before creating the
        figure. The default is false to avoid surprising global rcParam changes.
    kwargs:
        Additional keyword arguments passed to ``matplotlib.pyplot.subplots``.
    """
    import matplotlib.pyplot as plt

    if apply_default_style:
        apply_style()

    fig, ax = plt.subplots(figsize=size, **kwargs)
    if title:
        _set_window_title(fig, title)
        ax.set_title(title)
    return fig, ax


def subplots(
    rows: int = 1,
    cols: int = 1,
    *,
    title: str | None = None,
    size: FigureSize | None = None,
    sharex: bool | str = False,
    sharey: bool | str = False,
    squeeze: bool = True,
    apply_default_style: bool = False,
    **kwargs: Any,
) -> tuple[Any, Any]:
    """Create a multi-axis Matplotlib figure using project defaults."""
    import matplotlib.pyplot as plt

    if rows < 1 or cols < 1:
        msg = "rows and cols must both be at least 1"
        raise ValueError(msg)

    if apply_default_style:
        apply_style()

    fig, axes = plt.subplots(
        rows,
        cols,
        figsize=size,
        sharex=sharex,
        sharey=sharey,
        squeeze=squeeze,
        **kwargs,
    )
    if title:
        _set_window_title(fig, title)
        fig.suptitle(title)
    return fig, axes


def _set_window_title(fig: Any, title: str) -> None:
    """Set a GUI window title when the active backend exposes a manager."""
    manager = getattr(getattr(fig, "canvas", None), "manager", None)
    if manager is not None and hasattr(manager, "set_window_title"):
        manager.set_window_title(title)
