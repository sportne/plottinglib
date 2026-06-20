# plottinglib

`plottinglib` is a small Matplotlib conventions package for exploratory plotting.

It is **not** a replacement for Matplotlib and it does **not** select a
Matplotlib GUI backend. Users still work with ordinary Matplotlib `Figure`,
`Axes`, and `Line2D` objects. The package adds a thin, consistent layer for:

- shared plotting style defaults
- simple figure/subplot creation
- `mplcursors` data tips
- linked x/y axes
- time-series plotting helpers
- explicit opt-in downsampling for large traces
- consistent figure export

The initial design goal is to make Python plotting feel more consistent for
MATLAB-to-Python migration work without building a custom GUI framework.

## Requirements

- Python 3.11+
- uv

Runtime dependencies are intentionally minimal:

- `matplotlib`
- `mplcursors`
- `numpy`

Development tooling:

- `ruff` for formatting, import sorting, linting, and static analysis
- `ty` for type checking
- `pytest` and `pytest-cov` for testing and coverage
- `hatchling` as the package build backend

## Install for development

From the repository root:

```bash
uv sync --all-packages
```

This installs `plottinglib` as an editable workspace package.

Run package checks:

```bash
uv run --package plottinglib python packages/plottinglib/scripts/check.py
```

Or run checks individually from `packages/plottinglib`:

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run python -m pytest -s
uv run python scripts/check_coverage.py --minimum 80
```

Coverage policy:

- 80% total coverage via `pytest-cov`
- 80% per source file via `scripts/check_coverage.py`

## Build a package

Build source and wheel distributions:

```bash
uv build --package plottinglib
```

Build a wheel only:

```bash
uv build --package plottinglib --wheel
```

Build a platform-specific wheelhouse containing the package wheel and runtime dependency wheels:

```bash
uv run --package plottinglib python packages/plottinglib/scripts/build_wheelhouse.py --clean
```

Include development dependencies in the wheelhouse:

```bash
uv run --package plottinglib python packages/plottinglib/scripts/build_wheelhouse.py --clean --include-dev
```

From the repository root, the wheelhouse is written to:

```text
packages/plottinglib/dist/wheelhouse/
```

## Basic use

```python
import numpy as np
import plottinglib as ap

ap.apply_style()

x = np.linspace(0, 20, 2_000)
y = np.sin(x)

fig, ax = ap.figure("Signal")
line = ap.plot_timeseries(ax, x, y, label="sensor A")
ax.set_xlabel("Time [s]")
ax.set_ylabel("Amplitude")
ax.legend()

ap.enable_cursor(line)
fig.show()
```

## Linked axes

```python
import numpy as np
import plottinglib as ap

x = np.linspace(0, 30, 4_000)
fig, axes = ap.subplots(2, 1, title="Linked views")

ap.plot_timeseries(axes[0], x, np.sin(x), label="sin")
ap.plot_timeseries(axes[1], x, np.cos(x), label="cos")

link = ap.link_x_axes(axes[0], axes[1])
```

Keep the returned `link` object alive for as long as the axes should remain
linked. Call `link.disconnect()` to remove the callbacks.

## Large time series

Downsampling is **off by default**. This is intentional: users see raw data
unless they explicitly opt in.

```python
line = ap.plot_timeseries(
    ax,
    time,
    signal,
    downsample=True,
    max_points=50_000,
)
```

The current downsampling strategy retains min/max values from uniform bins and
preserves the first and last samples. It is intended as a conservative display
helper, not a signal-processing operation.

## Export

```python
ap.export_figure(fig, "results/signal.pdf")
ap.export_figure(fig, "results/signal", formats=["png", "pdf", "svg"])
```

## Examples

Run the example scripts from the repository root:

```bash
uv run --package plottinglib python packages/plottinglib/examples/simple_plot.py
uv run --package plottinglib python packages/plottinglib/examples/linked_axes.py
uv run --package plottinglib python packages/plottinglib/examples/large_timeseries.py
```

For interactive desktop windows, use a Matplotlib backend appropriate for your
environment. This package deliberately does not force `TkAgg`, `QtAgg`, or any
other backend.
