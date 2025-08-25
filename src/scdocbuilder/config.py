"""Configuration helpers for placeholder schemas."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def _parse_simple_yaml(text: str) -> Dict[str, str]:
    """Parse a very small subset of YAML used in tests.

    Supports ``key: value`` pairs with optional quotes around the value. It is
    **not** a general YAML parser but avoids a heavy dependency when PyYAML is
    unavailable.
    """

    result: Dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()

            quoted = bool(value and value[0] in {'"', "'"})
            # Remove inline comments for unquoted values.  YAML only treats "#"
            # as a comment start when it is preceded by whitespace.  The previous
            # implementation discarded everything after the first "#" regardless
            # of context which meant values like ``url#fragment`` were truncated.
            # Honour the whitespace rule to keep hashes that are part of the
            # actual value.
            if not quoted:
                hash_idx = value.find("#")
                if hash_idx != -1 and (hash_idx == 0 or value[hash_idx - 1].isspace()):
                    value = value[:hash_idx].rstrip()
                value = value.strip("'\"")
            else:
                quote = value[0]
                end = value.find(quote, 1)
                if end != -1:
                    raw = value[1:end]
                    trailing = value[end + 1 :].lstrip()
                    if trailing.startswith("#") or not trailing:
                        value = raw
                    else:
                        # Any non-comment content after a quoted value is
                        # invalid YAML.  The previous implementation
                        # silently concatenated the trailing text which
                        # produced surprising results such as
                        # ``A: "B"C`` parsing to ``BC``.  Treat these cases
                        # as errors instead.
                        raise ValueError("Trailing characters after quoted YAML value")
                else:
                    raise ValueError("Unclosed quote in YAML value")

            # Basic sanity check: if the value contains unmatched brackets or
            # braces (e.g. ``[1,``) treat it as invalid YAML.  The previous
            # implementation silently accepted such tokens, leading to confusing
            # behaviour when malformed files were provided.  Quoted values are
            # exempt because their bracket characters are literal.
            if not quoted:
                for open_b, close_b in (("[", "]"), ("{", "}"), ("(", ")")):
                    if value.count(open_b) != value.count(close_b):
                        raise ValueError("Unbalanced brackets in YAML value")

            result[key.strip()] = value
        else:
            # Any non-comment, non-empty line without a colon indicates the file
            # is not a simple key/value mapping.  Reject it to mirror YAML's
            # behaviour instead of silently ignoring data.
            raise ValueError("Schema must be a mapping")
    return result


def load_placeholder_schema(path: Path | str) -> Dict[str, str]:
    """Load placeholder schema from a JSON or YAML file.

    Args:
        path: File containing placeholder mappings.

    Returns:
        Dictionary mapping worksheet fields to template placeholders.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        ImportError: If a YAML file is requested without ``PyYAML``.
        ValueError: If the file extension is unsupported or the file content is invalid.
    """

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(str(path))

    suffix = path.suffix.lower()
    if suffix == ".json":
        try:
            with path.open("r", encoding="utf-8") as f:
                json_data: Any = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON schema") from exc
        if not isinstance(json_data, dict):
            raise ValueError("Schema must be a mapping")
        return dict(json_data)

    if suffix in {".yaml", ".yml"}:
        try:
            yaml = __import__("yaml")
        except ModuleNotFoundError:
            return _parse_simple_yaml(path.read_text(encoding="utf-8"))
        except ImportError as exc:
            raise ImportError("PyYAML is required for YAML files") from exc
        try:
            with path.open("r", encoding="utf-8") as f:
                yaml_data: Any = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            raise ValueError("Invalid YAML schema") from exc
        if not isinstance(yaml_data, dict):
            raise ValueError("Schema must be a mapping")
        return dict(yaml_data)

    raise ValueError("Unsupported schema format")
