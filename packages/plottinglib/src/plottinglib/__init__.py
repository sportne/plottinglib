"""Small Matplotlib helpers for user-focused exploratory plotting.

The package intentionally keeps Matplotlib as the primary user-facing API. It
adds a thin layer of conventions around styling, figure creation, data cursors,
axis linking, time-series plotting, and export.
"""

from plottinglib.cursors import CursorFormatter, default_cursor_formatter, enable_cursor
from plottinglib.export import export_figure
from plottinglib.figure import figure, subplots
from plottinglib.linking import AxisLink, link_axes, link_x_axes, link_y_axes
from plottinglib.style import apply_style, publication_style, reset_style
from plottinglib.timeseries import (
    DownsampledSeries,
    downsample_minmax,
    plot_timeseries,
    prepare_timeseries,
)

__all__ = [
    "AxisLink",
    "CursorFormatter",
    "DownsampledSeries",
    "apply_style",
    "default_cursor_formatter",
    "downsample_minmax",
    "enable_cursor",
    "export_figure",
    "figure",
    "link_axes",
    "link_x_axes",
    "link_y_axes",
    "plot_timeseries",
    "prepare_timeseries",
    "publication_style",
    "reset_style",
    "subplots",
]
