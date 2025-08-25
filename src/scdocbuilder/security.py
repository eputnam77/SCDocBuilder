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

    max_len = max(len(p) for p in MACRO_PATTERNS)
    with path.open("rb") as f:
        tail = b""
        for chunk in iter(lambda: f.read(4096), b""):
            data = (tail + chunk).lower()
            for pattern in MACRO_PATTERNS:
                if pattern in data:
                    raise ValueError("Macro-enabled documents are not allowed")
            tail = data[-(max_len - 1) :]


def cleanup_uploads(*paths: Path) -> None:
    """Delete uploaded files.

    Args:
        *paths: Files to remove.
    """
    for p in paths:
        try:
            p.unlink()
        except (FileNotFoundError, IsADirectoryError, PermissionError):
            # Ignore missing files, directories, or permission issues to make
            # cleanup idempotent and resilient on platforms with restrictive
            # permissions.
            pass
