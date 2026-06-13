from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pytest

import plottinglib as ap


def test_link_x_axes_synchronizes_limits_and_disconnects() -> None:
    fig, (ax1, ax2) = plt.subplots(2, 1)
    link = ap.link_x_axes(ax1, ax2)

    ax1.set_xlim(2, 4)
    assert ax2.get_xlim() == pytest.approx((2, 4))

    link.disconnect()
    ax1.set_xlim(5, 6)
    assert ax2.get_xlim() == pytest.approx((2, 4))

    plt.close(fig)


def test_link_axes_validates_inputs() -> None:
    fig, ax = plt.subplots()

    with pytest.raises(ValueError, match="at least two"):
        ap.link_axes(ax)

    with pytest.raises(ValueError, match="at least one"):
        ap.link_axes(ax, ax, x=False, y=False)

    plt.close(fig)


def test_link_y_axes_synchronizes_limits() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    link = ap.link_y_axes(ax1, ax2)

    ax2.set_ylim(-3, 3)
    assert ax1.get_ylim() == pytest.approx((-3, 3))

    link.disconnect()
    plt.close(fig)


def test_export_figure_writes_single_and_multiple_formats(tmp_path: Path) -> None:
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])

    single = ap.export_figure(fig, tmp_path / "single.png")
    multiple = ap.export_figure(fig, tmp_path / "multi", formats=["png", "pdf"])

    assert single == [tmp_path / "single.png"]
    assert (tmp_path / "single.png").exists()
    assert multiple == [tmp_path / "multi.png", tmp_path / "multi.pdf"]
    assert all(path.exists() for path in multiple)

    with pytest.raises(ValueError, match="at least one"):
        ap.export_figure(fig, tmp_path / "empty", formats=[])

    plt.close(fig)
