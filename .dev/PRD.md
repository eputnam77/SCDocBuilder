**Product Requirements Document (PRD)**
**Special Conditions Doc Builder (SCDocBuilder)**
**Version 0.2 – July 2025**

---

### 1 · Problem Statement

Rule-writers in the FAA Aircraft Certification Service currently copy content from an internal *Special-Conditions Worksheet* (DOCX form) into a legally formatted *Special Conditions Notice* (template DOCX). Manual copy-and-paste is slow and error-prone.
**Goal:** ship a small Python utility that (1) ingests a worksheet, (2) injects its answers into a template, and (3) returns both a finished Word document **and** clean HTML ready for TipTap editing.

---

### 2 · Scope

| Area                                                      | **In** | **Out**                 |
| --------------------------------------------------------- | ------ | ----------------------- |
| Placeholder replacement in body, tables, headers, footers | ✔      | PDF export (backlog)    |
| CLI execution (`scdocbuilder …`)                           | ✔      | Desktop GUI             |
| Minimal web UI (upload → download)                        | ✔      | SharePoint add-in       |
| FastAPI REST endpoint                                     | ✔      | User auth / RBAC        |
| Robust logging, validation & test suite                   | ✔      | Full AI “rewrite” mode  |
| Worksheet #6 conditional blocks                           | ✔      | Other conditional logic |

---

### 3 · Personas & User Stories

* **Regulations Engineer (CLI).** “One command turns my worksheet into a clean notice.”
* **OPA Reviewer (Web).** “Upload worksheet, preview, download notice on any device.”
* **Automation Engineer (API).** “Integrate into CI with deterministic exit codes and JSON logs.”

---

### 4 · Functional Requirements

| ID  | Requirement                                                                                                                                                                                |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| F-1 | Accept two required inputs: `--template <docx>` and `--worksheet <docx>` (CLI or upload).                                                                                                  |
| F-2 | Extract answers from paragraphs *and* tables in the worksheet (existing code).                                                                                                             |
| F-3 | Replace placeholders across paragraphs, tables, headers, footers & text boxes **without losing formatting** using *python-docx* APIs ([python-docx Documentation][1]).                     |
| F-4 | Handle multiline answers for Q15-17 by reading the paragraph **after** the prompt.                                                                                                         |
| F-5 | Worksheet #6 conditional block – render exactly one of four `[[OPTION_n]]` blocks; delete the rest.                                                                                        |
| F-6 | Add **TipTap HTML export**: generate semantic HTML from the completed DOCX via *mammoth* and sanitise it with *bleach* before returning to the UI ([PyPI][2], [bleach.readthedocs.io][3]). |
| F-7 | `--output` optional → filename `{template-stem}_{timestamp}.docx`.                                                                                                                         |
| F-8 | Exit 0 on success; non-zero on `ENOFILE`, `EVALID`, `EREPLACE`.                                                                                                                            |
| F-9 | `--dry-run` prints a DeepDiff-style JSON diff of `{placeholder: {old,new}}` ([PyPI][4]).                                                                                                   |

---

### 5 · Non-Functional Requirements

| Category            | Requirement                                                                                                                       |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Reliability         | Deterministic output; unit-test coverage ≥ 90 %.                                                                                  |
| Performance         | ≤ 1 s for 500 KB template + 1 MB worksheet on t3.micro.                                                                           |
| Logging             | Structured JSON logs via **structlog** or colourised console via **rich** ([structlog][5], [rich.readthedocs.io][6]).             |
| Validation          | Pre-flight: file exists, ≤ 10 MB, MIME verified with *python-magic*; worksheet must contain Applicant, Model, Q15-17. ([PyPI][7]) |
| Security            | Reject macros; delete uploads after request.                                                                                      |
| Portability         | Runs on CPython 3.10 +. No Windows-only paths.                                                                                    |
| Accessibility (Web) | WCAG 2.1 AA – alt-text, keyboard navigation.                                                                                      |

---

### 6 · Open-Source Optimisations (no scope creep)

| Need                             | Suggested OSS & Benefit                                                                                                                                      |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Safer placeholder rendering      | **python-docx-template** — Jinja-style templating instead of manual run iteration ([Docxtpl Documentation][8])                                               |
| Cleaner CLI UX                   | **Typer** – autocompletion & rich-help based on type hints ([typer.tiangolo.com][9])                                                                         |
| Declarative input checks         | **Pydantic** models for filenames/options → immediate, typed error messages ([docs.pydantic.dev][10])                                                        |
| Structured/pretty logging        | **structlog** (machine-readable JSON) or **loguru**/ **rich** for colourised console ([structlog][5], [loguru.readthedocs.io][11], [rich.readthedocs.io][6]) |
| Fast diff output for `--dry-run` | **DeepDiff** – avoids home-grown dict comparison ([PyPI][4])                                                                                                 |
| HTML sanitisation                | **bleach** – strips unsafe tags/attrs before feeding TipTap ([bleach.readthedocs.io][3])                                                                     |

