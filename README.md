# plottinglib workspace

This repository is a polyglot-ready monorepo for plotting-related libraries,
applications, and tools. The current workspace contains one Python package:

- `packages/plottinglib` - a small Matplotlib conventions package for exploratory plotting
- `migration_examples/matlab_parity` - a self-contained MATLAB-to-Python parity demo

Python package management is handled with `uv` workspaces. The root project is
only an orchestration layer and is not intended to be built or published.

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

## Development

Install all workspace dependencies from the repository root:

```bash
uv sync --all-packages
```

Run all workspace checks:

```bash
uv run python scripts/check.py
```

Run checks for only `plottinglib`:

```bash
uv run --package plottinglib python packages/plottinglib/scripts/check.py
```

Build the `plottinglib` package:

```bash
uv build --package plottinglib
```

See `packages/plottinglib/README.md` for package-specific usage examples,
coverage policy, and wheelhouse build instructions.

See `migration_examples/matlab_parity/README.md` for a small example of
MATLAB-to-Python migration parity testing that works even when MATLAB is not
installed locally.
