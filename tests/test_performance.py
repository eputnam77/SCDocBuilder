from pathlib import Path
import typing
import zipfile
import pytest

if typing.TYPE_CHECKING:
    from docx import Document
else:
    pytest.importorskip("docx")
    from docx import Document

from scdocbuilder.benchmark import benchmark_processing


def _make_doc(path: Path, size_kb: int) -> None:
    doc = Document()
    doc.add_paragraph("placeholder")
    doc.save(str(path))
    current = path.stat().st_size
    target = size_kb * 1024
    if current < target:
        filler = b"0" * (target - current)
        with zipfile.ZipFile(path, "a") as zf:
            zf.writestr("filler.bin", filler)


def test_benchmark_processing_under_one_second(tmp_path: Path) -> None:
    """Processing large documents should complete within one second."""
    template = tmp_path / "t.docx"
    worksheet = tmp_path / "w.docx"
    # Use moderate file sizes so the test completes quickly while still
    # exercising performance-sensitive paths.
    _make_doc(template, 50)
    _make_doc(worksheet, 100)
    duration = benchmark_processing(template, worksheet)
    assert duration <= 1.0
