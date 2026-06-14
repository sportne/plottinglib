from __future__ import annotations

import numpy as np
import pytest
from migration_examples.matlab_parity.python import exponential_smooth


def test_exponential_smooth_matches_hand_calculated_values() -> None:
    values = np.array([0.0, 2.0, 4.0, 3.0, 5.0, 8.0])

    result = exponential_smooth(values, alpha=0.35, initial=1.0)

    np.testing.assert_allclose(
        result, np.array([1.0, 1.35, 2.2775, 2.530375, 3.39474375, 5.0065834375])
    )


def test_exponential_smooth_defaults_initial_to_first_sample() -> None:
    result = exponential_smooth([10.0, 20.0, 30.0], alpha=0.5)

    np.testing.assert_allclose(result, np.array([10.0, 15.0, 22.5]))


@pytest.mark.parametrize("alpha", [-0.1, 1.1])
def test_exponential_smooth_rejects_alpha_outside_unit_interval(alpha: float) -> None:
    with pytest.raises(ValueError, match="alpha"):
        exponential_smooth([1.0, 2.0], alpha=alpha)


def test_exponential_smooth_rejects_bad_shapes_and_empty_inputs() -> None:
    with pytest.raises(ValueError, match="one-dimensional"):
        exponential_smooth([[1.0, 2.0]], alpha=0.5)

    with pytest.raises(ValueError, match="at least one"):
        exponential_smooth([], alpha=0.5)
