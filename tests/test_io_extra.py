from pathlib import Path
import typing
import pytest

if not typing.TYPE_CHECKING:
    pytest.importorskip("docx")
from docx import Document

from scdocbuilder.io import load_document, save_document, validate_input_files


def test_load_document_and_save(tmp_path: Path) -> None:
    path = tmp_path / "doc.docx"
    Document().save(str(path))
    doc = load_document(path)
    out = tmp_path / "out.docx"
    save_document(doc, out)
    assert out.exists()

    with pytest.raises(ValueError):
        save_document(doc, tmp_path / "bad.txt")


def test_validate_input_files_rejects_wrong_mime(tmp_path: Path) -> None:
    bogus = tmp_path / "fake.docx"
    bogus.write_text("not a real docx")
    with pytest.raises(ValueError):
        validate_input_files(bogus, bogus)


def test_validate_input_files_rejects_directories(tmp_path: Path) -> None:
    """Directories masquerading as files should be rejected."""
    directory = tmp_path / "dir.docx"
    directory.mkdir()
    with pytest.raises(FileNotFoundError):
        validate_input_files(directory, directory)
