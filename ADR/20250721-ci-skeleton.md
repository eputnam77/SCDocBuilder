# CI Skeleton and Repository Layout

Date: 2025-07-21

## Status
Proposed

## Context
Upcoming tasks require continuous integration and a structured place for
manifests and database migrations. Tests must remain in the repository for
coverage enforcement.

## Decision
- Added `manifests/` and `migrations/` directories to prepare for deployment and
  schema evolution.
- Created `.github/workflows/ci.yml` with caching keyed on the `poetry.lock`
  hash. The workflow installs dependencies via Poetry and runs lint and tests.
- ADRs now live in an `ADR/` folder for easier discovery.
- `pyproject.toml` excludes the new directories from distribution so test files
  remain packaged only for development.

## Consequences
The project tree now matches `NEW_STRUCTURE.md`. CI will speed up using the
lockfile cache and ensures tests always run.
