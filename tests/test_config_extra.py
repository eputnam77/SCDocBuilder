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


def test_load_placeholder_schema_accepts_str_path(tmp_path: Path) -> None:
    path = tmp_path / "schema.json"
    path.write_text('{"A": "{a}"}')
    assert config.load_placeholder_schema(str(path)) == {"A": "{a}"}


def test_parse_simple_yaml_inline_comment() -> None:
    text = (
        "A: B # trailing" "\n# full-line\nC: 'D # not comment'"
    )  # comment inside quotes
    result = config._parse_simple_yaml(text)
    assert result == {"A": "B", "C": "D # not comment"}


def test_parse_simple_yaml_comment_after_quotes() -> None:
    text = "A: 'B' # trailing comment\nB: \"C\" # another"
    result = config._parse_simple_yaml(text)
    assert result == {"A": "B", "B": "C"}


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


def test_load_placeholder_schema_requires_mapping(tmp_path: Path) -> None:
    path = tmp_path / "schema.json"
    path.write_text("[1, 2, 3]")
    with pytest.raises(ValueError):
        config.load_placeholder_schema(path)


def test_load_placeholder_schema_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{invalid}")
    with pytest.raises(ValueError):
        config.load_placeholder_schema(path)


def test_load_placeholder_schema_invalid_yaml(tmp_path: Path) -> None:
    path = tmp_path / "bad.yml"
    path.write_text("A: [1,")
    with pytest.raises(ValueError):
        config.load_placeholder_schema(path)


def test_load_placeholder_schema_yaml_non_mapping(tmp_path: Path) -> None:
    path = tmp_path / "list.yml"
    path.write_text("- a\n- b")
    with pytest.raises(ValueError):
        config.load_placeholder_schema(path)


def test_parse_simple_yaml_unclosed_quote() -> None:
    with pytest.raises(ValueError):
        config._parse_simple_yaml("A: 'B")


def test_parse_simple_yaml_trailing_garbage_after_quotes() -> None:
    """Quoted values may only be followed by whitespace or comments."""
    with pytest.raises(ValueError):
        config._parse_simple_yaml("A: 'B' C")


def test_parse_simple_yaml_empty_value() -> None:
    assert config._parse_simple_yaml("A:") == {"A": ""}


def test_parse_simple_yaml_rejects_empty_keys() -> None:
    with pytest.raises(ValueError):
        config._parse_simple_yaml(": value")


def test_load_placeholder_schema_yaml_fallback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    yml = tmp_path / "f.yml"
    yml.write_text("A: B")
    orig_import = __import__

    def fake_import(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "yaml":
            raise ModuleNotFoundError
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    assert config.load_placeholder_schema(yml) == {"A": "B"}


def test_parse_simple_yaml_hash_in_value() -> None:
    text = "A: value#1"
    assert config._parse_simple_yaml(text) == {"A": "value#1"}


def test_parse_simple_yaml_allows_brackets_in_quotes() -> None:
    """Quoted values may legitimately contain unmatched brackets."""
    text = "A: '[1,'"
    assert config._parse_simple_yaml(text) == {"A": "[1,"}


def test_parse_simple_yaml_rejects_misordered_brackets() -> None:
    """Misordered brackets in unquoted values should be rejected."""
    text = "A: ]1["
    with pytest.raises(ValueError):
        config._parse_simple_yaml(text)


def test_load_placeholder_schema_reloads_on_change(tmp_path: Path) -> None:
    path = tmp_path / "schema.json"
    path.write_text('{"A": "x"}')
    assert config.load_placeholder_schema(path) == {"A": "x"}
    path.write_text('{"A": "y"}')
    assert config.load_placeholder_schema(path) == {"A": "y"}
