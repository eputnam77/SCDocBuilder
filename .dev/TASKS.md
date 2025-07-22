# Development Tasks

last_generated: 2025-07-21T14:29:12Z

| id | title | status | priority | estimate | acceptance_criteria | labels |
|----|-------|--------|----------|----------|--------------------|--------|
| T-001 | Restructure repository using `src/` layout and Poetry | DONE | | | `src/faa_sc_replacer/__init__.py` exists | area/setup type/chore |
| T-002 | Initialize Poetry with dependencies and lock file | DONE | | | `pyproject.toml` and `poetry.lock` present | area/setup type/chore |
| T-003 | Remove Gradio and Streamlit references | DONE | | | No mentions in repo | area/docs type/chore |
| T-004 | Implement argparse CLI for `--template` and `--worksheet` | DONE | | | `cli.py` argument parser | area/cli type/feat |
| T-005 | Add `--dry-run` flag printing JSON diff | DONE | | | `cli.py` diff output | area/cli type/feat |
| T-006 | Auto-name output when `--output` omitted and print path | DONE | | | `cli.py` generates timestamped name and prints path | area/cli type/feat |
| T-007 | Validate input files and exit with codes | DONE | | | `io.py` validation and `cli.py` error handling | area/io type/feat |
| T-008 | Refactor into modular functions | DONE | | | `__init__.py` exposes helpers | area/core type/chore |
| T-009 | Logging with configurable level and rotation | DONE | | | `cli.py` configures `RotatingFileHandler` | area/logging type/feat |
| T-010 | Batch mode to process directory of worksheets | DONE | | | `cli.py` `--batch` option | area/cli type/feat |
| T-011 | Traverse DOCX parts for placeholder replacement | DONE | | | `processing.py` iterates body, tables, headers, footers | area/core type/feat |
| T-012 | Worksheet #6 conditional blocks support | DONE | | | `processing.py` `apply_conditionals` | area/core type/feat |
| T-013 | Handle multiline answers for Q15–17 | DONE | | | `processing.py` next paragraph logic | area/core type/feat |
| T-014 | Configurable placeholder schema via JSON/YAML | DONE | Should | 4h | CLI accepts `--schema` path loading mappings | area/cli type/feat |
| T-015 | Unit tests for extraction and conditional logic | DONE | | | `tests/test_processing.py` | area/tests type/feat |
| T-016 | Test package import | DONE | | | `tests/test_import.py` | area/tests type/feat |
| T-017 | Coverage ≥70% with linting pre-commit hooks | DONE | Must | 3h | `pytest --cov` ≥70% and hooks run on commit | area/ci type/chore |
| T-018 | Enable GitHub Actions multi-agent workflow | DONE | Must | 2h | `.github/workflows/agents.yml` active | area/ci type/feat |
| T-019 | Expand README with usage and contribution guidelines | DONE | Should | 2h | README shows install, quick start, contribution section | area/docs type/feat |
| T-020 | Create FastAPI `/generate` endpoint for uploads | OPEN | Must | 5h | POST `/generate` returns generated DOCX path | area/api type/feat |
| T-021 | Provide `/health` endpoint returning status JSON | OPEN | Must | 1h | GET `/health` → `{"status": "ok"}` | area/api type/feat |
| T-022 | API tests using `TestClient` | OPEN | Must | 3h | Pytest suite covers both endpoints | area/tests type/feat |
| T-023 | Simple web UI for upload, preview and download | OPEN | Could | 6h | User can upload files and download result via browser | area/web type/feat |
| T-024 | Benchmark processing <1 s for 500 KB/1 MB files | OPEN | Could | 4h | Automated perf test under threshold | area/perf type/chore |
| T-025 | Ensure web UI meets WCAG 2.1 AA guidelines | DONE | Should | 4h | Keyboard navigation and alt-text verified | area/web type/feat |
