# Configuration Issues

## Dependency Pinning

The following dependencies in `pyproject.toml` are not pinned to exact versions:

- python-docx
- python-dateutil
- rich
- pytest
- hypothesis
- ruff
- black
- mypy
- bandit
- semgrep
- playwright
- pre-commit
- pytest-cov

All dependencies must be pinned without using version specifiers like `^`, `*`, or `latest`.

## Lock File Check

Attempted to run `poetry lock --check`, but this option is not available in Poetry 2.1.3. Also attempted `pip-compile --dry-run`, but `pip-compile` was not installed and could not be installed due to network restrictions.

ready-for:builder
