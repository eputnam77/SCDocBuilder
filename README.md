# SCDocBuilder

Fill FAA Special Conditions templates with worksheet answers.

## What

SCDocBuilder reads your worksheet and writes a polished Special Conditions
notice. It handles table fields, conditional blocks and multiline responses.

## Why

You avoid manual editing and stay consistent with AIR-646 style in seconds.

______________________________________________________________________

## ✨ Quick install (recommended)

This path uses **pipx** for system‑wide tool isolation, **uv** for ultra‑fast package resolution, and **Poetry 1.8+** for lock‑file‑driven dependency management.

```bash
# 0. One-time setup: Python & pipx -------------------------------------------------
python --version                # confirm Python ≥3.11

# Debian / Raspberry Pi OS
sudo apt update
sudo apt install -y python3 python3-venv pipx
pipx ensurepath                # add pipx to PATH
source ~/.bashrc               # reload shell so PATH is updated
# If using zsh instead of bash, run:
# source ~/.zshrc

# Windows
python -m pip install --user pipx
python -m pipx ensurepath       # restart shell if PATH changes

# All platforms
pipx install uv                 # fast resolver, venv mgr, lockfile, tool runner

# 1. Clone project ---------------------------------------------------------------
git clone https://github.com/eputnam77/SCDocBuilder.git
cd SCDocBuilder

# 2. Create and activate venv (Python 3.12) --------------------------------------
uv python install 3.12.0        # Download if not present
uv venv --python 3.12.0

# Activate the venv:
#   On Mac/Linux:
source .venv/bin/activate
#   On Windows:
.venv\Scripts\activate

python -m pip install --upgrade pip

# 3. Install project + extras (dev, test, security) ------------------------------
uv pip install -e ".[dev,test,security]"
# (Optional) Allow prerelease dependencies if needed:
# uv pip install -e ".[dev,test,security]" --prerelease=allow

# 4. (Optional) Upgrade pip and pre-commit inside the venv -----------------------
uv pip install --upgrade pip pre-commit

# 5. Install Git hooks -----------------------------------------------------------
pre-commit install

# 6. (Optional) Open generated docs in Word --------------------------------------
# Windows/macOS: double-click the .docx to open in Microsoft Word 2019+
# Debian/Raspberry Pi OS: `sudo apt install libreoffice` or copy to a machine with Word
```

______________________________________________________________________

## 🐍 Virtual‑environment fallback (no uv)

Prefer **uv** for speed, but a plain Python workflow also works:

```bash
python3 -m venv .venv

# Activate environment:
# On Unix/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Upgrade pip and install Poetry
python -m pip install --upgrade pip
pip install poetry

# Install dependencies via Poetry (preferred over requirements-dev.txt)
poetry install --sync

# (Optional) Install project in editable mode — only if not using Poetry's editable mode
pip install -e .
```

______________________________________________________________________

## Run the API, dashboard, and React frontend

```bash
# API – FastAPI with automatic Swagger UI at /docs
python -m scdocbuilder api serve --port 8000
# Browse http://localhost:8000/docs for interactive OpenAPI docs

# Dashboard – lightweight Streamlit example
pip install streamlit
streamlit run src/streamlit_dashboard.py

# React frontend – run the companion React app
# (requires Node.js 18+ and npm)
git clone https://github.com/eputnam77/scdocbuilder-react-frontend.git
cd scdocbuilder-react-frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env.local
npm run dev  # open http://localhost:5173
```

______________________________________________________________________

## 🧪 Quality Checks & Testing Guide

This project uses a multi-tool testing pipeline to ensure code quality, formatting, type safety, security, and robustness. Below is the full suite of commands and best practices for local development and CI validation.

______________________________________________________________________

### 1. ✅ Lint, Format, and Static Type Checks

**Defined in `.pre-commit-config.yaml`** and run automatically before every commit (after running `pre-commit install`):

- **Ruff:** Linting and formatting for Python code (also handles import sorting)
- **Black:** Auto-formats Python code to a consistent style
- **Mypy:** Static type checking
- **Bandit:** Python code security scanning (see below for details)
- **mdformat:** Markdown linting and formatting, with Ruff rules
- **Codespell:** Checks for common spelling mistakes in code, comments, and docs

