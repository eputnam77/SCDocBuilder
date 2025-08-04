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


def test_export_html_strips_script_tags() -> None:
    doc = Document()
    doc.add_paragraph("<script>alert('x')</script>")
    html = export_html(doc)
    assert "<script" not in html


@pytest.mark.xfail(reason="Heading tags not implemented")
def test_export_html_produces_heading_tags() -> None:
    doc = Document()
    doc.add_heading("Title", level=1)
    html = export_html(doc)
    assert "<h1>Title</h1>" in html
