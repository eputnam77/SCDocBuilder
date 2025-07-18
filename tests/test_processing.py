from pathlib import Path
from docx import Document

from faa_sc_replacer.processing import (
    extract_fields,
    replace_placeholders,
    apply_conditionals,
)


def _make_template(path: Path) -> None:
    doc = Document()
    doc.add_paragraph("Hello {name}")
    doc.save(str(path))


def test_extract_fields() -> None:
    doc = Document()
    doc.add_paragraph("Applicant name: Foo")
    fields = extract_fields(doc)
    assert fields["{Applicant name}"] == "Foo"


def test_replace_placeholders(tmp_path: Path) -> None:
    path = tmp_path / "t.docx"
    _make_template(path)
    doc = Document(str(path))
    replace_placeholders(doc, {"{name}": "Bar"})
    assert "Bar" in doc.paragraphs[0].text


def test_apply_conditionals() -> None:
    doc = Document()
    doc.add_paragraph("[[OPTION_1]]Yes[[/OPTION_1]][[OPTION_2]]No[[/OPTION_2]]")
    apply_conditionals(doc, {"{Action option}": "1"})
    assert doc.paragraphs[0].text == "Yes"


def test_apply_conditionals_across_runs() -> None:
    doc = Document()
    para = doc.add_paragraph()
    para.add_run("[[OPTION_1]]Yes")
    para.add_run("[[/OPTION_1]]")
    para.add_run("[[OPTION_2]]No[[/OPTION_2]]")
    apply_conditionals(doc, {"{Action option}": "1"})
    assert doc.paragraphs[0].text == "Yes"
