from pathlib import Path
import pytest
from docx import Document

from faa_sc_replacer.io import load_document, save_document


def test_load_document_and_save(tmp_path: Path) -> None:
    path = tmp_path / "doc.docx"
    Document().save(str(path))
    doc = load_document(path)
    out = tmp_path / "out.docx"
    save_document(doc, out)
    assert out.exists()

    with pytest.raises(ValueError):
        save_document(doc, tmp_path / "bad.txt")
