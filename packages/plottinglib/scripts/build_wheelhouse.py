"""Build the package wheel and a platform-specific dependency wheelhouse.

This script intentionally uses uv for the project workflow and invokes pip only
for the one capability uv does not currently expose as ``uv pip download``:
collecting wheels into a directory without installing them.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
WHEELHOUSE = DIST / "wheelhouse"
REQUIREMENTS = WHEELHOUSE / "requirements-runtime.txt"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--include-dev",
        action="store_true",
        help="also include development dependencies in the wheelhouse",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="remove dist/wheelhouse before building",
    )
    args = parser.parse_args()

    if args.clean and WHEELHOUSE.exists():
        shutil.rmtree(WHEELHOUSE)
    WHEELHOUSE.mkdir(parents=True, exist_ok=True)

    _run(["uv", "lock"], cwd=ROOT)
    _run(
        ["uv", "build", "--package", "plottinglib", "--wheel", "--out-dir", str(DIST)],
        cwd=ROOT,
    )

    export_command = [
        "uv",
        "export",
        "--package",
        "plottinglib",
        "--format",
        "requirements.txt",
        "--no-hashes",
        "--no-emit-project",
        "--output-file",
        str(REQUIREMENTS),
    ]
    if not args.include_dev:
        export_command.insert(2, "--no-dev")
    _run(export_command, cwd=ROOT)

    _run(
        [
            "uv",
            "run",
            "--with",
            "pip",
            "python",
            "-m",
            "pip",
            "download",
            "--only-binary=:all:",
            "--dest",
            str(WHEELHOUSE),
            "-r",
            str(REQUIREMENTS),
        ],
        cwd=ROOT,
    )

    for wheel in DIST.glob("plottinglib-*.whl"):
        shutil.copy2(wheel, WHEELHOUSE / wheel.name)

    print(f"Wheelhouse written to {WHEELHOUSE}")
    return 0


def _run(command: list[str], *, cwd: Path) -> None:
    print(f"$ {' '.join(command)}")
    subprocess.run(command, cwd=cwd, check=True)


if __name__ == "__main__":
    raise SystemExit(main())
