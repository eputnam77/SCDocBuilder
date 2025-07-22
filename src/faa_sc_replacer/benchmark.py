"""Benchmark utilities for measuring processing speed."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter


def benchmark_processing(template: Path, worksheet: Path) -> float:
    """Return time in seconds to fill template using ``worksheet``."""
    start = perf_counter()
    # TODO: run fill_template and measure elapsed time
    raise NotImplementedError
    end = perf_counter()
    return end - start
