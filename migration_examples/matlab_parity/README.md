# MATLAB Parity Migration Example

This example demonstrates a MATLAB-to-Python processing migration workflow that
still works on machines where MATLAB is not installed.

The sample algorithm is an exponential smoothing filter. It is intentionally
small so the migration pattern is the focus.

## Migration Lifecycle

1. Define representative NumPy inputs.
2. Run the new Python implementation.
3. Optionally run the MATLAB reference through MATLAB Engine for Python.
4. Compare Python and MATLAB outputs.
5. Freeze trusted outputs into golden `.npz` files.
6. Keep long-term Python-only regression tests against those golden files.

The important idea is that MATLAB is useful for establishing trust, but it does
not have to be present forever. Once a MATLAB result is trusted, it can be
frozen as a golden `.npz` file and checked by ordinary Python-only tests.

## Layout

```text
migration_examples/matlab_parity/
├── matlab/
│   └── exponential_smooth.m
├── python/
│   └── processing.py
├── scripts/
│   └── generate_golden.py
└── tests/
    ├── data/golden/
    ├── matlab_helpers.py
    ├── test_golden_regression.py
    ├── test_matlab_parity.py
    └── test_python_processing.py
```

## What Each Test Does

- `test_python_processing.py` checks the Python implementation directly.
- `test_matlab_parity.py` compares Python output with the MATLAB reference when
  `--run-matlab` is passed.
- `test_golden_regression.py` compares Python output with the committed golden
  `.npz` file and does not require MATLAB.

## Commands

Run the normal repository test suite. MATLAB tests are skipped unless explicitly
requested.

```bash
uv run pytest
```

Run only this example's tests.

```bash
uv run pytest migration_examples/matlab_parity/tests
```

Run MATLAB Engine parity tests. If `matlab.engine` is unavailable, the MATLAB
test skips with a clear message.

```bash
uv run pytest migration_examples/matlab_parity/tests -m matlab --run-matlab
```

Regenerate the golden file without requiring MATLAB.

```bash
uv run python migration_examples/matlab_parity/scripts/generate_golden.py
```

When MATLAB Engine for Python is installed, refresh the golden output from the
MATLAB reference implementation:

```bash
uv run python migration_examples/matlab_parity/scripts/generate_golden.py --prefer-matlab
```

The golden file stores the representative input values, smoothing parameter,
initial condition, expected output, and the source used to generate that output.

## MATLAB is optional

`matlabengine` is not a project dependency. The MATLAB-specific test imports it
only after `--run-matlab` is passed, and the Python-only golden regression test
is what protects the migrated implementation in everyday development and CI.

If `--run-matlab` is passed but MATLAB Engine for Python is not installed, the
MATLAB parity test is skipped with a clear message instead of failing the normal
test suite.
