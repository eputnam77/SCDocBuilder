import pytest
from hypothesis import given

from pathlib import Path

from faa_sc_replacer.io import validate_input_files
from tests.property.strategies import docx_path


@pytest.mark.property
@given(template=docx_path(), worksheet=docx_path())
def test_validate_input_files_not_implemented(template: Path, worksheet: Path) -> None:
    """validate_input_files should eventually accept valid paths."""
    with pytest.raises(NotImplementedError):
        validate_input_files(template, worksheet)
