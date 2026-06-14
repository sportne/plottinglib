from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-matlab",
        action="store_true",
        default=False,
        help="run MATLAB Engine parity tests",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "matlab: requires MATLAB Engine for Python")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--run-matlab"):
        return

    skip_matlab = pytest.mark.skip(reason="MATLAB parity tests require --run-matlab")
    for item in items:
        if "matlab" in item.keywords:
            item.add_marker(skip_matlab)
