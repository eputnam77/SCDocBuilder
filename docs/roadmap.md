## 🚧 FAA SC Template Filler – Roadmap (v1.0)

### 🗂️ Phase 1 – Project Setup and Planning  
**Timeline**: April 21–25, 2025  
**Goals**:
- Set up repo, environments, initial boilerplate
- Finalize requirements, design, and acceptance criteria

| Task | Description | Owner | Deliverable |
|------|-------------|-------|-------------|
|1.1|Create GitHub repo with CI/CD scaffolding (Ubuntu & Windows)|Dev Lead|Repo + `.github/workflows`|
|1.2|Draft milestone plan with sprint breakdown|PM|Gantt-style plan or tracker|
|1.3|Define logging schema (log levels, rotation)|Lead Dev|Logging config module|
|1.4|Draft template and worksheet sample files|Docs/Legal|Sample `.docx` files|
|1.5|Create test plan structure (unit/integration)|QA|`tests/` folder structure|

**Sources**: N/A  

---

### 🧠 Phase 2 – Core Engine Development (CLI MVP)  
**Timeline**: April 26–May 10, 2025  
**Goals**:
- Build CLI app with full placeholder replacement, validation, logging, dry-run

| Task | Description | Owner | Deliverable |
|------|-------------|-------|-------------|
|2.1|Parse CLI args; implement validation logic for DOCX files|Dev|`main.py`, `args.py`|
|2.2|Extract placeholders and values from worksheet body/tables|Dev|`extract.py`|
|2.3|Apply replacements across all DOCX sections (header, body, footer)|Dev|`replace.py`|
|2.4|Implement conditional logic for Q6 blocks (with deletion of unused)|Dev|`conditionals.py`|
|2.5|Insert `[[NEED:<Field>]]` for missing values, log warning|Dev|`fallback.py`|
|2.6|Implement `--dry-run` output with JSON diff|Dev|`diff.py`|
|2.7|Add output filename autogeneration|Dev|`output.py`|
|2.8|Return proper exit codes|Dev|`exitcodes.py`|

**Milestone**: Fully functioning CLI app  
**Test**: Run `pytest`, golden file comparison  
**Source refs**: [python-docx](https://python-docx.readthedocs.io/en/latest/)

---

### 🌐 Phase 3 – Web UI (Gradio)  
**Timeline**: May 11–20, 2025  
**Goals**:
- Wrap CLI logic in Gradio Blocks interface with preview/dry-run support

| Task | Description | Owner | Deliverable |
|------|-------------|-------|-------------|
|3.1|Build Gradio UI form with file inputs, dry-run checkbox|Frontend|`webui.py`|
|3.2|Wire Gradio inputs to backend engine|Frontend|`interface.py`|
|3.3|Render dry-run diff JSON to preview|Frontend|`diff_view.py`|
|3.4|Implement session cleanup + upload size limit|Security/Dev|Gradio config patch|
|3.5|Add alt-text and keyboard nav for accessibility|Frontend|ARIA-ready Gradio|

**Test**: Manual UI test + Cypress or Playwright optional  
**Reference**: [Gradio Docs](https://www.gradio.app/docs/)

---

### 🔍 Phase 4 – Validation & Testing  
**Timeline**: May 21–28, 2025  
**Goals**:
- Ensure deterministic outputs, performance, and robust error handling

| Task | Description | Owner | Deliverable |
|------|-------------|-------|-------------|
|4.1|Build 90%+ coverage unit test suite|QA|`tests/unit/`|
|4.2|Golden input/output test cases for real FAA forms|QA|`tests/integration/`|
|4.3|Test diff output + edge cases for missing data|QA|Regression matrix|
|4.4|Verify all log levels work as expected|QA|Sample log files|
|4.5|Performance test on `t3.micro`|DevOps|Benchmark report|

**Acceptance Criteria**: PRD Section 14  
**Tools**: Pytest, GitHub Actions, time/perf profiler

---

### 📦 Phase 5 – Packaging & Distribution  
**Timeline**: May 29–31, 2025  
**Goals**:
- Package for PyPI, `pipx`, Hugging Face Space deployment

| Task | Description | Owner | Deliverable |
|------|-------------|-------|-------------|
|5.1|Write setup files for `faa-sc-filler` package|DevOps|`setup.py`, `pyproject.toml`|
|5.2|Create CLI wrapper with `__main__.py`|Dev|Installable CLI tool|
|5.3|Test `pip install` and `pipx install` flows|QA|Validation notes|
|5.4|Deploy demo to Hugging Face Spaces|DevOps|Space public link|

**Confidence**: Medium–High  
**Dependencies**: PyPI, HF account

---

### 📘 Phase 6 – Documentation & Training  
**Timeline**: June 1–5, 2025  
**Goals**:
- Author user guides, internal developer docs, troubleshooting guide

| Task | Description | Owner | Deliverable |
|------|-------------|-------|-------------|
|6.1|User guide with screenshots for Gradio & CLI|Docs|`docs/user_guide.md`|
|6.2|Dev guide: architecture, modules, CLI flags|Dev|`docs/dev_guide.md`|
|6.3|Troubleshooting guide with error code mapping|QA|`docs/errors.md`|
|6.4|Training video or screencast|Outreach|MP4 or YouTube unlisted|

**Reference**: FAA internal SOP or Confluence (if used)

---

### 🔧 Phase 7 – Enhancements (Optional / P2-P3 Backlog)  
**Timeline**: June 6–30, 2025  
**Optional Goals**:
- HTML preview, PDF export, batch processing, Docker

| Feature | Est. Time | Owner | Notes |
|---------|-----------|-------|-------|
|HTML preview|2–3 days|Frontend|Use `python-docx2html` or custom|
|PDF export|1 day|Dev|Requires headless LibreOffice or docx2pdf|
|Batch mode|3–5 days|Dev|Input zip → Output zip|
|Docker support|1 day|DevOps|Dockerfile + `docker run`|

**Dependencies**: Tools like `libreoffice`, `docker-py`

---

### 📋 Summary Timeline

| Date Range | Milestone |
|------------|-----------|
|Apr 21–25 | Planning + Environment Setup |
|Apr 26–May 10 | CLI Core Tool |
|May 11–20 | Gradio Web UI |
|May 21–28 | Testing + Validation |
|May 29–31 | Packaging & HF Launch |
|June 1–5 | Docs + Training |
|June 6–30 | Optional Enhancements |
