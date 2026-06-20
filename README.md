# plottinglib Workspace

This repository is a polyglot-ready monorepo for plotting-related libraries,
applications, examples, and tools.

The repository currently contains:

- `packages/plottinglib`: a small Matplotlib conventions package for exploratory plotting.
- `migration_examples/matlab_parity`: a self-contained MATLAB-to-Python parity demo.

Python package management is handled with `uv` workspaces. The root project
exists for orchestration and shared checks; it is not intended to be built or
published.

## Quick Start

From the repository root:

```bash
uv sync --all-packages
uv run python scripts/check.py
```

That installs the workspace environment, runs root-level quality checks, runs
the migration example tests, and then runs the `plottinglib` package checks.

## Layout

```text
.
├── packages/
│   └── plottinglib/
│       ├── examples/
│       ├── scripts/
│       ├── src/plottinglib/
│       └── tests/
├── migration_examples/
│   └── matlab_parity/
├── scripts/
│   └── check.py
├── pyproject.toml
└── uv.lock
```

## Common Commands

Install all workspace dependencies from the repository root:

```bash
uv sync --all-packages
```

Run all repository checks:

```bash
uv run python scripts/check.py
```

Run root-level checks individually:

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check .
uv run pytest
```

Run checks for only `plottinglib`:

```bash
uv run --package plottinglib python packages/plottinglib/scripts/check.py
```

Build the `plottinglib` package distributions:

```bash
uv build --package plottinglib
```

Run only the MATLAB parity migration example tests:

```bash
uv run pytest migration_examples/matlab_parity/tests
```

Run the MATLAB parity test when MATLAB Engine for Python is installed:

```bash
uv run pytest migration_examples/matlab_parity/tests -m matlab --run-matlab
```

## Project Guides

See `packages/plottinglib/README.md` for package-specific usage examples,
coverage policy, and wheelhouse build instructions.

See `migration_examples/matlab_parity/README.md` for a small example of
MATLAB-to-Python migration parity testing that works even when MATLAB is not
installed locally.
