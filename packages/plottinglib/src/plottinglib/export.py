"""Figure export helpers."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

DEFAULT_FORMATS = ("png", "pdf")


def export_figure(
    fig: Any,
    path: str | Path,
    *,
    formats: Iterable[str] | None = None,
    dpi: int = 300,
    tight: bool = True,
    transparent: bool = False,
    **savefig_kwargs: Any,
) -> list[Path]:
    """Export a Matplotlib figure with consistent defaults.

    Parameters
    ----------
    fig:
        Matplotlib figure to save.
    path:
        Output path. If it has a suffix, a single file is written unless
        ``formats`` is supplied. If it has no suffix, each requested format is
        written using that stem.
    formats:
        Optional iterable of formats such as ``["png", "pdf", "svg"]``.
        When omitted and ``path`` has no suffix, ``png`` and ``pdf`` are written.
    dpi:
        Raster output DPI.
    tight:
        Whether to use ``bbox_inches="tight"``.
    transparent:
        Forwarded to ``Figure.savefig``.
    savefig_kwargs:
        Additional keyword arguments passed to ``Figure.savefig``.

    Returns
    -------
    list[pathlib.Path]
        The files written.
    """
    base_path = Path(path)
    output_paths = _resolve_output_paths(base_path, formats)
    bbox_inches = "tight" if tight else None

    for output_path in output_paths:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(
            output_path,
            dpi=dpi,
            bbox_inches=bbox_inches,
            transparent=transparent,
            **savefig_kwargs,
        )
    return output_paths


def _resolve_output_paths(path: Path, formats: Iterable[str] | None) -> list[Path]:
    if formats is None and path.suffix:
        return [path]

    selected_formats = DEFAULT_FORMATS if formats is None else tuple(formats)
    if not selected_formats:
        msg = "at least one export format is required"
        raise ValueError(msg)

    stem = path.with_suffix("")
    return [stem.with_suffix(f".{fmt.lstrip('.')}") for fmt in selected_formats]
