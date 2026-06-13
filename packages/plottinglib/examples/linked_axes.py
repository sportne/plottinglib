"""Two views with linked x axes."""

from __future__ import annotations

import numpy as np

import plottinglib as ap


def main() -> None:
    ap.apply_style()

    x = np.linspace(0, 30, 4_000)
    y1 = np.sin(x)
    y2 = np.cos(0.5 * x)

    fig, axes = ap.subplots(2, 1, title="Linked x-axis example", sharex=False)
    line1 = ap.plot_timeseries(axes[0], x, y1, label="sin")
    line2 = ap.plot_timeseries(axes[1], x, y2, label="cos")

    axes[0].legend()
    axes[1].legend()
    axes[1].set_xlabel("Time [s]")

    ap.link_x_axes(axes[0], axes[1])
    ap.enable_cursor([line1, line2])
    fig.show()


if __name__ == "__main__":
    main()
