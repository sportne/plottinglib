"""Generate golden MATLAB parity data for the exponential smoothing example."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from migration_examples.matlab_parity.python import exponential_smooth
from migration_examples.matlab_parity.tests.matlab_helpers import (
    matlab_to_numpy,
    numpy_to_matlab_column,
    start_matlab,
)

EXAMPLE_ROOT = Path(__file__).resolve().parents[1]
MATLAB_DIR = EXAMPLE_ROOT / "matlab"
GOLDEN_DIR = EXAMPLE_ROOT / "tests" / "data" / "golden"
GOLDEN_PATH = GOLDEN_DIR / "exponential_smooth_case_001.npz"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--prefer-matlab",
        action="store_true",
        help="use MATLAB Engine output when available, otherwise fall back to Python output",
    )
    args = parser.parse_args()

    values = np.array([0.0, 2.0, 4.0, 3.0, 5.0, 8.0])
    alpha = 0.35
    initial = 1.0

    expected, source = _expected_output(
        values, alpha=alpha, initial=initial, prefer_matlab=args.prefer_matlab
    )
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    np.savez(
        GOLDEN_PATH,
        values=values,
        alpha=np.array(alpha),
        initial=np.array(initial),
        expected=expected,
        source=np.array(source),
    )
    print(f"Wrote {GOLDEN_PATH} using {source} output")
    return 0


def _expected_output(
    values: NDArray[Any],
    *,
    alpha: float,
    initial: float,
    prefer_matlab: bool,
) -> tuple[NDArray[Any], str]:
    if prefer_matlab:
        try:
            engine = start_matlab(MATLAB_DIR)
        except ModuleNotFoundError:
            print("MATLAB Engine for Python is not installed; using Python output")
        else:
            try:
                matlab_result = engine.exponential_smooth(
                    numpy_to_matlab_column(values),
                    alpha,
                    initial,
                )
            finally:
                engine.quit()
            return matlab_to_numpy(matlab_result), "matlab"

    return exponential_smooth(values, alpha=alpha, initial=initial), "python"


if __name__ == "__main__":
    raise SystemExit(main())
