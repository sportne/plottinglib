"""Helpers for optional MATLAB Engine parity tests."""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray


def import_matlab_engine() -> Any:
    """Import MATLAB Engine lazily so it is never a required dependency."""
    return importlib.import_module("matlab.engine")


def start_matlab(matlab_dir: Path) -> Any:
    """Start MATLAB Engine and add the reference implementation directory."""
    matlab_engine = import_matlab_engine()
    engine = matlab_engine.start_matlab()
    engine.addpath(str(matlab_dir), nargout=0)
    return engine


def numpy_to_matlab_column(values: ArrayLike) -> Any:
    """Convert a 1-D NumPy-compatible input to a MATLAB double column vector."""
    matlab = importlib.import_module("matlab")
    array = np.asarray(values, dtype=float)
    if array.ndim != 1:
        msg = "only one-dimensional arrays can be converted to MATLAB columns"
        raise ValueError(msg)
    return matlab.double([[float(value)] for value in array])


def matlab_to_numpy(values: Any) -> NDArray[Any]:
    """Convert a MATLAB Engine numeric result to a flattened NumPy array."""
    return np.asarray(values, dtype=float).reshape(-1)
