"""Security utilities for uploads."""

from __future__ import annotations

from pathlib import Path


def reject_macros(path: Path) -> None:
    """Raise an error if ``path`` contains macros."""
    # TODO: inspect the file for macros (e.g., .docm) and raise ValueError
    raise NotImplementedError


def cleanup_uploads(*paths: Path) -> None:
    """Delete uploaded files."""
    # TODO: remove files from disk after processing
    raise NotImplementedError
