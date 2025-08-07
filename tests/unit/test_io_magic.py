from pathlib import Path
import sys

import pytest

from scdocbuilder.io import validate_input_files, DOCX_MIME


def test_validate_input_files_magic(monkeypatch, tmp_path: Path) -> None:
    path = tmp_path / "a.docx"
    path.write_bytes(b"PK\x00\x00")

    class BadMagic:
        @staticmethod
        def from_buffer(data, mime=True):  # type: ignore[unused-argument]
            return "text/plain"

    monkeypatch.setitem(sys.modules, "magic", BadMagic)
    with pytest.raises(ValueError):
        validate_input_files(path, path)

    class GoodMagic:
        @staticmethod
        def from_buffer(data, mime=True):  # type: ignore[unused-argument]
            return DOCX_MIME

    monkeypatch.setitem(sys.modules, "magic", GoodMagic)
    validate_input_files(path, path)
