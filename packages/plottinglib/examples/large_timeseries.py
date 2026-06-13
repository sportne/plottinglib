"""Large time-series plotting with explicit opt-in downsampling."""

from __future__ import annotations

import numpy as np

import plottinglib as ap


def main() -> None:
    ap.apply_style()

    n = 1_000_000
    x = np.linspace(0, 100, n)
    y = np.sin(x) + 0.05 * np.random.default_rng(7).standard_normal(n)

    fig, ax = ap.figure("Large time series")
    line = ap.plot_timeseries(
        ax,
        x,
        y,
        label="1M samples, downsampled for display",
        downsample=True,
        max_points=50_000,
    )
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude")
    ax.legend()

    ap.enable_cursor(line)
    fig.show()


if __name__ == "__main__":
    main()