**To run all checks across the codebase:**

```bash
pre-commit install           # (First time only) Installs pre-commit hooks
pre-commit run --all-files   # Run all checks across the codebase
```

> **Tip:** This is the recommended first step before committing or pushing code.

______________________________________________________________________

### 2. ✅ Unit Tests with Coverage

Run the full test suite with code coverage reporting using pytest:

```bash
pytest --cov=src
```

- Replace `src` with your module's directory if different.
- Coverage results can be uploaded to Codecov or other CI tools.

______________________________________________________________________

### 3. 🔡 Spellchecking

Run [Codespell](https://github.com/codespell-project/codespell) to catch common typos in code, comments, and documentation:

```bash
codespell src tests docs
```

> **Note:** Codespell is also included in pre-commit, so this check runs automatically before each commit.

______________________________________________________________________

### 4. 📚 Docstring Formatting (Optional)

[docformatter](https://github.com/PyCQA/docformatter) ensures all Python docstrings follow [PEP 257](https://peps.python.org/pep-0257/) conventions.

```bash
docformatter -r src/
```

- Recommended for teams/projects that enforce strict docstring style.

______________________________________________________________________

### 5. 🛡️ Security Scanning

Run security scanners to identify vulnerabilities:

- **Bandit:** Scans Python source code for security issues

  ```bash
  bandit -r src -lll --skip B101
  ```

  - `-r src`: Recursively scans the `src` directory
  - `-lll`: Only high-severity issues
  - `--skip B101`: Skip assert statement warnings

- **pip-audit:** Checks installed dependencies for known security vulnerabilities

  ```bash
  pip-audit
  pip-audit -r requirements.txt
  ```

- **Safety (Optional):** Another dependency vulnerability scanner

  ```bash
  safety check
  ```

  - Not required if using pip-audit, but can be added for redundancy.

______________________________________________________________________

### 6. 🧬 Mutation Testing (Optional)

[Mutmut](https://mutmut.readthedocs.io/en/latest/) tests your suite’s effectiveness by making small code changes ("mutations") and checking if your tests catch them.

```bash
mutmut run --paths-to-mutate src
mutmut results
```

- Use this occasionally or in CI for robust projects.
- Mutation testing can be time-consuming.

______________________________________________________________________

### 7. 📦 Suggested Workflow

```bash
pre-commit run --all-files        # Lint, format, type check, spellcheck, markdown, security
pytest --cov=src                  # Unit tests with coverage
bandit -r src -lll --skip B101    # Security scan (code)
pip-audit                         # Security scan (dependencies)
codespell src tests docs          # Spell check (if not running in pre-commit)
docformatter -r src/              # (Optional) Docstring formatting
mutmut run --paths-to-mutate src  # (Optional) Mutation testing
mutmut results
```

______________________________________________________________________

### 8. 📋 Quick Reference Table

| Tool         | Purpose                     | Command Example                               |
| ------------ | --------------------------- | --------------------------------------------- |
| Ruff         | Lint/format Python code     | `pre-commit run --all-files`                  |
| Black        | Code formatter              | `pre-commit run --all-files`                  |
| Mypy         | Static type checking        | `pre-commit run --all-files`                  |
| Bandit       | Security (code)             | `bandit -r src -lll --skip B101`              |
| pip-audit    | Security (dependencies)     | `pip-audit` / `pip-audit -r requirements.txt` |
| Codespell    | Spell check                 | `codespell src tests docs`                    |
| mdformat     | Markdown formatting/linting | `pre-commit run --all-files`                  |
| docformatter | Docstring style (optional)  | `docformatter -r src/`                        |
| Mutmut       | Mutation test (optional)    | `mutmut run --paths-to-mutate src`            |
| Pytest       | Unit tests/coverage         | `pytest --cov=src`                            |
| Safety       | Security (deps, optional)   | `safety check`                                |

______________________________________________________________________


## Quick start

```bash
python -m pip install scdocbuilder
python -m scdocbuilder --template template.docx --worksheet worksheet.docx
```

## Contributing

* `poetry install --with dev`
* `pre-commit run --files <changed-files>`
* `pytest -q`

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
