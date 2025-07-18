"""IO helpers for loading and saving Word documents."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from docx import Document

MAX_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_input_files(template: Path, worksheet: Path) -> None:
    """Validate that the provided files exist, are DOCX files and <10MB."""

    for file in (template, worksheet):
        if not file.exists():
            raise FileNotFoundError(str(file))
        if file.suffix.lower() != ".docx":
            raise ValueError(f"{file} is not a .docx file")
        if file.stat().st_size > MAX_SIZE:
            raise ValueError(f"{file} exceeds size limit")


def load_document(path: Path) -> Any:
    """Load a Word document from ``path`` using ``python-docx``."""

    validate_input_files(path, path)  # same file for both params to reuse checks
    return Document(str(path))


def save_document(doc: Any, path: Path) -> None:
    """Persist ``doc`` to ``path``."""

    if path.suffix.lower() != ".docx":
        raise ValueError("Output path must be .docx")
    doc.save(str(path))
