# AGENTS.md

*Authoritative playbook for the OpenAI Codex multi‑agent workflow in this repository*

---

## 0 · Global Settings

| Key                  | Value                                                |
| -------------------- | ---------------------------------------------------- |
| Default shell        | `bash` (Linux)                                       |
| Python version       | **3.12**                                             |
| Virtual env manager  | **uv** (falls back to `python -m venv`)              |
| Package manager      | **poetry** (`poetry install`)                        |
| Test runner          | **pytest**                                           |
| Coverage thresholds  |  70 % on feature branches → 90 % on `main`           |
| Code formatter       | **black**                                            |
| Linter               | **ruff** (includes import‑sorting)                   |
| Static‑type checker  | **mypy --strict**                                    |
| Security scanners    | **bandit -r src**, **pip‑audit -r requirements.txt** |
| Docs generator       | **MkDocs Material** (`mkdocs build`)                 |
| Commit message style | **Conventional Commits**                             |
| CI provider          | **GitHub Actions**                                   |

> **Data flow**  Every agent works from the latest commit on its branch and communicates only via GitHub Issues/PRs.

---

## 1 · Agents & Execution Order

|  #  | Agent ID     | Purpose (summary)                                                                     | Auto‑trigger condition        |
| --- | ------------ | ------------------------------------------------------------------------------------- | ----------------------------- |
|  0  | `planner`    | Parse `PRD.md`, create `TASKS.md` (epics → issues with acceptance criteria & labels). | manual                        |
|  1  | `architect`  | Design folder layout, write ADRs, initialise `pyproject.toml`, CI workflow.           | `planner` PR merged           |
|  2  | `scaffolder` | Generate skeleton code/tests for each open issue.                                     | `architect` PR merged         |
|  3  | `builder`    | Implement code for issues marked **ready**; keep tests ≥70 % cov.                     | new ready issue               |
|  4  | `linter`     | Run `ruff --fix` & `black`; open PR if diff.                                          | after builder push            |
|  5  | `tester`     | Execute dev‑gate (`pytest`, type‑check, coverage ≥70 %).                              | after linter green            |
|  6  | `fixer`      | Patch only failing files, re‑run gate until green.                                    | on test failure               |
|  7  | `security`   | Run Bandit & pip‑audit; open CVE issues.                                              | nightly · before merge → main |
|  8  | `docwriter`  | Update `README.md`, API refs, examples, changelog.                                    | branch green & cov ≥90 %      |
|  9  | `reviewer`   | Human‑style review; request approvals.                                                | after docwriter               |
|  10 | `releasebot` | Bump semver, tag, build & push Docker image, draft release notes.                     | PR merged → main              |

### Agent Handoff Conventions

* **Feature branches** enforce the *dev gate* (70 % coverage).
* The **main** branch enforces the *release gate* (90 % coverage, security pass, docs build).
* Each agent finishing successfully applies the label `ready‑for:<next‑agent>`; a GitHub Action reads this label and triggers the next agent via the Codex API.

---

## 2 · Quality Gates

### Dev Gate (feature branches)

```bash
ruff check src tests
black --check src tests
mypy --strict src
bandit -r src -lll --skip B101      # allow asserts during early dev
pytest -q --cov=src --cov-fail-under=70
```

### Release Gate (`main`)

```bash
ruff check src tests
black --check src tests
mypy --strict src
bandit -r src -lll
pip-audit -r requirements.txt
pytest -q --cov=src --cov-fail-under=90
mkdocs build --strict
```

Any non‑zero exit hands control to **fixer**.

---

## 3 · Branch & Commit Policy

* **Branches**  `plan/<slug>` · `scaffold/<slug>` · `feat/<slug>` · `fix/<issue>` · `docs/<topic>` · `test/<scope>`
* **Commits** follow Conventional Commits, e.g.

  ```
  feat(auth): add OAuth2 login flow
  fix(api): prevent division‑by‑zero in calculator
  chore(ci): raise coverage threshold to 90%
  ```
* Default merge strategy: **squash‑merge**, with required‑status checks on `main`.

---

## 4 · Automation Workflow (GitHub Actions)

The central router (`.github/workflows/agents.yml`) decides which agent to launch next:

```yaml
on:
  push:
    branches: ["**"]
jobs:
  codex-router:
    steps:
      - uses: actions/checkout@v4
      - name: Detect next agent
        run: >-
          ./scripts/next-agent.sh  # sets $NEXT_AGENT env var
      - name: Trigger agent via Codex API
        if: env.NEXT_AGENT != ''
        run: >-
          codex run --agent "$NEXT_AGENT"
```

---

## 5 · Environment Setup

* **Python 3.12** via `pyenv` or container.
* Local dev startup:

  ```bash
  uv venv
  uv pip install -r requirements-dev.txt
  pre-commit install
  ```
* Codespaces/VS Code: devcontainer runs pre‑commit on open.

---

## 6 · Failure‑Recovery Matrix

| Problem            | Responsible Agent | Remedy                         |
| ------------------ | ----------------- | ------------------------------ |
| Lint error         | linter            | Auto‑fix & push                |
| Type error         | tester → fixer    | Patch types/code               |
| Test failure       | fixer             | Minimal diff fix, ensure green |
| Coverage drop      | builder/tester    | Add tests or mark exceptions   |
| High CVE           | security          | Bump dependency or patch code  |
| Docs build failure | docwriter         | Regenerate & push fix          |

---

## 7 · References

* [Ruff documentation](https://docs.astral.sh/ruff/)
* [Black documentation](https://black.readthedocs.io/)
* [Pytest documentation](https://docs.pytest.org/)
* [Bandit documentation](https://bandit.readthedocs.io/)
* [pip‑audit](https://pypi.org/project/pip-audit/)

---

*End of AGENTS.md*
