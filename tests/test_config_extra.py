from typing import Any
import builtins
from pathlib import Path
import typing
import pytest

if not typing.TYPE_CHECKING:
    pytest.importorskip("docx")

from scdocbuilder import config


def test_load_placeholder_schema_yaml(tmp_path: Path) -> None:
    path = tmp_path / "schema.yaml"
    path.write_text("A: '{a}'\n")
    assert config.load_placeholder_schema(path) == {"A": "{a}"}


def test_load_placeholder_schema_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    missing = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        config.load_placeholder_schema(missing)

    txt = tmp_path / "schema.txt"
    txt.write_text("noop")
    with pytest.raises(ValueError):
        config.load_placeholder_schema(txt)

    yml = tmp_path / "schema.yml"
    yml.write_text("A: B")

    def fake_import(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "yaml":
            raise ImportError
        return orig_import(name, *args, **kwargs)

    orig_import = __import__
    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(ImportError):
        config.load_placeholder_schema(yml)
