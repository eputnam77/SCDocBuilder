**Product Requirements Document (PRD)**  
*FAA Special‑Conditions Placeholder Replacer*  
*Version 0.1 – April 21 2025*

---

### 1. Problem Statement
Rule‑writers in the FAA Aircraft Certification Service must turn a *Special‑Conditions Worksheet* (internal MS Word form) into a legally formatted *Special Conditions Notice* (template DOCX). Manual copy‑and‑paste is slow and error‑prone. The goal is to ship a Python utility that accepts a worksheet DOCX, replaces all placeholders in a template DOCX, and returns a finished Word file.

---

### 2. Goals & Non‑Goals
| Scope | In | Out |
|-------|----|-----|
|Replace placeholders inside the body, tables, headers & footers of a DOCX|✔|PDF or other formats|
|CLI execution (`python sc_replacer.py --template … --worksheet …`)|✔|Desktop GUI|
|Simple web UI for uploads and downloads|✔|Enterprise SharePoint add‑in|
|REST API with FastAPI (upload worksheet, return DOCX)|✔|User management & authentication|
|Robust logging, validation, and test suite|✔|Automatic style rewriting by AI (future)|
|Conditional text for Worksheet #6 action (TC, amended TC, change, STC)|✔|Other conditional logic|

---

### 3. Personas & User Stories
* **Regulations Engineer (CLI)** – “Run one command during drafting to get a clean SC notice.”  
* **OPA Reviewer (Web)** – “Upload a worksheet, verify a preview, and download the notice on any device.”  
* **Automation Engineer** – “Integrate the script into CI/CD with deterministic exit codes and rich logs for debugging.”

---

### 4. Functional Requirements

