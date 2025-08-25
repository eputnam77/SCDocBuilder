"""FastAPI application exposing document generation endpoints."""

from __future__ import annotations

import tempfile
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

from . import fill_template
from .io import load_document
from .html_export import export_html
from .security import reject_macros, cleanup_uploads

OUTPUT_DIR = Path(tempfile.gettempdir()) / "faa_sc_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()

app.mount("/files", StaticFiles(directory=str(OUTPUT_DIR)), name="files")


def index() -> HTMLResponse:
    """Serve a simple upload form."""
    return HTMLResponse(
        """
        <html lang='en'>
        <body>
        <form action='/web-generate' method='post' enctype='multipart/form-data'>
            <label for='template'>Template:</label>
            <input id='template' type='file' name='template' aria-label='Template DOCX'><br>
            <label for='worksheet'>Worksheet:</label>
            <input id='worksheet' type='file' name='worksheet' aria-label='Worksheet DOCX'><br>
            <button type='submit'>Generate</button>
        </form>
        </body>
        </html>
        """
    )


async def web_generate(template: UploadFile, worksheet: UploadFile) -> HTMLResponse:
    """Process files uploaded via the HTML form.

    Args:
        template: DOCX template file.
        worksheet: DOCX worksheet file.

    Returns:
        HTML page with a download link for the generated document.
    """
    template_path = OUTPUT_DIR / f"{uuid4().hex}_template.docx"
    worksheet_path = OUTPUT_DIR / f"{uuid4().hex}_worksheet.docx"
    template_path.write_bytes(await template.read())
    worksheet_path.write_bytes(await worksheet.read())
    reject_macros(template_path)
    reject_macros(worksheet_path)
    output = fill_template(template_path, worksheet_path)
    href = f"/files/{output.name}"
    cleanup_uploads(template_path, worksheet_path)
    return HTMLResponse(f"<a href='{href}'>Download result</a>")


async def generate(
    template: UploadFile, worksheet: UploadFile, html: bool = False
) -> Response:
    """Generate DOCX or HTML from uploaded files.

    Args:
        template: DOCX template file.
        worksheet: DOCX worksheet file.
        html: When ``True`` return sanitized HTML instead of DOCX.

    Returns:
        FileResponse with DOCX or HTMLResponse.
    """
    template_path = OUTPUT_DIR / f"{uuid4().hex}_template.docx"
    worksheet_path = OUTPUT_DIR / f"{uuid4().hex}_worksheet.docx"
    template_path.write_bytes(await template.read())
    worksheet_path.write_bytes(await worksheet.read())
    reject_macros(template_path)
    reject_macros(worksheet_path)
    output = fill_template(template_path, worksheet_path)
    if html:
        doc = load_document(output)
        html_str = export_html(doc)
        cleanup_uploads(template_path, worksheet_path, output)
        return HTMLResponse(html_str)
    cleanup_uploads(template_path, worksheet_path)
    return FileResponse(output, filename=output.name)


def health() -> dict[str, str]:
    """Return service status."""
    return {"status": "ok"}


app.get("/", response_class=HTMLResponse)(index)
app.post("/web-generate", response_class=HTMLResponse)(web_generate)
app.post("/generate")(generate)
app.get("/health")(health)
