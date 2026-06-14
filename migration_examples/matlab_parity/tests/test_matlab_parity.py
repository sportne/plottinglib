from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from migration_examples.matlab_parity.python import exponential_smooth
from migration_examples.matlab_parity.tests.matlab_helpers import (
    matlab_to_numpy,
    numpy_to_matlab_column,
    start_matlab,
)

EXAMPLE_ROOT = Path(__file__).resolve().parents[1]
MATLAB_DIR = EXAMPLE_ROOT / "matlab"


@pytest.mark.matlab
def test_exponential_smooth_matches_matlab_engine_reference() -> None:
    values = np.array([0.0, 2.0, 4.0, 3.0, 5.0, 8.0])
    alpha = 0.35
    initial = 1.0

    try:
        engine = start_matlab(MATLAB_DIR)
    except ModuleNotFoundError:
        pytest.skip("MATLAB Engine for Python is not installed")

    try:
        matlab_result = engine.exponential_smooth(
            numpy_to_matlab_column(values),
            alpha,
            initial,
        )
    finally:
        engine.quit()

    python_result = exponential_smooth(values, alpha=alpha, initial=initial)

    np.testing.assert_allclose(
        python_result, matlab_to_numpy(matlab_result), rtol=1e-12, atol=1e-12
    )
