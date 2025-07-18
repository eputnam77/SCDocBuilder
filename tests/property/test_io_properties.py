import pytest
pytest.importorskip("hypothesis")
from hypothesis import given

from pathlib import Path

from faa_sc_replacer.io import validate_input_files
from tests.property.strategies import docx_path


@pytest.mark.property
@given(template=docx_path(), worksheet=docx_path())
def test_validate_input_files_accepts_paths(tmp_path: Path, template: Path, worksheet: Path) -> None:
    """validate_input_files should accept existing DOCX files."""

    t = tmp_path / template.name
    w = tmp_path / worksheet.name
    t.write_bytes(b"\0")
    w.write_bytes(b"\0")

    validate_input_files(t, w)

    with pytest.raises(FileNotFoundError):
        validate_input_files(t, tmp_path / "missing.docx")
