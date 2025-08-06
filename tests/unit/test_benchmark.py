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
    """Create a DOCX file roughly ``size_kb`` kilobytes in size."""
    doc = Document()
    chunk = "X" * 1024  # ~1 KB per paragraph
    for _ in range(size_kb):
        doc.add_paragraph(chunk)
    doc.save(str(path))


def test_benchmark_under_one_second(tmp_path: Path) -> None:
    template = tmp_path / "t.docx"
    worksheet = tmp_path / "w.docx"
    _make_doc(template, 500)  # 500 KB
    _make_doc(worksheet, 1024)  # 1 MB

    duration = benchmark_processing(template, worksheet)

    assert duration < 1.0
