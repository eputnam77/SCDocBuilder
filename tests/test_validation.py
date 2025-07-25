from pathlib import Path
import typing
import pytest

if typing.TYPE_CHECKING:
    from docx import Document
else:
    pytest.importorskip("docx")
    from docx import Document

from scdocbuilder import fill_template


def _make_template(path: Path) -> None:
    doc = Document()
    doc.add_paragraph("{Applicant name} {Airplane model}")
    doc.save(str(path))


def test_missing_question_15_raises(tmp_path: Path) -> None:
    template = tmp_path / "t.docx"
    worksheet = tmp_path / "w.docx"
    _make_template(template)

    ws = Document()
    ws.add_paragraph("Applicant name: Foo")
    ws.add_paragraph("Airplane model: Bar")
    # Question 15 prompt without answer
    ws.add_paragraph("Question 15:")
    ws.save(str(worksheet))

    with pytest.raises(ValueError):
        fill_template(template, worksheet, tmp_path / "out.docx")
