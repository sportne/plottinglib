"""Run quality gates for all workspace projects."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COMMANDS = [
    ["uv", "run", "ruff", "format", "--check", "."],
    ["uv", "run", "ruff", "check", "."],
    ["uv", "run", "ty", "check", "."],
    ["uv", "run", "pytest"],
    ["uv", "run", "--package", "plottinglib", "python", "packages/plottinglib/scripts/check.py"],
]


def main() -> int:
    for command in COMMANDS:
        print(f"$ {' '.join(command)}")
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode != 0:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
