"""Configuration helpers for placeholder schemas."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


def load_placeholder_schema(path: Path) -> Dict[str, str]:
    """Load placeholder schema from a JSON or YAML file."""

    if not path.exists():
        raise FileNotFoundError(str(path))

    if path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    elif path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except Exception as exc:  # pragma: no cover - optional dependency
            raise ImportError("PyYAML is required for YAML files") from exc
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        raise ValueError("Unsupported schema format")
