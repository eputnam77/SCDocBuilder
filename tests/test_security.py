"""Tests for security utilities."""

from pathlib import Path

import pytest

from scdocbuilder.security import reject_macros, cleanup_uploads


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


def test_reject_macros_rejects_directory(tmp_path: Path) -> None:
    """Directories should be treated like missing files."""
    directory = tmp_path / "dir.docx"
    directory.mkdir()
    with pytest.raises(FileNotFoundError):
        reject_macros(directory)


def test_reject_macros_scans_entire_file(tmp_path: Path) -> None:
    """Macro signatures after the initial chunk should still be detected."""
    path = tmp_path / "late.docx"
    path.write_bytes(b"A" * 5000 + b"vbaProject")
    with pytest.raises(ValueError):
        reject_macros(path)


def test_cleanup_uploads_ignores_missing_and_dirs(tmp_path: Path) -> None:
    missing = tmp_path / "missing.docx"
    directory = tmp_path / "dir"
    directory.mkdir()
    cleanup_uploads(missing, directory)
    assert directory.exists()


def test_cleanup_uploads_handles_permission_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    file_path = tmp_path / "file.docx"
    file_path.write_text("x")

    def fake_unlink(self: Path) -> None:
        raise PermissionError

    monkeypatch.setattr(Path, "unlink", fake_unlink)
    # Should not raise even if unlink reports a permission problem
    cleanup_uploads(file_path)


def test_cleanup_uploads_handles_generic_oserror(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Unexpected OS errors should be ignored during cleanup."""
    file_path = tmp_path / "file.docx"
    file_path.write_text("x")

    def fake_unlink(self: Path) -> None:
        raise OSError("boom")

    monkeypatch.setattr(Path, "unlink", fake_unlink)
    # Should not raise even if a generic OSError occurs
    cleanup_uploads(file_path)
