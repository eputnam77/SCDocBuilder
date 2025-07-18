# Development Tasks

## Epic 1: Project Setup
- [ ] Restructure repository to match the layout in `.dev/AGENTS.md` (`src/`, `tests/`, `.dev`, etc.).
- [ ] Initialize Poetry and create `pyproject.toml`/`poetry.lock` with dependencies (`python-docx`, `gradio`, `python-dateutil`, testing packages).

## Epic 2: CLI Implementation
- [ ] Replace hard-coded file paths with an `argparse` CLI accepting `--template` and `--worksheet` (required) and `--output` (optional). (`tests/e2e/features/cli_argument_parsing.feature`)
- [ ] Add `--dry-run` flag that prints a JSON diff instead of writing a file. (`tests/e2e/features/cli_dry_run.feature`).
- [ ] When `--output` is omitted, save as `{template-stem}_{timestamp}.docx` and print the path on stdout. (`tests/e2e/features/output_auto_naming.feature`).
- [ ] Validate file existence, extension, and size (<10 MB) before processing; exit with descriptive codes. (`tests/e2e/features/input_validation.feature`, `tests/property/test_io_properties.py`).
- [ ] Refactor script into modular functions (`load_document`, `extract_fields`, `replace_placeholders`, `apply_conditionals`, `validate_input_files`, `save_document`). (`tests/property/test_processing_properties.py`)
- [ ] Add minimal logging with configurable level. (`tests/e2e/features/logging_levels.feature`)
- [ ] Optional batch mode to process all worksheets in a directory. (`tests/e2e/features/batch_mode.feature`)

## Epic 3: Placeholder Replacement Logic
- [ ] Traverse paragraphs, tables, headers, footers, numbered lists and textboxes for placeholders. (`tests/e2e/features/docx_traversal.feature`, `tests/property/test_processing_properties.py`)
- [ ] Implement Worksheet #6 conditional blocks (`[[OPTION_n]]...[[/OPTION_n]]`) keeping only the selected option. (`tests/e2e/features/conditional_blocks.feature`, `tests/property/test_processing_properties.py`)
- [ ] Handle multiline answers (questions 15–17) by reading the paragraph following the prompt. (`tests/e2e/features/multiline_answers.feature`, `tests/property/test_processing_properties.py`)
- [ ] Support configurable placeholder schema loaded from YAML or JSON. (`tests/e2e/features/configurable_schema.feature`, `tests/property/test_processing_properties.py`)

## Epic 4: Testing & CI
- [ ] Add unit tests for extraction, conditional logic, and header/footer replacement.
- [ ] Add tests verifying the package can be imported and used programmatically.
- [ ] Achieve ≥70 % coverage with pytest and integrate Ruff, Black, MyPy, Bandit, and Semgrep via pre-commit.
- [ ] Provide a GitHub Actions workflow implementing the multi-agent process.

## Epic 5: Documentation
- [ ] Expand `README.md` with installation steps, quick-start usage, and contribution guidelines. (`tests/e2e/features/readme_expansion.feature`)
