# Development Tasks

## Epic 1: Project Setup
- [ ] Restructure repository to match the layout in `.dev/AGENTS.md` (`src/`, `tests/`, `.dev`, etc.).
- [ ] Initialize Poetry and create `pyproject.toml`/`poetry.lock` with dependencies (`python-docx`, `gradio`, `python-dateutil`, testing packages).

## Epic 2: CLI Implementation
- [ ] Replace hard-coded file paths with an `argparse` CLI accepting `--template` and `--worksheet` (required) and `--output` (optional).
- [ ] Add `--dry-run` flag that prints a JSON diff instead of writing a file.
- [ ] When `--output` is omitted, save as `{template-stem}_{timestamp}.docx` and print the path on stdout.
- [ ] Validate file existence, extension, and size (<10 MB) before processing; exit with descriptive codes.

## Epic 3: Placeholder Replacement Logic
- [ ] Traverse headers, footers, numbered lists and textboxes for placeholders.
- [ ] Implement Worksheet #6 conditional blocks (`[[OPTION_n]]...[[/OPTION_n]]`) keeping only the selected option.
- [ ] Handle multiline answers (questions 15–17) by reading the paragraph following the prompt.

## Epic 4: Testing & CI
- [ ] Add unit tests for extraction, conditional logic, and header/footer replacement.
- [ ] Achieve ≥70 % coverage with pytest and integrate Ruff, Black, MyPy, Bandit, and Semgrep via pre-commit.
- [ ] Provide a GitHub Actions workflow implementing the multi-agent process.

## Epic 5: Documentation
- [ ] Expand `README.md` with installation steps, quick-start usage, and contribution guidelines.
