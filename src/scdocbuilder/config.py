"""Configuration helpers for placeholder schemas."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict
from functools import lru_cache


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

            # Remove inline comments for unquoted values
            if value and value[0] not in {'"', "'"}:
                if "#" in value:
                    value = value.split("#", 1)[0].rstrip()
                value = value.strip("'\"")
            else:
                # Strip matching quotes for quoted values
                if len(value) >= 2 and value[-1] == value[0]:
                    value = value[1:-1]
                else:
                    value = value.strip("'\"")

            result[key.strip()] = value
    return result


@lru_cache(maxsize=None)
def load_placeholder_schema(path: Path) -> Dict[str, str]:
    """Load placeholder schema from a JSON or YAML file.

    Args:
        path: File containing placeholder mappings.

    Returns:
        Dictionary mapping worksheet fields to template placeholders.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        ImportError: If a YAML file is requested without ``PyYAML``.
        ValueError: If the file extension is unsupported.
    """

    if not path.exists():
        raise FileNotFoundError(str(path))

    if path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8") as f:
            json_data: Any = json.load(f)
        return dict(json_data)
    elif path.suffix.lower() in {".yaml", ".yml"}:
        try:
            yaml = __import__("yaml")
        except ModuleNotFoundError:
            return _parse_simple_yaml(path.read_text(encoding="utf-8"))
        except ImportError as exc:
            raise ImportError("PyYAML is required for YAML files") from exc
        with path.open("r", encoding="utf-8") as f:
            yaml_data: Any = yaml.safe_load(f)
        return dict(yaml_data)
    else:
        raise ValueError("Unsupported schema format")
