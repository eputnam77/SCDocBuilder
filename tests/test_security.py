"""Tests for security utilities."""

from pathlib import Path

import pytest

from scdocbuilder.security import reject_macros


def test_reject_macros_docm_extension(tmp_path: Path) -> None:
    """Macro-enabled .docm files should be rejected."""
    path = tmp_path / "file.docm"
    path.write_bytes(b"\0")
    with pytest.raises(ValueError):
        reject_macros(path)


def test_reject_macros_signature(tmp_path: Path) -> None:
    """DOCX containing macro signatures should be rejected."""
    path = tmp_path / "file.docx"
    path.write_bytes(b"vbaProject")
    with pytest.raises(ValueError):
        reject_macros(path)
