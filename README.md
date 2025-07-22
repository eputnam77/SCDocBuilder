# FAA Special Condition Template Filler

This project automates replacing placeholders in FAA Special Condition notice templates using data from worksheet documents.

## Repository layout

```
├── src/                # library code
│   └── faa_sc_replacer/
├── tests/              # unit and property tests
├── docs/               # documentation for MkDocs
├── scripts/            # helper scripts used in CI
├── .github/workflows/  # CI configuration
└── .dev/               # planning documents and ADRs (not packaged)
```

The `src/` layout keeps import paths stable when running tests and building wheels.

## Development setup

Use [Poetry](https://python-poetry.org/) and `uv` to manage the virtual environment:

```bash
uv venv "3.12"
poetry install --with dev
poetry sync --with dev
pre-commit install
```

Run the CLI with:

```bash
python -m faa_sc_replacer --help
```

## Quick start

Generate a document from the command line:

```bash
python -m faa_sc_replacer \
  --template template.docx \
  --worksheet worksheet.docx \
  --schema schema.json
```

## Contributing

1. Install dev dependencies with `poetry install --with dev`.
2. Run `pre-commit` before committing to lint and format code.
3. Ensure tests pass with `pytest -q`.
