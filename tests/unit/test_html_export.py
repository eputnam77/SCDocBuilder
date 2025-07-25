import typing
import pytest

if typing.TYPE_CHECKING:
    from docx import Document
else:
    pytest.importorskip("docx")
    from docx import Document

from scdocbuilder.html_export import export_html


def test_export_html_returns_string() -> None:
    doc = Document()
    doc.add_paragraph("Hello")

    html = export_html(doc)

    assert "<p" in html
