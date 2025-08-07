"""Configuration helpers for placeholder schemas."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any
from functools import lru_cache


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
            import yaml  # type: ignore
        except Exception as exc:  # pragma: no cover - optional dependency
            raise ImportError("PyYAML is required for YAML files") from exc
        with path.open("r", encoding="utf-8") as f:
            yaml_data: Any = yaml.safe_load(f)
        return dict(yaml_data)
    else:
        raise ValueError("Unsupported schema format")
