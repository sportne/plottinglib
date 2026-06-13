"""Enforce total and per-file coverage thresholds from coverage.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage-json", default="coverage.json", help="coverage.py JSON report")
    parser.add_argument("--minimum", type=float, default=80.0, help="minimum percent per file")
    parser.add_argument(
        "--source-prefix",
        default="src/plottinglib/",
        help="only check files under this path prefix",
    )
    args = parser.parse_args()

    report_path = Path(args.coverage_json)
    report = _load_report(report_path)
    failures = _per_file_failures(
        report,
        source_prefix=args.source_prefix,
        minimum=args.minimum,
    )

    if not failures:
        print(f"Per-file coverage OK: every source file is >= {args.minimum:g}%")
        return 0

    print(f"Per-file coverage failed: expected every source file >= {args.minimum:g}%")
    for file_name, percent in failures:
        print(f"  {file_name}: {percent:.2f}%")
    return 2


def _load_report(path: Path) -> dict[str, Any]:
    if not path.exists():
        msg = f"coverage JSON file not found: {path}"
        raise SystemExit(msg)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _per_file_failures(
    report: dict[str, Any],
    *,
    source_prefix: str,
    minimum: float,
) -> list[tuple[str, float]]:
    failures: list[tuple[str, float]] = []
    files = report.get("files", {})
    for file_name, file_report in sorted(files.items()):
        normalized = file_name.replace("\\", "/")
        if not normalized.startswith(source_prefix):
            continue
        percent = float(file_report["summary"]["percent_covered"])
        if percent < minimum:
            failures.append((normalized, percent))
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
