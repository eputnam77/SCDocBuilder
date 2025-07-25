"""HTML export using mammoth and bleach."""

from __future__ import annotations

from docx.document import Document
from html import escape


def export_html(doc: Document) -> str:
    """Convert ``doc`` to sanitized HTML string."""

    parts = ["<html><body>"]
    for paragraph in doc.paragraphs:
        parts.append(f"<p>{escape(paragraph.text)}</p>")
    parts.append("</body></html>")
    return "".join(parts)
