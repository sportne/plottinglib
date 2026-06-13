"""Time-series plotting helpers with optional large-data downsampling."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray

DEFAULT_MAX_POINTS = 100_000


@dataclass(frozen=True)
class DownsampledSeries:
    """A downsampled time series and the original indices retained."""

    x: NDArray[Any]
    y: NDArray[Any]
    original_indices: NDArray[np.int_]
    original_points: int

    @property
    def plotted_points(self) -> int:
        """Number of points retained for plotting."""
        return int(self.y.size)

    @property
    def was_downsampled(self) -> bool:
        """Whether the result contains fewer points than the original series."""
        return self.plotted_points < self.original_points


def prepare_timeseries(
    x: ArrayLike, y: ArrayLike | None = None
) -> tuple[NDArray[Any], NDArray[Any]]:
    """Normalize one- or two-argument time-series inputs to 1-D arrays.

    ``prepare_timeseries(y)`` creates an integer sample index for ``x``.
    ``prepare_timeseries(x, y)`` validates that both arrays are one-dimensional
    and have the same length.
    """
    if y is None:
        y_array = _as_1d_array(x, "y")
        x_array = np.arange(y_array.size)
        return x_array, y_array

    x_array = _as_1d_array(x, "x")
    y_array = _as_1d_array(y, "y")
    if x_array.size != y_array.size:
        msg = f"x and y must have the same length; got {x_array.size} and {y_array.size}"
        raise ValueError(msg)
    return x_array, y_array


def plot_timeseries(
    ax: Any,
    x: ArrayLike,
    y: ArrayLike | None = None,
    *,
    label: str | None = None,
    downsample: bool = False,
    max_points: int = DEFAULT_MAX_POINTS,
    **plot_kwargs: Any,
) -> Any:
    """Plot a time series on an existing Matplotlib axes.

    Parameters
    ----------
    ax:
        Matplotlib axes to plot into.
    x, y:
        Either ``plot_timeseries(ax, y)`` or ``plot_timeseries(ax, x, y)``.
    label:
        Optional Matplotlib line label.
    downsample:
        If false, plot all points. If true and the series is longer than
        ``max_points``, retain min/max points from uniform bins. The default is
        intentionally false so users always see raw data unless they opt in.
    max_points:
        Maximum approximate number of plotted points when ``downsample=True``.
    plot_kwargs:
        Additional keyword arguments passed to ``Axes.plot``.

    Returns
    -------
    Any
        The Matplotlib ``Line2D`` object created by ``Axes.plot``.
    """
    x_array, y_array = prepare_timeseries(x, y)
    original_points = int(y_array.size)
    original_indices = np.arange(original_points)
    plotted_x = x_array
    plotted_y = y_array
    plotted_indices = original_indices

    if downsample:
        downsampled = downsample_minmax(x_array, y_array, max_points=max_points)
        plotted_x = downsampled.x
        plotted_y = downsampled.y
        plotted_indices = downsampled.original_indices

    if label is not None:
        plot_kwargs = {**plot_kwargs, "label": label}

    (line,) = ax.plot(plotted_x, plotted_y, **plot_kwargs)
    _attach_timeseries_metadata(
        line,
        original_indices=plotted_indices,
        original_points=original_points,
        downsampled=plotted_indices.size != original_points,
    )
    return line


def downsample_minmax(
    x: ArrayLike,
    y: ArrayLike,
    *,
    max_points: int = DEFAULT_MAX_POINTS,
) -> DownsampledSeries:
    """Downsample a time series by retaining min/max y values per x-ordered bin.

    The returned points are always sorted by their original order. The first and
    last samples are preserved when downsampling occurs.
    """
    x_array, y_array = prepare_timeseries(x, y)
    n_points = int(y_array.size)

    if max_points < 4:
        msg = "max_points must be at least 4"
        raise ValueError(msg)

    if n_points <= max_points:
        indices = np.arange(n_points)
        return DownsampledSeries(
            x=x_array.copy(),
            y=y_array.copy(),
            original_indices=indices,
            original_points=n_points,
        )

    n_bins = max(1, (max_points - 2) // 2)
    bin_edges = np.linspace(0, n_points, n_bins + 1, dtype=np.int_)
    retained: list[int] = [0, n_points - 1]

    for start, stop in pairwise(bin_edges):
        if stop <= start:
            continue
        retained.extend(_minmax_indices_for_segment(y_array, int(start), int(stop)))

    indices = np.array(sorted(set(retained)), dtype=np.int_)
    if indices.size > max_points:
        indices = _trim_indices(indices, max_points=max_points, last_index=n_points - 1)

    return DownsampledSeries(
        x=x_array[indices],
        y=y_array[indices],
        original_indices=indices,
        original_points=n_points,
    )


def _as_1d_array(values: ArrayLike, name: str) -> NDArray[Any]:
    array = np.asarray(values)
    if array.ndim != 1:
        msg = f"{name} must be one-dimensional; got shape {array.shape}"
        raise ValueError(msg)
    return array


def _minmax_indices_for_segment(y: NDArray[Any], start: int, stop: int) -> list[int]:
    segment = y[start:stop]
    if segment.size == 0:
        return []

    if np.issubdtype(segment.dtype, np.number):
        finite_mask = np.isfinite(segment)
        if not bool(np.any(finite_mask)):
            return [start, stop - 1]
        finite_positions = np.flatnonzero(finite_mask)
        finite_values = segment[finite_mask]
        min_idx = start + int(finite_positions[int(np.argmin(finite_values))])
        max_idx = start + int(finite_positions[int(np.argmax(finite_values))])
        return [min_idx, max_idx]

    min_idx = start + int(np.argmin(segment))
    max_idx = start + int(np.argmax(segment))
    return [min_idx, max_idx]


def _trim_indices(
    indices: NDArray[np.int_], *, max_points: int, last_index: int
) -> NDArray[np.int_]:
    """Trim retained indices while preserving endpoints."""
    interior = indices[(indices != 0) & (indices != last_index)]
    keep_interior = max_points - 2
    if keep_interior <= 0:
        return np.array([0, last_index], dtype=np.int_)
    if interior.size > keep_interior:
        positions = np.linspace(0, interior.size - 1, keep_interior, dtype=np.int_)
        interior = interior[positions]
    return np.array([0, *interior.tolist(), last_index], dtype=np.int_)


def _attach_timeseries_metadata(
    line: Any,
    *,
    original_indices: NDArray[np.int_],
    original_points: int,
    downsampled: bool,
) -> None:
    # The attributes are intentionally private and best-effort. They allow this
    # package's cursor formatter to show original data indices while returning a
    # normal Matplotlib Line2D to users.
    line._plottinglib_original_indices = original_indices
    line._plottinglib_original_points = original_points
    line._plottinglib_downsampled = downsampled
