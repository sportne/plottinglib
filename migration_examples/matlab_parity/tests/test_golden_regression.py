from __future__ import annotations

from pathlib import Path

import numpy as np
from migration_examples.matlab_parity.python import exponential_smooth

GOLDEN_DIR = Path(__file__).resolve().parent / "data" / "golden"


def test_exponential_smooth_matches_golden_case_001() -> None:
    golden_path = GOLDEN_DIR / "exponential_smooth_case_001.npz"

    with np.load(golden_path) as golden:
        values = golden["values"]
        alpha = float(golden["alpha"])
        initial = float(golden["initial"])
        expected = golden["expected"]

    result = exponential_smooth(values, alpha=alpha, initial=initial)

    np.testing.assert_allclose(result, expected, rtol=1e-12, atol=1e-12)
