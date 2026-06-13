from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pytest

import plottinglib as ap


def test_prepare_timeseries_accepts_y_only() -> None:
    x, y = ap.prepare_timeseries([10, 20, 30])

    np.testing.assert_array_equal(x, np.array([0, 1, 2]))
    np.testing.assert_array_equal(y, np.array([10, 20, 30]))


def test_prepare_timeseries_rejects_bad_shapes() -> None:
    with pytest.raises(ValueError, match="same length"):
        ap.prepare_timeseries([1, 2], [1])

    with pytest.raises(ValueError, match="one-dimensional"):
        ap.prepare_timeseries([[1, 2], [3, 4]])


def test_plot_timeseries_does_not_downsample_by_default() -> None:
    fig, ax = plt.subplots()
    x = np.arange(10)
    y = x**2

    line = ap.plot_timeseries(ax, x, y, max_points=4)

    np.testing.assert_array_equal(line.get_xdata(), x)
    np.testing.assert_array_equal(line.get_ydata(), y)
    assert line._plottinglib_downsampled is False
    assert line._plottinglib_original_points == 10

    plt.close(fig)


def test_plot_timeseries_downsamples_only_when_requested() -> None:
    fig, ax = plt.subplots()
    x = np.arange(101)
    y = np.sin(x / 3)

    line = ap.plot_timeseries(ax, x, y, downsample=True, max_points=20, label="signal")

    assert len(line.get_xdata()) <= 20
    assert line.get_label() == "signal"
    assert line._plottinglib_downsampled is True
    assert line._plottinglib_original_indices[0] == 0
    assert line._plottinglib_original_indices[-1] == 100

    plt.close(fig)


def test_downsample_minmax_preserves_extrema_and_endpoints() -> None:
    x = np.arange(12)
    y = np.array([0, 1, 9, 2, 3, -8, 4, 5, 11, 6, 7, 0])

    result = ap.downsample_minmax(x, y, max_points=8)

    assert result.was_downsampled is True
    assert result.plotted_points <= 8
    assert result.original_indices[0] == 0
    assert result.original_indices[-1] == 11
    assert 2 in result.original_indices
    assert 5 in result.original_indices
    assert 8 in result.original_indices


def test_downsample_minmax_handles_small_and_nan_inputs() -> None:
    x = np.arange(5)
    y = np.array([np.nan, np.nan, 2.0, -1.0, np.nan])

    unchanged = ap.downsample_minmax(x, y, max_points=5)
    assert unchanged.was_downsampled is False

    with pytest.raises(ValueError, match="at least 4"):
        ap.downsample_minmax(x, y, max_points=3)
