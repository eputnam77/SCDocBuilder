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
