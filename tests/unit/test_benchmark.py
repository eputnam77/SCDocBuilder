from pathlib import Path
import typing
import pytest

if typing.TYPE_CHECKING:
    from docx import Document
else:
    pytest.importorskip("docx")
    from docx import Document

from faa_sc_replacer.benchmark import benchmark_processing


def test_benchmark_under_one_second(tmp_path: Path) -> None:
    template = tmp_path / "t.docx"
    worksheet = tmp_path / "w.docx"
    Document().save(str(template))
    Document().save(str(worksheet))

    duration = benchmark_processing(template, worksheet)

    assert duration < 1.0
