"""Security utilities for uploads."""

from __future__ import annotations

from pathlib import Path

MACRO_PATTERNS = [b"vbaProject", b"macros"]


def reject_macros(path: Path) -> None:
    """Raise an error if ``path`` contains macros."""
    if path.suffix.lower() == ".docm":
        raise ValueError("Macro-enabled documents are not allowed")
    try:
        with path.open("rb") as f:
            chunk = f.read(4096)
            for pattern in MACRO_PATTERNS:
                if pattern in chunk:
                    raise ValueError("Macro-enabled documents are not allowed")
    except FileNotFoundError:
        raise


def cleanup_uploads(*paths: Path) -> None:
    """Delete uploaded files."""
    for p in paths:
        try:
            p.unlink()
        except FileNotFoundError:
            pass
