"""Security utilities for uploads."""

from __future__ import annotations

from pathlib import Path

MACRO_PATTERNS = [b"vbaproject", b"macros"]


def reject_macros(path: Path) -> None:
    """Raise ``ValueError`` if ``path`` contains macros.

    Args:
        path: Uploaded document to inspect.

    Raises:
        ValueError: If macros are detected.
        FileNotFoundError: If ``path`` does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(str(path))
    if path.suffix.lower() in {".docm", ".dotm"}:
        raise ValueError("Macro-enabled documents are not allowed")
    with path.open("rb") as f:
        chunk = f.read(4096).lower()
        for pattern in MACRO_PATTERNS:
            if pattern in chunk:
                raise ValueError("Macro-enabled documents are not allowed")


def cleanup_uploads(*paths: Path) -> None:
    """Delete uploaded files.

    Args:
        *paths: Files to remove.
    """
    for p in paths:
        try:
            p.unlink()
        except FileNotFoundError:
            pass
