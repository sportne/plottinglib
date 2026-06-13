"""Helpers for synchronizing axes within or across Matplotlib figures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

AxisName = Literal["x", "y"]
CallbackRecord = tuple[Any, str, int]


@dataclass
class AxisLink:
    """Manage synchronized Matplotlib axes limits.

    Keep the returned object alive for as long as synchronization should remain
    active. Call :meth:`disconnect` to remove all callbacks.
    """

    axes: tuple[Any, ...]
    x: bool = True
    y: bool = False
    _callbacks: list[CallbackRecord] = field(default_factory=list, init=False)
    _updating: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        if len(self.axes) < 2:
            msg = "at least two axes are required for linking"
            raise ValueError(msg)
        if not self.x and not self.y:
            msg = "at least one axis direction must be linked"
            raise ValueError(msg)

        for ax in self.axes:
            if self.x:
                callback_id = ax.callbacks.connect("xlim_changed", self._on_xlim_changed)
                self._callbacks.append((ax, "xlim_changed", callback_id))
            if self.y:
                callback_id = ax.callbacks.connect("ylim_changed", self._on_ylim_changed)
                self._callbacks.append((ax, "ylim_changed", callback_id))

    def disconnect(self) -> None:
        """Disconnect all callbacks associated with this link."""
        for ax, _event_name, callback_id in self._callbacks:
            ax.callbacks.disconnect(callback_id)
        self._callbacks.clear()

    def _on_xlim_changed(self, changed_ax: Any) -> None:
        self._sync(changed_ax, "x")

    def _on_ylim_changed(self, changed_ax: Any) -> None:
        self._sync(changed_ax, "y")

    def _sync(self, changed_ax: Any, axis: AxisName) -> None:
        if self._updating:
            return

        self._updating = True
        try:
            limits = changed_ax.get_xlim() if axis == "x" else changed_ax.get_ylim()
            for ax in self.axes:
                if ax is changed_ax:
                    continue
                if axis == "x":
                    ax.set_xlim(limits)
                else:
                    ax.set_ylim(limits)
            self._draw_idle_once_per_figure()
        finally:
            self._updating = False

    def _draw_idle_once_per_figure(self) -> None:
        seen: set[int] = set()
        for ax in self.axes:
            fig = ax.figure
            fig_id = id(fig)
            if fig_id in seen:
                continue
            seen.add(fig_id)
            fig.canvas.draw_idle()


def link_axes(*axes: Any, x: bool = True, y: bool = False) -> AxisLink:
    """Link x and/or y limits for two or more axes."""
    return AxisLink(tuple(axes), x=x, y=y)


def link_x_axes(*axes: Any) -> AxisLink:
    """Link x-limits for two or more axes."""
    return link_axes(*axes, x=True, y=False)


def link_y_axes(*axes: Any) -> AxisLink:
    """Link y-limits for two or more axes."""
    return link_axes(*axes, x=False, y=True)
