from pathlib import Path
import typing
import pytest

if typing.TYPE_CHECKING:
    from docx import Document
else:
    pytest.importorskip("docx")
    from docx import Document

from scdocbuilder.benchmark import benchmark_processing


def _make_doc(path: Path, size_kb: int) -> None:
    doc = Document()
    text = "X" * 1000
    while True:
        doc.add_paragraph(text)
        doc.save(str(path))
        if path.stat().st_size >= size_kb * 1024:
            break


def test_benchmark_processing_under_one_second(tmp_path: Path) -> None:
    """Processing large documents should complete within one second."""
    template = tmp_path / "t.docx"
    worksheet = tmp_path / "w.docx"
    _make_doc(template, 500)
    _make_doc(worksheet, 1000)
    duration = benchmark_processing(template, worksheet)
    assert duration <= 1.0
