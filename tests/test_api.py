from pathlib import Path
from docx import Document

from faa_sc_replacer import fill_template


def test_fill_template_writes_output(tmp_path: Path) -> None:
    template = tmp_path / "t.docx"
    worksheet = tmp_path / "w.docx"

    doc = Document()
    doc.add_paragraph("{Applicant name}")
    doc.save(str(template))
    ws_doc = Document()
    ws_doc.add_paragraph("Applicant name: Foo")
    ws_doc.save(str(worksheet))

    output = tmp_path / "out.docx"
    result = fill_template(template, worksheet, output)

    assert result == output
    processed = Document(str(output))
    assert "Foo" in processed.paragraphs[0].text
