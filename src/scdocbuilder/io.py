"""IO helpers for loading and saving Word documents."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from docx import Document

MAX_SIZE = 10 * 1024 * 1024  # 10 MB
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def validate_input_files(template: Path, worksheet: Path) -> None:
    """Validate that ``template`` and ``worksheet`` are DOCX files.

    Args:
        template: Path to the template document.
        worksheet: Path to the worksheet document.

    Raises:
        FileNotFoundError: If any file is missing.
        ValueError: If a file is not ``.docx`` or exceeds ``MAX_SIZE`` bytes.
    """

    for file in (template, worksheet):
        if not file.exists():
            raise FileNotFoundError(str(file))
        if file.suffix.lower() != ".docx":
            raise ValueError(f"{file} is not a .docx file")
        if file.stat().st_size > MAX_SIZE:
            raise ValueError(f"{file} exceeds size limit")
        with file.open("rb") as fh:
            head = fh.read(2048)
            if head[:2] != b"PK":
                raise ValueError(f"{file} is not a valid docx file")
            try:
                import magic

                mime = magic.from_buffer(head, mime=True)
            except (ImportError, AttributeError):
                pass
            else:
                if mime != DOCX_MIME:
                    raise ValueError(f"{file} has MIME {mime}")


def load_document(path: Path) -> Any:
    """Load a Word document from ``path``.

    The file is first validated using :func:`validate_input_files` to ensure it
    looks like a real DOCX archive. The returned object is the
    :class:`python-docx` ``Document`` instance loaded from ``path``.
    """

    validate_input_files(path, path)
    return Document(str(path))


def save_document(doc: Any, path: Path) -> None:
    """Persist ``doc`` to ``path``.

    Args:
        doc: Document to write.
        path: Destination filename ending with ``.docx``.

    Raises:
        ValueError: If ``path`` does not end with ``.docx``.
    """

    if path.suffix.lower() != ".docx":
        raise ValueError("Output path must be .docx")
    doc.save(str(path))
