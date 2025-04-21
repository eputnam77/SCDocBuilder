## **Product Requirements Document (PRD)**  
**FAA Special Conditions Template Filler**  
**Version 1.0 – April 21, 2025**

---

### 1. Problem Statement
Rule‑writers in the FAA Aircraft Certification Service must turn a *Special‑Conditions Worksheet* (internal MS Word form) into a legally formatted *Special Conditions Notice* (template DOCX). Manual copy‑and‑paste is slow and error‑prone. This utility, usable via CLI or web (Gradio/Hugging Face Space), automates placeholder replacement from worksheet to template, including validation and visible markers for missing fields.

---

### 2. Goals & Non‑Goals
| Scope | In | Out |
|-------|----|-----|
|Replace placeholders inside the body, tables, headers & footers of a DOCX|✔|PDF or other formats|
|CLI execution (`python sc_filler.py --template … --worksheet …`)|✔|Desktop GUI|
|Web UI with Gradio (upload worksheet, click *Generate*, download DOCX)|✔|Enterprise SharePoint add‑in|
|Robust logging, validation, and test suite|✔|Automatic style rewriting by AI (future)|
|Conditional text for Worksheet #6 action (TC, amended TC, change, STC)|✔|Other conditional logic|
|Insert visible token if a required field is missing|✔|Abort on missing input|

---

### 3. Personas & User Stories
* **Regulations Engineer (CLI)** – “Run one command during drafting to get a clean SC notice.”  
* **OPA Reviewer (Web)** – “Upload a worksheet, verify a preview, and download the notice on any device.”  
* **Automation Engineer** – “Integrate the script into CI/CD with deterministic exit codes and rich logs for debugging.”

---

### 4. Functional Requirements

| ID | Requirement |
|----|-------------|
|F‑1|Accept two required inputs: `--template <docx>` and `--worksheet <docx>` (CLI) or upload (Web UI).|
|F‑2|Extract field values from paragraphs and tables of the worksheet.|
|F‑3|Replace placeholders in paragraphs, tables, headers, footers, textboxes, and numbered items without altering formatting.|
|F‑4|Handle multiline answers (Q15–17) by reading the line after the prompt.|
|F‑5|Implement Worksheet #6 conditional block using four options. Only one will be inserted; others removed.|
|F‑6|Generate output filename `{template‑stem}_{timestamp}.docx` when `--output` is not specified.|
|F‑7|Return full output path (CLI stdout and Gradio `DownloadButton`).|
|F‑8|Exit code 0 on success; non‑zero for known failure cases: `ENOFILE`, `EVALID`, `EREPLACE`.|
|F‑9|Support `--dry-run` to emit a JSON diff (`{placeholder: {"old":…, "new":…}}`) without writing a file.|
|F‑10|**Graceful Missing‑Field Handling**: If a field is missing, insert `[[NEED:<Field‑Label>]]` in output. Do not abort.|
|F‑11|**Need Token Override**: Use CLI flag `--need-token "<token>"` to set a custom missing-value marker.|

---

### 5. Non‑Functional Requirements

| Category | Requirement |
|----------|-------------|
|Reliability|Deterministic output for same inputs; 90%+ unit test coverage.|
|Performance|≤ 1 s for 1.5 MB combined input on AWS t3.micro.|
|Logging|Standard Python logging; DEBUG–ERROR; rotate logs ≥ 5 MB.|
|Validation|Check both files exist, are DOCX (zip test), and worksheet contains required fields (Applicant, Model, Q15–17). Insert NEED tokens if any are missing.|
|Security|Reject files > 10 MB; no macro execution; delete web uploads post-session.|
|Portability|Python 3.10+; platform-independent.|
|Accessibility (Web)|WCAG 2.1 AA compliant: alt-text, keyboard nav.|

---

### 6. Detailed Logic Flow

1. **Parse Args / Receive Upload**
2. **Validate Input**
   - Extension, size, required structure
3. **Extract Worksheet Data**
   - Multiline fields via `.paragraphs[i+1].text`
4. **Conditional Logic for Q6**
   - Enable only matching block via `[[OPTION_N]]…[[/OPTION_N]]`
5. **Missing Field Handling**
   - If missing, insert `[[NEED:<label>]]` (default token or user-specified)
