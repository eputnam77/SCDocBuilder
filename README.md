# FAA Special Conditions Document Builder

This project automates replacing placeholders in FAA Special Conditions notice templates using data from worksheet documents.

## Repository layout

```
├── src/                # library code
│   └── scdocbuilder/
├── tests/              # unit and property tests
├── docs/               # documentation for MkDocs
├── scripts/            # helper scripts used in CI
├── .github/workflows/  # CI configuration
└── .dev/               # planning documents and ADRs (not packaged)
```

The `src/` layout keeps import paths stable when running tests and building wheels.

---

# SCDocBuilder

Build FAA Special‑Conditions documents—CLI, FastAPI, and template engine in one repo.

**SCDocBuilder** takes a worksheet of parameters (title, applicability, regulatory basis, etc.) and produces a legally formatted Special‑Conditions Word document—or HTML for TipTap—ready for FAA publication. The repository bundles:

* a **CLI** (`scdocbuilder`) for local workflows
* a **FastAPI** backend (optional) for web integrations
* unit‑tested template logic so every output meets AIR‑646 style

---

## ✨ Quick install (recommended)

We keep the tooling consistent with the `*ScriptCLI` family: **pipx** for global shims, **uv** for super‑fast Python/venv work, and **Poetry ≥ 1.8** for lock‑file sync.

```bash
# 0 One‑time per machine ────────────────────────────────────────────────
python3 -m pip install --user pipx
python3 -m pipx ensurepath                         # restart shell if PATH changed

pipx install uv                                    # https://github.com/astral-sh/uv
pipx install poetry                                # https://python-poetry.org/

# 1 Per project ────────────────────────────────────────────────────────
git clone https://github.com/eputnam77/SCDocBuilder.git
cd SCDocBuilder

# 2 Create & activate .venv (CPython 3.13) --------------------------------
uv python install 3.13.0                           # downloads if missing
uv venv --python 3.13.0                            # writes .venv/ by default
source .venv/bin/activate                          # Windows: .venv\Scripts\activate

# 3 Sync deps at uv speed ------------------------------------------------
poetry config installer.executable uv              # once per machine
poetry sync --with dev                             # mirrors poetry.lock + dev deps

# 4 Developer extras ----------------------------------------------------
pre-commit install                                 # Git hooks
```

---

## Alternative installs

| Scenario                 | Command                                                                   |
| ------------------------ | ------------------------------------------------------------------------- |
| **PyPI (when released)** | `pip install scdocbuilder`                                                |
| **Direct Git source**    | `python -m pip install git+https://github.com/eputnam77/SCDocBuilder.git` |

After a package‑based install you can locate the source directory with:

```bash
cd "$(python - <<'PY'
import importlib, pathlib
print(pathlib.Path(importlib.import_module("scdocbuilder").__file__).parent.parent)
PY
)"
```

---

## 🐍 Virtual‑env fallback (no uv)

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

python -m pip install --upgrade pip
pip install poetry
poetry install --with dev --sync          # --sync flag still works but is deprecated
pre-commit install
```

---

## Usage examples

```bash
# Display the CLI help
python -m scdocbuilder --help

# Generate DOCX from a worksheet
scdocbuilder build worksheet.xlsx --format docx --output sc.docx

# Dry‑run HTML for TipTap editing
scdocbuilder build worksheet.xlsx --format html --dry-run
```

---

## Running the API (optional)

```bash
uvicorn scdocbuilder.api:app --reload --port 8000
# Browse interactive docs at http://localhost:8000/docs
```

---

### About the requirement files

`requirements.txt` & `requirements‑dev.txt` exist only for legacy tooling. **`poetry sync`** (or **`pip install -e ".[dev]"`**) remains the authoritative way to stay in lock‑step with **pyproject.toml**.

---

## Quick start

Generate a document from the command line:

```bash
python -m scdocbuilder \
  --template template.docx \
  --worksheet worksheet.docx \
  --schema schema.json
```

## Contributing

1. Install dev dependencies with `poetry install --with dev`.
2. Run `pre-commit` before committing to lint and format code.
3. Ensure tests pass with `pytest -q`.

## License

This project is licensed under the **GNU General Public License v3.0**. See
the [LICENSE](LICENSE) file for full terms.
