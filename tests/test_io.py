import pytest

from pathlib import Path


def test_validate_input_files_placeholder(tmp_path: Path) -> None:
    """Validation logic must ensure files exist and are <10MB."""
    pytest.fail("validate_input_files not implemented yet")
