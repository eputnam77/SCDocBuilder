"""Benchmark utilities for measuring processing speed."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter


def benchmark_processing(template: Path, worksheet: Path) -> float:
    """Return time in seconds to process a worksheet.

    Args:
        template: Path to the template file.
        worksheet: Path to the worksheet file.

    Returns:
        Time in seconds for loading both files.
    """
    from .io import load_document

    start = perf_counter()
    load_document(template)
    load_document(worksheet)
    end = perf_counter()
    return end - start
