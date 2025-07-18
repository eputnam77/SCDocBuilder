"""IO helpers for loading and saving Word documents."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def validate_input_files(template: Path, worksheet: Path) -> None:
    """Validate input files exist and are under size limits (stub)."""
    raise NotImplementedError("Input validation not implemented yet")


def load_document(path: Path) -> Any:
    """Load a Word document from ``path`` (stub)."""
    raise NotImplementedError("Document loading not implemented yet")


def save_document(doc: Any, path: Path) -> None:
    """Save a Word document to ``path`` (stub)."""
    raise NotImplementedError("Document saving not implemented yet")
