from pathlib import Path

import pytest

from faa_sc_replacer.security import cleanup_uploads, reject_macros


def test_reject_macros_raises(tmp_path: Path) -> None:
    path = tmp_path / "malicious.docm"
    path.write_bytes(b"dummy")
    with pytest.raises(ValueError):
        reject_macros(path)


def test_cleanup_uploads_removes_files(tmp_path: Path) -> None:
    path = tmp_path / "temp.docx"
    path.write_bytes(b"data")
    cleanup_uploads(path)
    assert not path.exists()
