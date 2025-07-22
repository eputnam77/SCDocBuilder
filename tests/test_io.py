import pytest
import typing
from pathlib import Path

if not typing.TYPE_CHECKING:
    pytest.importorskip("docx")

from faa_sc_replacer.io import validate_input_files


def test_validate_input_files(tmp_path: Path) -> None:
    """validate_input_files should raise for bad paths and succeed for good."""
    t = tmp_path / "t.docx"
    w = tmp_path / "w.docx"
    t.write_bytes(b"\0")
    w.write_bytes(b"\0")

    validate_input_files(t, w)

    with pytest.raises(FileNotFoundError):
        validate_input_files(t, tmp_path / "missing.docx")
