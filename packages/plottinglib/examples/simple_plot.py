"""Basic user plot with data tips."""

from __future__ import annotations

import numpy as np

import plottinglib as ap


def main() -> None:
    ap.apply_style()

    x = np.linspace(0, 20, 2_000)
    y = np.sin(x) + 0.1 * np.cos(8 * x)

    fig, ax = ap.figure("Simple plot")
    line = ap.plot_timeseries(ax, x, y, label="signal")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude")
    ax.legend()

    ap.enable_cursor(line)
    fig.show()


if __name__ == "__main__":
    main()