All libraries are OSI-approved, actively maintained, and installable from PyPI.

---

### 7 · Detailed Logic Flow

1. **Parse CLI args / Receive Upload** (Typer & FastAPI).
2. **Validate Files** (pydantic → size/MIME checks via python-magic).
3. **Extract Worksheet Data** (`extract_fields`).
4. **Determine Conditional Choice** (Q6).
5. **Load Template** (`python-docx` or `docxtpl`).
6. **Replace Placeholders & Apply Conditionals**.
7. **If dry-run:** produce DeepDiff JSON and exit.
8. **Save DOCX** and, if requested, **convert to HTML** (mammoth → bleach).
9. **Return** file path (CLI) or streamed download (FastAPI).

---

### 8 · Interfaces

#### 8.1 CLI (Typer)

```bash
scdocbuilder --template TEMPLATE.docx --worksheet WORKSHEET.docx \
            [--output OUT.docx] [--html-out OUT.html] [--dry-run]
```

#### 8.2 FastAPI

| Endpoint              | Method | Purpose                                                | Notes                                |
| --------------------- | ------ | ------------------------------------------------------ | ------------------------------------ |
| `/generate`           | POST   | Upload worksheet/template, return generated DOCX/HTML  | Core document generation             |
| `/health`             | GET    | Service health/status check                            | For uptime checks                    |
| `/schema`             | GET    | Return required placeholders/schema as JSON            | Enables dynamic UI/client validation |
| `/validate`           | POST   | Validate files/fields before full generation           | Early feedback for users             |
| `/preview`            | POST   | Return HTML preview (TipTap-ready) without saving DOCX | In-browser preview                   |
| `/download/{file_id}` | GET    | Download a previously generated file by unique ID      | Needed if async or persistent        |
| `/jobs`               | GET    | List previously generated jobs for a user/session      | Audit/download history               |
| `/logs/{job_id}`      | GET    | Retrieve logs/status for a specific job                | For advanced debugging               |
| `/batch-generate`     | POST   | Bulk ZIP of worksheets in, ZIP of results out          | Power users/automation               |
| `/config`             | GET    | Retrieve app version/configuration info                | Helps UI/clients adapt to backend    |


#### 8.3 Web UI

Simple single-page form (React/Vue) with drag-and-drop, preview, download buttons. No third-party hosting assumed; can run behind Nginx or in Docker.

---

### 9 · Logging & Debugging

| Level   | Example (structured)                                                              |
| ------- | --------------------------------------------------------------------------------- |
| DEBUG   | `{"event":"replace","field":"Applicant","old":"{Applicant name}","new":"Boeing"}` |
| INFO    | `{"event":"saved","path":"SC_Notice_20250722_113045.docx"}`                       |
| WARNING | `{"event":"missing_field","field":"Telephone"}`                                   |
| ERROR   | `{"event":"worksheet_parse_error","detail":"not a zip file"}`                     |

---

### 10 · Testing & Quality

* **Unit tests** – extraction, conditional logic, HTML sanitisation.
* **Integration tests** – golden DOCX/HTML fixtures.
* **CI** – GitHub Actions matrix (Ubuntu & Windows), code-coverage badge, Ruff + MyPy + Bandit pre-commit hooks.

---

### 11 · Packaging & Deployment

* Publish to PyPI as `scdocbuilder`; installable via `pipx`.
* Dockerfile (Alpine + Python 3.12) with entry-points for API & CLI.
* Optional Helm chart for internal Kubernetes deployment.

---

### 12 · Acceptance Criteria

1. Valid template + worksheet ⇒ CLI exits 0; no unreplaced tokens remain.
2. Missing Q15 answer ⇒ exit `EVALID` with clear message.
3. Web upload ⇒ download in ≤ 5 s on local Docker container.
4. All tests pass; coverage ≥ 90 %; lints/typing clean.

---

### 13 · Glossary

* *SC* – Special Conditions (14 CFR § 21.16)
* *Worksheet* – FAA internal form capturing project data
* *Template* – Word document with placeholders
* *Placeholder* – Token like `{Applicant name}` to be replaced
* *TipTap* – Rich-text editor used in downstream FAA tools

---

### 14 · Implementation Guidelines

```python
def load_document(path): ...
def extract_fields(doc): ...
def apply_conditionals(doc, choice): ...
def replace_placeholders(doc, fields): ...
def convert_to_html(doc): ...
```

Follow single-responsibility functions, exhaustive unit tests, and structured logs for ease of maintenance.

