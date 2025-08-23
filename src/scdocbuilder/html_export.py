"""HTML export using mammoth and bleach."""

from __future__ import annotations

from docx.document import Document
from html import escape
from io import BytesIO
from typing import Any
import re


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


def _heading_level(paragraph: Any) -> int:
    """Return heading level for ``paragraph`` if styled as a heading."""

    style = getattr(paragraph, "style", None)
    if not style:
        return 0

    candidates = [getattr(style, "name", ""), getattr(style, "style_id", "")]
    for cand in candidates:
        match = re.search(
            r"h(?:eading)?\s*([1-6])(?!\d)", str(cand), flags=re.IGNORECASE
        )
        if match:
            return int(match.group(1))
    return 0


def export_html(doc: Document) -> str:
    """Convert ``doc`` to sanitized HTML.

    When the optional :mod:`mammoth` and :mod:`bleach` dependencies are
    installed, they are used to perform the DOCX→HTML conversion and sanitise
    the result. This provides better formatting fidelity and XSS protection.
    If the libraries are unavailable a very small fallback renderer is used
    instead. The returned string intentionally omits ``<html>``/``<body>``
    wrappers so it can be embedded directly into editors like TipTap.
    """

    try:
        import mammoth
        import bleach
    except Exception:
        parts: list[str] = []
        for paragraph in doc.paragraphs:
            content = _render_runs(paragraph)
            level = _heading_level(paragraph)
            if level:
                parts.append(f"<h{level}>{content}</h{level}>")
            else:
                parts.append(f"<p>{content}</p>")
        return "".join(parts)

    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    result = mammoth.convert_to_html(buf)
    allowed = [
        "p",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "ul",
        "ol",
        "li",
        "em",
        "strong",
        "a",
    ]
    from typing import cast

    return cast(str, bleach.clean(result.value, tags=allowed, strip=True))
