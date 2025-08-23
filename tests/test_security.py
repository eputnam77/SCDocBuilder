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


def test_reject_macros_dotm_extension(tmp_path: Path) -> None:
    """Macro-enabled .dotm template files should be rejected."""
    path = tmp_path / "file.dotm"
    path.write_bytes(b"\0")
    with pytest.raises(ValueError):
        reject_macros(path)


def test_reject_macros_signature(tmp_path: Path) -> None:
    """DOCX containing macro signatures should be rejected."""
    path = tmp_path / "file.docx"
    path.write_bytes(b"vbaProject")
    with pytest.raises(ValueError):
        reject_macros(path)


def test_reject_macros_signature_case_insensitive(tmp_path: Path) -> None:
    path = tmp_path / "file.docx"
    path.write_bytes(b"VBAPROJECT")
    with pytest.raises(ValueError):
        reject_macros(path)


def test_reject_macros_missing_file(tmp_path: Path) -> None:
    """Missing files should raise ``FileNotFoundError`` even for .docm."""
    path = tmp_path / "missing.docm"
    with pytest.raises(FileNotFoundError):
        reject_macros(path)


def test_reject_macros_scans_entire_file(tmp_path: Path) -> None:
    """Macro signatures after the initial chunk should still be detected."""
    path = tmp_path / "late.docx"
    path.write_bytes(b"A" * 5000 + b"vbaProject")
    with pytest.raises(ValueError):
        reject_macros(path)