6. **Build Replacement Map**
7. **Traverse and Replace in Document**
8. **If dry-run: Show diff**
9. **Save DOCX or return preview**
10. **Return path or diff results**

```python
if not value:
    replacement = f"{NEED_TOKEN}{label}]]"
    log.warning(f'Field "{label}" missing – inserted {replacement}')
    missing_fields.append(label)
else:
    replacement = value
```

---

### 7. CLI Specification

```
usage: sc_filler.py --template TEMPLATE --worksheet WORKSHEET
                      [--output OUTPUT] [--dry-run]
                      [--need-token "[[NEED:"]
                      [--log-level {DEBUG,INFO,WARNING,ERROR}]
```

---

### 8. Gradio/Web UI Spec

```python
with gr.Blocks(title="FAA Special Conditions Template Filler") as demo:
    template_file = gr.File(label="SC Template (.docx)", file_types=['.docx'])
    worksheet_file = gr.File(label="Worksheet (.docx)", file_types=['.docx'])
    dry_run = gr.Checkbox(label="Dry‑run (preview JSON diff)")
    output_view = gr.File(label="Generated Document")
    diff_view = gr.JSON()

    def generate(template, worksheet, dry_run):
        path, diff = run_filler(template, worksheet, dry_run)
        return (None if dry_run else path), (diff or None)

    gr.Button("Generate").click(
        generate,
        inputs=[template_file, worksheet_file, dry_run],
        outputs=[output_view, diff_view]
    )
demo.launch()
```

If dry-run is selected and missing fields are found, render a preview table above the download button.

---

### 9. Logging & Debugging Plan
| Level | Example Message |
|-------|-----------------|
|DEBUG|`Replaced {Applicant name} -> "Boeing"`|
|INFO|`Saved file to SC_Notice_20250421_134500.docx`|
|WARNING|`Field "Q15" missing – inserted [[NEED: Q15]]`|
|ERROR|`Template not readable – invalid .docx zip structure`|

---

### 10. Validation Rules

| Rule | Behavior |
|------|----------|
|Schema|Validate presence of required placeholders; insert sentinel if missing.|
|Content|Validate date formats with `dateutil`; reject invalid.|
|Conditional|Q6 must have exactly one checked value (1–4).|
|Diff JSON|`"status":"missing"`, `"replacement":"[[NEED: Field]]"`|

---

### 11. Testing & Quality

| Type | Description |
|------|-------------|
|Unit Tests|Test extraction, missing value fallback, conditional blocks, and dry-run behavior.|
|Integration|Golden file comparison for real samples.|
|CI/CD|GitHub Actions on Ubuntu and Windows.|

---

### 12. Proposed Enhancements (Backlog)

| Priority | Feature | Notes |
|----------|---------|-------|
|P1|Export and download as docx.|
|P1|Inline DOCX→HTML preview in browser.|
|P2|AI “Rewrite” via OpenAI (opt-in, behind flag).|
|P2|External schema for placeholders.|
|P3|Export as PDF via `libreoffice` headless mode.|
|P3|Batch mode processing of multiple worksheets.|
|P3|Dockerized deployment + Hugging Face demo.|

---

### 13. Dependencies & Packaging

* `python-docx >= 1.1.2` – Word processing  
* `gradio >= 4.16` – Web UI  
* `python-dateutil`, `pytest`, `rich`  

Deliverable: `faa-sc-filler` on PyPI, `pipx install` supported.

---

### 14. Acceptance Criteria

| Scenario | Expected Result |
|----------|-----------------|
|Valid inputs|Clean DOCX output, no `{…}` placeholders, exit 0.|
|Missing Q15|Insert `[[NEED: Q15]]`, log warning, exit 0.|
|Dry-run|Returns JSON diff with `"status":"missing"` entries.|
|Web UI|Users upload, preview missing fields, and download in <5s.|
|CI tests|90%+ coverage, all unit tests pass.|

---

### 15. Glossary

| Term | Definition |
|------|------------|
|SC|Special Conditions (14 CFR § 21.16)|
|Worksheet|Internal FAA input form|
|Template|DOCX with placeholder tags|
|Placeholder|Tag like `{Applicant name}` or `[[OPTION_1]]`|
|NEED Token|Visible marker for missing values, e.g., `[[NEED: Field]]`|