| ID | Requirement |
|----|-------------|
|F‑1|Accept **two** required inputs: `--template <docx>` and `--worksheet <docx>` (CLI) or file‑upload components (UI).|
|F‑2|Extract field values by scanning paragraphs *and* tables of the worksheet (already implemented).|
|F‑3|Replace placeholders in all runs inside paragraphs, tables, headers, footers, textboxes, and numbered list items without losing formatting. (<https://python-docx.readthedocs.io/en/latest/user/text.html>) citeturn0search8|
|F‑4|Handle multiline answers for questions 15–17 by reading **the line immediately following** the question prompt (regex or table row).|
|F‑5|Implement new conditional block for Worksheet #6 (“Action prompting special conditions”) using four numbered choices: 1 TC, 2 Amended TC, 3 Change, 4 STC. • Placeholder text pattern: `[[OPTION_1]]…[[/OPTION_1]]`, etc. • Rule: include exactly **one** option (matching the worksheet digit); delete the other three entirely.|
|F‑6|Generate output filename `{template‑stem}_{timestamp}.docx` when `--output` is omitted.|
|F‑7|Return the full path in CLI **stdout** and provide a download link in the web UI|
|F‑8|Exit code 0 on success; non‑zero on handled error categories (`ENOFILE`, `EVALID`, `EREPLACE`).|
|F‑9|Provide `--dry‑run` flag to print a JSON diff (`{placeholder: {"old":…, "new":…}}`) without writing a file.|

---

### 5. Non‑Functional Requirements

| Category | Requirement |
|----------|-------------|
|Reliability|100 % deterministic output for same inputs; unit tests ≥ 90 % statement coverage.|
|Performance|Process ≤ 500 KB template + 1 MB worksheet in < 1 s on AWS t3.micro.|
|Logging|Python `logging` with levels **DEBUG**, **INFO**, **WARNING**, **ERROR**; rotate log file after 5 MB.|
|Validation|*Pre‑flight*: check both files exist, are DOCX (zip test), and worksheet contains mandatory fields (Applicant, Model, Q15–17).  Fail with helpful message.|
|Security|Reject files > 10 MB; never execute macros; delete uploads after web session ends.|
|Portability|Runs on Python 3.10+; no Windows‑only paths.|
|Accessibility (Web)|Follows WCAG 2.1 AA – alt‑text labels, keyboard navigation.|

---

### 6. Detailed Logic Flow

1. **Parse Args / Receive Upload**  
2. **Validate Input**  
   • size, extension, required fields  
3. **Extract Worksheet Data** (`extract_worksheet_data`)  
   • New *multiline* capture: on question match, read `.paragraphs[index+1].text` if empty answer area  
4. **Build *conditional‑map*** from Q6 digit → `active_option`  
5. **Load Template** (`python-docx.Document`)  
6. **Traverse Elements**  
   - `doc.paragraphs`, `table.rows.cells.paragraphs`, `doc.sections[i].header/footer.paragraphs`  
7. **Replacement Rules**  
   ```
   if '[[OPTION_' in text:  
       keep run if OPTION_N == active_option else delete run
   for placeholder in {Applicant name}, …: run.text = run.text.replace(placeholder, value)
   ```  
8. **Dry‑run diff** (if requested)  
9. **Save Output**  
10. **Return / Download**

---

### 7. CLI Specification

```
usage: sc_replacer.py --template TEMPLATE --worksheet WORKSHEET [--output OUTPUT]
                      [--dry-run] [--log-level {DEBUG,INFO,WARNING,ERROR}]
```

Example:

```bash
python sc_replacer.py \
  --template "Notice_SC_TEMPLATE.docx" \
  --worksheet "SC_worksheet_AT11885IB-T.docx"
```

---

### 8. Web UI Spec

A lightweight browser interface should allow the user to upload a template and worksheet, select **dry‑run** mode, and download the generated document. Implementation details are not prescribed.

### 8a. FastAPI API Spec

```python
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/generate")
async def generate(template: UploadFile, worksheet: UploadFile):
    path, _ = run_replacer(template.file, worksheet.file, dry_run=False)
    return FileResponse(path)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```


---

### 9. Logging & Debugging Plan
| Level | Example Message |
|-------|-----------------|
|DEBUG|`Replaced {Applicant name} -> "Boeing Commercial Aircraft"`|
|INFO |`Saved file to SC_Notice_20250421_134500.docx`|
|WARNING|`Field 'Telephone phone no' missing in worksheet; inserted blank`|
|ERROR|`Worksheet parsing failed: cannot read zip file`|

*Debug Tips*  
* Run with `--log-level DEBUG > run.log` and open in VS Code log viewer.  
* Use `--dry-run` to spot missing placeholders before generating the notice.

---

### 10. Validation Rules
* **Schema** – YAML file listing mandatory placeholders; script validates presence.  
* **Content** – Date fields parsed via `dateutil`; reject if invalid.  
* **Conditional** – Exactly one Q6 digit (1‑4) must be checked; else `EVALID`.

---

### 11. Testing & Quality
* **Unit Tests** (pytest)  
  - Test extraction for each worksheet question.  
  - Test conditional logic by crafting mini‑templates containing the four `[[OPTION_n]]` blocks.  
  - Test header/footer replacement.  
* **Integration Tests** – Golden‑file comparison.  
* **CI** – GitHub Actions matrix (Ubuntu, Windows).

---

### 12. Proposed Enhancements (Backlog)
| Priority | Feature | Notes |
|----------|---------|-------|
|P1|Add docx‑to‑PDF export via `libreoffice --headless`|
|P1|Preview finished notice in browser (docx→HTML)|
|P2|AI “Rewrite” mode: call OpenAI to simplify long answers; gated by `--rewrite` flag.|
|P2|Configurable placeholder schema via external YAML.|
|P3|Batch mode: accept folder of worksheets and zip outputs.|
|P3|Docker container & Hugging Face Space demo.|

---

### 13. Dependencies & Packaging
* `python-docx >= 1.1.2` – DOCX manipulation citeturn0search8
* `fastapi` – REST API service
* `python-dateutil`, `pytest`, `rich` (optional nicer logs)

Deliver on PyPI as `faa-sc-replacer` with `pipx install`.

---

### 14. Acceptance Criteria
1. Given valid template & worksheet, CLI exits 0 and produced DOCX contains no unreplaced braces `{…}`.  
2. If worksheet misses Q15 answer, script exits with `EVALID` and message “Question 15 summary missing”.  
3. Web UI running on Hugging Face Space lets user upload files and download result within 5 s.  
4. All unit tests pass in CI; coverage ≥ 90 %.

---

### 15. Glossary
*SC* – Special Conditions (14 CFR § 21.16)
*Worksheet* – Internal FAA form capturing project data
*Template* – Word document with placeholders
*Placeholder* – Token like `{Applicant name}` to be replaced

---

### 16. Implementation Guidelines

The utility should be structured as a set of small, single‑purpose functions so
future contributors can easily extend or embed the code.  Suggested helpers:

```
load_document(path)
extract_fields(worksheet_doc)
replace_placeholders(template_doc, fields)
apply_conditionals(template_doc, action_choice)
validate_input_files(template_path, worksheet_path)
save_document(doc, output_path)
```

Other best practices:

* Traverse **all** parts of the DOCX – body paragraphs, tables, headers,
  footers and, when possible, text boxes – to avoid leaving placeholders behind.
* Perform robust validation and return clear error codes if files are missing,
  invalid or lack required fields.
* Allow a YAML/JSON file to define the placeholder schema so new tokens can be
  added without code changes.
* The `--dry-run` option should print a JSON summary of replacements without
  writing the output file.
* Provide minimal logging with a configurable level.
* Optionally support a **batch mode** that processes every worksheet in a
  directory.
* Include unit tests so the package can be embedded with confidence.

| Improvement Area      | Value                     | How Complex? |
| --------------------- | ------------------------- | ------------ |
| Modular functions     | Easy maintenance          | Low          |
| Full DOCX traversal   | Fewer missed placeholders | Low‑Med      |
| Input validation      | More reliable embedding   | Low          |
| Dry‑run preview       | Safer, easier debugging   | Low          |
| Minimal logging       | Easy troubleshooting      | Low          |
| Configurable schema   | Adaptable to change       | Low‑Med      |
| Batch mode (optional) | Workflow boost            | Low          |

