"""Shared Matplotlib style presets for users.

The functions here only update Matplotlib ``rcParams`` when explicitly called.
The package does not select or force a GUI backend.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

DEFAULT_STYLE: dict[str, Any] = {
    "figure.figsize": (10.0, 6.0),
    "figure.dpi": 100,
    "axes.grid": True,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.labelsize": 11,
    "axes.titlesize": 13,
    "legend.frameon": False,
    "lines.linewidth": 1.4,
    "lines.markersize": 4.0,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
}

PUBLICATION_STYLE: dict[str, Any] = {
    **DEFAULT_STYLE,
    "figure.dpi": 150,
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "legend.fontsize": 9,
    "lines.linewidth": 1.2,
    "savefig.dpi": 600,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
}


def apply_style(overrides: Mapping[str, Any] | None = None) -> None:
    """Apply the default user plotting style.

    Parameters
    ----------
    overrides:
        Optional Matplotlib ``rcParams`` overrides layered on top of the default
        package style.
    """
    import matplotlib.pyplot as plt

    params = dict(DEFAULT_STYLE)
    if overrides:
        params.update(overrides)
    plt.rcParams.update(params)


def publication_style(overrides: Mapping[str, Any] | None = None) -> None:
    """Apply export-oriented defaults for publication-quality figures."""
    import matplotlib.pyplot as plt

    params = dict(PUBLICATION_STYLE)
    if overrides:
        params.update(overrides)
    plt.rcParams.update(params)


def reset_style() -> None:
    """Reset Matplotlib to its built-in defaults."""
    import matplotlib.pyplot as plt

    plt.rcdefaults()
