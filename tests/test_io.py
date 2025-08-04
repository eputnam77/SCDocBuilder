import pytest
import typing
from pathlib import Path

if not typing.TYPE_CHECKING:
    pytest.importorskip("docx")

from scdocbuilder.io import validate_input_files


def test_validate_input_files(tmp_path: Path) -> None:
    """validate_input_files should raise for bad paths and succeed for good."""
    t = tmp_path / "t.docx"
    w = tmp_path / "w.docx"
    t.write_bytes(b"\0")
    w.write_bytes(b"\0")

    validate_input_files(t, w)

    with pytest.raises(FileNotFoundError):
        validate_input_files(t, tmp_path / "missing.docx")


def test_validate_input_files_rejects_non_docx(tmp_path: Path) -> None:
    """Non-.docx inputs should raise ValueError."""
    t = tmp_path / "t.txt"
    w = tmp_path / "w.docx"
    t.write_bytes(b"\0")
    w.write_bytes(b"\0")
    with pytest.raises(ValueError):
        validate_input_files(t, w)


def test_validate_input_files_rejects_large_file(tmp_path: Path) -> None:
    """Files exceeding the size limit should be rejected."""
    big = tmp_path / "big.docx"
    big.write_bytes(b"0" * (11 * 1024 * 1024))
    with pytest.raises(ValueError):
        validate_input_files(big, big)
