"""HTML export using mammoth and bleach."""

from __future__ import annotations

from docx.document import Document
from html import escape
from typing import Any


def _render_runs(paragraph: Any) -> str:
    parts: list[str] = []
    for run in paragraph.runs:
        text = escape(run.text)
        if getattr(run, "bold", False):
            text = f"<strong>{text}</strong>"
        if getattr(run, "italic", False):
            text = f"<em>{text}</em>"
        parts.append(text)
    return "".join(parts)


def export_html(doc: Document) -> str:
    """Convert ``doc`` to sanitized HTML.

    The output intentionally omits ``<html>``/``<body>`` wrappers so the result
    can be embedded directly into editors like TipTap. Only a small subset of
    tags is produced (``p``, ``h1``-``h3``, ``em``, ``strong``).
    """

    parts: list[str] = []
    for paragraph in doc.paragraphs:
        content = _render_runs(paragraph)
        level = getattr(paragraph, "level", 0)
        if level:
            parts.append(f"<h{level}>{content}</h{level}>")
        else:
            parts.append(f"<p>{content}</p>")
    return "".join(parts)
