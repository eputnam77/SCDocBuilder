"""HTML export using mammoth and bleach."""

from __future__ import annotations

from docx.document import Document
from html import escape


def export_html(doc: Document) -> str:
    """Convert ``doc`` to sanitized HTML.

    Args:
        doc: Document to convert.

    Returns:
        HTML string safe for embedding in editors like TipTap.

    Example:
        >>> html = export_html(doc)
        >>> html.startswith("<html>")
        True
    """

    parts = ["<html><body>"]
    for paragraph in doc.paragraphs:
        parts.append(f"<p>{escape(paragraph.text)}</p>")
    parts.append("</body></html>")
    return "".join(parts)
