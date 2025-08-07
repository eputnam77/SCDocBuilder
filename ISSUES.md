# Issues

## Step 0: Lock-integrity
- `pip-compile --dry-run` failed: command not found.

## Step 1: Type checks
- `mypy` failed: Can't find package 'scdocbuilder'.

## Step 2: Tests
- `pytest -q --cov --cov-report=html:reports/coverage --cov-report=term` error: unrecognized arguments `--cov`.
- `coverage html --skip-css` failed: command not found.

## Step 3: Coverage packaging
- `gh run upload-artifact --name coverage-html coverage-html.zip` failed: command not found.

## Dependency installation attempts
- `pip install pip-tools coverage` failed: no matching distributions (403).
- `pip install pytest-cov` failed: no matching distribution (403).
- `apt-get update` failed: repositories not signed (403).
- `apt-get install -y gh` failed: Unable to locate package.
