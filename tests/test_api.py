from pathlib import Path
from docx import Document

from faa_sc_replacer import fill_template


def test_fill_template_writes_output(tmp_path: Path) -> None:
    template = tmp_path / "t.docx"
    worksheet = tmp_path / "w.docx"

    doc = Document()
    doc.add_paragraph("{Applicant name} {Airplane model}")
    doc.save(str(template))
    ws_doc = Document()
    ws_doc.add_paragraph("Applicant name: Foo")
    ws_doc.add_paragraph("Airplane model: Bar")
    ws_doc.add_paragraph("Question 15:")
    ws_doc.add_paragraph("Ans15")
    ws_doc.add_paragraph("Question 16:")
    ws_doc.add_paragraph("Ans16")
    ws_doc.add_paragraph("Question 17:")
    ws_doc.add_paragraph("Ans17")
    ws_doc.save(str(worksheet))

    output = tmp_path / "out.docx"
    result = fill_template(template, worksheet, output)

    assert result == output
    processed = Document(str(output))
    assert "Foo" in processed.paragraphs[0].text
