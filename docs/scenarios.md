# Scenarios

Real tasks that show how SCDocBuilder fits your workflow.

## Generate a document from the CLI

**Use case**

You want a filled Special Conditions notice from a worksheet.

**Before you begin**

* Install the package.
* Prepare `template.docx` and `worksheet.docx`.

**Steps**

1. Run:

   ```bash
   python -m scdocbuilder \
     --template template.docx \
     --worksheet worksheet.docx
   ```

**Result**

A new DOCX appears in your working folder.

## Preview changes without saving

**Use case**

You want to see the placeholder diff before writing a file.

**Before you begin**

* Follow the previous scenario.

**Steps**

1. Run:

   ```bash
   python -m scdocbuilder \
     --template template.docx \
     --worksheet worksheet.docx \
     --dry-run
   ```

**Result**

JSON diff prints to the terminal.

## Export sanitized HTML

**Use case**

You need HTML for a TipTap editor.

**Before you begin**

* Prepare template and worksheet files.

**Steps**

1. Run:

   ```bash
   python -m scdocbuilder \
     --template template.docx \
     --worksheet worksheet.docx \
     --html-out result.html
   ```

**Result**

`result.html` contains cleaned HTML ready for editors.

## Generate through the API

**Use case**

You want to automate document creation from another service.

**Before you begin**

* `uvicorn scdocbuilder.api:app --port 8000` is running.

**Steps**

1. Run:

   ```bash
   curl -F template=@template.docx \
        -F worksheet=@worksheet.docx \
        http://localhost:8000/generate \
        -o sc.docx
   ```

**Result**

`sc.docx` downloads with all placeholders replaced.

## Request HTML from the API

**Use case**

You need sanitized HTML instead of a DOCX file.

**Before you begin**

* API server is running.

**Steps**

1. Run:

   ```bash
   curl -F template=@template.docx \
        -F worksheet=@worksheet.docx \
        "http://localhost:8000/generate?html=true" \
        > sc.html
   ```

**Result**

`sc.html` contains sanitized markup.

## Check service health

**Use case**

You want to confirm the API is live.

**Before you begin**

* API server is running.

**Steps**

1. Run:

   ```bash
   curl http://localhost:8000/health
   ```

**Result**

`{"status": "ok"}`

## Macro rejection

**Use case**

You need assurance that uploaded files do not carry macros.

**Before you begin**

* Have a `.docm` file.

**Steps**

1. Run:

   ```bash
   curl -F template=@file.docm \
        -F worksheet=@worksheet.docx \
        http://localhost:8000/generate
   ```

**Result**

The API responds with an error and no file is kept on disk.
