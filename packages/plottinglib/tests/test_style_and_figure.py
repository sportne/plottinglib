from __future__ import annotations

import matplotlib.pyplot as plt
import pytest

import plottinglib as ap


def test_apply_and_reset_style() -> None:
    ap.reset_style()
    original_grid = plt.rcParams["axes.grid"]

    ap.apply_style({"axes.grid": not original_grid})
    assert plt.rcParams["axes.grid"] is (not original_grid)

    ap.publication_style({"savefig.dpi": 123})
    assert plt.rcParams["savefig.dpi"] == 123

    ap.reset_style()
    assert plt.rcParams["axes.grid"] == plt.rcParamsDefault["axes.grid"]


def test_figure_sets_axes_title() -> None:
    fig, ax = ap.figure("Demo", size=(4, 3))

    assert tuple(fig.get_size_inches()) == pytest.approx((4, 3))
    assert ax.get_title() == "Demo"

    plt.close(fig)


def test_subplots_validates_shape_and_sets_suptitle() -> None:
    fig, axes = ap.subplots(2, 1, title="Panels")

    assert len(axes) == 2
    assert fig._suptitle is not None
    assert fig._suptitle.get_text() == "Panels"

    plt.close(fig)

    with pytest.raises(ValueError, match="rows and cols"):
        ap.subplots(0, 1)
