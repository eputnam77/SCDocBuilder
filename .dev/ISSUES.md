# Known Issues

- **Unit tests** fail during collection because `python-docx` is not installed, causing `ModuleNotFoundError`.
- **Coverage** checks could not run because `pytest-cov` / `coverage` are missing.
- **Property tests** fail for the same missing dependency.
- **E2E tests** skipped due to missing Playwright.
