# Code Review

## Overview
The repository provides a Python package `faa_sc_replacer` with a CLI for filling FAA Special Condition templates. Core logic lives in `processing.py` and `io.py`. Unit tests cover the CLI, I/O helpers and processing functions.

The implementation generally satisfies the functional requirements in `.dev/PRD.md`:
- Required CLI arguments and options (`--template`, `--worksheet`, optional `--output`, `--dry-run`, `--log-level`)【F:src/faa_sc_replacer/cli.py†L26-L41】.
- Exit codes for common error categories and logging of failures【F:src/faa_sc_replacer/cli.py†L17-L83】.
- Placeholder extraction from paragraphs and tables and conditional blocks across headers, footers and textboxes【F:src/faa_sc_replacer/processing.py†L30-L147】.
- Input validation limiting file type and size【F:src/faa_sc_replacer/io.py†L13-L22】.

Tests run successfully (`pytest -q` → 10 passed, 2 skipped) but coverage measurement and property‑/e2e tests are skipped due to missing optional dependencies.

## Integration Risks
- The module `faa_sc_replacer.__init__` contains a large `PlaceholderReplacer` class implementing similar functionality to `processing.py`. Maintaining both could cause API confusion. Prefer consolidating logic in `processing.py` or exposing a consistent public API.
- `load_document` calls `validate_input_files(path, path)` which re‑validates the same path twice. While harmless, it is redundant and may be misleading.
- `--dry-run` diff currently shows `{placeholder: {"old": placeholder, "new": value}}`. This does not compare against the existing template text and may be confusing for users expecting an actual diff.

## Performance Notes
- Regex for conditional blocks is compiled each call to `apply_conditionals`. Compiling it once at module import would slightly reduce overhead.
- The placeholder replacement loops traverse all runs multiple times; performance is adequate for small documents but may degrade on large files. Profiling showed loops dominate runtime (see `.dev/PERFORMANCE_REPORT.md`). Consider caching regexes and avoiding repeated string scans.

## Maintainability
- Code is well formatted and passes Ruff, Black and MyPy. Tests are concise but could be expanded (e.g., batch mode, header/footer cases).
- The repository lacks a `poetry.lock` file, so environments may drift from declared dependencies. Generating and committing the lock file would improve reproducibility.
- CI workflow is present but disabled. Enabling it would enforce quality gates automatically.

## Mandatory Fixes
1. Remove or integrate the legacy `PlaceholderReplacer` class in `__init__.py` to avoid duplicate APIs and maintenance burden.
2. Commit a `poetry.lock` file and ensure optional dependencies (`pytest-cov`, `hypothesis`, `playwright`, etc.) are installable for the quality gates.
3. Enable the GitHub Actions workflow (`agents.yml`) or provide a manual script so tests and linters run consistently.

## Optional Improvements
- Precompile the conditional regex in `apply_conditionals`.
- Improve `--dry-run` output to show actual differences between the template and filled values.
- Expand tests to cover batch mode, header/footer traversal and schema loading from YAML.
- Consider caching placeholder schema files to avoid repeated disk reads during batch processing.

Overall the codebase is in good shape but requires the above mandatory fixes before shipping. Once addressed, the next agent should continue with feature implementation and CI integration.
