"""Benchmark utilities for measuring processing speed."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter


def benchmark_processing(template: Path, worksheet: Path) -> float:
    """Return time in seconds to fill template using ``worksheet``."""
    from .io import load_document

    start = perf_counter()
    load_document(template)
    load_document(worksheet)
    end = perf_counter()
    return end - start
