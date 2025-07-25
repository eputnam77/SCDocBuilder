from pathlib import Path
import typing
import pytest

if not typing.TYPE_CHECKING:
    pytest.importorskip("docx")

from scdocbuilder.config import load_placeholder_schema


def test_load_placeholder_schema(tmp_path: Path) -> None:
    data = {"A": "{a}"}
    path = tmp_path / "schema.json"
    path.write_text('{"A": "{a}"}')

    result = load_placeholder_schema(path)
    assert result == data
