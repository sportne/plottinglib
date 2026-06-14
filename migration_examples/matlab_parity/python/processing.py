"""Small processing routine used to demonstrate MATLAB parity testing."""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray


def exponential_smooth(
    values: ArrayLike,
    alpha: float,
    *,
    initial: float | None = None,
) -> NDArray[Any]:
    """Return an exponential smoothing filter result for a one-dimensional signal.

    The recurrence intentionally mirrors the MATLAB reference:

    ``y[0] = values[0]`` when ``initial`` is omitted, otherwise ``initial``.
    ``y[i] = alpha * values[i] + (1 - alpha) * y[i - 1]`` for each sample.
    """
    samples = np.asarray(values, dtype=float)
    if samples.ndim != 1:
        msg = "values must be a one-dimensional array"
        raise ValueError(msg)
    if samples.size == 0:
        msg = "values must contain at least one sample"
        raise ValueError(msg)
    if not 0.0 <= alpha <= 1.0:
        msg = "alpha must be between 0 and 1"
        raise ValueError(msg)

    smoothed = np.empty_like(samples, dtype=float)
    smoothed[0] = float(samples[0] if initial is None else initial)
    for index in range(1, samples.size):
        smoothed[index] = alpha * samples[index] + (1.0 - alpha) * smoothed[index - 1]
    return smoothed
