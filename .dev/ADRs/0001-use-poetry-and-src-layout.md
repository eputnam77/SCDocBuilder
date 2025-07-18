# 1. Adopt Poetry and `src` Layout

Date: 2025-07-18

## Status
Accepted

## Context
The repository initially contained a single `main.py` file at the project root and lacked dependency management or a defined folder structure. The multi‑agent workflow described in `.dev/AGENTS.md` requires reproducible environments, CI automation and packaging for distribution.

## Decision
We standardise on the `src` layout and manage dependencies with [Poetry](https://python-poetry.org/). Code lives under `src/faa_sc_replacer` and tests under `tests`. Poetry provides a `pyproject.toml` and lockfile for consistent installs. GitHub Actions will later run agents using `scripts/next-agent.sh`.

## Consequences
* Contributors install dependencies via `poetry install` and run pre‑commit hooks automatically.
* Packaging via `poetry build` produces wheels excluding `.dev` and `tests` content.
* Existing `main.py` was moved to `src/faa_sc_replacer` without functional changes.
